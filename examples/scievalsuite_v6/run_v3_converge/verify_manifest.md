# Manifest 哈希核验（R2b）

- manifest：`zip:evidence_manifest.json`（声明 root：`F:\deepseek\papers\scievalsuite`）
- 结论：**CRITICAL** —— 149/165 哈希一致，0 不一致，16 缺失

## 论文声明 vs manifest 实际条数

| 声明 | 口径 | 声明值 | manifest 条数 | 一致 |
|---|---|---|---|---|
| `46-entry` | manifest_entries | 46 | 165 | ❌ |
| `46-entry` | manifest_entries | 46 | 165 | ❌ |
| `165-entry` | manifest_entries | 165 | 165 | ✅ |
| `46-entry` | manifest_entries | 46 | 165 | ❌ |
| `46 SHA-256 hashes` | manifest_hashes | 46 | 165 | ❌ |
| `46 hashes` | manifest_hashes | 46 | 165 | ❌ |

## 不一致/缺失明细

| path | 状态 | 期望 sha256(前16) | 实际 sha256(前16) |
|---|---|---|---|
| `ROUND_R0.md` | MISSING | `8f4085ef3d1e17bf` | `-` |
| `ROUND_R1.md` | MISSING | `c2833a34522064ee` | `-` |
| `ROUND_R2_paperreview.md` | MISSING | `b9f424eb9adfbdf0` | `-` |
| `scripts/verify_claim_ledger.py` | MISSING | `94244862521b86c9` | `-` |
| `scripts/verify_labels.py` | MISSING | `ea643cff3383121f` | `-` |
| `scripts/verify_taint.py` | MISSING | `d6e063f72358299f` | `-` |
| `scripts/verify_tree_diff.py` | MISSING | `ae8335e62951c054` | `-` |
| `SELF_ASSESSMENT.md` | MISSING | `1fc17733df4ec8dc` | `-` |
| `submission/anonym_check.md` | MISSING | `0f0b674fe4691ce1` | `-` |
| `submission/openreview_checklist.md` | MISSING | `386589d7e2cfd87c` | `-` |
| `submission/submission_scievalsuite.zip` | MISSING | `f693b06877cd9694` | `-` |
| `submission/submission_scievalsuite_final.zip` | MISSING | `f1133a9daf83fcbc` | `-` |
| `submission/submission_scievalsuite_final_v3.zip` | MISSING | `6be924ea075a19aa` | `-` |
| `submission/submission_scievalsuite_final_v4.zip` | MISSING | `f38c0cb7572d9a1f` | `-` |
| `submission/submission_scievalsuite_final_v5.zip` | MISSING | `a96cc43370ba22bc` | `-` |
| `submission/submission_scievalsuite_v2.zip` | MISSING | `36924a4c47c7fbcd` | `-` |