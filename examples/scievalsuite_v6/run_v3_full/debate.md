# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\run_v3_full\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 10 / Major 1 （撤回 5，部分成立 4）；注：原始 38 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 18 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - **Critical**: AIRS-Bench / ResearchClawBench / GAIA2 三套派生/ | 将补充AIRS-Bench/ResearchClawBench/GAIA2三套数据集许可证信息,明确再分发与重跑权利。 | sustained | concede,三套数据集许可证未披露,待修订 |
| 2 | Critical | - **Critical**: L2 的 exact McNemar 检验 $n_d=0$（零不一致对），检验统计量退化 | 摘要用"no statistically detectable difference"非"等价",显式标注n_d=0<6 | withdrawn | 摘要写'no statistically detectable difference'非'等价',已 |
| 3 | Critical | - **Critical**: curated L1a 的 $p=0.0026$ 仅在"fail-as-worst en | 将对多种编码方案做Holm-Bonferroni多重比较校正,并强化exploratory定性。 | sustained | concede,未做多编码多重比较校正,p值当前版本不可信 |
| 4 | Critical | - Critical: "simulated second annotator α=0.894"——模拟标注者需要 se | 将披露模拟标注者的seed与模拟模型设定,使α=0.894可对账复现。 | sustained | concede,模拟标注者seed与模型未披露,α不可对账 |
| 5 | Critical | - Critical: L1b 所有模型 0/10，positive control 仅 Chemistry_000 1 | 将增加L1b正控任务数（不止Chemistry_000单例1/4）,排除任务不可解/harness缺陷混淆。 | sustained | concede,L1b正控仅Chemistry_000单例1/4,混淆未排除 |
| 6 | Critical | - Critical: L2 主对比 A vs F 仅 N=4，McNemar 功率显式为 0.0000，n_d=0<6 | 摘要写"no statistically detectable difference"非"无差异",并披露power 0 | withdrawn | 摘要披露power=0.0000、N=4、n_d=0<6,用'not detectable'非'无差 |
| 7 | Critical | - Critical: LLM-as-judge 在主轮次中零次调用（all SKIP），校准（21 gold，sing | 摘要明写"zero judge calls (all SKIP) so calibration is a methodo | partial | judge未实际运行是真限制,但论文已透明披露zero calls与'methodological  |
| 8 | Critical | - Critical: LLM-as-judge 校准仅 21 样本（11/10），FNR=0/FPR=0 但真实 FP | 摘要已报"Wilson 0.28 at FPR=0"暴露宽CI,并标"methodological warrant",未 | withdrawn | 论文未称校准可外推,已报Wilson 0.28暴露宽CI并标'warrant' |
| 9 | Critical | - Critical: P5 gold 计数矛盾："39 gold, 30 real+9 synthetic+1 att | 将修正P5 gold计数:30+9+1=40≠39,核对并统一口径。 | sustained | concede,30+9+1=40≠39计数矛盾待修正 |
| 10 | Critical | - Critical: SHA-256 清单条目数前后不一致——"46-entry manifest"与"165 ent | 将说明46→165系P5阶段扩充,明确哈希对账范围与口径。 | sustained | concede,46与165条目关系未说明,口径不清 |
| 11 | Critical | - Critical: ollama 模型的量化精度（Q4/Q8/FP16）未报告，7b/14b/9b 在不同精度下性能 | 将报告各ollama模型量化精度（Q4/Q8/FP16）,确保公平性与可复现性。 | sustained | concede,ollama量化精度未报告,影响公平性 |
| 12 | Critical | - Critical: seed 管理完全缺失——摘要明确写"bootstrap at step/seed level  | Introduction写"per-seed rows"按种子报告；摘要报"three independent tria | partial | 论文报per-seed rows和three trials非完全缺失,但种子级稳定性验证未做 |
| 13 | Critical | - Critical: åå¿åé£é©ï¼è¿åä¸º TMLR double-blindï¼G3ï¼ï¼ä½ mus | 将匿名化muse-spark模型名并泛化技术栈细节,以符合TMLR double-blind要求。 | sustained | concede,模型名含contributor及技术栈细节违反double-blind |
| 14 | Critical | - Critical: æª«ª»é¢çå©çºå®ï¼æ¨¡åmuse-spark-1.2-contributor å | 将补充COI声明,澄清作者与muse-spark关系及模型访问/授权信息。 | sustained | concede,COI未声明,作者与muse-spark关系未澄清 |
| 15 | Critical | - Critical: 全文宣称"byte-for-byte reproducibility"，但未披露任何 LLM 采 | 将披露LLM采样参数（seed/temperature/top-p）,确认ollama seed已固定以支持逐字节复现。 | sustained | concede,LLM采样seed/temperature/top-p未披露,逐字节复现不成立 |
| 16 | Critical | - Critical: 摘要自相矛盾——LLM-as-judge 声称"passed at FNR=0.0000, FP | 摘要"passed"指21 gold校准阶段；"zero calls"指主轮；"though...so methodol | withdrawn | FNR/FPR来自21 gold校准阶段有分母,零调用属主轮,'though...so'已区分两阶段 |
| 17 | Critical | - Critical: 样本量 $N=4$，自报 $d_{\min}=2.1279$（Cohen's $d>2$ 属于" | 摘要披露"d_min=2.1279""power 0.0000 at n_d=4","no statistically  | withdrawn | 摘要披露d_min=2.1279、power=0.0000,'not detectable'即承认无 |
| 18 | Critical | - Critical: 经验贡献基本为空结果——L2 两臂无统计可检测差异（McNemar p=1.0000, n_d= | L1a跨模型0/6 vs 2/6 vs 2/6、L2 0.1418/0.1918/0.2750、P5 6/6均显差异；n | partial | 存在null结果,但L1a 0/6 vs 2/6、L2均值不同、P5 6/6显示仍有跨模型区分力 |
| 19 | Major | - **Major**: "46-entry SHA-256 manifest" 似乎只是对已存储 artifact 做 | 将明确18/18 checks为clean environment fresh rerun而非re-hash,描述完整重 | sustained | concede,当前版本未明确18/18 checks为fresh rerun,循环证据风险未消 |
| 20 | Major | - **Major**: "simulated second annotator Î±=0.894" 是合成值，不是实测 | 摘要显式标"simulated second annotator"（非实测）与"zero judge calls...m | partial | α为合成值且管线未运行是真限制,但论文已透明标注'simulated'与'warrant' |
| 21 | Minor | （另有 18 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 10 / Major 1 / Minor 0；撤回 5 条（假阳性被作者驳回）；部分成立 4 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
