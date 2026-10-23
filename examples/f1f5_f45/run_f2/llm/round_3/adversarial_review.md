# 对抗审查报告

- 时间: 2026-08-27T19:34:29.081957+00:00
- 源: F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f2\extracted_text.txt
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（3）
- - Critical: cell/样本量定义不自洽：文中同时称“2,700 cells (270 episodes × 10 seeds, K=3..5 × γ=...)”但按 K×γ 网格展开应为更多单元，若按 episode-seed 则 P/B 的聚合层级不清，使分母、重复测量和所有置信区间无法审计。
- - Critical: 下界 B 是在 K=3 pilot 上拟合 c0 后直接在同一实验数据上宣称“超过 B 的所有 cell”，没有独立验证或交叉验证；由于 c0 可任意取小，该 bound 本质上不可证伪，P/B 的 tightness 是后验拟合而非有效证据。
- - Critical: 报告“0.68% improvement”的 95% Wilson CI [0.62,0.74] 并明确说“为避免与 0/15 矛盾”，属于为规避不利结果而选择统计方法；且 Wilson 区间用于比例而非组间改善差异，且未预先注册主结局与推断方法，结论的因果/统计推断不恰当。
### Major（5）
- - Major: 将 K 增加称为“ensemble improvement”并隐含 K 导致更可靠，但 K、γ、模型、任务、阈值措辞和种子在同一网格中联合变化，未控制混淆变量；该设计只能支持条件关联，不能支持 K 的因果效应。
- - Major: 两个引理依赖 verifier 可交换且 ρ<1，但未检验可交换性，也未说明 ρ 在不同 K、γ 和选择性保留子集下如何估计或是否恒定；实际使用多个本地模型时该假设很可能不成立，理论结论不能直接迁移到样本。
- - Major: “Fisher-like information”未给出似然或期望 Fisher 信息的正式定义，且“inverse variance decreases ... information increases”的数学方向混乱；方差公式不能自动等同于信息量，因此“更多 verifier 增加信息”的论证不成立。
- - Major: tightness 报告存在选择性：只报告 γ∈{0.5,1.0} 为 5–10×，摘要又给总体中位数 10.88×，未报告 γ=2 的结果、cell 级分布或不确定性；在 bound 可任意松的情况下，“全部超过”没有标定意义。
- - Major: 种子处理不够：主结果基于 single-generator seed 42，事后用 seeds 42–44 的 pooled SD 0.026 打补丁，未把种子作为随机效应或做预注册敏感性分析；K=6 仅一个观察值，不足以支撑 scaling 推断。
### Minor（1）
- - Minor: Cmin(K)、Rsel、ρ 和 “minimum coverage” 的构造式、阈值规则及 ρ 的估计方式未在摘要/简述中给出，关键命题不可证伪，降低可复现性。

## 统计（stat）— ok
### Critical（2）
- - Critical: 将 2,700 个 cell 当作独立样本，忽略了同一 episode/seed/model 在 K、γ 间重复测量产生的聚类结构；有效独立样本量远小于 2700，所有 CI 和检验都可能过窄。
- - Critical: c0 在 K=3 pilot 上拟合，又在同一数据集（很可能包含 pilot）上声称 “P exceeded B in all cells”，属于样本内循环验证，不能作为经验下界的证据。
### Major（5）
- - Major: 0.68% 的 ensemble 改进用单个比例的 Wilson CI [0.62, 0.74] 不恰当；改进是两条件/配对结果的差值，应使用差值的 Newcombe/Wilson 或 bootstrap CI，并报告 N、基线和效应量。
- - Major: pooled SD 0.026 仅来自 seeds 42–44，n=3 不足以估计生成器方差，也不能为 “single-generator seed 42” 提供有效的单点不确定性。
- - Major: K=6 只有单个 300-cell 观测，K=3..5 每格仅 30 episodes×10 seeds，且 ρ≈0.3 未给 CI；据此声称 scaling/monotonicity 的样本支持不足。
- - Major: 在 9 个 setting、2,700 cells、4 个 model 上筛选 “all cells exceeded B” 和 tightness 模式，属于探索性多重比较；若作任何推断性表述，需预注册或多重比较校正。
- - Major: “P/B 为 5–10×” 与 “median 10.88×” 相互矛盾，应报告分布分位数，并说明是否包含 K=6 或样本内/外结果。
### Minor（1）
- - Minor: “inverse variance decreases” 与 “I(K) increases” 自相矛盾；I(K) 只是逆方差/信号噪声比，除非明确模型和正则条件，否则不应称为 Fisher information。

## 实验（experiment）— ok
### Critical（2）
- - Critical: 核心下界 B(K,γ) 的 c0 在 K=3 pilot 上拟合，却在包含 K=3 的同一 2,700 cells 样本中宣称“全部 cells 超过 B”，且未报告独立验证集或样本外 K/γ 划分，构成循环验证/数据泄漏风险。
- - Critical: 样本量表述不一致：2,700 cells 与“30 episodes/setting × 9 settings × 10 seeds × 4 models”应有的 10,800 cells 或按模型分开的计数对不上，导致每个 cell 的样本量和统计功效无法核实。
### Major（6）
- - Major: 缺少真正可归因的对照组：仅提及 K=1,2 baseline，但未说明是否与 K≥3 使用相同任务、温度、解码参数、计算预算及 coverage-matched 设置，无法区分“更多 verifier”与“阈值/算力/投票机制”的效果。
- - Major: 消融不完整：未分别消融 K、γ、ρ、指数项和 K^{-1/2} 项，也未检验去掉 exp(-γK/10) 后下界是否仍成立，无法证明该函数形式的每一项都必要。
- - Major: 基准公平性不足：未报告具体 benchmark、任务分布、模型版本/大小，也未与 non-ensemble confidence thresholding、SelectiveNet 或 self-consistency 等选择性预测 baseline 对比，不能支撑集成 verifier 的相对优势。
- - Major: 超参数管理不规范：γ 只取三个固定值，c0=0.05 是单点拟合且无置信区间，K=6 仅一个 observation；未做超参敏感性分析或校准曲线，结论对阈值选择的依赖未知。
- - Major: seed 管理不完整：主实验虽有 10 seeds，但 generator seed 42 结果只用 42–44 的 pooled SD 修正，未说明 c0 拟合、P/B 和 bound 是否跨 seeds 稳定，也未报告 seed-level 方差。
- - Major: 泛化证据薄弱：明确号称 sample-descriptive，但未在 held-out models/tasks/thresholds 上验证，也未按四个模型分层报告；K=6 单点外推不足以支持“一般性 empirical characterization”。
### Minor（1）
- - Minor: 四个“local models”的选择标准、版本、量化/温度/解码超参和任务分布均未披露，无法评估模型多样性是否足以代表真实 verifier 集成。

## 新颖性（novelty）— ok
### Critical（3）
- - Critical: 两个 “lemma” 基本不是新贡献：Cmin(K) 在可交换/等相关模型下的单调性是经典多数投票或等相关样本结论的简单推论，而 I(K)=(Δp)²/[σ²(ρ+(1−ρ)/K)] 只是等相关样本均值的方差公式；文中没有定义参数似然，将其称为 “Fisher-like information” 是概念拔高。
- - Critical: 声称的 GAP 不真实：self-consistency 文献（如 Wang et al., 2022）已经系统刻画性能随采样路径/验证器数量 K 增加而提升并趋于平台，selective prediction 已有成熟的 risk–coverage 理论；“换成 local models + K×γ 网格”只是场景微调，不足以构成开放问题。
- - Critical: 主要经验贡献 B(K,γ)=c0 γ⁻¹K^{-1/2}exp(−γK/10) 是在 K=3 pilot 上拟合的任意函数，无推导、无 held-out 验证，且 P/B 为 5–10×（中位 10.88×），作为 lower bound 几乎平凡，无法支撑“经验刻画”的贡献。
### Major（2）
- - Major: 实验规模过薄：K 仅 3..5、γ 仅 3 个值、每 setting 仅 30 episodes、K=6 只有一个观察，四个本地模型不足以支持随 K/γ 的普适 scaling 结论。
- - Major: 核心改进只有 0.68%，作者又自曝 “0/15 zero-success” 和 pooled SD 等不稳定信号；窄 Wilson CI 与微小效应量不相称，容易夸大 K-verifier ensemble 的实际收益。
### Minor（2）
- - Minor: 摘要与贡献节一边称 characterize/lower bound，一边自认 sample-descriptive、not derived、does not tightly characterize，实质性削弱了新颖性主张。
- - Minor: Related Work 未与 self-consistency 的规模实验、ensemble selective prediction 和 conformal/abstention 工作充分对比，因此没有真正论证与现有文献的差异。

## 可复现（repro）— ok
### Critical（6）
- - Critical: 未提供任何可下载仓库、容器/依赖锁文件或一键复现命令；只声称“Gates 9/9 锚定到 L401–L409”，但附录内容并未随产出提供，行号无法独立验证。
- - Critical: seed 协议不可复现：正文称每 cell 用 10 seeds，却只明确写出 42 与 42–44，未给出 10 个 seed 的完整列表、各模型/任务/采样阶段的 seed 映射，也未解释 n=10 与 n=3 的矛盾。
- - Critical: 配置快照缺失：未报告四个本地模型的精确名称/版本/权重来源、prompt 模板、投票聚合方式、γ/阈值实现、temperature、top_p、max tokens、推理框架、GPU 与依赖版本等关键配置。
- - Critical: 数据许可与来源缺失：未说明任务数据集及模型输出数据的 license、是否允许重新分发、数据获取时间、数据集版本，也没有 data availability 链接。
- - Critical: 无哈希对账：未提供数据、模型权重、代码、config、日志或输出表 any SHA-256/checksum；仅靠“颜色编码绿色”的 ledger 无法做自动化对账。
- - Critical: 证据链不完整：2,700/300 个 cell 的逐 cell 原始结果、日志、中间 CSV、拟合 c0 的脚本均未提供，无法从 raw data 重算出 P 值范围和 0.68% CI。
### Major（5）
- - Major: 核心数字自相矛盾：P/B 先说 5–10× 又说 median 10.88×；P 范围 0.14–0.26 与 K=6 的 P=0.3326 不吻合；2,700 cells 的计数口径也需要明确。
- - Major: B(K,γ) 的 c0=0.05 “fitted on K=3 pilot”未报告拟合目标、优化器、数据划分、样本量和随机种子，也没有独立 cell 上的校准误差或置信区间，无法判断是否过拟合。
- - Major: “0.68% improvement，95% Wilson CI [0.62,0.74]”统计口径不清：improvement 不是比例，Wilson 公式的分子分母未给出，且“避免与 survey 0/15 矛盾”不是构造 CI 的可复现依据。
- - Major: “Gates 9/9 checklist”只是自评行号锚点，未提供 checklist 内容、判定脚本、输入输出和版本控制；行号和颜色都不是可执行证据。
- - Major: seed 42 single-generator 结果用 seeds 42–44 pooled SD 0.026 对冲，但未说明为何 10 seeds 变 3 seeds、pooled SD 如何计算、generator variance 如何建模，无法复核。
### Minor（2）
- - Minor: “Ledger 86 PASS entries are color-coded green”依赖视觉格式，应改为 CSV/JSON 加显式 PASS/FAIL 字段，才能被机器核对。
- - Minor: 未提供依赖锁文件/容器/随机数生成器设定（如 Python、PyTorch、transformers 等版本），即使有脚本也难以稳定复现。

## 写作（writing）— ok
### Critical（3）
- - Critical: 摘要中“inverse variance decreases (Fisher-like) I(K)=... with K (Fisher-like information increases)”自相矛盾：按公式 I(K) 应随 K 增大而增大，正确表述应是“variance decreases / inverse-variance information increases”。
- - Critical: 数字不一致：先说 “P/B 5–10× for γ∈{0.5,1.0} (median 10.88× across the 9 cells)”，中位数 10.88 与“5–10×”范围冲突；且按给出的 B 公式与 P=0.14–0.26 计算，γ=1、K=5 的 P/B 必然超过 10，除非另设子集，但文中未说明。
- - Critical: 摘要与引言混入大量审稿回复/复现检查式内容（“P0 26-block F1 24K→12K”、“Panorama 6-figure set was weakened”、“Ledger 86 PASS entries”、“Gates 9/9 checklist”、“single-generator seed 42”），破坏论文科学结构，且这些术语均未定义。
### Major（6）
- - Major: 样本量表述歧义：“2,700 cells (270 episodes × 10 seeds) ... across four local models”未说明 2,700 是每模型还是四模型合计；若是四模型合计，则与 270×10 的算式不一致。
- - Major: 摘要先说 P 范围 0.14–0.26，随后又说 K=6 “P=0.3326 gives P=0.33”，没有限定前者仅为 K=3..5 构造区间，读起来像直接矛盾。
- - Major: “The K-Verifier ensemble improvement of 0.68%”在摘要中无对比基线、无定义，读者无法知道提升相对什么；该句也与前文 P 随 K 增大的结果方向关系不明。
- - Major: “Fisher-like information”未作定义，且正文在“inverse variance”和“information increases”之间反复切换，术语方向不统一。
- - Major: 正文未给出可核对的图表/表格，却引用“Panorama 6-figure set”、“supplementary ledger table”、“Appendix L203–L212”等未编号视觉材料，图/表编号、标题与正文引用链缺失。
- - Major: 核心量 “selective risk–coverage product P=Rsel·Cmin”未说明 P 越大越好还是越小越好；后文既说 P 随 K 增大，又说“more verifiers yield predictably better reliability”，方向不明确。
### Minor（4）
- - Minor: 小数精度不统一：P=0.3326 与 P=0.33、P=0.14–0.26、P=0.08/0.11 混用不同有效位数。
- - Minor: “Ledger 86 PASS entries are color-coded green”仅靠颜色传递信息，既缺乏可访问性，也不是规范的学术表注。
- - Minor: 正文使用“weakened”“fronted”等主观/非学术措辞，与论文语气不符。
- - Minor: 摘要中的“local models”未给出模型名称或规模，导致结果范围无法独立解释。

## 伦理（ethics）— ok
### Critical（1）
- - Critical: 未披露数据/模型来源与许可：270 episodes、四个 local models、survey/生成器产出均无许可证、ToS、数据集出处或模型输出使用条款说明，若 episodes 或生成数据来自受保护语料/受限模型，已构成许可违规风险。
### Major（4）
- - Major: 隐私与人类数据合规缺失：文中出现 “survey 0/15 zero-success case” 和 “episodes”，但没有任何 IRB/伦理审批、知情同意、PII 脱敏或数据保留声明；若涉及人类反馈或真实对话，将直接违反隐私合规要求。
- - Major: 双盲匿名性被内部标识符破坏：P0 26-block F1 24K→12K、Panorama 6-figure set、Gates 9/9、Ledger 86 PASS、L203–L212/L401–L409 行号等高度特异的内部工程/审查痕迹可指纹化作者机构或产品线，且补充 ledger 可能未清理作者元数据。
- - Major: 缺少利益冲突与资助声明：未披露模型厂商、计算资源、雇主或内部 “Gates/P0/Ledger” 相关产品利益；这些内部流程暗示存在机构/商业关联，却未提供 competing interests 声明。
- - Major: 误用风险未加限制：选择性预测/弃权机制可被包装为“安全校准”并部署到高利害场景，但论文未说明弃权阈值不可等同于置信度、也不应作为医疗/法律/金融等高风险决策依据，存在误用与过度信任风险。
### Minor（1）
- - Minor: 缺少数据/代码/补充材料的再分发许可以及 artifact 可用性声明，导致合规审查和复现核查无法确认数据是否可合法共享。

## 汇总

- **Critical: 20 | Major: 33 | Minor: 12**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）