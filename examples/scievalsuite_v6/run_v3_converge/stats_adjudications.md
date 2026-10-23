# 统计定性报告（R4 自动化：口径换算机械层 + LLM 对抗裁决）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；RPC：HTTP 200
- 结论：**PASS** —— NOT_IN_PAPER 1 条全部定性为口径换算/噪音 → 已解释

| 类型 | json_path | 状态 | 机械候选 | 裁决 | 置信 | 依据 | 建议 |
|---|---|---|---|---|---|---|---|
| friedman_p | `simulated_k4_N12` | **NOT_IN_PAPER** | 阈值形式 p<0.05；粗精度舍入 0.04；显著性星号标记 | 噪音 | high | P5 curated L1a (6 tasks, k=4): chi2=14.25, p=0.0026, CD=1.91 | 无需行动,模拟内部一致性检查值,非论文声称。 |

- 裁决语义：口径换算/噪音=已解释（不构成门禁）；遗漏/疑似矛盾=维持 Major（文本层 WARN，不 FAIL）；MISMATCH 恒为机械 Critical