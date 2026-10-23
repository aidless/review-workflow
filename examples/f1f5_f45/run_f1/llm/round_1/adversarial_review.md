# 对抗审查报告

- 时间: 2026-08-27T19:01:00.241425+00:00
- 源: F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f1\extracted_text.txt
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（3）
- - Critical: 主要因果结论的统计单元混乱：报告的是 Qwen3:4b 单模型/单通道的 Wilcoxon 结果，却把 4 模型×3 通道×500 题=6000 对称为总体证据；若把全部 cells 当作独立样本，则同一题目跨模型、同一模型跨通道的重复测量会造成伪重复，Wilcoxon 的独立同分布假设不成立。
- - Critical: 存在未校正的多重比较与选择性报告风险：从 4 个模型和 3 个通道中挑出最显著的 Qwen3:4b 结果作为主发现，未报告全部 12 组检验或进行多重比较校正，p=1.6×10⁻⁵ 不能单独支持“instruction channel”的总体效应。
- - Critical: 混淆变量未排除，语义归因不成立：confidence-priming 与 length-matched neutral 的差异不只有“置信提示”，还可能有指令语气、肯定性/情感效价、行为要求、句法主题等；单一对照无法把效应归因于“confidence priming 的语义内容”，需要用多类安慰剂条件（如无置信指令的积极内容、不同措辞的相同指令）分离。
### Major（7）
- - Major: 配对设计缺少随机化/顺序平衡报告：若每个模型先看 benign 再看 priming，或固定通道顺序，则顺序效应、疲劳、跨条件污染都可能混入差异；未报告条件顺序是否 counterbalance。
- - Major: 长度对照只在一个子集上检验，主效应和对照效应不可直接比较：主效应来自全样本，control 来自子集；∆MAE 差异可能来自子集抽样差异而非“长度 vs 语义”。
- - Major: 结果变量 MAE 不是校准/ECE：对二元正确性取 |confidence−correctness| 是线性分数，混合了校准、锐度与基础正确率；因此“calibration shift”这一前提性结论未被该指标直接支持。
- - Major: power analysis 与检验方法不匹配：MDE dz=0.18 基于配对参数检验思路，但推断使用 Wilcoxon；非参数功效、所需样本量和效应量解释不同，且未说明实际分析单元是 500 题还是 6000 对。
- - Major: 后验基线检验逻辑不当：baseline 只在 held-out benign 数据上拟合，再检验 priming 条件是否仍偏移，只能说明“benign 拟合的校准器不迁移”，不能说明“校准无法消除条件效应”；四个基线还缺少多重比较校正和完整选择标准。
- - Major: 模型/题目抽样前提不透明：500 道 MMLU 题如何从全集选出、是否随机/分层未说明；4 个“small local models”的选择标准也未给出，限制了内部可比性和外部推广。
- - Major: 种子数 3 且作用不明：若 3 seeds 只是打乱顺序，没有覆盖模型解码或题目抽样的随机变异；未报告嵌套/混合效应模型，无法区分题目、模型、通道与条件效应。
### Minor（2）
- - Minor: 3 种 phrasing 的补充 pilot 只报告平均 confidence（0.645/0.646/0.649），未报告 ΔMAE、检验或效应量，“方向一致”不能作为泛化证据。
- - Minor: 前提与现实任务不对齐：真实 RAG/cache entry 很少是显式“answer with high confidence”的指令，多为检索文本、demo 或工具输出；实验操纵的生态效度不足。

## 统计（stat）— ok
### Critical（2）
- - Critical: 主发现是从 4 个模型族 × 3 个通道的检验矩阵中挑出的单个 Qwen3:4b 结果，未报告预注册或对全部 12 组比较进行多重比较校正；即使 p 值很小，也不能把该事后选择结果表述为普遍成立的“instruction channel”效应。
- - Critical: 将长度匹配良性对照的 p=0.62 解读为“无长度效应”属于 p 值误用：非显著不等于效应为零，且该对照只在子集上检验；应报告等效性检验或置信区间来判断长度是否可排除。
### Major（4）
- - Major: 效应量报告不完整：仅给出 dz=0.42 和点估计 ΔMAE=+0.047，未报告 dz 的置信区间；从多个组合中挑出的效应量还会因选择偏差而被高估。
- - Major: 方差与不确定性报告不足：摘要声称使用 B=5000 BCa bootstrap，但未报告 ΔMAE 的 bootstrap 置信区间、配对差分的 SD/分布或 Wilcoxon 检验的效应量 CI，读者无法判断估计精度。
- - Major: 样本量/独立性界定不清：12,000 cells / 6,000 paired differences 中包含同一批 500 题跨模型、跨通道重复使用，若未按问题、模型或种子进行聚类/随机效应处理，有效样本量可能被高估；3 个种子也应说明是合并还是仅作复现。
- - Major: 四个事后 baseline 均报告 p<.02，但未进行多重校正，且“reduce but not eliminate”只用显著性检验，无法支持“仍存在残余偏移”的结论；应改用非劣效/等价检验并报告校正后置信区间。
### Minor（2）
- - Minor: 配对差分是逐题绝对误差，可能有界且呈离散分布，Wilcoxon signed-rank 会受大量 ties 影响；未说明 tie 处理或连续性校正。
- - Minor: 功效分析声称 MDE dz=0.18 at n=500，但实际检验是 Wilcoxon 且存在多个比较；若按校正后显著性水平或 Wilcoxon 效率计算，功效可能不足。

## 实验（experiment）— ok
### Critical（2）
- - Critical: 长度匹配良性对照只在子集上测试，未覆盖主效应所在的全量 500×4×3 配对数据，因此“语义而非长度”的核心结论不能由主实验直接支持。
- - Critical: 对 4 个模型族 ×3 个通道（及 4 个事后基线）进行大量检验却未报告任何多重比较校正，且正文突出 Qwen3:4b 的显著结果，存在选择性报告/假阳性风险。
### Major（7）
- - Major: 缺少“无缓存/无指令”基线，只能比较 benign vs confidence-priming，无法区分“任意缓存条目都会改变置信度”与“置信度 priming 特有影响”。
- - Major: seed 管理不透明：只列出 42/43/44，未说明主统计量是否跨 seed 聚合、是否用 seed 作为随机效应、是否报告 seed-level 方差或最差 seed 结果。
- - Major: 功率分析基于 n=500，但实际 6,000 个配对差值来自同一批问题跨模型/通道复用，未处理问题内相关性，有效样本量与检验功效可能被高估。
- - Major: 解码超参数（temperature、top-p、max tokens、提示模板、答案抽取规则）和四个事后基线超参数未报告，也未说明是否在 benign held-out 上反复调参导致信息泄漏。
- - Major: 消融不完整：仅一个 priming 措辞、一个 75 字符中性前缀，未做语义内容×长度×位置的因子消融，也未明确“3 个通道”的操作化定义与各通道独立消融。
- - Major: 基准公平性不足：未进行 MMLU 数据污染/记忆化检查，未使用时间切分或排除训练重叠题，单基准 MMLU 也限制了公平性评估。
- - Major: 泛化性严重受限：4 个小型本地模型、置信度范围仅 0.52–0.76、单一任务和单一 priming 表述，缺乏真实 RAG/缓存注入场景，无法支撑广泛部署结论。
### Minor（2）
- - Minor: 细胞数表述不一致：12,000 cells 是否已包含 3 seeds 未说明；若 12,000 为单 seed，则总评估量应为 36,000，报告需澄清。
- - Minor: 补充 500×3 phrasings pilot 只列平均置信度 0.645/0.646/0.649，未给出差异检验、效应量或 seed 信息，证据强度不足以作为“方向一致”支撑。

## 新颖性（novelty）— ok
### Critical（1）
- - Critical: GAP 不真实：既有工作已直接证明显式“confident/cautious”式指令可方向性改变 LLM 的 verbalized confidence（如 SteerConf, arXiv:2503.02863），且输入中 trigger/perturbation/jailbreak 可操纵不确定性或 confidence（Uncertainty is Fragile, arXiv:2407.11282；On the Robustness of Verbal Confidence, arXiv:2507.06489）；本文的 cache entry 本质只是 prom
### Major（2）
- - Major: 增量贡献被夸大：将已有“prompt 指令影响置信度”的现象重新包装为“retrieved cache entries”并不能构成机制或理论贡献；第 1、2 条贡献主要是实验协议细节（paired ΔMAE、length control、Wasserstein sanity check），而第 2 条明确承认是 sanity check 而非 explanatory theory，不足以支撑“novel contribution”的定位。
- - Major: 与更近的 agent-memory / RAG-calibration 文献差异未做实：memory consolidation 可制造 agent 自信断言（Manufactured Confidence, arXiv:2606.29279），RAG 噪声上下文会加剧 overconfidence（NOVA, arXiv:2601.11004），memory poisoning 可使检索到的缓存内容影响后续行为；本文没有说明为何这些已有机制无法涵盖其结论，而只以“未在 MMLU + 长度控制下测 paired ΔMAE”这种极窄口径宣称空白，属于程序性而非概念性 GAP。
### Minor（2）
- - Minor: 结果仅来自 4 个小模型、单一 priming 措辞、单一基准（MMLU）和极小效应量（ΔMAE=+0.047, 仅 Qwen3:4b 报告显著），在该范围内更像是已知 prompt sensitivity 的补充性复制，而非足以改变领域认知的增量发现。
- - Minor: 四条 post-hoc baselines“减少但不消除 shift”对应的是校准方法无法消除输入级操纵这一已知现象，作为贡献 3 说服力有限；若不能展示 cache-specific 的差异化后果或防御基线，其增量仍停在“提示词可以影响置信度”的老结论上。

## 可复现（repro）— ok
### Critical（3）
- - Critical: 全文未提供代码仓库、数据仓库或任何复现入口，12,000 cells 的完整实验无法从匿名材料独立重跑。
- - Critical: 证据链断裂：MMLU 的确切版本、科目子集、500 题采样方式、缓存条目构造位置均未说明，也没有从原始数据→预处理→推理→评估→bootstrap 的中间产物清单。
- - Critical: 模型配置快照缺失：仅写 “4 local model families / Qwen3:4b”，没有精确 checkpoint/模型 ID、量化方式、推理框架、温度、采样策略、max tokens、dtype、确定性开关等，无法复现同一模型输出。
### Major（6）
- - Major: seed 作用域不清：42/43/44 只给出数字，未说明用于题目采样、prompt 顺序、模型解码、bootstrap 还是全部；也未报告每个 seed 的独立结果。
- - Major: 3 channels 与 2 cache conditions 的完整模板未给出；benign control 的 75-char 前缀具体文本、插入位置、分隔符和角色（system/user）均缺失。
- - Major: 无哈希对账：缺少 MMLU 数据、prompt 模板、代码、原始模型输出和聚合结果文件的 SHA-256 或等价校验和，无法核对 0.047、p=1.6×10⁻⁵、dz=0.42 等关键数字。
- - Major: 数据许可未声明：MMLU 的许可条款、数据集版本/镜像、以及缓存条目和中间输出再分发许可均未交代。
- - Major: 四个 post-hoc baselines 不可复现：held-out benign split 的划分方式、拟合实现、库版本、超参数和拟合代码均未给出，且未报告 baseline 后的置信区间。
- - Major: 无一键复现配置：缺少 Dockerfile、environment.yml、pip/conda lock、CLI/Makefile、GPU/内存需求说明，无法做到 one-click reproduce。
### Minor（2）
- - Minor: BCa bootstrap 统计细节不足：未说明使用 Python/R 具体函数、bias-correction 实现、B=5000 的随机数流如何由三个 seed 控制，以及 Wilcoxon 的 ties/近似处理方式。
- - Minor: 辅助 pilot（500×3 phrasings）仅报告 0.645/0.646/0.649 均值，未给出三条 phrasings 的完整文本、数据文件和对应哈希。

## 写作（writing）— ok
### Critical（1）
- - Critical: 摘要称 12,000 cells/6,000 paired differences，却又说 power 为 MDE dz=0.18 at n=500；文中未说明 n 是问题数、配对差数还是模型内样本量，导致 Wilcoxon、dz 和 bootstrap 的统计单位无法核对。
### Major（5）
- - Major: 摘要把“benign vs confidence-priming”列为 2 cache conditions，再单独引入“length-matched benign control”并注明 tested on a subset；Contributions 却把该控制写成主协议的一部分，未保留 subset 限定，摘要与正文矛盾。
- - Major: 摘要 headline 只点名 Qwen3:4b 的 ∆MAE=+0.047，但设计声明覆盖 4 local model families ×12,000 cells；未说明该结果是单模型报告还是跨模型汇总，读者无法判断摘要是否过度概括。
- - Major: “3 channels”在摘要/引言中从未定义，结果中又出现“instruction channel”；channel 的含义（置信度呈现通道、缓存通道还是注入通道）不明确，破坏结构可读性。
- - Major: 关键术语缩略语不一致：摘要直接用 ∆MAE 而不展开 Mean Absolute Error，引言使用 ECE 但未定义，且 verbalized-confidence error/MAE/ECE 混用。
- - Major: “descriptive Wasserstein upper bound (|∆MAE| ≤ LΓ)”中的 LΓ 和 Γ 未定义，读者无法判断这是 Lipschitz 常数、分布距离上界还是经验量，公式缺乏上下文。
### Minor（7）
- - Minor: 摘要写 “4 local model families”，Limitations 写 “4 small local models”，family 与 model 混用。
- - Minor: 摘要中 “0.645/0.646/0.649 conf” 使用非正式缩写 conf，未说明是 confidence 还是 confidence score，与正式摘要文体不符。
- - Minor: “3 seeds (42/43/44)” 未说明 12,000 cells 是每 seed 一次还是三 seed 汇总；若重复三次，总数/配对差异数应另行说明。
- - Minor: 四个 post-hoc baselines 只给 p<.02 的聚合界，未逐一报告效应量、方向和检验，且把 temperature scaling 等校准方法称为 baselines，术语不准确。
- - Minor: 全文唯一图引用是摘要中的 “see Fig. 1”，但正文与贡献未给出对应图注或结果表；图表现无法支撑摘要中的数字。
- - Minor: Related Work 中 “Naeini et al. (2015) derive the Brier score” 将 Brier score 的提出归于 Naeini 等人而非 Brier（1950），参考文献表述有误。
- - Minor: “Under review as submission to TMLR” 在标题区和 Contributions 后重复出现，疑似页眉/排版残留。

## 伦理（ethics）— ok
### Major（1）
- - Major: 误用风险：论文演示了通过缓存条目操纵模型口头置信度并以医疗 RAG 为动机示例，但可见文本未讨论该发现的 dual-use 风险、缓存投毒/提示注入攻击场景或缓解措施；该结果可能被用于让高风险输出显得过度可信。
### Minor（4）
- - Minor: 数据许可：MMLU 本身为 MIT 许可，但可见文本未明确标注数据集版本、原始引用或许可声明；若作者发布 500 题子集或复现脚本，需随附 MIT 许可并确认 Qwen 等模型权重的许可条款合规。
- - Minor: 隐私：实验看似只使用公开 MMLU 与本地模型，但未在数据可用性部分明确声明“不涉及个人/患者数据”；医疗 RAG 示例容易让读者误以为涉及临床数据，应写明数据边界与无需 IRB 的理由。
- - Minor: 双盲：当前标题与作者匿名形式合规，未发现明显违规；但需确认补充材料、URL、模型仓库或日志中不含可识别作者/机构的元数据（如私有 wandb、Hugging Face 或机构链接）。
- - Minor: 利益冲突：未披露资助、模型供应商或基准数据集相关利益；若作者与 Qwen/阿里等模型提供方存在雇佣、资助或合作关联，应按 TMLR 要求申报。

## 汇总

- **Critical: 12 | Major: 32 | Minor: 21**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）