# PRISM 四维自评报告（v1.3，LLM-as-judge）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f2\extracted_text.txt`
- RPC：http://127.0.0.1:3080（HTTP 200）
- 结论：**MAJOR** —— 最弱维度 R(严谨性) = 4 分（<= 6）→ 文本层 WARN；证据层门禁不受影响

## 维度评分（总分 = min，不平均）

| 维度 | 分 | 评分理由 | 最大弱点 |
|---|---|---|---|
| **P Pertinence**（契合度） | 6 | 主题契合LM智能体可靠性/选择性预测,与已有工作关系清楚；但核心贡献仅是对局部模型的小样本经验描述,且自认界限松散,问题真实但贡献偏常规,契合度属边缘。 | 论文自认仅样本描述性构造且界限松散,缺乏对该领域读者有普遍价值的可推广结论。 |
| **R Rigor**（严谨性） | 4 | 核心经验下界在K=3 pilot拟合后用于同一2,700 cells报告“超过B”,缺乏独立验证；ρ仅点估计,Wilson CI用于改进量/避免退化也有方法错配。作者虽有样本描述性声明,仍属实质缺陷。 | c0在K=3 pilot拟合后,用同一2,700 cells验证“全部超过B”,属样本内验证,不能确证下界。 |
| **I Impact**（贡献量） | 4 | 论文提供了K-verifier选择性预测的初步形式化与2700格经验刻画,但核心下界是样本描述性且宽松,泛化性受限于四个本地模型；属于有限但有参考价值的增量,而非扎实新能力或社区级贡献。 | 核心经验下界B是样本描述性构造且P/B达5–10×,宽松到不能支撑其声称的刻画价值。 |
| **S Sincerity**（诚实性） | 8 | 多处明确声明结果仅样本描述、非定理,并自述下界宽松与适用范围有限,CI/SD处理也较克制；但复现承诺依赖内部行号/ledger,未见可独立验证的数据或代码,且紧度比表述略有含混,故非满分。 | 复现承诺主要靠内部附录行号与彩色ledger,缺少可公开获取的数据/代码,可验证性不足。 |

**总分（min）= 4**，最弱维度：R(严谨性)

## 依据句（Sincerity 维度优先人工复核）

- P: This is explicitly a sample-descriptive construction, not a derived theorem.
- R: c0 = 0.05 fitted on K=3 pilot data
- I: The construction is loose (P/B 5–10×, median 10.88× after expansion)
- S: Gates 9/9 checklist items are anchored to L401–L409