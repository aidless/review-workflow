# 审稿工作流运行摘要：scievalsuite_v6_online

- 时间：2026-08-26T09:41:09+00:00
- 论文：`F:/deepseek/papers/scievalsuite/paper/main.tex`
- 投稿包：`F:/deepseek/papers/scievalsuite/submission/submission_scievalsuite_final_v6.zip`
- 证据目录：`F:/deepseek/papers/scievalsuite/results`, `F:/deepseek/scievalsuite/out_p5`

## 总体门禁：**WARN** | 建议评分：**6/10**（min 维度：{'structure': 6}）

证据层无 FAIL；R3 裁决收敛与 R5 人工定性完成后，终审人工给出最终分（suggested_score 是临时下界参考）。

## 阶段表

| 阶段 | 结论 | 门禁 | 关键指标 |
|---|---|---|---|
| R1b | MAJOR | **WARN** | MAJOR：条目 12，幽灵引用 0，结构 Major 0，ID 不存在 0，标题不符 2（联网核验 11 条） |
| R1c | PASS | **PASS** | PASS：断言 1 句（强 0）；检索 15 条，近重复 0（未引用 0） |

## 下一步（人工阶段）

1. **R4 统计定性（已自动化）**：MISMATCH/NOT_IN_PAPER 由口径换算机械层 + LLM 对抗裁决自动定性（stats_adjudications.md）；仅 llm_failed 条目需人工补判；检验选择配对、退化情形披露、功效、多重比较清单见 REVIEW_SOP.md R4

## 复跑命令

```powershell
python "F:\deepseek\research-kit\review-workflow\scripts\run_review.py" --config "F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\config_v3_online.json"
```