# 数字对账报告（R3）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f2\extracted_text.txt`，证据目录：`F:\Research\_inbox\F1-F5_F45_2026-08-26\supplementary`
- 结论：**MAJOR**（裁决 critical 0，待复核 99，机械噪音 30，已裁决 0）
- 无证据目录：否

## 方向 A：产物统计数字 → 论文出现（论文未改数字）

- 核心统计数字 1242 个，其中 254 个在论文中找到一致值（命中率 0.2045）

| json_path | 值 | 论文 token | 来源 |
|---|---|---|---|
| `keyResults.mcnemar_per_strategy.injection[0].p_exact` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_primary[0].p_holm` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[0].cohens_g` | 0.4995283760415029 | `0.5` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[0].p_exact` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[1].c` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[1].cohens_g` | 0.5 | `0.5` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[1].p_exact` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[2].delta_p` | 0.1400625 | `0.14` | `tier2_f45_results.json` |
| `keyResults.mcnemar_secondary[2].p_exact` | 0.0 | `0.00` | `tier2_f45_results.json` |
| `meta.alpha` | 0.05 | `0.05` | `tier2_phrasing_results.json` |
| `gamma_hierarchical.append-only.sd_cluster_means` | 0.03404703447686597 | `0.034` | `F3_Tier2_results.json` |
| `gamma_hierarchical.RAG_theta0.1.sd_cluster_means` | 0.034556758990994814 | `0.035` | `F3_Tier2_results.json` |
| `gamma_hierarchical.summarization.mean` | 6.700728333333332 | `6.7` | `F3_Tier2_results.json` |
| `holdout_K4_5_summary[0].violation_rate` | 0.02 | `0.02` | `tier2_refit.json` |
| `holdout_K4_5_summary[1].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `holdout_K4_5_summary[2].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `holdout_K4_5_summary[4].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `holdout_K4_5_summary[5].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `keyResults.accuracies_per_strategy.injection.trimmed` | 0.68975 | `0.69` | `tier2_f45_results.json` |
| `original_reference_biased_vs_benign[0].bootstrap.mean` | 0.041832 | `0.042` | `tier2_phrasing_results.json` |
| `original_reference_biased_vs_benign[3].bootstrap.mean` | 0.017240000000000005 | `0.017` | `tier2_phrasing_results.json` |
| `results_per_contrast[6].bootstrap.mean` | 0.0016859999999999974 | `0.002` | `tier2_phrasing_results.json` |
| `results_per_contrast[7].bootstrap.mean` | 0.0020859999999999976 | `0.002` | `tier2_phrasing_results.json` |
| `results_per_contrast[8].bootstrap.mean` | 0.002165999999999998 | `0.002` | `tier2_phrasing_results.json` |
| `sensitivity.holdout_summary_p5[1].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `sensitivity.holdout_summary_p5[2].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `sensitivity.holdout_summary_p5[4].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `sensitivity.holdout_summary_p5[5].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `train_K3_summary[0].P_mean` | 0.2598 | `0.26` | `tier2_refit.json` |
| `train_K3_summary[0].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `train_K3_summary[1].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `train_K3_summary[2].violation_rate` | 0.0 | `0.00` | `tier2_refit.json` |
| `c0_refit.c0_primary` | 0.179905 | `0.18` | `tier2_refit.json` |
| `c0_refit.c0_secondary_p5` | 0.22957 | `0.23` | `tier2_refit.json` |
| `c0_refit.per_gamma_mins.0.5` | 0.179905 | `0.18` | `tier2_refit.json` |
| `c0_refit.train_coverage_primary` | 1.0 | `1.0` | `tier2_refit.json` |
| `delta_hierarchical.append-only.p_boot_cluster` | 0.0 | `0.00` | `F3_Tier2_results.json` |
| `delta_hierarchical.append-only.p_boot_holm` | 0.0 | `0.00` | `F3_Tier2_results.json` |
| `delta_hierarchical.append-only.se_boot` | 0.0028676216251913374 | `0.003` | `F3_Tier2_results.json` |
| `delta_hierarchical.append-only.se_cluster` | 0.002854478937117831 | `0.003` | `F3_Tier2_results.json` |

## 方向 B：论文小数 → 产物支撑

- 论文小数 451 个，有支撑 322 个（支撑率 0.714）
- 机械噪音 30 个（版本号片段/日期/结构行，自动豁免）
- 已裁决 0 个（人工 verdict：noise/supported/critical）

### 人工复核清单（未裁决且非噪音）

- L16 `10.88`：tightness ratio P/B of 5–10× for γ ∈{0.5, 1.0} (median 10.88× across the 9 cells). We estimate ρ ≈0.
- L17 `0.08`：via intraclass correlation. Baselines at K=1 (P=0.08) and K=2 (P=0.11) show the product increases
- L17 `0.11`：via intraclass correlation. Baselines at K=1 (P=0.08) and K=2 (P=0.11) show the product increases
- L19 `10.88`：The construction is loose (P/B 5–10×, median 10.88× after expansion), indicating it does not tightly
- L22 `0.62`：[0.62,0.74] to avoid contradiction with the survey 0/15 zero-success case where CI is degenerate. Th
- L46 `10.88`：P/B (5–10× for γ ∈{0.5, 1.0}, median 10.88×) as a limitation.
- L108 `0.62`：predicts iff ai ≥τ(γ) where τ(γ) = 1/(1 + exp(−γ)) calibrates abstention; γ ∈{0.5, 1.0, 2.0} yields 
- L128 `2.5`：Qwen2.5:14B via Ollama, plus Qwen2.5:7b via API as fifth family member for cross-family robustness (
- L128 `2.5`：Qwen2.5:14B via Ollama, plus Qwen2.5:7b via API as fifth family member for cross-family robustness (
- L129 `98.2`：+ API model), temperature 0, seeds 42–51 (10 seeds). Parse rates: Qwen3:4b 98.2%, Gemma3:4b 93.3%, D
- L129 `93.3`：+ API model), temperature 0, seeds 42–51 (10 seeds). Parse rates: Qwen3:4b 98.2%, Gemma3:4b 93.3%, D
- L130 `96.1`：96.1%, Qwen2.5:14B 99.1%, Qwen2.5:7b 98.7% (API); unparseable votes excluded per cell (at most 6.7% 
- L130 `2.5`：96.1%, Qwen2.5:14B 99.1%, Qwen2.5:7b 98.7% (API); unparseable votes excluded per cell (at most 6.7% 
- L130 `99.1`：96.1%, Qwen2.5:14B 99.1%, Qwen2.5:7b 98.7% (API); unparseable votes excluded per cell (at most 6.7% 
- L130 `2.5`：96.1%, Qwen2.5:14B 99.1%, Qwen2.5:7b 98.7% (API); unparseable votes excluded per cell (at most 6.7% 
- L130 `98.7`：96.1%, Qwen2.5:14B 99.1%, Qwen2.5:7b 98.7% (API); unparseable votes excluded per cell (at most 6.7% 
- L131 `99.78`：Note: Gemma3:4b 99.78% supplementary accuracy (Appendix Table S1, uncalibrated confidence, Beta(1, 1
- L132 `0.989`：prior, Wilson CI [0.989, 1.000]) is reported as supplementary, not primary; primary outcomes use the
- L182 `0.53`：assumes K ≥3 for normal approximation; K=1, 2 use exact binomial, values 0.53 →1.21 scaled hold for 
- L182 `1.21`：assumes K ≥3 for normal approximation; K=1, 2 use exact binomial, values 0.53 →1.21 scaled hold for 
- L200 `10.88`：(median 10.88× across 9 cells; reaching 20–34× at γ=2.0 where the exponential term makes B very smal
- L210 `0.021`：Empirical B(K, γ) values. With c0 = 0.05: B(3, 0.5) = 0.050, B(3, 1.0) = 0.021, B(3, 2.0) = 0.008, B
- L217 `10.88`：and B(K, γ) 0.004–0.050. The tightness ratio P/B is 5–10× for γ ∈{0.5, 1.0} (median 10.88× across 9 
- L232 `5.2`：5.2×
- L237 `0.22`：0.22 ± 0.04
- L239 `10.3`：10.3×
- L246 `23.7`：23.7×
- L260 `10.6`：10.6×
- L274 `5.1`：5.1×
- L279 `0.15`：0.15 ± 0.03
- L281 `11.2`：11.2×
- L288 `33.7`：33.7×
- L292 `0.08`：Baselines: K=1: P=0.08, I=0.53, acc= 0.65
- L292 `0.53`：Baselines: K=1: P=0.08, I=0.53, acc= 0.65
- L293 `0.11`：K=2: P=0.11, I=0.82, acc= 0.69
- L294 `29.5`：K=6 observation (γ=1.0): P=0.33, B=0.011, P/B=29.5×, I=1.28, acc= 0.79 (observation, not held-out pr
- L294 `1.28`：K=6 observation (γ=1.0): P=0.33, B=0.011, P/B=29.5×, I=1.28, acc= 0.79 (observation, not held-out pr
- L296 `0.53`：variance, Fisher-like) increased 0.53 →0.82 →1.00 →1.12 →1.21 for K = 1 →2 →3 →4 →5 (Table 3), consi
- L296 `1.21`：variance, Fisher-like) increased 0.53 →0.82 →1.00 →1.12 →1.21 for K = 1 →2 →3 →4 →5 (Table 3), consi
- L297 `3.33`：with Lemma 2 where variance decreases as 1/K. The theoretical floor at ρ = 0.3 is I(∞) = 1/ρ = 3.33 
- L303 `0.08`：K=1, 2 baselines. P(K=1) = 0.08 and P(K=2) = 0.11 show the product increases from K=1 before the con
- L303 `0.11`：K=1, 2 baselines. P(K=1) = 0.08 and P(K=2) = 0.11 show the product increases from K=1 before the con
- L304 `0.53`：region K ≥3. The Fisher information at K=1 (I = 0.53, scaled) is the lowest, confirming that a singl
- L307 `0.15`：than K=5 (P=0.15 at γ=1.0), possibly due to saturation effects or the specific episode set. We repor
- L329 `2.5`：Qwen2.5:14B
- L334 `0.09`：Increasing K at fixed γ=1.0 reduced P by ≈0.04 per K step (descriptive point estimate; 95% bootstrap
- L336 `0.08`：≈0.03 per doubling (descriptive point estimate; 95% CI [−0.02, 0.08], overlapping zero, not signific
- L338 `16.8`：Cross-model comparison. Friedman test over 4 models × 9 cells (n=9 blocks) gave χ2=16.8, p=0.002; Ne
- L339 `1.52`：= 1.52 (Figure 2). No single model dominates overall product rankings (overlapping intervals).
- L376 `2.5`：Qwen2.5:14B
- L388 `1.52`：Figure 2: Critical difference diagram: mean ranks of the four models over the 9 (K, γ) cells, CD = 1
- L395 `10.88`：exponential term in B makes the construction value very small. The median P/B ratio across all 9 cel
- L399 `51.55`：single-tier baselines. The Abstract 51.55M vs. 7.61B 0.68% figure separates training GPU-hours (12.4
- L399 `7.61`：single-tier baselines. The Abstract 51.55M vs. 7.61B 0.68% figure separates training GPU-hours (12.4
- L399 `12.4`：single-tier baselines. The Abstract 51.55M vs. 7.61B 0.68% figure separates training GPU-hours (12.4
- L403 `10.88`：with a large margin (P/B ratio 5–10× for γ ∈{0.5, 1.0}, median 10.88×). The construction does not ti
- L470 `0.048`：Refitting c0 via leave-one-K-out CV gives c0 = 0.048 →0.052 (range 0.048-0.052), P/B 4.8-9.2×, showi
- L470 `0.052`：Refitting c0 via leave-one-K-out CV gives c0 = 0.048 →0.052 (range 0.048-0.052), P/B 4.8-9.2×, showi
- L470 `0.048`：Refitting c0 via leave-one-K-out CV gives c0 = 0.048 →0.052 (range 0.048-0.052), P/B 4.8-9.2×, showi
- L470 `0.052`：Refitting c0 via leave-one-K-out CV gives c0 = 0.048 →0.052 (range 0.048-0.052), P/B 4.8-9.2×, showi
- L470 `4.8`：Refitting c0 via leave-one-K-out CV gives c0 = 0.048 →0.052 (range 0.048-0.052), P/B 4.8-9.2×, showi
- L470 `9.2`：Refitting c0 via leave-one-K-out CV gives c0 = 0.048 →0.052 (range 0.048-0.052), P/B 4.8-9.2×, showi
- L476 `10.88`：for γ ∈{0.5, 1.0}, median 10.88×), and overreliance on it could lead practitioners to believe a K=5 
- L503 `2.5`：R1:7B (tag 755ced02ce7b), Qwen2.5:14B (tag 7cdf5a0187d5); Python 3.10; requirements.txt locks numpy=
- L503 `1.26`：R1:7B (tag 755ced02ce7b), Qwen2.5:14B (tag 7cdf5a0187d5); Python 3.10; requirements.txt locks numpy=
- L504 `3.8`：scipy==1.11, matplotlib==3.8.
- L551 `10.88`：10.88×) reflects this.
- L553 `57.3`：57.3% production-investment ratio cites LangChain PR #1300 line 42 for provenance.
- L555 `98.2`：Per-model breakdown for P vs. B margins (mean±SD, 10 seeds) in Table 5. Parse rates: Qwen3:4b 98.2%,
- L556 `93.3`：93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%; unparseable votes excluded per cell (max 6.7% in Gem
- L556 `96.1`：93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%; unparseable votes excluded per cell (max 6.7% in Gem
- L556 `2.5`：93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%; unparseable votes excluded per cell (max 6.7% in Gem
- L556 `99.1`：93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%; unparseable votes excluded per cell (max 6.7% in Gem
- L566 `0.25`：0.25 ± 0.04
- L574 `10.0`：10.0×
- L580 `10.0`：10.0×
- L586 `10.0`：10.0×
- L592 `5.4`：5.4×
- L598 `11.4`：11.4×
- L604 `5.2`：5.2×
- ……共 99 个，见 JSON

### 机械噪音（自动豁免）

- `0.021`（section-heading）：0.021
- `1.21`（section-heading）：1.21
- `1.21`（section-heading）：1.21
- `1.21`（section-heading）：1.21
- `0.20`（section-heading）：0.20
- `0.22`（section-heading）：0.22
- `0.24`（section-heading）：0.24
- `1.5`（section-heading）：1.5
- `0.2`（section-heading）：0.2
- `0.6`（section-heading）：0.6
- `0.15`（section-heading）：0.15
- `0.20`（section-heading）：0.20
- `0.25`（section-heading）：0.25
- `0.2`（section-heading）：0.2
- `0.15`（section-heading）：0.15
- `0.20`（section-heading）：0.20
- `0.25`（section-heading）：0.25
- `0.6`（section-heading）：0.6
- `1.2`（section-heading）：1.2
- `1.3`（section-heading）：1.3
- `2312.10997`（arxiv-id）：Retrieval-augmented generation for large language models: A survey. arXiv preprint arXiv:2312.10997,
- `2207.05221`（arxiv-id）：arXiv:2207.05221, 2022.
- `0.021`（section-heading）：0.021
- `0.53`（section-heading）：0.53
- `0.53`（section-heading）：0.53
- `1.21`（section-heading）：1.21
- `0.44`（section-heading）：0.44
- `1.28`（section-heading）：1.28
- `0.42`（section-heading）：0.42
- `3.33`（section-heading）：3.33