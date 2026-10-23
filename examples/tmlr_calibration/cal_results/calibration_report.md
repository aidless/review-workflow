# 评分校准报告（v2.2）

- 判读日志：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\cal_results\calibrations.json`（6 条，完整配对 6 条）

## 校准指标

- **bias = 1.67**（human − suggested，正 = 系统保守/低估）
- MAE = 1.67
- ⚠ suggested 或 human 为常数（无区分度）——相关性不可计算；PDF-only 模式下 min 维度评分塌缩是已知边界

## 逐条配对

| 论文 | suggested | human | 差 |
|---|---|---|---|
| 3i2ZRk8GDN | 6 | 8 | +2 |
| e0pSqIqwXO | 6 | 8 | +2 |
| cjU3YbcRr8 | 6 | 7 | +1 |
| Nm7dTogzfa | 6 | 8 | +2 |
| TupiNRpgHw | 6 | 8 | +2 |
| JQA0EfQIfj | 6 | 7 | +1 |

## 排序一致性（对照 TMLR claims 投票 yes_rate）

- ⚠ suggested_score vs yes_rate：suggested 为常数（无区分度）——min 维度评分在该模式下塌缩，排序校准不可用；请用 PRISM min 或带证据包的完整跑
- PRISM min vs yes_rate：Spearman ρ=0.853（p=0.0309，n=6）
- PRISM mean vs yes_rate：Spearman ρ=0.875（p=0.0223，n=6）
- PRISM P vs yes_rate：Spearman ρ=-0.261（p=0.6172，n=6）
- PRISM R vs yes_rate：Spearman ρ=0.89（p=0.0175，n=6）
- PRISM I vs yes_rate：Spearman ρ=-0.101（p=0.8498，n=6）
- PRISM S vs yes_rate：Spearman ρ=0.696（p=0.1243，n=6）
- 问题数 stable_C vs yes_rate：Spearman ρ=-0.03（p=0.9552，n=6）
- 问题数 stable_M vs yes_rate：Spearman ρ=0.094（p=0.8597，n=6）
- 问题数 sust_C vs yes_rate：Spearman ρ=-0.029（p=0.9559，n=6）
- 问题数 sust_M vs yes_rate：Spearman ρ=0.0（p=1.0，n=6）

## TMLR 官方审稿数据校准

- 6 条来自 OpenReview API v2（已接收论文；h_decision 映射：
  Accept as is=8 / Accept with minor revision=7）

| 论文 | 决议 | yes_rate | suggested | gate | PRISM P/R/I/S | h_decision |
|---|---|---|---|---|---|---|
| 3i2ZRk8GDN | Accept as is | 1.0 | 6 | WARN | 8/6/7/7 | 8 |
| e0pSqIqwXO | Accept as is | 1.0 | 6 | WARN | 8/7/6/8 | 8 |
| cjU3YbcRr8 | Accept with minor revision | 0.75 | 6 | WARN | 8/6/6/7 | 7 |
| Nm7dTogzfa | Accept as is | 0.667 | 6 | WARN | 7/6/7/7 | 8 |
| TupiNRpgHw | Accept as is | 0.333 | 6 | WARN | 8/5/6/7 | 8 |
| JQA0EfQIfj | Accept with minor revision | 0.333 | 6 | WARN | 9/5/7/6 | 7 |

**边界**：TMLR 拒稿不公开（无法标定 FAIL↔reject 一侧）；AE 决议仅 accept 侧
两级（7/8），绝对分 MAE 天然粗糙；claims 投票针对投稿版，与终版 PDF 存在版本差。
全 accept 样本上的 FAIL 门禁 = 证据层假阳性（对已接收论文误报），须逐条复核。


## 门禁-决策一致性

- 一致率 6/6 = 1.0

| 门禁 | 决策计数 |
|---|---|
| WARN | {'accept': 4, 'weak_accept': 2} |

## 解读纪律

- suggested_score 是**下界参考**（min 维度纪律天然保守），不是点估计
- bias>0 时：人工普遍高于系统——用于工具型论文时在终审上浮 bias 分
- 每新增一条人工终审都应回填本日志，n>=10 后相关性才有参考价值
