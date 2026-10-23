# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f45\extracted_text.txt`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f45\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 9 / Major 7 （撤回 0，部分成立 2）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: hybrid 的 McNemar 数字与准确率差内部不一致：在摘要给出的 16,000 per  | - | sustained | 作者未回应；hybrid的Δ与b/c在16,000/cell口径下确实不自洽,需统一。 |
| 2 | Critical | - Critical: 一键复现缺失：没有仓库链接、容器/依赖锁定、可执行脚本或端到端 pipeline，审稿人无法复现 | - | sustained | 作者未回应；无仓库/脚本/依赖锁定和端到端复现路径,问题成立。 |
| 3 | Critical | - Critical: 仅用单一参数点（N=7, f=2, pH=0.65）和两种 capture 策略就宣称“fals | - | sustained | 作者未回应；仅单参数点加两种策略确不足以排除更广sign flip,成立。 |
| 4 | Critical | - Critical: 从 16,000 个样本观察到 c=0 只能说明“该样本中未出现输给 majority 的 tr | - | sustained | 作者未回应；有限样本c=0不能直接推出regime内永不输,成立。 |
| 5 | Critical | - Critical: 全文没有给出代码/数据仓库地址、artifact DOI 或补充材料链接；`cells.json | - | sustained | 作者未回应；无数据/代码链接,cells.jsonl等仅名称,证据链断裂。 |
| 6 | Critical | - Critical: 摘要中真实 LLM 试点样本量自相矛盾：前面写 “400 trials”，后面却写 “3991/ | - | sustained | 作者未回应；400 trials与3991/4000、99.78%明显冲突,成立。 |
| 7 | Critical | - Critical: 摘要只给出截断 SHA（`6c375b43`、`798bbc2d`），既无完整 SHA-256， | - | sustained | 作者未回应；截断SHA无完整哈希与规范化说明,无法对账,成立。 |
| 8 | Critical | - Critical: 摘要自相矛盾：先报告 “Supplementary real-LLM pilot（gemma3: | - | sustained | 作者未回应；real-LLM pilot与All results are synthetic表述矛盾 |
| 9 | Critical | - Critical: 混合规则是在同一 128K 数据上“derived/阈值选择”后又在同一批数据上报告 McNem | - | sustained | 作者未回应；hybrid用同批128K数据选阈值又报p值,存在乐观偏倚。 |
| 10 | Major | - Major: F4/F5 是无定义标签，摘要既未说明它们是图、表还是 finding，也没有对应图表或正文解释，导致 | - | partial | 部分成立:F4/F5有简略说明但仍未明确图表/正文定位。 |
| 11 | Major | - Major: 基准公平性不清楚：未给出 4 个 model families 的逐族结果或 family×strat | - | sustained | 作者未回应；缺少逐family结果与交互,pooled可能被某family主导。 |
| 12 | Major | - Major: 对照组缺失：没有“无捕获/无攻击”或“置信度无信息”的 synthetic 条件，无法分离 trust | - | sustained | 作者未回应；无no-capture/无信息置信度对照,因果归因不完整。 |
| 13 | Major | - Major: 所有主要结论只来自单一合成参数点（N=7, f=2, pH=0.65），未扫描 N、f、pH、置信度生 | - | sustained | 作者未回应；单一参数点结论表述为falsify确实过度泛化。 |
| 14 | Major | - Major: 摘要中 F4/F5 未定义，若指图表应写 “Figure 4/5”，且正文截图中没有图表可核对；同时  | - | partial | 部分成立:F4/F5定位不清成立；Atv在引言已有简介,该项不完全成立。 |
| 15 | Major | - Major: 有效样本量可能被高估：若 4 个 model families 共享同一批 4,000 trials， | - | sustained | 作者未回应；若模型族共享4000 trials,独立样本量确被高估。 |
| 16 | Major | - Major: 核心术语 “mimicry” 前后定义冲突：摘要称 captured verifiers “anti- | - | sustained | 作者未回应；mimicry定义摘要与引言矛盾,论证对象不清,成立。 |
| 17 | Major | - Major: 真实 LLM pilot 报告不一致（摘要写 400 trials，但出现 “3991/4000” 和 | - | sustained | 作者未回应；pilot样本量矛盾且恒定置信度使c=0平凡,成立。 |
| 18 | Major | - Major: 隐私/IRB：虽然主体是合成数据，但真实-LLM pilot 未说明 prompt/输入语料来源是否包 | - | sustained | 作者未回应；未声明数据来源无PII/无需IRB,合规说明缺失。 |
| 19 | Minor | - Minor: “verbalized conf 0.985 vs 0.985 uninformative” 未说明  | - | sustained | 作者未回应；0.985指标含义及uninformative推导未说明,成立。 |
| 20 | Minor | - Minor: 报告 p<10^-100 / p<10^-400 不如报告精确 McNemar/binomial p  | - | sustained | 作者未回应；应报告精确p/b/c/效应量而非超小p值,成立。 |

**辩论后**：维持 Critical 9 / Major 7 / Minor 2；撤回 0 条（假阳性被作者驳回）；部分成立 2 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
