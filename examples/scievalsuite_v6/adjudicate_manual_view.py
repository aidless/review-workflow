import json
import sys

sys.path.insert(0, r"F:\deepseek\research-kit\review-workflow\scripts")
sys.path.insert(0, r"F:\deepseek\research-kit")
from pathlib import Path
import number_reconcile as nr

p = r"F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\run_v3_converge\number_reconcile.json"
report = json.load(open(p, encoding="utf-8"))
mrl = report["direction_B_paper_to_evidence"]["manual_review_list"]
unique = {}
for r in mrl:
    unique.setdefault(r["token"], []).append(r["context"])

evidence_nums = [(str(e["value"]), e["value"], e.get("path", "")) for e in report.get("_evidence", [])]

tex = Path(r"F:\deepseek\papers\scievalsuite\paper\main.tex")

for token, ctxs in unique.items():
    mech_verdict, mech_note = nr.mechanical_r3(token, ctxs, [(x[0], x[1]) for x in evidence_nums])
    print(f"===== token {token!r} =====")
    print(f"  mechanical: {mech_verdict!r} | {mech_note}")
    # full context from tex
    full = nr.collect_token_contexts(tex, token, max_lines=2)
    for c in full:
        print(f"  tex: {c[:160]}")
    # evidence matches
    try:
        val = float(token)
    except ValueError:
        val = None
    if val is not None:
        matches = []
        for s, v, path in evidence_nums:
            if abs(v - val) <= 5e-4 or (val != 0 and abs(v / val - 1) <= 5e-4) or abs(round(v, 2) - val) <= 1e-9:
                matches.append(f"{path}={v}")
        if matches:
            print(f"  evidence matches: {matches[:6]}")
    print()
