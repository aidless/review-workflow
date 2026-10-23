# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_JQA0EfQIfj\extracted_text.txt`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_JQA0EfQIfj\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 16 / Major 4 （撤回 0，部分成立 0）；注：原始 46 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 26 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: Koopman 理论仅在无穷维观测函数空间下严格保证非线性动力学线性化，论文用有限维学习到的潜在 | - | sustained | 论文确实声称有限维学习潜空间使非线性动力学线性化,Ko pman严格保证需无穷维,方法论前提过度泛化 |
| 2 | Critical | - Critical: OpenReview 链接书写为 `https: // openreview. net/ for | - | sustained | 论文片段中URL确实含空格'https: // openreview. net/ forum? id |
| 3 | Critical | - Critical: seed 管理与统计显著性缺失——在可见文本中无任何多 seed 运行、标准差、置信区间或显著性 | - | sustained | 可见文本无多seed、标准差、置信区间或显著性检验描述,统计支撑缺失属实。 |
| 4 | Critical | - Critical: åºåå ¬å¹³æ§å­çââæè¦ç§°âoutperfor | - | sustained | 摘要称超越所有baseline但baseline为视觉预测方法与CSI瞬时回归器性质不同,公平性存疑 |
| 5 | Critical | - Critical: 三项"创新组件"中 anchor-delta 预测头即残差/零速度预测（Martinez et  | - | sustained | anchor-delta即残差预测、KAL loss等价标准多步+线性一致性损失,二者非方法层创新却 |
| 6 | Critical | - Critical: 作者所屬機構「Middesex University」拼寫錯誤，應為「Middlesex Uni | - | sustained | 论文片段中'Middesex University'确实出现两次,应为'Middlesex',拼写错 |
| 7 | Critical | - Critical: 全文使用 MM-Fi 与 WiPose 两个含人体动作/姿态数据的数据集进行训练与评测,但未出现 | - | sustained | 使用MM-Fi与WiPose人体数据但无IRB/知情同意/合规说明,伦理审查疏漏属实。 |
| 8 | Critical | - Critical: 可见文本（Abstract、作者信息块、Introduction）中未出现任何代码仓库 URL、 | - | sustained | 可见文本无代码仓库URL、commit hash或artifact链接,可复现性证据链缺失属实。 |
| 9 | Critical | - Critical: 声称"robust, consistent performance across both sh | - | sustained | 声称robust/consistent但无方差、标准差或跨horizon离散度报告,统计断言无支撑。 |
| 10 | Critical | - Critical: 摘要声称"outperforming all baselines by a substantia | - | sustained | 'substantial margin'为统计断言但无显著性检验或效应量报告,双重缺失属实。 |
| 11 | Critical | - Critical: 摘要断言 KOALA 在 MM-Fi 与 WiPose 上"outperforming all  | - | sustained | 未见逐组件消融实验隔离各因素因果贡献,内部效度威胁属实。 |
| 12 | Critical | - Critical: 未披露随机种子（random seed / numpy seed / torch manual_ | - | sustained | 未披露任何随机种子设置,数值结果不可复现属实。 |
| 13 | Critical | - Critical: 核心 GAP（"CSI 时序预测几乎未被探索"）可能成立，但填充该 GAP 的主力方法 Deep | - | sustained | Deep Koopman在动力学学习中已成熟,实质为模态迁移却被表述为new paradigm/fu |
| 14 | Critical | - Critical: 缺少任何 dual-use/误用风险讨论。穿墙式人体运动预测天然可用于非知情监控(如非法跟踪住户 | - | sustained | 穿墙式人体运动预测有监控滥用风险,论文仅列正面用途无威胁模型或缓解措施。 |
| 15 | Critical | - Critical: 论文反复声称 WiFi CSI 是"inherently privacy-preserving" | - | sustained | CSI可穿墙推断在场/步态/手势,称'inherently privacy-preserving'误 |
| 16 | Critical | - Minor: 簡介段出現逗號斷句（comma splice）：「share a critical architect | - | sustained | 'share a critical architectural assumption, they o |
| 17 | Major | - Major: "anchor-delta prediction head eliminates the degene | - | sustained | 声称anchor-delta消除shortcut但未验证捷径是否转移到anchor通道,假设成立性未 |
| 18 | Major | - Major: "autoregressive rollouts amplify errors at every st | - | sustained | 将误差放大作为普适前提未给出CSI噪声误差传播定量建模,因果根基薄弱属实。 |
| 19 | Major | - Major: "identity attractor problem inherent from Koopman f | - | sustained | 'identity attractor problem'未对应文献公认定义,命名与现象缺乏可复现依据 |
| 20 | Major | - Major: KAL 损失被宣称"无需 contrastive、spectral、auxiliary losses" | - | sustained | 声称无需contrastive/spectral/auxiliary损失但未证明功能不等价,因果归因 |
| 21 | Minor | （另有 26 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 16 / Major 4 / Minor 0；撤回 0 条（假阳性被作者驳回）；部分成立 0 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
