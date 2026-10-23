# -*- coding: utf-8 -*-
"""PDF 文本提取（pdf_text）— 审稿工作流 v1.2 输入扩展。

无 tex 源码的投稿（PDF-only 审稿场景）提取文本，供 R1 静态审查 / R3 方向 B 数字对账使用。
提取文本是"伪 tex"：LaTeX 命令已不存在，因此 R2 引用审计在此模式下自动降级为 SKIP。

用法:
    python pdf_text.py --pdf main.pdf --out extracted.txt
    python pdf_text.py --pdf main.pdf --stats          # 只看提取统计（页数/字符数/数字数）
    python pdf_text.py --selftest
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

DEC_RE = re.compile(r"\d+\.\d+")
NOISE_RE = re.compile(r"^\s*(\d+|[A-Z])\s*$")


def extract_text(pdf_path: Path) -> str:
    import pymupdf

    pages = []
    with pymupdf.open(str(pdf_path)) as doc:
        for page in doc:
            pages.append(page.get_text("text"))
    # 页间分隔：空行保留段落结构，剔除单字符行（页码/栏标）
    out = []
    for p in pages:
        lines = [l.rstrip() for l in p.splitlines()]
        out.append("\n".join(l for l in lines if not NOISE_RE.match(l)))
    return "\n\n".join(out)


def extract_stats(text: str) -> dict:
    return {
        "chars": len(text),
        "lines": len(text.splitlines()),
        "decimals": len(DEC_RE.findall(text)),
    }


def selftest() -> int:
    import tempfile

    import pymupdf

    tmp = Path(tempfile.mkdtemp())
    pdf = tmp / "doc.pdf"
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 96), "Mean goal 0.1418 with p=1.0000.")
    page.insert_text((72, 120), "Wilson CI [0.4901, 0.9433] for 8/10.")
    doc.save(str(pdf))
    doc.close()

    text = extract_text(pdf)
    assert "0.1418" in text and "1.0000" in text, text
    assert "0.4901" in text and "0.9433" in text, text
    stats = extract_stats(text)
    assert stats["decimals"] >= 4, stats
    print("pdf_text selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pdf", type=Path)
    ap.add_argument("--out", type=Path, help="提取文本落盘路径（默认 <pdf同名>.txt）")
    ap.add_argument("--stats", action="store_true", help="只输出提取统计，不落盘")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.pdf:
        ap.error("--pdf required (or --selftest)")
    text = extract_text(args.pdf)
    stats = extract_stats(text)
    print(f"pages->chars={stats['chars']} lines={stats['lines']} decimals={stats['decimals']}")
    if not args.stats:
        out = args.out or args.pdf.with_suffix(".txt")
        out.write_text(text, encoding="utf-8")
        print(f"-> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
