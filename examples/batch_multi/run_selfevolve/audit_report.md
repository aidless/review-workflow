# 投稿包证据审计报告（R2）

- 投稿包：`F:\deepseek\papers\selfevolve-agent\submission\submission_selfevolve_agent.zip`（77 条目）
- 论文：`F:\deepseek\papers\selfevolve-agent\paper\main.tex`
- 结论：**CRITICAL**（引用缺失 4/5，路径泄漏 61，声明不符 0/0）

## 1. 论文引用但包内缺失（→ Critical）

- L566: `deploy_full_probe.sh`
- L623: `evidence/raw_ledgers/state_round*/ledger.jsonl`
- L625: `evidence/harness/agent/`
- L733: `evidence/raw_ledgers/state_round*/ledger.jsonl`

## 2. 引用匹配明细

| 引用 | 行 | 状态 | 匹配条目 |
|---|---|---|---|
| `deploy_full_probe.sh` | 566 | MISSING | - |
| `evidence/decisions_R1-17.json` | 622 | exact | `evidence/decisions_R1-17.json` |
| `evidence/raw_ledgers/state_round*/ledger.jsonl` | 623 | MISSING | - |
| `evidence/harness/agent/` | 625 | MISSING | - |
| `evidence/raw_ledgers/state_round*/ledger.jsonl` | 733 | MISSING | - |

## 3. Windows 绝对路径泄漏（→ Major，匿名/规范）

- `_r7_followup.py` L5: `F:\deepseek\papers\selfevolve-agent\evidence`
- `_r7_followup.py` L50: `F:\deepseek\papers\selfevolve-agent`
- `_r7_recheck.py` L6: `F:\deepseek\papers\selfevolve-agent\evidence`
- `evidence/extprobe/extprobe_satisfiability_v2.json` LNone: `F:\Temp\tmpx3l24qal\check.py`
- `evidence/extprobe/extprobe_satisfiability_v2.json` LNone: `F:\Temp\tmpxqlkf0am\check.py`
- `evidence/extprobe/extprobe_satisfiability_v2.json` LNone: `F:\Temp\tmpm6rvnmx2\check.py`
- `evidence/extprobe/extprobe_satisfiability_v2.json` LNone: `F:\Temp\tmpfx7qs4or\check.py`
- `evidence/extprobe/extprobe_satisfiability_v2.json` LNone: `F:\Temp\tmp4ihab9qt\check.py`
- `evidence/extprobe/extprobe_satisfiability_v2.json` LNone: `F:\Temp\tmp8d1r4t54`
- `evidence/extprobe/extprobe_satisfiability_v2.json` LNone: `F:\Temp\tmpe__t1ccv`
- `evidence/extprobe/extprobe_satisfiability_v2.json` LNone: `F:\Temp\tmpv5szhy9m\check.py`
- `evidence/extprobe/extprobe_satisfiability_v2.json` LNone: `F:\Temp\tmp_xwxghlr\check.py`
- `evidence/extprobe/extprobe_satisfiability_v2.json` LNone: `F:\Temp\tmpk44ps51k\check.py`
- `evidence/REVIEW.md` L318: `F:\deepseek\cloud_key.pem`（部署密钥，保留）；AK/SK`
- `paper/fancyhdr.sty` L284: `e:\MessageBreak`
- `paper/fancyhdr.sty` L291: `e:\MessageBreak`
- `scripts/check_submission_package.py` L39: `\\email\s*\{[^`
- `scripts/check_submission_package.py` L39: `\\affiliation\s*\{[^`
- `scripts/check_tmlr_compliance.py` L26: `\\usepackage\s*(?:\[[^\`
- `scripts/check_tmlr_compliance.py` L27: `\\documentclass\s*(?:\[[^\`
- `scripts/check_tmlr_compliance.py` L34: `\\bibliographystyle\s*\{[^`
- `scripts/check_tmlr_compliance.py` L35: `\\bibliography\s*\{`
- `scripts/compile_gate.py` L40: `\\label\{([^`
- `scripts/gate_citations.py` L58: `F:\deepseek\research-kit\citation-verifier\verify_citations.py`
- `scripts/make_camera_ready.py` L53: `\\usepackage\{tmlr\`
- `scripts/make_camera_ready.py` L59: `\\author\s*\{[^`
- `scripts/make_camera_ready.py` L75: `\\begin\{document\`
- `scripts/make_run_record.py` L55: `F:\deepseek\.datasets\cifar-10-batches-py`
- `scripts/prepare_submission.py` L44: `\\email\s*\{[^`
- `scripts/prepare_submission.py` L44: `\\thanks\s*\{[^`
- `scripts/prepare_submission.py` L45: `\\affiliation\s*\{[^`
- `scripts/prepare_submission.py` L70: `\\title\s*\{([^`
- `scripts/prepare_submission.py` L76: `\\begin\{abstract\`
- `scripts/prepare_submission.py` L76: `\\end\{abstract\`
- `scripts/prepare_submission.py` L86: `\\keywords\s*\{([^`
- `scripts/scan_figure_claims.py` L64: `\\label\{(fig:[^`
- `scripts/scan_number_consistency.py` L30: `\\begin\{(?:table|tabular|table\*`
- `scripts/scan_number_consistency.py` L30: `\\end\{(?:table|tabular|table\*`
- `scripts/scanner_regression.py` L55: `s:\s*(\d+`
- `scripts/scanner_regression.py` L56: `s:\s*(\d+`
- `scripts/scanner_regression.py` L57: `t:\s*(\d+`
- `scripts/scanner_regression.py` L58: `s:\s*(\d+`
- `scripts/scanner_regression.py` L101: `s:\s*(\d+`
- `scripts/scanner_regression.py` L102: `s:\s*(\d+`
- `scripts/scanner_regression.py` L103: `f:\s*(\d+`
- `scripts/scanner_regression.py` L106: `t:\s*(\d+`
- `scripts/scanner_regression.py` L109: `k:\s*(\d+`
- `scripts/scanner_regression.py` L124: `s:\s*(\d+`
- `scripts/scanner_regression.py` L125: `s:\s*(\d+`
- `scripts/scanner_regression.py` L126: `d:\s*(\d+`

## 4. 封包-磁盘同步检查

- zip 内 tex：`paper/main.tex` —— ❌ DESYNC（zip 内为旧版，磁盘已修订，需重封包）

## 5. 磁盘版 tex 声明 vs zip 实际

- 论文未出现可解析的文件数声明