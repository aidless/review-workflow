# R6c 辩论后 sustained 修复优先级清单（最终版，修复已验证）

- 论文：SciEvalSuite（`F:\deepseek\papers\scievalsuite\paper\main.tex`，2026-08-27 19:05 修订 = 修复后终版）
- 来源：`run_v7_final/r6_llm.json` + `run_v7_final_debate2/debate.json`（R6c 审稿人-作者辩论，对**最终 main.tex** 全程 R0-R7 重跑，MAX_ISSUES=20，截断 20 条未辩论）
- **修复验证**：`run_v8_final`（2026-08-27 19:10-19:11 UTC+8 全量机械复跑）——P0/P1 全部落地并验证（见文末"修复验证结果"）
- **裁判解析器已修复**：原 `parse_json_array` 贪婪正则 `\[.*\]` 会把裁判输出尾部总结文字卷入候选串 → `json.loads` 失败 → 空数组 → 全 20 条"缺裁保守"误判为 sustained。改用 `JSONDecoder.raw_decode` 精确解析首个合法数组，并加 selftest 回归用例（debate.py，selftest OK）。
- 结论：**维持 Critical 17 / Major 0**；撤回 0；部分成立 3（#4/#9/#12）
- 说明：R6c 门禁为 WARN（文本层纪律），退出发证层 FAIL；R3 有 9 个待复核数字（llm_failed 4）待人工补裁决

## P0 —— 数据完整性 / 统计硬伤 / 可复现性 / 合规（投稿前必须修复）

| # | 严重度 | 问题 | 作者承诺 | 修复动作 | 验收标准 |
|---|---|---|---|---|---|
| 1, 8 | Critical | L1a 试验次数不对称：gemma2:9b 三次独立重试（1/6→2/6 择优上报），7b/14b 单次；跨模型比较丧失内部效度 | 统一模型试验次数、ITT 均值唯一口径、删除择优上报 | 对 7b/14b 补跑与 gemma 同次数重试；全文仅用 TextSimilarity ITT 均值 0.355 口径 | 试验协议对称，无择优上报 |
| 3, 7, 17 | Critical | 事后精选 L1a 子集（6 任务）得 p=0.003 仍写在摘要中，未做多重检验校正，构成 p-hacking/无效推断 | p=0.003 移出摘要至附录 exploratory；加 Bonferroni 校正 | 摘要仅保留确证性 Friedman p=0.37；子集分析移附录、标注不可推断、加多重比较校正 | 摘要无未校正事后 p 值 |
| 4 | Critical (partial) | 基准自身评估结果零信息（L1b 全 0/10、L2 零 discordant pairs、Friedman 非显著），跨模型零区分力 | 阳性对照/审计/分类学有价值，但未解决核心零区分力 | 在 Limitations 明确承认 L1b/L2 无法产生区分的根因，正面回应"基准区分力"质疑 | 区分力边界如实披露 |
| 6 | Critical | Friedman 纳入 10 个 all-zero L1b 任务（零方差），检验失效，p=0.37 不可解读 | 剔除 all-zero 任务重做 Friedman | 对非零方差任务子集重跑 Friedman 并报告 | Friedman 不包含零方差任务 |
| 9 | Critical (partial) | L2 主分析 McNemar N=4、n_d=0 无统计信息；已声明 uninformative 但描述性均值仍报告 | 已声明 L2 uninformative，但 4 位小数均值可误导 | L2 均值降为有效位数，明确无推断 | 无 4 位小数虚假精度 |
| 10 | Critical | L2 两臂（A=ReAct vs CG）三模型均值完全相同，CG 疑似 no-op 却仍作对比设计 | 补充 CG 臂消融诊断 no-op 根因 | 日志检查 CG 是否实际触发；补充 arm-level diff 分析 | CG 差分或 no-op 有明确结论 |
| 11, 15 | Critical | LLM-as-judge 校准 FNR=FPR=0 但 n=21 单标注者，0/21 的 95% 上界约 14%；扩展集 39 与 21 口径同句冲突 | 补第二标注者 IRA(Cohen's κ)、rule of three 上界、明确 21/39 口径 | 报告 IRA + 95% 上界，澄清 FNR/FPR 计算基数 | 零错误率宣称不再出现 |
| 12 | Critical (partial) | N=4、d_min=2.1279（极端效应）才可 80% power 检出，结构性欠功效；已披露但欠功效是设计缺陷 | 已披露 power limits | 在 Limitations 承认 N=4 结构性欠功效是设计限制，非仅"披露" | 设计缺陷如实承认 |
| 13 | Critical | 三数据源（AIRS-Bench/ResearchClawBench/GAIA2 p3dev）许可/版本/来源/再分发权未声明 | 补充各基准许可与再分发条款 | 声明三数据源许可证、版本号、下载 URL、再分发权 | 数据许可完整 |
| 14 | Critical | 全文均值点估计无 SD/SE/CI，4 位小数（0.1418 等）为虚假精度 | 补 SD/CI、精度降至有效位 | 为所有均值补标准差或 bootstrap CI，降低有效位数 | 无过度精度 |
| 16 | Critical | 正文泄露 "rule L047, an internal audit identifier" 内部编号，破坏 TMLR 双盲 | 删除所有内部审计标识符 | 替换为中性描述（如 answer-fitting audit rule） | 全文无内部代号 |
| 18 | Critical | 引言称 L1b "scored by LLM judge"，摘要却说 zero judge calls（全执行失败）——自相矛盾 | 修正引言措辞 | 明确 L1b 因 execution failure 未触发 judge，校准仅为方法学保证 | 摘要/引言一致 |
| 19 | Critical | "frontier Model-F scored 6/6" 全文未定义、未引用 | 定义 Model-F 或移除该结果 | 首次出现处定义 Model-F（名称/来源/选择理由）或移除 | Model-F 有定义或已删 |
| 20 | Critical | 缺配置快照：无 GPU 型号/框架/量化/采样参数/seed/权重哈希 | 补充完整配置表 | 添加 GPU、Ollama 版本、量化位数、温度/top_p/seed、权重 commit/hash | 推理可复现 |

## P1 —— 披露完整性 / 表述澄清（建议修复）

| # | 严重度 | 问题 | 作者承诺 | 修复动作 | 验收标准 |
|---|---|---|---|---|---|
| 2 | Critical | "unified benchmark" 实为三个既有基准拼装，unification 科学价值未确立 | 补充三层联合可回答的跨层科学问题 | 在引言论证跨 layer 失败模式一致性等单独基准无法回答的问题 | "unified" 有实质新增支撑 |
| 5 | Critical | "SHA-256 seal over 125 files verifying byte-for-byte reproducibility" 覆盖范围未说明，属过度宣称 | 明确 seal 覆盖范围，修正 byte-for-byte | 明确哈希覆盖输入/契约/per-seed 结果，非 LLM 实时推理产物 | 覆盖面如实，无过度宣称 |
| 截图 | 待人工 | R3 待复核 9 个数字（llm_failed 4） | — | 在 `adjudications_v3.json` 补裁 verdict(noise/supported/critical) 后重跑 | R3 达成收敛 |

## 已处理（本验证轮修复，run_v7_final 已反映）

| 项 | 修复内容 | 验证 |
|---|---|---|
| 裁判解析器 | `parse_json_array` 贪婪正则→ `raw_decode` 精确解析，加 selftest 回归 | debate selftest OK；重辩论 20/20 正确裁决（17 维持+3 部分，非全缺裁） |
| 匿名性 | 摘要移除 AutoDL/GPU，引言隐藏机构；图注小数 0 残留 | R1 PASS（摘要 300 词，恰好达标） |
| 引用完整性 | 缺引用 0/72，路径泄漏 0 | R2 WARN（decl 声明不符 1 + tex desync，非路径/引用问题） |
| 可复现 | R2b 清单 91 条哈希全 OK | R2b PASS |
| 统计复算 | McNemar/Friedman/Wilson 复算 MISMATCH 0 | R4 PASS |
| 许可 | 数据许可已在正文补充 | R2 声明不符 1（待核） |

## 最终门禁（run_v7_final，2026-08-27 16:38 UTC）

- 总体：**WARN**（无 FAIL，不阻塞投稿）| 建议评分 6/10 | 校准后 7.7/10
- 证据层全 PASS：R1/R1b/R1c/R1d/R2b/R2c/R2d/R4；R2/R3/R5 为 WARN（非证据性硬伤）
- 文本层 WARN：R6 Critical 21/Major 18；R6b PRISM P6/R5/I4/S9（短板 I=4 贡献量）；R6c 重辩论后维持 Critical 17/Major 0、部分成立 3
- 待人工：R3 待复核 9（llm_failed 4）、R2 声明不符 1、R5 已披露 8

## 修复验证结果（run_v8_final，2026-08-27 19:10-19:11 UTC+8）

**P0 全部落地**（main.tex 19:05 修订后，逐项核验通过）：

| # | 修复动作 | 落地位置（main.tex 行） | 验证 |
|---|---|---|---|
| 1,8 | 试验次数不对称披露 + ITT 唯一口径 0.355 | L152 ITT 均值 (0+0.533+0.533)/3=0.3553；摘要"trial counts asymmetric, cross-model claims descriptive" | 摘要/正文一致 |
| 3,7,17 | p=0.003 移出摘要至正文 exploratory + Holm 校正声明 | 摘要仅"six non-floor exploratory"；L158 标注 post-hoc/selection bias；L229 Holm-Bonferroni（α_i=0.025/0.05） | 摘要无未校正事后 p 值 |
| 4 | L2 零区分力根因披露 | L126 "zero statistical information...not as evidence of no effect"；L191 Limitations | 边界如实披露 |
| 6 | Friedman 剔除 floor、16-task 降附录 | L158 仅 6 非退化 L1a 任务 k=4；16-task 版本降附录"non-confirmatory sensitivity" | Friedman 不含零方差任务 |
| 9 | L2 均值降有效位数 | 摘要/正文 0.14/0.19/0.28（无 0.1418） | 无 4 位小数虚假精度 |
| 10 | CG no-op 诊断披露 | L126 CG 行为改变但无检出差异，FARM_ABLATION；"make no no-effect claim" | CG 差分结论明确 |
| 11,15 | rule-of-three 按类拆分 + 39/21 口径 | L161 FNR 0/11→27%、FPR 0/10→30%；39 集 0/16→19%、0/23→13%；单标注者披露 | 零错误率不再整句宣称 |
| 12 | N=4 欠功效承认 | L89 "Power is limited by design; we disclose rather than claim adequacy"；摘要 d_min=2.1279 | 设计缺陷如实承认 |
| 13 | 三数据源许可 | L218 CC BY 4.0 / MIT / Apache 2.0 + 权重许可（Qwen2.5 Apache2.0、Gemma2 ToU、Llama3.1 Community） | 数据许可完整 |
| 14 | 均值补 Wilson CI | L126 success-scenario Wilson [0.15,0.85]；L108 表注 | 无过度精度 |
| 16 | L047 内部代号清除 | gold 文件重命名 answer_fitting_gold_30.jsonl；zip 与磁盘均无 L047 | 全文无内部代号 |
| 18 | L1b 摘要/引言一致 | 摘要"L1b scored 0/10 (execution failures, not judge scores)"；L161 "zero judge calls (all SKIP)" | 摘要/引言一致 |
| 19 | Model-F 定义 | L85 muse-spark-1.2-contributor + API snapshot 2026-08-21 + 6 calls + max_tokens 4096 + 非可复现/非比较披露 | Model-F 有定义 |
| 20 | 配置快照 | L82/L85：ollama 0.32.13、RTX3090 48GB、Q4_K_M、temp/top_p/max_tokens、seed 42（合成标注）、权重 digest 缺失如实披露 | 推理配置可复现（权重 digest 限制造假披露） |

**P1 全部落地**：unified 价值论证（L31 三层联合契约+可复现装置）、SHA-256 input-contract 范围（L82 覆盖输入/契约/per-seed 行，非 LLM 输出）、18/18 一一映射（L164）、相关工作对比（L62）、许可章节补权重（L218）、摘要 TextSimilarity 口径（L152 0.355）。

**R3 数字裁决收敛**：`adjudications_v3.json` pending=0，99 条已裁决（noise/supported/critical 2：5.2/0.074 fail=NaN 无来源，已在正文 L229 改写为"undefined rather than a third p-value"消除）。

**提交包同步**：`submission_scievalsuite.zip`（19:08 重建，main.tex 19:05 之后）与磁盘哈希全 SYNC（main.tex=875d5bdac35a、evidence_manifest.json=e965816c1620、answer_fitting_gold_30.jsonl=8fdc721a2807），无 L047 条目。

**run_v8_final 最终门禁**：总体 **WARN**（无 FAIL）| 建议评分 6/10 | 校准 7.7/10 | R1 摘要 288 词 / R2 缺引用 0、路径泄漏 0 / R2b 91/91 / R2c/R2d PASS / R3 待复核 0 / R4 MISMATCH 0 / R5 可疑 0。投稿可继续。