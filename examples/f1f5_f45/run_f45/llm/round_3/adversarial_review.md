# 对抗审查报告

- 时间: 2026-08-27T18:23:25.014443+00:00
- 源: F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f45\extracted_text.txt
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（1）
- - Critical: 混合规则是在同一份 128K cells 上“derived”并又在同一份数据上报告性能，属于样本内选择/评估循环；F5 的 McNemar p 和 c=0 不能作为独立证据，只能视为探索性事后分析。
### Major（4）
- - Major: 仅在单一合成 regime（N=7, f=2, pH=0.65）且诚实置信度“被构造为有信息量”的条件下检验，未扫描 f/N、pH、置信度区分度、捕获者置信度强度/占比等参数空间；当前设计可能从构造上就保证 trust_mean 对 majority 不输，因而无法真正检验符号翻转假设，只能说明“该点不翻转”。
- - Major: 两个 capture strategy 未必覆盖能使符号翻转出现的条件；若 mimicry 构造仍让 5/7 诚实多数携带充分信息量，那么加权投票必然占优，c=0 是设定使然而非经验发现；缺少一个理论上应出现负优势的对照条件作为阳性对照。
- - Major: 机制解释（“trust weighting downweights wrong honest low-confidence votes”）没有通过消融或中介分析验证；诚实置信度信息量与被捕获者行为同时变化，存在混淆变量；真实 LLM pilot 又显示置信度无信息量，因此因果归因不成立，主要结果依赖未经验证的有利假设。
- - Major: “4 model families”与 4,000 trials 的关系不明确；若多个 model family 共享同一 trial 或并非独立随机样本，McNemar 的独立性假设可能被违反，导致伪重复和检验效力/标准误被错误估计。
### Minor（1）
- - Minor: McNemar 报告 c=0 和极显著 p 值，但没有报告 tie 比例、效应量分布或加权得分分布；应检查 c=0 是否来自构造上的单调支配，而不是稳健优势。

## 统计（stat）— ok
### Critical（2）
- - Critical: 混合规则是在同一 128K cells 上“derived”后又在同一数据上评估并报告 McNemar p，属于数据依赖的模型选择/无独立验证集，p 值和效应量因过拟合/数据窥探而不可作为确认性证据。
- - Critical: 报告数字内部不一致：injection hybrid 0.620 vs 0.435、N=16,000、c=0 时 McNemar b 应为 0.185×16,000=2,960，mimicry 0.790 vs 0.732 时 b 应为 928；文中“b≈1600”与给出的准确率无法同时成立。
### Major（4）
- - Major: 未对“sign flip”进行正式的交互检验或对 Δ_injection 与 Δ_mimicry 的差异给置信区间；两个方向都显著的 McNemar 检验不能等价于“效应方向翻转”的统计推断。
- - Major: 16,000 per cell 来自 4,000 trials × 4 model families，但未说明 4 个 families 是否共享 trials 或存在聚类；若共享/相关，有效样本量只有约 4,000，McNemar 的独立性假设被违反，p 值被系统性夸大。
- - Major: 只报告点估计和极值 p 值，未提供配对差值的置信区间、标准化效应量（如 Cohen's h/OR）或任何方差/SE，无法评估效应量的精度与稳定性。
- - Major: 仅在单一参数格点（N=7, f=2, pH=0.65）和单一 seed 42 下模拟；对“within studied regime 无 sign flip”的否证性结论缺少多 seed、参数扫描或敏感性分析。
### Minor（3）
- - Minor: 多个规则、策略和次要终点都报告极值 p 值，未做多重比较校正或预先声明主/次分析层级；虽然 p 很小可能不改变结论，但报告方式存在多重比较风险。
- - Minor: c=0 使 McNemar 检验退化；若 c=0 是该投票构造下由构造保证的性质而非抽样偶然，则 p<10^-100/p<10^-400 不能作为关于随机不确定性的证据，应说明是否结构性必然并报告精确检验。
- - Minor: real-LLM pilot 的样本量/分母矛盾（400 trials 却出现 3991/4000 parse），且 400 样本不足以支撑“0.985 vs 0.985 uninformative”这一结论。

## 实验（experiment）— ok
### Critical（1）
- - Critical: 混合规则（adaptive hybrid）在同样的 128K cell 上“derive”后又在同一批数据上评估，缺少独立验证集/交叉验证，任何阈值或规则选择都属于 in-sample selection，F5 的“reinforces”结论不能作为有效证据。
### Major（10）
- - Major: 只使用 seed 42 生成全部合成数据，没有多 seed 重复、seed 间置信区间或最坏情况报告；McNemar p 值再小也只证明这一份固定数据上的差异，无法排除单一种子下的偶然性。
- - Major: “4,000 trials × 4 model families”高度暗示 4 个 model family 嵌套在同一批 trial 上，但统计检验把 128,000 个 cell 当作独立样本，未做按 trial/family 聚类的分析；配对设计虽好，但伪重复会严重夸大显著性。
- - Major: 缺少无捕获/诚实-only 对照条件；没有该控制组就无法区分“trust weighting 本身在无攻击下也有优势”与“被捕获 verifier 改变了相对优势”，也无法正确定位 sign flip 的边界。
- - Major: 没有 unweighted mean / soft-vote / median 等连续分数基线；trust_mean 相对 majority 的收益可能仅仅来自“使用连续置信度而非离散投票”，而不是“trust weighting”，消融不完整。
- - Major: 混合规则在 injection 下反而不如单组件 trimmed mean（hybrid 0.620 vs trimmed mean 0.690），但论文仍将其描述为强化结论；没有报告 hybrid vs 各组件的统计比较或解释为何组合反而变差，消融解释不完整。
- - Major: 关键超参数全部固定且未做敏感性分析：N=7、f=2、pH=0.65、trim 比例、置信度生成参数、hybrid 阈值 0.5、置信度信息量等均无扫描；无法判断结论是否依赖这些取值。
- - Major: 泛化证据不足：仅单一合成二元任务、单一 (N,f,pH) 和两种 capture 策略，没有变化 f/N、pH、置信度信息强度、任务难度、verifier 相关性或更多对抗策略，所谓“regime”实际只是一个点。
- - Major: 真实 LLM pilot 报告不一致（“400 trials” vs “3991/4000”），且只有 gemma3:4b、400/4000 样本、未在真实 LLM 上操纵 injection/mimicry capture，既不能验证合成 capture 设定，也不具备检验 c=0 的统计效力。
- - Minor: 对比基准过弱，只有 majority；未包括 median、robust aggregation、Dawid-Skene 等更强/更公平的 aggregation baseline，削弱“trust/hybrid 优于现有方法”的基准公平性。
- - Minor: 除 seed 和数据哈希外未提供完整生成代码/配置；且“c=0 从不输给 majority”这个极端结果没有给出理论解释或逐 family/逐 seed 分布，读者无法判断是否由构造恒成立。
### Minor（2）
- - Minor: 对比基准过弱，只有 majority；未包括 median、robust aggregation、Dawid-Skene 等更强/更公平的 aggregation baseline，削弱“trust/hybrid 优于现有方法”的基准公平性。
- - Minor: 除 seed 和数据哈希外未提供完整生成代码/配置；且“c=0 从不输给 majority”这个极端结果没有给出理论解释或逐 family/逐 seed 分布，读者无法判断是否由构造恒成立。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 核心 GAP 不真实：论文没有引用任何已有文献或理论真的预测“trust-weighted voting 在 mimicry 下会输给 majority”，而置信度加权多数（CWMV/WMV）在置信度可反映可靠性的条件下已被现有工作（如 Meyen et al., 2020；Bai et al., 2022；Li & Yu, 2014）视为最优或优于等权多数，因此“5/7 诚实且置信度有信息时加权不劣”近乎已知结论，作者自设的 sign-flip 假设更像稻草人。
- - Critical: 增量贡献被夸大：所谓“falsifies sign flip”只在一个合成参数点（N=7, f=2, pH=0.65，两种捕获策略）上成立，单点模拟即使出现 c=0 也只能算 illustrative case study，不能构成对 sign-flip 的证伪；标题和摘要把它表述为负面结论超越了证据范围。
### Major（4）
- - Critical: 核心 GAP 不真实：论文没有引用任何已有文献或理论真的预测“trust-weighted voting 在 mimicry 下会输给 majority”，而置信度加权多数（CWMV/WMV）在置信度可反映可靠性的条件下已被现有工作（如 Meyen et al., 2020；Bai et al., 2022；Li & Yu, 2014）视为最优或优于等权多数，因此“5/7 诚实且置信度有信息时加权不劣”近乎已知结论，作者自设的 sign-flip 假设更像稻草人。
- - Major: 缺少与现有对抗/鲁棒聚合方法的差异对比：未比较 Dawid-Skene、IWMV、trimmed/median/robust aggregation、adversarial-labeler/crowdsourcing 方法等已有基线，只与 simple majority 对比，因此“trust_weighted/hybrid 优于 majority”并非相对领域 SOTA 的贡献。
- - Major: 混合规则的增量贡献不可独立验证：hybrid 是在同一 128K cells 上事后构造并评估的（no new data），存在 in-sample/hindsight selection 风险，其增益可能被高估，不能支持“hybrid extension”作为稳健贡献。
- - Major: 给出的机制解释只是直觉性重述假设，未刻画 sign flip 的条件边界（如 f≥3、pH≤0.5、置信度去校准、不同捕获比例等），因此论文并未真正回答“答案是否依赖捕获方式”这一声称的研究空白。

## 可复现（repro）— ok
### Critical（2）
- - Critical: 没有公开代码仓库、容器镜像或一键复现脚本，也没有环境/依赖锁文件；仅凭 truncated SHA 无法让审稿人重新生成 cells.jsonl 或验证统计结果。
- - Critical: 证据链自相矛盾：正文写 real-LLM pilot 为 “400 trials”，却又给出 “3991/4000 honest parse 99.78%”，分母 4000 与 400 不一致，导致 pilot 规模、hash 对象和后续结论无法对账。
### Major（5）
- - Major: “seed 42” 只是单一全局种子，未给出 PRNG 类型/版本、生成顺序、各模型家族与 capture strategy 的随机流划分，无法确定能否复现同一份 128K cells。
- - Major: 配置快照缺失：未给出 trust-weighted 投票的确切公式、trimmed mean 的 trim 参数、0.5 阈值判定与 tie-breaking 规则、injection/mimicry 的参数化定义、温度/模板/采样参数等关键配置。
- - Major: 哈希对账不完整：只给 8 位截断 SHA256，没有完整 SHA-256、原始 cells.jsonl、计算命令或校验脚本，无法做可靠的完整性对账。
- - Major: 数据许可缺失：只声称 “Data are shared honestly”，未给出 cells.jsonl、real_llm_400_v6 或 gemma3:4b 派生数据的 license/terms，第三方无法合法复现和再分发。
- - Major: 中间产物链缺失：只有最终 cells.jsonl 的 hash，没有 raw LLM outputs → parse → confidence extraction → cells.jsonl → McNemar table 的逐级 artifact 与转换脚本，解析或 tie-breaking 错误无法被审计。
### Minor（1）
- - Minor: real-LLM 文件命名 “real_llm_400_v6” 与正文 “400 trials” 一致，但 hash 没有对应版本化的生成脚本与模型调用记录，后续无法追踪该 v6 文件是怎么产生的。

## 写作（writing）— ok
### Critical（3）
- - Critical: 摘要自相矛盾：先报告 “Supplementary real-LLM pilot（gemma3:4b）”，随后又说 “All results are synthetic / no real LLM deployment is tested”；应明确限定为 “All main results are synthetic; the LLM pilot is exploratory only.”
- - Critical: 数字不一致：pilot 写 “400 trials”（且文件名 real_llm_400_v6），但同一句写 “3991/4000 honest parse 99.78%”，400 与 4000 的分母直接冲突。
- - Critical: Hybrid 的 McNemar 统计不自洽：c=0 且 paired N=16,000 时 b 约等于 accuracy difference×16,000；injection diff=0.185 ⇒ b≈2,960，mimicry diff=0.058 ⇒ b≈928，不可能 “both ... b≈1600”。
### Major（4）
- - Major: 术语定义冲突：摘要把 mimicry 定义为 captured verifiers “anti-correlate confidence with correctness”，但引言称 mimicry 是 “mimic honest confidence behavior / making them indistinguishable”；反相关其实使 captured verifiers 可区分，与 mimicry 定义矛盾。
- - Major: 结构问题：摘要把实验配置、哈希、主/副结果、real-LLM pilot、F4/F5 全部塞进一个超长段落，主结论被密集数字淹没，结构上不利于读者快速抓取贡献。
- - Major: 图表/编号问题：摘要直接使用 F4/F5 而未说明是 Figure、Table 还是 Finding，且没有对应图表说明；若指图应统一写 “Figure 4/5”，并保证与正文编号一致。
- - Major: 术语含糊：hybrid “defined as the mean of trust_mean and trimmed mean thresholded at 0.5” 有歧义，应给出公式说明是对两个投票得分取平均后以 0.5 阈值，而不是对两个准确率取平均。
### Minor（2）
- - Minor: “Data are shared honestly” 是价值判断而非可验证陈述，且 “honestly” 不适合作为数据声明；建议改为 “Data and reproduction scripts are available at ...”。
- - Minor: “verbalized conf 0.985 vs 0.985 uninformative” 未写清对比对象（正确 vs 错误 trial），首次阅读易误以为是笔误。

## 伦理（ethics）— ok
### Major（2）
- - Major: 数据许可缺失：仅提供 SHA 哈希和“Data are shared honestly”，未给出数据集/代码仓库、明确许可证（如 CC/MIT）及 Gemma3:4b 输出的再分发条款，无法确认这些共享数据可合法复用。
- - Major: 未披露 AI 辅助/agent 参与写作；若该稿件确由 agent 生成，当前仅写“Anonymous authors”而无 AI 使用/作者责任声明，不符合透明性要求。
### Minor（4）
- - Minor: 隐私说明缺失：real-LLM pilot 未说明提示/输出是否包含个人信息、是否经过去标识化或无需 IRB/同意，分发前应明确声明。
- - Minor: 双盲合规未验证：补充数据与代码没有匿名化核验说明，哈希文件名、仓库元数据或提交链接仍可能泄露作者身份。
- - Minor: 利益冲突与资助未披露：未说明资助方、竞争利益或与 Google/Gemma 等模型提供方的关联，缺少可匿名化的 COI 声明。
- - Minor: 误用风险未讨论：论文详细构造 injection/mimicry 两种捕获策略，但未提供 broader impact/dual-use 讨论或滥用缓解说明。

## 汇总

- **Critical: 11 | Major: 33 | Minor: 13**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）