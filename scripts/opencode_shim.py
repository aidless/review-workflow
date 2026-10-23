"""opencode_shim.py — DSH 会话协议 → opencode CLI 的本地网关 shim（S5 审稿应急后端）。

背景：DSH 网关(3080) 401 冻结（gateway_doctor: R6/PRISM/裁决LLM 全冻）。
本 shim 在 3081 端口说同一套会话协议（POST /api/{method}，envelope
client-request/server-response），把 session.prompt 翻译成 `opencode run` 后台线程，
session.history 返回 client 期望的事件流（user/message → assistant/message → turn/end）。
审稿管线零改动：配置 rpc 指到 3081 + 环境变量 REVIEW_LLM_RPC 即可。

方法支持：session.create / rename / selectModel / prompt / history；
未知方法返回 ok=false（管线对 R3/R6 已有优雅降级：裁决无结果→保留断点→SKIP）。

用法: python opencode_shim.py [--port 3081] [--model opencode/mimo-v2.5-free]
日志: review-workflow/shim_log.jsonl
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import threading
import time
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = HERE / "shim_log.jsonl"

SESSIONS: dict[str, dict] = {}
LOCK = threading.Lock()
MODEL = "opencode/mimo-v2.5-free"
TIMEOUT = 900


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def log(row: dict) -> None:
    with LOCK:
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": now(), **row}, ensure_ascii=False) + "\n")


def _run_opencode(sid: str, text: str) -> None:
    """后台线程：调 opencode，把回复写成 assistant/message + turn/end 事件。"""
    sess = SESSIONS[sid]
    t0 = time.time()
    reply, ok, err = "", False, ""
    try:
        exe = shutil.which("opencode")
        if not exe:
            raise RuntimeError("opencode not found")
        r = subprocess.run([exe, "run", "-m", MODEL], input=text, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=TIMEOUT)
        if r.returncode != 0:
            raise RuntimeError(f"exit={r.returncode}: {r.stderr[-200:]}")
        reply = r.stdout
        ok = True
    except Exception as exc:  # noqa: BLE001
        err = str(exc)[:300]
    with LOCK:
        n = sess["next_seq"]
        if ok:
            sess["events"].append({"seq": n, "type": "assistant/message",
                                   "data": {"message": {"content": [{"type": "text", "text": reply}]}}})
            n += 1
            sess["events"].append({"seq": n, "type": "turn/end",
                                   "data": {"reason": {"kind": "stop"}}})
        else:
            sess["events"].append({"seq": n, "type": "turn/end",
                                   "data": {"reason": {"kind": "error",
                                                       "error": {"message": err}}}})
        sess["next_seq"] = n + 1
    log({"sid": sid, "op": "prompt-done", "model": MODEL, "ok": ok,
         "chars": len(reply), "secs": round(time.time() - t0, 1), "err": err})


def handle_method(method: str, payload: dict) -> dict:
    if method == "session.create":
        sid = "shim-" + uuid.uuid4().hex[:10]
        with LOCK:
            SESSIONS[sid] = {"events": [], "next_seq": 1, "model": ""}
        log({"sid": sid, "op": "create"})
        return {"sessionId": sid}
    if method == "session.rename":
        return {"renamed": True}
    if method == "session.selectModel":
        sid = payload.get("sessionId", "")
        with LOCK:
            if sid in SESSIONS:
                SESSIONS[sid]["model"] = f"{payload.get('provider','?')}/{payload.get('model','?')}"
        return {"selected": True}
    if method == "session.prompt":
        sid = payload.get("sessionId", "")
        text = "".join(b.get("text", "") for b in payload.get("content", [])
                       if isinstance(b, dict) and b.get("type") == "text")
        with LOCK:
            sess = SESSIONS.get(sid)
            if sess is None:
                return {"error": "unknown session"}
            n = sess["next_seq"]
            sess["events"].append({"seq": n, "type": "user/message", "data": {}})
            sess["next_seq"] = n + 1
        threading.Thread(target=_run_opencode, args=(sid, text), daemon=True).start()
        return {"queued": True}
    if method == "session.history":
        sid = payload.get("sessionId", "")
        before = payload.get("beforeSeq")
        with LOCK:
            evs = list(SESSIONS.get(sid, {}).get("events", []))
        if before is not None:
            evs = [e for e in evs if int(e.get("seq", 0)) < int(before)]
        return {"events": evs, "hasMore": False}
    # 未知方法：显式失败（管线对 R3/R6 有优雅降级），日志留痕便于补齐
    log({"op": "unknown-method", "method": method})
    return {"error": f"shim 不支持 method {method}"}


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        try:
            length = int(self.headers.get("Content-Length", 0))
            msg = json.loads(self.rfile.read(length).decode("utf-8"))
            method = msg.get("method", self.path.strip("/").replace("api/", ""))
            value = handle_method(method, msg.get("payload", {}) or {})
            ok = "error" not in (value or {})
            body = json.dumps({"type": "server-response",
                               "result": {"ok": ok, **({"error": value["error"]} if not ok else {"value": value})}},
                              ensure_ascii=False).encode("utf-8")
            self.send_response(200)
        except Exception as exc:  # noqa: BLE001
            body = json.dumps({"type": "server-response",
                               "result": {"ok": False, "error": str(exc)[:200]}}).encode("utf-8")
            self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        # 健康探针：run_review.rpc_health 与 debate 的裸 urlopen 用 GET；返回 200 JSON
        body = json.dumps({"ok": True, "service": "opencode-shim", "model": MODEL},
                          ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):  # 静默默认访问日志
        pass


def main() -> int:
    global MODEL
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=3081)
    ap.add_argument("--model", default=MODEL)
    args = ap.parse_args()
    MODEL = args.model
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"opencode shim on 127.0.0.1:{args.port} model={MODEL} (Ctrl+C 停止)")
    srv.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
