# PRISM 四维自评报告（v1.3，LLM-as-judge）

- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`
- RPC：http://127.0.0.1:3080（HTTP 200）
- 结论：**MAJOR** —— 最弱维度 R(严谨性) = 6 分（<= 6）→ 文本层 WARN；证据层门禁不受影响

## 维度评分（总分 = min，不平均）

| 维度 | 分 | 评分理由 | 最大弱点 |
|---|---|---|---|
| **P Pertinence**（契合度） | 8 | 问题真实且重要:LLM 智能体置信度校准与部署门控高度契合 TMLR 可信 ML 方向,与已有工作的关系也基本清楚。但核心实证仅为 N=30 的 in-sample 演示,作为 TMLR 论文的分量偏 | 核心结论高度依赖 N=30 的 in-sample/circular 演示,作为 TMLR 主体证据分量不足。 |
| **R Rigor**（严谨性） | 6 | 作者清楚标注N=30 pilot为in-sample且匹配器按行裁定存在循环性,并对ECE退化和CI宽有说明；更大MMLU数据与Holm校正提供部分外部效度,但核心示范结论仍受小样本和循环验证影响,需 | N=30行内样本、按行裁定后回填匹配器得到100%准确率,循环验证且无held-out界,削弱核心示范结论 |
| **I Impact**（贡献量） | 6 | 提出 matcher 依赖校准的理论刻画、binning-free 估计器和跨域数据集,对测量实践有警示与参考价值；但核心演示仅N=30且在样本内循环,跨域显著差异仅限极端情形,增量有限而有用。 | 核心结论证据规模过小:N=30、in-sample、裁决后100%校准结果循环论证,难以支撑扎实的社区影响。 |
| **S Sincerity**（诚实性） | 9 | 多次明确标注in-sample/circular/exploratory/not evidence of calibration,坦承N=30、退化分布与ECE局限,复现承诺具体；唯一瑕疵是代码数据入 | 复现承诺依赖附录/evidence package,片段内未展示可独立验证的数据或代码入口,需依赖后续核查。 |

**总分（min）= 6**，最弱维度：R(严谨性)

## 依据句（Sincerity 维度优先人工复核）

- P: in-sample on 30 rows, circular, 95% CI [88.4%,100%], not a held-out bound
- R: in-sample on 30 rows, circular
- I: in-sample on 30 rows, circular, 95% CI [88.4%,100%], not a held-out bound
- S: in-sample on 30 rows, circular, 95% CI [88.4%,100%], not a held-out bound