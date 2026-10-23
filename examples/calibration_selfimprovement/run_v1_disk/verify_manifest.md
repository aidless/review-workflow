# Manifest 哈希核验（R2b）

- manifest：`disk:F:\deepseek\papers\calibration-self-improvement\evidence_manifest.json`（声明 root：`.`）
- 结论：**CRITICAL** —— 635/638 哈希一致，3 不一致，0 缺失

## 不一致/缺失明细

| path | 状态 | 期望 sha256(前16) | 实际 sha256(前16) |
|---|---|---|---|
| `paper/main.fdb_latexmk` | HASH_MISMATCH | `99d17f77b606ce51` | `faf71c16d6f94891` |
| `paper/main.log` | HASH_MISMATCH | `14604fd6b86a6eb8` | `e8b31e45a0f35281` |
| `paper/main.pdf` | HASH_MISMATCH | `f4e5e75b2413a1b2` | `7d96be89c534c967` |