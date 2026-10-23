# 审稿工作流运行摘要：scievalsuite_v6_final

- 时间：2026-08-27T05:39:45+00:00
- 论文：`F:/deepseek/papers/scievalsuite/paper/main.tex`
- 投稿包：`F:/deepseek/papers/scievalsuite/submission/submission_scievalsuite.zip`
- 证据目录：`F:/deepseek/papers/scievalsuite/results`, `F:/deepseek/scievalsuite/out_p5`

## 总体门禁：**WARN** | 建议评分：**6/10**（min 维度：{'structure': 8, 'evidence': 6, 'text': 6}）

### 校准后评分：**7.7/10**（无 FAIL 剖面：min(8, 6 + 1.67) = 7.7（accept 侧保守偏移修正，上限 8 = Accept-as-is 映射））

- 排序信号：PRISM R vs yes_rate ρ=0.89（唯一显著维度）；问题数 null（ρ≈0）→ 本次 16 条 stable Critical 不进一步调幅文本维
- 边界：accept 侧单侧校准：TMLR 拒稿不公开，FAIL↔reject 方向无标定；n=6 小样本：偏移量本身有不确定性，calibrated_score 是排序参考而非绝对分；决议两级（7/8）映射，绝对分校准天然粗糙；claims 投票针对投稿版，与终版 PDF 有版本差

证据层无 FAIL；R3 裁决收敛与 R5 人工定性完成后，终审人工给出最终分（suggested_score 是临时下界参考）。

## 阶段表

| 阶段 | 结论 | 门禁 | 关键指标 |
|---|---|---|---|
| R0 | MAJOR | **WARN** | 缺失输入 0，跨源风险目录 1（F:\deepseek\scievalsuite\out_p5 不在 F:\deepseek\papers\scievalsuite 下 → 打包遗漏高风险） |
| R1 | PASS | **PASS** | 章节 8/8，无占位符，摘要 282 词 |
| R1b | PASS | **PASS** | PASS：条目 12，幽灵引用 0，结构 Major 0，ID 不存在 0，标题不符 0（联网核验 11 条） |
| R1c | PASS | **PASS** | PASS：断言 1 句（强 0）；检索 15 条，近重复 0（未引用 0） |
| R1d | PASS | **PASS** | PASS：行内算术 1 处（不符 0，含括号百分数 0）；悬空公式引用 0；符号推导/量纲不在机械覆盖内 |
| R2 | MAJOR | **WARN** | MAJOR：缺引用 0/69，路径泄漏 0，声明不符 1，tex desync True |
| R2b | PASS | **PASS** | PASS：清单 91 条，OK 91，哈希不符 0，缺失 0 |
| R2c | PASS | **PASS** | PASS：图 1 幅（矢量文本 1，位图跳过 0，缺失 0）；图注小数 1 个，无支撑 0；figure_only 0 |
| R2d | PASS | **PASS** | PASS：表 3 个（numeric cell 30），无支撑 0，\input 缺失 0，混精度列 0（INFO） |
| R3 | MAJOR | **WARN** | MAJOR：待复核 1，机械噪音 3，已裁决 70（critical 0）；裁决 MAJOR（mech 0 / llm 0 / noise 0 / supported 0 / critical 0 / llm_failed 1） |
| R4 | MAJOR | **PASS** | MAJOR：统计记录 6 条（MATCH 4，MISMATCH 0，NOT_IN_PAPER 1）——McNemar/Friedman/Wilson 复算；定性 PASS（resolved 1 / sustained 0 / llm_failed 0） |
| R5 | MAJOR | **WARN** | MAJOR：hint 命中 118，可疑 0（一票否决），已披露 8 |
| R6 | MAJOR | **WARN** | 文本层：Critical 16 / Major 17 / Minor 4（3 轮，RPC HTTP 200）；轮间不稳定（噪声候选，不计门禁）：Critical 17 / Major 48 |
| R6b | MAJOR | **WARN** | MAJOR：四维 {'P': 6, 'R': 5, 'I': 5, 'S': 9}（min=5，短板 R(严谨性)）——最弱维度 R(严谨性) = 5 分（<= 6）→ 文本层 WARN；证据层门禁不受影响 |
| R6c | MAJOR | **WARN** | MAJOR：辩论后维持 Critical 10 / Major 4（撤回 1，部分成立 5）；注：原始 37 条中仅严重度前 20 条进入辩论（MAX_ISSUES=20，截断 17 条未辩论） |

## 下一步（人工阶段）

1. **R4 统计定性（已自动化）**：MISMATCH/NOT_IN_PAPER 由口径换算机械层 + LLM 对抗裁决自动定性（stats_adjudications.md）；仅 llm_failed 条目需人工补判；检验选择配对、退化情形披露、功效、多重比较清单见 REVIEW_SOP.md R4
2. **R3 裁决收敛**：1 个待复核数字 → 在 `F:/deepseek/research-kit/review-workflow/examples/scievalsuite_v6/adjudications_v3.json` 填 verdict(noise|supported|critical) 后重跑
3. **R6 收敛**：LLM 意见修复后重跑至一轮无新 Critical/Major；--converge 3 可降轮间噪声
4. **R6b PRISM 复盘**：最弱维度 R(严谨性) = 5 分（P/R/I/S = {'P': 6, 'R': 5, 'I': 5, 'S': 9}），四维证据句见 prism_review.md
5. **R6c 辩论结果**：sustained 条目是作者 rebuttal 后仍成立的问题（修复优先级最高）；withdrawn 为 LLM 单轮假阳性；另有 17 条未进辩论（截断上限 20，见 debate.md 注记）

## 复跑命令

```powershell
python "F:\deepseek\research-kit\review-workflow\scripts\run_review.py" --config "F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\config_v5_final.json"
```