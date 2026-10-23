# 对抗审查报告

- 时间: 2026-08-26T06:11:24.620743+00:00
- 源: F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_3i2ZRk8GDN\extracted_text.txt
- 角色: method, stat, experiment, novelty, repro, writing, ethics

## 方法论（method）— ok
### Critical（1）
- - Critical: 组合打分器声称"一致地优于所有单打分器与基线"，但其训练/调参与评测若共用同一批 11 数据集×10 架构的样本，存在数据泄漏与样本内过拟合风险，内部效度被破坏；必须说明是否采用留出/交叉验证、组合器权重是否在评测集外学习。
### Major（3）
- - Major: 以源任务准确率作为基线存在严重混淆：当所有候选模型同源（如均 ImageNet 预训练）时，源准确率差异反映的是架构容量而非可迁移性，基线的"胜出"可能是容量伪迹而非方法论洞见；且在同源场景下该基线近乎常数、无判别力，使"优于多数打分器"的前提自相矛盾。
- - Major: 论文用排序相关（如 Kendall/Spearman）作为评测指标，属关联性而非因果性证据，却以"证明一致优于"做因果式断言；未对选择方法的因果效应做识别，因果推断不当。
- - Major: 真值迁移性能由单一微调协议（学习率/epoch/冻结策略等）定义，构成混淆变量；不同协议可改变排序，"单一协议即真实排名"的假设未经检验，结论的稳健性存疑。
### Minor（2）
- - Minor: 13 打分器/10 架构/11 数据集的选择可能存在选择偏倚，代表性不足，外推至更广模型库与任务类型的普适性声明缺乏支撑。
- - Minor: "一致优于"未说明是否做了统计显著性检验与多重比较校正，n=110 的配对结果难以支撑"consistently"的强断言。

## 统计（stat）— ok
### Critical（2）
- - Critical: 样本非独立。10×11=110 个 (模型, 数据集) 配对中，同一模型跨 11 个数据集、同一数据集跨 10 个模型反复出现，构成聚类/重复测量结构；任何相关性检验或显著性检验默认 i.i.d.，此处被严重违反，应使用混合效应模型或聚类 bootstrap。
- - Critical: 组合 scorer 的评估存在数据泄漏/过拟合风险。若组合 scorer 在参与评估的同一批 11 个数据集上拟合并在其上"一致超越"各单一 scorer，属于样本内自我验证；正文未见留出集或交叉验证协议，"consistently outperforms" 的结论在统计上无效。
### Major（4）
- - Major: 多重比较未校正。组合 scorer 同时与 13 个 scorer + 1 基线 = 14 个对手逐对比较，"超越全部"的声明在 14 次同时比较下 I 类错误被放大，未见 Bonferroni/FDR 等校正，易得到虚高显著性。
- - Major: 方差/不确定性缺失。摘要与设计未提及随机种子、置信区间或标准差；深度学习微调结果高方差，单次运行的点估计不足以支撑"surprisingly outperforms / consistently outperforms"等比较性结论。
- - Major: 样本量不足以支撑泛化声明。仅 11 个目标数据集、10 个架构，对"数百个预训练模型"的迁移性排序做"一致最优"的外推，样本过小且覆盖域窄，统计功效不足。
- - Major: p 值/显著性误用。"consistently outperforms"与"surprisingly outperforms most"均为基于点估计的确定性表述，缺乏配对假设检验框架；既无统计检验又声称一致性，属于以描述性结果冒充统计显著性。
### Minor（2）
- - Minor: 效应量未报告。即便排序胜出，未给出相关系数差异的绝对幅度（如 ΔKendall-τ / ΔSpearman）；小幅度差异可能在实践上无意义，仅有排名而无效应量无法判断实际价值。
- - Minor: 检验/相关性度量的选择未论证。迁移性评估常用 Kendall-τ、Spearman、Pearson，三者对异常值与单调性敏感度不同，结论可能随度量切换而反转；未见对所选度量及适用条件的说明。

## 实验（experiment）— ok
### Critical（2）
- - Critical: 组合打分器（combined scorer）"利用多个单打分器信息"且"始终优于所有单打分器与基线"，但引言未说明其训练/评估协议。若在 10 架构×11 数据集=110 个 (model, dataset) 对上同时训练与评估组合器，存在严重数据泄漏；必须做留一数据集/留一架构的交叉验证，否则"始终最优"是过拟合产物。
- - Critical: 仅 110 个样本、13 个打分器作为特征训练组合器，样本维度比约 8.5:1，极易过拟合；未提及正则化/特征选择/嵌套交叉验证，组合器的泛化性存疑。
### Major（5）
- - Major: 基线公平性问题——源任务准确率基线完全不需访问目标数据，而所有 transferability scorer 都需访问目标数据。二者信息量不对等，直接在同一排名指标上比较并不公平；且"基线意外优于多数打分器"恰恰暗示评估未在源准确率相近的难区分场景（scorer 真正有价值处）做压力测试。
- - Major: 缺少"朴素集成"对照组——没有随机排名、打分器均值/中位数等 trivial 组合基线，无法证明所学组合器优于简单平均，从而无法支撑"learned combination"的必要性。
- - Major: ground-truth 迁移性能需对每个 (model, dataset) 对做微调，微调本身随机；可见部分未提及 seed 管理与多 seed 方差。若单 seed，排名相关系数（如 Kendall-τ）会被噪声污染，组合器的"显著优势"可能落在噪声范围内。
- - Major: 泛化范围受限——10 架构、11 数据集全部为视觉/ImageNet 系，且数据集数仅 11。组合器在该分布上训练，能否外推到非 ImageNet 源域、不同模态、或新架构未做验证；"consistently outperforms" 的断言缺乏域外证据。
- - Major: 消融完整性不足——组合器未报告各单打分器的留一/贡献度消融，无法判断是少数打分器驱动还是冗余堆叠；也未说明组合方式（线性加权？非线性模型？），影响可解释性与可复现性。
### Minor（2）
- - Minor: 超参数管理——组合器作为学习型方法，其自身超参数（权重正则、模型选择）调优协议未说明；若在测试集上调参同样构成泄漏。
- - Minor: 13 个打分器间存在强相关性（多数共享源/目标特征），组合器可能退化为少数独立信号，但未做相关性分析或去冗，消融不完整。

## 新颖性（novelty）— ok
### Critical（2）
- - Critical: 论文宣称"领域缺少标准化评估协议"作为核心 GAP，但 Pándy et al. (2022)（论文自己引用）已经系统比较了多个 transferability estimators（LEEP、NCE、LogME 等），并提出了对比实验设计。论文虽提及该工作却仍将"无统一协议"作为本文动机，GAP 的表述存在自我矛盾，真实性与新颖性均被夸大。
- - Critical: "combined scorer" 被作为核心方法贡献提出（"novel combined scorer that leverages information from multiple individual scorers"），但将已有 scorer 做集成/stacking 是非常成熟的技术路径。论文未在可见部分论证该组合方法在机制层面的创新性（如是否有新的信息融合策略而非简单线性加权/学习排序），"novel" 一词存在过度声称风险。
### Major（3）
- - Major: "source accuracy baseline 出乎意料地优于大多数现有 scorer"被当作关键发现，但 Kornblith et al. (2019) 及更早迁移学习文献已反复报告源任务精度与目标性能强相关，该"surprising"结论在现有文献基础上并非全新，增量贡献被叙事性地放大。
- - Major: 论文将 13 scorers × 10 architectures × 11 datasets 的经验规模作为贡献亮点，但该规模在近期 transferability 评测文献（如 Pándy et al. 2022；You et al. 2021 的评估范围）中并不罕见，benchmark 的边际实证价值需要更明确的与现有评测在覆盖面、协议严谨性上的量化差异说明，否则贡献声明偏空泛。
- - Major: Abstract 与 Introduction 多次声称"best scorer in one study ranking among the worst in another"以论证协议缺失导致矛盾结论，但未在可见文本中量化哪些研究结论矛盾、矛盾是否源于协议差异还是 scorer 本身对数据敏感。该动机性论断缺少可验证支撑，GAP 的"真实性"建立在未经举证的轶事上。
### Minor（1）
- - Minor: 论文未明确讨论与 general model selection / AutoML 中 stacking-based meta-scorers 的关系，combined scorer 与该类现有方法的边界不清，容易被审稿人质疑增量贡献的定位。

## 可复现（repro）— ok
### Critical（4）
- - Critical: 通篇可见部分未提及任何随机种子（random seed）设定；微调、特征提取、scorer 计算均含随机性，缺种子则 13 scorers Ã 10 架构 Ã 11 数据集的排名结果无法复现。
- - Critical: 未提供配置快矧（configuration snapshot）；“standardized evaluation protocolâ 在引言中反复强调，却未公开协议细节（学习率、batch size、epoch、优化器、数据划分比例、增强策略），证据链从“标准协议”到“结论”断裂。
- - Critical: 无哈希对账；10 种架构、11 个数据集、预训练权重均未给出 SHA256/MD5 校验和，Torchvision/Hugging Face 上同名模型会因版本漂移导致复现失败，“相同模型池”无法对齐。
- - Critical: 未提供一键复现路径；可见部分仅给出 Torchvision/HuggingFace 主页链接，未给出代码仓库、容器镜像、environment.yml/requirements.txt 或运行脚本，违反 TMLR 复现性承诺。
### Major（3）
- - Major: 数据许可缺失；11 个目标数据集（提及 PASCAL VOC、SUN397、ImageNet）未标注许可证类型与重分发权限，复现者无法合规获取/重现数据，影响二次复现。
- - Major: 证据链缺口 ââ 摘要声称 âbaseline outperforms most existing scorersâ 与 âcombined scorer consistently outperforms all”，但未给出“outperformâçåº¦éå®ä¹ï¼å·®å¼éå¼ï¼æ¾èæ§æ£éªï¼æåç¸å
- - Major: 引用的上游资源未 pin 到具体 commit/版本；Torchvision、Hugging Face 仅列主页 URL，复现时模型池随在线更新变动，无确定性。
### Minor（2）
- - Minor: OpenReview 链接中含空格（`https: // openreview. net/ forum? id= 3i2ZRk8GDN`），无法直接点击，影响复现者快速溯源审查记录。
- - Minor: 作者邮箱中混用 Gmail（valle.do.eduardo@gmail.com）与机构邮箱，未统一，影响证据链中作者归属与联系复现者的便捷性。

## 写作（writing）— ok
### Critical（1）
- - Critical: 全文存在大量编码/连字符损坏（ligature 损坏）："e!cient"（efficient）、"o"ers"（offers）、"e"orts"（efforts）、"a"ect"（affect）、"di!culty"（difficulty）、"di"erent"（different）——处于已发表状态的论文，此类损坏直接破坏可读性，属严重排版问题。
### Major（3）
- - Major: 摘要数字不一致/歧义：摘要声明"evaluating 13 scorers"，随后又"propose a novel combined scorer"并称其"consistently outperforms all of them"——合并 scorer 是13之一还是第14个方法？未明确说明，读者无法确定实验总数。
- - Major: 引用格式错误——"the best-performing scorer in PÃ¡ndy et al. (2022), LEEP Nguyen et al. (2020)"：scorer 名称"LEEP"与引用"Nguyen et al. (2020)"直接连写，缺少括号/分隔，应为"LEEP (Nguyen et al., 2020)"，影响语义解析。
- - Major: 摘要与正文间的数字校验缺失——摘要给出"13 scorers / 10 architectures / 11 datasets"，但正文（引言）未在引出这些数字时进行呼应，导致摘要数字成为"无源之数"，读者无法在引言中找到交叉验证。
### Minor（5）
- - Minor: OpenReview 链接渲染异常——"https: // openreview. net/ forum? id= 3i2ZRk8GDN"，URL 中多处插入空格，链接无法直接点击/复制使用。
- - Minor: 摘要使用模糊量词"surprisingly outperforms most existing scorers"中的"most"未给出具体比例（如13中的几个），与全文强调"standardized evaluation protocol"的严谨定位不符。
- - Minor: 术语使用不统一——摘要用"transferability scorers"，正文引言同时出现"transferability estimation"与"transferability scorers"两个术语指代相关概念，未在首次出现时定义二者关系（是同义、属与包含）。
- - Minor: 结构——引言第二段尾部出现孤立的短段落"As a result, this approach reducesâ¦"及后续"However, comparingâ¦"，段落切割碎裂，逻辑连贯性被打断，应合并或重组。
- - Minor: 图/表——引言中引用"PÃ¡ndy et al. (2022)"的结论（LEEP 是最优还是最差），但未给出相应图表/表格交叉引用（如"see Table 1"/"Figure 2"），读耄无法快速定位实验证据。

## 伦理（ethics）— ok
### Critical（2）
- - Critical: 论文使用 ImageNet、PASCAL VOC、SUN397 等 11 个数据集，但全文未见任何数据许可（license）合规声明；ImageNet、SUN397 等含未征得个人同意采集的人物图像，复用与再分发存在版权与肖像权风险，却未作任何说明。
- - Critical: 未对所用预训练模型（Torchvision、Hugging Face 仓库中的 10 种架构）的许可条款（如 Apache-2.0、非商用、CC-BY-NC 等）进行核查与披露，benchmark 复用他人权重但未说明许可兼容性，存在合规隐患。
### Major（3）
- - Major: 缺少利益冲突（COI）与资金来源声明——作者 Eduardo Valle 任职于商业公司 Intercom，其余作者分属 MIT、UNICAMP 等机构，存在潜在商业利益与产业关联，但文中未见 COI 章节。
- - Major: 完全缺失 "broader impact / 误用风险" 讨论：迁移性评分器可用于高效筛选模型以部署于监控、人脸识别、深度伪造辅助等高风险场景，方法越通用越好用，误用风险越高，论文未作任何警示或缓解建议。
- - Major: 未讨论数据隐私影响——所用源/目标数据集中可能包含可识别个人身份信息（PII），benchmark 大规模复用此类数据未评估对数据主体的隐私影响，也未说明是否符合 GDPR 等法规。
### Minor（2）
- - Minor: TMLR 采用开放评审（非双盲），作者身份与机构公开可能引入评审偏见（虽为该刊既定政策），但论文未在伦理声明中对此加以说明或致谢潜在偏差。
- - Minor: 未声明代码与基准结果所依赖第三方组件的许可证清单，影响下游复用者的合规判断。

## 汇总

- **Critical: 14 | Major: 24 | Minor: 16**
- ⚠ 有 Critical：产出需修复后重审（收敛门：一轮无新 Critical/Major）