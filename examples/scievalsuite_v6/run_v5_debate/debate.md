# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\run_v4_fixed\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 15 / Major 1 （撤回 0，部分成立 4）；注：原始 37 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 17 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: "P3 SHA-256 seal over 125 files verifying byte-f | 将披露temperature=0与固定seed协议作为可复现前提,并区分文件哈希密封与结果可复现的适用范围。 | sustained | concede；当前版本未报告temperature/seed,摘要将bootstrap列为futu |
| 2 | Critical | - Critical: "P5 frontier Model-F 得 6/6"未指明是哪个模型/哪个权重文件/哪个 ol | 将补充Model-F的具体模型名称、权重文件与ollama digest,使外部可复现该前沿结果。 | sustained | concede；当前版本Model-F无模型名称/权重/digest,外部无法复现。 |
| 3 | Critical | - Critical: "curated L1a"从 16 个任务中事后挑选 6 个子集再做 Friedman 检验属于 | 将预注册L1a任务子集选择,并将Holm校正扩展至全文所有检验（含McNemar、16任务Friedman、LLM-ju | sustained | concede；当前版本存在事后挑选子集与选择性Holm校正,p-hacking风险未消除。 |
| 4 | Critical | - Critical: L2 对照实验样本量 N=4（仅 3 模型×2 臂×4 场景），McNemar n_d=0、po | 摘要用'no statistically detectable difference'而非'no difference' | partial | 摘要确用'no statistically detectable difference'且披露N=4 |
| 5 | Critical | - Critical: L2 的 $N=4$ 严重欠功效（自报 $d_{\min}=2.1279$、McNemar po | 'no statistically detectable difference'即无检测能力非无差异；摘要同段披露pow | partial | 摘要措辞谨慎且披露power=0,rebot部分成立；但Contributions将零功效结果框为' |
| 6 | Critical | - Critical: LLM-as-judge 在 21 gold 上校准通过（FNR=0/FPR=0），但实际评估轮 | 摘要明确写'zero judge calls (all SKIP) so calibration is a method | partial | 摘要确实承认zero judge calls且定位为methodological warrant,r |
| 7 | Critical | - Critical: LLM-as-judge 校准用到 "21 gold""39 gold（26 real + 13 | 将补充IRB/伦理委员会批准状态、标注员知情同意、报酬与劳动保护披露。 | sustained | concede；当前版本无IRB/知情同意/报酬披露,伦理规范缺失。 |
| 8 | Critical | - Critical: McNemar 检验在 $n_d=0$（零不一致对）时是退化/未定义的，报告 $p=1.0000 | 将标注n_d=0时McNemar退化为无信息量,p=1.0000不作无差异证据,仅报告零不一致对。 | sustained | concede；当前版本n_d=0时McNemar退化,p=1.0000误导性未标注。 |
| 9 | Critical | - Critical: P5 frontier Model-F（6/6, p=0.0026）作为探索性结果被引入，但未提 | 将补充Model-F配置快照、托管环境、模型权重哈希与ollama tag,补全证据链。 | sustained | concede；当前版本Model-F无配置快照/环境/权重哈希/ollama tag,证据链断裂。 |
| 10 | Critical | - Critical: intention-to-treat 均值 0.355 无法从所给分量推出。若 "0.2000Ã | 将逐项核实ITT各分量并重算均值,修正不自恰的0.355,确保可由分量推出。 | sustained | concede；当前版本0.355无法从分量推出,数字不自洽。 |
| 11 | Critical | - Critical: seed 管理缺失——仅对 gemma 做"3 次独立试验"，bootstrap at step | 将补充固定seed协议、跨seed方差报告,并将step/seed bootstrap从future work提前实施。 | sustained | concede；当前版本bootstrap列为future work,无固定seed协议与跨seed |
| 12 | Critical | - Critical: 三个子基准 AIRS-Bench、ResearchClawBench、GAIA2 均为既有外部数 | Introduction写'The contribution is not a new model but a meas | partial | 引言确实定位为measurement instrument,rebut成立；但三子基准均为既有数据集 |
| 13 | Critical | - Critical: 双盲去标识不足——摘要明确写出云平台"AutoDL RTX3090"、框架版本"ollama 0 | 将移除AutoDL、ollama版本号及内部代号,改用匿名化描述以符合TMLR G3。 | sustained | concede；当前版本含AutoDL/ollama版本/内部代号,违反TMLR G3匿名要求。 |
| 14 | Critical | - Critical: 哈希对账自相矛盾——"P3 SHA-256 seal over 125 underlying f | 将澄清125文件与91条目的关系,并在补充材料中发布逐文件SHA-256 manifest。 | sustained | concede；当前版本125文件与91条目关系未澄清,无逐文件manifest可对账。 |
| 15 | Critical | - Critical: 在 16 任务 Friedman 非显著（$p=0.3679$）的情况下仍报告 Nemenyi  | 将标注omnibus非显著时Nemenyi CD仅为描述性不作推断,或移除该事后比较。 | sustained | concede；当前版本omnibus非显著时仍报告Nemenyi CD,无统计意义。 |
| 16 | Critical | - Critical: 数据许可完全缺失——AIRS-Bench、ResearchClawBench、GAIA2 及"1 | 将为AIRS-Bench、ResearchClawBench、GAIA2及合成gold数据补充许可证与来源授权声明。 | sustained | concede；当前版本三数据集及合成gold均无许可证声明。 |
| 17 | Critical | - Critical: 显著性结果 p=0.0026 来自"curated L1a（6 tasks, k=4）"的事后挑 | 将Holm校正扩展至全部已执行检验（含退化检验）,不再按是否退化选择纳入校正族。 | sustained | concede；当前版本按是否退化选择Holm校正族,选择性校正致p=0.0261不可信。 |
| 18 | Critical | - Critical: 涉及人工标注(single annotator, 21/39 gold)却无 IRB/伦理审查声 | 将补充伦理审查声明、标注员知情同意、报酬与劳动保护披露,覆盖全部gold标注。 | sustained | concede；当前版本无伦理审查/知情同意/报酬披露。 |
| 19 | Critical | - Critical: 缺乏真正的对照组/参考基线——L1b 三个模型全部 0/10，仅靠 Chemistry_000  | 将增加API模型在L1b上的ceiling参考基线,建立floor/ceiling以判断0/10成因。 | sustained | concede；当前版本L1b三模型0/10无API ceiling基线,无法判断0/10成因。 |
| 20 | Major | - Major: "18/18 independent recomputation checks passing" 中  | 将明确'independent'定义（异机/异硬件/异pull日期）,或如实说明为同实例重现。 | sustained | concede；当前版本'independent'未定义,可能为同实例重现而非复现。 |
| 21 | Minor | （另有 17 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 15 / Major 1 / Minor 0；撤回 0 条（假阳性被作者驳回）；部分成立 4 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
