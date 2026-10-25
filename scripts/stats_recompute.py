# -*- coding: utf-8 -*-
"""统计复算（stats_recompute）— 审稿工作流 R4 机械化。

从证据产物 JSON 中识别三类统计记录，独立重算并与论文声明对照（审稿人自己的算术）：
  1. McNemar exact：{"b": x, "d": y, ...} → p = 2·Σ_{i≤min(b,d)} C(b+d,i)·0.5^(b+d)
  2. Friedman：    ratings 矩阵（N 任务 × k 模型）→ chi2；或 {"chi2": c, "df": d} → p 复核
  3. Wilson CI：   {"k": 成功数, "n": 总数} → 95% CI

判定：
  - 产物内存储的 p/chi2 与重算不符 → MISMATCH（Critical：统计错误或产物造假）
  - 重算值在论文中找不到（含舍入变体）→ NOT_IN_PAPER（Major：论文数字无来源）
  - 一致 → MATCH

用法:
    python stats_recompute.py --tex <main.tex> --evidence-dirs <dir1,dir2> --out <outdir>
    python stats_recompute.py --selftest
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from scipy.stats import chi2 as chi2_dist

SCRIPTS_DIR = Path(__file__).resolve().parent
KIT_DIR = SCRIPTS_DIR.parents[1]          # research-kit 根（adversarial_review 所在）
sys.path.insert(0, str(KIT_DIR))

TOL = 5e-4
NUM_RE = re.compile(r"\d+\.\d+")
KEY_HINTS = {
    "mcnemar": ("mcnemar", "b", "d"),
    "friedman": ("friedman", "chi2"),
    "wilson": ("wilson",),
}

# ---- R4 统计定性自动化：口径换算机械层 + LLM 对抗裁决层 ----
# 阈值形式：LaTeX 数学定界符（p$<$0.05）与纯文本（p<0.05）都覆盖
THRESHOLD_RE = re.compile(r"\bp\s*\$?\s*[<≤]\s*\$?\s*(\d+(?:\.\d+)?)")
PERCENT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*\\?%")
NS_RE = re.compile(r"\b(?:n\.?\s*s\.?|not\s+significant)\b", re.I)
STAR_RE = re.compile(r"(?<!\\)\*{1,3}(?!\*)")
INPUT_RE = re.compile(r"\\(?:input|include)\{([^{}]+)\}")
VERDICTS = ("口径换算", "遗漏", "疑似矛盾", "噪音")
RESOLVED_VERDICTS = ("口径换算", "噪音")   # 机械层/LLM 判定为已解释 → 不构成门禁
SUSTAINED_VERDICTS = ("遗漏", "疑似矛盾")  # 维持 Major（文本层 WARN，不 FAIL）


def num_variants(n: float) -> list[str]:
    out = {repr(n)}
    for d in (3, 4, 5, 6):
        out.add(f"{n:.{d}f}")
    s = f"{n:.10f}".rstrip("0").rstrip(".")
    out.add(s)
    return list(out)


def mcnemar_exact_p(b: int, d: int) -> float:
    n = b + d
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, i) for i in range(0, min(b, d) + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def wilson_ci(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return 0.0, 1.0
    z2 = z * z
    center = (k + z2 / 2) / (n + z2)
    half = z * math.sqrt(k * (n - k) / n + z2 / 4) / (n + z2)
    return center - half, center + half


def friedman_chi2(ratings: list[list[float]]) -> tuple[float, int]:
    """ratings: N 任务 × k 模型得分。返回 (chi2, df=k-1)。平均秩处理并列。"""
    n, k = len(ratings), len(ratings[0])
    rank_sums = [0.0] * k
    for row in ratings:
        order = sorted(range(k), key=lambda j: row[j])
        ranks = [0.0] * k
        i = 0
        while i < k:
            j = i
            while j + 1 < k and row[order[j + 1]] == row[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for t in range(i, j + 1):
                ranks[order[t]] = avg
            i = j + 1
        for m, r in enumerate(ranks):
            rank_sums[m] += r
    chi2 = 12 / (n * k * (k + 1)) * sum(r ** 2 for r in rank_sums) - 3 * n * (k + 1)
    return chi2, k - 1


def find_in_tex(value: float, tex_numbers: list[tuple[str, float]]) -> str | None:
    for tok, t in tex_numbers:
        if abs(t - value) <= TOL:
            return tok
    return None


# ---------------------------------------------------------------- R4 定性：口径换算机械层

def strip_comments(tex: str) -> str:
    return "\n".join(l for l in tex.splitlines() if not l.strip().startswith("%"))


def collect_input_bodies(tex: str, tex_path: Path) -> str:
    """把 \\input/\\include 的 .tex 文件正文并入，使表格文件中的数值也能被匹配。"""
    tex_dir = tex_path.parent
    bodies = [tex]
    for m in INPUT_RE.finditer(tex):
        name = m.group(1).strip()
        if not name.endswith(".tex"):
            name += ".tex"
        f = tex_dir / name
        if f.is_file():
            try:
                bodies.append(f.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                continue
    return "\n".join(bodies)


def mechanical_caliber(tex_body: str, value: float) -> list[str]:
    """口径换算机械层：返回命中的候选（低置信，需 LLM 复核是否对应本统计量）。

    覆盖：阈值形式（p<0.05）、百分数（4.2%）、粗精度舍入（0.04）、n.s. 标记、显著性星号。
    粗精度舍入按独立小数 token 匹配（避免 "0.0" 命中 "0.05" 的子串误报）。
    """
    hits = []
    for m in THRESHOLD_RE.finditer(tex_body):
        try:
            th = float(m.group(1))
        except ValueError:
            continue
        if value < th:
            hits.append(f"阈值形式 p<{th:g}")
            break
    for m in PERCENT_RE.finditer(tex_body):
        try:
            pct = float(m.group(1))
        except ValueError:
            continue
        if abs(pct - value * 100) <= 5e-2:
            hits.append(f"百分数 {pct:g}%")
            break
    # 粗精度舍入：2 位小数（1 位太弱，0.042→0.0 无判别力）
    rv2 = round(value, 2)
    if any(abs(float(t) - rv2) <= 1e-9 for t in NUM_RE.findall(tex_body)):
        hits.append(f"粗精度舍入 {rv2:.2f}")
    if value >= 0.05 and NS_RE.search(tex_body):
        hits.append("n.s./not significant 标记")
    if STAR_RE.search(tex_body):
        hits.append("显著性星号标记")
    return hits


def primary_value(check: dict) -> float | None:
    """取该条统计记录用于口径换算/LLM 裁决的主数值（p 优先，其次 chi2/CI 端点）。"""
    for key in ("recomputed", "recomputed_p", "recomputed_chi2"):
        v = check.get(key)
        if isinstance(v, (int, float)):
            return float(v)
    ci = check.get("recomputed_ci")
    if isinstance(ci, list) and ci and isinstance(ci[0], (int, float)):
        return float(ci[0])
    return None


def describe_value(check: dict) -> str:
    if check["kind"] == "mcnemar":
        return f"p={check.get('recomputed')} (b={check.get('b')},d={check.get('d')})"
    if check["kind"] == "friedman_p":
        return f"p={check.get('recomputed_p')} (chi2={check.get('chi2')},df={check.get('df')})"
    if check["kind"] == "friedman_raw":
        return (f"chi2={check.get('recomputed_chi2')},p={check.get('recomputed_p')} "
                f"(df={check.get('df')})")
    if check["kind"] == "wilson":
        return f"CI=[{check.get('recomputed_ci')}] (k={check.get('k')},n={check.get('n')})"
    return str(check)


def extract_context(tex_body: str, check: dict, max_chars: int = 3000) -> str:
    """提取与统计量相关的论文上下文：按 json_path 词元 + 复算值 + 统计关键词定位句子。"""
    tokens = [t for t in re.split(r"[^A-Za-z0-9]+", check["json_path"]) if t and not t.isdigit()]
    value_strs = []
    for key in ("recomputed", "recomputed_p", "recomputed_chi2"):
        v = check.get(key)
        if isinstance(v, (int, float)):
            value_strs.append(f"{v:.4f}".rstrip("0").rstrip("."))
    keywords = tokens + value_strs + ["sensitivity", "friedman", "chi2", "mcnemar", "wilson"]
    lines = tex_body.splitlines()
    hits = []
    for i, ln in enumerate(lines):
        low = ln.lower()
        if any(k.lower() in low for k in keywords if k):
            hits.append(i)
    if not hits:
        return tex_body[:max_chars] + "\n…(截断)"
    idx = set()
    for i in hits:
        for j in range(max(0, i - 2), min(len(lines), i + 3)):
            idx.add(j)
    ctx = "\n".join(lines[i] for i in sorted(idx))
    if len(ctx) > max_chars:
        ctx = ctx[:max_chars] + "\n…(截断)"
    return ctx


def build_adjudicate_prompt(check: dict, paper_context: str, mechanical_hits: list[str]) -> str:
    claimed = check.get("claimed_p") or check.get("claimed_chi2") or check.get("claimed")
    return (
        "你是统计审稿人（对抗裁决）。论文中有一个统计量能在产物 JSON 中独立复算，"
        "但论文正文/表格中找不到该数值。请裁决该统计量在论文中的呈现方式。\n\n"
        "【重要】不要使用任何工具、不要执行任何命令、不要读取或搜索文件系统——"
        "所有需要的信息都已在下文提供，直接根据上下文裁决并输出 JSON。\n\n"
        f"统计量信息：\n- 类型：{check['kind']}\n- 产物来源：{Path(check['source']).name}\n"
        f"- JSON 路径：{check['json_path']}\n- 复算值：{describe_value(check)}\n"
        f"- 产物存储值：{claimed if claimed is not None else '-'}\n"
        f"- 机械层命中的口径换算候选：{mechanical_hits or '无'}\n\n"
        "论文相关上下文：\n" + paper_context + "\n\n"
        "裁决要求（对抗性，必须怀疑）：\n"
        "1. 机械层候选可能对应论文中其他检验，逐条核对是否真的对应本统计量\n"
        "2. 在论文中搜索本统计量是否以其他形式出现（不同精度/百分数/阈值/表格/附录）\n"
        "3. evidence 必须引用论文原文句子（<=80字），不许编造\n"
        "4. 论文确实报告了本统计量（任何形式）→ verdict=口径换算\n"
        "5. 论文完全没有报告 → verdict=遗漏\n"
        "6. 论文报告了冲突的值 → verdict=疑似矛盾\n"
        "7. 这是无需报告的统计量（模拟/内部中间量/与论文无关）→ verdict=噪音\n\n"
        "输出严格 JSON（不要 markdown 代码块、不要多余文字）：\n"
        '{"verdict": "口径换算|遗漏|疑似矛盾|噪音", "confidence": "high|medium|low", '
        '"justification": "<=120字", "evidence": "<=80字 论文原句", "suggested_action": "<=60字"}'
    )


def _repair_json_quotes(text: str) -> str:
    """修复 LLM 常见错误：字符串值内未转义的双引号（如 "simulated_k4_N12"）。

    状态机区分 key/value：'{' 或 ',' 后的引号是 key 开头，':' 后的引号是 value 开头。
    key 的结束引号无条件闭合；value 内的引号仅当下一个非空白字符是 , ] } 或结尾时闭合，
    否则视为字符串内容 → 转义为 \\"。
    """
    out = []
    in_str = False
    is_key = False          # 当前字符串是否为 key
    expect_value = False    # 刚遇到 ':'，下一个 " 是 value 开头
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch == '"':
            if not in_str:
                out.append(ch)
                in_str = True
                is_key = not expect_value
                expect_value = False
            elif is_key:
                out.append(ch)
                in_str = False
            else:
                j = i + 1
                while j < n and text[j] in " \t\r\n":
                    j += 1
                nxt = text[j] if j < n else ""
                if nxt in ",}]" or j >= n:
                    out.append(ch)
                    in_str = False
                else:
                    out.append('\\"')
        elif ch == ":" and not in_str:
            out.append(ch)
            expect_value = True
        elif ch in "{," and not in_str:
            out.append(ch)
            expect_value = False
        elif ch == "\\" and in_str and i + 1 < n:
            out.append(ch)
            out.append(text[i + 1])
            i += 1
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def parse_verdict(raw: str) -> dict | None:
    """容错解析裁决输出：直接 JSON / 代码块包裹 / 引号修复 / 正则兜底。"""
    if not raw:
        return None
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if fence:
        text = fence.group(1)
    m = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text, re.S)
    if m:
        obj = None
        for cand in (m.group(0), _repair_json_quotes(m.group(0))):
            try:
                obj = json.loads(cand.replace("：", ":").replace("，", ","))
                break
            except (json.JSONDecodeError, ValueError):
                continue
        if obj is not None:
            verdict = obj.get("verdict")
            if verdict in VERDICTS:
                return {
                    "verdict": verdict,
                    "confidence": str(obj.get("confidence", "low"))[:16],
                    "justification": str(obj.get("justification", ""))[:300],
                    "evidence": str(obj.get("evidence", ""))[:200],
                    "suggested_action": str(obj.get("suggested_action", ""))[:200],
                    "parse": "json",
                }
    vm = re.search(r"(?:verdict|裁决)\s*[:：]?\s*[\"']?(" + "|".join(VERDICTS) + r")", text)
    if vm:
        return {"verdict": vm.group(1), "confidence": "low", "justification": raw[:200],
                "evidence": "", "suggested_action": "", "parse": "regex"}
    return None


def adjudicate_qualitative(report: dict, tex_path: Path, rpc_url: str = "http://127.0.0.1:3080",
                           timeout: int = 300, max_llm: int = 20) -> dict:
    """R4 统计定性自动化：口径换算机械层 + LLM 对抗裁决层。

    对 recompute 输出的 MISMATCH / NOT_IN_PAPER 条目逐条裁决：
      - 机械层先给口径换算候选（阈值/百分数/粗精度舍入/n.s./星号）
      - LLM 对抗 judge 复核候选并裁决：口径换算/遗漏/疑似矛盾/噪音
      - RPC 不可达 → SKIP（不阻塞机械审查，门禁维持 recompute 原判）
    """
    import urllib.error
    import urllib.request

    tex = tex_path.read_text(encoding="utf-8", errors="replace")
    body = collect_input_bodies(strip_comments(tex), tex_path)

    out = {
        "meta": {"tex": str(tex_path), "rpc": rpc_url,
                 "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")},
        "adjudications": [],
        "summary": {"total": 0, "resolved": 0, "sustained": 0, "llm_failed": 0,
                    "verdict": None, "detail": ""},
    }

    targets = [c for c in report["checks"] if c["status"] in ("MISMATCH", "NOT_IN_PAPER")]
    if not targets:
        out["summary"]["verdict"] = "PASS"
        out["summary"]["detail"] = "无 MISMATCH/NOT_IN_PAPER 条目，无需定性"
        return out

    # RPC 健康检查
    try:
        with urllib.request.urlopen(rpc_url.rstrip("/"), timeout=4) as r:
            health = f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        health = f"HTTP {e.code}（服务在监听）"
    except Exception as e:  # noqa: BLE001
        out["meta"]["rpc_health"] = f"不可达（{type(e).__name__}）"
        out["summary"]["verdict"] = "SKIP"
        out["summary"]["detail"] = "RPC 不可达 → LLM 裁决跳过，门禁维持 recompute 原判（MISMATCH=FAIL / NOT_IN_PAPER=WARN）"
        return out
    out["meta"]["rpc_health"] = health

    import adversarial_review as adv
    adv.RPC = rpc_url

    for c in targets[:max_llm]:
        val = primary_value(c)
        mech = mechanical_caliber(body, val) if val is not None else []
        entry = {
            "kind": c["kind"], "json_path": c["json_path"], "source": c["source"],
            "status": c["status"], "mechanical_hits": mech,
            "layer": "llm", "verdict": None, "confidence": None,
            "justification": None, "evidence": None, "suggested_action": None,
        }
        ctx = extract_context(body, c)
        rec = adv.prompt_turn(build_adjudicate_prompt(c, ctx, mech), "r4-adjudicate", timeout=timeout)
        if rec["status"] != "ok":
            entry["llm_status"] = rec["status"]
            entry["verdict"] = "未裁决"
            out["summary"]["llm_failed"] += 1
            out["adjudications"].append(entry)
            continue
        parsed = parse_verdict(rec["raw"])
        if parsed:
            entry.update(parsed)
            entry["layer"] = "llm"
        else:
            entry["llm_status"] = "parse_failed"
            entry["raw_head"] = rec["raw"][:300]
            entry["verdict"] = "未裁决"
            out["summary"]["llm_failed"] += 1
        out["adjudications"].append(entry)

    n_resolved = sum(1 for a in out["adjudications"] if a.get("verdict") in RESOLVED_VERDICTS)
    n_sustained = sum(1 for a in out["adjudications"] if a.get("verdict") in SUSTAINED_VERDICTS)
    n_unadjudicated = sum(1 for a in out["adjudications"] if a.get("verdict") in ("未裁决", None))
    out["summary"]["total"] = len(out["adjudications"])
    out["summary"]["resolved"] = n_resolved
    out["summary"]["sustained"] = n_sustained

    # 门禁合成：机械 MISMATCH 仍 FAIL；LLM 只影响 NOT_IN_PAPER 的 WARN→PASS；
    # 未裁决（LLM 超时/解析失败）→ 维持 recompute 原判（NOT_IN_PAPER=Major），绝不虚报 PASS
    n_mismatch = sum(1 for a in out["adjudications"] if a["status"] == "MISMATCH")
    n_notin_sustained = sum(1 for a in out["adjudications"]
                            if a["status"] == "NOT_IN_PAPER" and a.get("verdict") in SUSTAINED_VERDICTS)
    n_notin_total = sum(1 for a in out["adjudications"] if a["status"] == "NOT_IN_PAPER")
    if n_mismatch:
        out["summary"]["verdict"] = "CRITICAL"
        out["summary"]["detail"] = (f"MISMATCH {n_mismatch} 条为机械 Critical（统计错误/产物造假），"
                                    f"LLM 定性不改变 FAIL 门禁")
    elif n_notin_sustained:
        out["summary"]["verdict"] = "MAJOR"
        out["summary"]["detail"] = (f"NOT_IN_PAPER {n_notin_total} 条中 {n_notin_sustained} 条维持 Major"
                                    f"（遗漏/疑似矛盾）；{n_resolved} 条已定性为口径换算/噪音")
    elif n_unadjudicated:
        out["summary"]["verdict"] = "MAJOR"
        out["summary"]["detail"] = (f"NOT_IN_PAPER {n_notin_total} 条中 {n_unadjudicated} 条 LLM 未裁决"
                                    f"（llm_failed {out['summary']['llm_failed']}）→ 维持 recompute 原判 Major；"
                                    f"{n_resolved} 条已定性为口径换算/噪音")
    elif n_notin_total:
        out["summary"]["verdict"] = "PASS"
        out["summary"]["detail"] = f"NOT_IN_PAPER {n_notin_total} 条全部定性为口径换算/噪音 → 已解释"
    else:
        out["summary"]["verdict"] = "PASS"
        out["summary"]["detail"] = "无 MISMATCH/NOT_IN_PAPER 条目"
    return out


def write_qual_md(qual: dict, out_md: Path) -> None:
    s = qual["summary"]
    lines = [
        "# 统计定性报告（R4 自动化：口径换算机械层 + LLM 对抗裁决）",
        "",
        f"- 论文：`{qual['meta']['tex']}`；RPC：{qual['meta'].get('rpc_health', '-')}",
        f"- 结论：**{s.get('verdict')}** —— {s.get('detail', '')}",
        "",
        "| 类型 | json_path | 状态 | 机械候选 | 裁决 | 置信 | 依据 | 建议 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for a in qual["adjudications"]:
        lines.append(f"| {a['kind']} | `{a['json_path']}` | **{a['status']}** | "
                     f"{'；'.join(a['mechanical_hits']) or '-'} | {a.get('verdict') or '-'} | "
                     f"{a.get('confidence') or '-'} | {(a.get('evidence') or '')[:60]} | "
                     f"{(a.get('suggested_action') or '')[:60]} |")
    lines += ["", "- 裁决语义：口径换算/噪音=已解释（不构成门禁）；遗漏/疑似矛盾=维持 Major（文本层 WARN，不 FAIL）；MISMATCH 恒为机械 Critical"]
    out_md.write_text("\n".join(lines), encoding="utf-8")


def iter_records(obj, path=""):
    """产出 (path, dict) —— 任意深度下的 dict 节点。"""
    if isinstance(obj, dict):
        yield path, obj
        for k, v in obj.items():
            yield from iter_records(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:200]):
            yield from iter_records(v, f"{path}[{i}]")


def looks_like_int(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and float(v).is_integer() and v >= 0


def scan_records(data, source: str) -> list[dict]:
    out = []
    for path, rec in iter_records(data):
        keys = {k.lower() for k in rec}
        keys_raw = set(rec.keys())
        # 提示词来源：本层 key 或父级 path（如 {"mcnemar_pair": {"b":1,"d":9}}）
        hint = " ".join([path.lower()] + list(keys))
        # McNemar：整数 b/c 计数（标准约定：discordant = b+c，a/d 为 concordant；
        # 产物如 {"a":19,"b":0,"c":11,"d":0,"n_discordant":11}）。旧产物若只存
        # {b,d}（无 c）则回退按 b/d——2026-09-05 修：曾误读 b,d 致 6 处假 MISMATCH。
        if "mcnemar" in hint and "b" in keys and ("c" in keys or "d" in keys):
            b = rec.get("b")
            second = rec.get("c") if looks_like_int(rec.get("c")) else rec.get("d")
            if looks_like_int(b) and looks_like_int(second):
                out.append({"kind": "mcnemar", "source": source, "json_path": path, "b": int(b), "d": int(second),
                            "claimed_p": rec.get("p") or rec.get("pvalue") or rec.get("p_value")})
        # Friedman：chi2 + df/k
        if "chi2" in keys or "chi_2" in keys or "χ2" in keys_raw:
            chi2v = rec.get("chi2") or rec.get("chi_2")
            df = rec.get("df")
            k = rec.get("k")
            if isinstance(chi2v, (int, float)) and not isinstance(chi2v, bool):
                out.append({"kind": "friedman_p", "source": source, "json_path": path,
                            "chi2": float(chi2v), "df": int(df) if looks_like_int(df) else (int(k) - 1 if looks_like_int(k) and k >= 2 else None),
                            "claimed_p": rec.get("p") or rec.get("pvalue")})
        # Friedman：ratings 矩阵
        for key in ("ratings", "matrix", "scores_by_task"):
            v = rec.get(key)
            if isinstance(v, list) and len(v) >= 3 and all(
                isinstance(r, list) and len(r) >= 2 and all(isinstance(x, (int, float)) for x in r) for r in v
            ) and len({len(r) for r in v}) == 1 and len(v[0]) >= 2:
                out.append({"kind": "friedman_raw", "source": source, "json_path": f"{path}.{key}", "ratings": v,
                            "claimed_chi2": rec.get("chi2"), "claimed_p": rec.get("p")})
        # Wilson：整数 k/n
        if "wilson" in hint and "k" in keys and "n" in keys:
            k, n = rec.get("k"), rec.get("n")
            if looks_like_int(k) and looks_like_int(n) and 0 < int(n) >= int(k) >= 0:
                out.append({"kind": "wilson", "source": source, "json_path": path,
                            "k": int(k), "n": int(n),
                            "claimed": rec.get("ci") or rec.get("lower") or rec.get("upper")})
    return out


def recompute(tex_path: Path, evidence_dirs: list[Path]) -> dict:
    tex = tex_path.read_text(encoding="utf-8", errors="replace")
    body = collect_input_bodies(strip_comments(tex), tex_path)
    tex_numbers = []
    for m in NUM_RE.finditer(body):
        try:
            tex_numbers.append((m.group(0), float(m.group(0))))
        except ValueError:
            continue

    records, scanned = [], 0
    for d in evidence_dirs:
        if not d.exists():
            continue
        for f in sorted(d.rglob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                continue
            scanned += 1
            records += scan_records(data, str(f))

    checks = []
    for r in records:
        if r["kind"] == "mcnemar":
            p = mcnemar_exact_p(r["b"], r["d"])
            claimed = r["claimed_p"]
            agree_claim = claimed is None or not isinstance(claimed, (int, float)) or abs(float(claimed) - p) <= max(TOL, 5e-3)
            paper_tok = find_in_tex(p, tex_numbers)
            checks.append({**r, "recomputed": round(p, 6), "claimed_vs_recomputed": "OK" if agree_claim else "MISMATCH",
                           "in_paper": paper_tok,
                           "status": "MATCH" if (agree_claim and paper_tok) else ("MISMATCH" if not agree_claim else "NOT_IN_PAPER")})
        elif r["kind"] == "friedman_p":
            df = r["df"]
            if df is None:
                checks.append({**r, "status": "SKIP_NO_DF"})
                continue
            p = float(chi2_dist.sf(r["chi2"], df))
            claimed = r["claimed_p"]
            agree_claim = claimed is None or not isinstance(claimed, (int, float)) or abs(float(claimed) - p) <= max(TOL, 5e-3)
            paper_tok = find_in_tex(p, tex_numbers)
            checks.append({**r, "recomputed_p": round(p, 6), "claimed_vs_recomputed": "OK" if agree_claim else "MISMATCH",
                           "in_paper": paper_tok,
                           "status": "MATCH" if (agree_claim and paper_tok) else ("MISMATCH" if not agree_claim else "NOT_IN_PAPER")})
        elif r["kind"] == "friedman_raw":
            chi2, df = friedman_chi2(r["ratings"])
            p = float(chi2_dist.sf(chi2, df))
            claimed_chi2, claimed_p = r["claimed_chi2"], r["claimed_p"]
            agree = (claimed_chi2 is None or not isinstance(claimed_chi2, (int, float))
                     or abs(float(claimed_chi2) - chi2) <= max(TOL, 5e-2 * max(1.0, abs(chi2))))
            agree_p = claimed_p is None or not isinstance(claimed_p, (int, float)) or abs(float(claimed_p) - p) <= max(TOL, 5e-3)
            tok_chi = find_in_tex(chi2, tex_numbers)
            tok_p = find_in_tex(p, tex_numbers)
            checks.append({**r, "recomputed_chi2": round(chi2, 4), "recomputed_p": round(p, 6), "df": df,
                           "claimed_vs_recomputed": "OK" if (agree and agree_p) else "MISMATCH",
                           "in_paper": tok_p or tok_chi,
                           "status": "MATCH" if ((agree and agree_p) and (tok_p or tok_chi)) else ("MISMATCH" if not (agree and agree_p) else "NOT_IN_PAPER")})
        elif r["kind"] == "wilson":
            lo, hi = wilson_ci(r["k"], r["n"])
            tok_lo, tok_hi = find_in_tex(lo, tex_numbers), find_in_tex(hi, tex_numbers)
            checks.append({**r, "recomputed_ci": [round(lo, 4), round(hi, 4)],
                           "in_paper": tok_lo or tok_hi,
                           "status": "MATCH" if (tok_lo or tok_hi) else "NOT_IN_PAPER"})

    n_match = sum(1 for c in checks if c["status"] == "MATCH")
    n_mismatch = sum(1 for c in checks if c["status"] == "MISMATCH")
    n_notin = sum(1 for c in checks if c["status"] == "NOT_IN_PAPER")
    verdict = "CRITICAL" if n_mismatch else ("MAJOR" if n_notin else ("PASS" if checks else "PASS"))
    return {
        "meta": {"tex": str(tex_path), "evidence_dirs": [str(d) for d in evidence_dirs],
                 "json_scanned": scanned, "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")},
        "checks": checks,
        "summary": {"records": len(records), "match": n_match, "mismatch": n_mismatch,
                    "not_in_paper": n_notin, "verdict": verdict,
                    "note": "MISMATCH=Critical（产物统计值与复算不符）；NOT_IN_PAPER=Major（重算值未出现在论文）；"
                            "口径换算机械层已并入 \\input 表格正文；MISMATCH/NOT_IN_PAPER 的定性由 adjudicate_qualitative 自动裁决"},
    }


def write_md(report: dict, out_md: Path) -> None:
    s = report["summary"]
    lines = [
        "# 统计复算报告（R4 机械化）",
        "",
        f"- 论文：`{report['meta']['tex']}`；扫描 JSON {report['meta']['json_scanned']} 个，识别统计记录 {s['records']} 条",
        f"- 结论：**{s['verdict']}**（MATCH {s['match']}，MISMATCH {s['mismatch']}，NOT_IN_PAPER {s['not_in_paper']}）",
        "",
        "| 类型 | json_path | 重算值 | 产物存储值判定 | 论文出现 | 状态 | 来源 |",
        "|---|---|---|---|---|---|---|",
    ]
    for c in report["checks"]:
        if c["status"] == "SKIP_NO_DF":
            lines.append(f"| {c['kind']} | `{c['json_path']}` | -（无 df，跳过） | - | - | **SKIP_NO_DF** | `{Path(c['source']).name}` |")
            continue
        if c["kind"] == "mcnemar":
            val = f"p={c['recomputed']} (b={c['b']},d={c['d']})"
        elif c["kind"] == "friedman_p":
            val = f"p={c['recomputed_p']} (chi2={c['chi2']},df={c['df']})"
        elif c["kind"] == "friedman_raw":
            val = f"chi2={c['recomputed_chi2']},p={c['recomputed_p']} (df={c['df']})"
        else:
            val = f"CI=[{c['recomputed_ci'][0]},{c['recomputed_ci'][1]}] (k={c['k']},n={c['n']})"
        claim = c.get("claimed_vs_recomputed", "-")
        lines.append(f"| {c['kind']} | `{c['json_path']}` | {val} | {claim} | {c.get('in_paper') or '-'} | **{c['status']}** | `{Path(c['source']).name}` |")
    lines += ["", "- MISMATCH → 逐条人工定性（统计错误 or 产物造假）；NOT_IN_PAPER → 检查论文口径是否换算（如报告的是上界/下界）"]
    out_md.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    import tempfile

    from scipy.stats import binomtest

    tmp = Path(tempfile.mkdtemp())
    # McNemar b=1,d=9 → exact p = 2*11/1024
    p_exact = mcnemar_exact_p(1, 9)
    assert abs(p_exact - 2 * 11 / 1024) < 1e-12, p_exact
    ref = binomtest(1, 10, 0.5).pvalue
    assert abs(p_exact - min(1.0, 2 * ref)) < 1e-9 or abs(p_exact - ref) < 1e-9, (p_exact, ref)
    # 退化：b=d=0 → p=1
    assert mcnemar_exact_p(0, 0) == 1.0
    # Friedman 已知例：3 模型无并列 → chi2 = 12N/(k(k+1)) * (ΣR²-...)；N=6,k=3, 完全分歧排序
    ratings = [[1.0, 2.0, 3.0], [1.0, 3.0, 2.0], [2.0, 1.0, 3.0], [3.0, 1.0, 2.0], [2.0, 3.0, 1.0], [3.0, 2.0, 1.0]]
    chi2, df = friedman_chi2(ratings)
    assert df == 2
    # rank sums 均为 12 → chi2 = 0
    assert abs(chi2) < 1e-9, chi2
    ratings2 = [[1.0, 2.0, 3.0]] * 6  # 完全一致排序 → 最大 chi2=12
    chi2b, _ = friedman_chi2(ratings2)
    assert abs(chi2b - 12.0) < 1e-9, chi2b
    # Wilson k=8,n=10
    lo, hi = wilson_ci(8, 10)
    assert 0.44 < lo < 0.55 and 0.93 < hi < 0.96, (lo, hi)

    ev = tmp / "ev"
    ev.mkdir()
    (ev / "stats.json").write_text(json.dumps({
        "mcnemar_pair": {"b": 1, "d": 9, "p": round(p_exact, 4), "test": "mcnemar"},
        "wilson_gold": {"k": 8, "n": 10, "ci": [round(lo, 4), round(hi, 4)], "method": "wilson"},
        "friedman_pair": {"chi2": 6.0, "df": 2, "p": 0.0498, "test": "friedman"},
    }), encoding="utf-8")
    tex = tmp / "main.tex"
    p_s = f"{p_exact:.4f}"
    tex.write_text(
        f"Exact McNemar gives $p={p_s}$ ($b=1$, $d=9$).\n"
        f"Wilson CI $[{lo:.4f}, {hi:.4f}]$ for 8/10.\n"
        f"Friedman $\\chi^2=6.0$, $p=0.0498$.\n"
        "Bad claim p=0.9999 nowhere.\n",
        encoding="utf-8",
    )
    rep = recompute(tex, [ev])
    kinds = {c["kind"]: c for c in rep["checks"]}
    assert kinds["mcnemar"]["status"] == "MATCH", kinds
    assert kinds["wilson"]["status"] == "MATCH", kinds
    assert kinds["friedman_p"]["status"] == "MATCH", kinds
    assert rep["summary"]["verdict"] == "PASS", rep["summary"]

    # 造假场景：产物声称 p 与重算不符 → CRITICAL
    (ev / "stats.json").write_text(json.dumps({
        "mcnemar_pair": {"b": 1, "d": 9, "p": 0.5, "test": "mcnemar"},
    }), encoding="utf-8")
    rep2 = recompute(tex, [ev])
    assert rep2["summary"]["mismatch"] >= 1 and rep2["summary"]["verdict"] == "CRITICAL", rep2["summary"]

    # ---- R4 定性自动化：口径换算机械层 ------------------------------------
    # 阈值形式（LaTeX 数学定界符 p$<$0.05）与百分数
    assert mechanical_caliber("p$<$0.05 and p<0.01", 0.042) == ["阈值形式 p<0.05"], mechanical_caliber("p$<$0.05", 0.042)
    assert mechanical_caliber("accuracy 4.2\\% vs 3.1\\%", 0.042) == ["百分数 4.2%"], mechanical_caliber("4.2\\%", 0.042)
    # 粗精度舍入
    assert mechanical_caliber("cost is 0.04 per task", 0.042054) == ["粗精度舍入 0.04"], mechanical_caliber("0.04", 0.042054)
    # n.s. 标记（p>=0.05 才触发）
    assert "n.s./not significant 标记" in mechanical_caliber("result is n.s. here", 0.3)
    assert "n.s./not significant 标记" not in mechanical_caliber("result is n.s. here", 0.03)
    # 无命中
    assert mechanical_caliber("nothing relevant", 0.1234) == []

    # ---- R4 定性自动化：\input 表格正文并入 → 表格中的数值算 MATCH ----------
    (ev / "stats.json").write_text(json.dumps({
        "friedman_pair": {"chi2": 6.0, "df": 2, "p": 0.0498, "test": "friedman"},
    }), encoding="utf-8")
    tbl = tmp / "tbl_sens.tex"
    tbl.write_text("Sensitivity chi2=8.2 p=0.0498 (simulated k4 N12).\n", encoding="utf-8")
    tex2 = tmp / "main2.tex"
    tex2.write_text("Main text no stats.\n\\input{tbl_sens}\n", encoding="utf-8")
    rep3 = recompute(tex2, [ev])
    assert rep3["summary"]["match"] == 1, rep3["summary"]  # 0.0498 在 \input 表格中找到

    # ---- R4 定性自动化：NOT_IN_PAPER + 机械候选（阈值形式）→ mock LLM 全链路 ----
    (ev / "stats.json").write_text(json.dumps({
        "friedman_pair": {"chi2": 8.87, "df": 3, "p": 0.031, "test": "friedman"},
    }), encoding="utf-8")
    tbl2 = tmp / "tbl_sens2.tex"
    tbl2.write_text("Sensitivity chi2=8.2 p=0.0421 (simulated k4 N12) yields p$<$0.05.\n", encoding="utf-8")
    tex3 = tmp / "main3.tex"
    tex3.write_text("Main text no stats.\n\\input{tbl_sens2}\n", encoding="utf-8")
    rep4 = recompute(tex3, [ev])
    assert rep4["summary"]["not_in_paper"] == 1, rep4["summary"]

    # ---- R4 定性自动化：LLM 裁决解析 ---------------------------------------
    r = parse_verdict('{"verdict": "口径换算", "confidence": "high", "justification": "论文以阈值形式报告", "evidence": "p<0.05"}')
    assert r and r["verdict"] == "口径换算" and r["confidence"] == "high", r
    r = parse_verdict('```json\n{"verdict": "遗漏", "confidence": "medium", "justification": "j"}\n```')
    assert r and r["verdict"] == "遗漏", r
    r = parse_verdict('裁决：疑似矛盾，论文报告了冲突值')
    assert r and r["verdict"] == "疑似矛盾" and r["parse"] == "regex", r
    assert parse_verdict("no verdict here") is None

    # ---- R4 定性自动化：mock LLM 全链路（门禁合成） ------------------------
    import urllib.request
    import adversarial_review as adv
    calls = {"n": 0}

    class _FakeResp:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_prompt(text, role_key, timeout=300):
        calls["n"] += 1
        if "simulated" in text:
            return {"role": role_key, "status": "ok", "issues": {}, "raw":
                    '{"verdict": "疑似矛盾", "confidence": "medium", "justification": "论文报告敏感性 p=0.0498/0.3679/0.074，未含 0.042", "evidence": "sensitivity shows p=0.0498/0.3679/0.074", "suggested_action": "核对产物 note 声称 consistent with curated 是否成立"}'}
        return {"role": role_key, "status": "ok", "issues": {}, "raw":
                '{"verdict": "口径换算", "confidence": "high", "justification": "论文以阈值形式报告", "evidence": "p<0.05", "suggested_action": "无需处理"}'}

    orig_urlopen, orig_prompt = urllib.request.urlopen, adv.prompt_turn
    urllib.request.urlopen = lambda *a, **k: _FakeResp()
    adv.prompt_turn = fake_prompt
    try:
        qual = adjudicate_qualitative(rep4, tex3, rpc_url="http://127.0.0.1:3080")
    finally:
        urllib.request.urlopen, adv.prompt_turn = orig_urlopen, orig_prompt
    assert qual["summary"]["total"] >= 1, qual["summary"]
    # 有 NOT_IN_PAPER 且 LLM 判为疑似矛盾 → MAJOR（文本层 WARN，不 FAIL）
    assert qual["summary"]["verdict"] == "MAJOR", qual["summary"]
    assert qual["summary"]["sustained"] >= 1, qual["summary"]
    # 机械候选应传入 LLM（阈值形式 p<0.05）
    assert any(a["mechanical_hits"] for a in qual["adjudications"]), qual["adjudications"]

    # RPC 不可达 → SKIP，不阻塞
    qual_skip = adjudicate_qualitative(rep4, tex3, rpc_url="http://127.0.0.1:1")
    assert qual_skip["summary"]["verdict"] == "SKIP", qual_skip["summary"]

    # LLM 超时/失败 → 未裁决 → 维持 recompute 原判 MAJOR，绝不虚报 PASS
    def fake_timeout(text, role_key, timeout=300):
        return {"role": role_key, "status": "timeout", "issues": {}, "raw": ""}

    orig_urlopen2, orig_prompt2 = urllib.request.urlopen, adv.prompt_turn
    urllib.request.urlopen = lambda *a, **k: _FakeResp()
    adv.prompt_turn = fake_timeout
    try:
        qual_timeout = adjudicate_qualitative(rep4, tex3, rpc_url="http://127.0.0.1:3080")
    finally:
        urllib.request.urlopen, adv.prompt_turn = orig_urlopen2, orig_prompt2
    assert qual_timeout["summary"]["llm_failed"] >= 1, qual_timeout["summary"]
    assert qual_timeout["summary"]["verdict"] == "MAJOR", qual_timeout["summary"]
    assert all(a["verdict"] == "未裁决" for a in qual_timeout["adjudications"]), qual_timeout["adjudications"]

    # 无 MISMATCH/NOT_IN_PAPER → PASS
    qual_pass = adjudicate_qualitative(rep, tex, rpc_url="http://127.0.0.1:1")
    assert qual_pass["summary"]["verdict"] == "PASS", qual_pass["summary"]

    print("stats_recompute selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tex", type=Path)
    ap.add_argument("--evidence-dirs", type=str)
    ap.add_argument("--out", type=Path, default=Path("audit_out"))
    ap.add_argument("--qualitative", action="store_true",
                    help="R4 统计定性自动化：口径换算机械层 + LLM 对抗裁决层")
    ap.add_argument("--rpc", default="http://127.0.0.1:3080")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not (args.tex and args.evidence_dirs):
        ap.error("--tex and --evidence-dirs are required (or --selftest)")
    dirs = [Path(p) for p in args.evidence_dirs.split(",") if p.strip()]
    rep = recompute(args.tex, dirs)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "stats_recompute.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(rep, args.out / "stats_recompute.md")
    s = rep["summary"]
    print(f"verdict={s['verdict']} records={s['records']} match={s['match']} mismatch={s['mismatch']} not_in_paper={s['not_in_paper']}")
    print(f"-> {args.out / 'stats_recompute.md'}")
    if args.qualitative and (s["mismatch"] or s["not_in_paper"]):
        qual = adjudicate_qualitative(rep, args.tex, rpc_url=args.rpc)
        (args.out / "stats_adjudications.json").write_text(
            json.dumps(qual, ensure_ascii=False, indent=2), encoding="utf-8")
        write_qual_md(qual, args.out / "stats_adjudications.md")
        q = qual["summary"]
        print(f"qualitative={q['verdict']} total={q['total']} resolved={q['resolved']} sustained={q['sustained']} llm_failed={q['llm_failed']}")
        print(f"-> {args.out / 'stats_adjudications.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
