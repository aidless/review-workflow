# 统计定性报告（R4 自动化：口径换算机械层 + LLM 对抗裁决）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；RPC：HTTP 200
- 结论：**PASS** —— NOT_IN_PAPER 3 条全部定性为口径换算/噪音 → 已解释

| 类型 | json_path | 状态 | 机械候选 | 裁决 | 置信 | 依据 | 建议 |
|---|---|---|---|---|---|---|---|
| friedman_p | `cross_model.friedman` | **NOT_IN_PAPER** | 粗精度舍入 0.37；n.s./not significant 标记；显著性星号标记 | 口径换算 | high | Cross-model Friedman on 16 paired tasks ... was non-signific | 在表格或脚注补全精确值p=0.3679及chi2=2.0,df=2,便于产物溯源。 |
| friedman_p | `friedman_full_P3` | **NOT_IN_PAPER** | 粗精度舍入 0.37；n.s./not significant 标记；显著性星号标记 | 口径换算 | high | Cross-model Friedman on 16 paired tasks (with 10 all-zero L1 | 无需修正；0.37为0.3679的两位小数舍入,精度口径一致,建议可选补注chi2=2.0,df=2。 |
| friedman_p | `simulated_k4_N12` | **NOT_IN_PAPER** | 阈值形式 p<0.05；粗精度舍入 0.04；显著性星号标记 | 噪音 | high | Cross-model Friedman on 16 paired tasks ... was non-signific | 无需补报；simulated_k4_N12为内部模拟中间量,非论文报告统计量。 |

- 裁决语义：口径换算/噪音=已解释（不构成门禁）；遗漏/疑似矛盾=维持 Major（文本层 WARN，不 FAIL）；MISMATCH 恒为机械 Critical