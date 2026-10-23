# -*- coding: utf-8 -*-
"""引用核验（citation_check）— 审稿工作流 v1.2。

防伪造引用（LLM 时代新风险）：
  1. 解析 .bib：结构检查（缺字段/重复 key/占位标题/幽灵引用——tex 里 \cite 但 bib 无条目）
  2. arXiv ID 联网核验：export.arxiv.org API 查存在性 + 标题相似度（防 ID 填错或张冠李戴）
  3. DOI 联网核验：doi.org handle API 解析
联网失败时优雅降级为仅结构检查（offline 模式，不误报）。

判定：not_found（ID 不存在）= Critical；title_mismatch = Major；offline = 信息性跳过。

用法:
    python citation_check.py --tex <main.tex> [--bib <refs.bib>] [--online] --out <outdir>
    python citation_check.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

BIB_RE = re.compile(r"\\bibliography\{([^}]+)\}")
CITE_RE = re.compile(r"\\(?:cite|citep|citet|citealp|citeauthor)\*?(?:\[[^\]]*\])?\{([^}]+)\}")
ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.I)
FIELD_RE = re.compile(r"^\s*(\w+)\s*=\s*[{\"](.+?)[}\"],?\s*$", re.I)
ARXIV_ID_RE = re.compile(r"(?:arxiv:)?(\d{4}\.\d{4,5})(v\d+)?", re.I)
DOI_RE = re.compile(r"10\.\d{4,9}/\S+")
PLACEHOLDER_TITLE = re.compile(r"^\s*(title|todo|tbd|placeholder|\?)\s*$", re.I)
NS = {"atom": "http://www.w3.org/2005/Atom"}
MAX_ONLINE = 40
UA = {"User-Agent": "review-workflow-citation-check/1.2 (mailto:reviewer@example.org)"}


def norm_title(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def title_similarity(a: str, b: str) -> float:
    wa, wb = set(norm_title(a).split()), set(norm_title(b).split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / max(len(wa), len(wb))


def parse_bib(bib_path: Path) -> list[dict]:
    entries = []
    text = bib_path.read_text(encoding="utf-8", errors="replace")
    # 去注释
    text = re.sub(r"(?m)^\s*%.*$", "", text)
    for m in ENTRY_RE.finditer(text):
        etype, key = m.group(1).lower(), m.group(2)
        chunk_start = m.end()
        # 条目范围：到下一个 @ 或文末
        nxt = text.find("@", chunk_start)
        chunk = text[chunk_start: nxt if nxt != -1 else len(text)]
        fields = {}
        brace = 0
        cur_key, buf = None, ""
        for line in chunk.splitlines():
            fm = re.match(r"\s*(\w+)\s*=\s*[{\"](.*)$", line, re.I)
            if fm and brace == 0 and cur_key is None:
                cur_key, buf = fm.group(1).lower(), fm.group(2)
                brace = buf.count("{") - buf.count("}")
                if brace <= 0 and buf.rstrip().rstrip(",").rstrip("}").rstrip('"'):
                    fields[cur_key] = buf.rstrip().rstrip(",").rstrip("}").rstrip('"').strip()
                    cur_key, brace = None, 0
                continue
            if cur_key is not None:
                buf += " " + line.strip()
                brace += line.count("{") - line.count("}")
                if brace <= 0:
                    fields[cur_key] = buf.rstrip().rstrip(",").rstrip("}").rstrip('"').strip()
                    cur_key = None
        identifiers = {}
        for fkey in ("eprint", "arxiv", "note", "url", "howpublished", "doi"):
            v = fields.get(fkey, "")
            if not v:
                continue
            am = ARXIV_ID_RE.search(v)
            if am and fkey in ("eprint", "arxiv", "note", "url", "howpublished"):
                identifiers["arxiv"] = identifiers.get("arxiv") or am.group(1)
            dm = DOI_RE.search(v)
            if dm and fkey in ("doi", "url", "note"):
                identifiers["doi"] = identifiers.get("doi") or dm.group(0).rstrip(".,)")
        entries.append({"key": key, "type": etype, "title": fields.get("title", ""),
                        "fields": list(fields.keys()), "identifiers": identifiers})
    return entries


def structural_check(tex_path: Path, bib_path: Path, entries: list[dict]) -> list[dict]:
    tex = tex_path.read_text(encoding="utf-8", errors="replace")
    cited = set()
    for m in CITE_RE.finditer(tex):
        cited.update(k.strip() for k in m.group(1).split(","))
    bib_keys = [e["key"] for e in entries]
    dup = sorted({k for k in bib_keys if bib_keys.count(k) > 1})
    issues = []
    for c in sorted(cited):
        if c not in bib_keys:
            issues.append({"kind": "ghost_citation", "key": c, "severity": "Major",
                           "detail": f"tex 引用 {c} 但 bib 无此条目"})
    for d in dup:
        issues.append({"kind": "duplicate_key", "key": d, "severity": "Minor", "detail": f"bib 中 key 重复：{d}"})
    for e in entries:
        if not e["title"] or PLACEHOLDER_TITLE.match(e["title"]):
            issues.append({"kind": "missing_title", "key": e["key"], "severity": "Major",
                           "detail": f"{e['key']} 缺 title 或为占位符"})
    return issues


def check_arxiv(arxiv_id: str, claimed_title: str) -> dict:
    url = f"http://export.arxiv.org/api/query?id_list={urllib.parse.quote(arxiv_id)}&max_results=1"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            xml = r.read().decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        return {"status": "offline", "detail": f"{type(e).__name__}: {e}"}
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return {"status": "offline", "detail": "XML parse error"}
    entry = root.find("atom:entry", NS)
    if entry is None:
        return {"status": "not_found", "detail": f"arXiv:{arxiv_id} 不存在（API 返回空 entry）"}
    title = (entry.findtext("atom:title", "", NS) or "").strip()
    title = re.sub(r"\s+", " ", title)
    if not title:
        return {"status": "not_found", "detail": f"arXiv:{arxiv_id} 无标题（疑似不存在）"}
    sim = title_similarity(claimed_title, title) if claimed_title else None
    return {
        "status": "verified",
        "api_title": title,
        "similarity": round(sim, 3) if sim is not None else None,
        "title_match": (sim >= 0.5) if sim is not None else None,
    }


def check_doi(doi: str) -> dict:
    url = f"https://doi.org/api/handles/{urllib.parse.quote(doi, safe='/')}"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
        if data.get("responseCode") == 1:
            return {"status": "verified"}
        return {"status": "not_found", "detail": f"DOI {doi} 解析失败（code {data.get('responseCode')}）"}
    except Exception as e:  # noqa: BLE001
        return {"status": "offline", "detail": f"{type(e).__name__}: {e}"}


def find_bib(tex_path: Path, explicit: Path | None) -> Path | None:
    if explicit:
        return explicit if explicit.exists() else None
    tex = tex_path.read_text(encoding="utf-8", errors="replace")
    m = BIB_RE.search(tex)
    if m:
        for name in m.group(1).split(","):
            p = tex_path.parent / (name.strip() + ".bib")
            if p.exists():
                return p
    # 回退：同目录任一 bib
    cands = sorted(tex_path.parent.glob("*.bib"))
    return cands[0] if cands else None


def run_check(tex_path: Path, bib_path: Path | None, online: bool) -> dict:
    if bib_path is None:
        return {"meta": {"tex": str(tex_path), "bib": None,
                         "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")},
                "summary": {"verdict": "ERROR", "detail": "未找到 bib 文件（--bib 显式指定）"}}
    entries = parse_bib(bib_path)
    issues = structural_check(tex_path, bib_path, entries)

    online_results = []
    if online:
        checked = 0
        for e in entries:
            if checked >= MAX_ONLINE:
                break
            ids = e["identifiers"]
            if "arxiv" in ids:
                online_results.append({**e, "id_kind": "arxiv", "id": ids["arxiv"],
                                       "result": check_arxiv(ids["arxiv"], e["title"])})
                checked += 1
                time.sleep(1.0)  # arXiv 礼貌限速
            elif "doi" in ids:
                online_results.append({**e, "id_kind": "doi", "id": ids["doi"],
                                       "result": check_doi(ids["doi"])})
                checked += 1

    n_ghost = sum(1 for i in issues if i["kind"] == "ghost_citation")
    n_maj = sum(1 for i in issues if i["severity"] == "Major")
    n_notfound = sum(1 for r in online_results if r["result"]["status"] == "not_found")
    n_mismatch = sum(1 for r in online_results if r["result"].get("title_match") is False)
    # 幽灵引用会导致 LaTeX 编译失败，任一即为 Major；ID 不存在 = 伪造引用 = Critical
    verdict = ("CRITICAL" if n_notfound else
               "MAJOR" if (n_maj or n_mismatch) else "PASS")
    return {
        "meta": {"tex": str(tex_path), "bib": str(bib_path), "online": online,
                 "entries": len(entries), "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")},
        "structural_issues": issues,
        "online_results": online_results,
        "summary": {"entries": len(entries), "ghost_citations": n_ghost, "structural_major": n_maj,
                    "not_found": n_notfound, "title_mismatch": n_mismatch,
                    "online_checked": len(online_results), "verdict": verdict},
    }


def write_md(report: dict, out_md: Path) -> None:
    if "summary" in report and "detail" in report["summary"]:
        out_md.write_text(f"# 引用核验报告\n\n- {report['summary']['detail']}\n", encoding="utf-8")
        return
    s = report["summary"]
    lines = [
        "# 引用核验报告（v1.2）",
        "",
        f"- 论文：`{report['meta']['tex']}`；bib：`{report['meta']['bib']}`（{s['entries']} 条）",
        f"- 模式：{'联网核验' if report['meta']['online'] else '仅结构检查（offline）'}",
        f"- 结论：**{s['verdict']}**（幽灵引用 {s['ghost_citations']}，结构 Major {s['structural_major']}，"
        f"ID 不存在 {s['not_found']}，标题不符 {s['title_mismatch']}，联网核验 {s['online_checked']} 条）",
        "",
        "## 结构问题",
        "",
    ]
    if report["structural_issues"]:
        lines += [f"- [{i['severity']}] {i['detail']}" for i in report["structural_issues"]]
    else:
        lines.append("- 无")
    lines += ["", "## 联网核验", ""]
    if report["online_results"]:
        lines += ["| key | 标识 | 状态 | 相似度 | 说明 |", "|---|---|---|---|---|"]
        for r in report["online_results"]:
            res = r["result"]
            sim = r["result"].get("similarity")
            lines.append(f"| `{r['key']}` | {r['id_kind']}:{r['id']} | {res['status']} | "
                         f"{sim if sim is not None else '-'} | {res.get('api_title') or res.get('detail', '')[:60]} |")
    else:
        lines.append("- 未执行（--online 未开启或无 ID 可查）")
    out_md.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    import tempfile

    tmp = Path(tempfile.mkdtemp())
    bib = tmp / "refs.bib"
    bib.write_text(
        "@article{good2020,\n"
        "  title={Attention Is All You Need},\n"
        "  author={Vaswani},\n"
        "  eprint={1706.03762},\n"
        "  year={2017}\n"
        "}\n"
        "@article{notitle,\n"
        "  title={title},\n"
        "  year={2020}\n"
        "}\n"
        "@misc{dup1, title={A}, year={2020}}\n"
        "@misc{dup1, title={B}, year={2021}}\n",
        encoding="utf-8",
    )
    tex = tmp / "main.tex"
    tex.write_text(
        r"\cite{good2020} and \citep{ghost2020} and \cite{notitle} and \cite{dup1}.",
        encoding="utf-8",
    )
    entries = parse_bib(bib)
    by_key = {e["key"]: e for e in entries}
    assert "good2020" in by_key and by_key["good2020"]["identifiers"].get("arxiv") == "1706.03762", by_key
    assert by_key["good2020"]["title"] == "Attention Is All You Need"
    issues = structural_check(tex, bib, entries)
    kinds = {i["kind"] for i in issues}
    assert "ghost_citation" in kinds, issues
    assert "missing_title" in kinds, issues
    assert "duplicate_key" in kinds, issues

    # offline 模式（不联网）
    rep = run_check(tex, bib, online=False)
    assert rep["summary"]["verdict"] == "MAJOR", rep["summary"]
    # 标题相似度单元
    assert title_similarity("Attention Is All You Need", "attention is all you need") == 1.0
    assert title_similarity("A B C", "X Y Z") == 0.0
    assert 0 < title_similarity("Deep Learning Review", "A Review of Deep Learning") < 1
    print("citation_check selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tex", type=Path)
    ap.add_argument("--bib", type=Path)
    ap.add_argument("--online", action="store_true", help="联网核验 arXiv/DOI（默认仅结构检查）")
    ap.add_argument("--out", type=Path, default=Path("audit_out"))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.tex:
        ap.error("--tex required (or --selftest)")
    bib = find_bib(args.tex, args.bib)
    rep = run_check(args.tex, bib, args.online)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "citation_check.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(rep, args.out / "citation_check.md")
    s = rep["summary"]
    print(f"verdict={s['verdict']} entries={s['entries']} ghost={s['ghost_citations']} "
          f"not_found={s['not_found']} title_mismatch={s['title_mismatch']} (online={args.online})")
    print(f"-> {args.out / 'citation_check.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
