# 审稿工作流运行摘要：tmlr_JQA0EfQIfj

- 时间：2026-08-26T07:20:31+00:00
- 论文：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\pdfs\JQA0EfQIfj.pdf`
- 投稿包：`None`
- 证据目录：

## 总体门禁：**WARN** | 建议评分：**6/10**（min 维度：{'structure': 6, 'evidence': 6, 'text': 6}）

证据层无 FAIL；R3 裁决收敛与 R5 人工定性完成后，终审人工给出最终分（suggested_score 是临时下界参考）。

## 阶段表

| 阶段 | 结论 | 门禁 | 关键指标 |
|---|---|---|---|
| R0 | PASS | **PASS** | 缺失输入 0，跨源风险目录 0（上一轮，未重跑）（上一轮，未重跑） |
| R1 | MAJOR | **WARN** | 章节缺失 ['discussion', 'limitations']；未找到 abstract（PDF 提取文本）（上一轮，未重跑）（上一轮，未重跑） |
| R1b | - | **SKIP** | PDF 模式：无 bib 源，引用核验降级 SKIP（上一轮，未重跑）（上一轮，未重跑） |
| R1c | - | **SKIP** | PDF 模式：无 \title 源码，断言对照降级 SKIP（上一轮，未重跑）（上一轮，未重跑） |
| R1d | - | **SKIP** | PDF 模式：无 tex 源码，行内算术/公式引用核验降级 SKIP（上一轮，未重跑）（上一轮，未重跑） |
| R2 | - | **SKIP** | 未配置 zip（仅磁盘审查）（上一轮，未重跑）（上一轮，未重跑） |
| R2b | - | **SKIP** | 未配置 zip（上一轮，未重跑）（上一轮，未重跑） |
| R2c | - | **SKIP** | PDF 模式：无 \includegraphics 源码，图表核验降级 SKIP（上一轮，未重跑）（上一轮，未重跑） |
| R2d | - | **SKIP** | PDF 模式：无 tabular 源码，表格核验降级 SKIP（上一轮，未重跑）（上一轮，未重跑） |
| R3 | MAJOR | **SKIP** | SKIP 无证据目录：数字不可核验（论文小数 1081，机械噪音 843，待复核 238 清单备查） |
| R4 | PASS | **PASS** | PASS：统计记录 0 条（MATCH 0，MISMATCH 0，NOT_IN_PAPER 0）——McNemar/Friedman/Wilson 复算（上一轮，未重跑）（上一轮，未重跑） |
| R5 | PASS | **PASS** | PASS：hint 命中 0，可疑 0（一票否决），已披露 0（上一轮，未重跑）（上一轮，未重跑） |
| R6 | MAJOR | **WARN** | 文本层：Critical 16 / Major 24 / Minor 6（1 轮，RPC HTTP 200）（上一轮，未重跑）（上一轮，未重跑） |
| R6b | MAJOR | **WARN** | MAJOR：四维 {'P': 9, 'R': 5, 'I': 7, 'S': 6}（min=5，短板 R(严谨性)）——最弱维度 R(严谨性) = 5 分（<= 6）→ 文本层 WARN；证据层门禁不受影响（上一轮，未重跑）（上一轮，未重跑） |
| R6c | MAJOR | **WARN** | MAJOR：辩论后维持 Critical 16 / Major 4（撤回 0，部分成立 0）；注：原始 46 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 26 条未辩论）（上一轮，未重跑）（上一轮，未重跑） |

## 下一步（人工阶段）

1. **R4 统计定性（人工）**：stats_recompute.md 中 MISMATCH/NOT_IN_PAPER 条目逐条定性（统计错误 / 口径换算 / 产物造假）；检验选择配对、退化情形披露、功效、多重比较清单见 REVIEW_SOP.md R4
2. **R1b 联网核验（可选）**：config 设 citation_online=true 复跑，核验 arXiv/DOI 真实性
3. **R1c 新颖性对照（可选）**：config 设 novelty_online=true 复跑，arXiv 检索先行工作并比对断言
4. **R3 裁决收敛**：238 个待复核数字 → 在 `None` 填 verdict(noise|supported|critical) 后重跑
5. **R6 收敛**：LLM 意见修复后重跑至一轮无新 Critical/Major；--converge 3 可降轮间噪声
6. **R6b PRISM 复盘**：最弱维度 R(严谨性) = 5 分（P/R/I/S = {'P': 9, 'R': 5, 'I': 7, 'S': 6}），四维证据句见 prism_review.md
7. **R6c 辩论结果**：sustained 条目是作者 rebuttal 后仍成立的问题（修复优先级最高）；withdrawn 为 LLM 单轮假阳性；另有 26 条未进辩论（截断上限 20，见 debate.md 注记）

## 复跑命令

```powershell
python "F:\deepseek\research-kit\review-workflow\scripts\run_review.py" --config "F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\configs\JQA0EfQIfj.json"
```