# -*- coding: utf-8 -*-
"""新颖性断言对照（novelty_check）— 审稿工作流 v1.3。

LLM 时代"增量贡献夸大/先行工作遗漏"是高频问题，机械对照比 LLM 更可信：
  1. 断言提取：从论文正文抽取新颖性断言句（first / novel / we propose / SOTA / no prior work / 据我们所知）
  2. 断言分级：强断言（first、no prior work、据我们所知）= 审稿人必查；弱断言（novel、we propose）= 信息性
  3. arXiv 检索：以标题+摘要关键词检索先行工作（API，sortBy=relevance）
  4. 相似对照：论文标题/摘要 vs 检索结果标题/摘要 token 重叠 → 找"近重复工作"
  5. 引用对照：近重复工作若未在 bib 中（标题相似度 < 0.6）→ MAJOR（先行工作未披露）
联网失败优雅降级 offline（不误报）；未提取到强断言时给出信息性提示。

判定：未披露近重复（title_sim ≥ 0.65 或 abstract_sim ≥ 0.45）= MAJOR；
     全部近重复已引用 = PASS；offline = SKIP；无断言 = MINOR 提示。

用法:
    python novelty_check.py --tex <main.tex> [--bib <refs.bib>] [--online] --out <outdir>
    python novelty_check.py --selftest
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

NS = {"atom": "http://www.w3.org/2005/Atom"}
UA = {"User-Agent": "review-workflow-novelty-check/1.3 (mailto:reviewer@example.org)"}

# 断言模式：句级匹配；strong=True 的断言审稿人必查。
# first 排除句首枚举用法（"First, we..."）：要求 "the first" 或 first+特征名词
CLAIM_PATTERNS = [
    ("first", re.compile(r"(?i)\bthe\s+first\b|\bfirst\s+(?:to|systematic|comprehensive|"
                          r"large[- ]scale|benchmark|study|work|framework|evaluation)"), True),
    ("no_prior", re.compile(r"(?i)\bno\s+(?:prior|previous|existing)\s+work\b"), True),
    ("tok", re.compile(r"(?i)\bto\s+the\s+best\s+of\s+our\s+knowledge\b"), True),
    ("novel", re.compile(r"(?i)\bnovel(?:ty)?\b"), False),
    ("propose", re.compile(r"(?i)\bwe\s+(?:propose|introduce|present|develop)\b"), False),
    ("sota", re.compile(r"(?i)\bstate[- ]of[- ]the[- ]art\b|\bSOTA\b"), False),
    ("uniquely", re.compile(r"(?i)\bunique(?:ly)?\b|\bunprecedented\b"), False),
]
STOPWORDS = {
    "a", "an", "the", "of", "for", "and", "or", "to", "in", "on", "with", "we",
    "our", "is", "are", "as", "by", "that", "this", "it", "its", "from", "at",
    "be", "which", "than", "then", "these", "those", "such", "can", "will",
    "using", "used", "use", "based", "via", "into", "not", "no", "but", "also",
}

TITLE_SIM_FLAG = 0.65     # 标题近重复阈值
ABS_SIM_FLAG = 0.45       # 摘要 token 重叠阈值
BIB_CITED_SIM = 0.6       # bib 内已引用的判定阈值
MAX_RESULTS = 15


def norm_tokens(s: str) -> list[str]:
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s.lower())
    return [w for w in s.split() if w not in STOPWORDS and len(w) > 1]


def token_similarity(a: str, b: str) -> float:
    wa, wb = set(norm_tokens(a)), set(norm_tokens(b))
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / min(len(wa), len(wb))  # 重叠率（含词序无关、短文友好）


def extract_title_abstract(tex: str) -> tuple[str, str]:
    t = re.search(r"\\title\*?\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", tex)
    title = t.group(1) if t else ""
    title = re.sub(r"\$[^$]*\$", " ", title)
    title = re.sub(r"\\[a-zA-Z]+|[{}~^_\\]", " ", title)
    title = re.sub(r"\s+", " ", title).strip()
    a = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S)
    if not a:  # PDF 伪 tex：行首 Abstract
        a = re.search(r"(?im)^\s*Abstract\b[:.\s]*(.+?)(?=\n\s*\n|\Z)", tex)
    abstract = a.group(1) if a else ""
    abstract = re.sub(r"\$[^$]*\$", " ", abstract)
    abstract = re.sub(r"\\[a-zA-Z]+|[{}~^_\\%]", " ", abstract)
    return title, re.sub(r"\s+", " ", abstract).strip()


def _strip_latex(tex: str) -> str:
    """整文清洗：保留 title/正文文本，剔除命令名、引用、数学环境（先清洗再切句）。"""
    s = re.sub(r"(?m)%.*$", "", tex)                    # 去注释
    s = re.sub(r"\\(?:input|include|includegraphics|bibliography|documentclass|usepackage"
               r"|newcommand|renewcommand|definecolor|date|maketitle|thanks)"
               r"(?:\[[^\]]*\])?\{[^{}]*\}", " ", s)
    s = re.sub(r"\\(?:cite|citep|citet|citealp|ref|eqref|label|url|href|footnote)\{[^{}]*\}", " ", s)
    s = re.sub(r"\$\$.*?\$\$", " EQ ", s, flags=re.S)
    s = re.sub(r"\$[^$]*\$", " EQ ", s)
    s = re.sub(r"\\(?:begin|end)\{[a-zA-Z*]+\}", "\n", s)
    s = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", " ", s)
    s = re.sub(r"[{}~^_]", " ", s)
    return s


def extract_claims(tex: str) -> list[dict]:
    """句级断言抽取：先整文清洗再切句；一句可命中多种断言（kinds 列表）。"""
    body = _strip_latex(tex)
    # 缩写句点保护：vs. / et al. / e.g. / Fig. 等不应切句
    body = re.sub(r"(?i)\b(vs|et al|e\.g|i\.e|fig|figs|sec|secs|eq|eqs|cf|resp|approx|no)\.", r"\1@DOT@", body)
    claims = []
    for sent in re.split(r"(?<=[.!?;])\s+", body):
        clean = re.sub(r"\s+", " ", sent.replace("@DOT@", ".")).strip()
        if len(clean) < 15:
            continue
        matched = [(kind, strong) for kind, pat, strong in CLAIM_PATTERNS if pat.search(clean)]
        if matched:
            claims.append({"kinds": [k for k, _ in matched],
                           "strong": any(s for _, s in matched),
                           "text": clean[:300]})
    return claims


def build_query(title: str, abstract: str) -> str:
    words = norm_tokens(title)[:8] or norm_tokens(abstract)[:10]
    return " ".join(words)


def search_arxiv(query: str, max_results: int = MAX_RESULTS) -> list[dict] | None:
    """返回 [{"id","title","summary","published"}]；网络失败返回 None（调用方降级）。"""
    if not query.strip():
        return []
    url = ("http://export.arxiv.org/api/query?search_query="
           + urllib.parse.quote(f"all:{query}")
           + f"&max_results={max_results}&sortBy=relevance")
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            xml = r.read().decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        return None
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return None
    out = []
    for entry in root.findall("atom:entry", NS):
        eid = (entry.findtext("atom:id", "", NS) or "").strip()
        out.append({
            "id": eid.split("/abs/")[-1] if "/abs/" in eid else eid,
            "title": re.sub(r"\s+", " ", (entry.findtext("atom:title", "", NS) or "").strip()),
            "summary": re.sub(r"\s+", " ", (entry.findtext("atom:summary", "", NS) or "").strip())[:600],
            "published": (entry.findtext("atom:published", "", NS) or "")[:10],
        })
    return out


def load_bib_titles(bib_path: Path | None) -> list[str]:
    if bib_path is None or not bib_path.is_file():
        return []
    text = bib_path.read_text(encoding="utf-8", errors="replace")
    return [re.sub(r"\s+", " ", m.group(1)).strip()
            for m in re.finditer(r"(?im)^\s*title\s*=\s*[{\"](.+?)[}\"],?\s*$", text)]


def find_related(title: str, abstract: str, results: list[dict],
                 bib_titles: list[str]) -> list[dict]:
    """检索结果中与论文近重复的工作，标注是否已在 bib 引用。"""
    related = []
    for r in results:
        if not r["title"]:
            continue
        sim_t = token_similarity(title, r["title"]) if title else 0.0
        sim_a = token_similarity(abstract, r["summary"]) if abstract else 0.0
        if sim_t < TITLE_SIM_FLAG and sim_a < ABS_SIM_FLAG:
            continue
        cited = any(token_similarity(bt, r["title"]) >= BIB_CITED_SIM for bt in bib_titles)
        related.append({
            **r,
            "title_sim": round(sim_t, 3),
            "abstract_sim": round(sim_a, 3),
            "cited": cited,
            "overlap_words": sorted(set(norm_tokens(title or abstract)) & set(norm_tokens(r["title"])))[:12],
        })
    return sorted(related, key=lambda x: -(x["title_sim"] + x["abstract_sim"]))


def run_check(tex_path: Path, bib_path: Path | None, online: bool) -> dict:
    tex = tex_path.read_text(encoding="utf-8", errors="replace")
    title, abstract = extract_title_abstract(tex)
    claims = extract_claims(tex)
    strong = [c for c in claims if c["strong"]]
    bib_titles = load_bib_titles(bib_path)

    report = {
        "meta": {"tex": str(tex_path), "bib": str(bib_path) if bib_path else None,
                 "online": online, "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")},
        "title": title,
        "claims": claims,
        "related": [],
        "summary": {"verdict": None, "claims_total": len(claims), "claims_strong": len(strong),
                    "related_found": 0, "related_uncited": 0, "online_results": 0},
    }
    s = report["summary"]

    if not claims:
        s["verdict"] = "MINOR"
        s["detail"] = "未提取到新颖性断言句（first/novel/we propose 等）——检查断言抽取是否失效"
        return report

    if not online:
        s["verdict"] = "SKIP"
        s["detail"] = "offline 模式：未联网检索先行工作（--online 开启）"
        return report

    query = build_query(title, abstract)
    report["query"] = query
    results = search_arxiv(query)
    if results is None:
        s["verdict"] = "SKIP"
        s["detail"] = "arXiv API 不可达，降级 offline（不误报）"
        return report

    related = find_related(title, abstract, results, bib_titles)
    uncited = [r for r in related if not r["cited"]]
    s["online_results"] = len(results)
    s["related_found"] = len(related)
    s["related_uncited"] = len(uncited)
    if uncited:
        s["verdict"] = "MAJOR"
        s["detail"] = (f"{len(uncited)} 篇近重复先行工作未引用（title_sim≥{TITLE_SIM_FLAG} 或 "
                       f"abstract_sim≥{ABS_SIM_FLAG}）→ 新颖性断言存疑，需人工对照")
    elif related:
        s["verdict"] = "PASS"
        s["detail"] = f"{len(related)} 篇近重复工作均已在 bib 中披露"
    else:
        s["verdict"] = "PASS"
        s["detail"] = f"检索 {len(results)} 条无近重复（标题/摘要相似度低于阈值）"
    report["related"] = related
    return report


def write_md(report: dict, out_md: Path) -> None:
    s = report["summary"]
    lines = [
        "# 新颖性断言对照报告（v1.3）",
        "",
        f"- 论文：`{report['meta']['tex']}`",
        f"- 标题：{report.get('title') or '（未提取到）'}",
        f"- 检索式：`{report.get('query', '（未联网）')}`",
        f"- 结论：**{s['verdict']}** —— {s.get('detail', '')}",
        "",
        "## 新颖性断言",
        "",
        f"- 共 {s['claims_total']} 句（强断言 {s['claims_strong']}：first / no prior work / 据我们所知）",
        "",
    ]
    for c in report["claims"][:20]:
        mark = "**[强]**" if c["strong"] else "[弱]"
        lines.append(f"- {mark} `{'+'.join(c['kinds'])}` {c['text'][:160]}")
    lines += ["", "## 近重复先行工作", ""]
    if report["related"]:
        lines += ["| arXiv | 标题相似 | 摘要相似 | 已引用 | 发表 | 标题 |", "|---|---|---|---|---|---|"]
        for r in report["related"]:
            lines.append(f"| {r['id']} | {r['title_sim']} | {r['abstract_sim']} | "
                         f"{'是' if r['cited'] else '**否**'} | {r['published']} | {r['title'][:80]} |")
        uncited = [r for r in report["related"] if not r["cited"]]
        if uncited:
            lines += ["", "### 未引用的近重复工作（需人工对照）", ""]
            for r in uncited:
                lines.append(f"- `{r['id']}` {r['title']}（title_sim={r['title_sim']}，"
                             f"abstract_sim={r['abstract_sim']}，重叠词：{', '.join(r['overlap_words'][:8])}）")
                lines.append(f"  - 摘要：{r['summary'][:200]}…")
    else:
        lines.append(f"- {'无（检索未见近重复）' if report['meta']['online'] else '未联网检索'}")
    out_md.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    tmp = Path(__import__("tempfile").mkdtemp())
    tex = tmp / "main.tex"
    tex.write_text(
        "\\documentclass{article}\n"
        "\\title{A Benchmark Suite for Small Model Reliability}\n"
        "\\begin{document}\n"
        "\\begin{abstract}We present a benchmark suite measuring reliability of small "
        "language models under stress. Our suite covers four scenarios.\n\\end{abstract}\n"
        "\\section{Introduction}\n"
        "To the best of our knowledge, this is the first benchmark suite for small model "
        "reliability under GPU stress.\n"
        "We propose a three-layer evaluation framework.\n"
        "Prior studies focused on accuracy only.\n"
        "\\section{Conclusion}Done.\n\\end{document}\n",
        encoding="utf-8")

    title, abstract = extract_title_abstract(tex.read_text(encoding="utf-8"))
    assert title == "A Benchmark Suite for Small Model Reliability", title
    assert "benchmark suite" in abstract.lower()

    claims = extract_claims(tex.read_text(encoding="utf-8"))
    kinds = {k for c in claims for k in c["kinds"]}
    assert "tok" in kinds and "first" in kinds, claims          # 强断言
    assert "propose" in kinds, claims                            # 弱断言
    strong = [c for c in claims if c["strong"]]
    assert len(strong) == 1 and set(strong[0]["kinds"]) == {"first", "tok"}, strong
    assert all("\\" not in c["text"] for c in claims), claims    # 句子已清洗 LaTeX 命令

    # 相似度单元
    assert token_similarity("Small Model Reliability Benchmark",
                            "A Benchmark for Reliability of Small Models") >= 0.65
    assert token_similarity("Quantum Chemistry Datasets", "Small Model Reliability Benchmark") < 0.3

    # 检索式：去停用词、截断
    q = build_query(title, abstract)
    assert "benchmark" in q and " the " not in f" {q} ", q

    # 近重复对照（mock 检索结果，不联网）
    mock = [
        {"id": "2401.00001", "title": "A Benchmark Suite for Small Language Model Reliability",
         "summary": "We present a benchmark suite measuring reliability of small language models.",
         "published": "2024-01-01"},
        {"id": "2401.00002", "title": "Quantum Error Correction with Surface Codes",
         "summary": "Surface codes achieve fault tolerance in quantum computing systems.",
         "published": "2024-02-01"},
    ]
    rel = find_related(title, abstract, mock, bib_titles=[])
    assert len(rel) == 1 and rel[0]["id"] == "2401.00001" and not rel[0]["cited"], rel
    # 同一篇但 bib 已有 → cited=True
    rel2 = find_related(title, abstract, mock,
                        bib_titles=["A Benchmark Suite for Small Language Model Reliability"])
    assert rel2[0]["cited"], rel2

    # offline run_check：有断言 → SKIP（不误报）
    rep = run_check(tex, None, online=False)
    assert rep["summary"]["verdict"] == "SKIP", rep["summary"]
    assert rep["summary"]["claims_total"] >= 2

    write_md(rep, tmp / "novelty_check.md")
    assert (tmp / "novelty_check.md").exists()
    print("novelty_check selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tex", type=Path)
    ap.add_argument("--bib", type=Path, help="可选：显式 bib（判定近重复是否已引用）")
    ap.add_argument("--online", action="store_true", help="联网检索 arXiv 先行工作（默认 offline）")
    ap.add_argument("--out", type=Path, default=Path("audit_out"))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.tex:
        ap.error("--tex required (or --selftest)")
    bib = args.bib
    if bib is None:
        cands = sorted(args.tex.parent.glob("*.bib"))
        bib = cands[0] if cands else None
    rep = run_check(args.tex, bib, args.online)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "novelty_check.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(rep, args.out / "novelty_check.md")
    s = rep["summary"]
    print(f"verdict={s['verdict']} claims={s['claims_total']}(strong {s['claims_strong']}) "
          f"related={s['related_found']} uncited={s['related_uncited']} (online={args.online})")
    print(f"-> {args.out / 'novelty_check.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
