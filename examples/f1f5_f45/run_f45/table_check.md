# 表格数字核验报告（R2d）

- 论文：`F:\Research\MERGED_FLAGSHIPS\F45_Merged\paper\main.tex`，证据目录：`F:\Research\_inbox\F1-F5_F45_2026-08-26\supplementary`
- 结论：**MAJOR**（表 8 个，numeric cell 335 个，无支撑 116，\input 缺失 0，混精度列 0）

## 表清单

| 表（行号） | tabular | caption 小数（支撑） | cell 数 |
|---|---|---|---|
| L67 | 是 | - | 1 |
| L183 | 是 | 0.65(evid) | 10 |
| L234 | 是 | - | 24 |
| L323 | 是 | 0.65(evid) | 40 |
| L348 | 是 | - | 28 |
| L503 | 是 | 1.96(body) | 8 |
| L547 | 是 | - | 112 |
| L575 | 是 | - | 112 |

## 表格数字人工复核清单（无任何支撑）

- L67 [cell] `7,2`：[Ours (F4 primary + F5 secondary) × N,f  fixed / N{ }3f{+}1  bound / asymptotic / variable
- L234 [cell] `0.621`：[Qwen3:4b × Hybrid] = 0.621
- L234 [cell] `0.549`：[Gemma3:4b × Trust _mean] = 0.549
- L234 [cell] `0.434`：[Gemma3:4b × Majority] = 0.434
- L234 [cell] `0.434`：[DeepSeek-R1:7B × Majority] = 0.434
- L234 [cell] `0.619`：[DeepSeek-R1:7B × Hybrid] = 0.619
- L234 [cell] `0.731`：[Qwen3:4b × Majority] = 0.731
- L234 [cell] `0.829`：[DeepSeek-R1:7B × Trust _mean] = 0.829
- L323 [cell] `0.621`：[Qwen3:4b × Hybrid] = 0.621
- L323 [cell] `0.549`：[Gemma3:4b × Trust _mean] = 0.549
- L323 [cell] `0.434`：[Gemma3:4b × Majority] = 0.434
- L323 [cell] `0.434`：[Gemma3:4b × Median] = 0.434
- L323 [cell] `0.434`：[DeepSeek-R1:7B × Majority] = 0.434
- L323 [cell] `0.434`：[DeepSeek-R1:7B × Median] = 0.434
- L323 [cell] `0.619`：[DeepSeek-R1:7B × Hybrid] = 0.619
- L323 [cell] `0.731`：[Qwen3:4b × Majority] = 0.731
- L323 [cell] `0.731`：[Qwen3:4b × Median] = 0.731
- L323 [cell] `0.829`：[DeepSeek-R1:7B × Trust _mean] = 0.829
- L348 [cell] `1818`：[Trust vs.  Maj × b] = 1818
- L348 [cell] `456`：[Trust vs.  Maj × b] = 456
- L348 [cell] `458`：[Trust vs.  Maj × b] = 458
- L348 [cell] `455`：[Trust vs.  Maj × b] = 455
- L348 [cell] `449`：[Trust vs.  Maj × b] = 449
- L348 [cell] `1566`：[Trust vs.  Maj × b] = 1566
- L348 [cell] `397`：[Trust vs.  Maj × b] = 397
- L348 [cell] `394`：[Trust vs.  Maj × b] = 394
- L348 [cell] `387`：[Trust vs.  Maj × b] = 387
- L348 [cell] `388`：[Trust vs.  Maj × b] = 388
- L348 [cell] `2960`：[Hybrid vs.  Maj × b] = 2960
- L348 [cell] `928`：[Hybrid vs.  Maj × b] = 928
- L348 [cell] `4075`：[Trim vs.  Maj × b] = 4075
- L348 [cell] `397`：[Trim vs.  Maj × b] = 397
- L547 [cell] `7`：[ × N] = 7
- L547 [cell] `0.590`：[ × majority] = 0.590
- L547 [cell] `2209`：[ × b] = 2209
- L547 [cell] `9`：[ × N] = 9
- L547 [cell] `0.609`：[ × majority] = 0.609
- L547 [cell] `3222`：[ × b] = 3222
- L547 [cell] `9`：[ × N] = 9
- L547 [cell] `0.592`：[ × majority] = 0.592
- L547 [cell] `1923`：[ × b] = 1923
- L547 [cell] `13`：[ × N] = 13
- L547 [cell] `0.603`：[ × majority] = 0.603
- L547 [cell] `2748`：[ × b] = 2748
- L547 [cell] `7`：[ × N] = 7
- L547 [cell] `1566`：[ × b] = 1566
- L547 [cell] `9`：[ × N] = 9
- L547 [cell] `2213`：[ × b] = 2213
- L547 [cell] `9`：[ × N] = 9
- L547 [cell] `1424`：[ × b] = 1424
- L547 [cell] `13`：[ × N] = 13
- L547 [cell] `0.885`：[ × trust] = 0.885
- L547 [cell] `1899`：[ × b] = 1899
- L547 [cell] `7`：[ × N] = 7
- L547 [cell] `961`：[ × b] = 961
- L547 [cell] `9`：[ × N] = 9
- L547 [cell] `0.969`：[ × trust] = 0.969
- L547 [cell] `1085`：[ × b] = 1085
- L547 [cell] `9`：[ × N] = 9
- L547 [cell] `950`：[ × b] = 950
- L547 [cell] `13`：[ × N] = 13
- L547 [cell] `0.951`：[ × trust] = 0.951
- L547 [cell] `1163`：[ × b] = 1163
- L547 [cell] `7`：[ × N] = 7
- L547 [cell] `0.969`：[ × trust] = 0.969
- L547 [cell] `487`：[ × b] = 487
- L547 [cell] `9`：[ × N] = 9
- L547 [cell] `0.996`：[ × trust] = 0.996
- L547 [cell] `286`：[ × b] = 286
- L547 [cell] `9`：[ × N] = 9
- L547 [cell] `0.925`：[ × majority] = 0.925
- L547 [cell] `539`：[ × b] = 539
- L547 [cell] `13`：[ × N] = 13
- L547 [cell] `428`：[ × b] = 428
- L575 [cell] `7`：[ × N] = 7
- L575 [cell] `0.379`：[ × trust] = 0.379
- L575 [cell] `1890`：[ × b] = 1890
- L575 [cell] `9`：[ × N] = 9
- L575 [cell] `3935`：[ × b] = 3935
- L575 [cell] `9`：[ × N] = 9
- ……共 116 个，见 JSON