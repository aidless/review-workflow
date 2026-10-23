# PRISM 四维自评报告（v1.3，LLM-as-judge）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`
- RPC：http://127.0.0.1:3080（HTTP 200）
- 结论：**MAJOR** —— 最弱维度 R(严谨性) = 5 分（<= 6）→ 文本层 WARN；证据层门禁不受影响

## 维度评分（总分 = min，不平均）

| 维度 | 分 | 评分理由 | 最大弱点 |
|---|---|---|---|
| **P Pertinence**（契合度） | 6 | TMLR 接受评测方法论工作,论文强调可复现性与统计协议,venue 契合度尚可。但核心贡献是将 AIRS-Bench、ResearchClawBench、GAIA2 三个已有基准组合到一个统一契约下 | 核心贡献是组合已有基准而非提出新评测方法或新研究发现,且与各组件基准的差异在可见文本中未充分区分。 |
| **R Rigor**（严谨性） | 5 | 统计检验选择得当（exact McNemar、Friedman、Wilcoxon+CLES）,功效限制已诚实披露。但N=4导致L2核心比较功效为0、CI退化[0,0],结果无信息量；L1b校准过的ju | N=4使L2核心比较McNemar功效为0.0000、CI退化[0,0],null结果无信息量却被当结论呈现。 |
| **I Impact**（贡献量） | 5 | 主要贡献是测量工具而非新模型或新任务:将AIRS-Bench、ResearchClawBench、GAIA2三个已有基准统一到一个可复现契约下。复现工程扎实（SHA-256 manifest、重算脚本 | 三个子基准均为已有工作重新封装,实验严重欠功效且结果多为null,未产生可迁移的科学洞察。 |
| **S Sincerity**（诚实性） | 9 | 论文罕见地坦诚:主动报告零结果（L2无统计显著差异,McNemar p=1.0）、完全失败（L1b 0/10全模型）、零效用组件（judge零调用全SKIP）。明确披露功效极限（N=4, McNema | 'simulated second annotator α=0.894'将模拟标注者混入校准证据,虽已声明但仍有夸大校准稳健性之嫌。 |

**总分（min）= 5**，最弱维度：R(严谨性)

## 依据句（Sincerity 维度优先人工复核）

- P: To our knowledge, no prior benchmark jointly reports all three layers under one contract with byte-level reproducible manifests and pre-registered calibrated judges; we state this as a falsifiable gap
- R: $N=4$, $d_{\min}=2.1279$ at 80\% power; McNemar power $0.0000$ at $n_d=4$
- I: L2 showed no statistically detectable difference between arms (exact McNemar p=1.0000, n_d=0<6...N=4); L1b scored 0/10 for all models...the round made zero judge calls (all SKIP)
- S: the round made zero judge calls (all SKIP) so calibration is a methodological warrant