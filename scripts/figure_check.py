# -*- coding: utf-8 -*-
"""图表数字核验（figure_check）— 审稿工作流 v2.0。

图是证据链上最常被"眼睛跳过"的一环：正文数字对得上，图却可能用了另一版
数据（stale figure）。本模块做三件事：
  1. 图文件存在性：tex 引用 \\includegraphics 但磁盘无文件 → 编译即断 = CRITICAL
  2. 图内嵌数字（矢量 PDF 图的文本层）↔ 图注/论文正文/证据 JSON 三方对账：
     - 图注小数无任何支撑（图文本 / 证据 / 正文都没有）→ 人工复核清单（MAJOR）
     - 图内高精度统计值在论文与证据中均不出现 → figure_only 提示（INFO：柱上
       数据标签不进正文属正常，仅提示人工扫一眼）
  3. 位图（PNG/JPG）无文本层 → 明示 SKIP（不误报，不装懂）

复用 number_reconcile 的数字采集与噪音分类，保证与 R3 口径一致。

用法:
    python figure_check.py --tex main.tex [--evidence-dirs results] --out audit_out
    python figure_check.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from number_reconcile import (
    DEC_RE,
    collect_numbers,
    collect_tex_rows,
    classify_noise,
    find_support,
)

FIG_ENV_RE = re.compile(r"\\begin\{(figure\*?)\}(.*?)\\end\{\1\}", re.S)
INCGRAPH_RE = re.compile(r"\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^{}]+)\}")
CAPTION_RE = re.compile(r"\\caption\s*(?:\[[^\]]*\])?\s*\{")
GRAPHICSPATH_RE = re.compile(r"\\graphicspath\s*\{([^}]*)\}")
GPATH_ENTRY_RE = re.compile(r"\{([^{}]*)\}")
FIG_EXTS = [".pdf", ".png", ".jpg", ".jpeg", ".eps"]
LABEL_NUM_NOISE_RE = re.compile(
    r"(?i)\b(figure|fig|figs|table|tab|section|sec|eq|appendix)\.?\s+\d+(\.\d+)?\b")


def _brace_block(s: str, open_idx: int) -> tuple[str, int]:
    """open_idx 指向 '{'；返回（内容, 右花括号位置+1）。容错未闭合。"""
    depth = 0
    for i in range(open_idx, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return s[open_idx + 1:i], i + 1
    return s[open_idx + 1:], len(s)


def parse_figures(tex: str) -> tuple[list[dict], list[tuple[int, int]]]:
    """返回（图条目列表, 图注绝对 span 列表）。图注挂在同环境所有 includegraphics 上。"""
    figs: list[dict] = []
    cap_spans: list[tuple[int, int]] = []
    env_spans = [m.span() for m in FIG_ENV_RE.finditer(tex)]

    for m in FIG_ENV_RE.finditer(tex):
        env = m.group(2)
        base = m.start(2)
        cap = ""
        cm = CAPTION_RE.search(env)
        if cm:
            cap, _ = _brace_block(env, cm.end() - 1)
            start = base + cm.end() - 1
            cap_spans.append((start, start + len(cap) + 2))
        for g in INCGRAPH_RE.finditer(env):
            figs.append({"path": g.group(1).strip(), "caption": cap, "env": "figure",
                         "line": tex.count("\n", 0, m.start()) + 1})

    for g in INCGRAPH_RE.finditer(tex):  # 环境外独立小图（表内插图等）
        if any(a <= g.start() < b for a, b in env_spans):
            continue
        figs.append({"path": g.group(1).strip(), "caption": "", "env": "inline",
                     "line": tex.count("\n", 0, g.start()) + 1})
    return figs, cap_spans


def graphics_paths(tex: str, tex_dir: Path) -> list[Path]:
    roots = [tex_dir]
    for m in GRAPHICSPATH_RE.finditer(tex):
        for e in GPATH_ENTRY_RE.finditer(m.group(1)):
            p = Path(e.group(1).strip())
            roots.append(p if p.is_absolute() else tex_dir / p)
    return roots


def resolve_figure(path_str: str, roots: list[Path]) -> Path | None:
    cand = [r / path_str for r in roots]
    if Path(path_str).suffix:
        for c in cand:
            if c.is_file():
                return c
        return None
    for c in cand:
        for ext in FIG_EXTS:
            if (c.with_suffix(ext) if c.suffix else c.parent / (c.name + ext)).is_file():
                return (c.with_suffix(ext) if c.suffix else c.parent / (c.name + ext))
    return None


def extract_pdf_text(pdf: Path) -> str:
    import pymupdf  # noqa: PLC0415  # 延迟导入：位图论文用不到

    parts = []
    with pymupdf.open(str(pdf)) as doc:
        for page in doc:
            parts.append(page.get_text("text"))
    return "\n".join(parts)


def caption_noise(row: dict) -> str | None:
    """图注专属噪音：Figure 2.3 / Table 4 之类的标签编号（R3 通用规则覆盖不到）。"""
    if LABEL_NUM_NOISE_RE.search(row["context"]):
        m = LABEL_NUM_NOISE_RE.search(row["context"])
        if row["token"] in m.group(0):
            return "label-number"
    return classify_noise(row)


def check(tex_path: Path, evidence_dirs: list[Path]) -> dict:
    tex = tex_path.read_text(encoding="utf-8", errors="replace")
    tex_dir = tex_path.parent
    roots = graphics_paths(tex, tex_dir)
    figs, cap_spans = parse_figures(tex)

    # 正文小数（掩掉图注本体，避免"图注数字支撑自己"的空转）
    masked = list(tex)
    for a, b in cap_spans:
        for i in range(a, min(b, len(masked))):
            if masked[i].isdigit() or masked[i] == ".":
                masked[i] = " "
    masked_tex = "".join(masked)
    body_rows = [r for r in collect_tex_rows(masked_tex) if classify_noise(r) is None]
    body_tuples = [(r["token"], r["value"]) for r in body_rows]

    # 全论文小数（含图注，用于 figure_only 判断：图内数字是否在论文任何地方出现）
    paper_tuples = [(r["token"], r["value"]) for r in collect_tex_rows(tex)
                    if classify_noise(r) is None]

    evidence = collect_numbers(evidence_dirs)
    ev_tuples = [(str(e["value"]), e["value"]) for e in evidence]

    figures, missing_files, pending, figure_only = [], [], [], []
    n_text, n_raster = 0, 0

    for f in figs:
        resolved = resolve_figure(f["path"], roots)
        entry = {"path": f["path"], "line": f["line"], "resolved": bool(resolved)}
        fig_text, kind = "", "missing"
        if resolved is None:
            missing_files.append({**f, "issue": "includegraphics 引用但磁盘未找到"})
        else:
            entry["abs"] = str(resolved)
            suffix = resolved.suffix.lower()
            if suffix == ".pdf":
                try:
                    fig_text = extract_pdf_text(resolved)
                except Exception as e:  # noqa: BLE001  # 损坏/加密 PDF
                    entry["extract_error"] = f"{type(e).__name__}: {e}"
                kind = "pdf"
            elif suffix in (".png", ".jpg", ".jpeg"):
                kind = "raster"
            else:
                kind = "other"

        fig_rows = [r for r in collect_tex_rows(fig_text)] if fig_text else []
        fig_tuples = [(r["token"], r["value"]) for r in fig_rows]
        entry.update({"kind": kind, "text_chars": len(fig_text),
                      "fig_decimals": len(fig_tuples),
                      "fig_numbers_sample": [t for t, _ in fig_tuples[:30]]})
        if kind == "pdf" and not entry.get("extract_error"):
            n_text += 1
        elif kind == "raster":
            n_raster += 1

        # 图注数字支撑：figtext → evidence → body → unsupported
        cap_rows = collect_tex_rows(f["caption"])
        cap_out = []
        for r in cap_rows:
            if caption_noise(r) is not None:
                continue
            if find_support(r["value"], fig_tuples):
                sup = "figtext"
            elif find_support(r["value"], ev_tuples):
                sup = "evidence"
            elif find_support(r["value"], body_tuples):
                sup = "body"
            else:
                sup = "unsupported"
                pending.append({**r, "figure": f["path"]})
            cap_out.append({"token": r["token"], "support": sup})
        entry["caption_decimals"] = cap_out
        entry["caption"] = re.sub(r"\s+", " ", f["caption"])[:200]

        # figure_only：图内高精度数（≥3 位小数，多为统计标注）在论文/证据中都不出现
        for tok, val in fig_tuples:
            if len(tok.split(".")[1]) < 3:
                continue
            if find_support(val, paper_tuples) or find_support(val, ev_tuples):
                continue
            figure_only.append({"figure": f["path"], "token": tok, "value": val})
        figures.append(entry)

    n_cap = sum(len(e.get("caption_decimals", [])) for e in figures)
    n_unsup = len(pending)
    verdict = ("CRITICAL" if missing_files else
               "MAJOR" if n_unsup else "PASS")
    return {
        "meta": {
            "tex": str(tex_path),
            "evidence_dirs": [str(d) for d in evidence_dirs],
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "figures": figures,
        "missing_files": missing_files,
        "caption_pending_review": pending,
        "figure_only_numbers": figure_only,
        "summary": {
            "verdict": verdict,
            "figures_referenced": len(figs),
            "text_extracted": n_text,
            "raster_skipped": n_raster,
            "missing": len(missing_files),
            "caption_decimals": n_cap,
            "unsupported": n_unsup,
            "figure_only": len(figure_only),
            "note": "caption_pending_review = 图注小数在图文本/证据/正文中均无支撑；"
                    "figure_only = 仅出现在图内的高精度数（数据标签属正常，人工扫一眼即可）",
        },
    }


def write_md(report: dict, out_md: Path) -> None:
    s = report["summary"]
    lines = [
        "# 图表数字核验报告（R2c）",
        "",
        f"- 论文：`{report['meta']['tex']}`，证据目录："
        f"{', '.join('`'+d+'`' for d in report['meta']['evidence_dirs']) or '（无）'}",
        f"- 结论：**{s['verdict']}**（图 {s['figures_referenced']} 幅：矢量文本提取 {s['text_extracted']}，"
        f"位图跳过 {s['raster_skipped']}，缺失 {s['missing']}；图注小数 {s['caption_decimals']} 个，"
        f"无支撑 {s['unsupported']}；figure_only {s['figure_only']} 个）",
        "",
        "## 图清单",
        "",
        "| 图 | 类型 | 文本提取 | 图注小数（支撑） |",
        "|---|---|---|---|",
    ]
    for e in report["figures"]:
        caps = e.get("caption_decimals", [])
        cap_str = ", ".join(f"{c['token']}({c['support'][:4]})" for c in caps[:8]) or "-"
        if len(caps) > 8:
            cap_str += f" 等{len(caps)}个"
        lines.append(f"| `{e['path']}` (L{e['line']}) | {e.get('kind', '?')} | "
                     f"{'是' if e.get('fig_decimals') is not None and e.get('kind') == 'pdf' else '否'} | {cap_str} |")
    if report["missing_files"]:
        lines += ["", "## 缺失图文件（编译即断 = Critical）", ""]
        lines += [f"- L{m['line']} `{m['path']}`：{m['issue']}" for m in report["missing_files"]]
    pend = report["caption_pending_review"]
    if pend:
        lines += ["", "## 图注数字人工复核清单（无任何支撑）", ""]
        lines += [f"- [{p['figure']}] L{p['line']} `{p['token']}`：{p['context'][:100]}" for p in pend[:60]]
        if len(pend) > 60:
            lines.append(f"- ……共 {len(pend)} 个，见 JSON")
    fo = report["figure_only_numbers"]
    if fo:
        lines += ["", "## figure_only（仅出现在图内的高精度数，INFO）", ""]
        lines += [f"- [{f['figure']}] `{f['token']}`" for f in fo[:40]]
        if len(fo) > 40:
            lines.append(f"- ……共 {len(fo)} 个")
    out_md.write_text("\n".join(lines), encoding="utf-8")


def _tiny_png(path: Path) -> None:
    import struct
    import zlib

    def chunk(t: bytes, d: bytes) -> bytes:
        return (struct.pack(">I", len(d)) + t + d
                + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    raw = b"\x00\xff\x00\x00"
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
                     + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def selftest() -> int:
    import tempfile

    tmp = Path(tempfile.mkdtemp())
    tex = tmp / "main.tex"

    import pymupdf
    fig_a = tmp / "fig_a.pdf"
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 100), "kappa 0.894")
    page.insert_text((72, 130), "power 0.0000")
    page.insert_text((72, 160), "bar label 3.14159")
    doc.save(str(fig_a))
    doc.close()

    fig_b = tmp / "figs" / "fig_b.png"
    fig_b.parent.mkdir()
    _tiny_png(fig_b)

    ev = tmp / "results"
    ev.mkdir()
    (ev / "cap.json").write_text(json.dumps({"claim": 5.55}), encoding="utf-8")

    tex.write_text(
        "\\documentclass{article}\n"
        "\\graphicspath{{figs/}}\n"
        "\\begin{document}\n"
        "Body reports kappa $0.894$ with power $0.0000$, and 1.25 elsewhere.\n"
        "\\begin{figure}\n"
        "\\includegraphics{fig_a.pdf}\n"
        "\\caption{Judge agreement $\\alpha=0.894$ (power $0.0000$). "
        "See Section 2.3 for details. Unbacked 5.55.}\n"
        "\\label{fig:a}\n"
        "\\end{figure}\n"
        "\\begin{figure}\n"
        "\\includegraphics[width=0.5\\textwidth]{figs/fig_b.png}\n"
        "\\caption{Raster figure with body-backed number 1.25.}\n"
        "\\end{figure}\n"
        "\\begin{figure}\n"
        "\\includegraphics{ghost.pdf}\n"
        "\\caption{Ghost figure reports 2.5 ms.}\n"
        "\\end{figure}\n"
        "\\end{document}\n",
        encoding="utf-8",
    )

    rep = check(tex, [ev])
    s = rep["summary"]

    # 缺失图文件 → CRITICAL
    assert any(m["path"] == "ghost.pdf" for m in rep["missing_files"]), rep["missing_files"]
    assert s["verdict"] == "CRITICAL", s
    # 矢量 PDF 文本提取到位
    fa = next(e for e in rep["figures"] if e["path"] == "fig_a.pdf")
    assert fa["kind"] == "pdf" and fa["fig_decimals"] >= 3, fa
    # 图注数字支撑链：0.894/0.0000 来自图文本；1.25 来自正文；位图无文本层
    cap = {c["token"]: c["support"] for c in fa["caption_decimals"]}
    assert cap.get("0.894") == "figtext" and cap.get("0.0000") == "figtext", cap
    fb = next(e for e in rep["figures"] if e["path"].endswith("fig_b.png"))
    assert fb["kind"] == "raster" and {c["token"]: c["support"] for c in fb["caption_decimals"]}["1.25"] == "body", fb
    # "Section 2.3" 标签编号 → 图注噪音，不进支撑统计
    assert "2.3" not in cap, cap
    # 5.55 有证据支撑（不进待复核）；ghost 图注的 2.5 无支撑 → 待复核
    assert not any(p["token"] == "5.55" for p in rep["caption_pending_review"]), rep["caption_pending_review"]
    assert any(p["token"] == "2.5" for p in rep["caption_pending_review"]), rep["caption_pending_review"]
    # 3.14159 仅在图内（论文/证据均无）→ figure_only
    assert any(f["token"] == "3.14159" for f in rep["figure_only_numbers"]), rep["figure_only_numbers"]

    # 去掉 ghost 图 + 撤掉 5.55 的证据 → 图注 5.55 无支撑 → MAJOR
    tex.write_text(tex.read_text(encoding="utf-8").replace(
        "\\begin{figure}\n\\includegraphics{ghost.pdf}\n\\caption{Ghost figure reports 2.5 ms.}\n\\end{figure}\n", ""), encoding="utf-8")
    rep2 = check(tex, [])
    assert rep2["summary"]["verdict"] == "MAJOR", rep2["summary"]
    assert any(p["token"] == "5.55" for p in rep2["caption_pending_review"]), rep2["caption_pending_review"]

    # 无图论文 → PASS
    tex.write_text("No figures here, just $0.5$ text.\n", encoding="utf-8")
    rep3 = check(tex, [])
    assert rep3["summary"]["verdict"] == "PASS" and rep3["summary"]["figures_referenced"] == 0, rep3["summary"]

    out = tmp / "out"
    out.mkdir()
    write_md(rep, out / "figure_check.md")
    assert (out / "figure_check.md").exists()
    print("figure_check selftest: OK")
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
    (args.out / "figure_check.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(report, args.out / "figure_check.md")
    s = report["summary"]
    print(f"verdict={s['verdict']} figures={s['figures_referenced']} "
          f"(text={s['text_extracted']} raster={s['raster_skipped']} missing={s['missing']}) "
          f"caption_decimals={s['caption_decimals']} unsupported={s['unsupported']} "
          f"figure_only={s['figure_only']}")
    print(f"report -> {args.out / 'figure_check.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
