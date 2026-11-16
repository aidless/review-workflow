# Planted-defect protocol

Mechanical stages only. No LLM call, no network, no OpenReview pull.

1. `build_fixtures.py` writes `packages/` and `labels.json`.
2. `labels.json` is committed **before** any stage is run on these packages. Each package file has a sha256 in that commit. `scored` is `false`.
3. A later commit runs the stages and records the gate matrix. Expectations in `labels.json` are not edited to match the matrix.
4. `make check` rebuilds nothing. It re-hashes the package bytes, re-runs the stages offline, and fails if the live matrix or the README copy disagrees with the committed result.

A `not-PASS` expectation is met by WARN, FAIL, or SKIP. PASS on a planted stage is a miss. A PASS expectation that comes back otherwise is a false positive. Both are reported. Checkers are not changed to hide either one.
