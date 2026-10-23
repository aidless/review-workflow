# -*- coding: utf-8 -*-
"""gateway_doctor.py — 外部依赖体检聚合（E357，Agent-Reach doctor 模式移植）。

每个源自查，单源异常降级为 error，绝不掀翻整份报告；输出边界脱敏。
四态：ok / missing（配了但不可达）/ broken（通了但错）/ timeout / error。
hint 给修复处方。

检查：DSH Review RPC（prompt_turn 微探针）/ Haolo 网关（HTTPS 可达+SSL 分类）/
Crossref / arXiv。exit 0=全 ok；1=有非 ok（列清单）；2=脚本自身 infra 错。

用法: python gateway_doctor.py [--json out.json]
"""
from __future__ import annotations

import argparse
import json
import ssl
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

RESULTS: list[dict] = []


def rec(name: str, status: str, message: str = "", hint: str = ""):
    RESULTS.append({"name": name, "status": status, "message": message[:200], "hint": hint})


def probe_https(name: str, url: str, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "paper-pipeline/doctor"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            rec(name, "ok", f"HTTP {r.status}")
    except TimeoutError:
        rec(name, "timeout", "连接超时", "检查出口网络/代理后重试")
    except Exception as e:  # noqa: BLE001
        msg = str(e)
        if "SSL" in type(e).__name__ or "SSL" in msg or "EOF" in msg:
            rec(name, "error", f"SSL 中断：{msg[:100]}", "网关侧重置，等待恢复后重探")
        elif "NameResolution" in msg or "getaddrinfo" in msg or "11001" in msg:
            rec(name, "missing", f"DNS 不可达：{msg[:100]}", "检查 DNS/出口网络")
        elif " refused" in msg or "10061" in msg:
            rec(name, "error", f"连接被拒：{msg[:100]}", "服务未启动或端口错")
        else:
            rec(name, "error", msg[:150], "见 message 排查")


def probe_dsh(timeout=150):
    try:
        import adversarial_review as adv
        r = adv.prompt_turn("请只回复两个字：收到", "doctor", timeout=timeout)
        st = r.get("status", "?")
        if st == "ok":
            rec("dsh-rpc", "ok", f"chunks={len(r.get('raw',''))}")
        else:
            rec("dsh-rpc", "error", f"status={st}",
                "DSH 网关无响应：R6/R6b/PRISM/裁决LLM全冻，等恢复")
    except Exception as e:  # noqa: BLE001
        rec("dsh-rpc", "error", str(e)[:150], "检查 DSH 是否在 3080 监听")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path, default=None)
    ap.add_argument("--skip-dsh", action="store_true", help="跳过 DSH 微探针（只查可达性）")
    args = ap.parse_args()
    try:
        probe_https("haolo", "https://api.haolo.com/", timeout=12)
    except Exception as e:  # noqa: BLE001
        rec("haolo", "error", str(e)[:150], "见 message")
    probe_https("crossref", "https://api.crossref.org/works/10.1038/nature12373", timeout=15)
    probe_https("arxiv", "https://export.arxiv.org/api/query?id_list=1706.03762", timeout=15)
    if not args.skip_dsh:
        probe_dsh()
    else:
        rec("dsh-rpc", "missing", "skip-dsh（未探）", "去 flag 重探")
    print("# gateway doctor")
    bad = 0
    for r in RESULTS:
        flag = "OK " if r["status"] == "ok" else "FAIL"
        if r["status"] != "ok":
            bad += 1
        print(f"[{flag}] {r['name']}: {r['status']} {r['message']}")
        if r["hint"] and r["status"] != "ok":
            print(f"      处方：{r['hint']}")
    if args.json:
        args.json.write_text(json.dumps(RESULTS, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{len(RESULTS)-bad}/{len(RESULTS)} ok")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
