# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\calibration_selfimprovement\run_v6\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 7 / Major 8 （撤回 4，部分成立 1）；注：原始 22 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 2 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: N=30 且未说明样本抽样机制；若 30 行来自便利样本或事后挑选，27/30 置信度恰为 1. | 将补充N=30的抽样机制与纳入/排除标准,并把退化分布限定为该探索渠道而非任务分布总括 | sustained | 作者concede,当前版本确未说明抽样机制与纳入排除标准,待修订。 |
| 2 | Critical | - Critical: OOD-gating 结论使用“harmful/removes”等因果语言，但仅基于 N=30  | 将OOD部分改为纯探索性相关描述,去除harmful/removes因果词,并报告混淆变量与CI | sustained | 作者concede,当前因果表述与混淆控制缺失,需修订为探索性并补CI。 |
| 3 | Critical | - Critical: “only extreme Holm-corrected pairs significant”未 | 将报告全部比较数、检验统计量、未调整/调整p值与效应量,并预先指定对比或采用整体校正 | sustained | 作者concede,统计量、p值、效应量与预指定比较均需补充。 |
| 4 | Critical | - Critical: 所有随机/重采样环节均未给出 seed：3 次 resample 的自洽性、OOD N=30 的 | 将固定所有随机种子并公开:重采样、OOD选取、bootstrap、跨域子采样、生成参数 | sustained | 作者concede,随机种子未固定与公开,可复现性问题仍存在。 |
| 5 | Critical | - Critical: 摘要中 `in-sample on 30 rows, circular 95\% CI \.4\ | 将修复摘要LaTeX为规范区间,并用Clopper-Pearson重新计算30/30的95%CI | sustained | 作者concede,摘要LaTeX损坏且CI下限数值错误,需修复。 |
| 6 | Critical | - Critical: 未列出模型名称、版本、检查点或 API 调用日期，4/9 个模型无法被唯一定位。 | 将补充全部模型名称、版本/检查点、API调用日期与采样温度等定位信息 | sustained | 作者concede,模型版本/检查点/调用日期等信息待补充。 |
| 7 | Critical | - Critical: 未提供 matcher 实现代码、规则、阈值和 MSI 计算代码，无法对 label match | 论文已声明提供evidence package:matcher、adjudication record、canonica | withdrawn | 论文已声明evidence package含matcher与canonical recomputat |
| 8 | Critical | - Critical: 未提供原始模型输出和逐行 adjudication 数据，63.3%→86.7%→100% 的“ | 论文已声明按行adjudication记录和canonical recomputation包含于evidence pac | withdrawn | 论文已声明逐行adjudication record与canonical recomputation |
| 9 | Critical | - Critical: 核心 pilot 结论建立在 N=30 且 27/30 置信度恰为 1.0 的退化样本上，三种  | 将给pilot三种ECE加bootstrap标准误/CI,或将其明确降为无推断的图示 | sustained | 作者concede,三种ECE缺少标准误或bootstrap CI,需补或降为图示。 |
| 10 | Critical | - Critical: 核心“matcher 决定测量到的校准”是在同一 30 行样本上轮换 matcher 得到的，并 | 论文已明确标注100%/ECE=0.0037为in-sample、circular、not evidence of ca | withdrawn | 论文已明确in-sample/illustrative/not evidence of calibr |
| 11 | Major | - Major: MMLU 的 4999 pairs 由 600 items × 9 models 产生，同一 item | 将改用item/model两水平混合效应模型或聚类稳健标准误,并报告ICC | sustained | 作者concede,观测非独立问题需混合效应或聚类稳健标准误修正。 |
| 12 | Major | - Major: MSI 1.000 vs 0.334 以单点值呈现，没有 SE/CI、样本量和配对结构；在退化置信度分 | 将给MSI两侧的n、bootstrap/非参数CI,并说明配对结构 | sustained | 作者concede,MSI单点值缺n/CI/配对结构,待补充。 |
| 13 | Major | - Major: MSI 1.000（free-form）vs 0.334（MMLU）是协议、题目分布、模型集合、标注格 | 将分条件报告样本量与CI,MSI差异改称描述性混杂比较,不再归因protocol-dependent | sustained | 作者concede,混杂比较需分条件报告样本量与CI,不能归因protocol。 |
| 14 | Major | - Major: OOD-gating 分析仅 N=30 且标为 exploratory，40–50% wrong 对应 | 将给OOD gating二项/自助CI,报告阈值搜索与门控规则数,并仅作假设生成 | sustained | 作者concede,OOD gating需补CI与阈值搜索说明,仅作假设生成。 |
| 15 | Major | - Major: “ECE varies up to 4× / up to 0.45 absolute across d | 论文已报告95% CI并限定only extreme Holm-corrected pairs significant； | withdrawn | 论文已报告95%CI并限定仅extreme Holm-corrected pairs显著,up to |
| 16 | Major | - Major: “binning-based ECE 在退化置信分布下不可靠”是成熟结论，Nixon et al. ( | 将把binning-free caution定位为应用/复述,引用Nixon/Kumar/Błasiok等,不列为新贡献 | sustained | 作者concede,需将binning-free caution定位为综述并引用既有方法。 |
| 17 | Major | - Major: 摘要引用 `Proposition~8$'$`，但贡献列表只提及 Propositions 1--3， | 将统一命题编号,摘要Proposition 8'改为与贡献列表一致的编号或解释来源 | sustained | 作者concede,命题编号不一致,需统一或解释Proposition 8'来源。 |
| 18 | Major | - Major: 样本量证据链不一致/损耗未解释：600 items × 9 models 最多 5400 pairs， | 将补充4999较5400缺失401的逐项排除统计,以及300→600、1159→4999的扩展规则 | sustained | 作者concede,4999缺失401及扩展规则需逐项补充说明。 |
| 19 | Major | - Major: 泛化证据薄弱：核心结论来自 N=30 的 in-sample pilot 与 N=30 的 explo | 论文明确N=30为illustrative/in-sample且not evidence of calibration, | partial | 论文有illustrative/not evidence及未作部署结论的限定；但独立外部数据验证仍缺 |
| 20 | Major | - Major: 若 30/30 的 95% CI 确为 [0.4%,100%]，数值有误——Clopper-Pears | 将修正数值:30/30 Clopper-Pearson 95%CI为[88.4%,100%]；若用Bayesian须明确 | sustained | 作者concede,30/30 CI应约[88.4%,100%]或说明Bayesian先验。 |
| 21 | Minor | （另有 2 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 7 / Major 8 / Minor 0；撤回 4 条（假阳性被作者驳回）；部分成立 1 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
