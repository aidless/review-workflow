# 对抗审查报告

- 时间: 2026-08-28T04:26:52.058283+00:00
- 源: F:\deepseek\papers\calibration-self-improvement\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（2）
- - Critical: 用逐行 adjudication 不断扩展 matcher 直到同一批数据准确率达到 100%，再用这批标签计算 ECE，是循环论证；若这是“语义标签”的证据，则内部效度被完全破坏，因为没有独立 held-out 标签或预注册规则。
- - Critical: 主要 ECE 数字（0.363、0.1297）仍来自 binning-based ECE，而置信度分布退化（27/30 个值恰为 1.0）时 binning 估计无定义且不可靠，用它作核心比较缺乏测量效度。
### Major（6）
- - Major: OOD gating 分析 N=30、探索性、且按“confidence 与 consistency 负相关”事后分组；未做预注册/多重比较校正，40–50% 的估计对应极宽 CI，不能支持“confidence harmful”结论。
- - Major: “confidence harmful”“self-consistency removes overconfident answers”是因果/决策性语言，但只有观测相关性；没有随机干预、效用损失函数或与 random/oracle gate 的决策对照，不能推断 gating 的因果效应。
- - Major: 跨域 MMLU 比较中，domain/subject 与题目难度、准确率、模型能力混淆；ECE 与准确率和置信度水平天然相关，未控制 base rate/difficulty，域间差异可能不是校准差异。
- - Major: 将模型自报 confidence 当作概率的假设未验证；提示词表述、模型对概率刻度的理解、温度和采样参数都是潜在混淆变量，影响所有校准估计。
- - Major: 样本单位是 item-model pairs，同一 item/模型重复测量造成非独立性；若 95% CI 按 pairs 独立计算，会系统性过窄，统计结论内部效度不足。
- - Major: 形式化界限依赖 matcher 的 FNR/FPR 与置信度误差独立或已知相关；若 matcher 错误与置信度相关，Propositions 的界限和软标签估计都不再成立，文中未见该假设检验。
### Minor（4）
- - Minor: MSI 1.000 free-form vs 0.334 MMLU 的对比混杂了题目分布、答案格式和模型集合，不能归因于协议本身。
- - Minor: 摘要突出“varies up to 4×/0.45”但只有极端 Holm-corrected pairs 显著；大量比较不显著，存在选择性强调/发表偏差风险。
- - Minor: 从 300 items/4 models 扩到 600 items/9 models 是否预先计划未说明；若根据早期结果决定扩展或修改 matcher，研究者自由度威胁结论稳定性。
- - Minor: 逐行 adjudication 缺少标注者间一致性（IRR）和明确评分准则，软标签/语义正确性本身含主观噪声。

## 统计（stat）— ok
### Critical（2）
- - Critical: 将 N=30 的 OOD gating 探索结果当作证据，40–50% 的“高置信 OOD 答错”仅对应约 12–15/30 个样本，95% CI 很宽，且未报告低置信/自洽基线的对比，不能支持“confidence harmful”。
- - Critical: matcher 对 ECE 的比较（0.363 vs 0.1297）没有对 ECE 本身做 bootstrap CI 或显著性检验；不同 matcher 同时改变了 ground truth 与 accuracy，直接比较 ECE 混淆了标签测量误差和真实校准差异。
### Major（4）
- - Major: 4999/1159 个“pairs”是 model×item 配对数据，同一 item 和同一 model 重复出现；若按 pairs 当作独立样本计算 CI 或 p 值，会严重低估方差、虚增显著性，应使用 item/model 聚类 bootstrap 或混合效应模型。
- - Major: “single-model ECE varies up to 4×”这类比率效应量对 [0,1] 有界指标有误导性，受基线 ECE 大小支配；应报告绝对差（如 0.45）及其 95% CI，而不是“up to”的极值。
- - Major: “only extreme Holm-corrected pairs significant”与“calibration is domain-specific”的结论强度不匹配；非显著不等于效应不存在，未报告所有成对比较的效应量和校正后 CI，存在对多重比较后选择极值作叙述的问题。
- - Major: ECE 比较未说明检验方法；ECE 是偏态、有界、且在同一模型/题目上相关的统计量，简单正态近似或独立样本检验不合适，应使用 paired bootstrap 或 permutation 检验。
### Minor（4）
- - Minor: 30 个 confidence 值中 27 个等于 1.0 的退化分布下，binning-based ECE 的点估计不可靠；即使改用 smECE_sem，也应对每个点估计报告 bootstrap 分布而不是单值。
- - Minor: MSI 的 1.000（free-form）与 0.334（MMLU）没有 CI；1.000 在退化或小样本下可能是估计饱和/边界值，不能当作精确效应量。
- - Minor: “confidence and consistency are negatively correlated”未报告相关系数、样本量、CI 或检验结果；N=30 下该相关估计极不稳定。
- - Minor: 初始 matcher 对比的 accuracy 63.3% 与 86.7% 仅给点估计，未给 95% CI 或配对差异检验；300 项 pilot 的 accuracy 标准误约 ±2–3pp，直接比较点值可能误导。

## 实验（experiment）— ok
### Critical（1）
- - Critical: 核心校准测量没有独立金标准/对照：三种 matcher 中“逐条 adjudication 后扩展”将准确率推到 100%，存在用模型输出反推调整匹配规则/标签的循环验证风险，使 ECE 与准确率不再能证明真实校准。
### Major（7）
- - Major: 缺少合成/已知概率的对照实验验证 smECE_sem 与 MSI 的无偏性、方差和 binning-free 优势，也没有与 standard ECE、Brier score、reliability diagram 等既有基准作对照。
- - Major: 消融不完整：tolerant matcher 仅一个未说明阈值/规则的实例；MSI 未对语义相似度阈值、soft-label 权重、exact/tolerant/语义标签组合做消融，无法区分效应来自 matcher 还是 estimator。
- - Major: 基准公平不足：领域选择、每域题目抽样、300→600 的扩展规则未说明，且 free-form 与 MMLU 两种协议混在 MSI 对比里，1.000 vs 0.334 不能归因于 domain 而非格式/prompt/matcher。
- - Major: 超参数缺失：温度、采样方式、top-p、max tokens、3 次 self-consistency resample 依据、ECE bin 数与边界、MSI/门控阈值均未报告。
- - Major: seed 管理缺失：题目抽样、生成、resample、bootstrap CI、人工 adjudication 顺序均无 seed/固定流程，95% CI 和“4× / 0.45”差异不可复现。
- - Major: 泛化证据薄弱：仅 MMLU 单基准 + N=30 OOD，且 OOD 结论依赖后验子组（confidence-consistency 负相关），未预设假设也未做多重比较校正，不足以支撑部署层面的“confidence may be harmful”结论。
- - Major: 缺少门控任务的对照组：没有 random gating、always-defer、oracle、纯 consistency 等 trivial baseline，无法判断 confidence gate 的相对收益/危害。
### Minor（2）
- - Minor: 域间差异多数经 Holm 校正不显著，却仍概括为“calibration is domain-specific”，存在结果过释。
- - Minor: 9 个模型未说明是否同 prompt、同 decoding、同训练数据切分，无法排除模型家族/能力/格式混淆。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 主贡献“matcher 决定可测校准”并非新 GAP：语义等价/LLM-as-judge 与 exact match 导致评估结果不同已是 LLM 评测常识，且 label noise 文献早已研究标签翻转对 accuracy/ECE 的影响；Propositions 1–3 的 bound 可视为该已知现象的特例，增量被夸大。
- - Critical: “警告 binning-based ECE”并不新颖：ECE 对 bin 数量/边界敏感以及 binning-free 估计（KDE、adaptive/variance-based）已被 Nixon et al., Kumar et al., Gupta et al. 等系统建立；本文 smECE_sem 若只是又一个变体且未与这些已有指标对比，则“新估计器”贡献过度声明。
### Major（3）
- - Major: MSI 只是把不同 matcher 导致的 accuracy/ECE 差异重新命名，未展示其超出简单 delta-ECE 或 flip-rate/asymmetry 分析的独立信息量，作为新指标的贡献可能名大于实。
- - Major: Proposition 8’ 的“置信度退化时阈值门无判别力、self-consistency 仍有判别力”几乎同义反复/已知结论：置信度若退化为常数，阈值自然成为常数选择器；而 self-consistency/agreement/semantic entropy 优于 verbalized confidence 已被 Wang et al., Kuhn et al. 等大量工作建立。
- - Major: 跨领域 MMLU 测量（600 题/六领域/九模型）是对现有 verbalized-confidence 与 MMLU 领域校准研究的增量式数据补充，未展示与 ConfidenceBench 等已有基准/发现的实质差异，难以支撑“新发现”的表述。
### Minor（1）
- - Minor: OOD-gating 分析仅 N=30 且自述 exploratory，却用于“grounding an OOD-aware gating rule”，作为贡献证据不足，暂只能算假设生成而非新规则。

## 可复现（repro）— ok
### Critical（3）
- - Critical: 核心定量结论无法对账：未提供数据/代码仓库、数据集版本、item-level 输出与 gold-label 哈希/校验和，1159/4999 pairs 的任何行级变更都无法重现或核对。
- - Critical: 配置快照缺失：未固定模型 checkpoint/API 日期、temperature/top-p/max_tokens/seed、提示模板和输出解析代码，4/9 个模型的“同一测量”无法重跑得到相同数字。
- - Critical: 证据链断裂于 matcher：只有“exact-string→first tolerant→per-row adjudication”的结果，没有 matcher 规则/代码、逐行判定表、adjudicator 指南或一致性度量，63.3%/86.7% 的标签不可复核。
### Major（5）
- - Major: seed 未报告：300/600/30 样本选择、六 domain/split、自洽三次 resample、CI/permutation/Holm 流程均无随机种子或抽样脚本，任何随机过程都不可精确复现。
- - Major: 数据许可/模型条款只在附录引用未展示：MMLU 及各商用模型的 license/terms、是否允许再分发、抓取/缓存时间均未在可见稿件中确认。
- - Major: ECE 与 smECE_sem/MSI 实现不可复现：binning 参数、binning-free 算法、soft-label 权重、MSI 公式没有代码或精确数学定义（仅提及命题编号）。
- - Major: 缺一键复现入口：没有 repo、requirements/lockfile、Dockerfile、Makefile 或 `reproduce.sh`，附录声明不能替代可执行环境。
- - Major: 统计对账信息不足：95% CI、Holm 校正、up to 4x/0.45 差异的对比集合不明确，无法用同一脚本重现显著性结论。
### Minor（2）
- - Minor: 探索性 OOD N=30 的选择标准、confidence/consistency 阈值、三个 resample 的确切采样设置未说明，该部分结果难以独立验证。
- - Minor: MMLU 的“cross-domain collection”没有版本/科目/题号清单，300→600 的扩充规则不可审计。

## 写作（writing）— ok
### Critical（2）
- - Critical: 摘要第三组关键结果写作 `100% (ECE = 0.0037?)`，出现孤立问号/疑似缺右括号，核心数字无法正常阅读。
- - Critical: 摘要先用三组 `ECE` 数值作为核心发现，紧接着又断言该分布下 “binning-based ECE is unreliable”，却未说明这些 ECE 是传统 binning 指标还是 binning-free 估计量，摘要自身口径矛盾。
### Major（4）
- - Major: 摘要只引入 “semantic soft-label estimator with MSI”，中心句却直接使用未定义的 `$\mathrm{smECE}_{\mathrm{sem}}$+MSI`，术语/记号前后脱节。
- - Major: 标题称 “Pilot Measurement”，摘要却报告 “expanded to 600 items, nine models, 4999 pairs” 的大规模跨域结果，“pilot” 与全文规模表述冲突。
- - Major: “300 items, 4 models, 1159 pairs” 与 “600 items, six domains, nine models, 4999 pairs” 不能由 item×model 直接对应，且未说明缺失/筛选口径，数字一致性存疑。
- - Major: 摘要从 “Propositions~1--3” 直接跳到 “Proposition~8$'$”，未交代中间命题或 8′ 的附录/来源位置，命题编号体系混乱。
### Minor（3）
- - Minor: ECE 小数位不统一：`0.363`、`0.1297`、`0.0037` 分别用了 3 位和 4 位有效小数。
- - Minor: “Our central finding…” 作为无编号、无环境的独立段落在摘要与 Introduction 之间，重复摘要内容且引入新记号，结构上像未完成的 key-result 块。
- - Minor: “up to 0.45 absolute across six domains” 表述生硬，应改为 “absolute difference up to 0.45 across six domains”。

## 伦理（ethics）— ok
### Major（4）
- - Major: 数据许可仅靠“附录已声明”一笔带过，正文未给出 MMLU 子集的具体许可/版本，也未说明九个模型 API 输出是否可再分发、能否用于构建公开评测集；若 4999 对模型输出随论文发布，可能违反部分模型服务条款。
- - Major: 隐私与数据主体保护不透明：N=30 的 OOD 样本来源未交代，未说明是否包含个人/敏感信息、是否经 PII 清洗或需 IRB/同意；同时使用商业模型 API 处理评测数据，也应披露第三方数据处理与留存风险。
- - Major: 利益冲突与结果完整性：标签 matcher 经“逐行 adjudication”扩展至 100% 准确率，存在事后按期望结果调整标签口径的确认偏倚；未披露 adjudicator 是否独立、判断规则是否预注册，以及作者与模型/评测工具供应商的经济或雇佣关系。
- - Major: 误用风险：exact、tolerant、adjudicated 三种 matcher 给出 63.3%/86.7%/100% 的悬殊结果，若部署者只引用最有利口径，会系统性低估校准错误；高置信 OOD 错误率 40–50% 也可能被简化为“禁用置信度门控”而忽略阈值与一致性信号的完整评估。
### Minor（1）
- - Minor: 双盲方面正文未见明显作者身份泄露，但附录若包含 API 账号、机构订阅、模型版本链接或可识别的数据获取渠道，仍可能在审稿阶段去匿名化，需逐项检查。

## 汇总

- **Critical: 12 | Major: 33 | Minor: 17**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）