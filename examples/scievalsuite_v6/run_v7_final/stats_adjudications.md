# 统计定性报告（R4 自动化：口径换算机械层 + LLM 对抗裁决）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；RPC：HTTP 200
- 结论：**PASS** —— NOT_IN_PAPER 3 条全部定性为口径换算/噪音 → 已解释

| 类型 | json_path | 状态 | 机械候选 | 裁决 | 置信 | 依据 | 建议 |
|---|---|---|---|---|---|---|---|
| friedman_p | `cross_model.friedman` | **NOT_IN_PAPER** | 粗精度舍入 0.37；n.s./not significant 标记；显著性星号标记 | 口径换算 | high | Cross-model Friedman on 16 paired tasks (with 10 all-zero L1 | 无需修改；如严谨可在附录补全精度0.368及chi2=2.0,df=2 |
| friedman_p | `friedman_full_P3` | **NOT_IN_PAPER** | 粗精度舍入 0.37；n.s./not significant 标记；显著性星号标记 | 口径换算 | high | Cross-model Friedman on 16 paired tasks (with 10 all-zero L1 | 无需修改；建议在表格/附录补充精确值p=0.3679及chi2=2.0,df=2以增强可追溯性。 |
| friedman_p | `simulated_k4_N12` | **NOT_IN_PAPER** | 阈值形式 p<0.05；粗精度舍入 0.04；显著性星号标记 | 噪音 | high | post-hoc curated L1a subset (6 tasks) gives p=0.003 (explora | 无需补充；模拟中间量不属论文应报告统计量。 |

- 裁决语义：口径换算/噪音=已解释（不构成门禁）；遗漏/疑似矛盾=维持 Major（文本层 WARN，不 FAIL）；MISMATCH 恒为机械 Critical