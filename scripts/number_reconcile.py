# -*- coding: utf-8 -*-
"""数字对账（number_reconcile）— 审稿工作流 R3。

两个方向核验论文数字与产物 JSON 的一致性：
  A. 产物 → 论文：产物中的统计数字是否在论文中以一致值出现（论文没改数字）
  B. 论文 → 产物：论文中的小数是否能在产物中找到支撑（无支撑 → 人工复核清单）

B 方向三层降噪（裁决闭环）：
  1. 机械噪音过滤：版本号 x.y.z 片段、日期、结构命令行（\\ref/\\cite/\\section…）自动归为 noise
  2. 人工裁决持久化：--adjudications adjudications.json 逐 token 记录
     verdict = noise | supported | critical | pending；已裁决 token 不再进人工复核清单
  3. 裁决文件自动扩容：新出现的无支撑 token 以 pending 写回，人工补判后重跑 → 清单调收敛

匹配容差 0.0005（覆盖 0.14175 → 0.1418 的四舍五入）。

用法:
    python number_reconcile.py --tex main.tex --evidence-dirs results,out_p5 --out audit_out \
        [--adjudications adjudications.json]
    python number_reconcile.py --selftest
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
KIT_DIR = SCRIPTS_DIR.parents[1]          # F:\deepseek\research-kit（adversarial_review 所在）
sys.path.insert(0, str(KIT_DIR))

TOL = 5e-4
DEC_RE = re.compile(r"\d+\.\d+")
SKIP_KEYS = ("timestamp", "seed", "version", "sha256", "hash", "index", "token", "cost_usd")
# 2026-09-06: "line"/"id" 改整段匹配（子串会误杀 cost_baseline/valid/grid 等；"line" 仍跳过行号键）
SKIP_KEY_PARTS = ("line", "lines", "id")
SKIP_KEY_PART_RE = re.compile(r"[_\-./]")

DATE_TOKEN_RE = re.compile(r"^(19|20)\d{2}\.\d+$")
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
ARXIV_ID_RE = re.compile(r"^\d{4}\.\d{4,5}(v\d+)?$")   # 1306.5151 / 1710.06924v2
# 结构命令整体形态（含花括号参数）：数字只有落在这些花括号内才算噪音，同行不算
STRUCTURAL_CMD_RE = re.compile(
    r"\\(?:sub)*section\{[^{}]*\}"
    r"|\\(?:ref|label|cite|citep|citet|citealp|url|href|usepackage|documentclass|"
    r"bibliography|bibliographystyle|graphicspath|includegraphics|autoref|vref|eqref|cref)\{[^{}]*\}"
)


def flatten(obj, prefix="", out=None):
    if out is None:
        out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            kl = k.lower()
            if any(s in kl for s in SKIP_KEYS):
                continue
            if any(p in SKIP_KEY_PART_RE.split(kl) for p in SKIP_KEY_PARTS):
                continue
            flatten(v, f"{prefix}.{k}" if prefix else k, out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:200]):
            flatten(v, f"{prefix}[{i}]", out)
    else:
        if isinstance(obj, (int, float)) and not isinstance(obj, bool):
            # 含 0.0（论文 "goal-rate difference 0.0000" 需匹配证据 0.0）；排除近零噪音与超大值
            if math.isfinite(obj) and (obj == 0 or 1e-4 < abs(obj)) and abs(obj) < 1e7:
                out.append((prefix, float(obj)))
    return out


def collect_numbers(evidence_dirs: list[Path]) -> list[dict]:
    nums = []
    for d in evidence_dirs:
        for f in sorted(p for p in d.rglob("*") if p.suffix in (".json", ".jsonl")):
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if f.suffix == ".jsonl":
                # JSON Lines：每行独立 JSON 对象，逐行扁平化（行号进 json_path 便于溯源）
                for ln, line in enumerate(text.splitlines(), 1):
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                    except Exception:
                        continue
                    for path, val in flatten(data, prefix=f"L{ln}"):
                        nums.append({"source": str(f), "json_path": path, "value": val})
            else:
                try:
                    data = json.loads(text)
                except Exception:
                    continue
                for path, val in flatten(data):
                    nums.append({"source": str(f), "json_path": path, "value": val})
    return nums


def find_support(value: float, numbers: list[tuple[str, float]]) -> str | None:
    for tok, t in numbers:
        if abs(t - value) <= TOL or (value != 0 and abs(t / value - 1) <= TOL):
            return tok
    return None


def collect_tex_rows(tex: str) -> list[dict]:
    """带行号/上下文收集论文小数（剔除注释行）。"""
    rows = []
    for i, line in enumerate(tex.splitlines(), 1):
        if line.strip().startswith("%"):
            continue
        for m in DEC_RE.finditer(line):
            tok = m.group(0)
            try:
                val = float(tok)
            except ValueError:
                continue
            rows.append({"token": tok, "value": val, "line": i, "context": line.strip()})
    return rows


def classify_noise(row: dict) -> str | None:
    """机械噪音启发式：返回噪音类别，None = 需人工复核。"""
    tok, ctx = row["token"], row["context"]
    if re.search(re.escape(tok) + r"\.\d", ctx):  # 0.32 是 0.32.1 版本号的片段
        return "version-fragment"
    if DATE_TOKEN_RE.match(tok):
        return "date"
    if any(tok in m.group(0) for m in STRUCTURAL_CMD_RE.finditer(ctx)):
        return "tex-structural"
    # PDF 提取噪音（v2.2 TMLR 校准批处理实测）：arXiv 号 / Version 标注 / Section 交叉引用 /
    # 独立成行的章节标题 / 连字符模型版本（MobileNetV2-0.5）/ 无空格逗号连写（0.5,1.0）
    if ARXIV_ID_RE.match(tok) and re.search(r"(?i)arxiv", ctx):
        return "arxiv-id"
    if re.search(r"(?i)\bversion\s" + re.escape(tok) + r"\b", ctx):
        return "version-label"
    if re.search(r"(?i)\bsections?\s~?\s*" + re.escape(tok) + r"\b", ctx):
        return "section-ref"
    if ctx.strip() == tok:
        return "section-heading"
    if re.search(r"[A-Za-z][A-Za-z0-9]*-" + re.escape(tok) + r"\b", ctx):
        return "model-suffix"
    if re.search(r"," + re.escape(tok) + r"\b", ctx):
        return "compact-list"
    rest = ctx.replace(tok, "#", 1)
    if YEAR_RE.search(rest) and len(ctx) <= 80:
        return "date-adjacent"
    return None


def reconcile(tex_path: Path, evidence_dirs: list[Path], adjudications: dict | None = None) -> dict:
    adj = {k: v for k, v in (adjudications or {}).items() if not k.startswith("_")}
    tex = tex_path.read_text(encoding="utf-8", errors="replace")
    tex_rows = collect_tex_rows(tex)
    tuples = [(r["token"], r["value"]) for r in tex_rows]

    evidence = collect_numbers(evidence_dirs)

    # 方向 A：产物数字 → 论文（抽样核心统计量：p 值、均值、统计量）
    a_rows = []
    for e in evidence:
        key = e["json_path"].lower()
        is_stat = any(s in key for s in ("p", "goal", "mean", "chi", "rate", "alpha", "cles", "score", "wilcoxon", "mcnemar", "cd"))
        if not is_stat:
            continue
        tok = find_support(e["value"], tuples)
        a_rows.append({**e, "in_paper": tok is not None, "paper_token": tok})
    a_hit = [r for r in a_rows if r["in_paper"]]

    def _prio(row):
        kp = row["json_path"].lower()
        if any(s in kp for s in ("mcnemar", "chi2", "pvalue", "p_value", "pval", "_p.", "_p[", "alpha", "kappa")):
            return (0, kp)
        if "goal" in kp or "rate" in kp or "mean" in kp:
            return (1, kp)
        return (2, kp)

    a_hit.sort(key=_prio)

    # 方向 B：论文小数 → 产物支撑 + 三层降噪
    ev_tuples = [(str(e["value"]), e["value"]) for e in evidence]
    b_rows = [{**r, "supported": find_support(r["value"], ev_tuples) is not None} for r in tex_rows]
    n_paper = len(b_rows)
    n_supp = sum(1 for r in b_rows if r["supported"])
    unsupported = [r for r in b_rows if not r["supported"]]

    adjudicated, noise_rows, needs_review = [], [], []
    for r in unsupported:
        tok = r["token"]
        rec = adj.get(tok)
        if rec and rec.get("verdict") in ("noise", "supported", "critical"):
            adjudicated.append({**r, "verdict": rec["verdict"], "note": rec.get("note", "")})
            continue
        cat = classify_noise(r)
        if cat:
            noise_rows.append({**r, "noise_kind": cat})
            continue
        needs_review.append(r)
        if tok not in adj:
            adj[tok] = {"verdict": "pending", "note": "", "context": r["context"][:120]}

    n_critical = sum(1 for r in adjudicated if r["verdict"] == "critical")
    support_rate = round(n_supp / n_paper, 4) if n_paper else None
    evidence_absent = not evidence        # 无证据目录/目录内无 JSON：方向 A/B 均无从对账
    if n_critical:
        verdict = "CRITICAL"
    elif evidence_absent:
        # 无证据可对账 ≠ 数字不符：不以 support_rate<0.3 判 CRITICAL——
        # 分母全是不可核验的数字，阈值恒触发（PDF-only/第三方论文评审场景）
        verdict = "MAJOR" if needs_review else "PASS"
    elif support_rate is not None and support_rate < 0.3:
        verdict = "CRITICAL"
    else:
        verdict = "MAJOR" if needs_review else "PASS"

    def _short(r):
        return {k: (v[:100] if isinstance(v, str) else v) for k, v in r.items() if k in ("token", "value", "line", "context", "verdict", "note", "noise_kind")}

    return {
        "meta": {
            "tex": str(tex_path),
            "evidence_dirs": [str(d) for d in evidence_dirs],
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "direction_A_evidence_to_paper": {
            "checked": len(a_rows),
            "found_in_paper": len(a_hit),
            "hit_rate": round(len(a_hit) / len(a_rows), 4) if a_rows else None,
            "key_matches": [
                {"json_path": r["json_path"], "value": r["value"], "paper_token": r["paper_token"], "source": r["source"]}
                for r in a_hit[:60]
            ],
        },
        "direction_B_paper_to_evidence": {
            "paper_decimals": n_paper,
            "supported": n_supp,
            "unsupported": n_paper - n_supp,
            "support_rate": support_rate,
            "noise_filtered": [_short(r) for r in noise_rows],
            "adjudicated": [_short(r) for r in adjudicated],
            "manual_review_list": [_short(r) for r in needs_review],
        },
        "adjudications_state": adj,
        "_evidence": [{"source": e["source"], "json_path": e["json_path"], "value": e["value"]} for e in evidence],
        "summary": {
            "verdict": verdict,
            "critical_adjudicated": n_critical,
            "pending_review": len(needs_review),
            "noise_filtered": len(noise_rows),
            "adjudicated": len(adjudicated),
            "paper_decimals": n_paper,
            "evidence_absent": evidence_absent,
            "note": "manual_review_list = 未裁决且非机械噪音；裁决文件填 verdict(noise|supported|critical) 后重跑即收敛",
        },
    }


# ---------------------------------------------------------------- R3 裁决自动化：机械层 + LLM 语义裁决

TABCOL_RE = re.compile(r"p\{(\d+\.\d+)cm\}")
INCLUDE_W_RE = re.compile(r"width=(\d+\.\d+)\\?linewidth")
MODEL_RE = re.compile(r"\b(?:qwen|llama|gemma|deepseek|gpt|claude)[\w.-]*?(\d+\.\d+)")
COST_RE = re.compile(r"(?:\\\$|[¥€]|\\yen)\s*(\d+\.\d+)")
TIME_RANGE_RE = re.compile(r"\d+(?:\.\d+)?\s*[-–—]{1,2}\s*\d+\.\d+\s*h\b")
R3_VERDICTS = ("noise", "supported", "critical")


def mechanical_r3(token: str, contexts: list[str], evidence_nums: list[tuple[str, float]]) -> tuple[str | None, str]:
    """R3 机械裁决：返回 (verdict, note)。verdict ∈ {supported, noise, None}；None = 需 LLM。

    只使用高置信规则：证据直接/比例/2 位舍入匹配 → supported；明显噪音形态 → noise。
    不用百分数/缩放 100 启发（实测对计数/时间/成本产生大量误报，如 0.87 误配 elapsed_s=86.97）。
    """
    try:
        val = float(token)
    except ValueError:
        return None, ""
    for path, v in evidence_nums:
        if abs(v - val) <= TOL or (val != 0 and abs(v / val - 1) <= TOL):
            return "supported", f"证据匹配 {path}={v}"
        if abs(round(v, 2) - val) <= 1e-9 and abs(v - val) > TOL:
            return "supported", f"证据 2 位舍入 {path}={v}→{round(v, 2)}"
    for ctx in contexts:
        if any(abs(float(m.group(1)) - val) <= 1e-9 for m in TABCOL_RE.finditer(ctx)):
            return "noise", "表格列宽 p{...cm}"
        if any(abs(float(m.group(1)) - val) <= 1e-9 for m in INCLUDE_W_RE.finditer(ctx)):
            return "noise", "插图宽度 width=...\\linewidth"
        if any(abs(float(m.group(1)) - val) <= 1e-9 for m in MODEL_RE.finditer(ctx)):
            return "noise", "模型版本号"
        if any(abs(float(m.group(1)) - val) <= 1e-9 for m in COST_RE.finditer(ctx)):
            return "noise", "成本/价格"
        if TIME_RANGE_RE.search(ctx):
            return "noise", "时间范围"
    return None, ""


def collect_token_contexts(tex_path: Path, token: str, max_lines: int = 4) -> list[str]:
    """收集 token 在论文中的完整上下文行（剔除注释行）。"""
    lines = tex_path.read_text(encoding="utf-8", errors="replace").splitlines()
    pat = re.compile(r"(?<![\d.])" + re.escape(token) + r"(?![\d.])")
    out = []
    for i, ln in enumerate(lines, 1):
        if ln.strip().startswith("%"):
            continue
        if pat.search(ln):
            out.append(f"L{i}: {ln.strip()}")
            if len(out) >= max_lines:
                break
    return out


def build_r3_prompt(token: str, contexts: list[str], mechanical: str) -> str:
    return (
        "你是数字对账审稿人（对抗裁决）。论文中有一个小数无法在产物 JSON 中机械匹配到支撑。"
        "请裁决该数字的性质：noise（误报，非实质断言）/ supported（实质断言且有来源）/ "
        "critical（实质断言但无来源，一票 Critical）。\n\n"
        f"数字：{token}\n"
        f"出现位置（论文原文行）：\n" + "\n".join(contexts) + "\n\n"
        f"机械层已做：直接/比例/2 位舍入容差匹配（TOL=5e-4）→ {mechanical or '无命中'}\n\n"
        "裁决要求（对抗性，必须怀疑）：\n"
        "1. 该数字是否为实质断言（结果/统计量/指标）？还是噪音（成本/版本号/表格列宽/模型版本/"
        "阈值/时间范围/参数/派生中间量）？\n"
        "2. 若是实质断言：论文是否声明其来源（如 see out_p5/xxx.json / results/xxx.json）？"
        "证据 JSON 中是否可能有对应值（不同精度/派生形式）？\n"
        "3. 若是实质断言且论文未声明任何来源 → critical\n"
        "4. evidence 必须引用论文原文句子（<=80字），不许编造\n\n"
        "输出严格 JSON（不要 markdown 代码块、不要多余文字）：\n"
        '{"verdict": "noise|supported|critical", "confidence": "high|medium|low", '
        '"justification": "<=120字", "evidence": "<=80字 论文原句", "suggested_action": "<=60字"}'
    )


def adjudicate_pending(report: dict, tex_path: Path, rpc_url: str = "http://127.0.0.1:3080",
                       timeout: int = 300, max_llm: int = 100,
                       existing: dict | None = None, checkpoint: Path | None = None) -> dict:
    """R3 裁决自动化：机械层 + LLM 语义裁决，落盘裁决结果（token → verdict）。

    对 manual_review_list 的每个唯一 token：
      - 机械层先判（证据匹配/明显噪音）
      - 剩余交 LLM 对抗裁决：noise / supported / critical
      - RPC 不可达 → SKIP（不阻塞，门禁维持原判）
    """
    import urllib.error
    import urllib.request

    mrl = report["direction_B_paper_to_evidence"]["manual_review_list"]
    unique = {}
    for r in mrl:
        unique.setdefault(r["token"], []).append(r["context"])

    evidence_nums = [(str(e["value"]), e["value"]) for e in report.get("_evidence", [])]

    out = {
        "meta": {"tex": str(tex_path), "rpc": rpc_url,
                 "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")},
        "adjudications": [],
        "summary": {"total": 0, "mechanical": 0, "llm": 0, "llm_failed": 0,
                    "noise": 0, "supported": 0, "critical": 0, "verdict": None, "detail": ""},
    }
    if not unique:
        out["summary"]["verdict"] = "PASS"
        out["summary"]["detail"] = "无待复核 token，无需裁决"
        return out

    # RPC 健康检查（DSH 过载时响应可达 15s+，超时放宽到 20s，避免误判不可达清空断点）
    try:
        with urllib.request.urlopen(rpc_url.rstrip("/"), timeout=20) as r:
            health = f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        health = f"HTTP {e.code}（服务在监听）"
    except Exception as e:  # noqa: BLE001
        out["meta"]["rpc_health"] = f"不可达（{type(e).__name__}）"
        out["summary"]["verdict"] = "SKIP"
        out["summary"]["detail"] = "RPC 不可达 → LLM 裁决跳过，门禁维持 recompute 原判"
        return out
    out["meta"]["rpc_health"] = health

    import adversarial_review as adv
    adv.RPC = rpc_url

    prior = {a["token"]: a for a in (existing or {}).get("adjudications", [])
             if a.get("verdict") in R3_VERDICTS}
    n_prior = len(prior)
    if n_prior:
        print(f"  [R3] 断点续跑：复用已裁决 {n_prior}/{len(unique)}", flush=True)

    def _checkpoint() -> None:
        if checkpoint is not None:
            checkpoint.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")

    n_llm_calls = 0
    for i, (token, ctxs) in enumerate(unique.items(), 1):
        if token in prior:
            out["adjudications"].append(prior[token])
            continue
        mech_verdict, mech_note = mechanical_r3(token, ctxs, evidence_nums)
        entry = {"token": token, "contexts": ctxs, "mechanical": mech_note or None}
        if mech_verdict:
            entry.update({"layer": "mechanical", "verdict": mech_verdict, "confidence": "high",
                          "justification": mech_note, "evidence": ctxs[0][:80] if ctxs else "",
                          "suggested_action": ""})
            out["adjudications"].append(entry)
            _checkpoint()
            continue
        if n_llm_calls >= max_llm:
            entry.update({"layer": "llm", "verdict": "未裁决", "llm_status": "max_llm"})
            out["adjudications"].append(entry)
            out["summary"]["llm_failed"] += 1
            continue
        n_llm_calls += 1
        print(f"  [R3] 裁决 {i}/{len(unique)}：{token[:24]!r}（LLM 第 {n_llm_calls} 次）", flush=True)
        ctx = "\n".join(ctxs)
        rec = adv.prompt_turn(build_r3_prompt(token, ctxs, mech_note), "r3-adjudicate", timeout=timeout)
        if rec["status"] != "ok":
            entry.update({"layer": "llm", "verdict": "未裁决", "llm_status": rec["status"]})
            out["adjudications"].append(entry)
            out["summary"]["llm_failed"] += 1
            _checkpoint()
            continue
        parsed = parse_r3_verdict(rec["raw"])
        if parsed:
            entry.update(parsed)
            entry["layer"] = "llm"
        else:
            entry.update({"layer": "llm", "verdict": "未裁决", "llm_status": "parse_failed",
                          "raw_head": rec["raw"][:300]})
            out["summary"]["llm_failed"] += 1
        out["adjudications"].append(entry)
        _checkpoint()

    for a in out["adjudications"]:
        v = a.get("verdict")
        if v in R3_VERDICTS:
            out["summary"][v] += 1
            if a["layer"] == "mechanical":
                out["summary"]["mechanical"] += 1
            else:
                out["summary"]["llm"] += 1
    out["summary"]["total"] = len(out["adjudications"])

    n_critical = out["summary"]["critical"]
    n_unadjudicated = sum(1 for a in out["adjudications"] if a.get("verdict") == "未裁决")
    if n_critical:
        out["summary"]["verdict"] = "CRITICAL"
        out["summary"]["detail"] = (f"critical {n_critical} 个（实质断言无来源，一票 Critical）；"
                                    f"noise {out['summary']['noise']} / supported {out['summary']['supported']}")
    elif n_unadjudicated:
        out["summary"]["verdict"] = "MAJOR"
        out["summary"]["detail"] = (f"{n_unadjudicated} 个未裁决（LLM 失败 {out['summary']['llm_failed']}）"
                                    f"→ 维持 recompute 原判 Major；noise {out['summary']['noise']} / "
                                    f"supported {out['summary']['supported']}")
    elif out["summary"]["supported"] or out["summary"]["noise"]:
        out["summary"]["verdict"] = "PASS"
        out["summary"]["detail"] = (f"全部裁决：noise {out['summary']['noise']} / "
                                    f"supported {out['summary']['supported']}，无 critical")
    else:
        out["summary"]["verdict"] = "PASS"
        out["summary"]["detail"] = "无待复核 token"
    return out


def parse_r3_verdict(raw: str) -> dict | None:
    if not raw:
        return None
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if fence:
        text = fence.group(1)
    m = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text, re.S)
    if m:
        try:
            obj = json.loads(m.group(0).replace("：", ":").replace("，", ","))
            verdict = obj.get("verdict")
            if verdict in R3_VERDICTS:
                return {
                    "verdict": verdict,
                    "confidence": str(obj.get("confidence", "low"))[:16],
                    "justification": str(obj.get("justification", ""))[:300],
                    "evidence": str(obj.get("evidence", ""))[:200],
                    "suggested_action": str(obj.get("suggested_action", ""))[:200],
                    "parse": "json",
                }
        except (json.JSONDecodeError, ValueError):
            pass
    vm = re.search(r"(?:verdict|裁决)\s*[:：]?\s*[\"']?(" + "|".join(R3_VERDICTS) + r")", text)
    if vm:
        return {"verdict": vm.group(1), "confidence": "low", "justification": raw[:200],
                "evidence": "", "suggested_action": "", "parse": "regex"}
    return None


def write_r3_md(adj: dict, out_md: Path) -> None:
    s = adj["summary"]
    lines = [
        "# 数字对账裁决报告（R3 自动化：机械层 + LLM 语义裁决）",
        "",
        f"- 论文：`{adj['meta']['tex']}`；RPC：{adj['meta'].get('rpc_health', '-')}",
        f"- 结论：**{s.get('verdict')}** —— {s.get('detail', '')}",
        "",
        "| token | 层 | 裁决 | 置信 | 依据 | 论文原句 |",
        "|---|---|---|---|---|---|",
    ]
    for a in adj["adjudications"]:
        lines.append(f"| `{a['token']}` | {a.get('layer', '-')} | **{a.get('verdict') or '-'}** | "
                     f"{a.get('confidence') or '-'} | {(a.get('justification') or '')[:60]} | "
                     f"{(a.get('evidence') or '')[:50]} |")
    lines += ["", "- 语义：noise=误报（非实质断言）；supported=实质断言且有来源；critical=实质断言无来源（一票 Critical）；未裁决=LLM 失败维持原判"]
    out_md.write_text("\n".join(lines), encoding="utf-8")


def write_md(report: dict, out_md: Path) -> None:
    a = report["direction_A_evidence_to_paper"]
    b = report["direction_B_paper_to_evidence"]
    s = report["summary"]
    lines = [
        "# 数字对账报告（R3）",
        "",
        f"- 论文：`{report['meta']['tex']}`，证据目录：{', '.join('`'+d+'`' for d in report['meta']['evidence_dirs']) or '（无）'}",
        f"- 结论：**{s['verdict']}**（裁决 critical {s['critical_adjudicated']}，待复核 {s['pending_review']}，机械噪音 {s['noise_filtered']}，已裁决 {s['adjudicated']}）",
        f"- 无证据目录：{('是——方向 A/B 均无从对账，支撑率不可判（PDF-only/第三方论文评审）' if s.get('evidence_absent') else '否')}",
        "",
        "## 方向 A：产物统计数字 → 论文出现（论文未改数字）",
        "",
        f"- 核心统计数字 {a['checked']} 个，其中 {a['found_in_paper']} 个在论文中找到一致值（命中率 {a['hit_rate']}）",
        "",
        "| json_path | 值 | 论文 token | 来源 |", "|---|---|---|---|",
    ]
    lines += [f"| `{m['json_path']}` | {m['value']} | `{m['paper_token']}` | `{Path(m['source']).name}` |" for m in a["key_matches"][:40]]
    lines += [
        "",
        "## 方向 B：论文小数 → 产物支撑",
        "",
        f"- 论文小数 {b['paper_decimals']} 个，有支撑 {b['supported']} 个（支撑率 {b['support_rate']}）",
        f"- 机械噪音 {len(b['noise_filtered'])} 个（版本号片段/日期/结构行，自动豁免）",
        f"- 已裁决 {len(b['adjudicated'])} 个（人工 verdict：noise/supported/critical）",
        "",
        "### 人工复核清单（未裁决且非噪音）",
        "",
    ]
    mrl = b["manual_review_list"]
    if mrl:
        lines += [f"- L{r['line']} `{r['token']}`：{r['context']}" for r in mrl[:80]]
        if len(mrl) > 80:
            lines.append(f"- ……共 {len(mrl)} 个，见 JSON")
    else:
        lines.append("- 无（全部已支撑 / 已豁免 / 已裁决）")
    adjd = b["adjudicated"]
    if adjd:
        lines += ["", "### 已裁决明细", "", "| token | verdict | note |", "|---|---|---|"]
        lines += [f"| `{r['token']}` | {r['verdict']} | {r.get('note', '')} |" for r in adjd[:60]]
    nf = b["noise_filtered"]
    if nf:
        lines += ["", "### 机械噪音（自动豁免）", ""]
        lines += [f"- `{r['token']}`（{r['noise_kind']}）：{r['context']}" for r in nf[:40]]
        if len(nf) > 40:
            lines.append(f"- ……共 {len(nf)} 个")
    out_md.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    import tempfile

    tmp = Path(tempfile.mkdtemp())
    ev = tmp / "results"
    ev.mkdir()
    (ev / "stats.json").write_text(json.dumps({"l2": {"mean_goal_A": 0.14175, "mcnemar_p": 1.0}}), encoding="utf-8")
    tex = tmp / "main.tex"
    tex.write_text(
        "Mean goal was $0.1418$ with $p=1.0000$.\n"
        "Headline metric 0.355 with no source.\n"
        "Version v0.32.1 released 2026.08.26.\n"
        "Unsupported 7.77 and 9.99.\n"
        "\\section{Results} achieved 7.88 overall.\n"
        "See \\ref{tab:4.5} for the table.\n"
        "See Section 5.3 for details.\n"
        "4.1\n"
        "MobileNetV2-0.5,1.5 baseline.\n"
        "Version 1.5 notes.\n"
        "Preprint arXiv:1306.5151 (2013).\n",
        encoding="utf-8",
    )
    adj_path = tmp / "adj.json"
    adj_path.write_text(json.dumps({"7.77": {"verdict": "critical", "note": "正文声称值无产物来源"}}), encoding="utf-8")
    adj = json.loads(adj_path.read_text(encoding="utf-8"))

    rep = reconcile(tex, [ev], adj)
    a = rep["direction_A_evidence_to_paper"]
    b = rep["direction_B_paper_to_evidence"]

    assert a["found_in_paper"] >= 1, a
    assert not any(r["token"] == "0.1418" for r in b["manual_review_list"])
    # 7.77 已裁决 critical → verdict CRITICAL，且不进待复核清单
    assert rep["summary"]["verdict"] == "CRITICAL", rep["summary"]
    assert any(r["token"] == "7.77" and r["verdict"] == "critical" for r in b["adjudicated"]), b["adjudicated"]
    # 0.32 是版本号片段 → 机械噪音；2026.08 是日期 → 机械噪音
    assert any(r["token"] == "0.32" and r["noise_kind"] == "version-fragment" for r in b["noise_filtered"]), b["noise_filtered"]
    assert any(r["token"] == "2026.08" for r in b["noise_filtered"]), b["noise_filtered"]
    # \ref{tab:4.5} 里的 4.5 → tex-structural；\section 同行但花括号外的 7.88 → 不豁免
    assert any(r["token"] == "4.5" and r["noise_kind"] == "tex-structural" for r in b["noise_filtered"]), b["noise_filtered"]
    assert not any(r["token"] == "7.88" for r in b["noise_filtered"]), b["noise_filtered"]
    assert any(r["token"] == "7.88" for r in b["manual_review_list"]), b["manual_review_list"]
    # 9.99 未裁决 → 进待复核清单，且以 pending 写回裁决状态
    assert any(r["token"] == "9.99" for r in b["manual_review_list"]), b["manual_review_list"]
    assert rep["adjudications_state"]["9.99"]["verdict"] == "pending", rep["adjudications_state"]
    # 人工把 9.99 裁决为 noise 后重跑 → 清单收敛
    adj2 = dict(rep["adjudications_state"])
    adj2["9.99"] = {"verdict": "noise", "note": "表格维度"}
    rep2 = reconcile(tex, [ev], adj2)
    assert not any(r["token"] == "9.99" for r in rep2["direction_B_paper_to_evidence"]["manual_review_list"])
    # PDF 提取噪音（v2.2）：章节引用/独立标题行/模型版本/连写列表/arXiv ID/Version 标注
    nf = {(r["token"], r["noise_kind"]) for r in b["noise_filtered"]}
    assert ("5.3", "section-ref") in nf, nf
    assert ("4.1", "section-heading") in nf, nf
    assert ("0.5", "model-suffix") in nf, nf
    assert ("1.5", "compact-list") in nf, nf
    assert ("1306.5151", "arxiv-id") in nf, nf
    assert ("1.5", "version-label") in nf, nf
    # 无证据目录：支撑率不可判 → 不判 CRITICAL（PDF-only/第三方论文评审）
    rep3 = reconcile(tex, [], {})
    s3 = rep3["summary"]
    assert s3["evidence_absent"] is True and s3["verdict"] != "CRITICAL", s3
    # 无证据 + 人工裁决 critical 仍然一票 CRITICAL
    rep4 = reconcile(tex, [], {"7.77": {"verdict": "critical", "note": ""}})
    assert rep4["summary"]["verdict"] == "CRITICAL", rep4["summary"]

    # ---- R3 裁决自动化：机械层 --------------------------------------------
    # 证据直接匹配 → supported
    v, n = mechanical_r3("0.1418", ["goal was 0.1418"], [("stats.json:goal", 0.14175)])
    assert v == "supported" and "证据匹配" in n, (v, n)
    # 2 位舍入匹配（0.1418 → 0.14）
    v, n = mechanical_r3("0.14", ["goal 0.14"], [("stats.json:goal", 0.1418)])
    assert v == "supported" and "2 位舍入" in n, (v, n)
    # 表格列宽 / 插图宽度 / 模型版本 / 成本 / 时间范围 → noise
    v, n = mechanical_r3("2.4", ["\\begin{tabular}{p{2.4cm}p{2.8cm}}"], [])
    assert v == "noise" and "列宽" in n, (v, n)
    v, n = mechanical_r3("0.98", ["\\includegraphics[width=0.98\\linewidth]"], [])
    assert v == "noise" and "插图宽度" in n, (v, n)
    v, n = mechanical_r3("2.5", ["qwen2.5:7b and qwen2.5:14b"], [])
    assert v == "noise" and "模型版本" in n, (v, n)
    v, n = mechanical_r3("1.87", ["cost \\yen1.87/h"], [])
    assert v == "noise" and "成本" in n, (v, n)
    v, n = mechanical_r3("2.5", ["GPU time 2--2.5h"], [])
    assert v == "noise" and "时间范围" in n, (v, n)
    # 无命中 → None（交 LLM）
    v, n = mechanical_r3("0.355", ["headline 0.355"], [("stats.json:x", 0.36)])
    assert v is None, (v, n)
    # 缩放 100 误报不触发（0.87 不应匹配 elapsed_s=86.97）
    v, n = mechanical_r3("0.87", ["rho=0.87 trend"], [("L2.json:elapsed_s", 86.97)])
    assert v is None, (v, n)

    # ---- R3 裁决自动化：LLM 语义裁决（mock 全链路） ------------------------
    import urllib.request
    import adversarial_review as adv

    class _FakeResp:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    calls = {"n": 0}

    def fake_prompt(text, role_key, timeout=300):
        calls["n"] += 1
        if "0.355" in text:
            return {"role": role_key, "status": "ok", "issues": {}, "raw":
                    '{"verdict": "critical", "confidence": "medium", "justification": "摘要头号指标无任何产物来源声明", "evidence": "yields 24 L2 rows", "suggested_action": "补证据"}'}
        return {"role": role_key, "status": "ok", "issues": {}, "raw":
                '{"verdict": "noise", "confidence": "high", "justification": "成本", "evidence": "cost", "suggested_action": ""}'}

    orig_urlopen, orig_prompt = urllib.request.urlopen, adv.prompt_turn
    urllib.request.urlopen = lambda *a, **k: _FakeResp()
    adv.prompt_turn = fake_prompt
    try:
        qual = adjudicate_pending(rep, tex, rpc_url="http://127.0.0.1:3080")
    finally:
        urllib.request.urlopen, adv.prompt_turn = orig_urlopen, orig_prompt
    assert qual["summary"]["total"] >= 1, qual["summary"]
    assert qual["summary"]["llm"] >= 1, qual["summary"]
    assert qual["summary"]["verdict"] == "CRITICAL", qual["summary"]  # 0.355 → critical 一票
    assert any(a["token"] == "0.355" and a["verdict"] == "critical" for a in qual["adjudications"]), qual["adjudications"]

    # RPC 不可达 → SKIP，不阻塞
    qual_skip = adjudicate_pending(rep, tex, rpc_url="http://127.0.0.1:1")
    assert qual_skip["summary"]["verdict"] == "SKIP", qual_skip["summary"]

    # LLM 超时 → 未裁决 → MAJOR（不虚报 PASS）
    def fake_timeout(text, role_key, timeout=300):
        return {"role": role_key, "status": "timeout", "issues": {}, "raw": ""}

    orig_urlopen2, orig_prompt2 = urllib.request.urlopen, adv.prompt_turn
    urllib.request.urlopen = lambda *a, **k: _FakeResp()
    adv.prompt_turn = fake_timeout
    try:
        qual_to = adjudicate_pending(rep, tex, rpc_url="http://127.0.0.1:3080")
    finally:
        urllib.request.urlopen, adv.prompt_turn = orig_urlopen2, orig_prompt2
    assert qual_to["summary"]["llm_failed"] >= 1, qual_to["summary"]
    assert qual_to["summary"]["verdict"] == "MAJOR", qual_to["summary"]

    # 全部机械裁决（无 LLM 候选）→ 但 RPC 不可达 → SKIP
    qual_pass = adjudicate_pending(rep2, tex, rpc_url="http://127.0.0.1:1")
    assert qual_pass["summary"]["verdict"] == "SKIP", qual_pass["summary"]

    # ---- max_llm 分批：只限制 LLM 调用数，机械条目不占额度 -------------------
    urllib.request.urlopen = lambda *a, **k: _FakeResp()
    adv.prompt_turn = fake_prompt
    try:
        qual_b1 = adjudicate_pending(rep, tex, rpc_url="http://127.0.0.1:3080", max_llm=1)
    finally:
        urllib.request.urlopen, adv.prompt_turn = orig_urlopen, orig_prompt
    assert qual_b1["summary"]["llm"] == 1, qual_b1["summary"]      # 恰好 1 次 LLM 调用
    assert qual_b1["summary"]["llm_failed"] >= 1, qual_b1["summary"]  # 其余 LLM 候选标未裁决（下一批重跑）

    print("number_reconcile selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tex", type=Path)
    ap.add_argument("--evidence-dirs", type=str)
    ap.add_argument("--out", type=Path, default=Path("audit_out"))
    ap.add_argument("--adjudications", type=Path, help="人工裁决文件（JSON，token→{verdict,note}；重跑后自动扩容 pending）")
    ap.add_argument("--llm-adjudicate", action="store_true",
                    help="R3 裁决自动化：机械层 + LLM 语义裁决待复核 token（noise/supported/critical）")
    ap.add_argument("--max-llm", type=int, default=100,
                    help="单次运行最多 LLM 裁决调用数（分批执行时设小值，如 5；已裁决 token 下次运行自动跳过）")
    ap.add_argument("--rpc", default="http://127.0.0.1:3080")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not (args.tex and args.evidence_dirs):
        ap.error("--tex and --evidence-dirs are required (or --selftest)")
    dirs = [Path(p) for p in args.evidence_dirs.split(",") if p.strip()]

    adj = {}
    if args.adjudications and args.adjudications.exists():
        adj = json.loads(args.adjudications.read_text(encoding="utf-8"))

    report = reconcile(args.tex, dirs, adj)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "number_reconcile.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(report, args.out / "number_reconcile.md")

    if args.llm_adjudicate and report["summary"]["pending_review"]:
        qual = adjudicate_pending(report, args.tex, rpc_url=args.rpc, max_llm=args.max_llm)
        (args.out / "r3_adjudications.json").write_text(json.dumps(qual, ensure_ascii=False, indent=2), encoding="utf-8")
        write_r3_md(qual, args.out / "r3_adjudications.md")
        q = qual["summary"]
        print(f"r3_adjudicate={q['verdict']} total={q['total']} mech={q['mechanical']} llm={q['llm']} "
              f"noise={q['noise']} supported={q['supported']} critical={q['critical']} llm_failed={q['llm_failed']}")
        print(f"-> {args.out / 'r3_adjudications.md'}")
        if args.adjudications:
            merged = dict(adj)
            for a in qual["adjudications"]:
                if a.get("verdict") in R3_VERDICTS:
                    merged[a["token"]] = {"verdict": a["verdict"],
                                          "note": (a.get("justification") or "")[:200],
                                          "context": (a.get("evidence") or "")[:120],
                                          "layer": a.get("layer")}
            state = {
                "_meta": {
                    "usage": "verdict: noise=误报(版本/日期/派生/维度) | supported=人工确认有来源 | critical=真实无支撑 → 一票 Critical | pending=待判",
                    "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "pending": sum(1 for v in merged.values() if isinstance(v, dict) and v.get("verdict") == "pending"),
                },
                **merged,
            }
            args.adjudications.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"adjudications merged -> {args.adjudications}")

    if args.adjudications and not args.llm_adjudicate:
        state = {
            "_meta": {
                "usage": "verdict: noise=误报(版本/日期/派生/维度) | supported=人工确认有来源 | critical=真实无支撑 → 一票 Critical | pending=待判",
                "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "pending": sum(1 for v in report["adjudications_state"].values() if isinstance(v, dict) and v.get("verdict") == "pending"),
            },
            **report["adjudications_state"],
        }
        args.adjudications.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    s = report["summary"]
    a = report["direction_A_evidence_to_paper"]
    b = report["direction_B_paper_to_evidence"]
    print(f"verdict={s['verdict']} A: {a['found_in_paper']}/{a['checked']} hit | B: {b['supported']}/{b['paper_decimals']} supported")
    print(f"pending={s['pending_review']} noise={s['noise_filtered']} adjudicated={s['adjudicated']} critical={s['critical_adjudicated']}")
    print(f"manual review list: {len(b['manual_review_list'])} numbers -> {args.out / 'number_reconcile.md'}")
    if args.adjudications:
        print(f"adjudications updated -> {args.adjudications}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
