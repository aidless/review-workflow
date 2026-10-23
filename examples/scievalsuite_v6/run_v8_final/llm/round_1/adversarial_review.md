# 对抗审查报告

- 时间: 2026-08-27T10:16:06.240691+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（5）
- - Critical: L2 比较宣称 "in both arms" 分数相同，构成等效性声明，但在 N=4、McNemar n_d=0 的情况下既无等效性检验（TOST）也无等效性界值，"无差异"结论在功效为零时不可做。
- - Critical: L1a 显式承认 "trial counts asymmetric"，不同模型接受了不等量的试验次数（剂量），这直接混淆了"模型能力"与"试验预算"两个变量，使跨模型分数比较的因果归因无效。
- - Critical: 对照模型 Model-F 以 API 方式服务，而三个被测模型以本地 GPU 方式服务，服务通道本身（量化、延迟、稳定性）是未控制的混淆变量，6/6 无法归因于模型能力。
- - Critical: L1b 全部模型 0/10 属于 floor effect，测量工具在该任务层失效，无区分力；在此条件下仍执行并报告 Friedman p=0.37，等于对一个不产生信息量的退化数据做推断，方法论上自相矛盾。
- - Critical: 报告 d_min=2.1279（80% power），即只能检测 Cohen's d>2 的极端效应；对于合理效应量完全没有功效，这意味着整套实验设计在当前 N 下结构性地无法回答"模型间是否存在差异"这一核心问题。
### Major（7）
- - Major: 将三个特定开源模型的表现作为因果证据来比较"模型能力"，但模型选择非随机、服务环境非统一，属观察性比较而非受控实验，因果推断框架不恰当。
- - Major: Friedman "16 paired tasks" 中 10 个全零任务不提供任何区分信息，却仍纳入检验矩阵，人为稀释效应并改变 p 值；应在排除全零任务后单独报告有效子集。
- - Major: LLM-as-judge 校准仅 21 gold、单一标注者（single annotator），无法估计标注者间变异；rule-of-three 给出 FNR/FPR 95% 上界≈14%，在 0/6 或 2/6 评分场景中 14% 错误率足以翻转模型排名结论。
- - Major: TextSimilarity ITT 将失败试验硬编码为 0，但 TextSimilarity 是连续度量，失败试验可能存在部分语义重叠；设为 0 的前提未经验证，可能系统性人为压低均值并扭曲跨模型比较。
- - Major: "18/18 recomputation checks passing" 验证的是计算管线的字节级可重复性，而非统计估计的有效性或无偏性；可重复的偏差仍是偏差，不能作为结论可信度的证据。
- - Major: 前提"三层任务覆盖 scientific agent capability"未经外部效度论证：L1a 仅六道 AIRS-Bench rad 题、L1b 仅十道 ResearchClawBench 题、L2 仅四个 GAIA 场景，从如此窄的任务面外推到"科学代理能力"的归纳跳跃过大。
- - Major: 摘要未披露本地模型的推理配置（量化精度、temperature、top-p、max tokens），这些参数是已知影响代码生成与工具调用成功率的关键混淆变量。
### Minor（2）
- - Minor: post-hoc subset 分析虽标记为 "non-confirmatory sensitivity"，但仍在论文中呈现并可能影响读者解读，未做多重比较校正也未声明 family-wise error 率。
- - Minor: 承认 "bootstrap at step/seed level as future work"，但在 N=4 的极端小样本下，缺少任何不确定性量化（bootstrap CI 或 permutation interval）使点估计无置信带支撑。

## 统计（stat）— ok
### Critical（2）
- - Critical: Friedman检验合并16个paired task，其中10个L1b任务全零→产生完全结秩（all tied at rank 2），有效判别信息仅来自6个block，报告N=16虚高n_eff≈6，且大量结秩使χ²近似失效，p=0.37在地板效应下无统计推断意义。
- - Critical: 全部点估计（goal completion 0.14/0.19/0.28、TextSimilarity ITT 0.355、各层得分比例）均未报告SD/SE/CI/任何离散度指标；N=4下点估计极不稳定，读者无法评估不确定性区间。
### Major（6）
- - Major: 将L1a（6任务，代码执行评分）与L1b（10任务，报告/图表评分，全零）合并入同一Friedman检验，混合异质任务类型与评分构念，pooling违反同质性前提，使检验结果不可解释。
- - Major: 三模型×三层×多指标+Model-F frontier参照+appendix post-hoc子集分析构成多重比较族，全文未报告任何family-wise校正（Bonferroni/Holm/FDR），仅Nemenyi+CD控制层内post-hoc，族间错误率未控。
- - Major: L2 N=4且n_d=0（A/CG两臂在所有task上二值结果完全相同→两臂统计恒等），d_min=2.1279远超Cohen's "large"=0.8，检测阈值不合理；将"non-significant"与"exploratory"标签并用仍存在Type II误读风险，应明确声明"无推断能力"而非"non-significant"。
- - Major: LLM-as-judge校准仅单标注者、n=21、FNR=FPR=0.00，未报告inter-annotator agreement（κ/ICC）；rule-of-three上界≈14%意味着真实错误率可达14%，以点估计0.00作为"passed"gate具误导性。
- - Major: 协议声明Wilcoxon+CLES与Friedman+Nemenyi+CD，但摘要未报告任何已观测效应量（CLES值、rank-biserial r、η²_H），仅报告MDE d_min，无法评估实际效应大小与统计显著性之外的实践意义。
- - Major: L1a trial counts不对称违反配对比较前提；2/6 vs 2/6在n=6下无检验力，"cross-model claims descriptive"声明未配套任何不确定性量化或置信区间。
### Minor（2）
- - Minor: "18/18 independent recomputation checks passing"作为有效性证据呈现，但可复现性（数值一致性）≠统计推断有效性，不构成样本量或检验力论证。
- - Minor: bootstrap step/seed级方差估计推迟至future work，承认不确定性量化缺失但未在结果解读（如"non-significant"结论）中体现该限制的影响。

## 实验（experiment）— ok
### Critical（2）
- - Critical: L2 对照组（A=ReAct vs CG=completion-guided）N=4 且 n_d=0 discordant pairs，两 arm 在所有样本上结果完全相同（mean goal completion 在两 arm 中逐模型一致），McNemar 结构性失效，该对照组无法支持任何关于 CG harness 价值的结论，等效于无对照。
- - Critical: 泛化严重不足且存在 floor effect——仅三个中小型模型（≤14b）、任务量极少（L1a=6, L1b=10, L2=4），L1b 三个模型全部 0/10，Friedman 16 paired tasks 中 10 个全零，floor-limited 数据使跨模型排序与 Nemenyi/CD 结论无意义；缺乏大模型与跨家族验证，"统一基准"的泛化主张未成立。
### Major（6）
- - Major: L1a 的 Model-F（API frontier reference, opencode.ai alias）仅在 L1a 上做 exploratory 6/6，既未作为正式对照组跨三层验证，也因 API 服务 vs 本地 GPU 部署而与三个 open-weight 模型不可比，无法构成公平基准线。
- - Major: 消融不完整——CG harness 作为干预变量未对其内部组件（completion guidance 的触发、强度、回退策略）做消融；L1a 将 code generation 与 execution 耦合评分，未分离"生成能力"与"执行能力"的贡献；L1b 的 answer-fitting audit 与 LLM-as-judge 两道关卡未分别消融，无法判断 0/10 是由 audit 拦截还是 judge 判定驱动。
- - Major: 基准不公平——三个模型分属不同家族（Qwen2.5 vs Gemma2）且参数量跨 7b/9b/14b，并非同族同尺度对照；通过 "rented cloud GPU" 本地部署但未披露是否使用量化、KV cache 配置、batch 策略是否一致，这些都会系统性影响不同架构模型的实测性能。
- - Major: 推理超参数未披露——摘要与引论均未给出 temperature、top-p、max_tokens、重复惩罚等采样参数；L1a 明确承认 "trial counts asymmetric, one success needed re-trials"，意味着不同模型获得不等的重试机会，直接违反配对公平比较前提。
- - Major: seed 管理不透明——声称 "per-seed rows" 但未说明每个配置运行几个 seed、seed 如何选取；L2 的 "N=4" 与 "N=8 supplement" 究竟是场景数还是 seed×场景运行数不清晰；且明确将 "bootstrap at step/seed level" 列为 future work，意味着 seed 级别方差完全未量化，单 seed 行无法支撑统计推断。
- - Major: Friedman p=0.37 在 10/16 全零的 floor-limited 数据上虽标注 exploratory，但仍被用于支撑 "cross-model non-significant" 的叙述，存在以零效力检验"确认"无差异的误导风险；应明确该结果不具任何证据效力而非仅标注 exploratory。
### Minor（2）
- - Minor: L1b 的 "positive control demonstrates pipeline solvability" 未说明该正控覆盖多少任务、是否覆盖全部 10 项，亦未说明正控本身的设计（人工脚本？最强模型？），正控强度存疑。
- - Minor: LLM-as-judge 校准仅用 21 gold 且 single annotator，FNR=FPR=0.00 借 rule-of-three 给出 95% 上界≈14%，该校准规模过小，难以支撑将 judge 用于正式跨模型比较的基准公平性。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 三个子基准（AIRS-Bench rad、ResearchClawBench、GAIA2 p3dev）均为既有 benchmark，本文的"统一"实际上是把三个现成 benchmark 打包进一个 run.json 契约 + SHA-256 清单，核心 GAP（"evaluation remains fragmented"）虽然真实但解决方案几乎是工程封裌，增量贡献被"unified reproducible benchmark"的框架性表述明显夸大。
- - Critical: 所谓"unified"在方法学上并不成立——L1a 用代码执行打分、L1b 用 LLM-as-judge、L2 用 goal completion，三层各自独立的 metric / 统计 / 判定协议，并未形成统一评分理论，属于松散联邦而非统一框架，"unified"词义与现有 multi-benchmark suite（如 BIG-bench、HELM、Open Evaluator）的差异未给出。
### Major（4）
- - Major: 核心可复现性声明明确写明 SHA-256 seal 是 over "committed files (not live LLM outputs)"，即最不可复现的 LLM 采样输出被排除在外，"byte-level reproducibility"实际只覆盖后处理产物，与摘要中暗含的"复现性贡献"存在表述缺口，增量被高估。
- - Major: "three-layer statistical protocol"（exact McNemar / Wilcoxon+CLES / Friedman+Nemenyi+CD）全部是教科书级标准检验，无方法创新；将它们编进单个脚本并作为贡献点列出，属于将常见实践包装为方法贡献，与任何 benchmark 统计教程无实质差异。
- - Major: 经验结果几乎全部落地为 null / floor（L1b 0/10、L2 McNemar 结构性 power=0、Friedman p=0.37 n.s.、L1a 多为 0），无效的实证发现意味着实验贡献极弱；"small open-weight models fail at scientific agent tasks"本身不构成对现有认知的增量。
- - Major: "denominator discipline"、"answer-fitting audit"、"positive control"均为标准评测卫生手段，未与现有 robustness/contamination 审查文献（如 SWE-bench 的解决验证、Data Contamination 检测）做对比，未证明越过它们的增量。
### Minor（2）
- - Minor: 判定校准仅 21 gold、单标注者、rule-of-three 上界≈14%，校准样本之小使得"calibrated LLM-as-judge"的新颖性声明缺乏支撑，且与已有 LLM-judge calibration 文献的差异未阐述。
- - Minor: Model-F（opencode.ai alias）作为"frontier reference"且标为 exploratory，来源不透明，无法支撑"对比贡献"，应删除或明确归属。

## 可复现（repro）— ok
### Critical（4）
- - Critical: SHA-256 seal 仅覆盖 125 个"committed files"且明言"not live LLM outputs"——被评分的随机性 LLM 输出本身未哈希封存，所谓 byte-level reproducibility 只对输入成立；重跑必发散且无输出侧哈希对账机制。
- - Critical: 模型身份未钉死：qwen2.5:7b/14b、gemma2:9b 是可变的 registry tag（无 weights commit/digest/量化版本）；"Model-F (opencode.ai alias)" 是未披露的路由后端，可静默更换——主模型与 6/6 参考模型均不可复现。
- - Critical: 采样配置（temperature/top_p/max_tokens/seed）全文缺失；"one success needed re-trials" 隐含随机采样却无服务端 seed 钉死，调用级复现在结构上不可能。
- - Critical: "independent recomputation script" 只从已提交的 raw rows 重新聚合、"without new LLM calls"——这只校验内部一致性，并非端到端复现；被当作 reproducibility 保证与一键复现来宣传，名实不符。
### Major（7）
- - Major: "rented cloud GPU + local OpenAI-compatible endpoint" 无运行时/量化/CUDA/driver/容器镜像快照；新租实例的 kernel/quant 路径可产生不同 logits，配置快照缺失。
- - Major: seed 未说明：承诺"per-seed rows"却未给出 seed 取值、数量及其控制对象（模型采样？harness RNG？任务顺序？）；"bootstrap at step/seed level as future work" 等于自认 seed 级方差分析缺失。
- - Major: 预算/调用计数不透明：568 calls(<1000) 与"trial counts asymmetric""re-trials"并存，但 call/retrial 如何计入预算无定义，budget-control 主张不可审计。
- - Major: 数据许可未披露：AIRS-Bench、ResearchClawBench、GAIA2 三基准及 125 文件的 license provenance 未核验，再分发与复现可能被法律阻断。
- - Major: 证据链断口：568 calls→24/18/30 rows→聚合 的映射被宣称但无 per-row provenance schema（call id/seed/arm/retry index）；run.json contract 被引用却未展示/未版本化。
- - Major: judge 不可复现：LLM-as-judge 的模型身份/版本/seed 未披露，judge 本身随机却被当作确定性门（FNR=0/FPR=0）；"21 gold, single annotator" 的 gold 集是否发布未说明。
- - Major: "positive control demonstrates pipeline solvability" 的配置/输入/期望输出/通过判据均未描述，无法重跑以确认 pipeline 非平凡可解。
### Minor（2）
- - Minor: Friedman"16 paired tasks"的配对单元（seed？task？）未声明，且含 10 个 all-zero L1b 任务使配对退化，复现意义存疑。
- - Minor: 统计规范脚本（scipy 路径）未钉版本/哈希；rule-of-three 上界≈14% 与 FNR/FPR=0.00 并列呈现时未在复现框架内强调极小 n 的脆弱性。

## 写作（writing）— ok
### Critical（1）
- - Critical: 摘要声明"18/18 independent recomputation checks passing"，而引言声明"every leaderboard number recomputed"，72 行结果（24+18+30）仅 18 项校验相矛盾，重算覆盖范围被严重夸大。
### Major（7）
- - Major: 模型简称在同一句中不一致："0.14 (7b), 0.19 (14b) and 0.28 (gemma)"，前两个用参数量、第三个突然换成模型族名而非 "9b"。
- - Major: 命名不一致：摘要写 "AIRS-Bench"，引言写 "AIRS-Bench rad"，未说明 "rad" 后缀含义。
- - Major: 引言称 L1b "scored by a heterogeneous LLM judge"，摘要称 "single annotator"，"heterogeneous"与"single"表面矛盾，未阐明是多 judge 模型还是多标注者。
- - Major: 摘要同时写 "d_min=2.1279 at 80% power" 与 "McNemar power structurally 0"，未区分假设性灵敏度分析与实陌功效，读者会看到"80% power"与"power=0"自相矛盾。
- - Major: 含义不明术语未定义即首次使用："p3dev"、"opencode.ai alias"、"GAIA2"（缩略表定义的是"GAIA"）。
- - Major: 摘要结构严重超载，约 400 词密度堆积 20+ 个数字与统计术语，违反摘要应高层概括的写作规范。
- - Major: "mean goal completion â¦ in both arms" 两臂均值完全相同（0.14/0.19/0.28）却未给出任何解释，读者无法判断是设计决定还是异常。
### Minor（5）
- - Minor: 缩略表列出 ECE、TS 等，但可见正文未使用或定义。
- - Minor: 摘要 "SHA-256 seal"（单数）与引言 "SHA-256 manifests"（复数）数不一致。
- - Minor: 摘要称 per-seed rows 已交付，又称 "bootstrap at step/seed level as future work"，有 seed 级数据却无法做 seed 级 bootstrap，逻辑张力未解释。
- - Minor: 引言提及 "Wilcoxon+CLES" 为三层统计协议之一，但摘要从未提及 Wilcoxon，摘要与正文统计框架描述不对齐。
- - Minor: 提及 "21 gold" judge 校准结果与 L1b 失败分类，但无任何可见表格/图呈现，数据无法检验。

## 伦理（ethics）— ok
### Critical（2）
- - Critical: 全文无任何 Ethics / IRB / 数据使用许可章节，而 benchmark 涉及代码执行、工具调用、人类标注与第三方 API，缺少最基本的合规框架
- - Critical: SHA-256 封印覆盖"125 committed files"——若以 Git 仓库形式发布，commit 的 author/邮箱/时间戳将直接泄露作者身份，破坏 TMLR 双盲审稿
### Major（7）
- - Major: AIRS-Bench "rad"（疑似放射学子集）、GAIA2（含网页抓取内容）可能涉及患者 PHI 或第三方 PII，全文未做隐私审查与去标识化说明
- - Major: AIRS-Bench / ResearchClawBench / GAIA2 三个数据集及 qwen2.5、gemma2 模型的许可条款均未披露，无法判断其研究/商用使用是否合规
- - Major: 使用第三方商用 API "Model-F (opencode.ai alias)" 进行评测，数据外发至外部服务商，既未评估隐私影响也未披露是否存在利益关系
- - Major: "21 gold, single annotator" 人类标注环节未说明标注者知情同意、报酬与伦理审查（IRB），单标注者亦无伦理留痕
- - Major: 全文无 Conflict of Interest 声明，而评测对象（Qwen/Gemma）与所用服务（opencode.ai、云 GPU 厂商）均可能与作者存在 affiliation 或商业关系
- - Major: 评估并记录了 agent 的 "answer-fitting"（答案拟合/作弊）行为，却未讨论 dual-use 风险与防滥用措施，发布后可被用于优化欺骗性 agent
- - Major: 代码生成与执行、L2 工具调用环境缺少沙箱安全与误用风险章节，存在生成恶意代码或越权操作的隐患
### Minor（1）
- - Minor: "rented cloud GPU" 未指明供应商与数据处理协议，云上推理的数据驻留/留存策略不明

## 汇总

- **Critical: 18 | Major: 44 | Minor: 16**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）