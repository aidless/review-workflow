# Failure modes

What the mechanical stages miss, what they only warn on, and what this repository does not show. The planted-defect matrix is the measured record. It is not a claim that a real submission will be caught at the same rate.

## Gates

`overall` is the worst stage: FAIL > WARN > SKIP > PASS. SKIP means the stage did not judge. It is not a pass. An evidence-layer FAIL caps the suggested score at 4. That cap is a rule in `scripts/run_review.py`, not a calibrated probability of rejection.

## Measured on the frozen synthetic packages

| Plant | What happened | What it does not mean |
|---|---|---|
| Missing `\texttt` path | R2 FAIL | Other citation styles (plain prose paths, `\path`, `\input` outside R2d) are not this plant |
| Manifest sha256 of 64 zeros | R2b FAIL | A matching size with a wrong hash is caught. A manifest that simply omits the file is not this plant |
| Table cell 0.777 vs JSON 0.812 | R2d WARN and R3 WARN | The cell is unsupported, not proved to be the "wrong" copy of a paired JSON field. R3 fires because the same decimal is in the tex |
| `45/50 = 0.92` | R1d WARN | The wrong value was also stored in JSON, so R3 PASSed. R3 does not recompute arithmetic |
| McNemar `p=0.5000` with `b=1,c=9` | R4 FAIL, status MISMATCH | This is the recompute |
| Wilson `ci=[0.1,0.2]` with `k=8,n=10` | R4 status NOT_IN_PAPER, not MISMATCH | The stored `ci` is not compared to the interval implied by `k,n`. The paper omitted the true endpoints, so the record is "not in the paper." A paper that also printed the true endpoints could MATCH while `ci` stayed wrong. Not patched |
| Undisclosed `simulated` annotator note plus `alpha=0.894` | R5 FAIL | R5's lexicon is simulated/mock/synthetic/placeholder/dummy/fake/toy/pending/TODO/FIXME and a few siblings. A sentence such as "state of the art" is outside that list |
| `\cite` key absent from the bib | R1b WARN | Offline only. A real arXiv id that does not exist is a different check and needs the network |

Clean controls A and B were PASS on R1b, R1d, R2, R2b, R2c, R2d, R3, R4, and R5. That is two fixtures, not a false-positive rate on real papers.

## Selftest

Round 1 of `run_review.py --selftest` used to be described in the README as R4 PASS with 0 records. The current fixture has 3 matched records (McNemar, Friedman, Wilson). The selftest now fails if that count is 0. A PASS on an empty record list is not evidence that recomputation works.

The PDF-mode section of the same selftest still overwrites the evidence file with `{"l2": {"mean_goal_A": 0.14175}}` and then reports R4 PASS with 0 records. That path is vacuous on purpose so a missing statistic does not cap the PDF-mode score. It is not a recompute.

If PyMuPDF is not installed, the PDF section of the selftest SKIPs. Previously that section raised `ModuleNotFoundError` after the mechanical rounds had already passed, because `pdf_text.py` imports without importing PyMuPDF.

## Out of scope for the mechanical layer

- Symbolic derivation and units (R1d says so).
- LLM review quality. R6, R6b, and R6c SKIP without a local RPC. They are not in the planted benchmark.
- Whether using the workflow changes accept or reject decisions. There is no randomized comparison.
- Novelty search (R1c) when `novelty_online` is false. That stage SKIPs.

## TMLR / OpenReview

`examples/tmlr_calibration/cal_results/calibration_report.json` stores Spearman ρ=0.89, p=0.0175 for PRISM dimension R versus `yes_rate`, n=6, bias=1.67, MAE=1.67. Recomputing from `calibrations.json` gives ρ=0.889898, p=0.017516. The older README figure p=0.018 was a second rounding.

Every suggested score in that table is 6, so correlation of suggested versus human is undefined. Every decision is an accept. Rejected TMLR papers are not in the table. This is arithmetic on a stored accept-side report. It is not a new pull from OpenReview and it is not a calibration of review quality.

The dump file has 85 paper objects. Its meta says 100 fetched and 15 errors. Review objects contain `ce`, `aud`, and `n_req` only. No review prose longer than 40 characters is in the dump. See `HYGIENE.md` and `examples/tmlr_calibration/THIRD_PARTY.md`.

## Paths and license

Committed example runs and `runs/` embed `F:\deepseek\...` paths from the machine that produced them. Five source files name that prefix as a legacy search path. They were left in place. Deleting the run logs would delete the archived evidence those logs are.

`__pycache__` from local runs is gitignored. Nothing tracked was deleted as junk in this change.

## GitHub About (not updated from this PR)

Current About text:

> 16-stage multi-agent LLM paper-review pipeline: citation/number/statistics verification, debate denoising, OpenReview calibration. Offline recompute, append-only ledgers.

That sentence calls the project a multi-agent LLM pipeline and states OpenReview calibration without the n=6 accept-only limit. Replacement text, for the person who can edit About:

> Mechanical checks for a paper submission (cited files, hashes, tables, arithmetic, McNemar/Wilson/Friedman). Optional LLM stages skip without a local RPC. Not a reviewer replacement. In-repo TMLR figures are an n=6 accept-only stored report.

Until About is changed, README, PREREG, and About do not agree. That is why the status line is work in progress.
