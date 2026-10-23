# -*- coding: utf-8 -*-
"""诚实性扫描（honesty_scan）— 审稿工作流 R5b。

机械捕获"论文声称 X、产物注明 simulated/pending/mock"类诚实性问题：
  1. 扫描产物（JSON/JSONL/MD/tex 源）中的诚实性关键词命中（simulated/mock/synthetic/pending/placeholder/…）
  2. 每个命中提取关联概念（annotator/judge/ablation/…）与数值（α/k/p/率）
  3. 与论文 tex 比对：论文是否引用了该产物数字却未披露 simulated/pending 状态
     —— 论文含产物数值 + 论文无披露词 + 产物有 simulated 标记 → SUSPICIOUS（人工定性为 Critical/Major）
用法:
    python honesty_scan.py --tex main.tex --evidence-dirs results,out_p5 --out out_dir
    python honesty_scan.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

HINT_WORDS = [
    ("simulated", "simulate", "模拟"),
    ("mock", None, "mock"),
    ("synthetic", None, "合成"),
    ("placeholder", None, "占位"),
    ("dummy", None, "dummy"),
    ("fake", None, "fake"),
    ("toy", None, "toy"),
    ("pending", None, "待办/未做"),
    ("draft only", None, "仅草稿"),
    ("not real", None, "非真实"),
    ("TODO", None, "TODO"),
    ("FIXME", None, "FIXME"),
]
# 论文中的"披露词"：若论文引用了被标记产物且含这些词，视为已披露
DISCLOSURE_NEAR_RE = re.compile(r"simulat|simulation|\bsim\b|mock|synthetic|pending|placeholder|future work|planned|not run|interim", re.I)
NUM_RE = re.compile(r"\d+\.\d+")
CONCEPT_RE = re.compile(r"(annotator|judge|ablation|bootstrap|trial|agreement|kappa|alpha|double|annotat)", re.I)


def near_disclosure(tex: str, num: str) -> bool:
    """数值在论文中出现的位置 ±150 字符内是否有披露词（就近披露才算披露）。"""
    for v in num_variants(num):
        for m in re.finditer(re.escape(v), tex):
            window = tex[max(0, m.start() - 150) : m.end() + 150]
            if DISCLOSURE_NEAR_RE.search(window):
                return True
    return False


def num_variants(n: str) -> list[str]:
    """论文常截断产物全精度数字（0.894 vs 0.8940217391304347）：生成可匹配变体。"""
    try:
        v = float(n)
    except ValueError:
        return [n]
    out = {n}
    for d in (3, 4):
        out.add(f"{v:.{d}f}")
    return list(out)


def num_in_text(n: str, text: str) -> bool:
    return any(v in text for v in num_variants(n))


def iter_strings(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_strings(v, f"{prefix}.{k}" if prefix else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_strings(v, f"{prefix}[{i}]")
    elif isinstance(obj, str):
        yield prefix, obj


def scan_file(path: Path) -> list[dict]:
    hits = []
    ext = path.suffix.lower()
    try:
        if ext == ".json":
            data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
            # 顶层分块：dict 按顶层 key 分块（hint 与关联数字同块，如 note 命中 + alpha 数值）
            if isinstance(data, dict):
                blocks = [{k: v} for k, v in data.items()]
            elif isinstance(data, list):
                blocks = data
            else:
                blocks = [data]
            for block in blocks:
                block_nums = NUM_RE.findall(json.dumps(block, ensure_ascii=False))[:12]
                if not block_nums:
                    # hint 与数值分属不同顶层 key（如 note 块 vs alpha 块）时回退全文件数字
                    block_nums = NUM_RE.findall(path.read_text(encoding="utf-8", errors="replace"))[:12]
                for key, s in iter_strings(block):
                    for h in match_hints(path, key, s):
                        h["context_numbers"] = block_nums
                        hits.append(h)
        elif ext == ".jsonl":
            for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    for key, s in iter_strings(obj):
                        for h in match_hints(path, f"L{i}:{key}", s):
                            h["context_numbers"] = NUM_RE.findall(line)[:12]
                            hits.append(h)
                except Exception:
                    hits += match_hints(path, f"L{i}", line)
        else:
            for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                hits += match_hints(path, f"L{i}", line)
    except Exception:
        pass
    return hits


def match_hints(path: Path, where: str, text: str) -> list[dict]:
    out = []
    low = text.lower()
    for word, alt, zh in HINT_WORDS:
        needles = [w for w in (word, alt) if w]
        if any(n in low for n in needles):
            nums = NUM_RE.findall(text)
            concepts = CONCEPT_RE.findall(text)
            out.append({
                "file": str(path), "where": where, "hint": word,
                "text": text.strip()[:200],
                "numbers": nums[:6], "concepts": list(dict.fromkeys(concepts))[:4],
            })
            break  # 一个字符串只报最强的第一个命中
    return out


def collect_clean_numbers(path: Path) -> set[str]:
    """收集无 hint 文件的全部数字：用于交叉验证（数字另有真实产物来源则降级）。"""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        return set(NUM_RE.findall(text))
    except Exception:
        return set()


def scan(tex_path: Path, evidence_dirs: list[Path], allowlist: list[dict] | None = None) -> dict:
    """诚实性扫描。allowlist：人工定性误报清单 [{hint, file_contains, reason, by}]，
    命中条目记 disclosed='human-allowlisted'，不计入门限（2026-09-06 治理决议：用户批准检测器校准，
    已披露/交叉证实/人工定性误报不构成 finding；证据文件原样保留）。"""
    tex = tex_path.read_text(encoding="utf-8", errors="replace")

    hits = []
    clean_numbers: set[str] = set()
    scanned: dict[Path, list[dict]] = {}
    for d in evidence_dirs:
        if not d.exists():
            continue
        for f in sorted(d.rglob("*")):
            if f.suffix.lower() in {".json", ".jsonl", ".md", ".txt", ".py", ".log"} and f.is_file():
                f_hits = scan_file(f)
                scanned[f] = f_hits
                hits += f_hits
    for f, f_hits in scanned.items():
        if not f_hits:  # 无 hint 标记的文件，其数字视为有真实来源
            clean_numbers |= collect_clean_numbers(f)

    suspicious, disclosed_hits = [], []
    clean_variants: set[str] = set()
    for n in clean_numbers:
        clean_variants.update(num_variants(n))
    for h in hits:
        nums = list(dict.fromkeys(h.get("numbers", []) + h.get("context_numbers", [])))
        h["all_numbers"] = nums[:8]
        # 产物数字出现在论文中 + 论文讨论同概念 + 数值附近无披露词 → 可疑
        num_in_paper = [n for n in nums if len(n) >= 3 and num_in_text(n, tex)]
        concept_in_paper = any(
            re.search(rf"\b{re.escape(c)}\b", tex, re.I) for c in h["concepts"]
        ) if h["concepts"] else False
        if num_in_paper and concept_in_paper:
            undisclosed = [n for n in num_in_paper if not near_disclosure(tex, n)]
            if not undisclosed:
                h["disclosed"] = True
                disclosed_hits.append(h)
                continue
            corroborated = [n for n in undisclosed if any(v in clean_variants for v in num_variants(n))]
            if len(corroborated) == len(undisclosed):
                # 全部数字另有真实（无 hint）产物来源 → 交叉证实，降级
                h["disclosed"] = "cross-corroborated"
                h["corroborated_by"] = "clean artifact numbers"
                disclosed_hits.append(h)
                continue
            h["why_suspicious"] = (
                f"产物标注 '{h['hint']}'（{h['where']}），数值 {undisclosed[:3]} 出现在论文中且附近无披露词，"
                f"论文讨论了 {h['concepts'][:2]}"
                + (f"（{corroborated[:2]} 另有真实来源）" if corroborated else "")
            )
            suspicious.append(h)

    n, n_sus = len(hits), len(suspicious)
    # 人工 allowlist 定性误报（治理决议 2026-09-06）：命中特定 hint+文件模式的条目视为已披露
    n_allow = 0
    for h in hits:
        if h.get("disclosed"):
            continue
        for rule in (allowlist or []):
            if (not rule.get("hint") or rule["hint"] == h.get("hint")) and \
               (not rule.get("file_contains") or rule["file_contains"] in str(h.get("file", ""))):
                h["disclosed"] = "human-allowlisted"
                h["allow_rule"] = {k: rule.get(k) for k in ("hint", "file_contains", "reason", "by")}
                disclosed_hits.append(h)
                n_allow += 1
                break
    eff = [h for h in hits if not h.get("disclosed")]
    verdict = "CRITICAL" if n_sus else ("MAJOR" if eff else "PASS")
    return {
        "meta": {
            "tex": str(tex_path), "evidence_dirs": [str(d) for d in evidence_dirs],
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "hint_hits": hits,
        "suspicious": suspicious,
        "disclosed_hits": disclosed_hits,
        "summary": {
            "hint_hits": n,
            "suspicious": n_sus,
            "disclosed": len(disclosed_hits),
            "allowlisted": n_allow,
            "effective": len(eff),
            "verdict": verdict,
            "note": "suspicious = 人工定性入口：逐条判定论文表述是否如实披露（Critical）或措辞需补披露（Major）",
        },
    }


def write_md(report: dict, out_md: Path) -> None:
    s = report["summary"]
    lines = [
        "# 诚实性扫描报告（R5b）",
        "",
        f"- 论文：`{report['meta']['tex']}`；证据目录：{', '.join('`'+d+'`' for d in report['meta']['evidence_dirs'])}",
        f"- 结论：**{s['verdict']}** —— 关键词命中 {s['hint_hits']}，可疑（论文数值+无就近披露）{s['suspicious']}，已就近披露 {s['disclosed']}",
        "",
        "## 可疑命中（论文引用了被标记产物的数值，需人工定性）",
        "",
    ]
    if report["suspicious"]:
        lines += [f"- **{h['file']}** `{h['where']}` [{h['hint']}]：\"{h['text'][:120]}\"\n  - {h['why_suspicious']}" for h in report["suspicious"]]
    else:
        lines.append("- 无")
    lines += ["", "## 全部关键词命中（按文件）", ""]
    if report["hint_hits"]:
        cur = None
        for h in report["hint_hits"]:
            if h["file"] != cur:
                cur = h["file"]
                lines.append(f"### `{cur}`")
            mark = "（已就近披露）" if h.get("disclosed") else ""
            lines.append(f"- `{h['where']}` [{h['hint']}]{mark} {h['text'][:100]}")
        if len(report["hint_hits"]) > 200:
            lines.append(f"- ……共 {len(report['hint_hits'])} 条，见 JSON")
    else:
        lines.append("- 无")
    out_md.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    import tempfile

    tmp = Path(tempfile.mkdtemp())
    ev = tmp / "out_p5"
    ev.mkdir()
    (ev / "report.json").write_text(json.dumps({
        "agreement": {"alpha": 0.894, "note": "Second annotator simulated with 2/40 disagreements"}
    }), encoding="utf-8")
    tex = tmp / "main.tex"
    tex.write_text(r"Double-annotator $\alpha=0.894$ validates the judge.", encoding="utf-8")
    rep = scan(tex, [ev])
    assert rep["summary"]["hint_hits"] >= 1, rep["summary"]
    assert rep["summary"]["suspicious"] == 1, rep["summary"]
    assert rep["summary"]["verdict"] == "CRITICAL", rep["summary"]
    # 已披露则不升 CRITICAL
    tex2 = tmp / "main2.tex"
    tex2.write_text(r"Simulated second annotator gives $\alpha=0.894$ (disclosed as simulation).", encoding="utf-8")
    rep2 = scan(tex2, [ev])
    assert rep2["summary"]["suspicious"] == 0, rep2["summary"]
    assert rep2["summary"]["verdict"] != "CRITICAL"
    print("honesty_scan selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tex", type=Path)
    ap.add_argument("--evidence-dirs", type=str)
    ap.add_argument("--out", type=Path, default=Path("audit_out"))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not (args.tex and args.evidence_dirs):
        ap.error("--tex and --evidence-dirs required (or --selftest)")
    dirs = [Path(p) for p in args.evidence_dirs.split(",") if p.strip()]
    report = scan(args.tex, dirs)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "honesty_scan.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(report, args.out / "honesty_scan.md")
    s = report["summary"]
    print(f"verdict={s['verdict']} hint_hits={s['hint_hits']} suspicious={s['suspicious']}")
    for h in report["suspicious"][:10]:
        print(f"  SUSPICIOUS {h['file']} {h['where']}: {h['text'][:80]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
