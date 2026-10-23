import os
"""为单篇论文生成 S6_BACKLOG.md:汇总 R6 stable issues + PRISM 最弱维 + R2d/R5/R1c/R2 残留."""
import json, sys
from pathlib import Path

p = sys.argv[1]
base = Path(os.environ.get("QONE_PAPERS_DIR", "./papers")) / p / "reviews" / "pipeline_S5"
out = base / "S6_BACKLOG.md"
L = [f"# S6 返修 backlog — {p}", "", f"生成时间: 见文件 mtime；数据源: {base}", ""]

def load(n):
    fp = base / n
    return json.loads(fp.read_text(encoding="utf-8")) if fp.exists() else None

r6 = load("r6_llm.json")
if r6:
    st = r6.get("stable_issues", [])
    L += [f"## R6 文本层 stable issues（{len(st)} 条）", ""]
    for i in st:
        L += [f"### [{i.get('sev')}] ({i.get('roles')})", "", i.get("text", "")[:1500], ""]
else:
    L += ["## R6：暂无 r6_llm.json（链未跑出文本层）", ""]

pr = load("prism_review.json")
if pr:
    dims = pr.get("dimensions", {})
    L += ["## PRISM 四维（最弱维优先改）", ""]
    for k in sorted(dims, key=lambda k: (dims[k].get("score") is None, dims[k].get("score") or 0)):
        v = dims[k]
        L += [f"- {k}={v.get('score')}：{v.get('justification','')[:300]}",
              f"  最弱点：{v.get('top_weakness','')[:300]}"]
    L += [""]

for n, title in [("table_check.json", "R2d 表格"), ("honesty_scan.json", "R5 诚实"),
                 ("number_reconcile.json", "R3 对账"), ("stats_recompute.json", "R4 复算")]:
    d = load(n)
    if d:
        L += [f"## {title}: {json.dumps(d.get('summary', {}), ensure_ascii=False)[:400]}", ""]

L += ["## 通用 S6 动作（8 分必需）",
      "- R1c 联网新颖性对照（novelty_online=true，需验证 arXiv 可达）",
      "- R2/R2b 投稿 zip 封包（audit_package 零缺失零泄漏）",
      "- R6 收敛：修复后重跑至一轮无新 Critical/Major（--converge 3）",
      "- R6b 最弱维：针对性补强并写入正文（非自评分数游戏）",
      "- R6c 辩论：sustained 清零或逐条 tex 修订+证据",
      ""]
out.write_text("\n".join(L), encoding="utf-8")
print("wrote", out, len("\n".join(L)), "chars")
