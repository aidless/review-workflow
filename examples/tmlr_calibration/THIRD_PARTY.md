# Third-party material in this directory

The MIT license at the repository root covers the code in this repository. It does not cover the files below.

| Path | What it is | License note |
|---|---|---|
| `pdfs/*.pdf` | Six TMLR articles used as the stored calibration sample | TMLR's author guide says submissions are CC BY 4.0 and copyright remains with the authors. Redistribution needs attribution. This tree does not add author names beyond what is inside each PDF. |
| `tmlr_dump.json` | 85-paper metadata dump (decisions, claim votes `ce`/`aud`/`n_req`, titles, PDF paths). No review prose is stored | OpenReview's terms treat a submitted Comment, including a review, as CC BY 4.0, and metadata as CC0 where a copyright exists. The dump kept votes and decisions, not review text. |
| `cal_results/` | Scores produced by running this workflow on those six PDFs | The PRISM numbers are outputs of this repo. The paper identity and `yes_rate` values come from the dump. |

Fetched 2026-08-26 according to `tmlr_dump.json` meta. No new OpenReview download was made for the planted-defect benchmark.

Do not treat a Spearman on `cal_results/calibrations.json` as a new experiment. `make check` only recomputes that stored table.
