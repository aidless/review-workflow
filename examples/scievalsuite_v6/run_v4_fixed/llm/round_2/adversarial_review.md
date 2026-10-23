# 对抗审查报告

- 时间: 2026-08-27T03:45:04.407033+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（4）
- - Critical: L2 的核心结论"两臂无差异"基于 N=4、discordant pairs n_d=0 的 McNemar 检验，该检验在 n_d=0 时退化为恒等式，p=1.0000 与 CI[0,0] 不构成"无差异"的证据，而是"检验无信息"；摘要却以"no statistically detectable difference"框定结论，犯了 absence-of-evidence â  evidence-of-absence 的因果推断错误，前提（N=4 足以检验臂间效应）不成立。
- - Critical: L1b 的 LLM-as-judge 在实际评测轮次中"零调用（全 SKIP）"，校准集（gold set）与评测分布完全脱节，校准通过不能外推到真实评分；以"calibration is a methodological warrant"为由保留 judge 效度属于循环论证，L1b 所有基于该 judge 的覆盖度断言缺乏内部效度。
- - Critical: 显著性结果 p=0.0026 来自"curated L1a（6 tasks, k=4）"的事后挑选，task 子集选择本身引入选择偏差，而 Holm 校正仅"over the two non-degenerate encodings"——按结果（是否退化）决定纳入哪些检验做校正，是选择性校正，p=0.0261 不可信。
- - Critical: "P3 SHA-256 seal over 125 files verifying byte-for-byte reproducibility"混淆了"文件哈希一致"与"结果可复现"：LLM 输出具随机性，未报告温度/种子固定策略时，哈希密封不保证数值结果可复现，可复现性前提（确定性生成）未验证。
### Major（7）
- - Major: P5 引入的 Model-F（6/6）与本地 7Bâ14B 模型在规模/访问方式/可能为 API 调用上属不同类别，将其与本地小模型同纳入 Friedman 检验，模型类别作为混淆变量未控制，跨模型因果归因（"frontier 能力差异"）不恰当。
- - Major: gemma 的"intention-to-treat mean 0.355 including the failed trial as 0"将执行失败等同于任务能力为零，混淆了"系统级执行失败"与"科学推理失败"两个构念，该编码假设未经论证即偏向低估。
- - Major: L1b 全模型 0/10 存在地板效应，无方差时"stable failure taxonomy"无法被数据验证，且 1/4 正控仅证明管线可解而非评分量表有效，量表效度前提未成立。
- - Major: 单标注者、未测 inter-annotator agreement，即便 Wilson 区间报告，也只刻画抽样不确定度而非标注可靠性；"second annotator left as future work"意味着 L1b judge 信度假设（标注一致）尚未检验。
- - Major: 跨模型比较（7b/14b/gemma 在 L1a 上得分）隐含"各 task 难度等价"假设，但各模型得分来自不同 task 子集（14b: TextClassification/Zinc；gemma: Sentiment/TextSimilarity），task 难度作为混淆变量未控制，跨模型排序无内部效度。
- - Major: L2 两臂 A/F 的配对设计未说明随机化、顺序平衡或 carry-over 控制；若同一 scenario 先后跑两臂，学习/状态残留作为混淆变量未被讨论，臂间因果推断缺乏可识别性。
- - Major: "36 extra trials"在初始 532 之外事后追加，且总预算 <1000 的边界暗示存在可选停止（optional stopping），未预先注册分析计划，多重试探性分析膨胀 I 类错误。
### Minor（2）
- - Minor: "18/18 independent recomputation checks"若在同一硬件/同一种子下重算，只检验确定性而非跨环境可复现性，"independent"用词易误导。
- - Minor: N=8 supplement 仍 p=1.0000，但未报告该补样本的 n_d 与功效，补充分析的信息量同样存疑。

## 统计（stat）— ok
### Critical（2）
- - Critical: L2 仅 N=4、McNemar 功效 0.0000、可检最小效应 d_min=2.13（只够捕捉巨大效应），却把 p=1.0000 与退化 95%CI[0,0] 当作"两臂无差异"的依据——典型将"无证据"误读为"无效应"，该比较在统计上无信息量。
- - Critical: Holm 校正只对"两个非退化编码"执行、事后剔除退化比较以缩小校正基数，属选择性多重比较校正；多重性应覆盖全部已执行检验，剔除会人为保住 p=0.0261 的显著性。
### Major（7）
- - Major: 全 suite 同时报告 McNemar(L2)、Friedman(16 任务)、Friedman(6 任务 curated)、Model-F 探索性、L1b 校准等多个 p 值，却没有任何跨检验的全局多重性控制。
- - Major: L2 主结局 goal completion 以连续比例(0.1418/0.1918/0.2750)报告，却采用只处理配对二分类的 McNemar；若结局为连续/比例量，二值化会损失信息，检验选择存疑（应配对 Wilcoxon 或配对 t）。
- - Major: 将异质尺度任务的指标（Sentiment 0.2、TextSimilarity 0.533、失败 trial=0）直接平均成 ITT 均值 0.355，未做归一化或加权，该均值在统计上不可解释。
- - Major: LLM-as-judge 校准仅 21 gold、单标注者，却把 FNR=0.0000、FPR=0.0000 当精确值报告；按 rule-of-3 真实 FNR/FPR 可达约 27%/30%，且未报告 Cohen's κ 等标注者间一致性。
- - Major: Friedman 检验 k=4、n=6 时卡方近似不可靠，未给出精确/置换 p 值；CD=0.8284 也无 bootstrap 置信区间。
- - Major: 大量点估计（0.1418/0.1918/0.2750/0.6252/1.5422）未报告 SE/SD/CI，方差信息完全缺失。
- - Major: 唯一显著的 p=0.0026 未配套报告任何效应量（CLES/d 在 acronym 中定义却从未计算），无法判断实际意义大小。
### Minor（2）
- - Minor: 532 次之外另有 36 次 extra trials，若非预注册则构成可选停次/重复尝试，会膨胀 I 类错误率。
- - Minor: Wilson 仅报单侧界值(0.28/0.143)未注明置信水平或双侧区间；Zinc 1.5422 等"分数"未说明分母与量表单位。

## 实验（experiment）— ok
### Critical（3）
- - Critical: L2 对照设计彻底失效——N=4、n_d=0、McNemar 功率为 0，95% CI [0,0] 退化，"no statistically detectable difference" 在此功率下是空白措辞而非实陌结论，等效于未做对照。
- - Critical: gemma L1a 同一任务三次试跑得分 0.2000 vs 0.5330 波动剧烈，但 seed 管理却作为 "future work" 明确放弃，18/18 重算检查无法证明是 seed 固定可复现还是平均后偶然一致。
- - Critical: "curated L1a (6 tasks, k=4)" 得出 p=0.0026，与 16-task Friedman 的 p=0.3679 矛盾，明显存在任务筛选 / 编码方式搜索；Holm 仅校正 "two non-degenerate encodings" 暗示曾尝试多种编码后挑选报告，属 p-hacking。
### Major（7）
- - Major: 消融不完整——completion-guided harness (arm F) 相对 ReAct (arm A) 的各组件（completion 引导、工具调用策略、终止判据）无任何组件级消融，无法归因性能差异。
- - Major: L1b 仅有 1/4 正控制（Chemistry_000），样本太小无法证明 pipeline 可解性；同时所有模型 0/10，缺少负控制（如随机/无效输出 baseline）来确认 0/10 不是 harness bug。
- - Major: 基准不公平——3 个模型分属不同架构族（qwen2.5 vs gemma2）且参数量 7b/14b/9b 不一致，横截面对比混淆了族内缩放与族间差异；Model-F（frontier）仅出现在 L1a，L2/L1b 缺少前沿模型参照，无法定标上限。
- - Major: 超参数透明度为零——未报告 temperature、top-p、max tokens、提示策略（few-shot/zero-shot）、轮次上限；ollama 版本号不是超参数。
- - Major: 各模型试跑次数不均——gemma L1a 跑了 3 次，7b/14b 只跑 1 次，intention-to-treat 均值将 failed trial 记 0，但 7b/14b 缺少对等的多轮数据，三模型间比较基础不一致。
- - Major: 种子/随机性管理缺失——"bootstrap at step/seed level as future work with dependence caveat" 明确承认未固定 seed，36 extra trials 与 532 initial trials 的关系、重试触发条件均未说明，568 calls 中的超出部分可能引入选择性偏差。
- - Major: LLM-as-judge 校准零实陌效用——判官轮次全部 SKIP、无判决调用，21 gold（11/10）校准集过小，无标注者间一致性，"校准"只是方法学担保而非实验验证。
### Minor（2）
- - Minor: 泛化面狭窄——仅单一硬件提供商（AutoDL RTX3090）、仅 3 个小型本地模型（≤14b），4+6+10=20 个任务覆盖面有限，无跨硬件/跨推理引擎复现证据。
- - Minor: P3âP5 多轮数据采集（125 filesâ91 entries）暗示分批扩展，存在 optional stopping / peeking 风险，未说明每轮的预定终止规则。

## 新颖性（novelty）— ok
### Critical（3）
- - Critical: "Unified suite" 的核心贡献实质上是将三个已有 benchmark（AIRS-Bench、ResearchClawBench、GAIA/GAIA2）用一个 `run.json` 契约 + SHA-256 seal 捆绑在一起；未论证 "联合评估" 相比分别运行三者产生了何种原本无法获得的科学见解，增量贡献陷于工程封装。
- - Critical: GAP 缺失实证——Introduction 仅引用 `\citep{goodfellow2016deep}`（2016 年深度学习教科书）一篇，未对 GAIA、AgentBench、SciBench、ToolBench 等已有多能力/统一 agent benchmark 进行任何对比，"evaluation remains fragmented" 的 GAP 断言无文献支撑，无法证明 "unification" 是未被填补的空白。
- - Critical: 中心发现几乎全部为零结果或功效不足——L2 两臂无差异（p=1.0, N=4, McNemar power=0.0000）、L1b 全 0/10、L1a 主力模型 0â2/6；唯一显著结果（p=0.0026）来自 "curated 6 tasks, k=4, fail-as-worst encoding" 的探索性子集，属明显的事后挑选/编码 hack，suite 的区分效度未被真正证明。
### Major（3）
- - Major: 评测模型仅 3 个小型本地模型（7b/14b/9b），与 "scientific agents" 前沿严重错位；唯一 6/6 的 "P5 frontier Model-F" 未命名、未入主实验，被当作补充展示，存在以强模型单点支撑 "suite 可解" 论点的嫌疑。
- - Major: "Calibrated LLM-as-judge" 实际未发起任何 judge 调用（all SKIP），却在摘要中作为方法贡献呈现，属于未被实际使用的空架方法，贡献被夸大。
- - Major: benchmark 总规模仅 20 个任务（6+10+4），与 "Suite" / 跨三层科学能力的宏大定位不相称，外部效度存疑，难以支撑 "scientific agent evaluation" 的普适性主张。
### Minor（1）
- - Minor: "L047 audit""P3 SHA-256 seal""P5 expansion""ARS v3.11" 等标签疑为冖部无法核验的冖部流程编号，未证明相对已有审计/可复现方法论的新颖性，存在以冖部命名制造方法创新假象的嫌疑。

## 可复现（repro）— ok
### Critical（4）
- - Critical: 全文未声明任何随机种子（采样温度、top-p、系统提示、max-tokens 均缺失）；gemma 在 L1a 上"1/6→2/6 after three independent trials"恰恰暴露未控种子的方差，却把三次试跑当作复现证据，违反可复现性核心契约。
- - Critical: L1b 评分依赖的 LLM-as-judge "made zero judge calls (all SKIP)"，校准仅是"methodological warrant"——评分证据链断链，声称的"0/10 稳定失败分类"无法经judge流水线复现，复现契约名存实亡。
- - Critical: 哈希对账自相矛盾——"P3 SHA-256 seal over 125 underlying files (91 entries after the P5 expansion)"，125 文件与 91 条目关系未澄清，且未给出任何 manifest/逐文件哈希列表，"byte-for-byte reproducibility"无据可对账。
- - Critical: 数据许可完全缺失——AIRS-Bench、ResearchClawBench、GAIA2 及"13 synthetic / attack-style synthetic"gold 数据均未声明许可证与来源授权，复现者无法合法获取/再分发。
### Major（5）
- - Major: 无模型权重快照——仅给 ollama 0.32.13 版本，未提供 qwen2.5:7b/14b、gemma2:9b 的 GGUF 量化级别、权重 SHA-256、ollama Modelfile（温度/seed/num_ctx），同一 tag 在不同时间拉取的权重可能不同，无法对账。
- - Major: 配置快照不完整——仅给"AutoDL RTX3090"，缺 CUDA/驱动/OS/PyTorch/python 版本及容器镜像 digest，run.json 契约内容从未展示。
- - Major: "一键复现"承诺与事实冲突——"532 initial + 36 extra trials"中的 extra trials 及 gemma 三次独立试跑均为人手重跑，非自动化一键流程；摘要中亦无仓库 URL / 复现脚本入口。
- - Major: LLM-as-judge 校准为"single annotator, no inter-annotator agreement measured, second annotator left as future work"，judge 可复现性/稳定性零证据，却作为 L1b 评分依据。
- - Major: 统计功效与可复现性冲突未化解——L2 McNemar $p=1.0000$、$n_d=0<6$ "not-detectable"、CI 退化为 [0,0]，且"bootstrap at step/seed level as future work"，即差异检验本身不可复现复核。
### Minor（2）
- - Minor: "P3 / P5 / L047 / ARS v3.11" 等关键标签在摘要中未定义，复现者无法定位对应审计规程与版本。
- - Minor: "39 gold, 26 real + 13 synthetic with attack-style synthetic included in the synthetic count" 的合成数据生成过程、种子、生成模型未披露，合成 gold 本身不可复现。

## 写作（writing）— ok
### Critical（2）
- - Critical: 摘要声称 LLM-as-judge "passed at FNR=0.0000, FPR=0.0000"，同时又写 "the round made zero judge calls (all SKIP)"。零调用意味着无 TP/FP/FN/TN，FNR 与 FPR 应为 undefined，而非 0.0000；这是摘要内部的逻辑矛盾。
- - Critical: intention-to-treat 均值 0.355 无法从所给分量推出。若 "0.2000Ã3" 表示三次 0.2000、"0.5330Ã2" 表示两次 0.5330，加一次失败(0)，则 (0.6+1.066+0)/6=0.278；若除以 5 则为 0.333；均≠ 0.355。数字不自恰。
### Major（7）
- - Major: 摘要中 L047、P3、P5、ARS v3.11、CD、p3dev、"rad" 等术语/缩写均未定义，读者无法理解含义；"Acronyms" 注释列了 ECE/TS/GAIA/CLES 但正文实际用到的缩写反而未收录。
- - Major: 符号 "0.2000Ã3" / "0.5330Ã2" 滥用乘号 "Ã"，无法判断是 "0.2000 重复 3 次" 还是 "0.2000 Ã 3 = 0.6"；与 "1/6â2/6 after three independent trials" 叙述相结合时，3+2=5 个数据点与 "three trials" 矛盾。
- - Major: p=0.0026 出现两次——一次归属 Model-F 6/6，一次归属 curated L1a Friedman——未说明是同一检验还是两个独立检验；若为同一检验则重复报告，若为不同检验则相同 p 值需解释。
- - Major: "125 underlying files (91 entries after the P5 expansion)"ââ"files" 与 "entries" 的区别及数量跳变(125â91)朠给出合理解释，读者无法判断可复现性范围。
- - Major: 实验臂标注为 A 与 F，跳过 BâE；模型标注为 "Model-F"，暗示 AâE 存在但未提及；命名体系不连贯，令读者困惑。
- - Major: 摘要为单一 ~450 词段落，结果、统计检验、方法论警告、局限性披鲲交织，无逻辑分层；L2âL1aâL1bâFriedmanâLLM-judgeâpower 跳跃，缺乏可读性。
- - Major: "n_d=0<6 not-detectable" 符号不符规范，应写 "n_d=0 (<6, not detectable)"；"95% CI [0,0] degenerate" 报为结果似有意义，实际上退化区间不提供信息。
### Minor（4）
- - Minor: 小数精度不一致——0.355(3位)、0.28/0.143(2位)、0.0000/0.0026(4位)混用，缺乏统一报告规范。
- - Minor: "Wilson 0.28" / "Wilson 0.143" 以单数值报告 Wilson 区间，未指明是区间宽度、下界还是上界。
- - Minor: "AutoDL RTX3090, ollama 0.32.13" 在摘要中过于实现细节，庒碎核心贡献；应移至实验环节。
- - Minor: "attack-style synthetic included in the synthetic count" 同义反复——synthetic 已在 synthetic count 中，表述冗余。

## 伦理（ethics）— ok
### Critical（2）
- - Critical: 整篇未声明任何源数据集的许可证/使用权（AIRS-Bench、ResearchClawBench、GAIA2 以及 P3 SHA-256 密封的 125 个"underlying files"）；若含第三方受版权/受限协议数据，重新分发 benchmark 即构成合规违规。
- - Critical: LLM-as-judge 校准用到 "21 gold""39 gold（26 real + 13 synthetic）"且明确为"single annotator"人工标注，却无 IRB/伦理委员会批准、无知情同意、无标注员报酬与劳动保护披露——隐私与人体受试规范缺失。
### Major（4）
- - Major: 双盲完整性风险：摘要点名"AutoDL RTX3090""ollama 0.32.13"等特定国内云平台与精确版本号，形成可追踪的计算指纹，可能暴露作者机构/地区身份。
- - Major: 无利益冲突（COI）声明，却在评测商业模型（Qwen、Gemma）并命名商业平台（AutoDL、ollama），TMLR 要求披露相关性。
- - Major: 无误用/双用风险讨论；该 suite 包含无约束代码生成并执行、交互式工具调用的 agent 评测，释出后可被改造为有害自主 agent，且未声明沙箱/执行隔离安全措施。
- - Major: "attack-style synthetic" gold 数据被生成并纳入统计，却未记录基底数据来源、生成方法与危害审查，存在将敏感/泄露内容嵌入释出物的风险。
### Minor（2）
- - Minor: 内部标识符（L047、P3、P5、ARS v3.11）泄露未发布的内部流程/工具命名，可暗示作者所属，削弱匿名性。
- - Minor: 单标注员治理缺失："second annotator left as future work"仅作统计局限处理，未提及标注员工作量、报酬与督导，存在劳动伦理隐患。

## 汇总

- **Critical: 20 | Major: 40 | Minor: 15**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）