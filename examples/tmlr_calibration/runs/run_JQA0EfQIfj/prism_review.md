# PRISM 四维自评报告（v1.3，LLM-as-judge）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_JQA0EfQIfj\extracted_text.txt`
- RPC：http://127.0.0.1:3080（HTTP 200）
- 结论：**MAJOR** —— 最弱维度 R(严谨性) = 5 分（<= 6）→ 文本层 WARN；证据层门禁不受影响

## 维度评分（总分 = min，不平均）

| 维度 | 分 | 评分理由 | 最大弱点 |
|---|---|---|---|
| **P Pertinence**（契合度） | 9 | 问题真实且重要:WiFi-CSI运动预测是新兴且有实际意义的研究方向,隐私保护、无视线约束的感知需求明确。与已发表CSI姿态估计工作关系清晰,准确指出其仅做瞬时回归、未建模时序动力学的空白。Koopm | 问题虽真实,但建立在尚不成熟的CSI姿态估计基础上,下游预测任务的基准与评测体系仍在早期,可能被质疑问题成熟度。 |
| **R Rigor**（严谨性） | 5 | 可见片段（摘要+引言）中方法论框架（Koopman提升、残差算子、anchor-delta头）概念上合理,但缺乏任何统计检验、多重比较校正、seed管理或消融设计的描述。性能声称（'substanti | 声称'outperforming all baselines by a substantial margin'但无统计显著性检验、seed方差或消融对照的可见证 |
| **I Impact**（贡献量） | 7 | 首次将WiFi-CSI从瞬时姿态估计扩展到多时程运动预测,问题 formulation 本身具有新能力价值；Koopman 潜空间线性化、anchor-delta 头、KAL loss 组合构成针对  | 'outperforming all baselines by a substantial margin'的断言缺乏可见的量化证据支撑,贡献大小与证据匹配度存疑 |
| **S Sincerity**（诚实性） | 6 | 摘要中存在多处措辞偏强的断言,如âsubstantial marginââall baselinesââthe first unified frameworkâ,但本片段未提供 | âoutperforming all baselines by a substantial marginâ缺乏可见量化证据,属断言超出证据。 |

**总分（min）= 5**，最弱维度：R(严谨性)

## 依据句（Sincerity 维度优先人工复核）

- P: Modeling forward temporal dynamics, predicting where a person will be rather than where they are, remains largely unexplored. ... the first unified framework for WiFi-CSI-based human motion prediction
- R: KOALA achieves robust, consistent performance across both short- and long-term prediction horizons, outperforming all baselines by a substantial margin.
- I: KOALA, the first unified framework for WiFi-CSI-based human motion prediction... outperforming all baselines by a substantial margin.
- S: KOALA achieves robust, consistent performance across both short- and long-term prediction horizons, outperforming all baselines by a substantial margin.