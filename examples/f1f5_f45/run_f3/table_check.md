# 表格数字核验报告（R2d）

- 论文：`F:\Research\F3_Single_10page\paper\main.tex`，证据目录：`F:\Research\_inbox\F1-F5_F45_2026-08-26\supplementary`
- 结论：**MAJOR**（表 5 个，numeric cell 32 个，无支撑 10，\input 缺失 0，混精度列 0）

## 表清单

| 表（行号） | tabular | caption 小数（支撑） | cell 数 |
|---|---|---|---|
| L76 | 是 | - | 0 |
| L162 | 是 | 0.008(evid), 0.42(body) | 3 |
| L182 | 是 | - | 7 |
| L201 | 是 | - | 1 |
| L245 | 是 | 0.1(evid), 0.1(evid) | 21 |

## 表格数字人工复核清单（无任何支撑）

- L182 [cell] `-0.0064`：[Append-only × MAE] = -0.0064
- L182 [cell] `0.503`：[RAG TF-IDF   {=}0.1 × p  (exact)] = 0.503
- L245 [cell] `45`：[ × Filtered] = 45
- L245 [cell] `1.5`：[ × ] = 1.5
- L245 [cell] `62`：[ × Filtered] = 62
- L245 [cell] `0.15`：[ × {lcccc}] = 0.15
- L245 [cell] `78`：[ × Filtered] = 78
- L245 [cell] `0.20`：[ × {lcccc}] = 0.20
- L245 [cell] `85`：[ × Filtered] = 85
- L245 [cell] `91`：[ × Filtered] = 91