# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\run_v7_final\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 17 / Major 0 （撤回 0，部分成立 3）；注：原始 40 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 20 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - **Critical**: gemma2:9b 在 L1a 上获得三次独立试验(1/6â2/6)，而 7b、14 | 将统一所有模型L1a试验次数,对7b/14b补跑相同次数试验,跨模型比较仅用ITT均值口径。 | sustained | 作者concede承诺统一试验次数,当前版本跨模型试验次数不对称的公平性违规仍存在 |
| 2 | Critical | - **Critical**: 三层结构本质上是三个已有基准（AIRS-Bench、ResearchClawBench、 | 将在引言补充统一契约可回答的跨层科学问题（如同一模型prediction/workflow/execution能力解耦） | sustained | 作者concede承诺补充科学问题论证,当前版本unification科学价值未确立仍存在 |
| 3 | Critical | - **Critical**: 全套 Friedman 非显著(p=0.37)后，事后筛选 L1a 子集(6 任务)得到 | 将把p=0.003移出摘要至附录exploratory分析,并加Bonferroni校正。 | sustained | 作者concede承诺移出摘要,当前版本p=0.003事后子集值仍在摘要中构成误导 |
| 4 | Critical | - **Critical**: 基准论文自身的评估结果全面处于地板或零信息状态——L1b 全模型 0/10、L2 零 d | 论文L1b报告审计拦截3/3模型answer-fitting、稳定失败分类学及阳性对照证明pipeline可解,这些是有 | partial | 论文确有审计/分类学/阳性对照发现,但未解决L1b全0、L2零信息致跨模型零区分力的核心问题 |
| 5 | Critical | - Critical: "SHA-256 seal over 125 files verifying byte-for- | 将明确SHA-256 seal覆盖范围为输入/契约文件及存储的per-seed结果,非LLM实时推理产物,并修正过度宣称 | sustained | 作者concede承诺修正覆盖范围,当前版本byte-for-byte过度宣称仍存在 |
| 6 | Critical | - Critical: Friedman 检验纳入 10 个 all-zero 的 L1b 任务，这些任务零方差、零判别 | 将从Friedman中剔除10个all-zero L1b任务,仅对非零方差任务子集重做检验并报告。 | sustained | 作者concede承诺剔除all-zero任务,当前版本Friedman含零方差任务致检验失效仍存在 |
| 7 | Critical | - Critical: L1a 事后精选 6 个任务子集得到 p=0.003，明确标注 post-hoc/explora | 将对L1a子集p值做Bonferroni校正,并移出摘要仅保留于附录exploratory分析。 | sustained | 作者concede承诺校正并移出摘要,当前版本post-hoc p值未校正仍在摘要中 |
| 8 | Critical | - Critical: L1a 的 "1/6 → 2/6 after three independent trials  | 将统一所有模型试验次数协议,跨模型对比仅采用ITT均值0.355口径,删除择优上报。 | sustained | 作者concede承诺统一ITT口径,当前版本仅gemma三次重试择优上报的选择偏差仍存在 |
| 9 | Critical | - Critical: L2 主分析用 exact McNemar，N=4、n_d=0 不协调对，补充 N=8 同样 n | 论文摘要已声明'L2 statistically uninformative: exact McNemar inappl | partial | 论文确已声明L2无统计信息且未推断,但仍报告4位小数均值,描述性结果可误导读者 |
| 10 | Critical | - Critical: L2 的两个 arm（A=ReAct vs CG=completion-guided）在三个模型 | 将补充CG arm消融实验调查no-op退化原因,并在论文中明确标注该null结果。 | sustained | 作者concede承诺补充消融,当前版本CG两arm完全相同却无解释仍存在 |
| 11 | Critical | - Critical: LLM-as-judge 校准报告 FNR=0.00、FPR=0.00，但金标仅 n=21（扩展 | 将补充标注者间一致性IRA,按rule of three报告0/21的95%上界约14%,不再声称零错误率。 | sustained | 作者concede承诺补IRA和上界,当前版本n=21单标注者零错误率宣称不可信仍存在 |
| 12 | Critical | - Critical: d_min=2.1279（Cohen's d>2 属极端效应）方在 80% power 下可检出 | 论文已披露'd_min=2.1279 at 80% power; McNemar power structurally  | partial | 论文确已披露功率限制且未做因果推断,但N=4结构性欠功效本身是基准设计缺陷,披露不消除 |
| 13 | Critical | - Critical: 三数据源(AIRS-Bench / ResearchClawBench / GAIA2 p3de | 将补充三数据源许可证、版本号、下载URL与再分发权声明。 | sustained | 作者concede承诺补充许可声明,当前版本三数据源无许可/来源/版本声明仍存在 |
| 14 | Critical | - Critical: 全文以点估计汇报均值（L2 goal completion 0.1418/0.1918/0.27 | 将为L2均值补充标准差/置信区间,并将精度降至2位小数。 | sustained | 作者concede承诺补CI降精度,当前版本N=4下4位小数虚假精度仍存在 |
| 15 | Critical | - Critical: 判官校验的 gold 数量在同句内冲突 — 先写"(21 gold, single annota | 将明确FNR/FPR分别在校准集21 gold与扩展集39 gold上的计算口径。 | sustained | 作者concede承诺明确口径,当前版本21与39 gold同句冲突未澄清仍存在 |
| 16 | Critical | - Critical: 双盲违规——正文显式泄露 "rule L047, an internal audit ident | 将删除'rule L047, an internal audit identifier'等内部标识符,替换为匿名化描述。 | sustained | 作者concede承诺删除内部标识符,当前版本rule L047泄露致双盲违规仍存在 |
| 17 | Critical | - Critical: 对 L1a 子集进行**事后挑选（post-hoc curated subset）**得到 p= | 将对post-hoc子集p值做多重检验校正,移至附录,摘要不再报告该p值。 | sustained | 作者concede承诺校正移至附录,当前版本post-hoc子集p值未校正仍构成无效推断 |
| 18 | Critical | - Critical: 引言称 L1b "scored by a heterogeneous LLM judge"，但摘 | 将修正引言措辞,明确L1b因全部execution failure致zero judge calls,judge校准仅为 | sustained | 作者concede承诺修正措辞,当前版本引言称judge评分与摘要zero judge calls直 |
| 19 | Critical | - Critical: 摘要出现 "frontier Model-F scored 6/6 (exploratory)" | 将在首次出现处定义Model-F（名称、来源、选择理由）,或从摘要移除。 | sustained | 作者concede承诺定义或移除,当前版本Model-F全文未定义仍在摘要出现 |
| 20 | Critical | - Critical: 缺配置快照——"rented cloud GPU"无 GPU 型号/提供商/驱动/CUDA 版本 | 将补充配置表:GPU型号/提供商/驱动/CUDA、Ollama版本、量化规格、采样参数、推理seed、权重哈希。 | sustained | 作者concede承诺补充配置表,当前版本缺GPU/框架/量化/采样/seed/权重哈希仍存在 |
| 21 | Minor | （另有 20 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 17 / Major 0 / Minor 0；撤回 0 条（假阳性被作者驳回）；部分成立 3 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
