import os
"""首屏审计：每篇的关键证据数字是否落在 PRISM 视野（前 REVIEW_LLM_MAX_CHARS=6000 字符）内。
输出每篇 ledger verified 数字在首屏的命中率 + 缺失清单（指导摘要/前置改写）。"""
import json, os, re
from pathlib import Path

PAPERS = ["just-agent-60", "mem0", "agent-comparison", "codeact-vs-fc", "scievalsuite",
          "kg-retrieval", "selfevolve-agent", "10paradigm-os", "calibration-self-improvement"]
BASE = Path(os.environ.get("QONE_PAPERS_DIR", "./papers"))
MAXC = int(os.environ.get("REVIEW_LLM_MAX_CHARS", "6000"))

for p in PAPERS:
    tex = (BASE / p / "paper/main.tex").read_text(encoding="utf-8", errors="replace")
    head = tex[:MAXC]
    try:
        adj = json.loads((BASE / p / "reviews/pipeline_S5/adjudications.json").read_text())
    except FileNotFoundError:
        print(f"{p}: 无裁决文件"); continue
    keys = [k for k, v in adj.items()
            if not k.startswith("_") and isinstance(v, dict) and v.get("verdict") == "supported"]
    hit = [k for k in keys if k in head]
    miss = [k for k in keys if k not in head]
    print(f"{p}: 首屏 {len(hit)}/{len(keys)}")
    if miss:
        print("   缺失:", ", ".join(miss[:14]))
