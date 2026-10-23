# 投稿包证据审计报告（R2）

- 投稿包：`F:\deepseek\papers\calibration-self-improvement\submission_clean_20260827.zip`（362 条目）
- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`
- 结论：**CRITICAL**（引用缺失 2/43，路径泄漏 47，声明不符 0/0）

## 1. 论文引用但包内缺失（→ Critical）

- L1229: `census_sig600/`
- L1855: `results/verified/`

## 2. 引用匹配明细

| 引用 | 行 | 状态 | 匹配条目 |
|---|---|---|---|
| `label_adjudication.json` | 363 | exact | `evidence/label_adjudication.json` |
| `dual_judge_adjudication.json` | 371 | exact | `evidence/dual_judge_adjudication.json` |
| `theory/` | 700 | prefix-dir | `theory/estimator_design.md`, `theory/msi.py` |
| `multi_model/matcher_vs_judge.json` | 785 | exact | `evidence/multi_model/matcher_vs_judge.json` |
| `multi_model/per_source_judge_agreement.json` | 817 | exact | `evidence/multi_model/per_source_judge_agreement.json` |
| `multi_model/three_judge_analysis.json` | 857 | exact | `evidence/multi_model/three_judge_analysis.json` |
| `multi_model/flip_audit_list.json` | 870 | exact | `evidence/multi_model/flip_audit_list.json` |
| `multi_model/flip_audit_results.json` | 871 | exact | `evidence/multi_model/flip_audit_results.json` |
| `multi_model/consensus_ece_result.json` | 901 | exact | `evidence/multi_model/consensus_ece_result.json` |
| `flip_audit_list.json` | 902 | exact | `evidence/multi_model/flip_audit_list.json` |
| `multi_model/consensus_ece_result.json` | 918 | exact | `evidence/multi_model/consensus_ece_result.json` |
| `census_sig600/` | 1229 | MISSING | - |
| `evidence/confidence.jsonl` | 1807 | exact | `evidence/confidence.jsonl` |
| `recompute_analysis.py` | 1813 | exact | `scripts/recompute_analysis.py` |
| `confidence_pilot.jsonl` | 1813 | exact | `evidence/confidence_pilot.jsonl` |
| `evidence/confidence_pilot.jsonl` | 1814 | exact | `evidence/confidence_pilot.jsonl` |
| `evidence/label_adjudication.json` | 1816 | exact | `evidence/label_adjudication.json` |
| `evidence/analysis_summary.json` | 1818 | exact | `evidence/analysis_summary.json` |
| `evidence/three_arm_result.json` | 1821 | exact | `evidence/three_arm_result.json` |
| `scripts/collect_pilot_data.py` | 1824 | exact | `scripts/collect_pilot_data.py` |
| `scripts/label_match.py` | 1825 | exact | `scripts/label_match.py` |
| `scripts/adjudicate_labels.py` | 1826 | exact | `scripts/adjudicate_labels.py` |
| `scripts/verify_labels.py` | 1826 | exact | `scripts/verify_labels.py` |
| `scripts/recompute_analysis.py` | 1828 | exact | `scripts/recompute_analysis.py` |
| `scripts/run_three_arm.py` | 1830 | exact | `scripts/run_three_arm.py` |
| `evidence/bootstrap_ci.json` | 1832 | exact | `evidence/bootstrap_ci.json` |
| `scripts/bootstrap_ci.py` | 1834 | exact | `scripts/bootstrap_ci.py` |
| `evidence/dual_judge_adjudication.json` | 1835 | exact | `evidence/dual_judge_adjudication.json` |
| `theory/` | 1836 | prefix-dir | `theory/estimator_design.md`, `theory/msi.py` |
| `sim_matcher_bias.py` | 1838 | exact | `theory/sim_matcher_bias.py` |
| `sim_sem_ece.py` | 1839 | exact | `theory/sim_sem_ece.py` |
| `evidence/multi_model/` | 1841 | prefix-dir | `evidence/multi_model/consensus_ece_result.json`, `evidence/multi_model/consensus_result.json` |
| `collect_multi_model.py` | 1842 | exact | `scripts/collect_multi_model.py` |
| `multi_model_analysis.py` | 1842 | exact | `scripts/multi_model_analysis.py` |
| `evidence/census_sig600/` | 1844 | prefix-dir | `evidence/census_sig600/census600_tasks.json`, `evidence/census_sig600/for_judge.jsonl` |
| `pull_crossfamily.py` | 1846 | exact | `scripts/pull_crossfamily.py` |
| `merge_judged.py` | 1847 | exact | `scripts/merge_judged.py` |
| `compute_significance_analysis.py` | 1847 | exact | `scripts/compute_significance_analysis.py` |
| `compute_judge_calibration.py` | 1849 | exact | `scripts/compute_judge_calibration.py` |
| `judge_calibration_9model.json` | 1850 | exact | `evidence/census_sig600/judge_calibration_9model.json` |
| `evidence/frontier/` | 1852 | prefix-dir | `evidence/frontier/collect.log`, `evidence/frontier/DeepSeek-V4-Flash-0731.jsonl` |
| `evidence_manifest.json` | 1854 | exact | `evidence_manifest.json` |
| `results/verified/` | 1855 | MISSING | - |

## 3. Windows 绝对路径泄漏（→ Major，匿名/规范）

- `paper/main.tex` L207: `i:\hat{y`
- `paper/main.tex` L252: `i:\hat{y`
- `paper/main.tex` L441: `i:\hat{y`
- `paper/main.tex` L1611: `F:\hat{y`
- `paper/main.tex` L1611: `F:\hat{y`
- `paper/main.tex` L1615: `i:\hat{y`
- `paper/fancyhdr.sty` L284: `e:\MessageBreak`
- `paper/fancyhdr.sty` L291: `e:\MessageBreak`
- `paper/main.tex` L207: `i:\hat{y`
- `paper/main.tex` L252: `i:\hat{y`
- `paper/main.tex` L441: `i:\hat{y`
- `paper/main.tex` L1611: `F:\hat{y`
- `paper/main.tex` L1611: `F:\hat{y`
- `paper/main.tex` L1615: `i:\hat{y`
- `scripts/check_tmlr_compliance.py` L26: `\\usepackage\s*(?:\[[^\`
- `scripts/check_tmlr_compliance.py` L27: `\\documentclass\s*(?:\[[^\`
- `scripts/check_tmlr_compliance.py` L34: `\\bibliographystyle\s*\{[^`
- `scripts/check_tmlr_compliance.py` L35: `\\bibliography\s*\{`
- `scripts/collect_census.py` L24: `y:\n`
- `scripts/collect_frontier.py` L41: `y:\n`
- `scripts/collect_frontier.py` L46: `y:\n`
- `scripts/collect_ood.py` L26: `y:\n`
- `scripts/compile_gate.py` L40: `\\label\{([^`
- `scripts/dual_assessment.py` L57: `\\begin\{abstract\`
- `scripts/dual_assessment.py` L57: `\\end\{abstract\`
- `scripts/dual_model_final_eval.py` L20: `\\begin\{abstract\`
- `scripts/dual_model_final_eval.py` L20: `\\end\{abstract\`
- `scripts/dual_model_final_eval.py` L46: `T:\n`
- `scripts/dual_model_final_eval.py` L47: `S:\n`
- `scripts/dual_model_final_eval.py` L48: `s:\n`
- `scripts/judge_census.py` L22: `y:\n`
- `scripts/judge_hetero.py` L26: `y:\n`
- `scripts/scanner_regression.py` L39: `s:\s*(\d+`
- `scripts/scanner_regression.py` L40: `s:\s*(\d+`
- `scripts/scanner_regression.py` L41: `t:\s*(\d+`
- `scripts/scanner_regression.py` L78: `s:\s*(\d+`
- `scripts/scanner_regression.py` L79: `s:\s*(\d+`
- `scripts/scanner_regression.py` L80: `f:\s*(\d+`
- `scripts/scanner_regression.py` L83: `t:\s*(\d+`
- `scripts/scanner_regression.py` L86: `k:\s*(\d+`
- `scripts/scanner_regression.py` L101: `s:\s*(\d+`
- `scripts/scanner_regression.py` L102: `s:\s*(\d+`
- `scripts/scanner_regression.py` L103: `d:\s*(\d+`
- `scripts/scan_figure_claims.py` L64: `\\label\{(fig:[^`
- `scripts/verify_taint.py` L93: `C:\\...`
- `CLAIM_LEDGER.md` L42: `E:\AGI-KIT\logs\cloud_smoke_{baseline`
- `evidence_manifest.json` LNone: `F:\deepseek\_stage_calib_20260827`

## 4. 封包-磁盘同步检查

- zip 内 tex：`paper/main.tex` —— ✅ 一致

## 5. 磁盘版 tex 声明 vs zip 实际

- 论文未出现可解析的文件数声明