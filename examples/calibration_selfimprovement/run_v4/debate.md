# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\calibration_selfimprovement\run_v4\r6_llm.json`
- RPC：HTTP 200
- 结论：**SKIP** —— 作者会话失败：timeout

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: 1159/4999 pairs 中同一 item、同一 model 的重复观测被当作独立样本做  | - | sustained(缺裁保守) |  |
| 2 | Critical | - Critical: 30 个样本中有 27 个置信度恰为 1.0，分布已退化，却仍把 ECE 报到 0.363/0. | - | sustained(缺裁保守) |  |
| 3 | Critical | - Critical: 主贡献“matcher 决定可测校准”并非新 GAP：语义等价/LLM-as-judge 与 e | - | sustained(缺裁保守) |  |
| 4 | Critical | - Critical: 将 N=30 的 OOD gating 探索结果当作证据，40–50% 的“高置信 OOD 答错 | - | sustained(缺裁保守) |  |
| 5 | Critical | - Critical: 核心结论建立在 N=30 的 in-sample 数据上，且 “extended matcher | - | sustained(缺裁保守) |  |
| 6 | Critical | - Critical: 用同一批 30 条样本逐行 adjudication 构造 matcher 后又用同一批数据计算 | - | sustained(缺裁保守) |  |
| 7 | Critical | - Critical: 用同一批数据逐行裁决后再扩展 matcher，再用该 matcher 回算 100% accur | - | sustained(缺裁保守) |  |
| 8 | Major | - Major: 4999 pairs 来自 600 items × 9 models，同一 item 被多个模型重复评 | - | sustained(缺裁保守) |  |
| 9 | Major | - Major: MSI 1.000 vs 0.334 只有点估计，无样本量、不确定性区间或重抽样结果，protocol | - | sustained(缺裁保守) |  |
| 10 | Major | - Major: OOD-gating 的“grounding”仅来自 N=30 的探索性分析，并依赖“confiden | - | sustained(缺裁保守) |  |
| 11 | Major | - Major: smECE_sem 与 MSI 没有与既有 binning-free 校准量（Brier score、 | - | sustained(缺裁保守) |  |
| 12 | Major | - Major: “ECE varies up to 4×”用比值作为效应量在基线 ECE 接近 0 或置信度退化时极不 | - | sustained(缺裁保守) |  |
| 13 | Major | - Major: “cross-domain MMLU collection” 未说明 MMLU 版本、split、题目 | - | sustained(缺裁保守) |  |
| 14 | Major | - Major: “per-row adjudication”涉及人工判断，但未说明裁决者资质、独立性、样本量、报酬/同 | - | sustained(缺裁保守) |  |
| 15 | Major | - Major: “varies up to 4× across subjects and up to 0.45 abs | - | sustained(缺裁保守) |  |
| 16 | Major | - Major: 从“仅极端 Holm-corrected pairs significant”推出“calibrati | - | sustained(缺裁保守) |  |
| 17 | Major | - Major: 摘要从 Propositions 1–3 直接跳到 Proposition 8′，未交代 4–7；若正 | - | sustained(缺裁保守) |  |
| 18 | Major | - Major: 泛化证据不足：OOD 分析仅 30 条 exploratory 样本，且跨域结论仅来自 MMLU 单一 | - | sustained(缺裁保守) |  |
| 19 | Major | - Major: 消融不完整：MSI、semantic soft-label estimator、binning-fre | - | sustained(缺裁保守) |  |
| 20 | Major | - Major: 缺少门控任务的对照组：没有 random gating、always-defer、oracle、纯 c | - | sustained(缺裁保守) |  |
| 21 | Minor | （另有 5 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |