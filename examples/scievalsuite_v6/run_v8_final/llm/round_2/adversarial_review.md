# 对抗审查报告

- 时间: 2026-08-27T10:24:57.279716+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（4）
- - Critical: L1a 试次不对称（"one success needed re-trials; trial counts asymmetric"）构成核心混淆变量——各模型获得的重试额度不等，即使标注"descriptive"，0/6 vs 2/6 的跨模型比较仍缺乏内部效度，因为差异可能完全归因于重试机会而非模型能力。
- - Critical: L2 报告了模型均值（0.14/0.19/0.28）但无任何推断统计支撑（McNemar 因 n_d=0 不适用）；N=4 时这些均值的方差极大，将它们并列呈现隐含模型间存在差异的因果暗示，而实际上零个 discordant pairs 意味着对 arm 效应和模型效应均无任何因果证据。
- - Critical: Friedman 检验包含 16 个任务中 10 个 all-zero（floor）任务，违反了 Friedman 检验对任务需具备区分度的隐含假设；floor 任务不贡献排名信息却放大了有效 N，使检验被"稀释"到无法解释，而非仅仅是"non-significant"。
- - Critical: L1b 全部 0/10 源于执行失败（"execution failures, not judge scores"），这意味着该层实际测量的是执行基础设施可靠性而非研究工作流质量；构念效度威胁使得"L1b 评估 research-workflow synthesis"这一前提根本未被检验。
### Major（5）
- - Major: Model-F（6/6）通过 API 服务，而其他模型在本地云 GPU 上推理，混淆了模型能力与服务基础设施；6/6 的成功无法归因于模型质量，"exploratory"标签不足以消除此混淆。
- - Major: LLM-as-judge 仅用 21 个 gold 样本、单标注者验证，无标注者间一致性；rule-of-three 上界≈14% 意味着真实错误率可能高达 14%，单标注者设计无法排除系统性偏差。
- - Major: 模型族与参数量混淆——qwen2.5（7b/14b）vs gemma2（9bï¼ââä»»ä½•è·¨æ¨¡åå·®å¼æ æ³å½å äºè§æ¨¡æåºè¿æ¯æ¶æå·®å¼ï¼åå¼±äºå¯¹æ¨¡åè½åæ¢¯åº¦çä»»ä½å æè§£éã
- - Major: 每个 cell 仅单次运行（24=4Ã3Ã2, 18=6Ã3, 30=10Ã3），无多 seed 变异控制；LLM 输出的随机性使得单次结果可能完全是采样器声，内部效度根本无法评估，而"bootstrap at step/seed level"仍为 future work。
- - Major: "Byte-level reproducibility"的 SHA-256 密封明确排除了 live LLM outputs，仅覆盖 harness 与数据文件；这一框架可能误导读者将流程可复现性等同于结果可复现性，而后者因随机输出未被验证。
### Minor（2）
- - Minor: "Answer-fitting audit"拦截 3/3 模型为规则驱动，未报告假阳性率；若审计误杀合法推理路径，则 all-zero 结果可能是审计机制自我实现的人工地板。
- - Minor: L2 的"oracle-free goal completion"未说明在无 oracle 时如何判定目标完成，测量可靠性不明；若依赖人工或 LLM 判定，则引入未校准的二次判定器，形成未控制的测量混淆。

## 统计（stat）— ok
### Critical（4）
- - Critical: Friedman 检验在 16 个配对任务中含 10 个全零（地板效应）block——全零 block 内所有模型获并列平均秩、对处理间离差贡献为零但仍计入 n=16 与卡方近似所依赖的有效样本量，实际判别 block 仅 6 个；62.5% 全零 block 使卡方近似严重失真，所得 p=0.37 既不表示"无差异"也不可作推断，报告该 p 值并标注"non-significant"即构成 p 值误用。
- - Critical: 全文所有点估计（goal completion 0.14/0.19/0.28、L1a 0/6·2/6·2/6、TextSimilarity 均值 0.355）均无 SD/SE/CI/bootstrap 区间，方差报告完全缺失；bootstrap 被列为 future work，致使无法判断模型间差异是否落在噪声带内，任何跨模型叙述缺乏统计可解释性。
- - Critical: L2 N=4（补充 N=8）且两臂均 n_d=0 discordant pairs，exact McNemar 不可用且功效"结构性为 0"；d_min=2.13 属 Cohen"极大效应"量级，仅能探测不现实的效应量——实验在事前即无能力回答研究问题，却仍作为"三层统计协议"一层呈现，误导读者以为存在可用统计层。
- - Critical: LLM-as-judge 校准 21 gold、单一标注者、FNR=FPR=0.00，rule-of-three 上界 ≈14% 计算有误——FNR 分母为 gold 正例数 k、FPR 分母为 gold 负例数 21−k，3/21≈14% 同时适用于两者在数学上不可能（需 k=21 且 21−k=21）；未报告正/负例拆分，若拆分不均各率真实上界可远超 14%（如 11/10 拆分时上界分别 ≈27%、30%），且单一标注者无 inter-rater reliability 指标。
### Major（3）
- - Major: L1a 各模型试验次数不对称（"one success needed re-trials; trial counts asymmetric"），跨模型比较被试验次数/努力混杂；标注"descriptive"不消除统计混淆，且这些被污染的 L1a 分数被纳入跨模型 Friedman，使"配对"前提（同等条件）不成立。
- - Major: 多重比较未系统控制：3 模型 × 3 层 × 2 臂衍生大量对比，正文仅一个 Friedman 检验，附录 post-hoc subset 分析即使标注"non-confirmatory sensitivity"仍构成 multiplicity 膨胀，全文未报告任何 FWER/Bonferroni/Holm 校正或 family-wise 策略。
- - Major: 协议声明 Wilcoxon+CLES 但摘要与可见正文均无任何 CLES、Cohen's d 或 r 等观察效应量；仅报告 d_min（功效下限），而功效下限是设计参数而非观察效应量，读者无法据以判断实际差异的大小或实际意义，违反效应量报告规范。
### Minor（2）
- - Minor: Model-F 6/6 为单次运行无方差、且形成天花板效应，作为"exploratory reference"仍被置于跨模型对比语境中，易被误读为可比较基准。
- - Minor: 协议提及 ECE/TS（温度缩放校准）但可见文本无对应数值，校准评估的统计基础不可核实；CLES 在 acronym 列表定义但正文无值。

## 实验（experiment）— ok
### Critical（3）
- - Critical: L2 对照组 N=4、n_d=0、McNemar power "structurally 0"，A vs CG 两臂对照在统计上完全无区分力，"两臂分数相同"实为功效不足的伪结论而非真等价。
- - Critical: L1a 存在 re-trials 且 "trial counts asymmetric"，不同模型实际调用次数与预算消耗不均，一个成功靠重试获得，破坏了 denominator discipline 与 cross-model 公平性，却仍报告分数并做跨模型描述性声称。
- - Critical: L1b 三模型均 0/10，floor effect 使该层零区分度，Friedman 16 paired tasks 中 10 个全零，p=0.37 形同虚设，却仍纳入 cross-model 统计与"稳定失败分类"的结论。
### Major（6）
- - Major: 推理超参数（temperature、top-p、max_tokens）、re-trial 上限与策略、1000-call budget 在 task/model/seed 间的分配规则均未披露，复现性与公平性双受损。
- - Major: seed 管理不透明：仅提"per-seed rows"但未给出 seed 数量与方案，且 bootstrap at seed level 列为 future work，所有点估计无置信区间/不确定性量化。
- - Major: 消融不完整：仅 L2 有 A vs CG 消融（且已失效），L1a/L1b 缺 harness 组件、LLM-as-judge、denominator 规则等消融，无法定位性能来源。
- - Major: 基准公平性未论证：三模型异构（gemma2 vs qwen2.5、9B/7B/14B、不同家族与参数量），同端点下是否用一致超参未说明；Model-F 仅 exploratory 且用 "opencode.ai alias" 匿名，不参与主比较却作 frontier 参照，可比性存疑。
- - Major: 泛化性严重不足：仅 3 个 7B–14B 开源模型、每层任务数极小（L1a=6/L1b=10/L2=4），N=4 功效下 d_min=2.13，外部效度低，无法支持"scientific agent 能力"的广义结论。
- - Major: LLM-as-judge 校准仅 21 gold、单标注者，FNR=FPR=0 时 rule-of-three 95% 上界≈14%，作为 L1b 唯一评分依据的 judge 公平性与可靠性证据过弱。
### Minor（3）
- - Minor: positive control 仅定性证明 pipeline "solvable"，未量化 solvability margin，对照强度单薄。
- - Minor: post-hoc subset 分析明示为 non-confirmatory sensitivity，却仍出现在 appendix，存在选择性报告风险。
- - Minor: 三层统计协议虽"统一脚本"，但各层样本量与功效差异巨大（L2 功效为 0、L1b floor-limited），统一协议并未带来可比结论。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 三层基准（AIRS-Bench、ResearchClawBench、GAIA2 p3dev）均为既有数据集的直接复用，论文未构造任何新任务、新能力轴或新评测维度；所谓"unified benchmark"实质上是把三个现成 benchmark 装进同一个 `run.json` + SHA-256 脚本的"外壳"，核心贡献是 orchestrator/harness 而非 benchmark 本身，但标题与摘要以"A Unified Benchmark"自称，存在显著的概念偷换与贡献夸大。
- - Critical: 摘要自曝三层统计结果全部不可用或无信息量——L2 McNemar 因 $n_d=0$ 结构性失效、L1b 全部 0/10 触发 floor、Friedman $p=0.37$ 非显著且自标"exploratory"。这意味着论文引以为豪的"three-layer statistical protocol"在其实际实验中从未产出任何有效结论，统计协议的贡献既未被验证也未被 demonstration，被当作核心卖点过度宣传。
### Major（5）
- - Major: 所声称的 GAP"evaluation remains fragmented"是领域内陈词滥调，且已有 OpenCompass / HELM / lm-eval-harness / BIG-bench 等成熟"统一 harness + 可复算"框架；intro 仅泛引 GAIA、SWE-bench、MATH 等单点 benchmark，刻意回避与"unified evaluation harness"类文献的正面对比，导致差异性与增量贡献无法判定——GAP 是否真实、是否已被既有 harness 解决，论文未给出任何对照论证。
- - Major: "byte-level reproducibility"被刻意限定为"125 committed files, not live LLM outputs"——即 SHA-256 只覆盖提交的中间文件而非 LLM 调用本身；考虑到温度/采样的不确定性，所谓"reproducibility contract"对最不可复现的环节（LLM 输出）恰恰不适用，"reproducible benchmark"作为标题级卖点被夸大，且未与已有的 LLM 评测复现难题文献（如 nondeterminism-by-design 讨论）对话。
- - Major: "two arms A=baseline ReAct vs CG=completion-guided harness"的对比在摘要中显示两臂 goal completion 完全相同（0.14/0.19/0.28），即 CG harness 毫无增益；该"双臂设计"既无统计显著性（McNemar 失效）也无效应量差异，却被列为 suite 的方法学卖点之一，增量贡献为零却未被诚实降级。
- - Major: "denominator discipline（失败计零并保留分母）""judge calibration with FNR/FPR gates""budget cap 1000 calls"均属评测工程常识，并非方法学创新；论文将其与真正的研究贡献并列陈述，构成把工程规范包装为学术贡献的增量夸大，且未与已有 judge calibration 文献（如 LLM-as-judge bias/cost 文献）做增量对比。
- - Major: 实验规模极小（L2 仅 4 scenario、L1a 仅 6 task、L1b 仅 10 task；N=4，power 显式不足 $d_{\min}=2.13$），却以"suite"之名宣称覆盖"prediction / workflow / execution"三大科学能力；样本量不足以支撑任何跨能力、跨模型的概括性结论，覆盖广度的声称与实际证据体量严重不匹配，属 GAP 真实性层面的以偏概全。
### Minor（2）
- - Minor: L1a 的"denominator discipline"在 6 个任务上、且 7b 为 0/6 的情况下，"TextSimilarity intention-to-treat mean 0.355"与硬指标 0/6 并存，存在用连续相似度分数稀释硬失败信号的嫌疑，但论文未说明该软指标是否进入主结论，贡献边界模糊。
- - Minor: 摘要中"frontier reference Model-F (opencode.ai alias) scored 6/6 (exploratory)"作为孤立正例被提及，既未纳入统计对比、也未定义"frontier"边界，容易被读者误读为 suite 能区分强弱模型的能力证据，属于用未受控的旁证间接抬高 suite 价值。

## 可复现（repro）— ok
### Critical（3）
- - Critical: "byte-level reproducibility" 的 SHA-256 封印明确标注 "not live LLM outputs"——只对 125 个提交文件做哈希，而真正的实验产物（LLM 原始输出）既未哈希校验、也无法字节级复现（LLM 非确定性）；证据链在最关键一环断裂，"byte-level reproducibility" 构成误导性表述。
- - Critical: 推理栈无配置快照——"rented cloud GPU" + "local OpenAI-compatible endpoint" 未指明推理引擎（vLLM/Ollama/llama.cpp）、GPU 型号、量化等级、temperature/top-p、模型权重 commit hash；缺任一项即无法复现单次调用。
- - Critical: 全文未给出所用 seed 取值与数量；"per-seed rows" 仅声明存在，seed 如何注入 LLM 采样、温度是否锁 0 均未说明，且自承 "bootstrap at step/seed level as future work"，seed 级复现缺失却以 "reproducible" 自居。
### Major（5）
- - Major: "Model-F (opencode.ai alias)" 以别名隐藏真实模型与 API 端点，其 6/6 前沿参考结果完全不可复现，且无对应配置快照。
- - Major: 数据许可未披露（AIRS-Bench / ResearchClawBench / GAIA2 p3dev），且各 benchmark 任务集未做版本/commit 钉定（rad 六任务、十任务、四场景的具体 ID 与快照缺失），任务漂移使复现者无基准可对。
- - Major: "18/18 independent recomputation checks" 实为从已存储 per-seed rows 重算聚合分数且 "without new LLM calls"，只校验统计脚本而非实验本身，属循环自证，不等于实验可复现。
- - Major: 缺少容器化镜像（Docker/Singularity）与依赖锁文件（requirements/conda lock），且 "rented cloud GPU" 为临时资源未留机器快照，部署环境不可复现，"fully recomputable harness" 名实不符。
- - Major: L1a "trial counts asymmetric / one success needed re-trials" 的重试策略与计分规则未形式化，影响 568 calls 预算核算与"哪次 trial 入分"的可复现性；Model-F 的 exploratory 调用是否计入预算亦未说明。
### Minor（3）
- - Minor: 可见文本未给出代码仓库 / manifest / recomputation 脚本的 URL 或 DOI，"release the suite" 无落地入口。
- - Minor: 判官校准仅 21 gold、单一标注者，未报告标注者间一致性（IAA），判官可复现性受限。
- - Minor: 标题 "A Unified, Reproducible Benchmark" 与正文 "not live LLM outputs / seed bootstrap 为 future work / N=4 功效不足" 等限定语不一致，存在过度承诺。

## 写作（writing）— ok
### Major（4）
- - Major: 摘要称“18/18 recomputation checks”与正文“every leaderboard number recomputed”矛盾——24+18+30=72 行数据中仅 18 项（恰好等于 L1a 行数）被核验，“every”疑为过度声明。
- - Major: 摘要写 goal completion â0.14/0.19/0.28 in both arms”，两个 arm 均值完全相同却未明言“两 arm 逐场景结果一致”；既然 n_d=0、两 arm 等价，双 arm 对比实为空比较，行文未区分“per-arm”与“pooled”。
- - Major: 摘要为单段~200词，嵌套~15 个统计量与多层括号（如 L1a 子句“one success needed re-trials; trial counts asymmetric…”），可读性差且未引用任何汇总表/图。
- - Major: âbyte-level reproducibilityâ(SHA-256 over 125 files)与“18/18 recomputation checks”紧邻并列，混淆了“文件完整性哈希”与“数值重算”两类可复现性，“not live LLM outputs”限定被掩埋，易误导。
### Minor（8）
- - Minor: 顺序不一致——摘要列“24 L2, 18 L1a, 30 L1b”（L2 在前），全文其他处均为 L1aâL1bâL2。
- - Minor: 术语漂移——摘要“three capabilitiesâvs正文“three layers”；摘要“AIRS-Benchâvs正文“AIRS-Bench rad”；缩写注释定义“GAIA”但正文用“GAIA2”。
- - Minor: CLES/ECE/TS 缩写定义仅存于 LaTeX 注释，正文“Wilcoxon+CLES”对读者未展开。
- - Minor: 过度精度——“$d_{\min}=2.1279$”在 N=4 下给出 4 位小数，暗示虚假精度。
- - Minor: 非标准/非正式术语——“denominator disciplineââanswer-fitting auditââintention-to-treatâârented cloud GPUââopencode.ai alias”，且 arm 标签“A vs CG”（非 A vs B）不对称。
- - Minor: Friedmanâ16 paired tasks (10 all-zero L1b)”把 N=16 前置，实际有效判别任务仅 6，应前景化“effective Nâ6”。
- - Minor: 预算核算不清——“568 calls (<1000)”未说明探索性 Model-F(6/6)及 re-trials 是否计入 568/预算。
- - Minor: 关键词“SciEvalSuite”与标题重复，属冗余 keyword。

## 伦理（ethics）— ok
### Critical（2）
- - Critical: 无数据许可披露 â 重用的 AIRS-Bench、ResearchClawBench、GAIA2 三套基准，12l项 SHA-256 密封提交文件，以及开放权重模型（Qwen2.5、Gemma2）均未声明许可证条款；在无许可声明的情况下宣称可重现/释放属合规风险。
- - Critical: 双盲破坏风险 â 论文声称 TMLR 匿名提交，却同时宣布公开发布含 125 个提交文件及 SHA-256 密封的 suite，并点名 "rented cloud GPU"、"opencode.ai"；提交文件（很可能在公开仓库）可通过 git 历史或基础设施指纹追踪去匿名化作者。
### Major（3）
- - Major: 未披露利益冲突 â "Model-F (opencode.ai alias)" 故意遮掩前沿模型真实身份，未给出化名理由，也无 COI 声明；若作者与 opencode.ai 或该模型供应商有任何关联，则构成隐瞒 COI。
- - Major: 隐私缺失 â GAIA2 任务源自真实网络内容，可能含 PII；文中朠提供 PII 审计、脱敏措施，也未披露租用云 GPU / 本地 endpoint 的数据处理与驻留条款。
- - Major: 误用/安全风险 â 释放的 harness 会本地执行模型生成的代码（L1a/L1b）并驱动交互式工具调用（L2），却未描述沙箱隔离、能力限制或滥用缓解策略；"fully recomputable" 降低了任意代码执行的门槛。
### Minor（1）
- - Minor: 单标注员 LLM-as-judge 校准（21 gold）未披露标注员身份/隶属，可能隐藏作者自标注偏见（COI/内部评分风险）。

## 汇总

- **Critical: 18 | Major: 31 | Minor: 21**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）