# 对抗审查报告

- 时间: 2026-08-28T05:02:50.640468+00:00
- 源: F:\deepseek\papers\calibration-self-improvement\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（2）
- - Critical: 核心证据存在循环性：matcher 是在逐行人工裁决后才“扩展”到 100% 准确率，标签标准与模型输出并未独立，ECE≈0 很可能是测量构造而非模型校准改善，使“matcher 决定校准”沦为同义反复。
- - Critical: 中心结论基于 N=30 且其中 27 个置信度恰为 1.0 的退化样本，统计功效极低；从如此小的样本推出“校准由 matcher 决定”“OOD 门控有害”等一般性结论，内部效度不足。
### Major（5）
- - Major: 跨域结果中作者自述只有“极端的 Holm 校正后配对”显著，却仍以非显著的点估计差异（最高 4×、绝对 0.45）支撑“校准是领域特异的”结论，存在把噪声当效应的风险。
- - Major: OOD 门控分析是探索性 N=30，且“当 confidence 与 consistency 负相关时”是事后发现的条件性子组，可能是在结果变量上选择数据，无法作为因果或稳健的门控证据。
- - Major: free-form 与 MMLU 的 MSI 对比（1.000 vs 0.334）同时混淆了任务格式、题目领域、模型与采样协议，不能把差异归因于“protocol”本身。
- - Major: 用于界定 matcher 偏差边界的 FPR/FNR 若来自同一份人工裁决样本，则存在过拟合与乐观偏差；缺少留出标注集时，Proposition 给出的界不能直接视为经验界的保证。
- - Major: 人工逐行裁决未说明是否对模型答案盲审，也无 inter-annotator agreement；裁决者看到模型输出后可能偏向接受模型答案，从而抬高语义准确率并压低 ECE。
### Minor（2）
- - Minor: “在置信度退化时 confidence-threshold gate 不携带正确性信息”是从 30 个退化值推出的局部现象，可能由离散化/提示格式造成，不能外推到其他模型和题项。
- - Minor: self-consistency 仅用三次重采样，且未报告温度、采样次数、重采样相关性的敏感性分析；其“优于置信度”的结论缺乏因果识别和稳健性检验。

## 统计（stat）— ok
### Critical（3）
- - Critical: 核心 OOD 门控结论来自 N=30（且 27/30 个 confidence 恰为 1.0）；“40–50% 高置信答案错误”只对应约 12–15 个观测，未给精确计数和置信区间，样本量远不足以支持强结论。
- - Critical: 4999/1159 “pairs”不是独立样本：同一个 item 被多个模型回答、同一个模型贡献多条数据；若不按 item/model 做聚类 bootstrap 或混合模型，95% CI 会系统性过窄、p 值系统性偏小。
- - Critical: “per-row adjudication 后扩展 matcher”得到的 100% accuracy/近零 ECE 是数据驱动重定义标签后的结果，等价于用同一批数据同时选标签规则并评估，存在严重的选择偏差/过拟合，不能作为无偏校准估计。
### Major（5）
- - Major: 0.363 vs 0.1297 等 ECE 差异只给点估计，没有 bootstrap 方差、配对差值 CI 或检验；且这些 ECE 来自同一批输出被不同 matcher 重标，不是独立样本，不能按独立样本比较。
- - Major: “ECE 最多相差 4×”是误导性效应量：小 ECE 做分母会放大比率，应结合绝对差（如 0.45）和 CI 报告，并说明基线大小。
- - Major: “95% CIs; only extreme Holm-corrected pairs significant”存在多重比较与推断不一致：Holm 只校正 p 值未校正 CI，且未报告比较总数；不显著的 domain 对不能证明 ECE 相同，属 p 值误用/证据缺失当证据。
- - Major: MSI 1.000 vs 0.334 只报两个点估计，没有样本量、方差/CI、或统计检验；1.000 很可能是退化分布产物，不能直接解释为协议效应。
- - Major: 在 confidence 几乎全为 1.0 的退化样本上声称“confidence-threshold gate 无信息”主要是 range restriction/零方差伪影；不能从该样本外推阈值普遍无效，也不能用同一数据估计 confidence 与 consistency 的相关。
### Minor（3）
- - Minor: 摘要中的 ECE 未说明 bin 数、是否 adaptive、是否含最小样本量约束；在退化分布上 binning ECE 本身不可靠，应始终并列 binning-free 指标和不确定性。
- - Minor: 未报告各 domain/subject/model 的样本量是否均衡；domain-specific 差异可能混淆题目难度、模型构成与 domain 本身，不能只归因于校准属性。
- - Minor: 从前 300 items 到 expanded 600 items 的“pilot→扩展”分析未说明是否预注册、哪些假设是事后 HARKing；只报告“极端 Holm 显著”有选择性报告风险。

## 实验（experiment）— ok
### Critical（1）
- - Critical: 对照组缺失且存在标签泄漏：被扩展为 100% 的 matcher 是在同一批测试样本上逐行 adjudication 后构造的，实质是用测试标签调判决器，不是独立人工/预注册标签的公平对照，基于该 100% 结果计算的 ECE 不能支撑校准结论。
### Major（6）
- - Major: 消融不完整：没有分离“matcher 容错度”“语义打分器质量”“soft-label 阈值/语义相似度阈值”各自对 smECE 与 MSI 的贡献，也没有与现有 binning-free 校准指标（如量化/核密度估计）做替代方法消融。
- - Major: 基准公平性不足：未报告 MMLU 题目是否可能出现在模型预训练/指令微调数据中，无污染筛查或按时间切分；不同模型见过的 MMLU 数据分布不同，跨模型比较校准会被数据泄漏混淆。
- - Major: matcher 对比不公平：free-form 与 MMLU 两组协议在题目分布、答案格式、判定标准上不匹配，直接比较 MSI（1.000 vs 0.334）无法区分“matcher 敏感性”与“任务/标签格式差异”。
- - Major: 超参数报告不完整：未给出解码温度、top-p、max tokens、confidence 提示模板、bin 数量/边界、high-confidence 阈值、软标签阈值等关键设置，也没有对这些超参数做敏感性分析；尤其 ECE 的 bin 数选择会显著改变数值。
- - Major: seed 管理缺失：未报告采样/重采样种子，也没有用多 seed 或多独立重复估计解码随机性带来的方差；给出的 95% CI 看起来只反映样本间不确定性，不覆盖生成随机性。
- - Major: 泛化证据薄弱：OOD gating 分析只有 N=30，且仅来自 MMLU 派生设置，无法支撑“confidence 在 OOD 上有害/self-consistency 更优”的部署级结论；六个“domain”实际是 MMLU 科目子集，科目间题量、难度和先验概率不均，可能造成 ECE 差异被样本构成驱动。
### Minor（4）
- - Minor: 没有设置“不 adjudication 的独立人工标注基准”作为对照组，无法判断 tolerant matcher 与人工语义判定之间究竟差异多大。
- - Minor: 未报告每个 matcher/模型/domain 子集的样本量、每模型 item 数、每 domain 题目数，导致无法判断 ECE 差异是模型行为还是样本量噪声。
- - Minor: 没有消融 self-consistency 的重采样次数（当前固定为 3），也没有比较 1、5、10 次一致性信号对 gating 的稳定性。
- - Minor: 未说明“模型九种”的选取标准、是否覆盖不同系列/规模/训练数据，限制了跨模型结果的可推广性。

## 新颖性（novelty）— ok
### Critical（3）
- Need maybe look at exact "Unmatched Does Not Mean False" if it includes a closed-form criterion and exact decomposition, likely similar to bound. We can cite it as prior that already establishes matcher/label dependence and even reversal of calibration rankings, a stronger result than "measurement b
- - Critical: 核心贡献“measured calibration is determined by the label matcher”并非新发现——semantic parsing 中 exact-match vs. execution-accuracy 会改变 ECE/过拟合结论（Stengel-Eskin et al., TACL 2023），QA answer-equivalence 文献也早已指出 reference 覆盖不足会低估正确率；arXiv 2608.25654 已证明不完整 reference+matcher 可反转校准排名并给出 exact decomposi
- - Critical: “adjudication 后 100% 准确率、ECE≈0”基本是把模型输出重新判定为正确后换标签产生的测量恒等式，而不是关于模型置信度的新经验发现；用其作为“matcher 决定校准”的例证会把已知的评估协议敏感性包装成夸大贡献。
### Major（4）
- Need maybe look at exact "Unmatched Does Not Mean False" if it includes a closed-form criterion and exact decomposition, likely similar to bound. We can cite it as prior that already establishes matcher/label dependence and even reversal of calibration rankings, a stronger result than "measurement b
- - Major: 所提 `smECE_sem`+MSI 与现有工作高度重叠：arXiv 2605.08432 的 Sem-ECE 已用语义类别做采样并证明估计器无偏，arXiv 2511.04869 已把校准定义为由语义/等价类参数化的 B-calibration，arXiv 2603.14092 的 SMECE 已把 ECE 推广到软标签；论文没有给出相对这些方法的区分性理论或实验，增量看似只是已有组件的组合。
- - Major: 标题和摘要声称研究“agent confidence calibration”，但实验是单轮 MMLU/自由回答的标准 LLM 问答，未覆盖 agent 轨迹、工具调用或多步决策，也没有与 agentic uncertainty/selective agent 方法比较，因此“agent 自身任务分布上验证”的部署 GAP 未被真正检验。
- - Major: 跨域 MMLU 结论的增量被夸大：arXiv 2605.06673 已用 33 个模型、1500 条 MMLU、六域 verbalized confidence 证明 aggregate 指标掩盖稳定的域级差异；本文仅 9 模型/600 条，且只有极端 Holm 校正对显著，只能算小规模复现，不足以支撑“校准是 domain-specific”的新主张。
### Minor（1）
- - Minor: 退化置信度下 binning ECE 不可靠、温度缩放不鲁棒、self-consistency 比 verbalized confidence 有判别力均已有大量文献（Measuring Calibration in Deep Learning、Smooth ECE、Benchmarking Uncertainty Calibration 等），而 Proposition 8' 对“常值置信度⇒阈值无信息”几乎是定义直接推论；N=30 的 OOD 探索不足以支撑新的 gating rule。

## 可复现（repro）— ok
### Critical（5）
- - Critical: 核心度量依赖 matcher 与 per-row adjudication，但可见部分未给出 matcher 的版本化定义、伪代码和 adjudication 明细，无法从原始输出重算出 63.3%/86.7% 与对应 ECE。
- - Critical: 未报告任何随机 seed，包括 300/600 item 抽样、解码温度/采样、self-consistency 三次 resample、OOD N=30，抽样方差无法审计。
- - Critical: 无配置快照：模型名/checkpoint 版本、prompt 模板、解码超参、matcher 版本、依赖和运行环境均缺失，只有 “4/9 models” 等笼统描述。
- - Critical: 无一键复现：没有仓库/DOI/容器/顶层命令/README，4999 pairs 等全部数值无法独立重跑。
- - Critical: 无哈希对账：数据集快照、原始模型输出、标注/对账结果、代码与配置没有 SHA-256/manifest，无法确认评审者拿到的数据与作者一致。
### Major（2）
- - Major: 数据许可与模型条款仅声明“见附录”，当前提交物未展示 MMLU 许可、输出再分发条款或数据卡片，合规性不可审计。
- - Major: smECE_sem、MSI、Proposition 8'、OOD gating 与 “27/30 退化分布” 的计算脚本和原始证据在可见文本中缺失，结论的证据链不完整。
### Minor（1）
- - Minor: Python/库版本、模型权重哈希和数值结果对应的 artifact 索引均未固定，附录引用无法从当前提交物核验。

## 写作（writing）— timeout

## 伦理（ethics）— ok
### Critical（2）
- - Critical: 误用风险：论文面向“agent 用置信度门控行动/调用工具”的真实部署场景，但可见部分没有更广泛影响/危害分析；OOD 上 40–50% 高置信答案错误这一结果若被下游开发者直接用于自动决策，可能造成实质伤害，仅靠摘要中的 caution 不足。
- - Critical: 数据许可与模型条款：正文仅说“licenses, model terms, ethical compliance 见附录”，但未给出 MMLU 的具体版本/子集/许可、专有模型 API 使用条款、输出再分发许可以及 4999 条模型输出可否公开；审查者当前无法核实合规性。
### Major（3）
- - Major: 利益冲突：匿名双盲稿件未披露资助来源、模型厂商雇佣/咨询/股权关系；在评估九个模型时，若作者与任一被评模型厂商存在关联，MSI 与校准结论会产生无法被审查者评估的偏倚。
- - Major: 双盲：LaTeX 源码含 camera-ready、preprint、corresponding@example.com 等占位内容，若误用 `[preprint]` 选项、附带含作者元数据的代码/数据包，或指向含作者名的版本，都会破坏 TMLR 双盲要求。
- - Major: 隐私：正文未说明模型输入输出、置信度与三次重采样日志是否保存、共享、去标识化；MMLU 的医学/法律/伦理/人类性学等子任务可能涉及敏感话题，数据集卡本身也标注 Personal and Sensitive Information 待补充。
### Minor（2）
- - Minor: 数据许可：MMLU 本身是 MIT 许可，但论文未明确使用的是哪个 split/版本、是否包含 auxiliary_train 或其他拼接数据，也未给出可核验的许可保留与引用；附录缺失使该声明不可审计。
- - Minor: 双盲/合规：TMLR 要求作者在 OpenReview 提交 funding/competing interests/IRB 信息，但论文把合规完全推迟到不可见的附录，审稿人在双盲阶段无法验证是否存在隐藏的人类受试者或伦理审批需求。

## 汇总

- **Critical: 16 | Major: 25 | Minor: 13**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）