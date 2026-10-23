# 数字对账报告（R3）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`，证据目录：`F:\deepseek\papers\scievalsuite\results`, `F:\deepseek\scievalsuite\out_p5`
- 结论：**MAJOR**（裁决 critical 0，待复核 62，机械噪音 10，已裁决 0）
- 无证据目录：否

## 方向 A：产物统计数字 → 论文出现（论文未改数字）

- 核心统计数字 752 个，其中 425 个在论文中找到一致值（命中率 0.5652）

| json_path | 值 | 论文 token | 来源 |
|---|---|---|---|
| `alpha` | 0.05 | `0.05` | `power_analysis.json` |
| `alpha_interim` | 1.0 | `1.0000` | `JUDGE_40_REPORT.json` |
| `cohens_kappa` | 0.8940217391304347 | `0.894` | `JUDGE_40_DOUBLE_REPORT.json` |
| `cross_model.friedman.chi2` | 2.0 | `2.0000` | `p3_stats.json` |
| `friedman_curated.chi2` | 6.0 | `6.0` | `P5_FINAL_FRONTIER_CURATED.json` |
| `friedman_full_P3.chi2` | 2.0 | `2.0000` | `P5_FINAL_FRONTIER_CURATED.json` |
| `friedman_full_P3_k3_N16.chi2` | 2.0 | `2.0000` | `P5_MUSE_FINAL.json` |
| `friedman_L1a_6tasks_k4.chi2` | 14.25 | `14.25` | `P5_MUSE_FINAL.json` |
| `krippendorff_alpha` | 0.8940217391304347 | `0.894` | `JUDGE_40_DOUBLE_REPORT.json` |
| `l2_arm_stats.gemma2_9b.mcnemar_p` | 1.0 | `1.0000` | `p3_stats.json` |
| `l2_arm_stats.qwen2.5_14b.mcnemar_p` | 1.0 | `1.0000` | `p3_stats.json` |
| `l2_arm_stats.qwen2.5_7b.mcnemar_p` | 1.0 | `1.0000` | `p3_stats.json` |
| `L2_arms.gemma2_9b.mcnemar_discordant_F_A[0]` | 0.0 | `0.0000` | `p3_effects.json` |
| `L2_arms.gemma2_9b.mcnemar_discordant_F_A[1]` | 0.0 | `0.0000` | `p3_effects.json` |
| `L2_arms.qwen2.5_14b.mcnemar_discordant_F_A[0]` | 0.0 | `0.0000` | `p3_effects.json` |
| `L2_arms.qwen2.5_14b.mcnemar_discordant_F_A[1]` | 0.0 | `0.0000` | `p3_effects.json` |
| `L2_arms.qwen2.5_7b.mcnemar_discordant_F_A[0]` | 0.0 | `0.0000` | `p3_effects.json` |
| `L2_arms.qwen2.5_7b.mcnemar_discordant_F_A[1]` | 0.0 | `0.0000` | `p3_effects.json` |
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
| `friedman_L1a_6tasks_k4.mean_ranks[3]` | 1.0 | `1.0000` | `P5_MUSE_FINAL.json` |
| `L1a.qwen2.5_7b.mean_z` | 0.0 | `0.0000` | `p3_stats_normalized.json` |
| `l2_arm_stats.gemma2_9b.mean_goal_A` | 0.275 | `0.2750` | `p3_stats.json` |
| `l2_arm_stats.gemma2_9b.mean_goal_F` | 0.275 | `0.2750` | `p3_stats.json` |
| `l2_arm_stats.gemma2_9b.wilcoxon_goalF_minus_A.cles` | 0.5 | `0.5` | `p3_stats.json` |
| `l2_arm_stats.gemma2_9b.wilcoxon_goalF_minus_A.p` | 1.0 | `1.0000` | `p3_stats.json` |
| `l2_arm_stats.qwen2.5_14b.mean_goal_A` | 0.1918 | `0.1918` | `p3_stats.json` |

## 方向 B：论文小数 → 产物支撑

- 论文小数 219 个，有支撑 147 个（支撑率 0.6712）
- 机械噪音 10 个（版本号片段/日期/结构行，自动豁免）
- 已裁决 0 个（人工 verdict：noise/supported/critical）

### 人工复核清单（未裁决且非噪音）

- L20 `2.5`：We present SciEvalSuite, a unified evaluation suite for scientific agents that jointly covers three 
- L20 `2.5`：We present SciEvalSuite, a unified evaluation suite for scientific agents that jointly covers three 
- L20 `0.355`：We present SciEvalSuite, a unified evaluation suite for scientific agents that jointly covers three 
- L20 `3.1`：We present SciEvalSuite, a unified evaluation suite for scientific agents that jointly covers three 
- L20 `0.28`：We present SciEvalSuite, a unified evaluation suite for scientific agents that jointly covers three 
- L20 `3.11`：We present SciEvalSuite, a unified evaluation suite for scientific agents that jointly covers three 
- L31 `2.5`：We instantiate the suite on three small-to-medium local models hosted on AutoDL (RTX3090 48GB, ollam
- L31 `2.5`：We instantiate the suite on three small-to-medium local models hosted on AutoDL (RTX3090 48GB, ollam
- L31 `3.1`：We instantiate the suite on three small-to-medium local models hosted on AutoDL (RTX3090 48GB, ollam
- L43 `2.4`：\begin{tabular}{p{2.4cm}p{2.8cm}p{2.4cm}p{4.2cm}}
- L43 `2.8`：\begin{tabular}{p{2.4cm}p{2.8cm}p{2.4cm}p{4.2cm}}
- L43 `2.4`：\begin{tabular}{p{2.4cm}p{2.8cm}p{2.4cm}p{4.2cm}}
- L43 `4.2`：\begin{tabular}{p{2.4cm}p{2.8cm}p{2.4cm}p{4.2cm}}
- L62 `0.007`：ResearchClawBench (RCB) is the closest to L1b, providing checklist-based report scoring, but it cove
- L79 `3.1`：L1b text-judge was llama3.1:8b (cloud). Before use it had to pass a calibration gate on a gold set o
- L79 `3.11`：L1b text-judge was llama3.1:8b (cloud). Before use it had to pass a calibration gate on a gold set o
- L79 `0.10`：L1b text-judge was llama3.1:8b (cloud). Before use it had to pass a calibration gate on a gold set o
- L79 `0.28`：L1b text-judge was llama3.1:8b (cloud). Before use it had to pass a calibration gate on a gold set o
- L85 `2.5`：\paragraph{Models.} Evaluated: qwen2.5:7b, qwen2.5:14b, gemma2:9b (SUTs); judge: llama3.1:8b. Refere
- L85 `2.5`：\paragraph{Models.} Evaluated: qwen2.5:7b, qwen2.5:14b, gemma2:9b (SUTs); judge: llama3.1:8b. Refere
- L85 `3.1`：\paragraph{Models.} Evaluated: qwen2.5:7b, qwen2.5:14b, gemma2:9b (SUTs); judge: llama3.1:8b. Refere
- L85 `1.87`：\paragraph{Models.} Evaluated: qwen2.5:7b, qwen2.5:14b, gemma2:9b (SUTs); judge: llama3.1:8b. Refere
- L85 `2.5`：\paragraph{Models.} Evaluated: qwen2.5:7b, qwen2.5:14b, gemma2:9b (SUTs); judge: llama3.1:8b. Refere
- L89 `0.4600`：\paragraph{Power.} Sample size is fixed by benchmark design, so we report achieved power / minimum d
- L91 `3.12`：\paragraph{Implementation.} \texttt{scievalsuite/p3\_run\_l\{1a,1b,2\}.py} launchers (provider flag:
- L91 `3.12`：\paragraph{Implementation.} \texttt{scievalsuite/p3\_run\_l\{1a,1b,2\}.py} launchers (provider flag:
- L99 `0.98`：\includegraphics[width=0.98\linewidth]{fig_overview.pdf}
- L115 `2.5`：qwen2.5:7b & A & 0.1418 & 0/4 & 0 & 0 & 1.0000 \\
- L116 `2.5`：qwen2.5:7b & F & 0.1418 & 0/4 & 0 & 0 & 1.0000 \\
- L126 `0.42`：All three models showed \emph{identical} paired outcomes: win\_F=0, loss\_F=0, ties=4, exact McNemar
- L126 `0.69`：All three models showed \emph{identical} paired outcomes: win\_F=0, loss\_F=0, ties=4, exact McNemar
- L129 `0.355`：Table~\ref{tab:l1a} reports official metrics. Failures are counted as zero and remain in the denomin
- L137 `2.5`：Task & qwen2.5:7b & qwen2.5:14b & gemma2:9b & muse-spark \\
- L137 `2.5`：Task & qwen2.5:7b & qwen2.5:14b & gemma2:9b & muse-spark \\
- L152 `2.5`：qwen2.5:7b scored 0/6 (all exec-fail across 3 trials, stable). qwen2.5:14b scored 2/6 (TextClassific
- L152 `2.5`：qwen2.5:7b scored 0/6 (all exec-fail across 3 trials, stable). qwen2.5:14b scored 2/6 (TextClassific
- L152 `0.355`：qwen2.5:7b scored 0/6 (all exec-fail across 3 trials, stable). qwen2.5:14b scored 2/6 (TextClassific
- L158 `2.3333`：Friedman over 16 paired tasks (L1a+L1b, lower-is-better after sign-flipping accuracy/correlation whe
- L161 `3.1`：The 21-item gold set (15 real workspace reports plus 6 synthetic boundary cases, 11 positive / 10 ne
- L161 `3.11`：The 21-item gold set (15 real workspace reports plus 6 synthetic boundary cases, 11 positive / 10 ne
- L161 `0.10`：The 21-item gold set (15 real workspace reports plus 6 synthetic boundary cases, 11 positive / 10 ne
- L161 `0.28`：The 21-item gold set (15 real workspace reports plus 6 synthetic boundary cases, 11 positive / 10 ne
- L164 `2.5`：Total calls 568 $<1000$ (L2 480 usage-logged, L1a 54 (18 initial + 36 extra trials), L1b gen 34, jud
- L164 `1.87`：Total calls 568 $<1000$ (L2 480 usage-logged, L1a 54 (18 initial + 36 extra trials), L1b gen 34, jud
- L164 `0.64`：Total calls 568 $<1000$ (L2 480 usage-logged, L1a 54 (18 initial + 36 extra trials), L1b gen 34, jud
- L164 `1.87`：Total calls 568 $<1000$ (L2 480 usage-logged, L1a 54 (18 initial + 36 extra trials), L1b gen 34, jud
- L164 `0.007`：Total calls 568 $<1000$ (L2 480 usage-logged, L1a 54 (18 initial + 36 extra trials), L1b gen 34, jud
- L164 `0.04`：Total calls 568 $<1000$ (L2 480 usage-logged, L1a 54 (18 initial + 36 extra trials), L1b gen 34, jud
- L171 `0.074`：\textbf{(Q2) Larger N:} L2 N=8 (vs 4) and curated L1a N=6 k=4 (muse 6/6) give \textbf{p=0.0026 explo
- L173 `0.28`：\textbf{(Q4) Judge:} Gold 21$\rightarrow$39 (30 real+9 synthetic+1 attack, 1 empty filtered) in \tex
- L175 `0.10`：\textbf{(Q5) F-arm Ablation:} 2$\times$2 (nudges$\times$guards) on 4 scenarios: all arms goal 0.1418
- L175 `0.14`：\textbf{(Q5) F-arm Ablation:} 2$\times$2 (nudges$\times$guards) on 4 scenarios: all arms goal 0.1418
- L175 `0.27`：\textbf{(Q5) F-arm Ablation:} 2$\times$2 (nudges$\times$guards) on 4 scenarios: all arms goal 0.1418
- L175 `0.87`：\textbf{(Q5) F-arm Ablation:} 2$\times$2 (nudges$\times$guards) on 4 scenarios: all arms goal 0.1418
- L182 `0.2400`：The central empirical pattern was a consistently not-detectable difference between arms: three indep
- L191 `0.28`：Sample sizes are small by construction ($N=4$ L2 scenarios, $N=16$ tasks for Friedman, trials=1 for 
- L191 `0.10`：Sample sizes are small by construction ($N=4$ L2 scenarios, $N=16$ tasks for Friedman, trials=1 for 
- L194 `0.007`：SciEvalSuite provides a unified, budget-controlled, independently recomputable harness that jointly 
- L221 `3.12`：Code, manifests and per-seed rows are sealed with SHA-256; all numbers recomputed from raw rows; env
- L224 `0.28`：46-entry, 46-hash G11 verification PASS (125 underlying files), \texttt{evidence\_manifest.json} at 
- L227 `5.2`：Fail MAE as worst is post-hoc. Sensitivity on curated 6-task k=3 Friedman: fail=-10 $\rightarrow$ ch
- L227 `0.074`：Fail MAE as worst is post-hoc. Sensitivity on curated 6-task k=3 Friedman: fail=-10 $\rightarrow$ ch

### 机械噪音（自动豁免）

- `0.32`（version-fragment）：We present SciEvalSuite, a unified evaluation suite for scientific agents that jointly covers three 
- `1.2`（model-suffix）：We present SciEvalSuite, a unified evaluation suite for scientific agents that jointly covers three 
- `0.32`（version-fragment）：We instantiate the suite on three small-to-medium local models hosted on AutoDL (RTX3090 48GB, ollam
- `0.32`（version-fragment）：\paragraph{Models.} Evaluated: qwen2.5:7b, qwen2.5:14b, gemma2:9b (SUTs); judge: llama3.1:8b. Refere
- `2.5`（date-adjacent）：qwen2.5:14b & A & 0.1918 & 1/4 & 0 & 0 & 1.0000 \\
- `2.5`（date-adjacent）：qwen2.5:14b & F & 0.1918 & 1/4 & 0 & 0 & 1.0000 \\
- `1.2`（model-suffix）：\caption{L1a AIRS-Bench (official metric; Acc/Spearman higher better, MAE lower better). $\dagger$0 
- `1.2`（model-suffix）：qwen2.5:7b scored 0/6 (all exec-fail across 3 trials, stable). qwen2.5:14b scored 2/6 (TextClassific
- `1.2`（model-suffix）：All three models scored 0/10 (no report passed the checklist; score stage fully SKIP). The 30 worksp
- `1.2`（model-suffix）：\textbf{(Q1) L1b/L2 Positive Control:} \texttt{muse-spark-1.2-contributor} (opencode, 4096 tokens) s