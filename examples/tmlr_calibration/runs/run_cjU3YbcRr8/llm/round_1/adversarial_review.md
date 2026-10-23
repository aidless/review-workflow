# 对抗审查报告

- 时间: 2026-08-26T06:25:36.076261+00:00
- 源: F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_cjU3YbcRr8\extracted_text.txt
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（2）
- - Critical: The paper derives quasi-causal claims ("verifier quality materially affects skill-aware RL," "flat retrieval can degrade as libraries grow") from cross-paper observational synthesis across heterogeneous systems with different base models, task domains, RL algorithms, reward structures, a
- - Critical: The foundational premise that structurally orthogonal artifacts (code functions, NL lessons, SKILL.md packages, learned parametric adapters, memory traces, capability labels) are all instances of one coherent category ("skill") is asserted, not validated; collapsing these into a single l
### Major（5）
- - Major: No inclusion/exclusion criteria, search strategy, or inter-annotator agreement is stated for the "124-paper 2023–2026 audit set," leaving the corpus's representativeness and the taxonomy's generalizability unestablished (selection bias threat to external validity).
- - Major: "Admission and repair are repeatedly important" conflates frequency of appearance in papers with demonstrated importance; a design decision recurring across publications may reflect trend-following, shared codebases, or author overlap rather than empirically validated significance—a popular
- - Major: The eight-stage lifecycle architecture is presented as a universal decomposition but its derivation method is unspecified; it is unclear whether stages were inductively grounded in the corpus or top-down imposed, and no fit analysis shows real systems actually exhibit all eight stages versu
- - Major: A strong temporal confound is unaddressed: the 2023–2026 window spans rapid base-model capability shifts, so patterns attributed to "dynamic skill library" design (e.g., "flat retrieval degrades as libraries grow") may instead be artifacts of changing underlying model capacity, retrieval-vi
- - Major: "Evidence-graded patterns" are claimed but the grading rubric, evidence hierarchy, and rater reliability are absent, making the grades non-reproducible and unverifiable; it is unclear whether grades reflect empirical rigor of source studies or mere count of papers mentioning a pattern.
### Minor（2）
- - Minor: Boundary cases ("memory traces," "capability labels") are included "when they illuminate library behavior"—this subjective inclusion criterion undermines the taxonomy's systematicity and its claimed mutual-exclusivity / exhaustiveness.
- - Minor: Table 1's "Portable" column uses a single "∼a" symbol with an undefined footnote for most entries, collapsing a multi-dimensional property (cross-model? cross-environment? cross-agent?) into one mark, weakening comparability across the taxonomy's own axis.

## 统计（stat）— ok
### Critical（2）
- - Critical: 124 篇 audit set 未报告抽样框与抽样方法，属方便样本/非概率抽样，既无代表性分析也无功效分析，在此基础上对整个领域做归纳性外推结论（如"admission and repair are repeatedly important"）缺乏统计推断依据。
- - Critical: 因果断言"verifier quality materially affects skill-aware RL"与"flat retrieval can degrade as libraries grow"未报告任何效应量、置信区间或显著性检验，"materially/degrade"无量化阈值，属效应量缺失与推断误用。
### Major（3）
- - Major: 跨六类技能 Ã 八阶段生命周期同时合成多条"evidence-graded patterns"，构成多重比较情境，但无 Bonferroni/FDR 等校正，也未声明这些为描述性而非推断性结论。
- - Major: 分类学编码（sense 归属、lifecycle stage 归属）未报告编码者间信度（Cohen's/Fleiss' Îº）及其方差，无法判断分类一致性是否显著优于随机基线，方差/可复现性信息缺失。
- - Major: "evidence-graded"分级标准未见操作化定义，未说明分级是否基于效应量、样本量或 p 值，存在分级主观化与 p 值误用风险。
### Minor（1）
- - Minor: 表 1 可移植性列标注"â¼a"（近似）未定义"近似"的统计含义（不确定性来源与量级），不确定性未报告。

## 实验（experiment）— ok
### Critical（2）
- - Critical: 124 篇 audit set 没有给出可复现的检索/纳入/排除协议（检索词、数据库、时间窗判定、迭代轮次），本质是无对照的便利样本，所有 "evidence-graded patterns" 都继承该选择偏差，且对更广文献的泛化从未被检验。
- - Critical: "verifier quality materially affects skill-aware RL"、"flat retrieval can degrade as libraries grow" 等是因果性断言，但方法仅为文献通读，既无对照/消融比较、无 meta 分析的效应量汇总，也未区分"单研究内因果证据"与"跨研究相关观察"，结论在当前方法下不可证伪。
### Major（5）
- - Major: 全文为单作者，六感 taxonomy 编码与证据分级均由同一人完成，却未报告任何 inter-annotator agreement（κ/α）或 seed/reproducibility 协议，编码者偏差不可量化，整个分级体系无信度支撑。
- - Major: 缺少对 taxonomy/lifecycle 方案本身的 held-out 验证——6 感分类、8 阶段生命周期、10 算子词汇表都在同一批 124 篇上"既拟合又评估"，无 train/test 切分或外部语料验证，存在对 audit set 的过拟合风险。
- - Major: 六感之间的基准覆盖结构性不公平：前四种（可执行代码等）构成 "main dynamic-skill cluster"，记忆痕迹与能力标签被降为 "boundary cases"，导致 admission/repair/retrieval 等跨类型结论实际偏向代码型 skill，对其他 artifact 形式的代表性被系统性低估。
- - Major: 跨年代基准公平性未处理：2023 系统（Voyager、LATM）在已过时的任务套件上评测，与 2026 系统在不同 benchmark、不同模型骨干上评测被置于同一证据等级，未对 benchmark 难度、任务覆盖、backbone 差异做归一化，跨年比较不公平。
- - Major: 无消融验证分类粒度——未检验将 6 感合并为 4 感、8 阶段压缩为更少阶段是否会改变所综合的模式；粒度选择既无论证也无敏感性分析。
### Minor（2）
- - Minor: "evidence-graded" 的分级层级、判定阈值、"repeatedly important" 的频次门槛均未给出超参数式明确规格，综合结论不可复现。
- - Minor: 任何频次/模式计数统计均无 seed 管理与不确定性估计（置信区间/方差），"repeatedly important" 等表述缺乏量化支撑。

## 新颖性（novelty）— ok
### Critical（1）
- - Critical: 八阶段生命周期架构（evidence acquisitionâproposalâverify/admitâstorageâretrieval/compositionâmaintenanceâdistillationâgovernance）与已有 agent memory/tool-learning survey 的 memory lifecycle（acquireâencodeâstoreâretrieveâupdateâforget/govern）高度重叠；文中未给出与前序 survey 的显式 delta 对比表，"技
### Major（4）
- - Major: GAP 声明（"现有工作把 skill 当作静态集合"）被断言而非证明——引言列举了前置系统（Voyager/LATM 等）但未引用、逐条对比那些"据称忽视动态性"的前序 survey；缺少明确的"无人覆盖 lifecycle"的学术论据，GAP 的真实性存疑。
- - Major: "ten-operator vocabulary"与"skill-record schema"被明确 disclaimer 为"not a separate method contribution"，却又被列为三大 survey tool 之一并占据贡献位；这种套路让论文既能声称工具贡献、又可在受挑战时开溜"非方法贡献"——贡献定位自矛，新颖性不应既享利益又免审查。
- - Major: 六感 taxonomy 的主体（code/instruction/SKILL.md/adapter）实为工件类型的自然枚举，且后两类（memory traces、capability labels）被自认为"boundary cases"并基本排除；一个主要 case 已被前人非正式区分的四类工件 taxonomy，结构性新颖度限。
- - Major: Voyager（2023）已实现 verify(unit test)、admit、compose、增长式 library；多个"lifecycle stage"实际在单一基础系统中已齐备，部分"综合发现"更像是对一个早期系统设计的回溯性重标签，而非跨系统 pattern discovery。
### Minor（2）
- - Minor: "evidence-graded patterns"作为综合装置被提出，但摘录中未展示 grading 方法；证据分级在 systematic review 中属常规做法，本身不构成应被加权的新颖性。
- - Minor: "benchmarks under-report library trajectories / usageâutility gaps / safety surfaces"是 survey 中几乎套路化的 gap 表述；usageâutility gap、safety surface 在 tool-learning/memory 文献中已被讨论，"open problems"部分的增量性未被单独论证。

## 可复现（repro）— ok
### Critical（2）
- - Critical: "124-paper 2023â2026 audit set" 是本文的经验骨架，但可见文本未披鲜检索协议——无数据库、无搜索串/seed、无纳入/排除标准、无检索日期，语料根本无法复现。
- - Critical: 未发布任何可一键复现的工件（标注表、编码细则、论文→类目映射）；文中呼吁"concrete reporting standards"，自身却未践行。
### Major（4）
- - Major: Table 1 将每个系统归类到 taxonomy sense 与 verification handle，但未报告任何 inter-annotator agreement / 编码可靠性指标，归类赋值不可独立复现。
- - Major: 缺少配置快照：若筛选/编砠过程中使用了 LLM 辅助，则模型版本、prompt、temperature、日期均未披鲜。
- - Major: 无数据许可声明（论文语料、标注数据、释放代码）；被调研系统的 artifact 许可未对账。
- - Major: 引用消歧性脆弱——"Zhang et al., 2026i" 暗示同年同作者引用达 9+ 条，截断处"(截断)"表明参考列表不完整，证据链可追溯性存疑。
### Minor（2）
- - Minor: 无 SHA-256/任何哈希对账，语料清单或代码工件均无完整性校验。
- - Minor: 除 OpenReview 论坛链接外，无持久归档快照（DOI/Zenodo）锁定 124 篇论文清单，链接腐坏后无法回溯。

## 写作（writing）— timeout

## 伦理（ethics）— ok
### Critical（2）
- - Critical: 调研涵盖医学影像、推荐系统等领域，技能从"交互"中采集并持久存储，却未讨论 PII/PHI 嵌入存储技能与 provenance 元数据的隐私风险（HIPAA/GDPR），也无 IRB/知情同意议题。
- - Critical: "governance"阶段涉及技能跨 agent 共享与发布，但未讨论共享技能制品（爬取的代码、SKILL.md 包、学习到的 adapter）的数据许可与版权归属（GPL/Apache/专有许可污染），存在直接合规缺陷。
### Major（3）
- - Major: 作者姓氏"Li"出现在引文列表中（Li et al., 2026c），疑似自引，但未在正文或致谢中披鲲利益冲突与自引比例，违反 TMLR 利益冲突披鲲惯例。
- - Major: 技能涵盖网页操纵、桌面自动化、软件编写等双用能力，论文仅提及"safety surfaces"却未提供误用风险分类（技能投毒、凭据窃取、自动化攻击），与其"safety audits"引用不相称。
- - Major: 124 篇审计集的筛选标准未披鲲选择偏差，无法排除作者所在机构（CMU）相关工作被过度纳入的利益冲突嫌疑。
### Minor（2）
- - Minor: 发布版暴露作者身份并附 OpenReview 链接本身符合 TMLR 发表惯例，但审稿期间如自引密集，可能已弱化双盲性，建议核对投稿版匿名处理。
- - Minor: 技能从终端用户交互中蒸馏（distillation/portability 阶段）无用户同意讨论，部署场景下存在同意性缺失。

## 汇总

- **Critical: 11 | Major: 24 | Minor: 11**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）