#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write the planted-defect packages and labels.json.

This script does not import or run any review stage. labels.json records
sha256 of the package bytes and the gate expectations taken from the stage
contracts (PASS / WARN / FAIL). Score only after that file is committed.
"""
from __future__ import annotations

import hashlib
import json
import math
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PKG = ROOT / "packages"
STAGES = ["R1b", "R1d", "R2", "R2b", "R2c", "R2d", "R3", "R4", "R5"]
ZIP_DATE = (2026, 1, 1, 0, 0, 0)


def mcnemar_exact_p(b: int, d: int) -> float:
    n = b + d
    tail = sum(math.comb(n, i) for i in range(0, min(b, d) + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def wilson_ci(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    z2 = z * z
    center = (k + z2 / 2) / (n + z2)
    half = z * math.sqrt(k * (n - k) / n + z2 / 4) / (n + z2)
    return center - half, center + half


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dumps(obj) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def zip_bytes(members: list[tuple[str, bytes]]) -> bytes:
    import io
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, data in members:
            info = zipfile.ZipInfo(name, date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o644 << 16
            zf.writestr(info, data)
    return buf.getvalue()


BIB = """@article{vaswani2017,
  title = {Attention Is All You Need},
  author = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N. and Kaiser, Lukasz and Polosukhin, Illia},
  year = {2017},
  eprint = {1706.03762}
}
"""


def tex_of(*, acc: str, arith: str, p_tok: str, w_lo: str, w_hi: str,
           extra_method: str, extra_results: str, extra_cite: str) -> str:
    return (
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "\\begin{abstract}\n"
        "Synthetic submission used only as a mechanical-check fixture.\n"
        "\\end{abstract}\n"
        "\\section{Introduction}\n"
        "The study compares two systems on a fixed split.\n"
        "\\section{Related Work}\n"
        f"Prior work is cited as \\cite{{{extra_cite}}}.\n"
        "\\section{Method}\n"
        "Counts and intervals are stored in \\texttt{results/stats.json}.\n"
        f"{extra_method}\n"
        "\\section{Results}\n"
        "Held-out accuracy is listed in the table.\n"
        f"Exact McNemar $p={p_tok}$ ($b=1$, $c=9$).\n"
        f"Wilson CI $[{w_lo}, {w_hi}]$.\n"
        f"Inline check: 45/50 = {arith}.\n"
        f"{extra_results}\n"
        "\\begin{table}\n"
        "\\caption{Held-out accuracy.}\n"
        "\\label{tab:acc}\n"
        "\\begin{tabular}{lc}\n"
        "\\toprule\n"
        "Model & Acc \\\\\n"
        "\\midrule\n"
        f"A & {acc} \\\\\n"
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "\\end{table}\n"
        "\\section{Discussion}\n"
        "The table is the only accuracy display.\n"
        "\\section{Limitations}\n"
        "The sample is synthetic.\n"
        "\\section{Conclusion}\n"
        "No further claim is made.\n"
        "\\end{document}\n"
    )


def stats_of(*, acc: float, arith: float, claimed_p: float,
             ci: list[float], agreement: dict | None) -> dict:
    obj = {
        "arith_check": {"ratio": arith},
        "mcnemar_pair": {"b": 1, "c": 9, "p": claimed_p, "test": "mcnemar"},
        "table_acc": {"acc": acc},
        "wilson_gold": {"ci": ci, "k": 8, "method": "wilson", "n": 10},
    }
    if agreement is not None:
        obj["agreement"] = agreement
    return obj


def manifest_of(tex: bytes, stats: bytes, *, bad_stats_sha: bool) -> dict:
    stats_sha = "0" * 64 if bad_stats_sha else sha256_bytes(stats)
    return {
        "files": [
            {"path": "main.tex", "sha256": sha256_bytes(tex), "size": len(tex)},
            {"path": "results/stats.json", "sha256": stats_sha, "size": len(stats)},
        ],
        "root": ".",
    }


def expect_all_pass() -> dict:
    return {s: "PASS" for s in STAGES}


def write_case(name: str, spec: dict) -> dict:
    true_p = mcnemar_exact_p(1, 9)
    lo, hi = wilson_ci(8, 10)
    # 4 d.p. is within the checkers' 5e-4 tolerance of the recomputed interval.
    true_lo, true_hi = f"{lo:.4f}", f"{hi:.4f}"
    true_p_tok = f"{true_p:.4f}"  # 0.0215

    acc = spec.get("acc", "0.812")
    arith = spec.get("arith", "0.90")
    p_tok = spec.get("p_tok", true_p_tok)
    w_lo = spec.get("w_lo", true_lo)
    w_hi = spec.get("w_hi", true_hi)
    tex = tex_of(
        acc=acc,
        arith=arith,
        p_tok=p_tok,
        w_lo=w_lo,
        w_hi=w_hi,
        extra_method=spec.get("extra_method", ""),
        extra_results=spec.get("extra_results", ""),
        extra_cite=spec.get("extra_cite", "vaswani2017"),
    ).encode("utf-8")
    bib = BIB.encode("utf-8")
    agreement = spec.get("agreement")
    stats_obj = stats_of(
        acc=float(acc) if spec.get("json_acc") is None else spec["json_acc"],
        arith=float(arith),
        claimed_p=float(p_tok),
        ci=[float(w_lo), float(w_hi)],
        agreement=agreement,
    )
    stats = dumps(stats_obj)
    man = dumps(manifest_of(tex, stats, bad_stats_sha=spec.get("bad_hash", False)))
    blob = zip_bytes([
        ("main.tex", tex),
        ("refs.bib", bib),
        ("results/stats.json", stats),
        ("evidence_manifest.json", man),
    ])
    dest = PKG / name
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "evidence").mkdir(exist_ok=True)
    files = {
        "main.tex": tex,
        "refs.bib": bib,
        "evidence/stats.json": stats,
        "evidence_manifest.json": man,
        "submission.zip": blob,
    }
    hashes = {}
    for rel, data in files.items():
        path = dest / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        hashes[rel] = sha256_bytes(data)
    return {
        "role": spec["role"],
        "planted": spec["planted"],
        "primary_stage": spec["primary_stage"],
        "expect": spec["expect"],
        "files_sha256": hashes,
        "notes_before_scoring": spec.get("notes", ""),
    }


def main() -> None:
    true_p = mcnemar_exact_p(1, 9)
    lo, hi = wilson_ci(8, 10)
    if PKG.exists():
        for child in sorted(PKG.rglob("*"), reverse=True):
            if child.is_file():
                child.unlink()
    PKG.mkdir(parents=True, exist_ok=True)

    base_expect = expect_all_pass()
    cases_spec = [
        ("clean_control_a", {
            "role": "control",
            "planted": None,
            "primary_stage": None,
            "expect": base_expect,
            "acc": "0.812",
            "notes": "Clean control. Every decimal in main.tex is also in evidence/stats.json. Manifest hashes match the zip bytes. No simulation hint.",
        }),
        ("clean_control_b", {
            "role": "control",
            "planted": None,
            "primary_stage": None,
            "expect": base_expect,
            "acc": "0.640",
            "notes": "Second clean control with a different supported accuracy, so a single control cannot hide a systematic false positive.",
        }),
        ("missing_cited_file", {
            "role": "defect",
            "planted": "missing cited file",
            "primary_stage": "R2",
            "expect": {**base_expect, "R2": "not-PASS"},
            "extra_method": "The supplement is \\texttt{results/heldout.json}.",
            "notes": "results/heldout.json is cited from \\\\texttt and is absent from the zip and the manifest. R2 should not PASS. R2b should stay PASS because the manifest does not list the missing path.",
        }),
        ("hash_mismatch", {
            "role": "defect",
            "planted": "checklist hash mismatch",
            "primary_stage": "R2b",
            "expect": {**base_expect, "R2b": "not-PASS"},
            "bad_hash": True,
            "notes": "evidence_manifest.json records sha256 of results/stats.json as 64 zero digits. Size is the real size. File bytes in the zip are unchanged.",
        }),
        ("table_number_mismatch", {
            "role": "defect",
            "planted": "table number disagrees with results JSON",
            "primary_stage": "R2d",
            "expect": {**base_expect, "R2d": "not-PASS", "R3": "not-PASS"},
            "acc": "0.777",
            "json_acc": 0.812,
            "notes": "Table cell is 0.777. evidence/stats.json table_acc.acc stays 0.812, and 0.777 appears nowhere else. R2d should not PASS. R3 reads the same tex decimals, so a pending number is an expected co-detection, not a false positive.",
        }),
        ("arithmetic_error", {
            "role": "defect",
            "planted": "inline arithmetic error",
            "primary_stage": "R1d",
            "expect": {**base_expect, "R1d": "not-PASS"},
            "arith": "0.92",
            "notes": "45/50 is written as 0.92. The value 0.92 is also stored in arith_check.ratio so R3 can support the token. R1d is the stage that recomputes the expression.",
        }),
        ("stats_mcnemar_wilson", {
            "role": "defect",
            "planted": "wrong McNemar p and wrong Wilson interval versus raw counts",
            "primary_stage": "R4",
            "expect": {**base_expect, "R4": "not-PASS"},
            "p_tok": "0.5000",
            "w_lo": "0.1000",
            "w_hi": "0.2000",
            "notes": (
                f"Raw counts stay b=1,c=9 and k=8,n=10. Recomputed McNemar p is {true_p:.6f}; "
                f"recomputed Wilson interval is [{lo:.4f}, {hi:.4f}]. "
                "The paper and the JSON instead claim p=0.5000 and CI [0.1000, 0.2000]. "
                "R4 should not PASS. A Wilson record whose status is MATCH means the stored ci was not checked against the counts; report that status, do not relabel the case."
            ),
        }),
        ("undisclosed_simulation", {
            "role": "defect",
            "planted": "overclaim: undisclosed simulated annotator agreement",
            "primary_stage": "R5",
            "expect": {**base_expect, "R5": "not-PASS"},
            "agreement": {
                "alpha": 0.894,
                "note": "Second annotator simulated with disagreements",
            },
            "extra_results": "Annotator agreement alpha is 0.894.",
            "notes": "The evidence note says the annotator was simulated. The tex reports alpha 0.894 and the word annotator, and does not disclose a simulation. R5 should not PASS. Generic boast phrases are not part of this plant; R5's hint list is the contract.",
        }),
        ("ghost_citation", {
            "role": "defect",
            "planted": "unresolved citation",
            "primary_stage": "R1b",
            "expect": {**base_expect, "R1b": "not-PASS"},
            "extra_cite": "vaswani2017,notinthebib",
            "notes": "\\\\cite includes notinthebib, which is absent from refs.bib. Offline structural check only; no network.",
        }),
    ]

    cases = {}
    for name, spec in cases_spec:
        cases[name] = write_case(name, spec)

    labels = {
        "frozen_before_scoring": True,
        "scored": False,
        "stages": STAGES,
        "gate_vocabulary": {
            "PASS": "stage gate is PASS",
            "not-PASS": "stage gate is WARN, FAIL, or SKIP",
        },
        "how_expectations_were_chosen": (
            "Written from the stage contracts in scripts/ (missing tex path, hash mismatch, "
            "unsupported table cell, inline arithmetic, McNemar/Wilson recompute, honesty hint, "
            "ghost citation) before any score run. Do not edit expect after seeing scores. "
            "If a live gate disagrees, keep the label and record the miss or false positive."
        ),
        "recomputed_constants_used_to_build_fixtures": {
            "mcnemar_b": 1,
            "mcnemar_c": 9,
            "mcnemar_p": round(true_p, 6),
            "wilson_k": 8,
            "wilson_n": 10,
            "wilson_lo": round(lo, 6),
            "wilson_hi": round(hi, 6),
        },
        "cases": cases,
    }
    (ROOT / "labels.json").write_text(
        json.dumps(labels, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(cases)} packages and labels.json")
    print(f"mcnemar_p={true_p:.6f} wilson=[{lo:.4f}, {hi:.4f}]")


if __name__ == "__main__":
    main()
