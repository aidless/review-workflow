# 对抗审查报告

- 时间: 2026-08-26T06:59:48.508219+00:00
- 源: F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_Nm7dTogzfa\extracted_text.txt
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（2）
- - Critical: 前提不成立风险——将含随机延迟的异步梯度法当作经典 AA 所要求的确定性、平稳不动点迭代；延迟使每步算子依到达顺序随机变化，AA 收敛与加速所依赖的"一致压缩且算子平稳"前提在异步设定下是否成立，全文未见严格论证，动摇整个方法的地基。
- - Critical: 混淆变量与因果归因——safe-guard 回退机制本身可能成为加速来源的混淆变量；若实验中 safe-guard 频繁触发、回退到普通梯度步，则观测到的收敛/加速无法归因于 AA，论文未做消融以隔离 AA 贡献与 safe-guard 贡献，加速的因果归因不当。
### Major（4）
- - Major: 因果推断失当——"delay-free step-size 往往导致更快收敛"缺乏逻辑与实证支撑；延迟无关步长须按最坏情形延迟取保守小值，在低延迟环境下反而更慢，该因果宣称与保守性论证自相冲突且未被匹配延迟分布的对照实验检验。
- - Major: 混淆变量未控——迭代数收敛比较未扣除 AA 每步额外的最小二乘求解与历史存储开销；墙上时间比较又受实现质量、通信与硬件强混淆，"同时改进迭代数与墙上时间"在两套口径下都不干净。
- - Major: 假设过强——"mild conditions" 的含糊表述掩盖了全局收敛对强凸性、光滑性、有界延迟等强假设的依赖；这些假设排除了动机部分强调的非凸深度学习场景，前提与动机自相矛盾。
- - Major: 验证范围不匹配——实验仅限凸分类任务，而动机与应用场景（多 GPU 分布式训练）普遍非凸；在凸问题上得到的加速结论无法外推至论文宣称的目标场景，内部与外部效度均存疑。
### Minor（2）
- - Minor: 选择性报告风险——"most test examples" 与 "comparable in remaining" 的对冲措辞暗示存在未胜出样例，测试集选取标准与完整结果在可见部分未透明披露，存在 cherry-picking 嫌疑。
- - Minor: 创新性宣称过强——"AA 在分布式优化中尚未被探索"忽略了多块 ADMM 加速、分布式拟牛顿等已有工作，新颖性框架可能夸大，影响对方法定位的判断。

## 统计（stat）— timeout
### Critical（1）
- - Critical: 摘要核心结论"ADGM-AA improves both iteration-count and wall-clock-time convergence over the baselines in most test examples"为比较性效能主张，但全文未见任何统计检验、置信区间或重复试验次数（n）的报告，等于以无统计支撑的定性叙述做出泛化性优劣判断，存在 p 值/检验缺失的根本性缺陷。
### Major（4）
- - Major: 样本量未声明且极可能为单次运行（n=1）——分布式异步算法的 wall-clock-time 受网络延迟、worker 负载、系统调度等随机因素影响方差极大，单次运行的收敛曲线无法区分真实改进与噪声，n=1 不支持任何统计推断。
- - Major: 无方差/不确定性报告——未见误差棒、标准差、置信带或多次随机种子下的均值±SD/SE 报告，读者无法评估结果的可重复性与显著性。
- - Major: 多重比较未校正——ADGM-AA 同时与多个 baseline 在多个数据集 × 2 个指标（iteration-count、wall-clock-time）上做比较，比较矩阵膨胀假阳性率，未见 Bonferroni/Holm/FDR 等校正或预注册分析协议。
- - Major: 无效应量量化——"improves"与"comparable"无操作化定义，缺少如相对加速比（speedup ratio）、收敛步数减少百分比等效应量指标及其置信区间，无法判断改进的实际意义大小。
### Minor（2）
- - Minor: "in most test examples…comparable in the remaining cases"表述含糊——未给出具体计数（几个数据集中几个）及"comparable"的判定阈值（如相对差距 <5%？），存在选择性报告/cherry-picking 风险。
- - Minor: 两个指标（iteration-count 与 wall-clock-time）并列声称改进，但未讨论二者一致性——异步场景下 iteration-count 少未必 wall-clock-time 快（单次迭代通信/同步开销可能更大），缺乏对指标间不一致可能性的统计讨论。

## 实验（experiment）— ok
### Critical（2）
- - **Critical**: 泛化性严重不足——仅在"convex classification tasks"上验证，未涵盖非凸优化（如深度学习训练）、回归、非平滑优化等场景；而异步分布式优化的实际主要应用场景恰恰是非凸大规模模型训练，凸分类任务是最容易收敛的设定，泛化论证极弱。
- - **Critical**: 基准公平性存疑——文中强调自己的"delay-free step-size"比现有方法的"delay-dependent step-size"更易确定且收敛更快；但如果基准方法的 delay-dependent step-size 未经公平调优（如未搜索最伏步长、或故意取保守参数），则对比结果存在系统性偏见；摘要未提及基准方法的步长调优协议。
### Major（5）
- - **Major**: 结果报道存在选择性偏差嫌疑——"improves...in most test examples, while achieving comparable performance in the remaining cases"是典型的套话式表述，暗示部分实验中未能超越基准，但未明确披鲲失败案例的比例、场景及原因，存在 cherry-picking 风险。
- - **Major**: 消融实验不完整——论文提出两个核心组件（Anderson acceleration 本身 + reference-path-based safe-guard scheme），摘要中无任何消融实验的提及，无法判断性能提升到底来自 AA 还是 safe-guard，抑或二者相互依赖；应至少提供"基础异步法 vs. AA-only vs. AA+safeguard"的三路对比。
- - **Major**: seed 管理与统计显著性缺失——摘要完全未提及随机种子数量、方差/置信区间、或统计检验；异步方法因延迟随机性与数据 shuffle，run-to-run 方差可能很大，单次运行的收敛曲线不足以支持"faster convergence"的结论。
- - **Major**: wall-clock-time 对比的前提条件不明——异步方法的墙钟时间强烈依赖于延迟模型的设定（工作节点异构性、网络延迟分布、 straggler 比例）；若延迟模型为人工模拟且未经实测验证，则 wall-clock 结论的外部效度存疑；同时 AA 每步额外计算成本（矩阵求解）应在 wall-clock 中公平计入。
- - **Major**: 超参数报道不明——AA 本身有关键超参数（历史深度 m、safe-guard 阈值、混合系数β），摘要未提及这些参数如何选取、是否对每个数据集单独调优；若 AA 参数经 dataset-specific 调优而基准使用默认参数，则对比不对称。
### Minor（1）
- - **Minor**: 实验章节未在审阅材料中完整呈现（内容被截断），无法核实上述猜测是否在正文中已被克服；建议审稿中要求作者补全完整实验细节后再评。

## 新颖性（novelty）— ok
### Critical（1）
- - Critical: 文猠自己声称“the application of AA to distributed optimization remains unexplored”，但引用的 Ouyang et al. (2020) 已将 AA 应用于 ADMM，而 ADMM 本身就是分布式优化的核心框架，GAP 应收窄为“异步 + 分布式”而非“分布式”，现有表述构成对文献的误导性概括。
### Major（4）
- - Major: “首次将异步梯度法转化为定点迭代”被作为贡献之一，但异步方法作为定点迭代分析是 ARock、异步坐标更新等的标准范式，此步骤不存在方法论新意，增量贡献被夸大。
- - Major: ânovel reference-path-based safe-guard scheme”的新颖性缺乏与已有 safe-guarded Anderson acceleration（如 Toth & Kelly 2015、Evans et al. 2018，以及本文自引的 Mai & Johansson 2020 中的安全网设计）的细致差异化对比，“reference-path”命名未被明确区别于已有 restart/trust-region 性质的 safe-guard。
- - Major: âdelay-free step-size”被作为对比优势，但异步优化中已有延迟无关步长的工作（如 ARock、异步 SGD 中 delay-bounded but delay-independent 类分析），“现有工作多为 delay-dependent”的论断未给出明确文献覆盖，GAP 真实性存疑。
- - Major: 相关工作以“AA”与“异步分布式优化”两个独立类别展开，却未调研二者交集的潜在工作（AA + asynchronous、quasi-Newton + async distributed、或 async ADMM-AA），造成“交集未被开拓”的错觉，是利用分类割裂来放大新颖性的常见手法。
### Minor（1）
- - Minor: 实验仅限“convex classification tasks”，贡献声称的“easier to determine, often leads to faster convergence”缺乏对非凸/强凸场景的宽广度，增量优势的普适性论证不足。

## 可复现（repro）— ok
### Critical（3）
- - Critical: 全文未见任何代码仓库链接或匿名代码提交地址，读者无法获取 ADGM-AA 实现源码，整个实验证据链从源头断裂。
- - Critical: 异步分布式方法的核心特征是执行顺序由 worker 完成时间（wall-clock）驱动，具有内在非确定性；论文未说明如何在实验中控制/模拟延迟时序（如固定延迟序列、进程调度快照），导致"异步"这一关键变量不可复现。
- - Critical: 论文以 wall-clock-time 收敛速度作为主要卖点之一，但未提供任何硬件配置（CPU/GPU 型号、核心数、内存、网络带宽/延迟）、集群拓扑、worker 数量 n 的快照，wall-clock 结果在不同机器上无法对齐复现。
### Major（5）
- - Major: 未声明任何随机种子（数据划分、初始化、异步调度中的随机因素），多次运行结果无法对账。
- - Major: 实验所用"convex classification tasks"的具体数据集名称、来源、规模、类别分布、训练/测试划分均未披露，更无数据许可证（如 CC-BY、MIT、专有）声明，存在数据合规与获取障碍。
- - Major: 缺少配置快照：软件栈版本（PyTorch/TensorFlow、MPI/gRPC、CUDA）、固定步长具体取值、Anderson 加速深度 m、safe-guard 阈值、延迟分布参数等超参数均未在可见部分完整列出。
- - Major: 未提供代码/数据的哈希校验（如 commit SHA、数据集 checksum），即使后续补传代码也无法做版本对账，难以锁定被评审的精确版本。
- - Major: 未提供一键复现方案（Docker/Singularity 容器、Makefile、README 跑通脚本），第三方需自行逆向工程环境与超参，复现成本极高。
### Minor（1）
- - Minor: OpenReview 链接格式含空格（`https: // openreview. net/`），无法直接点击，增加定位原始材料的摩擦。

## 写作（writing）— ok
### Critical（1）
- - Critical: **Li & Li (2020) 在相关工作中被矛盾性地分类。** 第1.1.1节将 Li & Li (2020) 与 Mai & Johansson (2020)、Liu et al. (2024) 一并归为"apply AA to the **proximal gradient method**"的工作，但紧接着又单独描述"the work (Li & Li, 2020) first incorporates AA with Chebyshev polynomials and then applies the resulting technique to the *
### Major（2）
- - Major: **摘要中"safe-guard"拼写非标准。** 摘要写为"reference-path-based **safe-guard** scheme"，而优化文献中的标准术语为"**safeguard**"（一个单词，无连字符）。这是全文核心贡献的命名，术语拼写错误会降低正式性。
- - Major: **"incorporate it with AA" / "incorporates AA with" 表达不符合英语习惯。** 摘要写"transform the asynchronous gradient method into a fixed-point iteration, and then **incorporate it with AA**"，相关工作中同样出现"**incorporates AA with** Chebyshev polynomials"。"incorporate A with B"非地道用法，应为"incorporate AA **into**
### Minor（4）
- - Minor: **Anderson 大小写不一致。** 标题为"Anderson **Accelerated** Asynchronous Method"，方法全称为"...with Anderson **Acceleration**"（大写A），但正文中反复使用"Anderson **acceleration** (AA)"（小写a）。术语在文中的大小写应统一。
- - Minor: **摘要与引言高度冗余。** 摘要已阐述"AA is an effective technique for accelerating fixed-point iterations, but it is rarely applied to distributed optimization"，引言相关工作1.1.1又以近乎相同的句式重新定义AA，且引言对贡献的概述（fixed-point 变换+AA+safe-guard+delay-free step-size）与摘要高度重合，缺乏增量信息。
- - Minor: **摘要实验描述与理论贡献的范围不对称。** 摘要实验部分明确限定"convex classification tasks"，但理论部分只说"under mild conditions"而未指明 convex 假设。若理论仅限 convex 情形，摘要应在理论贡献处同步标明，否则暗示理论适用范围更广，构成摘要与正文潜在矛盾。
- - Minor: **OpenReview 链接格式异常。** 首页链接显示为"https: // openreview. net/ forum? id= Nm7dTogzfa"，含多余空格，链接无法直接点击（可能为 PDF 提取副产品，但仍应检查源文件）。

## 伦理（ethics）— ok
### Critical（1）
- - Critical: 论文未声明任何利益冲突（conflict of interest）与资金来源（funding/sponsorship），TMLR 投稿规范要求作者披露资助方与潜在利益冲突，此处完全缺失。
### Major（3）
- - Major: 实验使用"convex classification tasks"但未说明所用数据集名称、来源及数据许可（License），无法判断训练数据是否可合法用于学术发布与再分发。
- - Major: 所提分布式方法以 master-worker 架构在本地数据上训练模型，但全文未讨论梯度/聚合结果可能泄露 worker 私有训练样本的隐私风险（如梯度反演、成员推断），缺乏隐私影响评估。
- - Major: 未包含 Broader Impact / Misuse Risk 章节；加速式异步分布式优化可被用于大规模监控训练或对抗模型拟合等高风险场景，作者未提示潜在误用与缓解措施。
### Minor（2）
- - Minor: 论文采用单盲评审（TMLR 为 single-blind）故公开作者身份不违规，但作者邮箱（licong@sustech.edu.cn 等）与机构同时出现在正文，未在单独元数据字段隔离，存在轻度信息规范问题。
- - Minor: 未提供代码与数据可用性声明（Reproducibility Statement），第三方无法核验实验所用数据许可与来源，削弱合规可追溯性。

## 汇总

- **Critical: 11 | Major: 27 | Minor: 13**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）