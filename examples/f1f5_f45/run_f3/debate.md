# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f3\extracted_text.txt`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f3\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 7 / Major 12 （撤回 0，部分成立 1）；注：原始 21 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 1 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: 双盲合规风险：正文出现 `gates_config.json L10–L28`、`protoco | 将删除全部内部文件路径与行号（gates_config/protocol/results/analysis.json）, | sustained | 作者承认并承诺删除内部文件路径与行号；按规则concede一律维持,待修订。 |
| 2 | Critical | - Critical: 对照组不匹配：no-memory 与 memory 条件未控制上下文长度/注入内容量，appen | 将增加匹配 token/字符预算的 no-memory 基线,并报告 prefix-length 协变量与长度匹配后的稳 | sustained | 作者承认并承诺增加匹配token/字符预算的基线与prefix-length协变量分析；问题真实待修 |
| 3 | Critical | - Critical: 样本量报告自相矛盾：摘要写 24,000 单元、18,000 paired，贡献节却写 18,0 | 将统一 24,000/18,000/9,000 数字,明确定义 paired cell,并补充 power n=500  | sustained | 作者承认并承诺统一样本量数字并定义paired cell与power关系；concede成立。 |
| 4 | Critical | - Critical: 核心推断把 18,000/24,000 个“单元格”或 500 题当作独立样本，但同一 500  | 将按题目、模型、seed 建立混合效应/聚类稳健推断,报告聚类内相关与有效样本量。 | sustained | 作者承认并承诺按题目/模型/seed做混合效应或聚类稳健推断；concede成立。 |
| 5 | Critical | - Critical: 正文在贡献列表后混入内部工作流内容（“Claim ledger 86 PASS”“protoco | 将删除 Claim ledger、protocol.md、Gamma precursor 等流程用语,改写为正式方法/附 | sustained | 作者承认并承诺删除流程用语并改写为正式方法/附录；concede成立。 |
| 6 | Critical | - Critical: 证据链核心数字对不上——摘要称 24,000 cells（18,000 memory + 6,0 | 将统一对账公式:18,000 memory cell 与 6,000 no-memory cell 复用形成 18,00 | sustained | 作者承认并承诺统一对账公式并解释配对定义；concede成立。 |
| 7 | Critical | - Critical: 配对结构重复使用同一批 no-memory 样本（6,000 cells）与 3 个记忆条件配对 | 将共享 no-memory baseline 的跨条件相关性纳入模型,改用分层/宽格式配对分析并调整检验。 | sustained | 作者承认并承诺将共享no-memory非独立结构纳入模型；concede成立。 |
| 8 | Major | - Major: Γ=W1 的分布对象和量纲未明确，Γ=12.3 相对 ΔMAE=-0.034 的显著结果可能由极端值或 | 将明确定义 W1 的分布对象与单位,报告效应量、Γ/ΔMAE 分布图及去极值稳健性。 | sustained | 作者承认并承诺明确W1对象/单位并报告效应量与稳健性；concede成立。 |
| 9 | Major | - Major: “post-hoc calibrators reduced but did not eliminate | 将说明校准器在独立训练/验证集拟合、测试集评估,并补充 in-sample/out-of-sample 对比。 | sustained | 作者承认并承诺说明校准器独立拟合与in/out-of-sample对比；concede成立。 |
| 10 | Major | - Major: 仅 3 个低编号 seed，且“seed-pooled”是在 seed 42 之后补充 43/44 的 | 将预先注册 seed 与聚合规则（或明确 exploratory）,报告每个 model×seed 的完整分布与 per | sustained | 作者承认并承诺预注册seed或说明exploratory并报告per-seed分布；concede成 |
| 11 | Major | - Major: 图表层面混乱：正文出现“Panorama six-figure synthesis”，但全文没有规范的 | 将 Panorama six-figure 改为规范编号 Figure/Table,补充标题、图注与正文引用。 | sustained | 作者承认并承诺改为规范图表编号、标题、图注与正文引用；concede成立。 |
| 12 | Major | - Major: 多重比较控制不足：3 架构、4 模型、3 种子、4 个 post-hoc calibrator、6-g | 将对主结果与 θ sweep、calibrator、ablation 统一应用 Holm/FDR,并明确主要-次要检验层 | sustained | 作者承认并承诺统一应用Holm/FDR并明确检验层级；concede成立。 |
| 13 | Major | - Major: 摘要中“0.68% share”和“survey Wilson [0, 0.21] for 0/15” | 将删除摘要中无语境百分比,移至 Results 并定义 0.68% 与 0/15 的分子分母及结论关系。 | sustained | 作者承认并承诺删除无语境百分比并移至Results定义分子分母；concede成立。 |
| 14 | Major | - Major: 摘要中的 MAE 公式书写错误且术语不完整：“MAE = i |ci −yi|”缺少求和号、下标范围及 | 将改写为 MAE=(1/n)Σ_{i=1}^n |c_i−y_i|,明确定义 c_i、y_i、n。 | sustained | 作者承认并承诺改写MAE公式并定义变量；concede成立。 |
| 15 | Major | - Major: 数据许可与版本缺失——未指明 MMLU 的版本/来源/许可证、500 题的具体 ID 或抽样方式，也未 | 将补充 MMLU 版本/许可证、500 题抽样方式与题目 ID 清单,并说明衍生数据再分发许可。 | sustained | 作者承认并承诺补充MMLU版本/许可证、抽样与再分发许可；concede成立。 |
| 16 | Major | - Major: 方差报告不充分：仅报告 seed-pooled SD=0.026 和某些百分比的 Wilson CI， | 将报告各架构×模型的 paired ΔMAE 方差、Γ 的 bootstrap CI 与主效应置信区间。 | sustained | 作者承认并承诺报告方差、bootstrap CI与主效应CI；concede成立。 |
| 17 | Major | - Major: 校准器评估公平性：四个 post-hoc calibrator 未说明是否在独立验证集上拟合、在测试集 | 将在独立验证集拟合四个 calibrator,在测试集评估,并报告拟合/评估样本与 MAE。 | sustained | 作者承认并承诺独立验证集拟合、测试集评估并报告样本；concede成立。 |
| 18 | Major | - Major: 理论贡献 |ΔMAE| ≤ LΓ 是 |c−y| 作为 1-Lipschitz 函数下 Wassers | 我们已限定为 descriptive upper bound 并提供非退化条件与反例,贡献是刻画退化/过滤检索下失效边界 | partial | 论文确有非退化条件与反例,rebut部分成立；但核心上界仍属简单Lipschitz推论,定理级贡献质 |
| 19 | Major | - Major: 结构重复且越界：“Under review as submission to TMLR” 在摘要前后重 | 将删除重复的 TMLR 页眉,重构摘要/贡献/引言边界,将流程内容移至附录。 | sustained | 作者承认并承诺删除重复TMLR页眉并重构章节边界；concede成立。 |
| 20 | Major | - Major: 补充 θ sweep 与主结果未对齐：主文 θ=0.1 的 Γ=1.2，sweep 只给 8.1→0. | 将补充 θ sweep 中 θ=0.1 的 Γ 值,统一与主结果 1.2 的对账,并定义 conf 0.99。 | sustained | 作者承认并承诺补充θ=0.1的Γ值、统一对账并定义conf；concede成立。 |
| 21 | Minor | （另有 1 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 7 / Major 12 / Minor 0；撤回 0 条（假阳性被作者驳回）；部分成立 1 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
