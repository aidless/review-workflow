# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\run_v3_converge\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 8 / Major 1 （撤回 4，部分成立 7）；注：原始 38 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 18 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - **Critical**: AIRS-Bench / ResearchClawBench / GAIA2 三套派生/ | 将补充披露AIRS-Bench、ResearchClawBench、GAIA2三套数据集的许可证及再分发条款。 | sustained | 作者concede将补披露许可证,当前版本问题未消除 |
| 2 | Critical | - **Critical**: L2 的 exact McNemar 检验 $n_d=0$（零不一致对），检验统计量退化 | 摘要已标n_d=0<6为'not-detectable'、CI为'degenerate'并披露power=0.0000； | withdrawn | 摘要用'not-detectable'非声称等价,已标degenerate,审稿误读为等价推断 |
| 3 | Critical | - **Critical**: curated L1a 的 $p=0.0026$ 仅在"fail-as-worst en | 摘要将该结果标为'exploratory',注明'only under fail-as-worst encoding(s | partial | 标exploratory减轻p-hacking担忧,但未对编码方案数做多重比较校正 |
| 4 | Critical | - Critical: "simulated second annotator α=0.894"——模拟标注者需要 se | 将补充披露模拟标注者的seed、模拟模型及参数设定,使α=0.894可对账复现。 | sustained | 作者concede将补seed/模型,当前版本α=0.894不可对账 |
| 5 | Critical | - Critical: L1b 所有模型 0/10，positive control 仅 Chemistry_000 1 | L047审计3/3模型截获answer-fitting证harness运行且模型交互；阳性对照Chemistry_000 | partial | L047审计3/3证harness运行,但0/10全模型+1/4阳性对照仍弱 |
| 6 | Critical | - Critical: L2 主对比 A vs F 仅 N=4，McNemar 功率显式为 0.0000，n_d=0<6 | 摘要同句披露N=4、power=0.0000、n_d=0<6；'no statistically detectable  | withdrawn | 摘要同句披露N=4/power=0/n_d=0,'not detectable'即无力检验非无差异 |
| 7 | Critical | - Critical: LLM-as-judge 在主轮次中零次调用（all SKIP），校准（21 gold，sing | 摘要原文写'zero judge calls(all SKIP)so calibration is a methodol | partial | 透明标注methodological warrant,但管线实际未运行、保证空桥 |
| 8 | Critical | - Critical: LLM-as-judge 校准仅 21 样本（11/10），FNR=0/FPR=0 但真实 FP | 摘要已披露'Wilson 0.28 at FPR=0'即上界,并定位校准为'methodological warrant | partial | Wilson0.28已披露,但21样本FPR上界高且零调用,外推前提弱 |
| 9 | Critical | - Critical: P5 gold 计数矛盾："39 gold, 30 real+9 synthetic+1 att | 将修正P5 gold计数:30 real+9 synthetic=39,攻击条目另行单列,使分项与总数一致。 | sustained | 作者concede将修正计数,当前版本30+9+1=40≠39 |
| 10 | Critical | - Critical: SHA-256 清单条目数前后不一致——"46-entry manifest"与"165 ent | 将明确说明46-entry manifest与165 entries(with P5)的口径关系及P5阶段定义。 | sustained | 作者concede将说明46与165关系,当前版本口径不清 |
| 11 | Critical | - Critical: ollama 模型的量化精度（Q4/Q8/FP16）未报告，7b/14b/9b 在不同精度下性能 | 将补充报告ollama各模型的量化精度(Q4/Q8/FP16)及对应推理参数。 | sustained | 作者concede将补量化精度,当前版本未报告 |
| 12 | Critical | - Critical: seed 管理完全缺失——摘要明确写"bootstrap at step/seed level  | Introduction写'All results are delivered with per-seed rows', | partial | Introduction称per-seed rows已报告,但种子级稳定性分析确为future wo |
| 13 | Critical | - Critical: åå¿åé£é©ï¼è¿åä¸º TMLR double-blindï¼G3ï¼ï¼ä½ mus | 将muse-spark-1.2-contributor更名为匿名标识(如Model-F)并移除可识别团队的技术栈细节。 | sustained | 作者concede将匿名化,当前版本技术栈可识别团队 |
| 14 | Critical | - Critical: æª«ª»é¢çå©çºå®ï¼æ¨¡åmuse-spark-1.2-contributor å | 将声明COI与模型访问/所有权关系,并对frontier模型采用匿名标识消除'contributor'暗示。 | sustained | 作者concede将声明COI,当前版本唯一通过模型未声明利益关系 |
| 15 | Critical | - Critical: 全文宣称"byte-for-byte reproducibility"，但未披露任何 LLM 采 | 将补充披露LLM采样seed/temperature/top-p及ollama确定性配置,支撑逐字节可复现声明。 | sustained | 作者concede将补采样参数,当前版本逐字节可复现声明无支撑 |
| 16 | Critical | - Critical: 摘要自相矛盾——LLM-as-judge 声称"passed at FNR=0.0000, FP | FNR/FPR=0来自21-gold校准集(11正/10负,有分母)非实际轮次；摘要写'zero judge calls | withdrawn | FNR/FPR来自21-gold校准集有分母,非实际轮次,审稿混淆二者 |
| 17 | Critical | - Critical: 样本量 $N=4$，自报 $d_{\min}=2.1279$（Cohen's $d>2$ 属于" | 摘要显式披露d_min=2.1279与power=0.0000 at n_d=4；'no statistically d | withdrawn | d_min与power=0已充分披露,'not detectable'为诚实表述非冒充发现 |
| 18 | Critical | - Critical: 经验贡献基本为空结果——L2 两臂无统计可检测差异（McNemar p=1.0000, n_d= | L1a有区分力(7b 0/6,14b 2/6,gemma 1→2/6)；L047审计3/3模型截获answer-fitt | partial | L1a有描述性区分力,但L2/L1b多为null,唯一显著结果exploratory |
| 19 | Major | - **Major**: "46-entry SHA-256 manifest" 似乎只是对已存储 artifact 做 | 将明确说明18/18 recomputation checks是否为fresh-environment重跑并补充重跑环境 | sustained | 作者concede将说明是否fresh rerun,当前版本循环证据嫌疑 |
| 20 | Major | - **Major**: "simulated second annotator Î±=0.894" 是合成值，不是实测 | 摘要标'simulated second annotator α=0.894'为合成值并写'calibration is | partial | 标simulated/warrant透明,但管线未运行、α为合成值非实测 |
| 21 | Minor | （另有 18 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 8 / Major 1 / Minor 0；撤回 4 条（假阳性被作者驳回）；部分成立 7 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
