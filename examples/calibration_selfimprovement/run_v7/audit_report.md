# 投稿包证据审计报告（R2）

- 投稿包：`F:\deepseek\papers\calibration-self-improvement\submission_clean_20260827_v7.zip`（283 条目）
- 论文：`F:\deepseek\papers\calibration-self-improvement\paper\main.tex`
- 结论：**PASS**（引用缺失 0/49，路径泄漏 0，声明不符 0/0）

## 1. 论文引用但包内缺失（→ Critical）

- 无

## 2. 引用匹配明细

| 引用 | 行 | 状态 | 匹配条目 |
|---|---|---|---|
| `label_adjudication.json` | 355 | exact | `evidence/label_adjudication.json` |
| `dual_judge_adjudication.json` | 363 | exact | `evidence/dual_judge_adjudication.json` |
| `theory/` | 692 | prefix-dir | `theory/estimator_design.md`, `theory/msi.py` |
| `multi_model/matcher_vs_judge.json` | 777 | exact | `evidence/multi_model/matcher_vs_judge.json` |
| `multi_model/per_source_judge_agreement.json` | 809 | exact | `evidence/multi_model/per_source_judge_agreement.json` |
| `multi_model/three_judge_analysis.json` | 849 | exact | `evidence/multi_model/three_judge_analysis.json` |
| `multi_model/flip_audit_list.json` | 862 | exact | `evidence/multi_model/flip_audit_list.json` |
| `multi_model/flip_audit_results.json` | 863 | exact | `evidence/multi_model/flip_audit_results.json` |
| `multi_model/consensus_ece_result.json` | 893 | exact | `evidence/multi_model/consensus_ece_result.json` |
| `flip_audit_list.json` | 894 | exact | `evidence/multi_model/flip_audit_list.json` |
| `multi_model/consensus_ece_result.json` | 910 | exact | `evidence/multi_model/consensus_ece_result.json` |
| `evidence/census_sig600/` | 1221 | prefix-dir | `evidence/census_sig600/census600_tasks.json`, `evidence/census_sig600/for_judge.jsonl` |
| `evidence/confidence.jsonl` | 1835 | exact | `evidence/confidence.jsonl` |
| `recompute_analysis.py` | 1841 | exact | `scripts/recompute_analysis.py` |
| `confidence_pilot.jsonl` | 1841 | exact | `evidence/confidence_pilot.jsonl` |
| `evidence/confidence_pilot.jsonl` | 1842 | exact | `evidence/confidence_pilot.jsonl` |
| `evidence/label_adjudication.json` | 1844 | exact | `evidence/label_adjudication.json` |
| `evidence/analysis_summary.json` | 1846 | exact | `evidence/analysis_summary.json` |
| `evidence/three_arm_result.json` | 1849 | exact | `evidence/three_arm_result.json` |
| `scripts/collect_pilot_data.py` | 1852 | exact | `scripts/collect_pilot_data.py` |
| `scripts/label_match.py` | 1853 | exact | `scripts/label_match.py` |
| `scripts/label_match.py` | 1853 | exact | `scripts/label_match.py` |
| `evidence/label_adjudication.json` | 1853 | exact | `evidence/label_adjudication.json` |
| `scripts/recompute_analysis.py` | 1853 | exact | `scripts/recompute_analysis.py` |
| `scripts/adjudicate_labels.py` | 1853 | exact | `scripts/adjudicate_labels.py` |
| `scripts/verify_labels.py` | 1853 | exact | `scripts/verify_labels.py` |
| `scripts/recompute_analysis.py` | 1855 | exact | `scripts/recompute_analysis.py` |
| `scripts/run_three_arm.py` | 1857 | exact | `scripts/run_three_arm.py` |
| `evidence/bootstrap_ci.json` | 1859 | exact | `evidence/bootstrap_ci.json` |
| `scripts/bootstrap_ci.py` | 1861 | exact | `scripts/bootstrap_ci.py` |
| `evidence/dual_judge_adjudication.json` | 1862 | exact | `evidence/dual_judge_adjudication.json` |
| `theory/` | 1863 | prefix-dir | `theory/estimator_design.md`, `theory/msi.py` |
| `sim_matcher_bias.py` | 1865 | exact | `theory/sim_matcher_bias.py` |
| `sim_sem_ece.py` | 1866 | exact | `theory/sim_sem_ece.py` |
| `evidence/multi_model/` | 1868 | prefix-dir | `evidence/multi_model/consensus_ece_result.json`, `evidence/multi_model/consensus_result.json` |
| `collect_multi_model.py` | 1869 | exact | `scripts/collect_multi_model.py` |
| `multi_model_analysis.py` | 1869 | exact | `scripts/multi_model_analysis.py` |
| `evidence/census_sig600/` | 1871 | prefix-dir | `evidence/census_sig600/census600_tasks.json`, `evidence/census_sig600/for_judge.jsonl` |
| `pull_crossfamily.py` | 1873 | exact | `scripts/pull_crossfamily.py` |
| `merge_judged.py` | 1874 | exact | `scripts/merge_judged.py` |
| `compute_significance_analysis.py` | 1874 | exact | `scripts/compute_significance_analysis.py` |
| `compute_judge_calibration.py` | 1876 | exact | `scripts/compute_judge_calibration.py` |
| `judge_calibration_9model.json` | 1877 | exact | `evidence/census_sig600/judge_calibration_9model.json` |
| `evidence/frontier/` | 1879 | prefix-dir | `evidence/frontier/collect.log`, `evidence/frontier/DeepSeek-V4-Flash-0731.jsonl` |
| `evidence_manifest.json` | 1881 | exact | `evidence_manifest.json` |
| `evidence_manifest.json` | 1882 | exact | `evidence_manifest.json` |
| `evidence/licenses/mmlu_license.md` | 1898 | exact | `evidence/licenses/mmlu_license.md` |
| `evidence/census_sig600/` | 1898 | prefix-dir | `evidence/census_sig600/census600_tasks.json`, `evidence/census_sig600/for_judge.jsonl` |
| `evidence/licenses/chinese_freeform_license.md` | 1901 | exact | `evidence/licenses/chinese_freeform_license.md` |

## 3. Windows 绝对路径泄漏（→ Major，匿名/规范）

- 无

## 4. 封包-磁盘同步检查

- zip 内 tex：`paper/main.tex` —— ✅ 一致

## 5. 磁盘版 tex 声明 vs zip 实际

- 论文未出现可解析的文件数声明