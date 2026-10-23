# -*- coding: utf-8 -*-
"""R3 分批续跑 v2：每批 max_llm=batch 跑 R3（断点续跑），循环到全部 token 裁决完。

v2 变更（DSH 会话内存累积 → OOM）：
  - 每批开始前用 psutil 检查 DSH 内存（端口 3080 监听进程）
  - 超阈值自动重启 DSH（会话内存清零，磁盘断点不受影响）
  - REVIEW_LLM_PROVIDER/MODEL 环境变量固定为 ali/deepseek-v4-flash-0731（baidu 链路挂起）

用法:
    python r3_resume_loop.py --config f45.json [--batch 5] [--max-runs 40] [--stages R3]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
RUN_REVIEW = SCRIPTS / "run_review.py"
R3_VERDICTS = ("noise", "supported", "critical")
DSH_PORT = 3080
DSH_MEM_MB = int(os.environ.get("DSH_MEM_MB", "900"))
LLM_PROVIDER = os.environ.get("REVIEW_LLM_PROVIDER", "ali")
LLM_MODEL = os.environ.get("REVIEW_LLM_MODEL", "deepseek-v4-flash-0731")
DSH_LOG = Path(os.environ.get("DSH_LOG", r"F:\Temp\dsh_restart.log"))
DSH_BIN = r"C:\Program Files\nodejs\node_global\node_modules\@deepseek-ai\dsh\lib\bin.js"


def dsh_pid() -> int | None:
    try:
        import psutil
        for conn in psutil.net_connections():
            if conn.laddr.port == DSH_PORT and conn.status == "LISTEN":
                return conn.pid
    except Exception:  # noqa: BLE001
        pass
    return None


def dsh_mem_mb(pid: int) -> int:
    try:
        import psutil
        return int(psutil.Process(pid).memory_info().rss / 1024 / 1024)
    except Exception:  # noqa: BLE001
        return 0


def dsh_healthy(timeout: int = 10) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{DSH_PORT}/", timeout=timeout) as r:
            return r.status == 200
    except Exception:  # noqa: BLE001
        return False


def restart_dsh() -> bool:
    pid = dsh_pid()
    if pid:
        try:
            import psutil
            psutil.Process(pid).kill()
            print(f"[dsh] killed pid {pid}", flush=True)
        except Exception as e:  # noqa: BLE001
            print(f"[dsh] kill failed: {e}", flush=True)
    # 等端口释放
    for _ in range(30):
        if dsh_pid() is None:
            break
        time.sleep(1)
    node = shutil.which("node") or r"C:\Program Files\nodejs\node.exe"
    # 旧 DSH 的 stdout 重定向可能仍锁着日志文件：先删，再带重试打开
    try:
        if DSH_LOG.exists():
            DSH_LOG.unlink()
    except OSError:
        pass
    log_f = None
    for _ in range(10):
        try:
            log_f = open(DSH_LOG, "a", encoding="utf-8")
            break
        except OSError:
            time.sleep(1)
    if log_f is None:
        log_f = open(os.devnull, "w")
    subprocess.Popen([node, DSH_BIN, "--profile", "web", "--no-open"],
                     stdout=log_f, stderr=subprocess.STDOUT,
                     creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    print(f"[dsh] 启动新 DSH（{DSH_LOG}）", flush=True)
    # 就绪判断：root 200 太早（API 可能尚未注册，首次调用 404）→ 必须等到 session.create 可用
    api_ok = False
    for i in range(90):
        time.sleep(2)
        if not dsh_healthy():
            continue
        try:
            body = json.dumps({"type": "client-request", "rpcId": "dsh-warm",
                               "method": "session.create",
                               "payload": {"agentPreset": "minimal", "cwd": r"F:\deepseek"}}).encode()
            req = urllib.request.Request(f"http://127.0.0.1:{DSH_PORT}/api/session.create",
                                         data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as r:
                env = json.loads(r.read().decode())
            if (env.get("result") or {}).get("ok"):
                api_ok = True
                print(f"[dsh] API 就绪（{i * 2}s）", flush=True)
                break
        except Exception:  # noqa: BLE001
            pass
    if not api_ok:
        print("[dsh] API 就绪超时（180s）", flush=True)
        return False
    return True


def expected_unique(out: Path) -> int:
    p = out / "number_reconcile.json"
    if not p.exists():
        return -1
    try:
        j = json.loads(p.read_text(encoding="utf-8"))
        mrl = j["direction_B_paper_to_evidence"]["manual_review_list"]
        return len({r["token"] for r in mrl})
    except Exception:  # noqa: BLE001
        return -1


def load_adj(out: Path) -> dict:
    p = out / "r3_adjudications.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            return {}
    return {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--batch", type=int, default=5)
    ap.add_argument("--max-runs", type=int, default=40)
    ap.add_argument("--stages", default="R3")
    ap.add_argument("--sleep", type=int, default=5)
    ap.add_argument("--restart-first", action="store_true", help="首批前先重启 DSH")
    args = ap.parse_args()

    os.environ["REVIEW_LLM_PROVIDER"] = LLM_PROVIDER
    os.environ["REVIEW_LLM_MODEL"] = LLM_MODEL
    print(f"[loop] provider={LLM_PROVIDER}/{LLM_MODEL} DSH_MEM_MB={DSH_MEM_MB}", flush=True)

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    out = Path(cfg["out"])
    expected = expected_unique(out)
    eff_cfg_path = out / "_r3_batch_effective.json"
    eff_cfg = dict(cfg)
    eff_cfg["r3_max_llm"] = args.batch
    eff_cfg_path.write_text(json.dumps(eff_cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    cmd = [sys.executable, str(RUN_REVIEW), "--config", str(eff_cfg_path), "--stages", args.stages]
    print(f"[loop] 唯一 token 目标数：{expected if expected > 0 else '未知'}", flush=True)

    if args.restart_first or not dsh_healthy():
        print("[loop] 首轮前重启 DSH…", flush=True)
        if not restart_dsh():
            return 3

    last_done = -1
    no_progress = 0
    for run in range(1, args.max_runs + 1):
        pid = dsh_pid()
        mem = dsh_mem_mb(pid) if pid else 0
        if pid and mem > DSH_MEM_MB:
            print(f"[dsh] 内存 {mem}MB > {DSH_MEM_MB}MB → 重启", flush=True)
            if not restart_dsh():
                return 3
            time.sleep(args.sleep)
        else:
            print(f"[dsh] mem={mem}MB pid={pid}", flush=True)

        t0 = time.time()
        print(f"[batch-run {run}] max_llm={args.batch} 开始（{time.strftime('%H:%M:%S')}）", flush=True)
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        for line in (r.stdout or "").splitlines():
            if line.strip():
                print(f"  {line}", flush=True)
        if r.returncode != 0:
            print(f"[batch-run {run}] 退出码 {r.returncode}；stderr 尾："
                  f"{(r.stderr or '').strip().splitlines()[-3:]}", flush=True)

        adj = load_adj(out)
        entries = adj.get("adjudications", [])
        done = sum(1 for a in entries if a.get("verdict") in R3_VERDICTS)
        capped = sum(1 for a in entries if a.get("llm_status") == "max_llm")
        failed = sum(1 for a in entries if a.get("verdict") == "未裁决" and a.get("llm_status") != "max_llm")
        print(f"[batch-run {run}] 已裁决 {done} / {expected if expected > 0 else len(entries)}；"
              f"max_llm 截断 {capped}；LLM 失败 {failed}（耗时 {time.time()-t0:.0f}s）", flush=True)

        if expected > 0 and done >= expected:
            print(f"[batch-run {run}] 已裁决数达到唯一 token 目标 → 完成", flush=True)
            return 0
        if done > last_done:
            no_progress = 0
        else:
            no_progress += 1
        last_done = done
        if no_progress >= 4:
            print(f"[batch-run {run}] 连续 {no_progress} 轮无新裁决（done={done}，expected={expected}）→ "
                  f"疑似 RPC 不可达或任务卡死，放弃本轮", flush=True)
            return 2
        print(f"[batch-run {run}] 继续下一批（{args.sleep}s 后）…", flush=True)
        time.sleep(args.sleep)

    print(f"[loop] 达到 max-runs={args.max_runs}，仍有未处理 token；可再次运行续跑", flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
