# 数字对账报告（R3）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`，证据目录：`F:\deepseek\papers\scievalsuite\results`, `F:\deepseek\scievalsuite\out_p5`
- 结论：**PASS**（裁决 critical 0，待复核 0，机械噪音 5，已裁决 99）
- 无证据目录：否

## 方向 A：产物统计数字 → 论文出现（论文未改数字）

- 核心统计数字 752 个，其中 409 个在论文中找到一致值（命中率 0.5439）

| json_path | 值 | 论文 token | 来源 |
|---|---|---|---|
| `alpha` | 0.05 | `0.05` | `power_analysis.json` |
| `alpha_interim` | 1.0 | `1.0000` | `JUDGE_40_REPORT.json` |
| `cross_model.friedman.chi2` | 2.0 | `2.0` | `p3_stats.json` |
| `friedman_curated.chi2` | 6.0 | `6.0` | `P5_FINAL_FRONTIER_CURATED.json` |
| `friedman_full_P3.chi2` | 2.0 | `2.0` | `P5_FINAL_FRONTIER_CURATED.json` |
| `friedman_full_P3_k3_N16.chi2` | 2.0 | `2.0` | `P5_MUSE_FINAL.json` |
| `friedman_L1a_6tasks_k4.chi2` | 14.25 | `14.25` | `P5_MUSE_FINAL.json` |
| `l2_arm_stats.gemma2_9b.mcnemar_p` | 1.0 | `1.0000` | `p3_stats.json` |
| `l2_arm_stats.qwen2.5_14b.mcnemar_p` | 1.0 | `1.0000` | `p3_stats.json` |
| `l2_arm_stats.qwen2.5_7b.mcnemar_p` | 1.0 | `1.0000` | `p3_stats.json` |
| `L2_arms.gemma2_9b.mcnemar_discordant_F_A[0]` | 0.0 | `0.00` | `p3_effects.json` |
| `L2_arms.gemma2_9b.mcnemar_discordant_F_A[1]` | 0.0 | `0.00` | `p3_effects.json` |
| `L2_arms.qwen2.5_14b.mcnemar_discordant_F_A[0]` | 0.0 | `0.00` | `p3_effects.json` |
| `L2_arms.qwen2.5_14b.mcnemar_discordant_F_A[1]` | 0.0 | `0.00` | `p3_effects.json` |
| `L2_arms.qwen2.5_7b.mcnemar_discordant_F_A[0]` | 0.0 | `0.00` | `p3_effects.json` |
| `L2_arms.qwen2.5_7b.mcnemar_discordant_F_A[1]` | 0.0 | `0.00` | `p3_effects.json` |
| `cross_model.friedman.mean_ranks[0]` | 2.0625 | `2.0625` | `p3_stats.json` |
| `cross_model.friedman.mean_ranks[1]` | 2.0625 | `2.0625` | `p3_stats.json` |
| `cross_model.friedman.mean_ranks[2]` | 1.875 | `1.8750` | `p3_stats.json` |
| `cross_model_gradient.qwen2.5:7b→qwen2.5:14b.A_goal_diff` | 0.05 | `0.05` | `p3_effects.json` |
| `friedman_curated.N` | 6.0 | `6.0` | `P5_FINAL_FRONTIER_CURATED.json` |
| `friedman_curated.p` | 0.04978706836786395 | `0.05` | `P5_FINAL_FRONTIER_CURATED.json` |
| `friedman_L1a_6tasks_k4.mean_ranks[0]` | 3.3333333333333335 | `3.3333` | `P5_MUSE_FINAL.json` |
| `friedman_L1a_6tasks_k4.mean_ranks[1]` | 2.8333333333333335 | `2.8333` | `P5_MUSE_FINAL.json` |
| `friedman_L1a_6tasks_k4.mean_ranks[2]` | 2.8333333333333335 | `2.8333` | `P5_MUSE_FINAL.json` |
| `friedman_L1a_6tasks_k4.mean_ranks[3]` | 1.0 | `1.0000` | `P5_MUSE_FINAL.json` |
| `L1a.qwen2.5_7b.mean_z` | 0.0 | `0.00` | `p3_stats_normalized.json` |
| `l2_arm_stats.gemma2_9b.wilcoxon_goalF_minus_A.cles` | 0.5 | `0.5` | `p3_stats.json` |
| `l2_arm_stats.gemma2_9b.wilcoxon_goalF_minus_A.p` | 1.0 | `1.0000` | `p3_stats.json` |
| `l2_arm_stats.qwen2.5_14b.wilcoxon_goalF_minus_A.cles` | 0.5 | `0.5` | `p3_stats.json` |
| `l2_arm_stats.qwen2.5_14b.wilcoxon_goalF_minus_A.p` | 1.0 | `1.0000` | `p3_stats.json` |
| `l2_arm_stats.qwen2.5_7b.wilcoxon_goalF_minus_A.cles` | 0.5 | `0.5` | `p3_stats.json` |
| `l2_arm_stats.qwen2.5_7b.wilcoxon_goalF_minus_A.p` | 1.0 | `1.0000` | `p3_stats.json` |
| `L2_arms.gemma2_9b.mean_diff_F_minus_A` | 0.0 | `0.00` | `p3_effects.json` |
| `L2_arms.qwen2.5_14b.mean_diff_F_minus_A` | 0.0 | `0.00` | `p3_effects.json` |
| `L2_arms.qwen2.5_7b.mean_diff_F_minus_A` | 0.0 | `0.00` | `p3_effects.json` |
| `models.gemma2:9b.mean_diff` | 0.0 | `0.00` | `p3_bootstrap.json` |
| `models.qwen2.5:14b.mean_diff` | 0.0 | `0.00` | `p3_bootstrap.json` |
| `models.qwen2.5:7b.mean_diff` | 0.0 | `0.00` | `p3_bootstrap.json` |
| `rows[0].exact_rate` | 0.0 | `0.00` | `L2_deepseek-v4-flash.json` |

## 方向 B：论文小数 → 产物支撑

- 论文小数 219 个，有支撑 115 个（支撑率 0.5251）
- 机械噪音 5 个（版本号片段/日期/结构行，自动豁免）
- 已裁决 99 个（人工 verdict：noise/supported/critical）

### 人工复核清单（未裁决且非噪音）

- 无（全部已支撑 / 已豁免 / 已裁决）

### 已裁决明细

| token | verdict | note |
|---|---|---|
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `0.14` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_deepseek-v4-flash.json:rows[2].repeat_rate=0.143 |
| `0.19` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\p3_effects.json:L2_arms.qwen2.5_14b.A_goal_mean=0.1 |
| `0.28` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_gemma2_9b.json:summary.arms.A.goal_rate=0.275→0. |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `3.1` | noise | 模型版本 llama3.1:8b 中的 3.1，非实质断言 |
| `2.4` | noise | 表格列宽 p{...cm} |
| `2.8` | noise | 表格列宽 p{...cm} |
| `2.4` | noise | 表格列宽 p{...cm} |
| `4.2` | noise | 表格列宽 p{...cm} |
| `0.007` | noise | 成本 $0.007 per task，非实质断言 |
| `3.1` | noise | 模型版本 llama3.1:8b 中的 3.1，非实质断言 |
| `0.10` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\judge_robustness_report.json:per_perturb.numeric.FP |
| `0.28` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_gemma2_9b.json:summary.arms.A.goal_rate=0.275→0. |
| `3.1` | noise | 模型版本 llama3.1:8b 中的 3.1，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `3.1` | noise | 模型版本 llama3.1:8b 中的 3.1，非实质断言 |
| `1.87` | noise | 成本 ¥1.87/h，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `3.1` | noise | 模型版本 llama3.1:8b 中的 3.1，非实质断言 |
| `1.2` | noise | 模型版本 muse-spark-1.2-contributor，非实质断言 |
| `3.12` | noise | Python 3.12 版本号，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `12.1` | noise | CUDA runtime 12.1（torch 2.5.1+cu121），技术版本描述，非实质断言 |
| `3.12` | noise | Python 3.12 版本号，非实质断言 |
| `0.46` | supported | 机械复算 paired t N=16 d=0.5 power=0.4648（scipy nct.sf）→0.46 |
| `3.12` | noise | Python 3.12 版本号，非实质断言 |
| `3.12` | noise | Python 3.12 版本号，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `0.3553` | supported | ITT 均值可复算：(0+0.5330+0.5330)/3=0.35537≈0.3553（t1 exec-fail 计 0） |
| `0.355` | supported | TextSimilarity ITT 均值可复算：(0+0.533048+0.533048)/3=0.3554≈0.355（t1 exec-fail 计 0） |
| `0.98` | noise | 插图宽度 width=...\linewidth |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `0.14` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_deepseek-v4-flash.json:rows[2].repeat_rate=0.143 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `0.14` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_deepseek-v4-flash.json:rows[2].repeat_rate=0.143 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `0.19` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\p3_effects.json:L2_arms.qwen2.5_14b.A_goal_mean=0.1 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `0.19` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\p3_effects.json:L2_arms.qwen2.5_14b.A_goal_mean=0.1 |
| `0.28` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_gemma2_9b.json:summary.arms.A.goal_rate=0.275→0. |
| `0.28` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_gemma2_9b.json:summary.arms.A.goal_rate=0.275→0. |
| `0.14` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_deepseek-v4-flash.json:rows[2].repeat_rate=0.143 |
| `0.19` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\p3_effects.json:L2_arms.qwen2.5_14b.A_goal_mean=0.1 |
| `0.28` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_gemma2_9b.json:summary.arms.A.goal_rate=0.275→0. |
| `0.08` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\p3_effects.json:cross_model_gradient.qwen2.5:14b→ge |
| `0.13` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\p3_effects.json:cross_model_gradient.qwen2.5:7b→gem |
| `0.42` | supported | CI 下界幅值：p3_effects.json 7b→gemma ci95_approx[0]=-0.4221（符号翻转匹配） |
| `0.69` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\p3_effects.json:cross_model_gradient.qwen2.5:7b→gem |
| `0.14` | supported | 证据 2 位舍入 F:\deepseek\papers\scievalsuite\results\L2_deepseek-v4-flash.json:rows[2].repeat_rate=0.143 |
| `0.3553` | supported | ITT 均值可复算：(0+0.5330+0.5330)/3=0.35537≈0.3553（t1 exec-fail 计 0） |
| `0.355` | supported | TextSimilarity ITT 均值可复算：(0+0.533048+0.533048)/3=0.3554≈0.355（t1 exec-fail 计 0） |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |
| `2.5` | noise | 时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言 |

### 机械噪音（自动豁免）

- `0.32`（version-fragment）：Per-seed rows were sealed with SHA-256; the P3-stage manifest sealed 125 underlying files (per-seed 
- `0.32`（version-fragment）：\paragraph{Models.} Evaluated: qwen2.5:7b, qwen2.5:14b, gemma2:9b (SUTs); judge: llama3.1:8b. Refere
- `0.32`（version-fragment）：\paragraph{Models.} Evaluated: qwen2.5:7b, qwen2.5:14b, gemma2:9b (SUTs); judge: llama3.1:8b. Refere
- `0.32`（version-fragment）：\paragraph{Models.} Evaluated: qwen2.5:7b, qwen2.5:14b, gemma2:9b (SUTs); judge: llama3.1:8b. Refere
- `0.32`（version-fragment）：\paragraph{Dataset licenses.} All three derived datasets are redistributable under permissive licens