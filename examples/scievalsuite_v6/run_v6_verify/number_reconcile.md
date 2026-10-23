# 数字对账报告（R3）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`，证据目录：`F:\deepseek\papers\scievalsuite\results`, `F:\deepseek\scievalsuite\out_p5`
- 结论：**MAJOR**（裁决 critical 0，待复核 8，机械噪音 3，已裁决 66）
- 无证据目录：否

## 方向 A：产物统计数字 → 论文出现（论文未改数字）

- 核心统计数字 752 个，其中 433 个在论文中找到一致值（命中率 0.5758）

| json_path | 值 | 论文 token | 来源 |
|---|---|---|---|
| `alpha` | 0.05 | `0.05` | `power_analysis.json` |
| `alpha_interim` | 1.0 | `1.00` | `JUDGE_40_REPORT.json` |
| `cross_model.friedman.chi2` | 2.0 | `2.00` | `p3_stats.json` |
| `friedman_curated.chi2` | 6.0 | `6.0` | `P5_FINAL_FRONTIER_CURATED.json` |
| `friedman_full_P3.chi2` | 2.0 | `2.00` | `P5_FINAL_FRONTIER_CURATED.json` |
| `friedman_full_P3_k3_N16.chi2` | 2.0 | `2.00` | `P5_MUSE_FINAL.json` |
| `friedman_L1a_6tasks_k4.chi2` | 14.25 | `14.25` | `P5_MUSE_FINAL.json` |
| `l2_arm_stats.gemma2_9b.mcnemar_p` | 1.0 | `1.00` | `p3_stats.json` |
| `l2_arm_stats.qwen2.5_14b.mcnemar_p` | 1.0 | `1.00` | `p3_stats.json` |
| `l2_arm_stats.qwen2.5_7b.mcnemar_p` | 1.0 | `1.00` | `p3_stats.json` |
| `L2_arms.gemma2_9b.mcnemar_discordant_F_A[0]` | 0.0 | `0.00` | `p3_effects.json` |
| `L2_arms.gemma2_9b.mcnemar_discordant_F_A[1]` | 0.0 | `0.00` | `p3_effects.json` |
| `L2_arms.qwen2.5_14b.mcnemar_discordant_F_A[0]` | 0.0 | `0.00` | `p3_effects.json` |
| `L2_arms.qwen2.5_14b.mcnemar_discordant_F_A[1]` | 0.0 | `0.00` | `p3_effects.json` |
| `L2_arms.qwen2.5_7b.mcnemar_discordant_F_A[0]` | 0.0 | `0.00` | `p3_effects.json` |
| `L2_arms.qwen2.5_7b.mcnemar_discordant_F_A[1]` | 0.0 | `0.00` | `p3_effects.json` |
| `arms.A.goal_rate` | 0.1418 | `0.1418` | `FARM_ABLATION.json` |
| `arms.F-guards.goal_rate` | 0.1418 | `0.1418` | `FARM_ABLATION.json` |
| `arms.F-nudges.goal_rate` | 0.1418 | `0.1418` | `FARM_ABLATION.json` |
| `arms.F.goal_rate` | 0.1418 | `0.1418` | `FARM_ABLATION.json` |
| `cross_model.friedman.mean_ranks[0]` | 2.0625 | `2.0625` | `p3_stats.json` |
| `cross_model.friedman.mean_ranks[1]` | 2.0625 | `2.0625` | `p3_stats.json` |
| `cross_model.friedman.mean_ranks[2]` | 1.875 | `1.8750` | `p3_stats.json` |
| `cross_model_gradient.qwen2.5:14b→gemma2:9b.A_goal_diff` | 0.0832 | `0.0832` | `p3_effects.json` |
| `cross_model_gradient.qwen2.5:7b→gemma2:9b.A_goal_diff` | 0.1332 | `0.1332` | `p3_effects.json` |
| `cross_model_gradient.qwen2.5:7b→qwen2.5:14b.A_goal_diff` | 0.05 | `0.05` | `p3_effects.json` |
| `friedman_curated.N` | 6.0 | `6.0` | `P5_FINAL_FRONTIER_CURATED.json` |
| `friedman_curated.p` | 0.04978706836786395 | `0.05` | `P5_FINAL_FRONTIER_CURATED.json` |
| `friedman_L1a_6tasks_k4.mean_ranks[0]` | 3.3333333333333335 | `3.3333` | `P5_MUSE_FINAL.json` |
| `friedman_L1a_6tasks_k4.mean_ranks[1]` | 2.8333333333333335 | `2.8333` | `P5_MUSE_FINAL.json` |
| `friedman_L1a_6tasks_k4.mean_ranks[2]` | 2.8333333333333335 | `2.8333` | `P5_MUSE_FINAL.json` |
| `friedman_L1a_6tasks_k4.mean_ranks[3]` | 1.0 | `1.00` | `P5_MUSE_FINAL.json` |
| `L1a.qwen2.5_7b.mean_z` | 0.0 | `0.00` | `p3_stats_normalized.json` |
| `l2_arm_stats.gemma2_9b.mean_goal_A` | 0.275 | `0.2750` | `p3_stats.json` |
| `l2_arm_stats.gemma2_9b.mean_goal_F` | 0.275 | `0.2750` | `p3_stats.json` |
| `l2_arm_stats.gemma2_9b.wilcoxon_goalF_minus_A.cles` | 0.5 | `0.5` | `p3_stats.json` |
| `l2_arm_stats.gemma2_9b.wilcoxon_goalF_minus_A.p` | 1.0 | `1.00` | `p3_stats.json` |
| `l2_arm_stats.qwen2.5_14b.mean_goal_A` | 0.1918 | `0.1918` | `p3_stats.json` |
| `l2_arm_stats.qwen2.5_14b.mean_goal_F` | 0.1918 | `0.1918` | `p3_stats.json` |
| `l2_arm_stats.qwen2.5_14b.wilcoxon_goalF_minus_A.cles` | 0.5 | `0.5` | `p3_stats.json` |

## 方向 B：论文小数 → 产物支撑

- 论文小数 209 个，有支撑 132 个（支撑率 0.6316）
- 机械噪音 3 个（版本号片段/日期/结构行，自动豁免）
- 已裁决 66 个（人工 verdict：noise/supported/critical）

### 人工复核清单（未裁决且非噪音）

- L20 `0.37`：We present SciEvalSuite, a unified evaluation suite for scientific agents that jointly covers three 
- L85 `12.1`：\paragraph{Models.} Evaluated: qwen2.5:7b, qwen2.5:14b, gemma2:9b (SUTs); judge: llama3.1:8b. Refere
- L89 `0.46`：\paragraph{Power.} Sample size is fixed by benchmark design, so we report achieved power / minimum d
- L129 `0.3553`：Table~\ref{tab:l1a} reports official metrics. Failures are counted as zero and remain in the denomin
- L152 `0.3553`：qwen2.5:7b scored 0/6 (all exec-fail across 3 trials, stable). qwen2.5:14b scored 2/6 (TextClassific
- L158 `0.37`：Friedman over 16 paired tasks (L1a+L1b, lower-is-better after sign-flipping accuracy/correlation whe
- L171 `0.37`：\textbf{(Q2) Larger N:} L2 N=8 (vs 4) and curated L1a N=6 k=4 (Model-F 6/6) give \textbf{p=0.003 exp
- L229 `0.37`：Fail MAE as worst is post-hoc. Sensitivity on curated 6-task Friedman via the canonical \texttt{out\

### 已裁决明细

| token | verdict | note |
|---|---|---|
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `0.355` | supported | TextSimilarity ITT 均值可复算：(0+0.533048+0.533048)/3=0.3554≈0.355（t1 exec-fail 计 0） |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `3.1` | noise | 模型版本 llama3.1:8b 中的 3.1，非实质断言 |
| `2.4` | noise | 表格列宽 p{...cm} |
| `2.8` | noise | 表格列宽 p{...cm} |
| `2.4` | noise | 表格列宽 p{...cm} |
| `4.2` | noise | 表格列宽 p{...cm} |
| `0.007` | noise | 成本 $0.007 per task，非实质断言 |
| `3.1` | noise | 模型版本 llama3.1:8b 中的 3.1，非实质断言 |
| `3.11` | noise | ARS v3.11 版本号，非实质断言 |
| `0.10` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\judge_robustness_report.json:per_perturb.numeric.FP |
| `0.28` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_gemma2_9b.json:summary.arms.A.goal_rate=0.275→0. |
| `3.1` | noise | 模型版本 llama3.1:8b 中的 3.1，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `3.1` | noise | 模型版本 llama3.1:8b 中的 3.1，非实质断言 |
| `1.87` | noise | 成本 ¥1.87/h，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `3.12` | noise | Python 3.12 版本号，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `3.12` | noise | Python 3.12 版本号，非实质断言 |
| `3.12` | noise | Python 3.12 版本号，非实质断言 |
| `3.12` | noise | Python 3.12 版本号，非实质断言 |
| `0.98` | noise | 插图宽度 width=...\linewidth |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `0.42` | supported | CI 下界幅值：p3_effects.json 7b→gemma ci95_approx[0]=-0.4221（符号翻转匹配） |
| `0.69` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\p3_effects.json:cross_model_gradient.qwen2.5:7b→gem |
| `0.355` | supported | TextSimilarity ITT 均值可复算：(0+0.533048+0.533048)/3=0.3554≈0.355（t1 exec-fail 计 0） |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `0.355` | supported | TextSimilarity ITT 均值可复算：(0+0.533048+0.533048)/3=0.3554≈0.355（t1 exec-fail 计 0） |
| `2.3333` | supported | 均值差：P5_MUSE_FINAL.json mean_ranks 3.3333-1.0=2.3333（muse vs 7b） |
| `3.1` | noise | 模型版本 llama3.1:8b 中的 3.1，非实质断言 |
| `3.11` | noise | ARS v3.11 版本号，非实质断言 |
| `0.10` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\judge_robustness_report.json:per_perturb.numeric.FP |
| `0.28` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_gemma2_9b.json:summary.arms.A.goal_rate=0.275→0. |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `1.87` | noise | 成本 ¥1.87/h，非实质断言 |
| `0.64` | noise | 成本 ~$0.64 total，非实质断言 |
| `1.87` | noise | 成本 ¥1.87/h，非实质断言 |
| `0.007` | noise | 成本 $0.007 per task，非实质断言 |
| `0.04` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\judge_robustness_report.json:overall.FNR=0.04273504 |
| `3.12` | noise | Python 3.12 版本号，非实质断言 |
| `0.28` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_gemma2_9b.json:summary.arms.A.goal_rate=0.275→0. |
| `0.10` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\judge_robustness_report.json:per_perturb.numeric.FP |
| `0.14` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_deepseek-v4-flash.json:rows[2].repeat_rate=0.143 |
| `0.27` | supported | L2 goal 0.275 舍入：L2_gemma2_9b.json goal_rate=0.275 |
| `0.87` | supported | 跨层 Spearman ρ=0.87：out_p5/CROSS_LAYER_ANALYSIS.md 原文 |
| `0.2400` | supported | invalid rate 上界：L2_qwen2.5_14b.json invalid_rate=0.237→0.24（2 位舍入） |
| `0.28` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_gemma2_9b.json:summary.arms.A.goal_rate=0.275→0. |
| `0.10` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\judge_robustness_report.json:per_perturb.numeric.FP |

### 机械噪音（自动豁免）

- `0.32`（version-fragment）：Per-seed rows were sealed with SHA-256; the P3-stage manifest sealed 125 underlying files (per-seed 
- `0.32`（version-fragment）：\paragraph{Models.} Evaluated: qwen2.5:7b, qwen2.5:14b, gemma2:9b (SUTs); judge: llama3.1:8b. Refere
- `0.32`（version-fragment）：\paragraph{Models.} Evaluated: qwen2.5:7b, qwen2.5:14b, gemma2:9b (SUTs); judge: llama3.1:8b. Refere