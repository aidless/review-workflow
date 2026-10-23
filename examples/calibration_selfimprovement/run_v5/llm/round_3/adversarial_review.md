# 对抗审查报告

- 时间: 2026-08-28T05:22:17.935876+00:00
- 源: F:\deepseek\papers\calibration-self-improvement\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（2）
- - Critical: 核心结论“校准由 matcher 决定/overconfidence 消失”基于用同一批答案逐条 adjudication 后扩展 matcher、再用该 matcher 给同一批数据生成标签并计算 ECE，标签构造与评估数据同源，构成循环验证/标签泄漏，内部效度失效。
- - Critical: 关键校准图景只有 30 个样本且 27 个置信度恰为 1.0，分布严重退化；此时任何 ECE（包括 binning-free 与 smECE_sem）都对少数标签翻转极敏感，宣称 ECE 0.0037 或“信号消失”属于小样本过度解释。
### Major（4）
- - Major: OOD gating 分析 N=30，且“40–50% 高置信 OOD 答案错误”没有说明阈值如何选择、是否事后在同一数据上调参，也没有低置信度/ID/随机基线对照，无法支持“confidence 对 gating 有害”的因果或方向性推断。
- - Major: 4999 对答案来自 600 题 × 9 模型/多领域等嵌套结构，若按独立样本计算 95% CI 和显著性会因伪重复（pseudoreplication）高估精度；需按 item/model 聚类或使用混合效应模型。
- - Major: 跨领域/跨模型 ECE 比较混淆了题目难度、各领域样本量、模型族、解码温度、提示格式等变量；“calibration is domain-specific”可能反映难度或样本构成差异，而非校准本质的领域效应。
- - Major: 形式化结论（flip rate 界、FNR/FPR 不对称项、MSI、Proposition 8'）依赖未明确检验的假设，例如 matcher 错误与置信度/正确性独立、soft-label 估计无偏等；理论边界未被实证验证，经验推广不充分。
### Minor（3）
- - Minor: “first tolerant matcher”和“extended after per-row adjudication”的 matcher 选择过程不透明，且可能受已观察结果影响，存在未完全控制的 matcher 选择偏差。
- - Minor: 扩展 matcher 后 accuracy 被标成 100%，此时 ECE≈0 几乎是“正确率被重标为 1”的定义性结果，而非校准能力改善的直接证据。
- - Minor: 摘要使用“determined by”等强因果措辞描述测量协议与 ECE 的关系，但当前设计是探索性/事后分析，因果推断不恰当。

## 统计（stat）— ok
### Critical（3）
- - Critical: N=30 的 OOD gating 分析（且 27/30 置信度恰为 1.0）样本量过小，“40–50% high-confidence OOD wrong”可能只来自个位数样本，未给置信区间，无法支撑“confidence harmful / consistency removes overconfident OOD”的结论。
- - Critical: 所有核心数值（ECE 0.363/0.1297/0.0037、accuracy 63.3%/86.7%/100%、MSI、domain 差异 0.45）均只报点估计，没有 SE、bootstrap CI 或 cluster-robust 方差；在 item/model 重复观测结构下无法判断差异是否超过噪声。
- - Critical: 多重比较与检验选择不透明：只写“95% CIs; only extreme Holm-corrected pairs significant”，未说明检验名称、比较总数、是否对 matcher/model/domain 的全部比较做控制；事后挑选“extreme pairs”再校正会扭曲 family-wise error。
### Major（4）
- - Major: “extended matcher after per-row adjudication → 100% / ECE=0.0037”是在同一批数据上迭代修正标注规则得到的 in-sample 结果，没有 held-out adjudication 或交叉验证，100% 是典型的标签过拟合，不能作为校准问题消失的证据。
- - Major: “up to 4×”和“up to 0.45 absolute”只给极端范围，缺少标准化效应量与不确定性；近零 ECE 的倍率极易误导，且小样本比例未报告精确 CI。
- - Major: 用 mean confidence 0.9963 vs 86.7% 直接称“overconfidence signal”，再因 matcher 改变而称其“vanishes”，没有配对差异检验或区间估计；退化分布下该均值比较也违反常规正态假设。
- - Major: 样本单位/依赖性未交代：300/600 items、4/9 models、1159/4999 pairs 的缺失机制不明，同一 item 被多模型重复观测会伪增殖样本量；domain/model 比较应采用 mixed-effects 或 cluster-robust 推断。
### Minor（2）
- - Minor: 未报告退化置信度分布下 binning-free ECE 估计量的方差/重采样稳定性；27/30 个点集中在 1.0 时，任何校准估计都对极少量非 1.0 样本极其敏感。
- - Minor: “only extreme Holm-corrected pairs significant”隐含着“不显著=无差异”，但小样本下不显著不等于等价；应补充等价性检验或完整 adjusted p 值与效应量。

## 实验（experiment）— ok
### Critical（2）
- - Critical: 没有独立的 ground-truth 对照组：三种 matcher 都在同一批数据上构造/调整，且 per-row adjudication 后达到 100%，等于用测试标签拟合判定规则，无法排除“标签泄漏/过拟合 matcher”解释。
- - Critical: 消融完整性不足：未把“语义容错”与“per-row 人工裁定”拆开，也未对 matcher 的容错阈值、判定条件做单因素消融，因此 63.3%→86.7%→100% 的差异无法归因于某个具体设计成分。
### Major（5）
- - Major: 基准公平性不清楚：MMLU 扩展集未说明各 domain/模型的样本量是否均衡、题目难度与 free-form 是否匹配、提示格式和选项顺序是否控制；MSI 在 free-form 与 MMLU 的差异可能来自任务/难度混淆而非协议本身。
- - Major: seed 管理缺失：未报告 MMLU 题目抽样 seed、解码 temperature/seed、self-consistency 三次 resample 的 seed，也没有多 seed 重复实验；27/30 个 1.0 的退化分布可能只是单一采样/解码配置的产物。
- - Major: 超参数不透明：ECE 的 bin 数/边界、temperature scaling 的训练-验证划分与优化细节、tolerant matcher 的判对阈值、MSI 的敏感度参数均未说明；尤其一边批评 binning ECE 一边未给出 binning-free 指标的完整参数设置。
- - Major: OOD gating 分析无对照组：N=30 的探索没有 no-gating、random-gating、confidence-only、consistency-only 或匹配 ID 基线，40–50% 高置信错误率无基线可比，不能支持“confidence 对 OOD gating 有害”的结论。
- - Major: 泛化与过拟合风险：matcher 扩展基于同一批 per-row adjudication，且结果标注为 in-sample；缺少 held-out 集、交叉验证、独立标注者一致性或独立复现，9 models/4999 pairs 的汇总也可能掩盖 per-model 过拟合。
### Minor（3）
- - Minor: 统计设计不完整：跨 6 domains/9 models 的比较只报告 Holm 校正后显著性，未报告每 cell 样本量、效应量、CI 构造方法和多重比较总数；N=30 的 OOD 结论也不足以支持“calibration is domain-specific”的强表述。
- - Minor: 缺少与已有校准基线的对照：未与原始置信、Platt/temperature、isotonic 等标准校准方法在相同数据上对比，难以评估 smECE+MSI 的增量价值。
- - Minor: 模型级消融不足：9 个模型的对齐/规模/系列差异未作为因素分析，结果可能由个别模型主导；应报告按模型分层和随机效应的稳定性。

## 新颖性（novelty）— ok
### Critical（1）
- - Critical: 核心宣称“measured calibration is determined by the label matcher”并非真实 GAP：已有语义采样校准框架（Sem-ECE/Sem2-ECE）和 Ambiguous Ground Truth 校准研究已表明标签/语义类划分会系统性改变准确率与 ECE 估计，本文更像用 N=30 样例复述已知现象，首次性被夸大。
### Major（4）
- - Major: 所谓“semantic soft-label estimator + MSI”与 Sem-ECE 的语义类分组估计、以及 “Calibration Is Not Enough”的 stability/sensitivity 评估高度重叠；未给出与这些工作的非平凡差异或比较实验，增量贡献被高估。
- - Major: “binning-based ECE 不可靠”是校准领域早已确立的问题（binning bias、adaptive/debiased ECE、kernel calibration error 等），将其包装为核心 caution 只是把已知结论迁移到退化 confidence 分布，缺少新的度量理论贡献。
- - Major: Propositions 1–3 的 flip-rate 与 FNR/FPR 不对称边界，形式上很像 label noise / 不确定标签下校准误差的已知分解，未论证为何不能直接从已有 noisy-label calibration 结果推出，理论新颖性有限。
- - Major: OOD gating 的“confidence 有害、self-consistency 有用”以探索性 N=30 为基础，且自洽性作为置信/门控信号已有大规模审计（如 self-consistency/cross-model agreement 工作），不足以支撑“grounding an OOD-aware gating rule”的新贡献。
### Minor（1）
- - Minor: 跨域 MMLU 的“domain-specific calibration”是描述性且已有大量文献支持；且只有极端 Holm 校正对显著，样本量扩大后仍难支撑高强度的普适性结论。

## 可复现（repro）— ok
### Critical（3）
- - Critical: 全文未提供数据/代码/工件仓库或 DOI，且未给出从 raw logs → matcher 判定 → accuracy/ECE 的逐条证据链，63.3%/86.7%/100% 等核心数字无法独立复算。
- - Critical: 未报告任何随机种子及解码/采样配置（temperature、top-p、resample 次数），自洽性“三次重采样”与 OOD/N=30 抽样无法可复现地重现。
- - Critical: 没有一键复现脚本、容器镜像或依赖锁定（Dockerfile/environment.yml/requirements.txt 均缺失），无法从零重建 300/600 items、1159/4999 pairs 的全部结果。
### Major（4）
- - Major: 缺少配置快照：模型版本/revision、API 或本地部署方式、system prompt、verbalized-confidence 模板、matcher 规则/版本、ECE 分箱方式均未给出，实验环境不可枚举。
- - Major: “per-row adjudication 后扩展 matcher”未公开 adjudication 协议、标注者/规则与中间判定文件，无法排除标签泄露与事后拟合，证据链在关键环节断裂。
- - Major: 数据许可与模型条款仅在摘要中承诺“附录说明”，未见 MMLU 版本/URL、许可文本、模型 terms 及再分发/重实验权限，合规性无法核验。
- - Major: 没有哈希对账（原始数据集、模型输出、annotation/matcher 结果、最终 tables 的 SHA-256 等），无法确认 1159→4999 对和 N=30 样本对应的数据版本是否一致。

## 写作（writing）— ok
### Major（2）
- - Major: 摘要中 “matcher extended after per-row adjudication 100% (ECE=0.0037)” 未说明这是用裁决后标签重算的 matcher/label 准确率，不是模型原始准确率；写成 “100% accuracy” 有误导，且使“测量由 matcher 决定”的证据近乎同义反复。
- - Major: Keywords 之后的 “Our central finding…” 是游离于任何章节之外的段落，且其中的 `smECE_sem` 未在摘要或引言中定义/展开，读者无法解析这一核心主张。
### Minor（5）
- - Minor: 三个 ECE 数值精度不一致（0.363 vs. 0.1297 vs. 0.0037），应统一有效数字或小数位数。
- - Minor: 摘要引用 “Propositions~1--3” 和 “Proposition~8$'$” 却没有给出语境；正文编号一旦调整即失效，且摘要可读性差。
- - Minor: “only extreme Holm-corrected pairs significant” 表述含糊：哪些 pairs、多 extreme、效应量与 CI 均未交代。
- - Minor: “We use single-turn verbalized confidence as probe, agentic multi-step left to \S6 Discussion” 语法破碎，且与前文 “multi-step agentic metrics are orthogonal” 的范围表述不完全一致；应为 “as a probe” 并明确 “defer agentic multi-step to Section 6”。
- - Minor: 在可见部分中，关键 ECE/accuracy 数字均为内联数字，未见对应表/图编号或引用；若正文后续也无图表支撑，应补充。

## 伦理（ethics）— ok
### Critical（1）
- - Critical: 论文声称数据许可、模型条款和伦理合规在附录中，但当前提交正文/材料中看不到可核验的清单；若 9 个模型的部分输出来自商业 API，存储、二次分发或用于训练/评估可能违反服务条款，评审无法确认合规性。
### Major（4）
- - Major: 若“per-row adjudication”涉及人工标注或人工裁决，未说明标注者招募、知情同意、报酬、IRB/伦理审查流程，也未报告标注者间一致性和偏见控制。
- - Major: 收集并可能发布 4999 对模型输出时，未明确说明对输出中可能出现的记忆化个人信息、有害内容或提示泄露进行过滤/去标识化/审查。
- - Major: 使用多个专有模型做比较，未声明作者与模型厂商之间可能存在的资助、隶属、早期访问或咨询关系，存在利益冲突披露缺口。
- - Major: OOD-gating 结论基于探索性 N=30 数据，却可能被读者当作部署依据；高置信但错误率 40–50% 的结果若被简化为“用 self-consistency 做门控”的建议，会带来误用风险。
### Minor（2）
- - Minor: 双盲方面仅隐藏作者名不够；若附录、自引（如 beyond2025）或模型访问信息可反推作者身份/机构，仍会破坏 TMLR 双盲。
- - Minor: “matcher extended after per-row adjudication 后达到 100% accuracy” 表明标签裁决可被反复调整以美化结果；若不预先注册 matcher/裁决协议，指标存在被 gaming 的误用风险。

## 汇总

- **Critical: 12 | Major: 27 | Minor: 16**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）