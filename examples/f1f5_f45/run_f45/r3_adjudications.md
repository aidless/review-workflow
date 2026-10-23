# 数字对账裁决报告（R3 自动化：机械层 + LLM 语义裁决）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f45\extracted_text.txt`；RPC：HTTP 200
- 结论：**CRITICAL** —— critical 35 个（实质断言无来源，一票 Critical）；noise 14 / supported 13

| token | 层 | 裁决 | 置信 | 依据 | 论文原句 |
|---|---|---|---|---|---|
| `0.098` | llm | **critical** | high | 0.098为mimicry条件的∆统计量,属实质结果断言；论文未声明对应JSON来源,机械匹配无命中,按规则判criti | Our observed ∆=0.114 (injection) and 0.098 (mimicr |
| `0.620` | mechanical | **supported** | high | 证据 2 位舍入 0.6219=0.6219→0.62 | the finding: hybrid achieves 0.620 vs. 0.435 for m |
| `99.78` | llm | **noise** | high | 该数字出现在 parse/is_real/verbalized 的模型输出描述中,是生成内容中的置信度或中间解析值,非论 | parse 99.78% is_real, SHA 798bbc2d (truncated SHA2 |
| `0.985` | llm | **critical** | medium | 0.985为置信度指标,属实质断言；机械匹配无对应,原句未指明来源；虽标称uninformative,仍为统计数据,按规 | conf 0.985 vs 0.985 uninformative |
| `3.5` | mechanical | **supported** | high | 证据 2 位舍入 3.502=3.502→3.5 | than binary voting. Both require f < N/2, which ho |
| `0.08` | mechanical | **supported** | high | 证据 2 位舍入 0.0809=0.0809→0.08 | N(0.80, 0.08) truncated to [0, 1]. This models a c |
| `2.5` | llm | **noise** | high | 该数字是模型名称Qwen2.5的版本号,属于标识符而非实质断言,不涉及结果或统计量。 | Four model families (Qwen3:4b, Gemma3:4b, DeepSeek |
| `0.185` | llm | **critical** | high | 0.185 是混合方法性能提升的实质统计量,并非噪音；机械匹配无命中,且论文未声明对应结果 JSON 来源,按规则一票  | hybrid 0.620 vs. 0.435, ∆=+0.185 (McNemar b≈2960,  |
| `0.112` | llm | **critical** | high | 该数字为实验统计结果（信任优势）,属实质断言。论文未声明对应证据文件或来源,机械层亦无匹配,构成无来源的关键断言。 | Injection advantage of trust over majority ranged  |
| `0.099` | llm | **critical** | high | 0.099为mimicry优势区间上限,属实质统计断言；论文未给出可机械匹配的来源JSON路径或数值,按对抗裁决判为无来 | Injection advantage of trust over majority ranged  |
| `0.563` | llm | **critical** | high | 0.563是实质统计量（诚实平均置信度）,非噪音。论文未声明任何数据文件或JSON来源,仅给出理论混合公式,无法机械匹配 | Honest mean confidence 0.563 (SD 0.08) ... matchin |
| `0.522` | llm | **critical** | high | 0.522是实质性能指标（准确率）,非噪声；论文未指明来源,机械匹配无对应,且无法从已有JSON定位,构成无来源关键断言 | honest) and 0.522 under mimicry (50% correct with  |
| `3.12` | mechanical | **supported** | high | 证据 2 位舍入 3.118=3.118→3.12 | Environment: Python 3.12, numpy, scipy, matplotlib |
| `2.7` | mechanical | **supported** | high | 证据 2 位舍入 2.703=2.703→2.7 | 2.7×10−138 |
| `2.2` | llm | **critical** | high | 2.2×10−137为极小数值,通常是统计检验p值或显著性结果,属实质断言；机械匹配无命中,且论文未声明对应JSON来源 | 2.2×10−137 |
| `6.2` | llm | **critical** | medium | 该数字以科学计数法表示一个极小的数值（6.2×10^-120）,通常为概率或显著性统计量,属于实质断言。产物JSON无对 | 6.2×10−120 |
| `6.3` | llm | **critical** | medium | 6.3×10−117 为极小显著性数量级,通常对应 p 值/统计结果,属实质断言而非噪音；机械层在证据 JSON 中无直 | 6.3×10−117 |
| `3.2` | llm | **critical** | high | 该数字是科学计数法中的统计结果（3.2e-117）,属实质断言而非噪音；机械匹配未命中,且未声明可核验来源,按规则一票  | 3.2×10−117 |
| `0.56` | mechanical | **supported** | high | 证据 2 位舍入 0.5571=0.5571→0.56 | confidence is a mixture: 0.65×0.70+0.35×0.30 = 0.5 |
| `0.525` | llm | **noise** | high | 0.525 是由 0.30 与 0.75 按 0.5 权重直接计算的派生中间量,属于噪音而非独立结果；产物 JSON 无 | yielding mean 0.5×0.30 + 0.5×0.75 = 0. |
| `0.2` | mechanical | **supported** | high | 证据 2 位舍入 0.1953=0.1953→0.2 | confidence bin shows accuracy increasing from ≈0.3 |
| `0.42` | mechanical | **supported** | high | 证据 2 位舍入 0.4249=0.4249→0.42 | [0.2, 0.3] rises from 0.35 to 0.42 because capture |
| `0.51818` | llm | **noise** | high | 该 token 是数学式 0.5^{1818} 丢失上标后的误读,不是独立十进制统计量；2×0.51818≈1.036, | Under H0: b = c, the probability of c=0, b=1818 is |
| `0.92` | mechanical | **supported** | high | 证据 2 位舍入 0.9214=0.9214→0.92 | aim to rule out a sign flip, not just detect a sma |
| `1.96` | llm | **noise** | high | 1.96 是95%正态近似置信区间的固定z值,属于统计公式参数/阈值,非论文报告的实质结果或指标。机械无匹配不构成问题。 | Normal-approximation 95% CIs for per-rule correctn |
| `0.012` | llm | **critical** | high | 0.012为统计误差项,属于实验结果的实质断言（不确定性指标）,并非噪音。机械匹配未命中,且论文未明确声明任何可定位的J | seed 42) are ∆inj=0.114±0.012 and ∆mim=0.098±0.011 |
| `1.26` | llm | **noise** | high | 1.26 是 numpy 版本号,属于环境描述噪音,非结果指标或实质断言。 | Compute. Simulator runtime ≈4 minutes on a single  |
| `3.8` | llm | **noise** | high | 3.8出现在matplotlib 3.8中,是软件版本号,非实质断言或结果指标,属于噪音。 | figure generation ≈10 seconds (matplotlib 3.8). No |
| `0.302` | llm | **critical** | high | 0.302±0.10 是 injection 条件下的实验结果统计量,属于实质断言而非阈值/版本等噪音；论文原句未声明任 | wrong 0.302 ± 0.10 (injection) and 0.699 ± 0.10 vs |
| `0.301` | llm | **critical** | high | 0.301为实质结果统计量（均值±标准差）,非噪音；论文未声明来源,机械层无匹配,属无来源实质断言。 | wrong 0.302 ± 0.10 (injection) and 0.699 ± 0.10 vs |
| `0.540` | mechanical | **supported** | high | 证据 2 位舍入 0.5354=0.5354→0.54 | [0.540, 0.556] |
| `0.556` | llm | **critical** | high | 0.556 为置信区间上界,属统计结果而非噪音；论文未声明任何 JSON 来源,机械匹配也无命中。 | [0.540, 0.556] |
| `0.443` | llm | **critical** | medium | 0.443 作为区间 [0.427,0.443] 的上界,属于统计量/结果的一部分,而非成本/版本等噪音；机械匹配无命中 | 论文原文行:[0.427, 0.443] |
| `0.697` | llm | **noise** | medium | 0.697仅为区间上界,属于范围参数,非独立统计量；且机械匹配无命中,无来源声明,判定为噪音。 | [0.683, 0.697] |
| `0.612` | llm | **critical** | high | 0.612 是置信区间/范围的下界,属于结果统计量而非噪音；机械匹配未命中,且给出的原句位置未声明 results JS | 论文原文行:'[0.612, 0.628]' |
| `0.102` | llm | **critical** | low | 0.102作为区间[0.102,0.126]的一部分,疑似统计量（如置信区间下限）而非噪声；机械层无匹配,且未在证据中声 | 论文原文行:[0.102, 0.126] |
| `0.103` | llm | **critical** | high | 0.103为置信区间下界,属实质统计断言。机械匹配无命中,且原句未声明来源文件,无法在证据JSON中核实。 | Under injection, ∆trust bootstrap CI [0.103, 0.125 |
| `0.087` | llm | **noise** | high | 数字 0.087 是区间 [0.087, 0.109] 的左端点,属于范围/边界的一部分,非独立统计结果；机械匹配无命中 | 论文原文行: [0.087, 0.109] |
| `0.109` | llm | **critical** | medium | 该数以置信区间上界形式出现,属于结果/统计量而非噪音；机械层在证据 JSON 中未命中,且给出行未声明来源,符合 cri | 出现位置行原文为 [0.087, 0.109]。 |
| `0.108` | llm | **critical** | medium | 0.108为mimicry条件下Δtrust bootstrap置信区间上限,属实质统计断言；机械层无命中且未声明任何来 | under mimicry [0.088, 0.108 |
| `0.173` | llm | **critical** | medium | 0.173 作为区间下界属于统计结果/指标,非噪音；机械层未命中,且未见论文声明对应来源。 | 原文行:[0.173, 0.197] |
| `0.197` | llm | **critical** | medium | 数字0.197与0.173构成数值区间,疑似统计量（如置信区间或指标范围）,属实质断言；机械匹配无命中且未见明确来源声明 | 论文原文行: [0.173, 0.197] |
| `0.048` | llm | **critical** | low | 0.048 是区间 [0.048,0.068] 的下限端点,属统计结果而非噪音；机械匹配未命中,且该行未声明来源,构成无 | [0.048, 0.068] |
| `0.068` | llm | **critical** | medium | 0.068 与区间上界相同且带正号,属于统计结果而非噪声；机械层无命中,且未声明可溯源证据JSON,符合 critica | 原文行:"[0.048, 0.068] +0.068" |
| `0.067` | llm | **noise** | medium | 0.067 出现在区间 [0.049, 0.067] 中,作为区间上界而非独立统计量,属于区间表示的一部分,非实质断言, | [0.049, 0.067] |
| `0.154` | llm | **critical** | high | 0.154是效应量-0.142的置信区间上界,属于统计结果实质断言；论文未声明来源,机械匹配无命中,构成无来源关键数值。 | trust −trimmed = −0.142 [−0.154, −0.130], mimicry  |
| `0.084` | llm | **critical** | high | 0.084是mimicry系数置信区间上界,属实质统计断言；机械匹配无命中,论文原文未声明来源,构成无来源关键数据。 | mimicry = +0.073 [+0.062, +0.084], confirming the  |
| `0.6` | mechanical | **supported** | high | 证据 2 位舍入 0.604=0.604→0.6 | per bin: [0, 0.2]: 0.31, [0.2, 0.4]: 0.38, [0.4, 0 |
| `0.58` | mechanical | **supported** | high | 证据 2 位舍入 0.5819=0.5819→0.58 | captured high-confidence wrong votes). Under mimic |
| `0.138` | llm | **critical** | low | 该数字以“+0.138”形式重复出现,疑似统计结果或指标；机械层在产物 JSON 中无命中,且未见任何来源声明,无法归为 | +0.138（论文原文行） |
| `0.201` | llm | **critical** | low | 孤立正数+0.201无法匹配任何JSON值；上下文缺失,无法判定为参数/中间量,通常是回归系数或统计量；且未声明来源,按 | +0.201 |
| `0.120` | mechanical | **supported** | high | 证据 2 位舍入 0.11514918024534128=0.11514918024534128→0.12 | +0.120 |
| `0.172` | llm | **critical** | medium | 数字0.172带符号出现,似为统计量或结果；机械匹配无命中,论文未声明来源,无法在产物JSON中找到对应。 | +0.172 |
| `0.119` | llm | **critical** | medium | 数字0.119为实质断言（如结果或指标）,但机械匹配无任何命中,且论文未声明来源,违反可追溯性,故一票critical。 | +0.119 |
| `0.018` | llm | **noise** | low | 数字以增量形式出现（+0.018）,非独立统计量；机械层未匹配到支撑,且缺乏上下文证明其为核心结果,故按非实质断言处理。 | +0.018 |
| `1.61` | llm | **critical** | high | 1.61×10^-86 是极小的概率/显著性结果,属于实质统计断言而非噪音；产物 JSON 在容差内无匹配,论文未给出可 | 1.61×10−86 |
| `0.118` | llm | **critical** | medium | 0.118为具体数值结果,机械匹配无命中,论文未声明任何来源,疑似无支撑的关键数字。 | 论文原文行出现 '+0.118' 作为独立数值。 |
| `0.074` | llm | **critical** | medium | 带+号小数疑似效应量/增量,属于实质结果断言；机械匹配直接/比例/舍入均无命中,且未见来源引用,无法支撑。 | +0.074 |
| `0.128` | llm | **noise** | low | 孤立行 '+0.128' 无指标名/统计量/来源,无法构成实质断言；按噪声处理,避免将上下文不明的数字误判为缺源关键结果 | 论文原文行仅为 '+0.128',未给出指标或来源声明。 |
| `0.231` | llm | **critical** | medium | 数字0.231为孤立数值,无上下文表明其属噪音,机械层无匹配,论文未声明来源,视为实质断言无来源。 | +0.231 |
| `0.075` | llm | **noise** | medium | 孤立数字+0.075无上下文,无法判断为结果或统计量,且未指明来源,可能为参数、增量或其他非实质性信息,故按噪声处理。 | +0.075 |
| `0.046` | llm | **noise** | high | 孤立文本'+0.046'无统计量语义,无法构成实质断言,且机械匹配无命中,判定为噪音误报。 | +0.046 |

- 语义：noise=误报（非实质断言）；supported=实质断言且有来源；critical=实质断言无来源（一票 Critical）；未裁决=LLM 失败维持原判