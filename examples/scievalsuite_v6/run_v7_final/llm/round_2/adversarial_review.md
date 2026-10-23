# 对抗审查报告

- 时间: 2026-08-27T08:26:08.160317+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（2）
- - Critical: 样本量根本性不足（L2 N=4、L1a N=6、L1b N=10），远低于任何可靠推断所需最低；论文承认 McNemar 功效"structurally 0"却仍报告 L2 描述性均值（0.1418/0.1918/0.2750）并将其呈现为有信息量的结果，制造虚假精确性（false precision）。
- - Critical: L1b 全面地板效应（0/10 for all models，10/16 tasks 全零）使 Friedman 检验实质无效——全零任务的秩不携带任何区分信息，p=0.37 反映的是噪声而非"无差异"，该检验在此数据上不满足适用前提。
### Major（8）
- - Major: Gemma L1a 主结果使用三试最优（1/6→2/6）作为标题数字，而 intention-to-treat 均值（0.355，含失败试次计 0）被降级叙述——这是选择性报告/winner's curse；按方法论规范，ITT 应为主分析，best-of-three 需多重比较校正。
- - Major: 事后精选 L1a 6-task 子集得到 p=0.003 是典型的 garden-of-forking-paths 违规；无论标注"exploratory"与否，事后子集选择已使该 p 值的频率派解释失效，因为选择空间未被纳入 family-wise error 控制。
- - Major: LLM-as-judge 校准（FNR=0.00、FPR=0.00）基于 21 gold、单一标注者，且实际运行零 judge 调用（all SKIP）——校准在 vivo 中从未被行使，inter-annotator reliability 未知，零误判率在如此小样本上置信区间极宽，不能作为有效 guarantee。
- - Major: A 臂与 CG 臂在三个模型上 L2 均值完全相同，说明处理变量（harness 类型）未产生可观测效应——要么操纵失败（manipulation failure），要么存在未识别混淆变量抵消了处理效应，arm 比较的内部效度不成立。
- - Major: 核心混淆变量未控制：三个模型分属不同家族（Qwen vs Gemma）、不同参数量（7B/9B/14B）、可能不同量化与服务配置；观测到的分数差异无法因果归因于任一单一因素（如"科学推理能力"），模型间比较的因果推断不恰当。
- - Major: "positive control demonstrates pipeline solvability"与 L1b 全模型 0/10 矛盾——若管线可解却普遍失败，benchmark 可能测量的是执行机制/工程适配能力而非科学推理，构念效度（construct validity）受威胁。
- - Major: "answer-fitting audit intercepting 3/3 models"表明所有模型的测量分数可能反映 gaming 行为而非真实能力，这构成对分数解释的系统性混淆，但论文未将此纳入分数效度的因果分析。
- - Major: frontier Model-F 6/6（exploratory）为单一数据点、无 seed 重复、无统计处理，却作为比较锚点嵌入结果叙述，可能不当锚定读者对"能力梯度"的因果预期。
### Minor（3）
- - Minor: SHA-256 字节级可复现性与 recomputation 通过被等同于测量有效性；可复现性是必要非充分条件，不保证 benchmark 测量的是目标构念（scientific reasoning），二者在叙述中被混淆。
- - Minor: 1000-call 预算上限被叙述为"budget-controlled"特性，但该约束是导致统计功效不足的直接设计原因；将其正向框架（feature）掩盖了功效-成本权衡的方法论代价。
- - Minor: 三层能力（prediction/workflow/execution）覆盖"scientific agent"构念这一前提未经独立验证；将 code generation+execution 等同于"scientific prediction capability"是未检验的构念假设。

## 统计（stat）— ok
### Critical（4）
- - Critical: Friedman 检验称"16 个配对任务"，其中 10 个为全零 L1b 任务；全零任务零方差、无判别信息却被计入 Friedman 分母归一化，等于用无信号数据充数放大名义 N，应仅对 6 个有变异任务检验或分层处理。
- - Critical: 事后精选 L1a 子集（6 任务）得 p=0.003 属子集选择偏倚/数据 dredging；未对该族系做 Bonferroni/Holm/FDR 校正，若按已尝试的若干子集做校正即丧失显著性，标签"exploratory"不豁免推断风险。
- - Critical: 全文以点估计汇报均值（L2 goal completion 0.1418/0.1918/0.2750 精确到 4 位小数）却无标准差/标准误/置信区间；N=4 下不确定性极大，4 位小数为虚假精度。
- - Critical: d_min=2.1279（Cohen's d>2 属极端效应）方在 80% power 下可检出，表明 N=4 配对比较结构性欠功效、无法检测任何现实效应量；"披露"不等于"可推断"。
### Major（4）
- - Major: LLM-as-judge 校准仅 21（后扩 39）金标、单标注者，FNR=FPR=0.00 未报告置信区间；n≈20 时零错误率的 Wilson 下限远高于 0，且无标注者间一致性（κ/Cohen's）。
- - Major: L1a gemma 做 3 次独立试验后 1/6→2/6，未说明是否取最优；多重试验未校正，与 ITT 均值 0.355 并置易误导读者选择性解读。
- - Major: 跨 3 层 × 3 模型 × 多指标 + 事后子集构成多重比较家族，全文未见族系错误率控制；Nemenyi+CD 亦未报告实际 CD 值与秩均值。
- - Major: 协议声明 Wilcoxon+CLES、Friedman+Nemenyi+CD，但摘要结果仅给 p 值，未报告对应效应量（CLES/CD/秩均值/Cliff's δ），违反"p 值须配效应量"的报告规范。
### Minor（2）
- - Minor: L2 两臂 N=4、n_d=0 不一致对，McNemar 功效结构性为 0，却仍以 3 模型×2 臂完成率均值横向呈现"趋势"，在零信息条件下诱导读者读出排序。
- - Minor: 补充集 N=8 同样 n_d=0，主文已声明无效后补充集无统计增量，应明确标注无推断价值而非作为佐证陈列。

## 实验（experiment）— ok
### Critical（4）
- - **Critical**: L2 两臂(A=ReAct vs CG=completion-guided)在 N=4 和 N=8 补充中均产生完全相同的均值(0.1418/0.1918/0.2750)，n_d=0 discordant pairs，核心消融/对照实验彻底无效——CG 干预没有任何可观察效应，整个 L2 对比毫无统计信息量。
- - **Critical**: gemma2:9b 在 L1a 上获得三次独立试验(1/6â2/6)，而 7b、14b 仼似单次试验；不同模型获得不同试验/种子次数，是基准公平性的根本违规，无法做跨模型对比。
- - **Critical**: 全套 Friedman 非显著(p=0.37)后，事后筛选 L1a 子集(6 任务)得到 p=0.003，是典型的 garden-of-forking-paths / p-hacking；即便标注"exploratory"，将它与确证性结果混在同一摘要中本身就是误导。
- - **Critical**: 研究严重 underpowered：L2 的 N=4、d_min=2.13(Cohen's d>2 为巨大效应)、McNemar 功效结构性为 0；在此功效下，"无显著差异"与"无法检测差异"不可区分，所有阴性结果都无法解释。
### Major（6）
- - **Major**: L1b 全模型 0/10(floor effect)，10 个 all-zero 任务被纳入 Friedman，统计检验被地板效应污染；基准无法区分模型，"positive control demonstrates solvability"未给出对照细节(何模型、何配置)。
- - **Major**: LLM-as-judge 实际调用次数为零(all SKIP)，校准(21 gold、单标注、FNR/FPR=0.00)是空转的方法学担保，从未在真实判分上验证；单标注者无 inter-annotator reliability，21 项上完美分数可信度极低。
- - **Major**: Model-F(frontier)仅在 L1a(6 任务, exploratory)上测试，缺失 L1b 与 L2 结果，无法支撑"跨能力层、跨模型规模"的泛化声明；同时主套件中完全没有闭源模型，泛化性严重不足。
- - **Major**: 三个模型来自两个家族、三种参数量(7b/9b/14b)、不同架构，无匹配设计；在没有控制推理预算/上下文长度/训练数据重叠度的情况下，分数差异无法归因于"科学能力"。
- - **Major**: 完全未披鲛推理超参数(temperature、top-p、max_tokens、system prompt、few-shot 策略)；"per-seed rows"被声明但未说明种子数量、取值、是否跨模型共享；可复现性声明(SHA-256 seal)与实验配置不透明存在矛盾。
- - **Major**: 种子/试验管理不一致：gemma 有三次试验(含一次失败记为 0 的 ITT)，7b/14b 似乎单次；失败试验的根因(seed 依赖性崩溃?)未调查，TextSimilarity 作为 fallback metric 未与官方指标对齐验证。
### Minor（3）
- - **Minor**: FNR=0.00、FPR=0.00 在 21 项上报告至两位小数，精度误导(单项即可使比率跳变 4.8%)；应报告二项比侏 置信区间。
- - **Minor**: "answer-fitting audit intercepting 3/3 models"未报告该审计的 false positive rate 与人工验证协议，无法判断审计本身的可靠性。
- - **Minor**: L1a 仅 6 任劁、L1b 仅 10 任务、L2 仅 4 场景，每层单一域(rad / ResearchClawBench / p3dev)；如此狭窄的任务面使得泛化声明缺乏支撑。

## 新颖性（novelty）— ok
### Critical（2）
- - **Critical**: 核心 GAP 论证（"evaluation remains fragmented"）仅靠把三个**已存在的**基准（AIRS-Bench、ResearchClawBench、GAIA2）打包进一个 `run.json` 契约来回应，但全文未与任何已有统一评测套件（HELM、BIG-bench、Open LLM Leaderboard、lm-eval-harness 等多任务聚合框架）做差异对比。"统一"可能只是工程拼装而非研究空白，GAP 的真实性未被建立。
- - **Critical**: 声称的三层统计协议（McNemar / Wilcoxon+CLES / Friedman+Nemenyi+CD）全部是教科书级检验，且实际部署后**产出零有效信号**：McNemar 结构性零功效（$n_d=0$）、Friedman 非显著（$p=0.37$）、L1b 全模型 0/10 触底。一个自身首次运行即全面失效的协议，其作为"贡献"的价值未被证明，只是被声明。
### Major（4）
- - **Major**: 唯一正向统计结果——L1a 事后精选 6 任务子集 $p=0.003$——被作者自标"exploratory, not confirmatory"，本质是在 $N=3$ 模型、6 任务上的 post-hoc 选择性分析，却被放入摘要作为亮点呈现，增量贡献被夸大。
- - **Major**: 首次实证规模极小（4 个 L2 场景、6 个 L1a 任务、10 个 L1b 任务、3 个 7–14B 小模型），且未系统评测前沿模型（仅一个"exploratory Model-F"在 L1a 上 6/6）。摘要声称套件可"compare models / audit claims of research capability"，但在该规模与模型档位下，该能力未被实证支撑，贡献主张与证据不匹配。
- - **Major**: 摘要大量篇幅用于"SHA-256 seal、125 文件逐字节复现、18/18 重算检查"等复现工程细节，但未与已有可复现基准框架（HELM 的标准化运行记录、lm-eval-harness 的版本固定与 task schema）对比，这些机制的新颖性未被论证，增量贡献可能仅属工程实践。
- - **Major**: "denominator discipline（失败计零且留在分母）"被列为套件强制规则并暗示为方法论贡献，但这在 SWE-bench、GAIA 原始协议等已有基准中已是默认做法；文中未说明该纪律相对于各被组合基准原始设计的**增量**何在，存在把既有做法重新包装为贡献的嫌疑。
### Minor（3）
- - **Minor**: Introduction 以 `\citep{goodfellow2016deep}` 支撑"scientific agents advancing rapidly"这一具体论断，引用的是通用深度学习教科书，而非近两年科学智能体综述/基准；GAP 动机缺乏针对性文献支撑，削弱了"fragmentation"论断的可信度。
- - **Minor**: "answer-fitting audit（rule L047）"作为防作弊贡献被提及，但未与已有数据污染/泄露检测方法（canary、membership inference、训练数据检查等）区分，其相对于标准 contamination check 的增量新颖性未陈述。
- - **Minor**: 摘要中 "calibrated LLM-as-judge … passed at FNR=0.00, FPR=0.00" 但同时承认"该轮零次 judge 调用（全 SKIP），calibration 仅为 methodological warrant"。把一个未在实际评测中触发使用的校准结果放入摘要作为贡献展示，属于将潜在能力当作已验证贡献呈现。

## 可复现（repro）— ok
### Critical（3）
- - Critical: "SHA-256 seal over 125 files verifying byte-for-byte reproducibility" 未说明哈希覆盖范围——若含 LLM 生成产物则该强主张几乎不可能成立（未交代推理引擎确定性/固定种子/确定性 batching/排序），若仅覆盖输入与契约文件则"byte-for-byte reproducibility"系过度宣称，二者必居其一且均未澄清。
- - Critical: "independent recomputation script â¦ without new LLM calls" 实为从已存原始 per-seed 行重算汇总统计（算术校验），并非重跑实验；摘要把"recomputable"与"reproducible"混用，真正的一键复现（重发 LLM 调用、重跑 L2 环境）并未被任何脚本覆盖。
- - Critical: 缺配置快照——"rented cloud GPU"无 GPU 型号/提供商/驱动/CUDA 版本；模型用"qwen2.5:7b"冒号命名强烈暗示 Ollama 但从未点明服务框架及其版本；无量化规格（GGUF 位数）、无采样参数（temperature/top_p/max_tokens）、无推理 seed；模型权重 commit/文件哈希未固定，无法复现同一推断。
### Major（6）
- - Major: seed 链断裂——"per-seed rows"与"three independent trials (gemma)"被同时引用但 seed 数量、取值、与 trial 的映射关系全程未给出；又自承"bootstrap at step/seed level as future work"，即 seed 级统计尚未落地，却以 per-seed rows 作为复现承诺。
- - Major: 数据许可缺失——AIRS-Bench、ResearchClawBench、GAIA2 p3dev 三套基准及"125 files"的许可证、来源、再分发条款均未声明，复现者无法合法获取/重用数据。
- - Major: 哈希对账不可验证——未给出 SHA-256 清单文件（manifest）的发布位置、校验命令、对账流程；"run.json contract"被反复引用为复现中枢但其 schema/字段/版本号从未展示，审稿人无法据其对账。
- - Major: "rule L047, an internal audit identifier"系内部标识，若不随产物释放则该 answer-fitting 审计（3/3 模型）无法被第三方复现或核验。
- - Major: L2 环境（GAIA2 p3dev）未以 Docker 镜像哈希/lockfile/环境快照固定，"interactive environment execution"的多步工具调用复现高度依赖环境版本，却无任何快照。
- - Major: "frontier Model-F"被匿名化且仅作 exploratory 出现一次（6/6），无模型标识/权重/API 版本，无法复现也无法对账。
### Minor（3）
- - Minor: L1b 校准 gold 集规模前后不一致（FNR 用 21 gold、FPR 用 39 gold），未说明两集关系，影响校准结果的可复现解读。
- - Minor: L1b gold 为"single annotator"（21 gold），标注本身无可复现性保障（无第二标注者/一致性指标）。
- - Minor: 摘要"$N=4$"与"$N=8$ supplement"的 seed/场景对应关系未说明，复现者无法判断补集如何并入主集。

## 写作（writing）— ok
### Critical（3）
- - Critical: 摘要称 "post-hoc curated L1a subset (6 tasks)" 但引言明确 L1a 总共只有 six tasks —— 6/6 不是 "subset" 也不是 "curated"，用词自相矛盾、误导读者以为做了筛选。
- - Critical: 引言称 L1b "scored by a heterogeneous LLM judge"，但摘要自承 "0/10 for all models (execution failures, not judge scores)" 且 "zero judge calls (all SKIP)" —— 摘要与正文在"judge 是否实际参与评分"上直接矛盾。
- - Critical: 摘要出现 "frontier Model-F scored 6/6 (exploratory)"，Model-F 全文未定义、未引用、未说明为何只此一个 frontier 模型，读者无法理解其角色。
### Major（7）
- - Major: 摘要为单段约 300 词，塞入 3 层分数、McNemar/Friedman 多个 p 值、FNR/FPR、SHA-256、power 等数字，远超常规摘要长度与信息密度，结构性可读性缺陷。
- - Major: "passed at FNR=0.00, FPR=0.00 (39 gold in the expanded set)" 与前文 "(21 gold, single annotator)" 并置，读者无法判断校验通过的是 21 还是 39 gold，括号位置制造歧义。
- - Major: L2 报告 n_d=0 discordant pairs（两 arm 完全一致）却仍并列两 arm 设计并给出 0.1418/0.1918/0.2750 四位小数均值，"in both arms" 语义含混——是两 arm 均值相同还是跨 arm 合并？未澄清。
- - Major: "TextSimilarity intention-to-treat mean 0.355" 中的 TextSimilarity 指标从未定义，且与同一子句中的 exact-match 分数 (1/6→2/6) 混排，造成指标混淆。
- - Major: 术语漂移：摘要用 "three independent trials"，引言用 "per-seed rows"，另有 "runs" 概念——同一实体三种叫法未统一。
- - Major: 缩写表定义 "GAIA (General AI Assistant)"，正文却用 "GAIA2 p3dev"，"2" 与 "p3dev" 从未解释，缩写表与实际用法不一致。
- - Major: "AIRS-Bench rad" 中 "rad" 限定词无任何说明，读者不知其为子集名还是领域名。
### Minor（5）
- - Minor: 过度精度：d_min=2.1279、goal completion 0.1418/0.1918/0.2750 均为 N=4 数据，四位小数暗示虚假精确度。
- - Minor: 模型命名用 Ollama 式冒号记法 (qwen2.5:7b) 而非学术惯用名，与正式论文语境不符。
- - Minor: "rule L047, an internal audit identifier" 将内部编号暴露在论文正文，不适合外部发表。
- - Minor: 缩写表定义了未使用的 ECE、TS，而实际使用的 ReAct、SKIP、CG 缺少定义。
- - Minor: "18/18 independent recomputation checks" 的分母 18 未说明映射关系——若对应 18 L1a 行，则 L2/L1b 的重算覆盖范围不清。

## 伦理（ethics）— ok
### Critical（3）
- - Critical: 三类子基准（AIRS-Bench、ResearchClawBench、GAIA2）的数据许可条款只字未提——合并使用与发布前未声明各基准的 License 兼容性、再分发权与下游使用限制，存在直接合规风险。
- - Critical: L1a/L1b 要求 agent 生成并本地执行代码，全文未披露沙箱隔离、权限收敛或恶意代码防护措施，构成可复现的代码执行误用风险。
- - Critical: "frontier Model-F" 以单字母匿名出现且无任何解释——若为闭源商用模型可能违反其服务条款；若作者与其存在机构/商业关系则属未披露的利益冲突。
### Major（5）
- - Major: L1b 黄金标注仅 "21 gold, single annotator"，未声明标注者身份、与作者关系，亦无 IRB/伦理审查记录，在双盲评审下构成标注者利益冲突与人类受试合规缺口。
- - Major: "rule L047, an internal audit identifier" 暴露了作者所在机构的内部规则编号，存在双盲去匿名化泄露风险。
- - Major: GAIA2/p3dev 涉及真实环境交互（可能含网页浏览、工具调用），未做隐私影响评估、PII 处理或第三方服务条款合规说明。
- - Major: 事后 curated L1a 子集得 p=0.003 虽标注 "exploratory" 但仍在摘要中与确认性结果并列呈现，属选择性报告的伦理灰色地带。
- - Major: 全文无 responsible use / misuse disclosure 章节——一个教会 agent 生成并执行代码、规避 answer-fitting 审计的基准套件缺失滥用风险声明。
### Minor（3）
- - Minor: "rented cloud GPU" 的服务商、地区及服务条款未披露，影响可复现性与合规透明度。
- - Minor: 源码注释中 `corresponding@example.com` 占位符及 "camera-ready" 字样虽不渲染，但属双盲投稿的源码洁净度疏漏。
- - Minor: LLM-as-judge 校准轮 "made zero judge calls (all SKIP)" 却报告 FNR=0.00/FPR=0.00，该校准保证实质为空，存在以校准之名行背书之实的方法论伦理问题。

## 汇总

- **Critical: 21 | Major: 40 | Minor: 22**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）