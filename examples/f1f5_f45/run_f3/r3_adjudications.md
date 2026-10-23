# 数字对账裁决报告（R3 自动化：机械层 + LLM 语义裁决）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f3\extracted_text.txt`；RPC：HTTP 200
- 结论：**CRITICAL** —— critical 19 个（实质断言无来源，一票 Critical）；noise 8 / supported 8

| token | 层 | 裁决 | 置信 | 依据 | 论文原句 |
|---|---|---|---|---|---|
| `1.2` | mechanical | **supported** | high | 证据 2 位舍入 1.1992616666666667=1.1992616666666667→1.2 | ∆MAE −0.034) versus RAG Γ=1.2 (p=.42, ∆MAE +0.008) |
| `8.1` | llm | **critical** | high | 8.1是结果指标Γ的数值断言,机械匹配无命中,且原句未声明任何来源或证据文件,属于实质断言但无来源,构成一票Critic | cells, conf 0.99) shows Γ monotonic 8.1→0.9 but wi |
| `0.45` | mechanical | **supported** | high | 证据 2 位舍入 0.45258333333333334=0.45258333333333334→0.45 | examined descriptively as a candidate proxy (r=0.4 |
| `0.999` | llm | **critical** | high | 0.999为统计功效的实质断言,属结果/指标而非噪音；论文未声明对应产物JSON来源,机械层亦无命中,故一票 Criti | Our n=500 per architecture yields power >0.999 for |
| `0.08` | mechanical | **supported** | high | 证据 2 位舍入 0.0809=0.0809→0.08 | effect and minimum detectable dmin=0.18 at power 0 |
| `2.5` | llm | **noise** | high | 2.5是模型版本号Qwen2.5:14B的一部分,属于模型标识而非统计量或结果指标,不构成实质断言。 | Models: Qwen3:4b, Gemma3:4b, DeepSeek-R1:7B, Qwen2 |
| `13.1` | llm | **critical** | high | 数字13.1是Γ值的上界,属于具体结果/统计量,并非噪音或派生中间量。论文句子未声明任何来源文件,机械层也未匹配到证据J | whereas our Γ values (up to 13.1) reflect length-s |
| `12.1` | llm | **critical** | high | 该数字是Γ的经验估计值,属实质统计断言；机械匹配无命中且论文未指明可核验来源,故一票 Critical。 | per-seed Γ (prefix-length W1) for append-only: 12. |
| `12.5` | llm | **noise** | high | 论文原文行中只有12.1和12,未出现12.5；机械匹配无命中,非实质断言或提取误报。 | Empirical estimates of Γ. Within our sample, per-s |
| `6.5` | llm | **critical** | high | 6.5为summarization评估指标结果（实质断言）,机械匹配无命中,且论文未声明来源。 | for summarization: 6.5, 6.9, 6.7 (mean 6.7, |
| `6.9` | llm | **critical** | high | 6.9是摘要任务的一组结果指标之一,属于实质断言；机械匹配无命中且论文未声明该数值来源,无法在产物JSON中核实。 | for summarization: 6.5, 6.9, 6.7 (mean 6.7, |
| `98.2` | llm | **critical** | high | 98.2%是解析率指标,属实质断言；上下文仅列数值,未声明来源,机械匹配无命中,违反一票Critical。 | Parse rates: Qwen3:4b 98.2%, Gemma3:4b 93.3% |
| `93.3` | llm | **critical** | medium | 93.3%是Gemma3:4b的parse rate,属实质结果指标,但论文未声明任何来源文件,机械匹配无命中。 | Parse rates: Qwen3:4b 98.2%, Gemma3:4b 93.3%, Deep |
| `96.1` | llm | **critical** | high | 96.1%是DeepSeek-R1:7B的解析率,属结果指标实质断言；机械层无匹配支撑,原句未声明来源,且未提供JSON | Parse rates: Qwen3:4b 98.2%, Gemma3:4b 93.3%, Deep |
| `99.1` | llm | **critical** | high | 99.1% 是 Qwen2.5:14B 解析率,属结果型实质性指标；论文未声明来源,且机械匹配证据 JSON 无命中,不 | Parse rates: ... Qwen2.5:14B 99.1%. |
| `0.11` | mechanical | **supported** | high | 证据 2 位舍入 0.1129=0.1129→0.11 | ton, no-memory product 0.08) and K=2 (mean product |
| `0.084` | llm | **critical** | high | 0.084为区间端点/统计量,属实质结果断言；机械匹配未命中且未声明证据来源,不能视为噪声。 | [+0.014, +0.084] |
| `1.6` | llm | **critical** | high | 1.6 为 p 值指数部分,属于实质统计断言；论文未声明对应结果文件或派生路径,机械层无匹配,故判 critical。 | append-only was associated with the largest shift  |
| `0.012` | llm | **critical** | high | 0.012 是 Qwen2.5:14B 的 append-only ∆MAE 效应量,属实质统计结果；机械层直接/舍入匹 | Qwen2.5:14B append-only +0.012, |
| `51.55` | llm | **noise** | high | 51.55 位于 Training cost 成本对比中,按裁决规则属于成本类噪音,非结果/统计量/指标；无需机械匹配支 | Training cost (51.55M vs 7.61B, 0.68%) |
| `7.61` | llm | **noise** | high | 7.61B为训练成本数值,属于成本类非实质结果指标,且机械匹配无命中,视为误报。 | Training cost (51.55M vs 7.61B, 0.68%) |
| `0.038` | llm | **critical** | medium | 0.038 是校准后偏差区间的实质统计量；机械匹配无命中,且论文片段未声明任何来源,无法验证。 | the shift persisted after calibration, though redu |
| `0.039` | llm | **critical** | medium | 数字0.039带显著性星号,属于回归系数/统计量实质断言；机械匹配无命中,论文未声明其来源,构成无来源关键断言。 | +0.039∗ |
| `8.69` | llm | **critical** | high | p值8.69e-6是统计显著性实质断言,论文未声明其来源文件或计算方法,机械匹配无命中,无法追溯。 | Gamma-DeltaMAE r=0.89 (9 combos excl Qwen2.5:14B,  |
| `0.032` | llm | **critical** | high | 原文为−0.032,是∆MAE统计量,属于实质断言；机械匹配无命中,且该行未声明任何来源如JSON路径。 | ∆MAE for append-only across 3 seeds: −0.032, −0.03 |
| `0.6` | mechanical | **supported** | high | 证据 2 位舍入 0.604=0.604→0.6 | 0.002); for RAG θ=0.1: +0.007, +0.010, +0.006 (SD  |
| `0.15` | mechanical | **supported** | high | 证据 2 位舍入 0.151=0.151→0.15 | Limitations. (i) Single threshold θ=0.1; other thr |
| `1.26` | llm | **noise** | high | 1.26 为 numpy 版本号,属软件环境配置信息,非实质断言或统计量,无需在产物 JSON 中匹配。 | requirements.txt pins numpy 1.26, scipy 1.11, matp |
| `3.8` | llm | **noise** | high | 3.8 是 matplotlib 的版本号,属于依赖配置信息,非结果或统计指标,不构成实质断言。 | requirements.txt pins numpy 1.26, scipy 1.11, matp |
| `12.2` | llm | **noise** | high | Γ≈12.2 是理论边界中的参数/中间量,用于计算 bound,并非论文结论性结果或统计指标,故为噪音。 | with Γ ≈12.2 the bound gives |∆MAE| ≤0.049, close  |
| `57.3` | llm | **critical** | medium | 57.3% 是百分比结果/指标,非噪声；可见上下文未声明其来源或 JSON 路径；机械匹配无命中,无法归为 suppor | The 57.3% production- |
| `0.018` | llm | **critical** | medium | 机械层直接/比例/舍入匹配无命中；该数字以'+0.018'独立出现,形态类似结果增量,且未见来源声明,按对抗原则视为无来 | 原文行:+0.018 |
| `0.42` | mechanical | **supported** | high | 证据 2 位舍入 0.4249=0.4249→0.42 | 0.42, temperature 0.31, top_p 0.08. |
| `0.2` | mechanical | **supported** | high | 证据 2 位舍入 0.1953=0.1953→0.2 | 0.15→78%, 0.2→85%, 0.3→91%. Γ and ∆MAE are sample- |
| `1.5` | llm | **noise** | high | 数字1.5为baseline Gamma参数值,属于模型配置参数而非实质结果指标；且原文明确标注Values are d | baseline Gamma 1.5 →0.4, ∆MAE −0.030 →−0.015 as fi |

- 语义：noise=误报（非实质断言）；supported=实质断言且有来源；critical=实质断言无来源（一票 Critical）；未裁决=LLM 失败维持原判