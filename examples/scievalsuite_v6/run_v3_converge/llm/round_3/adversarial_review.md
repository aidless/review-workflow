# 对抗审查报告

- 时间: 2026-08-26T04:50:58.759930+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（4）
- - Critical: L2 "无可检测差异" 的因果推断无效。N=4、McNemar 功效 0.0000、n_d=0、95% CI 退化为 [0,0]——这是"无信息"而非"无差异"。将"未能否定零假设"表述为"两臂表现相同（均值保持不变）"，是把证据缺失当作效应缺失，违反等效性推断的基本前提；即便补充 N=8 仍 p=1.0000，只能说明检验彻底失效，而非治疗无效。
- - Critical: 可选停止 / 结果选择偏倚。gemma L1a "1/6 → 2/6 after three independent trials"，且整体 568 调用 = 532 初始 + 36 次额外试验。在看到初始失败后追加试验直至改善，是典型的 optional stopping；为何仅对 gemma 追加三次、其他模型不追加，未给出预注册规则，选择规则与结果相关，破坏内部效度。
- - Critical: LLM-as-judge 校准与实验脱节。实际评测轮次"零次 judge 调用（全部 SKIP）"，校准却建立在 21 条 gold（且为单一标注者）之上；"simulated second annotator α=0.894" 为模拟而非真实。校准对象与被评对象非同一分布，校准 warrant 无法迁移到实验结论，外部/生态效度不成立。
- - Critical: 多重检验与编码挑选。Friedman 全集 16 任务非显著（p=0.3679），随后"curated L1a（6 任务, k=4, exploratory）"在 "fail-as-worst encoding" 下才得 p=0.0026。子集挑选 + 编码挑选 + 事后贴 "exploratory" 标签，研究自由度极高，该显著结果极可能是假阳性；未做多重比较校正。
### Major（6）
- - Major: N=4 下仍将统计比较作为"发现"呈现。即便披露 d_min=2.1279，功效披露不等于推断有效——在功效为零的设计上同时报告点估计、p 值与 CI，本身具有误导性，应作为"无法估计"而非"估计为零"。
- - Major: 混杂变量未控制。三模型（7b/14b/9b）跨家族跨参数量，模型族×规模×训练数据完全混杂；跨模型 Friedman 的任何差异（或无差异）都无法归因到任一可控因素，因果推断不可识别。
- - Major: 治疗捆绑。L2 的 F 臂="completion-guided harness"，相较于 A=ReAct 同时改变了 harness 结构与 completion-guidance，未隔离单一变量；任何差异或无差异都无法归因于 completion-guidance 本身。
- - Major: L1b 全模型 0/10 的地板效应威胁建构效度。全零既可能是任务不可解，也可能是度量失灵；"L047 audit intercepting answer-fitting in 3/3" 与 "P5 positive control 1/4 demonstrates solvability" 无法证明该层对目标能力具有区分度。
- - Major: 可复现性被混同为效度。SHA-256 / 18 次重算通过仅保证"同输入同输出"的字节级确定性，并不证明基准测的是"科学能力"而非"基础设施失败"；denominator discipline 把执行错误、超时、错误答案统一记 0，进一步混淆失败模式，削弱因果归因。
- - Major: McNemar 配对独立性假设可疑。智能体在同一任务集上、同模型采样下运行；若温度非零，单次运行的随机变异未受控，配对二值结果未必独立；n=4 下 χ² 近似亦不成立。
### Minor（2）
- - Minor: "intention-to-treat" 借用临床术语但类比失当——将"执行失败试验记 0"与"真实零分"等同处理，把基础设施失败与能力零分混为一谈，影响得分解释。
- - Minor: 顺序/疲劳效应未讨论；A、F 两臂若固定先 A 后 F 运行，配对设计无法消除顺序混杂。

## 统计（stat）— ok
### Critical（2）
- - Critical: McNemar 检验在 `n_d=0, N=4, power=0.0000` 下 `p=1.0000` 是数学退化值而非统计证据，将其表述为"no statistically detectable difference"属于将"证据不足"当作"无差异的证据"；`d_min=2.1279` 表明该设计仅能检测 Cohen's d > 2 的极大效应，在功效为零时接受原假设无统计意义。
- - Critical: 跨三层 × 三模型 × 多任务报告了多个 p 值（McNemar `p=1.0`、Friedman `p=0.3679`、exploratory `p=0.0026`）但全文无任何多重比较校正（Bonferroni / Holm / FDR），家族错误率严重膨胀。
### Major（3）
- - Major: 从 16 任务 Friedman 不显著（`p=0.3679`）切换到 curated 6 任务、k=4 子集得到 `p=0.0026`，且该 p 值仅在 fail-as-worst 编码下成立，构成选择性分析 / p-hacking；虽标注 exploratory 仍报告具体 p 值会误导读者。
- - Major: 多处点估计缺失不确定性度量：L2 均值（0.1418 / 0.1918 / 0.2750）无标准差或标准误；ITT mean 0.355 无方差；`95% CI [0,0] degenerate` 完全无信息量但仍作为结论呈现。
- - Major: LLM-as-judge 校准声称 FNR=0.0000 / FPR=0.0000 通过，但本轮零次 judge calls（all SKIP），校准无实际数据支撑；"simulated second annotator `α=0.894`"为模拟值而非实测标注一致性，"single annotator" 也无法评估 IRR。
### Minor（2）
- - Minor: `0.2000×3`、`0.5330×2` 等多次独立试验结果完全相同（方差为零），未讨论其原因（确定性解码？固定种子？还是数据错误？），影响可重复性的统计解读。
- - Minor: `CD=0.8284` 未说明所依据的 alpha 水平与 q 值；Wilson 区间（0.28 / 0.143）的含义、覆盖概率及与 FPR=0 零事件的交互未充分阐释。

## 实验（experiment）— ok
### Critical（4）
- - Critical: L2 McNemar 在 N=4、n一=0（零不一致对）时统计功效为 0.0000，CI 退化为 [0,0]，声称"无统计检出差异"是空洞的非结果被当作发现呈现，等价于"未测试"而非"无效应"。
- - Critical: gemma L1a 从 1/6 â 2/6 经"三次独立试验"，直接证明存在运行间方差；但 SHA-256 清单声称"byte-for-byte 可复现"，两者矛盾——说明 seed/temperature 未固定或复现声明属性存疑。
- - Critical: 532 初始调用之外追加 36 次"extra trials"将 gemma 从 1/6 推至 2/6，无预注册、无多重比较校正，属于 garden-of-forking-paths 式数据挖妄。
- - Critical: curated L1a 的 p=0.0026 仅在"fail-as-worst encoding"特定编码下成立，且涉及任务筛选（curated 6/16），显著性依赖事后规格选择——典型 specification-curve fishing。
### Major（8）
- - Major: Arm F（"completion-guided harness"）作为整体黑盒与 A 对比，未对其内部组件（completion 策略、prompt 模板、工具调用顺序等）做任何消融，无法归因效应或零结果的来源。
- - Major: LLM-as-judge 在 L1b 实际运行中"made zero judge calls (all SKIP)"，校准从未在真实输出上执行；L1b 全 0/10 可能是 SKIP/harness 属性而非模型能力底线，控制组失效。
- - Major: 跨模型 Friedman 将 6 个 L1a（代码生成）+ 10 个 L1b（工作流）任务池化，指标/尺度不兼容；且 10 个 L1b 任务全为 0 分平局，不贡献排名信号，虚增 N=16。
- - Major: Agent 与 judge 的超参数（temperature、top_p、max_tokens、system prompt、few-shot 示例数）均未披鲲，基准公平性与复现性无法验证。
- - Major: 仅 3 个小型本地模型（7â14B）+ 1 个前沿模型；qwen 7b/14b 同族不同尺寸与 gemma 9b 异族异尺寸混合，家族效应与规模效应完全混淆，泛化声明无支撑。
- - Major: "simulated second annotator Î±=0.894"是模拟而非真实标注一致性；21 个 gold（11/10）、单真实标注者的校准集过小，FNR=0/FPR=0 在此 n 下极为脆弱。
- - Major: P5"positive control"仅 1/4 于单个任务（Chemistry_000），样本量不足以证明管线可解性；同时缺少 negative control（已知不可解任务）验证判别效度。
- - Major: L2 goal-completion 指标无 oracle 或人类基准对照，无法区分"模型能力不足"与"指标/harness 噪声"。
### Minor（3）
- - Minor: ollama 模型量化等级（Q4/Q8/FP16）未报告，跨尺寸模型可能使用不同精度，影响基准公平。
- - Minor: "46-entry manifest（165 entries with P5）"范围不一致，byte-level 可复现到底覆盖哪些制品不清楚。
- - Minor: N=8 supplement 仍 p=1.0000，但未报告 supplement 的 n一（可能仍为 0），补充实验的信息增量不明。

## 新颖性（novelty）— ok
### Critical（3）
- - Critical: 核心"新颖性"仅为将三个**已有**基准（AIRS-Bench / ResearchClawBench / GAIA2 p3dev）缝合到一个 `run.json` 契约下；统一契约 + 统计协议（McNemar/Wilcoxon/Friedman 均为现成检验）+ SHA-256 manifest 属工程集成，未见任何新任务、新指标或新方法论贡献，增量贡献被框架为"unified benchmark"时明显夸大。
- - Critical: 所谓 GAP"evaluation remains fragmented"是通用且被反复讨论的老生常谈；引言中对该 gap 的唯一文献支撑是 `\citep{goodfellow2016deep}`（2016 年深度学习教科书），无法确立"科学 agent 评测碎片化"这一具体缺口，且未展示与当前相关工作的差异表，GAP 构造疑似 strawman。
- - Critical: 主体实验结果几乎全部为空（L2 McNemar p=1.0000 / n_d=0、Friedman p=0.3679、L1b 三模型全 0/10、L1a 多为 0/6）；N=4、McNemar power=0.0000，基准根本无法检出差异——在此前提下"可区分 genuine scientific reasoning from execution failure"的贡献主张缺乏实证支撑，属空洞声明。
### Major（3）
- - Major: 唯一显著结果（P5 muse-spark-1.2-contributor 6/6, p=0.0026）被明确标为"exploratory"且仅在 fail-as-worst encoding 下成立；论文将此用作支撑"benchmark 可解性 / frontier 可达性"的卖点，属于把探索性、编码敏感的副结果当主贡献宣传。
- - Major: LLM-as-judge 校准（FNR/FPR gates、Wilson、α=0.894）被列为核心方法贡献，但"the round made zero judge calls (all SKIP)"——即实陘中根本未调用 judge，校准纯粹是"methodological warrant"；将未经实战验证的组件计入贡献清单构成夸大。
- - Major: 文中反复强调的"denominator discipline（failures score zero, remain in denominator）"与"three-layer statistical protocol"均为评测惯例与标准检验组合，既未超越现有文献，也未给出与已有评测框架（如 HELM、BIG-bench、AgentBench 等）的差异化对比，增量边界模糊。
### Minor（1）
- - Minor: "46-entry SHA-256 manifest"的核心可复现性规模有限，"165 entries with P5"的扩展又依赖探索性 P5 层，可复现贡献的"量级"存在注水嫌疑。

## 可复现（repro）— ok
### Critical（3）
- - Critical: 全文明确"bootstrap at step/seed level as future work"——seed 未受控，却给出 4 位小数精度结果（如 0.6252、0.1918、0.6552），这些精确数值在无 seed 固定的情况下不可字节级复现，与"byte-for-byte reproducibility"自相矛盾。
- - Critical: LLM-as-judge 校准声称通过（FNR=0.0000, FPR=0.0000），但同句承认"the round made zero judge calls (all SKIP)"——校准从未在主运行中实际执行，L1b 的 0/10 评分证据链断裂，"calibration is a methodological warrant"只是承诺而非证据。
- - Critical: SHA-256 清单条目数前后不一致——"46-entry manifest"与"165 entries with P5"未说明二者关系（P5 是何阶段？为何 46→165 跳跃？），哈希对账范围与口径无法核对。
### Major（9）
- - Major: 模型标识仅用 ollama tag（qwen2.5:7b、qwen2.5:14b、gemma2:9b），未提供权重 commit hash 或 HuggingFace 指纹；ollama tag 可随 registry 更新漂移，配置快照不完整。
- - Major: "muse-spark-1.2-contributor"（P5 frontier 模型）无来源、无版本、无访问方式，第三方完全无法复现该 6/6 结果。
- - Major: 三个基准（AIRS-Bench、ResearchClawBench、GAIA2）均未声明数据许可（License），数据再分发与复现的合规性存疑。
- - Major: "simulated second annotator α=0.894"——模拟方法与随机种子未披露，该 κ 值不可复现，且用"模拟"冒充真实第二标注者构成证据链注水。
- - Major: gemma 在 L1a 上"0.2000×3 on Sentiment, 0.5330×2 on TextSimilarity"——不同任务试验次数不一致（×3 vs ×2），且"1/6→2/6 after three independent trials"显示结果非确定性，与"fully recomputable"主张冲突。
- - Major: 声称"release the suite as a budget-controlled, fully recomputable harness"，但摘要中无一键复现入口（无 repo URL、无 setup 脚本、无容器镜像/lockfile 引用），复现契约不可触达。
- - Major: "18/18 independent recomputation checks passing"未说明复算条件（同环境？同 seed？重跑还是重放？），"independent"一词无操作化定义，证据链空洞。
- - Major: 虽提及"one run.json contract"，但摘要未披露关键配置快照字段（temperature、top-p、max tokens、retry 策略、超时），run.json 仅作为口号出现而非可审计 artifact。
- - Major: L2 统计 N=4、n_d=0、McNemar p=1.0000、power=0.0000——在零检测力下声明"no statistically detectable difference"是空真而非复现性证据，结论不可证伪。
### Minor（3）
- - Minor: "P5"在摘要中多处出现（P5 frontier / P5: 39 gold / 165 entries with P5）但从未定义，读者无法定位其复现范围。
- - Minor: "568 calls (532 initial + 36 extra trials)"中 36 次额外试验的触发原因、是否计入哈希清单、是否影响最终数值均未说明，复现账目不平。
- - Minor: 摘要未给出 ollama 之外的依赖锁版本（Python、评估脚本、judge 模型 llama3.1:8b 的 tag 同样可漂移），配置快照仅覆盖单一组件。

## 写作（writing）— ok
### Critical（1）
- - Critical: 摘要中 "39 gold, 30 real+9 synthetic+1 attack" â 30+9+1=40â 39，gold 总数與分项明細自相矛盾，无论 "1 attack" 是否計入 gold，文本表面即存在硬性算術矛盾。
### Major（5）
- - Major: 摘要约 400 词、单段，将所有统计量、p 值、CI、Wilson、α 等堆叠于一段，夹杂大量未定义缩写（P5、L047、ARS v3.11、arms A/F），结构上是结果倾倒而非摘要，严重影响可读性。
- - Major: "intention-to-treat mean 0.355 including the failed trial as 0" 无法从已给分量重构 â 已知 gemma 仅 Sentiment(0.2Ã3)、TextSimilarity(0.533Ã2) 非零，无论按 6 任务(0.733/6=0.122)、按试次(1.666/5=0.333)或均值(0.367)均无法得出 0.355，数字一致性存疑。
- - Major: 引言称 L1b 由 "heterogeneous LLM judge" 评分，但摘要仅命名单一模型 "llama3.1:8b"；"heterogeneous"（异构多样）与单模型单标注者直接矛盾，术语与正文矛盾。
- - Major: 摘要耗约 80 词铺陈 judge 校准（FNR/FPR/Wilson/ARS v3.11/Î±=0.894），随后披露 "zero judge calls (all SKIP)" â 头重脚轻的结构性矛盾，校准细节实际未被执行，应前置披露或大幉削减。
- - Major: 摘要内出现内部交叉引用 "(see sensitivity)" â 摘要应自涵，不应指向正文章节。
### Minor（5）
- - Minor: L2 实验手臂标注为 "A" 与 "F"（跳过 BâE），缺口原因未交代，术语命名不自明。
- - Minor: "$<1000$ budget" 未标明单位（calls / tokens / USD），且 568<1000 为平凡约束，缺乏信息量。
- - Minor: "0.2000Ã3"、"0.5330Ã2" 符号非标准，无法区分 "3 次试验各得 0.2" 还是 "0.2Ã3=0.6"，表述歧义。
- - Minor: "AIRS-Bench rad" 中 "rad" 未定义；N=4（McNemar）、N=8 supplement 与 24 L2 rows 之间的样本映射关系未在可见文本中澄清。
- - Minor: 引言结尾以 "â¦"（截断）结束，句子未完成，结构不完整（虽为摘录截断，但影响审阅连贯性）。

## 伦理（ethics）— ok
### Critical（3）
- - Critical: 三大基准（AIRS-Bench、ResearchClawBench "L047"、GAIA2 p3dev）均未声明数据来源与许可证（如 Apache-2.0/CC-BY/研究仅用条款），GAIA2 疑为 GAIA 派生版本，派生许可与再分发合规性未交代，存在侵权与再发布风险。
- - Critical: 全篇无任何伦理声明/安全审查章节；L1a 要求"代码生成+本地执行"、L2 要求"交互式环境执行+工具调用"，直接触及生成可执行代码与工具滥用的误用风险（如生成恶意代码、未沙箱化的工具调用），却未描述沙箱隔离、危险代码过滤或负责任使用约束。
- - Critical: 双盲完整性存疑——摘要与注释暴露高度可识别的组合特征：特定云平台（AutoDL RTX3090）、精确框架版本（ollama 0.32.13）、以及对"P5 frontier muse-spark-1.2-contributor"前沿模型的内部访问权，足以缩小甚至定位作者群体，与 TMLR 双盲要求冲突。
### Major（4）
- - Major: 存在未披露的潜在利益冲突——作者能访问"muse-spark-1.2-contributor"前沿模型并在文中以 P5 正面对照形式呈现其成绩，若作者与该模型提供方存在隶属或合作关系，正向结果可能构成隐性利益冲突，全文未见 COI 声明。
- - Major: 人工标注伦理缺位——"21 gold（11 正/10 负，单标注员）"涉及人工判断劳动，未交代标注者知情同意、报酬、劳动条件或 IRB/伦理审查；"模拟第二标注员 α=0.894"更使标注真实性可疑，既涉及合规也涉及诚实性。
- - Major: 合成数据（"9 synthetic"）与"1 attack"条目的生成方法、来源模型、潜在有害内容与审核流程均未披露，合成/攻击样本若混入评测集可能引入偏见或不当内容，provenance 不明。
- - Major: 未对任一基准数据集进行隐私/PII 审查——ResearchClawBench 含"报告+图表"任务、GAIA2 含真实交互场景，是否含个人可识别信息或敏感科研数据未评估，违反数据最小化与隐私合规原则。
### Minor（2）
- - Minor: 注释中遗留 `corresponding@example.com` 占位邮箱及"camera-ready"字样，虽为占位但在双盲稿件中应彻底清除以避免格式泄露。
- - Minor: 关键词与缩写表中提及 GAIA 等第三方商标/项目名，未声明商标归属与使用授权，存在轻微合规瑕疵。

## 汇总

- **Critical: 20 | Major: 38 | Minor: 18**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）