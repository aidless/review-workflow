# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_Nm7dTogzfa\extracted_text.txt`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_Nm7dTogzfa\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 10 / Major 10 （撤回 0，部分成立 0）；注：原始 40 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 20 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - **Critical**: 基准公平性存疑——文中强调自己的"delay-free step-size"比现有方法的 | 将在实验部分补充基准方法delay-dependent步长的网格搜索协议及最优步长选取标准,确保公平对比。 | sustained(缺裁保守) |  |
| 2 | Critical | - **Critical**: 泛化性严重不足——仅在"convex classification tasks"上验证， | 将增加非凸优化（深度学习训练）、回归、非平滑优化场景实验,验证方法泛化性。 | sustained(缺裁保守) |  |
| 3 | Critical | - Critical: **Li & Li (2020) 在相关工作中被矛盾性地分类。** 第1.1.1节将 Li &  | 将修正Li & Li (2020)分类描述,统一归为gradient descent方向,消除与proximal gra | sustained(缺裁保守) |  |
| 4 | Critical | - Critical: 全文未见任何代码仓库链接或匿名代码提交地址，读者无法获取 ADGM-AA 实现源码，整个实验证据 | 将在论文中补充匿名代码仓库链接（含ADGM-AA实现与实验脚本）,于Camera-Ready前公开。 | sustained(缺裁保守) |  |
| 5 | Critical | - Critical: 前提不成立风险——将含随机延迟的异步梯度法当作经典 AA 所要求的确定性、平稳不动点迭代；延迟使 | 论文设计reference-path-based safe-guard确保全局收敛,并证明mild conditions | sustained(缺裁保守) |  |
| 6 | Critical | - Critical: 异步分布式方法的核心特征是执行顺序由 worker 完成时间（wall-clock）驱动，具有内 | 将在实验部分详述延迟模拟协议（延迟序列类型、worker异构参数、调度快照）,确保异步变量可复现。 | sustained(缺裁保守) |  |
| 7 | Critical | - Critical: 摘要核心结论"ADGM-AA improves both iteration-count and | 将补充多次重复试验（n≥10）、均值±标准差及配对t检验,为比较性结论提供统计支撑。 | sustained(缺裁保守) |  |
| 8 | Critical | - Critical: 文猠自己声称“the application of AA to distributed opti | 将GAP收窄为'AA在异步分布式优化中尚未探索',并明确承认Ouyang et al.(2020)已将AA用于ADMM。 | sustained(缺裁保守) |  |
| 9 | Critical | - Critical: 混淆变量与因果归因——safe-guard 回退机制本身可能成为加速来源的混淆变量；若实验中 s | 将增加消融实验:基础异步法 vs AA-only vs AA+safeguard三路对比,隔离各自贡献。 | sustained(缺裁保守) |  |
| 10 | Critical | - Critical: 论文未声明任何利益冲突（conflict of interest）与资金来源（funding/s | 将在论文末尾补充利益冲突声明与资金来源披露,符合TMLR投稿规范。 | sustained(缺裁保守) |  |
| 11 | Major | - **Major**: seed 管理与统计显著性缺失——摘要完全未提及随机种子数量、方差/置信区间、或统计检验；异步 | 将在摘要与实验中报告随机种子数量、方差/置信区间及统计检验结果。 | sustained(缺裁保守) |  |
| 12 | Major | - **Major**: wall-clock-time 对比的前提条件不明——异步方法的墙钟时间强烈依赖于延迟模型的设 | 将明确延迟模型设定依据,并在wall-clock中公平计入AA每步矩阵求解的额外计算开销。 | sustained(缺裁保守) |  |
| 13 | Major | - **Major**: 消融实验不完整——论文提出两个核心组件（Anderson acceleration 本身 +  | 将增加'基础异步法 vs AA-only vs AA+safeguard'三路消融对比,判明性能提升来源。 | sustained(缺裁保守) |  |
| 14 | Major | - **Major**: 结果报道存在选择性偏差嫌疑——"improves...in most test example | 将明确披露成功/失败案例比例,并分析未超越基准的具体场景及原因。 | sustained(缺裁保守) |  |
| 15 | Major | - Major: **"incorporate it with AA" / "incorporates AA with" | 将'incorporate it with AA'改为'apply AA to it',统一全文相关表述。 | sustained(缺裁保守) |  |
| 16 | Major | - Major: ânovel reference-path-based safe-guard scheme”的新颖 | 将与Toth & Kelly 2015、Evans et al. 2018及Mai & Johansson 2020逐项 | sustained(缺裁保守) |  |
| 17 | Major | - Major: “首次将异步梯度法转化为定点迭代”被作为贡献之一，但异步方法作为定点迭代分析是 ARock、异步坐标更 | 文中'we first transform...and then incorporate it with AA'的'fi | sustained(缺裁保守) |  |
| 18 | Major | - Major: 假设过强——"mild conditions" 的含糊表述掩盖了全局收敛对强凸性、光滑性、有界延迟等强 | 将明确列出具体假设（强凸性、光滑性、有界延迟）,并讨论与非凸场景的差距与局限。 | sustained(缺裁保守) |  |
| 19 | Major | - Major: 多重比较未校正——ADGM-AA 同时与多个 baseline 在多个数据集 × 2 个指标（iter | 将对多重比较采用Holm或FDR校正,控制比较矩阵膨胀的假阳性率。 | sustained(缺裁保守) |  |
| 20 | Major | - Major: 所提分布式方法以 master-worker 架构在本地数据上训练模型，但全文未讨论梯度/聚合结果可能 | 将增加隐私影响评估,讨论梯度反演、成员推断风险及潜在缓解措施。 | sustained(缺裁保守) |  |
| 21 | Minor | （另有 20 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 10 / Major 10 / Minor 0；撤回 0 条（假阳性被作者驳回）；部分成立 0 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
