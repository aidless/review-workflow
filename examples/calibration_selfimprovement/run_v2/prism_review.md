# PRISM 四维自评报告（v1.3，LLM-as-judge）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`
- RPC：http://127.0.0.1:3080（HTTP 200）
- 结论：**MAJOR** —— 最弱维度 R(严谨性) = 6 分（<= 6）→ 文本层 WARN；证据层门禁不受影响

## 维度评分（总分 = min，不平均）

| 维度 | 分 | 评分理由 | 最大弱点 |
|---|---|---|---|
| **P Pertinence**（契合度） | 7 | 研究问题真实且重要:LLM agent 自报置信度被广泛用于 deferral/memory-gating,但校准 rarely validated,且 label matcher 影响测量结果这一方 | 核心研究以 N=30 pilot 为主,作为 TMLR 完整研究的方法论说服力偏弱,即便有 600-item 扩展仍以 pilot 定性。 |
| **R Rigor**（严谨性） | 6 | 方法学框架有合理之处:使用Holm校正多重比较、报告95%CI、形式化命题给出测量偏差界、双judge标注。但核心结论依赖N=30且分布退化（27/30=1.0）,统计功效严重不足；4×/17×ECE | N=30且置信度退化（27/30=1.0）使核心校准测量统计功效极低,点估计比与OOD结论均缺乏稳健支撑。 |
| **I Impact**（贡献量） | 6 | 贡献包含matcher依赖性的形式化（命题1-3）、smECE_sem+MSI估计器、退化分布下分箱不可靠的警示、以及600项×9模型跨域普查。这些对社区有方法论和警示价值。但核心证据基于N=30试点 | 几乎所有关键结论建立在N=30试点上且反复自述为'indicative/proof-of-concept',不足以支撑论文声称的部署级指导影响力。 |
| **S Sincerity**（诚实性） | 9 | 论文全程克制标注局限:pilot、N=30、in-sample illustrative、not a validated bound、indicative 等限定词密集出现；明确声明不解决编排问题、s | "self-reported confidence appears useless—even harmful"措辞偏强,虽以 n=30 与 suggests 对 |

**总分（min）= 6**，最弱维度：R(严谨性)

## 依据句（Sincerity 维度优先人工复核）

- P: with an N=30 pilot as an illustrative example...calibration of self-reported confidence is rarely validated on the agent's own task distribution before use in deferral or memory-gating decisions
- R: 27 of 30 values are exactly 1.0…binning-based ECE is unreliable; point-estimate ratio; 95% CI wide…Holm-corrected…only the most extreme pairs are significant; indicative, n=30
- I: We report a measurement methodology study—with an N=30 pilot as an illustrative example…in-sample illustrative, not a validated bound…a pattern worth further study…indicative, n=30
- S: in-sample illustrative, not a validated bound;…indicative, n=30…We do not claim to resolve the orchestration question