"""check_external_review.py — 外部评审闭环校验（关闭自证环的机器门）。

论文在 S7（封包）前必须完成 ≥1 次"外部评审"：真人合作者，或训练谱系独立于
本地模型家族的前沿云模型。评审记录放 papers/<paper>/external_review/：

  record.json:
  {
    "reviews": [
      {
        "kind": "human" | "model",
        "id": "张三 @ Univ." 或 "claude-sonnet-4-6 (Anthropic API)",
        "date": "2026-09-10",
        "independence": "非本工作区作者；未接触本地模型家族",
        "access": ["paper/main.pdf", "evidence_manifest.json"],
        "transcripts": ["review1.md"],
        "sha256": ["<每个 transcript 的 sha256，与 transcripts 一一对应>"]
      }
    ]
  }

本脚本只验机器可判的部分：record.json 存在且 reviews ≥ --min-reviews、
transcript 文件存在、sha256 匹配、kind=model 时 id 不命中本地模型家族名单。
评审内容质量（是否真批评）不在此验——由人工在 S6/S7 判读。

用法: python check_external_review.py <paper_dir> [--min-reviews 1]
退出码: 0 = 满足；1 = 不满足；2 = 参数错误
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

# 本地模型家族名单：kind=model 时 id 命中即判"不独立"。
# 判据：训练谱系与本地推理生态同源（qwen/deepseek/llama/mistral/gemma/phi
# 系 + 本地 ollama/RPC 网关），对工作区的写作套路有"同门"偏置风险。
LOCAL_FAMILY = [
    "qwen", "qwq", "deepseek", "llama", "mistral", "mixtral", "gemma",
    "phi-", "phi3", "phi4", "ollama", "127.0.0.1", "localhost", "vllm",
    "glm-4-flash", "internlm", "yi-",
]


def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description="外部评审闭环校验")
    ap.add_argument("paper_dir")
    ap.add_argument("--min-reviews", type=int, default=1)
    args = ap.parse_args()

    paper = Path(args.paper_dir).resolve()
    er = paper / "external_review"
    problems = []

    if not er.exists():
        print(f"FAIL external_review/ 目录缺失: {er}")
        print("     按 research-kit/review-workflow/EXTERNAL_REVIEW_PROTOCOL.md 完成 ≥1 次外部评审")
        return 1
    rec_path = er / "record.json"
    if not rec_path.exists():
        print(f"FAIL record.json 缺失: {rec_path}")
        return 1
    try:
        rec = json.loads(rec_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        print(f"FAIL record.json 解析失败: {exc}")
        return 1

    reviews = rec.get("reviews") or []
    if len(reviews) < args.min_reviews:
        problems.append(f"外部评审数 {len(reviews)} < 要求 {args.min_reviews}")

    for i, r in enumerate(reviews):
        tag = f"review[{i}]"
        kind = str(r.get("kind", ""))
        rid = str(r.get("id", ""))
        if kind not in ("human", "model"):
            problems.append(f"{tag}: kind 必须为 human|model，得到 {kind!r}")
        if not rid:
            problems.append(f"{tag}: id 缺失（真人姓名+单位，或 模型名+API 来源）")
        if not str(r.get("date", "")):
            problems.append(f"{tag}: date 缺失")
        if kind == "model" and any(k in rid.lower() for k in LOCAL_FAMILY):
            problems.append(f"{tag}: 模型 {rid!r} 命中本地家族名单，不构成独立评审")
        if not str(r.get("independence", "")):
            problems.append(f"{tag}: independence 声明缺失（评审人/模型与本项目无利益关联的说明）")
        transcripts = r.get("transcripts") or []
        digests = r.get("sha256") or []
        if not transcripts:
            problems.append(f"{tag}: transcripts 缺失（评审原文必须落盘）")
            continue
        if len(digests) != len(transcripts):
            problems.append(f"{tag}: sha256 条数({len(digests)})与 transcripts({len(transcripts)})不符")
        for t, d in zip(transcripts, digests):
            tp = er / t
            if not tp.exists():
                problems.append(f"{tag}: transcript 缺失 {t}")
                continue
            actual = sha256_of(tp)
            if str(d).lower() != actual:
                problems.append(f"{tag}: sha256 不符 {t}（record={d} actual={actual[:12]}…）")

    if problems:
        print("FAIL 外部评审闭环校验未通过：")
        for p in problems:
            print(f"     - {p}")
        return 1

    print(f"PASS external_review: {len(reviews)} 条外部评审，transcript+hash 齐全")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
