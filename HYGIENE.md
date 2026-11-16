# Repo hygiene

Checked in this change. `make check` recomputes the count block. Narrative below is the judgment; the block is the measurement.

## OpenReview dump

`examples/tmlr_calibration/tmlr_dump.json` says it was fetched 2026-08-26 from OpenReview API v2 (`content.venueid=TMLR`, "100 most recent accepted"). The file contains 85 paper objects. Meta stats say total 100 and errors 15. Decisions in the meta are Accept as is (49) and Accept with minor revision (36).

Each review object has only `ce`, `aud`, and `n_req`. There is no review prose, no reviewer name, and no free-text `requested_changes` body in this file. The key list `rv_keys` names those fields; the values are not stored.

OpenReview's terms (fetched for this audit) say a Comment, which includes a tasked review, is released by the submitter under CC BY 4.0, and that metadata is CC0 to the extent a copyright exists. TMLR's author guide says submissions are CC BY 4.0 and copyright stays with the authors. Those licenses allow redistribution with attribution. They do not make the files part of this repository's MIT license.

Raw reviewer text is not in the dump, so the question "should the prose be in a public repo" does not arise for this file. If prose were added later it would need its own CC BY notice and attribution (anonymous reviewer text attributes poorly; a forum id is not a name). Vote counts and decisions are what is here. They are public on OpenReview for accepted TMLR papers. Keeping them is consistent with that public record. The missing piece is a license notice, added at `examples/tmlr_calibration/THIRD_PARTY.md`. The papers were not deleted.

The six PDFs under `examples/tmlr_calibration/pdfs/` are full articles. Same notice. They account for most of the checkout size.

## Personal paths

`make check` counts text files that contain the legacy prefix `F:\deepseek` or `F:/deepseek`. Source hits are the files that document that prefix as a fallback search path. The hundreds of example and `runs/` hits are archived run logs that recorded absolute paths. They are research/run records. They were not removed. `chain_logs/` did not match that prefix.

No API token or cloud credential was identified in that scan. `.gitleaksignore` already marks generic-api-key hits inside `examples/scievalsuite_v6/**/citation_check.json` as false positives. Those files were not opened as secrets and were not deleted.

## What was removed

Nothing tracked. Local `__pycache__` from running the tests is gitignored. The planted-defect packages are new synthetic fixtures, not a cleanup of prior data.

## Clone size

GitHub reports the repository size in the repo metadata (see the PR for the clone timing measured from this environment). A fresh `make check` does not read the TMLR PDFs. It does read the dump JSON once, for the counts below.

<!-- hygiene-counts:begin -->
dump_papers: 85
fetch_meta_total: 100
fetch_meta_errors: 15
decisions: Accept as is=49, Accept with minor revision=36
review_keys: aud,ce,n_req
review_string_fields_longer_than_40: 0
pdfs_in_tree: 6
legacy_path_source_files: FAILURE_MODES.md,HYGIENE.md,README.md,REVIEW_SOP.md,scripts/audit_package.py,scripts/make_linux_configs.py,scripts/run_external_review.py,scripts/run_review.py
legacy_path_example_or_run_files: 817
<!-- hygiene-counts:end -->
