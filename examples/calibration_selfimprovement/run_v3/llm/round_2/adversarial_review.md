# 对抗审查报告

- 时间: 2026-08-27T16:23:38.719256+00:00
- 源: F:\deepseek\papers\calibration-self-improvement\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（3）
- - Critical: “matcher extended after per-row adjudication”是事后根据同一批标签反复迭代构造的，100%准确率/ECE≈0本质上是构造结果而非独立测量，用其支撑“matcher决定校准”存在循环论证。
- - Critical: 三种 matcher 没有独立于它们的人类金标准或盲法裁决；宽容 matcher 可能只是把失败重标为正确，因此“过度自信信号消失”无法区分是校准改善还是标签放宽。
- - Critical: OOD gating 仅 n=30、未定义 OOD 的构成、无对照组，并事后按“置信度与一致性负相关”分组，不能支持“self-consistency 移除过度自信 OOD 答案”的因果结论。
### Major（7）
- - Major: 30 个样本中 27 个置信度恰为 1.0，有效非退化样本仅 3 个；对 0.363/0.1297 等 ECE 点估计报告到 4 位小数缺乏统计依据。
- - Major: 用平均置信度 0.9963 对准确率 86.7% 作为过度自信证据只比较边缘均值，不是条件校准；在退化分布下 binning ECE 高度依赖分箱选择，文中虽承认却仍将其作为 headline 指标。
- - Major: “domain-specific calibration”中 domain 与题目难度、题型、各域 matcher 协议、judge 一致性等混杂，未控制这些变量，不能把 ECE 差异归因于 domain 本身。
- - Major: 4999 个 dual-judged pairs 来自 item/model 嵌套结构，并非独立样本；Holm 校正 p 值若按 pair 独立处理会严重低估不确定性。
- - Major: MSI 从 1.000 降至 0.334 同时改变语言、答案格式、数据集、样本量和 matcher 定义，无法把差异归因于“protocol”。
- - Major: semantic soft-label 估计器/smECE_sem 依赖未检验假设（soft label 是概率、逐行裁决无偏且不受模型置信度影响），且未报告标注者间一致性与盲法。
- - Major: 号称 600-item×9-model census 并宣称 findings reproduce，但 4×/17× 的域间比率基于宽 CI 点估计且仅极端 pair 显著，与强结论不匹配。
### Minor（2）
- - Minor: Proposition 8′ 的“置信度门控无信息”依赖退化分布假设，跨模型/跨域未必成立，未说明适用边界。
- - Minor: 研究未见预注册或预先固定分析方案，多个 matcher 为看到结果后扩展，存在 researcher degrees of freedom。

## 统计（stat）— ok
### Critical（3）
- - Critical: N=30 pilot 的核心结论（matcher 决定定标、OOD gating 危险、self-consistency 有效）没有独立验证或交叉验证；“extended after per-row adjudication”得到的 100% accuracy/ECE 0.0037 是样本内后验拟合，不是可推广的估计。
- - Critical: OOD 探针中“40–50% high-confidence answers wrong”基于 n=30，二项 95% CI 极宽（如 50% 约 [31%,69%]），不足以支撑“confidence useless even harmful”或“self-consistency removes overconfident OOD answers”的结论。
- - Critical: ECE 域间比较用“4×/17×”点估计比值作为效应量；ECE 有界且其中一个值接近 0 时比值极不稳定，应报告差值、方向和 bootstrap CI，否则效应量被系统性夸大。
### Major（5）
- - Major: 多重比较报告不完整：6 domains 每模型 15 对、9 模型约上百次检验，Holm 修正范围、检验方法、未修正 p 值均未说明；“只有最极端对显著”是在查看数据后反选结果，不能作为整体一致证据。
- - Major: 检验单位不明确：ECE 是聚合统计量，域间/模型间 p 值应基于 item-level paired bootstrap 或分层模型，而非直接对聚合点估计做检验；当前写法无法判断样本量是 items、pairs、models 还是 subjects。
- - Major: 95% CI 方法未报告（bootstrap 类型、是否 studentized/BCa、是否按 item/model 分层），如 Qwen2.5-7B 的 0.028 [0.001,0.08] 下界接近 0，说明估计极不稳定，却仍用于支撑“domain-specific”声明。
- - Major: 非显著≠无效应；在小样本/低功效下“Holm 后只有最极端对显著”不能证明其他域间无差异，需要功效分析、等价检验或同时报告效应量及其 CI。
- - Major: 不同 matcher 同时改变标签、accuracy 和 ECE，把 exact/tolerant/adjudicated 三种设置下的 ECE 直接比较是标签系统与测量方法混淆；应固定标签或对 matcher 不确定性建模，而不能直接宣称 overconfidence“vanishes”。
### Minor（3）
- - Minor: 30 个样本中 27 个 confidence=1.0，非退化样本仅 3 个；此时 binning ECE 的主数值（0.363/0.1297/0.0037）本身不可靠，摘要却将其作为核心结果突出，与自身 caution 矛盾。
- - Minor: 证据权重混用：600-item×9-model census、300-item pilot 和 n=30 probe 被放在同一叙述中支撑“reproduce/external validity/pattern worth study”，但对外部效度起关键作用的仍是极小样本，且未做加权或敏感性分析。
- - Minor: 没有预先指定假设、分析计划或探索性分析边界；Holm 修正只能控制已报告检验的 FWER，不能修复同一数据上反复探索 matcher、阈值和域对产生的选择偏差。

## 实验（experiment）— ok
### Critical（2）
- - Critical: 扩展 matcher 是在同一批 30 条 pilot 数据上逐条 adjudication 后构造的，报告 100% 准确率/ECE 0.0037 本质是标签泄漏和过拟合，缺少独立 held-out 集或独立标注者作为对照。
- - Critical: 无真正对照组/预注册基线：没有固定规则 matcher、随机 baselines 或第二标注者一致性对照，无法区分 matcher 效应与人工规则工程/主观裁决效应。
### Major（5）
- - Major: 消融不完整：提出的 smECE_sem、MSI、self-consistency gating 均未做组件消融，未分别报告只用置信度、只用一致性、两者组合、去掉 MSI 等条件。
- - Major: 基准不公平：MMLU 是公开 MCQ 且可能受预训练污染，中文 free-form 与英文 MMLU 在语言、格式、难度、题量上不对齐；比较 MSI/domain ECE 时未控制模型族、数据格式和题目数量等混淆因素。
- - Major: 超参数报告缺失：未给出 ECE 分箱数、温度、resample 次数、matcher 相似度阈值、置信度阈值等，也没有敏感性分析，结论无法复现。
- - Major: seed 管理缺失：未见任何随机种子或多 seed 重复；N=30 pilot、30-item OOD probe 与 3 次 resample 的随机波动均未被量化。
- - Major: 泛化证据不足：OOD gating 结论基于 n=30，且仅选取 confidence-consistency 负相关的模型（事后子组），外部有效性声明又用 N=30 pilot 自证，未在 held-out domain/新模型上验证。
### Minor（1）
- - Minor: domain 间 ECE 的 4×/17× 只是点估计比值，Holm 校正后仅极端域显著，不能支撑强 domain-specific 结论。

## 新颖性（novelty）— error: [WinError 10054] 远程主机强迫关闭了一个现有的连接。

## 可复现（repro）— error: <urlopen error [WinError 10061] 由于目标计算机积极拒绝，无法连接。>

## 写作（writing）— error: <urlopen error [WinError 10061] 由于目标计算机积极拒绝，无法连接。>

## 伦理（ethics）— error: <urlopen error [WinError 10061] 由于目标计算机积极拒绝，无法连接。>

## 汇总

- **Critical: 8 | Major: 17 | Minor: 6**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）