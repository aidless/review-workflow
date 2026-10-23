import sys, json
sys.path.insert(0, r'F:/deepseek/research-kit')
sys.path.insert(0, r'F:/deepseek/research-kit/review-workflow/scripts')
import number_reconcile as nr

report = json.load(open(r'F:/deepseek/research-kit/review-workflow/examples/scievalsuite_v6/run_v3_converge/number_reconcile.json', encoding='utf-8'))
st = report.get('adjudications_state', {})
evidence = report.get('_evidence', [])
evidence_nums = []
for it in evidence:
    if isinstance(it, dict) and 'value' in it:
        src = it.get('source', '?')
        path = it.get('json_path', '?')
        evidence_nums.append((src + ':' + path, it['value']))
print('evidence_nums count:', len(evidence_nums))
print()
for token, entry in st.items():
    if entry.get('verdict') == 'pending':
        ctxs = [entry.get('context', '')]
        mech_verdict, mech_note = nr.mechanical_r3(token, ctxs, evidence_nums)
        print('%-12s mech=%-10s %s' % (repr(token), str(mech_verdict), mech_note[:90]))
