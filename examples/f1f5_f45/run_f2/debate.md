# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f2\extracted_text.txt`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f2\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 13 / Major 5 （撤回 0，部分成立 0）；注：原始 21 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 1 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: c0=0.05 是在 K=3 pilot 上拟合的，却用“all cells”包括 K=3 来验 | - | sustained | 作者未回应,未提供反驳或引用；按规则维持该问题,待修订。 |
| 2 | Critical | - Critical: seed 协议不可复现：正文称每 cell 用 10 seeds，却只明确写出 42 与 42– | - | sustained | 作者未回应,未说明 seed 协议；无可核验的 rebut,维持。 |
| 3 | Critical | - Critical: 下界 B 的 c0 在 K=3 的 pilot 数据上拟合，却又在包含同一 K=3 数据的所有  | - | sustained | 作者未回应,样本内验证问题无反驳证据,维持。 |
| 4 | Critical | - Critical: 将 270 episodes × 10 seeds 当作 2,700 个独立“cells”，忽略 | - | sustained | 作者未回应,相关性高估样本量问题未被反驳,维持。 |
| 5 | Critical | - Critical: 引理“Cmin(K) 在 exchangeability 且 ρ<1 下单调非降”并非由这些前提 | - | sustained | 作者未回应,未给出引理充分条件或证明,维持。 |
| 6 | Critical | - Critical: 报告“0.68% improvement”的 95% Wilson CI [0.62,0.74] | - | sustained | 作者未回应,统计方法选择与预注册问题未解释,维持。 |
| 7 | Critical | - Critical: 摘要与引言混入大量审稿回复/复现检查式内容（“P0 26-block F1 24K→12K”、“ | - | sustained | 作者未回应,摘要混入审稿痕迹问题未处理,维持。 |
| 8 | Critical | - Critical: 摘要中 “P/B 5–10× for γ∈{0.5,1.0}” 与 “median 10.88× | - | sustained | 作者未回应,数字冲突无解释,维持。 |
| 9 | Critical | - Critical: 摘要和贡献列表写 “inverse variance decreases (Fisher-lik | - | sustained | 作者未回应,术语自相矛盾未澄清,维持。 |
| 10 | Critical | - Critical: 未提供任何可下载仓库、容器/依赖锁文件或一键复现命令；只声称“Gates 9/9 锚定到 L40 | - | sustained | 作者未回应,可复现性与行号验证问题未解决,维持。 |
| 11 | Critical | - Critical: 核心理论贡献只是“相关随机变量均值方差公式”和“多数/一致覆盖随 K 变化”的改写；把 `1/[ | - | sustained | 作者未回应,理论贡献质疑无反驳,维持。 |
| 12 | Critical | - Critical: 核心验证存在循环风险：B 的 c0 是在 K=3 pilot 上拟合的，随后又在包含 K=3 的 | - | sustained | 作者未回应,循环验证风险未说明数据切分,维持。 |
| 13 | Critical | - Critical: 正文残留 “P0 26-block F1 24K→12K”“Ledger 86 PASS”“Ga | - | sustained | 作者未回应,匿名性/串稿风险未澄清,维持。 |
| 14 | Major | - Major: P = Rsel·Cmin 把风险与覆盖率相乘，K 或 γ 改变时会通过覆盖率产生机械性变化；没有报告 | - | sustained | 作者未回应,P 的机械性缩放问题未回应,维持。 |
| 15 | Major | - Major: 引言末尾突然插入 “P0 26-block F1 24K→12K”“Panorama 6-figure | - | sustained | 作者未回应,引言未定义内容破坏结构问题未处理,维持。 |
| 16 | Major | - Major: 摘要先说 P 随 K 从 K=1 到 K≥3 增大，又说 “K-Verifier ensemble i | - | sustained | 作者未回应,improvement 定义与方向矛盾未解释,维持。 |
| 17 | Major | - Major: 正文/摘要没有规范的图、表编号和正文引用；“Panorama 6-figure set”和 “Ledg | - | sustained | 作者未回应,图表编号与定位缺失未解决,维持。 |
| 18 | Major | - Major: 隐私与人类受试者合规缺失：文中出现 “survey 0/15 zero-success case”，若 | - | sustained | 作者未回应,隐私与合规问题无说明,维持。 |
| 19 | Minor | - Minor: 0/15 的 Wilson 区间并非退化区间；若用“CI degenerate”作为不报告或调整结果的 | - | sustained | 作者未回应,Wilson 区间退化问题未反驳,维持。 |
| 20 | Minor | - Minor: “sample-descriptive”在摘要中反复出现并与“lower bound”连用，造成术语冗 | - | sustained | 作者未回应,术语冗余文体问题无修订说明,维持。 |
| 21 | Minor | （另有 1 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 13 / Major 5 / Minor 2；撤回 0 条（假阳性被作者驳回）；部分成立 0 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
