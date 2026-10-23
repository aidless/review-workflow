# 对抗审查报告

- 时间: 2026-08-26T04:34:13.672339+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（5）
- - Critical: L2 仅 N=4 且 McNemar 功效为 0.0000，由"未检测到差异"推出两臂无差异/干预无效属于 absence-of-evidence 谬误，因果推断不成立。
- - Critical: McNemar n_d=0、配对差异 CI 退化为 [0,0]，无法排除 completion-guided harness 根本未生效（干预未实施），混淆了"未实施"与"无效"。
- - Critical: L1b 所有模型 0/10，positive control 仅 Chemistry_000 1/4 单例，无法排除"任务不可解/harness 缺陷"这一混淆，内部效度不足以区分模型无能与评测失效。
- - Critical: P5 muse-spark 与 qwen/gemma 在规模、训练数据、对齐上完全不可比，作为对照存在强混淆变量，6/6 与 0/2/1 之分不能做因果归因。
- - Critical: LLM-as-judge 校准仅 21 样本（11/10），FNR=0/FPR=0 但真实 FPR 的 95% 上界可达约 0.26（Wilson 0.28 已暴露），且实际轮次零调用（all SKIP），"校准可外推到真实任务"这一前提不成立。
### Major（5）
- - Major: gemma L1a 由 1/6 经三次试验升为 2/6，疑似选择性保留较优结果；把 failed trial 记 0 的 ITT 假设取决于失败是模型原因还是 infra/harness 原因，二者混淆。
- - Major: Friedman 前提（连续型、块内独立）在 0/1 小整数得分且同模型跨任务可能非独立时不成立；在 Friedman 非显著下报告 Nemenyi CD=0.8284 无意义。
- - Major: p=0.0026 仅在 fail-as-worst 编码下出现、标注为 exploratory 却未做多重比较校正，结论对编码假设敏感且 p 值解释不当。
- - Major: byte-for-byte 可复现性在 LLM 采样下需固定 temperature=0/seed 并排除量化、浮点、ollama 版本等非确定性来源，论文未论证该强假设。
- - Major: 36 次 extra trials 与 gemma 三次独立试验属失败后选择性重试，采样非随机，引入选择偏差。
### Minor（2）
- - Minor: L1b judge 单标注者引入标注偏差；P5 用"模拟第二标注者 α=0.894"代替真实双人标注，其信度假设未经实证。
- - Minor: L047 answer-fitting audit 的判定标准与 ground truth 未校准，3/3 拦截结论可能有测量偏差。

## 统计（stat）— ok
### Critical（2）
- - **Critical**: L2 的 exact McNemar 检验 $n_d=0$（零不一致对），检验统计量退化为无意义常量；$p=1.0000$ 与 95% CI $[0,0]$ 同为退化值，既不能证明"无差异"也不能证明"有差异"，摘要将其作为 L2 两臂等价的推断依据是误导性的。
- - **Critical**: curated L1a 的 $p=0.0026$ 仅在"fail-as-worst encoding"一种编码方案下显著，属于在多种编码/敏感性选择中挑选显著结果（specification search / p-hacking），未对编码方案数做多重比较校正，该 p 值不可信。
### Major（7）
- - **Major**: 整套基准运行了大量检验（L2 McNemar Ã3 模型、L1a Friedman Ã2 编码、P5 探索性 $p=0.0026$、L1b judge 校准 FNR/FPR 门控等），摘要未报告任何 family-wise（Bonferroni）或 FDR（Benjamini-Hochberg）校正，总体 Type I 错误率失控。
- - **Major**: 在 Friedman omnibus 非显著（$p=0.3679$）的情况下仍执行 Nemenyi 事后检验并报告 CD$=0.8284$；根据 Nemenyi 事后检验的逻辑前提，omnibus 非显著时不应进行/解释成对比较，CD 的报告暗示了无效的事后推断。
- - **Major**: 16 paired tasks 的 Friedman 中包含 10 个 L1b 任务，而 L1b 对所有模型均为 0/10（全部平绑）；这些非判别性任务不提供任何排名信息，却虚增 $n$，可能扭曲 $\chi^2$ 统计量与自由度，应剔除后重跑或明确报告剥离后结果。
- - **Major**: L2 各模型均值（0.1418 / 0.1918 / 0.2750）及 L1a 逐任务分数（0.6252、1.5422、0.2000Ã3 等）均以点估计形式报告，未附 SD、SE、CI 或任何分散度量；无法评估估计精度。
- - **Major**: L2 $N=4$，$d_{\min}=2.1279$，McNemar power $0.0000$；尽管披鲲了功效限制，但将退化 95% CI $[0,0]$ 与"无统计学可检测差异"并列呈现，暗示了等价性判断（absence of evidence â  evidence of absence）；应明确声明无法做等价/非劣性推断。
- - **Major**: curated L1a Friedman $n=6, k=4$，使用渐近 $\chi^2$ 近似；$n=6$ 时渐近近似不可靠，应使用 exact permutation 或 $F$ 修正（Iman-Davenport）；$p=0.0026$ 在渐近近似下可能被夸大。
- - **Major**: LLM-as-judge 校准仅用 21 gold items（11+10）且 FNR=FPR=0（Wilson 0.28），零错分类在如此小样本上显著过拟合；更严重的是"zero judge calls (all SKIP)"意味着校准从未在实际评分中被执行，整个 judge 保证是未经验证的方法论合约而非实证证据。
### Minor（3）
- - **Minor**: "simulated second annotator $\alpha=0.894$"——模拟的标注者间一致性不是真实 reliability 证据，不应与真实α等同呈现。
- - **Minor**: ITT mean 0.355 与报告分量算术不一致：$0.2\times3 + 0.533\times2 + 0\times1 = 1.666$，无论除以 6（=0.278）还是 5（=0.333）均不等于 0.355，存在计算错误或分量描述缺失。
- - **Minor**: L1a 各任务指标尺度异构（0.0105 至 1.5422）却被二分化为 pass/fail（6/6 含 0.0105 的任务），阈值任意且信息丢失严重；应报告连续分数及各任务单独统计量。

## 实验（experiment）— ok
### Critical（4）
- - Critical: L2 主对比 A vs F 仅 N=4，McNemar 功率显式为 0.0000，n_d=0<6，CI 退化为 [0,0]，这不是"无差异"而是"无力检验"，将结论框定为"no statistically detectable difference"构成性误导。
- - Critical: seed 管理完全缺失——摘要明确写"bootstrap at step/seed level as future work"，主实验未报告任何随机种子、未做种子级稳定性验证，所有数值结果可能纯为种子噪声。
- - Critical: LLM-as-judge 在主轮次中零次调用（all SKIP），校准（21 gold，single annotator）永未在实际评分场景中验证，所谓"方法学保证"是空桥。
- - Critical: ollama 模型的量化精度（Q4/Q8/FP16）未报告，7b/14b/9b 在不同精度下性能可差数倍，直接影响基准公平性与可复现性。
### Major（9）
- - Major: 主 suite 仅含 3 个小型本地模型（7b/14b/9b），唯一 frontier（muse-spark-1.2-contributor）被归入"P5 exploratory"分歧，核心设计无大模型参照，泛化能力严重不足。
- - Major: L1b 全模型 0/10，地板效应导致该子基准对模型间比较零判别力，正控仅 1/4 单任务，无法证明 pipeline 可解性的普适性。
- - Major: 超参数（temperature、top-p、max tokens、retry 策略）完全未报告，completion-guided harness（arm F）的内部参数也不明。
- - Major: 试验计数不一致——L2 N=4（补充 N=8），gemma L1a "三次独立试验"，L1a 共 18 行，L1b 30 行，各层的试验次数与重复协议不统一，无法跨层比较。
- - Major: "36 extra trials"相对"532 initial"未说明触发条件与选入规则，存在结果驱动补跑（result-driven补给ï¼çæ¨±æé£é©ã
- - Major: arm F（completion-guided harness）无任何组件消融，仅 A vs F 二元对比，无法归因增益来源。
- - Major: "curated L1a (6 tasks, k=4)"的策屈过程不透明，且与 Friedman 用的"16 paired tasks"是不同任务集，统计显著性仅在 curate 后子集上出现，选择偏差嫌疑极强。
- - Major: 第二标注者为"simulated"（α=0.894）而非真实人工标注，inter-annotator agreement 为模拟值，校准的外部效度存疑。
- - Major: 不同参数量模型（7b vs 14b）直接横同比较无 scale 归一化，L2 中 14b > 7b 的差异可仅映射模型大小而非 harness 效果。
### Minor（3）
- - Minor: 单一硬件（RTX3090）、单一云商（AutoDL），无跨硬件复现验证。
- - Minor: fail-as-worst 仅测了一种替代编码（sensitivity），消融不完整，缺 fail-as-missing / fail-as-excluded 对比。
- - Minor: P5 positive control 仅在 Chemistry_000 单任务上 1/4，无法支持 pipeline 可解性的广义声明。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 核心 GAP（"evaluation remains fragmented"）的填补仅是把三个已有 benchmark（AIRS-Bench、ResearchClawBench、GAIA2）裁缝进一个 run.json 契约；统一本身不产生新的比较洞见，属工程集成而非研究贡献。
- - Critical: 引言部分对相关工作几乎零对接，唯一引用是 \citep{goodfellow2016deep}（深度学习教科书），未对比 AgentBench、HELM、LM-Eval-Harness、ScienceAgentBench、MLE-bench、SciCode 等多能力/科学 agent 基准，"GAP 是否真实"无法验证。
### Major（4）
- - Major: 增量贡献被夸大——实验结果几乎全部为零结果（L2 p=1.0000、L1b 0/10、Friedman n.s.），唯一正向结果（muse-spark 6/6, p=0.0026）自贴"exploratory"且依赖 fail-as-worst 编码；suite 未产出超越"小模型失败"的可行动发现。
- - Major: "unified reproducible contract" 与 SHA-256 manifest 被作为 novel 贡献呈现，但可复现工件/哈希清单在 HELM、BIG-bench 等中已是标配，未说明相对已有 reproducible benchmark 基础设施的新增点。
- - Major: "same agent system across three layers" 的统一性被夸大——三层使用不同任务格式与评分（代码执行/LLM-judge/目标完成），唯一共享的是 JSON 契约，"unified"是松散的语义而非方法论上的统一。
- - Major: L1b 的 calibrated LLM-as-judge 自称通过 FNR/FPR 门控，但"the round made zero judge calls (all SKIP)"，即校准的 judge 从未实际运行，这一"贡献"是未经演示的 warrant，被当作已成果呈现。
### Minor（2）
- - Minor: "oracle-free goal completion"对 GAIA2 的定义未与 GAIA 自身目标级评分区分，"oracle-free"的新颖性未被论证。
- - Minor: "denominator discipline / fail-as-zero"作为贡献点提出，但此为 benchmark 常见做法，未与现有 fail-handling 约定对比。

## 可复现（repro）— ok
### Critical（2）
- - **Critical**: 未声明并固定任何 RNG seed；摘要明确把 "seed-level" 控制列为 "future work"，却同时声称 "byte-for-byte reproducibility" ââ 二者互斥，随机 LLM 采样无法字节级复现。
- - **Critical**: AIRS-Bench / ResearchClawBench / GAIA2 三套派生/第三方数据集均未披露许可证（license）；无法核实合法再分发与重跑权利，法律层面即不可复现。
### Major（9）
- - **Major**: "46-entry SHA-256 manifest" 似乎只是对已存储 artifact 做哈希（re-hash）而非新鲜环境重跑后对账；"18/18 recomputation checks" 未说明是否为 fresh rerun，属于 "存什么就能验什么" 的循环证据，不构成真复现。
- - **Major**: 三个互不对齐的计数 ââ "46-entry manifest"、"165 entries with P5"、"18/18 recomputation checks" ââ 与报告的 72 行（24+18+30）之间无映射关系，哈希对账的覆盖范围不透明，无法审核是否漏验。
- - **Major**: 无一键复现 artifact：未给出仓库 URL、容器镜像、或 `run.json` 的实际内容；"fully recomputable harness" 在可见文本中是未经证明的口头承诺。
- - **Major**: 模型配置快照残缺 ââ ollama tag "qwen2.5:7b/14b、gemma2:9b" 未注明量化（Q4_K_M / Q8 / FP16）、temperature、top-p、num_ctx、权重 digest；相同 tag 在不同 ollama 版本可解析为不同权重，模型身份不可锁定。
- - **Major**: L2 两个 arm（A vs F）在三个模型上均产出完全相同的 mean completion（0.1418 / 0.1918 / 0.2750）；在未固定 seed 的随机采样下几乎不可能，暗示 arm 间共享/复用了输出或 cache，arm 独立性与复现性均存疑。
- - **Major**: "simulated second annotator Î±=0.894" 是合成值，不是实测互标复现；结合 "single annotator" 与 "zero judge calls (all SKIP)"，整个 LLM-as-judge 管线在报告的 round 中根本未运行，校准仅为 "methodological warrant" 而非已复现事实。
- - **Major**: gemma L1a 的 "three independent trials" 未附 seed 或 trial间差异清单；"独立" 是断言而非证据，trial 可能为相关重跑。
- - **Major**: ARS v3.11、L047 audit、统计 "canonical script" 均未给出版本化 URL 或 commit hash；协议/脚本 drift（v3.11 â 复现者 checkout）无控，复现者无法锁定同一定义。
- - **Major**: 事后任务筛选（"curated L1a, 6 tasks, k=4"）与编码敏感性（"fail-as-worst"）使得标题 p=0.0026 依赖一个非默认、未在 config snapshot 中 pin 住的选择，复现者用默认编码会得到不同结论。
### Minor（3）
- - **Minor**: 环境快照除 "ollama 0.32.13 / RTX3090" 外为空；未记录 CUDA、Python、OS、ollama server config（OLLAMA_NUM_PARALLEL、上下文长度、GPU 分配）。
- - **Minor**: "P5 frontier muse-spark-1.2-contributor" 未提供访问/发布/权重 digest 信息；专有前沿模型结果对第三方不可独立复现。
- - **Minor**: 预算单位未定义（"<1000 budget"）；budget-controlled 停止规则的复现需要在 config 中 pin 住单位与阈值。

## 写作（writing）— ok
### Critical（2）
- - Critical: P5 gold 计数矛盾："39 gold, 30 real+9 synthetic+1 attack"中 30+9+1=40 â  39，无论攻击条目是否计入 gold，写法都与总数不吻合。
- - Critical: 摘要自相矛盾——LLM-as-judge 声称"passed at FNR=0.0000, FPR=0.0000"，却同句承认"the round made zero judge calls (all SKIP)"；零调用无泖产生预测，FNR/FPR 无分母，"passed"是逻辑空洞。
### Major（7）
- - Major: 核心术语未定义即首次使用：P5、L047、ARS v3.11、arms "A" 与 "F"（跳过 BâE）在摘要和引言中均无定义，读者无法理解。
- - Major: 同一基准在摘要与正文命名不一致：摘要称"AIRS-Bench"，引言称"AIRS-Bench rad"，"rad"子集未说明。
- - Major: intention-to-treat mean $0.355$ 无法从所给分量推出：Sentiment $0.2000\times3$、TextSimilarity $0.5330\times2$ 含 1 次失败记 0，无论怎样加权平均（$(0.6{+}1.066)/5{=}0.333$、$(0.2{+}0.533{+}0)/3{=}0.244$ 等）均不等于 0.355，数字不可复现。
- - Major: "McNemar power $0.0000$ at $n_d=4$"——统计功效为严格零不合理；即便效应极小，power 应为接近零的正值，此处报 0.0000 疑为截断或误用。
- - Major: 摘要结构失衡——单段堆叠 30+ 个数值、5层统计检验、3 种能力层，缺乏概括性论断，读如结果表而非摘要。
- - Major: 缩写表定义"GAIA (General AI Assistant)"，正文却使用"GAIA2 p3dev"，未说明 GAIA2 与 GAIA 的区别。
- - Major: 引言统计协议含"Wilcoxon+CLES"，摘覃媒介绍 McMemar 与 Friedman 却完全省略 Wilcoxon，摘覂与正文方法描述不对齐。
### Minor（4）
- - Minor: "95% CI [0,0] degenerate"中"degenerate"词汇偏随意，应使用"point mass"或"zero-width"等正式表述。
- - Minor: "$0.2000\times3$"符号非标准，易误读为乘积 0.6 而非"3 次试验均得 0.2"。
- - Minor: "46-entry SHA-256 manifest (165 entries with P5)"从 46 跳至 165 无任何过渡解释，跨度异常且无表格支撑。
- - Minor: "intention-to-treat"为临床试验术语，在基准评测语境下未做概念映射，术语借用欠妥。

## 伦理（ethics）— ok
### Critical（2）
- - Critical: æª«ª»é¢çå©çºå®ï¼æ¨¡åmuse-spark-1.2-contributor åç§°å«âcontributorâï¼æç¤ºä½è æ¯è¯¥åç«æ¨¡åçè´¡ç®èï¼èå®å´æ¯æ´ä¸ªå®éªä¸å¯ä¸âéè¿âçç³»ç»ï¼6/6ï¼p=0.0026ï¼ï¼æ¢æªå£°æ COI ä¹æªå£°ææ¨¡åè®¿é®/ææï¼æ¶åä¸¥éå©çå²çªä¸éå¬é£é©ã
- - Critical: åå¿åé£é©ï¼è¿åä¸º TMLR double-blindï¼G3ï¼ï¼ä½ muse-spark-1.2-contributor è¿ä¸å«âè´¡ç®èâçç¹æåç«æ¨¡åãç¹å®æ¶æ¯æ ï¼AutoDL/ollama 0.32.13ãqwen2.5:7b çï¼å¯è½åç¬¦ååºè´¡ç®èå¢éï¼æ§æ double-blind å¿åæ§ï¼åºä¸»å¨å¿ååæ¨¡å«ç§°ï¼å¦ MUSE-CONTRIB-P5ï¼ã
### Major（4）
- - Major: æ°æ®è®¸å¯ç¼ºå¤±ï¼å¤ç¨ AIRS-BenchãResearchClawBenchãGAIA2 ä¸å¥æ°æ®éååä»»å¡ï¼ä½æªå£°æåä»½æ°æ®éçè®¸å¯è¯ãå¯åé®åè®¸å¯å¼ç¨æ¡æ¬¾ï¼åæ¶å£°ç§°ârelease the suiteâ+46/165 æ¡ç® SHA-256 manifestï¼å´æªè¯´æå¯åé¨åçè®¸å¯å¼æ§ä¸åçº§ææã
- - Major: è¯¯ç¨/å®å¨é£é©ï¼å ¬å¼åå¸ç harness ä¼çæå¹¶æ¬å°æ§è¡ä»»æä»£ç ï¼L1a/L1bï¼å¹¶è¿è¡èªä¸»ç¯å¢æ§è¡ agentï¼L2 GAIA2 p3dev oracle-freeï¼ï¼ä½æªææè½¯çæ§ãæ²ççæ§è¡ãææ³è¾åºè¿æ»¤ãæ»¥ç¨é²æ¤ä¸æ¬¡æ§å£°æã
- - Major: åå¾·é£é©ï¼L047 answer-fitting audit ä¸ä»»å¡åæ¥åå¸ï¼ä¼è®©æ»å»èæ¬å¨è®ç»æ¶éå¯¹æ§å°é¿å¼è¯¥å®¡è®¡ï¼ä»èéåanswer-fitting/æ³é²ï¼å±äºæªæ§è®¨è®ºç dual-useã
- - Major: éç§/äººä½å£°æç¼ºå¤±ï¼GAIA2 äº¤äºå¼ç½ç»ä»»å¡å¯è½æ¥è§¦å®æ¶ web å§å®¹/PIIï¼LLM-as-judge æ¡é¶ä¸ºåäººæ æ³¨ï¼21 goldï¼ï¼åä½æªæ IRBãç¥æãPII å¤çå£°æï¼ä¹æªè¯´æâ9 synthetic + 1 attackâ gold æ¡ç®çæ¥æºä¸åæ³å¤å®ã
### Minor（1）
- - Minor: judge æ¨¡å llama3.1:8b çè®¸å¯æªå£°æï¼åsimulated second annotator Î±=0.894 ç»è¿çå®äººæ æ³¨ä½åä»¥æ ¡åï¼æ¢æªå¤å®åæ³§ä¹æªè¯´æåæ³æ§æä¾ã

## 汇总

- **Critical: 19 | Major: 45 | Minor: 18**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）