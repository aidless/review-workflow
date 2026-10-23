# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\run_v6_verify\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 15 / Major 1 （撤回 0，部分成立 4）；注：原始 35 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 15 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: "deepseek-v4-flash / Model-F" 为 API 黑盒且 "v4-flas | 将补录API版本号、快照日期与回放凭证；若无法提供则将deepseek-v4-flash/Model-F移出确认性结果, | sustained | 作者concede补录API版本/快照；当前版本仍缺复现凭证,deepseek-v4-flash疑似 |
| 2 | Critical | - Critical: "per-seed rows"与"three independent trials"反复出现，但 | 将在附录列出完整seed清单并与per-seed行逐条对齐,使seed值可追溯。 | sustained | 作者concede补seed清单；当前版本全文无具体seed值,逐行复现无法对齐。 |
| 3 | Critical | - Critical: A=ReAct 与 CG=completion-guided 两臂在三个模型上 mean goa | 将对A与CG臂做输出级diff诊断根因（功能等价或缓存/seed复用）,补充arm-level不一致性分析。 | sustained | 作者concede做diff诊断；当前版本两臂均值完全相同且n_d=0,根因未诊断。 |
| 4 | Critical | - Critical: Friedman 检验纳入 16 个配对任务中 10 个为全零（floor），全零任务不产生任何 | 将剔除全零floor任务后重跑Friedman,并改用含平局校正的置换exact Friedman。 | sustained | 作者concede剔除floor任务重跑；当前版本Friedman含10个全零任务,统计量失真未校正 |
| 5 | Critical | - Critical: GAP 论证空洞且无据——声称"evaluation remains fragmented"却只 | 将引用HELM/BIG-bench/AgentBench/GAIA/AIRS-Bench原作建立gap真实性与新颖性。 | sustained | 作者concede补引用；当前版本gap仅引goodfellow2016deep,HELM/BIG- |
| 6 | Critical | - Critical: L1a/L1b 要求本地执行模型生成代码、L2 执行交互式工具调用，但全文未披露沙箱、能力限制、 | 将新增沙箱、网络隔离、能力限制及安全缓解措施披露章节。 | sustained | 作者concede补安全披露；当前版本无沙箱/网络隔离/能力限制说明,安全风险存在。 |
| 7 | Critical | - Critical: L1b 的 LLM-as-judge 校准（FNR=0、FPR=0）是离线 warrant，而实 | 论文明确将校准定位为methodological warrant而非L1b评分有效性支撑；L1b得0/10源于执行失败而 | partial | 论文确未声称校准支撑L1b评分有效性（rebut成立）；但校准未在真实产出验证的内部效度缺口客观存在 |
| 8 | Critical | - Critical: L2 双臂对比（A=ReAct vs CG）在 N=4 且 n_d=0（零不一致对）条件下，Mc | 论文明确称L2为statistically uninformative、reported for transparenc | partial | 论文确称statistically uninformative、未暗示无差异（rebut成立）；但零 |
| 9 | Critical | - Critical: L2 的精确 McNemar 检验在 $n_d=0$（零不一致对）、$N=4$ 下报 $p=1. | 将把p=1.00替换为检验退化/不适用(n_d=0)声明,不再报告p值,直接声明McNemar在此条件下不可用。 | sustained | 作者concede将声明检验不适用；当前版本仍报p=1.00,属退化检验误用。 |
| 10 | Critical | - Critical: LLM-as-judge 校准仅 21 gold、单标注者、FNR=FPR=0.00，样本太小且 | 将添加二项CI与第二标注者IAA,并明确声明校准集与实际施测分布的迁移局限。 | sustained | 作者concede补CI/IAA/迁移局限；当前版本样本小、无IAA、校准与施测分布脱节。 |
| 11 | Critical | - Critical: LLM-as-judge 校准报告 FNR=0.00、FPR=0.00（N=21，扩展集 39） | 将按rule of three给出0/21与0/39的95%上界（约14%/7.7%）,并将passed改为0误差观测、 | sustained | 作者concede加rule of three上界；当前版本passed at 0.00未给CI,属 |
| 12 | Critical | - Critical: gemma2:9b 在 L1a 上获得 3 次独立试验而 7b/14b 仅 1 次：采样次数与模 | 将对所有模型统一试次数或添加混淆声明与敏感性分析,分离模型效应与试次效应。 | sustained | 作者concede统一试次数；当前版本gemma3试次与其余1试次混淆模型效应。 |
| 13 | Critical | - Critical: post-hoc âcuratedâ L1a 子集（6 tasks）给出 p=0.003 | 将对事后子集施加Bonferroni/Holm校正或预设登记,并标注选择规则。 | sustained | 作者concede加Bonferroni/Holm校正；当前版本事后子集无多比较校正,选择偏倚存在。 |
| 14 | Critical | - Critical: 三大组件（AIRS-Bench、ResearchClawBench、GAIA2）均为已有基准的直 | 论文明确声明贡献为measurement instrument而非新任务；新元素含L047 audit、calibrat | partial | 论文确声明为measurement instrument并列新元素（rebut成立）；但纯集成无新任 |
| 15 | Critical | - Critical: 事后 curated L1a 子集（6 任务）得 p=0.003 与确认性非显著结果并列呈现，存 | 将披露事后子集选择规则（是否数据驱动）,隔离为exploratory并加选择敏感性分析。 | sustained | 作者concede披露选择规则；当前版本事后子集选择规则未说明,HARKing风险存在。 |
| 16 | Critical | - Critical: 摘要写“three cloud-hosted local models”，正文写“three s | 将统一术语为开放权重模型经云端推理端点部署,消除cloud-hosted与local矛盾。 | sustained | 作者concede统一术语；当前版本cloud-hosted与local自相矛盾。 |
| 17 | Critical | - Critical: 摘要称校准"passed at FNR=0.00, FPR=0.00"，紧接着又写"the ro | 将把passed改为校准在gold集完成、实际轮次零judge调用,明确分离离线校准与在线施测。 | sustained | 作者concede分离校准与施测；当前版本passed与zero judge calls直接矛盾。 |
| 18 | Critical | - Critical: 效力不足且不可证伪：N=4、d_min=2.1279（属"巨大"效应量）意味着只有极端效应可检出 | 论文已披露power limits(N=4,d_min=2.1279,McNemar power structurall | partial | 论文确披露power limits并称uninformative（rebut成立）；但零功效组件纳入 |
| 19 | Critical | - Critical: 数据许可未披露——复用 AIRS-Bench、ResearchClawBench、GAIA2 三 | 将声明各基准原始许可证与再分发条款,并限定125文件封存范围。 | sustained | 作者concede声明许可；当前版本未披露各基准原始许可证与再分发条款。 |
| 20 | Major | - Major: "cloud-hosted local models"ââ"云端托管"与"本地"构成术语矛盾（ | 将明确为本地权重可复现的开放模型统一部署于云端推理端点,消除oxymoron。 | sustained | 作者concede明确术语；当前版本cloud-hosted local models为oxymor |
| 21 | Minor | （另有 15 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 15 / Major 1 / Minor 0；撤回 0 条（假阳性被作者驳回）；部分成立 4 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
