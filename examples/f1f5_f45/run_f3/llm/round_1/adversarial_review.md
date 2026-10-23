# 对抗审查报告

- 时间: 2026-08-27T19:46:27.981690+00:00
- 源: F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f3\extracted_text.txt
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（3）
- - Critical: 前提/内部效度：三种记忆条件并不只改变“记忆架构”，还同时改变了注入内容长度、信息量、提示位置、检索阈值、摘要生成过程等；append-only 与 RAG 的差异可完全由上下文长度或信息泄露解释，不能归因于架构本身。
- - Critical: 配对结构重复使用同一批 no-memory 样本（6,000 cells）与 3 个记忆条件配对成 18,000 对，造成跨条件非独立比较；若不按题目/模型/seed/no-memory cell 建模相关性，检验的样本量和 p 值会被系统性高估。
- - Critical: 因果推断不恰当：虽然标题用“associated”，但“controlled comparison”“we observed”及对 p 值的解释仍把观测关联表述为记忆架构的效应；在未控制记忆内容是否泄露答案、上下文长度、模板差异和检索语料构建方式时，无法排除混淆变量。
### Major（6）
- - Major: 有效样本量远低于表面数字：500 题、4 模型、3 seeds 是分层/聚类数据，不能把 24,000 cells 当独立样本；缺少 mixed-effects 或 cluster-robust 推断，主结论的显著性可能被严重夸大。
- - Major: 仅 3 个低编号 seed，且“seed-pooled”是在 seed 42 之后补充 43/44 的做法，存在事后分析/选择痕迹；应预先注册 seed 与聚合规则，并报告每个 model×seed 的完整分布而非只给 pooled SD。
- - Major: θ=0.1 是主分析阈值，而补充 θ sweep 显示 Γ 随 θ 单调变化；若 θ 是事后挑选的“有利”值，则主结论有 cherry-picking 风险，需预先固定或对 θ 做联合敏感性检验而非单独报告。
- - Major: “post-hoc calibrators reduced but did not eliminate”未说明校准器是否在独立训练/验证集上拟合；若在同一批数据上拟合再评估，会低估校准后的误差，不能支持“无法消除 shift”的结论。
- - Major: 定理 |∆MAE|≤LΓ 依赖 Lipschitz 常数、non-degeneracy 和配对耦合等假设，但文中未验证这些条件；θ sweep 中“uninformative verbalized confidence”可能正说明存在退化分布，使 Γ 与上界失效。
- - Major: 500 道 MMLU 题的选取标准、学科分层、模型版本与解码参数、记忆注入语料的构造方式均未交代；这既影响外部效度，也可能因子集选择造成内部效度问题。
### Minor（1）
- - Minor: MAE 与 Γ 的单位和定义不清晰（ci 是 0-1 概率还是百分数、Γ=12.3 是 0.123 还是 12.3%、W1 是在什么配对/前缀对象上计算），影响结果解释与可复现性。

## 统计（stat）— ok
### Critical（2）
- - Critical: 核心推断把 18,000/24,000 个“单元格”或 500 题当作独立样本，但同一 500 题被 4 模型×3 种子×3 架构反复复用；未按题目、模型、种子做聚类/混合效应建模，p 值和置信区间会严重低估不确定性。
- - Critical: 样本量报告自相矛盾：摘要写 24,000 单元、18,000 paired，贡献节却写 18,000 单元、9,000 paired；无法确认配对定义和有效独立样本量，power analysis 的 n=500 与这些单元数之间的关系也不清楚。
### Major（4）
- - Major: Γ 的 p 值是分别对 append-only 和 RAG 检验 Γ=0，没有报告或检验两架构之间 Γ 差异（或架构×配对交互），不能由“一个显著、一个不显著”推出两架构效应不同。
- - Major: 多重比较控制不足：3 架构、4 模型、3 种子、4 个 post-hoc calibrator、6-group ablation、θ sweep 均涉及多次检验，全文只在 ablation 处提到 Holm，主结果未说明是否控制多重比较。
- - Major: 效应量报告不完整：只给出原始 Γ 和 ∆MAE，没有标准化效应量（如 Cohen’s d、η²）和主效应 ∆MAE/Γ 的 95% CI；Γ 非负且随样本规模变化，原始数值不能直接解释效应大小。
- - Major: 方差报告不充分：仅报告 seed-pooled SD=0.026 和某些百分比的 Wilson CI，未报告各架构/模型的 paired ∆MAE 方差、题目间相关、W1 的抽样方差或主效应的置信区间。
### Minor（3）
- - Minor: MAE 公式写为 `MAE = i |ci−yi|` 未说明是否求和、均值、是否除以 n，也未定义 ci/yi 的具体量纲；否则 ∆MAE 会随问题数缩放而不可比较。
- - Minor: θ sweep 只用 0.05/0.1/0.3 三个点宣称“Γ monotonic 8.1→0.9”，没有置信区间或趋势检验，且“conf 0.99”表述含糊。
- - Minor: 只有 3 个种子，“seed-pooled SD”不能可靠估计 seed 随机效应，也不能作为模型或种子层面不确定性的充分替代。

## 实验（experiment）— ok
### Critical（2）
- - Critical: 对照组不匹配：no-memory 与 memory 条件未控制上下文长度/注入内容量，append-only 天然比 RAG 前缀更长，Γ 与 ΔMAE 可能反映 token 预算或 prefix length 而非记忆架构本身。
- - Critical: 配对统计不独立：18,000 memory 单元只共享 6,000 个 no-memory 基线（3 个记忆臂共用一个基线），若按独立配对做检验会虚增有效样本量、低估 p 值；需按 question/model/seed 聚类或建多水平模型。
### Major（5）
- - Major: 超参数公平性不足：RAG 仅用 TF-IDF θ=0.1，未做主实验超参搜索；summarization 的摘要模型、压缩率、更新策略、检索 top-k/chunk 大小均未报告，也没有保证三个架构的 token 预算或计算量可比。
- - Major: 消融不完整：所谓 6-group ablation 未交代分组内容，缺少检索阈值、摘要长度、记忆容量、记忆顺序、注入轮数、matched-length append-only 等组件级消融，无法把效应归因到“架构”而非某个实现细节。
- - Major: 校准器评估可能泄漏：four post-hoc calibrators 未说明是否在独立校准集拟合、独立测试集评估；若在同一个 500 题上拟合并报告“reduced but did not eliminate”，结果会偏乐观且不具公平性。
- - Major: seed 管理不足：仅 3 个固定 seed（42/43/44），未报告 per-seed 结果或 seed×condition 交互；seed 同时影响记忆生成与答案采样时，pooled SD 0.026 会掩盖条件内 seed 波动，也无法评估跨 seed 泛化。
- - Major: 泛化证据有限：所有结论来自 synthetic memory-injection 且仅 MMLU 500 题、4 个本地模型，无真实 agent 轨迹、无其他任务/领域/OOD 验证；“sample-descriptive”免责声明不能替代外部效度检验。
### Minor（3）
- - Minor: 基准公平性：MMLU 是公开基准，未报告 500 题子集的抽样/分层方式，也未做 contamination/记忆化检查；模型可能见过题目，导致记忆架构效应被记忆答案混淆。
- - Minor: θ sweep 证据薄弱：0.05/0.1/0.3 各 500 cells 可能仅单 seed，且报告“uninformative verbalized conf”意味着该 sweep 的 Γ 单调趋势未必能支持主结论。
- - Minor: 多重比较与功效：主比较 3 个记忆臂未明确做多重比较校正，power 分析使用任意 d=0.35，且共享基线使有效 N 低于表面 18,000，需重新说明功效。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 声称“memory design 与 confidence error 的关系从未在受控配对协议下检验”不成立：RAG 噪声/检索对 verbalized confidence 的影响已被 NOVA、Do RALMs Know When They Don't Know、REHEARSE、Agentic Confidence Calibration 等研究覆盖，本文只替换了“配对 ΔMAE”这一测量细节，并未打开新的 GAP。
- - Critical: “agent memory architecture”名不副实：实验只是 MMLU 单题上注入 synthetic memory/retrieval 上下文，没有真实 agent 轨迹、写入/压缩/检索循环或多轮交互，与已有 agentic memory/calibration 工作的差异被显著夸大。
### Major（2）
- - Major: 理论贡献 |ΔMAE| ≤ LΓ 是 |c−y| 作为 1-Lipschitz 函数下 Wasserstein 上界的直接推论，属于已知 Lipschitz/Wasserstein 性质的平凡应用；文中还给出反例与退化条件，进一步说明该 bound 不足以支撑“定理”级别的贡献。
- - Major: 实证增量很弱：append-only Γ 显著但 ΔMAE 仅 −0.034，RAG Γ 不显著，且 θ sweep 自述 verbalized confidence “uninformative”，因此结果主要说明置信分布移动，而非记忆架构系统性改变校准误差，“较大 shift”的贡献被包装。
### Minor（2）
- - Minor: Related work 以“没有人测过 paired ΔMAE”作为 GAP 是 strawman；已有 prompt/context/retrieval 扰动下的校准研究（Zhao et al., 2021; Ovadia et al., 2019; RAG calibration）已覆盖同类现象，本文缺乏对这些工作的机制或因果区分。
- - Minor: 范围过窄（500 MMLU、4 个本地模型、单一 TF-IDF θ、synthetic memory），且共享 no-memory baseline 可能被重复计入 paired cells，贡献 1 中的配对规模被夸大。

## 可复现（repro）— ok
### Critical（3）
- - Critical: 证据链核心数字对不上——摘要称 24,000 cells（18,000 memory + 6,000 no-memory；18,000 paired），贡献节却写 18,000 cells（9,000 paired），且 18,000 memory 与 6,000 no-memory 如何形成 18,000 个配对未解释，无法对账实验规模。
- - Critical: 哈希对账完全缺失——未提供 results/analysis.json、原始日志、MMLU 500 题子集、gates_config.json、claim ledger 的 SHA-256/commit hash，任何“Gates 9/9”“86 PASS”都无法独立校验。
- - Critical: 一键复现未提供——没有公开代码仓库、commit hash、Dockerfile/requirements.lock、可执行脚本或 notebook，仅称“archived in results/analysis.json”不足以在任何新环境复现。
### Major（4）
- - Major: Seed 信息不完整——只列了 42/43/44，却出现“single-generator (seed 42)”这一未展开概念；MMLU 子采样、记忆内容生成、检索、解码、后处理的 seed 映射均未逐环节记录，无法重建同一生成轨迹。
- - Major: 数据许可与版本缺失——未指明 MMLU 的版本/来源/许可证、500 题的具体 ID 或抽样方式，也未说明衍生日志和分析文件的再分发许可，复现与合规均存障碍。
- - Major: 配置快照不足以固定实验——模型具体名称/量化/权重版本、prompt 与 memory 注入模板、summarization 方法、TF-IDF 的 tokenizer/stopwords/θ 语义、采样 temperature/top-p 等关键配置未随快照给出。
- - Major: 统计定义与代码不可复现——Γ=W1、MAE 公式（缺少 1/n 或离差写法）、paired ∆MAE、四类 post-hoc calibrator、θ sweep 的 conf=0.99、Wilson CI 样本来源等没有精确公式、超参和可执行代码，p 值无法重算。
### Minor（2）
- - Minor: 内部行号引用不稳定——protocol.md L42–L58、gates_config.json L10–L28、Appendix B L210–L235 依赖未版本化文件行号，改行即失效；彩色 ledger 也没有机器可读等价物。
- - Minor: “sample-descriptive”声明不能替代复现材料——未提供数据字典、缺失值说明、逐 cell 输入输出样例和失败日志，读者无法判断哪些 cell 被排除或重跑后应得到什么。

## 写作（writing）— ok
### Critical（3）
- - Critical: 摘要与贡献列表的核心数字互相矛盾：摘要称 24,000 cells（18,000 memory + 6,000 no-memory / 18,000 paired），贡献 1 却称 18,000 cells（9,000 paired），读者无法判断实际实验规模。
- - Critical: 理论贡献表述不一致：贡献 2 称定理为 |ΔMAE| ≤ Γ，摘要却写成 |ΔMAE| ≤ LΓ，且 L 未定义；这不仅是用词不一致，而是数学声明不一致。
- - Critical: 正文在贡献列表后混入内部工作流内容（“Claim ledger 86 PASS”“protocol.md L42–L58”“gates_config.json”“Gamma precursor strings (24K→12K)”），这些不是论文写作语言，严重破坏 TMLR 稿件结构和可读性。
### Major（5）
- - Major: 摘要塞入了不应出现在摘要的实现细节与无上下文统计：Gates 9/9、Wilson CI [0.52, 0.84]% / [0, 0.21]、results/analysis.json、gates_config.json L10–L28，结构上严重失衡。
- - Major: 摘要中的 MAE 公式书写错误且术语不完整：“MAE = i |ci −yi|”缺少求和号、下标范围及 ci/yi 的定义，作为核心指标定义不可读。
- - Major: 术语不统一：“models”与正文“local families”混用，摘要的 “θ sweep”与正文 “θ=0.1” 的阈值关系也未显式衔接。
- - Major: 图表层面混乱：正文出现“Panorama six-figure synthesis”，但全文没有规范的 Figure/Table 编号、标题或正文引用；“six-figure”含义不明，违反论文图表写作规范。
- - Major: 摘要中“0.68% share”和“survey Wilson [0, 0.21] for 0/15”完全没有前置语境，读者不知道这是在描述什么结果，也看不出与主要结论的关系。
### Minor（2）
- - Minor: “conf”作为 “confidence” 的缩写未定义，摘要中 “uninformative verbalized conf” 表述模糊。
- - Minor: 语法/表达瑕疵：“their effect ... remain unstudied”主谓不一致；“hedges”过于口语化，不适合正式学术写作。

## 伦理（ethics）— ok
### Critical（1）
- - Critical: 若摘要中的“survey ... 0/15”涉及人类受试者评估，论文未报告 IRB/伦理审批、知情同意、匿名化与数据保留条款，可能直接违反涉及人类参与研究的合规要求。
### Major（3）
- - Major: 盲审材料直接引用内部文件名和行号（results/analysis.json、gates_config.json L10–L28、protocol.md L42–L58），且未说明补充材料已剥离作者元数据、绝对路径、仓库 URL 与系统用户名，存在破坏双盲匿名性的风险。
- - Major: 未交代 MMLU 及其底层第三方考试题目、四个 local model 权重的许可证与再分发条款；发布 500 题子集、全量日志或配置快照可能涉及原始题目版权和模型权重许可合规问题。
- - Major: 缺少 broader-impact/misuse 声明；记忆架构对 verbalized confidence 的影响可被用于操纵模型自信度或在不安全场景中过度信任 agent，“sample-descriptive”这一限定不足以防止结果被误用或过度外推。
### Minor（2）
- - Minor: 未披露利益冲突、资助来源或机构关系；匿名稿件中仍可提供不含作者身份的通用 COI/伦理声明。
- - Minor: 隐私边界不清晰：未说明 synthetic memory 是否模拟或包含个人数据、发布日志是否可能泄露提示词、模型记忆化文本或敏感信息，以及是否做了 redaction。

## 汇总

- **Critical: 16 | Major: 29 | Minor: 15**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）