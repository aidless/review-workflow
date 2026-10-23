# 对抗审查报告

- 时间: 2026-08-27T19:08:18.763600+00:00
- 源: F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f1\extracted_text.txt
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（3）
- - Critical: 将“置信度启动”作为单一处理归因，但仅比较一个特定信心提示文本与一个中性前缀，二者在祈使语气、情绪效价、任务难度断言、是否出现“confidence/correct”等多个语义维度上同时不同，长度匹配只能排除长度，不能排除其他语义混淆，也不能支持“语义而非长度”的因果结论。
- - Critical: 结果变量ΔMAE是置信度与正确率的联合函数；若信心提示同时改变答案选择或正确率，MAE变化可能来自准确率变化而非校准偏移，摘要中“不改变准确率”的假设未在方法/结果中验证。
- - Critical: 从4模型×3通道（可能还含3 seeds）中单独报告Qwen3:4b的p=1.6×10⁻⁵而未做多重比较校正；按n=500、MDE dz=0.18的效力计算只适用于单一预设检验，不能为事后挑选的最大效应背书。
### Major（5）
- - Major: 长度匹配的benign control只在子集上测试，p=0.62不能作为“无长度效应”的证据；需要同一子集上的置信区间/等价性检验，否则无法与全样本主结果比较。
- - Major: “语义 vs 长度”是错误二分法；语义内容包含多个可分离成分，需设置正交控制条件（如非信心的祈使句、负向信心句、去除“几乎总是正确”等）才能定位机制。
- - Major: 500道MMLU题的选择、分层和主题分布未说明；MMLU各主题内题目高度相关，按题目简单配对可能高估独立样本量，需报告抽样方式并使用聚类稳健推断。
- - Major: 3个seed的作用与样本独立性不明确：若同一题目×模型×通道在3个seed下重复，则每个单元存在重复测量，不能简单把n=500作为独立配对样本量。
- - Major: 四个post-hoc baselines在held-out benign数据上拟合后用于priming数据，面临分布偏移与多重检验问题；仅报告“p<.02”不足以说明“不能消除”，需给出CI或等价性界限。
### Minor（2）
- - Minor: 统计报告不一致：Wilcoxon W、Cohen’s dz、BCa bootstrap的关系未交代，也未报告bootstrap CI；对离散且有界的置信分数，dz与bootstrap的适用性需要说明。
- - Minor: “hypothesis-generating”与“power-justified”、p值推断的定位矛盾；探索性研究的p值应明确标记为未校正/描述性，或采用预设与探索两阶段报告。

## 统计（stat）— ok
### Critical（3）
- - Critical: 多重比较未控制：4 模型 ×3 通道（甚至更多事后通道）会产生至少 12 个主检验，摘要只突出 Qwen3:4b 的 p=1.6×10⁻⁵，未给出任何 FWER/FDR 校正或预注册规则，头条效应可能是挑选结果。
- - Critical: “语义作用而非长度作用”的结论基于“ priming 显著、control 不显著”两个 p 值比较，这在统计上不成立；必须直接检验 priming 与 length-control 的 ΔMAE 之差（difference-in-differences）或其交互项。
- - Critical: 3 个 seed 不是独立样本；若把 seed 当作额外样本量（6,000/12,000/36,000），有效样本被高估；Wilcoxon/bootstrap 也未采用按 question/model 分层的聚类方法，p 值可能虚假偏小。
### Major（5）
- - Major: 方差报告不足：只给 ΔMAE=+0.047 和 dz=0.42，未报告配对差分的 SD、95% CI、BCa 区间或置信区间宽度；B=5000 BCa 的存在但没有 CI 不可检验。
- - Major: 检验选择与模型结构不匹配：同一 500 题被多个模型/通道重复使用，各单元格的 Wilcoxon 假设 500 个独立差分解，忽略题目与模型的聚类相关，应使用混合效应模型或 cluster bootstrap。
- - Major: 控制条件在子集上检验且样本量/功效未说明；p=0.62 不能证明效应不存在，需提供 control 的置信区间或等价性检验，并报告其 n 与 MDE。
- - Major: 功效分析不完整：未报告 α、power、单双侧、Wilcoxon 功效或对多重比较/聚类的调整；MDE dz=0.18 仅对单一配对 t 检验成立，不能支撑整个 12 单元格协议。
- - Major: 事后 baselines “reduce but do not eliminate”没有伴随推断统计量（CI、置换检验或效应量），无法判断“仍存在”是否只是噪声。
### Minor（2）
- - Minor: 效应量 dz 未给出置信区间，且 0.047 的 MAE 变化是否实际部署相关未定义；建议同时报告 rank-biserial 或中位差。
- - Minor: MMLU 是固定题库而非随机抽样，对模型总体的统计推断需更明确地限定为“该题库/该批问题”的 superpopulation 假设。

## 实验（experiment）— ok
### Critical（3）
- - Critical: 主效应仅报告 Qwen3:4b 的单一指令信道结果，而完整设计包含 4 models×3 channels×2 conditions，至少 12 个可比检验；未做多重比较校正，存在选择性报告/假阳性风险。
- - Critical: 长度匹配良性对照只在子集上测试，主效应和对照不是同一题目/模型/信道集合；p=0.62 不能证明“长度无影响”，也可能只是子集功效不足，长度对照结论不成立。
- - Critical: 6,000 个配对差值来自相同的 500 题并跨模型/信道重复使用，若按单元而非题目/模型聚类做 Wilcoxon 检验，会严重夸大有效样本量；3 个 seed 也未说明是数据子采样、解码采样还是 bootstrap seed，伪重复问题未处理。
### Major（6）
- - Major: 没有对 priming 文本做成分消融（“容易”“几乎全对”“请给高置信”单独/组合），无法判断是哪个语义成分驱动置信度偏移。
- - Major: 长度控制不是长度×语义的完整因子设计：只有一个 75 字符良性前缀和一个 priming 短语，缺少多种长度、低置信/反向语义对照，不能严格分离语义与长度效应。
- - Major: 500 道 MMLU 题的选择方式未说明；未报告是否按学科分层或随机抽样，子集可能偏向某类任务，影响基准公平性和结论代表性。
- - Major: 四种 post-hoc baseline 的超参数（temperature、isotonic 分箱、ensemble 规模、judge prompt/temperature）未交代，也未做敏感性分析；此外“held-out benign data”是否按题目与测试题完全分离未说明，可能存在题目级泄漏。
- - Major: 泛化证据薄弱：只有 4 个小规模本地模型、单一 MMLU 子集、单一 phrasing、单一 cache 注入形式，且 verbalized confidence 只在 0.52–0.76 窄区间，无法支持对检索缓存场景的较广结论。
- - Major: 3 个 seed（42/43/44）不足以说明训练/采样/划分稳定性；未报告各 seed 的 ∆MAE、置信区间重叠或 seed 效应，也没有固定数据划分的 seed 管理方案。
### Minor（2）
- - Minor: “3 channels”始终未定义或未按 channel 分别报告结果；若指 system/prefix/user 等注入渠道，效应可能只在特定渠道成立，当前表述混淆。
- - Minor: 缺少“无前缀”或不带任何语义的纯长度基线，无法确认是 priming 语义本身而非任何额外上下文导致的偏移方向。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 核心 GAP 不成立：已有工作已系统研究“用提示/指令把 LLM 的 verbalized confidence 向乐观或保守方向引导”，例如 SteerConf (arXiv:2503.02863) 明确用 steering prompts 改变置信度并评估校准，FaR (arXiv:2402.17124) 也发现提示策略会诱发过度自信；把 cache entry 中的 confidence-priming 指令换成“检索到的 prompt 前缀”并不会产生新的科学机制。
- - Critical: “检索侧/缓存上下文被当作惰性内容”这一前提在文献中已不成立：间接 prompt injection、RAG 知识投毒、以及 NOVA (arXiv:2601.11004) 等 RAG 校准工作都证明检索内容可以携带可执行指令或噪声并影响答案/口头置信度；本文的 confidence-priming cache entry 是这些已知威胁的一个特例。
### Major（3）
- - Major: 声称“首次用 paired ΔMAE + length control 在 MMLU 上测量”只是把已有 benchmark、配对统计量和长度控制组合起来，是实验配置的增量，而非有意义的文献空白；calibration-prompt 对照实验（如 Xiong et al. 2023、Influences on LLM Calibration 等）已大量存在。
- - Major: Contribution 2 把 “descriptive Wasserstein upper bound” 列为贡献，但文中自述是 “sanity check, not explanatory theory”，这属于对贡献的夸大描述。
- - Major: Related Work 未引用最接近的 SteerConf、FaR、NOVA 等工作就直接断言 “no prior work measures…”，使 GAP 判断建立在缺失文献上；与这些工作对齐后，剩余增量主要是场景包装而非概念突破。
### Minor（1）
- - Minor: 摘要用 12,000 cells/6,000 paired 的总规模包装，但显著结果似乎只突出 Qwen3-4B 某个 channel；已有文献显示 prompt 对置信度的影响具有很强的模型/提示异质性，单模型亮点不足以支撑“缓存置信度风险”的普适贡献主张。

## 可复现（repro）— ok
### Critical（3）
- - Critical: 全文未提供任何代码仓库、数据工件或复现链接，12,000 个 cell、6,000 个配对差值、Fig.1 与补充实验均无法从外部对账，属于证据链断裂。
- - Critical: 未指定 MMLU 的具体版本/子集/抽样过程（original 还是 auxiliary、500 题如何抽取、是否固定题目顺序），问题子集不可唯一重建。
- - Critical: 未给出完整实验材料：confidence-priming 与 benign cache entry 的逐字模板、75-char neutral prefix 原文、题面/选项注入方式、“verbalized confidence”的解析规则，语义处理无法复现。
### Major（5）
- - Major: 仅列出 seeds 42/43/44，未说明 seed 控制哪些环节（MMLU 抽样、推理采样、bootstrap、校准拟合、基线划分），也未报告 3 个 seed 的独立结果，无法确认随机性已充分固定。
- - Major: 无配置快照：4 个本地模型族未完整列出，未给模型确切 checkpoint/量化/temperature/top_p/max_tokens/设备与依赖版本，Qwen3:4b 之外的模型结果也无对应表格。
- - Major: 无数据与模型许可说明：MMLU 及 Qwen 等模型的 license、再分发/研究使用条款、生成输出的许可均未声明，复现时存在许可不确定性。
- - Major: 无哈希对账：数据集、模型权重、prompt 模板、生成输出与中间统计量均无 checksum/SHA，无法核验“下载到的东西就是论文用的东西”。
- - Major: 统计流水线不可一键复现：B=5000 BCa bootstrap 未给原始 paired-difference 表、RNG 流与脚本；Wilcoxon W/p 的计算方式（exact/approx、有无 continuity correction）未说明；power/MDE 也无脚本。
### Minor（2）
- - Minor: 长度匹配对照组只在 subset 上运行，未给出该 subset 的大小、抽样规则与筛选条件，导致部分结论无法全量复现且易受子集选择影响。
- - Minor: 文档自身不完整/含截断与乱码（如“…(截断)”、Fig.1 和附录未提供），无法确认 500×3 phrasings pilot 与四个 baseline 的完整数据表。

## 写作（writing）— ok
### Critical（1）
- - Critical: 数字不一致：摘要/贡献写 500×4×3×2=12,000 cells、6,000 paired differences，正文却把功效分析写成“n=500, MDE dz=0.18 at n=500”；n 是问题数、单元数还是配对差异数没有交代，12 倍差异使统计声明无法核对。
### Major（4）
- - Major: 摘要与正文矛盾：摘要明确说长度匹配对照“control tested on a subset, see Limitations”，引言/贡献却称“paired protocol (n=500…) including a length-matched benign control”，未说明子集与 n=500 的关系。
- - Major: 术语未定义且指代不清：“3 channels”在摘要中从未解释，随后又用单数“The instruction channel”报告主结果；读者不知道是哪一条通道、其余两条通道结果如何。
- - Major: 术语/引文错误：Related Work 称 Naeini et al. (2015) “derive the Brier score and reliability diagrams”，Brier score 并非该文提出，reliability diagrams 也更早，这类事实性表述会损害可信度。
- - Major: 术语混用：摘要主结果使用 ∆MAE（verbalized-confidence error），引言却写“shift self-reported confidence and ECE”，标题又是“Confidence Shifts”；三者不是同一个量，正文未统一“结果变量到底是置信度本身还是校准误差”。
### Minor（5）
- - Minor: 结构/悬空参数：Abstract 罗列 B=5000 BCa bootstrap，但摘要和可见正文未报告任何 bootstrap 区间，读者无法判断该参数如何参与结论。
- - Minor: 结构：摘要把 Wilcoxon W、p、dz、B、图号等细节全部塞入，却未定义 3 channels、4 families、BCa，信息密度过高，可读性差。
- - Minor: 图表现：摘要用“see Fig. 1”指代长度对照结果，但可见正文/贡献未说明 Fig. 1 内容；若图在截断部分后应补充图题与坐标轴说明，否则无法验证 +0.005/p=0.62。
- - Minor: 数字一致性：摘要写“Four post-hoc baselines … p<.02”，但未给出各项 baseline 的具体 p 值或置信区间，无法判断是否四项都显著、是否经多重比较校正。
- - Minor: 结构/术语：贡献 #2 的“Wasserstein upper bound |∆MAE| ≤LΓ”符号未定义，且与摘要/正文其他部分没有对应展开，像是孤立贡献。

## 伦理（ethics）— ok
### Critical（1）
- - Critical: 论文直接给出可复制的“缓存条目置信度提升”提示（含医疗 RAG 示例）并展示其可系统性制造高置信错误输出，却未见 TMLR 要求的 Broader Impact Statement，也未讨论缓存投毒、医疗/金融等高风险场景的误用与缓解措施。
### Major（1）
- - Major: 未说明 MMLU 数据及所用模型/补充数据的许可证与归属；MMLU 为 MIT 许可，若随文发布 500 题子集或缓存提示样例，需保留版权和许可声明，当前提交中未见该合规说明。
### Minor（3）
- - Minor: 未明确声明数据来源是否包含真实用户缓存/日志；若使用在线 API（如 LLM-as-judge）或真实 RAG 缓存数据，应说明去标识化、同意机制与数据流向。
- - Minor: 双盲方面未见明显作者信息，但未声明补充材料/代码/数据已完成匿名化且未链接可识别作者身份的预印本；需同时清理 PDF/ZIP 元数据。
- - Minor: 未在可见文本中披露与 Qwen3 等模型厂商的资助或隶属关系；尽管 TMLR 通过 OpenReview 收集 COI，仍应确认不存在未披露的利益冲突。

## 汇总

- **Critical: 16 | Major: 29 | Minor: 17**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）