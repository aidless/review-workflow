# Planted-defect matrix

Recomputed by `python3 scripts/score_planted.py`. Expectations are the frozen `labels.json` values.
tp = planted stage did not PASS. fn = planted stage PASSed (miss). fp = control or off-stage flag. tn = expected PASS.

Labels commit: `60c0ed202fe693ba3310498c2e7c5c5efaef16f2`. Labels file was not edited by the scorer.

| case | planted | R1b | R1d | R2 | R2b | R2c | R2d | R3 | R4 | R5 |
|---|---|---|---|---|---|---|---|---|---|---|
| `arithmetic_error` | inline arithmetic error | PASS ok | WARN TP | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok |
| `clean_control_a` | clean control | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok |
| `clean_control_b` | clean control | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok |
| `ghost_citation` | unresolved citation | WARN TP | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok |
| `hash_mismatch` | checklist hash mismatch | PASS ok | PASS ok | PASS ok | FAIL TP | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok |
| `missing_cited_file` | missing cited file | PASS ok | PASS ok | FAIL TP | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok |
| `stats_mcnemar_wilson` | wrong McNemar p and wrong Wilson interval versus raw counts | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | FAIL TP | PASS ok |
| `table_number_mismatch` | table number disagrees with results JSON | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | WARN TP | WARN TP | PASS ok | PASS ok |
| `undisclosed_simulation` | overclaim: undisclosed simulated annotator agreement | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | PASS ok | FAIL TP |

Counts: tp=8 fn=0 fp=0 tn=73.

No misses and no false positives against the frozen expectations.

Observations (not relabeled):

- stats_mcnemar_wilson R4 checks: {"mcnemar": [{"kind": "mcnemar", "status": "MISMATCH", "json_path": "mcnemar_pair"}], "wilson": [{"kind": "wilson", "status": "NOT_IN_PAPER", "json_path": "wilson_gold"}]}
- Wilson stored ci was not marked MISMATCH. stats_recompute.py compares recomputed Wilson endpoints to tex decimals and does not compare the stored ci field to those endpoints. This is reported, not patched.
