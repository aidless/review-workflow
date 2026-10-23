import json

runs = "F:/deepseek/research-kit/review-workflow/examples/tmlr_calibration/runs"
entries = json.load(open("F:/deepseek/research-kit/review-workflow/examples/tmlr_calibration/tmlr_entries.json", encoding="utf-8"))
print(f'{"paper":14} {"yes":6} {"stableC":8} {"stableM":8} {"sustC":6} {"sustM":6} {"prism P/R/I/S":14} {"sugg":5} {"human":6}')
rows = []
for e in entries:
    p = e["paper"]
    r6 = json.load(open(f"{runs}/run_{p}/r6_llm.json", encoding="utf-8"))
    st = r6["summary"]["counts"]
    d = json.load(open(f"{runs}/run_{p}/debate.json", encoding="utf-8"))
    su = d["summary"]["counts_sustained"]
    pr = json.load(open(f"{runs}/run_{p}/prism_review.json", encoding="utf-8"))
    dims = {k: v.get("score") for k, v in pr.get("dimensions", {}).items()}
    g = json.load(open(f"{runs}/run_{p}/gates.json", encoding="utf-8"))
    print(f'{p:14} {e["yes_rate"]:<6} {st["Critical"]:<8} {st["Major"]:<8} {su["Critical"]:<6} {su["Major"]:<6} '
          f'{dims.get("P")}/{dims.get("R")}/{dims.get("I")}/{dims.get("S"):<8} {g["suggested_score"]:<5} {e["human"]:<6}')
    rows.append({"paper": p, "yes_rate": e["yes_rate"], "stable_C": st["Critical"], "stable_M": st["Major"],
                 "sust_C": su["Critical"], "sust_M": su["Major"], "prism": dims,
                 "suggested": g["suggested_score"], "human": e["human"]})

from scipy import stats as sps
ys = [r["yes_rate"] for r in rows]
for key in ("stable_C", "stable_M", "sust_C", "sust_M"):
    xs = [r[key] for r in rows]
    if len(set(xs)) >= 2 and len(set(ys)) >= 2:
        rho, pv = sps.spearmanr(xs, ys)
        print(f"{key} vs yes_rate: rho={rho:+.3f} p={pv:.4f}")
    else:
        print(f"{key} vs yes_rate: constant column, no corr")
