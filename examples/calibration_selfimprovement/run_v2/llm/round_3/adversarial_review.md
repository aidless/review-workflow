# 对抗审查报告

- 时间: 2026-08-27T13:37:53.264700+00:00
- 源: F:\deepseek\papers\calibration-self-improvement\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（3）
- - Critical: N=30 试点同时承载了"40--50% 高置信 OOD 答案错误""置信度无用甚至有害""自一致性保留下判别力"等多条实质性因果式结论，统计功效极低、无显著性检验、无效应量置信区间，却以"值得进一步研究的模式（pattern worth further study）"之名行结论之实，内部效度严重不足。
- - Critical: 匹配器的三层扩展（exact â tolerant â 逐行裁定扩展）是在"看到残余错误后"才进行的 in-sample adjudication，匹配器并非独立施加的干预，而是事后依据结果拟合的；由此声称"matcher 决定 measured calibration"存在循环论证/确认偏倚，因果归因（"determined by the matcher"）不成立——混淆变量是"裁定者已看到错误标签"这一信息泄漏。
- - Critical: 将匹配器扩展到 100% 正确后宣称 overconfidence 信号"消失"，但若允许匹配器不断放宽至覆盖所有答案，accuracyâ1、ECEâ0 几乎是构造性必然；缺少匹配器有效性的 held-out 验证，"语义正确答案被识别"与"匹配器被拟合到数据"无法区分，内部效度崩塌。
### Major（6）
- - Major: MSI 在中文自由形式集为 1.000、在 MMLU 多选降至 0.334，被归因于"protocol-dependent"，但两者同时混淆了领域、语言、题型（自由形式 vs 多选）、匹配器实现四者；把差异归结于"协议"是典型的混淆变量误归因，无法支持该因果陈述。
- - Major: 跨域比较以"4Ã""17Ã"的点估计比率作为卖点，但作者自承 Holm 校正后仅最极端对显著、多数 95% CI 极宽且重叠；在多数比较不显著的情况下强调比率，属于选择性报告，因果/比较推断不当。
- - Major: 命题 8â²"自一致性保留判别力"的实证依据是 n=30、且仅对"置信与一致性负相关"的模型成立——"负相关"本身是事后选股条件（post-hoc subset selection），由此引出 OOD-aware gating 的形式基础存在选择偏倚，因果方向与外部效度均存疑。
- - Major: "temperature scaling 对 relabeling 不稳健"这一主张缺少对"relabeling 在温度拟合之前还是之后发生""匹配器翻转率分布"等前提的说明；在 degenerate 分布下温度缩放本就不可识别，把不可识别表述为"不稳健"是假设误设。
- - Major: 摘要中"外部效度来自 600-itemÃ9-model census"与同段"MMLU 为 proof-of-concept pilot N=30 as external-validity demonstration"自相矛盾；外部效度声称与样本性质不一致，内部效度与外部效度的边界被模糊。
- - Major: 前提"从业者用自报置信度去 gate 行动，因而须视为已校准概率"被默认成立，但本文实际测量的"自报置信度"在 27/30 恰为 1.0，已属退化分布；在退化分布上构建的 smECE_sem、MSI、Propositions 1--3 的可识别性与估计一致性未被论证，假设是否成立存疑。
### Minor（2）
- - Minor: "matcher sensitivity is protocol-dependent"中"protocol"定义模糊（是匹配器实现、题型、还是评分流程？），与 MSI 的形式化定义未对齐，影响命题可证伪性。
- - Minor: 匹配器偏差界（matcher flip rate 与 $|\mathrm{FNR}\cdot p-\mathrm{FPR}(1-p)|$）依赖的 flip rate 本身是数据依赖且通常未知的量，界之紧致性未被经验评估，因果推断的"有界偏差"叙述易被误读为可操作保证。

## 统计（stat）— ok
### Critical（3）
- - Critical: 全文核心 ECE 数字（0.363 / 0.1297 / 0.0037）基于 N=30，其中 27/30 置信度恰为 1.0，即这些"精确到 4 位小数"的 ECE 本质上由 3 个非退化样本决定，却未报告任何 SE/置信区间/重抽样方差，属于极端过度精确。
- - Critical: "ECE 跨六个 domain 变化达 17×" 是点估计之比（0.479/0.028），但两区间极宽：比值 CI 约为 [0.30/0.08, 0.60/0.001] ≈ [3.75, 600]，跨度超两个数量级，"17×" 这一效应量在统计上几乎无意义且具误导性。
- - Critical: n=30 上做"置信度与一致性负相关→可移除 OOD 过自信答案"的结论仅标注 "indicative"，未报告相关系数 r、所用检验（Pearson? Spearman?）、相关 CI 或显著性，无法判断是否达到 n=30 下 |r|>0.36 的名义显著性门槛。
### Major（4）
- - Major: ECE 的 95% CI 构造方法未说明；ECE 是分箱不可微统计量，正态近似 CI 不适用，应使用 bootstrap（且在 27/30=1.0 退化分布下 bootstrap 也会失效），CI [0.001, 0.08] 相对点估计 0.028 严重偏右、下界贴近 0 令人存疑。
- - Major: Holm 校正的"domain-pair p 值"未交代比较总数与检验类型；6 domain×9 model 可达 ~135 次两两比较，且"仅最极端的几对显著"叠加极宽 CI，强烈提示多重比较后严重欠功效，却以"significant"措辞暗示稳健发现。
- - Major: 双判（dual-judged, 4999 对）作为标签 adjudication 的基础，却全程未报告评分者间信度（Cohen's κ / 一致率 / 翻转率），而 matcher 翻转率正是本文核心命题，缺该方差来源使全部 ECE 差异无法归因。
- - Major: "40–50% 的高置信 OOD 答案错误" 既无分子分母（high-confidence 子集 n=?），也无该比例的 CI，在 N=30 总样本下该子集可能 n≤10，区间将覆盖 [0.2, 0.7] 量级，结论不稳。
### Minor（3）
- - Minor: 小数精度不一致——0.363（3 位）、0.1297 与 0.0037（4 位）并存，且 63.3% 实为 19/30，以百分比+1 位小数呈现制造伪精度。
- - Minor: MSI 1.000 vs 0.334 为两点估计，未附 CI，无法判断该"protocol-dependent"差异是否超出抽样噪声。
- - Minor: "4× across three subjects" 同为点估计比值，未给比值 CI，与 17× 同病。

## 实验（experiment）— ok
### Critical（3）
- - Critical: 核心结论"confidence 无用甚至有害于 OOD gating""40–50% 高置信 OOD 答案错误""self-consistency 有效"全部建立在 N=30 的探针上，无任何功效分析、置信区间或重复实验支撑，统计效力严重不足，无法支撑因果性/比较性结论。
- - Critical: 缺少对照组/对照基线——gating 规则的评估既无"随机 gate""恒定阈值 gate""无 gate"等朴素基线，也无除 self-consistency 之外的其他廉价信号对照（如 token logprob、长度、检索分数），导致"self-consistency 优于 confidence"这一比较缺乏公平的对照组。
- - Critical: "matcher 经 per-row 裁决后扩展"得到 100% 准确率 / ECE=0.0037，本质是在同一 N=30 样本上逐行拟合标签（in-sample label engineering），构成基准不公平与测试集泄漏；作者虽自承"in-sample illustrative, not a validated bound"，但该数字仍被用于支撑"过度自信信号消失"的核心叙事，且无 held-out 验证。
### Major（6）
- - Major: 消融不完整——self-consistency 仅用 3 次 resample，未报告 resample 次数 K∈{1,3,5,10}、采样温度、agreement 判定阈值（完全一致 vs 多数一致）的消融，无法判断"3 次"是否为关键超参数。
- - Major: 温度scaling 被断言"对重标定不鲁棒"，但未报告温度搜索范围、优化目标、是否在 held-out 上拟合、是否跨 matcher 稳定，超参数过程完全缺失，结论不可复现。
- - Major: ECE 跨域变化"4×（三科）/17×（六科）"为点估计之比，且 Holm 校正后仅最极端 domain-pair 显著，其余不显著；用比值放大效应量而 CI 极宽（如 Qwen2.5-7B 0.028 [0.001,0.08] vs 0.479 [0.30,0.60]），domain-specificity 主张证据不足，且未做正式多域方差分量分解。
- - Major: 数据采集中途变更协议——从"300 items × 4 models × 1159 pairs"扩展为"600 items × 9 models × 4999 pairs"，模型集合、域数、judge 对数在研究过程中非同时变化，无法分离"扩样本""扩模型""扩域"三个因素的贡献，构成混杂设计。
- - Major: seed 管理缺失——resample-based self-consistency、温度采样、MMLU 子集抽样、matcher 裁决顺序均未报告随机种子与重复次数，故既无法评估 self-consistency 信号的方差，也无法复现；"negatively correlated"结论（n=30）尤其依赖单次随机实现。
- - Major: 泛化范围狭窄且不均衡——9 个模型横跨 5 个 family，但每个 family 仅 1–2 个模型、单次 N=30 探针；OOD gating 结论仅在未指明的一两个模型上"indicative"，无法判断结论是否依赖特定模型族/规模/对齐方式，亦未报告跨模型的异质性检验。
### Minor（3）
- - Minor: MSI 1.000（中文 free-form）→ 0.334（MMLU 多选）的跨协议差异未控制任务难度/语言/题型混杂因素，无法归因于"协议差异"本身。
- - Minor: "dual-judged pairs"中 judge 之间的一致率/仲裁机制未作为消融项报告，matcher 敏感性的测量本身依赖 judge，存在循环验证风险。
- - Minor: binning-based ECE 被判"不可靠"，但未报告 bin 数、equal-width vs equal-mass、以及 binning-free 指标（如 smECE、brier）随 matcher 的完整对照表，"binning-free 更优"缺少直接消融。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: GAP 被夸大。摘要声称"self-reported confidence 的校准在 agent 自身任务分布上很少被验证"是核心缺口，但校准验证在 calibration 文献（Guo et al. 2017、Lin et al.、Kumar et al.）中是标准流程；真正的窄缺口（memory-gating / deferral 这类 agentic 部署场景）与实际研究（N=30 QA + MMLU 多选）之间严重错配，用通用 QA 任务支撑"agentic 部署前未验证"的 GAP 不成立。
- - Critical: "matcher 决定测量校准"被当作 central finding，但这本质是 LLM 评测中 exact-match vs semantic-match 的已知问题（fuzzy/semantic matching 在 QA/benchmark 评测中早已被反复讨论）。Propositions 1–3 给出的"matcher flip rate + |FNR·p − FPR(1−p)|"界更像是测量误差理论的标准套用，理论增量贡献被表述得偏深。
### Major（4）
- - Major: 以 N=30 pilot 为基础却多处给出方向性结论（"40–50% 高置信 OOD 答案错误""self-consistency 消除过自信 OOD 答案""confidence 与 consistency 负相关"），并冠以"methodology study"提升定位；pilot 的指示性结果被包装成可引用的发现，增量证据强度被夸大。
- - Major: 跨域 MMLU 的"校准是 domain-specific、ECE 跨域变化达 17×"是已知现象（domain-specific calibration 已有先例），且 17× 是点估计比、CI 极宽、Holm 校正后仅极端对显著——摘要仍以 17× 领衔，贡献被放大。
- - Major: smECE_sem + MSI 的新颖性未经与最接近先行工作（smooth ECE、soft-label/semantic 评测框架、classifier-based calibration）的逐项对照；"semantic soft-label 校准估计器"看起来是已有概念的组合，是否真正新增未自证，存在增量贡献被高估风险。
- - Major: degeneracy 导致 binning-ECE 不可靠、temperature scaling 对 relabeling 不稳健——前者近乎同义反复（置信度塌缩到 1.0 时分箱自然失效），后者是 relabel 改变最优温度的直接推论，作为"caution"贡献的原创性偏弱。
### Minor（3）
- - Minor: 摘要先以 63.3%→100% 的"initially alarming"信号吸引注意，随后又括注"in-sample illustrative, not a validated bound"，存在用强反差叙事抬高观感再对冲的写法，削弱了贡献表述的诚实度。
- - Minor: Keywords 含"self-improvement"，但正文仅以单条 \citep{beyond2025} 串联，与自改进文献的差异未展开，主题归属与实际贡献不一致。
- - Minor: "Proposition 8′"等编号带撇号暗示存在 8→8′ 的修订谱系，但未交代与原 Proposition 8 的关系，读者无法判断该形式化结果的真实增量。

## 可复现（repro）— ok
### Critical（5）
- - Critical: 全文未见任何代码/数据仓库链接或 reproducibility statement，N=30 pilot 与 600×9 census 既无匿名 repo 也无 Zenodo DOI，无法一键复现核心结论。
- - Critical: "九个模型、五个家族"只给了 Qwen2.5-7B 一个名字，其余八个模型无精确 checkpoint/版本/commit hash；模型权重是可复现性的根，缺失即证据链断裂。
- - Critical: 三次 resample 的 self-consistency 探针未指定采样温度、top-p、随机 seed 与解码停止规则；复现者无法重现"负相关→剔除 OOD 过置信"这一关键信号。
- - Critical: per-row 人工 adjudication 是论文核心matcher 演化的来源，但未记录 adjudicator 人数、资格、判定协议、冲突解决规则或 inter-annotator agreement；主观标注无协议=不可复现。
- - Critical: 缺少配置快照——system prompt、max tokens、上下文窗口、API 端点版本（若用商业 API）均未冻结到附录，ECE 数值随 prompt 漂移即变。
### Major（5）
- - Major: 两个 matcher（"first tolerant""extended after adjudication"）的精确判定规则未形式化给出；matcher 决定测量结论却无可执行定义，复现者只能猜。
- - Major: "1159/4999 dual-judged pairs"未说明 judge 身份——人工还是 LLM？若是 LLM，哪个版本、什么 prompt、什么温度；judge 不可复现则 dual-judged 数据不可对账。
- - Major: MMLU 子集、Chinese free-form set 的具体来源、split、license（MMLU 为 MIT/CC-BY-SA 混源，Chinese 集许可不明）与再分发权均未声明，违反数据许可可复现要求。
- - Major: 30 条 pilot、600 条 census 的抽样过程（分层？随机？哪些 MMLU subject、哪条 split、第几道题）无 seed 无清单；无法对账到同一批 item。
- - Major: 无任何数据/输出文件 hash（SHA256）或 model-output manifest；"27/30 恰为 1.0"这类精确断言无法做哈希对账，存在静默修改风险。
### Minor（3）
- - Minor: ECE 精度不一致（0.363 vs 0.1297 vs 0.0037），暗示数值未经统一固定流水线产出，复现时小数位会漂。
- - Minor: "27 of 30 exactly 1.0"未说明 confidence 提取协议（是 parse 原始 token 还是 post-hoc 归一化、浮点截断阈值），影响严格相等性的复现。
- - Minor: self-consistency "indicative, n=30"虽加了免责，但未给出 bootstrap CI 或 seed 列表，小样本信号连统计稳定性都无法复现。

## 写作（writing）— ok
### Critical（2）
- - Critical: 摘要本身存在數字矛矛盾——称 "proof-of-concept pilot N=30 as external-validity demonstration" 的跨域收集同時又是 "300 items expanded to 600 items"，N=30、300、600 三個數字之間的關係在摘要中完全無法理清，讀者無法判斷到底是 30 還是 600 item 的外部效度證據。
- - Critical: 摘要提到 "Propositions 1--3" 後直接跳到 "Proposition 8$'$"，缺少 Propositions 4--8 的存在意義，且使用 prime 符號（8'）作為命題子編號是非標準做法，在摘要中造成嚴重結構混亂。
### Major（6）
- - Major: `smECE_sem`+MSI"，但摘要正文從未出現 `smECE_sem` 的縮寫或定義，僅稱 "a semantic soft-label calibration estimator with a matcher sensitivity index (MSI)"，讀者在摘要到正文的銜接處遭遇未定義符號。
- - Major: ECE 數孼精度不一致——0.363（3 位小數）、0.1297（4 位）、0.0037（4 位），同一批次報告的指標應保持統一精度。
- - Major: 摘要同時強調 "ECE varies by up to 17Ã" 又坦言 "Holm-corrected domain-pair p-values show only the most extreme pairs are significant"，這兩句互相削弱：17Ã 是點估計比，且 95% CI 大幅重疊（0.028 [0.001,0.08] vs 0.479 [0.30,0.60]，CI 上界 0.08 僅略低於下界 0.30），"17Ã" 的框架性表述誇大了統計顯著性。
- - Major: 4999 dual-judged pairs 對應 600 items Ã 9 models = 5400 可能，缺失 401 對（約 7.4%）；1159 對對應 300 Ã 4 = 1200，缺失 41 對（約 3.4%），摘要未對如此大量缺失做任何說明。
- - Major: 摘要過長（估計 400+ 詞），塞入了方法學細節、多個 Proposition 編號、兩個延伸方向、大量帶 CI 的數字，違反摘要應簡潔概述核心貢獻的寫作規範，應將方法細節與完整數字移至正文。
- - Major: 關鍵詞列出 "self-improvement"，但摘要核心論述圍繞匹配器依賴性與校準，self-improvement 僅在引言中一筆帶過，關鍵詞與論文中心主題不匹配。
### Minor（3）
- - Minor: 摘要中 "temperature scaling is not robust to relabeling" 為重大論斷，但在可見正文中未見對應的實驗或理論支撐，存在摘要超前於正文的風險。
- - Minor: "40--50% of high-confidence OOD answers are wrong" 的區間跨度過大（10 個百分點），且僅基於 30-item probe，此精度區間對 N=30 而言過度精確，應給出原始數字。
- - Minor: 摘要反覆出現 "in-sample illustrative, not a validated bound"、"point-estimate ratio"、"indicative, n=30" 等多個保守性插語，雖體現學術誠實，但過度密集地插在數字之後，嚴重影響句子結構與可讀性。

## 伦理（ethics）— ok
### Critical（2）
- - Critical: 全文未声明任何数据许可信息。MMLU（MIT）、"Chinese free-form set"（来源与许可证完全缺失）、600 items×9 模型所涉及的各模型许可证（如 Qwen2.5 系列的 Tongyi Qianwen/Apache 2.0）均无归属与合规说明，违反可复现与开源合规要求。
- - Critical: 存在大量人工标注（"per-row adjudication"、"4999 dual-judged pairs"），但全文未见 IRB/伦理审查批准、标注者知情同意、报酬或隐私保护声明，涉及人类被试/众包合规缺失。
### Major（4）
- - Major: 缺失利益冲突声明（Conflict of Interest）。TMLR 要求作者披露资助方、雇主与可能影响结论的利益关系，本稿无任何此类段落（截断处亦未见）。
- - Major: 双盲风险——"Chinese free-form set"这一未公开来源的私有/自建数据集若为特定团队独有，可能构成身份去匿名化线索；同时"九模型×五家族"的具体配置若与作者既往工作高度重叠，存在 de-anonymization 隐患，未做匿名化处理说明。
- - Major: 误用风险未讨论。本文核心发现"matcher adjudication 可将准确率推至 100%、ECE 降至 0.0037"本身即是 calibration benchmark gaming 的方法学模板，可被用于粉刷模型安全/可靠性指标，但全文无 misuse/双重用途或缓解措施的 broader impact 讨论。
- - Major: 部署建议（OOD-aware gating、以 self-consistency 替代 confidence 门控）涉及 defer-to-human、write-to-memory 等安全相关决策，却未评估误判后果（如错误放行高置信 OOD 答案、一致性信号被对抗扰动），存在安全部署缺失。
### Minor（1）
- - Minor: 摘要中将"in-sample illustrative, not a validated bound"与"40–50% of high-confidence OOD answers are wrong"并陈，后者基于 n=30 探针，若被下游读者当作部署阈值依据可能引发误用，警示力度不足。

## 汇总

- **Critical: 20 | Major: 35 | Minor: 18**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）