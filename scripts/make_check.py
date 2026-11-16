#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline check. No network.

Fails when the planted-defect rerun, the README copies, the version strings,
or the stored TMLR arithmetic disagree. A miss that is already written into
the committed matrix is not by itself a failure: hiding it would be.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import score_planted  # noqa: E402


def extract(text: str, begin: str, end: str) -> str:
    if begin not in text or end not in text:
        raise ValueError(f"missing markers {begin} … {end}")
    a = text.index(begin) + len(begin)
    b = text.index(end, a)
    return text[a:b].strip()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def calibration_facts() -> dict:
    report = load_json(ROOT / "examples/tmlr_calibration/cal_results/calibration_report.json")
    pairs = load_json(ROOT / "examples/tmlr_calibration/cal_results/calibrations.json")
    try:
        from scipy.stats import spearmanr
    except ImportError as exc:
        raise SystemExit(f"scipy is required for make check (R4 and the stored Spearman): {exc}") from exc
    yes = [e["yes_rate"] for e in pairs]
    rigor = [e["prism_dims"]["R"] for e in pairs]
    rho, p = spearmanr(rigor, yes)
    human = [e["human"] for e in pairs]
    suggested = [e["suggested"] for e in pairs]
    bias = sum(h - s for h, s in zip(human, suggested)) / len(pairs)
    mae = sum(abs(h - s) for h, s in zip(human, suggested)) / len(pairs)
    decisions = {e.get("decision") for e in pairs}
    accept_only = bool(decisions) and all(str(d).startswith("Accept") for d in decisions)
    stored = report["rank_consistency"]["prism_dims_vs_yesrate"]["R"]
    return {
        "n": len(pairs),
        "stored_rho": stored["spearman"],
        "stored_p": stored["p"],
        "rho": float(rho),
        "p": float(p),
        "bias_stored": report["metrics"]["bias"],
        "mae_stored": report["metrics"]["mae"],
        "bias": bias,
        "mae": mae,
        "suggested_unique": sorted(set(suggested)),
        "accept_only": accept_only,
        "report_n": report["metrics"]["pairs"],
    }


def calibration_block(facts: dict) -> str:
    return "\n".join([
        f"n: {facts['n']}",
        f"prism_R_spearman_stored: {facts['stored_rho']}",
        f"prism_R_p_stored: {facts['stored_p']}",
        f"prism_R_spearman_recomputed: {facts['rho']:.6f}",
        f"prism_R_p_recomputed: {facts['p']:.6f}",
        f"bias_stored: {facts['bias_stored']}",
        f"mae_stored: {facts['mae_stored']}",
        f"bias_recomputed: {facts['bias']:.2f}",
        f"mae_recomputed: {facts['mae']:.2f}",
        f"suggested_unique: {facts['suggested_unique']}",
        f"accept_only: {str(facts['accept_only']).lower()}",
        "scope: stored n=6 accept-side table; not a new OpenReview pull; suggested score is constant so correlation vs human is undefined",
    ])


def dump_facts() -> dict:
    dump = load_json(ROOT / "examples/tmlr_calibration/tmlr_dump.json")
    papers = dump["papers"]
    keys = set()
    long_strings = 0
    for paper in papers:
        for review in paper.get("reviews") or []:
            keys |= set(review)
            for value in review.values():
                if isinstance(value, str) and len(value) > 40:
                    long_strings += 1
    pdfs = list((ROOT / "examples/tmlr_calibration/pdfs").glob("*.pdf"))
    return {
        "papers": len(papers),
        "fetch_meta_total": dump["meta"]["stats"]["total"],
        "fetch_meta_errors": dump["meta"]["stats"]["errors"],
        "decisions": dump["meta"]["stats"]["decisions"],
        "review_keys": sorted(keys),
        "review_string_fields_longer_than_40": long_strings,
        "pdfs": len(pdfs),
    }


def path_hits() -> dict:
    """Count text files that embed the legacy F:/deepseek machine prefix."""
    # One backslash (source and markdown) and two backslashes (JSON escaping).
    needles = (b"F:\\deepseek", b"F:/deepseek", b"F:\\\\deepseek")
    skip_dirs = {".git", "__pycache__", ".venv"}
    source, runs = [], []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.suffix.lower() in {".pdf", ".zip", ".png", ".pyc"}:
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if any(n in data for n in needles):
            rel = path.relative_to(ROOT).as_posix()
            if rel == "scripts/make_check.py":
                continue  # the scanner's own needles are not a machine path
            if rel.startswith(("examples/", "runs/", "chain_logs/")):
                runs.append(rel)
            else:
                source.append(rel)
    return {"source_files": sorted(source), "run_or_example_files": len(runs)}


def hygiene_block(dump: dict, paths: dict) -> str:
    decisions = ", ".join(f"{k}={v}" for k, v in sorted(dump["decisions"].items()))
    return "\n".join([
        f"dump_papers: {dump['papers']}",
        f"fetch_meta_total: {dump['fetch_meta_total']}",
        f"fetch_meta_errors: {dump['fetch_meta_errors']}",
        f"decisions: {decisions}",
        f"review_keys: {','.join(dump['review_keys'])}",
        f"review_string_fields_longer_than_40: {dump['review_string_fields_longer_than_40']}",
        f"pdfs_in_tree: {dump['pdfs']}",
        f"legacy_path_source_files: {','.join(paths['source_files'])}",
        f"legacy_path_example_or_run_files: {paths['run_or_example_files']}",
    ])


def check_versions(readme: str, failures: list[str]) -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version != "2.2":
        failures.append(f"VERSION file is {version!r}, expected 2.2")
    for name in ("README.md", "REVIEW_SOP.md", "PREREG.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        if "v2.2" not in text:
            failures.append(f"{name} does not mention v2.2")
    try:
        marked = extract(readme, "<!-- version:begin -->", "<!-- version:end -->")
    except ValueError as exc:
        failures.append(str(exc))
        return
    if marked != f"v{version}":
        failures.append(f"README version marker {marked!r} != v{version}")


def check_calibration(readme: str, failures: list[str]) -> None:
    facts = calibration_facts()
    if facts["n"] != facts["report_n"]:
        failures.append(f"calibration n {facts['n']} != report pairs {facts['report_n']}")
    if abs(facts["rho"] - float(facts["stored_rho"])) > 0.001:
        failures.append(
            f"recomputed Spearman {facts['rho']:.6f} disagrees with stored {facts['stored_rho']}"
        )
    if abs(facts["p"] - float(facts["stored_p"])) > 0.001:
        failures.append(
            f"recomputed p {facts['p']:.6f} disagrees with stored {facts['stored_p']}"
        )
    if abs(facts["bias"] - float(facts["bias_stored"])) > 0.01:
        failures.append(f"recomputed bias {facts['bias']:.4f} != stored {facts['bias_stored']}")
    if abs(facts["mae"] - float(facts["mae_stored"])) > 0.01:
        failures.append(f"recomputed MAE {facts['mae']:.4f} != stored {facts['mae_stored']}")
    if facts["suggested_unique"] != [6]:
        failures.append(f"suggested scores are not the constant 6: {facts['suggested_unique']}")
    if not facts["accept_only"]:
        failures.append("calibration pairs are not accept-only")
    try:
        marked = extract(readme, "<!-- calibration-stored:begin -->", "<!-- calibration-stored:end -->")
    except ValueError as exc:
        failures.append(str(exc))
        return
    want = calibration_block(facts)
    if marked != want:
        failures.append("README calibration block drifted:\n--- live ---\n" + want + "\n--- readme ---\n" + marked)


def check_matrix(readme: str, failures: list[str]) -> None:
    committed = load_json(ROOT / "benchmarks/planted_defects/results/matrix.json")
    live = score_planted.score(committed["labels_commit"])
    if live != committed:
        failures.append("planted-defect rerun does not match benchmarks/planted_defects/results/matrix.json")
    if committed.get("hash_errors"):
        failures.append(f"matrix records hash errors: {committed['hash_errors']}")
    matrix_md = (ROOT / "benchmarks/planted_defects/results/matrix.md").read_text(encoding="utf-8").strip()
    try:
        marked = extract(readme, "<!-- planted-matrix:begin -->", "<!-- planted-matrix:end -->")
    except ValueError as exc:
        failures.append(str(exc))
        return
    if marked != matrix_md:
        failures.append("README planted-matrix block does not match results/matrix.md")
    labels = load_json(ROOT / "benchmarks/planted_defects/labels.json")
    if labels.get("scored") is not False:
        failures.append("labels.json scored flag was changed after the freeze commit; leave it false")


def check_hygiene(failures: list[str]) -> None:
    text = (ROOT / "HYGIENE.md").read_text(encoding="utf-8")
    try:
        marked = extract(text, "<!-- hygiene-counts:begin -->", "<!-- hygiene-counts:end -->")
    except ValueError as exc:
        failures.append(str(exc))
        return
    want = hygiene_block(dump_facts(), path_hits())
    if marked != want:
        failures.append("HYGIENE.md counts drifted:\n--- live ---\n" + want + "\n--- file ---\n" + marked)


def check_prose(readme: str, failures: list[str]) -> None:
    lower = readme.lower()
    if "can't replace" in lower or "cant replace" in lower:
        failures.append("README still says \"can't replace\"")
    if "0 条记录" in readme:
        failures.append("README still describes the R4 selftest as 0 records")
    if "p=0.018" in readme or "p=0.018" in readme:
        failures.append("README still states the TMLR p-value as 0.018")
    for heading in ("## Quickstart", "### Linux / macOS", "### Windows (PowerShell)"):
        if heading not in readme:
            failures.append(f"README missing heading {heading}")
    problem = extract(readme, "<!-- problem:begin -->", "<!-- problem:end -->")
    lines = [ln for ln in problem.splitlines() if ln.strip()]
    if len(lines) > 3:
        failures.append(f"problem statement is {len(lines)} lines; the cap is 3")
    if "STATUS: WORK-IN-PROGRESS" not in readme and "STATUS: A" not in readme:
        failures.append("README has no STATUS line")


def main() -> int:
    failures: list[str] = []
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    try:
        check_versions(readme, failures)
        check_calibration(readme, failures)
        check_matrix(readme, failures)
        check_hygiene(failures)
        check_prose(readme, failures)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        failures.append(f"{type(exc).__name__}: {exc}")
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "run_review.py"), "--selftest"],
        cwd=ROOT,
    )
    if proc.returncode != 0:
        failures.append(f"run_review.py --selftest exited {proc.returncode}")
    if failures:
        print("make check: FAIL")
        for item in failures:
            print("- " + item)
        return 1
    print("make check: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
