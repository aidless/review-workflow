# 对抗审查报告

- 时间: 2026-08-27T06:39:22.214702+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（6）
- - Critical: L2 双臂对比（A=ReAct vs CG）在 N=4 且 n_d=0（零不一致对）条件下，McNemar 检验结构性地无法产生任何信息；但仍报告 per-model 均值（0.1418/0.1918/0.2750）并暗示"两臂无差异"，这在统计上是无意义的——前提"该设计能检测臂间差异"不成立，因果推断（臂→效果）无效力。
- - Critical: 事后策展 L1a 子集（6 tasks）得到 p=0.003：依据观测方差选择任务属于对因变量的选择偏差（selection on outcome）；即使标注"exploratory"，该 p 值仍以结果为条件，不具备任何频率派有效性，p=0.003 不可作为证据引用。
- - Critical: Friedman 检验在 16 个配对任务中含 10 个全零任务（62.5%）：全零任务中所有模型并列同秩、贡献零信息，Friedman 的排序假设在 10/16 任务上被违反；有效样本量约 6，"非显著（p=0.37）"是地板效应伪影而非"无差异"的证据。
- - Critical: L1b 的 LLM-as-judge 管线在本轮实际运行中零次调用（all SKIP），核心贡献（report coverage 评判）从未在真实模型输出上执行；gold-set 校准仅是必要条件，不能替代对真实数据的有效性验证——内部效度为零。
- - Critical: gemma2:9b 在 L1a 上获得 3 次独立试验而 7b/14b 仅 1 次：采样次数与模型身份完全混淆，"1/6→2/6"可能是多试次抽奖的噪声而非模型能力提升；因果归因（模型→分数）被混淆变量（试次数）污染。
- - Critical: 效力不足且不可证伪：N=4、d_min=2.1279（属"巨大"效应量）意味着只有极端效应可检出；"McNemar power 结构性为 0"等于声明 L2 研究在设计上无法检出任何合理效应——"未发现差异"不携带任何信息量，研究在 Popper 意义上不可证伪。
### Major（5）
- - Major: 判官校准仅用单一标注者，无标注者间一致性报告；21（或39）个 gold 上 FNR=0.00/FPR=0.00 的置信区间极宽（如 39 项零错误，FPR 单侧 95% 上界约 7.4%），"通过校准"是对完美率的过度声称。
- - Major: 跨层级/层内指标不兼容：L1a 混用二值 pass@1（0/6、2/6）与连续 TextSimilarity ITT 均值（0.355）；跨层 Friedman 将 L1b 二值执行成功与 L2 连续 goal completion 混合排序，对异质度量做 Friedman 秩比较假设不成立。
- - Major: "独立重算检查（18/18 passing）"混淆了聚合算术的可复现性与测量的有效性：从同一份 raw per-seed rows 经另一条 scipy 路径重算仅验证四则运算，不验证原始数据采集是否正确或度量定义是否构念有效。
- - Major: 跨模型混淆：qwen2.5:7b/14b（同族不同尺度）与 gemma2:9b（异族/异架构/异训练数据）在尺度、架构、训练数据三个维度上同时变化；将分数差异归因于"模型能力"而未解耦这些混淆变量，因果推断不当。
- - Major: SHA-256 文件封条（125 files byte-for-byte）≠ 结果可复现性：harness 文件字节一致不解决 LLM 输出随机性；相同 harness+相同 seed 在不同 serving 环境（量化、批处理、延迟）下仍可能产生不同输出，"可复现"前提过强。
### Minor（3）
- - Minor: 校准 gold 集规模不一致（21 vs 39"expanded set"）未说明扩充判据及新增 18 项的采样方式，可能引入选择偏差。
- - Minor: frontier Model-F 在 6 个任务上 6/6 作为 positive control：N=6 且单一参考模型，对"任务集可解性天花板"的论证过于薄弱。
- - Minor: "cloud-hosted local models"引入未受控的基础设施混淆：serving 延迟、批处理策略、量化精度差异可能独立于模型能力影响 agent 行为。

## 统计（stat）— ok
### Critical（3）
- - Critical: post-hoc âcuratedâ L1a 子集（6 tasks）给出 p=0.003，但子集是事后挑选的，无任何多比较校正（如 Bonferroni/Holm 或预设登记的子集），标注“exploratory”不能抵消选择偏倚对类型 I 误误的膨胀，属典型 p-hacking。
- - Critical: Friedman 检验纳入 16 个配对任务中 10 个为全零（floor），全零任务不产生任何排序信息、且引入大量平局，标准 Friedman 的 ÏÂ² 统计量在此情形下失真；应剔除 floor 任务或改用含平局校正/置换的 exact Friedman。
- - Critical: LLM-as-judge 校准报告 FNR=0.00、FPR=0.00（N=21，扩展集 39），但未给出二项比例的置信区间；按“rule of three”，0/21 的 95% 上界约 14%、0/39 约 7.7%，“passed at 0.00”属小样本下对零误差的误读。
### Major（5）
- - Major: 多处报告均值（goal completion 0.1418/0.1918/0.2750、TextSimilarity mean 0.355）均未附 SD/SE/CI，无法判断估计不确定性，方差报告缺失。
- - Major: 显著结果（L1a post-hoc p=0.003）仅报 p 值，未报告效应量（如 Kendall W、平均序差、或 Nemenyi 的 q/r 统计量），无法评估实际效应大小是否与 p 值相称。
- - Major: 存在多个并行检验（McNemar、FriedmanÃ2、Wilcoxon+CLES、judge FNR/FPR），未提及任何 family-wise 或 FDR 多比较控制，整体类型 I 误失控。
- - Major: L2 的 McNemar 使用 N=4（补充 N=8）、discordant n_d=0，并自报 power âstructurally 0”、d_min=2.1279；这等于坦言设计无法检出任何现实效应（d>2 属“巨大”），该 arm 对比在统计上无效，应明确宣布不假设检验而非报“p=1.00”。
- - Major: Friedman（3 modelsÃ6 tasks）依赖 ÏÂ² 渐近近似，样本规模过小，应改用 exact/permutation Friedman 并报告其 p 值与效应量。
### Minor（3）
- - Minor: âintention-to-treat mean 0.355”的计算基源未说明（是 task 均值还是 trial 均值、与 1/6â2/6 的换算关系不清），影响复现与解读。
- - Minor: judge gold 为单标注者，未报告标注者间一致性（如 Cohen's κ），校准的可靠性缺乏人工基线。
- - Minor: CLES 作为效应量被引入但未给出置信区间（bootstrap 列为 future work），效应量估计无不确定性。

## 实验（experiment）— ok
### Critical（3）
- - Critical: L2 的 A/CG 双臂对照在三个模型上均值完全相同（0.1418/0.1918/0.2750 两臂一致）、discordant 对 n_d=0、McNemar 势"结构性为 0"——该对照实验零信息量，无法支撑任何关于 CG harness 的结论，却作为核心"两臂"设计呈现，且 N=8 补充同样 p=1.00 说明设计本身检测不到臂间差异。
- - Critical: L1b 三个模型全部 0/10（完全地板效应），整层无信号，仅靠单一 positive control 证明"管线可解"，cross-model Friedman 含 10 个全零任务后仍不显著——该层的统计与泛化结论均无依据。
- - Critical: 重试/seed 策略在模型间不一致——gemma2:9b 在 L1a 做"三次独立试验"(1/6→2/6) 而 7b(0/6)/14b(2/6) 似乎只跑一次，破坏基准公平并将 seed 变异与模型能力混淆；同时对 gemma 还另报 TextSimilarity(ITT 0.355) 的异质指标，跨模型口径不统一。
### Major（8）
- - Major: 仅有的消融是 A vs CG 双臂且结果为 null；answer-fitting 审计(L047)、分母纪律、judge 校准、三层统计协议等核心组件均无消融，无法判断任一组件的贡献或必要性。
- - Major: L1b 的 LLM-as-judge 在真实运行中零调用（全 SKIP），校准集(FNR=0/FPR=0, 21→39 gold, 单标注者)从未在真实数据上验证，judge 实际有效性存疑且 gold 集无标注者间一致性。
- - Major: 主基准仅跑 3 个小型本地模型(7b/14b/9b)，唯一前沿/API 参考(deepseek-v4-flash 5/6、Model-F 6/6)均标注为 exploratory 且不入主比较，泛化到更强模型/其他家族的证据严重不足。
- - Major: 样本量极小（L2 N=4、L1a 6 题、L1b 10 题），作者自述 McNemar 势为 0、Friedman floor-limited、bootstrap 列为 future work——整套实验在统计上欠势，任何"无差异"结论都不可作确认性解读。
- - Major: "post-hoc curated L1a subset(6 tasks) p=0.003(exploratory)"为同一数据上事后子集选择，构成多重检验/挑樱桃，该 p 值不可解释，应做预注册或 Bonferroni 校正。
- - Major: seed 管理不透明：声称 per-seed rows 与 SHA-256 字节级可复现，但未说明 seed 数量、随机解码如何固定/缓存、为何仅 gemma 多次试验；seed 级 bootstrap 被推迟，字节级 seal 无法证明随机性受控。
- - Major: 超参数未报告：temperature/top-p/max_tokens/system prompt、ReAct 与 CG harness 配置、1000-call 预算在各任务/模型/层间的分配（568/1000 用法）均缺失，agent 行为无法复现评估。
- - Major: L1b judge 为 llama3.1:8b，与被评模型体量相当且真实零调用，judge 公平性与能力双重未验证；无 judge 消融或换 judge 的稳健性检查。
### Minor（2）
- - Minor: "cloud-hosted local models"表述自相矛盾（本地还是云？），部署形态与可复现性获取路径不清。
- - Minor: Friedman 的 16 配对任务中含 10 个 L1b 全零任务，全零行扭曲配对比较，应剔除或对全零层单独分析，避免人为稀释/膨胀秩统计。

## 新颖性（novelty）— timeout
### Critical（3）
- - Critical: GAP-1 是"合取式交集 gap"——"无先验基准同时报告三层 + oracle-free completion + 预算≤1000 + 预注册校准 judge + 字节级 manifest"。不断追加合取项直到无人匹配，近乎同义反复，并非真实科学缺口；Table 1 各行的"Limitation"全是"缺另一层"，构成循环论证。
- - Critical: 四个"新元素"中三个在主实验里经验性空转——CG 臂零可检测差异（p=1.00、n_d=0、power 结构性为 0）；校准 judge 全程零调用（all SKIP，从未在真实报告上执行）；L047 audit 仅在 Material 任务上 3/3 验证、其余任务无 gold 集未量化 P/R。标题级新意缺乏已验证的科学信号。
- - Critical: 基准的区分效力被作者自承未验证（Limitations：所有 SUT 7–14B 近地板，0/6、2/6、0/10）；唯一能跑通的是作者自家的 Model-F（6/6），且为探索性单 trial、COI 已披露。一个尚未证明能区分模型的测量工具不构成可发表贡献。
### Major（6）
- - Major: "统一"是套在三个外部异质管线（不同 scorer/judge/metric）上的 run.json 包装；Intro 所动机的"fragmentation"在套件内部并未真正消解——scoring/judge/metric 仍各异，统一仅为契约层 cosmetic。
- - Major: Contribution(3) 把"一致不可检测的引导效应"列为贡献，但作者自己反复声明该 null 零统计信息（N=4、power=0）；把无信息量的 null 当贡献是夸大。
- - Major: 唯一显著结果 p=0.003 被明确标注 post-hoc、curated、exploratory，且附录显示对 fail 编码敏感（k=3 fail-as-worst p=0.05，fail-as-0 p=0.37，fail=NaN 退化为 0 任务）。论文唯一的"正向"经验信号既不稳定也非确认性。
- - Major: "oracle-free goal completion"标签自相矛盾——指标定义为"被 oracle 动作覆盖的比例"，依赖 oracle；而对照的 PaperArena 才是真正 oracle-free。该"新度量"的新颖性被错误标签夸大，且相对 PaperArena 无实质增量。
- - Major: Contribution(2)（SHA-256 manifest、18/18 recompute、Dockerfile、210 pins）属可复现性工程规范，且 CORE-Bench 已做 VM 级 repro；将工程卫生升格为核心贡献属增量夸大。
- - Major: Contribution(5)（"完整失败 taxonomy + 功效披露"）本质是 limitations 章节改写为贡献；失败 taxonomy 已在 ProjectEval（被引）中存在，增量有限。
### Minor（3）
- - Minor: L047 是"内部 audit 标识符"却被提升为具名贡献；给内部规则命名会放大感知新颖性。
- - Minor: Discussion 把"开发期抓到三个自身 bug"包装为"仪器首要效用"（primary utility）；抓自己 dev bug 不构成科学贡献。
- - Minor: Intro 用 \citep{goodfellow2016deep}（教材）支撑"advancing rapidly"，唯一动机性引用与基准文献无关，削弱 gap 论证的相关性。

## 可复现（repro）— ok
### Critical（5）
- - Critical: 模型只给 Ollama 标签（qwen2.5:7b/14b、gemma2:9b、llama3.1:8b）未给权重 SHA-256/digest，标签会随时间漂移；serving 栈（Ollama/vLLM/llama.cpp 版本）未固化，本地端点不可复现。
- - Critical: "deepseek-v4-flash / Model-F" 为 API 黑盒且 "v4-flash" 并非已发布型号，疑似虚构；API 模型随时下线/改版，无版本号、无快照、无回放凭证，6/6 结果不可复现。
- - Critical: 声称 "125 文件 SHA-256 seal、byte-for-byte 可复现"，但 LLM 输出本质随机，未披露 temperature=0/固定解码 seed/贪婪解码；且未列出 125 文件 manifest 与"封的是输入还是含随机输出"，哈希对账无法核验、claim 不可信。
- - Critical: A=ReAct 与 CG=completion-guided 两臂在三个模型上 mean goal completion 完全相同（0.1418/0.1918/0.2750）且 McNemar n_d=0，要么两臂功能等价（CG 无效），要么复用同一缓存输出/seed，二者都破坏独立可复现性且未诊断根因。
- - Critical: 全文未给出可一键复现的产物——无 repo URL、无 DOI、无 Docker 镜像、无 requirements.txt/environment.yml、无 run.sh；"fully recomputable harness" 仅为口头声明。
### Major（7）
- - Major: 数据许可缺失——AIRS-Bench / ResearchClawBench / GAIA2 的 license（GAIA 有特定 CC 许可）均未声明，再分发与商用可复现性存疑。
- - Major: "per-seed rows" 与 "gemma 三次独立 trial" 未披露 seed 取值、seed 数量、随机源；GAIA2 多步环境的 RNG/工具随机性未 seed，环境执行不可复现。
- - Major: "18/18 independent recomputation checks" 仅从 raw per-seed rows 重新聚合（scipy 路径），证据链在 LLM 生成环节断裂——raw rows 本身是随机输出、未被独立重生成校验，"复算"≠"复现"。
- - Major: 无配置快照——temperature/top-p/max_tokens/system prompt/prompt 模板/检索库版本/工具版本全部缺失，run.json 契约内容未展示。
- - Major: L1a gemma "1/6→2/6 after three trials" 实为 best-of-3 取最优，与"单次可复现"矛盾；intention-to-treat 把失败 trial 记 0 又同时报 2/6，复现口径不统一。
- - Major: 校准过的 LLM-as-judge 在真实 run 中"zero judge calls (all SKIP)"，校准仅为离线 warrant，运行期无证据，judge 通道不可复现/未实跑。
- - Major: "568 calls (<1000 budget)" 的 "call" 计量单位跨三层未定义（prompt token？回合？工具调用？），预算约束无法被第三方对账。
### Minor（3）
- - Minor: "separate scipy path" 未锁 scipy/Python 版本，统计复算仍可能因版本漂移而变。
- - Minor: "rule L047, an internal audit identifier" 为内部不透明标识，外部无法复现/审计 answer-fitting 检测逻辑。
- - Minor: bootstrap "as future work"——无 seed/step 级重采样 CI，统计不确定性不可复现。

## 写作（writing）— ok
### Critical（1）
- - Critical: 摘要称“frontier Model-F scored 6/6”，而引言称 API-model referenceâdeepseek-v4-flash, 5/6”，二者显然指同一前沿参考模型，却给出 L1a 得分 6/6 与 5/6 两个矛盾数值，构成摘要–正文数字矛盾。
### Major（4）
- - Major: 摘要描述三模型为“three cloud-hosted local models”，“cloud-hosted”与“local”自相矛盾；引言又一致地写为“local models served via a local OpenAI-compatible endpoint”，术语自相打架。
- - Major: âpost-hoc curated L1a subset (6 tasks)”误导—L1a 总任务数在摘要与引言中均为 6，“subset(6)”实为全集，把全集称为“curated subset”会虚高 p=0.003 的选择性印象。
- - Major: âmean goal completion was 0.1418(7b), 0.1918(14b) and 0.2750(gemma) in both arms”既歧义又不合理—两套不同 harness（ReAct vs CG）对三个模型给出到小数点后四位完全相同的均值，未说明是“每臂相同”还是“双臂合并均值”，两种读法都成问题。
- - Major: 摘要为单段约 300 词，将主结果、方法细节、功率披露（d_min=2.1279、McNemar power âstructurally 0”）与校准caveat 揉在一起，埋没了核心发现，首读不可复现，结构失败。
### Minor（5）
- - Minor: 基准名在摘要为“AIRS-Bench”、引言中为“AIRS-Bench rad”，核心组件命名不一致。
- - Minor: âModel-F”与度量“TextSimilarity”在摘要中直接使用却未定义/展开；注释声称 ECE、TS 已“defined”但正文可见部分从未出现。
- - Minor: 引言承诺“three-layer statistical protocol”含 Wilcoxon+CLES，但摘要只报告 McNemar 与 Friedman，缺少 Wilcoxon/CLES 结果，存在方法–结果缺口。
- - Minor: 已加载 booktabs 与 graphicx，但可见稿中无任何表格或图；24/18/30 行结果与多个 p 值应以汇总表/CD 图呈现，而非埋于散文。
- - Minor: âSciEvalSuite”既在标题又列入关键词，冗余；“deepseek-v4-flash”借用 Google â-flash”命名习惯且非已文档化的 DeepSeek 发行版本，削弱术语可信度。

## 伦理（ethics）— ok
### Critical（1）
- - Critical: 未声明上游基准/数据集（AIRS-Bench、ResearchClawBench、GAIA2 p3dev）与模型权重（Qwen2.5、Gemma2、LLaMA3.1、DeepSeek）的许可与再分发授权，却计划发布 125 个文件及原始每种子行，存在版权/许可违规风险。
### Major（6）
- - Major: 隐私风险：L2 环境执行可能触发真实网页/工具/API 调用，且发布原始输出与 manifest 未说明 PII、密钥、凭证或个人数据的脱敏与审计流程。
- - Major: 使用外部 API 模型 deepseek-v4-flash 会把基准数据外传第三方，缺少数据处理协议、隐私合规与该服务商使用条款核查。
- - Major: 双盲风险：匿名投稿期间承诺发布可逐字节复现的代码/数据/SHA-256 manifest，但未说明匿名化发布方案，仓库元数据/commit/署名可能造成去匿名化。
- - Major: 利益冲突：评估商业第三方模型并发布基准，但未披露资金、算力赞助、与模型提供方关系或 COI 声明。
- - Major: 误用风险：harness 自动生成并执行模型代码与多步工具动作，未说明沙箱隔离、安全过滤、速率限制、可接受使用条款或负责任发布许可。
- - Major: 人工标注/校准（21 gold、单标注者）未说明是否为作者，缺少 IRB/知情同意/报酬与标注者隐私合规。
### Minor（1）
- - Minor: 发布包未指定 SciEvalSuite 自身许可证或限制有害用途条款；Model-F 匿名而其他模型具名，可能掩盖相关利益或可复现性。

## 汇总

- **Critical: 22 | Major: 41 | Minor: 20**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）