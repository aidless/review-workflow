# Manifest 哈希核验（R2b）

- manifest：`zip:evidence_manifest.json`（声明 root：`F:\deepseek\papers\kg-retrieval`）
- 结论：**CRITICAL** —— 64/69 哈希一致，0 不一致，5 缺失

## 不一致/缺失明细

| path | 状态 | 期望 sha256(前16) | 实际 sha256(前16) |
|---|---|---|---|
| `ROUND_R0.md` | MISSING | `8f4085ef3d1e17bf` | `-` |
| `scripts/verify_claim_ledger.py` | MISSING | `94244862521b86c9` | `-` |
| `scripts/verify_labels.py` | MISSING | `ea643cff3383121f` | `-` |
| `scripts/verify_taint.py` | MISSING | `d6e063f72358299f` | `-` |
| `scripts/verify_tree_diff.py` | MISSING | `ae8335e62951c054` | `-` |