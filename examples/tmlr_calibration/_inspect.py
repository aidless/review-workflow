# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path(__file__).parent
d = json.loads((root / 'tmlr_dump.json').read_text(encoding='utf-8'))
if isinstance(d, dict):
    print('dump keys:', list(d.keys())[:10])
    papers = d.get('papers', d.get('notes', []))
else:
    papers = d
print('dump papers:', len(papers))
if papers:
    p0 = papers[0]
    print('paper[0] keys:', sorted(p0.keys()) if isinstance(p0, dict) else type(p0))

es = json.loads((root / 'tmlr_entries.json').read_text(encoding='utf-8'))
print('entries:', len(es))
for e in es:
    title = (e.get('title') or '')[:60]
    print('  %s  yes_rate=%s  decision=%s  n_reviews=%s  human=%s' % (
        e['paper'], e.get('yes_rate'), e.get('decision'), e.get('n_reviews'), e.get('human')))
    print('    title:', title)
