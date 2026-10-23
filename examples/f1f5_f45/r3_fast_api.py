# -*- coding: utf-8 -*-
"""R3 数字裁决加速版：OpenAI 兼容 API 直连（绕过 DSH agent 框架）。

与 number_reconcile.adjudicate_pending 同提示词/同解析/同断点格式，仅换传输层：
- 机械层 mechanical_r3 完全复用
- LLM 层改用直连 chat/completions（并发 6），每次 ~1-2s（DSH 需 100-300s）
- 断点格式 byte 兼容：r3_adjudications.json + r3_adjudications.md

用法:
    python r3_fast_api.py --config f45.json [--workers 6]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, r"F:\deepseek\research-kit\review-workflow\scripts")
import number_reconcile as nr  # noqa: E402

R3_VERDICTS = ("noise", "supported", "critical")
API_BASE = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL = "deepseek-v4-flash-0731"


def load_ali_key() -> str:
    cred = yaml.safe_load(open(r"C:\Users\Administrator\.dsh\.credentials.yaml", encoding="utf-8"))
    key = (cred.get("refs") or {}).get("ALI_API_KEY", "")
    if not key:
        raise RuntimeError("ALI_API_KEY 不在 .credentials.yaml refs 中")
    return key


def chat_complete(key: str, prompt: str, model: str, timeout: int = 180, max_tokens: int = 8000) -> str:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(API_BASE + "/chat/completions", data=body,
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        resp = json.loads(r.read().decode("utf-8"))
    return (resp.get("choices") or [{}])[0].get("message", {}).get("content", "")


_VERDICT_RE = re.compile(r'"verdict"\s*:\s*"(noise|supported|critical)"')


def parse_lenient(raw: str) -> dict | None:
    """宽松解析：JSON 截断/空响应时按 'verdict' 字段抽取，避免整条报废。"""
    import re as _re
    m = _VERDICT_RE.search(raw or "")
    if m:
        return {"verdict": m.group(1), "confidence": "low",
                "justification": (raw or "")[:200], "evidence": "",
                "suggested_action": "", "parse": "lenient"}
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--model", default=os.environ.get("REVIEW_LLM_MODEL", DEFAULT_MODEL))
    args = ap.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    out = Path(cfg["out"])
    rep = json.loads((out / "number_reconcile.json").read_text(encoding="utf-8"))
    adj_path = out / "r3_adjudications.json"

    mrl = rep["direction_B_paper_to_evidence"]["manual_review_list"]
    unique: dict[str, list[str]] = {}
    for r in mrl:
        unique.setdefault(r["token"], []).append(r["context"])
    evidence_nums = [(str(e["value"]), e["value"]) for e in rep.get("_evidence", [])]

    existing = {}
    if adj_path.exists():
        try:
            existing = json.loads(adj_path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            existing = {}
    prior = {a["token"]: a for a in existing.get("adjudications", [])
             if a.get("verdict") in R3_VERDICTS}

    out_adj = {
        "meta": {"tex": str(rep.get("_meta", {}).get("tex", "")), "rpc": "direct-API(ali)",
                 "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                 "rpc_health": "direct-API via chat/completions"},
        "adjudications": [],
        "summary": {"total": 0, "mechanical": 0, "llm": 0, "llm_failed": 0,
                    "noise": 0, "supported": 0, "critical": 0, "verdict": None, "detail": ""},
    }

    key = load_ali_key()

    # 收集需 LLM 的 token
    pending = []
    for token, ctxs in unique.items():
        if token in prior:
            out_adj["adjudications"].append(prior[token])
            continue
        mech_verdict, mech_note = nr.mechanical_r3(token, ctxs, evidence_nums)
        entry = {"token": token, "contexts": ctxs, "mechanical": mech_note or None}
        if mech_verdict:
            entry.update({"layer": "mechanical", "verdict": mech_verdict, "confidence": "high",
                          "justification": mech_note, "evidence": ctxs[0][:80] if ctxs else "",
                          "suggested_action": ""})
            out_adj["adjudications"].append(entry)
        else:
            entry["_prompt"] = nr.build_r3_prompt(token, ctxs, mech_note)
            pending.append(entry)

    print(f"[r3-fast] 复用已裁决 {len(prior)}；机械层 {len(out_adj['adjudications']) - len(prior)}；"
          f"待 LLM {len(pending)}", flush=True)

    def _do(entry: dict) -> dict:
        last_err = ""
        raw = ""
        for attempt in range(1, 4):
            try:
                raw = chat_complete(key, entry["_prompt"], args.model)
            except Exception as e:  # noqa: BLE001
                last_err = f"api-error: {type(e).__name__}"
                time.sleep(2 * attempt)
                continue
            parsed = nr.parse_r3_verdict(raw)
            if not parsed:
                parsed = parse_lenient(raw)
            if parsed:
                entry.update(parsed)
                entry["layer"] = "llm"
                return entry
            last_err = "parse_failed" if raw else "empty"
            time.sleep(2 * attempt)
        entry.update({"layer": "llm", "verdict": "未裁决", "llm_status": last_err,
                      "raw_head": raw[:300]})
        return entry

    t0 = time.time()
    n_failed = 0
    n_done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(_do, e): e for e in pending}
        for i, fut in enumerate(as_completed(futs), 1):
            entry = fut.result()
            entry.pop("_prompt", None)
            out_adj["adjudications"].append(entry)
            n_done += 1
            if entry.get("verdict") == "未裁决":
                n_failed += 1
            if i % args.workers == 0 or i == len(pending):
                adj_path.write_text(json.dumps(out_adj, ensure_ascii=False), encoding="utf-8")
                print(f"[r3-fast] {i}/{len(pending)} 完成（失败 {n_failed}）{time.time()-t0:.0f}s", flush=True)

    for a in out_adj["adjudications"]:
        v = a.get("verdict")
        if v in R3_VERDICTS:
            out_adj["summary"][v] += 1
            if a["layer"] == "mechanical":
                out_adj["summary"]["mechanical"] += 1
            else:
                out_adj["summary"]["llm"] += 1
    out_adj["summary"]["total"] = len(out_adj["adjudications"])
    out_adj["summary"]["llm_failed"] = n_failed

    n_critical = out_adj["summary"]["critical"]
    n_unadjudicated = sum(1 for a in out_adj["adjudications"] if a.get("verdict") == "未裁决")
    if n_critical:
        out_adj["summary"]["verdict"] = "CRITICAL"
        out_adj["summary"]["detail"] = (f"critical {n_critical} 个（实质断言无来源，一票 Critical）；"
                                        f"noise {out_adj['summary']['noise']} / supported {out_adj['summary']['supported']}")
    elif n_unadjudicated:
        out_adj["summary"]["verdict"] = "MAJOR"
        out_adj["summary"]["detail"] = (f"{n_unadjudicated} 个未裁决（LLM 失败 {n_failed}）"
                                        f"→ 维持 recompute 原判 Major；noise {out_adj['summary']['noise']} / "
                                        f"supported {out_adj['summary']['supported']}")
    else:
        out_adj["summary"]["verdict"] = "PASS"
        out_adj["summary"]["detail"] = (f"全部裁决：noise {out_adj['summary']['noise']} / "
                                        f"supported {out_adj['summary']['supported']}，无 critical")

    adj_path.write_text(json.dumps(out_adj, ensure_ascii=False), encoding="utf-8")
    nr.write_r3_md(out_adj, out / "r3_adjudications.md")
    print(f"[r3-fast] 完成 {time.time()-t0:.0f}s  verdict={out_adj['summary']['verdict']} "
          f"({out_adj['summary']['detail']})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
