# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f1\extracted_text.txt`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f1\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 6 / Major 10 （撤回 3，部分成立 0）；注：原始 24 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 4 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: 主要因果结论的统计单元混乱：报告的是 Qwen3:4b 单模型/单通道的 Wilcoxon 结果 | 摘要明确主检验为 Qwen3:4b 单模型/单通道 Wilcoxon（n=500 对）；12,000 cells/6,0 | withdrawn | 摘要确以Qwen3:4b单模型/单通道Wilcoxon为主检验,12,000/6,000仅为实验规模 |
| 2 | Critical | - Critical: 存在未校正的多重比较与选择性报告风险：从 4 个模型和 3 个通道中挑出最显著的 Qwen3:4 | 将报告全部 4×3=12 组检验及 BH-FDR 校正,并以校正后仍显著的结果作为主发现。 | sustained | 作者承认将补报12组检验并做BH-FDR校正；当前版本确实存在未校正多重比较与选择性报告风险。 |
| 3 | Critical | - Critical: 摘要称 12,000 cells/6,000 paired differences，却又说 po | 将统一定义 n=500 为每模型×通道的问题配对样本量,并在功效分析与 Wilcoxon 中明确分析单位为 500 对而 | sustained | 作者承认需统一定义n=500分析单元；当前功效分析、Wilcoxon与样本规模的统计单位仍无法核对。 |
| 4 | Critical | - Critical: 未给出完整实验材料：confidence-priming 与 benign cache entr | 将在附录/补充材料给出两条件逐字模板、75-char neutral prefix、注入方式与 verbalized-c | sustained | 作者承诺补充逐字模板、前缀、注入方式与解析规则；当前版本实验材料缺失,无法复现。 |
| 5 | Critical | - Critical: 模型配置快照缺失：仅写 “4 local model families / Qwen3:4b”， | 将补充全部模型精确 checkpoint/ID、量化方式、推理框架、温度、采样、max tokens、dtype 与确定 | sustained | 作者承诺补充模型checkpoint、量化、推理框架及采样配置；当前模型配置快照缺失。 |
| 6 | Critical | - Critical: 混淆变量未排除，语义归因不成立：confidence-priming 与 length-matc | 将新增多种安慰剂条件（积极无置信指令、同指令不同措辞、句法主题匹配）,以分离语义内容与其他混淆。 | sustained | 作者承诺新增多类安慰剂条件；当前单一对照无法排除语义以外的混淆变量。 |
| 7 | Critical | - Critical: 证据链断裂：MMLU 的确切版本、科目子集、500 题采样方式、缓存条目构造位置均未说明，也没有 | 将补充 MMLU 版本、科目子集、500 题采样代码、缓存条目注入位置,及原始数据到评估/bootstrap 的中间产物 | sustained | 作者承诺补充MMLU版本、采样方式及中间产物清单；当前证据链条断裂。 |
| 8 | Critical | - Critical: 长度匹配良性对照只在子集上测试，未覆盖主效应所在的全量 500×4×3 配对数据，因此“语义而非 | 论文已披露对照仅在子集测试:摘要明确标 hypothesis-generating、control tested on  | withdrawn | 摘要已明确标注hypothesis-generating及control tested on a s |
| 9 | Major | - Major: power analysis 与检验方法不匹配：MDE dz=0.18 基于配对参数检验思路，但推断使 | 将补充与 Wilcoxon/置换检验匹配的功效分析,并明确 MDE dz 对应的分析单元与 n=500 对的定义。 | sustained | 作者承认将补充与Wilcoxon匹配的非参数功效分析；当前MDE dz与检验方法确实不匹配。 |
| 10 | Major | - Major: seed 管理不透明：只列出 42/43/44，未说明主统计量是否跨 seed 聚合、是否用 seed | 将说明 3 seeds 的跨 seed 聚合方式、是否作随机效应,并报告 seed 级方差与最差 seed 结果。 | sustained | 作者承认需说明seed聚合方式并报告seed级方差；当前seed管理不透明。 |
| 11 | Major | - Major: “3 channels”在摘要/引言中从未定义，结果中又出现“instruction channel” | 将在方法开头精确定义 3 channels（缓存/注入/置信度呈现通道）,并统一全文术语与结果小节。 | sustained | 作者承诺精确定义3 channels并统一术语；当前channel含义确实不明确。 |
| 12 | Major | - Major: “descriptive Wasserstein upper bound (|∆MAE| ≤ LΓ)” | 将显式定义 Γ 为经验 Wasserstein 距离、L 为 Lipschitz 常数,并给出 |∆MAE|≤LΓ 的推 | sustained | 作者承诺定义Γ、L并给出推导；当前Wasserstein上界公式缺乏上下文。 |
| 13 | Major | - Major: 主实验只有单一 priming 措辞；补充 pilot 仅给出 0.645/0.646/0.649 的 | 将补充 pilot 的 ΔMAE、95%CI、功效/样本量信息,并增加至少 3 种措辞的完整消融。 | sustained | 作者承诺补充pilot的ΔMAE、CI及完整措辞消融；当前措辞消融不完整。 |
| 14 | Major | - Major: 四个 post-hoc baselines 不可复现：held-out benign split 的划 | 将公开 held-out benign 划分方法、baseline 拟合代码、库版本、超参数及 baseline 后 Δ | sustained | 作者承诺公开划分方式、代码、库版本与超参数；当前baseline不可复现。 |
| 15 | Major | - Major: 效应量报告不完整：仅给出 dz=0.42 和点估计 ΔMAE=+0.047，未报告 dz 的置信区间； | 将报告 dz 与 ΔMAE 的 bootstrap CI,并给出全部 12 组检验结果以校正选择偏差。 | sustained | 作者承诺报告dz和ΔMAE的CI及全部12组结果；当前效应量报告不完整且存在选择偏差。 |
| 16 | Major | - Major: 未说明 MMLU 数据及所用模型/补充数据的许可证与归属；MMLU 为 MIT 许可，若随文发布 50 | 将补充 MMLU MIT 许可声明与数据归属；若发布 500 题子集或模板样例,将保留版权和许可信息。 | sustained | 作者承诺补充MMLU许可与数据归属；当前版权合规说明确实缺失。 |
| 17 | Major | - Major: 术语/引文错误：Related Work 称 Naeini et al. (2015) “derive | 将修正引文表述:Naeini et al. 提出基于 binning 的可靠性/ECE 估计,Brier score 与 | sustained | 作者承诺修正Naeini et al.引文表述；当前事实性归因有误。 |
| 18 | Major | - Major: 术语混用：摘要主结果使用 ∆MAE（verbalized-confidence error），引言却写 | 将统一结果变量为 verbalized-confidence ΔMAE,并在标题、摘要与引言中改用一致表述,避免与置信度 | sustained | 作者承诺统一为verbalized-confidence ΔMAE；当前标题、摘要与引言确实变量混用 |
| 19 | Major | - Major: 泛化证据薄弱：只有 4 个小规模本地模型、单一 MMLU 子集、单一 phrasing、单一 cach | 摘要已限定 sample-descriptive、4 small local models、单一 MMLU 子集、单一  | withdrawn | 摘要已限定sample-descriptive、4小模型、单一子集/措辞/置信区间及hypothes |
| 20 | Minor | - Minor: 全文唯一图引用是摘要中的 “see Fig. 1”，但正文与贡献未给出对应图注或结果表；图表现无法支撑 | 将为 Fig.1 补充完整图注、坐标/误差线说明与对应结果表,并在正文和贡献中显式引用。 | sustained | 作者承诺补充Fig.1图注、坐标与对应结果表；当前图表确实无法支撑摘要数字。 |
| 21 | Minor | （另有 4 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 6 / Major 10 / Minor 1；撤回 3 条（假阳性被作者驳回）；部分成立 0 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
