import os
"""S5 五轮制达标审计：整轮>=5 + 末轮>=8 + 0 Critical（9 篇）。供目标完成判据用。"""
import json
from pathlib import Path

PAPERS = ["just-agent-60", "mem0", "agent-comparison", "codeact-vs-fc", "scievalsuite",
          "kg-retrieval", "selfevolve-agent", "10paradigm-os", "calibration-self-improvement"]
BASE = Path(os.environ.get("QONE_PAPERS_DIR", "./papers"))

print(f"{'paper':28} {'rounds':>6} {'last':>4} {'crit_last':>9} {'PASS5':>6} {'PASS8':>6}")
allok = True
for p in PAPERS:
    try:
        rounds = [json.loads(l) for l in (BASE / p / "reviews/pipeline_S5/rounds_ledger.jsonl").read_text().splitlines() if l.strip()]
    except FileNotFoundError:
        print(f"{p:28} {'MISSING LEDGER'}"); allok = False; continue
    n = len(rounds)
    last = rounds[-1]
    p5 = "Y" if n >= 5 else "n"
    p8 = "Y" if (last.get("overall") == "PASS" and last.get("score", 0) >= 8) else "n"
    crit = last.get("criticals", "?")
    # 0 Critical 全轮检查：任一轮 criticals>0 即标出
    bad = [r["round"] for r in rounds if isinstance(r.get("criticals"), int) and r["criticals"] > 0]
    flag = "" if (p5 == "Y" and p8 == "Y" and not bad) else "  <-- GAP"
    if flag:
        allok = False
    print(f"{p:28} {n:>6} {last.get('score'):>4} {str(crit):>9} {p5:>6} {p8:>6}{flag}"
          + (f" crit_rounds={bad}" if bad else ""))
print("OVERALL:", "ALL PASS" if allok else "GAPS REMAIN")
