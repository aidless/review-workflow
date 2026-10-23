# PRISM 四维自评报告（v1.3，LLM-as-judge）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`
- RPC：http://127.0.0.1:3080（HTTP 200）
- 结论：**MAJOR** —— 最弱维度 I(贡献量) = 4 分（<= 6）→ 文本层 WARN；证据层门禁不受影响

## 维度评分（总分 = min，不平均）

| 维度 | 分 | 评分理由 | 最大弱点 |
|---|---|---|---|
| **P Pertinence**（契合度） | 6 | TMLR明确接受benchmark/measurement类贡献,venue契合度尚可；评测碎片化问题真实存在。但论文几乎所有统计结果为floor效应或不可判定的无效结果（L2 n_d=0不可分析、L | 三层面评测几乎全部出现floor效应或统计无效结果,benchmark作为测量仪器的区分能力未被证明,实际研究价值存疑。 |
| **R Rigor**（严谨性） | 5 | 统计检验选择基本正确（McNemar在n_d=0时正确判为不可用,Friedman用于多模型比较）,且对功效限制透明披露。但N=4严重功效不足,唯一显著结果(p=0.003)来自post-hoc cu | 唯一显著p=0.003来自post-hoc curated subset,属数据挖掘；N=4且judge零调用致校准无效。 |
| **I Impact**（贡献量） | 4 | 该论文将三个已有基准(AIRS-Bench/ResearchClawBench/GAIA2)整合于一个可复现契约下,新增元素为集成协议、L047审计、校准judge等工程性贡献。但实证结果大面积无效: | 三层评估的实证结果几乎全部无效或地板受限,基准在最先进可测模型上未能产生有区分力的发现,削弱了其对社区的实际可用性。 |
| **S Sincerity**（诚实性） | 9 | 论文在诚实性方面表现突出:明确标注exploratory vs confirmatory分析,主动披露统计无效力(McNemar power structurally 0)、地板效应、样本量极小(N= | 校准后的LLM裁判实际零调用(all SKIP),校准仅为方法论担保而非经实战验证,benchmark核心评分组件未被真正行使。 |

**总分（min）= 4**，最弱维度：I(贡献量)

## 依据句（Sincerity 维度优先人工复核）

- P: L1b scored 0/10 for all models (execution failures...); L2 was statistically uninformative: exact McNemar is inapplicable with n_d=0... Cross-model Friedman... was non-significant (p=0.37...floor-limi
- R: a post-hoc curated L1a subset (6 tasks) gives p=0.003 (exploratory, not confirmatory); the round made zero judge calls (all SKIP) so calibration is a methodological warrant
- I: L2 was statistically uninformative... n_d=0 discordant pairs; L1b scored 0/10 for all models (execution failures); Friedman... non-significant (p=0.37; exploratory, floor-limited)
- S: L2 was statistically uninformative: exact McNemar is inapplicable with n_d=0 discordant pairs… the round made zero judge calls (all SKIP) so calibration is a methodological warrant