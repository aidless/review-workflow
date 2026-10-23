# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_e0pSqIqwXO\extracted_text.txt`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_e0pSqIqwXO\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 12 / Major 5 （撤回 0，部分成立 3）；注：原始 62 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 42 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: "62 also show long-horizon loss worsening, never | 将'never without'改为纯观测性共现表述,讨论共同原因可能性,明确声明未做干预实验 | sustained | 作者concede；当前版本含因果/必要性断言,观测性共现未经干预验证,问题属实 |
| 2 | Critical | - Critical: "no run reaches our 5 percent meaningful-gap thr | 将补充功效分析与效应量报告,不再仅以未越阈值断言'相似' | sustained | 作者concede；当前版本仅因未越阈值断言相似,缺功效分析与效应量,接受H0错误属实 |
| 3 | Critical | - Critical: GAP 的真实性存疑。原文的耦合系统分析（coupled-system diagnostics、 | 论文透明声明'We use their framework',但报告阴性结果:tanh仅保留transient peak | partial | rebut引用框架透明声明及分化结果成立,但Section 10建议非新创的质疑未直接回应 |
| 4 | Critical | - Critical: 低秩控制器"meet the same criterion because their open | 将加入数值溢出/梯度范数检测,将发散rollout单独报告,不计入准则通过 | sustained | 作者concede；当前版本低秩rollout数值爆炸满足准则,构念效度污染问题属实 |
| 5 | Critical | - Critical: 低秩控制器"因开环 rollout 产生极大 loss"而满足同一判据——这是数值发散而非耦合动 | 将增设控制实验:同初始条件下teacher-forced与free-running rollout对比,区分数值失稳与耦 | sustained | 作者concede；当前版本无数值失稳控制实验,区分效度缺失问题属实 |
| 6 | Critical | - Critical: 全文同时检验 GRU、tanh、low-rank、two-layer、gated-control | 将对该多重比较场景施加BH-FDR校正并声明family-wise错误率 | sustained | 作者concede；当前版本十余子集多重比较无FDR校正,假阳性率不可控属实 |
| 7 | Critical | - Critical: 全文未包含任何利益冲突披露；唯一作者隶属商业实体 Eon Systems PBC（Public  | 将补充利益冲突披露声明,说明Eon Systems PBC在本方向无相关产品或投资利益 | sustained | 作者concede；当前版本无利益冲突披露,单作者商业实体隶属属实 |
| 8 | Critical | - Critical: 全文未声明任务数据（double-integrator、tracking、path-integr | 将补充double-integrator/tracking/path-integration任务数据来源与许可声明 | sustained | 作者concede；当前版本未声明任务数据来源与许可属实 |
| 9 | Critical | - Critical: 全文未提供任何代码/数据仓库链接、DOI 或长期归档快照；摘要声称"Explicit confi | 将提供代码仓库链接、DOI及配置文件长期归档快照 | sustained | 作者concede；摘要声称配置文件可访问但实际无仓库链接/DOI,证据链断裂属实 |
| 10 | Critical | - Critical: 唯一指向评审记录的 OpenReview 链接被注入了空格（"https: // openrev | 将修正OpenReview链接,去除注入空格,确保可解析跳转 | sustained | 作者concede；当前版本OpenReview链接确含注入空格无法解析 |
| 11 | Critical | - Critical: 头条效应量"mean peak reaching 19.1 times the initial  | 将补充50 seed的SD、95% CI及中位数/范围 | sustained | 作者concede；当前版本19.1x仅报均值无SD/CI/中位数,右偏比率可靠性不明属实 |
| 12 | Critical | - Critical: 未给出代码 commit hash、数据 checksum/SHA256 或模型权重指纹，哈希对 | 将提供代码commit hash、数据SHA256校验和及模型权重指纹 | sustained | 作者concede；当前版本无commit hash/checksum/权重指纹属实 |
| 13 | Critical | - Critical: 本文核心定位是 Ger and Barak (2025) 的"独立复现"，而摘要自述的主要发现是 | 摘要报告多项架构特异性新发现:GRU/tracking retain final-loss divergence、tan | partial | rebutt引用架构特异性新发现属实,但摘要仍以确认性表述为主轴,贡献偏薄问题部分成立 |
| 14 | Critical | - Critical: 预设阈值（5% meaningful-gap、短视界改善+谱半径增加的复合判据）驱动了全部二元结 | 将对1%/5%/10%阈值做敏感性分析,报告结论是否翻转 | sustained | 作者concede；当前版本预设阈值无敏感性分析,结论稳健性未知属实 |
| 15 | Major | - Major: "5 percent meaningful-gap threshold"是实用显著性阈值，却被当作统计 | 将该阈值与效应量及置信区间挂钩,补充配对统计检验 | sustained | 作者concede；当前版本5%阈值被用作统计推断却无CI/错误率控制属实 |
| 16 | Major | - Major: "50 paired seeds"歧义——是 50 个种子（paired 与什么配对？）还是 50 对 | 将明确'50 paired seeds'为50个种子在开/闭环paired条件下的测试 | sustained | 作者concede；当前版本50 paired seeds含义歧义属实 |
| 17 | Major | - Major: "all 120 runs meet the criterion"与"reproduce in all | 准则具证伪力:仅62/120出现long-horizon worsening；tanh仅保留transient peak | partial | rebut示62/120及架构分化有证伪力,但复合准则仍100%通过,过度宽松问题部分成立 |
| 18 | Major | - Major: "independent implementation"是核心主张，却未提供与 Ger & Barak | 将补充与Ger & Barak原始代码的协议对齐表及关键差异diff | sustained | 作者concede；当前版本无协议对齐表/diff,独立性不可证伪属实 |
| 19 | Major | - Major: "losses are similar""transfer is weak"为定性判断，既无效应量（C | 将补充Cohen's d效应量及配对t/Wilcoxon signed-rank检验 | sustained | 作者concede；当前版本定性判断无效应量及配对检验属实 |
| 20 | Major | - Major: "protocol changes"在摘要与引言中被反复提及为 robustness 审查的关键手段， | 将在正文逐项列出protocol changes的具体改动内容 | sustained | 作者concede；当前版本protocol changes具体内容未说明属实 |
| 21 | Minor | （另有 42 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 12 / Major 5 / Minor 0；撤回 0 条（假阳性被作者驳回）；部分成立 3 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
