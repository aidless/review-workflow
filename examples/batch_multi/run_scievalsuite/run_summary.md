# 审稿工作流运行摘要：scievalsuite_v6

- 时间：2026-08-26T04:39:41+00:00
- 论文：`F:/deepseek/papers/scievalsuite/paper/main.tex`
- 投稿包：`F:/deepseek/papers/scievalsuite/submission/submission_scievalsuite_final_v6.zip`
- 证据目录：`F:/deepseek/papers/scievalsuite/results`, `F:/deepseek/scievalsuite/out_p5`

## 总体门禁：**FAIL** | 建议评分：**4/10**（min 维度：{'structure': 6, 'evidence': 4, 'text': 6}）

证据层存在 FAIL → 按评分纪律 cap 4；先修 FAIL 项再进入文本层评审。

## 阶段表

| 阶段 | 结论 | 门禁 | 关键指标 |
|---|---|---|---|
| R0 | MAJOR | **WARN** | 缺失输入 0，跨源风险目录 1（F:\deepseek\scievalsuite\out_p5 不在 F:\deepseek\papers\scievalsuite 下 → 打包遗漏高风险） |
| R1 | MAJOR | **WARN** | 摘要 358 词（>300） |
| R1b | PASS | **PASS** | PASS：条目 12，幽灵引用 0，结构 Major 0（offline 结构检查） |
| R1c | PASS | **PASS** | PASS：断言 1 句（强 0）；检索 15 条，近重复 0（未引用 0） |
| R1d | PASS | **PASS** | PASS：行内算术 1 处（不符 0，含括号百分数 0）；悬空公式引用 0；符号推导/量纲不在机械覆盖内 |
| R2 | CRITICAL | **FAIL** | CRITICAL：缺引用 24/58，路径泄漏 139，声明不符 0，tex desync True |
| R2b | CRITICAL | **FAIL** | CRITICAL：清单 165 条，OK 149，哈希不符 0，缺失 16 |
| R2c | PASS | **PASS** | PASS：图 1 幅（矢量文本 1，位图跳过 0，缺失 0）；图注小数 1 个，无支撑 0；figure_only 0 |
| R2d | PASS | **PASS** | PASS：表 3 个（numeric cell 30），无支撑 0，\input 缺失 0，混精度列 0（INFO） |
| R3 | MAJOR | **WARN** | MAJOR：待复核 94，机械噪音 5，已裁决 0（critical 0） |
| R4 | MAJOR | **WARN** | MAJOR：统计记录 6 条（MATCH 4，MISMATCH 0，NOT_IN_PAPER 1）——McNemar/Friedman/Wilson 复算 |
| R5 | MAJOR | **WARN** | MAJOR：hint 命中 113，可疑 0（一票否决），已披露 9 |
| R6 | - | **SKIP** | LLM 审查未启用（--skip-llm 或 llm.enabled=false） |
| R6b | - | **SKIP** | PRISM 未启用（--skip-llm 或 llm.enabled=false） |
| R6c | - | **SKIP** | 辩论未启用（--skip-llm 或 llm.enabled=false） |

## 下一步（人工阶段）

1. **R4 统计定性（人工）**：stats_recompute.md 中 MISMATCH/NOT_IN_PAPER 条目逐条定性（统计错误 / 口径换算 / 产物造假）；检验选择配对、退化情形披露、功效、多重比较清单见 REVIEW_SOP.md R4
2. **R1b 联网核验（可选）**：config 设 citation_online=true 复跑，核验 arXiv/DOI 真实性
3. **R3 裁决收敛**：94 个待复核数字 → 在 `None` 填 verdict(noise|supported|critical) 后重跑

## 复跑命令

```powershell
python "F:\deepseek\research-kit\review-workflow\scripts\run_review.py" --config "F:\deepseek\research-kit\review-workflow\examples\batch_multi\paper1_scievalsuite.json"
```