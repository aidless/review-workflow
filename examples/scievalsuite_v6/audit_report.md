# 投稿包证据审计报告（R2）

- 投稿包：`F:\deepseek\papers\scievalsuite\submission\submission_scievalsuite_final_v6.zip`（150 条目）
- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`
- 结论：**CRITICAL**（引用缺失 24/58，路径泄漏 139，声明不符 0/9）

## 1. 论文引用但包内缺失（→ Critical）

- L29: `run.json`
- L33: `run.json`
- L66: `run.json`
- L71: `analysis.py`
- L71: `audit_generated_script.py`
- L76: `papers/agent-comparison/analysis.py`
- L82: `_g11_hashcheck.py`
- L91: `calib_run_l1b.py`
- L91: `data/cache`
- L155: `insufficient_data.png`
- L155: `workspaces/p5_muse_l1b_Chemistry_000`
- L158: `out_p5/P5_MUSE_FINAL.json`
- L164: `_g11_hashcheck.py`
- L167: `out_p5/`
- L169: `out_p5/P5_L2_8SCENARIOS.json`
- L173: `out_p5/JUDGE_40_GOLD.jsonl`
- L173: `out_p5/JUDGE_40_DOUBLE_REPORT.json`
- L175: `out_p5/FARM_ABLATION.json`
- L175: `out_p5/CROSS_LAYER_ANALYSIS.md`
- L175: `FAILURE_TAXONOMY_QUANTIFIED.md`
- L177: `out_p5/L047_GOLD_30.jsonl`
- L221: `data/cache`
- L221: `_g11_hashcheck.py`
- L224: `out_p5/P5_MUSE_FINAL.json`

## 2. 引用匹配明细

| 引用 | 行 | 状态 | 匹配条目 |
|---|---|---|---|
| `run.json` | 29 | MISSING | - |
| `LITERATURE_REVIEW.md` | 31 | exact | `LITERATURE_REVIEW.md` |
| `run.json` | 33 | MISSING | - |
| `run.json` | 66 | MISSING | - |
| `analysis.py` | 71 | MISSING | - |
| `report/report.md` | 71 | basename | `qa_out_final/report.md` |
| `audit_generated_script.py` | 71 | MISSING | - |
| `papers/agent-comparison/analysis.py` | 76 | MISSING | - |
| `scievalsuite/p3_aggregate.py` | 76 | basename | `results/p3_aggregate.py` |
| `p3_effects.py` | 76 | exact | `results/p3_effects.py` |
| `p3_recompute.py` | 76 | exact | `results/p3_recompute.py` |
| `evidence_manifest.json` | 82 | exact | `evidence_manifest.json`, `paper/evidence_manifest.json` |
| `_g11_hashcheck.py` | 82 | MISSING | - |
| `p3_cost.json` | 82 | exact | `results/p3_cost.json` |
| `results/p3_bootstrap.json` | 89 | exact | `results/p3_bootstrap.json` |
| `p3_aggregate.py` | 91 | exact | `results/p3_aggregate.py` |
| `p3_recompute.py` | 91 | exact | `results/p3_recompute.py` |
| `p3_cost.py` | 91 | exact | `results/p3_cost.py` |
| `p3_effects.py` | 91 | exact | `results/p3_effects.py` |
| `calib_run_l1b.py` | 91 | MISSING | - |
| `requirements.txt` | 91 | exact | `paper/requirements.txt`, `requirements.txt` |
| `paper/requirements.txt` | 91 | exact | `paper/requirements.txt` |
| `data/cache` | 91 | MISSING | - |
| `evidence/protocol.md` | 91 | exact | `evidence/protocol.md` |
| `p3_effects.json` | 108 | exact | `results/p3_effects.json` |
| `results/L2_deepseek-v4-flash.json` | 126 | exact | `results/L2_deepseek-v4-flash.json` |
| `p3_stats_normalized.json` | 132 | exact | `results/p3_stats_normalized.json` |
| `report/report.md` | 155 | basename | `qa_out_final/report.md` |
| `report.md` | 155 | exact | `qa_out_final/report.md` |
| `insufficient_data.png` | 155 | MISSING | - |
| `workspaces/p5_muse_l1b_Chemistry_000` | 155 | MISSING | - |
| `p3_stats_normalized.json` | 158 | exact | `results/p3_stats_normalized.json` |
| `out_p5/P5_MUSE_FINAL.json` | 158 | MISSING | - |
| `p3_recompute.py` | 164 | exact | `results/p3_recompute.py` |
| `_g11_hashcheck.py` | 164 | MISSING | - |
| `out_p5/` | 167 | MISSING | - |
| `out_p5/P5_L2_8SCENARIOS.json` | 169 | MISSING | - |
| `out_p5/JUDGE_40_GOLD.jsonl` | 173 | MISSING | - |
| `out_p5/JUDGE_40_DOUBLE_REPORT.json` | 173 | MISSING | - |
| `out_p5/FARM_ABLATION.json` | 175 | MISSING | - |
| `out_p5/CROSS_LAYER_ANALYSIS.md` | 175 | MISSING | - |
| `FAILURE_TAXONOMY_QUANTIFIED.md` | 175 | MISSING | - |
| `out_p5/L047_GOLD_30.jsonl` | 177 | MISSING | - |
| `SCIEVALSUITE_README.md` | 188 | exact | `evidence/SCIEVALSUITE_README.md` |
| `requirements.txt` | 221 | exact | `paper/requirements.txt`, `requirements.txt` |
| `paper/requirements.txt` | 221 | exact | `paper/requirements.txt` |
| `data/cache` | 221 | MISSING | - |
| `evidence/protocol.md` | 221 | exact | `evidence/protocol.md` |
| `_g11_hashcheck.py` | 221 | MISSING | - |
| `evidence_manifest.json` | 224 | exact | `evidence_manifest.json`, `paper/evidence_manifest.json` |
| `results/p3_stats.json` | 224 | exact | `results/p3_stats.json` |
| `results/p3_effects.json` | 224 | exact | `results/p3_effects.json` |
| `results/calib_l1b_v2-numeric-mismatch.json` | 224 | exact | `results/calib_l1b_v2-numeric-mismatch.json` |
| `results/gold_l1b_text.jsonl` | 224 | exact | `results/gold_l1b_text.jsonl` |
| `results/p3_stats_normalized.json` | 224 | exact | `results/p3_stats_normalized.json` |
| `results/p3_bootstrap.json` | 224 | exact | `results/p3_bootstrap.json` |
| `out_p5/P5_MUSE_FINAL.json` | 224 | MISSING | - |
| `fig_overview.pdf` | 224 | exact | `paper/fig_overview.pdf` |

## 3. Windows 绝对路径泄漏（→ Major，匿名/规范）

- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\papers\agent-comparison\analysis.py`
- `evidence/ASSET_MANIFEST.json` LNone: `C:\Users\Administrator\.dsh\.agent-presets\qa-gate\references\AGIKIT评测门方法论.md`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek（本工作区）；E:\AGI-KIT`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\research-kit\eval-contract\`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\study_repos\gaia2-eval-contract\`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\papers\agent-comparison\`
- `evidence/ASSET_MANIFEST.json` LNone: `E:\AGI-KIT\`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\scievalsuite\`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\research-kit\judge-calibration\`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\research-kit\confidence-calibration\`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\research-kit\qa-gate\`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\study_repos\equal-budget-experiment\`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\.agent-memory\sci-agent-eval-significance-2026\P4_EVIDENCE_PACKAGE.md`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\scievalsuite\out_p3\`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\cloud-gpu-setup\（SOP/RUNBOOK/成本日志）；实例`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\research-kit\`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\scievalsuite\out_p3`
- `evidence/ASSET_MANIFEST.json` LNone: `F:\deepseek\research-kit\airs-eval`
- `evidence/ASSET_MANIFEST.json` LNone: `E:\AGI-KIT`
- `evidence/MISSION.md` L95: `F:\deepseek\scievalsuite\`（统一基准正式落盘）——contract_spec.json`
- `evidence/MISSION.md` L98: `F:\deepseek\scievalsuite\out_p3\``
- `evidence/P0_STATUS_REPORT.md` L13: `F:\deepseek\study_repos\SELF_ASSESSMENT_v4.md``
- `evidence/P0_STATUS_REPORT.md` L14: `F:\deepseek\study_repos\NOVELTY_ARGUMENT.md``
- `evidence/P0_STATUS_REPORT.md` L23: `F:\deepseek\research-kit\`（10`
- `evidence/P0_STATUS_REPORT.md` L36: `E:\AGI-KIT\`（正式部署，logs`
- `evidence/P0_STATUS_REPORT.md` L46: `E:\AGI-KIT\eval-contract\`。`
- `evidence/P0_STATUS_REPORT.md` L48: `F:\deepseek\study_repos\`（可执行协议与实验台）`
- `evidence/P0_STATUS_REPORT.md` L53: `C:\Users\Administrator\.dsh\.agent-presets\qa-gate\references\AGIKIT评测门方法论.md`（单一权威源，G041`
- `evidence/P0_STATUS_REPORT.md` L60: `E:\AGI-KIT\logs\`）。`
- `evidence/P0_STATUS_REPORT.md` L110: `E:\AGI-KIT`
- `evidence/P0_STATUS_REPORT.md` L110: `F:\deepseek`
- `evidence/P0_STATUS_REPORT.md` L111: `F:\deepseek`（本工作区），`
- `evidence/P5_COMPLIANCE_REPORT.md` L35: `E:\AGI-KIT\p3_benchmark.py``
- `evidence/P5_COMPLIANCE_REPORT.md` L45: `F:\deepseek\papers\agent-comparison\analysis.py`（文件而非目录）`
- `evidence/P5_COMPLIANCE_REPORT.md` L46: `F:\deepseek\papers\agent-comparison\`；哈希验真`
- `evidence/PHASE_LOG.md` L26: `E:\AGI-KIT`（正式部署，logs`
- `evidence/PHASE_LOG.md` L31: `E:\AGI-KIT`（非`
- `evidence/PHASE_LOG.md` L32: `F:\deepseek，AGI-KIT`
- `evidence/PHASE_LOG.md` L71: `F:\deepseek\scievalsuite\`）：`
- `evidence/PHASE_LOG.md` L81: `E:\learn\ResearchClawBench-main\tasks；4`
- `evidence/PHASE_LOG.md` L141: `F:\deepseek\_repo_survey\airs-bench-main\airs-bench-main`（work_*`
- `evidence/PHASE_LOG.md` L291: `E:\AGI-KIT\p3_benchmark.py``
- `evidence/PHASE_LOG.md` L539: `E:\AGI-KIT\p3_benchmark.py``
- `evidence/SCIEVALSUITE_README.md` L9: `E:\AGI-KIT`、`study_repos``
- `evidence/SCIEVALSUITE_README.md` L35: `E:\AGI-KIT\``
- `evidence/SCIEVALSUITE_README.md` L43: `E:\AGI-KIT）`
- `evidence/SCIEVALSUITE_README.md` L50: `F:\deepseek\study_repos\gaia2-eval-contract\cli.py`
- `evidence/SCIEVALSUITE_README.md` L53: `F:\deepseek\papers\agent-comparison\analysis.py`
- `evidence/SCIEVALSUITE_README.md` L56: `F:\deepseek\research-kit\qa-gate\group_healthcheck.py`
- `evidence_manifest.json` LNone: `F:\deepseek\papers\scievalsuite`

## 4. 封包-磁盘同步检查

- zip 内 tex：`paper/main.tex` —— ❌ DESYNC（zip 内为旧版，磁盘已修订，需重封包）

封包内旧版声明核对（投稿事实口径）：

| 声明原文 | 口径 | 声明值 | zip 实际条目数 | 判定 |
|---|---|---|---|---|
| `144 files` | zip_entries | 144 | 150 | ❌ |
| `46-entry` | manifest_entries | 46 | 150 | ⚠️ 人工核对 |
| `46-entry` | manifest_entries | 46 | 150 | ⚠️ 人工核对 |
| `46-entry` | manifest_entries | 46 | 150 | ⚠️ 人工核对 |
| `46-entry` | manifest_entries | 46 | 150 | ⚠️ 人工核对 |
| `46 SHA-256 hashes` | manifest_hashes | 46 | 150 | ⚠️ 人工核对 |
| `46 hashes` | manifest_hashes | 46 | 150 | ⚠️ 人工核对 |
| `18/18 checks` | recompute_checks | 18 | 150 | ⚠️ 人工核对 |
| `18/18 recompute` | recompute_checks | 18 | 150 | ⚠️ 人工核对 |

## 5. 磁盘版 tex 声明 vs zip 实际

| 声明原文 | 口径 | 声明值 | zip 实际条目数 | 判定 |
|---|---|---|---|---|
| `150 files` | zip_entries | 150 | 150 | ✅ |
| `46-entry` | manifest_entries | 46 | 150 | ⚠️ 人工核对 |
| `46-entry` | manifest_entries | 46 | 150 | ⚠️ 人工核对 |
| `165-entry` | manifest_entries | 165 | 150 | ⚠️ 人工核对 |
| `46-entry` | manifest_entries | 46 | 150 | ⚠️ 人工核对 |
| `46 SHA-256 hashes` | manifest_hashes | 46 | 150 | ⚠️ 人工核对 |
| `46 hashes` | manifest_hashes | 46 | 150 | ⚠️ 人工核对 |
| `18/18 checks` | recompute_checks | 18 | 150 | ⚠️ 人工核对 |
| `18/18 recompute` | recompute_checks | 18 | 150 | ⚠️ 人工核对 |