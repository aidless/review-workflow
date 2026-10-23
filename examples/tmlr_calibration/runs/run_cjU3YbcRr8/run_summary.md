# 审稿工作流运行摘要：tmlr_cjU3YbcRr8

- 时间：2026-08-26T07:20:27+00:00
- 论文：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\pdfs\cjU3YbcRr8.pdf`
- 投稿包：`None`
- 证据目录：

## 总体门禁：**WARN** | 建议评分：**6/10**（min 维度：{'structure': 6, 'evidence': 6, 'text': 6}）

证据层无 FAIL；R3 裁决收敛与 R5 人工定性完成后，终审人工给出最终分（suggested_score 是临时下界参考）。

## 阶段表

| 阶段 | 结论 | 门禁 | 关键指标 |
|---|---|---|---|
| R0 | PASS | **PASS** | 缺失输入 0，跨源风险目录 0（上一轮，未重跑）（上一轮，未重跑） |
| R1 | MAJOR | **WARN** | 章节缺失 ['related', 'discussion']；未找到 abstract（PDF 提取文本）（上一轮，未重跑）（上一轮，未重跑） |
| R1b | - | **SKIP** | PDF 模式：无 bib 源，引用核验降级 SKIP（上一轮，未重跑）（上一轮，未重跑） |
| R1c | - | **SKIP** | PDF 模式：无 \title 源码，断言对照降级 SKIP（上一轮，未重跑）（上一轮，未重跑） |
| R1d | - | **SKIP** | PDF 模式：无 tex 源码，行内算术/公式引用核验降级 SKIP（上一轮，未重跑）（上一轮，未重跑） |
| R2 | - | **SKIP** | 未配置 zip（仅磁盘审查）（上一轮，未重跑）（上一轮，未重跑） |
| R2b | - | **SKIP** | 未配置 zip（上一轮，未重跑）（上一轮，未重跑） |
| R2c | - | **SKIP** | PDF 模式：无 \includegraphics 源码，图表核验降级 SKIP（上一轮，未重跑）（上一轮，未重跑） |
| R2d | - | **SKIP** | PDF 模式：无 tabular 源码，表格核验降级 SKIP（上一轮，未重跑）（上一轮，未重跑） |
| R3 | MAJOR | **SKIP** | SKIP 无证据目录：数字不可核验（论文小数 271，机械噪音 177，待复核 94 清单备查） |
| R4 | PASS | **PASS** | PASS：统计记录 0 条（MATCH 0，MISMATCH 0，NOT_IN_PAPER 0）——McNemar/Friedman/Wilson 复算（上一轮，未重跑）（上一轮，未重跑） |
| R5 | PASS | **PASS** | PASS：hint 命中 0，可疑 0（一票否决），已披露 0（上一轮，未重跑）（上一轮，未重跑） |
| R6 | MAJOR | **WARN** | 文本层：Critical 9 / Major 24 / Minor 11（1 轮，RPC HTTP 200）（上一轮，未重跑）（上一轮，未重跑） |
| R6b | MAJOR | **WARN** | MAJOR：四维 {'P': 8, 'R': 6, 'I': 6, 'S': 7}（min=6，短板 R(严谨性)）——最弱维度 R(严谨性) = 6 分（<= 6）→ 文本层 WARN；证据层门禁不受影响（上一轮，未重跑）（上一轮，未重跑） |
| R6c | MAJOR | **WARN** | MAJOR：辩论后维持 Critical 7 / Major 10（撤回 1，部分成立 2）；注：原始 44 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 24 条未辩论）（上一轮，未重跑）（上一轮，未重跑） |

## 下一步（人工阶段）

1. **R4 统计定性（人工）**：stats_recompute.md 中 MISMATCH/NOT_IN_PAPER 条目逐条定性（统计错误 / 口径换算 / 产物造假）；检验选择配对、退化情形披露、功效、多重比较清单见 REVIEW_SOP.md R4
2. **R1b 联网核验（可选）**：config 设 citation_online=true 复跑，核验 arXiv/DOI 真实性
3. **R1c 新颖性对照（可选）**：config 设 novelty_online=true 复跑，arXiv 检索先行工作并比对断言
4. **R3 裁决收敛**：94 个待复核数字 → 在 `None` 填 verdict(noise|supported|critical) 后重跑
5. **R6 收敛**：LLM 意见修复后重跑至一轮无新 Critical/Major；--converge 3 可降轮间噪声
6. **R6b PRISM 复盘**：最弱维度 R(严谨性) = 6 分（P/R/I/S = {'P': 8, 'R': 6, 'I': 6, 'S': 7}），四维证据句见 prism_review.md
7. **R6c 辩论结果**：sustained 条目是作者 rebuttal 后仍成立的问题（修复优先级最高）；withdrawn 为 LLM 单轮假阳性；另有 24 条未进辩论（截断上限 20，见 debate.md 注记）

## 复跑命令

```powershell
python "F:\deepseek\research-kit\review-workflow\scripts\run_review.py" --config "F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\configs\cjU3YbcRr8.json"
```