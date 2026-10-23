# Manifest 哈希核验（R2b）

- manifest：`zip:evidence_manifest.json`（声明 root：`.`）
- 结论：**PASS** —— 91/91 哈希一致，0 不一致，0 缺失

## 论文声明 vs manifest 实际条数

| 声明 | 口径 | 声明值 | manifest 条数 | 一致 |
|---|---|---|---|---|
| `91-entry` | manifest_entries | 91 | 91 | ✅ |

## 不一致/缺失明细

- 无（全部 byte-for-byte 一致）