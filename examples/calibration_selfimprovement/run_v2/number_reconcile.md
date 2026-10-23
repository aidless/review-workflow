# 数字对账报告（R3）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`，证据目录：`F:\deepseek\papers\calibration-self-improvement\evidence`
- 结论：**PASS**（裁决 critical 0，待复核 0，机械噪音 29，已裁决 193）
- 无证据目录：否

## 方向 A：产物统计数字 → 论文出现（论文未改数字）

- 核心统计数字 1963 个，其中 1099 个在论文中找到一致值（命中率 0.5599）

| json_path | 值 | 论文 token | 来源 |
|---|---|---|---|
| `cohens_kappa` | 0.699 | `0.699` | `dual_judge_summary.json` |
| `comparison_to_existing.existing_d0.7.L2_before.power_McNemar` | 0.0 | `0.0002` | `power_recomputed.json` |
| `comparison_to_existing.existing_d0.7.provenance.alpha` | 0.05 | `0.05` | `power_recomputed.json` |
| `L2_before.power_McNemar` | 0.0 | `0.0002` | `power_curve.json` |
| `llama3.2-1b.cohens_kappa` | 0.91 | `0.91` | `per_source_judge_agreement.json` |
| `provenance.alpha` | 0.05 | `0.05` | `power_curve.json` |
| `0.3_1.error_rate` | 0.276 | `0.276` | `lvu_cons_pareto.json` |
| `0.3_2.error_rate` | 0.226 | `0.226` | `lvu_cons_pareto.json` |
| `0.5_1.error_rate` | 0.26 | `0.26` | `lvu_cons_pareto.json` |
| `0.5_2.error_rate` | 0.21 | `0.21` | `lvu_cons_pareto.json` |
| `binned.bins[6].mean_conf` | 0.9 | `0.90` | `estimators_real_comparison.json` |
| `binned.bins[7].mean_conf` | 0.95 | `0.95` | `estimators_real_comparison.json` |
| `binned.bins[9].mean_conf` | 1.0 | `1.0` | `estimators_real_comparison.json` |
| `bins[2].mean_conf` | 0.9 | `0.90` | `figure_data_reliability.json` |
| `bins[3].mean_conf` | 0.95 | `0.95` | `figure_data_reliability.json` |
| `bins[4].mean_conf` | 1.0 | `1.0` | `figure_data_reliability.json` |
| `bins_all[6].mean_conf` | 0.9 | `0.90` | `figure_data_reliability.json` |
| `bins_all[7].mean_conf` | 0.95 | `0.95` | `figure_data_reliability.json` |
| `bins_all[9].mean_conf` | 1.0 | `1.0` | `figure_data_reliability.json` |
| `deepseek-r1-7b.ceiling_rate` | 0.7222 | `0.722` | `summary.json` |
| `degeneracy.T0.0.ceiling_rate` | 0.9 | `0.90` | `temperature_ablation.json` |
| `degeneracy.T0.0.ceiling_rate` | 0.9 | `0.90` | `temperature_ablation_real.json` |
| `degeneracy.T0.2.ceiling_rate` | 0.73 | `0.73` | `temperature_ablation.json` |
| `degeneracy.T0.2.ceiling_rate` | 0.73 | `0.73` | `temperature_ablation_real.json` |
| `degeneracy.T0.5.ceiling_rate` | 0.5 | `0.5` | `temperature_ablation.json` |
| `degeneracy.T0.5.ceiling_rate` | 0.5 | `0.5` | `temperature_ablation_real.json` |
| `eta_j_posterior.mean` | 0.1 | `0.1` | `human_gold_300.json` |
| `examples.pilot_30.ceiling_rate` | 0.9 | `0.90` | `msi_saturation_warning.json` |
| `examples.qwen2.5-1.5b.ceiling_rate` | 0.0 | `0.0002` | `msi_saturation_warning.json` |
| `examples.qwen2.5-7b.ceiling_rate` | 0.3 | `0.30` | `msi_saturation_warning.json` |
| `fig_crossmodel_conf.models.deepseek-r1-7b.ceiling_rate` | 0.7222 | `0.722` | `figure_data_extended.json` |
| `fig_crossmodel_conf.models.llama3.2-1b.ceiling_rate` | 0.2 | `0.20` | `figure_data_extended.json` |
| `fig_crossmodel_conf.models.qwen2.5-1.5b-instruct-q4_K_M.ceiling_rate` | 0.2222 | `0.222` | `figure_data_extended.json` |
| `fig_crossmodel_conf.models.qwen2.5-3b.ceiling_rate` | 0.9 | `0.90` | `figure_data_extended.json` |
| `fold_rows[10].mean_conf_raw` | 0.98 | `0.98` | `oos_temperature_results.json` |
| `fold_rows[11].mean_conf_scaled` | 0.8327 | `0.833` | `oos_temperature_results.json` |
| `fold_rows[12].mean_conf_raw` | 0.9667 | `0.967` | `oos_temperature_results.json` |
| `fold_rows[13].mean_conf_raw` | 0.9667 | `0.967` | `oos_temperature_results.json` |
| `fold_rows[14].mean_conf_raw` | 0.98 | `0.98` | `oos_temperature_results.json` |
| `fold_rows[5].mean_conf_scaled` | 0.5067 | `0.507` | `oos_temperature_results.json` |

## 方向 B：论文小数 → 产物支撑

- 论文小数 993 个，有支撑 771 个（支撑率 0.7764）
- 机械噪音 29 个（版本号片段/日期/结构行，自动豁免）
- 已裁决 193 个（人工 verdict：noise/supported/critical）

### 人工复核清单（未裁决且非噪音）

- 无（全部已支撑 / 已豁免 / 已裁决）

### 已裁决明细

| token | verdict | note |
|---|---|---|
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `0.334` | supported | Qwen2.5-7B MMLU MSI：evidence/census/census_analysis.json overall.msi=0.333（300-task），significance_an |
| `0.334` | supported | Qwen2.5-7B MMLU MSI：evidence/census/census_analysis.json overall.msi=0.333（300-task），significance_an |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `1.5` | noise | 模型名后缀 Qwen2.5-1.5B，非独立数字声明 |
| `36.7` | supported | exact 高置信错误率 = 11/30（19/30 正确），可由 analysis_summary accuracy_pct 63.3 推导 |
| `13.3` | supported | tolerant 高置信错误率 = 4/30（26/30 正确），由 accuracy_pct 86.7 推导 |
| `88.4` | supported | Clopper-Pearson 95% CI 下界 for 30/30，标准统计量 = 0.8841 |
| `2.74` | supported | evidence/analysis_summary.json counterfactual_v15.temperature=2.7358 |
| `14.2` | supported | evidence/analysis_summary.json v1_tolerant.thermometer.brier_rel_drop_pct：14.3（未舍入）/14.2（舍入值） |
| `0.887` | supported | sigmoid(logit(1-eps)/6.71)，可由 T=6.71 与退化分布推导 |
| `6.64` | supported | evidence/analysis_summary.json v1_tolerant.thermometer.T_fit_mass_only=6.6439 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `10.98` | supported | Brier 界 = sum|2c_i-1| = 10.98/30=0.366，可由置信分布推导 |
| `2.2` | supported | MSE 比值（0.0014/0.0059/0.0135），可由模拟证据推导 |
| `5.04` | supported | h 网格 MSE 优势比值，模拟证据推导 |
| `5.26` | supported | h 网格 MSE 优势比值，模拟证据推导 |
| `0.71` | supported | evidence/estimators_real_comparison.json 出现 0.71（degenerate 平均） |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `10.98` | supported | Brier 界 = sum|2c_i-1| = 10.98/30=0.366，可由置信分布推导 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `1.5` | noise | 模型名后缀 Qwen2.5-1.5B，非独立数字声明 |
| `1.2` | supported | ECE 翻转比值 1.2-4.0×，由 census 各模型 exact/tolerant ECE 推导 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `1.5` | noise | 模型名后缀 Qwen2.5-1.5B，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `1.5` | noise | 模型名后缀 Qwen2.5-1.5B，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `1.5` | noise | 模型名后缀 Qwen2.5-1.5B，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `1.5` | noise | 模型名后缀 Qwen2.5-1.5B，非独立数字声明 |
| `0.241` | supported | DeepSeek-R1-7B tolerant ECE：evidence/oos_ece_per_model_report.json 及 multi_model 数据含 0.241 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `16.4` | supported | +16.4 = 0.782-0.618，可由对应对齐数据推导 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `0.378` | supported | 0.502-0.124=0.378，表中同列可推导 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `2.5` | noise | 模型名后缀 Qwen2.5-*，非独立数字声明 |
| `1.5` | noise | 模型名后缀 Qwen2.5-1.5B，非独立数字声明 |

### 机械噪音（自动豁免）

- `3.2`（model-suffix）：disabled, Llama-3.2-1B; temperature 0, local inference via Ollama).
- `3.2`（model-suffix）：while DeepSeek-R1 and Llama-3.2 emit 8--10 distinct values with lower
- `3.2`（model-suffix）：not strictly monotonic: Llama-3.2-1B has the most distinct values of all
- `3.2`（model-suffix）：(3--6 distinct values, mass at 1.0); DeepSeek-R1-7B and Llama-3.2-1B spread
- `3.2`（model-suffix）：Llama-3.2-1B ($\kappa=0.91$) and the Qwen2.5-1.5B/3B sources
- `3.2`（model-suffix）：lowest-accuracy source, Llama-3.2-1B, has near-maximal agreement) but
- `3.2`（model-suffix）：Llama-3.2-1B (Meta) & 0.278 / 0.389 & 0.484 / 0.395 & 0.800 & 10 & 0.20 \\
- `3.2`（model-suffix）：Llama-3.2-1B at $-14\%$ ($0.395 \rightarrow 0.339$); the reduction does not
- `3.2`（model-suffix）：Llama-3.2-1B, with the smallest gap, still shows $-14\%$).
- `3.2`（model-suffix）：Llama-3.2-1B & 0.389 & 0.395 & 0.391 & 0.339 & 0.878 \\
- `3.2`（model-suffix）：Llama-3.2-1B the NLL-optimal $T$ saturates the grid at 20, and (ii) the
- `3.2`（model-suffix）：model, and for Llama-3.2-1B the ECE improvement ($0.395 \rightarrow 0.161$)
- `3.2`（model-suffix）：Qwen2.5-3B, Qwen2.5-1.5B, Llama-3.2-1B; two seeds, so the spread is
- `3.2`（model-suffix）：Llama-3.2-1B; the DeepSeek-R1-7B run was omitted because the shared GPU
- `3.2`（model-suffix）：Llama-3.2-1B $0.544$ vs.\ $0.395$ (Table~\ref{tab:holdout}). The
- `3.2`（model-suffix）：Llama-3.2-1B ($0.433$ vs.\ $0.389$ accuracy, ECE $0.544$ vs.\ $0.395$),
- `3.2`（model-suffix）：Llama-3.2-1B & 0.433 / 0.389 & 0.544 / 0.395 & 0.511 / 0.543 & 0.200 / 0.200 \\
- `3.2`（model-suffix）：Llama-3.2-1B & 20.0$^*$ & 0.395 & 0.161 & 0.406 & 0.260 & 0.487 \\
- `3.2`（model-suffix）：Llama-3.2-1B & 0.474 / 0.460 & 0.40 & 0.10 \\
- `3.2`（model-suffix）：sample) for four local models (Qwen2.5-7B/3B/1.5B and Llama-3.2-1B;
- `3.2`（model-suffix）：Llama-3.2-1B$^\dagger$ & 0.417 & 0.298 & 0.362 & --- & --- & --- \\
- `3.2`（model-suffix）：more reliable. $^\dagger$Llama-3.2-1B: 259/300 items (collection
- `3.2`（model-suffix）：Llama-3.1-8B, Llama-3.2-1B, Mistral-7B, Gemma2-9B, and Phi3.5; Phi3.5
- `3.2`（model-suffix）：Llama-3.2-1B & 558 & 0.507 & 0.267 & 0.680 & $4.1\times$ \\
- `5.2`（model-suffix）：(DeepSeek-V4-Flash-0731, GLM-5.2, Kimi-K3, MiniMax-M3;
- `5.2`（model-suffix）：GLM-5.2 (Zhipu) & 0.750 & 0.139 & 0.882 & $9.6\times$ & 0.67 \\
- `3.2`（model-suffix）：(Qwen2.5-1.5B $+0.30$, Llama-3.2-1B), the consistency gate is not
- `3.2`（model-suffix）：Llama-3.2-1B & 0.19 & $+0.05$ & 0.80 & \textbf{0.17} \\
- `3.2`（model-suffix）：(judge-soft ECE is reported instead); Llama-3.2-1B covers 259/300 items