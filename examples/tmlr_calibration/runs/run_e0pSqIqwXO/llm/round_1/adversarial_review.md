# 对抗审查报告

- 时间: 2026-08-26T06:35:27.375995+00:00
- 源: F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_e0pSqIqwXO\extracted_text.txt
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（3）
- - Critical: "no run reaches our 5 percent meaningful-gap threshold, so ... losses are similar" 是典型的接受零假设（H0）错误——仅因差异未越过任意阈值就断言"相似"，未做统计功效分析（power analysis），缺席证据≠缺席。在50个种子的成对比较中，若无效应量与功效报告，"无差异"结论无内部效度。
- - Critical: 低秩控制器"meet the same criterion because their open-loop rollouts often produce extremely large losses"——判定准则被数值爆炸/溢出满足，而非被其声称的耦合动力学机制满足。这使该准则对该架构丧失构念效度（construct validity），属于测量效度污染，却仍被计入"满足同一标准"的计数。
- - Critical: "62 also show long-horizon loss worsening, never without the radius increase" 被解读为谱半径增大是远程恶化的必要条件，暗含因果/必要性断言。但这是观测性共现，谱半径变化与行为恶化可同源于训练动力学这一共同原因（common cause），未做干预或对照以排除反向因果与混淆。
### Major（6）
- - Major: 均值峰值为"19.1倍初始损失"，仅报告均值而无分布、方差、中位数或离群值分析；在重尾损失分布下均值易被极端种子主导，该统计量的代表性存疑，且50个成对种子是否构成有效重复（effective replicates）未说明。
- - Major: 跨架构比较（GRU vs tanh vs low-rank vs two-layer）同时改变了门控机制、秩约束、容量与优化地形，多重混淆变量并存却未做控制变量或析因设计，无法将观测差异归因于任一单一因素，内部效度受损。
- - Major: "all 120 runs meet the criterion"与"reproduce in all 50 seeds"的100%通过率，本身可能是准则区分度不足（overly permissive criterion）的征兆而非稳健性的证据；若任何配置都通过，该检验几乎不具备证伪力。
- - Major: 多个架构×任务×准则的交叉检验（GRU/跟踪/tanh/路径积分/环形/部分可观/隐层尺寸/层数）构成大量多重比较，未见Bonferroni/FDR等校正，族错误率膨胀使单项"显著"结论不可靠。
- - Major: 在自称将定性主张转为定量检验的框架中，仍使用"weak behavioral transfer""finish close to the stability boundary""retains only the transient peak"等定性措辞，未给出可复现的数值阈值与判定规则，量化承诺未兑现。
- - Major: tanh隐层从50增至400的对比，同时改变了容量、参数量、优化轨迹与可能的过参数化效应，将"peak与稳定性穿越被保留"归因为架构不变性忽略了这些混淆。
### Minor（3）
- - Minor: "5 percent meaningful-gap threshold"的选取依据未给出，该先验阈值的任意性影响所有"无差异"判定的有效性。
- - Minor: "paired seeds"的配对机制（何者与何者配对、是否平衡、配对结构是否引入伪重复）未充分说明，影响方差估计与独立性假设。
- - Minor: 所选架构与任务子集（为何选GRU/低秩/环形任务而非其他）缺乏先验注册理由，存在报告选择偏差风险。

## 统计（stat）— ok
### Critical（2）
- - Critical: 头条效应量"mean peak reaching 19.1 times the initial loss"仅报告均值，跨 50 个 seed 无任何离散度指标（无 SD、无 95% CI、无中位数/范围）；比率型量天然右偏，均值极易被少数极端 rollout 拉高，读者无法判断 19.1x 的可靠性。
- - Critical: 全文同时检验 GRU、tanh、low-rank、two-layer、gated-controller、partial-observation、hidden size 50→400、path-integration 等十余个条件子集，属于典型多重比较场景，却无 Bonferroni / BH-FDR 校正，也未声明预先锁定的 family-wise 错误率，假阳性率不可控。
### Major（5）
- - Major: "all 50 seeds reproduce""all 120 runs meet the criterion"以 50/50、120/120 的计数结论呈现，但未给出二项比例的置信区间（如 Wilson/Clopper–Pearson）；"全部复现"在有限 n 下仍有非零未观测失败概率，结论强度被高估。
- - Major: "losses are similar""transfer is weak"为定性判断，既无效应量（Cohen's d / Δ / 优势比）也无对应统计检验；自称"paired seeds"却未对连续结局（峰值比、final-loss gap）做配对检验（配对 t / Wilcoxon signed-rank），配对设计的信息被浪费。
- - Major: "62 also show long-horizon loss worsening, never without the radius increase"是一个共现/条件概率论断，但未用 Fisher 精确检验或 McNemar 检验评估共现是否显著超出偶然；"never without"在 n=120 下既无 CI 也无检验，无法排除小样本侥幸。
- - Major: 50、120、60 等 seed/run 数量无任何样本量论证或功效分析；复现型研究虽 seed 偏多，但在判定"persistent final gap""weak transfer"等差异时缺乏对最小可检测效应量的说明。
- - Major: "5 percent meaningful-gap threshold"是实用显著性阈值，却被当作统计推断使用——它既不提供 CI、也不控制第一类错误，实质是把决策规则伪装成统计检验，且未与效应量及其不确定性挂钩。
### Minor（1）
- - Minor: "low-rank controllers meet the same criterion because their open-loop rollouts often produce extremely large losses"用"extremely large"模糊描述，未报告该子集峰值比的分布或是否构成离群驱动，存在选择性归因风险。

## 实验（experiment）— ok
### Critical（2）
- - Critical: 预设阈值（5% meaningful-gap、短视界改善+谱半径增加的复合判据）驱动了全部二元结论，但全文未对该阈值做任何敏感性分析；5% 与 1%、10% 之间结论是否翻转完全未知。
- - Critical: 低秩控制器"因开环 rollout 产生极大 loss"而满足同一判据——这是数值发散而非耦合动力学效应，说明该判据对此架构缺乏区分效度，却仍被并入"泛化成功"的叙事；缺少区分"真耦合效应"与"开环数值失稳"的控制实验。
### Major（9）
- - Major: 复现实验同时引入"新 seed"与"protocol changes"两个变量，无法将复现一致性/差异归因到任一因素；正确做法应分别仅变 seed、仅变 protocol，再做联合。
- - Major: 跨架构（GRU/tanh/low-rank）比较未说明是否对每个架构独立调参；若共享同一组超参，则架构间结论存在系统性偏差（如某架构因超参不匹配而表现"不迁移"）。
- - Major: 各实验 seed 池数量不一致（主对比 50、horizon 120、gated+ring 60），且未说明这些 seed 集是否重叠、跨架构比较是否使用配对 seed；无配对 seed 则"GRU 保留 final-loss 分歧而 tanh 仅保留瞬态峰"之类的跨架构比较无统计效力。
- - Major: 复合判据（短视界改善 ∧ 谱半径增加）始终以联合形式报告，未拆解各分量单独的贡献率与假阳/假阴率，无法判断是哪一子条件在驱动结论。
- - Major: 缺少负对照环境/任务——即一个耦合动力学理应不产生所声称效应的设置；当前所有任务均在预期效应范围内，无法证明诊断工具具有判别力而非"恒为正"。
- - Major: 120 次 horizon 实验中 62/120 出现长视界 loss 恶化，但"all 120 meet the criterion（含谱半径增加）"使得"never without the radius increase"这一条件陈述在逻辑上平庸（所有 120 都有半径增加），论文未报告反向条件（半径增加但长视界未恶化的数量），条件依赖性被夸大。
- - Major: hidden size 消融仅取 50 与 400 两个端点，无中间点（100/200 等），无法刻画单调性或相变位置；400 相对 50 跨度过大，"两端保留"≠"全程保留"。
- - Major: 两层控制器出现 persistent final gap 这一负面结果仅在摘要一句带过，既未匹配参数量相当的单层对照，也未做深度系统消融，无法判断这是深度效应还是参数量效应。
- - Major: 多个子实验（架构 × 任务 × horizon × 观测模式）产出大量二元判定，但未描述多重比较校正（如 Bonferroni/FDR），也无配对统计检验框架（binomial / McNemar / paired t）。
### Minor（2）
- - Minor: path-integration 迁移"weak"为定性表述，未像其他实验设定量化阈值，判据应用在全文中不一致。
- - Minor: 部分观测变体"finish close to the stability boundary"缺少同任务全观测配对对照，无法量化观测缺失的边际效应。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 本文核心定位是 Ger and Barak (2025) 的"独立复现"，而摘要自述的主要发现是"50 个配对种子全部复现瞬态峰值""谱阶段与耦合稳定性转换在全部 50 种子中复现"——这本质上是确认原结论，而非发现新现象。一篇以"复现且结论成立"为主轴的论文，其科学贡献的增量本身就很薄，但摘要用"every one of 50""all 120 runs meet the criterion"等强措辞营造了高强度的发现感，存在以统计严格性包装确认性结果、从而夸大贡献的嫌疑。
- - Critical: GAP 的真实性存疑。原文的耦合系统分析（coupled-system diagnostics、spectral radius of the coupled agent-environment system）本就是 Ger and Barak 自己提出的框架，本文只是沿用并复现它；而 Section 10 的"建议"——沿部署轨迹跟踪训练、显式报告 horizon 与失败 run——属于通用实验报告规范，并非针对某个被现有文献遗漏的科学问题。因此本文既没有在概念上超越原作，也没有提出可被证伪的新假设，所谓 GAP 更像是"审计/报告层面"的缺口而非科学缺口，被当作全文动
### Major（3）
- - Major: 与既有文献的差异未被清晰界定。Related Work 明确引用了 DAgger (Ross et al., 2011) 与 scheduled sampling (Bengio et al., 2015)，二者已系统处理 open-loop 训练 / closed-loop 部署的状态偏移问题；但正文仅一句"the coupled dynamics may differ from those of the RNN alone"带过，没有说明本文相对于这些经典 distribution-shift 工作究竟新增了什么不可替代的洞见，读者无法判断增量贡献是"方法上的新诊断"还是
- - Major: 架构扩展（GRU、low-rank、tanh、two-layer）与任务扩展（tracking、path-integration、ring）的结果高度混合——GRU 保留 final-loss 分歧、tanh 仅保留瞬态峰、path-integration 转移"weak"、partial-observation"finish close to the stability boundary"——这些是"有的复现、有的不复现"的散点结论，没有提炼出解释性的机制或可预测的判据。把"换架构/换任务后结果不一致"作为 robustness 贡献，但缺少统一解释，使其增量贡献停留在现象
- - Major: "protocol changes"在摘要与引言中被反复提及为 robustness 审查的关键手段，但从未在可见文本中具体说明改了什么协议（仅说"new seeds and protocol changes"）。若协议扰动的内容不透明，则"协议敏感性"这一贡献维度无法被读者评估，存在用未定义的实验维度填充贡献叙事的嫌疑。
### Minor（2）
- - Minor: 报告建议（Section 10）过于泛化——"follow deployed behavior throughout training with paired seeds""explicit reporting of horizons and failed runs"几乎适用于任何 ML 复现研究，未与本文独有发现绑定，难以构成与现有复现方法论文献的差异化贡献。
- - Minor: low-rank controller"满足同一判据"被归为支持性结果，但其原因是"open-loop rollouts often produce extremely large losses"——即满足判据源于数值不稳定而非真实耦合动力学效应，这削弱了"跨架构一致性"这一被暗示的贡献。

## 可复现（repro）— ok
### Critical（4）
- - Critical: 全文未提供任何代码/数据仓库链接、DOI 或长期归档快照；摘要声称"Explicit configuration files control our independent reproduction"，但这些配置文件根本无法访问，证据链在第一环就断裂。
- - Critical: 唯一指向评审记录的 OpenReview 链接被注入了空格（"https: // openreview. net / forum? id= e0pSqIqwXO"），无法直接解析跳转，主证据链失效。
- - Critical: 未给出代码 commit hash、数据 checksum/SHA256 或模型权重指纹，哈希对账完全无法进行，无法判定"独立实现"是否与原始 Ger & Barak 协议一致。
- - Critical: 全文未声明任务数据（double-integrator、tracking、path-integration）的来源与数据许可（License），下游复现者无法合法获取/再分发数据。
### Major（6）
- - Major: 多处以"50 paired seeds""all 120 runs""all 60 runs"作为统计依据，但实际种子值既未枚举也未发布（无 seeds.json/manifest），他人无法按相同 seed 逐 run 复算。
- - Major: 没有一键复现入口（无 Dockerfile/conda-env.yaml/Makefile/复现脚本），"Reproduction"出现在标题里却没有可执行的最小复现路径。
- - Major: 声称"criteria fixed before the reported sweeps"与"5 percent meaningful-gap threshold"是预注册门槛，但没有引用任何带时间戳的预注册记录或冻结的 config 快照，预注册主张不可验证。
- - Major: 关键数值（如"mean peak reaching 19.1 times the initial loss"）只给均值，未给方差/CI/seed 级分布，复现者无法判定数值是否落在噪声带内，无法做定量对账。
- - Major: "independent implementation"是核心主张，却未提供与 Ger & Barak 原始代码的 fork/diff 或协议对齐表，独立性无法证伪。
- - Major: 单一作者隶属私营公司（Eon Systems PBC），无学术合作机构背书，"独立复现"的第三方独立性难以佐证。
### Minor（3）
- - Minor: 原始基线"Ger and Barak, 2025"在可见片段中无完整书目信息（期刊/卷期/DOI），难以定位被复现对象。
- - Minor: 门槛定义（"meaningful-gap threshold""local-Jacobian crossing""spectral radius increase"）以叙述形式出现，未见机器可读的公式/配置表，复现口径易漂移。
- - Minor: 架构与超参（tanh hidden 50→400、two-layer controller、low-rank 维度等）散落在叙述中，未集中为可版本化的 config snapshot。

## 写作（writing）— ok
### Major（7）
- - Major: 摘要塞入 6+ 组数值（50、19.1、5%、120、62、60、50â400），读起来像结果章节而非概要，结构失衡。
- - Major: 术语不一致——"coupled-stability transition""stability crossing""local-Jacobian crossing""stability boundary"四个术语在摘要内交替出现，未定义也未说明是否同义。
- - Major: "50 paired seeds"歧义——是 50 个种子（paired 与什么配对？）还是 50 对（=100 个种子）？数字含义不明。
- - Major: "62 also show long-horizon loss worsening, never without the radius increase"为同义反复——前句已确立 120 runs 全部有 radius increase，62 作为子集自然也有，"never without"不增加任何信息。
- - Major: 50 / 120 / 60 三组运行数之间的关系（重叠、独立、嵌套）未在摘要中说明，读者无法判断实验设计。
- - Major: 引言以"ask whether the coupled-system analysis extends to nonlinear controllers and path-integration tasks"框定为开放问题，但摘要已对该问题给出明确答案（GRU/Tanh/low-rank 各自结论），摘要与正文框架矛盾。
- - Major: 引言无任何章节路线图，却突兀引用"Section 10"，结构突兀。
### Minor（7）
- - Minor: "deployed loss""meaningful-gap threshold"两个核心概念在摘要首次出现时未定义。
- - Minor: 数字"50"既表种子数（"50 paired seeds"）又表隐藏层大小（"50 to 400"），在同一段落中易致混淆。
- - Minor: Related Work 中"Barak describes these networksâ¦"以孤立段落出现，格式断裂。
- - Minor: URL"https: // openreview. net/ forum? id= e0pSqIqwXO"含多余空格，链接无效。
- - Minor: 引用格式"Ger and Barak (Ger and Barak, 2025)"重复作者名。
- - Minor: "extremely large losses"用词模糊，与文章其他处的精确数值（19.1×、5%）风格不一致。
- - Minor: 可见部分无任何图表引用，尽管涉及谱阶段、稳定性转换、loss 轨迹等本应可视化的内容。

## 伦理（ethics）— ok
### Critical（1）
- - Critical: 全文未包含任何利益冲突披露；唯一作者隶属商业实体 Eon Systems PBC（Public Benefit Corporation），且为单作者，若该公司在闭环控制/RNN 部署诊断方向有产品或投资利益，则"部署诊断"的正面框架存在未披露的财务偏向，且单作者结构消除了机构内部制衡。
### Major（3）
- - Major: 缺少数据与产物许可声明；论文"独立复现"Ger and Barak 的协议，但从未说明所访问的原始代码、数据或训练模型依据何种许可证获取，也未声明作者自身配置文件/代码将以何种许可证发布，存在合规与可复现性风险。
- - Major: 无 broader-impact / 双重用途误用风险讨论；闭环学习控制器及其稳定性诊断可直接迁移至自主武器、监控与对抗性控制场景，论文未提供任何负责任使用指引或缓解措施。
- - Major: 研究为单作者设计且无分析盲法；作者既"在报告扫描前固定判据"（预注册），又自行裁定"定性声明"是否被定量复现，假设生成与结果解读之间无任何独立盲审分析者，确认偏倚风险未被缓解。
### Minor（2）
- - Minor: 未显式声明"未使用人类或动物受试者数据"；尽管工作看似纯计算性质，但若引入了行为基准或经验数据，缺失声明会留下合规歧义。
- - Minor: TMLR 采用非匿名开放评审，作者商业隶属在评审期间即对审稿人可见，论文未承认潜在机构归属偏倚或描述任何缓解措施。

## 汇总

- **Critical: 14 | Major: 39 | Minor: 20**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）