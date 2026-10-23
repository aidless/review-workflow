# -*- coding: utf-8 -*-
"""Probe the RPC session server with minimal prompts to isolate the debate-author stall."""
import json
import sys
import time
import urllib.request

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


def prompt_turn(text, label, timeout=90):
    sid = rpc("session.create", {"agentPreset": "minimal", "cwd": CWD})["sessionId"]
    rpc("session.selectModel", {"sessionId": sid, "provider": PROVIDER, "model": MODEL})
    before_turns = sum(1 for e in all_events(sid) if e.get("type") == "turn/end")
    before_user = max((e.get("seq", -1) for e in all_events(sid) if e.get("type") == "user/message"), default=-1)
    rpc("session.prompt", {"sessionId": sid, "mode": "queue",
                           "content": [{"type": "text", "text": text}]})
    deadline = time.time() + timeout
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
            print(f"[{label}] OK len={len(raw)} head={raw[:80]!r}")
            return
        time.sleep(5)
    print(f"[{label}] STALLED after {timeout}s (no turn/end)")


def main():
    tests = [
        ("simple", "你好，请回复：OK"),
        ("json", '输出严格 JSON 数组：\n[{"id": 1, "action": "rebut", "rebuttal": "test"}]'),
        ("author_head", "你是论文作者，正在回复审稿意见（rebuttal）。逐条回应下面的问题清单。\n规则：\n- 能用论文中的具体内容/数据/披露驳回的，选 rebut，rebuttal 必须引用论文具体内容（不许空辩）\n- 确实是问题的，选 concede，fix 用「将/会」表述具体修改方案（是承诺，尚未执行，不许写成已完成动作）\n- 不许回避任何一条\n\n输出严格 JSON 数组（不要 markdown、不要多余文字）：\n[{\"id\": 1, \"action\": \"rebut\", \"rebuttal\": \"<=80字，引用论文依据\"}, {\"id\": 2, \"action\": \"concede\", \"fix\": \"<=60字\"}]\n\n问题清单：\n1. [Critical] test issue one\n2. [Major] test issue two"),
    ]
    for label, text in tests:
        try:
            prompt_turn(text, label)
        except Exception as e:
            print(f"[{label}] ERROR: {e}")
        time.sleep(3)


if __name__ == "__main__":
    main()
