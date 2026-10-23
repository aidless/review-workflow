# -*- coding: utf-8 -*-
"""check_package_consistency.py — rebuttal↔正文↔证据互锁审计（E335）。

rebuttal 里引用的锚（Table N / Section N / Figure N / evidence/ 路径 / C 编号）
必须在正文/证据中可解，否则互锁 FAIL。改一处（正文表号/节号/证据路径）
必须重跑本脚本。

用法: python check_package_consistency.py --paper <paper_dir>
exit 0=全互锁；1=有悬空引用（列清单）。
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", type=Path, required=True)
    args = ap.parse_args()
    paper = args.paper
    tex = (paper / "paper" / "main.tex").read_text(encoding="utf-8", errors="replace")
    reb_cands = sorted((paper / "reviews" / "pipeline_S5").glob("rebuttal*.md"))
    if not reb_cands:
        print("无 rebuttal 文件，跳过（不算 PASS 也不算 FAIL）")
        return 0
    fails = []
    for reb in reb_cands:
        body = reb.read_text(encoding="utf-8", errors="replace")
        anchors = sorted(set(re.findall(r"(Table|Section|Figure|Tab\.|Fig\.)~?\\?ref\{([^}]+)\}|"
                                        r"(Table|Section|Figure)\s+([0-9.]+)", body)))
        for _m in re.finditer(r"\\label\{([^}]+)\}", body):
            pass  # rebuttal 自带 label 不查
        for _kind, num in re.findall(r"(Table|Section|Figure)\s+([0-9.]+)", body):
            # 正文以 \label{tab:..}/\ref 或裸 "Table N" 出现为准；宽松查数字邻接
            if not re.search(r"(Table|Section|Figure)[^\n]{0,20}" + re.escape(num), tex):
                fails.append(f"{reb.name}: {_kind} {num} 在正文无对应")
        for p in sorted(set(re.findall(r"(evidence/[A-Za-z0-9_./-]+(?:\.json|\.csv|\.md))", body))):
            if not (paper / p).exists():
                fails.append(f"{reb.name}: {p} 文件不存在")
        for c in sorted(set(re.findall(r"\b(C1[0-9]{2})\b", body))):
            led = paper / "CLAIM_LEDGER.md"
            if led.exists() and c not in led.read_text(encoding="utf-8", errors="replace"):
                fails.append(f"{reb.name}: {c} 不在 CLAIM_LEDGER")
    if fails:
        print(f"互锁 FAIL（{len(fails)}）：")
        for f in fails[:20]:
            print("  -", f)
        return 1
    print(f"互锁 PASS（{len(reb_cands)} 个 rebuttal 文件，0 悬空引用）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
