# PRISM 四维自评报告（v1.3，LLM-as-judge）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`
- RPC：http://127.0.0.1:3080（HTTP 200）
- 结论：**MAJOR** —— 最弱维度 R(严谨性) = 6 分（<= 6）→ 文本层 WARN；证据层门禁不受影响

## 维度评分（总分 = min，不平均）

| 维度 | 分 | 评分理由 | 最大弱点 |
|---|---|---|---|
| **P Pertinence**（契合度） | 8 | 该问题对TMLR读者真实相关:LLM置信度校准直接影响可信AI与部署决策；论文聚焦测量方法、matcher依赖与ECE缺陷,契合venue范围。但定位偏方法学警示,与既有校准文献相比略常规,故8分。 | 与已发表校准工作的关系阐述偏少,问题虽真实但增量更偏警示/测量而非突破,契合中有常规感 |
| **R Rigor**（严谨性） | 6 | 核心实证依赖N=30小样本；标签匹配器经逐行裁决后在相同数据上扩展,且单一审判者/样本内标签使高准确率与低ECE近乎自证。虽作者明确标注illustrative并做Holm校正,但该设计仍是明显可质疑 | 匹配器在评估所用同一批数据上人为扩展,单审判者无独立验证,导致100%准确率/ECE0.0037可能自证 |
| **I Impact**（贡献量） | 6 | 将标签匹配器依赖形式化并提出MSI等诊断工具,跨域600项/4999对数据提供实证与警示,对社区有使用价值；但核心结果多为N=30例示性或探索性,显著性弱,属增量有限但有用的贡献。 | 核心实证来自N=30说明性/探索性样本,跨域显著性弱,贡献规模与证据强度不匹配。 |
| **S Sincerity**（诚实性） | 8 | 文中大量使用 illustrative/exploratory/not evidence 等限定,复现承诺具体,局限披露坦率；但摘要用“We show…determined by the label  | 摘要强断言与 N=30 illustrative 证据强度不完全对齐,易被读成已确证结论 |

**总分（min）= 6**，最弱维度：R(严谨性)

## 依据句（Sincerity 维度优先人工复核）

- P: This practice presupposes that self-reported confidence is a calibrated probability.
- R: in-sample, single judge, near-empty favorable reading; not evidence of calibration
- I: We show measured calibration is determined by the label matcher
- S: We show measured calibration is determined by the label matcher