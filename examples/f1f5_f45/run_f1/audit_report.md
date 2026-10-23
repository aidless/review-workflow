# 投稿包证据审计报告（R2）

- 投稿包：`F:\Research\_inbox\F1-F5_F45_2026-08-26\TMLR_4p5_Tier123_FINAL_20260827.zip`（12 条目）
- 论文：`F:\Research\F1_Single_10page\paper\main.tex`
- 结论：**CRITICAL**（引用缺失 16/16，路径泄漏 9，声明不符 1/1）

## 1. 论文引用但包内缺失（→ Critical）

- L56: `cover_letter_F4_F5.md`
- L91: `verify_length_control.py`
- L168: `power_analysis.json`
- L190: `generate_figures.py`
- L192: `results/cells.jsonl`
- L192: `results/analysis.json`
- L192: `results/power_analysis.json`
- L192: `paper/figures_f1/*.pdf`
- L192: `paper/figures_f1/generate_figures.py`
- L243: `power_analysis.json`
- L243: `paper/figures_f1/*.pdf`
- L243: `paper/figures_f1/generate_figures.py`
- L245: `verify_length_control.py`
- L245: `patch_policy_key_numbers.json`
- L245: `_audit_recompute.json`
- L245: `./models/all-MiniLM`

## 2. 引用匹配明细

| 引用 | 行 | 状态 | 匹配条目 |
|---|---|---|---|
| `cover_letter_F4_F5.md` | 56 | MISSING | - |
| `verify_length_control.py` | 91 | MISSING | - |
| `power_analysis.json` | 168 | MISSING | - |
| `generate_figures.py` | 190 | MISSING | - |
| `results/cells.jsonl` | 192 | MISSING | - |
| `results/analysis.json` | 192 | MISSING | - |
| `results/power_analysis.json` | 192 | MISSING | - |
| `paper/figures_f1/*.pdf` | 192 | MISSING | - |
| `paper/figures_f1/generate_figures.py` | 192 | MISSING | - |
| `power_analysis.json` | 243 | MISSING | - |
| `paper/figures_f1/*.pdf` | 243 | MISSING | - |
| `paper/figures_f1/generate_figures.py` | 243 | MISSING | - |
| `verify_length_control.py` | 245 | MISSING | - |
| `patch_policy_key_numbers.json` | 245 | MISSING | - |
| `_audit_recompute.json` | 245 | MISSING | - |
| `./models/all-MiniLM` | 245 | MISSING | - |

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
| `396 files` | zip_entries | 396 | 12 | ❌ |