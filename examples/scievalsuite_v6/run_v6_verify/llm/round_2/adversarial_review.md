# 对抗审查报告

- 时间: 2026-08-27T06:45:52.902408+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（5）
- - Critical: L2 核心因果比较（A=ReAct vs CG）在 N=4、discordant pairs n_d=0 下运行，McNemar 功效结构性为 0；此时“无法检测差异”是设计失效而非“无效应”，把 A/CG 两臂均值并列呈现等于在零信息设计上做因果读图，absence of evidence 被默认成 evidence of no effect。
- - Critical: L1b 全部 0/10 且被自述为“execution failures, not judge scores”，因此 L1b 分数测的是执行环境/管线的可靠性而非模型的 workflow 能力；将其纳入“scientific agent benchmark”并按模型维度作 Friedman 比较属于因果归因错位（把环境失效当成能力差异）。
- - Critical: Friedman 在 16 个配对任务中含 10 个全零 L1b 任务，地板效应使检验退化；此时 p=0.37“非显著”不是发现而是设计无分辨力，却仍以探索性名义与显著性结果并列报告，构成确认性/探索性边界模糊。
- - Critical: L1b 的 LLM-as-judge 校准（FNR=0、FPR=0）是离线 warrant，而实际轮次全部 SKIP、零次 judge 调用；校准从未在真实产出上验证，内部效度存在直接缺口，不能作为 L1b 评分有效性的支撑。
- - Critical: 事后 curated L1a 子集（6 任务）得 p=0.003 与确认性非显著结果并列呈现，存在 HARKing / cherry-picking 风险；事后子集选择规则、是否数据驱动未说明，因果/推断地位未隔离。
### Major（6）
- - Major: 仅三个小尺寸本地模型（7b/14b/9b，Qwen 与 Gemma 混用），规模与模型族交叉混淆，无法把差异归因于规模或族；“scientific agents”普遍性前提缺乏支撑。
- - Major: gemma L1a 经“三次独立试验”从 0/6→1/6→2/6 后取成功值，best-of-trials 引入选择偏差与多重比较膨胀；intention-to-treat 的 0.355 与执行分 0/6 属不同量表却混入同一摘要陈述，可比性受损。
- - Major: “18/18 独立重算 + SHA-256 封存”共享同一原始 per-seed 行，验证的是聚合脚本与文件字节而非实验可复现性（未重跑种子/未控制 LLM 随机性）；把其表述为 reproducibility 证据是假设偷换。
- - Major: A/CG 两臂均值逐模型完全相同，可能源于弱模型下 CG 退化为基线行为或 completion guidance 未实际生效，该混淆变量未被机制性核查；相同均值被当作“臂无差异”的证据缺乏内部效度。
- - Major: L1b answer-fitting 审计在 3/3 模型上命中，但审计自身无金标准、未知 FNR/FPR；把审计命中当作“成功拦截”是未经验证的假设。
- - Major: L1b gold 仅单标注者（21→39 gold），FNR=FPR=0 可能是标注者=gold 创建者的人为一致，校准的内部效度未经独立标注检验。
### Minor（4）
- - Minor: “positive control” 仅 N=1（Model-F 6/6 与 L1b pipeline solvability），单点无方差，不足以构成内部效度意义上的对照。
- - Minor: L1b judge（llama3.1:8b）与被评小模型同处小模型同源空间，存在 judge-model 偏倚混淆，未做 judge 与被评模型的去耦。
- - Minor: 预算仅用 568/1000 却同时披露功率不足（N=4、d_min=2.13），功率上限部分为自设预算未耗尽所致，前提与结论存在张力。
- - Minor: N=8 补充样本仍 p=1.00，补充集与主样本的合并/分层规则未说明，假设其可作独立佐证缺乏依据。

## 统计（stat）— ok
### Critical（2）
- - Critical: 事后精选 L1a 子集（6 tasks）跑出 `p=0.003` 属于选择性推断（selective inference）：子集是基于"10 个全零 L1b 任务"这一观察结果事后剔除得来，p 值未对子集选择过程做任何多重比较/条件化校正，仅贴"exploratory"标签并不能使该 p 值有效，等于在已知数据形状后双 dipping。
- - Critical: 跨模型 Friedman 在 16 个配对任务上含 10 个全零 L1b 任务（`p=0.37`）：全零任务在所有模型上产生并列秩，既稀释信号又违反 Friedman 对秩差异的依赖前提；该检验实质上无信息量，却以 `p=0.37` 形式呈现为"真实但非显著"的检验结果，属误用。
### Major（4）
- - Major: L2 goal completion 均值（0.1418 / 0.1918 / 0.2750）在 `N=4` 下未报告任何方差、标准误或置信区间；N=4 时 SE 极大，这些点估计几乎不可解释，违反方差报告基本要求。
- - Major: LLM-as-judge 校准报告 `FNR=0.00, FPR=0.00`（n=39）却未给置信区间；按 Rule of Three，0 错误在 n=39 时 95% 上界约 7.7%，"0.00"是对小样本下完美性的过度陈述。
- - Major: 重复试验设计不对称：gemma L1a 跑了三次独立试验（1/6→2/6），而 7b/14b 仅单次，却以相同 `k/6` 计数格式并列报告；多次试验的逐次分数未披露，TextSimilarity ITT 均值 0.355 又混入失败 trial 为 0，估计口径不一致且无法做可比推断。
- - Major: L2 主分析 `p=1.00, n_d=0<6, N=4` 与补充 `N=8 p=1.00` 在 McNemar 上结构性无功率（discordance=0 时统计量恒定），摘要仍以 p 值形式呈现结论，易被误读为"无差异的证据"而非"无信息"；正确做法是不报告该 p 值作为推断结果。
### Minor（2）
- - Minor: `d_min=2.1279`（80% power）已表明该研究仅能检测 Cohen's d>2.1 的超大效应，即严重 underpowered，但正文仍以点估计形式报告 L2 差异，未同步给出置信区间以体现不确定性。
- - Minor: 摘要提及 Wilcoxon+CLES 作为协议一部分，但 L1a 跨模型比较中未报告任何 CLES 效应量数值，仅有计数与 p 值，效应量缺失削弱了对实际差异大小的判断。

## 实验（experiment）— ok
### Critical（2）
- - Critical: L2 两个 arm（A=baseline ReAct vs CG=completion-guided）在全部三个模型上给出完全相同的 goal completion 均值（0.1418 / 0.1918 / 0.2750"in both arms"），且 n_d=0 discordant pairs——核心消融的处置效应恒为零，要么 CG 实现与 baseline 实际等价、要么 harness 未真正分叉，该对照实验在结构上测不出任何东西。
- - Critical: 在明知 McNemar 功效"structurally 0"、N=4、d_min=2.1279 的前提下仍跑实验并报 p=1.00，属于零信息实验设计；运行一个功效为零的对照本身即设计缺陷，而非仅"透明性披露"可豁免。
### Major（11）
- - Major: L1a 对各模型试验次数不对等——gemma 跑了"three independent trials"并出现 1/6→2/6 的变动，而 7b/14b 似乎只单次运行；同一基准内不同受试者施加不同重复次数，破坏配对比较的公平性。
- - Major: 全样本 Friedman（16 任务，p=0.37）不显著后，"post-hoc curated L1a subset (6 tasks)"得到 p=0.003；即便标注 exploratory，事后挑选 6/16 子集再检验属于选择性 Reporting / p-hacking，无预注册或 Bonferroni 校正。
- - Major: Friedman 把 10 个全零 L1b 任务纳入 16 任务配对检验；floor-limited 下大量并列使非参数检验退化为无信息，"non-significant"结论不可信，应剔除全零任务或单独报告。
- - Major: 系统性受测模型仅 3 个小规模本地模型（7b/9b/14b）；唯一强模型 Model-F 只在 L1a、且 exploratory、单点 6/6，无法支撑任何跨能力层或跨规模泛化主张。
- - Major: LLM-as-judge 校准集（21 gold、single annotator、FNR=FPR=0）与实际运行脱节——"the round made zero judge calls (all SKIP)"，校准是对空集的 warrant；且单标注、无 inter-annotator agreement，校准本身不可信。
- - Major: seed 管理未量化："per-seed rows"被反复引用但 seed 数量、seed 与 trial 的关系未说明；gemma 的"three independent trials"是否即三个 seed、是否对其余模型/其余层同样施加，均未交代，导致可复现性声明悬空。
- - Major: 超参数（temperature / top-p / max_tokens / CG 引导强度 / 重试上限）在摘要与引言中完全不出现；568 calls 的预算在三层×三模型×多任务间如何分配、是否按模型等额配给，影响基准公平性但未披露。
- - Major: TextSimilarity intention-to-treat（含失败 trial 记 0，均值 0.355）只对 gemma 施加，其余模型无对应指标，造成跨模型度量不对称，无法在同一标尺下比较。
- - Major: L1b 全模型 0/10 归因于 execution failure 而非 judge 评分；"positive control demonstrates pipeline solvability"只能说明 harness 可解，却无法在受测模型间产生任何区分度——该层对受测集合而言是失效基准。
- - Major: answer-fitting audit（L047）声称拦截 3/3 模型，但无消融报告"无 audit"条件下的分数变化；安全机制对最终分数的因果影响未测量，消融不完整。
- - Major: L2 在 N=4 主结果外追加"N=8 supplement p=1.00"，事后扩样无预注册，且与主结果合并/替代规则未定义，属 ad hoc 样本量调整。
### Minor（1）
- - Minor: 参考模型"deepseek-v4-flash"型号名非标准/疑似不存在，且其作为 API baseline 的受测层、调用次数、是否参与配对检验均未说明，基准公平性无法核验。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 三大组件（AIRS-Bench、ResearchClawBench、GAIA2）均为已有基准的直接复用，"unified benchmark" 的核心新颖性实质是 harness/contract 包装层，没有任何新任务设计或新能力维度的引入，集成型贡献被包装成研究型贡献。
- - Critical: 实证结果几乎全面塌在地板上——L1b 三模型均 0/10、L2 统计无信息量（p=1.00、power 结构性为 0、N=4），唯一显著的 L1a 子集 p=0.003 被自标为 "exploratory, not confirmatory"；即基准在所测模型上未展示出判别力，"能区分真实科学推理"的 GAP 没有被实证闭合。
### Major（4）
- - Major: GAP 论证薄弱——"evaluation remains fragmented" 是合理观察，但未与已有统一型 agent 基准（AgentBench、GAIA 多级设计、OSWorld 等）做差异对比，且 Intro 仅以 goodfellow2016deep（深度学习教材）支撑动机性论断，相关工作覆盖缺失，使"碎片化未被解决"的 GAP 真实性存疑。
- - Major: "three-layer statistical protocol" 被作为方法贡献宣传，但 McNemar/Wilcoxon/Friedman 均为教科书级现成检验，且论文自承 L2 功率为 0、N=4 无法检出任何 arm 差异；协议被宣称却未在主结果上产出有效信息，贡献被夸大。
- - Major: LLM-as-judge 校准作为卖点列出（FNR/FPR 门控），但该轮"made zero judge calls (all SKIP)"，校准过的 judge 从未在报告结果上实际运行，所谓贡献仅是"methodological warrant"而非已证能力，不应计入实质贡献。
- - Major: 所测均为小模型（7b/9b/14b）且近乎全失败，核心发现退化为"小模型不行"这一非新颖结论；唯一能体现基准上界的 frontier Model-F 仅在 L1a 给出 6/6 且标注 exploratory，基准的科学能力判别上界未被正式建立。
### Minor（2）
- - Minor: "answer-fitting audit (rule L047, an internal audit identifier)" 暴露项目内部规则编号，未给出可迁移的通用化定义，作为可复用贡献存疑。
- - Minor: L1a/L1b/L2 分层命名沿用 GAIA Level 1/2/3 思路，"a/b" 子拆分为增量修饰，分类学贡献微小。

## 可复现（repro）— ok
### Critical（5）
- - Critical: 全文宣称"fully recomputable harness"却未给出任何代码仓库URL或一键复现入口；corresponding author邮箱为占位符 `corresponding@example.com`，且双盲状态下评审无法核验任何复现声明。
- - Critical: "per-seed rows"与"three independent trials"反复出现，但全文未列出任何具体seed值/seed清单；seed级bootstrap还明确列为future work，seed不可追溯导致逐行复现无法对齐。
- - Critical: 缺少配置快照——未给出各模型权重commit哈希、量化方式、temperature/top-p等采样参数、scipy等库版本（"separate scipy path"对版本敏感）、本地OpenAI-compatible endpoint配置，离开快照无法复刻相同推理环境。
- - Critical: 宣称LLM输出"byte-for-byte reproducibility"却未声明采样配置（temperature=0？固定seed？）；本地模型推理在硬件/库版本差异下即便temperature=0也未必逐字节一致，该声明缺乏可验证依据。
- - Critical: SHA-256 seal over 125 files 与 SHA-256 manifests 仅口头提及，正文未给出任何实际哈希值、文件清单或对账流程（哪125个文件、canonical list如何生成、如何比对），哈希对账无法执行。
### Major（6）
- - Major: 三类基准(AIRS-Bench/ResearchClawBench/GAIA2)的数据许可均未声明；"fully recomputable harness"若涉及数据再分发，许可缺失直接阻断第三方复现。
- - Major: 参考模型"deepseek-v4-flash"版本身份可疑（DeepSeek公开版本到V3，未见V4-flash），frontier参考不可标识则对照结果不可复现。
- - Major: "18/18 independent recomputation checks passing"未枚举18项检查内容，且从已缓存的raw per-seed rows用scipy重算并非对LLM生成的独立复现，把recomputation与reproduction混为一谈。
- - Major: 证据链不对账：568 calls 与 24+18+30=72 reported rows 之间、以及与"125 files"之间的映射关系未透明化，无法逐条从原始调用追溯到报表数字。
- - Major: "rule L047, an internal audit identifier"为内部编号，外部无法定位answer-fitting审计的实现，破坏审计环节的可复现性。
- - Major: 1000-call budget下"复现"实需重新发起LLM调用（成本/算力），而recomputation才免新调用；论文将二者打包宣传"fully recomputable"，对读者构成误导性复现承诺。
### Minor（3）
- - Minor: L1b judge校准仅single annotator(21/39 gold)，无inter-annotator agreement，judge可复现性证据不足。
- - Minor: post-hoc curated L1a subset(6 tasks)得p=0.003，子集筛选规则未明示，复现时子集选择不可重复。
- - Minor: gemma L1a把pass/fail与连续TextSimilarity及intention-to-treat混用，计分细则未完整给出，影响该行结果的精确复现。

## 写作（writing）— ok
### Critical（1）
- - Critical: 摘要写“three cloud-hosted local models”，正文写“three small-to-medium local models served via a local OpenAI-compatible endpoint”；“cloud-hosted”与“local”自相矛盾，“cloud-hosted local models”本身就是悖论式表述，摘要与正文直接矛盾。
### Major（5）
- - Major: 摘要称“frontier Model-F scored 6/6”，正文引入“API-model reference (deepseek-v4-flash, 5/6”；若为同一模型则 6/6 vs 5/6 为数字矛盾，若为不同模型则 Model-F 与 deepseek-v4-flash 的映射关系未交代。
- - Major: 摘要“18/18 independent recomputation checks”与正文“every leaderboard number recomputed from raw per-seed rows”矛盾；总行数 24+18+30=72，18 项检查无法覆盖“每个数字”，重算范围无法对齐。
- - Major: âdeepseek-v4-flash”疑为虚构型名；DeepSeek 并无公开 v4 版本，“flash”为 Google Gemini 的命名惯例而非 DeepSeek 的，术语/事实性存疑。
- - Major: gemma 的 L1a 结果混用两种不可比指标——“1/6 â 2/6”（离散通过计数）与“TextSimilarity ITT mean 0.355”（连续相似度）未给出映射，1/6â2/6 与 0.355 之间的关系不可核验。
- - Major: L2âmean goal completion was 0.1418(7b), 0.1918(14b), 0.2750(gemma) in both arms”两个 arm 均值完全相同且无分 arm 明细；结合 n_d=0，暗示两 arm 可能功能等价，且无表格予以区分，数字呈现存疑。
### Minor（6）
- - Minor: FNR、FPR、CD、CLES 等缩写在摘要首次出现未展开；acronym 注释列出 ECE/TS/GAIA/CLES 为“defined”，但 FNR/FPR 未列，CLES 仅在正文出现。
- - Minor: ârule L047, an internal audit identifier”直接将内部编号泄入手稿，术语不规范，应改为有语义的标签。
- - Minor: â21 gold, single annotator) passed at FNR=0.00, FPR=0.00 (39 gold in the expanded set)”；21 与 39 两套 gold 的区别、0.00 是否同时适用于两套均未说明，数字关系含糊。
- - Minor: 摘要篇幅过长且密度过高（约300词、堆叠几十个括号 p 值/比率/效应量），结构上读如结果附录而非摘要，掩盖了贡献主线。
- - Minor: âGAIA2 p3dev”从未展开；acronym 仅注 GAIA=General AI Assistant，“GAIA2”与“p3dev”未解释，基准名称不透明。
- - Minor: 引入了 graphicx 与 booktabs，但所给文本无任何图表；如此密集的数值结果急需一张汇总表，intro 缺表属结构性缺失。

## 伦理（ethics）— ok
### Critical（1）
- - Critical: 数据许可未披露——复用 AIRS-Bench、ResearchClawBench、GAIA2 三个第三方基准并对外封存/发布 125 个衍生文件（SHA-256 seal），全文未声明各基准原始许可证与再分发条款，存在侵权与合规风险。
### Major（4）
- - Major: 隐私——GAIA2/L1b 任务含真实网页与人物信息，模型生成的报告含图表，释放 125 文件前未说明是否做过 PII/敏感内容脱敏与内容审核。
- - Major: 利益冲突——全文无 COI 声明；比较 qwen2.5(阿里)、gemma2(Google)、deepseek、llama3.1(Meta) 与匿名 "Model-F"，命名不一致，匿名可能掩盖作者与某模型厂商的关联或选择性披露。
- - Major: 双盲——对外释放的制品（per-seed 行、125 文件清单、正文公开的"内部审计标识 L047"）可能携带文件系统/git/时间戳等元数据，存在去匿名化风险，未声明已清洗作者元信息。
- - Major: 误用风险——L1a/L1b 让 LLM 生成并在本地执行代码、L2 让 agent 于真实环境交互工具，全文无沙箱隔离、安全门禁或负责任发布（responsible release）声明，harness 公开后可被用于有害自动化执行。
### Minor（3）
- - Minor: "frontier Model-F" 匿名损害可复现性，且与其余模型全部实名相矛盾；未给出统一匿名理由或访问说明。
- - Minor: 单一标注者、21 条 gold，未披露标注者资质、同意与报酬，缺乏伦理/人力审查说明（虽可能为内部标注）。
- - Minor: "deepseek-v4-flash" 似非公开发布版本，未给版本号与获取途径，影响可复现与透明度。

## 汇总

- **Critical: 18 | Major: 40 | Minor: 21**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）