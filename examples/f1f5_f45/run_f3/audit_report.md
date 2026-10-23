# 投稿包证据审计报告（R2）

- 投稿包：`F:\Research\_inbox\F1-F5_F45_2026-08-26\TMLR_4p5_Tier123_FINAL_20260827.zip`（12 条目）
- 论文：`F:\Research\F3_Single_10page\paper\main.tex`
- 结论：**CRITICAL**（引用缺失 21/27，路径泄漏 9，声明不符 0/0）

## 1. 论文引用但包内缺失（→ Critical）

- L121: `results/power_analysis.json`
- L180: `cloud_experiment_design.md`
- L219: `figures_f3/gen_figures.py`
- L219: `results/analysis.json`
- L288: `results/cells.jsonl`
- L288: `results/analysis.json`
- L288: `results/power_analysis.json`
- L288: `results/F3_fixed_correctness_results.json`
- L288: `scripts/F3_Tier2_hierarchical_token_ablation.py`
- L288: `scripts/F3_fixed_correctness_recompute.py`
- L288: `paper/figures_f3/`
- L288: `gen_figures.py`
- L308: `scripts/F3_fixed_correctness_recompute.py`
- L308: `results/cells.jsonl`
- L308: `F3_ERRATUM.md`
- L310: `results/power_analysis.json`
- L311: `power_analysis.json`
- L326: `results/cells.jsonl`
- L326: `results/F3_fixed_correctness_results.json`
- L326: `scripts/F3_fixed_correctness_recompute.py`
- L326: `paper/figures_f3/gen_figures.py`

## 2. 引用匹配明细

| 引用 | 行 | 状态 | 匹配条目 |
|---|---|---|---|
| `results/F3_Tier2_results.json` | 118 | basename | `supplementary/F3_Tier2_results.json` |
| `results/power_analysis.json` | 121 | MISSING | - |
| `results/F3_Tier2_results.json` | 158 | basename | `supplementary/F3_Tier2_results.json` |
| `cloud_experiment_design.md` | 180 | MISSING | - |
| `results/F3_Tier2_results.json` | 203 | basename | `supplementary/F3_Tier2_results.json` |
| `figures_f3/gen_figures.py` | 219 | MISSING | - |
| `results/analysis.json` | 219 | MISSING | - |
| `results/cells.jsonl` | 288 | MISSING | - |
| `results/analysis.json` | 288 | MISSING | - |
| `results/power_analysis.json` | 288 | MISSING | - |
| `results/F3_Tier2_results.json` | 288 | basename | `supplementary/F3_Tier2_results.json` |
| `results/F3_fixed_correctness_results.json` | 288 | MISSING | - |
| `scripts/F3_Tier2_hierarchical_token_ablation.py` | 288 | MISSING | - |
| `scripts/F3_fixed_correctness_recompute.py` | 288 | MISSING | - |
| `paper/figures_f3/` | 288 | MISSING | - |
| `gen_figures.py` | 288 | MISSING | - |
| `scripts/F3_fixed_correctness_recompute.py` | 308 | MISSING | - |
| `results/cells.jsonl` | 308 | MISSING | - |
| `F3_ERRATUM.md` | 308 | MISSING | - |
| `results/F3_Tier2_results.json` | 309 | basename | `supplementary/F3_Tier2_results.json` |
| `results/power_analysis.json` | 310 | MISSING | - |
| `power_analysis.json` | 311 | MISSING | - |
| `results/cells.jsonl` | 326 | MISSING | - |
| `results/F3_Tier2_results.json` | 326 | basename | `supplementary/F3_Tier2_results.json` |
| `results/F3_fixed_correctness_results.json` | 326 | MISSING | - |
| `scripts/F3_fixed_correctness_recompute.py` | 326 | MISSING | - |
| `paper/figures_f3/gen_figures.py` | 326 | MISSING | - |

## 3. Windows 绝对路径泄漏（→ Major，匿名/规范）

- `supplementary/F3_Tier2_results.json` LNone: `F:\Research\F3_Single_10page`
- `supplementary/F3_Tier2_results.json` LNone: `F:\Research\F1_Single_10page`
- `supplementary/F3_Tier2_results.json` LNone: `F:\Research\F1_Single_10page`
- `supplementary/F3_Tier2_results.json` LNone: `F:\Research\F4_Single_10page`
- `supplementary/F3_Tier2_results.json` LNone: `F:\Research\F4_Single_10page`
- `supplementary/F3_Tier2_results.json` LNone: `F:\Research\F2_Single_10page`
- `supplementary/F3_Tier2_results.json` LNone: `F:\Research\F2_Single_10page`
- `supplementary/tier2_phrasing_results.json` LNone: `F:\Research\F1_Single_10page`
- `supplementary/tier2_phrasing_results.json` LNone: `F:\Research\F1_Single_10page`

## 4. 封包-磁盘同步检查

- zip 内未找到与磁盘同名的 tex（跳过同步检查）

## 5. 磁盘版 tex 声明 vs zip 实际

- 论文未出现可解析的文件数声明