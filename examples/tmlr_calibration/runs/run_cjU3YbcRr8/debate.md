# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_cjU3YbcRr8\extracted_text.txt`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_cjU3YbcRr8\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 7 / Major 10 （撤回 1，部分成立 2）；注：原始 44 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 24 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: "124-paper 2023â2026 audit set" 是本文的经验骨架，但可见文本 | 将在附录补充完整检索协议:数据库、搜索串/seed、纳入排除标准、检索日期与迭代轮次。 | sustained | 作者concede将补充检索协议；当前版本确无数据库、搜索串、纳入排除标准、检索日期,语料不可复现。 |
| 2 | Critical | - Critical: "governance"阶段涉及技能跨 agent 共享与发布，但未讨论共享技能制品（爬取的代码 | 将在governance阶段增设许可与版权小节,覆盖GPL/Apache/专有许可污染及制品归属。 | sustained | 作者concede将增设许可版权小节；当前版本governance阶段确未讨论GPL/Apache污 |
| 3 | Critical | - Critical: 124 篇 audit set 未报告抽样框与抽样方法，属方便样本/非概率抽样，既无代表性分析也 | 将补充抽样框与抽样方法说明,并添加代表性局限与功效分析缺失的明确caveat。 | sustained | 作者concede将补充抽样框与caveat；当前版本无抽样方法、代表性分析或功效分析,归纳外推缺乏 |
| 4 | Critical | - Critical: 124 篇 audit set 没有给出可复现的检索/纳入/排除协议（检索词、数据库、时间窗判定 | 将补充可复现检索/纳入排除协议,显式讨论选择偏差对evidence-graded patterns的继承影响。 | sustained | 作者concede将讨论选择偏差继承；当前版本无检索协议且未检验泛化,evidence-graded |
| 5 | Critical | - Critical: The foundational premise that structurally ortho | 论文六类taxonomy(Table 1)正因异构而设,明确区分六种skill sense并将后两类列为boundary | withdrawn | 论文Table 1明确区分六种skill sense,后两类列为boundary case,非混为一 |
| 6 | Critical | - Critical: The paper derives quasi-causal claims ("verifier | Abstract明确标注"evidence-graded patterns with explicit caveats" | partial | Abstract确有'patterns with explicit caveats'框架支持观察性解 |
| 7 | Critical | - Critical: 八阶段生命周期架构（evidence acquisitionâproposalâveri | 将与已有memory/tool-learning survey的lifecycle逐阶段对比,阐明skill独有的adm | sustained | 作者concede将逐阶段对比已有survey；当前版本未讨论与memory/tool-learni |
| 8 | Critical | - Critical: 未发布任何可一键复现的工件（标注表、编码细则、论文→类目映射）；文中呼吁"concrete re | 将发布标注表、编码细则、论文→类目映射等可复现工件作为补充材料。 | sustained | 作者concede将发布工件；当前版本未发布标注表/编码细则/映射,自身未践行报告标准。 |
| 9 | Critical | - Critical: 调研涵盖医学影像、推荐系统等领域，技能从"交互"中采集并持久存储，却未讨论 PII/PHI 嵌入 | 将增设隐私风险小节,覆盖PII/PHI嵌入技能与provenance元数据的HIPAA/GDPR及IRB议题。 | sustained | 作者concede将增设隐私小节；当前版本覆盖医学影像等领域却未讨论PII/PHI嵌入技能的HIPA |
| 10 | Major | - Major: "Admission and repair are repeatedly important" con | 将"repeatedly important"改为"repeatedly observed",明确区分出现频率与已证实重 | sustained | 作者concede将改为'repeatedly observed'；当前版本'repeatedly  |
| 11 | Major | - Major: "Evidence-graded patterns" are claimed but the grad | 将补充grading rubric、证据层级定义及rater reliability指标(如Cohen's kappa) | sustained | 作者concede将补充rubric/层级/可靠性；当前版本grading rubric、证据层级与 |
| 12 | Major | - Major: "evidence-graded"分级标准未见操作化定义，未说明分级是否基于效应量、样本量或 p 值， | 将操作化分级标准,明确基于效应量/样本量,消除主观化与p值误用风险。 | sustained | 作者concede将操作化分级标准；当前版本无操作化定义,未说明依据效应量/样本量,存在主观化风险。 |
| 13 | Major | - Major: "ten-operator vocabulary"与"skill-record schema"被明确  | 将明确schema/vocabulary为描述性术语而非独立贡献,消除贡献定位歧义。 | sustained | 作者concede将明确为描述性术语；当前版本schema/vocabulary既disclaim非 |
| 14 | Major | - Major: 124 篇审计集的筛选标准未披鲲选择偏差，无法排除作者所在机构（CMU）相关工作被过度纳入的利益冲突嫌 | 将披露CMU关联论文比例并补充选择标准,排除利益冲突嫌疑。 | sustained | 作者concede将披露CMU比例；当前版本未披露机构关联与选择标准,利益冲突嫌疑未排除。 |
| 15 | Major | - Major: A strong temporal confound is unaddressed: the 2023 | 将增设时间混淆讨论,分析base-model能力跃迁对dynamic skill patterns的混淆效应。 | sustained | 作者concede将增设时间混淆讨论；当前版本未讨论base-model能力跃迁对dynamic s |
| 16 | Major | - Major: GAP 声明（"现有工作把 skill 当作静态集合"）被断言而非证明——引言列举了前置系统（Voya | 将逐条引用对比前序survey,系统论证lifecycle维度未被覆盖,实证支撑GAP声明。 | sustained | 作者concede将逐条对比前序survey；当前版本GAP声明为断言而非证明,未引用对比据称忽视动 |
| 17 | Major | - Major: No inclusion/exclusion criteria, search strategy, o | 将补充纳入排除标准、检索策略与inter-annotator agreement,确保语料可复现。 | sustained | 作者concede将补充纳入排除标准与IAA；当前版本无检索策略、纳入排除标准或inter-anno |
| 18 | Major | - Major: Table 1 将每个系统归类到 taxonomy sense 与 verification hand | 将为Table 1编码报告IAA指标(如Cohen's kappa),使归类赋值可独立复现。 | sustained | 作者concede将报告IAA指标；当前版本Table 1未报告任何编码可靠性指标,归类不可独立复现 |
| 19 | Major | - Major: The eight-stage lifecycle architecture is presented | 将说明八阶段推导方法(归纳自语料或自上而下)及grounding过程与迭代轮次。 | sustained | 作者concede将说明推导方法；当前版本八阶段推导方法未指定,不清是否归纳自语料。 |
| 20 | Major | - Major: Voyager（2023）已实现 verify(unit test)、admit、compose、增长 | Table 1含20+系统,验证handle涵盖unit test/rollout/env reward/rubric  | partial | Table 1确含20+系统与多类验证handle,反驳了单一系统重标签；但Voyager已齐备多阶 |
| 21 | Minor | （另有 24 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 7 / Major 10 / Minor 0；撤回 1 条（假阳性被作者驳回）；部分成立 2 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
