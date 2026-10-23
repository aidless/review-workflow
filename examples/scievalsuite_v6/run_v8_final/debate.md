# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\run_v8_final\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 14 / Major 2 （撤回 1，部分成立 3）；注：原始 36 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 16 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: Friedman 检验包含 16 个任务中 10 个 all-zero（floor）任务，违反了 | 将剔除10个all-zero L1b floor任务,以6个可区分任务为主Friedman分析,16-task版本降为附 | sustained | concede；当前版本仍含被稀释的16-task Friedä¸»åæï¼å¾ 修订 |
| 2 | Critical | - Critical: L1b 全部模型 0/10 属于 floor effect，测量工具在该任务层失效，无区分力；在 | 将L1b从Friedman主分析移除,重定位为pipeline压力测试（failure taxonomy+answer- | sustained | concede；当前版本L1b floorä»å ¥Friedman主分析 |
| 3 | Critical | - Critical: L2 对照组（A=ReAct vs CG=completion-guided）N=4 且 n_d | 论文已声明'L2 was statistically uninformative',n_d=0不报p值,两arm均值相同 | partial | rebut部分成立:已称uninformative未作CG结论；但L2ç»ææ§æ ç¨ |
| 4 | Critical | - Critical: L2 比较宣称 "in both arms" 分数相同，构成等效性声明，但在 N=4、McNem | 论文称L2'statistically uninformative','in both arms'为均值相同的描述性陈述 | withdrawn | rebut成立:论文明称uninformative,'in both arms'为描述性陈述非等效性 |
| 5 | Critical | - Critical: LLM-as-judge 校准 21 gold、单一标注者、FNR=FPR=0.00，rule- | 将报告gold正/负例拆分(k与21−k),分别计算FNR上界3/k与FPR上界3/(21−k),修正≈14%统一上界。 | sustained | concede；3/21â14%同用于FNR与FPR分母数学不可能,当前版本有误 |
| 6 | Critical | - Critical: Model-F 仅以"opencode.ai alias"出现，无模型版本钉死、无权重哈希、无  | 将钉死Model-F后端模型版本与API快照日期,明确排除于SHA-256复现契约范围,标注为不可复现探索性参考。 | sustained | concede；当前版本Model-F alias无版本钉死/快照 |
| 7 | Critical | - Critical: SHA-256 seal 仅覆盖 125 个"committed files"且明言"not l | 将'byte-level reproducibility'改述为'input-contract byte-level r | sustained | concede；当前版本称byte-level reproducibility却排除LLM输出,自相 |
| 8 | Critical | - Critical: 三个子基准（AIRS-Bench rad、ResearchClawBench、GAIA2 p3d | 论文明确列出新增贡献:answer-fitting audit、calibrated heterogeneous jud | partial | rebut列出新增元素部分成立；但超越工程打包的novelty/显著性仍存疑 |
| 9 | Critical | - Critical: 全文未声明任何数据集许可——AIRS-Bench、ResearchClawBench、GAIA2 | 将增设Data Availability & Licensing章节,披露AIRS-Bench/ResearchClaw | sustained | concede；当前版本无数据集许可声明 |
| 10 | Critical | - Critical: 全文未给出所用 seed 取值与数量；"per-seed rows" 仅声明存在，seed 如何 | 将披露seed取值与数量、temperature/top_p设定及seed注入方式,并承认服务端seed未钉死时call | sustained | concede；当前版本未披露seed取值与注入方式 |
| 11 | Critical | - Critical: 全部点估计（goal completion 0.14/0.19/0.28、TextSimilar | 将为主要点估计添加Wilson精确二项CI及SD/SE,N=4时明确标注宽区间并补充不确定性披露。 | sustained | concede；当前版本点估计无CI/SD/SE离散度指标 |
| 12 | Critical | - Critical: 对照模型 Model-F 以 API 方式服务，而三个被测模型以本地 GPU 方式服务，服务通道 | 将显式披露API与本地GPU服务通道混淆变量,将Model-F 6/6重定位为非比较性图示不归因模型能力。 | sustained | concede；当前版本未披露API与本地GPU服务通道混淆变量 |
| 13 | Critical | - Critical: 报告 d_min=2.1279（80% power），即只能检测 Cohen's d>2 的极端 | 论文已披露'd_min=2.1279 at 80% power'与'McNemar power structurally | partial | rebut成立:功率限制已透明披露并标exploratory；但结构性功效缺失仍为真实局限 |
| 14 | Critical | - Critical: 摘要声明"18/18 independent recomputation checks pass | 将明确18项重算检查与72行结果的映射关系,统一摘要'18/18 checks'与引言'every leaderboar | sustained | concede；18/18 checks与72行结果矛盾在当前版本存在 |
| 15 | Critical | - Critical: 无数据许可披露 â 重用的 AIRS-Bench、ResearchClawBench、GAI | 将增设许可声明章节,披露三套基准、125个SHA-256密封文件及Qwen2.5/Gemma2/llama3.1开源权重 | sustained | concede；当前版本无许可声明（同#9） |
| 16 | Critical | - Critical: 模型身份未钉死：qwen2.5:7b/14b、gemma2:9b 是可变的 registry t | 将为qwen2.5:7b/14b、gemma2:9b、llama3.1:8b钉死权重SHA-256 digest、Oll | sustained | concede；当前版本模型registry tag无digest/量化版本钉死 |
| 17 | Critical | - Critical: 缺少伦理审查/IRB 声明——"21 gold, single annotator" 涉及人工标 | 将增设Ethics Statement,披露标注者知情同意、IRB审批或豁免依据及标注者隐私保护措施。 | sustained | concede；当前版本无IRB/伦理审查声明 |
| 18 | Critical | - Critical: 采样配置（temperature/top_p/max_tokens/seed）全文缺失；"one | 将全文披露temperature/top_p/max_tokens/seed采样配置,承认无服务端seed钉死时call | sustained | concede；当前版本未披露temperature/top_p/seed等采样配置 |
| 19 | Major | - **Major**: "TextSimilarity intention-to-treat mean 0.355"  | 将在摘要中定义TextSimilarity度量或将该指标值移至正文,避免未定义术语在摘要突兀出现。 | sustained | concede；TextSimilarity在摘要未定义,当前版本存在 |
| 20 | Major | - Major: "denominator discipline"、"answer-fitting audit"、"po | 将增设相关工作对比,将denominator discipline/answer-fitting audit/posit | sustained | concede；当前版本未与SWE-bench等robustness/contamination文献 |
| 21 | Minor | （另有 16 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 14 / Major 2 / Minor 0；撤回 1 条（假阳性被作者驳回）；部分成立 3 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
