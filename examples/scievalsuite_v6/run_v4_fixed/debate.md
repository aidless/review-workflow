# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\run_v4_fixed\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 19 / Major 1 （撤回 0，部分成立 0）；注：原始 37 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 17 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: "P3 SHA-256 seal over 125 files verifying byte-f | - | sustained | 摘要自报seed/bootstrap为future work,无固定温度/种子协议；SHA-256仅 |
| 2 | Critical | - Critical: "P5 frontier Model-F 得 6/6"未指明是哪个模型/哪个权重文件/哪个 ol | - | sustained | 摘要仅称'Model-F scored 6/6',未给出模型名/权重/digest/ollama t |
| 3 | Critical | - Critical: "curated L1a"从 16 个任务中事后挑选 6 个子集再做 Friedman 检验属于 | - | sustained | 从16任务事后挑选6个做Friedman属选择偏差；Holm仅覆盖'两个非退化编码',刻意缩小校正族 |
| 4 | Critical | - Critical: L2 对照实验样本量 N=4（仅 3 模型×2 臂×4 场景），McNemar n_d=0、po | - | sustained | N=4、n_d=0、power=0.0000、CI[0,0]退化,实验自报即无法检出任何效应,对照实 |
| 5 | Critical | - Critical: L2 的 $N=4$ 严重欠功效（自报 $d_{\min}=2.1279$、McNemar po | - | sustained | power=0.0000却将'no statistically detectable differe |
| 6 | Critical | - Critical: LLM-as-judge 在 21 gold 上校准通过（FNR=0/FPR=0），但实际评估轮 | - | sustained | judge在gold上FNR/FPR=0但实际轮次零调用全SKIP,校准集与部署集脱节,内部效度归零 |
| 7 | Critical | - Critical: LLM-as-judge 校准用到 "21 gold""39 gold（26 real + 13 | - | sustained | single annotator标注21/39 gold,论文未提及IRB/知情同意/报酬披露,人体 |
| 8 | Critical | - Critical: McNemar 检验在 $n_d=0$（零不一致对）时是退化/未定义的，报告 $p=1.0000 | - | sustained | n_d=0时McNemar退化/未定义,p=1.0000不提供任何信息量,作为'无差异'证据具误导性 |
| 9 | Critical | - Critical: P5 frontier Model-F（6/6, p=0.0026）作为探索性结果被引入，但未提 | - | sustained | Model-F不属于三个本地模型,摘要未给配置快照/托管环境/权重哈希/ollama tag,证据链 |
| 10 | Critical | - Critical: intention-to-treat 均值 0.355 无法从所给分量推出。若 "0.2000Ã | - | sustained | 核算:0.2×3+0.533×2=1.666；/6=0.278、/5=0.333,均≠0.355；I |
| 11 | Critical | - Critical: seed 管理缺失——仅对 gemma 做"3 次独立试验"，bootstrap at step | - | sustained | 仅gemma'3次独立试验',bootstrap列为future work,无固定seed协议、无跨 |
| 12 | Critical | - Critical: 三个子基准 AIRS-Bench、ResearchClawBench、GAIA2 均为既有外部数 | - | sustained | 三个子基准均为既有外部数据集,实质贡献为编排外壳+run.json+SHA-256封印,摘要却包装为 |
| 13 | Critical | - Critical: 双盲去标识不足——摘要明确写出云平台"AutoDL RTX3090"、框架版本"ollama 0 | - | sustained | 摘要写出AutoDL RTX3090、ollama 0.32.13及大量内部代号,足以反查作者,违反 |
| 14 | Critical | - Critical: 哈希对账自相矛盾——"P3 SHA-256 seal over 125 underlying f | - | sustained | 125文件与91条目关系未澄清,无manifest/逐文件哈希列表,'byte-for-byte r |
| 15 | Critical | - Critical: 在 16 任务 Friedman 非显著（$p=0.3679$）的情况下仍报告 Nemenyi  | - | sustained | Friedman omnibus非显著(p=0.3679)时仍报告Nemenyi CD=0.8284 |
| 16 | Critical | - Critical: 数据许可完全缺失——AIRS-Bench、ResearchClawBench、GAIA2 及"1 | - | sustained | 三个外部数据集及合成gold均未声明许可证与来源授权,复现者无法合法获取/再分发。 |
| 17 | Critical | - Critical: 显著性结果 p=0.0026 来自"curated L1a（6 tasks, k=4）"的事后挑 | - | sustained | p=0.0026来自事后挑选6任务；Holm仅覆盖'两个非退化编码',按退化与否决定纳入属选择性校正 |
| 18 | Critical | - Critical: 涉及人工标注(single annotator, 21/39 gold)却无 IRB/伦理审查声 | - | sustained | single annotator标注21/39 gold,无IRB/伦理审查/知情同意/劳酬披露,不 |
| 19 | Critical | - Critical: 缺乏真正的对照组/参考基线——L1b 三个模型全部 0/10，仅靠 Chemistry_000  | - | sustained | L1b三模型全0/10,仅Chemistry_000 1/4阳性对照,未建立floor/ceilin |
| 20 | Major | - Major: "18/18 independent recomputation checks passing" 中  | - | sustained | 'independent recomputation'未定义是否异机/异硬件/异pull日期,若同A |
| 21 | Minor | （另有 17 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 19 / Major 1 / Minor 0；撤回 0 条（假阳性被作者驳回）；部分成立 0 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
