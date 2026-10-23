# 投稿包证据审计报告（R2）

- 投稿包：`F:\deepseek\papers\kg-retrieval\submission\submission_kg-retrieval.zip`（65 条目）
- 论文：`F:\deepseek\papers\kg-retrieval\paper\main.tex`
- 结论：**MAJOR**（引用缺失 0/0，路径泄漏 52，声明不符 0/0）

## 1. 论文引用但包内缺失（→ Critical）

- 无

## 2. 引用匹配明细

| 引用 | 行 | 状态 | 匹配条目 |
|---|---|---|---|

## 3. Windows 绝对路径泄漏（→ Major，匿名/规范）

- `evidence/protocol.md` L28: `F:\deepseek\papers\kg-retrieval\requirements.txt`
- `evidence/protocol.md` L33: `F:\deepseek\papers\kg-retrieval\scripts\analysis.py锛堝彧璇婚噸绠楋紝涓嶅悎鎴愭暟鎹級`
- `evidence_manifest.json` LNone: `F:\deepseek\papers\kg-retrieval`
- `paper/fancyhdr.sty` L284: `e:\MessageBreak`
- `paper/fancyhdr.sty` L291: `e:\MessageBreak`
- `scripts/check_submission_package.py` L39: `\\email\s*\{[^`
- `scripts/check_submission_package.py` L39: `\\affiliation\s*\{[^`
- `scripts/check_tmlr_compliance.py` L30: `\\usepackage\s*(?:\[[^\`
- `scripts/check_tmlr_compliance.py` L31: `\\documentclass\s*(?:\[[^\`
- `scripts/check_tmlr_compliance.py` L38: `\\bibliographystyle\s*\{[^`
- `scripts/check_tmlr_compliance.py` L39: `\\bibliography\s*\{`
- `scripts/check_tmlr_compliance.py` L204: `\\usepackage\s*(?:\[[^\`
- `scripts/check_tmlr_compliance.py` L307: `\\end\{document\`
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
- `scripts/scanner_regression.py` L149: `s:\s*(\d+`
- `scripts/scanner_regression.py` L150: `s:\s*(\d+`
- `scripts/scanner_regression.py` L151: `s:\s*(\d+`
- `scripts/scanner_regression.py` L152: `s:\s*(\d+`
- `scripts/scanner_regression.py` L153: `s:\s*(\d+`
- `scripts/scanner_regression.py` L154: `s:\s*(\d+`
- `scripts/scanner_regression.py` L155: `s:\s*(\d+`
- `scripts/scanner_regression.py` L156: `d:\s*(\d+`
- `scripts/switch_project.py` L25: `F:\deepseek\papers`

## 4. 封包-磁盘同步检查

- zip 内 tex：`paper/main.tex` —— ❌ DESYNC（zip 内为旧版，磁盘已修订，需重封包）

## 5. 磁盘版 tex 声明 vs zip 实际

- 论文未出现可解析的文件数声明