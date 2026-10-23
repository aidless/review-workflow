# -*- coding: utf-8 -*-
"""表格数字核验（table_check）— 审稿工作流 v2.1（R2d）。

表格是论文数字密度最高的结构，但 R3 全文对账没有表格语义：同一列混精度、
行标签与列头对应的数字无来源、\\input 的生成表文件缺失——这些只有按表格
结构解析才能看到。本模块做四件事：

  1. 表内 \\input{...} 辅助文件存在性：磁盘未找到 → CRITICAL（编译即断）
  2. 每个 numeric cell（按 行标签 × 列头 定位）在证据 JSON / 表格外正文中
     找支撑；无支撑 → 人工复核清单（MAJOR，与 R2c/R3 同款裁决哲学）
  3. 列内混精度探测：同列小数位数差 ≥2（如 0.92 与 92.1）→ 结构异常
     提示（INFO 级，可能是百分数/小数混用或复制错误）
  4. caption 小数沿用 R2c 口径（图注噪音豁免 + 三级支撑链）

复用 number_reconcile 的数字采集与噪音分类，保证与 R3/R2c 口径一致。

用法:
    python table_check.py --tex main.tex [--evidence-dirs results] --out audit_out
    python table_check.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from number_reconcile import (
    collect_numbers,
    collect_tex_rows,
    classify_noise,
    find_support,
)

TABLE_ENV_RE = re.compile(r"\\begin\{(table\*?)\}(.*?)\\end\{\1\}", re.S)
TABULAR_RE = re.compile(r"\\begin\{(tabular\*?|tabularx|longtable)\}(.*?)(?:\\end\{\1\})", re.S)
CAPTION_RE = re.compile(r"\\caption\s*(?:\[[^\]]*\])?\s*\{")
INPUT_RE = re.compile(r"\\(?:input|InputIfFileExists)\s*\{([^{}]+)\}")
CELL_NUM_RE = re.compile(r"\d+(?:\.\d+)?")
LABEL_NUM_NOISE_RE = re.compile(
    r"(?i)\b(figure|fig|figs|table|tab|section|sec|eq|appendix)\.?\s+\d+(\.\d+)?\b")


def _brace_block(s: str, open_idx: int) -> tuple[str, int]:
    depth = 0
    for i in range(open_idx, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return s[open_idx + 1:i], i + 1
    return s[open_idx + 1:], len(s)


def _clean_cell(cell: str) -> str:
    """cell 内容 → 纯文本：去命令保留参数、去 math 定界符。"""
    s = re.sub(r"\\(?:textbf|textit|emph|texttt|text|mathrm|mathbf)\{([^{}]*)\}", r"\1", cell)
    s = re.sub(r"\\cite[a-z]*\s*(?:\[[^\]]*\])?\{[^{}]*\}", "", s)
    s = re.sub(r"\\ref\{[^{}]*\}", "", s)
    s = re.sub(r"\\[a-zA-Z]+", " ", s)          # 其余裸命令
    s = s.replace("$", " ").replace("\\", " ")
    s = re.sub(r"[%~]", " ", s)
    return s.strip()


def _split_cells(row: str) -> list[str]:
    cells, buf, depth = [], [], 0
    for ch in row:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        if ch == "&" and depth <= 0:
            cells.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    cells.append("".join(buf))
    return cells


def parse_table(env_body: str) -> dict:
    """解析单个 table 环境：caption / 表格行（含行标签与列头）。"""
    cap = ""
    cm = CAPTION_RE.search(env_body)
    if cm:
        cap, _ = _brace_block(env_body, cm.end() - 1)

    tab = TABULAR_RE.search(env_body)
    rows_out: list[dict] = []
    if tab:
        body = tab.group(2)
        body = re.sub(r"\\toprule|\\midrule|\\bottomrule|\\hline", " ", body)
        body = re.sub(r"\\multicolumn\s*\{[^{}]*\}\s*\{[^{}]*\}\s*\{([^{}]*)\}", r"\1", body)
        body = re.sub(r"\\multirow\s*\{[^{}]*\}\s*\{[^{}]*\}\s*\{([^{}]*)\}", r"\1", body)
        raw_rows = re.split(r"\\\\(?:\[[^\]]*\])?", body)
        parsed = [_split_cells(r) for r in raw_rows]
        parsed = [[_clean_cell(c) for c in cells] for cells in parsed if any(c.strip() for c in cells)]

        first_data = None
        for i, cells in enumerate(parsed):
            if any(CELL_NUM_RE.fullmatch(c) or _is_numeric_cell(c) for c in cells):
                first_data = i
                break
        header_rows = parsed[:first_data] if first_data is not None else parsed[:1]
        headers = [" / ".join(dict.fromkeys(filter(None, (r[j] if j < len(r) else "" for r in header_rows))))
                   for j in range(max((len(r) for r in parsed), default=0))]

        for cells in (parsed[first_data:] if first_data is not None else parsed[1:]):
            row_label = cells[0] if cells and not _is_numeric_cell(cells[0]) else ""
            for j, c in enumerate(cells):
                if _is_numeric_cell(c):
                    rows_out.append({"label": row_label, "col": headers[j] if j < len(headers) else f"col{j}",
                                     "text": c})
    return {"caption": cap, "cells": rows_out, "has_tabular": tab is not None}


def _is_numeric_cell(c: str) -> bool:
    """cell 去掉 ±/()/%/-- 修饰后是否整体为一个数字。"""
    s = c.strip().replace(",", "")
    s = re.sub(r"^\((.*)\)$", r"\1", s)          # 括号负数 (0.92)
    if s in ("", "-", "--", "---", "–", "—", "n/a", "N/A", "NA"):
        return False
    return bool(re.fullmatch(r"[±~≈<>≤≥]?\s*-?\d+(?:\.\d+)?\s*%?", s))


def _cell_value(c: str) -> float | None:
    s = c.strip().replace(",", "").rstrip("%")
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    if not m:
        return None
    try:
        return float(m.group(0))
    except ValueError:
        return None


def caption_noise(row: dict) -> str | None:
    if LABEL_NUM_NOISE_RE.search(row["context"]):
        m = LABEL_NUM_NOISE_RE.search(row["context"])
        if row["token"] in m.group(0):
            return "label-number"
    return classify_noise(row)


def check(tex_path: Path, evidence_dirs: list[Path]) -> dict:
    tex = tex_path.read_text(encoding="utf-8", errors="replace")
    tex_dir = tex_path.parent
    tex_nocomment = re.sub(r"(?<!\\)%.*", "", tex)

    tables, missing_inputs, pending, anomalies = [], [], [], []

    # 表格外正文（供 cell 支撑链；掩掉全部 table 环境避免"表格数字支撑自己"）
    masked = tex_nocomment
    env_spans = [m.span() for m in TABLE_ENV_RE.finditer(tex_nocomment)]
    for a, b in env_spans:
        masked = masked[:a] + " " * (b - a) + masked[b:]
    body_rows = [r for r in collect_tex_rows(masked) if classify_noise(r) is None]
    body_tuples = [(r["token"], r["value"]) for r in body_rows]

    evidence = collect_numbers(evidence_dirs)
    ev_tuples = [(str(e["value"]), e["value"]) for e in evidence]

    for m in TABLE_ENV_RE.finditer(tex_nocomment):
        env = m.group(2)
        line = tex_nocomment.count("\n", 0, m.start()) + 1

        # 1) \input 文件存在性
        for im in INPUT_RE.finditer(env):
            p = im.group(1).strip()
            if not (tex_dir / p).is_file() and not (tex_dir / (p + ".tex")).is_file():
                missing_inputs.append({"line": line, "path": p, "issue": "表内 \\input 引用但磁盘未找到"})

        # 2) caption 小数（R2c 口径）
        parsed = parse_table(env)
        cap_clean = re.sub(r"\\[a-zA-Z]+\s?", " ", parsed["caption"])
        cap_rows = collect_tex_rows(cap_clean)
        cap_out = []
        for r in cap_rows:
            if caption_noise(r) is not None:
                continue
            if find_support(r["value"], ev_tuples):
                sup = "evidence"
            elif find_support(r["value"], body_tuples):
                sup = "body"
            else:
                sup = "unsupported"
                pending.append({**r, "table_line": line, "where": "caption"})
            cap_out.append({"token": r["token"], "support": sup})

        # 3) numeric cells 支撑链 + 列内混精度
        cells_out, col_decimals = [], {}
        for c in parsed["cells"]:
            v = _cell_value(c["text"])
            if v is None:
                continue
            rec = {"row": c["label"][:40], "col": c["col"][:40], "text": c["text"], "value": v}
            if find_support(v, ev_tuples):
                rec["support"] = "evidence"
            elif find_support(v, body_tuples):
                rec["support"] = "body"
            else:
                rec["support"] = "unsupported"
                pending.append({"token": c["text"], "value": v, "line": line,
                                "context": f"[{c['label']} × {c['col']}] = {c['text']}",
                                "table_line": line, "where": "cell"})
            cells_out.append(rec)
            if "." in c["text"]:
                col_decimals.setdefault(c["col"], []).append(len(c["text"].split(".")[1].split()[0]))
        for col, decs in col_decimals.items():
            if len(set(decs)) >= 2 and max(decs) - min(decs) >= 2:
                anomalies.append({"table_line": line, "col": col[:40],
                                  "decimals": sorted(set(decs)),
                                  "issue": "同列小数位数差 ≥2（疑似百分数/小数混用或复制错误）"})

        tables.append({"line": line, "has_tabular": parsed["has_tabular"],
                       "caption": parsed["caption"][:150],
                       "caption_decimals": cap_out, "cells": cells_out})

    n_cells = sum(len(t["cells"]) for t in tables)
    n_unsup = len(pending)
    verdict = ("CRITICAL" if missing_inputs else "MAJOR" if n_unsup else "PASS")
    return {
        "meta": {"tex": str(tex_path), "evidence_dirs": [str(d) for d in evidence_dirs],
                 "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")},
        "tables": tables,
        "missing_inputs": missing_inputs,
        "pending_review": pending,
        "precision_anomalies": anomalies,
        "summary": {
            "verdict": verdict,
            "tables": len(tables),
            "numeric_cells": n_cells,
            "unsupported": n_unsup,
            "missing_inputs": len(missing_inputs),
            "precision_anomalies": len(anomalies),
            "note": "pending_review = 表格 cell/图注数字在证据与表格外正文中均无支撑；"
                    "precision_anomalies = 列内混精度（INFO，人工扫一眼）",
        },
    }


def write_md(report: dict, out_md: Path) -> None:
    s = report["summary"]
    lines = [
        "# 表格数字核验报告（R2d）",
        "",
        f"- 论文：`{report['meta']['tex']}`，证据目录："
        f"{', '.join('`'+d+'`' for d in report['meta']['evidence_dirs']) or '（无）'}",
        f"- 结论：**{s['verdict']}**（表 {s['tables']} 个，numeric cell {s['numeric_cells']} 个，"
        f"无支撑 {s['unsupported']}，\\input 缺失 {s['missing_inputs']}，混精度列 {s['precision_anomalies']}）",
        "",
        "## 表清单",
        "",
        "| 表（行号） | tabular | caption 小数（支撑） | cell 数 |",
        "|---|---|---|---|",
    ]
    for t in report["tables"]:
        caps = t.get("caption_decimals", [])
        cap_str = ", ".join(f"{c['token']}({c['support'][:4]})" for c in caps[:8]) or "-"
        lines.append(f"| L{t['line']} | {'是' if t['has_tabular'] else '否'} | {cap_str} | {len(t['cells'])} |")
    if report["missing_inputs"]:
        lines += ["", "## 缺失 \\input 文件（编译即断 = Critical）", ""]
        lines += [f"- L{m['line']} `{m['path']}`：{m['issue']}" for m in report["missing_inputs"]]
    pend = report["pending_review"]
    if pend:
        lines += ["", "## 表格数字人工复核清单（无任何支撑）", ""]
        lines += [f"- L{p.get('table_line', p.get('line'))} [{p.get('where', 'cell')}] `{p['token']}`：{p['context'][:90]}"
                  for p in pend[:80]]
        if len(pend) > 80:
            lines.append(f"- ……共 {len(pend)} 个，见 JSON")
    if report["precision_anomalies"]:
        lines += ["", "## 列内混精度（INFO）", ""]
        lines += [f"- L{a['table_line']} 列「{a['col']}」：小数位 {a['decimals']}——{a['issue']}"
                  for a in report["precision_anomalies"]]
    out_md.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    import tempfile

    tmp = Path(tempfile.mkdtemp())
    tex = tmp / "main.tex"
    ev = tmp / "results"
    ev.mkdir()
    (ev / "tbl.json").write_text(json.dumps({"model_a": 0.923, "model_b": 0.711}), encoding="utf-8")

    tex.write_text(
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "Body mentions 0.923 and 0.711 for reference.\n"
        "\\begin{table}[t]\n"
        "\\caption{Accuracy on Judge40. Best is 0.923.}\n"
        "\\label{tab:main}\n"
        "\\begin{tabular}{lcc}\n"
        "\\toprule\n"
        "Model & Acc & F1 \\\\\n"
        "\\midrule\n"
        "A & 0.923 & 0.711 \\\\\n"
        "B & 0.88 & 91.2 \\\\\n"
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "\\end{table}\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    rep = check(tex, [ev])
    s = rep["summary"]
    # 0.923/0.711 evidence 支撑；0.88 与 91.2 无支撑 → MAJOR；Acc 列混精度（2 vs 1）
    assert s["verdict"] == "MAJOR", s
    assert s["tables"] == 1 and s["numeric_cells"] == 4, s
    toks = {p["token"]: p for p in rep["pending_review"]}
    assert "0.88" in toks and "91.2" in toks, toks
    assert toks["0.88"]["context"] == "[B × Acc] = 0.88", toks["0.88"]
    assert not any(p["token"] == "0.923" for p in rep["pending_review"]), toks
    assert any(a["col"].startswith("F1") for a in rep["precision_anomalies"]), rep["precision_anomalies"]
    # caption 0.923 有 evidence 支撑，不进 pending
    assert not any(p.get("where") == "caption" for p in rep["pending_review"]), rep["pending_review"]

    # 缺失 \input → CRITICAL
    tex.write_text(tex.read_text(encoding="utf-8").replace(
        "\\begin{table}[t]", "\\begin{table}[t]\n\\input{gen_table_missing.tex}\n"), encoding="utf-8")
    rep2 = check(tex, [ev])
    assert rep2["summary"]["verdict"] == "CRITICAL", rep2["summary"]
    assert any(m["path"] == "gen_table_missing.tex" for m in rep2["missing_inputs"]), rep2["missing_inputs"]

    # 存在的 \input + 全支撑 + 无混精度 → PASS
    good = tmp / "gen_table.tex"
    good.write_text("A & 0.923 \\\\\n", encoding="utf-8")
    tex.write_text(
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "Body 0.923.\n"
        "\\begin{table}\n\\caption{Results.}\n\\input{gen_table.tex}\n\\end{table}\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    rep3 = check(tex, [ev])
    assert rep3["summary"]["verdict"] == "PASS", rep3["summary"]
    assert not rep3["missing_inputs"], rep3["missing_inputs"]

    # 无表格论文 → PASS
    tex.write_text("No tables, just $0.5$ text.\n", encoding="utf-8")
    rep4 = check(tex, [])
    assert rep4["summary"]["verdict"] == "PASS" and rep4["summary"]["tables"] == 0, rep4["summary"]

    out = tmp / "out"
    out.mkdir()
    write_md(rep, out / "table_check.md")
    assert (out / "table_check.md").exists()
    print("table_check selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tex", type=Path)
    ap.add_argument("--evidence-dirs", type=str, default="")
    ap.add_argument("--out", type=Path, default=Path("audit_out"))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.tex:
        ap.error("--tex is required (or --selftest)")
    dirs = [Path(p) for p in args.evidence_dirs.split(",") if p.strip()]
    report = check(args.tex, dirs)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "table_check.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(report, args.out / "table_check.md")
    s = report["summary"]
    print(f"verdict={s['verdict']} tables={s['tables']} cells={s['numeric_cells']} "
          f"unsupported={s['unsupported']} missing_inputs={s['missing_inputs']} "
          f"precision_anomalies={s['precision_anomalies']}")
    print(f"report -> {args.out / 'table_check.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
