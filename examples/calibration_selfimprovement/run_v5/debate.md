# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\calibration_selfimprovement\run_v5\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 6 / Major 7 （撤回 0，部分成立 0）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: OOD gating 分析仅 N=30、未预先定义 OOD 分布、未给出置信区间或功效分析，40 | - | sustained(缺裁保守) |  |
| 2 | Critical | - Critical: “per-row adjudication 后扩展 matcher”得到的 100% accur | - | sustained(缺裁保守) |  |
| 3 | Critical | - Critical: 中心结论基于 N=30 且其中 27 个置信度恰为 1.0 的退化样本，统计功效极低；从如此小的 | - | sustained(缺裁保守) |  |
| 4 | Critical | - Critical: 多重比较与检验选择不透明：只写“95% CIs; only extreme Holm-corre | - | sustained(缺裁保守) |  |
| 5 | Critical | - Critical: 核心证据存在循环性：matcher 是在逐行人工裁决后才“扩展”到 100% 准确率，标签标准与 | - | sustained(缺裁保守) |  |
| 6 | Critical | - Critical: 置信度分布严重退化（27/30 个值恰为 1.0），有效非退化样本仅 3 个，任何 ECE/校准 | - | sustained(缺裁保守) |  |
| 7 | Major | - Major: Keywords 之后的 “Our central finding…” 是游离于任何章节之外的段落，且 | - | sustained(缺裁保守) |  |
| 8 | Major | - Major: MSI 1.000 vs 0.334 只报两个点估计，没有样本量、方差/CI、或统计检验；1.000  | - | sustained(缺裁保守) |  |
| 9 | Major | - Major: free-form 与 MMLU 的 MSI 对比（1.000 vs 0.334）同时混淆了任务格式、 | - | sustained(缺裁保守) |  |
| 10 | Major | - Major: seed 管理缺失：未报告采样/重采样种子，也没有用多 seed 或多独立重复估计解码随机性带来的方差 | - | sustained(缺裁保守) |  |
| 11 | Major | - Major: “ECE 最多相差 4×”是误导性效应量：小 ECE 做分母会放大比率，应结合绝对差（如 0.45）和 | - | sustained(缺裁保守) |  |
| 12 | Major | - Major: 摘要和正文反复称“initially alarming overconfidence signal ( | - | sustained(缺裁保守) |  |
| 13 | Major | - Major: 跨域 ECE 比较混淆了领域、题目难度、模型、样本量及同一题目在多模型间的重复测量依赖；Holm 校正 | - | sustained(缺裁保守) |  |
| 14 | Minor | - Minor: 摘要使用“Propositions 1–3”“Proposition 8′”这类内部编号引用，既未在摘 | - | sustained(缺裁保守) |  |

**辩论后**：维持 Critical 6 / Major 7 / Minor 1；撤回 0 条（假阳性被作者驳回）；部分成立 0 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
