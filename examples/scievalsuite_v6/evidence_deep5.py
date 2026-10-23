import re
from pathlib import Path

# 1. Check gemma L1a console logs for actual scores
print('### gemma L1a console logs (score lines)')
for f in ['L1a_gemma2_9b_console.log', 'A1_l1a_gemma2_9b_t3_console.log', 'A1_l1a_gemma2_9b_t3b_console.log']:
    fp = Path(r'F:/deepseek/papers/scievalsuite/results') / f
    if not fp.exists():
        continue
    txt = fp.read_bytes().decode('utf-8', errors='replace')
    lines = txt.splitlines()
    print('  [%s] %d lines' % (f, len(lines)))
    for i, line in enumerate(lines):
        low = line.lower()
        if any(k in low for k in ['sentiment', 'textsim', 'score', 'spearman', 'mae', 'acc']):
            print('    L%d: %s' % (i + 1, line.strip()[:140]))

# 2. Read compute scripts
print()
print('### compute_curated_friedman.py')
print(Path(r'F:/deepseek/scievalsuite/out_p5/compute_curated_friedman.py').read_text(encoding='utf-8', errors='replace'))
print()
print('### compute_muse_friedman.py')
print(Path(r'F:/deepseek/scievalsuite/out_p5/compute_muse_friedman.py').read_text(encoding='utf-8', errors='replace'))
