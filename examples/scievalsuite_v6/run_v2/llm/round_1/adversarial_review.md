# 对抗审查报告

- 时间: 2026-08-25T19:11:35.460690+00:00
- 源: F:\deepseek\papers\scievalsuite\paper\main.tex
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（5）
- - **Critical**: L2 "no statistically detectable difference between arms" 的断言在 N=4、n_d=0、McNemar power=0.0000 的条件下属于经典的 "absence of evidence â  evidence of absence" 谬误；论文将零功率下的不显著结果当作 "两种 arm 等效" 的实质发现，混淆了 "未检测到差异" 与 "不存在差异"。
- - **Critical**: LLM-as-judge 校准（21 gold, FNR=0/FPR=0）与实际评分完全脱节——实际 round "made zero judge calls (all SKIP)"，校准集的 FNR/FPR 为 0 不能外推到未经测试的评分场景；21 样本上 FNR=FPR=0 极可能是过拟合，没有留出 hold-out 验证集。
- - **Critical**: "curated L1a (6 tasks, k=4) gives p=0.0026 **only under** fail-as-worst encoding" 存在双重 post-hoc 选择偏差：(a) "curated" 暗示任务筛选，(b) 结果依赖特定 encoding 策略，且作者自标 "exploratory" 却将 p=0.0026 列为 abstract 主线结果，构成 p-hacking 嫌疑。
- - **Critical**: 多重检验（McNemar + Wilcoxon + Friedman + Nemenyi + curated L1a + P5 frontier + judge calibration 等）未报告家族性误差率校正（如 Bonferroni / BH-FDR），p=0.0026 在至少 6+ 次检验中的含义被严重膨胀。
- - **Critical**: "simulated second annotator Î±=0.894" 并非真实人间一致性，而是模拟值；将模拝 Î± 作为校准可靠性证据是循环论证，无法支撑 judge 信度效度。
### Major（6）
- - **Major**: 跨模型 Friedman (ÏÂ²=2.0, p=0.3679) 将 7b/14b/9b 三个不同架构、不同训练数据的模型当作 "处理" 对比，混淆变量（模型大小、架构、预训练语料、对齐方法）未受控，任何跨模型差异都无法归因于单一因素。
- - **Major**: A vs. F 为准实验性对比，但仅 3 个模型 Ã 4 场景 = 12 个 N=4 子单元，且报告的 McNemar 是汇总后的 N=4，那么汇总逻辑（是跨模型 pool 还是按模型分层）未说明；若 pool 则忽略了 model-level 聚类依赖，若分层则 N=4/模型更无统计意义。
- - **Major**: "intention-to-treat mean 0.355 including the failed trial as 0" 滥用临床试验术语；ITT 的核心是防止流失偏倚，这里只是将失败记 0 分后取均值，与 ITT 无因果含义，且将单个 failed trial 与成功 trial 等权平均的合理性未论证。
- - **Major**: "byte-for-byte reproducibility" (SHA-256 manifest) 的前提是 LLM 输出可确定性复现，但未在 abstract 中报告 temperature、seed、采样策略；若 temperature>0，SHA-256 匹配只是 "运气好的单次跑通"，非统计意义上的可复现性。
- - **Major**: L1a 中 gemma 报告 "1/6 â 2/6 after three independent trials"，将多次重试后的最伳结果作为报告值，构成 best-of-N 选择偏差；应报告所有 trial 的分布或预注册的 single-trial 协议。
- - **Major**: L1b "0/10 for all models" + "positive control 1/4 on Chemistry_000 demonstrates pipeline solvability" ââ 仅 1/4 的正控制不足以证明 pipeline 可解；全零结果可能是 pipeline bug 而非模型能力不足，正控的内部效度威胁未得到充分排除。
### Minor（3）
- - **Minor**: "165 entries with P5"、"46-entry SHA-256 manifest" 两个数字在同一句中出现，P5 与 manifest 的关系未阐明，读者无法判断 reproducibility claim 的边界。
- - **Minor**: P5 frontier muse-spark-1.2-contributor 的 p=0.0026 用于 6 个任务的非预注对比，虽标注 "exploratory"，但与 baseline 模型的样本量、计算预算不可比，存在第三方混淆。
- - **Minor**: L047 "answer-fitting audit" 的方法学细节（何为 "Material answer-fitting"、检测规则、假阳性率）在 abstract 中完全缺失，无法评估其效度。

## 统计（stat）— ok
### Critical（4）
- - Critical: L2 主检验用 exact McNemar，但 discordant pairs n_d=0（零不一致对），p=1.0000 是退化解——该检验无任何区分力，将其表述为"no statistically detectable difference"属误导性等价声明；正确解读是"检验无法提供信息"，而非"无差异"。
- - Critical: 95% CI [0,0] 因配对结果完全相同而退化为零宽度，这不是有效精度估计而是零方差的数学产物；报告它制造虚假的统计确定性。
- - Critical: p=0.0026 仅在"fail-as-worst encoding"下成立、其余编码不显著——在多种编码方案中选取唯一显著者为选择性报告（garden of forking paths），本质是 p-hacking；标注"exploratory"不消解多重分析的选择偏差。
- - Critical: LLM-as-judge 校准在 21 gold 上 FNR=0/FPR=0，但该轮实际零 judge 调用（all SKIP）——完美指标基于零观测，宣称校准"passed"无效；校准仅为 methodological warrant 而非实证验证。
### Major（6）
- - Major: 最小可检效应 d_min=2.1279（Cohen's d>2.0 属"巨大"量级）在 80% power 下表明 N=4 灾难性欠功效；同时自报 McNemar power=0.0000 at n_d=4，却仍以该检验作为 L2 主分析——任何非显著结论均无信息量。
- - Major: 多重检验未做族级校正：McNemar（L2）、两次 Friedman（16 任务 / 6 任务子集）、探索性 p=0.0026、judge FNR/FPR 双门控等多项独立检验并行报告，无 Bonferroni / Holm / FDR 任一校正。
- - Major: Friedman"16 paired tasks"含 10 个 L1b 任务全模型得 0/10（跨模型零方差、完全并列排名），对 χ² 贡献为零；有效区分任务仅 6 个，表观 n=16 虚高，应报告有效任务数。
- - Major: 所有点估计（completion 0.1418 / 0.1918 / 0.2750；L1a 0.6252 / 1.5422 / 0.355 等）均未报告 SD / SE / CI 或重复试验方差，裸均值不可解读、不可复算不确定性。
- - Major: "simulated second annotator α=0.894"为模拟而非实测标注者间一致性——模拟 α 不构成评分可靠性的经验证据，且 P5 的 39 gold 中含 9 synthetic + 1 attack，真实标注占比未单独报告。
- - Major: "intention-to-treat mean 0.355 including the failed trial as 0"将单次失败试次硬编码为 0 后取均值，但仅 3 次试次无方差报告；ITT 处理在 n=3 时无统计意义，且零填充引入系统性负偏。
### Minor（2）
- - Minor: Nemenyi CD=0.8284 与非显著 Friedman（p=0.3679）并列报告——omnibus 检验未显著时事后两两比较不应作为结论性证据呈现。
- - Minor: gemma L1a"three independent trials"以 0.2000×3 / 0.5330×2 报告为乘法记法，实际试次数与任务数混淆，未做重复测量方差分析或试次间变异报告。

## 实验（experiment）— ok
### Critical（4）
- - **Critical**: L2 结论"无统计学差异"在 N=4、n_d=0（零不一致对）、McNemar 功效=0.0000 的条件下完全无法支持"无差异"结论；零功效下的零结果只是"未检测到"，论文却将其表述为两个 arm 等效，属于经典的"absence of evidence â  evidence of absence"错误。
- - **Critical**: 全文未报告任何 seed 管理策略；"bootstrap at step/seed level as future work"直言 seed 未在主实验中控制；568 calls 中的 36 次 extra trials 无 seed 可追溯，复现性声明（SHA-256 manifest）只能验证文件字节一致，无法验证采样随机性可复现。
- - **Critical**: L1b 的 LLM-as-judge 在实际评分中"made zero judge calls (all SKIP)"，校准（21 gold、Wilson 0.28）从未在真实评分中被调用，整个 L1b 评分管线缺少有效验证；在 judge 缺席的情况下 0/10 的结果无法归因于模型能力还是评分管线故障。
- - **Critical**: L1b 全部三个模型得分 0/10，零方差，无法区分"模型无能力"与"基准不可解"；positive control 仅 1/4（Chemistry_000），样本量极小且未覆盖其余 9 个任务，无法证明 pipeline 对多数任务可解。
### Major（6）
- - **Major**: 主实验仅测试 3 个小规樼开源模型（7B/9B/14B），模型族多样性极低（仅 Qwen+Gemma），泛化声明缺乏支撑；P5 muse-spark 为"exploratory"独立阶段，条件与主实验不一致，不应作为泛化证据。
- - **Major**: 超参数未报告——temperature、top-p、max_tokens、shot数、prompt 模板均缺失；仅报告 ollama 版本号，无法判断基准公平性（如不同模型是否使用相同推理配置）。
- - **Major**: 处理不对等——gemma 在 L1a 获得 3 次独立 trial（1/6â2/6），7b 和 14b 显然只跑 1 次；不同模型试验次数不同破坏了跨模型比较的公平性，Friedman 检验的有效性存疑。
- - **Major**: 消融不完整——除 L2 的 A vs F 外无任何组件消融（L047 audit、judge 管线、completion-guided harness 的各子组件均未消融），且 A vs F 因零功效实际无法提供任何消融信息。
- - **Major**: L1a 显著性（p=0.0026）仅在"fail-as-worst encoding"一种编码方式下出现，暗示多重比较/编码选择偏差；未报告尝试了多少种编码方案、是否做多重检验校正。
- - **Major**: 缺少负控制/随机 baseline（如随机选择、输入直输出等），无法确立 chance-level 表现，0 分结果缺乘法参照。
### Minor（3）
- - **Minor**: L1a 仅 6 个任务、L1b 仅 10 个任务、L2 仅 4 个 scenario，总任务数极少；Friedman 在 16 paired tasks / 3 models 下同样可能严重欠功。
- - **Minor**: "46-entry SHA-256 manifest"与"165 entries with P5"的数字不一致，P5 阶段的报告粒度与主实验混杂，影响可复现性判断。
- - **Minor**: "36 extra trials"的触发条件、选择机制未披鲲；存在结果驱动补跑（result-driven rerun）的 p-hacking 风险。

## 新颖性（novelty）— ok
### Critical（2）
- - **Critical**: âUnification”实质上是把三个已有 benchmark（AIRS-Bench、ResearchClawBench、GAIA2）包裹在同一个 `run.json` 契约下，核心数据/任务/环境均非自创，增量贡献接近 "glue harness"，与 AgentBench、ML-Bench、ScienceWorld 等已有统一 agent 评测线的差异未在摘要/引言中给出任何对比。
- - **Critical**: 引言声称科学 agent "advancing rapidly" 却引用 `\citep{goodfellow2016deep}`（深度学习教科书），与科学 agent 无关；"fragmentation" GAP 无任何对应工作引用，GAP 的真实性未被证明，疑为堆积话术。
### Major（4）
- - **Major**: 统计协议（exact McNemar、Wilcoxon+CLES、Friedman+Nemenyi）均为标准 off-the-shelf 检验，被包装为贡献点；"denominator discipline"（失败记零留分母）是评测常识，不构成方法论新性。
- - **Major**: LLM-as-judge 校准 "made zero judge calls (all SKIP)"，自认为 "methodological warrant"，即未在真实评测中使用，该贡献点为空转工程，被措辞为已验证的能力属夸大。
- - **Major**: 实验结果主体为零/无效差异（L2 两臂 p=1.0、L1b 0/10 全失败、L1a 7b 0/6），对 "科学能力" 的实证 insight 极度有限，使用 P5 muse-spark-1.2-contributor（源不明、标注 "exploratory"）填补 6/6 结果有为零结果 "找补" 之嫌，增量见解被高估。
- - **Major**: 引言提出要 "distinguish genuine scientific reasoning from execution failure or contract violation"，但 suite 仅跑分，未提供任何归因解耦机制，标题的科学推理辨析 GAP 并未被 suite 真正填补。
### Minor（1）
- - **Minor**: "reproducible contract / SHA-256 manifest" 为工程实践，在已有 reproducibility 框架（例如 MLRepis、PapersWithCode 流程）下属常规实现，不应列为主要贡献。

## 可复现（repro）— ok
### Critical（5）
- - Critical: 全文未给出任何随机 seed（模型采样温度/top-p、trial 顺序、bootstrap），摘要自承"bootstrap at step/seed level as future work"，即 seed 级可复现性尚未实现却宣称"byte-for-byte reproducible"。
- - Critical: SHA-256 manifest 数量自相矛盾——正文称"46-entry manifest"，括号又写"(165 entries with P5)"，未说明哪个为权威快照、P5 指什么，哈希对账无法落地。
- - Critical: 三个基准 AIRS-Bench / ResearchClawBench / GAIA2 均未披露数据许可证与再分发条款，复现者无法合法获取与校验数据集。
- - Critical: 摘要宣称"fully recomputable harness"，但未提供任何一键复现工件（容器镜像、repo 链接、setup 脚本、依赖锁文件），"run.json contract"与"single canonical script"均只被提及而未展示或链接。
- - Critical: LLM-as-judge 该轮"zero judge calls (all SKIP)"，校准仅为"methodological warrant"，无任何可执行证据链支撑其 FNR/FPR=0 的主张；复现者无法复跑校准。
### Major（7）
- - Major: 无完整配置快照——模型 qwen2.5:7b/14b、gemma2:9b 的 system prompt、context window、temperature、decoding 参数均缺失，"run.json"内容不可见。
- - Major: "simulated second annotator α=0.894"为模拟值而非真实双标注，模拟代码与 seed 未公开，该 κ 不可复现。
- - Major: P5 gold 含"9 synthetic + 1 attack"合成/攻击样本，但其生成方法、所用模型、seed、校验哈希均未交代，合成 gold 破坏哈希对账闭环。
- - Major: 关键协议标识 P5、ARS v3.11、L047 在可见文本中无定义，复现者无法对齐审计与校准流程版本。
- - Major: ollama 版本写作"0.32.13"，该版本号格式异常（ollama 官方无此版本），无法精确 pin，模型推理后端不可复现。
- - Major: gemma "three independent trials"未说明每次 trial 的 seed 与重跑触发条件，0.2000×3 / 0.5330×2 的稳定性无法独立验证。
- - Major: 对应作者匿名（corresponding@example.com 占位），复现受阻时无有效联络通道。
### Minor（3）
- - Minor: 仅给出 RTX3090 硬件，未 pin CUDA / 驱动 / OS / ollama 上下游依赖版本。
- - Minor: 预算"<1000 calls"未拆解单任务成本与时长，复现者无法预估资源。
- - Minor: "canonical script"被引用但未命名/版本化（无 commit hash 或版本号）。

## 写作（writing）— ok
### Critical（2）
- - Critical: 摘要稱 L1b judge "passed at FNR=0.0000, FPR=0.0000"，同一句卻說 "the round made zero judge calls (all SKIP)"——零調用下宣稱零誤差率是邏輯矛盾；無觀測即無 FNR/FPR å¯è¨ï¼æå ±å "undefined" 而非 0。
- - Critical: gemma 的 intention-to-treat mean 0.355 無法由給定分量算出：無論 (0.2Ã3+0.533Ã2+0)/6=0.278、(0.2+0.533)/2=0.367、還是 (0.2Ã3+0.533Ã2)/5=0.333，均不等於 0.355；數字一致性破裂。
### Major（7）
- - Major: 14b 的 Zinc 分數 1.5422 > 1，而摘要中所有其他 L1a 分數（0.2000、0.5330、0.5607â¦0.0105）均在 [0,1]，metric 尺度不一致且未說明。
- - Major: Friedman "16 paired tasks" 含 10 個 L1b 任務，而摘要明言 L1b "0/10 for all models"ââ10 個零方差任務對 Friedman 排底無判別力，只是虛增 n，ㄧ 結果存在誤導性。
- - Major: "39 gold, 30 real+9 synthetic+1 attack"ââ30+9+1=40 â  39；gold 定義與分項數量矛盾，或將 attack 與 gold 混為一談。
- - Major: 實驗手臂標籤為 "A" 與 "F"，未說明為何跳過 BâE；讀者無法判斷是否存在未報告的中間手臂，命名不一致。
- - Major: P5 frontier 宣稱 "6/6" pass，卻含 0.0105 這樣的近零分數；6/6 與 0.0105 在未給定 pass threshold 的情況下自相矛盾。
- - Major: 摘要為單一 400+ 字段落，夾爆 P5、ARS v3.11、L047、CD、CLES 等未定義縮寫，結構上不可讀；違反 abstract 應自成接近 200 字的寫作規範。
- - Major: "simulated second annotator Î±=0.894"——模擬值不是真實 IAA，用 Î± 表述暗示經驗證實的互標者一致性，屬術語濫用。
### Minor（5）
- - Minor: 摘要寫 "AIRS-Bench"，正文 Introduction 寫 "AIRS-Bench rad"，"rad" 後綴無解釋。
- - Minor: Introduction protocol 列出 "Wilcoxon+CLES"，摘覌結果卻完全缺席 Wilcoxon/CLES 數值，方法清單與結果回報不對稱。
- - Minor: 引用 Goodfellow 2016《Deep Learning》支撐 "scientific agents â¦ advancing rapidly"，文獻與論點顯著不匹配。
- - Minor: 關鍵字列出 "SciEvalSuite"（本文自身標題），非搜索术語，非推薦做法。
- - Minor: 95% CI [0,0] 標註 "degenerate"，統計報告髒話非標準；應以 n_d=0 不可估計明載，而非稱 "degenerate CI"。

## 伦理（ethics）— ok
### Critical（1）
- - Critical: "P5 frontier muse-spark-1.2-contributor" 命名后缀 "-contributor" 强烈暗示作者本人是该模型贡献者，却在双盲投稿中对其给出 6/6 的有利结果（其余模型 0/6~2/6），既涉嫌违反 TMLR 双盲匿名（身份自指暴露），又构成未披露的利益冲突，全文无 COI 声明。
### Major（5）
- - Major: 未声明所用数据集与模型的许可条款——AIRS-Bench、ResearchClawBench、GAIA2 以及 qwen2.5(Qwen License)、gemma2(Gemma Terms)、llama3.1(Llama Community License)、muse-spark 各有不同许可限制，商用/再分发/研究用途合规性无法判断。
- - Major: ResearchClawBench、L047 等命名疑似作者自建资产，在双盲稿中作为自有 benchmark 命名披露，存在去匿名化线索；L047 这种不透明内部编号亦可能泄露机构身份。
- - Major: GAIA2 类任务常含真实网页/邮件/文件数据，且 judge 校准集含 "30 real+9 synthetic+1 attack"，未说明真实样本的 PII 脱敏、采集同意与合成/攻击样本的来源与许可，存在隐私与数据合规风险。
- - Major: "simulated second annotator α=0.894" 系模拟而非真实人工标注，却与 Wilson/inter-annotator agreement 并列陈述，易误导读者认为存在双标注员；属标注伦理与可复现性失实。
- - Major: L1a/L1b/L2 均涉及代码生成与执行、交互式环境操控（p3dev、ReAct harness），却未讨论沙箱隔离、有害代码/工具滥用的缓解措施与 misuse 风险声明，违反 benchmark 安全披露惯例。
### Minor（2）
- - Minor: judge 校准仅 "single annotator"，未说明人工标注的知情同意、报酬与 IRB/伦理审查状态。
- - Minor: 摘要未给出模型权重来源（ollama 拉取渠道、版本指纹）与第三方 API 调用（如有）的合规与条款遵循情况。

## 汇总

- **Critical: 23 | Major: 41 | Minor: 19**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）