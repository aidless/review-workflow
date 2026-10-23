# 对抗审查报告

- 时间: 2026-08-27T10:30:30.399976+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（2）
- - Critical: L2 的两臂对比（A=ReAct vs CG=completion-guided）在 N=4、n_d=0 discordant pairs 下结构性地零功效；"both arms 均值相同"既不能支持"两臂等价"也不能支持"无差异"，却仍作为 L2 能力维度呈现，因果操纵实际上未被检验。
- - Critical: L1b 全模型 0/10 均为执行失败，LLM-as-judge 从未在真实模型输出上运行；在 21 条 gold 上校准的 FNR/FPR=0 无法迁移到"全部失败"的测量情境，构念效度（construct validity）失效——测到的是执行管道而非工作流质量。
### Major（6）
- - Major: Friedman 把 16 个"配对任务"与 10 个全零 L1b 任务、且混搭异质的 L1a（预测）与 L1b（工作流）能力合并；Friedman 假定有序变异与项目可公度性，地板效应+大量并列+跨层混池同时违反二者，p=0.37 不可解释。
- - Major: L1a 重试次数不对称（某成功需重试）是未受控混淆；标注为"descriptive"并不能在仍报告并比较分数时消除对内部效度的威胁，公平比较的前提（等试验预算）不成立。
- - Major: N=4（L2）/N=6（L1a）且种子数未在摘要中说明，d_min=2.13@80% power 意味着只能探测到巨型效应；所有"non-significant"结果与大真效应相容，故将结果作"无差异"框架是不恰当的因果/推断表述。
- - Major: 三模型在规模/家族/服务栈上不同，Model-F 又是不同服务栈的 API 前沿模型；跨模型比较将能力与服务/量化/上下文长度差异混淆（selection/serving confound），观测性比较却隐含能力排序。
- - Major: "18/18 重算校验"与 SHA-256 封章验证的是已提交文件的可复现性，而非方法论有效性；将可复现性呈现为稳健性证据，混淆了两个不同属性。
- - Major: LLM-as-judge 校准为单标注者（无标注者间一致性）、n=21 零误差（rule-of-three 上界≈14% FNR/FPR）；gold 标签可靠性与判官外推性均检验不足，"calibrated"前提脆弱。
### Minor（3）
- - Minor: "goal completion 0.14/0.19/0.28 in both arms"两臂完全相同未作解释；既可能表明两臂功能等价，也可能是 N=4 粒度无法分辨，削弱了"A vs CG 是有意义操纵"这一前提。
- - Minor: "oracle-free goal completion"的构念操作化在摘要中未受论证；无 oracle 时"目标完成"的判定规则本身即待验证的测量假设。
- - Minor: "统一基准"前提——假定代码执行/报告合成/工具使用三层在单一 run.json 契约下可公度——是未经检验的假设，统一性主张依赖于此。

## 统计（stat）— ok
### Critical（2）
- - Critical: Friedman 检验在 16 个配对任务上运行，其中 10 个任务三模型得分全为零（floor effect），大量并列值严重违反 Friedman 秩检验的排序假设；有效可区分样本仅 6 而非 16，检验结果实质无效。
- - Critical: 全文所有点估计（goal completion 均值 0.14/0.19/0.28、TextSimilarity 均值 0.355、L1a 0/6 与 2/6、L1b 0/10）均无方差、标准误或置信区间报告；bootstrap 被推迟为"future work"，导致所有效应大小无法判断精度。
### Major（6）
- - Major: 样本量极小（L2: N=4，L1a: n=6，L1b: n=10），披露的 d_min=2.1279 表明仅能检测到 Cohen's d>2 的巨型效应；在此功率下任何"非显著"结论均无信息量，不能作为"无差异"的证据。
- - Major: 存在大量多重比较（3 模型 × 3 层基准 + 附录 post-hoc 子集分析 + 探索性 frontier Model-F + Nemenyi 事后配对 3 对），全文未提及 Bonferroni/Holm/FDR 等任何校正；仅以"exploratory""non-confirmatory"标签规避不等于消除 I 类错误膨胀。
- - Major: 未报告任何观测效应量（CLES、Cohen's d、rank-biserial 等）；d_min 是最小可检测效应（功率分析量），非观测效应，无法据此评估实际显著性。
- - Major: 报告 Friedman p=0.37 并标注"非显著"，但该检验同时受 floor-limitation 与结构性欠功率双重污染；从无效检验得到的非显著 p 值不能解读为"组间无差异"。
- - Major: McNemar 检验设计本身结构性失效：N=4 且 n_d=0（附录 N=8 亦 n_d=0），检验功率恒为零；在此条件下仍将 L2 纳入"统一评估套件"的三层之一，造成套件整体统计有效性的虚假承诺。
- - Major: Nemenyi 事后检验隐含 3 对模型两两比较，需族水平校正，但正文与摘要均未说明 Nemenyi 的显著性与 CD 值是否在多重比较校正后的阈值上判定。
### Minor（2）
- - Minor: LLM-as-judge 校准仅 21 个 gold 样本、单一标注者，报告 FNR=0.00、FPR=0.00；rule-of-three 95% 上限 ≈14% 意味着真实错误率可能相当高，且未报告标注者间一致性（Cohen's κ）。
- - Minor: L1a 中"one success needed re-trials; trial counts asymmetric"引入了试验次数不对称导致的偏倚，仅以"cross-model claims descriptive"标签回避，未做任何统计控制或敏感性分析。

## 实验（experiment）— ok
### Critical（2）
- - Critical: L2 的核心消融（A=ReAct vs CG=completion-guided）在三个模型上得到完全相同的目标完成度（0.14/0.19/0.28 "in both arms"）且 discordant pairs $n_d=0$，McNemar 结构性失效——这要么说明 CG 干预零效应，要么是 harness 实现错误，而论文没有任何诊断来区分二者，等于消融实验形同虚设。
- - Critical: L2 样本量 $N=4$（附录 $N=8$）且作者自承 McNemar power 结构性为 0、$d_{\min}=2.1279$——整个 L2 统计层不是"低功效实验"而是"非实验"，样本量由 1000-call 预算倒推而非功效驱动，设计层面即无效。
### Major（8）
- - Major: L1a 各模型 trial 数不对称（"one success needed re-trials; trial counts asymmetric"），跨模型得分（7b 0/6、14b 2/6、gemma 2/6）被 unequal trial budget 混杂，benchmark 公平性被破坏；"descriptive only" 声明并不能消除该混杂，应做 intention-to-treat 等trial 设计。
- - Major: 前沿参考 "Model-F (opencode.ai alias)" 是不透明的路由别名，后端模型随时可能更换、不可复现，其 6/6 探索性结果无法锚定任何跨层级（frontier vs. small open-weight）的对比主张，对照组本身不可信。
- - Major: 摘要未披露任何解码/服务超参数（temperature、top-p、max_tokens、量化等级、GPU 类型/并发），三个模型在同一 cloud GPU 上的公平性（是否同量化、同上下文窗口、同系统提示）无法核验。
- - Major: 摘要反复宣称 "per-seed rows" 与 "seed/step 级 bootstrap（future work）"，但从未说明：用了几个 seed、seed 取值、seed 是跨场景还是跨模型、为何 L2 的 $N=4$ 看似是场景数而非 seed×场景——seed 管理在论文层面对外不可见。
- - Major: L1b 三个模型全部 0/10（执行失败）且 Friedman 中混入 10 个全零任务，floor effect 把 ties 拉满使 $p=0.37$ 的跨模型检验在数学上几乎不可能显著；基准难度严重失配，却未报告任务难度校准或难度分层。
- - Major: 除 CG 臂外没有任何组件消融：answer-fitting audit（"intercepting 3/3 models"）、judge 校准、harness contract 均为断言式存在，audit 自身的 FP/FN 特征、judge 替换敏感性、contract 字段必要性均未消融。
- - Major: LLM-as-judge 仅 21 gold、单一标注者、无 inter-annotator agreement；FNR=FPR=0.00 配 rule-of-three 上界 ~14%，意味着校准门仍可能放行大量错判，且 single-annotator 使 FNR/FPR 估计本身不可靠。
- - Major: 泛化性极弱：仅 3 个 7b–14b 量级开放权重模型，无任何真实 frontier 开放权重模型直接受测（仅经不透明别名间接），suite 在其本应最有区分度的强模型区间上的行为完全未知。
### Minor（1）
- - Minor: L1b 的 "positive control demonstrates pipeline solvability" 未描述该对照 agent/配置，可解性主张在摘要层不可核查。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 所谓"统一基准"实质是把三个已存在基准（AIRS-Bench、ResearchClawBench、GAIA2）打包进同一个 run.json 契约，未引入新任务、新能力维度或新评测方法论；声称的 GAP（"评测碎片化"）是工程包装问题而非开放研究问题，且未与 HELM/BIG-bench 等已有"统一套件"路线对比以证明该 GAP 真实且未被解决。
- - Critical: 实证结果无法支撑基准的核心价值：L2 仅 N=4 且 n_d=0（McNemar 不可用、power 结构性为 0）、L1b 三个模型全 0/10（地板效应、Friedman p=0.37）、L1a 多为 0–2/6；作为基准它在本论文范围内不具备区分模型的能力，贡献主张与证据严重不匹配。
### Major（3）
- - Major: "三层统计协议"（exact McNemar、Wilcoxon+CLES、Friedman+Nemenyi+CD）均为教科书非参数检验，套用到 agent 评测不构成方法创新；论文未将其与现有 agent 评测的统计实践对照，无法说明填补了何种统计缺口。
- - Major: 可复现性贡献被夸大：SHA-256 封印显式声明覆盖的是"已提交文件而非实时 LLM 输出"，只校验静态产物；"独立重算"是对已存的 per-seed 行做确定性聚合，本就是可复现的平凡操作，未超越标准 leaderboard 的复算水平。
- - Major: "denominator discipline"（失败计零并留在分母）与"answer-fitting audit"被当作贡献呈现，实为代码生成/agent 评测中的基础评测卫生与污染检查（如 SWE-bench 执行评分、contamination filtering），增量被膨胀表述。
### Minor（2）
- - Minor: 仅三个 7b–14b 小模型加一个"探索性"前沿参照（Model-F=opencode.ai 别名，6/6 单点），未系统对照这些模型在既有基准上的分数，无法证明本套件产出了超越现有基准的新发现。
- - Minor: 引言声称"区分真正科学推理与执行失败/契约违规"未落地为可量化的新指标；提及的 failure taxonomy 未与代码/agent 评测中既有错误分类法对比，难以认定其增量。

## 可复现（repro）— ok
### Critical（3）
- - Critical: SHA-256 印章明确标注覆盖"125 committed files (not live LLM outputs)"，即真正承载结果的 LLM 原始生成轨迹未被哈希/封存，却声称"byte-level reproducibility"——证据链从 raw LLM trace → 汇总数字这一段是断的，印章只验证了代码/配置，未验证实验证据本身。
- - Critical: Model-F 仅以"opencode.ai alias"出现，无模型版本钉死、无权重哈希、无 API 快照；alias 会随时间重路由到不同后端，掺入该不可复现的 frontier 参考会污染整个 suite 的复现契约。
- - Critical: 推理配置快照缺失——"rented cloud GPU"未说明 GPU 型号/厂商/推理引擎（qwen2.5:7b 的冒号命名暗示 Ollama 但未确认）、量化等级（q4/q8/fp16？）、引擎版本、chat template 与 system prompt；同一开权重模型不同量化下分数差异显著，无此快照结果不可复现。
### Major（5）
- - Major: 反复引用"per-seed rows"但摘要未给出 seed 取值、数量、选择依据；又自承"bootstrap at step/seed level as future work"，即 seed 级方差根本未刻画，per-seed 复现性无法被独立校验。
- - Major: L1a"one success needed re-trials; trial counts asymmetric"——非对称重试破坏固定预算(1000)/固定分母契约；568 calls 无法与确定性 per-seed 调度对账，且重试策略（何时重试、上限几次）未规约，复现者无法重现同一调用序列。
- - Major: "18/18 independent recomputation checks"与报告的 24+18+30=72 行粒度不匹配且未解释；且该脚本只是对已保存行重新聚合，并非重新跑 LLM，因此只验证了"算术可复现"而非"实验可复现"，措辞存在误导。
- - Major: 数据许可（AIRS-Bench、ResearchClawBench、GAIA2）完全未声明；125 committed files 是否包含数据集产物（潜在许可违规）或需另行获取（破坏一键复现）均不明确。
- - Major: 无环境/容器制品（Dockerfile、requirements.txt、env lock）描述，"rented cloud GPU"是临时环境，跨机器/跨主机一键复现未给出任何证据。
### Minor（3）
- - Minor: 三个开权重模型未提供权重哈希（如 HuggingFace commit SHA 或 GGUF sha256），无法对账被加载的具体权重。
- - Minor: 采样参数（temperature、top_p、max_tokens）未声明；对随机 LLM 而言仅凭"seed"不足以复现采样轨迹。
- - Minor: recomputation"via a separate scipy path"未钉死 scipy 版本，数值路径跨版本可能漂移，削弱独立对账的可重复性。

## 写作（writing）— ok
### Critical（2）
- - **Critical**: 摘要称"three **capabilities**"，æ­£æå¼è¨ç§°"three **layers**"——核心贡献的框架词在摘要与正文间不一致，读者无法确定到庆是"能力维度"还是"层次结构"。
- - **Critical**: L2 的 McNemar（二分检验）报告 $n_d{=}0$，却同时给出连续型 "mean goal completion"（0.14/0.19/0.28）；这些均值不是 $1/4$ 或 $1/8$ 的整数倍，说明 goal completion 是连续分数，但二分化阈值（pass/fail cut-off）从未声明，统计检验与指标类型存在概念性错配。
### Major（7）
- - **Major**: 摘要单段塞入 30+ 个数字与缩写（24/18/30 rows、568 calls、125 files、18/18 checks、SHA-256、$n_d{=}0$、$N{=}4/8$、0.14/0.19/0.28、0/6、2/6、6/6、0/10、3/3、16 tasks、$p{=}0.37$、21 gold、FNR/FPR、14%、$d_{\min}{=}2.1279$……），无方法/结果/局限的结构分层，读如数据堆栈而非摘要。
- - **Major**: "Cross-model Friedman on 16 paired tasks (with 10 all-zero L1b tasks)"ââ16 = 6(L1a)+10(L1b) 隐式排除了 L2 的 4 个 scenario，但排除原因从未说明，读者必须自行反推算术。
- - **Major**: "TextSimilarity intention-to-treat mean 0.355" 在摘覄中首次出现，无定义、无单位、无引用，突光嵌在 L1a 的括号长句内，属未定义术语突然引入。
- - **Major**: "trial counts asymmetric, cross-model claims descriptive" 为碎片化短语，缺主谓宾，不是完整句子，可读性极差。
- - **Major**: "SHA-256 seal over 125 committed files (not live LLM outputs)"——括注 "not live LLM outputs" 意义不明；committed files 本就不是 live outputs，此区分无前提说明，反而制造困惑。
- - **Major**: 缩写注释列出 ECE、TS、CLES，但这些缩写在可见正文中均未出现；GAIA 展开为 "General AI Assistant" 但文中用的是 "GAIA2"；"etc. defined" 是占位符式表述。
- - **Major**: $N{=}4$（主）与 $N{=}8$（supplement）的关系未说明——supplement 多出的 4 个 paired observation 从何而来？与前文 "four scenarios" 的关系不清，数字来源断裂。
### Minor（4）
- - **Minor**: $d_{\min}{=}2.1279$ 给出五位有效数字，对 power 计算而言精度过剩，显得人为精确。
- - **Minor**: 摘要称 "AIRS-Bench"，正文称 "AIRS-Bench **rad**"；摘要省略的 "rad" 后缀在正文突然出现，基准命名不一致。
- - **Minor**: "opencode.ai alias"、"21 gold" 含义不明（21 gold 什么？items / examples / labels？）；SciEvalSuite 既在标题又在 Keywords 中，冗余。
- - **Minor**: 可见文本无任位置引用 Table / Figure 编号，摘覄大量结果无处可查，图表引用缺失（可能因截断，但截断部分前已存的正文同样无引用）。

## 伦理（ethics）— ok
### Critical（3）
- - Critical: 全文未声明任何数据集许可——AIRS-Bench、ResearchClawBench、GAIA2 p3dev 三套基准及 125 个提交文件的许可证、再分发权、第三方数据来源均未披露，存在侵权与不可复现的法律风险。
- - Critical: 双盲存在泄露风险——文中出现 `opencode.ai alias` 指名商业 API、`corresponding@example.com` 占位邮箱、"rented cloud GPU" 服务来源，任一真实信息即可反推作者身份或所属机构，违反 TMLR 双盲要求。
- - Critical: 缺少伦理审查/IRB 声明——"21 gold, single annotator" 涉及人工标注与人工评判，未说明标注者是否知情同意、是否经伦理委员会批准、标注者身份与隐私保护。
### Major（4）
- - Major: 完全没有利益冲突（COI）声明——Model-F 使用 opencode.ai 商业 API、租用云 GPU 服务商、LLM-as-judge 服务提供方，均可能存在商业或合作关系却未披露。
- - Major: 隐私保护缺失——GAIA2 场景为真实网页/工具交互任务，可能涉及第三方个人数据；缓存并提交的 125 个文件与"live LLM outputs"是否含可识别个人信息（PII）未做脱敏与合规说明。
- - Major: 模型权重许可未说明——qwen2.5（Qwen 许可）、gemma2（Gemma Terms of Use）各自的使用条款与商用限制未引用，下游复现者无法判断合规边界。
- - Major: 误用/双用风险未讨论——基准包含代码生成与本地执行、报告合成、工具交互，且已证实"answer-fitting"作弊能力，可被用于生成伪造研究报告或恶意代码，全文无 responsible use、安全过滤或危害缓解措施章节。
### Minor（2）
- - Minor: LLM-as-judge 标注与评判均依赖单一标注者且未声明其与作者的关系，存在评判偏见与隐性利益冲突。
- - Minor: 未说明生成代码执行沙箱隔离与副作用控制，若基准被复用执行不可信代码，存在安全与合规隐患。

## 汇总

- **Critical: 16 | Major: 39 | Minor: 17**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）