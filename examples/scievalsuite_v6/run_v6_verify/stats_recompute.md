# 统计复算报告（R4 机械化）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`；扫描 JSON 25 个，识别统计记录 6 条
- 结论：**MAJOR**（MATCH 2，MISMATCH 0，NOT_IN_PAPER 3）

| 类型 | json_path | 重算值 | 产物存储值判定 | 论文出现 | 状态 | 来源 |
|---|---|---|---|---|---|---|
| friedman_p | `cross_model.friedman` | p=0.367879 (chi2=2.0,df=2) | OK | - | **NOT_IN_PAPER** | `p3_stats.json` |
| friedman_p | `friedman_curated` | p=0.049787 (chi2=6.0,df=2) | OK | 0.05 | **MATCH** | `P5_FINAL_FRONTIER_CURATED.json` |
| friedman_p | `friedman_full_P3` | p=0.367879 (chi2=2.0,df=2) | OK | - | **NOT_IN_PAPER** | `P5_FINAL_FRONTIER_CURATED.json` |
| friedman_p | `simulated_k4_N12` | p=0.042054 (chi2=8.2,df=3) | OK | - | **NOT_IN_PAPER** | `P5_FINAL_FRONTIER_CURATED.json` |
| friedman_p | `friedman_L1a_6tasks_k4` | p=0.002584 (chi2=14.25,df=3) | OK | 0.003 | **MATCH** | `P5_MUSE_FINAL.json` |
| friedman_p | `friedman_full_P3_k3_N16` | -（无 df，跳过） | - | - | **SKIP_NO_DF** | `P5_MUSE_FINAL.json` |

- MISMATCH → 逐条人工定性（统计错误 or 产物造假）；NOT_IN_PAPER → 检查论文口径是否换算（如报告的是上界/下界）