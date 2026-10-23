# 对抗审查报告

- 时间: 2026-09-02T04:37:14.109942+00:00
- 源: F:\deepseek\papers\calibration-self-improvement\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（2）
- - Critical: 核心证据在样本内（N=30）且标签是“逐行 adjudication 后扩展 matcher”产生的，等于用待评估模型的输出反推正确标签，存在直接循环性；100%/ECE≈0.0037 不能支持“matcher 决定校准”这一中心结论。
- - Critical: “overconfidence signal vanishes once semantically-correct answers are recognized”是因果式表述，但语义 matcher 没有独立金标准验证、没有盲法、没有标注者间一致性；宽松 matcher 可能把错误答案判对，机械地降低 ECE 而不代表真实校准改善。
### Major（5）
- - Major: N=30 且 27/30 置信度为 1.0，有效样本量极小；不同 matcher 的 ECE/准确率差异缺乏可靠的不确定性量化，宽 CI 虽被承认，仍被用于推断“matcher-dependent results”和“domain-specific calibration”。
- - Major: Propositions 1–3 的界限依赖 FNR/FPR 已知且可能假设 matcher 错误与模型置信度独立；若这些量从同一批 adjudicated 数据估计则循环，若不独立则偏差界不成立，文中未检验或做敏感性分析。
- - Major: 跨域 MMLU 比较混淆了领域、模型、题目难度、提示格式和每域样本量；“domain-specific”“free-form vs MMLU”的 ECE/MSI 差异不能归因于单一协议或领域因素。
- - Major: OOD gating 分析（N=30，探索性，无干预）使用了“self-consistency removes overconfident OOD answers”的因果性语言；高置信 OOD 错误与一致性负相关可能只是领域偏移程度、题目难度或采样噪声的混淆，并非一致性“移除”了过度自信。
- - Major: “Temperature scaling 对 relabeling 不稳健”基于退化分布和极小样本，未见独立的训练/验证/测试划分或重复 relabeling 的稳定性检验，不能支撑该稳健性结论。
### Minor（3）
- - Minor: 将 verbalized confidence 直接当作概率并计算 ECE 的前提未论证；未说明置信度文本如何解析、是否映射到数值概率。
- - Minor: 大量领域/模型/协议的成对比较多为事后探索，Holm 校正只覆盖极端配对，剩余比较仍存在多重比较问题，头版结论“calibration is domain-specific”被过度陈述。
- - Minor: Proposition 8′ 在退化置信度下是接近平凡的结论；而“self-consistency retains discriminative power”依赖重采样假设，缺少 AUC/C-statistic 及置信区间等判别力证据。

## 统计（stat）— ok
### Critical（2）
- - Critical: 核心校准结论建立在 N=30 的 pilot 上，而 “扩展 matcher 后 100% accuracy / ECE=0.0037” 是对同一 30 行逐行 adjudication 后的 in-sample 结果，无 held-out 或交叉验证，属于循环论证，不能作为 matcher 效应的统计证据。
- - Critical: MMLU 的 4999 个 “pairs” 并非独立样本：同一 item 被多模型、多次采样重复使用，按 pair 数计算 ECE/CI/p 值会严重低估方差；应使用 item/model 聚类稳健标准误或混合效应模型。
### Major（4）
- - Major: 三个 matcher 的 ECE 点估计 0.363 / 0.1297 / 0.0037 均未报告 bootstrap 或置信区间，在 N=30 和 27/30 退化分布下，三者差异可能完全落在噪声范围内。
- - Major: OOD gating 分析 N=30，只报 “40–50% high-confidence OOD answers wrong”，未给出精确分子/分母、二项 CI 或检验；例如 12/30 与 15/30 的 95% CI 高度重叠，不足以支持 “confidence may be harmful”。
- - Major: “single-model ECE varies up to 4×” 使用倍率作为效应量具有误导性：ECE 有界且接近 0 时倍率极不稳定；应报告绝对差、方向和逐对比 CI，并区分 Holm 校正后显著与不显著的对子。
- - Major: MSI 的 1.000 vs 0.334 没有方差、CI 或显著性检验，且 1.000 在小样本/退化置信分布下可能只是天花板效应，不能直接解释为协议差异。
### Minor（2）
- - Minor: “temperature scaling is not robust to relabeling” 未提供任何定量证据（如拟合后 ECE、交叉验证结果或重标记扰动分布），目前更像断言而非统计结论。
- - Minor: “40–50% of high-confidence OOD answers wrong” 属于探索性多重比较中的事后百分比，未做形式化二项检验或探索性多重性校正，容易产生选择性报告。

## 实验（experiment）— ok
### Critical（2）
- - Critical: 30 行 pilot 的“adjudicated matcher”在逐行人工裁定后用同一批 30 行评估得到 100%/ECE=0.0037，是典型 in-sample/circular 实验，不能作为 matcher 有效的证据，更不能支持“overconfidence 消失”的结论。
- - Critical: 缺少任何受控的 held-out 对照：没有把 exact/tolerant/adjudicated 三个 matcher 统一在留出集或交叉验证上比较，也没有随机/固定规则/human-label 作为 baseline，无法区分“语义正确识别”与“过拟合 pilot 行”的贡献。
### Major（7）
- - Major: 消融不完整：MSI、smECE_sem、软标签、self-consistency、threshold gate 等核心组件没有逐一移除/替换的消融，也没有与 Brier score、原始 ECE、普通 self-consistency 等 baseline 做对照，不能证明每个组件都必要。
- - Major: 基准公平性不足：MMLU 跨 domain 比较、free-form 与 MMLU 的 MSI 比较被题目难度、答案格式、subject 构成、每 domain/模型样本量、模型版本和 prompt 差异混淆，不能把 ECE 差异直接归因为 calibration 的 domain specificity。
- - Major: 超参数管理缺失：ECE bin 数、temperature scaling 拟合/验证方式、self-consistency 的采样温度与 resample 数（3 次）、OOD 判定阈值等均未报告或做敏感性分析，“temperature scaling 不鲁棒”可能是超参选择 artifact。
- - Major: seed 管理缺失：MMLU 子采样、模型 decoding、self-consistency 重采样、OOD 30 行子集均未说明 seed 或重复次数；在 27/30 置信度=1.0 的退化分布上没有任何跨 seed 方差/稳定性检验。
- - Major: 泛化证据不足：OOD-gating 是 N=30 的 exploratory 分析，没有独立 OOD 集、多个 OOD 分布或外部任务验证，却用于“grounding OOD-aware gating rule”，严重超出数据支持范围。
- - Major: gating 实验缺少对照组：没有 random gating、always-defer、no-confidence、consistency-only、confidence+consistency 组合等对照，也没有干预/反事实设计，“confidence harmful”与“self-consistency removes wrong answers”缺乏可比基线。
- - Major: 人工 adjudication 本身没有过程控制：未报告标注者数量、盲法、重复标注一致性或预注册规则，逐行扩展 matcher 易引入主观偏差，使三个 matcher 对比不是公平实验。
### Minor（3）
- - Minor: 统计功效不足：600 items/4999 pairs 分散到 6 domains×9 models 后每 cell 可能很小，且只有极端 Holm 校正 pair 显著，说明跨 domain 差异主要受噪声限制，4×/0.45 绝对差异不宜作为稳健结论。
- - Minor: 没有记录模型、数据集版本、prompt 模板、解码参数和采样seed 等完整复现配置，且 N=30 pilot 的任何数值（63.3%、86.7%、0.363、0.1297）都不应作为可泛化的测量值。
- - Minor: self-consistency 仅 3 次 resample，未证明该数量稳定，也未报告不同 resample 数下的判别力变化，导致“优于 confidence”的结论受实现细节影响。

## 新颖性（novelty）— ok
### Critical（7）
- - Critical: 核心发现被既有工作覆盖 (cited).
- - Critical: 新度量/估计量是已有工作的重命名/微小泛化 (SMECE, Sem-ECE, binning-free ECE), no comparison/positioning.
- Need choose severity. The user wants "每行一条 `- {severity}: 问题描述`（severity 为 Critical|Major|Minor）". We can have multiple Critical. But "Critical" should be severe novel issues. I'd assign:
- 1 Critical: Central "matcher determines calibration" claim not novel due to prior works (2608.25654 etc). If paper cites them, it must differentiate; if not, omission. This is direct contribution attack.
- 2 Critical: Semantic soft-label + binning-free + MSI contribution is incremental/overclaimed; existing SMECE/Sem-ECE/Smooth ECE cover much of it; no head-to-head.
- Let's produce final answer with exact format. Use "建议: 一句话修复" at end. No extra.</think>- Critical: 核心主张“matcher 决定测量到的 calibration”并非新 GAP；已有工作（arXiv:2608.25654 显示有限参考集+matcher 能反转 calibration ranking；arXiv:2605.27752 显示打分字符串/答案槽/读出方式都会改变 ECE 结论；arXiv:2210.16133 显示人类分歧下按多数标签校准本身有问题）已覆盖该现象，论文未说明自己相对这
- - Critical: “binning-free 语义 soft-label 估计量 + MSI”的增量被夸大；SMECE（arXiv:2603.14092）已把 ECE 推广到概率/软标签，Sem-ECE（arXiv:2605.08432）已用语义分组做开放问答 calibration，且 binning-free/Smooth ECE/KDE calibration error 是成熟方向，论文没有与这些方法进行必要对比或消融。
### Major（10）
- - Major: 形式化 Propositions 1-3 and 8' are near-tautological / simple label-noise algebra; no meaningful theorem.
- - Major: N=30 pilot used for OOD gating claims, not a real GAP; exploratory and no held-out; claims of "caution" may be okay but contribution exaggerated.
- - Major: Cross-domain empirical results (domain-specific ECE) already known and no new insight; Holm correction says few significant differences, so "varies up to 4x" may be unstable.
- Need choose severity. The user wants "每行一条 `- {severity}: 问题描述`（severity 为 Critical|Major|Minor）". We can have multiple Critical. But "Critical" should be severe novel issues. I'd assign:
- 3 Major: Theoretical propositions are trivial; matcher flip-rate bound is standard label-noise sensitivity; Prop 8' under degeneracy is tautological.
- 4 Major: Empirical "GAP" is not real: self-consistency as uncertainty signal and OOD gating are established; N=30 exploratory insufficient to support "grounding an OOD-aware gating rule".
- 5 Major: The cross-domain dataset and MSI protocol differences are observational; not enough to substantiate a "new phenomenon"; significance is weak (only extreme Holm-corrected pairs significant).
- - Major: Propositions 1–3 的 FNR/FPR 界更像 label-noise/relabeling 下 ECE 敏感性的标准代数结果，而 Proposition 8’（置信度全为 1 时阈值无判别力）在 27/30 个值为 1.0 的条件下近乎同义反复，不足以支撑“formal account”或“新理论”的贡献表达。
- - Major: OOD-gating 贡献的 GAP 不真实；self-consistency 作为不确定性/选择性预测信号已被广泛建立（如 arXiv:2602.11619、self-consistency 相关工作、UniCR），而本文仅用 N=30 探索性数据就声称“grounding an OOD-aware gating rule”，样本量与因果宣称不匹配。
- - Major: “domain-specific ECE”属于已知且宽泛的实证现象，且作者自述只有极端 Holm 校正对显著，因此“ECE 变化达 4×/0.45”更像不稳定点估计，不等价于新发现，无法支撑作为独立贡献。
### Minor（5）
- - Minor: Adjudicated matcher yields 100% accuracy "in-sample circular" and thus the headline ECE 0.0037 is definitional artifact; not a contribution.
- - Maybe Minor: "temperature scaling not robust to relabeling" already in prior work (Temperature Scaling Is Not Enough / Confidence Calibration under Ambiguous Ground Truth) so it shouldn't be listed as main finding.
- Need choose severity. The user wants "每行一条 `- {severity}: 问题描述`（severity 为 Critical|Major|Minor）". We can have multiple Critical. But "Critical" should be severe novel issues. I'd assign:
- 6 Minor: The in-sample adjudication 100% result is circular and shouldn't be used as evidence; but perhaps it's acknowledged, so minor.
- - Minor: 延后 per-row adjudication 得到 100% accuracy/ECE=0.0037 的“消失的 overconfidence”是循环定义产物；虽在摘要中标注 in-sample/circular，仍不宜作为衡量 matcher 影响的中心证据。

## 可复现（repro）— ok
### Critical（5）
- - Critical: 证据链断裂：30/300/600 行的 item ID、每个 agent 的原始置信度、三类 matcher 的逐行标签/判决结果均未作为可审计 artifact 发布，63.3%/86.7%/100% 和 ECE 无法对账。
- - Critical: 配置快照缺失：模型名/版本、API 或本地权重、温度、top-p、max tokens、prompt template 均未锁定，重跑无法稳定复现置信度分布。
- - Critical: 数据许可与来源不完备：未说明 MMLU 的具体 subset/版本、600 项到六个 domain 的映射、数据再分发许可及模型输出许可。
- - Critical: 无一键复现：没有 repo/commit、Docker/requirements 锁定、Makefile 或运行入口，第三方无法按原样重建结果。
- - Critical: 哈希对账缺失：原始数据、中间置信度、逐行 adjudication 结果未提供 SHA-256 哈希或版本化记录，无法证明报告数字来自同一份数据。
### Major（4）
- - Major: seed 缺失：自洽性 “three resamples”、OOD 采样和任何 bootstrap CI 的随机种子/采样协议均未给出，结果不可重现。
- - Major: adjudication 协议未定义：谁标注、判定标准、是否盲审、独立/多人标注及一致性未报告，“per-row adjudication” 后的 100% 标签不可复现且循环。
- - Major: matcher 定义与代码缺失：exact/tolerant/extended matcher 的判定规则、smECE_sem 和 MSI 的公式/伪代码/实现链接均未提供。
- - Major: 统计细节不足：95% CI 的计算方法（Clopper-Pearson/bootstrap 等）、bootstrap 次数、Holm 校正对应的检验集合未说明。
### Minor（1）
- - Minor: 正文引用的 Propositions 1–3、8' 和附录均无永久版本化链接或页码，截断/审阅版本无法核验完整证明与合规内容。

## 写作（writing）— ok
### Critical（1）
- - Critical: 摘要先说“binning-based ECE 不可靠”，随后又用“single-model ECE varies up to 4× / 0.45 absolute”作为跨域结论，却不说明后者是否已改用 binning-free 指标，造成摘要内部方法与证据的表面矛盾。
### Major（4）
- - Major: 摘要中 95% CI 写成 `\$88.4\%,100\%\$`，在 LaTeX 中会渲染成字面美元符而非区间，且缺少方括号，属于数字/排版错误。
- - Major: 数字精度不统一：准确率 63.3%、86.7%、100%，ECE 0.363、0.1297、0.0037，MSI 1.000 与 0.334，以及“0.45 absolute”的位数和量纲均不一致。
- - Major: “$\mathrm{smECE}_{\mathrm{sem}}$+MSI”在摘要后的 central finding 中首次出现，但摘要只定义了 MSI，未定义 `smECE_sem`，术语跳变。
- - Major: 摘要先说“calibration is domain-specific”，随后又说“only extreme Holm-corrected pairs significant”，多数配对差异并不显著时，结论强度与统计证据不匹配。
### Minor（6）
- - Minor: 摘要结构过载，一个段落同时塞入 pilot 结果、MMLU 扩展、OOD 分析、方法论建议和结论，主次不清。
- - Minor: OOD 句连续出现两个“exploratory”，且“removes overconfident OOD answers”表述含糊，未说清是过滤答案还是消除错误。
- - Minor: 数据规模从“300 items, 4 models, 1159 pairs”扩展到“600 items, nine models, 4999 pairs”，600×9=5400 不等于 4999，未说明排除原因，读者无法核对。
- - Minor: pilot 的 N=30 与 OOD-analysis 的 N=30 未说明是否为同一批样本，两个 N=30 易混淆。
- - Minor: 可见部分没有任何图表引用；如果正文有图/表，应在对应结果处引用；若没有，则 CI、4×、0.45 等数字缺少可视化支撑。
- - Minor: “agentic multi-step left to \S6 Discussion” 与前面的 `Section~\ref{sec:compliance}` 引用风格不统一。

## 伦理（ethics）— ok
### Critical（1）
- - Critical: 未提供 MMLU 及衍生“pairs”的数据许可与模型输出再分发条款；若附录未明确 benchmark license 和 API/模型 ToS，可复现数据/代码包存在侵权与合规风险。
### Major（4）
- - Major: 未见隐私、IRB 或知情同意说明；“per-row adjudication”若涉及人工标注，未说明标注者同意、补偿、去标识化及数据保护；若纯自动也需明示不涉及个人数据。
- - Major: 利益冲突与资助/机构关联未披露；特别是作者若与模型厂商、API 提供商或所提 matcher/gating 方法有商业利益，匿名评审不能替代独立 COI 声明。
- - Major: 双盲风险：附录、数据或代码元数据可能泄露作者身份、模型厂商、API 账户或 funding 信息；提交前需对全部材料做去匿名扫描。
- - Major: 误用风险：N=30 的探索性 OOD gating 结果被表述为“grounding an OOD-aware gating rule”，可能被误读为部署安全依据；需明确“不构成生产环境安全保证、不得单独用于高风险门控”的限定。
### Minor（2）
- - Minor: 人工 adjudication 若由作者本人完成，存在评估者利益与确认偏误风险；应报告盲法、独立双人标注、分歧裁决或至少说明为何不适用。
- - Minor: “Compliance in appendix”在本可见版本中不可验证，无法确认许可、隐私、COI 等声明确实存在且完整。

## 汇总

- **Critical: 20 | Major: 38 | Minor: 22**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）