import json, os
from pathlib import Path

def load(fp):
    try:
        return json.load(open(fp, encoding='utf-8'))
    except Exception as e:
        return {'__error__': str(e)}

def walk(d, suffix='.json'):
    out = []
    if not Path(d).exists():
        return out
    for root, dirs_, files in os.walk(d):
        for f in files:
            if f.endswith(suffix):
                out.append(Path(root) / f)
    return out

# 1. P5_MUSE_FINAL.json - check for 2.3333, mean ranks, chi2
print('### P5_MUSE_FINAL.json')
for fp in walk(r'F:/deepseek/scievalsuite/out_p5'):
    if 'MUSE_FINAL' in fp.name or 'P5_MUSE' in fp.name:
        d = load(fp)
        s = json.dumps(d, ensure_ascii=False)
        print(' ', fp.name, 'len', len(s))
        for t in ['2.3333', '3.3333', '2.8333', '1.0000', '14.25', '0.0026', '1.9148']:
            if t in s:
                print('    contains', t)
        # find the friedman structure
        def find_key(o, key, path=''):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == key:
                        print('    %s.%s = %s' % (path, k, json.dumps(v, ensure_ascii=False)[:200]))
                    find_key(v, key, path + '.' + k)
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    find_key(v, key, path + '[%d]' % i)
        find_key(d, 'friedman', '')
        find_key(d, 'mean_rank', '')
        find_key(d, 'mean_ranks', '')

# 2. p3_effects.json CI
print()
print('### p3_effects.json cross_model_gradient')
fp = Path(r'F:/deepseek/papers/scievalsuite/results/p3_effects.json')
d = load(fp)
cmg = d.get('cross_model_gradient', {})
for k, v in cmg.items():
    print(' ', k, '=', json.dumps(v, ensure_ascii=False)[:200])

# 3. sensitivity files
print()
print('### sensitivity / zinc files in out_p5')
for fp in walk(r'F:/deepseek/scievalsuite/out_p5'):
    low = fp.name.lower()
    if 'sens' in low or 'zinc' in low or 'friedman' in low or 'cross' in low:
        d = load(fp)
        s = json.dumps(d, ensure_ascii=False)
        print(' ', fp.name, 'len', len(s))
        for t in ['5.2', '0.074', '0.0498', '0.87', '0.27']:
            if t in s:
                print('    contains', t)

# 4. gemma Sentiment data
print()
print('### gemma sentiment raw')
for fp in walk(r'F:/deepseek/papers/scievalsuite/results'):
    low = fp.name.lower()
    if 'gemma' in low or 'l1a' in low:
        d = load(fp)
        s = json.dumps(d, ensure_ascii=False)
        if '0.355' in s or 'sentiment' in s.lower():
            print(' ', fp.name, 'len', len(s), 'has 0.355:', '0.355' in s)
