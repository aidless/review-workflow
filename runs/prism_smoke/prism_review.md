# PRISM 四维自评报告（v1.3，LLM-as-judge）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`
- RPC：http://127.0.0.1:3080（HTTP 200）
- 结论：**MAJOR** —— 最弱维度 R(严谨性) = 5 分（<= 6）→ 文本层 WARN；证据层门禁不受影响

## 维度评分（总分 = min，不平均）

| 维度 | 分 | 评分理由 | 最大弱点 |
|---|---|---|---|
| **P Pertinence**（契合度） | 6 | 问题真实（科学智能体评估碎片化）且TMLR接受benchmark类工作,但贡献本质是将现有benchmark（AIRS-Bench/ResearchClawBench/GAIA2）打包到一个contr | 核心结果均为null且模型规模极小（7b-14b）,无法证明该suite具有区分不同方法的能力,削弱了benchmark存在的科学价值。 |
| **R Rigor**（严谨性） | 5 | 统计检验选择基本正确（配对McNemar、Friedman+Nemenyi+CD、Wilson区间）,且透明披露功效局限。但核心L2实验N=4且零不一致对,检验完全无区分力；唯一显著结果（p=0.00 | L2核心对比N=4、n_d=0使McNemar完全无功效；唯一显著的p=0.0026来自事后精选子集与特定编码,存在选择性报告风险。 |
| **I Impact**（贡献量） | 5 | 论文将三个已有基准(AIRS-Bench、GAIA2、ResearchClawBench)整合到统一可复现框架下,作为测量工具有一定实用价值。但实证结果几乎全为null或近零(L1b全0/10,L2臂 | 实证结果以null为主且功效为零(N=4, McNemar power 0.0000),基准产出科学洞察的能力未被证明。 |
| **S Sincerity**（诚实性） | 9 | 论文在断言-证据对齐上表现克制:明确披露统计功效不足（N=4, McNemar power 0.0000）、L2无显著差异、judge零调用、simulated第二标注者、结果对编码方式敏感等局限。复 | calibrated LLM-as-judge实际零调用（all SKIP）,calibration仅为方法论担保而非实证验证,与abstract中'calib |

**总分（min）= 5**，最弱维度：R(严谨性)

## 依据句（Sincerity 维度优先人工复核）

- P: evaluation remains fragmented: prediction benchmarks test single-step code execution, workflow benchmarks test report synthesis, and environment benchmarks test multi-step tool use, each under differe
- R: exact McNemar p=1.0000, n_d=0<6 not-detectable, paired difference 0.0000, 95% CI [0,0] degenerate, N=4; McNemar power 0.0000 at n_d=4
- I: L1b scored 0/10 for all models; McNemar p=1.0000, n_d=0<6; McNemar power 0.0000 at n_d=4
- S: the round made zero judge calls (all SKIP) so calibration is a methodological warrant