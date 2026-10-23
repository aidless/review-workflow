# 表格数字核验报告（R2d）

- 论文：`F:\Research\F1_Single_10page\paper\main.tex`，证据目录：`F:\Research\_inbox\F1-F5_F45_2026-08-26\supplementary`
- 结论：**MAJOR**（表 4 个，numeric cell 34 个，无支撑 10，\input 缺失 0，混精度列 0）

## 表清单

| 表（行号） | tabular | caption 小数（支撑） | cell 数 |
|---|---|---|---|
| L52 | 是 | - | 1 |
| L104 | 是 | 0.017(evid) | 6 |
| L125 | 是 | 0.017(evid), 0.42(body), 0.35(evid), 0.37(evid), 0.34(evid), 0.38(evid) | 0 |
| L209 | 是 | - | 27 |

## 表格数字人工复核清单（无任何支撑）

- L104 [cell] `0.60`：[Qwen2.5:14B × CLES] = 0.60
- L104 [cell] `0.44`：[Qwen3:4b × CLES] = 0.44
- L209 [cell] `0.15`：[Qwen3:4b × d_z] = 0.15
- L209 [cell] `0.44`：[Qwen3:4b × CLES] = 0.44
- L209 [cell] `0.54`：[Gemma3:4b × CLES] = 0.54
- L209 [cell] `0.22`：[DeepSeek-R1:7B × d_z] = 0.22
- L209 [cell] `0.58`：[DeepSeek-R1:7B × CLES] = 0.58
- L209 [cell] `0.09`：[DeepSeek-R1:7B × d_z] = 0.09
- L209 [cell] `0.22`：[DeepSeek-R1:7B × p] = 0.22
- L209 [cell] `0.60`：[Qwen2.5:14B × CLES] = 0.60