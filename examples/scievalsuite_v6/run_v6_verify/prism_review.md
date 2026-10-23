# PRISM 四维自评报告（v1.3，LLM-as-judge）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`
- RPC：http://127.0.0.1:3080（HTTP 200）
- 结论：**MAJOR** —— 最弱维度 I(贡献量) = 5 分（<= 6）→ 文本层 WARN；证据层门禁不受影响

## 维度评分（总分 = min，不平均）

| 维度 | 分 | 评分理由 | 最大弱点 |
|---|---|---|---|
| **P Pertinence**（契合度） | 6 | 问题真实（科学智能体评估碎片化）,TMLR接受benchmark/评估方法学论文,venue契合度尚可。但实证结果大面积为零或统计无信息量（L2统计无效、L1b全0）,使得基准本身能否有效回答所提研究 | 三层数据大面积null或全零,基准未能证明自身可区分模型能力,研究问题的实际可解决性存疑。 |
| **R Rigor**（严谨性） | 6 | 统计检验选择基本正确（配对McNemar、跨模型Friedman）,透明披露功效限制并标注探索性分析。但含10个全零任务的Friedman检验、post-hoc curated子集(p=0.003)及 | post-hoc curated L1a子集得p=0.003存在cherry-picking风险,且Friedman纳入10个全零任务降低有效辨别力。 |
| **I Impact**（贡献量） | 5 | 论文的核心贡献是一个集成复现框架（run.json契约、SHA-256重算、答案拟合审计）,而非新任务或新模型——三层均复用已有基准（AIRS-Bench、ResearchClawBench、GAIA | 复用已有任务且大部分结果为null/floor效应（L2 N=4无差异、L1b全0、judge零调用）,基准的区分能力基本未被验证。 |
| **S Sincerity**（诚实性） | 9 | 摘要异常克制:L2 明确称 'statistically uninformative',post-hoc 结果标注 'exploratory, not confirmatory',功效限制（N=4,  | 校准过的 LLM-as-judge 通过 FNR/FPR 门但实际零调用（all SKIP）,使校准担保在实践中形同虚设,虽已披露但仍放大了方法严谨性的外观。 |

**总分（min）= 5**，最弱维度：I(贡献量)

## 依据句（Sincerity 维度优先人工复核）

- P: L2 was statistically uninformative…L1b scored 0/10 for all models (execution failures, not judge scores)…The contribution is not a new model but a measurement instrument
- R: with 10 all-zero L1b tasks...post-hoc curated L1a subset (6 tasks) gives p=0.003 (exploratory, not confirmatory)
- I: L1b scored 0/10 for all models (execution failures, not judge scores)
- S: L2 was statistically uninformative: exact McNemar could not detect any arm difference (p=1.00, n_d=0<6, N=4)