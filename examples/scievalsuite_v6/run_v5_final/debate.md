# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\run_v5_final\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 10 / Major 4 （撤回 1，部分成立 5）；注：原始 37 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 17 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - **Critical**: ITT 均值 0.355 无法对账 â gemma 三次试验分数述为 1/6â2 | 将重新核算gemma ITT均值,0.355修正为(1/6+2/6+0)/3â0.167,并更新摘要与正文所有引用处 | sustained | concede；ITT 0.355算术不闭合,(1/6+2/6+0)/3â0.167,当前版本真 |
| 2 | Critical | - **Critical**: `deepseek-v4-flash` 不是已知公开模型（DeepSeek 现有 v2/ | 将核实并更正为实际使用的DeepSeek公开版本（如v3/R1）,统一全文命名,移除'v4-flash'。 | sustained | concede；deepseek-v4-flash非已知公开模型,当前版本存在 |
| 3 | Critical | - Critical: "curated L1a（6 题，探索性）$p=0.0026$，Holm 校正后 $p=0.02 | 将改为在全部16任务上做Holm校正,或事先预注册6任务集并标注为探索性,消除事后挑选偏倚。 | sustained | concede；事后curate再Holm校正无法消除选择偏倚 |
| 4 | Critical | - Critical: 16 任务 Friedman 非显著（p=0.3679）后，再"curated"出 6 任务子集 | 将移除先看全量结果再选子集的流程；若报告curated子集,会标注为事后探索性,不作为主结论。 | sustained | concede；先看全量结果再选子集的forking-paths偏倚确实存在 |
| 5 | Critical | - Critical: L1b 三个模型全部得 0/10，存在严重地板效应；在此基础上对 16 个配对任务（含 10 个 | 将含全零L1b的Friedman降格为探索性,补充仅对有变异任务的分析,明确说明地板效应限制。 | sustained | concede；全零L1b地板效应使Friedman注定非显著、无信息量 |
| 6 | Critical | - Critical: L2 主对比设计（A=ReAct vs F=completion-guided）仅 N=4，Mc | 论文用'no statistically detectable difference'非'等效',并披露power=0. | partial | rebut部分成立:论文未称等效；但零功效下'not detectable'作发现仍误导 |
| 7 | Critical | - Critical: L2 用 exact McNemar 但 $n_d=0<6$、$N=4$、且自报 McNemar | 论文æ«é²McNemar power=0.0000、n_d=0、N=4、d_min=2.1279,用'not de | partial | rebut部分成立:用not detectable非无差异；但零功效结果作结论仍无信息量 |
| 8 | Critical | - Critical: L2 的核心结论"arms 之间无统计学可检测差异"是在 N=4、McNemar 统计功效明确报 | 论文ç¨'not detectable'（未检测到）非'no difference'（不存在）,并披露power=0. | partial | rebut部分成立:已披露power；但零功效trivially true作发现仍为真问题 |
| 9 | Critical | - Critical: L2 结论 "no statistically detectable difference" 建 | 论文å·²æ«é²d_min=2.1279、power=0.0000、N=4、n_d=0,用'not detecta | partial | 同8；披露d_min/power不消除零功效检验作发现呈现的根本问题 |
| 10 | Critical | - Critical: LLM-as-judge 的校准（21/39 gold 上 FNR=FPR=0）被明确称为"me | 论文æè¨'zero judge calls (all SKIP), calibration is a metho | partial | rebut部分成立:0/10为执行失败；但未使用校准作方法贡献仍误导 |
| 11 | Critical | - Critical: gemma 的 intention-to-treat 均值 0.355 与所报离散得分无法对账： | 与问题1同一错误,将修正ITT均值为(1+2+0)/18â0.167,核对所有整数计分口径并更新全文。 | sustained | concede；与#1同一错误,0.355Ã18=6.39非整数,不可能成立 |
| 12 | Critical | - Critical: 全篇样本量极小（L2 $N=4$、L1a 6 题、L1b 10 题），且 L1b 三模型均为 $ | 将降低p俛制的报告精度至2位小数,并添加小样本与地板效应caveat,避免虚假精度。 | sustained | concede；小样本地板效应下4位小数p值制造虚假精度 |
| 13 | Critical | - Critical: 实验臂标签"F"（completion-guided harness）与"Model-F"（fr | 将重命名L2实验臂标签（如FâCG）,避免与frontier Model-F术语碰撞。 | sustained | concede；臂标签F与Model-F指代不同实体,术语碰撞 |
| 14 | Critical | - Critical: 所谓"统一基准"的核心组成 AIRS-Bench、ResearchClawBench、GAIA2 | 将明确区分各基准新增部分与原始版本,论证GAIA2 p3dev等改造的实质性贡献。 | sustained | concede；基准拼装未论证相对原始版本的实质新增 |
| 15 | Critical | - Critical: 摘要声称 LLM-as-judge "passed at FNR=0.0000, FPR=0.0 | FNR/FPR=0来自21/39 gold校准阶段；论文明言'the round made zero judge cal | withdrawn | rebut成立:FNR/FPR来自校准阶段,零调用来自评测轮次,论文已用though区分,非矛盾 |
| 16 | Critical | - Critical: 摘要称"frontier Model-F scored 6/6"，但引言称"API-model  | 将核对frontier模型L1a实际分数,统一摘要6/6与正文5/6及模型名称Model-F vs deepseek-v | sustained | concede；摘要6/6与正文5/6矛盾且名称不一致 |
| 17 | Major | - **Major**: 全部评测对象为 7b–14b 小模型且大面积失败，前沿模型仅以"exploratory"出现（ | 将在Limitations中明确说明suite在有能力模型上区分度未验证,并补充前沿模型探索性结果。 | sustained | concede；suite在有能力模型上区分度未验证 |
| 18 | Major | - Major: "18/18 independent recomputation checks"语义不明——重算的是分 | 将说明recomputation检查对象（分数/哈希/统计量）、输入来源及是否触发新LLM调用。 | sustained | concede；recomputation检查对象与独立性未说明 |
| 19 | Major | - Major: "L047 answer-fitting audit"中的"L047"未在任何处定义或解释，突兀出现， | 将在首次出现处定义L047（审计规则编号或方法标识符）,消除未定义术语。 | sustained | concede；L047未定义即使用 |
| 20 | Major | - Major: "McNemar power 0.0000"——将统计功效报告为精确零在方法上不合理且易误导；功效极少 | 将报告McNemar功效实际计算值及条件（N=4, n_d=0）,说明退化原因而非直接报0.0000。 | sustained | concede；power报为精确零不合理且易误导 |
| 21 | Minor | （另有 17 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 10 / Major 4 / Minor 0；撤回 1 条（假阳性被作者驳回）；部分成立 5 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
