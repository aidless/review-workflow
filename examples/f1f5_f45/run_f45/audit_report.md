# 投稿包证据审计报告（R2）

- 投稿包：`F:\Research\_inbox\F1-F5_F45_2026-08-26\TMLR_4p5_Tier123_FINAL_20260827.zip`（12 条目）
- 论文：`F:\Research\MERGED_FLAGSHIPS\F45_Merged\paper\main.tex`
- 结论：**CRITICAL**（引用缺失 18/18，路径泄漏 9，声明不符 0/0）

## 1. 论文引用但包内缺失（→ Critical）

- L179: `results/cells.jsonl`
- L179: `gen_figures_f4.py`
- L304: `results/cells.jsonl`
- L306: `results/analysis.json`
- L306: `gen_figures_f4.py`
- L306: `gen_f5_figures_real.py`
- L306: `figures/voting_comparison.pdf`
- L306: `figures/sign_flip.pdf`
- L306: `figures/reliability_voting.pdf`
- L310: `paper/`
- L495: `results/cells.jsonl`
- L495: `results/analysis.json`
- L495: `gen_figures_f4.py`
- L495: `figures/`
- L528: `figures/`
- L528: `results/analysis.json`
- L603: `F:/Research/F4_Single_10page/simulator.py`
- L603: `paper/appendix_Q_sweep.json`

## 2. 引用匹配明细

| 引用 | 行 | 状态 | 匹配条目 |
|---|---|---|---|
| `results/cells.jsonl` | 179 | MISSING | - |
| `gen_figures_f4.py` | 179 | MISSING | - |
| `results/cells.jsonl` | 304 | MISSING | - |
| `results/analysis.json` | 306 | MISSING | - |
| `gen_figures_f4.py` | 306 | MISSING | - |
| `gen_f5_figures_real.py` | 306 | MISSING | - |
| `figures/voting_comparison.pdf` | 306 | MISSING | - |
| `figures/sign_flip.pdf` | 306 | MISSING | - |
| `figures/reliability_voting.pdf` | 306 | MISSING | - |
| `paper/` | 310 | MISSING | - |
| `results/cells.jsonl` | 495 | MISSING | - |
| `results/analysis.json` | 495 | MISSING | - |
| `gen_figures_f4.py` | 495 | MISSING | - |
| `figures/` | 495 | MISSING | - |
| `figures/` | 528 | MISSING | - |
| `results/analysis.json` | 528 | MISSING | - |
| `F:/Research/F4_Single_10page/simulator.py` | 603 | MISSING | - |
| `paper/appendix_Q_sweep.json` | 603 | MISSING | - |

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