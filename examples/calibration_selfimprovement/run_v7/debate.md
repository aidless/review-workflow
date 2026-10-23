# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\calibration_selfimprovement\run_v7\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 5 / Major 12 （撤回 1，部分成立 2）；注：原始 24 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 4 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: MMLU 的 4999 个 “pairs” 并非独立样本：同一 item 被多模型、多次采样重复 | 将采用 item/model 双层聚类稳健标准误或混合效应模型重算 ECE/CI/p 值,并在附录报告聚类数量。 | sustained | 作者承认pair非独立并承诺改用聚类稳健标准误或混合模型,当前版本确未处理,问题成立。 |
| 2 | Critical | - Critical: OOD-gating 因果推断不恰当：“confidence may be harmful”“c | 将把 OOD-gating 改为探索性相关分析,补充 gold/拒绝率匹配基准与二项/覆盖率 CI,删除‘harmful | sustained | 作者承认OOD-gating仅观察相关且将弱化因果措辞并补基准,当前版本因果断言不当的问题真实存在。 |
| 3 | Critical | - Critical: “matcher extended after per-row adjudication” 是后 | 将冻结裁定协议并发布逐行 adjudication log、matcher 版本、重算脚本；100% 结果明确标注为后验 | sustained | 作者承认裁定协议未冻结、日志未发布,后验扩展matcher的可复现性缺陷成立。 |
| 4 | Critical | - Critical: “语义 soft-label 估计器 + MSI”被现有文献高度预见：语义等价类定义下的校准（B | B-calibration/Sem-ECE 构造语义校准标签；本文 MSI 审计同一输出在不同 matcher 下的敏感 | partial | 语义软标签估计确与B-cal/Sem-ECE重叠,但MSI及flip-rate界有区分度,故仅部分成 |
| 5 | Critical | - Critical: 核心发现“校准由标签 matcher 决定”并非真实 GAP：已有工作直接证明 finite-r | 本文不止复现翻转:Prop 1–3 给出 matcher 依赖解析界与非对称条件,smECE_sem+MSI 诊断退化分 | partial | 已有工作确示matcher翻转,但本文Prop1–3、诊断工具与4999 census超出单纯复现, |
| 6 | Critical | - Critical: 核心校准结论建立在 N=30 的 pilot 上，且 ECE 只报点估计（0.363 / 0.1 | 将把 pilot 结论限定为 illustrative,并补充 bootstrap/解析 CI；中心论断改由 4999- | sustained | 作者承认pilot缺CI并承诺限为illustrative、改由大样本聚类检验支持中心结论。 |
| 7 | Critical | - Critical: 核心证据在样本内（N=30）且标签是“逐行 adjudication 后扩展 matcher”产 | 文内已明示该 100% 为 in-sample、circular、not evidence of calibration | withdrawn | 文内已明确100%为in-sample、circular、not evidence,且中心结论由Pr |
| 8 | Critical | - Critical: 配置快照缺失：模型版本/API 调用日期、temperature、top_p、max_token | 将发布完整配置快照:模型版本/调用日期、temperature/top_p/max_tokens、prompt/syst | sustained | 作者承认配置快照缺失并承诺发布完整版本、参数、prompt与依赖信息。 |
| 9 | Major | - Major: 1159 pairs 和 4999 pairs 来自 300/600 items × models，p | 将采用 item/model 双层聚类稳健标准误或多水平模型重算 1159/4999-pair 的 SE、CI 和 p  | sustained | 作者承认1159/4999 pair存在item/model聚类并承诺重算SE/CI/p及去重规则。 |
| 10 | Major | - Major: MSI 的 1.000 vs 0.334 没有方差、CI 或显著性检验，且 1.000 在小样本/退化 | 将报告 MSI 的 bootstrap CI 与显著性检验,并讨论 1.000 在退化置信分布下的天花板效应,避免直接归 | sustained | 作者承认MSI比较缺方差/CI/显著性检验并承诺讨论天花板效应。 |
| 11 | Major | - Major: MSI 的 1.000（free-form）与 0.334（MMLU）比较混淆了 protocol 与 | 将把结论改为‘MSI 随 protocol 与数据集共同变化’,补充同数据集不同 protocol 或难度匹配对照,不再 | sustained | 作者承认MSI比较混淆protocol与数据集因素,承诺改为共同变化并补对照。 |
| 12 | Major | - Major: OOD gating 分析 N=30，只报 “40–50% high-confidence OOD a | 将给出 OOD-gating 的精确分子/分母、二项 CI 与检验,并说明 40–50% 区间重叠,仅作探索性发现。 | sustained | 作者承认OOD gating未给精确分子分母与二项CI,承诺补检验并仅作探索性发现。 |
| 13 | Major | - Major: semantic soft-label estimator 如果由同一类或同源 LLM judge 产 | 将补充独立 gold 或异源 judge 的稳健性分析；若仍用同源软标签,则明确 smECE/MSI 仅作敏感度审计而非 | sustained | 作者承认同源软标签可能继承matcher偏差,承诺补独立gold或异源judge稳健性。 |
| 14 | Major | - Major: “$\mathrm{smECE}_{\mathrm{sem}}$+MSI”在摘要后的 central  | 将在摘要和首次出现处定义 smECE_sem（semantic soft-label ECE）,并统一后续术语,消除跳变 | sustained | 作者承认smECE_sem摘要与首次出现处未定义,承诺补定义并统一术语。 |
| 15 | Major | - Major: “95% CI 88.4%–100%”看起来只是 30/30 成功的精确二项单侧下界，不是双侧 CI  | 将把 88.4%–100% 改为‘30/30 的单侧 95% 下界’,并补充双侧 CI 及 held-out 说明。 | sustained | 作者承认88.4%–100%实为单侧下界,承诺补双侧CI与held-out说明。 |
| 16 | Major | - Major: “domain-specific ECE”属于已知且宽泛的实证现象，且作者自述只有极端 Holm 校正 | 将把 domain-specific ECE 降为探索性观测,强调仅极端 Holm 校正显著,并从贡献清单中移除独立新发 | sustained | 作者承认domain-specific ECE显著性有限,承诺降为探索性并撤下独立新发现表述。 |
| 17 | Major | - Major: 引言末句 “We use single-turn verbalized confidence as p | 将补全为:‘单轮口头置信用作探针；多步 agentic 指标延至第6节讨论。’ | sustained | 作者承认语法破碎并承诺补全为规范表达,当前版本确有写作缺陷。 |
| 18 | Major | - Major: 扩展数据（600 items/6 domains/9 models/4999 pairs）缺少逐域清单 | 将发布逐域数据清单、去重/划分规则、版本号与 SHA-256 哈希,并提供对账脚本核验 4999-pair 各项数字。 | sustained | 作者承认扩展数据缺逐域清单、去重规则与哈希,承诺发布对账材料。 |
| 19 | Major | - Major: 摘要中 “An OOD-gating analysis (exploratory, N=30) sug | 将删去重复的 exploratory,并规整括号为‘N=30; no causal claim or intervent | sustained | 作者承认摘要重复exploratory且括号混乱,承诺规整措辞。 |
| 20 | Major | - Major: 摘要以 “Compliance in appendix (Section~\ref{sec:compl | 将删除摘要末端孤立句,并在附录开头说明 compliance 内容（数据/模型/代码/许可清单）。 | sustained | 作者承认摘要残句不当并承诺删除且于附录说明compliance含义。 |
| 21 | Minor | （另有 4 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 5 / Major 12 / Minor 0；撤回 1 条（假阳性被作者驳回）；部分成立 2 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
