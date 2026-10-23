# 表格数字核验报告（R2d）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`，证据目录：`F:\deepseek\papers\calibration-self-improvement\evidence`
- 结论：**MAJOR**（表 17 个，numeric cell 228 个，无支撑 12，\input 缺失 0，混精度列 4）

## 表清单

| 表（行号） | tabular | caption 小数（支撑） | cell 数 |
|---|---|---|---|
| L476 | 是 | - | 12 |
| L525 | 是 | - | 9 |
| L635 | 是 | 0.0297(evid), 0.0169(evid), 0.0328(evid), 0.028(evid) | 8 |
| L702 | 是 | - | 3 |
| L825 | 是 | - | 15 |
| L904 | 是 | - | 6 |
| L961 | 是 | - | 29 |
| L1064 | 是 | - | 0 |
| L1087 | 是 | - | 33 |
| L1109 | 是 | - | 6 |
| L1196 | 是 | - | 20 |
| L1249 | 是 | - | 45 |
| L1308 | 是 | - | 20 |
| L1380 | 是 | - | 14 |
| L1488 | 是 | - | 0 |
| L1773 | 是 | 0.0668(evid), 0.0733(evid), 0.1267(evid), 0.1816(evid), 0.1928(evid) | 8 |
| L1789 | 是 | - | 0 |

## 表格数字人工复核清单（无任何支撑）

- L476 [cell] `36.7`：[High-conf (  0.8 ) error rate × Exact-string / 63.3   (19/30)] = 36.7
- L476 [cell] `13.3`：[High-conf (  0.8 ) error rate × Tolerant (v1) / 86.7   (26/30)] = 13.3
- L961 [cell] `0.241`：[DeepSeek-R1-7B × ECE (10-bin)] = 0.241
- L1087 [cell] `0.241`：[DeepSeek-R1-7B × ECE raw] = 0.241
- L1249 [cell] `3.1`：[Qwen2.5-3B × domain ECE spread] = 3.1
- L1249 [cell] `2.6`：[Phi3.5 ^ × domain ECE spread] = 2.6
- L1249 [cell] `10.3`：[Qwen2.5-1.5B × domain ECE spread] = 10.3
- L1308 [cell] `9.6`：[GLM-5.2 (Zhipu) × domain ECE spread] = 9.6
- L1308 [cell] `6.3`：[MiniMax-M3 (MiniMax) × domain ECE spread] = 6.3
- L1380 [cell] `-0.18`：[Qwen2.5-3B × (conf, cons)] = -0.18
- L1380 [cell] `0.86`：[Qwen2.5-1.5B × cons-gate hi-conf] = 0.86
- L1773 [cell] `83.3`：[B: per-generation cal. × Acc] = 83.3

## 列内混精度（INFO）

- L476 列「Exact-string / 63.3   (19/30)」：小数位 [1, 3, 4]——同列小数位数差 ≥2（疑似百分数/小数混用或复制错误）
- L476 列「Tolerant (v1) / 86.7   (26/30)」：小数位 [1, 4]——同列小数位数差 ≥2（疑似百分数/小数混用或复制错误）
- L635 列「Self-report」：小数位 [1, 4]——同列小数位数差 ≥2（疑似百分数/小数混用或复制错误）
- L635 列「Temperature scaling ( T=6.71 )」：小数位 [1, 4]——同列小数位数差 ≥2（疑似百分数/小数混用或复制错误）