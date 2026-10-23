# 审稿人-作者辩论报告（v2.0）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_TupiNRpgHw\extracted_text.txt`；问题来源：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_TupiNRpgHw\r6_llm.json`
- RPC：HTTP 200
- 结论：**MAJOR** —— 辩论后维持 Critical 11 / Major 8 （撤回 0，部分成立 1）；注：原始 50 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 30 条未辩论）；文本层 WARN 纪律不变

| # | 严重度 | 问题 | 作者回应 | 终裁 | 理由 |
|---|---|---|---|---|---|
| 1 | Critical | - Critical: "various environments with dynamics shifts"对环境样本 | 将在实验部分补充测试环境数量、每环境随机种子数（≥5）及均值±标准差报告方式。 | sustained | Concede; current version lacks env count and seed  |
| 2 | Critical | - Critical: Figure 1 中箭头标注 `(s^tar, a^tar, r^tar, s'^tar) â | 将把Figure 1箭头改为从源域校正元组指向目标域对齐方向,并补充文字说明校正语义。 | sustained | Concede; Figure 1 arrow direction currently mislea |
| 3 | Critical | - Critical: 全文（含摘要/引言/图1）未见代码仓库链接、commit hash 或匿名代码包，无法定位可复现 | 将在摘要与图1补充匿名代码仓库链接及commit hash。 | sustained | Concede; no code link/commit hash in current versi |
| 4 | Critical | - Critical: 摘要与 Figure 1 caption 在"哪些模型执行校正"上矛盾—摘要称"leverage | 将把caption中"by using the inverse policy model"改为包含reward mode | sustained | Concede; abstract-caption contradiction on reward  |
| 5 | Critical | - Critical: 摘要中称"STC achieves superior performance against e | 将补充t检验或Wilcoxon秩和检验及95%置信区间以支撑"superior"声明。 | sustained | Concede; no significance tests or CIs in current v |
| 6 | Critical | - Critical: 摘要声称"Instead, we propose to modify the source do | 将修改摘要措辞,明确STC是"校正reward至目标域"而非"惩罚式reward modification"。 | sustained | Concede; STC does modify rewards via reward model, |
| 7 | Critical | - Critical: 校正仅修改动作 $\hat{a}_{src}=f_{inv}(s_{src}, s'_{src} | 论文摘要称"employ a forward dynamics model to retain corrected sa | partial | Rebut cites Selection step in paper, but paper doe |
| 8 | Critical | - Critical: 核心校正机制依赖逆策略模型 $f_{inv}(s, s')$，但该模型仅在有限目标域数据上训练— | 将在讨论部分补充逆/前向模型均依赖有限目标域数据这一循环依赖的局限性分析。 | sustained | Concede; circular dependency of inverse model on l |
| 9 | Critical | - Critical: 正文实验部分被截断，无法确认基线是否享有与 STC 同等的目标域监督（STC 额外训练前向动力学 | 将确保所有基线享有等量目标域模型容量与数据访问,并在实验部分明确说明公平性。 | sustained | Concede; baseline fairness (equal model capacity/d |
| 10 | Critical | - Critical: 消融完整性存疑：STC 同时包含"动作修正 + 奖励修正 + 前向模型选择"三组件，但摘要/介绍 | 将补充"仅动作修正""仅奖励修正""仅选择""修正+选择"的解耦消融实验。 | sustained | Concede; no decoupled ablation of action/reward/se |
| 11 | Critical | - Critical: 类似地，文中将本法与"transition filtering"对立，但 STC 的"Selec | 将修改摘要定位,明确STC含校正+筛选,筛选作用于校正后数据,区别于纯筛选。 | sustained | Concede; Selection step is filtering by definition |
| 12 | Critical | - Critical: 论文有4名作者来自腾讯（Jiafei Lyu、Jingwen Yang、Zichuan Lin、 | 将补充利益冲突声明、资金来源披露及腾讯角色说明。 | sustained | Concede; 4 Tencent authors, no COI/funding disclos |
| 13 | Major | - Major: Figure 1 中 reward model 标注为 `r(s,a)`，与 forward/inve | 将统一图中r(s,a)命名为f_r并移至Correction模块旁,与f_fwd/f_inv规范一致。 | sustained | Concede; r(s,a) naming and placement inconsistent  |
| 14 | Major | - Major: Figure 1 中数据集符号不一致—图体内为粗正体 `ð·ð¡ðð`/`ð· | 将统一图体与caption中数据集符号为同一排版格式。 | sustained | Concede; dataset symbol formatting inconsistency b |
| 15 | Major | - Major: GAP 的真实性未被证明。"may lead to insufficient exploitation | 将补充定量分析:现有filtering方法丢弃的源数据比例 vs STC保留比例。 | sustained | Concede; 'may lead to insufficient exploitation' i |
| 16 | Major | - Major: caption 称三个模型"are trained to capture the bidirectio | 将把caption中"bidirectional dynamics transition information"改为含 | sustained | Concede; reward model r(s,a) misclassified as 'dyn |
| 17 | Major | - Major: inverse dynamics model 用于 action relabeling、forward | 将在相关工作中与ICM等文献明确区分,强调校正+选择组合在跨域离线RL中的新颖性。 | sustained | Concede; novelty over ICM and existing model-based |
| 18 | Major | - Major: seed 管理缺失：可见部分未声明随机种子数量、均值±方差报告方式或显著性检验，仅称"achieves | 将在实验部分声明随机种子数（≥5）、均值±方差报告及显著性检验。 | sustained | Concede; no seed count, mean±std, or significance  |
| 19 | Major | - Major: 前向模型一致性选择准则会系统性偏好某些转移类型（如确定性高、模型置信度高的区域），引入选择偏差，改变合 | 将讨论前向模型选择偏差对数据覆盖性的影响,并补充选择准则敏感性分析。 | sustained | Concede; selection bias from forward model consist |
| 20 | Major | - Major: 因果推断不充分——"直接合并导致次优性能"作为核心动机被陈述为前提而非经验验证；且若缺少将"仅校正"" | 将补充"直接合并"实证对比及各组件消融,将性能提升因果归因于所提机制而非数据增量。 | sustained | Concede; 'direct merging suboptimal' stated as pre |
| 21 | Minor | （另有 30 条问题超出 20 条上限被截断，未参与辩论） | - | 截断标注（不计入统计） |  |

**辩论后**：维持 Critical 11 / Major 8 / Minor 0；撤回 0 条（假阳性被作者驳回）；部分成立 1 条

## 解读

- sustained = 经过作者 rebuttal 仍然成立的问题（修复优先级最高）
- withdrawn = 作者引用论文内容成功驳回（LLM 单轮审稿的假阳性）
- partial = 部分成立（建议作者在 camera-ready 中处理）
