# 数字对账裁决报告（R3 自动化：机械层 + LLM 语义裁决）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`；RPC：HTTP 200
- 结论：**MAJOR** —— 2 个未裁决（LLM 失败 2）→ 维持 recompute 原判 Major；noise 0 / supported 0

| token | 层 | 裁决 | 置信 | 依据 | 论文原句 |
|---|---|---|---|---|---|
| `0.207` | llm | **未裁决** | - |  |  |
| `0.275` | llm | **未裁决** | - |  |  |

- 语义：noise=误报（非实质断言）；supported=实质断言且有来源；critical=实质断言无来源（一票 Critical）；未裁决=LLM 失败维持原判