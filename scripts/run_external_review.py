"""run_external_review.py — 执行一次外部评审并落盘（EXTERNAL_REVIEW_PROTOCOL.md 的执行器）。

通道：
  --engine opencode   opencode CLI（默认），如 -m opencode/mimo-v2.5-free（小米 MiMo，谱系独立）
                      备选：opencode/ling-3.0-flash-fin-free（蚂蚁 Ling）
  --engine http-anthropic  Anthropic 兼容 HTTP（MiniMax Coding Plan 充值后可用）：
                      --base-url https://api.minimaxi.com/anthropic --model MiniMax-M3
                      key 从 MINIMAX_API_KEY 环境变量取

纪律（协议 §硬性规则）：
  - 评审输入只有论文 tex + 通用评审提示词，不带工作区内部上下文/自评分/账本；
  - transcript 原文落盘 + sha256 记入 record.json（check_external_review.py 校验格式）；
  - 模型 id 必须避开本地模型家族（qwen/deepseek/llama/mistral/gemma/phi/ollama/…）。

用法:
  python run_external_review.py --paper F:/deepseek/papers/calibration-self-improvement \
      --engine opencode --model opencode/mimo-v2.5-free
  python run_external_review.py --paper ... --engine http-anthropic \
      --base-url https://api.minimaxi.com/anthropic --model MiniMax-M3
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

PROMPT_TEMPLATE = """You are an expert reviewer for the Transactions on Machine Learning Research (TMLR).

Review the following paper (LaTeX source, anonymized). Requirements:
1. Every criticism must cite the specific claim/number/section it targets. No vague complaints.
2. Label each point Critical / Major / Minor / Nit.
3. Say explicitly when you are uncertain — do not fabricate.
4. Check: Are the numbers internally consistent? Is every claim supported by the described
   evidence? Are the statistical protocols sound (multiple comparisons, CI construction,
   matched baselines)? Is the contribution appropriate for TMLR's criteria (claim-evidence
   alignment rather than novelty threshold)?
5. End with four scores 1-10 (evidence, interest, clarity, and overall with min-discipline)
   and your accept/reject tendency with one-paragraph justification.

Paper follows after this line.
===PAPER===
"""

LOCAL_FAMILY = [
    "qwen", "qwq", "deepseek", "llama", "mistral", "mixtral", "gemma",
    "phi-", "phi3", "phi4", "ollama", "127.0.0.1", "localhost", "vllm",
    "glm-4-flash", "internlm", "yi-",
]


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_tex(paper: Path) -> str:
    tex = paper / "paper" / "main.tex"
    if not tex.exists():
        raise SystemExit(f"FAIL 找不到 {tex}")
    return tex.read_text(encoding="utf-8", errors="replace")


def guard_model(model: str) -> None:
    low = model.lower()
    if any(k in low for k in LOCAL_FAMILY):
        raise SystemExit(f"FAIL 模型 {model} 命中本地家族名单（EXTERNAL_REVIEW_PROTOCOL.md 独立性要求）")


def call_opencode(model: str, prompt: str, timeout: int) -> str:
    exe = shutil.which("opencode")
    if not exe:
        raise SystemExit("FAIL 找不到 opencode 可执行文件（PATH）")
    # prompt 走 stdin：全文 tex 超 Windows 32KB 命令行上限（WinError 206）
    r = subprocess.run([exe, "run", "-m", model], input=prompt,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout)
    if r.returncode != 0:
        raise SystemExit(f"FAIL opencode exit={r.returncode}: {r.stderr[-400:]}")
    return r.stdout


def call_http_anthropic(base_url: str, model: str, prompt: str, timeout: int, retries: int = 3) -> str:
    key = os.environ.get("MINIMAX_API_KEY", "")
    if not key:
        raise SystemExit("FAIL 环境变量 MINIMAX_API_KEY 缺失")
    body = json.dumps({"model": model, "max_tokens": 8000,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    last = ""
    for i in range(retries):
        req = urllib.request.Request(f"{base_url.rstrip('/')}/v1/messages", data=body,
                                     headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                                              "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.loads(r.read())
                return "".join(c.get("text", "") for c in d.get("content", []))
        except Exception as exc:  # noqa: BLE001
            last = str(exc)
            detail = ""
            try:
                detail = exc.read().decode()[:300]  # type: ignore[attr-defined]
            except Exception:  # noqa: S110
                pass
            print(f"  attempt {i + 1}/{retries} FAIL: {last[:120]} {detail}", file=sys.stderr)
            if "2056" in detail or "用量上限" in detail:
                raise SystemExit("FAIL 配额耗尽（2056）：需升级 Token Plan 或购买积分") from None
            time.sleep(20)
    raise SystemExit(f"FAIL 重试耗尽：{last[:200]}")


def main() -> int:
    ap = argparse.ArgumentParser(description="执行外部评审并落盘")
    ap.add_argument("--paper", required=True)
    ap.add_argument("--engine", choices=["opencode", "http-anthropic"], default="opencode")
    ap.add_argument("--model", default="opencode/mimo-v2.5-free")
    ap.add_argument("--base-url", default="https://api.minimaxi.com/anthropic")
    ap.add_argument("--timeout", type=int, default=1800)
    args = ap.parse_args()

    paper = Path(args.paper).resolve()
    guard_model(args.model)
    tex = read_tex(paper)
    prompt = PROMPT_TEMPLATE + tex
    print(f"paper: {paper.name} | engine: {args.engine} | model: {args.model} | tex {len(tex)} chars")

    if args.engine == "opencode":
        review = call_opencode(args.model, prompt, args.timeout)
    else:
        review = call_http_anthropic(args.base_url, args.model, prompt, args.timeout)
    if not review.strip():
        raise SystemExit("FAIL 评审输出为空")

    er = paper / "external_review"
    er.mkdir(exist_ok=True)
    today = date.today().isoformat()
    # 时间戳命名：同日多轮不互相覆盖（R1 曾被同日 R2 覆盖——教训）
    stamp = time.strftime("%Y%m%d-%H%M%S")
    safe_model = args.model.replace("/", "_")
    tname = f"review_{safe_model}_{today}_{stamp}.md"
    tpath = er / tname
    tpath.write_text(review, encoding="utf-8")
    digest = sha256_bytes(tpath.read_bytes())

    rec_path = er / "record.json"
    rec = {"reviews": []}
    if rec_path.exists():
        try:
            rec = json.loads(rec_path.read_text(encoding="utf-8-sig"))
        except Exception:
            print("WARN record.json 解析失败，重建", file=sys.stderr)
    rec["reviews"] = [r for r in rec.get("reviews", []) if r.get("id") != args.model]
    rec["reviews"].append({
        "kind": "model",
        "id": args.model,
        "channel": "opencode zen gateway" if args.engine == "opencode" else args.base_url,
        "date": today,
        "independence": "小米自研 MiMo 系（opencode 免费网关），非 qwen/deepseek/llama/mistral/gemma/phi 家族；"
                        "与本项目作者无关联；仅输入论文 tex + 通用评审提示词",
        "access": ["paper/main.tex"],
        "transcripts": [tname],
        "sha256": [digest],
    })
    rec_path.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS transcript -> {tpath}（sha256 {digest[:12]}…）")
    print(f"PASS record.json 已更新（{len(rec['reviews'])} 条外部评审）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
