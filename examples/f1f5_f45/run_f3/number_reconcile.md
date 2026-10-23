# 数字对账报告（R3）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f3\extracted_text.txt`，证据目录：`F:\Research\_inbox\F1-F5_F45_2026-08-26\supplementary`
- 结论：**MAJOR**（裁决 critical 0，待复核 84，机械噪音 23，已裁决 0）
- 无证据目录：否

## 方向 A：产物统计数字 → 论文出现（论文未改数字）

- 核心统计数字 1242 个，其中 309 个在论文中找到一致值（命中率 0.2488）

| json_path | 值 | 论文 token | 来源 |
|---|---|---|---|
| `keyResults.mcnemar_per_strategy.injection[0].p_exact` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_per_strategy.mimicry[0].delta_p` | 0.028375 | `0.028` | `tier2_f45_results.json` |
| `keyResults.mcnemar_primary[0].delta_p_bootstrap_lo` | 0.089 | `0.089` | `tier2_f45_results.json` |
| `keyResults.mcnemar_primary[0].p_holm` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[0].cohens_g` | 0.4995283760415029 | `0.5` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[0].p_exact` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[1].c` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[1].cohens_g` | 0.5 | `0.5` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[1].p_exact` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[2].delta_p` | 0.1400625 | `0.14` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[2].p_exact` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `meta.alpha` | 0.05 | `0.05` | `tier2_phrasing_results.json` |
| `delta_hierarchical.RAG_theta0.1.sd_cluster_means` | 0.05950893164313473 | `0.06` | `F3_Tier2_results.json` |
| `delta_hierarchical.summarization.sd_cluster_means` | 0.060384793064471955 | `0.06` | `F3_Tier2_results.json` |
| `gamma_hierarchical.append-only.mean` | 12.301053333333334 | `12.3` | `F3_Tier2_results.json` |
| `gamma_hierarchical.append-only.sd_cluster_means` | 0.03404703447686597 | `0.034` | `F3_Tier2_results.json` |
| `gamma_hierarchical.RAG_theta0.1.sd_cluster_means` | 0.034556758990994814 | `0.035` | `F3_Tier2_results.json` |
| `gamma_hierarchical.summarization.mean` | 6.700728333333332 | `6.7` | `F3_Tier2_results.json` |
| `holdout_K4_5_summary[0].violation_rate` | 0.02 | `0.02` | `tier2_refit.json` |
| `holdout_K4_5_summary[1].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `holdout_K4_5_summary[2].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `holdout_K4_5_summary[4].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `holdout_K4_5_summary[5].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `keyResults.accuracies.trimmed_mean.lo` | 0.71846875 | `0.718` | `tier2_f45_results.json` |
| `original_reference_biased_vs_benign[0].bootstrap.mean` | 0.041832 | `0.042` | `tier2_phrasing_results.json` |
| `original_reference_biased_vs_benign[1].bootstrap.mean` | 0.0007879999999999989 | `0.001` | `tier2_phrasing_results.json` |
| `original_reference_biased_vs_benign[3].bootstrap.mean` | 0.017240000000000005 | `0.017` | `tier2_phrasing_results.json` |
| `results_per_contrast[0].bootstrap.mean` | 0.022387999999999995 | `0.022` | `tier2_phrasing_results.json` |
| `results_per_contrast[1].bootstrap.mean` | 0.023587999999999998 | `0.024` | `tier2_phrasing_results.json` |
| `results_per_contrast[2].bootstrap.mean` | 0.025108 | `0.025` | `tier2_phrasing_results.json` |
| `results_per_contrast[6].bootstrap.mean` | 0.0016859999999999974 | `0.0012` | `tier2_phrasing_results.json` |
| `results_per_contrast[7].bootstrap.mean` | 0.0020859999999999976 | `0.002` | `tier2_phrasing_results.json` |
| `results_per_contrast[8].bootstrap.mean` | 0.002165999999999998 | `0.002` | `tier2_phrasing_results.json` |
| `sensitivity.holdout_summary_p5[1].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `sensitivity.holdout_summary_p5[2].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `sensitivity.holdout_summary_p5[4].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `sensitivity.holdout_summary_p5[5].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `sensitivity.pooled_B_mean_p5` | 0.088626 | `0.089` | `tier2_refit.json` |
| `train_K3_summary[0].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `train_K3_summary[1].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |

## 方向 B：论文小数 → 产物支撑

- 论文小数 352 个，有支撑 245 个（支撑率 0.696）
- 机械噪音 23 个（版本号片段/日期/结构行，自动豁免）
- 已裁决 0 个（人工 verdict：noise/supported/critical）

### 人工复核清单（未裁决且非噪音）

- L26 `1.2`：∆MAE −0.034) versus RAG Γ=1.2 (p=.42, ∆MAE +0.008).
- L29 `8.1`：cells, conf 0.99) shows Γ monotonic 8.1→0.9 but with uninformative verbalized conf. We
- L64 `1.2`：with a larger distributional shift (Γ=12.3, p<.001) than RAG with θ=0.1 (Γ=1.2, p=.42), alongside
- L66 `0.45`：examined descriptively as a candidate proxy (r=0.45).
- L190 `0.45`：descriptive proxy; its sample correlation with Γ was r=0.45 in our data. All findings are sample-des
- L200 `0.999`：normal, slightly higher n for heavy tails). Our n=500 per architecture yields power >0.999 for the t
- L201 `0.08`：effect and minimum detectable dmin=0.18 at power 0.8. For the smaller RAG effect (dz=0.08 < 0.18), p
- L204 `2.5`：57 subjects. Models: Qwen3:4b, Gemma3:4b, DeepSeek-R1:7B, Qwen2.5:14B, served locally via Ollama at
- L216 `13.1`：whereas our Γ values (up to 13.1) reflect length-scale distances. The bound is descriptive.
- L246 `12.1`：Empirical estimates of Γ. Within our sample, per-seed Γ (prefix-length W1) for append-only: 12.1, 12
- L246 `12.5`：Empirical estimates of Γ. Within our sample, per-seed Γ (prefix-length W1) for append-only: 12.1, 12
- L247 `6.5`：12.0 (mean 12.3, SD 0.21, p<.001 vs. 0 by permutation); for summarization: 6.5, 6.9, 6.7 (mean 6.7, 
- L247 `6.9`：12.0 (mean 12.3, SD 0.21, p<.001 vs. 0 by permutation); for summarization: 6.5, 6.9, 6.7 (mean 6.7, 
- L248 `1.2`：for RAG θ=0.1: 1.1, 1.4, 1.0 (mean 1.2, SD 0.17, p=.42). The proxy correlation r(ℓ, Γ)=0.45 is descr
- L248 `0.45`：for RAG θ=0.1: 1.1, 1.4, 1.0 (mean 1.2, SD 0.17, p=.42). The proxy correlation r(ℓ, Γ)=0.45 is descr
- L254 `98.2`：Parse rates: Qwen3:4b 98.2%, Gemma3:4b 93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Unparseable
- L254 `93.3`：Parse rates: Qwen3:4b 98.2%, Gemma3:4b 93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Unparseable
- L254 `96.1`：Parse rates: Qwen3:4b 98.2%, Gemma3:4b 93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Unparseable
- L254 `2.5`：Parse rates: Qwen3:4b 98.2%, Gemma3:4b 93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Unparseable
- L254 `99.1`：Parse rates: Qwen3:4b 98.2%, Gemma3:4b 93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Unparseable
- L260 `0.45`：significance; r=0.45 is sample correlation between authority-marker length and Γ. Baselines K=1 (sin
- L261 `0.08`：ton, no-memory product 0.08) and K=2 (mean product 0.11, n=500 each) show product increases before
- L261 `0.11`：ton, no-memory product 0.08) and K=2 (mean product 0.11, n=500 each) show product increases before
- L273 `0.084`：[+0.014, +0.084]
- L274 `1.6`：1.6×10−5 ∗
- L285 `0.012`：[−0.012, +0.029]
- L287 `0.08`：K=1 singleton (no-memory) product 0.08; K=2 mean product 0.11 (n=500 each, Wilcoxon ∆vs K=3, p<0.01;
- L287 `0.11`：K=1 singleton (no-memory) product 0.08; K=2 mean product 0.11 (n=500 each, Wilcoxon ∆vs K=3, p<0.01;
- L290 `1.6`：Within our sample, append-only was associated with the largest shift (Γ=12.3, ∆MAE −0.034, p=1.6×10−
- L292 `1.2`：distinguishable from zero (Γ=1.2, p=.42, ∆MAE +0.008, p=0.38). Per-model patterns were consistent; e
- L295 `2.5`：Qwen3:4b append-only ∆MAE −0.034, Gemma3:4b append-only +0.035, Qwen2.5:14B append-only +0.012,
- L295 `0.012`：Qwen3:4b append-only ∆MAE −0.034, Gemma3:4b append-only +0.035, Qwen2.5:14B append-only +0.012,
- L299 `51.55`：memories for the first unified three-layer comparison. Training cost (51.55M vs 7.61B, 0.68%) separa
- L299 `7.61`：memories for the first unified three-layer comparison. Training cost (51.55M vs 7.61B, 0.68%) separa
- L304 `0.038`：the shift persisted after calibration, though reduced (Qwen: from −0.034 to +0.038–0.042; Gemma: fro
- L315 `0.039`：+0.039∗
- L317 `0.038`：+0.038∗
- L357 `2.5`：Gamma-DeltaMAE r=0.89 (9 combos excl Qwen2.5:14B, p=8.69×10−6; recomputed Pearson p=0.0012 on 9
- L357 `8.69`：Gamma-DeltaMAE r=0.89 (9 combos excl Qwen2.5:14B, p=8.69×10−6; recomputed Pearson p=0.0012 on 9
- L358 `2.5`：points via scipy.stats.pearsonr, analysis.json gamma_vs_delta_r), r=0.75 (12 combos incl Qwen2.5:14B
- L362 `0.032`：Cross-seed stability and proxy. ∆MAE for append-only across 3 seeds: −0.032, −0.036, −0.034 (SD
- L363 `0.6`：0.002); for RAG θ=0.1: +0.007, +0.010, +0.006 (SD 0.002); no significant seed effect (p>0.6). The au
- L364 `0.45`：marker length proxy correlated descriptively with Γ at r=0.45 (n=500, 95% CI [0.38, 0.52]), which we
- L405 `2.5`：Qwen2.5:14B
- L411 `2.5`：descriptive association Gamma-DeltaMAE r=0.89 (9 combos excl Qwen2.5:14B, p=8.69×10−6; recom-
- L411 `8.69`：descriptive association Gamma-DeltaMAE r=0.89 (9 combos excl Qwen2.5:14B, p=8.69×10−6; recom-
- L413 `2.5`：Qwen2.5:14B, p=0.005) (n=12 and n=9; Pearson, two-tailed; analysis.json gamma_vs_delta_r). Vertical
- L425 `8.69`：The append-only ∆MAE −0.034 shows a descriptive association with Γ at r=0.89 (descriptive, p=8.69×10
- L426 `2.5`：9 combos excl Qwen2.5:14B) and r=0.75 (p=0.005, 12 combos), consistent with Lemma 1 as descriptive
- L442 `0.15`：Limitations. (i) Single threshold θ=0.1; other thresholds (0.05, 0.15, 0.30) may yield different tra
- L447 `0.45`：∅> 0); the proxy r=0.45 is
- L466 `0.45`：(r=0.45) are both correlational and non-causal.
- L505 `2.5`：Qwen3:4b/Gemma3:4b/DeepSeek-R1:7B/Qwen2.5:14B, θ=0.1, n=500, seeds 42/43/44, B=5000) is archived
- L510 `2.5`：with gen_figures.py. Environment: Ollama with Qwen3:4b, Gemma3:4b, DeepSeek-R1:7B, Qwen2.5:14B
- L511 `1.26`：at temperature 0; Python 3.10; requirements.txt pins numpy 1.26, scipy 1.11, matplotlib 3.8. Seed 42
- L511 `3.8`：at temperature 0; Python 3.10; requirements.txt pins numpy 1.26, scipy 1.11, matplotlib 3.8. Seed 42
- L571 `12.2`：character, and with Γ ≈12.2 the bound gives |∆MAE| ≤0.049, close to the observed −0.034 for append-o
- L582 `98.2`：Parse rates: Qwen3:4b 98.2%, Gemma3:4b 93.3%,
- L582 `93.3`：Parse rates: Qwen3:4b 98.2%, Gemma3:4b 93.3%,
- L583 `96.1`：DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Unparseable cells (6.7%) excluded pairwise.
- L583 `2.5`：DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Unparseable cells (6.7%) excluded pairwise.
- L583 `99.1`：DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%. Unparseable cells (6.7%) excluded pairwise.
- L584 `0.08`：K=1/K=2 baselines (construction region). K=1 singleton (no-memory) product 0.08 and K=2 mean
- L585 `0.11`：product 0.11 (n=500 each, paired) increase before K≥3; Wilcoxon ∆vs K=3: p<0.01 (K=2 vs K=3),
- L594 `2.5`：mains loose but trend significant. Excl Qwen2.5:14B (smallest effect 0.004–0.012) raises r 0.75→0.89
- L594 `0.012`：mains loose but trend significant. Excl Qwen2.5:14B (smallest effect 0.004–0.012) raises r 0.75→0.89
- L596 `57.3`：The F4 128k paired McNemar p<10−546 is traceable to simulator.py L118–L145. The 57.3% production-
- L599 `0.999`：Power: at d=0.35, α=0.05, power 0.8 →n=67; n=500 gives power >0.999. Minimum detectable dmin=0.18 at
- L616 `1.6`：1.6×10−5
- L656 `0.018`：+0.018
- L665 `2.5`：Qwen2.5:14B
- L668 `0.012`：+0.012
- L671 `2.5`：Qwen2.5:14B
- L678 `2.5`：via scipy.stats.pearsonr (verify_r.py); loose vertical but trend significant. Excl Qwen2.5:14B (smal
- L679 `0.012`：effect 0.004–0.012) raises r 0.75→0.89 to avoid cherry-picking; both n=12 and n=9 reported; Table 2 
- L688 `2.5`：Excl Qwen2.5:14B (3×3)
- L690 `8.69`：8.69×10−6 rep. / 0.0012 recomputed
- L692 `0.42`：0.42, temperature 0.31, top_p 0.08.
- L692 `0.08`：0.42, temperature 0.31, top_p 0.08.
- L695 `0.15`：0.15→78%, 0.2→85%, 0.3→91%. Γ and ∆MAE are sample-descriptive for those thresholds (append-only
- ……共 84 个，见 JSON

### 机械噪音（自动豁免）

- `1.2`（section-heading）：1.2
- `0.08`（section-heading）：0.08
- `0.6`（section-heading）：0.6
- `0.45`（section-heading）：0.45
- `0.60`（section-heading）：0.60
- `2312.10997`（arxiv-id）：arXiv:2312.10997, 2024.
- `2207.05221`（arxiv-id）：arXiv preprint arXiv:2207.05221, 2022.
- `12.4`（section-heading）：12.4
- `0.42`（section-heading）：0.42
- `6.8`（section-heading）：6.8
- `1.3`（section-heading）：1.3
- `0.09`（section-heading）：0.09
- `13.1`（section-heading）：13.1
- `6.9`（section-heading）：6.9
- `0.11`（section-heading）：0.11
- `1.5`（section-heading）：1.5
- `11.8`（section-heading）：11.8
- `0.22`（section-heading）：0.22
- `6.2`（section-heading）：6.2
- `1.5`（section-heading）：1.5
- `1.2`（section-heading）：1.2
- `0.15`（section-heading）：0.15
- `0.20`（section-heading）：0.20