import sys, json
sys.path.insert(0, r'F:/deepseek/research-kit')
sys.path.insert(0, r'F:/deepseek/research-kit/review-workflow/scripts')
import number_reconcile as nr
from pathlib import Path

tex = Path(r'F:/deepseek/papers/scievalsuite/paper/main.tex')
report = json.load(open(r'F:/deepseek/research-kit/review-workflow/examples/scievalsuite_v6/run_v3_converge/number_reconcile.json', encoding='utf-8'))
st = report.get('adjudications_state', {})
evidence = report.get('_evidence', [])
evidence_nums = []
for it in evidence:
    if isinstance(it, dict) and 'value' in it:
        src = it.get('source', '?')
        path = it.get('json_path', '?')
        evidence_nums.append((src + ':' + path, it['value']))

targets = ['2.5','0.355','1.2','3.1','3.11','0.007','1.87','0.4600','3.12','0.42','2.3333','0.64','0.074','0.27','0.87','0.2400','5.2']
for token in targets:
    entry = st.get(token, {})
    print('=' * 70)
    print('TOKEN:', repr(token))
    mech_verdict, mech_note = nr.mechanical_r3(token, [entry.get('context','')], evidence_nums)
    print('mech:', mech_verdict, '|', mech_note[:120])
    # full context from tex
    full = nr.collect_token_contexts(tex, token, max_lines=3)
    for c in full:
        print('  tex:', c[:200])
    # evidence matches
    try:
        val = float(token)
    except ValueError:
        val = None
    if val is not None:
        matches = []
        for s, v in evidence_nums:
            if abs(v - val) <= 5e-4 or (val != 0 and abs(v / val - 1) <= 5e-4) or abs(round(v, 2) - val) <= 1e-9:
                matches.append('%s=%s' % (s, v))
        if matches:
            print('  evidence matches: %s' % matches[:6])
    print()
