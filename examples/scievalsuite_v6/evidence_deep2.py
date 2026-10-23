import json, os
from pathlib import Path

def load(fp):
    try:
        return json.load(open(fp, encoding='utf-8'))
    except Exception as e:
        return {'__error__': str(e)}

# 1. power_analysis.json
print('### power_analysis.json')
d = load(r'F:/deepseek/papers/scievalsuite/results/power_analysis.json')
print(json.dumps(d, ensure_ascii=False, indent=1)[:1500])

# 2. P5_FINAL_FRONTIER_CURATED.json - sensitivity
print()
print('### P5_FINAL_FRONTIER_CURATED.json')
d = load(r'F:/deepseek/scievalsuite/out_p5/P5_FINAL_FRONTIER_CURATED.json')
s = json.dumps(d, ensure_ascii=False)
print('len', len(s))
for t in ['5.2', '0.074', '0.0498', '0.3679', '6.0', '2.0', '14.25', '0.0026']:
    if t in s:
        print('  contains', t)
# print structure keys
def keys(o, prefix='', depth=0):
    if depth > 3:
        return
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)):
                print('  ' * depth + prefix + k + ':')
                keys(v, '', depth + 1)
            else:
                print('  ' * depth + prefix + k + ' = ' + str(v)[:80])
keys(d)

# 3. CROSS_LAYER_ANALYSIS.md
print()
print('### CROSS_LAYER_ANALYSIS.md')
md = Path(r'F:/deepseek/scievalsuite/out_p5/CROSS_LAYER_ANALYSIS.md').read_text(encoding='utf-8')
for line in md.splitlines():
    if any(t in line for t in ['0.87', '0.27', 'rho', 'rho', 'corr', '0.14']):
        print('  ', line.strip()[:160])

# 4. FARM_ABLATION.json
print()
print('### FARM_ABLATION.json')
d = load(r'F:/deepseek/scievalsuite/out_p5/FARM_ABLATION.json')
s = json.dumps(d, ensure_ascii=False)
for t in ['0.27', '0.87', '0.1418', '0.05', '0.10']:
    if t in s:
        print('  contains', t)
print(json.dumps(d, ensure_ascii=False, indent=1)[:1200])
