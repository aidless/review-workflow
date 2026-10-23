# 对抗审查报告

- 时间: 2026-08-27T08:19:00.763757+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（3）
- - Critical: L1a 事后精选 6 个任务子集得到 p=0.003，明确标注 post-hoc/exploratory，但仍将该 p 值写入摘要，构成 data dredging；未做多重检验校正，该 p 值对因果推断无效。
- - Critical: L2 两个 arm（A vs CG）在所有三个模型上得分完全相同（n_d=0），N=4，直接断言"statistically uninformative"规避了更合理的解释——CG harness 可能根本未生效（实现 bug / arm 退化为同一逻辑），将实现缺陷误归为"无差异"。
- - Critical: Friedman 检验纳入 10 个 all-zero 的 L1b 任务，这些任务零方差、零判别力，违反 Friedman 对组内方差非退化的隐含前提；p=0.37 不是"无显著差异"的证据，而是检验失效。
### Major（5）
- - Major: 模型间比较存在混淆变量——三个模型经租用云 GPU 通过本地 OpenAI-compatible endpoint 提供，未报告量化策略、context window、推理参数是否跨模型一致；跨模型得分差异可能混入服务配置而非模型能力本身。
- - Major: L1b judge 校准（21 gold，后扩至 39 gold）声称 FNR=0.00/FPR=0.00，但实际评估中 judge 零调用（全 SKIP）；校准集与实际评分分布完全不重合，零错误率不能外推到未触发的评分场景，"methodological warrant"是空载保证。
- - Major: 功效分析披露 d_min=2.1279（80% power），这是极端大的效应量；在此功效下将"无显著差异"作为结论（如 L2 arms 无差异、Friedman 无显著）属于将备择假设未被拒绝误读为原假设成立。
- - Major: L1a 对 gemma 进行三次独立试验并报告 1/6â2/6 的"改善"，未对多次试验做多重比较校正；"intention-to-treat mean 0.355"将临床试验概念套用到 benchmark 试验，前提不匹配（无分组分配、无意向性治疗）。
- - Major: L1b gold 仅单标注者（21 gold），未报告标注者间一致性，judge 校准的"ground truth"本身缺乏信度保障，传递误差未被约束。
### Minor（2）
- - Minor: 前提"三层（L1a/L1b/L2）覆盖科学 agent 能力"未经独立验证；每层仅 4/6/10 个任务，构建效度的代表性假设缺乏支撑证据。
- - Minor: L1b positive control 仅证明"管线可解"，无法排除三个模型全 0/10 是由模型与环境交互的系统性因素（如 prompt 格式不兼容、工具调用协议偏差）而非真正能力不足。

## 统计（stat）— ok
### Critical（3）
- - Critical: 对 L1a 子集进行**事后挑选（post-hoc curated subset）**得到 p=0.003，这是典型的子集选择型 p-hacking；即便标注 "exploratory"，只要报告 p 值即构成无效推断，因为该子集是由数据本身诱导的，所得 p 不再服从原假设分布。
- - Critical: 对 16 个配对任务做 Friedman（p=0.37），其中 **10 个任务全为零**，存在严重地板效应与海量并列（ties）；Friedman 在并列占比 >60% 时渐近近似失效，该 p=0.37 既无意义又误导，等于把无效检验当作"无显著差异"的结论。
- - Critical: LLM-as-judge 校准报告 FNR=0.00、FPR=0.00，但金标仅 n=21（扩展集 39），且为**单一标注者**；按 "rule of three"，0/21 的 95% 上界约 14%，零错误率不可信，且无标注者间一致性（IRA）证据，"校准通过"在统计上站不住。
### Major（5）
- - Major: 全文所有均值（0.1418 / 0.1918 / 0.2750 / 0.355 等）**均未报告方差、标准误或置信区间**；点估计无离散度，无法判断差异是否落在噪声范围内，尤其 N=4 时单点不可解释。
- - Major: L2 的 N=4 对应 d_min=2.1279（Cohen's d≈2.13 属"极大"量级），说明设计**只对天文级效应才有 80% 功效**；如此严重 under-power 下，任何"无显著差异"都只是功效不足的假阴性，而非真无效应。
- - Major: McNemar 声称 n_d=0 导致功效"结构性为 0"，却仍并列报告 A 与 CG 两臂均值并称"both arms"一致；两臂完全不可区分应被定性为**设计退化/对照失效**，而非中性结果，且 A vs CG 的任何比较在此 N 下均属空操作。
- - Major: 跨 McNemar / Wilcoxon+CLES / Friedman+Nemenyi+CD / 事后子集进行了**多次检验**，全文未见 Bonferroni 或 FDR 校正；多重比较下 p=0.003 经校正后几乎必然不显著。
- - Major: gemma 在 L1a 上 "1/6 → 2/6 after three independent trials" 实质是**多次重跑取优**，违反 intention-to-treat 原则、抬高表面能力；同时把通过/失败计数（0/6、2/6）与 TextSimilarity 连续分（0.355）混为同一"均值"汇报，量纲不一致。
### Minor（2）
- - Minor: 摘要声称协议含 CLES（效应量）报告，但**未给出任何效应量数值**（如 CLES、r、η²），只报 p 与原始得分，效应量承诺落空。
- - Minor: 前沿 Model-F 仅 n=6 任务得 6/6，标 "exploratory"，无方差、无对照模型，属轶事级证据，不应进入任何比较性结论。

## 实验（experiment）— ok
### Critical（3）
- - Critical: L2 的两个 arm（A=ReAct vs CG=completion-guided）在三个模型上均得到完全相同的均值（0.1418/0.1918/0.2750），说明 CG 没有实际差分或已退化为 no-op，却仍被当作对比设计，且没有任何消融实验解释这一 null。
- - Critical: L2 主分析用 exact McNemar，N=4、n_d=0 不协调对，补充 N=8 同样 n_d=0，该检验在结构上无统计信息；在此前提下任何关于 arm/模型差异的描述都是无效的，相当于没有对照组。
- - Critical: L1b 三模型全部 0/10（执行失败），显著地板效应；跨模型 Friedman 把 10 个 all-zero 任务纳入 16 项，tie 过度膨胀，无法区分模型，对更强模型的泛化性未经检验。
### Major（5）
- - Major: seed/trial 管理在模型间不一致——gemma 在 L1a 上跑了"三次独立试验"（1/6â2/6），但 7b、14b 似乎是单次试验；用不同试验次数的结果做跨模型比较破坏了配对性与公平性。
- - Major: 关键超参数未报告（temperature、top-p、max tokens、few-shot、ReAct max-steps、预算 568/1000 在 layers/models/seeds 间的分配）；三个不同大小的模型在"rented cloud GPU"上以 OpenAI-compatible endpoint 服务，量化/推理后端未披露，可能造成不公平基准。
- - Major: "frontier Model-F"仅在 L1a 上探索性地跑出 6/6，未在 L1b/L2 上运行，不能作为跨层天花板/ceiling 基准，无法判断各层难度是否对齐。
- - Major: L1a 的"post-hoc curated subset(6 tasks)âp=0.003"明确标注为探索性/事后选取，无多重比较校正，泛化性不能成立，且 6 个任务样本太小。
- - Major: LLM-as-judge 校准（21â39 gold、单标注）声称 FNR=0/FPR=0，但实际 round "made zero judge calls(all SKIP)"，即 judge 在真实评分中从未被调用，校准与实际使用场景脱节，单一 positive control 不足以建立操作效度。
### Minor（2）
- - Minor: 跨模型比较混合了不同家族（Qwen vs Gemma）与不同参数量（7b/9b/14b），架构与训练数据混淆因子未去混淆。
- - Minor: "bootstrap at step/seed level as future work"，未报告任何方差 CI，seed 级不确定性完全未量化；L2 仅 N=4 场景，任务多样性不足以支撑泛化声明。

## 新颖性（novelty）— ok
### Critical（2）
- - **Critical**: 三层结构本质上是三个已有基准（AIRS-Bench、ResearchClawBench、GAIA2 p3dev）的重新打包，核心"统一"贡献相当于一个 wrapper 脚本加一个 `run.json` 契约。论文未论证"将这三个特定基准放在一起跑"能回答哪些单独跑时无法回答的科学问题，unification 的科学价值未确立，仅停留在工程便利层面。
- - **Critical**: 基准论文自身的评估结果全面处于地板或零信息状态——L1b 全模型 0/10、L2 零 discordant pairs 无法做统计推断、Friedman 非显著（p=0.37）。唯一显著的 p=0.003 来自事后精选子集且论文自标 exploratory。一个基准在自身实验中无法产生任何有区分力的发现，其作为评估工具的贡献根基存疑。
### Major（4）
- - **Major**: GAP 框架（"evaluation remains fragmented"）被夸大。论文引用的已有基准各自已覆盖对应领域且本身具备 harness/metric/reproducibility 设计；"三个基准用不同 harness"是工程摩擦而非研究空白，仅靠"用一个脚本统跑"并不构成需要新建一个 suite 才能填补的 gap。
- - **Major**: "denominator discipline"（失败计入分母归零）和"reproducibility contract"（SHA-256 seal + 独立重算脚本）被当作方法论贡献呈现，但前者是评测常识性规范、后者是标准工程实践，均不构成对现有文献的方法论增量。
- - **Major**: 两臂对比（ReAct vs completion-guided）作为 suite 的设计特性被提出，但结果显示两臂得分完全一致、discordant pairs = 0，即 suite 连自己的两个 harness 变体都无法区分。这直接削弱了"该 suite 能提供有区分力评估"的核心贡献主张。
- - **Major**: 统计协议（exact McNemar + Wilcoxon/CLES + Friedman/Nemenyi）全部使用标准现成检验，无任何针对科学 agent 评估场景的方法论适配或新设计；在 N=4/6/10 的极小样本上这些检验的结构性功效被论文自己承认为零，protocol 的贡献价值与实际可用性严重脱节。
### Minor（2）
- - **Minor**: LLM-as-judge 校准被列入摘要与关键词作为贡献点，但实际零次 judge 调用（all SKIP），校准仅作为"methodological warrant"存在，未在任何真实评估中行使过，不应在贡献叙事中与已验证组件并列。
- - **Minor**: 1000-call 硬预算被框架为方法论创新（"budget-controlled"），但预算约束是部署工程决策而非评测方法论贡献，且该约束直接导致样本量过小、统计无效，反而削弱了 suite 的科学产出能力，属于将限制包装为特性的嫌疑。

## 可复现（repro）— ok
### Critical（2）
- - Critical: 模型标识 "qwen2.5:7b / 14b / gemma2:9b" 形似 Ollama tag，可变且未钉定 commit/量化精度(Q4_K_M? Q8? FP16?)/serving 框架版本；摘要强称 "byte-for-byte reproducibility"，但可变权重直接证伪该声称。
- - Critical: 三数据源(AIRS-Bench / ResearchClawBench / GAIA2 p3dev)的许可证、版本号、下载来源与再分发权均未声明；在无许可与来源前提下，"125 文件 SHA-256 seal" 无法被第三方合法、一致地复现。
### Major（7）
- - Major: seed 全程缺失——"per-seed rows" 与 gemma "three independent trials" 提到种子，但具体 seed 值、RNG 来源、seed→row 映射均未披露；"bootstrap at step/seed level as future work" 反而坐实当前种子层不可复现。
- - Major: SHA-256 seal 的验证路径缺失——"125 files" 清单、聚合算法(逐文件哈希如何合并为单一 seal)、manifest 存储位置与第三方校验命令均未给出，"byte-for-byte" 无法独立核验。
- - Major: 配置快照不完整——"rented cloud GPU" 未给 GPU 型号/显存/厂商/区域；inference 引擎(vLLM/Ollama/llama.cpp)版本、temperature/top_p/max_tokens/system prompt、endpoint 配置、"run.json contract" 的 schema 均未在可见文本展示。
- - Major: 一键复现未落地——"independent recomputation script" 与 "fully recomputable harness" 仅有声称，无仓库 URL、无 Docker/lockfile、无 requirements 版本钉定、无安装与运行命令，不符合 TMLR 复现清单。
- - Major: "18/18 independent recomputation checks" 未定义——这 18 项检查的内容、判定阈值、输入输出均未列出，"passing" 不可复核，证据链断裂。
- - Major: TextSimilarity 指标实现未定义——0.355 依赖未指定的相似度计算(嵌入模型/tokenizer/聚合方式/归一化)，无法被独立重算。
- - Major: 判官校准 gold 仅 "21 gold, single annotator"——无标注协议、无 inter-annotator agreement、无标注者资质；gold 集本身复现性存疑，进而波及 FNR=0.00/FPR=0.00 的可复核性。
### Minor（2）
- - Minor: "568 calls (<1000 budget)" 的 call 计数口径未定义(按 prompt / 按 tool call / 按 model invocation?)，预算可复现性模糊。
- - Minor: "single canonical script"(McNemar / Wilcoxon+CLES / Friedman+Nemenyi+CD)未命名、未版本化、未链接，统计路径无法溯源。

## 写作（writing）— ok
### Critical（2）
- - Critical: "post-hoc curated L1a subset (6 tasks)" — 同一摘要已明确 L1a 恰为 6 道题（0/6, 2/6, 1/6→2/6），"6 道题的子集"即全集，"curated subset"自相矛盾。
- - Critical: 判官校验的 gold 数量在同句内冲突 — 先写"(21 gold, single annotator)"，紧跟"FNR=0.00, FPR=0.00 (39 gold in the expanded set)"，未说明 FNR/FPR 到底是在 21 还是 39 上计算的。
### Major（7）
- - Major: "18/18 independent recomputation checks"恰等于 18 条 L1a 行，但 L1b(30 行)、L2(24 行)的重算覆盖情况只字未提，可复现性声明范围不明确。
- - Major: "frontier Model-F scored 6/6 (exploratory)"中的 Model-F 全文无定义、无表格引用、无前文铺垫，读者无从知晓其身份。
- - Major: 术语漂移 — 摘要写"AIRS-Bench"，引言写"AIRS-Bench rad"；"GAIA2 p3dev"所引文献为 GAIA(General AI Assistant)，二者关系未作任何说明。
- - Major: "rule L047, an internal audit identifier"将内部追踪编号泄露进投稿稿件，属于不应出现的内部标签。
- - Major: 摘要结构失当 — Mcnemar 细节、d_min、FNR/FPR、SHA-256、p 值等统计量堆砌，淹没核心贡献，不具备摘要应有的概括功能。
- - Major: "mean goal completion … in both arms"表述歧义 — 要么 A 臂与 CG 臂均值完全相同（与"两臂不同 harness"矛盾且未解释），要么未真正给出分臂数值。
- - Major: "N=4; N=8 supplement likewise n_d=0" — L2 仅 4 个 scenario，N=8 的来源未交代，配对检验样本量定义不清。
### Minor（3）
- - Minor: "the round made zero judge calls (all SKIP)"中的"round"在摘要内无定义，读者无法判断所指实验轮次。
- - Minor: "$1/6 \rightarrow 2/6$ after three independent trials"使用非正式箭头记法，不适合摘要语境。
- - Minor: "calibration is a methodological warrant"措辞生硬，"warrant"非 ML 评估标准术语，含义模糊。

## 伦理（ethics）— ok
### Critical（2）
- - Critical: 双盲违规——"Conflicts of Interest"节明确披露"Model-F is a model contributed by the authors' team"，在 TMLR 双盲投稿中直接暴露作者团队拥有自研前沿模型；叠加"internal research funding"与组织专有标识符(L047、ARS v3.11、opencode.ai 别名)，足以反 anonymize 作者身份。
- - Critical: 利益冲突自相矛盾——声明"no conflicts of interest"却同时披露 Model-F 为作者自有模型，并将其作为 positive control 以 6/6 vs 0–2/6 优于全部竞品、再宣称"p=0.003 demonstrates frontier scaling"，属典型自评自利 COI；"no COI"声明与披露内容直接冲突。
### Major（6）
- - Major: 隐私主张存疑——声称"no PII"且"RCB/GAIA2 are synthetic"，但 GAIA 系列已知含真实网页抓取内容(潜在 PII)，GAIA2 p3dev 为"synthetic"无证据支撑；"no IRB was required"为作者自裁、未经机构伦理审查。
- - Major: Yelp 数据来源与许可未交代——Broader Impact 首次出现"Yelp is de-identified public text"，方法部分从未引入；Yelp Open Dataset ToU 限定学术用途并禁止再分发，与"release the harness"承诺可能冲突，且用户生成评论内容或落入 GDPR 个人数据范畴。
- - Major: 数据许可合规未落地——声称 CC BY 4.0/MIT/Apache 2.0"verified at primary sources"但核实仅藏于内部 evidence/protocol.md；CC BY 4.0 署名、Apache 2.0 NOTICE、MIT 许可证文本在再分发的 92 文件 zip 中是否齐备未在文中举证。
- - Major: 沙箱安全未经验证——执行模型生成代码但明言"a full capability/privilege boundary audit of the sandbox is future work"，网络隔离与超时仅声明未独立验证，对已发布的 harness 构成未评估安全风险。
- - Major: 误用/双用风险——公开 L047 answer-fitting 审计机制细节可反向指导模型开发者规避审计；"users must not fine-tune to produce disallowed content"为无技术约束的规范性声明，缺乏执行机制。
- - Major: 人工标注伦理缺失——"single annotator"对 21 gold 项做人工覆盖标签，未披露标注者身份(是否作者)、知情同意与报酬；若为作者自标则自标偏差未声明，"no IRB"亦为自裁。
### Minor（2）
- - Minor: 内部标识符(L047、ARS v3.11、FM-25、Q1–Q7、G11、GAP-1–4)为组织专有命名习惯，即便移除 Model-F 披露仍可作为匿名性指纹。
- - Minor: "opencode.ai model-pool alias"指向特定第三方平台关系，可能暴露身份且该平台 ToU/合规状态未交代。

## 汇总

- **Critical: 17 | Major: 39 | Minor: 15**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）