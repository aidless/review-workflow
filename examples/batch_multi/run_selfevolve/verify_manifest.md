# Manifest 哈希核验（R2b）

- manifest：`zip:evidence_manifest.json`（声明 root：`.`）
- 结论：**CRITICAL** —— 72/81 哈希一致，3 不一致，6 缺失

## 不一致/缺失明细

| path | 状态 | 期望 sha256(前16) | 实际 sha256(前16) |
|---|---|---|---|
| `paper/main.log` | HASH_MISMATCH | `9202a71af8419264` | `aaf472db9d0a23f4` |
| `paper/main.pdf` | HASH_MISMATCH | `0e7a880932221f1d` | `81d8a059667a4422` |
| `paper/main.tex` | HASH_MISMATCH | `361126a37b373563` | `9ae164ea05b2e3c7` |
| `REVIEW_R1_summary.md` | MISSING | `0cb3bb60ef7da692` | `-` |
| `ROUND_R0.md` | MISSING | `9d5df16cce1e7748` | `-` |
| `scripts/verify_claim_ledger.py` | MISSING | `d4cba827d819e9f8` | `-` |
| `scripts/verify_labels.py` | MISSING | `ea643cff3383121f` | `-` |
| `scripts/verify_taint.py` | MISSING | `d6e063f72358299f` | `-` |
| `scripts/verify_tree_diff.py` | MISSING | `ae8335e62951c054` | `-` |