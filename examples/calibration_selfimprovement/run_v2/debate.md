# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\calibration_selfimprovement\run_v2\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 8 / Major 10 （撤回 0，部分成立 2）；注：原始 25 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 5 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: "ECE 跨域变化达 17×" 是两个 ECE 点估计之比，而其中 Qwen2.5-7B 的 9 | 将以绝对ECE差值及CI替代比值,分母CI近零时不报告ratio。 | sustained | concede；当前版本仍以17×比值呈现,分母CI近零致比值不稳定,待修订。 |
| 2 | Critical | - Critical: N=30 且置信度分布退化（27/30 = 1.0），在该退化分布上计算并比较 ECE（0.36 | 论文已声明退化分布(27/30=1.0)下ECE unreliable,提供Props.1-3及smECE_sem替代； | partial | rebut部分成立:论文已声明退化下ECE不可靠并提供替代指标；但仍以0.363/0.1297/0. |
| 3 | Critical | - Critical: Proposition 编号跳跃：摘要引 "Propositions 1--3" 后直接跳至 " | 将在摘要补注Propositions 4-7出处并说明prime为修正版记号。 | sustained | concede；当前版本摘要仍跳号且prime记号未解释,待修订。 |
| 4 | Critical | - Critical: n=30 上做"置信度与一致性负相关→可移除 OOD 过自信答案"的结论仅标注 "indicat | 将报告r值、检验类型、95%CI及n=30显著性门槛。 | sustained | concede；当前版本未报告r/检验/CI/显著性门槛,待修订。 |
| 5 | Critical | - Critical: 存在大量人工标注（"per-row adjudication"、"4999 dual-judge | 将补充IRB/伦理批准、知情同意、报酬及隐私保护声明。 | sustained | concede；当前版本全文无IRB/伦理/知情同意/报酬/隐私声明,待补充。 |
| 6 | Critical | - Critical: 摘要本身存在數字矛矛盾——称 "proof-of-concept pilot N=30 as e | 将在摘要明确区分N=30探针与300→600跨域收集层级关系。 | sustained | concede；当前版本摘要N=30/300/600关系混乱,待澄清。 |
| 7 | Critical | - Critical: 数据许可缺失：全文未披露 MMLU 的许可证归属（MMLU 有特定 CC/MIT 条款需署名）、 | 将披露MMLU及中文free-form数据集许可证与模型使用条款。 | sustained | concede；当前版本未披露MMLU许可证、中文数据集来源与模型条款,待补充。 |
| 8 | Critical | - Critical: 核心结论"confidence 无用甚至有害于 OOD gating""40–50% 高置信 O | 将补充功效分析与效应量CI,将因果结论降级为探索性。 | sustained | concede；当前版本核心结论建在N=30无功效分析/CI/重复实验,待修订。 |
| 9 | Critical | - Critical: 逐行事后"裁定"（per-row adjudication）把准确率抬到 100%、ECE 降到 | 将增加adjudication预注册协议与独立性约束防结果导向调参。 | sustained | concede；当前版本adjudication无预注册/独立性约束,操纵风险仍存。 |
| 10 | Major | - **Major**: "40â50% of high-confidence OOD answers are wr | 将报告高置信OOD子集分母及百分比标准误与CI。 | sustained | concede；当前版本未报告高置信OOD子集分母及标准误/CI,待修订。 |
| 11 | Major | - **Major**: 相关性结论（"confidence 与 consistency 负相关"，n=30）未报告 r | 将报告各模型r/p/CI并对多模型相关做多重比较校正。 | sustained | concede；当前版本未报告r/p/CI及多重比较校正,待修订。 |
| 12 | Major | - Major: "temperature scaling 对重标注不鲁棒"的归因存在**混淆**：在退化分布上 tem | 将解耦退化性与重标注对temperature scaling影响分别归因。 | sustained | concede；当前版本将temperature scaling失效归因于重标注未与退化性解耦,待修 |
| 13 | Major | - Major: MSI 比较（中文自由形式 1.000 → MMLU 选择题 0.334）同时混淆了**协议类型、语言 | 将控制单一因素重做MSI比较或明确标注四因素混杂限制。 | sustained | concede；当前版本MSI比较混杂协议/语言/领域/题型四因素,待解耦或标注限制。 |
| 14 | Major | - Major: Proposition 8â² ââ"under confidence degeneracy | Prop.8'同时证self-consistency在退化下保留判别力(非平凡),confidence无信息仅为必要前提 | partial | rebut部分成立:Prop.8′兼证self-consistency在退化下保留判别力,非纯同义反 |
| 15 | Major | - Major: dual-judged pair 数与 itemÃmodel 乘积不一致且未解释：$300\time | 将说明1159 vs 1200、4999 vs 5400的缺失原因。 | sustained | concede；当前版本1159vs1200、4999vs5400缺失未解释,待说明。 |
| 16 | Major | - Major: self-consistency 优于 raw confidence 用于 OOD gating 的方 | 将引用Wang et al.(2022)等并明确区分自身增量。 | sustained | concede；当前版本未引用Wang et al.等并区分增量,待修订。 |
| 17 | Major | - Major: 两个 matcher（"first tolerant""extended after adjudica | 将形式化给出两个matcher的精确判定规则。 | sustained | concede；当前版本matcher精确规则未形式化,待补充。 |
| 18 | Major | - Major: 命题中用 matcher flip rate 与不对称项 |FNR·p − FPR(1−p)| 界定测 | 将给出bound的置信区间并讨论同源循环依赖限制。 | sustained | concede；当前版本bound从同一N=30估计,无CI且循环依赖未讨论,待修订。 |
| 19 | Major | - Major: 外部有效性标签自相矛盾——同一collection既是"proof-of-concept pilot  | 将统一外部有效性标签,去除N=30作external-validity demonstration表述。 | sustained | concede；当前版本外部有效性标签自相矛盾（pilot又claim外部效度）,待统一。 |
| 20 | Major | - Major: 数据采集中途变更协议——从"300 items × 4 models × 1159 pairs"扩展为 | 将标注扩样本/模型/域三因素混杂,限制跨条件因果归因。 | sustained | concede；当前版本中途变更协议混杂三因素,未标注限制,待修订。 |
| 21 | Minor | （另有 5 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 8 / Major 10 / Minor 0；撤回 0 条（假阳性被作者驳回）；部分成立 2 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
