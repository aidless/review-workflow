# 对抗审查报告

- 时间: 2026-08-27T16:21:27.033272+00:00
- 源: F:\deepseek\papers\calibration-self-improvement\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（3）
- - Critical: 循环论证破坏内部效度——从 86.7% 到 100% 是"逐行 adjudication 残余错误后扩展 matcher"得到的，即用人工重判把语义正确答案纳入 ground truth 再测校准，matcher 变更与 ground truth 定义变更不可分离；把所有残余错误判为"语义正确"必然使准确率→100%、ECE→0，过自信信号消失是定义性而非实证结论。
- - Critical: 因果推断不当——"matcher determines measured calibration"把测量工具的选择（测量偏差）表述为因果决定；Propositions 1–3 的 bias bound 是测量误差界限而非因果效应，matcher 改变的是观测值不是被测属性，据此宣称"matcher 决定校准"属于把测量偏差误当成因果机制。
- - Critical: 同一退化样本自相矛盾——N=30 且 27/30=1.0 的同一组数据既用于论证 binning-based ECE 不可靠，又用于推断 OOD 门控（40–50% 高置信 OOD 错误）和自一致性有效；若分布退化到 ECE 失效，基于同分布的门控/一致性结论同样不成立，内部效度自我抵消。
### Major（5）
- - Major: 混淆变量未分离——86.7%→100% 同时叠加 matcher 容忍度放宽与逐行人工裁决，两者效应完全混杂，无法归因；"matcher 依赖"结论无法排除是 adjudication 主观性所致。
- - Major: 统计效力不足支撑倍数声称——cross-domain 称"4×–17× 变化"与"domain-specific"，但 95% CI 极宽（如 0.001–0.08 vs 0.30–0.60）且仅最极端域对 Holm 显著，基于点估计比值做倍数论断在如此宽 CI 下站不住。
- - Major: 模型能力作为混淆变量未控制——跨域 ECE 变异未排除不同模型在各学科能力差异，ECE 变化可能完全源自能力差而非"域特异性"，前提（域是主导因素）未验证。
- - Major: Proposition 8′ 前提过强——"退化使置信阈值门控无信息"仅在 27/30=1.0 这一特定退化模式成立；若剩余非 1.0 置信与错误相关，门控仍携信息，命题的普遍性假设未被其他退化模式检验。
- - Major: 选择偏差与可能的 OOD 循环定义——自一致性"对置信与一致性负相关的模型有效"是在 N=30 内按相关性条件筛选后声称有效，存在 data snooping；若 OOD 由高错误率事后界定，则为循环定义，因果方向无法确立。
### Minor（2）
- - Minor: MSI 1.000 vs 0.334 的差异可能来自任务形式（中文自由形式 vs MMLU 固定选项多选）而非"协议依赖"，混淆变量未控制。
- - Minor: "degeneracy 与 matcher-dependence reproduce"复现的其实是测量偏差产物，将测量伪影的重现当作实质发现的外部效度，论证错位。

## 统计（stat）— ok
### Critical（2）
- - Critical: N=30 且 27/30=1.0 的退化分布下，ECE 本身基于分箱已无统计意义，却报告到小数点后 4 位（0.0037、0.1297），制造虚假精度。
- - Critical: N=30 pilot 的全部核心量（accuracy 63.3%/86.7%/100%、ECE 0.363/0.1297/0.0037、mean confidence 0.9963）均无置信区间或方差报告；63.3% 即 19/30，其 95% CI 约 [45%, 79%]，与"结论"跨度极大。
### Major（6）
- - Major: Qwen2.5-7B ECE 的 95% CI [0.001, 0.08] 下界 0.001 在 n=30 退化数据上精度不合理；未说明 CI 构造方法（bootstrap？jackknife？），退化分布下 bootstrap 近似本身失效。
- - Major: 头条效应量"4× / 17×"是点估计之比，但文中自陈 95% CI 宽；比值比的 CI 未报告，且分母 0.028 的 CI [0.001, 0.08] 上界已是分子的 1/6，比值 CI 跨度可能达两个数量级。
- - Major: "Holm-corrected domain-pair p-values" 仅校正 6 域间 C(6,2)=15 对比较，但实际涉及 9 模型 × 6 域的矩阵式比较，跨模型与跨域交互的多重检验负担未被纳入校正范围。
- - Major: 4999 dual-judged pairs 未报告评判者间一致性（Cohen's κ / agreement rate）；matcher 本身是核心变量，标注可靠性直接决定下游 ECE 的效度。
- - Major: "40–50% of high-confidence OOD answers are wrong" 来自 N=30 探针中"高置信 OOD"子集，实际计数可能仅个位数到十几个，无 binomial CI，将该比例作为头条发现。
- - Major: confidence 与 consistency "negatively correlated (indicative, n=30)" 未报告相关系数 r、p 值或 r 的 CI；n=30 下弱相关的检测功效极低，"indicative" 无可验证含义。
### Minor（2）
- - Minor: MSI 1.000 vs 0.334 的跨数据集比较无 CI 或差异检验，无法判断是否显著。
- - Minor: accuracy 以百分比（63.3%）而非分数（19/30）报告，在 N=30 时掩盖了离散计数本质。

## 实验（experiment）— ok
### Critical（4）
- - Critical: 核心结论（ECE 值、OOD gating 有害性）建立在 N=30 样本上，calibration 估计方差极大；27/30 置信度退化为 1.0，意味着实际有效样本量远低于 30，任何 binning-based ECE 点估计（0.363、0.1297、0.0037）在统计上不可解释。
- - Critical: Matcher 升级路径是 exact→tolerant→per-row adjudication，第三级 matcher 是"逐行审查残差错误后扩展"的——这是对评测集的数据泄露/过拟合，100% accuracy 和 ECE=0.0037 不是泛化结果而是 in-sample fit，论文虽标注 "in-sample illustrative" 却仍将其作为核心数据点呈现。
- - Critical: 论文同时主张"binning-based ECE 在退化分布上不可靠"，却仍以 ECE 作为跨域比较的主指标（报告 4×、17× 的 ECE 比值），这是自我矛盾——如果 ECE 在退化分布上无效，那么所有基于 ECE 的跨域结论（包括 domain-specificity 主张）同样无效。
- - Critical: 4999 dual-judged pairs 的 inter-annotator agreement（Cohen's κ 或同类指标）完全未报告；论文的核心论点是 matcher 决定校准测量，但双标注一致性是 matcher 可靠性的基础，缺失则无法支撑"语义正确答案被识别"的可信度。
### Major（5）
- - Major: "ECE 跨域变化达 17×"是点估计比值，但作者自己承认 95% CI 极宽且 Holm 校正后仅最极端对显著——这意味着绝大多数声称的 domain-specific 变异在统计上不成立，标题级数字具有误导性。
- - Major: 自一致性信号仅用 3 次 resample 的 agreement，未报告采样温度、生成参数、seed 管理策略；3 次采样的 agreement 估计方差极大，且"confidence 与 consistency 负相关的模型"具体是哪几个模型、相关系数多少、多少模型满足该条件均未说明——选择性报告风险高。
- - Major: 无独立对照组/基准方法：引入 smECE_sem + MSI 但未与已有校准度量（如 Brier score、log loss、sweepECE）做公平比较；temperature scaling 被断言"对 relabeling 不稳健"但未展示任何实际 temperature-scaling 实验的拟合细节与失败分析。
- - Major: 600 items / 6 domains / 9 models ≈ 每 domain 每模型 ~11 条样本，per-cell 样本量极小；OOD gating 结论仅基于 30-item probe 的 40–50% 错误率，该比例的 Wilson 区间宽度约 ±18%，无法支撑"useless—even harmful"的定性判断。
- - Major: OOD 未被形式化定义——是退化输入？是分布外域？是特定 subject？OOD 与 degeneracy 在文中混用，无法区分"confidence 在 OOD 上失效"与"confidence 在退化分布上失效"这两个不同机制。
### Minor（3）
- - Minor: 消融缺失：未对 resample 次数（为何 3 次而非 5/10）、ECE bin 数量、MSI 阈值选择做敏感性消融；这些超参数的选择依据未说明。
- - Minor: 跨域 census 声称"九模型跨五家族"但未报告模型选择标准（为何这 9 个？是否覆盖规模/指令调优阶段的多样性？），generalization 边界不清。
- - Minor: 中文 free-form set 的 MSI=1.000 vs MMLU MCQ 的 MSI=0.334 被作为"protocol-dependent"证据，但两套数据集在语言、任务格式、样本量上同时变化，无法归因于 protocol 差异——存在混淆变量。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 核心 GAP 不真实：论文宣称“matcher determines measured calibration”是新发现，但已有工作 *Same Answer, Different Confidence: Protocol Sensitivity in LLM Calibration*（arXiv:2605.27752）已系统证明正确性打分/答案形式/协议变化会改变 ECE 与 AUROC 的结论，甚至翻转信号优劣，且 verbalized confidence 也随可接受答案表述变化；*Trained on Tokens, Calibrated on Concepts
- - Critical: 提出的 smECE_sem/MSI 与已有语义校准估计器高度重叠：*A Semantic-Sampling Framework for Evaluating Calibration in Open-Ended Question Answering*（arXiv:2605.08432）已提出基于语义等价类的 Sem-ECE 及统计无偏性理论；*Trained on Tokens...* 也已提出语义置信校准。本文的“语义软标签校准估计器 + matcher sensitivity index”更像重命名或增量变体，摘要未给出与 Sem-ECE / B-calibratio
### Major（3）
- - Major: “置信度退化时 threshold gate 无信息”的 Proposition 8′ 是平凡推论：若 27/30 个置信度恰为 1.0，任何阈值门在该样本内当然无法区分对错；将其包装为“formal basis”和贡献高估了难度与新颖性。
- - Major: N=30 的“扩展 matcher 到 100% accuracy / ECE=0.0037”是循环论证式构造：先按行 adjudication 把剩余错误重新标注为正确，再宣称 overconfidence 消失，只能说明标签可以改变测量，不能支撑“校准由 matcher 决定”作为经验发现的强度；摘要又把 600×9 census 作为 external validity，但自述置信区间很宽且多数域间差异不显著，使该增量贡献显得虚高。
- - Major: 形式化界 `|FNR·p−FPR(1−p)|` 属于标签噪声下二分类校准偏差的初等代数，并未与已有 label-noise/calibration-bias 文献（如 ECE 的 binning bias、错误标注下的 calibration 分析）区分；作为 Proposition 1–3 的新理论贡献证据不足。
### Minor（1）
- - Minor: 论文没有与“protocol sensitivity”类工作的可比较实验（如同答案/同标签/多 matcher 下的 ECE/AUROC 翻转率），也没有验证 MSI 相对现有语义校准指标是否提供额外信息，导致“方法论贡献”缺乏定位。

## 可复现（repro）— ok
### Critical（3）
- - Critical: 证据链断裂：摘要给出 63.3%/86.7%/100% 与 ECE 0.363/0.1297/0.0037，但未提供原始模型输出、matcher 判定中间结果、逐行 adjudication 记录或可审计日志，无法由同一输入重算出这些数字。
- - Critical: 三个 label matcher 仅以“exact / first tolerant / extended after per-row adjudication”描述，未给出匹配函数、代码、阈值或等价判据；扩展 matcher 依赖人工裁决，核心测量不可复现。
- - Critical: 未报告任何随机种子与采样配置：三次 resample 的 self-consistency、OOD 30-item probe、600-item × 9-model census 均缺少 temperature、top_p、max_tokens、模型版本/API 日期、系统提示词与推理框架版本，LLM 非确定性下无法复现。
### Major（5）
- - Major: 无环境/配置快照：没有依赖 lockfile、推理框架与量化配置、checkpoint commit/hash、GPU/API 版本，无法构建 one-click 复现环境。
- - Major: 数据许可与获取条件未说明：MMLU 子集、中文 free-form 集、OOD probe 及 4999 条 dual-judged 数据未注明来源、版本、许可或再分发限制，评审者无法合法获取同一数据。
- - Major: 无哈希对账：未提供数据文件 SHA-256、代码仓库 commit hash、artifact DOI 或对账脚本，无法确认论文数字对应哪一版数据与代码。
- - Major: 外部效度 census 的统计细节不足：只给出少数点估计和个别 95% CI，未给出 9 模型 × 6 域完整 ECE 表、bootstrap 种子与方法、Holm 校正的原始 p 值矩阵及每 domain/item 数。
- - Major: 没有 one-click 复现入口：未提供 repo/README/容器配置/流水线脚本，也没有从 prompt → 模型输出 → matcher → ECE/MSI 的端到端自动化流程。
### Minor（2）
- - Minor: 人工 adjudication 与 dual-judged 过程缺少 inter-annotator agreement、判定指南和 judge 模型/版本/提示词，扩展 matcher 后处理步骤无法独立复核。
- - Minor: 关键指标缺乏精确定义与代码级实现：MSI、smECE_sem、matcher flip rate/FNR/FPR 未给出公式或可执行定义，1.000 与 0.334 等数值无法重算。

## 写作（writing）— ok
### Critical（2）
- - Critical: 摘要对 N=30 pilot 的定位自相矛盾：前文称其为方法学研究的 illustrative example，后文又将其描述为 external-validity demonstration；同时“English MMLU ... expanded to 600 items across six domains”没有说明 300→600 与六个 domain 的包含关系，外部效度规模无法对账。
- - Critical: 将“per-row adjudication 后的 100% (ECE=0.0037)”表述为第三个 matcher 的结果并据此宣称 overconfidence 消失，这在写作上构成标签泄漏/循环论证：那是重标注后的 oracle 天花板，不是可推广的 matcher 测量。
### Major（4）
- - Major: Keywords 与 Introduction 之间孤立出现 “Our central finding is that...” 一句，既不属于摘要也不属于任何章节，破坏论文结构。
- - Major: 摘要单段塞入 N=30、63.3%/86.7%/100%、0.363/0.1297/0.0037、300/600/1159/4999、Proposition 1–3 与 8′、MSI 1.000/0.334、Qwen 的 CI 等大量细节，信息密度过高，摘要应有的层次缺失。
- - Major: 术语不一致或未定义：`smECE_sem` 在核心句中首次出现但未展开，`FNR/FPR`、`dual-judged pairs`、`first tolerant matcher` 均未在摘要中定义，读者无法独立理解关键结论。
- - Major: “600-item × 9-model census”（隐含 5400 个 item-model cell）与“4999 dual-judged pairs”没有对账，无法判断是过滤、缺失还是两种计数口径。
### Minor（4）
- - Minor: 样本量记号不统一：摘要中 N=30 与 n=30 混用。
- - Minor: `Proposition~8$'$` 的编号写法不符合常规命题编号习惯，且摘要未解释为何从 1–3 跳到 8′。
- - Minor: “40–50% of high-confidence OOD answers are wrong in our 30-item probe” 未给出 high-confidence 子集的实际分子/分母，n=30 下范围表述过宽且难以核实。
- - Minor: 可见部分没有图/表可核验；若正文含图表，摘要未交叉引用关键 ECE 对比表，无法确认图表编号、数值与正文一致。

## 伦理（ethics）— ok
### Critical（2）
- - Critical: 未说明 MMLU 600 项子集、跨域数据及中文自由格式数据的来源版本与许可证，也未说明是否允许二次分发/发布模型输出与逐行标注，存在数据许可与版权合规风险。
- - Critical: 论文涉及大规模人工双盲评判/整合判读（4999 dual-judged pairs），但未报告 IRB/伦理审批、标注者知情同意、报酬标准、任务说明或数据保存期限，可能违反人类参与研究与劳动伦理要求。
### Major（3）
- - Major: 未提供利益冲突与资助声明；若作者与模型厂商、API 供应商或众包平台存在经济/雇佣关系，将影响结果可信度并违反 TMLR 披露要求。
- - Major: 双盲审查完整性未声明；需要确认代码、数据、补充材料、日志和 PDF 元数据中不含作者身份/机构/邮箱线索，否则可能破坏匿名评审。
- - Major: “匹配器扩展至 100%” 的方法可被滥用于事后挑选匹配器以宣称低 ECE；缺少预注册、全部匹配器变体报告或明确反 cherry-picking 约束，构成误用风险。
### Minor（2）
- - Minor: 若中文自由格式或跨域数据包含真实用户生成内容，需说明 PII 去除/匿名化、删除策略和重发布限制；当前仅依赖基准数据不足以覆盖隐私合规。
- - Minor: N=30 的“illustrative”结论和点估计比值容易被下游部署者误读为已验证边界，可能促成不安全的 deferral/memory-gating 决策，需更醒目地限定适用范围。

## 汇总

- **Critical: 18 | Major: 31 | Minor: 16**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）