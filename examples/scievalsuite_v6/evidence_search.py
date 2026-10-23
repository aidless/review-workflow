import json, os
from pathlib import Path

dirs = [Path(r'F:/deepseek/papers/scievalsuite/results'), Path(r'F:/deepseek/scievalsuite/out_p5')]
targets = {
    '0.355': [], '0.4600': [], '0.42': [], '2.3333': [], '0.074': [],
    '0.27': [], '0.87': [], '0.2400': [], '5.2': [], '0.007': [], '0.64': [],
}

def walk_json_files(d):
    for root, dirs_, files in os.walk(d):
        for f in files:
            if f.endswith('.json'):
                yield Path(root) / f

def find_value(obj, path, hits):
    if isinstance(obj, dict):
        for k, v in obj.items():
            find_value(v, path + '.' + k, hits)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            find_value(v, path + '[%d]' % i, hits)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        for t in targets:
            try:
                tv = float(t)
            except ValueError:
                continue
            if abs(obj - tv) <= 5e-4 or (tv != 0 and abs(obj / tv - 1) <= 5e-4) or abs(round(obj, 2) - tv) <= 1e-9:
                targets[t].append('%s=%s' % (path, obj))

for d in dirs:
    if not d.exists():
        print('MISSING DIR:', d)
        continue
    for fp in walk_json_files(d):
        try:
            data = json.load(open(fp, encoding='utf-8'))
        except Exception:
            continue
        find_value(data, fp.name, None)

for t, hits in targets.items():
    print('%-10s -> %d hits' % (t, len(hits)))
    for h in hits[:8]:
        print('    ', h)
    print()
