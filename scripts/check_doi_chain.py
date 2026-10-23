# -*- coding: utf-8 -*-
"""check_doi_chain.py — DOI 一跳 + 五档分级（E337，nature-ref-verifier Step 2.0 移植）。

对 bib/文本中的 DOI 先打最便宜的一跳：GET api.crossref.org/works/<DOI>，
404=错号；200 则比标题/首作。输出五档：
verified / mismatch / not_found / suspicious / manual_needed。

用法: python check_doi_chain.py --bib <main.bib> [--out report.md]
exit 0=无 mismatch/suspicious；1=有（列清单）；2=infra（全部网络失败）；
not_found/manual_needed 只告警。静默失败陷阱（E370）：HTTP 200 但无 message/title
按 suspicious 计（上游以成功报失败）。
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path


def crossref(doi: str, timeout=20):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": "paper-pipeline/doi-chain"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return 200, json.loads(r.read().decode("utf-8", "replace"))
    except Exception as e:  # noqa: BLE001
        code = getattr(getattr(e, "response", None), "status", None)
        return code or -1, {}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bib", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    text = args.bib.read_text(encoding="utf-8", errors="replace")
    entries = re.findall(r"@\w+\{([^,]+),(.+?)(?=@\w+\{|\Z)", text, re.S)
    rows = []
    for key, body in entries:
        m = re.search(r"doi\s*=\s*[{""]([^}""]+)[}""]", body, re.I)
        mt = re.search(r"title\s*=\s*[{""](.+?)[}""]", body, re.I | re.S)
        if not m:
            rows.append((key.strip(), "manual_needed", "无 DOI 字段"))
            continue
        doi = m.group(1).strip()
        code, data = crossref(doi)
        if code == 404 or code == -1 and not data:
            rows.append((key.strip(), "not_found", f"Crossref {code}"))
            continue
        if code == 200 and not (data.get("message") or {}).get("title"):
            rows.append((key.strip(), "suspicious", "HTTP 200 但无 title（静默失败）"))
            continue
        try:
            msg = data.get("message", {})
            rt = norm(" ".join(msg.get("title", [])))
            bt = norm(re.sub(r"[{}]", "", (mt.group(1) if mt else ""))[:120])
            if bt and rt and (bt[:40] in rt or rt[:40] in bt):
                rows.append((key.strip(), "verified", doi))
            elif bt and rt:
                rows.append((key.strip(), "mismatch", f"bib={bt[:50]} vs cr={rt[:50]}"))
            else:
                rows.append((key.strip(), "suspicious", "标题缺失无法比对"))
        except Exception:  # noqa: BLE001
            rows.append((key.strip(), "manual_needed", "解析异常"))
    bad = [r for r in rows if r[1] in ("mismatch", "suspicious")]
    netfail = [r for r in rows if r[1] == "not_found" and "Crossref -1" in r[2]]
    lines = ["# DOI 链核验", ""]
    for k, g, d in rows:
        lines.append(f"- [{g}] {k}: {d}")
    rep = "\n".join(lines)
    print(rep)
    if args.out:
        args.out.write_text(rep, encoding="utf-8")
    print(f"\n共 {len(rows)} 条：mismatch/suspicious={len(bad)}")
    if rows and len(netfail) == len([r for r in rows if r[1] == "not_found"]) and len(rows) > 0 and not bad:
        if all(r[1] in ("not_found", "manual_needed") for r in rows) and netfail:
            print("INFRA: 全部网络失败（exit 2，非门禁失败）")
            return 2
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
