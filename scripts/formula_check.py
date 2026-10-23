# -*- coding: utf-8 -*-
"""公式与算术核验（formula_check）— 审稿工作流 v2.1（R1d）。

论文推导正确性无法全自动验证（已知边界），但正文里两类"可机械核验的算术"
经常藏真实错误，本模块覆盖：

  1. 行内算术一致性：`45/50 = 0.90`、`12 × 3 = 36`、`3 + 4 = 7`、
     `(a+b)/c = d` 二元式、`X% of Y = Z`——重算并按结果位数容差比对；
     不符 → MISMATCH（人工复核清单）
  2. 括号百分数一致性：`0.894 (89.4%)`——值 × 100 应等于括号内百分数
     （单位漂移 / 手滑改数的常见藏身处）。只对 0-1 比例值生效：计数 + 百分数
     （如 `5 (20.6%)`）的基数不在本句，不可局部复算 → 跳过不误报
  3. 分数百分数一致性：`35/170 (20.6%)`——分子分母可直接重算
  4. 公式引用完整性：\\eqref/\\ref 指向不存在的 \\label → 悬空引用
     （编译警告级别，但审稿人应知道）

不覆盖（诚实边界）：符号推导、量纲分析、隐式步骤——留给 R6 文本层与人工。

用法:
    python formula_check.py --tex main.tex --out audit_out
    python formula_check.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

NUM = r"(\d[\d,]*(?:\.\d+)?)"
ARITH_RE = re.compile(
    NUM + r"\s*([+\u00d7\u00f7*/])\s*" + NUM + r"\s*=\s*" + NUM)
PAREN_PCT_RE = re.compile(r"(?<!@)" + NUM + r"\s*\(\s*(\d[\d]*(?:\.\d+)?)\s*%?\s*\\?%\s*\)")
FRAC_PCT_RE = re.compile(
    NUM + r"\s*/\s*" + NUM + r"\s*\(\s*(\d[\d]*(?:\.\d+)?)\s*%?\s*\\?%\s*\)")
PCT_OF_RE = re.compile(NUM + r"\s*\\?%\s*of\s*" + NUM + r"\s*=\s*" + NUM, re.I)
LABEL_RE = re.compile(r"\\label\s*\{([^{}]+)\}")
REF_RE = re.compile(r"\\(?:eqref|\bref)\s*\{([^{}]+)\}")
OP = {"+": lambda a, b: a + b, "\u00d7": lambda a, b: a * b, "*": lambda a, b: a * b,
      "/": lambda a, b: a / b, "\u00f7": lambda a, b: a / b}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _num(s: str) -> float:
    return float(s.replace(",", ""))


def _tol(result_token: str) -> float:
    """按写出的结果位数给舍入容差（如 0.90 → ±0.005）。"""
    if "." in result_token:
        return 0.5 * 10 ** -len(result_token.split(".")[1]) + 1e-12
    return 0.5 + 1e-12


def _line_of(tex: str, idx: int) -> int:
    return tex.count("\n", 0, idx) + 1


def check(tex_path: Path) -> dict:
    raw = tex_path.read_text(encoding="utf-8", errors="replace")
    tex = re.sub(r"(?<!\\)%.*", "", raw)          # 去注释
    # 去掉 label/ref 定义本身的数字干扰：只做行内算术，不碰 display math 的定义体
    text_no_math = re.sub(r"\$\$.*?\$\$", " ", tex, flags=re.S)
    text_no_math = re.sub(r"\\\[.*?\\\]", " ", text_no_math, flags=re.S)

    mismatches, checks_ok = [], []

    for m in ARITH_RE.finditer(text_no_math):
        a, op, b, c = m.group(1), m.group(2), m.group(3), m.group(4)
        if op == "-" and not (m.string[m.start(2) - 1] == " " and m.string[m.end(2)] == " "):
            continue                              # 无空格减号多为区间（3-5 items）
        try:
            true = OP[op](_num(a), _num(b))
        except ZeroDivisionError:
            continue
        got = _num(c)
        # "=30\%" 表示百分比：3/10=30% ⇔ 0.3×100=30，非 "30 单位"
        if m.string[m.end():m.end() + 2] == r"\%":
            true = true * 100
        if abs(true - got) > _tol(c):
            mismatches.append({"expr": m.group(0), "recomputed": round(true, 6),
                               "reported": got, "line": _line_of(text_no_math, m.start()),
                               "kind": "arith"})
        else:
            checks_ok.append(m.group(0))

    for m in PCT_OF_RE.finditer(text_no_math):
        pct, base, res = _num(m.group(1)) / 100, _num(m.group(2)), _num(m.group(3))
        if abs(pct * base - res) > _tol(m.group(3)):
            mismatches.append({"expr": m.group(0), "recomputed": round(pct * base, 6),
                               "reported": res, "line": _line_of(text_no_math, m.start()),
                               "kind": "percent-of"})

    for m in PAREN_PCT_RE.finditer(text_no_math):
        val, pct = _num(m.group(1)), _num(m.group(2))
        if not (0 < val <= 1):
            continue  # 非 0-1 比例（计数/指标参数）：百分数基数不在本句，不可局部复算
        if abs(val * 100 - pct) > _tol(m.group(2)):
            mismatches.append({"expr": m.group(0), "recomputed": round(val * 100, 6),
                               "reported": pct, "line": _line_of(text_no_math, m.start()),
                               "kind": "paren-percent"})
        else:
            checks_ok.append(m.group(0))

    for m in FRAC_PCT_RE.finditer(text_no_math):
        a, b, pct = _num(m.group(1)), _num(m.group(2)), _num(m.group(3))
        if b == 0:
            continue
        true = a / b * 100
        if abs(true - pct) > _tol(m.group(3)):
            mismatches.append({"expr": m.group(0), "recomputed": round(true, 6),
                               "reported": pct, "line": _line_of(text_no_math, m.start()),
                               "kind": "frac-percent"})
        else:
            checks_ok.append(m.group(0))

    labels = set(LABEL_RE.findall(tex))
    dangling = []
    for m in REF_RE.finditer(tex):
        for key in m.group(1).split(","):
            key = key.strip()
            if key and key not in labels:
                dangling.append({"ref": key, "line": _line_of(tex, m.start())})

    verdict = "MAJOR" if mismatches else ("MINOR" if dangling else "PASS")
    return {
        "meta": {"tex": str(tex_path), "timestamp": now()},
        "arith_checks": checks_ok,
        "mismatches": mismatches,
        "dangling_refs": dangling,
        "summary": {
            "verdict": verdict,
            "arith_total": len(checks_ok) + len(mismatches),
            "arith_mismatch": len(mismatches),
            "paren_pct_mismatch": sum(1 for x in mismatches if x["kind"] == "paren-percent"),
            "dangling_refs": len(dangling),
            "note": "MISMATCH = 行内算术重算与论文写出的结果不符（按结果位数舍入容差）；"
                    "符号推导/量纲/隐式步骤不在机械覆盖内（R6 文本层 + 人工）",
        },
    }


def write_md(report: dict, out_md: Path) -> None:
    s = report["summary"]
    lines = [
        "# 公式与算术核验报告（R1d）",
        "",
        f"- 论文：`{report['meta']['tex']}`",
        f"- 结论：**{s['verdict']}**（行内算术 {s['arith_total']} 处：不符 {s['arith_mismatch']}"
        f"（含括号百分数 {s['paren_pct_mismatch']}）；悬空引用 {s['dangling_refs']}）",
        "",
        "覆盖边界：行内算术重算 + 括号百分数一致性 + 公式引用完整性；"
        "符号推导与量纲分析不在机械覆盖内（见 R6 文本层与人工审）。",
        "",
    ]
    if report["mismatches"]:
        lines += ["## 算术不符（人工复核：单位漂移 / 手滑改数 / 误报）", ""]
        lines += [f"- L{m['line']} `{m['expr']}` → 重算 {m['recomputed']}，论文写 {m['reported']}"
                  f"（{m['kind']}）" for m in report["mismatches"]]
    if report["dangling_refs"]:
        lines += ["", "## 悬空引用（\\ref 指向不存在的 label）", ""]
        lines += [f"- L{d['line']} `\\ref{{{d['ref']}}}`" for d in report["dangling_refs"]]
    if not report["mismatches"] and not report["dangling_refs"]:
        lines.append("全部行内算术与公式引用一致，无悬空引用。")
    out_md.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    import tempfile

    tmp = Path(tempfile.mkdtemp())
    tex = tmp / "main.tex"
    tex.write_text(
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "Correct: 45/50 = 0.90 and 12 \\texttimes{} 3 = 36; range 3-5 items stays quiet.\n"
        "Percent ok: 0.894 (89.4\\%).\n"
        "Percent-eq ok: 3/10 = 30\\%.\n"
        "Wrong: 45/50 = 0.92 and 0.894 (88.0\\%).\n"
        "Metric notation stays quiet: 35/170 Hit@5 (20.6\\%), count 5 (20.6\\%).\n"
        "Fraction pct: 35/170 (20.6\\%) ok; 35/170 (21.5\\%) wrong.\n"
        "Equation \\eqref{eq:good} is fine, but \\eqref{eq:ghost} dangles.\n"
        "\\begin{equation}\\label{eq:good} e = mc^2 \\end{equation}\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    rep = check(tex)
    s = rep["summary"]
    # 45/50=0.92、0.894(88.0%)、35/170(21.5%) 三处不符 → MAJOR；eq:ghost 悬空
    # Hit@5 (20.6%) 与计数 5 (20.6%) 不得误报（基数不在本句）
    assert s["verdict"] == "MAJOR", s
    kinds = {m["kind"] for m in rep["mismatches"]}
    assert kinds == {"arith", "paren-percent", "frac-percent"}, rep["mismatches"]
    assert any(m["expr"].startswith("45/50") for m in rep["mismatches"]), rep["mismatches"]
    assert any("88.0" in m["expr"] for m in rep["mismatches"]), rep["mismatches"]
    assert any("21.5" in m["expr"] and m["kind"] == "frac-percent" for m in rep["mismatches"]), rep["mismatches"]
    assert not any("Hit@5" in m["expr"] or "(20.6" in m["expr"] for m in rep["mismatches"]), rep["mismatches"]
    assert not any(m["expr"].startswith("45/50 = 0.90") for m in rep["mismatches"]), rep["mismatches"]
    assert any(d["ref"] == "eq:ghost" for d in rep["dangling_refs"]), rep["dangling_refs"]
    assert not any(d["ref"] == "eq:good" for d in rep["dangling_refs"]), rep["dangling_refs"]
    assert any("0.90" in c for c in rep["arith_checks"]), rep["arith_checks"]
    assert any("3/10 = 30" in c for c in rep["arith_checks"]), rep["arith_checks"]  # "=30\%" 百分比，不得误报
    assert any("35/170 (20.6" in c for c in rep["arith_checks"]), rep["arith_checks"]

    # 无错误 → PASS；仅悬空 → MINOR
    tex.write_text("All good: 45/50 = 0.90, 0.894 (89.4\\%), 35/170 (20.6\\%).\n", encoding="utf-8")
    assert check(tex)["summary"]["verdict"] == "PASS"
    tex.write_text("Ref \\ref{eq:ghost} only.\n", encoding="utf-8")
    assert check(tex)["summary"]["verdict"] == "MINOR"

    out = tmp / "out"
    out.mkdir()
    write_md(rep, out / "formula_check.md")
    assert (out / "formula_check.md").exists()
    print("formula_check selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tex", type=Path)
    ap.add_argument("--out", type=Path, default=Path("audit_out"))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.tex:
        ap.error("--tex is required (or --selftest)")
    report = check(args.tex)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "formula_check.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(report, args.out / "formula_check.md")
    s = report["summary"]
    print(f"verdict={s['verdict']} arith={s['arith_total']} mismatch={s['arith_mismatch']} "
          f"dangling_refs={s['dangling_refs']}")
    print(f"report -> {args.out / 'formula_check.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
