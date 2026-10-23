# -*- coding: utf-8 -*-
"""Test author prompt reliability at different paper-excerpt lengths."""
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, r"F:\deepseek\research-kit\review-workflow\scripts")
import debate

RPC = "http://127.0.0.1:3080"
CWD = r"F:\deepseek"
PROVIDER = "baidu"
MODEL = "qianfan-code-latest"


def rpc(method, payload, timeout=120):
    body = json.dumps({"type": "client-request", "rpcId": f"probe-{time.time_ns()}",
                       "method": method, "payload": payload}).encode("utf-8")
    req = urllib.request.Request(f"{RPC}/api/{method}", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        envelope = json.loads(resp.read().decode("utf-8"))
    if envelope.get("type") != "server-response":
        raise RuntimeError(f"bad envelope: {envelope}")
    result = envelope.get("result") or {}
    if not result.get("ok"):
        raise RuntimeError(f"{method} failed: {result.get('error')}")
    return result.get("value")


def all_events(sid):
    events = {}
    before = None
    for _ in range(50):
        payload = {"sessionId": sid, "maxMessages": 400}
        if before is not None:
            payload["beforeSeq"] = before
        page = rpc("session.history", payload)
        evs = page.get("events", [])
        if not evs:
            break
        for item in evs:
            ev = item.get("event", item)
            events[ev["seq"]] = ev
        if not page.get("hasMore"):
            break
        before = min(int(e["seq"]) for e in events.values())
    return list(events.values())


def prompt_turn(text, label, timeout=180):
    sid = rpc("session.create", {"agentPreset": "minimal", "cwd": CWD})["sessionId"]
    rpc("session.selectModel", {"sessionId": sid, "provider": PROVIDER, "model": MODEL})
    before_turns = sum(1 for e in all_events(sid) if e.get("type") == "turn/end")
    before_user = max((e.get("seq", -1) for e in all_events(sid) if e.get("type") == "user/message"), default=-1)
    rpc("session.prompt", {"sessionId": sid, "mode": "queue",
                           "content": [{"type": "text", "text": text}]})
    deadline = time.time() + timeout
    t0 = time.time()
    while time.time() < deadline:
        evs = all_events(sid)
        ends = [e for e in evs if e.get("type") == "turn/end"]
        if len(ends) >= before_turns + 1:
            texts = []
            for ev in evs:
                if ev.get("type") == "assistant/message" and ev.get("seq", 0) > before_user:
                    m = (ev.get("data") or {}).get("message") or {}
                    for block in m.get("content") or []:
                        if isinstance(block, dict) and block.get("type") == "text":
                            texts.append(block.get("text", ""))
            raw = "\n".join(texts)
            print(f"[{label}] OK len={len(raw)} elapsed={time.time()-t0:.1f}s")
            return True
        time.sleep(5)
    print(f"[{label}] STALLED after {timeout}s")
    return False


def main():
    tex = Path(r"F:\deepseek\papers\scievalsuite\paper\main.tex")
    full = tex.read_text(encoding="utf-8", errors="replace")
    issues, tr = debate.load_issues(Path(r"F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\run_v4_fixed\r6_llm.json"), return_stats=True)
    real = [i for i in issues if not i.get("synthetic")]
    for excerpt in [3000, 2000, 1200]:
        paper = full[:excerpt] + "\n…(截断)"
        p = debate.author_prompt(real, paper)
        print(f"excerpt={excerpt} prompt_chars={len(p)}")
        ok = prompt_turn(p, f"excerpt-{excerpt}")
        if not ok:
            print(f"  -> excerpt={excerpt} FAILED, trying shorter")
        time.sleep(3)


if __name__ == "__main__":
    main()
