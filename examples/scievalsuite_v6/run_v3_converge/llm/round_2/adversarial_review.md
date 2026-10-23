# 对抗审查报告

- 时间: 2026-08-26T04:41:57.982496+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（3）
- - Critical: McNemar 测试在 N=4、n_d=0（零不一致对）时 p=1.0000 无法支持“两组无差异”的结论；CI [0,0] 退化为点，属于“缺乏证据”而非“无差异的证据”，将功率披露不等价于推断合法性。
- - Critical: LLM-as-judge 在实际评分轮次中“零次调用（全 SKIP）”，校准集与实际被评数据完全脱节，把校准当作“方法学担保”存在外部效度断裂；校准仪在空转。
- - Critical: âcurated L1a（6 tasks, k=4, exploratory）仅在 fail-as-worst 编码下 p=0.0026”是子集选择 + 编码方案选择后才显著，属于多重比较下的 p-hacking / specification search，且全文未见对多次检验做校正。
### Major（5）
- - Major: L1b 三模型全得 0/10，存在严重地板效应；在无分离度的前提下“稳定失败分类法”与“L047 审计 3/3 命中”对模型能力差异不具判别力，内部效度存疑。
- - Major: âsimulated second annotator Î±=0.894”系模拟而非真实第二标注者，不能作为标注一致性的证据；将模拟值当作观察信度违背假设。
- - Major: gemma L1a 既报“2/6”作头条，又报 ITT 均值 0.355（含一次失败计 0），两套报告口径不一致；三次“独立试验”后选 2/6 有 selective reporting 嫌疑，ITT 框架在此缺乏清晰的“处置”定义。
- - Major: 跨模型比较（7b/14b/9b、Qwen vs Gemma）同时混淆模型规模与架构家族，Friedman 不显著不能归因于其中任一因素，因果归因不合适。
- - Major: N=4/模型的 L2 实验严重不足功率（McNemar 功率 0.0000@n_d=4）；披露功玖限制并不消除对“completion-guided harness 无效”这一因果性结论的反驳。
### Minor（3）
- - Minor: âbyte-for-byte reproducibilityâ(SHA-256)只证明确定性，不证明效度；确定性地输出错误仍是错误。
- - Minor: P5 frontier（muse-spark-1.2-contributor 6/6）与本地小模型比较存在规模/数据/训练流程混淆，p=0.0026 标为“exploratory”位置与主结论边界模糊。
- - Minor: 校准仪在 FPR=0 门控下，11 正/10 负的校准集过小，Wilson 0.28 区间宽；FPR=0 本身易通过高阈值达成，缺乏诊断性。

## 统计（stat）— ok
### Critical（3）
- - Critical: L2 主要统计检验为 exact McNemar，但 $n_d=0$（零不一致对），检验完全退化。报告 $p=1.0000$ 和 95% CI $[0,0]$ æ¯éåæ 形下的数孼幻觉，不提供任何统计证据；将其作为"no statistically detectable difference"的支撑是对 $p$ 值的严重误用——$p=1$ 不等仁"证明无差异"，而是"检验无法提供信息"。
- - Critical: 样本量 $N=4$，自报 $d_{\min}=2.1279$（Cohen's $d>2$ 属于"极端大效应"，在实际研究中几乎不可能出现），McNemar power $=0.0000$ at $n_d=4$。设计在检测任何现实效应方面彻底无效，即便宣称"披鲲 power limits"，摘要仍以"L2 showed no statistically detectable difference"框定结论，这是将零功率结果伪装为阴性发现。
- - Critical: 存在大量并发检验（L2 McNemar、L1a curated Friedman、P5 frontier $p=0.0026$、L1b judge FNR/FPR gate、cross-model Friedman等），全文无任何多重比较校正（无 Bonferroni、Holm、FDR）。$p=0.0026$ 在 P5 frontier 与 curated L1a 两处出现，明显是从多个探索性分析中挑选出的最小 $p$ 值，属 selective reporting。
### Major（6）
- - Major: "curated L1a (6 tasks, k=4, exploratory) gives $p=0.0026$ **only under fail-as-worst encoding**"——显式承认尝试了多种编码方案，仅报告产生显著性的那一种，是经典的 specification-curve / p-hacking 行为；标注"exploratory"不构成正式校正。
- - Major: 报告了均值（goal completion $0.1418$/$0.1918$/$0.2750$；L1a 各分数）但未报告任何方差度量（SD、SE、CI、IQR）。对于小样本，点估计没有不确定性区间是不可接受的；无法判断值的稳健性。
- - Major: "simulated second annotator $\alpha=0.894$"——模拟的标注者产生的 Cohen's $\alpha$ 不是真实的 inter-annotator agreement，是循环验证（用模型模拟标注者再用其一致性证明 judge 可靠），方法论上无效。
- - Major: Judge 校准（21 gold，11 positive/10 negative）在 FPR$=0$、FNR$=0$ 条件下"通过"，但实际运行中"zero judge calls (all SKIP)"。统计检验从未被实际执行，校准结果是空操作的方法论担保，不应作为有效统计证据报告。
- - Major: 效应量缺失。协议声明使用 CLES，但摘要中未报告任何主要对比的效应量（CLES、Cohen's $d$、rank-biserial 等），仅报告 $d_{\min}$（最小可检测效应）而非实际观测效应，违反不仅报告 $p$ 值还须报告效应量的规范。
- - Major: Friedman 检验在"16 paired tasks"上跨越 L1a（代码执行）与 L1b（报告合成）异质任务类型，不同任务的分数尺度不同，Friedman 排序检验假定同质性；混合异质任务使排名无统计意义。
### Minor（3）
- - Minor: Friedman omnibus 非显著（$p=0.3679$）却仍报告 Nemenyi CD$=0.8284$；应在 omnibus 显著后才进行 post-hoc，报告 CD 但不进行任何 post-hoc 对比是多余且易误导的。
- - Minor: "intention-to-treat mean $0.355$ including the failed trial as $0$"ââITT 将失败记为 0 在原则上可接受，但仅基于 3 次试验（其中 1 次失败）计算均值并报告 4 位小数（$0.355$）赋予了过高精度，应报告不确定性。
- - Minor: $p$ 值报告至 4 位小数（$p=1.0000$, $p=0.3679$, $p=0.0026$），对于此类样本量，超过 2-3 位小数的精度是虚假精度。

## 实验（experiment）— ok
### Critical（3）
- - Critical: L2 统计功效严重不足（N=4，McNemar power=0.0000 at n_d=4，n_d=0<6 not-detectable），"无显著差异"实为假阴性，无法区分"真无差异"与"检测不到差异"。
- - Critical: 全文未报告任何生成超参数（temperature、top-p、max_tokens、num_predict 等），单次采样结果无法复现，也无法判断各模型是否在可比解码设置下评测。
- - Critical: seed 管理缺失并自认"bootstrap at step/seed level 为 future work"；gemma 的"three independent trials"、36 extra trials 的 seed 控制与随机性来源均未说明，无法判断多试验间变异来自模型还是 harness。
### Major（10）
- - Major: L1b 三模型全部 0/10 地板效应，cross-model Friedman（χ²=2.0, p=0.3679）non-significant 很可能仅由地板导致，而非模型间真无差异，结论被混淆。
- - Major: L1a 7b 同样 0/6 地板，无法区分该模型与 14b/gemma 的真实能力差距，cross-model 比较在该模型上无信息量。
- - Major: 消融不完整——A/F（baseline ReAct vs completion-guided harness）仅 L2 层有对照，L1a、L1b 完全无 arm 对照，无法判断 completion-guided harness 对预测/工作流是否同样无影响。
- - Major: L047 answer-fitting audit 拦截 3/3 模型，但无"无 audit"对照臂，audit 的因果作用与拦截率无法量化，可能高估或低估 answer-fitting 发生率。
- - Major: 三模型参数量不同（7B/9B/14B）直接横向比较且参与 Friedman，未对参数量做归一或分层，公平性存疑（14B 优势可能被 L1b 地板掩盖，也可能在 L1a 被夸大）。
- - Major: curated L1a（6 tasks, k=4）的 p=0.0026 仅在 fail-as-worst encoding 下成立，结果对任务子集筛选与失败编码方式高度敏感，未经多种编码（fail-as-zero、fail-excluded、rank-based）系统稳健性验证。
- - Major: LLM-as-judge（llama3.1:8b）该轮 zero judge calls（all SKIP），FNR=FPR=0 的校准只是方法学承诺而非实测；判分臂实际未运行，L1b 报告覆盖率打分的可靠性未在本轮被验证。
- - Major: L1b 正对照仅 1/4 单任务 Chemistry_000，pipeline 可解性证据过于单薄，无法排除"任务本身不可解"导致 0/10 的混淆。
- - Major: P5 frontier muse-spark-1.2-contributor 与三个小模型（7-14B）非同级别，作为对照/上限基准不公平，6/6 与小模型差距更多反映模型规模而非 harness 或任务设计差异。
- - Major: 仅评测 3 个本地小模型（7-14B），无大模型、无闭源模型，结论向更广模型规模与架构的泛化性证据不足。
### Minor（3）
- - Minor: 三层任务数不一致（L1a /6、L1b /10、L2 /4），原始分数跨层不可比，且 L2 仅 4 场景使 per-model 方差估计极不稳定。
- - Minor: 单一部署环境（AutoDL RTX3090, ollama 0.32.13）、单硬件批次，未在不同硬件/推理后端验证可复现性，byte-for-byte 复现声明仅对单一环境成立。
- - Minor: 568 calls 中 36 extra trials 的触发条件、来源与是否纳入分母的规则未说明，denominator discipline 在额外试验上的执行不透明。

## 新颖性（novelty）— ok
### Critical（3）
- - Critical: 核心贡献"统一三层基准"的 GAP 被夸大——L1a/L1b/L2 三个组件分别对应 AIRS-Bench、ResearchClawBench、GAIA2 p3dev，看似均为既有基准的再打包，真正的增量仅是 `run.json` 契约与"分母纪律"这类工程规约，缺乏与既有统一型 agent 基准（如 AgentBench、ScienceAgentBench、SciCode 等多能力评测工作）的逐项差异对比，"碎片化"痛点未被具体文献佐证。
- - Critical: 引言唯一引用 `\citep{goodfellow2016deep}` 用以支撑"scientific agents are advancing rapidly"，与论点几乎无关，暴露相关工作定位缺失，无法支撑"与现有文献差异"这一新颖性主张。
- - Critical: 经验贡献基本为空结果——L2 两臂无统计可检测差异（McNemar p=1.0000, n_d=0）、L1b 全模型 0/10、跨模型 Friedman 非显著（p=0.3679）；唯一显著结果（L1a p=0.0026）被自标为 exploratory 且仅在使用 fail-as-worst 编码时成立。一个首次全量运行即无法区分模型/臂的基准，其判别力贡献存疑。
### Major（3）
- - Major: "三层统计协议"（exact McNemar、Wilcoxon+CLES、Friedman+Nemenyi+CD）全部为现成标准检验，应用于 agent 评测并非方法新颖性，且未与既有 agent 评测的统计实践对照，增量被包装为创新。
- - Major: LLM-as-judge 校准被列为 suite 覆盖能力之一，但实际该轮"zero judge calls (all SKIP)"，校准仅是 methodological warrant 而非已验证能力，贡献被前置夸大。
- - Major: 可复现性机制（SHA-256 manifest、18/18 recomputation checks）是良好工程实践而非研究贡献，现代基准普遍具备此类 artifact，不应作为核心新颖性论点。
### Minor（2）
- - Minor: "denominator discipline（失败计零并保留分母）"属评测基本卫生，非可声称为创新协议的内容。
- - Minor: 样本量极小（L2 N=4，McNemar power=0.0000 at n_d=4），即便作为"预算受控"基准，其所能支撑的贡献证据强度被进一步削弱，但作者已部分披露，属次要。

## 可复现（repro）— ok
### Critical（4）
- - Critical: 全文宣称"byte-for-byte reproducibility"，但未披露任何 LLM 采样 seed/temperature/top-p 等采样参数；ollama 默认非确定性，未固定 seed 时"逐字节可复现"在物理上不成立。
- - Critical: SHA-256 对账自相矛盾——主轮 46 条、P5 轮 165 条，而总调用 568 次（532+36），未入账调用占绝大多数，"byte-for-byte"证据链不闭合、覆盖率严重不足。
- - Critical: LLM-as-judge 校准"该轮零调用（全 SKIP）"却声称通过 FNR=0/FPR=0 门控；校准证据来自未实际执行的运行，第三方无法复现该 0/0 结果。
- - Critical: "simulated second annotator α=0.894"——模拟标注者需要 seed 与模拟模型，二者均未披露，α 既不可对账也不可复现。
### Major（7）
- - Major: 缺配置快照：未固定 ollama 模型 digest/权重哈希、CUDA/驱动/OS/Python 版本、harness 代码 commit；仅给"ollama 0.32.13 + AutoDL RTX3090"不足以重建运行环境。
- - Major: 未提供一键复现入口（容器镜像/仓库 URL/DOI/Makefile），抽象承诺"fully recomputable harness"但无落地证据。
- - Major: 数据许可缺失：AIRS-Bench、ResearchClawBench、GAIA2 均为第三方数据集，未声明各自许可证与再分发条款，复现者无法合法对齐数据源。
- - Major: "36 extra trials"的增补触发规则与任务选择标准未说明，存在选择性增补风险，破坏 run.json 复现契约的确定性。
- - Major: P5 frontier "muse-spark-1.2-contributor" 无访问途径/权重来源/版本 digest，第三方无法复现该 6/6 结果。
- - Major: McNemar n_d=0<6 自述"not-detectable"且 McNemar power=0.0000，却仍报 p=1.0000 并下"两臂无差异"结论；N=4 下该结论不可稳定复现。
- - Major: "18/18 recomputation checks"未定义"recomputation"语义（从存档输出重算分数 vs 重新生成输出），若为前者则属同义反复，不构成真复现证据。
### Minor（4）
- - Minor: "three independent trials"未说明独立性指代（不同 seed/不同会话/不同机器），复现者无从对齐方差来源。
- - Minor: ARS v3.11、L047 audit 等内部协议仅给版本号无规范引用或哈希，复现者无法定位定义。
- - Minor: 单标注员 21 gold 的人工标注协议未存档（标注指南、顺序、耗时、录用规则），金标的人工复现性弱。
- - Minor: "curated L1a (6 tasks, k=4)"的筛选准则未固化，任务子集选择本身是不可复现的隐性配置。

## 写作（writing）— ok
### Critical（2）
- - Critical: 摘要寫 `39 gold, 30 real+9 synthetic+1 attack`，但 30+9+1=40â 39，數字直接矛盾。
- - Critical: LLM-as-judge 稱「passed at FNR=0.0000, FPR=0.0000」，卻同句承認「zero judge calls (all SKIP)ãï¼æªå·è¡ä»»ä½å¤æ·å³å®£ç¨±ééï¼æè¦å §èªç¸çç¾ã
### Major（7）
- - Major: 術語不一致——摘要寫 `AIRS-Bench`，引言寫 `AIRS-Bench rad`，缺少後綴 `rad` 的說明。
- - Major: P5、ARS v3.11、L047、p3dev ååè¡èªå¨æè¦èå¼è¨ä¸­åå¾©ä½¿ç¨ï¼å §åæªå®ç¾©ã
- - Major: 引言列出三層統計協議含 `Wilcoxon+CLES`，但摘覃完全未提及，摘要與正文描述矛盾。
- - Major: 摘要約 400+ 詞，嵌套 30+ 個數值與統計量，遠超 TMLR 摘要常規範圍，結構失衡。
- - Major: 實驗組標籤為 A 與 F，BâE 缺失，未給出命名理由。
- - Major: `46-entry SHA-256 manifest` 與 `165 entries with P5` 的關係未說明，讀者無法判斷兩者是子集、補充還是獨立測試。
- - Major: `cloud-hosted local models` 是自相矛盾的術語，應區分「雲端 GPU 實例上本地推理」或統一表述。
### Minor（4）
- - Minor: 95% CI `[0,0]` 為退化區間，無統計意義，卻以數值形式呈現，易誤導讀耞。
- - Minor: `McNemar power 0.0000 at n_d=4` å ±è¨æª¢å®åæçºé¶æ¥µä¸åçï¼å³ä¾¿æ¨£æ¬æ¥µå°ä¹ä¸æçºç²¾ç¢ºé¶ã
- - Minor: P5 `muse-spark` 第六任務得分 0.0105 被計入 6/6，但未定義「通過」閾值，0.0105 與 0.5607 同視為 pass 缺乏合理性。
- - Minor: ITT mean `0.355` 無法從給出的 `0.2000Ã3`、`0.5330Ã2`、failed=0 透明推導，數字可復現性存疑。

## 伦理（ethics）— ok
### Critical（3）
- - Critical: 双盲风险——摘要暴露特定云平台 AutoDL、精确版本号 ollama 0.32.13、内部模型名 muse-spark-1.2-contributor 与代号 L047，多个可逆推作者身份/地区的信号，违反 TMLR 匿名提交协议。
- - Critical: 利益冲突未披露——P5 评测对象 muse-spark-1.2-contributor 可能是作者自有/参与贡献的模型，无 COI 声明，自评自家前沿结果 6/6 存在偏见风险。
- - Critical: 数据许可缺失——AIRS-Bench、ResearchClawBench、GAIA2 p3dev 以及 Zinc、TextClassification 等上游数据集的许可证、使用条款、再分发权利均未说明，套件声称“release”存在侵权风险。
### Major（4）
- - Major: 隐私审查缺失——GAIA 类任务可能含真实网页/个人信息，L1b 生成报告经 LLM 评判，无 PII 脱敏、数据来源隐私审查或匿名化处理的记载。
- - Major: 人体受试/标注无伦理审查——“single annotator, 21 gold”涉及人工标注，未披露 IRB/伦理审批、标注者知情同意及劳动报酬情况。
- - Major: 误用风险未讨论——基准测试代理的代码生成+本地执行、多步工具调用能力，属双用风险，无沙箱安全策略、负责任使用声明或误用缓解章节。
- - Major: judge 校准中 â1 attackâ 条目未说明性质与安全影响——对抗性样本的构造与防御目的缺乏描述，存在评判被操纵的合规漏洞。
### Minor（1）
- - Minor: 发市的 46/165-entry SHA-256 manifest 可指纹化数据集，且未声明套件自身的开源许可证，影响下游合规复用。

## 汇总

- **Critical: 21 | Major: 42 | Minor: 20**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）