# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\calibration_selfimprovement\run_v1\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 13 / Major 6 （撤回 0，部分成立 1）；注：原始 31 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 11 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - **Critical**: Propositions 1–3 的偏差界依赖匹配器 FNR/FPR（相对真值），但"真 | 将引入真值不可知时FNR/FPR的bootstrap不确定性传播,并以保守上界替代点估计偏差界。 | sustained | concede,估计循环问题存在于当前版本,承诺bootstrap上界未落实 |
| 2 | Critical | - Critical: "ECE 跨域变化达 17×"作为摘要级头条效应量报告，但所给 95% CI（0.028 [0. | 将取消17Ã比值头条,改报ECE差值及CI,并注明比值CI包含1。 | sustained | concede,当前版本仍以17×点估计比值为头条,误导性报告未消除 |
| 3 | Critical | - Critical: GAP 声明"self-reported confidence 的校准很少在 agent 自身任 | 将引用Kadavath(2022),区分其P(True)校准与本文agent任务分布scalar验证。 | sustained | concede,GAP未引用Kadavath且未区分,当前版本问题仍在 |
| 4 | Critical | - Critical: N=30 试点中"逐行裁定后扩展 matcher"达到 100% 准确率，本质是把 matche | 论文已显式标注ECE=0.0037为'in-sample illustrative, not a validated b | partial | 论文确有in-sample标注,但census仅复现degeneracy/matcher-depen |
| 5 | Critical | - Critical: 主试点 N=30 的 ECE 报告至小数点后四位（0.1297、0.0037），且置信分布退化（ | 将ECE精度降至两位小数并注明有效样本量约3。 | sustained | concede,当前版本仍报四位小数且未注有效样本量 |
| 6 | Critical | - Critical: 主试点三个核心 ECE 值（0.363/0.1297/0.0037）均未报告任何不确定性估计（C | 将为0.363/0.1297/0.0037è¡¥åbootstrap CI。 | sustained | concede,当前版本三个核心ECE值无任何不确定性估计 |
| 7 | Critical | - Critical: 因果/定量结论（"40â50% high-confidence OOD 答案错误""conf | 将为N=30å®éç»è®ºè¡¥åCI并将因果措辞改为描述性。 | sustained | concede,当前版本N=30因果措辞仍在且无CI |
| 8 | Critical | - Critical: 大规模人工标注（4999 dual-judged pairs、逐行 adjudication、6 | å°è¡¥åIRB审查、知情同意、报酬及劳动保护声明。 | sustained | concede,当前版本无任何伦理合规声明 |
| 9 | Critical | - Critical: 摘要之后、Introduction 之前有一句孤立的「Our central finding i | 将删悬浮句并在摘要首次出现处定义smECE_sem全称与缩写。 | sustained | concede,当前版本悬浮句与未定义缩写仍在 |
| 10 | Critical | - Critical: 摘要约 450+ 词，远超常规 150â250 词限制；多层嵌套括号与分号长句交织（如 "i | 将摘要压缩至250词内,消除嵌套括号。 | sustained | concede,当前版本摘要超长且嵌套严重 |
| 11 | Critical | - Critical: 无数据许可/模型 ToS 合规声明——MMLU 许可未注明；"Chinese free-form | å°è¡¥åMMLU MIT许可、Chinese set来源及模型ToS研究使用合规声明。 | sustained | concede,当前版本无数据许可与ToS合规声明 |
| 12 | Critical | - Critical: 未提供任何数据许可/可用性声明；MMLU 与“Chinese free-form set”的来源 | å°è¡¥åæ°æ®å¯ç¨æ§å£°æï¼æ³¨æåæ°æ®éæ¥æºãç | sustained | concede,当前版本无数据可用性声明 |
| 13 | Critical | - Critical: 标注流程不可复现。"per-row adjudication of residual error | å°è¡¥åæ æ³¨è§èãæ æ³¨èäººæ°ãCohen's κ及裁定准则文本。 | sustained | concede,当前版本标注规范、κ、裁定准则均缺失 |
| 14 | Critical | - Critical: 门控分析缺少对照组——只比较 confidence-gating vs self-consist | å°è¡¥åæ é¨æ§ãéæºé¨æ§åoracle上界基线。 | sustained | concede,当前版本无对照组基线 |
| 15 | Major | - **Major**: MSI 比较（中文自由形式 1.000 vs MMLU 选择题 0.334）同时混淆语言×作答 | 将拆解语言×格式×领域为消融或限定MSI差异为描述性。 | sustained | concede,当前版本MSI混淆多因素无法归因 |
| 16 | Major | - Major: "40–50% 高置信 OOD 答案错误"基于 30 项探测，实际计数约 12–15 项，无置信区间， | 将为40-50%比例报告Clopper-Pearson CI。 | sustained | concede,当前版本40-50%比例无CI |
| 17 | Major | - Major: "ECE 跨域 4Ã/17Ã"为点估计比值，且作者承认 95% CI 极宽、Holm 校正后仅最极 | 将以ECE差值及比值CI替代点估计比值,注明CI含1。 | sustained | concede,当前版本仍用点估计比值且CI重叠 |
| 18 | Major | - Major: "Proposition~8$'$"（帶撇號編號）於摘要中突然出現，前文僅描述 Proposition | 将统一Proposition编号,删除撇号变体或先定义4-8。 | sustained | concede,当前版本Proposition 8'撇号编号未统一 |
| 19 | Major | - Major: "by up to $4\times$ across three subjects and by up | 将改写为'among 6 domains, max pairwise ECE ratio is 17Ã'。 | sustained | concede,当前版本'six'与'three subjects'关系歧义 |
| 20 | Major | - Major: "自一致性信号优于置信度用于 OOD 门控"与 Wang et al.(2022) Self-Cons | 将引用Wang(2022) Self-Consistency并论证相对增量,标注n=30为探索性。 | sustained | concede,当前版本未引用Wang(2022)且n=30门控结论无统计支撑 |
| 21 | Minor | （另有 11 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 13 / Major 6 / Minor 0；撤回 0 条（假阳性被作者驳回）；部分成立 1 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
