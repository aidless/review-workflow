# 投稿包证据审计报告（R2）

- 投稿包：`F:\deepseek\papers\calibration-self-improvement\submission_redteam_4fixes_20260825.zip`（535 条目）
- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`
- 结论：**CRITICAL**（引用缺失 6/44，路径泄漏 199，声明不符 0/0）

## 1. 论文引用但包内缺失（→ Critical）

- L700: `theory/`
- L1135: `cais/mmlu`
- L1229: `census_sig600/`
- L1836: `theory/`
- L1838: `sim_matcher_bias.py`
- L1839: `sim_sem_ece.py`

## 2. 引用匹配明细

| 引用 | 行 | 状态 | 匹配条目 |
|---|---|---|---|
| `label_adjudication.json` | 363 | exact | `evidence/label_adjudication.json` |
| `dual_judge_adjudication.json` | 371 | exact | `evidence/dual_judge_adjudication.json` |
| `theory/` | 700 | MISSING | - |
| `multi_model/matcher_vs_judge.json` | 785 | exact | `evidence/multi_model/matcher_vs_judge.json` |
| `multi_model/per_source_judge_agreement.json` | 817 | exact | `evidence/multi_model/per_source_judge_agreement.json` |
| `multi_model/three_judge_analysis.json` | 857 | exact | `evidence/multi_model/three_judge_analysis.json` |
| `multi_model/flip_audit_list.json` | 870 | exact | `evidence/multi_model/flip_audit_list.json` |
| `multi_model/flip_audit_results.json` | 871 | exact | `evidence/multi_model/flip_audit_results.json` |
| `multi_model/consensus_ece_result.json` | 901 | exact | `evidence/multi_model/consensus_ece_result.json` |
| `flip_audit_list.json` | 902 | exact | `evidence/multi_model/flip_audit_list.json` |
| `multi_model/consensus_ece_result.json` | 918 | exact | `evidence/multi_model/consensus_ece_result.json` |
| `cais/mmlu` | 1135 | MISSING | - |
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
| `theory/` | 1836 | MISSING | - |
| `sim_matcher_bias.py` | 1838 | MISSING | - |
| `sim_sem_ece.py` | 1839 | MISSING | - |
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
| `evidence_manifest.json` | 1854 | exact | `results/runs/20260816-215500-e6e45979/evidence_manifest.json`, `results/runs/20260817-002854-b917e1ff/evidence_manifest.json` |
| `results/verified/` | 1855 | prefix-dir | `results/verified/bundle-20260815-final/analysis_summary.json`, `results/verified/bundle-20260815-final/manifest.json` |

## 3. Windows 绝对路径泄漏（→ Major，匿名/规范）

- `paper/main.tex` L207: `i:\hat{y`
- `paper/main.tex` L252: `i:\hat{y`
- `paper/main.tex` L441: `i:\hat{y`
- `paper/main.tex` L1611: `F:\hat{y`
- `paper/main.tex` L1611: `F:\hat{y`
- `paper/main.tex` L1615: `i:\hat{y`
- `paper/fancyhdr.sty` L284: `e:\MessageBreak`
- `paper/fancyhdr.sty` L291: `e:\MessageBreak`
- `paper/main.tex` L204: `i:\hat{y`
- `paper/main.tex` L249: `i:\hat{y`
- `paper/main.tex` L438: `i:\hat{y`
- `paper/main.tex` L1597: `F:\hat{y`
- `paper/main.tex` L1597: `F:\hat{y`
- `paper/main.tex` L1601: `i:\hat{y`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\evidence_manifest.json`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `C:\Program`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\scripts\recompute_analysis.py`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\evidence\confidence_pilot.jsonl`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `F:\Temp\tmp4tt48ops\analysis_recompute.json`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `C:\Program`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\scripts\verify_claim_ledger.py`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `C:\Program`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\scripts\build_evidence_manifest.py`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\evidence_manifest.json`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `C:\Program`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\scripts\run_acceptance_gates.py`
- `results/runs/20260816-215500-e6e45979/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\gates_config.json`
- `results/runs/20260817-002854-b917e1ff/evidence_manifest.json` LNone: `F:\deepseek\papers\calibration-self-improvement`
- `results/verified/bundle-20260817-e6e45979-v2/STATUS.json` LNone: `C:\Program`
- `results/verified/bundle-20260817-e6e45979-v2/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\scripts\recompute_analysis.py`
- `results/verified/bundle-20260817-e6e45979-v2/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\evidence\confidence_pilot.jsonl`
- `results/verified/bundle-20260817-e6e45979-v2/STATUS.json` LNone: `F:\Temp\tmp4tt48ops\analysis_recompute.json`
- `results/verified/bundle-20260817-e6e45979-v2/STATUS.json` LNone: `C:\Program`
- `results/verified/bundle-20260817-e6e45979-v2/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\scripts\verify_claim_ledger.py`
- `results/verified/bundle-20260817-e6e45979-v2/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement`
- `results/verified/bundle-20260817-e6e45979-v2/STATUS.json` LNone: `C:\Program`
- `results/verified/bundle-20260817-e6e45979-v2/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\scripts\build_evidence_manifest.py`
- `results/verified/bundle-20260817-e6e45979-v2/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement`
- `results/verified/bundle-20260817-e6e45979-v2/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\evidence_manifest.json`
- `results/verified/bundle-20260817-e6e45979-v2/STATUS.json` LNone: `C:\Program`
- `results/verified/bundle-20260817-e6e45979-v2/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\scripts\run_acceptance_gates.py`
- `results/verified/bundle-20260817-e6e45979-v2/STATUS.json` LNone: `F:\deepseek\papers\calibration-self-improvement\gates_config.json`
- `results/verified/bundle-20260817-e6e45979-v2/verification/verification.json` LNone: `C:\Program`
- `results/verified/bundle-20260817-e6e45979-v2/verification/verification.json` LNone: `F:\deepseek\papers\calibration-self-improvement\scripts\recompute_analysis.py`
- `results/verified/bundle-20260817-e6e45979-v2/verification/verification.json` LNone: `F:\deepseek\papers\calibration-self-improvement\evidence\confidence_pilot.jsonl`
- `results/verified/bundle-20260817-e6e45979-v2/verification/verification.json` LNone: `F:\Temp\tmp4tt48ops\analysis_recompute.json`
- `results/verified/bundle-20260817-e6e45979-v2/verification/verification.json` LNone: `C:\Program`
- `results/verified/bundle-20260817-e6e45979-v2/verification/verification.json` LNone: `F:\deepseek\papers\calibration-self-improvement\scripts\verify_claim_ledger.py`

## 4. 封包-磁盘同步检查

- zip 内 tex：`paper/main.tex` —— ❌ DESYNC（zip 内为旧版，磁盘已修订，需重封包）

## 5. 磁盘版 tex 声明 vs zip 实际

- 论文未出现可解析的文件数声明