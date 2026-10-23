# 投稿包证据审计报告（R2）

- 投稿包：`F:\Research\_inbox\F1-F5_F45_2026-08-26\TMLR_4p5_Tier123_FINAL_20260827.zip`（12 条目）
- 论文：`F:\Research\F2_Single_10page\paper\main.tex`
- 结论：**CRITICAL**（引用缺失 14/16，路径泄漏 9，声明不符 0/1）

## 1. 论文引用但包内缺失（→ Critical）

- L99: `verify_length_control.py`
- L126: `scripts/fisher_real_likelihood.py`
- L140: `scripts/tier2_refit_c0_K3_holdout.py`
- L267: `results/cells.jsonl`
- L267: `results/analysis.json`
- L267: `scripts/tier2_refit_c0_K3_holdout.py`
- L267: `results/power_analysis.json`
- L267: `figures_f2/tau_sensitivity.pdf`
- L267: `figures_f2/per_model_comparison.pdf`
- L267: `figures_f2/pb_tightness_fisher.pdf`
- L289: `results/analysis.json`
- L343: `power_analysis.json`
- L343: `*.pdf`
- L343: `results/`

## 2. 引用匹配明细

| 引用 | 行 | 状态 | 匹配条目 |
|---|---|---|---|
| `verify_length_control.py` | 99 | MISSING | - |
| `scripts/fisher_real_likelihood.py` | 126 | MISSING | - |
| `results/tier2_refit.json` | 140 | basename | `supplementary/tier2_refit.json` |
| `scripts/tier2_refit_c0_K3_holdout.py` | 140 | MISSING | - |
| `results/cells.jsonl` | 267 | MISSING | - |
| `results/analysis.json` | 267 | MISSING | - |
| `results/tier2_refit.json` | 267 | basename | `supplementary/tier2_refit.json` |
| `scripts/tier2_refit_c0_K3_holdout.py` | 267 | MISSING | - |
| `results/power_analysis.json` | 267 | MISSING | - |
| `figures_f2/tau_sensitivity.pdf` | 267 | MISSING | - |
| `figures_f2/per_model_comparison.pdf` | 267 | MISSING | - |
| `figures_f2/pb_tightness_fisher.pdf` | 267 | MISSING | - |
| `results/analysis.json` | 289 | MISSING | - |
| `power_analysis.json` | 343 | MISSING | - |
| `*.pdf` | 343 | MISSING | - |
| `results/` | 343 | MISSING | - |

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

| 声明原文 | 口径 | 声明值 | zip 实际条目数 | 判定 |
|---|---|---|---|---|
| `7-entry` | manifest_entries | 7 | 12 | ⚠️ 人工核对 |