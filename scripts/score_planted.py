#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Score the frozen planted-defect packages. Does not edit labels.json.

Writes benchmarks/planted_defects/results/matrix.json and matrix.md.
Exit 0 always when the stages run: a miss is a result, not a scorer failure.
`make check` compares this output to the committed matrix and to the README.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent
BENCH = ROOT / "benchmarks" / "planted_defects"
sys.path.insert(0, str(SCRIPTS))

import audit_package  # noqa: E402
import citation_check  # noqa: E402
import figure_check  # noqa: E402
import formula_check  # noqa: E402
import honesty_scan  # noqa: E402
import number_reconcile  # noqa: E402
import table_check  # noqa: E402
import verify_manifest  # noqa: E402

try:
    import stats_recompute  # noqa: E402
except Exception as exc:  # noqa: BLE001
    stats_recompute = None
    _STATS_ERR = f"{type(exc).__name__}: {exc}"
else:
    _STATS_ERR = ""


def gate_of(verdict: str | None) -> str:
    if verdict in ("CRITICAL", "ERROR"):
        return "FAIL"
    if verdict == "MAJOR":
        return "WARN"
    if verdict in ("SKIP",):
        return "SKIP"
    return "PASS"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def classify(expect: str, gate: str) -> str:
    if expect == "PASS" and gate == "PASS":
        return "tn"
    if expect == "PASS" and gate != "PASS":
        return "fp"
    if expect == "not-PASS" and gate == "PASS":
        return "fn"
    if expect == "not-PASS" and gate != "PASS":
        return "tp"
    return "unexpected"


def score_case(case_dir: Path) -> dict:
    tex = case_dir / "main.tex"
    bib = case_dir / "refs.bib"
    evidence = case_dir / "evidence"
    zip_path = case_dir / "submission.zip"
    out = {}

    def put(stage: str, verdict: str | None, detail: dict) -> None:
        gate = "SKIP" if verdict is None else gate_of(verdict)
        out[stage] = {"verdict": verdict, "gate": gate, "detail": detail}

    cit = citation_check.run_check(tex, bib, online=False)
    put("R1b", cit["summary"]["verdict"], {
        "ghost_citations": cit["summary"]["ghost_citations"],
        "structural_major": cit["summary"]["structural_major"],
    })

    form = formula_check.check(tex)
    put("R1d", form["summary"]["verdict"], {
        "arith_mismatch": form["summary"]["arith_mismatch"],
        "arith_total": form["summary"]["arith_total"],
    })

    audit = audit_package.audit(zip_path, tex)
    put("R2", audit["summary"]["verdict"], {
        "refs_missing": audit["summary"]["refs_missing"],
        "refs_total": audit["summary"]["refs_total"],
    })

    man = verify_manifest.verify(zip_path, None, None, tex)
    put("R2b", man["summary"].get("verdict"), {
        "hash_mismatch": man["summary"].get("hash_mismatch"),
        "missing": man["summary"].get("missing"),
        "ok": man["summary"].get("ok"),
    })

    fig = figure_check.check(tex, [evidence])
    put("R2c", fig["summary"]["verdict"], {
        "figures_referenced": fig["summary"].get("figures_referenced", fig["summary"].get("figures")),
        "missing": fig["summary"].get("missing_files", fig["summary"].get("missing")),
    })

    tab = table_check.check(tex, [evidence])
    put("R2d", tab["summary"]["verdict"], {
        "unsupported": tab["summary"]["unsupported"],
        "missing_inputs": tab["summary"]["missing_inputs"],
    })

    rec = number_reconcile.reconcile(tex, [evidence], adjudications=None)
    put("R3", rec["summary"]["verdict"], {
        "pending_review": rec["summary"]["pending_review"],
        "paper_decimals": rec["summary"]["paper_decimals"],
    })

    if stats_recompute is None:
        put("R4", None, {"error": _STATS_ERR, "records": 0})
    else:
        st = stats_recompute.recompute(tex, [evidence])
        put("R4", st["summary"]["verdict"], {
            "records": st["summary"]["records"],
            "match": st["summary"]["match"],
            "mismatch": st["summary"]["mismatch"],
            "not_in_paper": st["summary"]["not_in_paper"],
            "checks": [
                {"kind": c.get("kind"), "status": c.get("status"),
                 "json_path": c.get("json_path")}
                for c in st.get("checks", [])
            ],
        })

    hon = honesty_scan.scan(tex, [evidence])
    put("R5", hon["summary"]["verdict"], {
        "suspicious": hon["summary"]["suspicious"],
        "hint_hits": hon["summary"]["hint_hits"],
    })
    return out


def render_md(matrix: dict) -> str:
    stages = matrix["stages"]
    lines = [
        "# Planted-defect matrix",
        "",
        "Recomputed by `python3 scripts/score_planted.py`. Expectations are the frozen `labels.json` values.",
        "tp = planted stage did not PASS. fn = planted stage PASSed (miss). fp = control or off-stage flag. tn = expected PASS.",
        "",
        f"Labels commit: `{matrix['labels_commit']}`. Labels file was not edited by the scorer.",
        "",
        "| case | planted | " + " | ".join(stages) + " |",
        "|---|---|" + "---|" * len(stages),
    ]
    for name, case in matrix["cases"].items():
        cells = []
        for stage in stages:
            cell = case["stages"][stage]
            mark = {"tp": "TP", "fn": "MISS", "fp": "FP", "tn": "ok"}.get(cell["class"], cell["class"])
            cells.append(f"{cell['gate']} {mark}")
        planted = case["planted"] or "clean control"
        lines.append(f"| `{name}` | {planted} | " + " | ".join(cells) + " |")
    s = matrix["summary"]
    lines += [
        "",
        f"Counts: tp={s['tp']} fn={s['fn']} fp={s['fp']} tn={s['tn']}.",
        "",
    ]
    if matrix["misses"]:
        lines.append("Misses (frozen expectation not met; checkers were not changed):")
        lines.append("")
        for m in matrix["misses"]:
            lines.append(f"- `{m['case']}` {m['stage']}: expected {m['expect']}, got {m['gate']} ({m['class']})")
        lines.append("")
    else:
        lines.append("No misses and no false positives against the frozen expectations.")
        lines.append("")
    obs = matrix.get("observations") or []
    if obs:
        lines.append("Observations (not relabeled):")
        lines.append("")
        for o in obs:
            lines.append(f"- {o}")
        lines.append("")
    return "\n".join(lines)


def score(labels_commit: str) -> dict:
    labels = json.loads((BENCH / "labels.json").read_text(encoding="utf-8"))
    hash_errors = []
    cases_out = {}
    counts = {"tp": 0, "fn": 0, "fp": 0, "tn": 0}
    misses = []
    observations = []
    for name, spec in labels["cases"].items():
        case_dir = BENCH / "packages" / name
        file_hashes = {}
        for rel, want in spec["files_sha256"].items():
            got = sha256_file(case_dir / rel)
            file_hashes[rel] = got
            if got != want:
                hash_errors.append(f"{name}/{rel}: label {want} live {got}")
        raw = score_case(case_dir)
        stages = {}
        for stage in labels["stages"]:
            expect = spec["expect"][stage]
            gate = raw[stage]["gate"]
            kind = classify(expect, gate)
            counts[kind] = counts.get(kind, 0) + 1
            stages[stage] = {
                "expect": expect,
                "gate": gate,
                "verdict": raw[stage]["verdict"],
                "class": kind,
                "detail": raw[stage]["detail"],
            }
            if kind in ("fn", "fp"):
                misses.append({
                    "case": name, "stage": stage, "expect": expect,
                    "gate": gate, "class": kind,
                })
        if name == "stats_mcnemar_wilson":
            checks = raw["R4"]["detail"].get("checks") or []
            wilson = [c for c in checks if c.get("kind") == "wilson"]
            mcn = [c for c in checks if c.get("kind") == "mcnemar"]
            observations.append(
                "stats_mcnemar_wilson R4 checks: "
                + json.dumps({"mcnemar": mcn, "wilson": wilson}, ensure_ascii=False)
            )
            if wilson and all(c.get("status") != "MISMATCH" for c in wilson):
                observations.append(
                    "Wilson stored ci was not marked MISMATCH. "
                    "stats_recompute.py compares recomputed Wilson endpoints to tex decimals "
                    "and does not compare the stored ci field to those endpoints. "
                    "This is reported, not patched."
                )
        cases_out[name] = {
            "planted": spec["planted"],
            "primary_stage": spec["primary_stage"],
            "role": spec["role"],
            "files_sha256_ok": all(
                file_hashes[rel] == spec["files_sha256"][rel] for rel in spec["files_sha256"]
            ),
            "stages": stages,
        }
    matrix = {
        "labels_commit": labels_commit,
        "labels_scored_flag_at_freeze": labels.get("scored"),
        "stages": labels["stages"],
        "scipy": stats_recompute is not None,
        "hash_errors": hash_errors,
        "summary": counts,
        "misses": misses,
        "observations": observations,
        "cases": cases_out,
    }
    return matrix


def main() -> int:
    commit = sys.argv[1] if len(sys.argv) > 1 else "UNKNOWN"
    matrix = score(commit)
    out = BENCH / "results"
    out.mkdir(parents=True, exist_ok=True)
    (out / "matrix.json").write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md = render_md(matrix)
    (out / "matrix.md").write_text(md, encoding="utf-8")
    print(md)
    if matrix["hash_errors"]:
        print("HASH ERRORS (labels do not match package bytes):")
        for e in matrix["hash_errors"]:
            print(" ", e)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
