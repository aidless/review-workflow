# 对抗审查报告

- 时间: 2026-08-27T18:13:04.343808+00:00
- 源: F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f45\extracted_text.txt
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（2）
- - Critical: 主结论中的 hybrid 规则是在同一 128K cells 上“derived”又在该数据上评估，属于样本内验证；其 McNemar p 值未考虑规则选择/阈值搜索条件，不能作为确认性证据。
- - Critical: 从 16,000 个样本观察到 c=0 只能说明“该样本中未出现输给 majority 的 trial”，不能推出“在该 regime 内 never loses”；除非给出解析证明，否则这是有限样本结果被过度一般化。
### Major（7）
- - Critical: 从 16,000 个样本观察到 c=0 只能说明“该样本中未出现输给 majority 的 trial”，不能推出“在该 regime 内 never loses”；除非给出解析证明，否则这是有限样本结果被过度一般化。
- - Major: 实验固定 N=7、f=2、pH=0.65 且只变化两种 capture strategy，而 sign-flip 最可能出现于 capture 接近半数、honest confidence 信息量弱或校准差等边界；当前设计无法排除这些混淆，且“within studied regime”是事后收窄假设。
- - Major: honest confidence 的“信息性”是合成数据生成时写入的属性，而非被操纵的自变量；real-LLM pilot 又显示 verbalized confidence 无信息（0.985 vs 0.985），因此主结论对真实 verifier 的前提不成立，也未做置信度随机化/去信息化的反事实对照。
- - Major: “mimicry”被操作化为 captured verifiers anti-correlate confidence with correctness，这本身仍使其可区分，与“模仿诚实、不可区分”的构念不一致；因此 mimicry 条件下的结果未必检验了原假设所说的伤害机制。
- - Major: 机制解释（正确 honest 高权重、错误 honest 低权重等）是事后叙述，未通过消融、中介或反事实分析证明该机制是优势来源，而不是由投票计数、置信度分布参数或 capture 模型共同决定的伪影。
- - Major: “4 model families”的独立性未说明；若它们共享 trial/ground truth 或只是同一批数据的不同变换，则 16,000 per cell 并非独立样本，McNemar 的样本量和 p 值会被虚增。
- - Major: 对 trust_mean、trimmed_mean、hybrid 等多个规则在同一数据上分别报告极显著 p 值，未做多重比较校正；F4/F5 的主/次分析划分也可能是事后选择，增加 researcher degrees of freedom。
### Minor（2）
- - Minor: 仅使用 seed 42 单一种子、未报告跨种子变异或置信区间，难以判断结果对随机数生成和模拟参数扰动的稳定性。
- - Minor: real-LLM pilot 数据存在内部不一致（“400 trials”与“3991/4000 parse”），且 400 trial 中 uninformative confidence 下仍出现 c=0 的含义未解释。

## 统计（stat）— ok
### Critical（2）
- - Critical: 混合投票的 McNemar 数字与所报准确率不自洽：注入下 0.620 vs 0.435 若 c=0，则 b≈2960，不是 b≈1600；模仿下 0.790 vs 0.732 若 c=0，则 b≈928，且其精确 p≈10^-279，不可能小于 10^-400。
- - Critical: 自适应混合规则是在同一 128K cells 上“derive”后再在同一批数据上检验并报告 p 值，属于样本内选择/循环验证；该规则的准确率和 McNemar p 值不能作为独立证据。
### Major（5）
- - Major: 4 个 model families × 4,000 trials 被合并成 16,000 个“独立”配对单元做 McNemar，未处理 family 或 trial 的聚类/重复测量结构，可能严重夸大有效样本量和检验精度。
- - Major: 全部结论基于 seed 42 的单次模拟实现，没有跨多个随机种子或 bootstrap 的变异性报告；单一 regime 内的“falsify”缺乏对模拟噪声的稳健性证据。
- - Major: 只报告点估计和原始百分比差值，没有置信区间、标准差/标准误、Cohen’s h 或风险差别的精确 CI；效应量未量化，且 c=0 导致 OR 无穷时不作解释。
- - Major: 真实 LLM pilot 的样本量表述矛盾：“400 trials”与“3991/4000 honest parse（99.78%）”不一致；同时以两个均值 0.985 vs 0.985 宣称“uninformative”但没有方差/置信区间/效用分析。
- - Minor: 对两种策略、多个规则（trust_mean、trimmed mean、hybrid、majority）作了多组 McNemar 检验，未做多重比较校正或预注册；虽然此次 p 极小，但方法上仍需说明。
### Minor（3）
- - Minor: 对两种策略、多个规则（trust_mean、trimmed mean、hybrid、majority）作了多组 McNemar 检验，未做多重比较校正或预注册；虽然此次 p 极小，但方法上仍需说明。
- - Minor: 对“sign flip”的证伪仅依赖两个方向的单独配对检验，未报告策略×投票规则的交互项或 difference-in-differences 的置信区间；应明确给出 Δ 差异的不确定性。
- - Minor: 仅报告单一 (N=7, f=2, pH=0.65) 参数点，未做 f/N 或 pH 敏感性分析；虽然文中有限定“studied regime”，但统计外推能力仍然有限。

## 实验（experiment）— ok
### Critical（2）
- - Critical: 混合规则在同一个 128K cells 上既被用于定义/选择（threshold 0.5）又被用于评估，没有 held-out 或交叉验证，属于同数据双重 dipping，hybrid 的增益不能作为有效泛化证据。
- - Critical: 全部合成数据仅用 seed 42 生成，c=0、Δ、McNemar p 都是单一种子下的结果，缺乏 multiple seeds 或 bootstrap CI，无法排除种子依赖和偶然性。
### Major（5）
- - Major: 缺少关键对照组：没有 f=0 无捕获、置信度无信息/反相关、以及随机权重或不使用权重的对照，无法把优势归因于“置信度信息性”或 trust weighting 本身。
- - Major: 消融不完整：hybrid 没有与 trust_mean、trimmed_mean 进行统计比较；实际结果中 hybrid 在 injection 下低于 trimmed_mean、在 mimicry 下低于 trust_mean，不能支持“混合更好”的结论。
- - Major: 超参数与泛化面过窄：仅 N=7、f=2、pH=0.65 和两种 capture 策略，未扫描 N/f/pH、置信度校准/噪声/相关结构、trim 参数或阈值，所谓“studied regime”实际只是一个参数点。
- - Major: real-LLM pilot 只有 400 trials、单一模型 gemma3:4b、且置信度被报告为无信息，没有功效分析、CI 或与合成条件的正式对比，不能作为现实泛化或 sign-flip 检验依据。
- - Minor: “4 model families”未具体说明，也未报告每个 family 的分层结果，pooled 结果可能掩盖某个 family 内 trust weighting 劣于 majority 的情况。
### Minor（2）
- - Minor: “4 model families”未具体说明，也未报告每个 family 的分层结果，pooled 结果可能掩盖某个 family 内 trust weighting 劣于 majority 的情况。
- - Minor: 以“no new data”作为 hybrid 分析的辩护反而暴露数据重用；阈值和组合方式应预先注册或在独立 validation fold 上选择。

## 新颖性（novelty）— timeout
### Critical（2）
- - Critical: 所声称的 GAP 不真实：现有鲁棒聚合文献（如 Guo & Kong 2024, arXiv:2403.08222 对 adversarial experts 的最优 truncated mean 分析；Bai et al. 2022 对 weighted majority voting 的 trust 不稳定性分析）已覆盖“固定被俘获/对抗专家数量、任意报告策略、是否需要鲁棒聚合”的核心问题，本文只在更窄的合成设定下重述其经验后果，未证明自己的问题空间是空白。
- - Critical: “sign-flip hypothesis” 不是从文献中确立的公开主张，更像论文自造的 strawman；没有证据表明先前工作断言“injection 下 trust weighting 必好、mimicry 下必坏”，因此用一个单点合成实验“falsify”它并非对既有科学争论的实质贡献。
### Major（4）
- - Critical: 所声称的 GAP 不真实：现有鲁棒聚合文献（如 Guo & Kong 2024, arXiv:2403.08222 对 adversarial experts 的最优 truncated mean 分析；Bai et al. 2022 对 weighted majority voting 的 trust 不稳定性分析）已覆盖“固定被俘获/对抗专家数量、任意报告策略、是否需要鲁棒聚合”的核心问题，本文只在更窄的合成设定下重述其经验后果，未证明自己的问题空间是空白。
- - Major: 核心结论被夸大：所谓“no sign flip”只在单一参数格点 (N=7, f=2, pH=0.65) 加两种 capture 策略下成立，没有对 f/N、N、pH、置信度校准强度或真实模型族做扫描，不能支持标题中 “when confidence is informative” 的一般化表述；大量 trials 只是重复而非探索假设空间。
- - Major: 增量贡献很薄：trust-weighted mean 和 trimmed mean 都是已知聚合器，hybrid 只是两者在 0.5 阈值处的简单平均，且是在同一 128K cells 上事后选取和评估的（“derived on the same 128K cells, no new data”），没有独立验证、理论刻画或搜索如何选择该混合权重，无法支撑其作为新方法的贡献。
- - Major: 唯一的真实 LLM pilot 反而削弱了 GAP：verbalized confidence 0.985 vs 0.985 说明真实 LLM 置信度不具备论文所需的信息性，因此该研究 regime 在现实 verifier pipeline 中未必存在；论文既没有建立从合成信息性假设到实际部署的桥梁，也未展示该问题在实践中的紧迫性。
### Minor（1）
- - Minor: 论文给出的解释（诚实者占多数且置信度有信息量，所以加权只会更好）本质上是 Condorcet/加权多数最优性的直接推论，没有提供超越已知理论的非显然机制，作为“novel finding”的增量很小。

## 可复现（repro）— ok
### Critical（3）
- - Critical: 全文没有给出代码/数据仓库地址、artifact DOI 或补充材料链接；`cells.jsonl` 和 `real_llm_400_v6` 只有名字，读者无法获取原始数据，证据链断裂，谈不上“data are shared honestly”。
- - Critical: 摘要只给出截断 SHA（`6c375b43`、`798bbc2d`），既无完整 SHA-256，也无规范化说明（JSON 键序、行序、浮点格式、哈希对象），无法执行“重跑→重算哈希→对账”这一可复现性核心步骤。
- - Critical: 没有配置快照：4 个 model families、2 种 capture strategies 的具体生成算法、置信度分布、trim 方式、“thresholded at 0.5”的作用对象与阈值选择过程均未完整定义，第三方无法唯一复现 0.548/0.435 等数字。
### Major（3）
- - Major: 只报告 `seed 42`，但未报告各 trial/model family/strategy 的 RNG 实例、numpy/torch/random 版本、采样参数、批处理顺序；单一种子也不足以说明结论对随机种子的稳健性。
- - Major: 数据许可不明确：未声明 `cells.jsonl` 和 LLM 输出的 license，也未说明 gemma3:4b 的具体权重版本、quantization、prompt 模板与 Ollama 配置，涉及再分发和衍生复现的合法性/可复现性。
- - Major: 统计对账信息不完整：McNemar 只给 `b`、`c` 和数量级 p 值，未提供完整列联表、精确 p 值计算脚本及数据行级核对方法；且 `3991/4000` 与 `99.78%` 的对应关系表述含糊，难以独立核验。
### Minor（2）
- - Minor: 没有一键复现入口：无 Dockerfile/requirements.txt/Makefile/单条命令，也没有说明 gemma3:4b 的获取方式、解析脚本和运行时长，无法一键重现实验。
- - Minor: 摘要声称 F4 为主分析、F5 在同一 128K cells 上 derived，未说明超参数/规则选择是否在同一数据上造成选择泄露，也未提供 pre-registration 或 holdout 对账，削弱证据链可信度。

## 写作（writing）— ok
### Critical（1）
- - Critical: 摘要内部数字矛盾：real-LLM pilot 前写 “400 trials”，后文却是 “3991/4000 honest parse 99.78% is_real”，99.78% 对应 4000 而非 400，读者无法确定真实样本量。
### Major（4）
- - Major: 摘要先说 “All results are synthetic”，又在同一段报告 “Supplementary real-LLM pilot”，二者直接矛盾；应明确为 “All primary/main results are synthetic” 或将 pilot 排除在 “results” 之外。
- - Major: F4/F5 是无定义标签，摘要既未说明它们是图、表还是 finding，也没有对应图表或正文解释，导致结构引用悬空。
- - Major: hybrid 定义有语法歧义：“mean of trust_mean and trimmed mean thresholded at 0.5” 可被读成“先取两者均值再阈值化”或“分别阈值化后再取平均”；同时 “derived on the same 128K cells (no new data)” 与 “defined as” 在方法学表述上互相矛盾。
- - Major: 摘要结构失衡：假设、实验设计、多组结果、机制解释、real-LLM pilot 和限制全部挤在一个超长段落中，并混入 trust_mean 等代码式标识符，可读性和可扫读性差。
### Minor（3）
- - Minor: “verbalized conf 0.985 vs 0.985 uninformative” 未说明 0.985 是什么指标（正确/错误平均置信度？AUC？），也未解释两个相等值如何推出 “uninformative”。
- - Minor: 术语不统一：摘要用 trust_mean/hybrid/trimmed mean，引言引入 Atv 后不再使用，正式名称与代码变量混用。
- - Minor: 除 F4/F5 外，正文未见任何图/表编号或说明，读者无法核对 b≈1600、c=0 等关键结果所对应的图表证据。

## 伦理（ethics）— ok
### Major（2）
- - Major: 误用风险：摘要与结论反复强调 “trust-weighted voting never loses to majority / no sign flip”，但实验仅覆盖 N=7、f=2、pH=0.65 和两种 capture 策略，且 real-LLM pilot 已显示真实置信度并不 informative；这种强表述极易被安全关键场景过度泛化、用于部署决策。
- - Major: 研究诚信/F5 同源数据问题：hybrid 分析是在同一 128K cells 上“推导并评估”，属于无独立验证的探索性后验分析，却以 “never loses” 的强结论呈现，可能高估可信度；需明确标注 exploratory 或提供 pre-registration/holdout。
### Minor（4）
- - Minor: 数据许可与溯源：真实 LLM pilot 使用 gemma3:4b，未说明 Gemma 模型许可、模型出处或任何第三方基准/提示数据集的许可情况；补充材料若含模型输出或提示数据需附许可与归属。
- - Minor: 隐私：合成实验本身不涉隐私，但未声明实验提示和任务不包含任何个人数据；若使用任何真实文本、日志或公开基准，应补充去标识化与隐私合规说明。
- - Minor: 利益冲突：正文未见资助来源、算力来源、机构关系或 COI 声明，需在投稿系统/补充材料中披露。
- - Minor: 双盲：表面匿名合规，但需确保补充数据、代码仓库和日志元数据不含作者身份信息（如文件名、路径、ORCID、机构水印），避免审稿期间破盲。

## 汇总

- **Critical: 12 | Major: 30 | Minor: 17**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）