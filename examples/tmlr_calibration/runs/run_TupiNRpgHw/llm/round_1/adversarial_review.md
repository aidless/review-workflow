# 对抗审查报告

- 时间: 2026-08-26T07:08:37.112879+00:00
- 源: F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_TupiNRpgHw\extracted_text.txt
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（2）
- - Critical: 核心校正机制依赖逆策略模型 $f_{inv}(s, s')$，但该模型仅在有限目标域数据上训练——而"目标域数据有限"正是本文引入源域数据的动机，构成循环依赖：数据不足→逆模型不准→校正不可靠→仍需源域数据，整个 pipeline 的有效性无法脱离"目标域数据已足够训练准确逆模型"这一与动机矛盾的隐含前提。
- - Critical: 校正仅修改动作 $\hat{a}_{src}=f_{inv}(s_{src}, s'_{src})$ 和奖励，但未处理 $s'_{src}$ 本身在目标域动力学下是否可达的问题。若源域与目标域动力学差异较大，$s'_{src}$ 可能根本不是目标域中的合法转移终点，此时无论动作如何校正，元组 $(s_{src}, \hat{a}, \hat{r}, s'_{src})$ 仍为目标域分布外样本，方法的前提"校正后即对齐目标动力学"不成立。
### Major（5）
- - Major: 选择步骤用前向动力学模型 $f_{fwd}$ 作为过滤器，但该模型同样在有限目标域数据上训练，与前述逆模型共享同一数据来源与误差来源。校正质量与选择质量被同一混淆变量（目标域数据量/覆盖度）共同驱动，无法在实验中分离"校正有效"与"选择有效"各自贡献，内部效度受损。
- - Major: 逆策略映射 $f_{inv}(s, s')$ 在随机动力学下为一对多关系（多个动作可导致同一转移），论文隐含假设确定性逆映射可恢复"正确"动作，该假设未经论证；若动力学具随机性，逆模型输出可能为均值化的不合理动作。
- - Major: 前向模型一致性选择准则会系统性偏好某些转移类型（如确定性高、模型置信度高的区域），引入选择偏差，改变合并后数据集的有效行为策略分布，可能违反离线 RL 对数据覆盖性的核心假设，构成内部效度威胁。
- - Major: 论文前提限定为"仅动力学失配"，未讨论奖励函数、状态空间表征或动作空间跨域差异的可能；若奖励结构亦随域变化，仅用目标域奖励模型重标定源域转移的合理性未经论证，外部效度受限。
- - Major: 因果推断不充分——"直接合并导致次优性能"作为核心动机被陈述为前提而非经验验证；且若缺少将"仅校正""仅选择""校正+选择"分别消融的设计，无法将性能提升因果归因于所提机制而非单纯数据增量效应。
### Minor（1）
- - Minor: "源域与目标域相似"这一关键假设未给出量化阈值或可操作界定，方法在多大动力学偏移下仍有效未知，泛化性声明的边界条件缺失。

## 统计（stat）— ok
### Critical（2）
- - Critical: 摘要中称"STC achieves superior performance against existing baselines"，这是一个统计性声明，但未提供任何显著性检验（如 t检验、Wilcoxon秩和检验）或置信区间支撑，仅凭均值排序即宣称"superior"，存在 p 值/显著性误用风险。
- - Critical: "various environments with dynamics shifts"对环境样本量描述模糊，既未明确测试环境数量，也未说明每个环境下的随机种子数，样本量不足时无法区分真实效应与随机噪声，尤其在 RL 中方差大、种子敏感场景下尤为严重。
### Major（3）
- - Major: 对多个 baseline å¨å¤ä¸ªç¯å¢ä¸è¿è¡æ¯è¾ï¼éå«å¤éæ¯è¾¸¼é®é¢ï¼è®ºææªæåä»»ä½å¤éæ¯è¾æ ¡æ­£æ¹æ³ï¼å¦ Bonferroni、Holm 或 FDR），存在 family-wise error rate 失控风险。
- - Major: 未报告效应量（effect size，如 Cohen's d 或相对提升百分比的置信区间），无法判断性能提升是否具有实际意义（practical significance），仅有统计显著不等于效应值得关注。
- - Major: 方差报告缺失——在摘要和引言中未提及结果是否以 meanÂ±std 或 meanÂ±95% CI 形式呈现；RL 实验中不同种子间方差可能很大，缺少方差信息使读者无法评估结果稳定性。
### Minor（1）
- - Minor: 引言中多处使用"may lead to""can significantly degrade"等描述性语句，暗示效应存在但未引用任何定量依据，缺乏统计背书。

## 实验（experiment）— ok
### Critical（2）
- - Critical: 正文实验部分被截断，无法确认基线是否享有与 STC 同等的目标域监督（STC 额外训练前向动力学模型 + 逆向策略模型 + 奖励模型三个目标域拟合器），若基线未补齐等量模型容量/数据访问，则"superior performance"结论无法成立——这构成基准公平性的致命缺口。
- - Critical: 消融完整性存疑：STC 同时包含"动作修正 + 奖励修正 + 前向模型选择"三组件，但摘要/介绍中未见对"仅修正""仅选择""仅动作修正""仅奖励修正"的解耦消融，无法判定各模块的真实贡献，存在"打包贩卖"嫌疑。
### Major（4）
- - Major: 缺乏对照组说明：未明确是否存在"随机修正/随机选择"或"全部保留源数据不筛选"的对照，无法证明选择机制优于随机保留，消融缺一关键下界基线。
- - Major: 超参数透明度不足：选择阈值（forward model 保留样本的匹配度阈值）、各模型训练 epoch/数据配比、Dsrc 与 Dtar 的采样比例 B 均未在可见文本中给出范围或调参协议，疑似在验证集上挑参后报告测试结果。
- - Major: seed 管理缺失：可见部分未声明随机种子数量、均值±方差报告方式或显著性检验，仅称"achieves superior performance"而无统计可信区间，单 seed 结果风险高。
- - Major: 泛化声称过强：摘要称"various environments with dynamics shifts"，但未交代环境数量、dynamics shift 的类型/幅度谱系（是否仅同一族 Mujoco 系统、是否仅低维状态空间），跨形态/高维/稀疏奖励场景未覆盖，泛化性主张缺乏支撑。
### Minor（2）
- - Minor: 基准选取疑似不完整：未提及与同样做"数据改写"类（而非过滤/奖励调整类）方法的对比，只在"filtering / reward modification"两大类中挑对手，可能回避了最接近的同质基线。
- - Minor: 模型误差未隔离：前向模型与逆向模型自身在有限目标数据下的拟合误差未作为独立变量报告，selection 机制对"模型偏差放大"的鲁棒性无对照实验。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 摘要声称"Instead, we propose to modify the source domain data into the target domain data"以区别于"reward modification"类方法，但 STC 本身就用 reward model 去"correct the rewards of source transitions"——即 STC 自己就在做奖励修改。所谓"区别于 reward modification"çå®ä½ä¸æ¹æ³å®ç°èªç¸çç¾ï¼çæ­£çæ°å¢ç»ä»¶
- - Critical: 类似地，文中将本法与"transition filtering"对立，但 STC 的"Selection"步骤用 forward dynamics model"retain corrected samples that better match the target dynamics"——这正是 filtering。因此 STC = filtering + reward modification + action correction，实际是对已有三类范式的组合，而非摘要暗示的"fundamentally different"新范式。
### Major（3）
- - Major: GAP 的真实性未被证明。"may lead to insufficient exploitation of the valuable source domain data"是软性断言（"may"），文中未给出现有 filtering/reward-modification 方法到底丢弃了多少源数据、STC 又多保留了多少的定量分析，GAP 属于"asserted but not established"。
- - Major: inverse dynamics model 用于 action relabeling、forward dynamics model 用于样本筛选，二者在表征学习与 model-based transfer RL 中均已成熟（如 ICM、model-based 数据筛选）；本文将二者组合的增量性未与这些已有文献明确区分。
- - Major: 相对 Liu et al. (2022)（domain classifier 做 reward modification），STC 的 reward model 分支本质上是同一思路的替换；文中未充分论证 STC 相对该工作的独立增量何在，只是组合了 action correction。
### Minor（1）
- - Minor: "bidirectional dynamics transition information"的框架被当作新颖概念，但 forward+inverse dynamics 的双向建模在 prior work 中已广泛出现，术语新颖性高于实质新颖性。

## 可复现（repro）— ok
### Critical（2）
- - Critical: 全文（含摘要/引言/图1）未见代码仓库链接、commit hash 或匿名代码包，无法定位可复现工件来源，证据链起点缺失。
- - Critical: 摘要声称"experiments on various environments with dynamics shifts"，但未在可见处给出环境名称、版本号（如 MuJoCo/gym 版本）、dynamics shift 的具体构造方式，下游无法重建相同实验设置。
### Major（4）
- - Major: 图1涉及 forward dynamics model、inverse policy model、reward model 三个模型，但可见部分未给出任何训练超参（学习率、网络结构、批大小、训练步数），缺乏配置快照。
- - Major: 未声明 source/target 离线数据集 Dsrc/Dtar 的来源、规模、采集策略及数据许可（license），无法判断数据是否可合法复现。
- - Major: 未提及随机种子设置或多次重复实验次数，无法评估结果方差与显著性，seed 可复现性缺失。
- - Major: 缺少数据/模型权重的哈希对账（如 SHA256/checksum），即使发布也无法验证下载工件与作者原始版本一致。
### Minor（2）
- - Minor: 摘要称"selectively correct source transitions"，但未见 selection 阈值的可复现取值与搜索范围说明。
- - Minor: 未见一键复现脚本（如 `run_all.sh` / Makefile / Dockerfile）或环境依赖锁文件（requirements.txt/conda env）的引用。

## 写作（writing）— ok
### Critical（2）
- - Critical: 摘要与 Figure 1 caption 在"哪些模型执行校正"上矛盾—摘要称"leverage an inverse policy model **and a reward model** to correct the actions and rewards"，但 caption 写"we correct the actions and rewards â¦ **by using the inverse policy model**"（未提及 reward model 参与校正），两处对 reward model 职责的描述直接冲突。
- - Critical: Figure 1 中箭头标注 `(s^tar, a^tar, r^tar, s'^tar) â¹ (s^src, Ã£_src, rÌ_src, s'^src)` 左侧为目标域元组、右侧为源域校正元组，方向与"对源域数据做校正"的语义相悖，让读者误以为是从目标域向源域转换。
### Major（4）
- - Major: 摘要称 forward dynamics model 用于"retain corrected samples that better match the target dynamics"（对已校正样本做筛选/保留），caption 却写"selectively correct source transitions"（选择性地去校正），"保留已校正样本"与"选择性校正"是两个不同动作，描述不一致。
- - Major: caption 称三个模型"are trained to capture the bidirectional dynamics transition information"，但 reward model r(s,a) 建模的是奖励而非动力学转移信息，将之归入"dynamics transition information"属术语误用。
- - Major: Figure 1 中数据集符号不一致—图体内为粗正体 `ð·ð¡ðð`/`ð·ð ðð`，caption 中变为斜体 `Dtar`/`Dsrc`，同一对象两种排版方式。
- - Major: Figure 1 中 reward model 标注为 `r(s,a)`，与 forward/inverse 模型的命名规范 `f_fwd`/`f_inv` 不统一，且图中 `r(s,a)` 置于 "Offline RL" 旁而非 "Correction" 旁，与摘要所述"reward model to correct â¦ rewards"的角色定位在图上看不出对应关系。
### Minor（4）
- - Minor: 标题内含换行断字痕迹 "Selective Tran-sition Correction"，应为单一单词 "Transition"。
- - Minor: "There are many researches focusing on" 中 "researches" 用法错误，research 为不可数名词，应改为 "many studies" 或 "much research"。
- - Minor: 摘要 "modify the source domain data into the target domain data" 表达笨拙，"modify â¦ into" 搭配不自然，建议 "transform source domain transitions to align with target dynamics"。
- - Minor: Figure 1 caption 过于冗长，将 Phase I、Phase II 两段描述全部塞入单一 caption，可拆分为子句或缩减。

## 伦理（ethics）— ok
### Critical（1）
- - Critical: 论文有4名作者来自腾讯（Jiafei Lyu、Jingwen Yang、Zichuan Lin、Deheng Ye），属典型产学研合作且RL技术具有直接商业价值，但全文未见利益冲突声明、资金来源披露与腾讯角色说明，违反学术出版伦理规范（如TMLR/COPE要求）。
### Major（3）
- - Major: 实验使用"various environments with dynamics shifts"，但未披露所用离线数据集与基准环境（如D4RL、MuJoCo等）的来源、版本及许可协议，数据可追溯性与合规性无法核实。
- - Major: 方法可对源域转移数据的动作与奖励进行"correction"，本质是跨域合成/改写训练数据，存在被滥用于伪造数据、掩盖数据真实来源、或在不安全真实系统中部署未经验证策略的风险，但全文缺乏误用风险与伦理讨论。
- - Major: 论文反复强调"real-world scenarios""costly or unsafe"应用，若源域/目标域离线数据来自真实系统（如腾讯产品用户行为数据），却完全未涉及隐私保护、匿名化、用户知情同意等合规说明。
### Minor（3）
- - Minor: 缺少独立的伦理与安全声明（ethics statement），尽管明确面向安全敏感的真实场景部署。
- - Minor: 多名作者使用个人邮箱（QQ、Gmail）而非机构邮箱，不利于身份核实与机构归属确认，在双盲评审与利益冲突追溯上存在隐患。
- - Minor: TMLR采用双盲评审，但清华-腾讯显著联合署名叠加高密度同组自引（Lyu et al. 2024a/2024b/2025/2026连续出现），可能在评审中暴露作者身份，削弱双盲有效性。

## 汇总

- **Critical: 13 | Major: 26 | Minor: 14**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）