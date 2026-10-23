# 审稿工作流运行摘要：scievalsuite_v6_converge3

- 时间：2026-08-26T07:46:02+00:00
- 论文：`F:/deepseek/papers/scievalsuite/paper/main.tex`
- 投稿包：`F:/deepseek/papers/scievalsuite/submission/submission_scievalsuite_final_v6.zip`
- 证据目录：`F:/deepseek/papers/scievalsuite/results`, `F:/deepseek/scievalsuite/out_p5`

## 总体门禁：**FAIL** | 建议评分：**4/10**（min 维度：{'structure': 6, 'evidence': 4, 'text': 6}）

### 校准后评分：**4.0/10**（证据层 FAIL：校准样本（n=6 全 accept，无 FAIL 论文）不含 FAIL 区间——偏移不外推，cap 4 纪律不变）

- 排序信号：PRISM R vs yes_rate ρ=0.89（唯一显著维度）；问题数 null（ρ≈0）→ 本次 18 条 stable Critical 不进一步调幅文本维
- 边界：accept 侧单侧校准：TMLR 拒稿不公开，FAIL↔reject 方向无标定；n=6 小样本：偏移量本身有不确定性，calibrated_score 是排序参考而非绝对分；决议两级（7/8）映射，绝对分校准天然粗糙；claims 投票针对投稿版，与终版 PDF 有版本差

证据层存在 FAIL → 按评分纪律 cap 4；先修 FAIL 项再进入文本层评审。

## 阶段表

| 阶段 | 结论 | 门禁 | 关键指标 |
|---|---|---|---|
| R0 | MAJOR | **WARN** | 缺失输入 0，跨源风险目录 1（F:\deepseek\scievalsuite\out_p5 不在 F:\deepseek\papers\scievalsuite 下 → 打包遗漏高风险）（上一轮，未重跑）（上一轮，未重跑） |
| R1 | MAJOR | **WARN** | 摘要 358 词（>300）（上一轮，未重跑）（上一轮，未重跑） |
| R1b | PASS | **PASS** | PASS：条目 12，幽灵引用 0，结构 Major 0（offline 结构检查）（上一轮，未重跑）（上一轮，未重跑） |
| R1c | - | **SKIP** | 未启用联网检索（config 设 novelty_online=true 开启 arXiv 先行工作对照）（上一轮，未重跑）（上一轮，未重跑） |
| R1d | PASS | **PASS** | PASS：行内算术 1 处（不符 0，含括号百分数 0）；悬空公式引用 0；符号推导/量纲不在机械覆盖内（上一轮，未重跑）（上一轮，未重跑） |
| R2 | CRITICAL | **FAIL** | CRITICAL：缺引用 24/58，路径泄漏 139，声明不符 0，tex desync True（上一轮，未重跑）（上一轮，未重跑） |
| R2b | CRITICAL | **FAIL** | CRITICAL：清单 165 条，OK 149，哈希不符 0，缺失 16（上一轮，未重跑）（上一轮，未重跑） |
| R2c | PASS | **PASS** | PASS：图 1 幅（矢量文本 1，位图跳过 0，缺失 0）；图注小数 1 个，无支撑 0；figure_only 0（上一轮，未重跑）（上一轮，未重跑） |
| R2d | PASS | **PASS** | PASS：表 3 个（numeric cell 30），无支撑 0，\input 缺失 0，混精度列 0（INFO）（上一轮，未重跑）（上一轮，未重跑） |
| R3 | MAJOR | **WARN** | MAJOR：待复核 94，机械噪音 5，已裁决 0（critical 0）（上一轮，未重跑）（上一轮，未重跑） |
| R4 | MAJOR | **WARN** | MAJOR：统计记录 6 条（MATCH 4，MISMATCH 0，NOT_IN_PAPER 1）——McNemar/Friedman/Wilson 复算（上一轮，未重跑）（上一轮，未重跑） |
| R5 | MAJOR | **WARN** | MAJOR：hint 命中 113，可疑 0（一票否决），已披露 9（上一轮，未重跑）（上一轮，未重跑） |
| R6 | MAJOR | **WARN** | 文本层：Critical 18 / Major 20 / Minor 0（3 轮，RPC HTTP 200）；轮间不稳定（噪声候选，不计门禁）：Critical 21 / Major 61 |
| R6c | MAJOR | **WARN** | MAJOR：辩论后维持 Critical 8 / Major 1（撤回 4，部分成立 7）；注：原始 38 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 18 条未辩论）（上一轮，未重跑） |

## 下一步（人工阶段）

1. **R4 统计定性（人工）**：stats_recompute.md 中 MISMATCH/NOT_IN_PAPER 条目逐条定性（统计错误 / 口径换算 / 产物造假）；检验选择配对、退化情形披露、功效、多重比较清单见 REVIEW_SOP.md R4
2. **R1b 联网核验（可选）**：config 设 citation_online=true 复跑，核验 arXiv/DOI 真实性
3. **R1c 新颖性对照（可选）**：config 设 novelty_online=true 复跑，arXiv 检索先行工作并比对断言
4. **R3 裁决收敛**：94 个待复核数字 → 在 `F:/deepseek/research-kit/review-workflow/examples/scievalsuite_v6/adjudications_v3.json` 填 verdict(noise|supported|critical) 后重跑
5. **R6 收敛**：LLM 意见修复后重跑至一轮无新 Critical/Major；--converge 3 可降轮间噪声
6. **R6c 辩论结果**：sustained 条目是作者 rebuttal 后仍成立的问题（修复优先级最高）；withdrawn 为 LLM 单轮假阳性；另有 18 条未进辩论（截断上限 20，见 debate.md 注记）

## 复跑命令

```powershell
python "F:\deepseek\research-kit\review-workflow\scripts\run_review.py" --config "F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\config_v3_converge.json"
```