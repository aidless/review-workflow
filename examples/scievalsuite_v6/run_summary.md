# 审稿工作流运行摘要：scievalsuite_v6

- 时间：2026-08-25T17:49:39+00:00
- 论文：`F:/deepseek/papers/scievalsuite/paper/main.tex`
- 投稿包：`F:/deepseek/papers/scievalsuite/submission/submission_scievalsuite_final_v6.zip`
- 证据目录：`F:/deepseek/papers/scievalsuite/results`, `F:/deepseek/scievalsuite/out_p5`

## 总体门禁：**FAIL**

证据层存在 FAIL → 按 R7 评分纪律 cap 4（min 维度）；先修 FAIL 项再进入文本层评审。

## 阶段表

| 阶段 | 结论 | 门禁 | 关键指标 |
|---|---|---|---|
| R0 | MAJOR | **WARN** | 缺失输入 0，跨源风险目录 1（F:\deepseek\scievalsuite\out_p5 不在 F:\deepseek\papers\scievalsuite 下 → 打包遗漏高风险） |
| R1 | MAJOR | **WARN** | 摘要 358 词（>300） |
| R2 | CRITICAL | **FAIL** | CRITICAL：缺引用 24/58，路径泄漏 139，声明不符 0，tex desync True |
| R2b | CRITICAL | **FAIL** | CRITICAL：清单 165 条，OK 149，哈希不符 0，缺失 16 |
| R3 | MAJOR | **WARN** | MAJOR：待复核 94，机械噪音 5，已裁决 0（critical 0） |
| R5 | MAJOR | **WARN** | MAJOR：hint 命中 113，可疑 0（一票否决），已披露 9 |
| R6 | MAJOR | **WARN** | 文本层：Critical 18 / Major 42 / Minor 19（RPC HTTP 200） |

## 下一步（人工阶段）

1. **R4 统计审查（人工）**：检验选择配对、退化情形披露、功效、多重比较、forking paths —— 清单见 REVIEW_SOP.md R4
2. **R3 裁决收敛**：94 个待复核数字 → 在 `F:/deepseek/research-kit/review-workflow/examples/scievalsuite_v6/adjudications.json` 填 verdict(noise|supported|critical) 后重跑
3. **R6 收敛**：LLM 意见修复后用 review_loop.py 复审至一轮无新 Critical/Major

## 复跑命令

```powershell
python "F:\deepseek\research-kit\review-workflow\scripts\run_review.py" --config "F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\config.json"
```