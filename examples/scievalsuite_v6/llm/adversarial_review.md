# 对抗审查报告

- 时间: 2026-08-25T17:49:39.736046+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（4）
- - Critical: N=4、退化 95% CI [0,0]、McNemar 功效 0.0000：声称"两臂无统计学可检测差异"实为不可证伪的零结果，无法支撑"两臂等价"的因果/效力推断——这是 absence of evidence 而非 evidence of absence，因果推断不恰当。
- - Critical: LLM-as-judge 全程零调用（all SKIP）：校准门控从未在真实评分中执行，所谓"methodological warrant"形同虚设，L1b 评分的内部效度断裂。
- - Critical: p=0.0026 仅在"fail-as-worst 编码 + 精选 6 任务子集（k=4）"下成立，且标注为 exploratory：研究者自由度过大，等同 p-hacking，该编码方案为何为基准的假设未论证，多重比较未校正。
- - Critical: L1b 全模型 0/10 地板效应：基准在此能力区间无区分效度，"stable failure taxonomy"为事后合理化，无法支撑"测量工作流能力"的构念前提。
### Major（6）
- - Major: McNemar 检验 n_d=0：检验前提（存在不一致对）被违反，p=1.0000 是退化值而非有效推断，携带零信息量却被当作结论呈现。
- - Major: P3/P5 多轮结果混合报告且无预注册：探索性与确证性边界模糊，跨轮多重比较未校正，I 类错误膨胀。
- - Major: "字节级可复现（SHA-256 manifest）"仅证明计算可重现，不回应构念效度——可复现 ≠ 测量的是声称的能力，前提被偷换。
- - Major: 阳性对照仅 1/4（Chemistry_000）：对"pipeline solvability"的证据过弱，无法排除"基准本身不可解"这一混淆。
- - Major: 仅 3 个模型且同属中小规模同类家族：模型选择构成混淆变量，无法区分"模型能力不足"与"基准过难"，外部效度受限。
- - Major: "oracle-free goal completion"评分机制未说明：去除 oracle 后目标达成如何判定引入主观评分混淆，臂间差异的因果归因被评分者偏差污染。
### Minor（2）
- - Minor: L047 answer-fitting 审计本身未经独立验证：审计的假阳/假阴率未知，可能系统性偏置 L1b 结果。
- - Minor: Friedman on 16 paired tasks 仅 3 个模型：CD=0.8284 但 df=2，检验严重欠功效，"非显著"同样不可作等价结论。

## 统计（stat）— ok
### Critical（3）
- - Critical: L2 的 exact McNemar 检验在 n_d=0（零不一致对）时退化，p=1.0000 与 95% CI [0,0] 是数学平凡值而非有意义的统计推断，将其作为"两臂无差异"的证据属于 p 值误用——零不一致对意味着检验本身不携带任何信息。
- - Critical: 声明 McNemar power=0.0000（n_d=4 时）即承认该检验在 N=4 下对任何效应都无检测能力，却仍以"no statistically detectable difference"作为结论呈现，混淆了"无证据发现差异"与"证据表明无差异"（absence of evidence ≠ evidence of absence）。
- - Critical: 全文报告了至少 4 个独立 p 值（McNemar p=1.0000、Friedman p=0.3679、L1a frontier p=0.0026、judge 校准通过判定），横跨 3 模型 × 3 层 × 多子任务，未见任何多重比较校正（Bonferroni / BH-FDR），p=0.0026 仅标注"exploratory"不构成对 family-wise error 或 FDR 的控制。
### Major（5）
- - Major: 所有效应量/分数（如 0.1418、0.1918、0.2750、0.355、0.6252、1.5422 等）均以点估计报告，未附带标准差、标准误或非退化置信区间；L2 的 95% CI [0,0] 退化，不提供任何精度信息，方差报告缺失。
- - Major: LLM-as-judge 校准以 21 条 gold（11 正 / 10 负）声称 FNR=0.0000、FPR=0.0000"passed"，但零误差观测在 n=21 下的单侧上界约为 3/21≈14%（rule of three），不能等价于真错误率为零，属于小样本下的效应量/误判率误用。
- - Major: "simulated second annotator α=0.894"为模拟而非真实第二标注者，Cohen's κ 的取值不具备经验效度；以此作为标注可靠性担保属于统计量的虚构报告。
- - Major: Friedman 检验（χ²=2.0000, p=0.3679）应用于 L1b 全 0/10、L1a 多为 0/6–2/6 的极端稀疏且高度并列（ties）数据，秩值几乎无区分度，Friedman 的渐近/精确近似前提受严重违反，结果不可信。
- - Major: "532 initial + 36 extra trials"表明在预设预算外追加试验，但未说明停止规则或预注册方案，存在 optional stopping / p-hacking 风险。
### Minor（2）
- - Minor: Wilson 区间报告不完整——"Wilson 0.28 at FPR=0"未指明对应 n 与置信水平；在 21 样本下 Wilson 下界 0.28 意味着上界仍很宽，不足以支撑"校准通过"的强主张。
- - Minor: d_min=2.1279（80% power）对应 Cohen's d>2.0 的超大效应，虽已披露但未提供补救方案（如增大 N 或改用等效性检验 / TOST 来正式支持"无差异"主张）。

## 实验（experiment）— ok
### Critical（3）
- - Critical: L2 的 A vs F 是空对照——两臂逐模型均值完全相同 (0.1418/0.1918/0.2750)、McNemar p=1.0000、n_d=0<6、N=4、功效自认 0.0000；completion-guided harness 要么无作用要么实验根本检测不出，该对照无统计意义也无消融价值。
- - Critical: L1b 的 LLM-as-judge 整轮零调用 (all SKIP)，所标榜的校准 (FNR/FPR gate、Wilson) 从未在真实数据上运行，核心评估方法未被执行，等于该层消融缺失。
- - Critical: 显著性靠挑选制造——16 任务 Friedman p=0.3679 不显著，却在 curated L1a (6 任务) 且仅 under fail-as-worst 编码下得到 p=0.0026，子集选取 + 编码选择双重 p-hacking。
### Major（6）
- - Major: seed 管理缺失——未报告任何随机种子/温度/top-p，却声称 SHA-256 字节级可复现 (46 与 165 条目数还自相矛盾)，且 bootstrap at step/seed level 列为 future work，自认依赖性未处理。
- - Major: 对照不公平的重跑——仅 gemma 在 L1a 做"三次独立试验" (且逐任务次数 ×3/×2 自相矛盾)，7b/14b 似为单次；36 条 extra trials 的分配规则未披露，引入选择性偏差。
- - Major: 基准跨层不公平——唯一前沿模型 muse-spark-1.2 仅在 L1a 跑 6/6 且标 exploratory，未上 L2/L1b，无法与跑满三层的本地模型做同协议跨档对照。
- - Major: 泛化薄弱——仅 3 个小模型 (7b–14b)、2 个家族；"规模消融"被家族混淆 (gemma2:9b vs qwen2.5:14b 不同族)；L2 仅 4 场景、L1a 6 任务、L1b 10 任务，样本极小。
- - Major: L1b 三模型全 0/10 无区分度，正向对照仅 Chemistry_000 1/4，基准可解性与判别力未建立，该层无有效实验信号。
- - Major: simulated second annotator α=0.894——第二标注者为模拟而非真实，标注者间一致性从未实测，校准外部效度存疑。
### Minor（2）
- - Minor: 同一模型同一指标既报成功计数 (0/6→2/6) 又报连续分 (ITT 均值 0.355)，口径混用未统一。
- - Minor: 仅钉死 ollama 0.32.13 版本，未报告采样超参数 (temperature/top-p/seed)，复现契约不完整。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 核心GAP（"评估碎片化"）的解决方案实质上是把三个已存在基准（AIRS-Bench、ResearchClawBench、GAIA2）拼接进同一个 `run.json` 契约；论文未论证"统一契约"在测量维度上比三者各自运行多揭示了什么能力，增量贡献被包装为"统一基准"而实质为可复现性工程封装（SHA-256清单、重算校验），属工程而非研究贡献。
- - Critical: 首次部署产出几乎全为零信号（L1b 三模型均 0/10；L2 McNemar p=1.0000、N=4、功效0.0000；跨模型 Friedman p=0.3679 非显著），一个在其主要对比上无法检出差异的基准，未提供任何判别力证据，基准的存在价值本身存疑。
### Major（5）
- - Major: 三个组成基准均被引用为既有工作，论文未指出统一harness能测量到三者单独无法测量的属性，"统一"的增量仅是元数据/契约层，却以"unified benchmark"作为标题级主张，贡献被夸大。
- - Major: 统计协议（exact McNemar、Wilcoxon+CLES、Friedman+Nemenyi+CD）均为教科书标准方法，却被列为"three-layer statistical protocol"作为贡献项，方法论新颖性不成立。
- - Major: LLM-as-judge 校准在本轮"zero judge calls (all SKIP)"，即未在实际评分中调用，却以"calibrated LLM-as-judge"出现在摘要与贡献中，该评估方法论贡献未被任何真实评分验证。
- - Major: "denominator discipline（失败计零并保留分母）"是ML评估的常规做法，不构成贡献；将其列为协议特征夸大了新颖性。
- - Major: 摘要将 P5 frontier（muse-spark 6/6, p=0.0026）作为亮点呈现，但该结果被自标为 exploratory、仅在某编码下显著、且为单一前沿模型，用以支撑基准有效性的力度被高估。
### Minor（1）
- - Minor: "L047 audit intercepting Material answer-fitting in 3/3 models"作为单任务单点审查，其作为基准内置防作弊机制的普适性与新颖性未与现有 answer-fitting/contamination 审查文献对比。

## 可复现（repro）— ok
### Critical（2）
- - Critical: 摘要声称 "byte-for-byte reproducibility"（46/165 条 SHA-256 manifest），但同一 gemma2:9b 在 L1a 上"三次独立试验"分数从 0/6 变为 2/6（Sentiment 0.2000×3、TextSimilarity 0.5330×2），证明生成是非确定性的；全文未报告任何采样 seed / temperature / top-p 固定，manifest 只能哈希静态产物，无法复现随机生成过程，"byte-for-byte" 与现象自相矛盾。
- - Critical: 模型未按权重 digest 固定——`qwen2.5:7b/14b`、`gemma2:9b`、`llama3.1:8b`、`muse-spark-1.2-contributor` 均为可漂移的 ollama/产品标签，可被重拉成不同 blob；配置快照只 pin 了 `ollama 0.32.13`，缺模型 SHA、CUDA/驱动版本、容器镜像哈希、AutoDL 实例镜像与地区，环境快照不完整。
### Major（7）
- - Major: 哈希对账证据链断裂——"46-entry manifest" 与 "165 entries with P5" 口径不一致，且未说明哈希覆盖对象（输入/输出/中间态/judge 调用）；568 calls（532+36 extra trials）是否全部入账、与 manifest 条目的映射表缺失，无法逐 call 对账。
- - Major: "18/18 independent recomputation checks passing" 中"独立"无定义——未说明是否换实例/换 seed/换容器重跑，极可能是同机原地重算，非真正第三方独立复现，证据强度被高估。
- - Major: 三个被测基准（AIRS-Bench、ResearchClawBench L047、GAIA2 p3dev）的数据许可、来源条款与再分发权全文未述，一键复现的合法性前提缺失，复现者可能因许可无法获取同一数据。
- - Major: 声称 "fully recomputable harness / budget-controlled"，但未给出单一命令/Makefile/容器入口与 `<1000` 预算的强制机制（如何阻止超支、如何回滚 extra trials），"一键复现"无落地证据。
- - Major: LLM-as-judge 校准"该轮零调用(all SKIP)"却作为方法学担保写入摘要，且 judge 模型 llama3.1:8b 未按 digest 固定，校准结果（FNR/FPR=0）无法被复现或证伪，证据链为空。
- - Major: "36 extra trials"（532→568）出现在 run.json 合同之外，未交代触发条件、是否入档、是否进入哈希对账，存在选择性补跑污染证据链的风险。
- - Major: P5 frontier `muse-spark-1.2-contributor`（6/6, p=0.0026）的模型来源、版本、权重哈希、访问权限均未披露，frontier 结论不可复现；且 P5 的 165 条 manifest 与主实验 46 条是否同一套对账流程未说明。
### Minor（4）
- - Minor: "single canonical script" 未给 commit hash / 自身 SHA / 版本号；ARS v3.11 规范未提供可校验的 pin（URL+digest），脚本与规范本身不可复现。
- - Minor: L047 audit 的判定规则/阈值/触发逻辑在摘要中无可复现定义，"3/3 models 拦截 answer-fitting" 的判定证据无法独立复核。
- - Minor: AutoDL 云实例仅记录 RTX3090，未记录实例镜像 ID、地区、运行时间戳与资源争用情况，云环境漂移与排队噪声未控；文档已被截断，配置快照/附录部分无法核实是否补齐上述缺口。
- - Minor: McNemar $n_d=0$、$N=4$、95% CI $[0,0]$ degenerate、power=0.0000，却作为"两臂无差异"的可复现证据呈现，实质为不可检测而非无差异，证据链表述误导。

## 写作（writing）— ok
### Critical（1）
- - Critical: æè¦å "39 gold, 30 real+9 synthetic+1 attack"ï¼ä½ 30+9+1=40â 39ï¼åæ¯èªç¸çç¾ã
### Major（9）
- - Major: L1a ä¸­ 14b ç Zinc å¾å 1.5422>1ï¼ä¸ææå
- - Major: "three cloud-hosted local models" æ¯çç¾æ¯è¯­ââcloud-hosted ä¸ local äºæ¥ï¼åºæç¡®"äºç§ GPU ä¸æ¬å°é¨ç½²çå¼æºæ¨¡å"ã
- - Major: æè¦å£°ç§° LLM-as-judge "passed at FNR=0.0000, FPR=0.0000"ï¼ç´§æ¥çåè¯´ "the round made zero judge calls (all SKIP)"ï¼é¶è°ç¨ä¸ç"éè¿"æ¯ç©ºçï¼è¡¨è¿°èªç¸çç¾ã
- - Major: "a 46-entry SHA-256 manifest â¦ (165 entries with P5)" åä¸å­å¥å
- - Major: p=0.0026 æ¢åºç°å¨ "P5 frontier muse-spark 6/6" ååºç°å¨ "curated L1a (6 tasks, k=4)"ï¼æªè¯´ææ¯åä¸æ¬¡ Friedman æµè¯è¿æ¯ä¸¤æ¬¡ï¼è¥åä¸æµè¯åéå¤å¼ç¨ï¼è¥ä¸¤æ¬¡åå®å
- - Major: intention-to-treat mean 0.355 æ æ³ç±ååºç 0.2Ã3 + 0.533Ã2ï¼+ å¤±è´¥è®° 0ï¼å¤ç°ï¼å¾ 0.278 æ 0.333ï¼ï¼ä¸ "three independent trials" ä¸ Ã3+Ã2=5 ä¸ª trial-å¾åç¸å²çªã
- - Major: L1b "0/10 for all models"ï¼å´åå P5 æ­£å¯¹ç
- - Major: æè¦ä¸­ P5ãARS v3.11ãL047 å¤æ¬¡åºç°ä½æªå®ä¹ï¼è¯»è
- - Major: æè¦ä¸ºåæ®µè¿ 400 è¯ãå ç  40+ ä¸ªæ°å­ï¼å¹¶åºç° "(see sensitivity)" æ­£æäº¤åå¼ç¨ï¼ä¸æ æ±æ»è¡¨æ¿æ¥è¿äºå¯éæ°å¼ï¼ç»æå¤±è¡¡ã
### Minor（6）
- - Minor: æè¦å "AIRS-Bench"ï¼å¼è¨å "AIRS-Bench rad"ï¼åç§°ä¸ä¸è´ã
- - Minor: L2 åè¯æ¹æ æ³¨ä¸º A ä¸ Fï¼æªè§£é BâE çç¼ºå¤±ï¼è¯¯å¯¼è¯»è
- - Minor: "0.2000Ã3" ç¬¦å·æè¯¯è¯»ä¸ºä¹æ³ï¼0.2Ã3=0.6ï¼ï¼åºåæ "3 trials, each 0.2000"ã
- - Minor: "Wilson 0.28" ä¸ "Wilson 0.143" æªè¯´ææ¯ä¸çãå®½åº¦è¿æ¯ä¸­ç¹ï¼ä¸å°æ°ä½æ°ä¸ä¸ï¼0.28 vs 0.143 vs 0.355ï¼ã
- - Minor: "ollama 0.32.13" çæ¬å·æ ¼å¼å¼å¸¸ï¼"GAIA2 p3dev" æä¸çå® GAIA benchmark æ··æ·ï¼åå¾
- - Minor: "simulated second annotator Î±=0.894"ââ"æ¨¡ææ æ³¨è

## 伦理（ethics）— ok
### Critical（3）
- - Critical: "muse-spark-1.2-contributor" 作为 P5 frontier 被评测且其结果（6/6, p=0.0026）被加粗强调——"contributor"字样强烈暗示作者即该模型贡献者，构成未披露的利益冲突，同时违反 TMLR 双盲匿名（泄露机构归属）。
- - Critical: 全文未声明所用第三方基准（AIRS-Bench、ResearchClawBench、GAIA2 p3dev）的数据许可与再分发授权，尤其 "GAIA2 p3dev" 是否为 GAIA 的授权衍生品、L047 审计来源均不明确，存在侵权与合规风险。
- - Critical: L1a 要求"代码生成后本地执行"、L2 为"交互式环境执行 / 完成引导式 harness（F 臂）"，但全文未披露沙箱隔离、执行权限边界或安全护栏，且承诺公开发布"可重算 harness"，误用风险（任意代码执行、自动化滥用）未被评估或缓解。
### Major（4）
- - Major: 无 IRB/伦理审查声明；GAIA 类任务可能涉及真实网页与个人可识别信息，而 L1b 报告由 LLM 合成、judge 读取，PII 与隐私数据处理流程缺失。
- - Major: "simulated second annotator α=0.894"——以模拟而非真实第二标注者冒充标注一致性，属于方法学层面诚信问题，可能掩盖真实标注分歧与偏差。
- - Major: P5 中 "9 synthetic + 1 attack" 金标准条目未说明合成数据的生成方式、来源模型、许可及"attack"项性质，合成评测数据混入官方指标可能污染结论并引发可重复性与公正性质疑。
- - Major: 计算在 AutoDL（境外/第三方云 GPU）进行，模型（Qwen、Gemma、Llama）各自许可（Apache-2.0、Gemma Terms、Llama Community License）合规性未声明，且任务数据上云的隐私与数据主权影响未讨论。
### Minor（2）
- - Minor: "L047 audit" 作为拦截"Material answer-fitting"的关键机制，其定义、出处、是否为作者自有工具未交代，影响审计中立性与可复现性。
- - Minor: 评测臂 F=completion-guided harness 对完成度的增强能力本身具双用途性，但未附 misuse/双用途风险评估或使用条款。

## 汇总

- **Critical: 18 | Major: 42 | Minor: 19**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）