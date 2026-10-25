# -*- coding: utf-8 -*-
"""Manifest 哈希核验（verify_manifest）— 审稿工作流 R2b。

核验"论文/manifest 声明"与"包内文件事实"：
  1. manifest 中每个条目的 path 是否存在于 zip
  2. zip 内该文件的 SHA-256 是否与 manifest 记录一致（byte-for-byte）
  3. size 是否一致
  4. 论文 tex 声明的 entry/hash 数 vs manifest 实际条数
支持 zip 内 manifest 或磁盘 manifest（--manifest 显式指定时验证磁盘文件）。

用法:
    python verify_manifest.py --zip submission.zip [--tex main.tex] [--out out_dir]
    python verify_manifest.py --manifest evidence_manifest.json --root /path/to/proj [--tex main.tex]
    python verify_manifest.py --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_NAMES = ("evidence_manifest.json", "ASSET_MANIFEST.json")
CLAIM_ENTRY_RE = re.compile(r"(\d+)\s*-?\s*entry", re.I)
CLAIM_HASH_RE = re.compile(r"(?<![A-Z0-9-])(\d+)\s*(?:SHA-?256\s*)?hash(?:es)?", re.I)  # 2026-09-06: SHA-256 本身不是计数声明


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def find_manifest(zf: zipfile.ZipFile) -> str | None:
    names = [i.filename for i in zf.infolist() if not i.is_dir()]
    for n in MANIFEST_NAMES:
        hit = next((e for e in names if e == n or e.endswith("/" + n)), None)
        if hit:
            return hit
    return None


def verify(zip_path: Path | None, manifest_path: Path | None, root: Path | None, tex_path: Path | None) -> dict:
    entries_checked: list[dict] = []
    manifest_meta: dict = {}
    manifest_entries: list[dict] = []
    src = None

    if zip_path is not None:
        with zipfile.ZipFile(zip_path) as zf:
            mf = manifest_path.name if manifest_path else None
            entry_name = mf or find_manifest(zf)
            if entry_name is None:
                return {"meta": {"zip": str(zip_path)}, "error": "manifest not found in zip (searched: " + ", ".join(MANIFEST_NAMES) + ")", "summary": {"verdict": "ERROR"}}
            raw = zf.read(entry_name)
            src = f"zip:{entry_name}"
            manifest = json.loads(raw.decode("utf-8"))
            zip_names = {i.filename: i for i in zf.infolist() if not i.is_dir()}
            manifest_meta = {"source": src, "declared_root": manifest.get("root")}
            manifest_entries = manifest.get("files", [])
            for rec in manifest_entries:
                p = str(rec.get("path", ""))
                want_sha = str(rec.get("sha256", "")).lower()
                want_size = rec.get("size")
                hit = zip_names.get(p) or next((v for k, v in zip_names.items() if k.endswith("/" + p)), None)
                if hit is None:
                    entries_checked.append({"path": p, "status": "MISSING", "expected_sha": want_sha[:16]})
                    continue
                actual_sha = sha256_bytes(zf.read(hit))
                ok_sha = actual_sha == want_sha
                ok_size = want_size is None or hit.file_size == want_size
                entries_checked.append({
                    "path": p,
                    "status": "OK" if (ok_sha and ok_size) else "HASH_MISMATCH",
                    "expected_sha": want_sha[:16], "actual_sha": actual_sha[:16],
                    "ok_sha": ok_sha, "ok_size": ok_size,
                })
    else:
        if not (manifest_path and root):
            raise ValueError("--manifest and --root required when no --zip")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        src = f"disk:{manifest_path}"
        manifest_meta = {"source": src, "declared_root": manifest.get("root")}
        manifest_entries = manifest.get("files", [])
        for rec in manifest_entries:
            p = str(rec.get("path", ""))
            f = root / p
            if not f.is_file():
                entries_checked.append({"path": p, "status": "MISSING", "expected_sha": str(rec.get("sha256", ""))[:16]})
                continue
            actual_sha = sha256_bytes(f.read_bytes())
            ok = actual_sha == str(rec.get("sha256", "")).lower()
            ok_size = rec.get("size") is None or f.stat().st_size == rec.get("size")
            entries_checked.append({
                "path": p, "status": "OK" if (ok and ok_size) else "HASH_MISMATCH",
                "expected_sha": str(rec.get("sha256", ""))[:16], "actual_sha": actual_sha[:16],
                "ok_sha": ok, "ok_size": ok_size,
            })

    n_ok = sum(1 for e in entries_checked if e["status"] == "OK")
    n_bad = sum(1 for e in entries_checked if e["status"] == "HASH_MISMATCH")
    n_miss = sum(1 for e in entries_checked if e["status"] == "MISSING")

    tex_claims = []
    if tex_path is not None:
        tex = tex_path.read_text(encoding="utf-8", errors="replace")
        for m in CLAIM_ENTRY_RE.finditer(tex):
            tex_claims.append({"claim": m.group(0), "declared": int(m.group(1)), "kind": "manifest_entries",
                               "matches_manifest": int(m.group(1)) == len(manifest_entries)})
        for m in CLAIM_HASH_RE.finditer(tex):
            tex_claims.append({"claim": m.group(0), "declared": int(m.group(1)), "kind": "manifest_hashes",
                               "matches_manifest": int(m.group(1)) == len(manifest_entries)})

    if n_bad or n_miss:
        verdict = "CRITICAL"
    elif tex_claims and any(c["matches_manifest"] is False for c in tex_claims):
        verdict = "MAJOR"
    else:
        verdict = "PASS"
    return {
        "meta": {
            "zip": str(zip_path) if zip_path else None,
            "tex": str(tex_path) if tex_path else None,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "manifest": manifest_meta,
        "entries_checked": entries_checked,
        "tex_claims": tex_claims,
        "summary": {
            "manifest_entries": len(manifest_entries),
            "ok": n_ok, "hash_mismatch": n_bad, "missing": n_miss,
            "verdict": verdict,
        },
    }


def write_md(report: dict, out_md: Path) -> None:
    s = report["summary"]
    if "error" in report:
        out_md.write_text(f"# Manifest 哈希核验（R2b）\n\n- ERROR: {report['error']}\n", encoding="utf-8")
        return
    lines = [
        "# Manifest 哈希核验（R2b）",
        "",
        f"- manifest：`{report['manifest']['source']}`（声明 root：`{report['manifest'].get('declared_root')}`）",
        f"- 结论：**{s['verdict']}** —— {s['ok']}/{s['manifest_entries']} 哈希一致，{s['hash_mismatch']} 不一致，{s['missing']} 缺失",
        "",
    ]
    if report["tex_claims"]:
        lines += ["## 论文声明 vs manifest 实际条数", "", "| 声明 | 口径 | 声明值 | manifest 条数 | 一致 |", "|---|---|---|---|---|"]
        for c in report["tex_claims"]:
            lines.append(f"| `{c['claim']}` | {c['kind']} | {c['declared']} | {s['manifest_entries']} | {'✅' if c['matches_manifest'] else '❌'} |")
        lines.append("")
    bad = [e for e in report["entries_checked"] if e["status"] != "OK"]
    lines += ["## 不一致/缺失明细", ""]
    if bad:
        lines += ["| path | 状态 | 期望 sha256(前16) | 实际 sha256(前16) |", "|---|---|---|---|"]
        lines += [f"| `{e['path']}` | {e['status']} | `{e.get('expected_sha','')}` | `{e.get('actual_sha','-')}` |" for e in bad]
    else:
        lines.append("- 无（全部 byte-for-byte 一致）")
    out_md.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    import tempfile

    tmp = Path(tempfile.mkdtemp())
    good = b"hello world"
    sha = hashlib.sha256(good).hexdigest()
    man = {"root": str(tmp), "files": [
        {"path": "results/a.json", "size": len(good), "sha256": sha},
        {"path": "results/b.json", "size": 3, "sha256": "0" * 64},
        {"path": "results/c.json", "size": 1, "sha256": "1" * 64},
    ]}
    zp = tmp / "sub.zip"
    with zipfile.ZipFile(zp, "w") as zf:
        zf.writestr("results/a.json", good)
        zf.writestr("results/b.json", b"xyz")
        zf.writestr("evidence_manifest.json", json.dumps(man))
    tex = tmp / "main.tex"
    tex.write_text("We have a 3-entry manifest and 3 hashes.", encoding="utf-8")
    rep = verify(zp, None, None, tex)
    s = rep["summary"]
    assert s["manifest_entries"] == 3 and s["ok"] == 1 and s["hash_mismatch"] == 1 and s["missing"] == 1, s
    assert s["verdict"] == "CRITICAL", s
    assert rep["tex_claims"][0]["matches_manifest"] is True
    # PASS 路径
    man2 = {"root": str(tmp), "files": [{"path": "results/a.json", "size": len(good), "sha256": sha}]}
    zp2 = tmp / "sub2.zip"
    with zipfile.ZipFile(zp2, "w") as zf:
        zf.writestr("results/a.json", good)
        zf.writestr("evidence_manifest.json", json.dumps(man2))
    rep2 = verify(zp2, None, None, None)
    assert rep2["summary"]["verdict"] == "PASS", rep2["summary"]
    print("verify_manifest selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--zip", type=Path)
    ap.add_argument("--manifest", type=Path, help="manifest 路径（zip 内 basename 或磁盘全路径+--root）")
    ap.add_argument("--root", type=Path, help="磁盘模式：manifest 条目的根目录")
    ap.add_argument("--tex", type=Path)
    ap.add_argument("--out", type=Path, default=Path("audit_out"))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.zip and not (args.manifest and args.root):
        ap.error("need --zip, or --manifest + --root (or --selftest)")
    report = verify(args.zip, args.manifest, args.root, args.tex)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "verify_manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(report, args.out / "verify_manifest.md")
    s = report["summary"]
    print(f"verdict={s['verdict']} manifest_entries={s['manifest_entries']} ok={s['ok']} hash_mismatch={s['hash_mismatch']} missing={s['missing']}")
    for e in report.get("entries_checked", []):
        if e["status"] != "OK":
            print(f"  {e['status']}: {e['path']}")
    for c in report.get("tex_claims", []):
        if c["matches_manifest"] is False:
            print(f"  CLAIM MISMATCH: {c['claim']} vs manifest {s['manifest_entries']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
