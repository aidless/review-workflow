import json
import time
import urllib.request


def rpc(method, payload, timeout=30):
    body = json.dumps(
        {"type": "client-request", "rpcId": f"diag-{time.time_ns()}", "method": method, "payload": payload}
    ).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:3080/api/" + method, data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        env = json.loads(resp.read().decode("utf-8"))
    return env.get("result") or {}


print("diag: create session", flush=True)
t0 = time.time()
try:
    r = rpc("session.create", {"agentPreset": "minimal", "cwd": "F:/deepseek"})
    print(f"  create took {time.time()-t0:.1f}s, ok={r.get('ok')}, keys={list(r.keys())}", flush=True)
    sid = r.get("value", {}).get("sessionId") or r.get("sessionId")
    print(f"  sessionId: {sid}", flush=True)
    if sid:
        t0 = time.time()
        r2 = rpc("session.history", {"sessionId": sid, "maxMessages": 50})
        print(f"  history took {time.time()-t0:.1f}s, events={len(r2.get('events', []))}", flush=True)
except Exception as e:
    print(f"  FAILED after {time.time()-t0:.1f}s: {type(e).__name__}: {str(e)[:200]}", flush=True)
