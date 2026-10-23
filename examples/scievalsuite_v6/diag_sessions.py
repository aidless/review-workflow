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


# List sessions to find the r3-adjudicate one
try:
    r = rpc("session.list", {})
    sessions = r.get("sessions") or r.get("items") or []
    print(f"num sessions: {len(sessions)}", flush=True)
    for s in sessions:
        title = s.get("title") or s.get("name") or ""
        sid = s.get("sessionId") or s.get("id") or ""
        if "adv-review" in str(title) or "r3" in str(title).lower():
            print(f"  {sid[:30]} | {str(title)[:60]}", flush=True)
except Exception as e:
    print(f"session.list failed: {type(e).__name__}: {str(e)[:100]}", flush=True)
