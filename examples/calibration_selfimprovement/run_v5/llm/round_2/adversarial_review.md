# 对抗审查报告

- 时间: 2026-08-28T05:16:39.223812+00:00
- 源: F:\deepseek\papers\calibration-self-improvement\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（2）
- - Critical: 逐行裁决后扩展 matcher 至 100% 准确率，是在看到模型输出后修改标签/评分规则，属于标签泄漏与事后拟合；ECE 降至 0.0037 不能证明模型校准变好，只能说明评分标准被拟合到了当前样本。
- - Critical: 没有独立于模型输出的金标准或留出集；“语义正确”判定与所有 matcher 对比都在同一批样本上构造，因此“matcher determines calibration”这一核心结论无法与标签集后验选择区分。
### Major（5）
- - Major: 用“平均置信度 0.9963 vs 准确率 86.7%”的边际比较宣称 overconfidence 消失并不成立；校准是联合分布性质，均值相等也不代表逐点校准良好，且该数字本身仍显示约 13 个百分点的差距。
- - Major: N=30 且 27/30 的置信度恰为 1.0 的退化分布，不足以支撑 ECE 数值比较、温度缩放鲁棒性判断或 Proposition 8' 的经验验证；缺少置信区间、置换检验或敏感性分析。
- - Major: 跨域 ECE 比较混淆了领域、题目难度、模型、样本量及同一题目在多模型间的重复测量依赖；Holm 校正后仅极端配对显著，却得出“calibration is domain-specific”的宽泛结论，内部效度不足。
- - Major: OOD-gating 分析为 N=30 的探索性相关证据，却表述为“confidence may be harmful for gating”；没有操纵变量或随机分配，也未排除 domain shift、模型、难度和 matcher 等混淆，负相关条件可能只是选择效应。
- - Major: MSI 的 free-form vs MMLU 比较不是受控协议对比；标签空间、题目内容、模型、匹配器和评分标准同时变化，不能把 MSI 差异归因于 protocol。
### Minor（2）
- - Minor: 形式化界假设 matcher 的 FNR/FPR 与模型 confidence/输出独立或非差分，但该假设未验证；若标签噪声随置信度或答案内容变化，bias bound 和 MSI 可能失效。
- - Minor: self-consistency 仅基于三次重采样，同一性测量受采样种子和温度影响，未报告稳定性或重复性，作为 gating 替代方案的证据较弱。

## 统计（stat）— ok
### Critical（2）
- - Critical: 判定准确率/校准的核心结论来自同一份 N=30 数据：先用逐行 adjudication 事后扩展 matcher，再在同一批样本上报告 100% accuracy 与 ECE=0.0037，标签和评估标准已被结果“拟合”，这是循环评估，不能作为独立统计证据。
- - Critical: 置信度分布严重退化（27/30 个值恰为 1.0），有效非退化样本仅 3 个，任何 ECE/校准估计的方差都会极大；但摘要仍以 0.363、0.1297、0.0037 等精确数值比较，且未报告这些估计的置信区间或有效样本量，定量结论不可靠。
### Major（4）
- - Major: “4999 pairs / 600 items / 9 models”存在明显非独立性：同一题目被多个模型重复回答、同一模型贡献大量回答；若按 pair 独立计算 95% CI，会低估标准误，可能把领域/模型差异误判为显著，需按题目或模型进行聚类/混合效应分析。
- - Major: 只写“only extreme Holm-corrected pairs significant”，未报告比较了多少个配对、检验统计量、原始/校正后 p 值、效应量及各领域/模型子样本量；无法区分“真的无差异”和“功效不足”，且事后挑选 extreme pairs 本身有选择性报告风险。
- - Major: 用“ECE 最多变化 4 倍/0.45 绝对差异”但未附差异的 CI 和效应量；ECE 接近 0 时倍数会被夸大，且若 ECE 依赖分箱方案，跨域 ECE 比较可能反映 binning 伪像而非真实校准差异。
- - Major: OOD gating 分析仅 N=30，且“40–50% 高置信 OOD 答案错误”的子集更小，未给 Wilson/Clopper-Pearson 区间；该样本量不足以支持“confidence harmful for gating”或“self-consistency removes overconfident OOD”的结论。
### Minor（2）
- - Minor: MSI 的 1.000 vs 0.334 未报告不确定性、样本量差异及离散/退化分布下的饱和效应；1.000 可能只是小样本或全同值导致的伪完美值。
- - Minor: 对 Holm 校正后不显著的结果缺少正确解读：不显著不等于两组 ECE 相等，应补充等价性检验（如 TOST）或明确的最小可检测差异，否则容易把“未检测到差异”误读为“无差异”。

## 实验（experiment）— ok
### Critical（2）
- - Critical: “matcher extended after per-row adjudication” 是在同一批评测样本上既构造/扩展匹配器又报告 100% 与 ECE=0.0037，属于标签泄漏/样本内过拟合，不能作为有效校准证据。
- - Critical: OOD gating 分析仅 N=30、未预先定义 OOD 分布、未给出置信区间或功效分析，40–50% 高置信错误率和 self-consistency 优势的结论不足以支撑文末部署建议。
### Major（6）
- - Major: 缺少对照组：没有随机猜测、恒为 1.0 的退化基线、无 gating 基线或标准校准方法（如 held-out temperature scaling）作为比较，无法判断 ECE 差异和“confidence harmful”的真实增量。
- - Major: seed 管理缺失：未见任何 seed、重复采样次数或跨 seed 方差报告，模型生成、resample、bootstrap 与 matcher 判定均可能受随机性主导。
- - Major: 超参数不透明：self-consistency 的 3 次 resample 未说明 temperature、decoding 策略、max tokens、prompt 模板和采样 seed，也没有对这些超参数做敏感性分析。
- - Major: 消融不完整：三种 matcher 不是系统消融，容错规则、阈值、FPR/FNR 权衡没有独立变化；per-row adjudication 既无独立验证集也无多人判定的一致性指标，无法分离 matcher 效应。
- - Major: 基准公平性不足：MMLU 从 300 项/4 模型扩展到 600 项/6 域/9 模型的选择标准、条目去重、域内条目均衡、模型版本与 prompt 控制均未交代，跨域比较可能反映数据构成而非模型校准。
- - Major: 泛化证据薄弱：校准结论基本来自 MMLU 多选题加单一 free-form 协议，没有 held-out 任务、分布偏移或新领域验证；“in-sample, illustrative”本身已承认缺乏泛化支撑。
### Minor（1）
- - Minor: 30 条样本出现 27 条置信度恰为 1.0，退化分布使任何 binning 类指标都高度不稳定，但文中未报告该 30 条样本的构成和选择方式。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 核心发现“matcher 决定校准测量”并非新事实：已有文献（如 Linguistic Calibration of Long-Form Generations 等）已明确指出 exact/string match 会把语义等价答案误判为错误，并用 semantic equivalence 改进 LLM 校准评估；将其包装成新的“matcher-dependence 理论”夸大了增量贡献。
- - Critical: “per-row adjudication 后扩展 matcher 得到 100% accuracy / ECE 0.0037”是事后根据模型输出构造标签的循环论证；这个结果只能说明匹配器可以被人为调到完美，不能作为“标签裁决应先于校准声明”的经验证据，也不能当作校准结果报告。
### Major（4）
- - Major: Proposition 1–3 的 matcher bias bound 本质上是 FNR/FPR 重参数化的定义式变形，只形式化了“标签变了 accuracy 和 ECE 就会变”这一显然事实，没有产出可证伪的新预测或新的评估设计准则。
- - Major: binning-based ECE 不可靠、退化置信分布需要 binning-free/adaptive 指标已是较成熟问题（如 Revisiting the Calibration of Modern Neural Networks 等工作）；smECE_sem 缺少与既有 adaptive CE、binning-free 估计量在偏差、方差和样本量上的直接比较，无法支撑“新估计器”的新颖性。
- - Major: 跨域“domain-specific calibration”的证据自相矛盾：摘要承认只有极端 Holm 校正对显著，却用未校正的“最多 4×/0.45 绝对差”作主要卖点；且 matcher/protocol 本身可能才是差异来源，不能据此断言领域效应真实存在。
- - Major: OOD gating 分析只有 N=30，且 self-consistency 优于 verbalized confidence/阈值门已被 Self-Consistency Boosts Calibration 等现有工作覆盖；当所有置信度都是 1.0 时“阈值门无信息”是平凡结论，不足以构成 Proposition 8′ 级贡献。
### Minor（2）
- - Minor: MSI 作为新指标仅报告两个协议值（1.000 vs 0.334），没有分布、置信区间、与既有一致性/可靠性指标的相关性或消融，无法判断其诊断增量是否真实。
- - Minor: “600 items、9 models、4999 pairs”的跨域语料缺少随机抽样和领域代表性论证，且多数领域差异不显著，样本功效不足以支撑“domain-specific”与“matcher-independent”的强结论。

## 可复现（repro）— ok
### Critical（5）
- - Critical: 全篇未声明任何随机种子（LLM 采样、三次 resampling、bootstrap 均无 seed），因此 4999 对/ECE/MSI 等数字无法精确重跑。
- - Critical: 缺少配置快照：模型版本、API 端点、温度、top-p、max_tokens、提示词模板、系统提示等均未给出，无法按同一配置复现。
- - Critical: 三类 matcher（exact、tolerant、extended）没有可执行代码、规则阈值或版本号，匹配与标注的核心证据链不可审计。
- - Critical: “per-row adjudication 后扩展 matcher”是事后人工改标签流程，且未提供标注协议、双盲性、变更行清单或哈希，100% 准确率无法独立复现。
- - Critical: 未提供一键复现入口：无代码仓库、Dockerfile、环境锁文件、固定依赖版本或端到端运行命令。
### Major（4）
- - Major: MMLU 子集缺少具体 item IDs、数据集版本、来源 URL、下载时间与内容哈希，300→600→4999 的扩展示例数据无法对账。
- - Major: 数据与模型许可仅在未展示的附录中被声称，没有实际许可证名称、条款链接或下载方证明，合规声明不可验证。
- - Major: 原始模型输出、匹配后标签、中间指标与最终 ECE/MSI/gating 结果之间没有日志链或校验和，无法从原始证据重算出论文数字。
- - Major: N=30 的 OOD gating 探索未提供原始数据、resample 参数和筛选条件，40–50% 高置信错误与自洽性去误报的结论不可复现。
### Minor（1）
- - Minor: 95% CI 的构造方法未说明（bootstrap 次数、分层方式、随机种子），统计不确定性无法精确重算。

## 写作（writing）— timeout
### Critical（1）
- - Critical: 摘要“single-model ECE varies up to 4× across subjects”与扩展 600 项正文/表 5（sig600）最高 17.1× 直接矛盾；同一句里把 300 项的 4× 和 600 项的 0.45 绝对差混在一起，读起来像扩展集也只有 4×。
### Major（8）
- - Major: 图 6（census_domains）图注称“roughly 4×”，但紧随其后的例子 Qwen2.5-1.5B 0.410 vs 0.041 是 10×，且表 4 又标注该模型的 matcher-scope ECE 不可靠，图注却把它当证据。
- - Major: 摘要称“confidence 与 consistency 负相关时 self-consistency removes overconfident OOD answers”，但正文/表 12 中 Qwen2.5-3B 的 ρ=-0.18 时 consistency gate 的 hi-conf 与基线同为 0.73，并未下降；摘要把单模型现象过度泛化。
- - Major: 正文残留审稿/回复痕迹：Method 中“G5: kernel integrates to 1…”，Limitations 中“R19 human gold…”“R24 addresses…”，均不应出现在正式论文里。
- - Major: 引言硬编码“\S6 Discussion”错误：按实际章节顺序 Discussion 是第 7 节，且硬编码小节号在改稿后极易失效。
- - Major: 摘要声称“95% CIs; only extreme Holm-corrected pairs significant”，但对应的 Table 5 及正文均未呈现任何 CI、Holm 校正 p 值或哪些 pair 显著，表注与摘要承诺不一致。
- - Major: 表 11（frontier）脚注写“n=48/domain”，但正文和表题都说明 48 个 MMLU items 来自 4 domains（12/domain），数字口径明显写错。
- - Major: 正文称“holdout ceiling rates are 0.80–0.93 for the Qwen models”，但表 7 中 Qwen2.5-1.5B 的 holdout/main ceiling 是 0.167/0.222；应限定为 Qwen2.5-7B/3B 或在表中说明排除理由。
- - Major: 摘要和正文反复称“initially alarming overconfidence signal (mean confidence 0.9963 vs. 86.7%)”，但“初始”的 exact-string 匹配是 63.3%，86.7% 已是第一个 tolerant matcher 后的读数；叙事与数字阶段的对应关系混乱。
### Minor（5）
- - Minor: 未编号的“Our central finding…”段落在 Introduction 前首次使用 $\mathrm{smECE}_{\mathrm{sem}}$，但该符号此时尚未定义或展开，属于结构/术语问题。
- - Minor: 标题和摘要使用“Degenerate Distributions”，但 27/30 为 1.0 另有 3 个非 1 值时正文又改用“near-degenerate”；术语应统一为严格/近似退化，避免读者理解为严格点质量分布。
- - Minor: 摘要/引言写 MSI“0.334 MMLU”，但扩展表 5 中同一 Qwen2.5-7B 的 MSI 是 0.330；若分别来自 300 项与 600 项样本，应在摘要或表中标注样本量，否则读者视为数值打架。
- - Minor: 表 12（OOD gating）没有 baseline hi-conf 列，正文却使用“0.70→0.64”“0.73→0.92”等基线数字；读者无法从表内验证这些关键变化。
- - Minor: 摘要使用“Propositions 1–3”“Proposition 8′”这类内部编号引用，既未在摘要中解释 prime 含义，也让摘要读起来像结果清单而非独立概述。

## 伦理（ethics）— ok
### Major（4）
- - Major: 数据集许可不可验证：摘要称数据许可/模型条款在附录中声明，但正文可见部分未给出 MMLU 及扩展 600 项数据的具体许可、是否允许再分发/衍生、以及九家模型提供方是否允许该评测用途，无法据此确认合规。
- - Major: 模型条款与利益冲突缺失：未披露九个模型的具体版本、供应商、评测是否符合各自服务条款，也未声明作者与模型厂商/云厂商的资助、雇佣或持股关系；匿名投稿下利益冲突应显式说明。
- - Major: 人工 adjudication 伦理不透明：“per-row adjudication”若涉及人工标注/裁决，未说明标注者知情同意、报酬、标注指南、IRB/伦理审批或数据去标识化；若纯自动则需明确声明无人类数据。
- - Major: 误用风险未约束：论文提出用一致性信号做 OOD gating，却未给出高风险场景的禁用边界、人工监督要求或失败模式说明；探索性 N=30 的结论易被过度泛化为可部署的安全门控。
### Minor（2）
- - Minor: 双盲匿名细节：可见版本含 “TMLR double-blind / camera-ready” 占位符与示例邮箱，若提交时未清理可能泄露投稿流程信息；应确保所有自引、致谢和数据来源均已匿名化。
- - Minor: 隐私与数据保留：MMLU 为公开基准，暂无明显个人数据，但扩展语料若包含模型输出或用户提示，应明确不含 PII 并说明存储、保留和删除策略。

## 汇总

- **Critical: 14 | Major: 35 | Minor: 15**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）