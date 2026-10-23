# 对抗审查报告

- 时间: 2026-08-28T04:18:43.487139+00:00
- 源: F:\deepseek\papers\calibration-self-improvement\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（1）
- - Critical: 用同一批数据逐行裁决后再扩展 matcher，再用该 matcher 回算 100% accuracy / ECE 0.0037，标签构造与评估不独立，属于事后拟合/循环验证；据此得出“overconfidence 消失”的结论不成立。
### Major（5）
- - Major: 主分析 N=30 且置信度 27/30 为 1.0，退化分布下 ECE 的 0.363/0.1297/0.0037 只是极不稳定点估计，缺少 CI、bootstrap 或敏感性分析，无法区分 matcher 效应与抽样噪声。
- - Major: 跨 domain/model 比较 ECE 时未控制准确率、领域难度、答案分布和样本量差异；ECE 本身依赖 marginal accuracy 与 confidence 分布，因此“domain-specific calibration”可能只是任务难度或准确率的伪影，不能直接归因于模型校准。
- - Major: 4999 pairs 来自 600 items × 9 models，同一 item 被多个模型重复评估，观测非独立；若按独立样本计算 95% CI，区间会系统性过窄，Holm 校正也只能处理多重比较，不能处理 item-level 相关性。
- - Major: OOD gating 的“confidence may be harmful”是因果性表述，但只有 N=30 的探索性相关统计，无随机门控基线、无混淆变量控制（domain、model、难度、采样温度），无法支持“confidence 有害”的因果结论。
- - Major: self-consistency “retains discriminative power”未报告判别力统计检验、阈值选择依据、三次 resample 的独立性与采样条件，N=30 不足以排除偶然性，也不能证明其优于 confidence。
### Minor（3）
- - Minor: MSI 在 free-form 与 MMLU 间的 1.000 vs 0.334 混淆了任务格式、领域、答案空间和样本来源，不能仅归因于“protocol-dependent”。
- - Minor: 论文假设不同模型自报 confidence 是可比概率标度，但未说明 verbalized confidence 的 prompt、格式和温度是否一致；不一致时跨模型校准比较缺少内部效度。
- - Minor: “matcher 决定测量结果”的 formal bound 可能只是标签翻转的代数恒等式，未说明该 bound 在何种真实标注噪声/裁决误差下可辨识，导致理论贡献与实证结论之间的假设链条不完整。

## 统计（stat）— ok
### Critical（2）
- - Critical: 核心结论建立在 N=30 的 in-sample 数据上，且 “extended matcher after per-row adjudication” 用模型输出逐行修正标签后再计算 100%/ECE，标签已泄漏进测量，无 held-out/交叉验证，无法支持可推广的校准结论。
- - Critical: 30 个样本中有 27 个置信度恰为 1.0，分布已退化，却仍把 ECE 报到 0.363/0.1297/0.0037 四位小数，且未给 bootstrap CI 或方差估计；这些点估计本身不可靠，不应作为核心证据。
### Major（5）
- - Major: 4999 pairs 来自 600 items×9 models 的重复测量，不能按独立样本处理；未使用 item/model 随机效应或聚类稳健标准误，样本量被高估、方差被低估。
- - Major: 跨域差异只报告“up to 4×”“0.45 absolute”和“仅极端 Holm 显著”，未给出比较总数、检验方法、原始/校正 p 值以及 ECE 差异的 CI；非极端差异不显著时不能宣称 domain-specific 普遍成立。
- - Major: OOD gating N=30 中 40–50% 的置信区间约 ±18 个百分点，且 confidence 与 consistency “负相关”未报告相关系数、p 值或 bootstrap CI，不能支撑 “confidence harmful” 和 “consistency removes overconfident” 的结论。
- - Major: MSI 1.000 vs 0.334 只有点估计，无样本量、不确定性区间或重抽样结果，protocol 差异的统计意义无法评估。
- - Major: “confidence-threshold gate carries no information” 与 “self-consistency retains discriminative power” 未报告区分度指标（如 AUC）、95% CI 或与随机水平的比较，且基于 N=30，结论强度远超证据。
### Minor（2）
- - Minor: 未报告每个 domain/subject 的样本量和对应 ECE 的 CI；“up to 4×”在分母接近 0 时极不稳定，应主要报告绝对差异及区间。
- - Minor: 100% accuracy/ECE 0.0037 等极端值未说明基于 30/30，单一样本翻转即可大幅改变结果，需报告敏感性。

## 实验（experiment）— ok
### Critical（2）
- - Critical: 没有独立控制组/验证集：matcher 是在同一批评估样本上“逐行裁定后扩展”的，随后又用同一批样本报告 100% 准确率与 ECE=0.0037，存在标签泄漏/对评估集过拟合，不能作为公平的 matcher 对比。
- - Critical: 实验设计缺少先验固定规则：从 exact、tolerant 到 extended matcher 属于事后逐步放宽判定标准，没有把 adjudication 规则预先锁定在训练/开发集上，导致精度提升可能只是阈值搜索过拟合。
### Major（5）
- - Major: 消融不完整：MSI、semantic soft-label estimator、binning-free ECE、一致性门控等核心组件没有逐一消融，也未测试不同语义相似度阈值或不同 binning-free 估计器，无法判断哪些成分驱动结论。
- - Major: 基准不公平：free-form 与 MMLU 的 MSI 直接比较（1.000 vs 0.334）混淆了任务格式、答案分布和评估协议差异；跨域 MMLU 也未说明各域题数、模型覆盖是否均衡（4999 pairs 与 600×9=5400 不匹配，缺失样本机制不明）。
- - Major: 超参数管理不足：未报告 temperature、采样次数、ECE bin 数量、温度缩放拟合/验证流程、语义匹配阈值、一致性判定阈值等关键超参，且没有做敏感性分析；论文一边警告 binning ECE 不可靠，一边仍用 ECE 作为跨域主结果。
- - Major: seed 管理不足：OOD gating 的 N=30 没有固定抽样 seed、多 seed 重复或置信区间，也没有说明模型解码随机性和 resample seed 控制，结论无法验证稳定性。
- - Major: 泛化证据不足：OOD 分析仅 30 条 exploratory 样本，且跨域结论仅来自 MMLU 单一 benchmark，不能支撑“部署门控应改用 consistency”的一般性结论。
### Minor（3）
- - Minor: OOD gating 缺少对照基线：没有与不动用 confidence 的 random gate、always-defer/never-defer gate，或仅 consistency 的受控条件比较，无法证明 consistency gate 有增量收益。
- - Minor: 多重比较与功效不足：跨域比较只有“极端 Holm-corrected pairs”显著，未先验设定样本量或功效分析，多数配对差异不显著却被解读为 domain-specific。
- - Minor: 模型/数据代表性不完整：九模型、六域、600 题的集合未说明模型版本、训练数据重叠和领域难度匹配，难以排除模型能力差异对 ECE/MSI 的混淆。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 核心 GAP 并不真实：校准本来就依赖“什么算正确/标签定义”，LLM 评估中 exact-match vs semantic-match 对 accuracy 与 ECE 的影响已有大量文献；本文用 pilot 数据把“matcher 决定测量结果”当作新发现，属于已知现象的再确认。
- - Critical: Proposition 8′ 近乎恒真且是已知结论：若 27/30 个置信度恒为 1.0，任何置信度阈值门控自然无判别信息；self-consistency 能筛选正确样本也已是广泛研究的机制。把这一平凡观察形式化并用于“grounding an OOD-aware gating rule”显著夸大了理论增量。
### Major（4）
- - Major: Propositions 1–3 的 matcher 偏差界只是标签噪声/混淆矩阵的基本代数（FNR、FPR 与先验的线性组合），未与现有 label-noise calibration、semantic equivalence evaluation 或 calibration under noisy labels 的理论对比，形式化贡献被高估。
- - Major: smECE_sem 与 MSI 没有与既有 binning-free 校准量（Brier score、log loss、KDE/adaptive ECE、reliability diagram 等）做差异化和基线比较，无法判断是“新估计器”还是已有度量的特例/重命名。
- - Major: 跨域结论被自身统计结果削弱：95% CIs 与 Holm 校正后仅极端配对显著，且 MSI 在 1.000 与 0.334 之间变化更像协议敏感性而非模型固有校准属性；数据收集本身不构成方法论贡献。
- - Major: OOD-gating 的“grounding”仅来自 N=30 的探索性分析，并依赖“confidence 与 consistency 负相关”的条件子集，且未与已有 OOD detection/self-consistency gating 基线对比，40–50% 的区间不足以支撑部署规则结论。
### Minor（1）
- - Minor: “adjudication 后 100% 准确 / ECE=0.0037”虽是 in-sample illustrative，但用模型输出参与逐行重标签后作为 matcher 结果展示仍有循环论证风险，应只作为 sanity check 而非证据。

## 可复现（repro）— ok
### Critical（4）
- - Critical: 未给出任何随机种子或采样代码，300/600 items 的抽取、N=30 OOD 子样本以及 self-consistency 的 “three resamples” 无法重算；小样本下 ECE/准确率对抽样极敏感，核心数字不可复现。
- - Critical: “matcher extended after per-row adjudication” 的判定规则、adjudicator 身份、逐行台账和仲裁标准均未提供；用 adjudication 结果反推 matcher 再评估同一批答案会导致标签泄漏/循环，100% accuracy 与 ECE 0.0037 不可复现。
- - Critical: “four models”“nine models” 未给出具体模型名称、权重版本/API snapshot 或日期；不同 checkpoint/API 版本下 confidence 分布和 ECE 可能完全不同，无法复现或对账。
- - Critical: 未提供代码仓库、commit hash、Docker/环境快照、一键复现脚本或 artifact DOI；论文声称 reproducible measurement 但无法端到端重跑。
### Major（6）
- - Major: 未报告解码配置：temperature、top_p、max_tokens、采样次数、是否 greedy；这些直接决定 “exactly 1.0” 的退化分布和 self-consistency 结果。
- - Major: 没有 pair-level 原始输出、confidence 数值矩阵或数据文件，也没有 SHA-256/commit 哈希可做数据与产出对账；证据链无法闭合。
- - Major: 数据许可与模型条款仅声称在附录，但可见产出中缺少具体许可证名称、URL、版本和再分发条款；MMLU 子集及模型输出转存合规性未核验。
- - Major: “cross-domain MMLU collection” 未说明 MMLU 版本、split、题目 ID、domain 定义和 300→600 扩展方式，4999 pairs 的生成过程也未记录。
- - Major: 95% CI、Holm 校正和 MSI 没有统计软件/包版本与计算代码；未见 model×domain 明细表，无法对 “up to 4×” 和 “0.45 absolute” 做独立核验。
- - Major: OOD 定义、N=30 的采样边界、负相关判定标准、gating 阈值网格和 self-consistency 实现未定义，探索性 gating 结论不可复现。
### Minor（2）
- - Minor: Propositions 1–3 与 8′ 的完整陈述、前提和证明未在提供内容中给出，理论推导链无法验证。
- - Minor: 未报告 adjudication 的标注者间一致性、仲裁人数或复现入口；即使附录有合规声明，也需要具体路径供审查者访问原始台账。

## 写作（writing）— timeout
### Critical（2）
- - Critical: 摘要将“40–50% 的高置信 OOD 答案错误”归因于“exploratory, N=30”的 OOD-gating 分析，但正文明确这 30 条 unanswerable 项没有 gold label，40–50% 来自另一处有标签扩展（60 项、分母 10）或跨域 MMLU 的 OOD fold，数据来源与摘要矛盾。
- - Critical: 正文/图注声称 ECE 跨 subject 最多约 $4\times$，但 Table~\ref{tab:census} 中 Qwen2.5-1.5B 为 $0.041$ vs $0.410\approx10\times$；Figure~\ref{fig:census_domains} 的 caption 还把 $0.410$ vs $0.041$ 写成“roughly $4\times$”，属数字错误。
### Major（6）
- - Major: 摘要把“300 items/3 subjects 的 $4\times$”和“600 items/six domains 的 up to 0.45 absolute”并置在同一句“expanded … shows”之下，而正文扩展部分报告 Qwen2.5-7B 为 $17.1\times$ 且明确说“far above the ${\sim}4\times$”，新旧样本数混用造成摘要与正文不一致。
- - Major: 摘要称“MSI is protocol-dependent (1.000 free-form vs.\ 0.334 MMLU)”，但正文承认该比较同时混淆 protocol、language、domain、item format，称为“protocol-dependent”是对混杂比较的过度简化。
- - Major: 摘要断言“95\% CIs; only extreme Holm-corrected pairs significant”，但对应 Table~\ref{tab:sig600} 与 Section~\ref{sec:significance} 既没有 CI 列也没有 p 值或哪些 pair 显著的说明，表格无法支撑摘要中的显著性表述。
- - Major: 摘要先用 binning-based ECE（0.363/0.1297/0.0037）作为核心数字，随即又说该退化分布上 binning-based ECE unreliable；正文 Limitations 也称这些 pilot ECE 仅 illustrative、应以 binning-free 诊断为主，摘要的呈现顺序自相矛盾。
- - Major: 正文存在编辑残片：第 675–676 行“Its value is transparency---it reports $\eta_j$ … see human adjudication). behaves on real degenerate data. The MSI has …”，其中“behaves on real degenerate data.”是孤立残句。
- - Major: Limitations 仍把 census extension 写成 N=300、3 subjects、4 local open-weight models，与正文新增的 600 items/six domains/nine models/4999 pairs 冲突。
### Minor（5）
- - Minor: Keywords 之后、Introduction 之前出现无标签的“Our central finding is that …”独立段落，不属于 abstract 也不是 section，结构上像未清理的插入批注。
- - Minor: “We use single-turn verbalized confidence as probe, agentic multi-step left to \S6 Discussion”缺冠词/谓语，且与前文“multi-step agentic metrics are orthogonal”在范围表述上含糊乃至冲突。
- - Minor: 摘要使用“Proposition~8$'$”但未解释 prime 记号；该命题证明仅在“consistency covaries with correctness”条件下才保证 consistency 有判别力，摘要缺少该条件限定。
- - Minor: MSI 在摘要/300-item 部分为 0.334，而 Table~\ref{tab:sig600} 的 600-item 扩展为 0.330，未标注样本口径差异。
- - Minor: Table~\ref{tab:gating} 只有 gated hi-conf 值，没有原始 hi-conf 列，正文“high-confidence rate does not fall”等判断无法从表直接核对；脚注中支撑 40–50% 的分母仅 10，摘要却将其作为稳健结论陈述。

## 伦理（ethics）— ok
### Major（6）
- - Major: 合规附录仅被正文一句“stated in appendix”带过，当前审阅材料未提供可核验的数据许可证清单，无法确认 MMLU 及扩展数据集的再分发/派生条款是否合规。
- - Major: 未逐项列出 9 个模型的许可与服务条款；商业模型 API 常限制输出用于基准评测/模型开发，缺少按模型版本核对 ToS 的记录。
- - Major: 全文未见利益冲突与资助披露；若作者与模型厂商存在资助、雇佣或持股关系，会影响“calibration/matcher”结论的可信度，TMLR 应要求显式声明。
- - Major: “per-row adjudication”涉及人工判断，但未说明裁决者资质、独立性、样本量、报酬/同意或 IRB 审查；若由作者自裁且未盲化，可能将主观预期注入标签。
- - Major: 论文展示通过扩展 matcher 把准确率/ECE 从“警报级”变成“完美级”，虽声明 illustrative，但缺少明确的反误用边界，容易被用来“选 matcher 压 ECE”包装高风险部署。
- - Major: N=30 的 OOD 探索性结论（confidence harmful、self-consistency 有效）被置于摘要，存在被产品团队过早固化为门控策略的误用风险，需要更强的统计与推广限制声明。
### Minor（1）
- - Minor: 双盲方面未发现作者信息实质性泄露，但模板中的 “camera-ready: corresponding@example.com” 等占位符和可能的日志/元数据应在提交前清理，避免匿名化工具或附录内容间接暴露身份。

## 汇总

- **Critical: 13 | Major: 37 | Minor: 17**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）