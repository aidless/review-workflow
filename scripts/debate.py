# -*- coding: utf-8 -*-
"""审稿人-作者辩论（debate）— 审稿工作流 v2.0。

单轮 LLM 审查的 Critical/Major 清单有噪声：有些问题作者一句话就能驳回（假阳性），
有些问题被作者 rebuttal 后反而暴露更严重（真阳性增强）。辩论机制把"哪些问题站得住"
交给对抗过程而不是单次生成：

  第 1 幕  作者   逐条回应：rebut（给出具体依据）或 concede（认错承诺修）
  第 2 幕  审稿人 评估 rebuttal：sustain（维持）/ withdraw（撤回）/ partial
  第 3 幕  裁判   终裁：只统计 sustained 的问题；撤回的不计入门禁

输入来源：--issues 可以是
  - R6 输出（adversarial_review.json / r6_llm.json 的 stable_issues）
  - PRISM 输出（prism_review.json 的 dimensions weaknesses）
  - 手写 JSON 数组 [{"sev": "Major", "text": "..."}]
辩论后 verdict 只按 sustained 重算（文本层仍只 WARN）。

用法:
    python debate.py --tex <main.tex> --issues <issues.json> --out <outdir> [--rounds 2]
    python debate.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
KIT_DIR = SCRIPTS_DIR.parents[1]
sys.path.insert(0, str(KIT_DIR))

# 环境变量覆盖（默认不变，来源同 prism_review）
import os as _os
MAX_CHARS = int(_os.environ.get("REVIEW_LLM_MAX_CHARS", "6000"))
MAX_ISSUES = 20          # 辩论成本控制：超出截断并标注
SEV_RANK = {"Critical": 3, "Major": 2, "Minor": 1}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_issues(src: Path, return_stats: bool = False):
    """从 R6/PRISM/手写 JSON 载入问题清单 → [{"id","sev","text"}]。

    return_stats=True 时额外返回 {"n_total", "n_debated", "n_truncated", "max_issues"}
    （截断是有意的成本控制，必须在报告里可见，不许静默丢问题）。"""
    data = json.loads(src.read_text(encoding="utf-8"))
    raw: list[dict] = []
    if isinstance(data, list):
        raw = data
    elif isinstance(data, dict) and "stable_issues" in data:            # r6_llm.json
        raw = [dict(i, sev=i.get("sev", "Minor")) for i in data["stable_issues"]]
    elif isinstance(data, dict) and "dimensions" in data:                # prism_review.json
        for k, d in data["dimensions"].items():
            if d.get("top_weakness"):
                raw.append({"sev": "Major", "text": f"[PRISM {k}] {d['top_weakness']}"})
    elif isinstance(data, dict) and "roles" in data:                     # adversarial_review.json
        for rec in data.get("roles", data.get("results", [])):
            for sev in ("Critical", "Major", "Minor"):
                for it in (rec.get("issues") or {}).get(sev) or []:
                    raw.append({"sev": sev, "text": it})
    elif isinstance(data, dict) and isinstance(data.get("issues"), dict):
        for sev in ("Critical", "Major", "Minor"):
            for it in data["issues"].get(sev) or []:
                raw.append({"sev": sev, "text": it})
    # 统一排序：严重者优先，且截断
    raw.sort(key=lambda i: -SEV_RANK.get(i.get("sev"), 0))
    raw = [i for i in raw if str(i.get("text", "")).strip()]
    n_total = len(raw)
    out = [{"id": k + 1, "sev": i.get("sev", "Minor"), "text": str(i["text"])[:300]}
           for k, i in enumerate(raw[:MAX_ISSUES])]
    n_truncated = n_total - len(out)
    if n_truncated > 0:
        out = out + [{"id": len(out) + 1, "sev": "Minor", "synthetic": True,
                     "text": f"（另有 {n_truncated} 条问题超出 {MAX_ISSUES} 条上限被截断，未参与辩论）"}]
    if return_stats:
        return out, {"n_total": n_total, "n_debated": min(n_total, MAX_ISSUES),
                     "n_truncated": n_truncated, "max_issues": MAX_ISSUES}
    return out


def author_prompt(issues: list[dict], paper_text: str) -> str:
    lines = "\n".join(f'{i["id"]}. [{i["sev"]}] {i["text"]}' for i in issues)
    return (
        "你是论文作者，正在回复审稿意见（rebuttal）。逐条回应下面的问题清单。\n"
        "规则：\n"
        "- 能用论文中的具体内容/数据/披露驳回的，选 rebut，rebuttal 必须引用论文具体内容（不许空辩）\n"
        "- 确实是问题的，选 concede，fix 用「将/会」表述具体修改方案（是承诺，尚未执行，"
        "不许写成已完成动作）\n"
        "- 不许回避任何一条\n\n"
        "输出严格 JSON 数组（不要 markdown、不要多余文字）：\n"
        '[{"id": 1, "action": "rebut", "rebuttal": "<=80字，引用论文依据"}, '
        '{"id": 2, "action": "concede", "fix": "<=60字"}]\n\n'
        f"问题清单：\n{lines}\n\n论文片段：\n{paper_text}"
    )


def judge_prompt(issues: list[dict], rebuttals: list[dict], paper_text: str) -> str:
    lines = "\n".join(f'{i["id"]}. [{i["sev"]}] {i["text"]}' for i in issues)
    rmap = {r.get("id"): r for r in rebuttals}
    rlines = "\n".join(
        f'{i["id"]}. 作者回应（{rmap.get(i["id"], {}).get("action", "未回应")}）：'
        f'{rmap.get(i["id"], {}).get("rebuttal") or rmap.get(i["id"], {}).get("fix") or "（无）"}'
        for i in issues)
    return (
        "你是独立裁判（不是原审稿人，也不是作者）。对每条审稿意见，评估作者的回应后终裁。\n"
        "辩论针对投稿当前版本：作者修改承诺（concede/fix）不消除当前版本的问题——concede 一律 "
        "sustain（真问题，待修订）；只有 rebut 且引用了论文现有内容、经你核对确实成立时才 "
        "withdraw（误报）；部分成立 → partial。\n\n"
        "输出严格 JSON 数组（不要 markdown、不要多余文字）：\n"
        '[{"id": 1, "disposition": "sustained|withdrawn|partial", '
        '"reason": "<=60字"}, ...]\n\n'
        f"审稿意见：\n{lines}\n\n作者回应：\n{rlines}\n\n论文片段：\n{paper_text}"
    )


def parse_json_array(raw: str) -> list[dict]:
    """容错解析 LLM 输出的 JSON 数组：剥代码块、截取数组、中文标点兼容。"""
    if not raw:
        return []
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.S)
    if fence:
        text = fence.group(1)
    text = text.replace("：", ":").replace("，", ",").replace("“", '"').replace("”", '"')
    # 用 raw_decode 从每个候选 `[` 精确解析第一个合法 JSON 数组，
    # 避免贪婪正则 `\[.*\]` 把尾部总结/尾注文字（含方括号或冒号）卷进候选串导致 json.loads 失败。
    # 这是"缺裁保守"故障（verdicts 空 → 全部 sustained）的根因修复。
    dec = json.JSONDecoder()
    i = 0
    while i < len(text):
        j = text.find("[", i)
        if j == -1:
            break
        try:
            arr, _ = dec.raw_decode(text[j:])
            if isinstance(arr, list):
                return [x for x in arr if isinstance(x, dict)]
            i = j + 1
        except (json.JSONDecodeError, ValueError):
            i = j + 1
    return []


def run_debate(tex_path: Path, issues_path: Path, rpc_url: str = "http://127.0.0.1:3080",
               timeout: int = 420) -> dict:
    import urllib.error
    import urllib.request

    paper = tex_path.read_text(encoding="utf-8", errors="replace")
    if len(paper) > MAX_CHARS:
        paper = paper[:MAX_CHARS] + "\n…(截断)"
    issues, tr_stats = load_issues(issues_path, return_stats=True)

    report = {"meta": {"tex": str(tex_path), "issues_file": str(issues_path),
                       "rpc": rpc_url, "timestamp": now()},
              "issues": issues, "rebuttals": [], "verdicts": [],
              "summary": {"verdict": None}}
    if not issues:
        report["summary"]["verdict"] = "SKIP"
        report["summary"]["detail"] = "问题清单为空——无可辩论事项"
        return report

    try:
        with urllib.request.urlopen(rpc_url.rstrip("/"), timeout=4) as r:
            report["meta"]["rpc_health"] = f"HTTP {r.status}"
    except Exception as e:  # noqa: BLE001
        report["summary"]["verdict"] = "SKIP"
        report["summary"]["detail"] = f"RPC 不可达（{type(e).__name__}）→ 辩论跳过；R6 原始清单仍有效"
        return report

    import adversarial_review as adv
    adv.RPC = rpc_url

    # 第 1 幕：作者（截断标注是披露行，不是真问题，不进 prompt）
    real = [i for i in issues if not i.get("synthetic")]
    print(f"[debate] 第 1 幕：作者回应 {len(real)} 条…", flush=True)
    rec_a = adv.prompt_turn(author_prompt(real, paper), "debate-author", timeout=timeout)
    if rec_a["status"] != "ok":
        report["summary"]["verdict"] = "SKIP"
        report["summary"]["detail"] = f"作者会话失败：{rec_a['status']}"
        return report
    rebuttals = parse_json_array(rec_a["raw"])
    report["rebuttals"] = rebuttals

    # 第 2 幕：裁判
    print("[debate] 第 2 幕：裁判终裁…", flush=True)
    rec_j = adv.prompt_turn(judge_prompt(real, rebuttals, paper), "debate-judge", timeout=timeout)
    if rec_j["status"] != "ok":
        report["summary"]["verdict"] = "SKIP"
        report["summary"]["detail"] = f"裁判会话失败：{rec_j['status']}"
        return report
    verdicts = parse_json_array(rec_j["raw"])
    report["verdicts"] = verdicts

    vmap = {v.get("id"): v for v in verdicts}
    sustained, withdrawn, partial = [], [], []
    for i in real:
        d = (vmap.get(i["id"]) or {}).get("disposition", "sustained")  # 缺裁 → 保守维持
        if d == "withdrawn":
            withdrawn.append(i)
        elif d == "partial":
            partial.append(i)
        else:
            sustained.append(i)
    cnt = {"Critical": sum(1 for i in sustained if i["sev"] == "Critical"),
           "Major": sum(1 for i in sustained if i["sev"] == "Major"),
           "Minor": sum(1 for i in sustained if i["sev"] == "Minor")}
    report["summary"] = {
        "verdict": "MAJOR" if (cnt["Critical"] or cnt["Major"]) else "PASS",
        "counts_sustained": cnt,
        "n_issues": len(real), "n_sustained": len(sustained),
        "n_withdrawn": len(withdrawn), "n_partial": len(partial),
        "truncation": tr_stats,
        "detail": (f"辩论后维持 Critical {cnt['Critical']} / Major {cnt['Major']} "
                   f"（撤回 {len(withdrawn)}，部分成立 {len(partial)}）；"
                   + (f"注：原始 {tr_stats['n_total']} 条中仅严重度前 {tr_stats['n_debated']} 条进入辩论"
                      f"（MAX_ISSUES={tr_stats['max_issues']}，截断 {tr_stats['n_truncated']} 条未辩论）；"
                      if tr_stats["n_truncated"] > 0 else "")
                   + "文本层 WARN 纪律不变"),
        "sustained_ids": [i["id"] for i in sustained],
        "withdrawn_ids": [i["id"] for i in withdrawn],
    }
    return report


def write_md(report: dict, out_md: Path) -> None:
    s = report["summary"]
    lines = [
        "# 审稿人-作者辩论报告（v2.0）",
        "",
        f"- 论文：`{report['meta']['tex']}`；问题来源：`{report['meta']['issues_file']}`",
        f"- RPC：{report['meta'].get('rpc_health', '-')}",
        f"- 结论：**{s.get('verdict')}** —— {s.get('detail', '')}",
        "",
        "| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |", "|---|---|---|---|---|---|",
    ]
    rmap = {r.get("id"): r for r in report.get("rebuttals", [])}
    vmap = {v.get("id"): v for v in report.get("verdicts", [])}
    for i in report.get("issues", []):
        r = rmap.get(i["id"], {})
        v = vmap.get(i["id"], {})
        resp = (r.get("rebuttal") or r.get("fix") or "-")[:60]
        disp = ("截断标注（不计入统计）" if i.get("synthetic")
                else v.get("disposition", "sustained(缺裁保守)"))
        lines.append(f"| {i['id']} | {i['sev']} | {i['text'][:60]} | {resp} | "
                     f"{disp} | {(v.get('reason') or '')[:50]} |")
    if s.get("counts_sustained"):
        lines += ["", f"**辩论后**：维持 Critical {s['counts_sustained']['Critical']} / "
                  f"Major {s['counts_sustained']['Major']} / Minor {s['counts_sustained']['Minor']}"
                  f"；撤回 {s['n_withdrawn']} 条（假阳性被作者驳回）；部分成立 {s['n_partial']} 条", "",
                  "## 解读",
                  "",
                  "- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）",
                  "- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）",
                  "- partial = 部分成立（建议作者在 camera-ready 中处理）",
                  ""]
    out_md.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    import tempfile

    tmp = Path(tempfile.mkdtemp())

    # 1) 解析：纯 JSON 数组
    arr = parse_json_array('[{"id": 1, "action": "rebut", "rebuttal": "见第3节"}]')
    assert len(arr) == 1 and arr[0]["action"] == "rebut", arr

    # 2) 解析：代码块 + 前后杂文
    arr = parse_json_array('作者回应：\n```json\n[{"id":1,"disposition":"withdrawn","reason":"论文已披露"}]\n```\n完毕')
    assert arr and arr[0]["disposition"] == "withdrawn", arr

    # 3) 解析：中文标点
    arr = parse_json_array('[{"id"：2，"action"：“concede”，"fix"：“将修”}]')
    assert arr and arr[0]["action"] == "concede", arr

    # 4) 解析：垃圾 → 空列表
    assert parse_json_array("无结构文本") == []
    assert parse_json_array("") == []

    # 4b) 解析：数组后带含方括号/冒号的尾注（原贪婪正则 `\[.*\]` 会将其卷进候选串 → 解析失败 → 全缺裁维持）
    _tail = ('[{"id":1,"disposition":"sustained","reason":"缺对照"},{"id":2,"disposition":"withdrawn",'
             '"reason":"见[第3节]"}] 共 2 条：sustained 1、withdrawn 1（合计数见上方）。')
    assert len(parse_json_array(_tail)) == 2, parse_json_array(_tail)
    _d = {x["id"]: x["disposition"] for x in parse_json_array(_tail)}
    assert _d == {1: "sustained", 2: "withdrawn"}, _d
    # 4c) reason 里含方括号嵌套，也应正确解析
    assert parse_json_array('[{"id":1,"disposition":"partial","reason":"论文[第5节]与[第6节]冲突"}]')[0]["disposition"] == "partial"

    # 5) issue 加载：r6_llm.json 形态
    r6 = {"stable_issues": [{"sev": "Critical", "text": "缺对照", "rounds": [1, 2]},
                            {"sev": "Major", "text": "样本小"}]}
    p6 = tmp / "r6_llm.json"
    p6.write_text(json.dumps(r6), encoding="utf-8")
    iss = load_issues(p6)
    assert len(iss) == 2 and iss[0]["sev"] == "Critical" and iss[0]["id"] == 1, iss

    # 6) issue 加载：prism 形态
    pr = {"dimensions": {"R": {"score": 5, "top_weakness": "零功效"}, "S": {"score": 9}}}
    pp = tmp / "prism.json"
    pp.write_text(json.dumps(pr), encoding="utf-8")
    iss2 = load_issues(pp)
    assert len(iss2) == 1 and "PRISM R" in iss2[0]["text"], iss2

    # 7) issue 加载：手写数组 + 截断（含结构化截断统计）
    many = [{"sev": "Minor", "text": f"问题{i}"} for i in range(30)]
    pm = tmp / "many.json"
    pm.write_text(json.dumps(many), encoding="utf-8")
    iss3, st3 = load_issues(pm, return_stats=True)
    assert len(iss3) == MAX_ISSUES + 1 and "截断" in iss3[-1]["text"], len(iss3)
    assert st3 == {"n_total": 30, "n_debated": 20, "n_truncated": 10, "max_issues": 20}, st3
    assert iss3[-1].get("synthetic") is True, iss3[-1]   # 截断标注行不进辩论统计
    iss3b = load_issues(pm)
    assert len(iss3b) == len(iss3)  # 默认返回值形态兼容

    # 8) prompt 构造
    ap = author_prompt([{"id": 1, "sev": "Major", "text": "样本小"}], "paper")
    assert "rebut" in ap and "concede" in ap and "paper" in ap
    jp = judge_prompt([{"id": 1, "sev": "Major", "text": "样本小"}],
                      [{"id": 1, "action": "rebut", "rebuttal": "见第5节表3"}], "paper")
    assert "withdrawn" in jp and "第5节表3" in jp

    # 9) write_md 落盘
    rep = {"meta": {"tex": "x", "issues_file": "y", "rpc_health": "HTTP 200"},
           "issues": [{"id": 1, "sev": "Major", "text": "样本小"}],
           "rebuttals": [{"id": 1, "action": "rebut", "rebuttal": "表3给出功效"}],
           "verdicts": [{"id": 1, "disposition": "partial", "reason": "部分成立"}],
           "summary": {"verdict": "MAJOR", "counts_sustained": {"Critical": 0, "Major": 0, "Minor": 1},
                       "n_issues": 1, "n_sustained": 0, "n_withdrawn": 0, "n_partial": 1,
                       "detail": "test", "sustained_ids": [], "withdrawn_ids": []}}
    write_md(rep, tmp / "debate.md")
    md = (tmp / "debate.md").read_text(encoding="utf-8")
    assert "辩论" in md and "partial" in md
    print("debate selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tex", type=Path)
    ap.add_argument("--issues", type=Path, help="R6/PRISM/手写 JSON 问题清单")
    ap.add_argument("--out", type=Path, default=Path("audit_out"))
    ap.add_argument("--rpc", default="http://127.0.0.1:3080")
    ap.add_argument("--timeout", type=int, default=420)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.tex or not args.issues:
        ap.error("--tex 与 --issues 必填（或 --selftest）")
    rep = run_debate(args.tex, args.issues, args.rpc, args.timeout)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "debate.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(rep, args.out / "debate.md")
    s = rep["summary"]
    print(f"verdict={s['verdict']} {s.get('detail', '')}")
    print(f"-> {args.out / 'debate.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
