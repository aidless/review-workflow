# 对抗审查报告

- 时间: 2026-08-27T05:25:31.824875+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（3）
- - Critical: L2 两侧对比仅 N=4、n_d=0<6、McNemar 功效明确为 0.0000，却以"no statistically detectable difference"措辞暗示两臂等价——这是典型的"未检出差异â 不存在差异"，在零功效下既无法支持等价结论也无法支持非劣效结论，因果推断（臂别→完成度）的前提（可检测效应）不成立。
- - Critical: 16 任务 Friedman 非显著 (p=0.3679) 后，对 L1a 6 任务子集做"curated"再检验得 p=0.0026，属事后子集选择（post-hoc subset selection）；即便加 Holm 校正也未校正"先全量非显著再挑子集"这一选择过程，多重比较/确认偏倚未被控制，p 值不可作有效推断。
- - Critical: L1b 的 LLM-as-judge 校准仅 21 gold、单标注者、FNR=FPR=0.0000，而该轮实际零次判官调用（全 SKIP）——校准未在真实评分中经受检验，且完美零误差在 n=21 上几乎必然是过拟合或判别阈值平庸化，将其作为"methodological warrant"等于以未生效的校准背书主结果，内部效度断裂。
### Major（6）
- - Major: L1b 全模型 0/10 的地板效应使该层完全失去区分模型能力的效度；"稳定失败分类"只是描述性产物，不能据此对模型间差异或流程可解性做任何统计推断。
- - Major: L2 的 A(ReAct) vs F(completion-guided harness) 两臂在脚手架实现上多处不同（提示、工具循环、完成信号注入等），"completion guidance"作为单一自变量未被隔离，存在严重混淆，即使有差异也无法归因到该因素。
- - Major: 前沿 Model-F(6/6) 与本地小模型的比较存在系统性混淆（API 服务、采样配置、上下文长度、可能的数据泄露），p=0.0026 不能支撑"前沿显著优于本地"的因果/能力推断；"exploratory"标签不消除混淆。
- - Major: gemma L1a 报"1/6→2/6 after three independent trials"同时给"ITT 均值 0.355（含失败试次记 0）"，既事后择优又混用两种估计框架；多次试次的选择与报告标准未在事前注册，损害可比性。
- - Major: 仅 3 个小规模本地模型(7b/9b/14b)支撑"unified benchmark"泛化主张，样本层与模型层都严重欠覆盖，外推到"scientific agents"总体的前提（代表性）不成立。
- - Major: "SHA-256 + 18/18 重算通过"证明的是可复现性而非效度；可复现地得到错误/有偏的测量仍不构成有效基准，不能以复现封条替代构念效度与区分效度论证。
### Minor（3）
- - Minor: "denominator discipline（失败记 0）"将崩溃、超时、契约违反、错误答案等异质失败模式塌缩为同一 0 值，可能掩盖模型间失败结构差异，损害对能力维度的细粒度推断。
- - Minor: answer-fitting 审计(3/3 命中)缺少该审计自身的灵敏度/特异度正对照（即对已知注入拟合的检出率），其作为防泄漏屏障的有效性只是假定而非已验证。
- - Minor: 本地端点采样确定性未明示（温度/seed/top-k），若非温度 0，所谓逐种子行与字节级复现依赖具体后端实现，可复现前提可能仅在特定栈下成立。

## 统计（stat）— ok
### Critical（3）
- - Critical: L2 的 exact McNemar 检验在 n_d=0（零不一致对）下是退化的/无信息的，p=1.0000 只是退化公式输出，却被表述为"未检测到差异"——这是把"无证据"偷换成"无差异"的经典 p 值误用；应声明该检验无统计信息量。
- - Critical: 样本量严重不足：L2 N=4，d_min=2.1279（Cohen d>2 属极端巨大效应），且自报 McNemar 功效=0.0000，意味着该实验本质上无法检验任何合理大小的效应，但摘要仍以"L2 结果"形式汇报均值差异作为发现。
- - Critical: gemma 的 intention-to-treat 均值 0.355 与所报离散得分无法对账：三个 6 任务试验（1/6、2/6、失败计 0）的 ITT 均值应为 (1+2+0)/18≈0.167，0.355×18=6.39 非整数，任何整数计分口径下都不可能得到 0.355，疑似计算错误。
### Major（7）
- - Major: 经典 p-hacking/子集选择：16 任务 Friedman 不显著(p=0.3679)后，另做"curated"6 任务子集得 p=0.0026；事后按结果挑选子集引入的选择偏倚 Holm 校正无法消除，该显著结果不可信。
- - Major: Holm 校正 p=0.0261/0.0026≈10 暗示进行了约 10 项检验，但摘要仅报告 2 项，多重比较校正不完整、不透明，存在大量未披露的沉默检验。
- - Major: 声称采用 Wilcoxon+CLES 协议，但摘要从未报告任何观测效应量（CLES 值缺失），只给了可检测下限 d_min，效应量报告不达标。
- - Major: 所有均值（goal completion 0.1418/0.1918/0.2750 等）均无 SD/SE/CI；在 N=4 下不确定度极大，点估计无方差报告无法判断差异是否可信。
- - Major: 判官校准 FNR=0、FPR=0 在 n=21/n=39 上无置信区间（按 Rule of 3 上界约 14%/8%），"完美"系小样本过拟合；且实际实验判官调用为零（全 SKIP），校准未在真实运行中验证。
- - Major: 21 gold 仅为单一标注者，未报告标注者间一致性/信度（IAA/Krippendorff α），判官 ground truth 的可靠性未建立。
- - Major: Model-F 6/6 的 p=0.0026 未说明所用检验与对比基线，n=6 下结果脆弱，虽贴"exploratory"标签仍被突出呈现。
### Minor（2）
- - Minor: L1b 全模型 0/10，数据全零、方差为零、无判别力，正对照仅为部分缓解，该层不具备统计可比较性。
- - Minor: bootstrap CI 明确推迟至"future work"，而这恰是小样本 N 下应优先采用的推断方法，当前推断框架与样本量不匹配。

## 实验（experiment）— ok
### Critical（3）
- - Critical: L2 双臂对照（A=ReAct vs F=completion-guided）样本量 N=4、discordant n_d=0、McNemar 功效=0.0000、d_min=2.1279，完全无统计功效；"未检测到差异"是空结论而非有效证据，无法支撑任何关于双臂等价或不等价的判断。
- - Critical: 任务规模过小且存在严重地板/天花板效应：L1a 仅 6 任务（7b 得 0/6）、L1b 10 任务全部 0/10、L2 仅 4 场景；在此分辨率下无法区分模型能力，泛化性主张无依据。
- - Critical: 事后挑选样本：整体 Friedman（16 任务）p=0.3679 不显著后，又对"curated L1a（6 任务，exploratory）"重做检验得 p=0.0026 并做 Holm 校正；Holm 校正无法弥补事后子集挑选带来的选择性偏倚，结论不可信。
### Major（7）
- - Major: 参考基线前后矛盾：引言称 deepseek-v4-flash 为"5/6 L1a"，摘要称"frontier Model-F 6/6"，二者是否同一模型未交代，基线公平性与可比性存疑。
- - Major: "deepseek-v4-flash"疑似不存在的模型名（DeepSeek 无 v4-flash 产品线），参考基线不可复现、不可核实。
- - Major: 受试模型与 F 臂"completion guidance"的关键超参数（temperature、top-p、max_tokens、采样/解码配置、引导强度等）在可见文本中全部缺失，无法判断各臂/各模型是否处于公平可比条件。
- - Major: seed/试验管理在各层不一致：L1a gemma 跑了"三次独立试验"，L2 仅 N=4 且只提"per-seed rows"却不给出 seed 数量，bootstrap 被推迟为 future work；缺乏统一的 seed 协议与可复现随机性披露。
- - Major: 将 L1a(6)+L1b(10)=16 任务合并进同一个 Friedman 检验不合理——L1b 全 0/10 零方差，这些任务对检验不贡献信息却参与秩比较，扭曲检验语义。
- - Major: LLM-as-judge 在实际运行中零调用（all SKIP），校准仅基于 gold 集，等于judge从未在真实输出上被验证；L1b 评分管线在实验条件下实质未被验证。
- - Major: ITT 算术不一致：gemma L1a 2/6=0.333，而把一次失败试验计为 0 后 ITT 均值竟为 0.355（高于 0.333），数值自相矛盾，统计口径不清。
### Minor（4）
- - Minor: 模型规模未控制（7b/14b/9b，跨 Qwen/Gemma 两族），无参数量匹配对照，跨模型结论的解释力受限。
- - Minor: 仅测试小到中等规模本地模型，L1b/L2 上无大模型或前沿模型参与，套件的判别力与泛化范围未被充分展示。
- - Minor: "N=8 supplement 仍 p=1.0000"同样无功效，且未见预注册停样本规则或样本量论证，存在随意补样本之嫌。
- - Minor: L1b gold 仅单标注者（21 gold），未报告标注者间一致性，gold 标签可靠性不足。

## 新颖性（novelty）— ok
### Critical（2）
- - **Critical**: "统一基准"的实质是将三个已有基准（AIRS-Bench、ResearchClawBench、GAIA2 p3dev）放入同一个 `run.json` 契约下运行，未提出任何新任务、新评测范式或新能力维度。核心贡献是工程编排（统一 harness + JSON 契约），而非研究突破，且未与已有的多能力 agent 基准（如 AgentBench 等已覆盖多种 agent 任务的统一框架）进行差异对比，增量贡献被严重夸大。
- - **Critical**: 声称的 GAP——"评测碎片化"——是一个泛化、众所周知的观察，论文既未引用具体文献证明该缺口无人填补，也未论证将这三个特定基准组合后产生了独立运行无法获得的洞察。GAP 的"真实性"未被建立：论文未说明跨三层能力的联合评测能揭示什么单独评测不能揭示的结论（例如，三层的得分相关性、能力迁移证据等均未提供），使得"统一"本身缺乏科学必要性论证。
### Major（5）
- - **Major**: L1b 在全部三个模型上得分为 0/10，该层完全无区分能力。一个测量工具在其三个声称能力之一上对所有被测对象返回相同零分，说明该层的任务设计或难度校准存在根本问题，其作为"基准"的贡献价值存疑。positive control 证明 pipeline 可解，但这恰恰反衬出所测模型范围全部落在该层有效测量区间之外。
- - **Major**: L2 使用 N=4 且自述 McNemar 功效 = 0.0000，即该实验在统计上无法检测任何效应量。论文明确承认这一点，却仍将"两 arm 无显著差异"作为发现呈现——这在逻辑上是空无结论（absence of evidence ≠ evidence of absence），不构成对基准判别力的支持。
- - **Major**: "校准的 LLM-as-judge"被作为方法论贡献列出（FNR/FPR 门控、21/39 gold），但实际评测中 judge 调用次数为零（全部 SKIP）。校准从未在真实评测中被行使，因此它是未经实战验证的方法论装饰，不能作为已演示的贡献。论文以"a methodological warrant"措辞软化了这一事实，但这本质上是贡献声明与实际执行之间的断裂。
- - **Major**: "三层统计协议"（McNemar / Wilcoxon+CLES / Friedman+Nemenyi+CD）与 SHA-256 可复现封印均由标准统计检验和常规工程实践构成，无任何方法创新。将这些包装为核心贡献属于将统计卫生和软件工程惯例重新标价为研究贡献。
- - **Major**: "Answer-fitting audit（L047）"被呈现为新颖的防作弊机制，但论文未将其与文献中已有的数据污染检测 / 泄漏检测方法（如 training-data extraction probes、membership inference、canonical answer contamination checks）进行定位对比，其相对增量未被界定，新颖性被默认放大。
### Minor（1）
- - **Minor**: 仅评测 7b–14b 本地小模型，唯一的前沿对比（Model-F，L1a 6/6，6 个任务，探索性）规模极小，基准的有效判别范围未得到充分展示，无法支撑"可跨模型规模区分"的隐含主张。

## 可复现（repro）— ok
### Critical（5）
- - **Critical**: 模型标识不可复现 â `qwen2.5:7b/14b`、`gemma2:9b` 仅给出 Ollama tag（可变），未销定 model digest/commit/量化方式，同一 tag 在不同时间点可对应不同权重。
- - **Critical**: `deepseek-v4-flash` 不是已知公开模型（DeepSeek 现有 v2/v3/R1，无 "v4"；"flash" 是 Google Gemini 命名惯例），无法定位、无法复现。
- - **Critical**: 证据链矛盾 â 摘要称 "frontier Model-F scored 6/6"，引言称 "deepseek-v4-flash, 5/6 L1a"；6/6 vs 5/6、Model-F vs deepseek-v4-flash，无法确认是否同一模型，哈希对账无从对起。
- - **Critical**: L1b 实际评测轮次 "made zero judge calls (all SKIP)"，即校准好的 judge（FNR=0, FPR=0）从未应用于真实评测数据；校准→结果的证据链断裂，"0/10 for all models" 与 judge 校准无因果联系。
- - **Critical**: ITT 均值 0.355 无法对账 â gemma 三次试验分数述为 1/6â2/6、一次失败记 0；(1/6+2/6+0)/3 â 0.167，与 0.355 差距显著，算术不闭合。
### Major（9）
- - **Major**: 未声明 temperature、top-p 等采样参数；未声明是否 greedy/temperature=0，LLM 输出的 seed 级可复现性无法验证。
- - **Major**: 未指定推理引擎（Ollama / vLLM / llama.cpp / text-generation-inference）；不同后端的量化方案、KV cache、batch 策略会改变输出，配置快照缺失。
- - **Major**: "SHA-256 seal over 125 files verifying byte-for-byte reproducibility" 未区分是 harness 脚本/配置文件还是模型输出文件；若含后者，对随机 LLM 声称 byte-for-byte 可复现是极强断言，需明确前提条件。
- - **Major**: "18/18 independent recomputation checks" 未定义检查范围 â 是从存储输出重算统计量（平凡可复现），还是重跑模型验证结果一致性（非平凡），二者含义差异巨大。
- - **Major**: 未声明 AIRS-Bench、ResearchClawBench、GAIA2 p3dev 的数据许可（license）；GAIA2 与 GAIA 的许可继承关系不明，复现者无法确定合法再分发权利。
- - **Major**: 声称 "we release the suite" 但正文未给出仓库 URL、DOI、Zenodo 档案号或持久化标识符，一键复现的入口缺失。
- - **Major**: 未提供环境锁定（requirements.txt / environment.yml / Dockerfile / Python 版本），"canonical script" 依赖的库版本未 pin，统计脚本跨版本可能产生不同 p 值。
- - **Major**: 未指定硬件（GPU 型号、VRAM、是否使用 GPU offloading）；14b 模型的量化与运行方式由此决定，直接影响输出。
- - **Major**: 声称 "per-seed rows" 但 seed 值未列举（几个 seed、具体整数、是否固定）；"bootstrap at step/seed level as future work" 更暴露 seed 级复现尚未完成。
### Minor（3）
- - **Minor**: `run.json` contract 的 schema 字段未在可见文本中定义，复现者无法验证自己的 run 是否符合契约。
- - **Minor**: 校准集仅 21/39 样本即报告 FNR=0.0000、FPR=0.0000，未给置信区间，小样本下的零值缺乏统计保障。
- - **Minor**: "deepseek-v4-flash, 5/6 L1a" 与摘要 "Model-F scored 6/6" 的映射关系未声明，应在表格中统一标识。

## 写作（writing）— ok
### Critical（2）
- - Critical: 摘要称"frontier Model-F scored 6/6"，但正文称"deepseek-v4-flash, 5/6 L1a"——若为同一模型则 6/6 vs 5/6 直接矛盾；若为不同模型则 Model-F 在正文中从未定义。
- - Critical: 摘要声称 LLM-as-judge "passed at FNR=0.0000, FPR=0.0000"，紧接着说"the round made zero judge calls (all SKIP)"——零调用不可能产出 FNR/FPR，二者自相矛盾，"methodological warrant"的辩解无法消除数值造假观感。
### Major（6）
- - Major: 正文定义统计协议为"Friedman+Nemenyi+CD"，但摘要报告的后续校正为"Holm correction (p=0.0261)"——Nemenyi 与 Holm 是不同方法，摘要与正文未交叉对应，读者无法判断究竟用了哪种。
- - Major: gemma 的 L1a 得分为 1/6→2/6 且含一次失败试验计 0，但"intention-to-treat mean 0.355"无法由 (0, 1/6, 2/6)/3≈0.167 或任何合理组合复现——数值不可调和。
- - Major: 字母"F"被同时用作 L2 臂标签（F=completion-guided harness）和前沿模型标签（Model-F），术语碰撞导致读者混淆。
- - Major: Friedman 声称"16 paired tasks"，但 L1a 仅 6 个任务，16 的来源从未解释；且"curated L1a (6 tasks)"即为全部 L1a 任务却称为"curated"（精选），用词误导。
- - Major: McNemar 检验 N=4，但摘要同时报告 24 行 L2 数据——检验单元与行数的映射关系缺失，读者无法确认 N=4 指 4 个场景还是其他。
- - Major: 两臂产出完全相同的均值至四位小数（0.1418 / 0.1918 / 0.2750 "for both arms"），即 n_d=0；两种不同方法产生逐位相同的结果是极强主张，仅以"p=1.0000"带过，缺乏解释。
### Minor（7）
- - Minor: 正文"L047 answer-fitting audit"中 L047 为未定义代号，首次出现无解释。
- - Minor: "deepseek-v4-flash"并非已知模型名称（DeepSeek 公开版本为 v2/v3），疑似名称错误或杜撰。
- - Minor: 摘要为单段超长文本，嵌套约 30 个数值与多层括号，结构严重过载，应拆分为背景—方法—结果—局限四句群或引入结果表。
- - Minor: "21 gold"与"39 gold in the expanded set"两个标注集规模的关系统一未说明。
- - Minor: McNemar power 报为精确"0.0000"，精确零值不合常理，应报近似值或说明退化原因。
- - Minor: "intention-to-treat"为临床试验术语，用于基准评测不常见且未做类比说明。
- - Minor: N=4 与"N=8 supplement"的关系（是否为补充场景、是否合并）未交代。

## 伦理（ethics）— ok
### Critical（3）
- - Critical: 未声明任何数据集/模型的许可合规信息。SciEvalSuite 复用了 AIRS-Bench、ResearchClawBench、GAIA2 三个外部基准以及 qwen2.5、gemma2、llama3.1、deepseek 等模型，但全文未给出许可证（GAIA 通常为 CC BY-NC，Qwen/Llama 各有各自的使用条款），存在未授权商用与再分发风险。
- - Critical: 比较基准中的 "deepseek-v4-flash" 为不存在的型号名（DeepSeek 官方并无 v4-flash），属虚构/误标模型，使"前沿 Model-F 得 6/6"这一关键对比无法核验，涉嫌结果不可复现与学术不端边缘。
- - Critical: 全文无任何安全/误用风险评估。所评测的 agent 涉及代码生成与执行、工具/环境交互（L2 GAIA2 p3dev），却未说明沙箱隔离、网络访问控制、有害代码防护、数据外泄防护等措施，存在被复用为危险能力评测的误用风险。
### Major（4）
- - Major: 利益冲突未披露。L2 的 F 臂（completion-guided harness）由作者自研并与 A 基线对比，属自评自家方法，未声明 COI 也无独立第三方复核，"无统计显著差异"的结论存在偏倚可能。
- - Major: LLM-as-judge 的校准声明（FNR=0.0000、FPR=0.0000）与"该轮零次 judge 调用（全 SKIP）"自相矛盾，把从未实际生效的校准当作"方法学担保"写入摘要，存在误导读者合规与可信度的风险。
- - Major: 双盲/可复现冲突。"Model-F" 身份在投稿中对评审隐藏，但模型并非作者，匿名化反而使摘要中最显著的 6/6 前沿对比无法独立验证，违背 TMLR 的可复现性承诺；若 Model-F 实为作者自有或关联模型，则同时构成 COI 隐瞒。
- - Major: 缺少隐私/PII 评估。GAIA 任务基于真实网络内容，可能含个人邮箱、账号、文档等个人信息，benchmark 将其打包并以 SHA-256 固定发布，未做脱敏与隐私审查，存在数据再披露风险。
### Minor（3）
- - Minor: L1b gold 标注仅"single annotator"（21 gold），未报告标注者间一致性（inter-annotator agreement），也未见标注者身份/资质/报酬披露，涉及众包伦理与标注可靠性。
- - Minor: 未定义的标记 "L047 answer-fitting audit"——"L047" 既非缩写表条目也无解释，疑似内部编号外泄，既影响可复现也可能暴露未脱敏的内部流程信息。
- - Minor: 在 N=4 且作者自报 McNemar 功效为 0.0000 的前提下仍于摘要断言"两臂无差异"，虽披露了功效限制但结论措辞仍可能被误读为有效阴性结果，存在过度解读的伦理风险。

## 汇总

- **Critical: 21 | Major: 44 | Minor: 23**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）