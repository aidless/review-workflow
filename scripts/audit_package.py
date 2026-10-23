# -*- coding: utf-8 -*-
"""投稿包证据审计（audit_package）— 审稿工作流 R2。

核验"论文声明"与"投稿包事实"是否一致：
  1. 论文 tex 引用的产物文件（\\texttt{...} 内路径）是否都在 zip 内
  2. Windows 绝对路径泄漏（匿名/规范违反）
  3. 文件数 / 清单条目数声明 vs zip 实际
输出 audit_report.json + audit_report.md。

用法:
    python audit_package.py --zip submission.zip --tex main.tex --out audit_out
    python audit_package.py --selftest
"""
from __future__ import annotations

import argparse
import io
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

TEXT_EXTS = {".tex", ".md", ".json", ".jsonl", ".txt", ".py", ".sh", ".bst", ".sty", ".bib", ".cfg", ".toml", ".yml", ".yaml"}
PATH_EXT = {".json", ".jsonl", ".md", ".py", ".sh", ".txt", ".tex", ".pdf", ".png", ".csv", ".log", ".ipynb", ".zip"}
DIR_HINTS = ("out_", "results/", "workspaces/", "evidence/", "reports/", "paper/", "scripts/", "figures/", "data/")

# 驱动器路径：F:\x\y / F:\\x\\y（JSON 转义）/ F:/x/y；UNC：\\server\share（2-4 个反斜杠开头）
# 2026-08-27 收紧：真 Windows 绝对路径 = 大写盘符 + ≥2 段反斜杠 + 首段非转义起始。
# 单段 `i:\hat`/`F:\hat`/`e:\MessageBreak`、小写 `s:\n\n`/`y:\n` 等 LaTeX 数学记号/JSON 转义/正则字面量不再误报；
# F:\deepseek\...、E:\AGI-KIT\...、C:\Program... 仍正常捕获。
WIN_PATH_RE = re.compile(r"[A-Z]:\\(?![nrtbfv0xu])[^\\\s\"',;)}\]]+\\[^\\\s\"',;)}\]]+")
UNC_RE = re.compile(r"\\{2,4}[A-Za-z0-9_.\-]{2,}\\+(?![nrtbfv0xu\"'\\/])[^\s\"',;)\}\]]+")  # 2026-09-06: 分隔符后为转义序列(\n等)时不算UNC路径（JSON内LaTeX如\\infty误报）
# 诚实性关键词（产物 JSON note/value 常见）：R5 人工审查的机械前置
HONESTY_HINTS = ("simulated", "simulate", "mock", "synthetic", "placeholder", "dummy", "fake", "toy", "pending", "TODO", "FIXME", "draft only", "not real")
CLAIM_PATTERNS = [
    # 只有 "N files" 是 zip 条目数声明，可与实际比对
    (re.compile(r"(\d+)\s*files\b", re.I), "zip_entries"),
    # manifest / 哈希 / 重算口径的声明只登记，需人工对照对应产物文件，不与 zip 总数比
    (re.compile(r"(\d+)\s*-?\s*entry\b", re.I), "manifest_entries"),
    (re.compile(r"(\d+)\s*(?:SHA-?256\s*)?hash(?:es)?", re.I), "manifest_hashes"),
    (re.compile(r"(\d+)\s*/\s*\d+\s*(?:checks|recompute)", re.I), "recompute_checks"),
]
# tex 里的引用形态：\texttt{out\_p5/P5\_MUSE\_FINAL.json} 或 \texttt{p3\_aggregate.py}
TEXTTT_RE = re.compile(r"\\texttt\{([^{}]*)\}")
# 外部 URL（scheme:// 或 domain.tld/path）不是投稿包内文件引用，须豁免，否则误报 MISSING
URL_RE = re.compile(
    r"^(?:[a-zA-Z][a-zA-Z0-9+.\-]*://|"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9\-.]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}(?::\d+)?(?:/|$))"
)


def unescape_latex(s: str) -> str:
    return s.replace(r"\_", "_").replace(r"\&", "&").replace(r"\%", "%").replace(r"\#", "#").replace("``", "`").replace("''", "'")


def extract_referenced_paths(tex: str) -> list[dict]:
    """从 \\texttt{...} 提取疑似文件/目录引用。"""
    refs = []
    for m in TEXTTT_RE.finditer(tex):
        raw = m.group(1)
        p = unescape_latex(raw)
        looks_like_path = (
            "/" in p
            or (Path(p).suffix.lower() in PATH_EXT and len(p) < 120)
            or any(p.startswith(h) for h in DIR_HINTS)
        )
        if not looks_like_path or p.endswith(".") or " " in p:
            continue
        if URL_RE.match(p):
            continue
        refs.append({"raw": raw, "path": p, "line": tex[: m.start()].count("\n") + 1})
    return refs


def match_ref(path: str, entries: list[str]) -> dict:
    """匹配策略：精确 → 目录前缀 → basename。"""
    norm = path.strip("/").replace("\\", "/")
    exact = [e for e in entries if e == norm or e.endswith("/" + norm)]
    if exact:
        return {"status": "exact", "matched": exact[:3]}
    if any(e.startswith(norm + "/") for e in entries):
        hits = [e for e in entries if e.startswith(norm + "/")][:3]
        return {"status": "prefix-dir", "matched": hits}
    base = norm.rsplit("/", 1)[-1]
    by_base = [e for e in entries if e.rsplit("/", 1)[-1] == base]
    if by_base:
        return {"status": "basename", "matched": by_base[:3]}
    if base.startswith("p3_") or base.startswith("calib_") or base.startswith("gold_"):
        stem = base.rsplit(".", 1)[0]
        loose = [e for e in entries if stem in e][:3]
        if loose:
            return {"status": "stem", "matched": loose}
    return {"status": "MISSING", "matched": []}


def scan_local_paths(name: str, text: str) -> list[dict]:
    leaks = []
    for i, line in enumerate(text.splitlines(), 1):
        for m in WIN_PATH_RE.finditer(line):
            snippet = line[max(0, m.start() - 30) : m.end() + 30].strip()
            leaks.append({"file": name, "line": i, "leak": m.group(0), "context": snippet})
        for m in UNC_RE.finditer(line):
            snippet = line[max(0, m.start() - 30) : m.end() + 30].strip()
            leaks.append({"file": name, "line": i, "leak": m.group(0), "context": snippet})
    return leaks


def scan_json_string_values(name: str, data, prefix="") -> list[dict]:
    """JSON 结构化扫描：值已解转义，正则干净且能报告泄漏所在的 key。"""
    leaks = []
    if isinstance(data, dict):
        for k, v in data.items():
            leaks += scan_json_string_values(name, v, f"{prefix}.{k}" if prefix else k)
    elif isinstance(data, list):
        for i, v in enumerate(data):
            leaks += scan_json_string_values(name, v, f"{prefix}[{i}]")
    elif isinstance(data, str):
        for m in WIN_PATH_RE.finditer(data):
            leaks.append({"file": name, "line": None, "leak": m.group(0), "context": prefix})
    return leaks


def scan_zip_entry(name: str, raw: bytes) -> list[dict]:
    """按文件类型选择扫描方式：JSON/JSONL 走结构化（避免转义误报、报告 key），其余走文本。"""
    ext = Path(name).suffix.lower()
    if ext == ".json":
        try:
            return scan_json_string_values(name, json.loads(raw.decode("utf-8")))
        except Exception:
            pass
    if ext == ".jsonl":
        out = []
        for i, line in enumerate(raw.decode("utf-8", errors="replace").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                for leak in scan_json_string_values(f"{name}:L{i}", json.loads(line)):
                    leak["line"] = i
                    out.append(leak)
            except Exception:
                out += scan_local_paths(f"{name}:L{i}", line)
        return out
    return scan_local_paths(name, raw.decode("utf-8", errors="replace"))


def extract_count_claims(tex: str) -> list[dict]:
    claims = []
    for pat, kind in CLAIM_PATTERNS:
        for m in pat.finditer(tex):
            claims.append({"claim": m.group(0).strip(), "declared": int(m.group(1)), "kind": kind, "line": tex[: m.start()].count("\n") + 1})
    # 去重
    seen, out = set(), []
    for c in claims:
        key = (c["claim"], c["line"])
        if key not in seen:
            seen.add(key)
            out.append(c)
    return out


def audit(zip_path: Path, tex_path: Path) -> dict:
    tex = tex_path.read_text(encoding="utf-8", errors="replace")
    with zipfile.ZipFile(zip_path) as zf:
        entries = [i.filename for i in zf.infolist() if not i.is_dir()]
        # 封包-磁盘同步检查：zip 内同名 tex 与磁盘 tex 是否为同一版本
        tex_base = tex_path.name
        zip_tex_entry = next((e for e in entries if e == tex_base or e.endswith("/" + tex_base)), None)
        zip_tex_content, desync = None, False
        if zip_tex_entry:
            zip_tex_content = zf.read(zip_tex_entry).decode("utf-8", errors="replace")
            norm = lambda s: s.replace("\r\n", "\n").replace("\r", "\n")
            desync = norm(zip_tex_content) != norm(tex)
        refs = extract_referenced_paths(tex)
        for r in refs:
            r.update(match_ref(r["path"], entries))

        leaks = scan_local_paths("paper/" + tex_path.name, tex)
        for info in zf.infolist():
            if info.is_dir() or info.file_size > 1_000_000:
                continue
            if Path(info.filename).suffix.lower() not in TEXT_EXTS:
                continue
            try:
                leaks += scan_zip_entry(info.filename, zf.read(info))
            except Exception:
                continue

    claims = extract_count_claims(tex)
    n_entries = len(entries)
    for c in claims:
        c["actual_entries"] = n_entries
        if c["kind"] == "zip_entries":
            c["matches_actual"] = c["declared"] == n_entries
        else:
            c["matches_actual"] = None  # 口径不同（manifest/哈希/重算），需人工对照对应产物
    zip_claims = [c for c in claims if c["kind"] == "zip_entries"]
    # 封包内旧版声明的核对（投稿事实口径）：desync 时磁盘声明可能已修复而 zip 未重封
    inpackage_claims = extract_count_claims(zip_tex_content) if zip_tex_content else []
    for c in inpackage_claims:
        c["actual_entries"] = n_entries
        if c["kind"] == "zip_entries":
            c["matches_actual"] = c["declared"] == n_entries
        else:
            c["matches_actual"] = None
        c["in_package_tex"] = True

    missing = [r for r in refs if r["status"] == "MISSING"]
    report = {
        "meta": {
            "zip": str(zip_path), "tex": str(tex_path), "entries": n_entries,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "referenced_paths": refs,
        "missing_refs": missing,
        "local_path_leaks": leaks,
        "count_claims": claims,
        "inpackage_tex": {
            "entry": zip_tex_entry,
            "desync_with_disk": desync,
            "count_claims": inpackage_claims,
        },
        "summary": {
            "refs_total": len(refs),
            "refs_missing": len(missing),
            "leaks": len(leaks),
            "count_claims": len(claims),
            "count_claims_mismatched": sum(1 for c in zip_claims if not c["matches_actual"]),
            "tex_desync": desync,
            "verdict": "CRITICAL" if missing else ("MAJOR" if leaks or desync or any(c["matches_actual"] is False for c in zip_claims) else "PASS"),
        },
    }
    return report


def write_md(report: dict, out_md: Path) -> None:
    s = report["summary"]
    lines = [
        "# 投稿包证据审计报告（R2）",
        "",
        f"- 投稿包：`{report['meta']['zip']}`（{report['meta']['entries']} 条目）",
        f"- 论文：`{report['meta']['tex']}`",
        f"- 结论：**{s['verdict']}**（引用缺失 {s['refs_missing']}/{s['refs_total']}，路径泄漏 {s['leaks']}，声明不符 {s['count_claims_mismatched']}/{s['count_claims']}）",
        "",
        "## 1. 论文引用但包内缺失（→ Critical）",
        "",
    ]
    if report["missing_refs"]:
        lines += [f"- L{r['line']}: `{r['path']}`" for r in report["missing_refs"]]
    else:
        lines.append("- 无")
    lines += ["", "## 2. 引用匹配明细", "", "| 引用 | 行 | 状态 | 匹配条目 |", "|---|---|---|---|"]
    for r in report["referenced_paths"]:
        lines.append(f"| `{r['path']}` | {r['line']} | {r['status']} | {', '.join('`'+m+'`' for m in r['matched'][:2]) or '-'} |")
    lines += ["", "## 3. Windows 绝对路径泄漏（→ Major，匿名/规范）", ""]
    if report["local_path_leaks"]:
        lines += [f"- `{l['file']}` L{l['line']}: `{l['leak']}`" for l in report["local_path_leaks"][:50]]
    else:
        lines.append("- 无")
    lines += [
        "",
        "## 4. 封包-磁盘同步检查",
        "",
    ]
    ip = report.get("inpackage_tex", {})
    if ip.get("entry"):
        mark = "❌ DESYNC（zip 内为旧版，磁盘已修订，需重封包）" if ip.get("desync_with_disk") else "✅ 一致"
        lines.append(f"- zip 内 tex：`{ip['entry']}` —— {mark}")
        if ip.get("desync_with_disk") and ip.get("count_claims"):
            lines += ["", "封包内旧版声明核对（投稿事实口径）：", "", "| 声明原文 | 口径 | 声明值 | zip 实际条目数 | 判定 |", "|---|---|---|---|---|"]
            for c in ip["count_claims"]:
                m = "✅" if c["matches_actual"] else ("❌" if c["matches_actual"] is False else "⚠️ 人工核对")
                lines.append(f"| `{c['claim']}` | {c['kind']} | {c['declared']} | {c['actual_entries']} | {m} |")
    else:
        lines.append("- zip 内未找到与磁盘同名的 tex（跳过同步检查）")
    lines += ["", "## 5. 磁盘版 tex 声明 vs zip 实际", ""]
    if report["count_claims"]:
        lines += ["| 声明原文 | 口径 | 声明值 | zip 实际条目数 | 判定 |", "|---|---|---|---|---|"]
        for c in report["count_claims"]:
            mark = "✅" if c["matches_actual"] else ("❌" if c["matches_actual"] is False else "⚠️ 人工核对")
            lines.append(f"| `{c['claim']}` | {c['kind']} | {c['declared']} | {c['actual_entries']} | {mark} |")
    else:
        lines.append("- 论文未出现可解析的文件数声明")
    out_md.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    import tempfile

    tmp = Path(tempfile.mkdtemp())
    tex = tmp / "main.tex"
    tex.write_text(
        r"Results are in \texttt{results/p3\_stats.json} and \texttt{out\_p5/P5\_MUSE\_FINAL.json}."
        r" Gateway at \texttt{opencode.ai/zen/go/v1}. The package has 3 files and 2-entry manifest."
        r" Path leak: \texttt{F:\deepseek\work}.",
        encoding="utf-8",
    )
    zp = tmp / "sub.zip"
    old_tex = r"Old version: \texttt{results/p3\_stats.json} with 2 files."
    with zipfile.ZipFile(zp, "w") as zf:
        zf.writestr("results/p3_stats.json", '{"x": 1}')
        zf.writestr("paper/main.tex", old_tex)
    rep = audit(zp, tex)
    assert rep["summary"]["refs_total"] == 2, rep["summary"]  # 外部 URL 豁免，不计为包内引用
    assert rep["summary"]["refs_missing"] == 1, rep["summary"]
    assert rep["summary"]["leaks"] >= 1
    assert rep["summary"]["tex_desync"] is True
    assert rep["inpackage_tex"]["count_claims"][0]["declared"] == 2
    assert any(c["matches_actual"] is False for c in rep["count_claims"] if c["kind"] == "zip_entries")
    assert all(c["matches_actual"] is None for c in rep["count_claims"] if c["kind"] != "zip_entries")
    print("audit_package selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--zip", type=Path)
    ap.add_argument("--tex", type=Path)
    ap.add_argument("--out", type=Path, default=Path("audit_out"))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not (args.zip and args.tex):
        ap.error("--zip and --tex are required (or --selftest)")
    report = audit(args.zip, args.tex)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "audit_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(report, args.out / "audit_report.md")
    s = report["summary"]
    print(f"verdict={s['verdict']} refs={s['refs_total']} missing={s['refs_missing']} leaks={s['leaks']} claims_mismatch={s['count_claims_mismatched']} tex_desync={s['tex_desync']}")
    if s["tex_desync"]:
        print(f"  DESYNC: zip 内 tex 旧于磁盘版 -> {report['inpackage_tex']['entry']}（需重封包）")
    for r in report["missing_refs"]:
        print(f"  MISSING L{r['line']}: {r['path']}")
    for l in report["local_path_leaks"][:10]:
        print(f"  LEAK {l['file']} L{l['line']}: {l['leak']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
