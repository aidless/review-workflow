# 数字对账裁决报告（R3 自动化：机械层 + LLM 语义裁决）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f1\extracted_text.txt`；RPC：HTTP 200
- 结论：**CRITICAL** —— critical 15 个（实质断言无来源，一票 Critical）；noise 7 / supported 7

| token | 层 | 裁决 | 置信 | 依据 | 论文原句 |
|---|---|---|---|---|---|
| `1.6` | llm | **critical** | medium | 1.6为p值指数系数,属统计显著性实质断言。论文中未声明具体数据来源或证据文件,机械匹配亦无命中,故一票Critical | p=1.6×10−5 (Qwen3:4b, Wilcoxon W=12480) |
| `0.42` | mechanical | **supported** | high | 证据 2 位舍入 0.4249=0.4249→0.42 | of +0.047 (Qwen3:4b, Wilcoxon W=12480, p=1.6×10−5, |
| `0.62` | mechanical | **supported** | high | 证据 2 位舍入 0.6219=0.6219→0.62 | control (75-char neutral prefix, +0.005, p=0.62, s |
| `0.645` | llm | **critical** | high | 0.645是pilot置信度指标,属于实质统计量；论文仅提及supplementary pilot,未声明具体来源文件, | supplementary 500×3 phrasings pilot 0.645/0.646/0. |
| `12.2` | llm | **noise** | high | Γ≈12.2是参数Γ的示例值,标注为illustrative,由前缀字符串长度派生,属于中间量而非最终结果。机械匹配无命 | Γ ≈12.2 chars from prefix string lengths (illustra |
| `98.2` | llm | **critical** | high | 98.2%是模型解析率,属于实质结果指标；机械匹配无命中,且原文未声明任何来源文件,按规则一票Critical。 | Parse rates: Qwen3:4b 98.2%, Gemma3:4b |
| `93.3` | llm | **critical** | high | 93.3% 是 Gemma3:4b 的 parse rate 结果指标,属于实质断言。机械层按直接/比例/舍入容差均未匹 | Gemma3:4b 93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B |
| `96.1` | llm | **critical** | medium | 96.1%是DeepSeek-R1:7B的解析率结果,属实质断言；机械匹配无命中,且论文未声明该数值来自任何结果文件或可 | Gemma3:4b 93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B |
| `2.5` | llm | **noise** | high | 该数字出现在模型名“Qwen2.5:14B”中,是版本号而非结果/统计量/指标,机械匹配无命中属正常,不应视为实质断言。 | Qwen2.5:14B tag 7cdf5a0187d5; Qwen2.5:14B 93.3% |
| `99.1` | llm | **critical** | medium | 99.1% 是模型性能指标,属实质断言；机械匹配无命中且原文未声明来源,无法验证支撑。 | Gemma3:4b 93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B |
| `0.084` | llm | **critical** | medium | 该小数以置信区间形式出现（区间上限）,属于统计结果,非参数/噪声；机械匹配无命中,且未见声明JSON来源,构成无来源实质 | [+0.014, +0.084] |
| `0.66` | mechanical | **supported** | high | 证据 2 位舍入 0.6578=0.6578→0.66 | 0.42 [0.18, 0.66] |
| `0.08` | mechanical | **supported** | high | 证据 2 位舍入 0.0809=0.0809→0.08 | 0.31 [0.08, 0.54] |
| `0.54` | mechanical | **supported** | high | 证据 2 位舍入 0.5354=0.5354→0.54 | 0.31 [0.08, 0.54] |
| `0.012` | llm | **critical** | medium | 该数字为性能提升指标（实质断言）,但产物JSON无匹配值,论文未声明来源,故为Critical。 | 论文原文行:+0.012（三处） |
| `0.067` | llm | **critical** | high | 0.067 是排名通道效应量/统计量,构成实质性结果断言；机械匹配无命中,且未声明任何 evidence JSON 来源 | The ranking channel exhibits the largest shift (+0 |
| `0.023` | llm | **critical** | low | 0.023 为区间的一部分,属于统计量（如置信区间/效应量）,构成实质断言；机械层无匹配,且未提供任何来源引用,无法支撑 | [+0.023, +0.121] |
| `0.121` | llm | **critical** | high | 该区间上界为结果型统计量,非成本/参数/中间量；机械匹配无命中且行内未声明数据来源,构成无来源实质断言。 | 论文原文行: '[+0.023, +0.121]' |
| `0.12` | mechanical | **supported** | high | 证据 2 位舍入 0.11514918024534128=0.11514918024534128→0.12 | 0.38 [0.12, 0.64] |
| `0.64` | mechanical | **supported** | high | 证据 2 位舍入 0.6375=0.6375→0.64 | 0.38 [0.12, 0.64] |
| `0.039` | llm | **critical** | high | 该数字带显著性星号,属于统计结果/回归系数,为实质断言；原文未声明结果文件等来源,机械匹配也未命中,故按一票 Criti | +0.039∗ |
| `0.038` | llm | **noise** | high | 该数字以“+0.038∗”形式出现在公式/表达式项中,是模型方程系数（参数）,非独立结果或统计量；参数类数字无需在产物J | +0.038∗ |
| `0.045` | llm | **critical** | high | 0.045是seed 0的∆MAE结果,属实质断言；机械层未在证据JSON中匹配,且原文未声明来源,因此按规则判crit | Cross-seed stability. ∆MAE across 3 seeds: seed 0  |
| `0.075` | llm | **critical** | low | 孤立数值疑似实质结果,无上下文且未声明来源,机械层无匹配,按对抗原则判为无来源实质断言。 | −0.075 |
| `1.26` | llm | **noise** | high | 1.26 是 numpy 版本号的一部分,属于环境配置信息,非结果/统计量/指标等实质断言,机械匹配无命中符合预期。 | requirements.txt locks numpy 1.26, scipy 1.11, mat |
| `3.8` | llm | **noise** | high | 3.8 是 matplotlib 的版本号,属于依赖环境配置,而非结果/统计量/指标,不构成实质断言。 | requirements.txt locks numpy 1.26, scipy 1.11, mat |
| `0.999` | llm | **critical** | high | 统计功效是实质断言,非噪声；论文未指明任何生成该数值的来源文件或计算方法,机械匹配无命中。 | Our n=500 yields power > 0.999 under either |
| `22.04` | llm | **noise** | high | 22.04 是 Ubuntu 操作系统版本号,非实质断言数值,属于环境配置噪音。 | environment.yml: Ubuntu 22.04, Pyth |
| `13.0` | llm | **noise** | high | 13.0 是 CUDA 版本号,属于环境配置噪音,非实质结果或统计量,机械层无匹配合理。 | 3.10, CUDA 13.0. Seed 42. |

- 语义：noise=误报（非实质断言）；supported=实质断言且有来源；critical=实质断言无来源（一票 Critical）；未裁决=LLM 失败维持原判