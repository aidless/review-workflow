# 审稿工作流运行摘要：f1f5_f1_cachemem

- 时间：2026-08-28T09:49:01+00:00
- 论文：`F:/Research/F1_Single_10page/paper/main.tex`
- 投稿包：`F:/Research/_inbox/F1-F5_F45_2026-08-26/TMLR_4p5_Tier123_FINAL_20260827.zip`
- 证据目录：`F:/Research/_inbox/F1-F5_F45_2026-08-26/supplementary`

## 总体门禁：**FAIL** | 建议评分：**4/10**（min 维度：{'structure': 6, 'evidence': 4, 'text': 6}）

### 校准后评分：**4.0/10**（证据层 FAIL：校准样本（n=6 全 accept，无 FAIL 论文）不含 FAIL 区间——偏移不外推，cap 4 纪律不变）

- 排序信号：PRISM R vs yes_rate ρ=0.89（唯一显著维度）；问题数 null（ρ≈0）→ 本次 8 条 stable Critical 不进一步调幅文本维
- 边界：accept 侧单侧校准：TMLR 拒稿不公开，FAIL↔reject 方向无标定；n=6 小样本：偏移量本身有不确定性，calibrated_score 是排序参考而非绝对分；决议两级（7/8）映射，绝对分校准天然粗糙；claims 投票针对投稿版，与终版 PDF 有版本差

证据层存在 FAIL → 按评分纪律 cap 4；先修 FAIL 项再进入文本层评审。

## 阶段表

| 阶段 | 结论 | 门禁 | 关键指标 |
|---|---|---|---|
| R0 | MAJOR | **WARN** | 缺失输入 0，跨源风险目录 1（F:\Research\_inbox\F1-F5_F45_2026-08-26\supplementary 不在 F:\Research\F1_Single_10page 下 → 打包遗漏高风险） |
| R1 | MAJOR | **WARN** | 章节缺失 ['limitations', 'conclusion'] |
| R1b | PASS | **PASS** | PASS：条目 10，幽灵引用 0，结构 Major 0（offline 结构检查） |
| R1c | - | **SKIP** | 未启用联网检索（config 设 novelty_online=true 开启 arXiv 先行工作对照） |
| R1d | PASS | **PASS** | PASS：行内算术 0 处（不符 0，含括号百分数 0）；悬空公式引用 0；符号推导/量纲不在机械覆盖内 |
| R2 | CRITICAL | **FAIL** | CRITICAL：缺引用 16/16，路径泄漏 9，声明不符 1，tex desync False |
| R2b | ERROR | **WARN** | 清单核验跳过：manifest not found in zip (searched: evidence_manifest.json, ASSET_MANIFEST.json) |
| R2c | PASS | **PASS** | PASS：图 3 幅（矢量文本 3，位图跳过 0，缺失 0）；图注小数 2 个，无支撑 0；figure_only 2 |
| R2d | MAJOR | **WARN** | MAJOR：表 4 个（numeric cell 34），无支撑 10，\input 缺失 0，混精度列 0（INFO） |
| R3 | MAJOR | **FAIL** | MAJOR：待复核 64，机械噪音 21，已裁决 0（critical 0）；裁决 CRITICAL（mech 7 / llm 22 / noise 7 / supported 7 / critical 15 / llm_failed 0）（上一轮，未重跑） |
| R4 | PASS | **PASS** | PASS：统计记录 0 条（MATCH 0，MISMATCH 0，NOT_IN_PAPER 0）——McNemar/Friedman/Wilson 复算（上一轮，未重跑） |
| R5 | MAJOR | **WARN** | MAJOR：hint 命中 1600，可疑 0（一票否决），已披露 0（上一轮，未重跑） |
| R6 | MAJOR | **WARN** | 文本层：Critical 8 / Major 11 / Minor 5（3 轮，RPC HTTP 200）；轮间不稳定（噪声候选，不计门禁）：Critical 23 / Major 61（上一轮，未重跑） |
| R6b | MAJOR | **WARN** | MAJOR：四维 {'P': 7, 'R': 6, 'I': 5, 'S': 8}（min=5，短板 I(贡献量)）——最弱维度 I(贡献量) = 5 分（<= 6）→ 文本层 WARN；证据层门禁不受影响（上一轮，未重跑） |
| R6c | MAJOR | **WARN** | MAJOR：辩论后维持 Critical 6 / Major 10（撤回 3，部分成立 0）；注：原始 24 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 4 条未辩论）（上一轮，未重跑） |

## 下一步（人工阶段）

1. **R4 统计定性（已自动化）**：MISMATCH/NOT_IN_PAPER 由口径换算机械层 + LLM 对抗裁决自动定性（stats_adjudications.md）；仅 llm_failed 条目需人工补判；检验选择配对、退化情形披露、功效、多重比较清单见 REVIEW_SOP.md R4
2. **R1b 联网核验（可选）**：config 设 citation_online=true 复跑，核验 arXiv/DOI 真实性
3. **R1c 新颖性对照（可选）**：config 设 novelty_online=true 复跑，arXiv 检索先行工作并比对断言
4. **R3 裁决收敛**：64 个待复核数字 → 在 `None` 填 verdict(noise|supported|critical) 后重跑
5. **R6 收敛**：LLM 意见修复后重跑至一轮无新 Critical/Major；--converge 3 可降轮间噪声
6. **R6b PRISM 复盘**：最弱维度 I(贡献量) = 5 分（P/R/I/S = {'P': 7, 'R': 6, 'I': 5, 'S': 8}），四维证据句见 prism_review.md
7. **R6c 辩论结果**：sustained 条目是作者 rebuttal 后仍成立的问题（修复优先级最高）；withdrawn 为 LLM 单轮假阳性；另有 4 条未进辩论（截断上限 20，见 debate.md 注记）

## 复跑命令

```powershell
python "F:\deepseek\research-kit\review-workflow\scripts\run_review.py" --config "F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\f1.json"
```