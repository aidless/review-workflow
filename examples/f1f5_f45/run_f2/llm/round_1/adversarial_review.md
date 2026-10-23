# 对抗审查报告

- 时间: 2026-08-27T19:23:28.240144+00:00
- 源: F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f2\extracted_text.txt
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（2）
- - Critical: 核心验证存在循环风险：B 的 c0 是在 K=3 pilot 上拟合的，随后又在包含 K=3 的主样本 2,700 cells 中宣称“P>B 在所有 cell 成立”；若 pilot/主样本未严格切分，该下界只是在拟合数据上自证，不能作为经验刻画的外部证据。
- - Critical: “K-Verifier ensemble improvement of 0.68%（95% Wilson CI [0.62,0.74]）”是因果性表述，但 K 并未随机分配，K=1/2、K=3..5、K=6 比较在样本规模、episode 构成、模型和轮次上不可比；且正文 P 随 K 从 0.08 增至 0.33，与“improvement”方向矛盾，因果推断不恰当。
### Major（5）
- - Major: 理论前提可交换性未经验证：四个本地模型的 verifier 在架构、训练噪声、seed、生成顺序上很可能异质且存在高阶依赖；仅用一个点估计 ρ≈0.3 不足以支撑“ρ<1 下 Cmin(K) 单调非降”的结论，且 ρ 无置信区间。
- - Major: Fisher-like I(K) 公式基于无条件投票平均的方差，但 selective prediction 是在 agreement 超过阈值时才输出；条件化会改变方差和相关结构，直接用无条件 ICC 刻画选择性风险混淆了条件分布与无条件分布。
- - Major: Cmin(K) 的单调性结论缺乏操作化定义与可检验条件；若 abstention 定义为“全部一致”或固定票数阈值，coverage 完全可能随 K 下降，不能仅由 exchangeability 和 ρ<1 推出。
- - Major: 四个模型和多任务数据被 pooled 分析，模型精度、任务难度、episode 分布、阈值措辞都是潜在混淆变量；未报告按模型/任务分层、固定效应或敏感性分析，K/γ 效应可能被 Simpson 悖论解释。
- - Major: K=6 expanded pilot 仅 300 cells，且未说明是否与主样本 2,700 cells 使用相同 episodes/seeds/模型，无法作为 K 扩展趋势的可比证据；P/B 的 “5–10×”与“median 10.88×”口径也未交代。
### Minor（2）
- - Minor: c0 只在 K=3 的少数 γ 水平上拟合，B 的指数函数形式缺乏理论约束，未做参数敏感性、模型选择或严格样本外验证。
- - Minor: P、B、ρ 均未报告标准误或聚类稳健区间，10 seeds 是否被当作独立样本不明确，可能高估精度。

## 统计（stat）— ok
### Critical（2）
- - Critical: 将 270 episodes × 10 seeds 当作 2,700 个独立“cells”，忽略同一 episode 在多个 seeds/settings 间的相关性，有效样本量被严重高估。
- - Critical: c0 是在 K=3 pilot 上拟合的，随后又在同一数据集（尤其 K=3 的 cells）上宣称 P>B 并计算 tightness，属于样本内验证/过拟合，不能作为独立下界证据。
### Major（4）
- - Major: 用 Wilson CI 报告“0.68% improvement”不合适：Wilson 区间适用于单一比例，不适用于差值/改进量；且 [0.62,0.74] 与 0.68% 量纲不一致，在 2,700/300 规模下精度也不可信。
- - Major: 对核心结论（K=1→2 的 P 上升、P 单调性、P>B、tightness 比值）没有给出任何检验、置信区间或效应量，无法判断是否为抽样噪声。
- - Major: ρ≈0.3 的 ICC 估计未报告置信区间、方差成分或估计方法，而它直接进入 Fisher-like 公式和下界，不确定性未传播。
- - Major: 9 个 cells 的“全部超过 B/中位 tightness”若作为推断性证据，未做多重比较校正；且“5–10×”与“median 10.88×”同时出现，数值自相矛盾。
### Minor（3）
- - Minor: K=6 扩展 pilot 仅报告 P=0.3326 点估计，无 SE/CI，无法评估其与 B 的差异是否显著。
- - Minor: 0/15 的 Wilson 区间并非退化区间；若用“CI degenerate”作为不报告或调整结果的依据，统计理由错误。
- - Minor: 方差报告措辞不一致：“inverse variance decreases”与 I(K) 随 K 增加而增加矛盾，应统一为方差下降/逆方差上升。

## 实验（experiment）— ok
### Critical（2）
- - Critical: K=1 对照不是有效的选择性预测对照：单个验证器不存在 disagreement/abstention 的可操作定义，且缺少“非选择性全覆盖率单模型”和“随机弃权”对照，无法把 K 的效应与选择机制本身分离。
- - Critical: 基准不公平：K 个验证器消耗约 K 倍推理/计算，未与同等算力的单模型多次采样、自洽性（self-consistency）、语义熵等非集成不确定性基线对比，P 随 K 增大可能只是算力/采样次数增加造成。
### Major（5）
- - Major: 消融不完整：未分别消融验证器数量、验证器多样性（同模型不同 seed vs 不同模型）、temperature、提示模板、投票/聚合方式及弃权阈值措辞；文中只把 threshold phrasing 列为限制，却没有对应消融实验。
- - Major: 超参数网格过疏且构造有拟合嫌疑：K 只有 3–5（加单点 K=6），γ 只有 0.5/1.0/2.0，不足以支撑 B 中 exp(−γK/10) 的具体函数形式；c0 仅在 K=3 pilot 上拟合，却在同一批 2,700 cells 上宣称“全部超过 B”，没有留出或折外验证。
- - Major: seed 管理不透明：未说明 10 个 seed 随机化的是 episode 采样、生成器还是验证器，主结果缺少 per-cell 的 seed 级误差条；seed 42 的单生成器结果只用 seed 42–44 三个值做 pooled SD hedging，样本过小且是事后选择。
- - Major: 泛化证据不足：只有 4 个本地模型且任务/数据集未明确，没有跨模型、跨任务、跨阈值措辞的 held-out 验证；K=6 只是单个 expanded pilot 点，不能证明 B(K,γ) 在 K≥6 或未见模型上成立。
- - Major: 统计量使用不当：Wilson CI 用于“0.68% improvement”而非比例本身，[0.62,0.74] 没有反映 4 模型/9 cell/10 seed 的分层随机效应；主表 P 的区间也未按 seed/模型报告。
### Minor（1）
- - Minor: 数值报告内部不一致：P/B 写为 5–10× 但中位数又报 10.88×，若不说明该中位数包含 K=6 扩展 pilot，读者无法复现该统计量。

## 新颖性（novelty）— ok
### Critical（1）
- - Critical: 声称的 GAP 不真实：选择性集成与拒识的关系并非未被刻画，Black et al. (ICLR 2022, *Selective Ensembles for Consistent Predictions*) 已对 n、置信/α 阈值、拒识率和 accuracy-rejection 曲线做理论与实证分析，self-consistency/majority voting 的采样数 scaling 也有大量工作；把 GAP 窄化为“local models + K×γ grid”只是换模型和超参，不是新问题。
### Major（4）
- - Critical: 声称的 GAP 不真实：选择性集成与拒识的关系并非未被刻画，Black et al. (ICLR 2022, *Selective Ensembles for Consistent Predictions*) 已对 n、置信/α 阈值、拒识率和 accuracy-rejection 曲线做理论与实证分析，self-consistency/majority voting 的采样数 scaling 也有大量工作；把 GAP 窄化为“local models + K×γ grid”只是换模型和超参，不是新问题。
- - Major: 贡献 2 中的 Fisher-like 信息公式是标准统计结果：等相关变量均值方差为 σ²(ρ+(1−ρ)/K)，其倒数随 K 增加并趋于相关下界是教科书结论，称为“lemma”并声称“纠正常见直觉”明显夸大增量贡献。
- - Major: 下界 B(K,γ) 是无理论依据的任意拟合曲线（c0 和 exp(−γK/10) 均为人工设定），只在 K=3 pilot 上拟合且未做独立验证；P/B 达 5–10×、中位 10.88× 说明它过于松散、几乎没有刻画或预测力，不足以作为独立贡献。
- - Major: 贡献与经验结果存在内部张力：P 从 K=1 的 0.08、K=2 的 0.11 升到 K=6 的 0.33，而 B 随 K 指数下降，若 P=Rsel·Cmin 增大代表可靠性下降，则“Cmin 单调非降/信息增加”并未桥接到“选择性可靠性随 K 改善”，结论被夸大或缺少关键理论连接。
### Minor（2）
- - Minor: “形式化模型/定义”基本沿用 El-Yaniv & Wiener (2010) 和 Geifman & El-Yaniv (2019) 的标准 selective prediction 记号，只是重命名，未提供新的 formalism。
- - Minor: ρ≈0.3 仅是对四个本地模型样本的 ICC 估计，未证明跨模型族、任务、温度和投票规则稳定，却支撑“correlation floor”的缩放叙述，外推性不足。

## 可复现（repro）— ok
### Critical（3）
- - Critical: 全文没有提供代码仓库、数据文件、模型版本或一键复现脚本，任何数字都无法独立重跑。
- - Critical: 证据链中样本口径自相矛盾：「2,700 cells / 270 episodes × 10 seeds」究竟是每个 local model 各 2,700，还是四个 model 合计 2,700？且 K×γ×episode×seed 是否为独立单元未定义。
- - Critical: `c0` 在 K=3 pilot 拟合，而主实验又包含 K=3 并报告 P/B；未说明 pilot 与主样本是否 disjoint，存在 in-sample fitting 和评估泄漏风险。
### Major（9）
- - Major: seed 报告不完整：仅出现「10 seeds」「seed 42」「seeds 42–44」，没有完整种子列表、各 model/任务/setting 的种子映射，也没有 RNG 初始化方式。
- - Major: 配置快照缺失：未给出 temperature、top-p、量化、prompt 模板、γ 的具体措辞、verifier 投票聚合方式等关键超参数，`gamma=scale*(1+rho)` 不足以复现。
- - Major: 数据许可与来源不清：未说明四个 local model、任务数据集、生成 episodes 的 license、使用条款、再分发权限或数据版本。
- - Major: 哈希对账完全缺失：没有对原始数据、模型权重、生成输出、ledger/table 或最终数值做 checksum/hash 核验。
- - Major: 统计数字不一致：正文称 P/B 为 5–10×，但 median 10.88× 超出该区间；同一指标在不同位置口径不一致，无法对账。
- - Major: K=6 expanded pilot 仅给 300 cells 和 P=0.3326，未说明其 episode/seed/K/γ/model 拆分、是否重拟 c0、CI 与复现命令。
- - Major: 「single-generator seed 42」却用「seeds 42–44 pooled SD 0.026」对冲；单一 seed 不可能产生三个 seed 的 SD，证据链前后冲突。
- - Major: 95% Wilson CI [0.62,0.74] 没有给出分子分母、样本量、四个 model 分层计数和效应定义，无法校验 0.68% 的构造。
- - Major: 「Gates 9/9 checklist 锚定 L401–L409」只给行号引用，未附带附录内容或版本文本，行号锚点不可验证、不可复现。
### Minor（2）
- - Minor: 「four local models」没有命名或注明版本/镜像，无法判断结果是否受特定权重文件影响。
- - Minor: ρ≈0.3 via ICC 缺少计算公式、软件、数据范围和置信区间，ICC 估计不可复现。

## 写作（writing）— ok
### Critical（2）
- - Critical: 摘要中 “P/B 5–10× for γ∈{0.5,1.0}” 与 “median 10.88× across the 9 cells” 直接冲突；即使 γ=2 的细胞点更高，9 个点里至少 6 个落在 5–10，中位数不可能超过 10。
- - Critical: 摘要和贡献列表写 “inverse variance decreases (Fisher-like) I(K) ... (Fisher-like information increases)”，方差下降时逆方差/信息量应上升，同一句内术语自相矛盾。
### Major（5）
- - Major: 引言末尾突然插入 “P0 26-block F1 24K→12K”“Panorama 6-figure set”“Ledger 86 PASS”“Gates 9/9 L401–L409” 等未定义内容，与 K-verifier ensemble 和 selective prediction 完全脱节，疑似串稿并严重破坏结构。
- - Major: 摘要先说 P 随 K 从 K=1 到 K≥3 增大，又说 “K-Verifier ensemble improvement 0.68%”，但未定义 improvement 是哪个指标、P 是越低越好还是越高越好，导致结论方向矛盾。
- - Major: “P/B 5–10×, median 10.88× after expansion” 与前面的 9-cell 中位数口径不一致，且未说明 “after expansion” 后中位数基于多少、哪些 cell，数字证据无法复核。
- - Major: 摘要中 “The K-Verifier ensemble improvement ... to avoid contradiction with the survey 0/15 zero-success case where CI is degenerate” 缺乏上下文，0/15、Wilson CI、survey 均未定义；报告 CI 不能“避免矛盾”，只会暴露不确定性。
- - Major: 正文/摘要没有规范的图、表编号和正文引用；“Panorama 6-figure set”和 “Ledger table”以未编号描述出现，读者无法定位支撑 P/B 或 86 PASS 的图表证据。
### Minor（3）
- - Minor: “cells”“episodes”“seeds”混用：2,700 cells 写成 270 episodes ×10 seeds，300 cells 又像是 30×10，术语不统一。
- - Minor: “A K=6 expanded pilot (300 cells, P=0.3326) gives P=0.33” 先给精确值再冗余重复约值，且精度不一致。
- - Minor: 摘要公式中 Δp、σ²、Rsel、Cmin 等符号首次出现时未定义，公式无法独立理解。

## 伦理（ethics）— ok
### Critical（1）
- - Critical: 数据许可与来源不明：论文未披露四个本地模型、任务、数据集的具体名称及许可证，无法核实数据/模型使用权是否合规；若涉及受版权、服务条款或非商业许可保护的内容，评测本身即可能构成侵权。
### Major（4）
- - Major: 隐私与人类受试者合规缺失：文中出现 “survey 0/15 zero-success case”，若该 survey 涉及人类参与者，则缺少 IRB 审批、知情同意、数据去标识化与存储说明；若来自用户数据，也未说明隐私合规机制。
- - Major: 双盲合规风险：匿名投稿却保留 “P0 26-block F1 24K→12K”“Ledger 86 PASS”“Gamma string gamma=scale*(1+rho)” 及附录行号等内部项目/仓库级标识，可能通过独有设计、补充材料或代码库路径暴露作者身份，破坏 double-blind。
- - Major: 利益冲突未披露：论文未声明作者、资助方与四款本地模型及其提供商/开发者是否存在雇佣、商业或研发合作关系；若为自家模型参与评测，未披露即构成实质性 COI。
- - Major: 误用风险警示不足：下界 B(K,γ) 仅由 K=3 试点数据拟合且是样本描述性构造，但摘要与正文的表述仍可能被读者误读为理论安全界限，存在被部署到医疗、金融等高风险选择性预测场景的误用风险。
### Minor（1）
- - Minor: 选择性报告风险：K=1/2 已显示 P 上升、K=6 为单点观测，但论文未系统说明哪些任务/模型/阈值组合下该模式会失效，也未提供 “survey 0/15 zero-success case” 的原始材料与许可说明，可能掩盖不利于结论的证据。

## 汇总

- **Critical: 13 | Major: 36 | Minor: 14**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）