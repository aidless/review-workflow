# PRISM 四维自评报告（v1.3，LLM-as-judge）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\f1f5_f45\run_f45\extracted_text.txt`
- RPC：http://127.0.0.1:3080（HTTP 200）
- 结论：**MAJOR** —— 最弱维度 R(严谨性) = 5 分（<= 6）→ 文本层 WARN；证据层门禁不受影响

## 维度评分（总分 = min，不平均）

| 维度 | 分 | 评分理由 | 最大弱点 |
|---|---|---|---|
| **P Pertinence**（契合度） | 6 | 研究问题与LLM验证器集成/投票聚合相关,且与已有工作关系清楚；但全部结论限于单一合成参数点且无真实部署,对TMLR读者普遍重要性不足,属边缘契合。 | 仅在N=7、f=2、pH=0.65一个合成场景下给出结论,未在更广参数或真实LLM上验证,契合度受限。 |
| **R Rigor**（严谨性） | 5 | 配对设计与精确McNemar检验合理,且明确将结论限定在单一regime；但F5混合规则在用于评估的同一128K cells上导出,缺少独立验证/预注册说明,存在数据依赖或后验选择风险；单一seed和 | 混合规则F5与结果在同一数据上导出并评估,缺乏独立验证,可能高估hybrid优势。 |
| **I Impact**（贡献量） | 5 | 配对实验否定了“符号翻转”假说并提供可复现负面结果,对验证器聚合设计有一定参考价值；但结论仅基于单一合成参数区间,混合规则未使用新数据,也无真实部署验证,增量有限。 | 核心否定结论仅在N=7、f=2、pH=0.65这一单一合成设置下成立,缺乏参数泛化或真实场景支持,社区级影响不足。 |
| **S Sincerity**（诚实性） | 9 | 全文反复限定“within the studied regime”,明确区分合成与真实LLM,坦承未测试部署,并给出seed/SHA/配对统计,复现承诺可信。仅“never loses”由单次抽样c= | 以16,000次抽样的c=0断言“never loses to majority”,未明确区分样本观测与参数域概率。 |

**总分（min）= 5**，最弱维度：R(严谨性)

## 依据句（Sincerity 维度优先人工复核）

- P: All results are synthetic at a single (N, f, pH); no real LLM deployment is tested.
- R: F5 is the secondary hybrid-joint analysis on the same 128K cells.
- I: falsifies within the studied regime, not a universal non-existence claim
- S: falsifies within the studied regime, not a universal non-existence claim