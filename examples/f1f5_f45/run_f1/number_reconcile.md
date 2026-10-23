# 数字对账报告（R3）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f1\extracted_text.txt`，证据目录：`F:\Research\_inbox\F1-F5_F45_2026-08-26\supplementary`
- 结论：**MAJOR**（裁决 critical 0，待复核 64，机械噪音 21，已裁决 0）
- 无证据目录：否

## 方向 A：产物统计数字 → 论文出现（论文未改数字）

- 核心统计数字 1242 个，其中 272 个在论文中找到一致值（命中率 0.219）

| json_path | 值 | 论文 token | 来源 |
|---|---|---|---|
| `keyResults.mcnemar_per_strategy.injection[0].p_exact` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_primary[0].delta_p_bootstrap_lo` | 0.089 | `0.089` | `tier2_f45_results.json` |
| `keyResults.mcnemar_primary[0].p_holm` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[0].cohens_g` | 0.4995283760415029 | `0.50` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[0].p_exact` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[1].c` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[1].cohens_g` | 0.5 | `0.50` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[1].p_exact` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[2].delta_p` | 0.1400625 | `0.14` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[2].p_exact` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `meta.alpha` | 0.05 | `0.05` | `tier2_phrasing_results.json` |
| `delta_hierarchical.RAG_theta0.1.sd_cluster_means` | 0.05950893164313473 | `0.06` | `F3_Tier2_results.json` |
| `delta_hierarchical.summarization.sd_cluster_means` | 0.060384793064471955 | `0.06` | `F3_Tier2_results.json` |
| `gamma_hierarchical.RAG_theta0.1.sd_cluster_means` | 0.034556758990994814 | `0.035` | `F3_Tier2_results.json` |
| `gamma_hierarchical.summarization.mean` | 6.700728333333332 | `6.7` | `F3_Tier2_results.json` |
| `holdout_K4_5_summary[0].violation_rate` | 0.02 | `0.020` | `tier2_refit.json` |
| `holdout_K4_5_summary[1].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `holdout_K4_5_summary[2].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `holdout_K4_5_summary[4].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `holdout_K4_5_summary[5].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `original_reference_biased_vs_benign[0].bootstrap.mean` | 0.041832 | `0.042` | `tier2_phrasing_results.json` |
| `original_reference_biased_vs_benign[1].bootstrap.mean` | 0.0007879999999999989 | `0.001` | `tier2_phrasing_results.json` |
| `original_reference_biased_vs_benign[3].bootstrap.mean` | 0.017240000000000005 | `0.017` | `tier2_phrasing_results.json` |
| `results_per_contrast[1].bootstrap.mean` | 0.023587999999999998 | `0.024` | `tier2_phrasing_results.json` |
| `results_per_contrast[2].bootstrap.mean` | 0.025108 | `0.025` | `tier2_phrasing_results.json` |
| `results_per_contrast[6].bootstrap.mean` | 0.0016859999999999974 | `0.002` | `tier2_phrasing_results.json` |
| `results_per_contrast[7].bootstrap.mean` | 0.0020859999999999976 | `0.002` | `tier2_phrasing_results.json` |
| `results_per_contrast[8].bootstrap.mean` | 0.002165999999999998 | `0.002` | `tier2_phrasing_results.json` |
| `sensitivity.holdout_summary_p5[1].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `sensitivity.holdout_summary_p5[2].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `sensitivity.holdout_summary_p5[4].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `sensitivity.holdout_summary_p5[5].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `sensitivity.pooled_B_mean_p5` | 0.088626 | `0.089` | `tier2_refit.json` |
| `train_K3_summary[0].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `train_K3_summary[1].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `train_K3_summary[2].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `c0_refit.c0_primary` | 0.179905 | `0.18` | `tier2_refit.json` |
| `c0_refit.per_gamma_mins.0.5` | 0.179905 | `0.18` | `tier2_refit.json` |
| `c0_refit.train_coverage_p5` | 0.95 | `0.95` | `tier2_refit.json` |
| `c0_refit.train_coverage_primary` | 1.0 | `1.0` | `tier2_refit.json` |

## 方向 B：论文小数 → 产物支撑

- 论文小数 229 个，有支撑 144 个（支撑率 0.6288）
- 机械噪音 21 个（版本号片段/日期/结构行，自动豁免）
- 已裁决 0 个（人工 verdict：noise/supported/critical）

### 人工复核清单（未裁决且非噪音）

- L15 `1.6`：of +0.047 (Qwen3:4b, Wilcoxon W=12480, p=1.6×10−5, dz=0.42); a length-matched benign
- L15 `0.42`：of +0.047 (Qwen3:4b, Wilcoxon W=12480, p=1.6×10−5, dz=0.42); a length-matched benign
- L16 `0.62`：control (75-char neutral prefix, +0.005, p=0.62, see Fig. 1) is associated with no significant
- L22 `0.645`：a single priming phrasing (supplementary 500×3 phrasings pilot 0.645/0.646/0.649 conf,
- L167 `12.2`：L ≈0.004/char and Γ ≈12.2 chars from prefix string lengths (illustrative), giving |∆MAE| ≤0.049 ≈0.0
- L174 `98.2`：6,000 paired differences), 3 seeds (42/43/44), B=5000 BCa, bootstrap seed 42. Parse rates: Qwen3:4b 
- L175 `93.3`：Gemma3:4b 93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Lower parse rates (Gemma) are due to
- L175 `96.1`：Gemma3:4b 93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Lower parse rates (Gemma) are due to
- L175 `2.5`：Gemma3:4b 93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Lower parse rates (Gemma) are due to
- L175 `99.1`：Gemma3:4b 93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Lower parse rates (Gemma) are due to
- L193 `0.084`：[+0.014, +0.084]
- L194 `1.6`：W=12480, 1.6×10−5 ∗
- L195 `0.42`：0.42 [0.18, 0.66]
- L195 `0.66`：0.42 [0.18, 0.66]
- L202 `0.08`：0.31 [0.08, 0.54]
- L202 `0.54`：0.31 [0.08, 0.54]
- L204 `2.5`：Qwen2.5:14B
- L206 `0.012`：+0.012
- L213 `0.067`：+0.067
- L214 `0.023`：[+0.023, +0.121]
- L214 `0.121`：[+0.023, +0.121]
- L216 `0.12`：0.38 [0.12, 0.64]
- L216 `0.64`：0.38 [0.12, 0.64]
- L223 `0.12`：−0.12 [−0.34, 0.10]
- L226 `1.6`：p=1.6 × 10−5) and Gemma3:4b ranking (+0.067, W=15670, p=0.007). The few-shot channel does not shift
- L226 `0.067`：p=1.6 × 10−5) and Gemma3:4b ranking (+0.067, W=15670, p=0.007). The few-shot channel does not shift
- L233 `0.42`：at p < .02 (Bonferroni α′=0.017). Shifts reported as ∆MAE; dz in brackets: raw [0.42], temp [0.35], 
- L242 `0.039`：+0.039∗
- L244 `0.038`：+0.038∗
- L248 `0.62`：The key comparison is benign-long (∆= + 0.005, p=0.62) vs confidence-priming
- L249 `1.6`：(∆= + 0.047, p=1.6 × 10−5): both prefixes are ∼75 chars, but only the priming condition is associate
- L258 `0.045`：Cross-seed stability. ∆MAE across 3 seeds: seed 0 +0.045, seed 1 +0.049, seed 2 +0.047 (SD = 0.002).
- L264 `0.067`：The ranking channel exhibits the largest shift (+0.067), suggesting that entry ordering is a
- L267 `0.067`：regardless of correctness, while the ranking channel (+0.067) additionally exploits attention bias t
- L286 `1.6`：* p=1.6e-5
- L287 `0.62`：n.s. p=0.62
- L393 `2.5`：Qwen2.5:14B tag 7cdf5a0187d5;
- L397 `0.075`：−0.075
- L411 `2.5`：Qwen2.5:14B
- L419 `0.012`：+0.012
- L420 `0.067`：+0.067 *
- L427 `1.26`：requirements.txt locks numpy 1.26, scipy 1.11, matplotlib 3.8; environment.yml specifies OS/CUDA. Se
- L427 `3.8`：requirements.txt locks numpy 1.26, scipy 1.11, matplotlib 3.8; environment.yml specifies OS/CUDA. Se
- L462 `12.2`：bounded by the confidence shift. Empirical: L ≈0.004/char, Γ ≈12.2 chars (from string lengths), boun
- L467 `98.2`：Per-model per-channel ∆MAE with dz and CLES (Table 4). Parse rates: Qwen3:4b 98.2%, Gemma3:4b
- L468 `93.3`：93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Unparseable cells (6.7%) excluded.
- L468 `96.1`：93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Unparseable cells (6.7%) excluded.
- L468 `2.5`：93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Unparseable cells (6.7%) excluded.
- L468 `99.1`：93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Unparseable cells (6.7%) excluded.
- L471 `0.645`：cells = 500×3 phrasings, 0.645/0.646/0.649 conf, direction consistent).
- L483 `1.6`：1.6×10−5
- L493 `0.12`：−0.12
- L504 `0.067`：+0.067
- L532 `2.5`：Qwen2.5:14B
- L534 `0.012`：+0.012
- L538 `2.5`：Qwen2.5:14B
- L544 `2.5`：Qwen2.5:14B
- L551 `0.42`：Power. At dz=0.42 (observed), α=0.05, power 0.8, the Wilcoxon signed-rank test (via t-approximation)
- L553 `0.999`：Our n=500 yields power > 0.999 under either
- L586 `0.42`：n=38 (dz=0.42),
- L590 `1.26`：able). requirements.txt: numpy 1.26, scipy 1.11, matplotlib 3.8. environment.yml: Ubuntu 22.04, Pyth
- L590 `3.8`：able). requirements.txt: numpy 1.26, scipy 1.11, matplotlib 3.8. environment.yml: Ubuntu 22.04, Pyth
- L590 `22.04`：able). requirements.txt: numpy 1.26, scipy 1.11, matplotlib 3.8. environment.yml: Ubuntu 22.04, Pyth
- L591 `13.0`：3.10, CUDA 13.0. Seed 42. Ollama model tags pinned by SHA. SOURCE_DATE_EPOCH=1720000000. Sanity

### 机械噪音（自动豁免）

- `0.62`（section-heading）：0.62
- `0.60`（section-heading）：0.60
- `0.44`（section-heading）：0.44
- `0.08`（section-heading）：0.08
- `0.2`（section-heading）：0.2
- `0.6`（section-heading）：0.6
- `0.2`（section-heading）：0.2
- `0.6`（section-heading）：0.6
- `0.075`（section-heading）：0.075
- `2312.10997`（arxiv-id）：arXiv:2312.10997, 2024.
- `2207.05221`（arxiv-id）：arXiv preprint arXiv:2207.05221, 2022.
- `0.42`（section-heading）：0.42
- `0.15`（section-heading）：0.15
- `0.44`（section-heading）：0.44
- `0.62`（section-heading）：0.62
- `0.54`（section-heading）：0.54
- `0.22`（section-heading）：0.22
- `0.58`（section-heading）：0.58
- `0.09`（section-heading）：0.09
- `0.22`（section-heading）：0.22
- `0.60`（section-heading）：0.60