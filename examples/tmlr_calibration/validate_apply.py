import json
import sys
from pathlib import Path

sys.path.insert(0, "F:/deepseek/research-kit/review-workflow/scripts")
import run_review as rr

cal_dir = Path("F:/deepseek/research-kit/review-workflow/examples/tmlr_calibration/cal_results")
entries = json.load(open(cal_dir / "calibrations.json", encoding="utf-8"))
rows = []
for e in entries:
    g = json.load(open(f"F:/deepseek/research-kit/review-workflow/examples/tmlr_calibration/runs/run_{e['paper']}/gates.json", encoding="utf-8"))
    results = {st: {"gate": v["gate"], "metric": v["metric"], "report": {}}
               for st, v in g["stages"].items()}
    c = rr.calibrated_scoring(g["suggested_score"], g["score_dimensions"], results, cal_dir)
    rows.append((e["paper"], e["human"], g["suggested_score"], c["calibrated_score"]))
    print(f"{e['paper']:14} human={e['human']}  suggested={g['suggested_score']}  calibrated={c['calibrated_score']}")

bias_old = sum(h - s for _, h, s, _ in rows) / len(rows)
bias_new = sum(h - c for _, h, _, c in rows) / len(rows)
mae_new = sum(abs(h - c) for _, h, _, c in rows) / len(rows)
print(f"\n样本内验证（n={len(rows)}，即校准样本自身——仅验证偏移算术，非泛化）:")
print(f"  bias: {bias_old:+.2f} -> {bias_new:+.2f}   MAE: {bias_old:.2f} -> {mae_new:.2f}")
