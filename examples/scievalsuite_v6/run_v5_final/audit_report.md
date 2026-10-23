# 投稿包证据审计报告（R2）

- 投稿包：`F:\deepseek\papers\scievalsuite\submission\submission_scievalsuite.zip`（92 条目）
- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`
- 结论：**MAJOR**（引用缺失 0/69，路径泄漏 0，声明不符 1/5）

## 1. 论文引用但包内缺失（→ Critical）

- 无

## 2. 引用匹配明细

| 引用 | 行 | 状态 | 匹配条目 |
|---|---|---|---|
| `run.json` | 29 | exact | `run.json` |
| `LITERATURE_REVIEW.md` | 31 | exact | `LITERATURE_REVIEW.md` |
| `run.json` | 33 | exact | `run.json` |
| `run.json` | 66 | exact | `run.json` |
| `analysis.py` | 71 | exact | `results/analysis.py` |
| `report/report.md` | 71 | basename | `workspaces/p5_modelF_l1b_Chemistry_000/report.md` |
| `results/audit_generated_script.py` | 71 | exact | `results/audit_generated_script.py` |
| `results/analysis.py` | 76 | exact | `results/analysis.py` |
| `results/p3_aggregate.py` | 76 | exact | `results/p3_aggregate.py` |
| `results/p3_effects.py` | 76 | exact | `results/p3_effects.py` |
| `p3_recompute.py` | 76 | exact | `results/p3_recompute.py` |
| `evidence_manifest.json` | 82 | exact | `evidence_manifest.json` |
| `_g11_hashcheck.py` | 82 | exact | `_g11_hashcheck.py` |
| `p3_cost.json` | 82 | exact | `results/p3_cost.json` |
| `requirements.txt` | 85 | exact | `paper/requirements.txt`, `requirements.txt` |
| `results/p3_bootstrap.json` | 89 | exact | `results/p3_bootstrap.json` |
| `results/p3_aggregate.py` | 91 | exact | `results/p3_aggregate.py` |
| `results/p3_recompute.py` | 91 | exact | `results/p3_recompute.py` |
| `results/p3_cost.py` | 91 | exact | `results/p3_cost.py` |
| `results/p3_effects.py` | 91 | exact | `results/p3_effects.py` |
| `results/calib_run_l1b.py` | 91 | exact | `results/calib_run_l1b.py` |
| `requirements.txt` | 91 | exact | `paper/requirements.txt`, `requirements.txt` |
| `paper/requirements.txt` | 91 | exact | `paper/requirements.txt` |
| `evidence/protocol.md` | 91 | exact | `evidence/protocol.md` |
| `p3_effects.json` | 108 | exact | `results/p3_effects.json` |
| `results/L2_deepseek-v4-flash.json` | 126 | exact | `results/L2_deepseek-v4-flash.json` |
| `p3_stats_normalized.json` | 132 | exact | `results/p3_stats_normalized.json` |
| `report/report.md` | 155 | basename | `workspaces/p5_modelF_l1b_Chemistry_000/report.md` |
| `report.md` | 155 | exact | `workspaces/p5_modelF_l1b_Chemistry_000/report.md` |
| `workspaces/p5_modelF_l1b_Chemistry_000` | 155 | prefix-dir | `workspaces/p5_modelF_l1b_Chemistry_000/images/fig1_dataset_overview.png`, `workspaces/p5_modelF_l1b_Chemistry_000/images/fig2_fourier_basis.png` |
| `p3_stats_normalized.json` | 158 | exact | `results/p3_stats_normalized.json` |
| `out_p5/P5_MODELF_FINAL.json` | 158 | exact | `out_p5/P5_MODELF_FINAL.json` |
| `p3_recompute.py` | 164 | exact | `results/p3_recompute.py` |
| `results/p3_recompute_checks.json` | 164 | exact | `results/p3_recompute_checks.json` |
| `requirements.txt` | 164 | exact | `paper/requirements.txt`, `requirements.txt` |
| `evidence/protocol.md` | 164 | exact | `evidence/protocol.md` |
| `evidence_manifest.json` | 164 | exact | `evidence_manifest.json` |
| `p3_recompute.py` | 164 | exact | `results/p3_recompute.py` |
| `_g11_hashcheck.py` | 164 | exact | `_g11_hashcheck.py` |
| `out_p5/` | 167 | prefix-dir | `out_p5/compute_curated_friedman.py`, `out_p5/compute_curated_v2.py` |
| `out_p5/P5_L2_8SCENARIOS.json` | 169 | exact | `out_p5/P5_L2_8SCENARIOS.json` |
| `out_p5/JUDGE_40_GOLD.jsonl` | 173 | exact | `out_p5/JUDGE_40_GOLD.jsonl` |
| `out_p5/JUDGE_40_DOUBLE_REPORT.json` | 173 | exact | `out_p5/JUDGE_40_DOUBLE_REPORT.json` |
| `out_p5/FARM_ABLATION.json` | 175 | exact | `out_p5/FARM_ABLATION.json` |
| `out_p5/CROSS_LAYER_ANALYSIS.md` | 175 | exact | `out_p5/CROSS_LAYER_ANALYSIS.md` |
| `FAILURE_TAXONOMY_QUANTIFIED.md` | 175 | exact | `out_p5/FAILURE_TAXONOMY_QUANTIFIED.md` |
| `out_p5/L047_GOLD_30.jsonl` | 177 | exact | `out_p5/L047_GOLD_30.jsonl` |
| `evidence/SCIEVALSUITE_README.md` | 188 | exact | `evidence/SCIEVALSUITE_README.md` |
| `out_p5/` | 216 | prefix-dir | `out_p5/compute_curated_friedman.py`, `out_p5/compute_curated_v2.py` |
| `run.json` | 216 | exact | `run.json` |
| `run.json` | 216 | exact | `run.json` |
| `evidence/protocol.md` | 218 | exact | `evidence/protocol.md` |
| `requirements.txt` | 223 | exact | `paper/requirements.txt`, `requirements.txt` |
| `paper/requirements.txt` | 223 | exact | `paper/requirements.txt` |
| `evidence/protocol.md` | 223 | exact | `evidence/protocol.md` |
| `evidence_manifest.json` | 223 | exact | `evidence_manifest.json` |
| `_g11_hashcheck.py` | 223 | exact | `_g11_hashcheck.py` |
| `evidence_manifest.json` | 226 | exact | `evidence_manifest.json` |
| `results/p3_stats.json` | 226 | exact | `results/p3_stats.json` |
| `results/p3_effects.json` | 226 | exact | `results/p3_effects.json` |
| `results/calib_l1b_v2-numeric-mismatch.json` | 226 | exact | `results/calib_l1b_v2-numeric-mismatch.json` |
| `results/gold_l1b_text.jsonl` | 226 | exact | `results/gold_l1b_text.jsonl` |
| `results/p3_stats_normalized.json` | 226 | exact | `results/p3_stats_normalized.json` |
| `results/p3_bootstrap.json` | 226 | exact | `results/p3_bootstrap.json` |
| `out_p5/P5_MODELF_FINAL.json` | 226 | exact | `out_p5/P5_MODELF_FINAL.json` |
| `out_p5/P5_CURATED_FRIEDMAN_SENSITIVITY.json` | 226 | exact | `out_p5/P5_CURATED_FRIEDMAN_SENSITIVITY.json` |
| `fig_overview.pdf` | 226 | exact | `paper/fig_overview.pdf` |
| `out_p5/compute_friedman_sensitivity.py` | 229 | exact | `out_p5/compute_friedman_sensitivity.py` |
| `out_p5/P5_CURATED_FRIEDMAN_SENSITIVITY.json` | 229 | exact | `out_p5/P5_CURATED_FRIEDMAN_SENSITIVITY.json` |

## 3. Windows 绝对路径泄漏（→ Major，匿名/规范）

- 无

## 4. 封包-磁盘同步检查

- zip 内 tex：`paper/main.tex` —— ❌ DESYNC（zip 内为旧版，磁盘已修订，需重封包）

封包内旧版声明核对（投稿事实口径）：

| 声明原文 | 口径 | 声明值 | zip 实际条目数 | 判定 |
|---|---|---|---|---|
| `92 files` | zip_entries | 92 | 92 | ✅ |
| `91-entry` | manifest_entries | 91 | 92 | ⚠️ 人工核对 |
| `18/18 checks` | recompute_checks | 18 | 92 | ⚠️ 人工核对 |
| `18/18 recompute` | recompute_checks | 18 | 92 | ⚠️ 人工核对 |

## 5. 磁盘版 tex 声明 vs zip 实际

| 声明原文 | 口径 | 声明值 | zip 实际条目数 | 判定 |
|---|---|---|---|---|
| `125 files` | zip_entries | 125 | 92 | ❌ |
| `92 files` | zip_entries | 92 | 92 | ✅ |
| `91-entry` | manifest_entries | 91 | 92 | ⚠️ 人工核对 |
| `18/18 checks` | recompute_checks | 18 | 92 | ⚠️ 人工核对 |
| `18/18 recompute` | recompute_checks | 18 | 92 | ⚠️ 人工核对 |