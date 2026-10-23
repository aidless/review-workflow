# 对抗审查报告

- 时间: 2026-08-27T05:18:48.324830+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（3）
- - Critical: L2 结论 "no statistically detectable difference" 建立在 McNemar n_d=0、N=4、power=0.0000 之上，这是典型的"无证据≠无效应"谬误；一个无信息量的检验不能支撑"两臂等效/无因果效应"的结论，d_min=2.1279 意味着只能检出巨型效应。
- - Critical: LLM-as-judge 的校准（21/39 gold 上 FNR=FPR=0）被明确称为"methodological warrant"，因为实际 L1b 轮次零调用（全 SKIP）；产出 "0/10 for all" 的打分路径从未被该校准过的裁判验证过，L1b 分数的内部效度未建立。
- - Critical: 16 任务 Friedman 非显著（p=0.3679）后，再"curated"出 6 任务子集得到 p=0.0026 并用 Holm 校正——这是先看结果再选子集的 garden-of-forking-paths 选择偏倚，Holm 校正无法修复子集挑选本身引入的混淆。
### Major（7）
- - Major: 正文称 API 参考模型 deepseek-v4-flash 为 "5/6 L1a"，摘要称 Model-F "6/6"（p=0.0026 exploratory）；同一比较组的参考值自相矛盾，使 p=0.0026 的模型差异推断失去可靠前提（即便是笔误也直接动摇核心统计量）。
- - Major: "intention-to-treat mean 0.355 including the failed trial as 0" 把执行/契约失败计为 0 能力分，与论文声称的"separates completion failures from contract failures"前提直接矛盾，把契约失败混入能力估计造成系统性向下偏倚。
- - Major: 该 ITT 均值 0.355 与报告的 "1/6→2/6 after three trials" 在算术上无法调和（任何合理组合都在 0.17–0.33 区间），说明打分方法存在内部一致性错误，削弱分数效度。
- - Major: "byte-for-byte reproducibility + SHA-256 over 125 files + 18/18 independent recomputation" 实为同一确定性管线的重跑，混淆了 re-execution 与独立 replication；且默认 LLM 在 temp/seed/硬件下完全确定的前提未被论证（GPU 非确定性、采样实现差异未排除）。
- - Major: L1b 的 positive control 仅证明"pipeline 可解/不崩溃"，并未建立 10 个计分任务对被测 agent 类别可解；存在难度/可解性混淆，0/10 可能反映任务不可达而非模型无能力。
- - Major: 21 gold 单标注者、FNR=FPR=0.0000，无标注者间一致性、无不确定度量化；在如此小集合上的完美率与"校准集过易/过拟合"相容，judge-validity 假设实际未被检验。
- - Major: 三个本地 served 模型与 API served 的 Model-F 比较，混淆了服务方式/延迟/上下文窗口/工具链差异与模型能力差异；观测到的差距不是模型能力的干净因果估计。
### Minor（2）
- - Minor: 在当前就给出方向性结论（"no difference""0/10 stable"）的同时把 "bootstrap at step/seed level" 列为 future work，使报告的不确定度与所作声明的强度不匹配。
- - Minor: McNemar 中引用 "n_d=0<6" 的经验阈值，但在 N=4 时该阈值无意义；引用它制造了存在某种原则性等价判定规则的假象。

## 统计（stat）— ok
### Critical（4）
- - Critical: L2 用 exact McNemar 但 $n_d=0<6$、$N=4$、且自报 McNemar 功效 $0.0000$，却以 $p=1.0000$ 得出"两臂无统计可检测差异"——零功效下这是"无证据"被误述为"无差异"的证据，检验退化、结论无效。
- - Critical: 全篇样本量极小（L2 $N=4$、L1a 6 题、L1b 10 题），且 L1b 三模型均为 $0/10$（方差为零、地板效应），在此之上仍报告精确到 4 位小数的 $p$（1.0000、0.3679、0.0026、0.0261），制造虚假精度。
- - Critical: "curated L1a（6 题，探索性）$p=0.0026$，Holm 校正后 $p=0.0261$"——先做事后任务挑选（curate）再在同一挑选集内做 Holm 校正，无法消除选择偏倚，该校正 $p$ 值不成立，属 p-hacking 风险。
- - Critical: LLM-as-judge 校准报告 FNR$=0.0000$、FPR$=0.0000$（21 gold，后扩 39 gold），却给到 4 位小数且无置信区间；按 rule-of-three，$n=21$ 与 $n=39$ 的 95% 上界分别约 14.2% 与 7.7%，"0.0000"具误导性；且为单一标注者，无标注间信度（κ/ICC）。
### Major（6）
- - Major: 自报 $d_{\min}=2.1279$（80% 功效）即"巨大"效应量门槛，但全文未给出任何观测效应量（Cohen's $d$、CLES 仅提名称无数值）、未给均值置信区间，无法判断非显著是否仅因功效不足。
- - Major: 所有均值（goal completion 0.1418/0.1918/0.2750、gemma 的 ITT 均值 0.355）均无 SD/SE/CI，bootstrap 被"推迟为 future work"，点估计无可信不确定性量化。
- - Major: 跨模型 Friedman（16 配对任务，$k=3$）$p=0.3679$ 被判"non-significant"，但 $n=16$、$k=3$ 下功效低且 $\chi^2$ 近似存疑，不能解读为"模型间无差异"的证据。
- - Major: 多重比较家族未统一界定：3 模型 × 3 层 × 2 臂产生多组检验，仅对单一 curated 比较做 Holm，"exploratory"标签被用来规避校正，家族定义不一致。
- - Major: "frontier Model-F 6/6（$p=0.0026$ exploratory）"作为事后引入的参照，比较对象与检验选择未说明，存在 cherry-picking 嫌疑。
- - Major: gemma 的"intention-to-treat mean 0.355（含失败 trial 记为 0）"将 3 次试运行混合到任务级打分，$n=3$ 试次无方差报告，ITT 框架在基准打分语境下用法不清且估计量定义不明。
### Minor（2）
- - Minor: $N=8$ 补充仍报 $p=1.0000$，若仍为 0 discordant 则合并并不增加信息，应说明 discordant 数而非仅给 $p$。
- - Minor: "18/18 recomputation checks passing"被用作证据但无统计含义，宜与推断结论区分表述。

## 实验（experiment）— ok
### Critical（3）
- - Critical: L2 主对比设计（A=ReAct vs F=completion-guided）仅 N=4，McNemar 功效 0.0000、n_d=0，统计上零信息量，论文却以"无显著差异"断言两臂等效，属于无法证伪的零结果被当作结论。
- - Critical: L1b 的 LLM-as-judge 经历 21+39 gold 校准，但实际运行中"made zero judge calls (all SKIP)"，即校准集与实测分布完全脱节，相当于在空集上声称 FNR=FPR=0，对秧组（校准效应）根本未被激活，消融完整性存在致命缺失。
- - Critical: gemma2:9b 在 L1a 上经历"三次独立试验"从 1/6â2/6，随后用 intention-to-treat 将失败 trial 记为 0 求得 mean 0.355，而 7b/14b 却未描述是否同样重跑，重跑策略在模型间不对称，构成选择性偏差，基准公平性破坏。
### Major（6）
- - Major: L1a "curated" 子集 p=0.0026 标注为 exploratory，但 L1a 总共仅 6 个任务，"curated"措辞模糊，无法区分是否事后筛选；同时全量 16 paired tasks 的 Friedman p=0.3679 不显著，仅子集显著，有 cherry-picking 嫌疑。
- - Major: 消融层面仅有 A vs F 一组对比，且因 N=4 无区分力；answer-fitting audit（3/3 模型被拦截）、judge 模块、denominator discipline 等组件均无独立消融，无法归因各组件贡献。
- - Major: 超参数（temperature、top-p、max-tokens、prompt template、few-shot 设置）在摘要中完全未披露；7b/14b/9b 参数量差异显著，若用相同超参，基准公平性存疑；深度归因不可能。
- - Major: seed 管理描述前后矛盾——称"per-seed rows"却同时承认"bootstrap at step/seed level as future work"，意味着 seed 级别的方差分析缺失；N=4 究竟是 4 个 scenarioÃ1 seed、1 scenarioÃ4 seed、还是 4 seedÃ1 scenario，不清楚，无法判断泛化性。
- - Major: 泛化性严重不足——仅三个本地中小型模型（两个同系列 qwen + 一个 gemma），架构多样性属性极低；Model-F 仅在 L1a 上 exploratory 出现，未跨三层覆盖，无法支撑"统一 benchmark"的泛化声明。
- - Major: L1b 三个模型全部 0/10，无区分度，"positive control demonstrates pipeline solvability"未说明正对秧究竟是 oracle/human 还是 frontier model、通过率多少，正对秧不明确则无法区分"任务不可解"与"模型太弱"。
### Minor（2）
- - Minor: 论文提到 568 calls < 1000 预算，剩余 432 calls 未用于扩大 N 或增加模型，浪费了提升功效的机会。
- - Minor: deepseek-v4-flash 作为 API 参考得 5/6 L1a，但未说明是否在相同 harness、相同 prompt、相同超参数下运行，与本地模型的公平性未保证。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 所谓"统一基准"的核心组成 AIRS-Bench、ResearchClawBench、GAIA2 似乎均为已有基准的拼装（GAIA 昬身是已知 benchmark），文中未论证三者的"新增部分"（如 GAIA2 p3dev 的改造、ResearchClawBench的新增）相对原始版本的实质性新增，"unified"实为"bundled existing benchmarks + reproducibility wrapper"，贡献增量性被夸大。
- - Critical: 引言部分的相关工作仅引用 `goodfellow2016deep`（深度学习教科书），未与实际 benchmark 文献（AgentBench、SWE-bench、ScienceAgentBench 等）对比差异，无法确立"碎片化 GAP"是否真实——即没有证据表明先前工作曾尝试统一却失败，GAP 可能只是"未被有人做过"èé"做了但有缺陷"。
### Major（3）
- - Major: 声称的 LLM-as-judge 校准组件在实际评估中"made zero judge calls (all SKIP)"，即该组件根本未在结果中起作用，却被列为 suite 的核心组成，贡献被显著夸大为"validated component"。
- - Major: 统计协议（McNemar、Wilcoxon+CLES、Friedman+Nemenyi）均为标准统计方法，将"应用标准统计"包装为方法论贡献属于增量；且 N=4、功率 0.0000、n_d=0<6 使得"no statistically detectable difference"这一经验发现无法提供有效的经验贡献，实验层面仅 frontier Model-F 的 6/6（p=0.0026 exploratory）是唯一"正向"结果，且自述为 exploratory。
- - Major: 局部模型在 L1b 上 0/10 全失败、L1a 上 0/6、2/6、1/6，benchmark 未展示对这一能力区间的区分性，"区分 genuine scientific reasoning from execution failure"的核心 GAP 声明在局部模型上未被证明可行，GAP 的现实意义存疑。
### Minor（2）
- - Minor: "three-layer (L1a/L1b/L2)"分层的科学依据未给出，为什么是这种划分（而非其他 taxonomy）缺乏论证，层级命名的"scientific"性的新颖性不足。
- - Minor: "denominator discipline"、"SHA-256 seal"、"run.json contract"等属工程实践，与现有可复现性工具链（ML reproducibility checklist、DVC、MLflow 等）的差异未对比，增量不明。

## 可复现（repro）— ok
### Critical（4）
- - Critical: 全文未提供代码仓库链接/DOI/容器镜像，"release the suite"与"fully recomputable harness"无落地入口，一键复现的入口证据链断裂。
- - Critical: 模型仅以松散标签标识（qwen2.5:7b 等），未固定权重哈希、量化级别、serving 后端（Ollama/vLLM 版本）；本地模型采样本就非确定，所谓"byte-for-byte reproducibility over 125 files"实为缓存转录回放，混淆了 transcript 复现与 run 复现。
- - Critical: 采样/服务配置（temperature、top_p、system prompt 版本、GPU/CUDA/OS/硬件）完全缺失，本地模型跨机不可复现。
- - Critical: AIRS-Bench / ResearchClawBench / GAIA2 p3dev 三套数据集均未声明数据许可与再分发条款（GAIA 有明确署名与许可要求），合法复现受阻。
### Major（5）
- - Major: 摘要声称"per-seed rows"但未披露实际 seed 取值、生成过程与 trial↔seed 映射；"gemma 三次独立试验"的规程（是否同 seed、是否重置 agent 状态）未定义，而 seed 级 bootstrap 又被推迟为 future work，方差不可复现。
- - Major: SHA-256 seal 描述不足：125 文件清单未列、清单自身是否被纳入哈希（循环哈希风险）、实际 seal 值未给出、recomputation 输入边界未界定。
- - Major: "18/18 independent recomputation checks"语义不明——重算的是分数、哈希还是统计量？若基于缓存 LLM 输出重算则非真正独立，未说明输入来源与是否触发新调用。
- - Major: L1b judge 校准"本轮零调用（全 SKIP）"，FNR=0/FPR=0 的 warrant 为空集，校准结果既不可复现也不可证伪，沦为方法论占位。
- - Major: 参考模型 deepseek-v4-flash 为 API 模型，未固定版本/快照日期；API 模型静默更新使 5/6 L1a 结果不可复现且无法字节对账，破坏跨时间复现契约。
### Minor（2）
- - Minor: McNemar 功效 0.0000、n_d=0<6、bootstrap 推迟，L2 双臂比较的可复现性/方差完全未被量化。
- - Minor: L1b positive control"pipeline solvability"所用模型与配置在可见文本中未指定，可解性结论的成立条件未交代。

## 写作（writing）— ok
### Critical（2）
- - Critical: 摘要称"frontier Model-F scored 6/6"，但引言称"API-model reference (deepseek-v4-flash, 5/6 L1a)"，同一参考模型在摘要与正文中分数矛盾（6/6 vs 5/6），且名称不一致（Model-F vs deepseek-v4-flash），无任何说明。
- - Critical: 实验臂标签"F"（completion-guided harness）与"Model-F"（frontier参考模型）共用字母 F，指代完全不同的两个实体，造成术语碰撞，读者极易混淆。
### Major（8）
- - Major: "intention-to-treat mean 0.355"无法与所述试验得分自洽：三次试验得分1/6、2/6、0（failed）的ITT均值应为(1/6+2/6+0)/3â0.167，与0.355相差一倍以上，数字不一致。
- - Major: 摘要称"three cloud-hosted local models"，引言称"local models served via a local OpenAI-compatible endpoint"，"云端托管"与"本地端点"直接矛盾。
- - Major: "L047 answer-fitting audit"中的"L047"未在任何处定义或解释，突兀出现，属未定义术语。
- - Major: "deepseek-v4-flash"不对应任何已知 DeepSeek 模型（截止最新为 V3），疑为命名错误或虚构模型名称。
- - Major: "McNemar power 0.0000"——将统计功效报告为精确零在方法上不合理且易误导；功效极少为正值，应报告实际计算值并说明条件。
- - Major: Holm 校正 p=0.0026â0.0261 隐含校正族约10个检验，但摘要仅披露2个p值，校正族成员不透明，无法复核。
- - Major: 同一 p=0.0026 在摘覌中出现两次（一次描述 Model-F 得分，一次描述 curated L1a Friedman），未说明是否同一检验，造成阅读困惑。
- - Major: 摘要结构严重超载——单段堆砌数十个数值（p值、比例、置信度、文件数、功效参数等），读作结果表而非概要，严重损害可读性。
### Minor（7）
- - Minor: 四舍五入不一致：0.0026Ã10=0.0260≠报告值0.0261，说明原始r值实为0.00261但显示为0.0026，同一数值舍入位数不统一。
- - Minor: "GAIA2 p3dev"中"GAIA2"与"p3dev"均未定义；缩略语注释定义了"GAIA"但 GAIA2 是不同标签。
- - Minor: 层级标签 L1a/L1b/L2 未解释"L1""L2"含义，读者无法理解分层逻辑。
- - Minor: "21 gold"â"39 gold in the expanded set"，扩展缘由未说明，两个数字关系不清。
- - Minor: "FNR=0.0000, FPR=0.0000"与"the round made zero judge calls (all SKIP)"并列，对未实际使用的裁判器报告完美校准指标，表述上高估了实陌验证。
- - Minor: "N=8 supplement"以括号一笔带过，未说明其内容、来源或与 N=4 主实验的关系。
- - Minor: 引言结尾句子断裂（"calibrated before its judge"后截断），句法不完整。

## 伦理（ethics）— ok
### Critical（2）
- - Critical: 全文未对所集成第三方基准（AIRS-Bench、ResearchClawBench、GAIA2 p3dev）给出任何数据许可/使用条款声明，再分发与修改权限不明，存在法律合规风险。
- - Critical: 该套件实质化"自主代码生成+执行"与交互式环境/工具控制能力，却完全缺失双用途/误用风险评估、沙箱与安全治理说明及负责任发布计划——一个把自主代码执行流程化的基准理应附伦理声明。
### Major（4）
- - Major: 缺少利益冲突（COI）披露，却直接对比多家商用模型（Qwen2.5/阿里、Gemma2/Google、DeepSeek）并引入匿名"Model-F"；若任一作者与某供方存在隶属或商业关系，框架偏向即未披露。
- - Major: 用于校准 LLM-as-judge 的标注金标集（"21 gold""39 gold"）未提供 IRB/人类受试者伦理审查说明；标注者知情同意、报酬，以及唯一标注者是否为作者本人（自标注 COI）均未交代。
- - Major: 模型被描述为"cloud-hosted local"，意味着基准任务、生成代码与执行轨迹会经第三方云基础设施流转，却无数据治理、留存策略或隐私风险讨论；若任务含真实科研/个人数据，数据外泄路径未被评估。
- - Major: "GAIA2 p3dev" 疑为 Meta GAIA 基准的衍生版本，但未举证其修改与再分发已获原始许可授权。
### Minor（2）
- - Minor: 源文件双盲卫生问题——.tex 源码内嵌投稿阶段元数据注释（"camera-ready: corresponding@example.com""TMLR G3"），虽编译后不可见，但源码释出前应清除以免泄露评审阶段标识。
- - Minor: "L047 answer-fitting audit" 以不透明内部代号引用且无审计协议描述，既损可复现性又可能泄露内部项目标识。

## 汇总

- **Critical: 20 | Major: 39 | Minor: 19**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）