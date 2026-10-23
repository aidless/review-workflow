# -*- coding: utf-8 -*-
"""log_s5_round.py — S5 整轮审稿登记（五轮制记账器）。

把一次 run_review.py --config 整轮执行登记为一轮：
  python log_s5_round.py --out <reviews/pipeline_S5> [--note "..."]

读取 gates.json（suggested_score/overall/各阶段门禁）+ honesty_scan.json
（suspicious）+ r6 产物（Critical 计数，尽力而为），追加
rounds_ledger.jsonl 一行：{round, timestamp, score, overall, criticals, stages, note}。
通过线（stages.yml S5）：轮数≥5 + 末轮≥8 + 0 未处置 Critical。
只追加不改写；gates.json 不存在则拒绝登记（先跑完整轮）。
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--note", default="")
    args = ap.parse_args()
    out = args.out
    gates = load(out / "gates.json")
    if not gates:
        print("拒绝登记：gates.json 缺失（先跑完 run_review 整轮）")
        return 1
    ledger = out / "rounds_ledger.jsonl"
    n = 0
    if ledger.exists():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if line.strip():
                n += 1
    hon = load(out / "honesty_scan.json") or {}
    r6 = load(out / "r6_llm.json") or load(out / "adversarial_review.json") or {}
    crit = 0
    if isinstance(hon, dict):
        crit += int((hon.get("summary") or {}).get("suspicious", 0) or 0)
    if isinstance(r6, dict):
        for k in ("critical", "criticals", "n_critical"):
            v = (r6.get("summary") or r6).get(k) if isinstance(r6.get("summary", r6), dict) else None
            if isinstance(v, int):
                crit += v
                break
    # panel 来源（E324：只记实测，不推断；peer 可见性未知即 unknown）
    cfg = load(out / "config.json") or {}
    llm = cfg.get("llm") or {}
    panel = {
        "roles": (llm.get("roles") or "unknown"),
        "rpc": (llm.get("rpc") or "unknown"),
        "actor": "model",
        "peer_visible": "unknown",
        "human_reviewer": None,
    }
    rec = {
        "round": n + 1,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "score": gates.get("suggested_score"),
        "overall": gates.get("overall"),
        "criticals": crit,
        "panel": panel,
        "note": args.note,
    }
    with ledger.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    scores = []
    if ledger.exists():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    scores.append(json.loads(line).get("score"))
                except Exception:
                    pass
    ok_rounds = (n + 1) >= 5
    ok_score = isinstance(rec["score"], (int, float)) and rec["score"] >= 8
    print(f"round {n + 1} 登记：score={rec['score']} overall={rec['overall']} criticals={crit}")
    print(f"五轮线：轮数 {n + 1}/5 {'OK' if ok_rounds else '..'}；末轮≥8 {'OK' if ok_score else '..'}；"
          f"0 Critical {'OK' if crit == 0 else 'FAIL'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
