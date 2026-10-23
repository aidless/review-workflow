# 表格数字核验报告（R2d）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`，证据目录：`F:\deepseek\papers\calibration-self-improvement\evidence`
- 结论：**MAJOR**（表 17 个，numeric cell 225 个，无支撑 20，\input 缺失 0，混精度列 4）

## 表清单

| 表（行号） | tabular | caption 小数（支撑） | cell 数 |
|---|---|---|---|
| L469 | 是 | 36.7(unsu), 13.3(unsu) | 12 |
| L518 | 是 | - | 9 |
| L628 | 是 | 0.0297(evid), 0.0169(evid), 0.0328(evid), 0.028(evid) | 8 |
| L695 | 是 | - | 3 |
| L818 | 是 | - | 15 |
| L897 | 是 | - | 6 |
| L954 | 是 | 0.241(unsu) | 29 |
| L1057 | 是 | - | 0 |
| L1080 | 是 | - | 33 |
| L1102 | 是 | - | 6 |
| L1189 | 是 | - | 20 |
| L1242 | 是 | 3.1(unsu), 2.6(unsu), 10.3(unsu), 9.6(unsu), 6.3(unsu) | 42 |
| L1301 | 是 | - | 20 |
| L1373 | 是 | - | 14 |
| L1506 | 是 | - | 0 |
| L1791 | 是 | 0.0668(evid), 0.0733(evid), 0.1267(evid), 0.1816(evid), 0.1928(evid) | 8 |
| L1807 | 是 | - | 0 |

## 表格数字人工复核清单（无任何支撑）

- L469 [caption] `36.7`：Calibration of self-reported confidence under three label-judgment regimes (N=30 pilot; sa
- L469 [caption] `13.3`：Calibration of self-reported confidence under three label-judgment regimes (N=30 pilot; sa
- L469 [cell] `36.7`：[High-conf (  0.8 ) error rate × Exact-string / 63.3   (19/30)] = 36.7
- L469 [cell] `13.3`：[High-conf (  0.8 ) error rate × Tolerant (v1) / 86.7   (26/30)] = 13.3
- L954 [caption] `0.241`：Semantic soft-label estimator vs.\ matcher-labeled binning ECE on real cross-model data (N
- L954 [cell] `0.241`：[DeepSeek-R1-7B × ECE (10-bin)] = 0.241
- L1080 [cell] `0.241`：[DeepSeek-R1-7B × ECE raw] = 0.241
- L1080 [cell] `0.275`：[DeepSeek-R1-7B × Brier raw] = 0.275
- L1242 [caption] `3.1`：Significance expansion: 600 MMLU items, six domains, nine models across five families (tol
- L1242 [caption] `2.6`：Significance expansion: 600 MMLU items, six domains, nine models across five families (tol
- L1242 [caption] `10.3`：Significance expansion: 600 MMLU items, six domains, nine models across five families (tol
- L1242 [caption] `9.6`：Significance expansion: 600 MMLU items, six domains, nine models across five families (tol
- L1242 [caption] `6.3`：Significance expansion: 600 MMLU items, six domains, nine models across five families (tol
- L1242 [cell] `3.1`：[Qwen2.5-3B × domain ECE spread] = 3.1
- L1242 [cell] `2.6`：[Phi3.5 ^ × domain ECE spread] = 2.6
- L1242 [cell] `10.3`：[Qwen2.5-1.5B × domain ECE spread] = 10.3
- L1301 [cell] `9.6`：[GLM-5.2 (Zhipu) × domain ECE spread] = 9.6
- L1301 [cell] `6.3`：[MiniMax-M3 (MiniMax) × domain ECE spread] = 6.3
- L1373 [cell] `-0.18`：[Qwen2.5-3B × (conf, cons)] = -0.18
- L1791 [cell] `83.3`：[B: per-generation cal. × Acc] = 83.3

## 列内混精度（INFO）

- L469 列「Exact-string / 63.3   (19/30)」：小数位 [1, 3, 4]——同列小数位数差 ≥2（疑似百分数/小数混用或复制错误）
- L469 列「Tolerant (v1) / 86.7   (26/30)」：小数位 [1, 4]——同列小数位数差 ≥2（疑似百分数/小数混用或复制错误）
- L628 列「Self-report」：小数位 [1, 4]——同列小数位数差 ≥2（疑似百分数/小数混用或复制错误）
- L628 列「Temperature scaling ( T=6.71 )」：小数位 [1, 4]——同列小数位数差 ≥2（疑似百分数/小数混用或复制错误）