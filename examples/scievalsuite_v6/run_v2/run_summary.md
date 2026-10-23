# 审稿工作流运行摘要：scievalsuite_v6

- 时间：2026-08-25T19:17:45+00:00
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
| R2 | CRITICAL | **FAIL** | CRITICAL：缺引用 24/58，路径泄漏 139，声明不符 0，tex desync True |
| R2b | CRITICAL | **FAIL** | CRITICAL：清单 165 条，OK 149，哈希不符 0，缺失 16 |
| R2c | PASS | **PASS** | PASS：图 1 幅（矢量文本 1，位图跳过 0，缺失 0）；图注小数 1 个，无支撑 0；figure_only 0 |
| R3 | MAJOR | **WARN** | MAJOR：待复核 94，机械噪音 5，已裁决 0（critical 0） |
| R4 | MAJOR | **WARN** | MAJOR：统计记录 6 条（MATCH 4，MISMATCH 0，NOT_IN_PAPER 1）——McNemar/Friedman/Wilson 复算 |
| R5 | MAJOR | **WARN** | MAJOR：hint 命中 113，可疑 0（一票否决），已披露 9 |
| R6 | MAJOR | **WARN** | 文本层：Critical 23 / Major 41 / Minor 19（1 轮，RPC HTTP 200） |
| R6b | MAJOR | **WARN** | MAJOR：四维 {'P': 6, 'R': 5, 'I': 5, 'S': 9}（min=5，短板 R(严谨性)）——最弱维度 R(严谨性) = 5 分（<= 6）→ 文本层 WARN；证据层门禁不受影响 |
| R6c | MAJOR | **WARN** | MAJOR：辩论后维持 Critical 15 / Major 0（撤回 0，部分成立 5） |

## 与上一轮对比（F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6）

| 指标 | 旧 | 新 | 趋势 |
|---|---|---|---|
| R2 引用缺失 | 24 | 24 | ＝ |
| R2 路径泄漏 | 139 | 139 | ＝ |
| R2 tex desync | 1 | 1 | ＝ |
| R2b 哈希不符 | 0 | 0 | ＝ |
| R2b 缺失 | 16 | 16 | ＝ |
| R3 裁决 critical | 0 | 0 | ＝ |
| R3 待复核 | 94 | 94 | ＝ |
| R4 统计 MISMATCH | 0 | 0 | ＝ |
| R4 NOT_IN_PAPER | 1 | 1 | ＝ |
| R5 可疑未披露 | 0 | 0 | ＝ |

## 下一步（人工阶段）

1. **R4 统计定性（人工）**：stats_recompute.md 中 MISMATCH/NOT_IN_PAPER 条目逐条定性（统计错误 / 口径换算 / 产物造假）；检验选择配对、退化情形披露、功效、多重比较清单见 REVIEW_SOP.md R4
2. **R1b 联网核验（可选）**：config 设 citation_online=true 复跑，核验 arXiv/DOI 真实性
3. **R3 裁决收敛**：94 个待复核数字 → 在 `F:/deepseek/research-kit/review-workflow/examples/scievalsuite_v6/adjudications.json` 填 verdict(noise|supported|critical) 后重跑
4. **R6 收敛**：LLM 意见修复后重跑至一轮无新 Critical/Major；--converge 3 可降轮间噪声
5. **R6b PRISM 复盘**：最弱维度 R(严谨性) = 5 分（P/R/I/S = {'P': 6, 'R': 5, 'I': 5, 'S': 9}），四维证据句见 prism_review.md
6. **R6c 辩论结果**：sustained 条目是作者 rebuttal 后仍成立的问题（修复优先级最高）；withdrawn 为 LLM 单轮假阳性

## 复跑命令

```powershell
python "F:\deepseek\research-kit\review-workflow\scripts\run_review.py" --config "F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\config_v2.json"
```