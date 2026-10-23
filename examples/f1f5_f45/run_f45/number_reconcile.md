# 数字对账报告（R3）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f45\extracted_text.txt`，证据目录：`F:\Research\_inbox\F1-F5_F45_2026-08-26\supplementary`
- 结论：**MAJOR**（裁决 critical 0，待复核 113，机械噪音 49，已裁决 0）
- 无证据目录：否

## 方向 A：产物统计数字 → 论文出现（论文未改数字）

- 核心统计数字 1242 个，其中 214 个在论文中找到一致值（命中率 0.1723）

| json_path | 值 | 论文 token | 来源 |
|---|---|---|---|
| `keyResults.mcnemar_per_strategy.injection[0].p_exact` | 0.0 | `0.0` | `tier2_f45_results.json` |
| `keyResults.mcnemar_per_strategy.mimicry[2].delta_p` | 0.07275 | `0.073` | `tier2_f45_results.json` |
| `keyResults.mcnemar_primary[0].cles` | 0.8489546629081512 | `0.849` | `tier2_f45_results.json` |
| `keyResults.mcnemar_primary[0].delta_p_bootstrap_hi` | 0.09675078124999999 | `0.097` | `tier2_f45_results.json` |
| `keyResults.mcnemar_primary[0].delta_p_bootstrap_lo` | 0.089 | `0.089` | `tier2_f45_results.json` |
| `keyResults.mcnemar_primary[0].p_holm` | 0.0 | `0.0` | `tier2_f45_results.json` |
| `keyResults.mcnemar_primary[1].delta_p` | 0.05853125 | `0.059` | `tier2_f45_results.json` |
| `keyResults.mcnemar_primary[1].delta_p_bootstrap_hi` | 0.06171875 | `0.062` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[0].cohens_g` | 0.4995283760415029 | `0.5` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[0].p_exact` | 0.0 | `0.0` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[1].c` | 0.0 | `0.0` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[1].cohens_g` | 0.5 | `0.5` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[1].p_exact` | 0.0 | `0.0` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[2].p_exact` | 0.0 | `0.0` | `tier2_f45_results.json` |
| `meta.alpha` | 0.05 | `0.05` | `tier2_phrasing_results.json` |
| `delta_hierarchical.RAG_theta0.1.sd_cluster_means` | 0.05950893164313473 | `0.060` | `F3_Tier2_results.json` |
| `delta_hierarchical.summarization.sd_cluster_means` | 0.060384793064471955 | `0.060` | `F3_Tier2_results.json` |
| `gamma_hierarchical.append-only.sd_cluster_means` | 0.03404703447686597 | `0.034` | `F3_Tier2_results.json` |
| `holdout_K4_5_summary[1].violation_rate` | 0.0 | `0.0` | `tier2_refit.json` |
| `holdout_K4_5_summary[2].violation_rate` | 0.0 | `0.0` | `tier2_refit.json` |
| `holdout_K4_5_summary[4].P_mean` | 0.1513 | `0.151` | `tier2_refit.json` |
| `holdout_K4_5_summary[4].violation_rate` | 0.0 | `0.0` | `tier2_refit.json` |
| `holdout_K4_5_summary[5].violation_rate` | 0.0 | `0.0` | `tier2_refit.json` |
| `keyResults.accuracies.trimmed_mean.hi` | 0.72834375 | `0.728` | `tier2_f45_results.json` |
| `keyResults.accuracies.trust_mean.mean` | 0.68903125 | `0.689` | `tier2_f45_results.json` |
| `keyResults.accuracies_per_strategy.injection.majority` | 0.43475 | `0.435` | `tier2_f45_results.json` |
| `keyResults.accuracies_per_strategy.injection.trimmed` | 0.68975 | `0.690` | `tier2_f45_results.json` |
| `keyResults.accuracies_per_strategy.injection.trust` | 0.548375 | `0.548` | `tier2_f45_results.json` |
| `keyResults.accuracies_per_strategy.mimicry.majority` | 0.7318125 | `0.732` | `tier2_f45_results.json` |
| `keyResults.accuracies_per_strategy.mimicry.trimmed` | 0.7569375 | `0.757` | `tier2_f45_results.json` |
| `keyResults.accuracies_per_strategy.mimicry.trust` | 0.8296875 | `0.830` | `tier2_f45_results.json` |
| `original_reference_biased_vs_benign[1].bootstrap.mean` | 0.0007879999999999989 | `0.001` | `tier2_phrasing_results.json` |
| `pooled_holdout.B_mean` | 0.069453 | `0.069` | `tier2_refit.json` |
| `pooled_holdout.P_mean` | 0.168 | `0.168` | `tier2_refit.json` |
| `sensitivity.holdout_summary_p5[1].violation_rate` | 0.0 | `0.0` | `tier2_refit.json` |
| `sensitivity.holdout_summary_p5[2].violation_rate` | 0.0 | `0.0` | `tier2_refit.json` |
| `sensitivity.holdout_summary_p5[4].P_mean` | 0.1513 | `0.151` | `tier2_refit.json` |
| `sensitivity.holdout_summary_p5[4].violation_rate` | 0.0 | `0.0` | `tier2_refit.json` |
| `sensitivity.holdout_summary_p5[5].violation_rate` | 0.0 | `0.0` | `tier2_refit.json` |
| `sensitivity.pooled_B_mean_p5` | 0.088626 | `0.089` | `tier2_refit.json` |

## 方向 B：论文小数 → 产物支撑

- 论文小数 623 个，有支撑 461 个（支撑率 0.74）
- 机械噪音 49 个（版本号片段/日期/结构行，自动豁免）
- 已裁决 0 个（人工 verdict：noise/supported/critical）

### 人工复核清单（未裁决且非噪音）

- L28 `0.098`：ity (paired ∆=+0.098, McNemar b=1566, c=0, p<10−100). In both cases c=0 within the
- L34 `0.620`：the finding: hybrid achieves 0.620 vs. 0.435 for majority under injection and 0.790 vs. 0.732
- L40 `99.78`：parse 99.78% is_real, SHA 798bbc2d (truncated SHA256 of real_llm_400_v6), verbalized
- L41 `0.985`：conf 0.985 vs 0.985 uninformative) reproduces c=0 pattern but confirms synthetic informa-
- L41 `0.985`：conf 0.985 vs 0.985 uninformative) reproduces c=0 pattern but confirms synthetic informa-
- L85 `0.620`：0.620 vs. 0.435 and mimicry 0.790 vs. 0.732 (both c=0). In all cases c=0 within the studied regime: 
- L129 `3.5`：than binary voting. Both require f < N/2, which holds here (2 < 3.5). For binary votes with odd N,
- L239 `0.08`：N(0.80, 0.08) truncated to [0, 1]. This models a confident-but-always-wrong adversary.
- L252 `2.5`：The four model families (Qwen3:4b, Gemma3:4b, DeepSeek-R1:7B, Qwen2.5:14B) serve as interchangeable
- L342 `3.5`：j vj > 3.5 (at least 4 votes for 1). Trust_mean
- L399 `0.098`：+0.098
- L405 `0.098`：+0.098
- L416 `0.185`：+0.185†
- L423 `0.620`：p<10−100); hybrid 0.620 vs. 0.435, ∆=+0.185 (McNemar b≈2960, c=0, p<10−400).
- L423 `0.185`：p<10−100); hybrid 0.620 vs. 0.435, ∆=+0.185 (McNemar b≈2960, c=0, p<10−400).
- L426 `0.098`：vs. 0.732, ∆=+0.098 (McNemar b=1566, c=0); hybrid 0.790 vs. 0.732, ∆=+0.058 (McNemar b≈928, c=0).
- L430 `0.098`：over majority is positive in both conditions within the studied regime (+0.114 injection, +0.098 mim
- L431 `0.185`：Hybrid advantage is also positive in both (+0.185 injection, +0.058 mimicry). McNemar c=0 in all cas
- L471 `0.112`：Injection advantage of trust over majority ranged +0.112 to +0.115 (SD 0.001); mimicry +0.097 to +0.
- L471 `0.099`：Injection advantage of trust over majority ranged +0.112 to +0.115 (SD 0.001); mimicry +0.097 to +0.
- L488 `0.098`：+0.098
- L493 `0.098`：positive: trust +0.114 injection / +0.098 mimicry; hybrid +0.185 injection / +0.058 mimicry. There i
- L493 `0.185`：positive: trust +0.114 injection / +0.098 mimicry; hybrid +0.185 injection / +0.058 mimicry. There i
- L521 `2.5`：Qwen2.5:14B
- L545 `2.5`：Qwen2.5:14B
- L557 `0.620`：0.620 injection (midway between trust 0.548 and trim 0.690) and 0.790 mimicry (between 0.830 and 0.7
- L560 `0.563`：Trust score statistics. Honest mean confidence 0.563 (SD 0.08), mixture of correct (µ=0.70, 65%) and
- L560 `0.08`：Trust score statistics. Honest mean confidence 0.563 (SD 0.08), mixture of correct (µ=0.70, 65%) and
- L563 `0.522`：honest) and 0.522 under mimicry (50% correct with anti-correlated confidence, slightly lower than ho
- L709 `3.12`：Environment: Python 3.12, numpy, scipy, matplotlib. Seed 42 throughout; per-trial seeds 42 + trial ×
- L710 `2.5`：model_idx×10000. Four model families (Qwen3:4b, Gemma3:4b, DeepSeek-R1:7B, Qwen2.5:14B) are seeded
- L793 `2.5`：Qwen2.5:14B
- L821 `2.5`：Qwen2.5:14B
- L851 `2.7`：2.7×10−138
- L855 `2.2`：2.2×10−137
- L858 `2.5`：Qwen2.5:14B inj
- L867 `6.2`：6.2×10−120
- L875 `6.3`：6.3×10−117
- L878 `2.5`：Qwen2.5:14B mim
- L879 `3.2`：3.2×10−117
- L944 `0.08`：µ−=0.30 (σ=0.10) when wrong, truncated to [0, 1]. This yields ECE ≈0.08 when measured against empiri
- L946 `0.56`：confidence is a mixture: 0.65×0.70+0.35×0.30 = 0.56, matching the observed 0.563. Captured injection
- L946 `0.563`：confidence is a mixture: 0.65×0.70+0.35×0.30 = 0.56, matching the observed 0.563. Captured injection
- L947 `0.08`：fidence (µ=0.80, σ=0.08) is deliberately higher than honest to model a confident adversary; captured
- L948 `0.525`：confidence is bimodal (µ=0.30 when correct, 0.75 when wrong), yielding mean 0.5×0.30 + 0.5×0.75 = 0.
- L949 `0.522`：matching observed 0.522.
- L952 `0.2`：confidence bin shows accuracy increasing from ≈0.35 at [0.2, 0.3] to ≈0.85 at [0.7, 0.8]. Under mimi
- L955 `0.2`：[0.2, 0.3] rises from 0.35 to 0.42 because captured voters contribute low-confidence correct votes. 
- L955 `0.42`：[0.2, 0.3] rises from 0.35 to 0.42 because captured voters contribute low-confidence correct votes. 
- L959 `0.51818`：c > 0 is exponentially unlikely. Under H0: b = c, the probability of c=0, b=1818 is 2×0.51818 ≈10−54
- L967 `0.098`：Our observed ∆=0.114 (injection) and 0.098 (mimicry) are 3–4× that
- L969 `0.92`：aim to rule out a sign flip, not just detect a small effect. Per-model M=4,000 has power 0.92 for ∆=
- L971 `1.96`：Precision. Normal-approximation 95% CIs for per-rule correctness: ±1.96
- L975 `0.012`：seed 42) are ∆inj=0.114±0.012 and ∆mim=0.098±0.011, both far from zero. Hybrid ∆CIs are 0.185±0.011
- L975 `0.098`：seed 42) are ∆inj=0.114±0.012 and ∆mim=0.098±0.011, both far from zero. Hybrid ∆CIs are 0.185±0.011
- L975 `0.185`：seed 42) are ∆inj=0.114±0.012 and ∆mim=0.098±0.011, both far from zero. Hybrid ∆CIs are 0.185±0.011
- L1018 `3.12`：Compute. Simulator runtime ≈4 minutes on a single core (Python 3.12, numpy 1.26, scipy 1.12) for 128
- L1018 `1.26`：Compute. Simulator runtime ≈4 minutes on a single core (Python 3.12, numpy 1.26, scipy 1.12) for 128
- L1019 `3.8`：cells; figure generation ≈10 seconds (matplotlib 3.8). No GPU required. Memory < 500 MB. Reproducibi
- L1028 `0.302`：wrong 0.302 ± 0.10 (injection) and 0.699 ± 0.10 vs. 0.301 ± 0.10 (mimicry), confirming informativene
- L1028 `0.301`：wrong 0.302 ± 0.10 (injection) and 0.699 ± 0.10 vs. 0.301 ± 0.10 (mimicry), confirming informativene
- L1049 `2.5`：model_names = ["Qwen3:4b","Gemma3:4b","DeepSeek-R1:7B","Qwen2.5:14B"]
- L1067 `0.08`：v = 1-y; c = trunc_gauss(0.80, 0.08)
- L1093 `1.96`：Normal CI: p ± 1.96
- L1106 `0.540`：[0.540, 0.556]
- L1106 `0.556`：[0.540, 0.556]
- L1107 `0.540`：[0.540, 0.556]
- L1107 `0.556`：[0.540, 0.556]
- L1113 `0.443`：[0.427, 0.443]
- L1114 `0.443`：[0.427, 0.443]
- L1120 `0.697`：[0.683, 0.697]
- L1121 `0.697`：[0.683, 0.697]
- L1127 `0.612`：[0.612, 0.628]
- L1128 `0.612`：[0.612, 0.628]
- L1134 `0.102`：[0.102, 0.126]
- L1135 `0.103`：[0.103, 0.125]
- L1136 `0.098`：+0.098
- L1137 `0.087`：[0.087, 0.109]
- L1137 `0.109`：[0.087, 0.109]
- L1138 `0.108`：[0.088, 0.108]
- ……共 113 个，见 JSON

### 机械噪音（自动豁免）

- `0.620`（section-heading）：0.620
- `0.2`（section-heading）：0.2
- `0.6`（section-heading）：0.6
- `0.15`（section-heading）：0.15
- `0.20`（section-heading）：0.20
- `0.621`（section-heading）：0.621
- `0.549`（section-heading）：0.549
- `0.434`（section-heading）：0.434
- `0.620`（section-heading）：0.620
- `0.434`（section-heading）：0.434
- `0.619`（section-heading）：0.619
- `0.620`（section-heading）：0.620
- `0.731`（section-heading）：0.731
- `0.829`（section-heading）：0.829
- `0.2`（section-heading）：0.2
- `0.6`（section-heading）：0.6
- `0.2`（section-heading）：0.2
- `0.6`（section-heading）：0.6
- `2112.00861`（arxiv-id）：In arXiv preprint arXiv:2112.00861, 2021.
- `0.621`（section-heading）：0.621
- `0.549`（section-heading）：0.549
- `0.434`（section-heading）：0.434
- `0.434`（section-heading）：0.434
- `0.620`（section-heading）：0.620
- `0.434`（section-heading）：0.434
- `0.434`（section-heading）：0.434
- `0.619`（section-heading）：0.619
- `0.620`（section-heading）：0.620
- `0.731`（section-heading）：0.731
- `0.731`（section-heading）：0.731
- `0.829`（section-heading）：0.829
- `0.620`（section-heading）：0.620
- `0.590`（section-heading）：0.590
- `0.609`（section-heading）：0.609
- `0.592`（section-heading）：0.592
- `0.603`（section-heading）：0.603
- `0.885`（section-heading）：0.885
- `0.969`（section-heading）：0.969
- `0.951`（section-heading）：0.951
- `0.969`（section-heading）：0.969
- ……共 49 个