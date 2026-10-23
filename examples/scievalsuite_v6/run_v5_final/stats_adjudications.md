# 统计定性报告（R4 自动化：口径换算机械层 + LLM 对抗裁决）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；RPC：HTTP 200
- 结论：**PASS** —— NOT_IN_PAPER 1 条全部定性为口径换算/噪音 → 已解释

| 类型 | json_path | 状态 | 机械候选 | 裁决 | 置信 | 依据 | 建议 |
|---|---|---|---|---|---|---|---|
| friedman_p | `simulated_k4_N12` | **NOT_IN_PAPER** | 阈值形式 p<0.05；粗精度舍入 0.04；显著性星号标记 | 噪音 | high | Cross-model Friedman on 16 paired tasks was non-significant  | 无需补报；确认simulated_k4_N12为内部模拟中间量,与论文实际Friedman检验无关,可从可复算性检查中排 |

- 裁决语义：口径换算/噪音=已解释（不构成门禁）；遗漏/疑似矛盾=维持 Major（文本层 WARN，不 FAIL）；MISMATCH 恒为机械 Critical