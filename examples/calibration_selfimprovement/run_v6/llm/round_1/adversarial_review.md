# 对抗审查报告

- 时间: 2026-08-28T12:25:24.534767+00:00
- 源: F:\deepseek\papers\calibration-self-improvement\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（2）
- - Critical: 核心“matcher 决定测量到的校准”是在同一 30 行样本上轮换 matcher 得到的，并且“扩展 matcher”是根据这批样本逐行 adjudication 后构造的；用同一批数据既构造标签/规则又计算 accuracy/ECE 属于 in-sample circularity，100% 与 ECE=0.0037 是定义性结果，不能支持“过度自信信号消失”的实质结论。
- - Critical: N=30 且未说明样本抽样机制；若 30 行来自便利样本或事后挑选，27/30 置信度恰为 1.0 的退化分布可能只是选择偏差，导致“该任务分布上置信度退化”这一前提不成立。
### Major（7）
- - Major: matcher 的 tolerant/extended 规则与 adjudication 流程没有 held-out 或交叉验证；规则很可能是在看到数据后迭代出来的，内部效度受损，无法区分“真实校准改善”与“对同一批数据过拟合”。
- - Major: 语义 soft-label estimator 与 MSI 的假设未验证：谁判定语义正确、判定是否可复现、soft label 是否独立于模型置信度；若 soft label 仍来自同一 matcher，MSI 与原 matcher dependence 问题同源，不能作为独立诊断工具。
- - Major: Proposition 的形式化界依赖于未知 gold labels 下的 matcher FPR/FNR 等量，但这些量在无独立金标准时无法估计；且界可能隐含 matcher 错误与置信度独立的假设，而实际中高置信度答案的 matcher 错误率往往不同。
- - Major: 跨域 MMLU 比较存在混淆：域间差异同时包含模型组合、题目难度、accuracy、答案分布、prompt/template 和 matcher 差异；“ECE 最多差 0.45”可能主要反映 base rate/accuracy 差异而非校准差异，且大多数 Holm 校正后比较不显著，强结论证据不足。
- - Major: OOD gating 分析是 N=30 的探索性结果，却使用了“confidence 有害”“self-consistency 移除错误”的因果式表述；没有随机分配、无基线、无置信区间，且“两者负相关时”是事后子组，不能推断 gating 的因果收益。
- - Major: 存在大量未完全校正的多重比较/选择性报告：多种 matcher、多个指标、多个模型、多个域和阈值都被尝试，只报告“极端 Holm 显著对”不能视为确认性证据，更未提供预注册。
- - Major: 除一个循环 95% CI 外，主要结论（ECE 差异、MSI 的 protocol 差异、OOD gating 危害）均无不确定性量化；在 n=30 且置信度退化的条件下，即使 binning-free ECE 也有很高方差，点估计不可靠。
### Minor（2）
- - Minor: “温度缩放对 relabeling 不鲁棒”仅基于 30 行退化样本，未报告温度缩放的具体拟合/验证流程，结论被过度泛化。
- - Minor: Proposition 8' 依赖“置信度退化”假设；若在更大测试分布中置信度并非全部接近 1.0，则“阈值门无信息”的结论不能直接外推。

## 统计（stat）— ok
### Critical（2）
- - Critical: 核心 pilot 结论建立在 N=30 且 27/30 置信度恰为 1.0 的退化样本上，三种 matcher 的 ECE（0.363/0.1297/0.0037）均未给标准误或 bootstrap CI，无法判断差异是否只是抽样误差。
- - Critical: 100% accuracy / ECE=0.0037 来自 per-row adjudication 后在同一批 30 行上评估，属于 in-sample/circular 估计；该 95% CI 无频率学有效性，不能支持“校准问题消失”的结论。
### Major（4）
- - Major: 若 30/30 的 95% CI 确为 [0.4%,100%]，数值有误——Clopper-Pearson 下限应约 88.4%；除非明确说明 Bayesian 先验，否则该区间不可复现。
- - Major: MMLU 的 4999 pairs 由 600 items × 9 models 产生，同一 item/model 被重复使用，观测不独立；直接做 pair-level 检验会低估方差，需混合效应模型或聚类稳健标准误。
- - Major: 跨域比较仅写“只有极端 Holm 校正对显著”，未报告检验类型、比较总数、全部校正后 p 值及 ECE 差值的效应量与 CI，多重比较结果不可审计。
- - Major: 退化置信分布下只报 ECE 点估计和“up to 4×/0.45”范围，未报告 binning-free 估计的方差/bootstrap CI；比值型效应量在 ECE 接近 0 时不稳健。
### Minor（2）
- - Minor: OOD gating 的 40–50% 错误率来自 N=30 探索性分析，未给出高置信子集样本量、二项 CI 或检验，结论表述过强。
- - Minor: MSI 1.000 vs 0.334 未给置信区间或样本量，1.000 很可能由小样本/退化分布造成。

## 实验（experiment）— timeout
### Critical（4）
- - The tolerant matcher v2 was designed/iterated on the same 30 rows after seeing exact/v1 failures, then evaluated on same 30 rows. The 100% accuracy / ECE 0.0037 is in-sample and circular. Paper acknowledges "in-sample, single judge" but still uses it as central result. For experimental design, it'
- - Control group: there is no baseline model/task set with human labels or independent gold for the pilot? The 30 tasks have gold labels but no human baseline; "accuracy 100%" under adjudicated labels based on LLM judge not human gold: tasks are programmatic gold; adjudication judges model answer equ
- - Critical: v2 matcher 是在同一批 30 行上“先逐行裁定、再扩展规则、再在同一批上打分”的，100%/ECE=0.0037 是在样本循环验证，不能作为“语义正确即校准”的核心证据；跨模型 holdout 并不能修复该同分布、同 agent 的 in-sample 问题。
- - Critical: OOD Stage B 的 30 个“不可答”题目没有 gold 标签，却报告“高置信 OOD 答案错误率”和“consistency 门控移除 overconfident OOD answers”，实际只能计算高置信比例/代理指标，无法证明“错误”或“移除错误答案”。
### Major（9）
- - Control group: there is no baseline model/task set with human labels or independent gold for the pilot? The 30 tasks have gold labels but no human baseline; "accuracy 100%" under adjudicated labels based on LLM judge not human gold: tasks are programmatic gold; adjudication judges model answer equ
- - Ablation completeness: They compare exact vs v1 vs v2 matcher, but v2 combines matcher extension + per-row adjudication, not separated. They don't ablate whether the ECE drop to 0.0037 comes from extended matcher or adjudication (though they claim both). They have v1 tolerant then v2 extended+adju
- - They propose smECE_sem with soft labels; they compare to "hard" smECE and binning ECE, which is an ablation of soft vs hard labels and kernel smoothing vs binning. They report decomposition pooled: binning 0.235 -> smECE_hard 0.226 -> smECE_sem 0.181. But per-model not shown? Table shows per-model
- Key: OOD gating Stage B uses consistency computed as normalized string similarity (norm exact equality) of three temp 0.3 resamples, but no seeds set in `collect_ood.py` (body options temperature 0.3, no seed). So "three resamples" are not seeded; but that's okay for stochastic. However no seed mana
- - Major: 对 pilot 标签没有独立人工或跨家族 judge 控制组；deepseek 系模型既产出答案又裁定答案，同源失败模式未被排除，v2 的“语义正确”判定本身也可能继承被测模型的偏差。
- - Major: 消融不完整：exact→v1→v2 同时改变了 matcher 规则和 per-row adjudication，没有“只扩 matcher 不裁定”“只裁定不扩 matcher”的消融臂，无法把 ECE 从 0.363→0.0037 的效应归因到 matcher 还是 adjudication。
- - Major: three-arm calibration schedules 没有 no-calibration/no-evolution 对照组，三个 arm 各自独立 seed 和轨迹，且 A 的优势主要由 accuracy 驱动；即使声明 observational，放进 Results 仍会被误读为实验性排序。
- - Major: 超参数和 seed 管理不足：smECE 带宽 h=0.05 为固定值，OOS 温度折叠只用一个非分层 seed，temp>0 的 consistency resample 未设置 seed，采样鲁棒性仅 2 seeds，主结论仍基于单 seed 或未 seed 的生成。
- - Major: 基准公平/泛化不足：MMLU 比较将“free-form 中文”与“multiple-choice 英文”混淆为 protocol 差异，且 DeepSeek 缺失、Llama 仅 259/300、Qwen1.5 置信度退化；摘要宣称的 600 items/six domains/nine models/4999 pairs 在可见方法和证据中没有对应对照，Q4 本地小模型单 seed 也难以支持“universal”结论。
### Minor（2）
- - They propose smECE_sem with soft labels; they compare to "hard" smECE and binning ECE, which is an ablation of soft vs hard labels and kernel smoothing vs binning. They report decomposition pooled: binning 0.235 -> smECE_hard 0.226 -> smECE_sem 0.181. But per-model not shown? Table shows per-model
- - Minor: 跨域显著性表述不规范：摘要只提“Holm-corrected 仅极端对显著”，但未给出检验族、假设集、CI 和预注册；同一批数据上多次比较后仅少数极值显著，不应作为领域特异性的强证据。

## 新颖性（novelty）— ok
### Critical（1）
- - Critical: 核心主张“标签匹配器决定测量到的校准”并非新发现：arXiv:2605.27752（*Same Answer, Different Confidence: Protocol Sensitivity in LLM Calibration*）已通过替换 exact/containment matcher 展示同一模型与数据上 ECE、AUROC 和优劣排序随 correctness scorer 改变，并给出“prediction event”对齐框架；本文若仅将该现象改称 matcher dependence 并加软标签估计，则中心贡献与现有工作高度重叠且未明确差异化。
### Major（5）
- - Major: Propositions 1–3 的翻转率/不对称项上界本质上是对 label flip 下 accuracy 与 ECE 变化的初等概率分解；label noise 如何影响 calibration 已有系统研究（如 label-noise calibration 评测、label smoothing 分析），若未证明该界比已有结果更紧或导出新的非平凡结论，理论增量被夸大。
- - Major: smECE_sem 与 MSI 的“诊断工具”和已有 semantic-level calibration 工作重叠明显：如 semantic entropy、semantic-level reward（CSR）、semantic parsing calibration 均已在语义等价/软标签空间做校准或打分；MSI 只是把不同 matcher 的 ECE/accuracy 差异压缩成一个指数，未证明其比直接报告多个 matcher 的 scorer-sensitivity 表提供额外可操作信息。
- - Major: “binning-based ECE 在退化置信分布下不可靠”是成熟结论，Nixon et al. (2019)、Kumar et al. (2018)、Błasiok & Nakkiran (2024) 等已提出 binning-free/KDE/MMCE 等替代；把该 caution 列为贡献会夸大增量。
- - Major: Proposition 8' 在 confidence 全部为 1.0 时“阈值门无信息”是定义直接推出的平凡结果，而“self-consistency 比 self-reported confidence 更有判别力”已由 Kadavath et al. (2022)、Wang et al. (2024) 和 semantic entropy 等建立；以 N=30 的探索性 OOD 分析宣称“grounding an OOD-aware gating rule”属于过强主张。
- - Major: 第三 matcher 在 per-row adjudication 后达到 100% accuracy 使 ECE=0.0037 成为事后标签构造保证的伪结果；这与其说是“校准由 matcher 决定”的证据，不如说是“校准由事后选定的标签决定”，进一步削弱了中心实证贡献。
### Minor（2）
- - Minor: “跨域/MMLU 分科校准是 domain-specific”是 confirmatory 结论：subject-level calibration heterogeneity 与 MMLU 分科 ECE 变异性已有工作（如 *Understanding Calibration Evolution in LLMs*、*Subject-Level Calibration Heterogeneity*），且本文多数对比 Holm 校正后不显著，实证增量有限。
- - Minor: “agent 任务分布上的校准很少被验证”这一 GAP 不准确：已有 agentic/trajectory-level 置信度校准工作（如 *Agentic Confidence Calibration* / HTC）直接处理 agent 任务；本文又自我限定为 single-turn probe，所以真正填补的是单轮 QA 校准敏感度分析，而非所宣称的 agent 校准空白。

## 可复现（repro）— ok
### Critical（2）
- - Critical: 核心结论建立在“同一 30 行 in-sample 数据上逐行 adjudication 后扩展 matcher，再得到 100% / ECE 0.0037”的证据链上，这是循环论证；没有盲评、没有 held-out adjudication 集，也没有记录 adjudication 前后的判定差异，无法证明 matcher 泛化而非过拟合到这 30 行。
- - Critical: 所有随机/重采样环节均未给出 seed：3 次 resample 的自洽性、OOD N=30 的选取、bootstrap/95% CI、跨域子采样、模型生成等都没有固定随机种子，结果不可重现。
### Major（5）
- - Major: 配置快照严重不足：仅写“4 models/9 models”，未列出模型标识与版本、temperature/top_p/max_tokens、system prompt、置信度提取 parser、matcher 实现版本及参数，无法按原配置复跑。
- - Major: 数据许可与来源不完整：MMLU 具体版本、license、原始题目来源、模型输出与人工 adjudication 数据是否可再分发均未说明；“Compliance in appendix”在可核查材料中不可见。
- - Major: 无哈希对账：没有对原始 MMLU items、模型 raw outputs、matcher 判定、adjudication 记录和最终统计表提供 SHA-256 或等价校验，读者无法确认论文数字与数据文件一致。
- - Major: 没有一键复现：未见代码仓库、Docker/conda 环境锁、固定依赖版本、运行命令或输入/输出 artifact 下载地址，“reproducible measurement”声明缺乏可执行支撑。
- - Major: 样本量证据链不一致/损耗未解释：600 items × 9 models 最多 5400 pairs，却报告 4999 pairs，缺少的 401 条（解析失败/拒答/截断/排除）未给出逐项统计；300→600、1159→4999 的扩展规则也未说明。
### Minor（2）
- - Minor: 摘要中 CI 文本疑似损坏（`\.4\%,100\%\$`）；且若 30/30 正确的 95% CI 通常约为 88.4%–100%，转录/计算需核对。
- - Minor: MSI 1.000 与 0.334 等关键指标只给聚合值，未给出逐模型、逐域、free-form/MMLU 的 protocol 定义和计算中间量，外部无法独立对账。

## 写作（writing）— ok
### Critical（1）
- - Critical: 摘要中 `in-sample on 30 rows, circular 95\% CI \.4\%,100\%\$` 是损坏的 LaTeX，且 30/30 正确的 95% CI 下限不可能是 0.4%，该句既不可读又在数字上不成立。
### Major（4）
- - Major: 摘要宣称 “grounding an OOD-aware gating rule”，但同一摘要中的 OOD 分析仅为 exploratory、N=30，且结论是 confidence may be harmful，承诺强度与证据不匹配。
- - Major: 高亮句直接使用未定义的 `smECE_sem`，摘要只提到 “semantic soft-label estimator”，读者无法从摘要或可见正文得知该符号含义。
- - Major: 摘要引用 `Proposition~8$'$`，但贡献列表只提及 Propositions 1--3，中间编号及撇号来源未交代，命题编号体系不一致。
- - Major: 标题称 “Pilot Measurement”，摘要却给出 600 items、9 models、4999 pairs 的扩展实验和部署相关结论，“pilot” 与实验规模及结论强度相矛盾。
### Minor（4）
- - Minor: 摘要用 mean confidence 0.9963 对比 86.7% 说明 overconfidence，却未解释为何不选更极端的 63.3% exact-match 作为“alarming”基线，基线选择不一致。
- - Minor: 摘要混用 “subjects” 与 “domains” 且未定义二者层级关系，易让读者误以为它们是同一概念。
- - Minor: 可见文本中没有图表或图表引用，无法核验摘要中 0.363、0.1297、0.0037、MSI 等数字与图表的对应关系；如正文有图表需补查一致性。
- - Minor: 摘要堆叠过多数字并以 appendix compliance 收尾，结构上稀释了 “matcher determines calibration” 这一核心信息。

## 伦理（ethics）— ok
### Critical（1）
- - Critical: “扩展后 matcher 得到 100% / ECE 0.0037”这一核心警示数字来自 30 行上逐行裁定后的循环、样本内验证，没有独立验证集或预注册；该结果极易被下游误读为“校准已解决”并用于部署，构成最直接的误用/安全风险。
### Major（3）
- - Major: 可见材料未说明 MMLU 及派生集合（600 items/4999 pairs）的 MIT 许可与归属是否随数据和代码一并保留；若只抽取题目并重新分发，可能违反数据许可条件。
- - Major: 使用多个商业/专有模型 API 生成自我报告置信度时，未确认并披露各服务商 ToS 是否允许发布、再分发模型输出或用于研究评估，存在合规风险。
- - Major: 未披露资助、机构关系及潜在利益冲突，尤其是与模型/API 供应商的关系；匿名提交也应在合规附录中提供明确的 COI 声明。
### Minor（3）
- - Minor: MMLU 本身不含个人数据，但若 agent 调用链涉及工具日志或发布原始 prompts/outputs，应明确说明去标识化、PII 清洗和数据保护审查，当前未见。
- - Minor: 正文匿名方式本身合规，但代码、数据链接、模型名、致谢或附录元数据仍可能泄露作者身份；仅凭“Compliance in appendix”无法核验盲审安全。
- - Minor: 若“per-row adjudication”由人工完成，应报告标注者数量、判定规则、一致率及劳动/IRB 合规信息；当前缺失。

## 汇总

- **Critical: 13 | Major: 37 | Minor: 17**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）