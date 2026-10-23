# 审稿报告模板（review_report）

> 填写说明：所有 [ ] 内为待填项；核验清单必须如实记录实际执行的命令与结果；评分纪律 = min(各维度)，不取平均。

---

# TMLR 审稿报告：[论文标题] ([版本号], [页数]页)

## 总评：[X.X]/10 — [Accept / Reject / Borderline]

[2-3 句定位：论文做了什么、最大亮点、与目标分的差距在哪]

## 独立核验清单（本次实际执行）

| 核验项 | 方法（命令/文件） | 结果 |
|---|---|---|
| 表格数字 vs 产物 JSON | `number_reconcile.py` 方向 A | ✅/❌ [n/n] |
| 论文数字有产物支撑 | `number_reconcile.py` 方向 B | ✅/❌ [n/n]，人工复核清单 |
| 包完整性（引用 vs zip 内容） | `audit_package.py` | ✅/❌ [缺失清单] |
| 路径泄漏/匿名性 | `audit_package.py` 泄漏扫描 | ✅/❌ |
| 声明数 vs 实际（文件数/哈希数） | `audit_package.py` 声明核对 | ✅/❌ |
| 关键检验手工复算 | scipy 手算 [检验名] | ✅/❌ |
| LLM 对抗审查 | `adversarial_review.py --roles all` | [n Critical / n Major] |

## Critical（不修则必被拒或降分）

**C1：[标题]**
- 现象：[发现什么]
- 证据：[核验命令 + 输出]
- 影响：[为什么是 Critical]
- 修复：[具体动作]

## Major

- **M1：[标题]** — [现象/证据/修复]
- **M2…**

## Minor

- **m1…**

## 被浪费的现成资产（可选小节）

[产物目录里已有但论文未用的数据/对照，零成本可加的分析]

---

## Strong Accept 方案（见 strong_accept_plan.md 附件）

[Tier 1/2/3 一览表 + 分数轨迹一行]

## 评分依据（TMLR 四维 + 证据层）

| 维度 | 评分 | 依据 |
|---|---|---|
| Soundness | [n] | [一句话] |
| Novelty / Contribution | [n] | [一句话] |
| Significance | [n] | [一句话] |
| Clarity | [n] | [一句话] |
| **证据层（包/数字/诚实性）** | [n] | [R2/R3/R5 结果] |
| **综合（min）** | **[X.X]** | |
