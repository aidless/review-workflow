import json
from pathlib import Path

report = json.load(open(r'F:/deepseek/research-kit/review-workflow/examples/scievalsuite_v6/run_v3_converge/number_reconcile.json', encoding='utf-8'))
ev = report.get('_evidence', [])
# check for 0.237, 0.42, 0.355, 2.3333, 0.074, 0.87, 5.2, 0.27, 0.4600 in evidence list
targets = [0.237, 0.42, 0.355, 2.3333, 0.074, 0.87, 5.2, 0.27, 0.4600, 0.69, 0.1418, 0.1918, 0.2750]
for t in targets:
    hits = []
    for e in ev:
        v = e.get('value')
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if abs(v - t) <= 5e-4 or (t != 0 and abs(v / t - 1) <= 5e-4) or abs(round(v, 2) - t) <= 1e-9:
                hits.append('%s:%s=%s' % (e.get('source','?').split('scievalsuite')[-1], e.get('json_path','?'), v))
    print('%-10s -> %d hits' % (t, len(hits)))
    for h in hits[:6]:
        print('    ', h)
    print()
