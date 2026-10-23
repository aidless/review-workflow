import json, os
from pathlib import Path

def load(fp):
    try:
        return json.load(open(fp, encoding='utf-8'))
    except Exception as e:
        return {'__error__': str(e)}

# 3. CROSS_LAYER_ANALYSIS.md - handle encoding
print('### CROSS_LAYER_ANALYSIS.md')
fp = Path(r'F:/deepseek/scievalsuite/out_p5/CROSS_LAYER_ANALYSIS.md')
raw = fp.read_bytes()
for enc in ['utf-8', 'gbk', 'latin-1']:
    try:
        md = raw.decode(enc)
        print('  decoded with', enc)
        break
    except Exception:
        continue
for line in md.splitlines():
    if any(t in line for t in ['0.87', '0.27', 'rho', 'corr', '0.14']):
        print('  ', line.strip()[:180])

# 4. FARM_ABLATION.json
print()
print('### FARM_ABLATION.json')
d = load(r'F:/deepseek/scievalsuite/out_p5/FARM_ABLATION.json')
s = json.dumps(d, ensure_ascii=False)
for t in ['0.27', '0.87', '0.1418', '0.05', '0.10']:
    if t in s:
        print('  contains', t)
print(json.dumps(d, ensure_ascii=False, indent=1)[:1500])

# 5. Search all out_p5 md/json for sensitivity chi2=5.2 / p=0.074
print()
print('### search sensitivity 5.2 / 0.074 across out_p5')
for f in os.listdir(r'F:/deepseek/scievalsuite/out_p5'):
    fp = Path(r'F:/deepseek/scievalsuite/out_p5') / f
    if fp.suffix in ('.md', '.json'):
        try:
            txt = fp.read_text(encoding='utf-8')
        except Exception:
            txt = fp.read_bytes().decode('gbk', errors='replace')
        if '5.2' in txt or '0.074' in txt:
            print('  ', f)
            for line in txt.splitlines():
                if '5.2' in line or '0.074' in line:
                    print('      ', line.strip()[:180])
