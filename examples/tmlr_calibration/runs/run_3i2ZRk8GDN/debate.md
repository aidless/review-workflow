# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_3i2ZRk8GDN\extracted_text.txt`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_3i2ZRk8GDN\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 14 / Major 6 （撤回 0，部分成立 0）；注：原始 49 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 29 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: "combined scorer" 被作为核心方法贡献提出（"novel combined sc | 将在方法部分补充组合scorer信息融合策略的机制说明,明确区别于标准stacking的创新点。 | sustained(缺裁保守) |  |
| 2 | Critical | - Critical: 仅 110 个样本、13 个打分器作为特征训练组合器，样本维度比约 8.5:1，极易过拟合；未提 | 将加入L2正则化、特征选择及嵌套交叉验证,并报告留出集泛化性能以缓解过拟合。 | sustained(缺裁保守) |  |
| 3 | Critical | - Critical: 全文存在大量编码/连字符损坏（ligature 损坏）："e!cient"（efficient） | 将以UTF-8重新生成PDF,修复全部ligature编码损坏（e!cientâefficient等）。 | sustained(缺裁保守) |  |
| 4 | Critical | - Critical: 无哈希对账；10 种架构、11 个数据集、预训练权重均未给出 SHA256/MD5 校验和，To | 将为10架构、11数据集及预训练权重补充SHA256校验和清单及具体版本号。 | sustained(缺裁保守) |  |
| 5 | Critical | - Critical: 未对所用预训练模型（Torchvision、Hugging Face 仓库中的 10 种架构）的 | 将逐一核查并披露所有预训练模型及数据集的许可条款,标注license类型及合规性。 | sustained(缺裁保守) |  |
| 6 | Critical | - Critical: 未提供一键复现路径；可见部分仅给出 Torchvision/HuggingFace 主页链接，未 | 将提供代码仓库、environment.yml、运行脚本及容器镜像的一键复现路径。 | sustained(缺裁保守) |  |
| 7 | Critical | - Critical: 未提供配置快矧（configuration snapshot）；“standardized ev | 将公开协议全部配置:学习率、batch size、epoch、优化器、数据划分及增强策略。 | sustained(缺裁保守) |  |
| 8 | Critical | - Critical: 样本非独立。10×11=110 个 (模型, 数据集) 配对中，同一模型跨 11 个数据集、同一 | 将以混合效应模型或聚类bootstrap重新检验,以模型和数据集为随机效应。 | sustained(缺裁保守) |  |
| 9 | Critical | - Critical: 组合 scorer 的评估存在数据泄漏/过拟合风险。若组合 scorer 在参与评估的同一批 1 | 将引入留一数据集/留一架构交叉验证,组合器权重仅在训练fold上学习。 | sustained(缺裁保守) |  |
| 10 | Critical | - Critical: 组合打分器声称"一致地优于所有单打分器与基线"，但其训练/调参与评测若共用同一批 11 数据集× | 将说明组合器权重在评测集外学习,采用留出集或k-fold交叉验证协议。 | sustained(缺裁保守) |  |
| 11 | Critical | - Critical: 组合打分器（combined scorer）"利用多个单打分器信息"且"始终优于所有单打分器与基 | 将实施留一数据集与留一架构交叉验证,组合器训练与评估使用独立fold。 | sustained(缺裁保守) |  |
| 12 | Critical | - Critical: 论文使用 ImageNet、PASCAL VOC、SUN397 等 11 个数据集，但全文未见任 | 将为11个数据集补充许可合规声明,标注license类型及肖像权风险说明。 | sustained(缺裁保守) |  |
| 13 | Critical | - Critical: 论文宣称"领域缺少标准化评估协议"作为核心 GAP，但 Pándy et al. (2022)（ | 论文已举具体反例:LEEP在Pándy(2022)中最佳却在Agostinelli(2022)中垫底,证明跨研究协议不统 | sustained(缺裁保守) |  |
| 14 | Critical | - Critical: 通篇可见部分未提及任何随机种子（random seed）设定；微调、特征提取、scorer 计算 | 将公开全部实验随机种子设定,确保排名结果可精确复现。 | sustained(缺裁保守) |  |
| 15 | Major | - Major: "source accuracy baseline 出乎意料地优于大多数现有 scorer"被当作关键 | 论文已引用Kornblith et al.(2019)并写明âPrior work...showed that th | sustained(缺裁保守) |  |
| 16 | Major | - Major: Abstract 与 Introduction 多次声称"best scorer in one stu | 论文已给出可验证实例:LEEP在Pándy et al.(2022)中最佳、在Agostinelli et al.(20 | sustained(缺裁保守) |  |
| 17 | Major | - Major: ground-truth 迁移性能需对每个 (model, dataset) 对做微调，微调本身随机； | 将对每对(model,dataset)多seed微调并报告Kendall-Ï均值与方差。 | sustained(缺裁保守) |  |
| 18 | Major | - Major: 以源任务准确率作为基线存在严重混淆：当所有候选模型同源（如均 ImageNet 预训练）时，源准确率差 | 将在源准确率相近子集上做压力测试,分析基线判别力,排除容量伪迹混淆。 | sustained(缺裁保守) |  |
| 19 | Major | - Major: 基线公平性问题——源任务准确率基线完全不需访问目标数据，而所有 transferability sco | 将在信息量对等条件下设计对比实验,并在难区分场景下做压力测试。 | sustained(缺裁保守) |  |
| 20 | Major | - Major: 多重比较未校正。组合 scorer 同时与 13 个 scorer + 1 基线 = 14 个对手逐对 | 将对14次多重比较进行Bonferroni/FDR校正并报告校正后显著性。 | sustained(缺裁保守) |  |
| 21 | Minor | （另有 29 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 14 / Major 6 / Minor 0；撤回 0 条（假阳性被作者驳回）；部分成立 0 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
