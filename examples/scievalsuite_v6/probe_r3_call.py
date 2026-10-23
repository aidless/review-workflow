import json
import sys
import time

sys.path.insert(0, r"F:\deepseek\research-kit\review-workflow\scripts")
sys.path.insert(0, r"F:\deepseek\research-kit")
import number_reconcile as nr
import adversarial_review as adv

adv.RPC = "http://127.0.0.1:3080"

# Monkey-patch rpc to log calls
_orig_rpc = adv.rpc


def logged_rpc(method, payload, timeout=120):
    t0 = time.time()
    print(f"  [rpc] {method} start", flush=True)
    try:
        r = _orig_rpc(method, payload, timeout=timeout)
        print(f"  [rpc] {method} done in {time.time()-t0:.1f}s", flush=True)
        return r
    except Exception as e:
        print(f"  [rpc] {method} FAILED in {time.time()-t0:.1f}s: {type(e).__name__}: {str(e)[:120]}", flush=True)
        raise


adv.rpc = logged_rpc

p = r"F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\run_v3_converge\number_reconcile.json"
report = json.load(open(p, encoding="utf-8"))
mrl = report["direction_B_paper_to_evidence"]["manual_review_list"]
unique = {}
for r in mrl:
    unique.setdefault(r["token"], []).append(r["context"])
evidence_nums = [(str(e["value"]), e["value"]) for e in report.get("_evidence", [])]

first_llm = None
for token, ctxs in unique.items():
    mech_verdict, mech_note = nr.mechanical_r3(token, ctxs, evidence_nums)
    if not mech_verdict:
        first_llm = (token, ctxs, mech_note)
        break

print("first LLM token:", first_llm[0], flush=True)
prompt = nr.build_r3_prompt(first_llm[0], first_llm[1], first_llm[2])
print("prompt length:", len(prompt), flush=True)

t0 = time.time()
print("step: calling prompt_turn...", flush=True)
rec = adv.prompt_turn(prompt, "r3-adjudicate", timeout=300)
dt = time.time() - t0
print(f"prompt_turn took {dt:.1f}s, status={rec['status']}", flush=True)
print("raw head:", (rec.get("raw") or "")[:300], flush=True)
