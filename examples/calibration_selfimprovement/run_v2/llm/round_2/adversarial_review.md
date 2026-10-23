# 对抗审查报告

- 时间: 2026-08-27T13:33:11.285828+00:00
- 源: F:\deepseek\papers\calibration-self-improvement\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（4）
- - Critical: The "matcher determines calibration" causal claim is near-tautologicalâthe matcher is the measurement instrument, so changing it changes the measurement by definition; there is no counterfactual (no "true" calibration held fixed), so the framing as a discovery rather than a measurement
- - Critical: In-sample per-row adjudication that extends the matcher until accuracy reaches 100% is circular (researcher degrees of freedom / confirmation bias): labels were modified based on observed residuals, so ECE=0.0037 is constructed, not estimated; the claim that overconfidence "vanishes once
- - Critical: The OOD-gating conclusion ("confidence is uselessâeven harmful; consistency retains discriminative power") rests on n=30 and selects on a post-treatment variable (models whose confidence and consistency are negatively correlated), conflating selection effect with gating efficacyâthis
- - Critical: The MSI cross-protocol comparison (1.000 on Chinese free-form vs. 0.334 on MMLU multiple-choice) varies language, domain, answer format, and model simultaneously; attributing the difference to "protocol" is an uncontrolled confound with no identification strategy.
### Major（6）
- - Major: The paper admits binning-based ECE is unreliable under degeneracy (27/30 = 1.0) yet still reports and interprets point ECE values (0.363, 0.1297, 0.0037) as meaningful summaries; if the distribution is degenerate, the ECE estimates themselves (not only the binning variant) are uninformative
- - Major: Cross-domain "domain-specific" calibration is supported by point-estimate ratios (4Ã, 17Ã) while the authors themselves note 95% CIs are wide and overlapping and Holm-corrected p-values show "only the most extreme pairs are significant"; drawing a broad domain-specificity conclusion from 
- - Major: Self-consistency is measured from only three resamples, yielding high sampling variance; treating three-sample agreement as a reliable discriminative signal relative to confidence is an unverified assumption that directly affects Proposition 8â² and the gating recommendation.
- - Major: Propositions 1â3 bound measurement bias by matcher flip rate and an asymmetry term, but no analysis of bound tightness or vacuity is given; a loose bound provides no actionable guarantee and the propositions' empirical relevance is unestablished.
- - Major: The 4999 dual-judged pairs are presented without inter-rater agreement / Cohen's Îº; label validity is the precondition for all downstream calibration claims, and its omission is a threat to internal validity.
- - Major: Proposition 8â² ("confidence-threshold gate carries no information about correctness") is conditioned on confidence degeneracy, but the paper does not establish that degeneracy is the general deployment condition; generalizing a degenerate-condition result to a broad gating caution is an u
### Minor（2）
- - Minor: The premise that practitioners treat self-reported confidence "as a calibrated probability" for deferral / memory-gating is asserted without citation or evidence of prevalence, weakening the motivation's external grounding.
- - Minor: The title-level "caution on binning-based ECE" generalizes from a single degenerate distribution specific to this setup; whether degeneracy is common across agents/tasks is not established, limiting the caution's scope.

## 统计（stat）— ok
### Critical（3）
- - **Critical**: N=30 上报告 ECE 精确到 4 位小数（0.0037、0.1297），且无任何不确定性区间。30 个样本下 ECE 的标准误约 0.05â0.10 量级，4 位小数是虚假精度，0.0037 与 0 在统计上无法区分。
- - **Critical**: 退化分布（27/30=1.0）下有效样本量远小于 30；ECE 由 â¤3 个非退化点 + 退化 bin 内的错误率决定，实际支撑点 < 10，却仍将 ECE 作为可解释点估计报告并据此得出结论。
- - **Critical**: 以点估计比值（4×、17×）作为 headline finding，但自述 95% CI 极宽（Qwen2.5-7B ECE [0.001, 0.08] 上下界比 80×）；0.028/0.479 的比值 CI 必跨越 1，17Ã 是无效应量报告。
### Major（5）
- - **Major**: 9 个模型 Ã 多个 domain pair 的 ECE 跨域比较未说明所用检验（ECE 无标准参数检验；bootstrap? permutation? ）；Holm 校正存在但基础检验统计量不明，无法判断 p 值合理性。
- - **Major**: 相关性结论（"confidence 与 consistency 负相关"，n=30）未报告 r 值、p 值或 CI，以 "indicative" 一词规避显著性判定；多模型间的相关检验未做多重比较校正。
- - **Major**: "40â50% of high-confidence OOD answers are wrong" 未报告分母（30-item probe 中 high-confidence OOD 子集可能仅 10â20 个），百分比的标准误极大，40â50% 的 10pp 区间在小 n 下几乎无信息量。
- - **Major**: 三个 matcher 的 ECE（0.363、0.1297、0.0037）是对同一组 30 个样本的配对重标签结果，未作配对不确定性传播（如 bootstrap over items），直接比较点值忽略了 label-flip 的相关性。
- - **Major**: N=30 pilot 的 ECE 点估计（0.363、0.1297、0.0037）无 CI，而 600-item census 部分有 CI，不确定性报告不一致，读者无法判断 pilot 结果的统计可靠性。
### Minor（2）
- - **Minor**: MSI 值（1.000、0.334）报告为确切点值无不确定性区间，且 1.000 暗示上界截断而非真值。
- - **Minor**: "4999 dual-judged pairs" 将判决对数与独立样本量混淆；用于校准估计的分析单像应是 600 items Ã 9 models ，4999 pairs 是判决层统计，不应作为样本量引用。

## 实验（experiment）— ok
### Minor（1）
- 

Let me examine the full paper to understand the experimental setup.
Let me find the actual paper file with content.


让我更仔细地查看实验部分、三臂研究、跨模型研究以及 OOD 实验。



让我检查一下 OOS 重校准部分和 three-arm 附录细节。

现在我已经有足够的信息来生成对抗审查报告了。让我来整理一下我的发现。

- 严重：三臂实验无有效对照组：各臂使用不同 seed（20260815/16/17）且各自独立进化轨迹，进化基本惰性（A/B 未提升任何候选）

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: "中心发现"——matcher 决定 measured calibration——本质上是评测领域早已熟知的常识：评分方式（exact match vs semantic match）影响准确率，准确率影响 ECE。NLP 评测文献中长期讨论 exact-match 对 BLEU/accuracy 的扭曲效应。将此包装为"Propositions 1–3 + flip rate bound"的形式化贡献，是对简单观察的数学化妆，增量贡献被严重夸大。
- - Critical: GAP 的真实性存疑。论文声称"agent 自报 confidence 的 calibration 在部署前很少被验证"，但这一 gap 未被文献综述支撑（正文截断，无法确认，但摘要未引用任何表明"前人忽略此验证"的工作）。calibration validation 本身是标准部署流程的一部分；"前人没做"这一前提是否成立直接关系到全文动机是否成立。
### Major（5）
- - Major: "置信度分布退化（大量值为 1.0）"在 LLM 文献中是广为人知的现象，多个前人工作已报告 instruction-tuned 模型的极端 overconfidence（摘要自身引用了 beyond2025）。将该现象作为"发现"提出，新颖性不足，未与已有 overconfidence 文献做差异声明。
- - Major: "binning-based ECE 在退化分布上不可靠"是 calibration 领域公认的已知限制（Nixon et al. 2019 等已系统讨论 binning 敏感性）。论文未与该文献做显式差异对比，且未说明提出的 smECE_sem 相对于已有 binning-free 校准指标（如 soft-ECE、log-loss-based metrics）的增量贡献具体在哪里。
- - Major: OOD-aware gating 部分的核心主张——"自一致性信号优于 confidence 用于 OOD gating"——直接落在 self-consistency 文献（Wang et al. 2022, Chen et al. 2023 等）的既定结论范围内。"confidence 在 OOD 上有害"这一点是否构成超越前人的新发现，未做文献差异声明。
- - Major: 贡献数量与证据体量不匹配。N=30 的 pilot 被冠以"methodology study"之名，摘要却在同一 N 上叠加至少五项独立声明（matcher dependence、degeneracy、ECE 不可靠、gating 无信息、consistency 有效）。即使补充了 600-item census，核心命题（degeneracy、gating 无信息）的验证仍仅依赖 N=30，贡献声称被系统性膨胀。
- - Major: 摘要声称"domain-specific calibration: ECE 跨域变化 4×–17×"——跨域/跨任务难度差异导致 calibration 差异是已知现象，且该结论的统计支撑薄弱（95% CI 极宽，Holm 校正后仅极端对显著）。将一个统计上几乎不显著的观察作为"reproduce"的贡献声明，新颖性与稳健性双重不足。
### Minor（2）
- - Minor: MSI（matcher sensitivity index）作为新指标提出，但其定义与现有 inter-rater agreement / label noise 文献中的 sensitivity metrics 的差异未在摘要中体现，读者无法判断其是否真正新颖。
- - Minor: "semantic soft-label calibration estimator"这一技术贡献在摘要中仅一笔带过，无法判断其相对于已有 soft-label / semantic matching 校准方法的增量是否被夸大。

## 可复现（repro）— ok
### Critical（4）
- - **Critical**: 通篇未声明代码/数据/adjudication log 的开源 release（TMLR 强制要求 Reproducibility Checklist），中心结论“matcher determines calibration”无法被独立复现。
- - **Critical**: 核心的 self-consistency 信号基于“agreement of three resamples”，但未给出 sampling seed、temperature、top-p；resample 生成不可复现，直接影响 Proposition 8' 与 OOD gating 结论。
- - **Critical**: âper-row adjudication of residual errors”属主观判定，未公布裁决者身份、标注指引(guidelines)、交叉标注一致率(IAA)；同一批样本可被不同裁决者翻转，100% accuracy 与 ECE 0.0037 无对账基准。
- - **Critical**: 模型检查点未 pin：“nine models spanning five families”与 Qwen2.5-7B 等均未给 commit/权重哈希；若含 API 模型（隐式 drift），跨时间复现必然失败。
### Major（5）
- - **Major**: 对偶计数对不上账：600Ã9=5400 但报 4999 dual-judged pairs（缺 401）；300Ã4=1200 但报 1159（缺 41），未说明缺失原因，哈希对账无法成立。
- - **Major**: MMLU 版本/commit 未 pin；“Chinese free-form setâ(MSI 1.000)无来源、无 license、无划分协议，数据许可链断裂。
- - **Major**: decoding 配置快照缺失：temperature、max tokens、few-shot 格式、system prompt 模板全未出现；“degenerate(27/30=1.0)”是否 greedy 产物无法判定，影响 degeneracy 结论的可复现性。
- - **Major**: 95% CI（如 Qwen2.5-7B 0.028[0.001,0.08]）与 Holm-corrected p-values 未指明 bootstrap 迭代次数/seed 或检验类型，CI ä¸显著性ç»è®ºä¸å¯å¤ç°ã
- - **Major**: OOD 定义缺失：“40â50% of high-confidence OOD answers are wrong”未给 OOD 划分阈值/条件，该 gating 结论无法重跑。
### Minor（2）
- - **Minor**: ânine models / five families”未在摘要枚举，家族与模型清单必须在附录 pin；当前仅可见 Qwen2.5-7B，对账子集不明。
- - **Minor**: N=30 pilot 未声明是否固定 item 集及其哈希；“in-sample illustrative, not a validated bound”虽已 hedge，但原始 30 行样本不发布则无法核验 63.3/86.7/100 三个 matcher 数字。

## 写作（writing）— timeout
### Critical（1）
- - Critical: 标题写"a Caution on Binning-Based ECE"、摘要又断言该退化分布上分箱ECE"unreliable"，但摘要三组头条校准数值（0.363 / 0.1297 / 0.0037）正是分箱ECE、且报至3–4位有效数字——核心证据用的是论文自己否定的指标。
### Major（7）
- - Major: 外部有效性标签自相矛盾——同一collection既是"proof-of-concept pilot N=30 as external-validity demonstration"，又括注为"external validity from 600-item × 9-model census"；标题亦称"Pilot"。N=30概念验证无法确立外部有效性，且有效性被挂到两个不一致的样本量上。
- - Major: 至少两处（可能四处）"N=30"样本混用——主pilot（中文free-form）、MMLU概念验证、"our 30-item probe"（OOD）、"indicative, n=30"（自一致性）——未说明哪些是同一样本，读者无法追踪样本身份。
- - Major: 正文标语行主张"smECE_sem+MSI"为诊断工具，但摘要证据全用普通ECE呈现；且"smECE_sem"在摘要中从未定义（只写"semantic soft-label calibration estimator"），被推荐的指标既未定义、又未用于所报结果。
- - Major: 摘要为单段约400词，糅合五条独立发现（matcher依赖、退化、形式化命题、跨域census、OOD gating），无主次，远超摘要承载。
- - Major: 命题引用为"1–3"后跳至"8′"——4–7缺省且撇号变体无解释；其间引入的MSI/soft-label估计器未对应任何命题编号，形式化结果地图不连贯。
- - Major: "subjects（3个）"与"domains（6个）"在4×/17×主张中并列，未说明二者是子集关系还是不同分类轴；且4×主张无示例支撑（仅给出17×的Qwen2.5-7B对比）。
- - Major: 头条"4×/17×"为点估计、95% CI很宽且"only the most extreme pairs are significant"，却放在census总结开头，框定强度超出统计支撑。
### Minor（7）
- - Minor: N=30下的伪精度——ECE报至4位有效数字（0.1297、0.0037）、均值置信度0.9963报4位，而单项粒度≈0.033；且精度不一致（0.363 vs 0.1297 vs 0.0037）。
- - Minor: 主pilot语言/领域（中文free-form）延迟到摘要末尾MSI句才出现，前文读者全程不知数据集为何。
- - Minor: 关键词（calibration, self-improvement, confidence, MMLU, ECE）遗漏matcher/degeneracy/gating/OOD/self-consistency，却收入边缘的self-improvement；中文数据集未命名。
- - Minor: "40–50% of high-confidence OOD answers are wrong in our 30-item probe"——小计数上的区间含糊，分母"high-confidence OOD answers"数量未给出。
- - Minor: "dual-judged pairs"语义模糊（model–item判定数 vs 每题判官对）；1159(对4×300=1200)与4999(对9×600=5400)的缺失未说明；"MSI 1.000"报为恰好1.0亦可疑。
- - Minor: 摘要含>15项数值声称却无任何Table/Figure引用，可见正文亦无\begin{table}/\begin{figure}；需核对正文表格是否与摘要数值逐一一致（如0.1297、4999、0.479[0.30,0.60]）。
- - Minor: 摘要后单独成段的"Our central finding…"是重复摘要结论的标语式句子，像宣传语；且"temperature scaling is not robust to relabeling"作为强论断在摘要中无支撑、无引用地抛出。

## 伦理（ethics）— ok
### Critical（2）
- - Critical: 全文未声明任何数据集许可协议——MMLU（MIT）未注明，"Chinese free-form set"来源与授权状态完全不明，存在版权侵权与不可复现的合规风险。
- - Critical: 通过"per-row adjudication"将 matcher 逐行调至 100% 准确率（ECE 0.0037）的过程本质是对评测口径的数据拟合，该方法可被滥用于伪造有利校准结论（matcher 造假/p-hacking），论文未设预注册或防滥用护栏。
### Major（4）
- - Major: 涉及 Qwen2.5-7B 等"五个家族九个模型"，若作者与任一模型供应商存在雇佣/资助关系须声明，但全文未见利益冲突（COI）与资助来源披露。
- - Major: 提及"4999 dual-judged pairs"与逐行 adjudication 暗示大量人工标注，却无 IRB/伦理审查、标注者招募条件、隐私保护与数据留存说明，违反人类被试/标注伦理规范。
- - Major: 双盲合规存疑——正文 `\citep{beyond2025}` 若为作者既往工作须以第三人称匿名化引用，且 `math_commands.tex` 等附属文件可能残留身份痕迹，均未声明已完成去标识。
- - Major: 以 N=30 得出"40–50% 高置信 OOD 答案错误"并据之提出部署 gating 建议，样本过小却用于安全相关结论，过度泛化可能误导下游误用，警示不足。
### Minor（1）
- - Minor: `corresponding@example.com` 占位符本身合规，但 camera-ready/preprint 去匿名指令行仍保留在匿名提交稿中，需确认不致身份泄露。

## 汇总

- **Critical: 16 | Major: 32 | Minor: 17**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）