# PRISM 四维自评报告（v1.3，LLM-as-judge）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`
- RPC：http://127.0.0.1:3080（HTTP 200）
- 结论：**MAJOR** —— 最弱维度 R(严谨性) = 5 分（<= 6）→ 文本层 WARN；证据层门禁不受影响

## 维度评分（总分 = min，不平均）

| 维度 | 分 | 评分理由 | 最大弱点 |
|---|---|---|---|
| **P Pertinence**（契合度） | 8 | 研究问题真实且与 TMLR 读者高度相关:智能体自信度被当作概率用于门控,却很少在自身任务分布上验证校准；与已有过度自信文献关系清楚。但大量 illustrative/exploratory 限定使契 | 论文反复自称 illustrative/exploratory 且关键示例仅 N=30,作为 TMLR 完整研究其问题解决度受质疑。 |
| **R Rigor**（严谨性） | 5 | 核心演示中匹配器经逐行人工裁定后扩展至100%,存在标签同源/循环评估风险；N=30且置信度退化,OOD分析亦为探索性小样本,虽多处声明illustrative,但方法严谨性仍有明显需解释之处。 | 匹配器根据同一批人工裁定标签事后扩展至100%准确率,再用该标签评估ECE,存在循环与过拟合风险。 |
| **I Impact**（贡献量） | 6 | 揭示了标签匹配器决定校准测量、退化分布使 ECE 不稳,并提供形式化与跨域数据,有方法警示价值；但核心是 N=30 illustrative/exploratory 证据,显著性弱,影响限于提醒而非确 | 核心发现依赖自认 illustrative/exploratory 的 N=30 小样本,作者明示非校准证据,削弱贡献强度。 |
| **S Sincerity**（诚实性） | 9 | 多处明确标注 illustrative/exploratory/N=30/not evidence of calibration,并坦白仅极端Holm校正配对显著；复现承诺含adjudication  | 核心pilot仅N=30且依赖单评判者逐行标签裁决,可能限制其测量可复现性的外部效度。 |

**总分（min）= 5**，最弱维度：R(严谨性)

## 依据句（Sincerity 维度优先人工复核）

- P: confidence from language-model agents is treated as usable probability
- R: a matcher extended after per-row adjudication 100% (ECE = 0.0037)
- I: We show measured calibration is determined by the label matcher
- S: near-empty favorable reading; not evidence of calibration