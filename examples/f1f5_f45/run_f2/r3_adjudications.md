# 数字对账裁决报告（R3 自动化：机械层 + LLM 语义裁决）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f2\extracted_text.txt`；RPC：HTTP 200
- 结论：**CRITICAL** —— critical 28 个（实质断言无来源，一票 Critical）；noise 7 / supported 9

| token | 层 | 裁决 | 置信 | 依据 | 论文原句 |
|---|---|---|---|---|---|
| `10.88` | llm | **critical** | high | 10.88是P/B tightness ratio的9格中位数,属实质统计断言；论文未声明任何产物JSON来源,机械匹配 | tightness ratio P/B of 5–10× for γ ∈{0.5, 1.0} (me |
| `0.08` | mechanical | **supported** | high | 证据 2 位舍入 0.0809=0.0809→0.08 | via intraclass correlation. Baselines at K=1 (P=0. |
| `0.11` | mechanical | **supported** | high | 证据 2 位舍入 0.1129=0.1129→0.11 | via intraclass correlation. Baselines at K=1 (P=0. |
| `0.62` | mechanical | **supported** | high | 证据 2 位舍入 0.6219=0.6219→0.62 | [0.62,0.74] to avoid contradiction with the survey |
| `2.5` | llm | **noise** | high | 2.5 是模型名称 Qwen2.5 的版本号,属于噪音,非数据指标或实质断言。 | Qwen2.5:14B via Ollama, plus Qwen2.5:7b via API |
| `98.2` | llm | **critical** | medium | 98.2%为Qwen3:4b的解析率,属于结果指标实质断言；机械层无匹配,且原文未声明对应来源文件,故一票Critica | Parse rates: Qwen3:4b 98.2%, Gemma3:4b 93.3%, D |
| `93.3` | llm | **critical** | high | 93.3% 是 Gemma3:4b 的 parse rate,属实验结果/统计指标,为实质断言；机械匹配无命中,且论文原 | Parse rates: Qwen3:4b 98.2%, Gemma3:4b 93.3%, D 93 |
| `96.1` | llm | **critical** | medium | 96.1为模型性能指标（准确率）,属实质断言；机械匹配无对应JSON值,且原文未声明来源,无法核验。 | 93.3%, DeepSeek-R1:7B 96.1%, Qwen2.5:14B 99.1%; un |
| `99.1` | llm | **critical** | high | 该数字为模型Qwen2.5:14B的性能百分比（99.1%）,属实质统计断言；论文未声明来源,机械匹配无命中,故一票cr | 96.1%, Qwen2.5:14B 99.1%, Qwen2.5:7b 98.7% (API);  |
| `98.7` | llm | **critical** | high | 98.7%是Qwen2.5:7b的API评估准确率,属于实质断言；机械匹配无命中,且原文未声明任何可核验来源,违反可复现 | Qwen2.5:7b 98.7% (API); unparseable votes excluded |
| `99.78` | llm | **supported** | high | 99.78%为补充准确率,属实质指标,论文明确标注来源Appendix Table S1,故非噪音且非无来源。机械层未命 | Note: Gemma3:4b 99.78% supplementary accuracy (App |
| `0.989` | llm | **critical** | medium | 0.989是Wilson置信区间下界,属于实质统计断言,非噪音。机械匹配未命中,论文未在该句声明来源,且无法由已知JSO | prior, Wilson CI [0.989, 1.000]) is reported as su |
| `0.53` | mechanical | **supported** | high | 证据 2 位舍入 0.533=0.533→0.53 | assumes K ≥3 for normal approximation; K=1, 2 use  |
| `1.21` | llm | **critical** | high | 1.21是K=5时的方差缩放值,属于实质统计断言。论文未声明任何可验证的数据来源（如JSON路径）,机械层无匹配,故判为 | increased 0.53 →0.82 →1.00 →1.12 →1.21 for K = 1 → |
| `0.021` | llm | **critical** | high | 0.021是经验B(K,γ)具体结果值,属实质断言；论文该处未声明来源,机械匹配亦无命中。 | With c0 = 0.05: B(3, 0.5) = 0.050, B(3, 1.0) = 0.0 |
| `5.2` | llm | **critical** | medium | 5.2× 以倍率形式表达,通常属结果/指标断言,不是版本号或阈值等噪音；机械匹配无命中,且原文未见产物 JSON 来源声 | 5.2× |
| `0.22` | mechanical | **supported** | high | 证据 2 位舍入 0.2247757194521495=0.2247757194521495→0.22 | 0.22 ± 0.04 |
| `10.3` | llm | **noise** | low | 仅出现10.3×,无上下文说明是结果或指标,可能为倍数/冗余标注；未能证明其为实质断言。 | 10.3× |
| `23.7` | llm | **critical** | medium | 23.7× 为倍数指标,属结果性实质断言；机械匹配无命中且未声明任何可追溯来源,故一票 critical。 | 23.7× |
| `10.6` | llm | **critical** | high | 10.6×为倍数型结果指标,属实质断言；机械匹配无对应且论文未声明来源,产物 JSON 无法支撑。 | 10.6× |
| `5.1` | llm | **critical** | high | 5.1×是明确的倍数型结果/指标,属于实质断言；机械匹配未命中,且论文未展示任何可追溯来源,按规则应判critical。 | 5.1× |
| `0.15` | mechanical | **supported** | high | 证据 2 位舍入 0.151=0.151→0.15 | 0.15 ± 0.03 |
| `11.2` | llm | **critical** | medium | 11.2× 为倍率型结果/统计量,属实质断言；机械层无任何 JSON 命中,且所给原文未见来源声明,按规则判 Criti | 11.2× |
| `33.7` | llm | **critical** | medium | 33.7× 为倍率型指标（如加速比/提升倍数）,属实质断言；产物 JSON 机械匹配无命中,且未见来源声明,按规则判 c | 33.7× |
| `29.5` | llm | **critical** | high | 29.5×是观察集上的P/B比值,属实质性能断言；论文未声明任何来源,机械层亦无匹配,故裁定critical。 | K=6 observation (γ=1.0): P=0.33, B=0.011, P/B=29.5 |
| `1.28` | llm | **critical** | medium | I=1.28 是观察结果指标（K=6, γ=1.0）,属实质断言；机械匹配无命中,论文未声明来源,故一票 Critica | K=6 observation (γ=1.0): P=0.33, B=0.011, P/B=29.5 |
| `3.33` | llm | **noise** | high | 3.33是理论公式1/ρ在ρ=0.3下的计算结果,属于派生中间量或理论阈值,非实验数据结果或统计指标,无需JSON支撑。 | The theoretical floor at ρ = 0.3 is I(∞) = 1/ρ = 3 |
| `0.09` | mechanical | **supported** | high | 证据 2 位舍入 0.0884=0.0884→0.09 | Increasing K at fixed γ=1.0 reduced P by ≈0.04 per |
| `16.8` | llm | **critical** | high | χ2=16.8是Friedman检验的统计量,属于实质断言；论文未声明数据来源,机械匹配无命中,且无法在证据JSON中找 | Cross-model comparison. Friedman test over 4 model |
| `1.52` | llm | **noise** | high | 1.52 是关键差异图中的临界差（CD）,属于统计检验阈值而非模型结果指标；按规则阈值/派生中间量归为噪音,无需在产物  | = 1.52 (Figure 2). No single model dominates overa |
| `51.55` | llm | **critical** | high | 51.55M 是摘要中模型参数量的核心对比指标,属于实质断言；机械匹配无命中,且未见来源声明,构成无来源关键数字。 | The Abstract 51.55M vs. 7.61B 0.68% figure separat |
| `7.61` | llm | **critical** | high | 7.61B是实质断言（模型参数量对比）,机械匹配无命中,论文未声明数据来源,属于无来源实质断言。 | The Abstract 51.55M vs. 7.61B 0.68% figure separat |
| `12.4` | llm | **noise** | high | 12.4 出现在 training GPU-hours 后,是训练算力成本/资源量,非结果指标。机械无命中符合成本类噪音 | The Abstract 51.55M vs. 7.61B 0.68% figure separat |
| `0.048` | llm | **critical** | high | 0.048 是 c0 经 leave-one-K-out CV 重拟合得到的实质统计量,非噪音；论文未声明其来源文件或路 | Refitting c0 via leave-one-K-out CV gives c0 = 0.0 |
| `0.052` | llm | **critical** | high | 该数字是留一K折交叉验证拟合 c0 的结果,属实质统计断言；论文仅给出数值,未声明可定位到产物 JSON 的来源,机械匹 | Refitting c0 via leave-one-K-out CV gives c0 = 0.0 |
| `4.8` | llm | **critical** | high | P/B 4.8-9.2× 是再拟合得到的实质统计量（区间下界）,非阈值/版本等噪音；论文未声明具体产物JSON来源,机械 | P/B 4.8-9.2×, showing looseness is structural not  |
| `9.2` | llm | **critical** | high | P/B 4.8-9.2× 是结果指标,非噪音；论文未声明来源文件,机械匹配无对应 JSON 值,属实质断言无来源。 | P/B 4.8-9.2×, showing looseness is structural |
| `1.26` | llm | **noise** | high | 1.26 为 requirements.txt 中 numpy 的版本号,属于环境依赖配置,非实质断言或统计结果。 | requirements.txt: numpy 1.26, scipy 1.11, matplo |
| `3.8` | llm | **noise** | high | 3.8是matplotlib版本号,属于环境依赖声明,非实质结果指标,机械匹配无命中属预期。 | scipy==1.11, matplotlib==3.8. |
| `57.3` | llm | **critical** | high | 57.3%为生产投资比例,是实质统计指标。机械层无匹配,论文仅引用外部PR#1300,未声明本地证据JSON路径,无来源 | 57.3% production-investment ratio cites LangChain  |
| `0.25` | mechanical | **supported** | high | 证据 2 位舍入 0.2514=0.2514→0.25 | 0.25 ± 0.04 |
| `10.0` | llm | **critical** | low | 数字 10.0× 出现四次,形式为倍数,可能代表性能指标或统计量,属于实质断言；机械层在产物 JSON 无匹配,且未见来 | 10.0× |
| `5.4` | llm | **critical** | high | 5.4×为结果倍数统计量,属实质断言；机械比对无命中,且原文未声明来源,无法追溯至证据 JSON。 | 5.4× |
| `11.4` | llm | **critical** | high | 11.4× 为倍数指标,属于实质断言。机械匹配无命中,且原文未声明来源,无法在证据 JSON 中验证,应判为无来源关键数 | 原文行:11.4× |

- 语义：noise=误报（非实质断言）；supported=实质断言且有来源；critical=实质断言无来源（一票 Critical）；未裁决=LLM 失败维持原判