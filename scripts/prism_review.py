# -*- coding: utf-8 -*-
"""PRISM 四维自评（prism_review）— 审稿工作流 v1.3（LLM-as-judge）。

机械证据门禁（R2-R5）管"数字对不对"，PRISM 管"科学质量怎么样"——
TMLR 审稿人视角四维评分（1-10 分 + 依据句 + 最大弱点）：

  P  Pertinence 契合度  论文与目标 venue/读者群的匹配、问题是否真实存在
  R  Rigor     严谨性   方法学正确性、统计检验选择、实验设计（对照/消融/seed）
  I  Impact    贡献量   增量贡献大小、对社区的有用性、新颖性是否实在
  S  Sincerity 诚实性   断言-证据对齐、局限是否坦率披露、可复现承诺是否可信

评分纪律与整套工作流一致：总分 = min(四维)（不平均）——短板决定论文命运。
LLM judge 只产 WARN 级门禁（文本层）；证据层 FAIL 由 R2-R5 机械核验决定。
RPC 不可达时 SKIP（不阻塞机械审查）。复用 adversarial_review 的会话管理。

用法:
    python prism_review.py --tex <main.tex> --out <outdir> [--dims P,R,I,S] [--rpc <url>]
    python prism_review.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
KIT_DIR = SCRIPTS_DIR.parents[1]          # research-kit 根
sys.path.insert(0, str(KIT_DIR))

# 环境变量覆盖（默认不变）：部分论文文本在 6000 字符截断点会让模型生成不终止
# （来源: tmlr-reviewer 集成轮实测；与 adversarial_review.REVIEW_LLM_* 同族）
import os as _os
MAX_CHARS = int(_os.environ.get("REVIEW_LLM_MAX_CHARS", "6000"))

DIMENSIONS = {
    "P": ("Pertinence", "契合度",
          "论文与目标 venue（如 TMLR）/读者群的匹配度；研究问题是否真实存在且值得解决；"
          "与已发表工作的关系是否清晰",
          "9-10=问题重要且 venue 完美契合；7-8=契合但问题常规；5-6=边缘契合或问题存疑；"
          "3-4=明显不契合/问题虚假；1-2=完全跑题"),
    "R": ("Rigor", "严谨性",
          "方法学正确性；统计检验选择与前提（配对/独立、多重比较、功效）；实验设计（对照、消融、seed 管理、"
          "基线公平）",
          "9-10=方法无可挑剔；7-8=小瑕疵不影响结论；5-6=有明显可质疑处需解释；3-4=实质缺陷可能动摇结论；"
          "1-2=方法学崩溃"),
    "I": ("Impact", "贡献量",
          "相对已有工作的增量；对社区的有用性（新能力/新基准/新洞察/负结果价值）；断言的贡献大小是否与证据匹配",
          "9-10=社区级影响；7-8=扎实增量；5-6=增量有限但有用；3-4=边际增量/已知结论重现；1-2=无实质贡献"),
    "S": ("Sincerity", "诚实性",
          "断言-证据对齐（不夸大）；局限是否坦率披露（而非营销式 limitation）；可复现承诺（数据/代码/脚本）"
          "是否可信",
          "9-10=表述克制、局限坦诚、复现完备；7-8=轻微夸大；5-6=有明显夸大或局限避重就轻；3-4=断言显著超出"
          "证据；1-2=误导性表述"),
}
GATE = {"P": "MAJOR", "R": "MAJOR", "I": "MAJOR", "S": "MAJOR"}  # 文本层只 WARN
SCORE_WARN = 6  # 任一维度 <=6 → MAJOR（门禁 WARN）


def build_judge_prompt(dim_key: str, paper_text: str) -> str:
    en, zh, desc, anchors = DIMENSIONS[dim_key]
    return (
        f"你是 TMLR 审稿人（LLM-as-judge），对下面的论文片段做单维度评分。\n"
        f"维度：{en}（{zh}）—— {desc}\n"
        f"评分锚点：{anchors}\n"
        "要求：\n"
        "1. 只评这一个维度，不要泛泛而谈其他维度\n"
        "2. evidence 字段必须引用论文原文中的具体句子片段（<=80字），不许编造\n"
        "3. top_weakness 给出该维度最致命的一个弱点\n\n"
        "输出严格 JSON（不要 markdown 代码块、不要多余文字）：\n"
        '{"score": <1-10 整数>, "justification": "<=120字 评分理由", '
        '"top_weakness": "<=60字", "evidence": "<=80字 论文原句依据>"}\n\n'
        "论文片段：\n" + paper_text
    )


def parse_judge_output(raw: str) -> dict | None:
    """容错解析 judge 输出：直接 JSON / 代码块包裹 / 中文冒号 / 正则兜底。"""
    if not raw:
        return None
    text = raw.strip()
    # 剥 markdown 代码块
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if fence:
        text = fence.group(1)
    # 取第一个平衡的大括号块
    m = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text, re.S)
    if m:
        try:
            obj = json.loads(m.group(0).replace("：", ":").replace("，", ","))
            score = obj.get("score")
            if isinstance(score, (int, float)) and 1 <= score <= 10:
                return {
                    "score": int(score),
                    "justification": str(obj.get("justification", ""))[:300],
                    "top_weakness": str(obj.get("top_weakness", ""))[:200],
                    "evidence": str(obj.get("evidence", ""))[:200],
                    "parse": "json",
                }
        except (json.JSONDecodeError, ValueError):
            pass
    # 正则兜底：找 score 字样后的数字
    sm = re.search(r"(?:\"score\"|score|评分)\s*[:：]?\s*[*>*]*\s*(\d+)", text)
    if sm:
        score = int(sm.group(1))
        if 1 <= score <= 10:
            return {"score": score, "justification": raw[:200],
                    "top_weakness": "", "evidence": "", "parse": "regex"}
    return None


def run_prism(tex_path: Path, rpc_url: str = "http://127.0.0.1:3080",
              dims: list[str] | None = None, timeout: int = 360) -> dict:
    import urllib.error
    import urllib.request

    text = tex_path.read_text(encoding="utf-8", errors="replace")
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n…(截断)"

    report = {
        "meta": {"tex": str(tex_path), "rpc": rpc_url, "timestamp":
                  datetime.now(timezone.utc).isoformat(timespec="seconds")},
        "dimensions": {},
        "summary": {"verdict": None, "scores": {}, "overall": None},
    }

    # RPC 健康检查
    try:
        with urllib.request.urlopen(rpc_url.rstrip("/"), timeout=4) as r:
            health = f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        health = f"HTTP {e.code}（服务在监听）"
    except Exception as e:  # noqa: BLE001
        report["summary"]["verdict"] = "SKIP"
        report["summary"]["detail"] = f"RPC 不可达（{type(e).__name__}）→ PRISM 跳过，不阻塞机械审查"
        return report
    report["meta"]["rpc_health"] = health

    import adversarial_review as adv
    adv.RPC = rpc_url

    keys = dims or list(DIMENSIONS)
    for k in keys:
        if k not in DIMENSIONS:
            continue
        print(f"[PRISM] {k} {DIMENSIONS[k][0]} 评审中…", flush=True)
        rec = adv.prompt_turn(build_judge_prompt(k, text), f"prism-{k.lower()}", timeout=timeout)
        if rec["status"] != "ok":
            report["dimensions"][k] = {"status": rec["status"], "score": None}
            continue
        parsed = parse_judge_output(rec["raw"])
        entry = {"status": "ok" if parsed else "parse_failed", "score": None}
        if parsed:
            entry.update(parsed)
        else:
            entry["raw_head"] = rec["raw"][:300]
        report["dimensions"][k] = entry

    scores = {k: v["score"] for k, v in report["dimensions"].items()
             if isinstance(v.get("score"), int)}
    report["summary"]["scores"] = scores
    if not scores:
        report["summary"]["verdict"] = "SKIP"
        report["summary"]["detail"] = "四个维度均未取得有效评分（RPC 会话失败或解析失败）"
        return report
    overall = min(scores.values())
    weakest = min(scores, key=scores.get)
    report["summary"]["overall"] = overall
    report["summary"]["weakest"] = f"{weakest}({DIMENSIONS[weakest][1]})"
    if overall <= SCORE_WARN:
        report["summary"]["verdict"] = "MAJOR"
        report["summary"]["detail"] = (f"最弱维度 {report['summary']['weakest']} = {overall} 分"
                                      f"（<= {SCORE_WARN}）→ 文本层 WARN；证据层门禁不受影响")
    else:
        report["summary"]["verdict"] = "PASS"
        report["summary"]["detail"] = f"四维均 > {SCORE_WARN}（min={overall}，短板纪律不平均）"
    return report


def write_md(report: dict, out_md: Path) -> None:
    s = report["summary"]
    lines = [
        "# PRISM 四维自评报告（v1.3，LLM-as-judge）",
        "",
        f"- 论文：`{report['meta']['tex']}`",
        f"- RPC：{report['meta']['rpc']}（{report['meta'].get('rpc_health', '-')}）",
        f"- 结论：**{s.get('verdict')}** —— {s.get('detail', '')}",
        "",
        "## 维度评分（总分 = min，不平均）",
        "",
    ]
    if s.get("scores"):
        lines += ["| 维度 | 分 | 评分理由 | 最大弱点 |", "|---|---|---|---|"]
        for k in DIMENSIONS:
            d = report["dimensions"].get(k, {})
            score = d.get("score")
            lines.append(f"| **{k} {DIMENSIONS[k][0]}**（{DIMENSIONS[k][1]}） | "
                         f"{score if score is not None else d.get('status', '-')} | "
                         f"{(d.get('justification') or '')[:100]} | {(d.get('top_weakness') or '')[:80]} |")
        lines += ["", f"**总分（min）= {s['overall']}**，最弱维度：{s['weakest']}", ""]
        lines += ["## 依据句（Sincerity 维度优先人工复核）", ""]
        for k in DIMENSIONS:
            d = report["dimensions"].get(k, {})
            if d.get("evidence"):
                lines.append(f"- {k}: {d['evidence']}")
    else:
        lines.append(f"- 无有效评分：{s.get('detail', '')}")
    out_md.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    # 1) prompt 构造：含维度描述与锚点
    p = build_judge_prompt("R", "dummy text")
    assert "Rigor" in p and "评分锚点" in p and "dummy text" in p
    assert '"score"' in p, p

    # 2) 解析：纯 JSON
    r = parse_judge_output('{"score": 7, "justification": "方法扎实", "top_weakness": "无", "evidence": "We test X"}')
    assert r and r["score"] == 7 and r["parse"] == "json", r

    # 3) 解析：markdown 代码块包裹 + 前后杂文
    r = parse_judge_output('好的，评分如下：\n```json\n{"score": 8, "justification": "j", '
                           '"top_weakness": "w", "evidence": "e"}\n```\n以上。')
    assert r and r["score"] == 8, r

    # 4) 解析：中文冒号
    r = parse_judge_output('{"score"：5，"justification"："中等"，"top_weakness"："样本小"，"evidence"："n=8"}')
    assert r and r["score"] == 5, r

    # 5) 解析：正则兜底（无 JSON 结构）
    r = parse_judge_output('评分：score: 4 —— 该文方法有明显问题')
    assert r and r["score"] == 4 and r["parse"] == "regex", r

    # 6) 解析：越界分 / 垃圾 → None
    assert parse_judge_output('{"score": 15}') is None
    assert parse_judge_output("完全无关的文本") is None
    assert parse_judge_output("") is None

    # 7) 聚合纪律（模拟 run_prism 的 summary 逻辑）
    dims = {"P": {"score": 8}, "R": {"score": 5}, "I": {"score": 7}, "S": {"score": 9}}
    scores = {k: v["score"] for k, v in dims.items() if isinstance(v.get("score"), int)}
    overall = min(scores.values())
    weakest = min(scores, key=scores.get)
    assert overall == 5 and weakest == "R"
    assert (overall <= SCORE_WARN) is True

    # 8) 维度表完整性
    assert len(DIMENSIONS) == 4 and set(DIMENSIONS) == {"P", "R", "I", "S"}
    for k, (en, zh, desc, anchors) in DIMENSIONS.items():
        assert en and zh and len(desc) > 20 and "9-10" in anchors, (k, en, zh)

    # 9) write_md 落盘
    from tempfile import mkdtemp
    tmp = Path(mkdtemp())
    rep = {"meta": {"tex": "x.tex", "rpc": "http://127.0.0.1:3080", "rpc_health": "HTTP 200"},
           "dimensions": {"P": {"status": "ok", "score": 8, "justification": "契合",
                               "top_weakness": "受众一般", "evidence": "we present"}},
           "summary": {"verdict": "PASS", "scores": {"P": 8}, "overall": 8,
                       "weakest": "P(契合度)", "detail": "四维均 > 6"}}
    write_md(rep, tmp / "prism.md")
    md = (tmp / "prism.md").read_text(encoding="utf-8")
    assert "PRISM" in md and "min" in md
    print("prism_review selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tex", type=Path)
    ap.add_argument("--out", type=Path, default=Path("audit_out"))
    ap.add_argument("--dims", default="P,R,I,S", help="逗号分隔维度键（P/R/I/S）")
    ap.add_argument("--rpc", default="http://127.0.0.1:3080")
    ap.add_argument("--timeout", type=int, default=360)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.tex:
        ap.error("--tex required (or --selftest)")
    dims = [d.strip().upper() for d in args.dims.split(",") if d.strip()]
    rep = run_prism(args.tex, args.rpc, dims, args.timeout)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "prism_review.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(rep, args.out / "prism_review.md")
    s = rep["summary"]
    print(f"verdict={s['verdict']} overall={s.get('overall')} scores={s.get('scores')}")
    print(f"-> {args.out / 'prism_review.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
