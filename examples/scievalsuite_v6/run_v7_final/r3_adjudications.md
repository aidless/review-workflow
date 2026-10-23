# 数字对账裁决报告（R3 自动化：机械层 + LLM 语义裁决）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；RPC：HTTP 200
- 结论：**MAJOR** —— 4 个未裁决（LLM 失败 4）→ 维持 recompute 原判 Major；noise 0 / supported 1

| token | 层 | 裁决 | 置信 | 依据 | 论文原句 |
|---|---|---|---|---|---|
| `0.37` | mechanical | **supported** | high | 证据 2 位舍入 0.367=0.367→0.37 | We present SciEvalSuite, a unified evaluation suit |
| `12.1` | llm | **未裁决** | - |  |  |
| `0.46` | llm | **未裁决** | - |  |  |
| `0.3553` | llm | **未裁决** | - |  |  |
| `7.7` | llm | **未裁决** | - |  |  |

- 语义：noise=误报（非实质断言）；supported=实质断言且有来源；critical=实质断言无来源（一票 Critical）；未裁决=LLM 失败维持原判