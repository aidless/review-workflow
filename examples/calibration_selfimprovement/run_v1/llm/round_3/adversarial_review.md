# 对抗审查报告

- 时间: 2026-08-27T12:21:19.690712+00:00
- 源: F:\deepseek\papers\calibration-self-improvement\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（3）
- - Critical: 所谓"matcher extended after per-row adjudication of residual errors"得到 100% 准确率/ECEâ0，本质是看到错误后再改标签的事后操作，ground truth 与 matcher 互不独立的假设被破坏，"overconfidence vanishes"是循环论证的人为产物而非发现。
- - Critical: 因果/定量结论（"40â50% high-confidence OOD 答案错误""confidence 与 consistency 负相关则 gating 有效"）基于 N=30（甚至条件子集更小），统计功效极低、置信区间未给出，内部效度不足以支撑任何因果推断。
- - Critical: 论文自陈 27/30 置信度恒为 1.0 致 binning-ECE 不可靠，却同时报告并据以下结论的 ECE=0.363/0.1297/0.0037 正是同一退化分布上算出的，存在自相矛盾的方法论前提。
### Major（4）
- - Major: "ECE 跨域 4Ã/17Ã"为点估计比值，且作者承认 95% CI 极宽、Holm 校正后仅最极端对显著，对重叠且接近零的 CI 取比值不构成有效推断。
- - Major: "self-reported confidence appears uselessâeven harmfulâfor gating"为因果性措辞，但来自无随机化、无反事实的观测性小样本，混淆变量（任务难度、模型族、解码温度、样本选择）未被控制。
- - Major: MSI 从中文自由形式 1.000 降至 MMLU 选择题 0.334 被归因于"protocol"，但语言、题型、判分粒度同时变化，存在多重混淆，无法分离协议效应。
- - Major: Propositions 1â3/8â² 的界依赖 matcher flip rate、FNR/FPR 等量稳定可估的假设，而在 N=30 退化样本上这些量既不稳定也无独立验证，命题适用性前提未成立。
### Minor（3）
- - Minor: "practitioners use them to gate actions â¦ presupposes calibrated probability"作为出发点是断言性前提，未对实际部署行为做测量，外部前提缺实证支撑。
- - Minor: 摘要同时声称"external validity from 600-itemÃ9-model census"与"proof-of-concept pilot N=30 as external-validity demonstration"，且自述 CI 宽、显著性有限，外部效度宣称与自身证据冲突。
- - Minor: "temperature scaling not robust to relabeling"的结论建立在人为事后重标之上，温度缩放失效可能由循环重标导致，因果归因不恰当。

## 统计（stat）— ok
### Critical（3）
- - Critical: 核心结论性数字（准确率 63.3%/86.7%、ECE 0.363/0.1297/0.0037）全部来自 N=30，却未给任何置信区间；在 30 个样本上把 ECE 报到 4 位小数（0.0037）是伪精度——二项 SE 约 9%，ECE 的 SE 同量级或更大。
- - Critical: "跨六域 ECE 变化达 17×" 是用点估计比 0.479/0.0037 算出的，而两者的 CI（[0.30,0.60] vs [0.001,0.08]）宽到比值 CI 几乎无界；效应量（比值）未做误差传播，数值上不可信。
- - Critical: 有效样本量被虚增——"4999 dual-judged pairs"是判官配对观测数，并非独立校准样本；落到每模型每域，ECE 实际仅基于约 600/9/6≈11 个样本，此时 ECE 本质是噪声。
### Major（4）
- - Major: "confidence 与 consistency 负相关（indicative, n=30）"未报告相关系数 r、未报告 CI、未说明用 Pearson 还是 Spearman、未给 p 值，却据此得出结论。
- - Major: "40–50% 高置信 OOD 答案错误"未给分子分母（30 题里有多少属高置信 OOD？）也未给二项 CI；该子样本大概率 <15，CI 宽度 >25 个百分点。
- - Major: 多重比较报告不完整：声称用了 Holm 校正，但比较总数、所用检验、校正后 p 值均未给出，只含糊说"最极端的几对显著"。
- - Major: MSI 以裸点估计给出（1.000、0.334），无 bootstrap CI、无估计方差，却被用于断言"协议依赖性"。
### Minor（2）
- - Minor: 用 "indicative" 对非显著结果打模糊补丁，未明确声明结果在统计上不显著。
- - Minor: 把"均值置信 0.9963 vs 准确率 86.7%"当作过置信信号呈现，却未给该 gap 的检验统计量或 CI；且 27/30 恒为 1.0 使均值几乎无信息。

## 实验（experiment）— ok
### Critical（3）
- - Critical: "100% accuracy (ECE=0.0037)" 的 matcher 是对同一 N=30 样本逐行 adjudication 后扩展得到的，属 in-sample 标签构造，无任何 held-out 验证；该 ECE 本质上是 matcher 对数据过拟合的产物，却被当作"vanishes once semantically-correct answers are recognized"的证据。
- - Critical: 全文未报告任何随机 seed 管理（采样、resample、推理温度）；在 N=30 且分布退化（27/30=1.0）的极端小样本下，"40–50% 高置信 OOD 答案错误""self-consistency removes overconfident OOD answers"等定性结论可能随 seed 翻转，无方差/多 seed 佐证。
- - Critical: OOD-aware gating 的核心结论建立在 n=30 探针上，且"对 confidence 与 consistency 负相关的模型才有效"是 post-hoc 模型子集筛选，存在选择性偏倚；子集规模未给出，无交叉验证。
### Major（4）
- - Major: 三个 matcher 在完全相同的 30 条上递进精修，并非独立 baseline 对照；matcher 间 ECE 差异与标签泄漏混淆，无法归因于"匹配语义"本身。
- - Major: 消融不完整：self-consistency 固定 k=3 resamples，未消融 k；smECE_sem 与 MSI 的各组件（软化温度、语义相似度阈值、MSI 截断点）无消融；binning 方案（等宽/等频/bin 数）未指定。
- - Major: baseline 不公平：仅以 temperature scaling 为对照宣告"not robust to relabeling"，未在相同 matcher 协议下与 isotonic / Platt / beta calibration 等公平比较；ECE vs smECE_sem 也未在相同数据划分上对照。
- - Major: 泛化声明与统计证据矛盾：600-item census 的 95% CI 极宽、Holm 校正后"only the most extreme pairs are significant"，却仍断言"calibration is domain-specific""varies by up to 17×"；"17×""4×"为宽 CI 点估计之比，无比值 CI，误导性强。
### Minor（3）
- - Minor: MMLU 600 项的题目采样程序（分层/随机/子集来源）在可见文本中未说明，难以判断跨域可比性；9 模型、5 家族的具体选型标准未交代。
- - Minor: 各 ECE 点估计未给出 bootstrap 或多 seed 置信区间，仅部分报告 CI，度量口径不一致。
- - Minor: 自一致性"agreement of three resamples"未说明采样温度与是否同 prompt，退化分布下该信号本身的稳定性未验证。

## 新颖性（novelty）— ok
### Critical（1）
- - Critical: 核心 "matcher determines measured calibration" 在本质上是标签噪声/标注质量扭曲校准度量的旧议题（Northcutt et al. 2021 Pervasive Label Errors; label-noise 对 ECE 的影响已有研究），论文未与该文献正面对位，所谓 GAP 部分是虚构的。
### Major（5）
- - Major: 头号 GAP——"self-reported confidence 的校准很少在 agent 自身任务分布上被验证"——被明显夸大：Kadavath et al. 2022、Tian et al. 2023、Lin et al. 2022 等已系统验证 LLM 置信度校准，论文未与之区分增量。
- - Major: "binning-based ECE 不可靠"被当作发现呈现，但这是已确立结论（Nixon et al. 2019; Kumar et al. 2019 Verified Uncertainty Calibration; Roelofs et al. 2022），未与这些工作对比，增量贡献近乎为零。
- - Major: 核心方法贡献（Propositions 1–3、MSI、smECE_sem）只在 N=30 上示意性验证；600 项 census 仅用于描述性 ECE 跨域差异，未用来验证估计器或命题，形式贡献的实证根基薄弱且被高估。
- - Major: OOD-aware gating 结论（"confidence 无用、self-consistency 有效"）复述了 self-consistency（Wang et al. 2022）与基于一致性的幻觉/OOD 检测的既有结果，新颖性不足却以 "pattern worth further study" 包装为核心卖点。
- - Major: 摘要中以 "ECE 跨域变化 4×/17×" 作为量化卖点，但论文自承 95% CI 极宽、仅最极端域对在 Holm 校正后显著——点估计比值被当强度证据，贡献被夸大。
### Minor（3）
- - Minor: "degenerate distribution（27/30 = 1.0）"的饱和置信度现象与已知 overconfident/saturated confidence 一致，未作为已知现象定位，弱化增量。
- - Minor: "temperature scaling 对 relabeling 不稳健"作为发现给出，但 TS 在标签偏移下的脆弱性已有讨论，未引用对比。
- - Minor: keywords 含 "self-improvement" 且引 beyond2025 关于迭代自改进过置信，但本文实际贡献是 matcher 依赖，与自改进无关，关键词/动机借用拉伸了与热点文献的关联以抬高定位。

## 可复现（repro）— ok
### Critical（3）
- - Critical: 全文未披露任何随机种子（N=30、600-item 抽样、self-consistency "three resamples"、bootstrap 95% CI、Holm 校正 p 值），复现者无法对齐同一样本集与重采样轨迹。
- - Critical: "nine models spanning five families" 与 dual-judge（4999/1159 pairs）未给出模型唯一标识/版本/checkpoint/权重哈希，还有 "Chinese free-form set"（MSI 1.000）未命名，模型漂移即无法对账。
- - Critical: 未提供一键复现载体（代码仓库、commit hash、environment.yml/requirements、Docker、运行脚本），abstract 中的数值结论无法被独立验证。
### Major（5）
- - Major: 配置快照缺失——confidence 引出、resample、judge 的 temperature/top-p/max_tokens/exact prompt 均未声明，MSI、smECE_sem 结果高度依赖这些超参数。
- - Major: 数据许可未声明——MMLU（MIT）与未命名中文集的 license、是否可再分发、数据出处/版本 tag 全缺。
- - Major: 无哈希对账——数据集、模型输出、adjudicated labels、judge 配对均朠 SHA256/档案哈希，"4999 dual-judged pairs" 与 "27/30 degenerate" 无法校验未被篡改。
- - Major: "per-row adjudication of residual errors" 无可复现协议（adjudicator 身份、标准、交叉核对、日志），主观判定直接驱动 100% 准确率结论，构成证据链断点。
- - Major: bootstrap CI（如 [0.001,0.08]）未报告重抽次数、种子与区间方法（percentile/BCa），CI 不可复现。
### Minor（2）
- - Minor: "27 of 30 values are exactly 1.0" 未引用 item-level 附录/表，审核者无法逐条对账。
- - Minor: \input{math_commands.tex} 依赖未版本化/哈希，构建环境未快照。

## 写作（writing）— ok
### Critical（2）
- - Critical: 摘要之后、Introduction 之前有一句孤立的「Our central finding is that...」悬浮句，无标题归属，且该句首次引入术语 `smECE_sem`，但摘要正文从未定义该缩写，读者无法对应"semantic soft-label calibration estimator"与 `smECE_sem`。
- - Critical: 摘要篇幅严重超标（约 400+ 词），单段塞入三组 matcher 数据、跨域 census、Proposition 编号、MSI、OOD gating 等至少五条独立结论，结构上应拆分或大幅精简。
### Major（6）
- - Major: ECE 小数位不一致——`0.363`（3 位）与 `0.1297`、`0.0037`（4 位）混用，同一类指标应统一精度。
- - Major: 置信区间精度不一致——`[0.001,0.08]`（左 3 位右 2 位）与 `[0.30,0.60]`（均 2 位），同一组 CI 应统一。
- - Major: Proposition 编号跳跃——摘要先提 Propositions 1–3，随后直接跳到「Proposition 8'」，既未解释 4–7 的存在，也未说明撇号（prime）含义，编号体系对读者不透明。
- - Major: MMLU 样本量描述混乱——同一句中先写「proof-of-concept pilot N=30」，紧接着写「300 items」再扩展到「600 items」，N=30 在 MMLU 语境中指代什么（每域？每模型？）完全不清，与后文 300/600 量级冲突。
- - Major: 数字书写格式不统一——同句内「4 models」（阿拉伯数字）与「nine models」「six domains」「five families」（英文单词）混用，应统一遵循期刊规范。
- - Major: 「a first tolerant matcher」表述模糊——"first" 相对什么而言？前文只定义了 exact-string matcher，此处"first"无参照系，读者无法判断是否还有第二个 tolerant matcher。
### Minor（3）
- - Minor: `$\mathrm{smECE}_{\mathrm{sem}}$+MSI` 缺少空格/排版分隔，下标与 `+MSI` 粘连，渲染后可读性差。
- - Minor: Keywords 中列出「self-improvement」，但摘要正文仅在引言动机层面一笔带过，关键词与摘要核心贡献不匹配。
- - Minor: 多处超长括注（如「in-sample illustrative, not a validated bound; external validity from 600-item × 9-model census」）嵌套在主句中间，严重打断阅读节奏。

## 伦理（ethics）— ok
### Critical（2）
- - Critical: 未提供任何数据许可/可用性声明；MMLU 与“Chinese free-form set”的来源、版权与再分发权利未说明，尤制n set”溯源不明，存在未经授权使用第三方数据的合规风险。
- - Critical: 4999 dual-judged pairs、per-row adjudication 暗示涉及人工标注/裁判，但文中无任何 IRB/ä¼¦çå®¡æ¥ãç¥æ
### Major（4）
- - Major: 无利益冲突/competing interests 声明；文中多次引用特定厂商模型（Qwen2.5-7B 等五大家族），与厂商是否存在合作、资助或属于同一机构的关系未披鲲。
- - Major: 误用风险——“confidence 对 OOD 门控无用甚至有害”的结论可能被部署方用于拆除安全延迟门，而替代方案（self-consistency）仅基于 n=30 的探索性结果，文中未设置明确的“不可据此移除现有安全门”的部署约束声明。
- - Major: âmatcher 扩展后达 100% accuracy (ECE=0.0037)”即使标注“in-sample illustrative”，仍易被读者断章取义为“标签裁判可消除过度自信”，缺少对该见解被用于合理化高风险部署的限制性用法警告。
- - Major: 双盲合规性——匿名版本中 \citep{beyond2025} 等自引可能暴鲲团队身份，且文中强烈依赖特定模型/数据集组合，建议核对是否需三人称匿名化自引（截断部分无法完全核验）。
### Minor（2）
- - Minor: free-form 数据集未说明是否进行 PII/个人隐私信息渿理，若含用户生成内容则存在隐私泄露风险。
- - Minor: 缺少 ethics / broader impact 专节，未声明研究成果的潜在负面影响与合负面用法缓解措施。

## 汇总

- **Critical: 17 | Major: 32 | Minor: 18**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）