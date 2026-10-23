# PRISM 四维自评报告（v1.3，LLM-as-judge）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`
- RPC：http://127.0.0.1:3080（HTTP 200）
- 结论：**MAJOR** —— 最弱维度 I(贡献量) = 5 分（<= 6）→ 文本层 WARN；证据层门禁不受影响

## 维度评分（总分 = min，不平均）

| 维度 | 分 | 评分理由 | 最大弱点 |
|---|---|---|---|
| **P Pertinence**（契合度） | 6 | 主题（LLM自信度校准的测量方法学）与TMLR读者群契合,问题真实存在——matcher依赖性和退化分布下ECE不可靠是有价值的方法论发现。但论文反复以N=30 pilot自居,大量使用'indica | 论文明确将自身框定为'pilot'和'a full study must address'的预备性工作,核心实验仅N=30,难以支撑TMLR级别的完整研究贡献定 |
| **R Rigor**（严谨性） | 6 | 论文展示了统计意识（Holm校正、CI、双重判定）并承认了关键局限（退化性、试点性质）。但核心结论依赖极小样本:N=30试点中27/30置信度值退化,推断力根本不足；'4Ã'和'17Ã'ECE变异 | 核心'4Ã/17Ã'变异结论为点估计比率,CI极宽且Holm校正后仅极端对显著,却被用作主要发现。 |
| **I Impact**（贡献量） | 5 | matcher依赖性和degenerate分布的警示对calibration社区有用,形式化命题(1-3,8')和smECE_sem+MSI estimator有一定方法论价值。但核心发现基于N=30 | N=30 pilot证据基础过薄,关键结论被自我标记为'illustrative''indicative'而非validated,断言的贡献范围与证据强度不匹配 |
| **S Sincerity**（诚实性） | 8 | 全文克制明显:反复标注N=30为illustrative、明确'not a validated bound'、披露CI宽且仅极端对显著、声明'single-turn probe'范围并主动'not c | 虽逐条加hedging,摘要仍以N=30 pilot承载命题1-3/8â²、跨域600项、OOD gating多重断言,断言密度相对证据偏重；且'reprod |

**总分（min）= 5**，最弱维度：I(贡献量)

## 依据句（Sincerity 维度优先人工复核）

- P: We report a measurement methodology study—with an N=30 pilot as an illustrative example…not a validated bound…cautionary findings that a full study must address
- R: point-estimate ratio; 95% CI wide... Holm-corrected domain-pair p-values show only the most extreme pairs are significant
- I: with an N=30 pilot as an illustrative example; initially alarming overconfidence signal...vanishes once semantically-correct answers are recognized (in-sample illustrative, not a validated bound)
- S: 'in-sample illustrative, not a validated bound'; 'indicative, n=30'; 'We do not claim to resolve the orchestration question'; 'suggests a pattern worth further study'; '95% CI wide...only the most ext