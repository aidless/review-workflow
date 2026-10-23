import json, os, re
from pathlib import Path

# 1. Find '3.1' in tex loosely
print('### find 3.1 in tex (loose)')
tex = Path(r'F:/deepseek/papers/scievalsuite/paper/main.tex').read_text(encoding='utf-8')
for m in re.finditer(r'3\.1\d*', tex):
    s = max(0, m.start() - 40)
    print('  ...%s...' % tex[s:m.end() + 40].replace('\n', ' ')[:120])

# 2. gemma Sentiment raw data from console logs
print()
print('### gemma Sentiment in console logs')
for f in ['L1a_gemma2_9b_console.log', 'A1_l1a_gemma2_9b_t3_console.log', 'A1_l1a_gemma2_9b_t3b_console.log']:
    fp = Path(r'F:/deepseek/papers/scievalsuite/results') / f
    if not fp.exists():
        continue
    txt = fp.read_bytes().decode('utf-8', errors='replace')
    for line in txt.splitlines():
        if 'sentiment' in line.lower() or '0.355' in line or '0.2000' in line or '0.2' in line:
            print('  [%s] %s' % (f, line.strip()[:150]))

# 3. All invalid rates across L2 files
print()
print('### invalid rates in L2 files')
for f in ['L2_qwen2.5_7b.json', 'L2_qwen2.5_14b.json', 'L2_gemma2_9b.json', 'L2_deepseek-v4-flash.json']:
    fp = Path(r'F:/deepseek/papers/scievalsuite/results') / f
    if not fp.exists():
        continue
    d = json.load(open(fp, encoding='utf-8'))
    arms = d.get('summary', {}).get('arms', {})
    for arm, ad in arms.items():
        print('  %s.%s invalid_rate=%s' % (f, arm, ad.get('invalid_rate')))

# 4. compute scripts for sensitivity
print()
print('### compute scripts mention sensitivity/fail handling')
for f in ['compute_curated_friedman.py', 'compute_curated_v2.py', 'compute_muse_friedman.py']:
    fp = Path(r'F:/deepseek/scievalsuite/out_p5') / f
    if not fp.exists():
        continue
    txt = fp.read_text(encoding='utf-8', errors='replace')
    print('  [%s] len=%d' % (f, len(txt)))
    for kw in ['NaN', 'exclude', 'fail', '5.2', '0.074', 'sensitivity']:
        if kw in txt:
            print('      mentions', kw)
