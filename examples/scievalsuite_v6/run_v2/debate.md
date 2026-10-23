# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\run_v2\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 15 / Major 0 （撤回 0，部分成立 5）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - **Critical**: "curated L1a (6 tasks, k=4) gives p=0.0026 * | 移除摘要中p=0.0026的呈现,仅在sensitivity分析中并列报告全部encoding结果,明确标注双重post | sustained | 作者concede承诺修改但论文摘要仍列p=0.0026,未落实 |
| 2 | Critical | - **Critical**: "simulated second annotator Î±=0.894" 并非真实人间 | 删除将模拟α=0.894作为校准可靠性证据的表述,明确标注为模拟值而非真实人间一致性,停止循环论证。 | sustained | 作者concede但论文仍以模拟α=0.894作校准证据,未落实 |
| 3 | Critical | - **Critical**: L1b 全部三个模型得分 0/10，零方差，无法区分"模型无能力"与"基准不可解"；po | 扩展positive control至全部10个L1b任务并补充专家基线,以区分模型无能力与基准不可解。 | sustained | 作者concede承诺扩展positive control但论文仍仅1/4,未落实 |
| 4 | Critical | - **Critical**: L1b 的 LLM-as-judge 在实际评分中"made zero judge ca | 补充L1b非SKIP的judge评分实例,建立从校准到实际评分的有效证据链,明确0/10归因。 | sustained | 作者concede承诺补充judge实例但论文仍all SKIP,未落实 |
| 5 | Critical | - **Critical**: L2 "no statistically detectable difference b | 论文摘要用'no statistically detectable difference'及'n_d=0<6 not-d | partial | 措辞较审稿人所言更谨慎,但摘要仍将零功率结果作为发现呈现 |
| 6 | Critical | - **Critical**: L2 结论"无统计学差异"在 N=4、n_d=0（零不一致对）、McNemar 功效=0 | 论文标注'not-detectable'并披露power=0.0000；n_d=0即配对结果完全相同为观察事实而非统计推 | partial | 同#5,含not-detectable措辞部分回应,但仍作为发现呈现 |
| 7 | Critical | - **Critical**: LLM-as-judge 校准（21 gold, FNR=0/FPR=0）与实际评分完全 | 增设hold-out验证集,报告hold-out上FNR/FPR,避免21样本上FNR=FPR=0的过拟合。 | sustained | 作者concede承诺设hold-out但论文无hold-out验证集,未落实 |
| 8 | Critical | - **Critical**: âUnification”实质上是把三个已有 benchmark（AIRS-Benc | 新增与AgentBench、ML-Bench、ScienceWorld的逐项对比表,明确run.json契约与统计协议的 | sustained | 作者concede承诺加对比表但论文未含,未落实 |
| 9 | Critical | - **Critical**: 全文未报告任何 seed 管理策略；"bootstrap at step/seed le | 补充seed管理策略（固定seed列表）,将bootstrap从future work提升为主实验,记录36次extra | sustained | 作者concede但论文明言bootstrap为future work,seed未控制 |
| 10 | Critical | - **Critical**: 多重检验（McNemar + Wilcoxon + Friedman + Nemenyi | 对全部6+次检验应用BH-FDR校正,报告校正后p值,重新评估p=0.0026的显著性。 | sustained | 作者concede承诺BH-FDR但论文无多重校正,未落实 |
| 11 | Critical | - **Critical**: 引言声称科学 agent "advancing rapidly" 却引用 `\citep | 替换goodfellow2016deep为科学agent综述引用；为fragmentation GAP补充2-3篇分段评 | sustained | 作者concede但论文仍引goodfellow2016deep,未落实 |
| 12 | Critical | - Critical: "P5 frontier muse-spark-1.2-contributor" 命名后缀 "- | 将模型重命名为匿名标识如Model-P5,添加COI声明,披露作者与该模型的关系。 | sustained | 作者concede但论文仍显示-contributor命名及6/6结果,未落实 |
| 13 | Critical | - Critical: 95% CI [0,0] 因配对结果完全相同而退化为零宽度，这不是有效精度估计而是零方差的数学产 | 移除摘要中95%CI[0,0]报告,或明确标注为零方差数学产物而非有效精度估计。 | partial | 论文已标注degenerate部分回应,作者承认需进一步处理 |
| 14 | Critical | - Critical: L2 主检验用 exact McNemar，但 discordant pairs n_d=0（零 | 论文摘要已标注'n_d=0<6 not-detectable',措辞与审稿人建议的'检验无法提供信息'一致,未声称'无差 | partial | 论文含not-detectable措辞部分回应,但仍作为发现呈现 |
| 15 | Critical | - Critical: LLM-as-judge 校准在 21 gold 上 FNR=0/FPR=0，但该轮实际零 ju | 论文明确'calibration is a methodological warrant'并披露'zero judge  | partial | 校准确在21gold上有观测非零观测,但实际评分脱节仍在 |
| 16 | Critical | - Critical: LLM-as-judge 该轮"zero judge calls (all SKIP)"，校准仅 | 公开校准数据集与脚本,确保复现者可复跑21 gold校准并验证FNR/FPR。 | sustained | 作者concede承诺公开校准数据但论文未含,未落实 |
| 17 | Critical | - Critical: SHA-256 manifest 数量自相矛盾——正文称"46-entry manifest"， | 明确46为主实验manifest条目数、165为含P5扩展总数,定义P5含义并指定权威快照。 | sustained | 作者concede但论文仍同时列46和165未澄清,未落实 |
| 18 | Critical | - Critical: gemma 的 intention-to-treat mean 0.355 無法由給定分量算出： | 重新核算gemma ITT mean,修正0.355为正确值(0.278),并公开逐trial分量供独立验证。 | sustained | 作者承认0.355错误应修正为0.278,论文仍显示错误值 |
| 19 | Critical | - Critical: p=0.0026 仅在"fail-as-worst encoding"下成立、其余编码不显著—— | 在sensitivity分析中并列报告全部encoding方案的p值,停止选择性呈现唯一显著者。 | sustained | 作者concede但论文仍only under唯一显著编码,未落实 |
| 20 | Critical | - Critical: 三个基准 AIRS-Bench / ResearchClawBench / GAIA2 均未披露 | 补充AIRS-Bench、ResearchClawBench、GAIA2各自的许可证与再分发条款。 | sustained | 作者concede承诺补许可证但论文未含,未落实 |
| 21 | Minor | （另有问题超出 20 条上限被截断，未参与辩论） | 修订中纳入被截断问题,逐一回应。 | sustained | 仅承诺纳入被截断问题,无具体内容 |

**辩论后**：维持 Critical 15 / Major 0 / Minor 1；撤回 0 条（假阳性被作者驳回）；部分成立 5 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
