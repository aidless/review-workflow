# 对抗审查报告

- 时间: 2026-09-02T04:53:03.730369+00:00
- 源: F:\deepseek\papers\calibration-self-improvement\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— timeout
### Critical（3）
- - Critical: 核心结论“matcher determines calibration”建立在事后构造的 v2 matcher 上：matcher 是先看到 30 行 adjudication 结果后再扩展规则、并在同一 30 行上评分，因此 100%/ECE=0.0037 是 in-sample circular 结果，不具备独立验证的内部效度。
- - Critical: 标签金标准不独立：pilot 的 adjudicator 与被测 agent 同属 deepseek-v4-flash 家族，两个“独立实例”仍共享同一模型族的失败模式；judge noise 与 confidence/任务难度相关时，基于 soft-label 的估计和 Theorem 6 的 $\eta_j$ 假设不成立。
- - Critical: OOD-gating 因果推断不恰当：“confidence may be harmful”“consistency removes overconfident answers”基于 N=30、无 gold、无覆盖率/拒绝率匹配基线、门限事后选定且未做多重比较校正的观察相关；相关证据不能支持“有害”或“移除错误”的因果/干预断言。
### Major（6）
- - Major: 样本量被虚增：4999/1159 “dual-judged pairs”不是独立样本，同一批 MMLU items 被多个模型和判官重复使用；有效变异在 model×item 层聚类，不按 item/model 随机效应或 cluster-robust 推断会低估 CI 和 p 值。
- - Major: “calibration is domain-specific”混淆了多个变量：domain 同时改变题目难度、准确率、答案格式、matcher 一致性和 judge 难度；ECE 跨 domain 差异可能完全由 accuracy 或标签噪声驱动，不能单独归因于 calibration 本身。
- - Major: MSI “protocol-dependent”比较 (1.000 free-form vs. 0.334 MMLU) 同时混淆 language、domain、item format、模型集合和 N，不能把差异归因于 protocol 或 answer format。
- - Major: 前提未验证：论文假设 verbalized confidence 是可用概率，但未检验 JSON prompt 引导、格式遵守、confidence token 与模型内部概率的对齐；所有 ECE 只是该 elicitation 协议下的条件测量，不必然反映“agent 的 confidence”。
- - Major: 退化性结论被过度外推：pilot 并非完全退化（3/30 非 1.0），Proposition 8′ 只说明完全退化质量上的条件信息为零，不能推出整个 confidence-threshold gate “carries no information”。
- - Major: smECE_sem 在真实 pilot 上不可识别：只有 3 个不同 confidence 值，KDE/smoothness/bandwidth 假设无法从数据检验；其相对 binning ECE 的优势来自模拟假设，而非真实数据的稳健证据。
### Minor（1）
- - Minor: 任务采样是 convenience/seeded subsets（30/90/300/600，frontier 甚至 n=48、domain n=12），无抽样框和功效分析；多个关键 ECE/domain spread 都是宽 CI 内的点估计，只宜作为提示而非验证。

## 统计（stat）— ok
### Critical（2）
- - Critical: 用“per-row adjudication 后扩展的 matcher”重新判定标签，再在同一批数据上计算 100% accuracy / ECE=0.0037，属于标签构造与评估同源（in-sample/circular），该结果不能作为真实校准水平的估计，只能说明 matcher 可以“解释”全部数据。
- - Critical: 主 pilot 仅 N=30，且 27/30 的置信度恰为 1.0，有效非退化样本极少；任何 ECE、binning CI 以及“40–50% 高置信 OOD 错误”的百分比都极不稳定，未给这些比例的精确置信区间，不足以支撑“confidence may be harmful for gating”的结论。
### Major（5）
- - Major: 在退化分布上使用 binning ECE 本身不可靠：大量值绑定在 1.0，bin 边界/位置任意，0.363、0.1297 等 binning ECE 不应作为主要结果；应给出 binning-free 的 smECE 及其分布/CI。
- - Major: 跨域比较使用“up to 4×”这种比值效应量，在分母接近 0 时极不稳定；同时未报告每个 domain 的 ECE 点估计、CI 及重抽样方差，无法判断 0.45 的绝对差异是否显著且可重复。
- - Major: “only extreme Holm-corrected pairs significant” 暗示先看数据再挑“极端”配对检验；Holm 只校正了被检验的配对，不能校正从大量 domain-model-domain 组合中事后搜索/选择带来的多重比较膨胀，p 值可能被高估显著性。
- - Major: 缺少效应量与不确定性报告：显著差异只报 p 值/Holm，未报标准化效应量、绝对差异的 bootstrap CI 或方差；大样本下微小 ECE 差异也可“显著”，结论应基于效应量和 CI。
- - Major: OOD gating 的 N=30 探索性分析中，“confidence and consistency negatively correlated”“self-consistency removes overconfident OOD answers”没有给出相关强度、置信区间或正式检验；基于 3 个 resamples 的一致性信号在如此小样本下结论不宜超出定性描述。
### Minor（2）
- - Minor: 摘要中的 95% CI (88.4%, 100%) 未说明是 Clopper-Pearson/Wilson 还是 bootstrap，也未说明是“held-out”前还是后；该区间的统计性质和覆盖意义不明确。
- - Minor: MSI（1.000 vs 0.334）只给点估计，未给 bootstrap CI 或样本量，协议间差异的稳定性无法评估。

## 实验（experiment）— ok
### Critical（2）
- - Critical: 核心“adjudicated matcher”结果是在逐行 adjudication 后于同一批样本上测得的，matcher 已见过正确答案，in-sample 100%/ECE≈0.0037 是标签泄漏下的结果，不能作为“adjudication 后校准良好”的证据。
- - Critical: 缺少有效对照组：没有在同一数据上比较标准温度缩放、随机/固定置信度基线、无 matcher 变化的模型原生输出等对照，无法把 ECE 差异归因于 matcher 效应。
### Major（6）
- - Major: 消融不完整：只切换 matcher，未消融置信度提取 prompt、模型、领域、resample 温度/次数、MSI 阈值、self-consistency 信号等组件，无法定位“matcher-dependent”结论的来源。
- - Major: 基准公平性差：exact-string、tolerant、adjudicated 三种 matcher 不是预先固定的同一评分协议，tolerant/adjudicated 在看过模型输出甚至标签后构造，三个条件不对等，跨模型/跨 domain 比较也不公平。
- - Major: 超参数未受控：ECE 分箱数/分箱方式、温度缩放拟合数据、OOD gating 的置信度阈值、3 次 resample 的温度等均未报告选择标准或敏感性分析，存在对当前数据集调参嫌疑。
- - Major: Seed 管理缺失：N=30 pilot 和 3 次 resample 未报告随机 seed、重复次数、采样方差；若温度采样非确定性，单次结果无法与随机波动区分。
- - Major: 泛化证据不足：OOD gating 只是 exploratory N=30、无 held-out OOD、无干预/因果 claim；MMLU 与 free-form 的 MSI 差异 (1.000 vs 0.334) 未剥离任务格式、模型、领域等混淆变量，不能支持 deployment 层面结论。
- - Major: 统计功效与基准规模不匹配：600 items/9 models/4999 pairs 看似大，但关键校准结论仍建在极小 pilot 上，且 cross-domain 只有少数 Holm 校正后显著的 pair，大部分比较可能只是噪声。
### Minor（2）
- - Minor: 未处理 benchmark contamination：MMLU 可能已进入各模型预训练数据，未报告 contamination 检查，影响跨模型校准差异的公平性。
- - Minor: 结论范围与 scope 矛盾：论文承认 multi-step agentic 是 orthogonal，却给出 deployment gating 的 cautionary guidance，泛化到真实 agent 场景缺少实验支持。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 核心“matcher 决定校准”的 GAP 并不真实：已有工作已证明 reference+matcher 可反转校准排名（arXiv:2608.25654），且评估协议（答案槽、匹配字符串、置信读取方式）可系统性改变 ECE/AUROC 结论（arXiv:2605.27752），本文只是将该现象搬到 agent 场景，未拉开实质差异。
- - Critical: “per-row adjudication 后扩展 matcher 得到 100% accuracy 与 ECE≈0.0037”属于用正确性反推匹配规则的事后标签构造/循环论证，不能作为“校准由 matcher 决定”的独立证据，反而削弱 smECE_sem 的诊断可信度。
### Major（4）
- - Major: 语义 soft-label 估计器与 MSI 与已有 semantic calibration 框架高度重叠，例如 Sem-ECE（arXiv:2605.08432）已做语义聚类采样、证明估计量无偏并区分同/留出样本，本文未给出相对该框架的形式化差异、新理论保证或可控实验增益。
- - Major: 退化置信分布与 binning ECE 的不可靠性已被 Smooth ECE（arXiv:2309.12236）、ECE 估计偏差（arXiv:2012.08668）及退化 verbal confidence 工作（arXiv:2604.24070）广泛覆盖；“binning-free 指标”属于工程适配而非新概念贡献。
- - Major: 置信门控在退化分布下无信息、自一致性仍有判别力的 Proposition 8′ 是 consistency-based calibration（AAAI 2024, arXiv:2402.13904）和 conformal self-consistency gate（arXiv:2602.21368）中的成熟结论，N=30 探索性 OOD 分析不足以支撑“grounding an OOD-aware gating rule”的贡献表述。
- - Major: 跨域校准差异及温度缩放对标签/标注分布不鲁棒也已有专门研究（如 ambiguous ground truth、human label distributions 下的 temperature scaling gaps），且文中多数域对仅在 Holm 校正后极少数显著，经验增量似为描述性复现而非新机制。
### Minor（1）
- - Minor: 标题与贡献把“Pilot”与“600 items/9 models/4999 pairs”混用，同时 OOD-gating 仍只有 N=30，导致“expanded collection”与“grounding rule”之间的贡献幅度被夸大。

## 可复现（repro）— ok
### Critical（3）
- - Critical: 全文未给出代码/数据仓库或可访问的附录链接，声称“reproducible measurement pipeline”但证据链断裂，无法独立复算 63.3%/86.7%/100% 与 ECE 等核心数字。
- - Critical: 未报告任何随机种子：300/600 item 采样、OOD N=30 选择、3 次 resample、bootstrap CI、MSI 计算等随机步骤均不可精确重放。
- - Critical: 配置快照缺失：模型版本/API 调用日期、temperature、top_p、max_tokens、prompt 模板、system prompt、agent 工具集及依赖库版本均未列出，API 模型结果无法跨时间复现。
### Major（3）
- - Major: matcher 缺少精确、机器可执行的正式定义；“per-row adjudication 后扩展 matcher”未说明 adjudicator 身份、标注指南、是否盲评、一致性指标，且用 adjudication 后的标签反推 matcher 存在循环论证与标签事后漂移风险。
- - Major: 没有数据/预测/标注文件的哈希对账（如 SHA-256），也没有逐行输出文件，无法验证 4999 pairs 与 600 items 的对应关系，也无法排除选择性报告或部分重跑。
- - Major: 数据许可不透明：MMLU 子集、扩展六领域题项、模型输出、逐行 adjudication 标注是否可再分发/使用均未说明；附录 Compliance 未出现在可见文本中，无法核实。
### Minor（2）
- - Minor: “300/1159 pairs → 600/4999 pairs”的 items/pairs/domains/models 口径变化缺少映射表、排除准则和逐 domain 明细，统计细节（95% CI 方法、Holm 校正、MSI 1.000 vs 0.334）也未提供可执行代码。
- - Minor: 一键复现缺失：没有 README、Dockerfile、Makefile、依赖 lockfile 或最小命令路径，无法“下载数据→运行 pipeline→生成表格→核对哈希”一步完成。

## 写作（writing）— ok
### Major（7）
- - Major: 摘要用 “Pilot Measurement”/“illustrative N=30 pilot” 定位全文，却同时给出 600 items / 6 domains / 9 models / 4999 pairs 的扩展集合，正文定位与实证规模自相矛盾。
- - Major: 引言 “We use single-turn verbalized confidence as probe, agentic multi-step left to \S6 Discussion.” 缺谓语/系动词，是残句。
- - Major: 摘要 “An OOD-gating analysis (exploratory, N=30) suggests (exploratory, no causal claim, no intervention)” 重复 “exploratory”，且限定词堆叠，削弱可读性。
- - Major: 摘要后的中心句使用 $\mathrm{smECE}_{\mathrm{sem}}$，但摘要只定义了 semantic soft-label estimator 与 MSI，未定义 $\mathrm{smECE}_{\mathrm{sem}}$，术语前后不衔接。
- - Major: 摘要将 “100\% (ECE = 0.0037; in-sample on 30 rows, not a held-out)” 与 exact/tolerant matcher 并列，虽括号披露，但“非 hold-out”限定过弱，易被误读为三档 matcher 的公平比较。
- - Major: 摘要以 “Compliance in appendix (Section~\ref{sec:compliance}).” 结尾是孤立残句，且未说明 compliance 指什么，不适合放入摘要。
- - Major: 引言 “calibration ... is validated on the agent's task distribution before use in the exact form it is consumed” 语法不通，语义上也混淆了“在任务分布上验证”与“按实际消费形式验证”。
### Minor（4）
- - Minor: 数字与词形不统一：300/600/4 用阿拉伯数字，而 six/nine 用英文；ECE 小数位 0.363 / 0.1297 / 0.0037 不一致。
- - Minor: “varies up to $4\times$ ... and up to 0.45 absolute” 中 “absolute” 用法不完整（应为 in absolute value），且 across subjects 与 across six domains 的粒度关系未说明。
- - Minor: “MSI is protocol-dependent (1.000 free-form vs.\ 0.334 MMLU)” 比较项不对等：一边是格式 free-form，一边是基准 MMLU。
- - Minor: 可见摘录中没有任何图表引用，摘要大量关键数字缺少表格/图锚点，读者无法快速定位支撑证据。

## 伦理（ethics）— ok
### Critical（1）
- - Critical: 用“逐行裁决后扩展 matcher”得到的 100% 准确率/近零 ECE 是 in-sample 循环验证，即使摘要声明非 held-out，仍极易被下游引用为“校准问题已消失”并用于高后果门控，存在严重误用风险。
### Major（4）
- - Major: 数据许可不透明：MMLU 本身为 MIT，但 600 items/4999 pairs 模型输出、逐行裁决标签及任何派生数据集的再发布/商用必须逐项满足各模型 API ToS 与许可要求，可见稿只写 “Compliance in appendix”，未给出可核验的许可矩阵。
- - Major: 隐私与人类裁决者合规缺失：per-row adjudication 若涉及众包或人工标注，未说明标注者知情同意、报酬、数据去标识化与内部审查；若仅作者标注，也应明确声明数据不含个人/敏感信息。
- - Major: 利益冲突与资助未披露：评测九个模型未在正文说明 API/算力资助、模型厂商关联或 competing interests，TMLR 双盲流程仍要求作者在 OpenReview 或附录披露 COI，仅说 “in appendix” 不足以证明合规。
- - Major: 双盲匿名化风险：正文虽隐藏作者，但模型版本清单、API/日志路径、PDF 元数据及附录 compliance 中的机构信息都可能破坏 TMLR 双盲，需在提交前系统清理而非仅隐藏作者栏。
### Minor（1）
- - Minor: N=30 探索性 OOD-gating 结论被提炼为 “OOD-aware gating rule”，容易被安全/医疗等场景误当生产规则；应把“探索性、不可部署、需外部 held-out 验证”放进摘要和结论首句。

## 汇总

- **Critical: 13 | Major: 35 | Minor: 13**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）