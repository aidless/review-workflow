# -*- coding: utf-8 -*-
"""审稿工作流编排器（run_review）— 一键执行 R0-R7。

把证据层四件套（包审计 / 清单哈希 / 数字对账 / 诚实性扫描）与文本层
LLM 对抗审查串成一条命令，统一落盘 run_summary.md（阶段表 + 门禁 + diff + 下一步命令）。

阶段:
  R0  输入登记      存在性 / 大小 / sha256 / 产物目录与论文不同源风险标记
  R1  论文静态审查  章节完整性 / 占位符 / 摘要词数 / 环境配对（信息层，仅 WARN）
  R1b 引用核验      citation_check —— 幽灵引用/占位标题；--online 联网核验 arXiv/DOI（ID 不存在 = FAIL）
  R1c 新颖性断言    novelty_check —— first/novel/据我们所知 断言抽取；novelty_online=true 时
                    arXiv 检索先行工作并比对（未引用近重复 = WARN）
  R1d 公式与算术    formula_check —— 行内算术重算（2+2=5 型手滑）+ 括号百分数一致性 +
                    悬空公式引用；符号推导/量纲不在机械覆盖内（已知边界，交给 R6+人工）
  R2  包审计        audit_package.audit —— 引用缺失 = FAIL(Critical)
  R2b 清单哈希核验  verify_manifest.verify —— 哈希不符/缺文件 = FAIL(Critical)
  R2c 图表数字核验  figure_check —— 图文件缺失 = FAIL；图注小数无支撑 = WARN（stale figure 探测）
  R2d 表格数字核验  table_check —— 表内 \\input 缺失 = FAIL(编译即断)；numeric cell 三层支撑链
                    （证据/表格外正文/无）+ 列内混精度（INFO）
  R3  数字对账      number_reconcile.reconcile —— 裁决 critical = FAIL；待复核 = WARN
  R4  统计复算      stats_recompute —— McNemar/Friedman/Wilson 重算，MISMATCH = FAIL(Critical)；
                    定性自动化（r4_llm）：口径换算机械层 + LLM 对抗裁决，NOT_IN_PAPER 全解释 → PASS
  R5  诚实性扫描    honesty_scan.scan —— suspicious = FAIL（一票否决）
  R6  LLM 对抗审查  RPC 健康检查 → adversarial_review.py（文本层，Critical/Major = WARN）
                    --converge N：跑 N 轮取轮间稳定问题（≥2 轮出现才计入门禁，降 LLM 噪声）
  R6b PRISM 四维    prism_review —— P 契合/R 严谨/I 贡献/S 诚实（LLM-as-judge，min 纪律，
                    任一维 ≤6 = WARN；RPC 不可达自动 SKIP）
  R6c 审稿人-作者辩论 debate —— R6/PRISM 问题清单经作者 rebuttal + 独立裁判终裁，
                    withdrawn = LLM 单轮假阳性被驳回；sustained Critical/Major = WARN；
                    仅严重度前 20 条进入辩论（MAX_ISSUES=20 成本控制，截断数在报告/metric 明示）
  R7  综合报告      run_summary.md + gates.json + suggested_score（min 维度半自动评分）

门禁纪律：overall = 最差阶段（FAIL > WARN > SKIP > PASS）。
R7 半自动评分（min 维度，不平均）：结构(R1/R1b/R1c/R1d) / 证据(R2/R2b/R2c/R2d/R3/R4/R5) / 文本(R6/R6b/R6c)
三维度各自映射分数（PASS=8, WARN/SKIP=6, FAIL=4），取 min；证据层 FAIL 直接 cap 4。
评分校准（calibrate.py）维护人工分对照日志，n≥5 前只当排序信号用。
人工阶段（R5 诚实性定性 / R3 裁决收敛 / R4 llm_failed 补判）未完成前 suggested_score 是临时值。

PDF 输入模式：config 提供 "pdf" 而非 "tex" 时，自动提取文本为伪 tex 供 R1/R3/R4/R5/R6；
R2/R2b/R1b/R1c/R1d/R2c/R2d 降级 SKIP（无源码无法审计包内一致性、bib 结构、图表与表格语义）。

可移植性：无硬编码盘符——LLM 脚本按 REVIEW_LLM_SCRIPT 环境变量 → review-workflow 上级
目录 → 历史路径自动发现；换机器先跑 `--doctor` 环境自检，依赖见 requirements.txt
（核心零第三方依赖；scipy/pymupdf 可选，缺失自动降级 SKIP）。

用法:
    python run_review.py --config <config.json> [--stages R0,R2,R3] [--skip-llm] [--diff <旧run目录>]
                         [--converge 3]
    python run_review.py --batch <configs目录 | list.json> [--skip-llm]
    python run_review.py --doctor
    python run_review.py --init <新config.json>
    python run_review.py --selftest

配置 schema:
{
  "name": "scievalsuite_v6",
  "tex": "F:/.../main.tex",             // 与 "pdf" 二选一
  "pdf": null,                           // PDF-only 审稿：提供后 tex 可为 null
  "zip": "F:/.../submission.zip",
  "evidence_dirs": ["F:/.../results"],
  "manifest": null,                    // 可选：zip 内 manifest 相对路径（默认自动发现）
  "adjudications": "F:/.../adj.json",  // 可选：R3 人工裁决持久化文件
  "bib": null,                          // 可选：R1b 显式指定 bib（默认从 tex 同目录发现）
  "citation_online": true,              // R1b 联网核验 arXiv/DOI（默认 false 仅结构检查）
  "novelty_online": false,              // R1c 联网检索 arXiv 先行工作对照新颖性断言
  "prism": true,                        // R6b PRISM 四维自评（LLM；默认开，RPC 不可达自动 SKIP）
  "debate": true,                       // R6c 审稿人-作者辩论（LLM；默认开）
  "r4_llm": true,                       // R4 统计定性自动化（口径换算机械层 + LLM 对抗裁决；默认开，RPC 不可达自动 SKIP）
  "converge": 1,                        // R6 轮数（≥2 时启用轮间稳定性过滤）
  "llm": {"enabled": true, "script": "F:/deepseek/research-kit/adversarial_review.py",
           "rpc": "http://127.0.0.1:3080", "roles": "all"},
  "out": "F:/.../runs/name"
}
"""
from __future__ import annotations

import argparse
import hashlib
import difflib
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

import audit_package  # noqa: E402
import honesty_scan  # noqa: E402
import number_reconcile  # noqa: E402
import verify_manifest  # noqa: E402

try:
    import citation_check  # noqa: E402  # scipy/网络无关，纯标准库
except Exception as _e:  # noqa: BLE001  # scipy/网络无关，纯标准库
    citation_check = None

try:
    import stats_recompute  # noqa: E402  # 需要 scipy
except Exception:  # noqa: BLE001
    stats_recompute = None

try:
    import figure_check  # noqa: E402  # 纯标准库（pymupdf 按需延迟导入）
except Exception:  # noqa: BLE001
    figure_check = None

try:
    import novelty_check  # noqa: E402  # 纯标准库（arXiv API 按需）
except Exception:  # noqa: BLE001
    novelty_check = None

try:
    import prism_review  # noqa: E402  # LLM-as-judge（RPC 按需）
except Exception:  # noqa: BLE001
    prism_review = None

try:
    import debate  # noqa: E402  # LLM 辩论（RPC 按需）
except Exception:  # noqa: BLE001
    debate = None

try:
    import pdf_text  # noqa: E402  # 需要 PyMuPDF
except Exception:  # noqa: BLE001
    pdf_text = None

try:
    import formula_check  # noqa: E402  # R1d 纯标准库
except Exception:  # noqa: BLE001
    formula_check = None

try:
    import table_check  # noqa: E402  # R2d 纯标准库（复用 number_reconcile）
except Exception:  # noqa: BLE001
    table_check = None


def _default_llm_script() -> str:
    """可移植的 adversarial_review.py 发现：环境变量 > 环境相对路径 > 历史盘符。

    顺序：REVIEW_LLM_SCRIPT 环境变量 → research-kit 同级目录（review-workflow 的
    上级）→ 历史 F:/deepseek/research-kit（本工具的出生地，存在才用）。
    换机器只需把 review-workflow 目录整体拷走，无需改代码。"""
    import os
    env = os.environ.get("REVIEW_LLM_SCRIPT")
    if env:
        return env
    here = SCRIPTS_DIR.parents[1]          # .../research-kit
    if (here / "adversarial_review.py").is_file():
        return str(here / "adversarial_review.py")
    legacy = Path("F:/deepseek/research-kit/adversarial_review.py")
    return str(legacy if legacy.is_file() else here / "adversarial_review.py")


DEFAULT_LLM = {
    "enabled": True,
    "script": _default_llm_script(),
    "rpc": "http://127.0.0.1:3080",
    "roles": "all",
}
ALL_STAGES = ["R0", "R1", "R1b", "R1c", "R1d", "R2", "R2b", "R2c", "R2d", "R3", "R4",
              "R5", "R6", "R6b", "R6c", "R7"]
GATE_ORDER = {"PASS": 0, "SKIP": 1, "WARN": 2, "FAIL": 3}
GATE_SCORE = {"PASS": 8, "SKIP": 6, "WARN": 6, "FAIL": 4}  # TMLR 10 分制，min 维度
# 各阶段报告落盘文件名：增量运行（--stages 子集）时据此回载未重跑阶段的 verdict
STAGE_REPORTS = {
    "R0": "r0_registration.json", "R1": "r1_static.json", "R1b": "citation_check.json",
    "R1c": "novelty_check.json", "R1d": "formula_check.json", "R2": "audit_report.json",
    "R2b": "verify_manifest.json", "R2c": "figure_check.json", "R2d": "table_check.json",
    "R3": "number_reconcile.json", "R4": "stats_recompute.json", "R5": "honesty_scan.json",
    "R6": "r6_llm.json", "R6b": "prism_review.json", "R6c": "debate.json",
}

SECTION_NEEDS = [
    ("abstract", r"\\begin\{abstract\}"),
    ("introduction", r"\\section\*?\{[^}]*Intro"),
    ("related", r"\\(sub)?section\*?\{[^}]*Relat"),
    ("method", r"\\section\*?\{[^}]*(Method|Approach|Benchmark|Suite|Framework|Design)"),
    ("results", r"\\section\*?\{[^}]*(Result|Experiment|Evaluation|Analysis)"),
    ("discussion", r"\\(sub)?section\*?\{[^}]*Discuss"),
    ("limitations", r"\\(sub)?section\*?\{[^}]*Limitation"),
    ("conclusion", r"\\section\*?\{[^}]*Conclu"),
]
# PDF 提取文本（无 LaTeX 命令）用的标题模式
SECTION_NEEDS_PDF = [
    ("abstract", r"(?m)^\s*Abstract\b"),
    ("introduction", r"(?m)^\s*\d*\.?\s*Introduction\b"),
    ("related", r"(?m)^\s*\d*\.?\s*\d*\.?\s*Related\s+Work\b"),
    ("method", r"(?m)^\s*\d*\.?\s*\d*\.?\s*(Methods?|Approaches?|Benchmarks?|Suites?|Frameworks?|Designs?)\b"),
    ("results", r"(?m)^\s*\d*\.?\s*\d*\.?\s*(Results?|Experiments?|Evaluations?|Analys[ie]s)\b"),
    ("discussion", r"(?m)^\s*\d*\.?\s*\d*\.?\s*Discussions?\b"),
    ("limitations", r"(?m)^\s*\d*\.?\s*\d*\.?\s*Limitations?\b"),
    ("conclusion", r"(?m)^\s*\d*\.?\s*(Conclusions?)\b"),
]
PLACEHOLDER_RE = re.compile(r"\b(TODO|FIXME|TBD|XXX)\b|\?\?\?")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dump_json(obj: dict, p: Path) -> None:
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def gate_of(verdict: str | None) -> str:
    if verdict in ("CRITICAL", "ERROR"):
        return "FAIL"
    if verdict == "MAJOR":
        return "WARN"
    return "PASS"


def resolve_source(cfg: dict, out: Path) -> tuple[Path | None, bool, str]:
    """返回 (审稿用文本路径, pdf_mode, 说明)。tex 优先；否则 pdf 提取伪 tex。"""
    tex = Path(cfg["tex"]) if cfg.get("tex") else None
    if tex and tex.is_file():
        return tex, False, "tex 源码模式"
    pdf = Path(cfg["pdf"]) if cfg.get("pdf") else None
    if pdf and pdf.is_file():
        if pdf_text is None:
            return None, True, "PyMuPDF 未安装，无法提取 PDF 文本"
        text = pdf_text.extract_text(pdf)
        pseudo = out / "extracted_text.txt"
        pseudo.write_text(text, encoding="utf-8")
        stats = pdf_text.extract_stats(text)
        return pseudo, True, (f"PDF 模式：{pdf.name} → 伪 tex（{stats['chars']} 字符，"
                              f"{stats['decimals']} 个小数）；R2/R2b/R1b 降级 SKIP")
    return None, False, "tex 与 pdf 均不可用"


# ---------------------------------------------------------------- R0 输入登记

def stage_r0(cfg: dict, src_note: str) -> tuple[dict, str, str]:
    tex = Path(cfg["tex"]) if cfg.get("tex") else None
    pdf = Path(cfg["pdf"]) if cfg.get("pdf") else None
    zp = Path(cfg["zip"]) if cfg.get("zip") else None
    evs = [Path(p) for p in cfg.get("evidence_dirs", [])]

    problems = []
    if (not tex or not tex.is_file()) and (not pdf or not pdf.is_file()):
        problems.append(f"tex 与 pdf 均不存在或未配置：tex={cfg.get('tex')} pdf={cfg.get('pdf')}")
    if zp is not None and not zp.is_file():
        problems.append(f"zip 不存在: {zp}")
    for d in evs:
        if not d.is_dir():
            problems.append(f"evidence 目录不存在: {d}")

    risk = []
    anchor = (tex or pdf or Path(".")).parent.parent  # paper/ 的上一级 = 项目根
    for d in evs:
        try:
            d.resolve().relative_to(anchor.resolve())
        except ValueError:
            risk.append(str(d))

    def _reg(p: Path | None) -> dict | None:
        return ({"path": str(p), "size": p.stat().st_size,
                 "sha256": sha256_file(p)} if p and p.is_file() else None)

    report = {
        "meta": {"timestamp": now(), "stage": "R0", "source_mode": src_note},
        "inputs": {
            "name": cfg.get("name", (tex or pdf or Path("paper")).parent.name),
            "tex": _reg(tex),
            "pdf": _reg(pdf),
            "zip": _reg(zp),
            "evidence_dirs": [{"path": str(d), "exists": d.is_dir()} for d in evs],
        },
        "cross_source_risk": risk,
        "problems": problems,
        "summary": {
            "problems": len(problems),
            "cross_source_risk": len(risk),
            "verdict": "ERROR" if problems else ("MAJOR" if risk else "PASS"),
        },
    }
    gate = "FAIL" if problems else ("WARN" if risk else "PASS")
    metric = f"缺失输入 {len(problems)}，跨源风险目录 {len(risk)}" + (
        f"（{risk[0]} 不在 {anchor} 下 → 打包遗漏高风险）" if risk else "")
    return report, gate, metric


# ---------------------------------------------------------------- R1 静态审查

def stage_r1(cfg: dict, tex_path: Path, pdf_mode: bool) -> tuple[dict, str, str]:
    tex = tex_path.read_text(encoding="utf-8", errors="replace")
    if pdf_mode:
        # PDF 提取文本常把多个标题挤在一行（以连续空格分隔）→ 拆行再匹配标题
        tex = re.sub(r"[ \t]{3,}", "\n", tex)

    needs = SECTION_NEEDS_PDF if pdf_mode else SECTION_NEEDS
    missing_sections = [name for name, pat in needs if not re.search(pat, tex, re.I)]

    placeholders = []
    for i, line in enumerate(tex.splitlines(), 1):
        if m := PLACEHOLDER_RE.search(line):
            placeholders.append({"line": i, "token": m.group(0), "context": line.strip()[:100]})

    abstract_words = None
    if pdf_mode:
        if m := re.search(r"(?im)^\s*Abstract\b[:.\s]*(.+?)(?=\n\s*\n|\n\s*1\s*\.|\Z)", tex):
            abstract_words = len(re.sub(r"\\[a-zA-Z]+|[{}$%]", " ", m.group(1)).split())
    elif m := re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S):
        abstract_words = len(re.sub(r"\\[a-zA-Z]+|[{}$%]", " ", m.group(1)).split())

    envs = {}
    if not pdf_mode:
        for m in re.finditer(r"\\(begin|end)\{([a-zA-Z*]+)\}", tex):
            envs.setdefault(m.group(2), {"begin": 0, "end": 0})[m.group(1)] += 1
    unbalanced = [e for e, c in envs.items() if c["begin"] != c["end"]]

    warns = []
    if missing_sections:
        warns.append(f"章节缺失 {missing_sections}")
    if placeholders:
        warns.append(f"占位符 {len(placeholders)} 处")
    if unbalanced:
        warns.append(f"环境不配对 {unbalanced}")
    if abstract_words is None:
        warns.append("未找到 abstract" + ("（PDF 提取文本）" if pdf_mode else " 环境"))
    elif abstract_words > 300:
        warns.append(f"摘要 {abstract_words} 词（>300）")

    report = {
        "meta": {"timestamp": now(), "stage": "R1", "pdf_mode": pdf_mode},
        "sections_found": [n for n, _ in needs if n not in missing_sections],
        "missing_sections": missing_sections,
        "placeholders": placeholders,
        "abstract_words": abstract_words,
        "unbalanced_envs": unbalanced,
        "summary": {"verdict": "MAJOR" if warns else "PASS", "warns": warns},
    }
    gate = "WARN" if warns else "PASS"
    metric = "；".join(warns) if warns else f"章节 {len(needs) - len(missing_sections)}/{len(needs)}，无占位符，摘要 {abstract_words} 词"
    return report, gate, metric


# ---------------------------------------------------------------- R1b 引用核验

def stage_r1b(cfg: dict, tex_path: Path, pdf_mode: bool) -> tuple[dict, str, str]:
    if citation_check is None:
        return ({"meta": {"stage": "R1b", "timestamp": now()}, "summary": {"verdict": None}},
                "SKIP", "citation_check 模块不可用")
    if pdf_mode:
        return ({"meta": {"stage": "R1b", "timestamp": now(), "pdf_mode": True},
                 "summary": {"verdict": None, "reason": "pdf_mode"}},
                "SKIP", "PDF 模式：无 bib 源，引用核验降级 SKIP")
    bib = citation_check.find_bib(tex_path, Path(cfg["bib"]) if cfg.get("bib") else None)
    if bib is None:
        return ({"meta": {"stage": "R1b", "timestamp": now()},
                 "summary": {"verdict": None, "reason": "no_bib"}},
                "SKIP", "未找到 bib（tex 同目录无 .bib、\\bibliography 未指向存在的文件）")

    online = bool(cfg.get("citation_online", False))
    rep = citation_check.run_check(tex_path, bib, online)
    citation_check.write_md(rep, Path(cfg["_out"]) / "citation_check.md")
    s = rep["summary"]
    gate = gate_of(s["verdict"])
    metric = (f"{s['verdict']}：条目 {s['entries']}，幽灵引用 {s['ghost_citations']}，"
              f"结构 Major {s['structural_major']}"
              + (f"，ID 不存在 {s['not_found']}，标题不符 {s['title_mismatch']}（联网核验 {s['online_checked']} 条）"
                 if online else "（offline 结构检查）"))
    return rep, gate, metric


# ---------------------------------------------------------------- R1c 新颖性断言对照

def stage_r1c(cfg: dict, tex_path: Path, pdf_mode: bool) -> tuple[dict, str, str]:
    if novelty_check is None:
        return ({"meta": {"stage": "R1c", "timestamp": now()}, "summary": {"verdict": None}},
                "SKIP", "novelty_check 模块不可用")
    if pdf_mode:
        return ({"meta": {"stage": "R1c", "timestamp": now(), "pdf_mode": True,
                          "summary": {"verdict": None}}},
                "SKIP", "PDF 模式：无 \\title 源码，断言对照降级 SKIP")
    if not cfg.get("novelty_online"):
        return ({"meta": {"stage": "R1c", "timestamp": now()},
                 "summary": {"verdict": None, "reason": "offline"}},
                "SKIP", "未启用联网检索（config 设 novelty_online=true 开启 arXiv 先行工作对照）")
    bib = None
    if citation_check is not None:
        bib = citation_check.find_bib(tex_path, Path(cfg["bib"]) if cfg.get("bib") else None)
    rep = novelty_check.run_check(tex_path, bib, online=True)
    novelty_check.write_md(rep, Path(cfg["_out"]) / "novelty_check.md")
    dump_json(rep, Path(cfg["_out"]) / "novelty_check.json")
    s = rep["summary"]
    if s["verdict"] == "SKIP":
        return rep, "SKIP", f"断言 {s['claims_total']} 句（强 {s['claims_strong']}）；arXiv 检索降级：{s.get('detail', '')}"
    gate = gate_of(s["verdict"])
    metric = (f"{s['verdict']}：断言 {s['claims_total']} 句（强 {s['claims_strong']}）；检索 {s['online_results']} 条，"
              f"近重复 {s['related_found']}（未引用 {s['related_uncited']}）")
    return rep, gate, metric


# ---------------------------------------------------------------- R1d 公式与算术核验

def stage_r1d(cfg: dict, out: Path, tex_path: Path | None, pdf_mode: bool) -> tuple[dict, str, str]:
    if formula_check is None:
        return ({"meta": {"stage": "R1d", "timestamp": now()}, "summary": {"verdict": None}},
                "SKIP", "formula_check 模块不可用")
    if pdf_mode or tex_path is None:
        return ({"meta": {"stage": "R1d", "timestamp": now(), "pdf_mode": pdf_mode,
                          "summary": {"verdict": None}}},
                "SKIP", "PDF 模式：无 tex 源码，行内算术/公式引用核验降级 SKIP")
    rep = formula_check.check(tex_path)
    formula_check.write_md(rep, out / "formula_check.md")
    dump_json(rep, out / "formula_check.json")
    s = rep["summary"]
    gate = gate_of(s["verdict"])
    metric = (f"{s['verdict']}：行内算术 {s['arith_total']} 处（不符 {s['arith_mismatch']}"
              f"，含括号百分数 {s['paren_pct_mismatch']}）；悬空公式引用 {s['dangling_refs']}"
              "；符号推导/量纲不在机械覆盖内")
    return rep, gate, metric


# ---------------------------------------------------------------- R2 包审计

def stage_r2(cfg: dict, out: Path, tex_path: Path | None, pdf_mode: bool) -> tuple[dict, str, str]:
    if not cfg.get("zip"):
        return (
            {"meta": {"stage": "R2", "timestamp": now()}, "summary": {"verdict": None}},
            "SKIP", "未配置 zip（仅磁盘审查）",
        )
    if pdf_mode or tex_path is None:
        return (
            {"meta": {"stage": "R2", "timestamp": now(), "pdf_mode": pdf_mode,
                      "summary": {"verdict": None}}},
            "SKIP", "PDF 模式：无 tex 源码，包审计降级 SKIP（zip-vs-disk desync 无法核验）",
        )
    rep = audit_package.audit(Path(cfg["zip"]), tex_path)
    audit_package.write_md(rep, out / "audit_report.md")
    dump_json(rep, out / "audit_report.json")
    s = rep["summary"]
    gate = gate_of(s["verdict"])
    metric = f"{s['verdict']}：缺引用 {s['refs_missing']}/{s['refs_total']}，路径泄漏 {s['leaks']}，声明不符 {s['count_claims_mismatched']}，tex desync {s['tex_desync']}"
    return rep, gate, metric


# ---------------------------------------------------------------- R2b 清单哈希

def stage_r2b(cfg: dict, out: Path, tex_path: Path | None, pdf_mode: bool) -> tuple[dict, str, str]:
    if not cfg.get("zip"):
        return (
            {"meta": {"stage": "R2b", "timestamp": now()}, "summary": {"verdict": None}},
            "SKIP", "未配置 zip",
        )
    if pdf_mode or tex_path is None:
        return (
            {"meta": {"stage": "R2b", "timestamp": now(), "pdf_mode": pdf_mode},
             "summary": {"verdict": None}},
            "SKIP", "PDF 模式：无 tex 源码，清单核验降级 SKIP",
        )
    rep = verify_manifest.verify(
        Path(cfg["zip"]),
        Path(cfg["manifest"]) if cfg.get("manifest") else None,
        None,
        tex_path,
    )
    verify_manifest.write_md(rep, out / "verify_manifest.md")
    dump_json(rep, out / "verify_manifest.json")
    if "error" in rep:
        return rep, "WARN", f"清单核验跳过：{rep['error']}"
    s = rep["summary"]
    gate = gate_of(s["verdict"])
    metric = f"{s['verdict']}：清单 {s['manifest_entries']} 条，OK {s['ok']}，哈希不符 {s['hash_mismatch']}，缺失 {s['missing']}"
    return rep, gate, metric


# ---------------------------------------------------------------- R2c 图表数字核验

def stage_r2c(cfg: dict, out: Path, tex_path: Path | None, pdf_mode: bool) -> tuple[dict, str, str]:
    if figure_check is None:
        return ({"meta": {"stage": "R2c", "timestamp": now()}, "summary": {"verdict": None}},
                "SKIP", "figure_check 模块不可用")
    if pdf_mode or tex_path is None:
        return ({"meta": {"stage": "R2c", "timestamp": now(), "pdf_mode": pdf_mode,
                          "summary": {"verdict": None}}},
                "SKIP", "PDF 模式：无 \\includegraphics 源码，图表核验降级 SKIP")
    dirs = [Path(p) for p in cfg.get("evidence_dirs", [])]
    rep = figure_check.check(tex_path, dirs)
    figure_check.write_md(rep, out / "figure_check.md")
    dump_json(rep, out / "figure_check.json")
    s = rep["summary"]
    gate = gate_of(s["verdict"])
    metric = (f"{s['verdict']}：图 {s['figures_referenced']} 幅（矢量文本 {s['text_extracted']}，"
              f"位图跳过 {s['raster_skipped']}，缺失 {s['missing']}）；图注小数 {s['caption_decimals']} 个，"
              f"无支撑 {s['unsupported']}；figure_only {s['figure_only']}")
    return rep, gate, metric


# ---------------------------------------------------------------- R2d 表格数字核验

def stage_r2d(cfg: dict, out: Path, tex_path: Path | None, pdf_mode: bool) -> tuple[dict, str, str]:
    if table_check is None:
        return ({"meta": {"stage": "R2d", "timestamp": now()}, "summary": {"verdict": None}},
                "SKIP", "table_check 模块不可用")
    if pdf_mode or tex_path is None:
        return ({"meta": {"stage": "R2d", "timestamp": now(), "pdf_mode": pdf_mode,
                          "summary": {"verdict": None}}},
                "SKIP", "PDF 模式：无 tabular 源码，表格核验降级 SKIP")
    dirs = [Path(p) for p in cfg.get("evidence_dirs", [])]
    rep = table_check.check(tex_path, dirs)
    table_check.write_md(rep, out / "table_check.md")
    dump_json(rep, out / "table_check.json")
    s = rep["summary"]
    gate = gate_of(s["verdict"])
    metric = (f"{s['verdict']}：表 {s['tables']} 个（numeric cell {s['numeric_cells']}），"
              f"无支撑 {s['unsupported']}，\\input 缺失 {s['missing_inputs']}，混精度列 {s['precision_anomalies']}（INFO）")
    return rep, gate, metric


# ---------------------------------------------------------------- R3 数字对账

def stage_r3(cfg: dict, out: Path, tex_path: Path, skip_llm: bool = False) -> tuple[dict, str, str]:
    adj_path = Path(cfg["adjudications"]) if cfg.get("adjudications") else None
    adj = {}
    if adj_path and adj_path.exists():
        adj = json.loads(adj_path.read_text(encoding="utf-8"))
    dirs = [Path(p) for p in cfg.get("evidence_dirs", [])]
    rep = number_reconcile.reconcile(tex_path, dirs, adj)
    number_reconcile.write_md(rep, out / "number_reconcile.md")
    dump_json(rep, out / "number_reconcile.json")

    # R3 裁决自动化：机械层 + LLM 语义裁决待复核 token（config r3_llm 默认开；skip_llm/llm.enabled=false 时跳过）
    llm_cfg = cfg.get("llm") or {}
    r3_qual = None
    if (cfg.get("r3_llm", True) and not skip_llm and llm_cfg.get("enabled", True)
            and rep["summary"].get("pending_review")):
        rpc_url = llm_cfg.get("rpc", "http://127.0.0.1:3080")
        r3_adj_path = out / "r3_adjudications.json"
        r3_existing = None
        if r3_adj_path.exists():
            try:
                r3_existing = json.loads(r3_adj_path.read_text(encoding="utf-8"))
                print(f"  [R3] 载入断点 {len(r3_existing.get('adjudications', []))} 条已裁决", flush=True)
            except Exception:  # noqa: BLE001
                r3_existing = None
        r3_qual = number_reconcile.adjudicate_pending(rep, tex_path, rpc_url=rpc_url,
                                                      existing=r3_existing, checkpoint=r3_adj_path,
                                                      max_llm=int(cfg.get("r3_max_llm", 100)))
        if r3_qual["adjudications"]:
            dump_json(r3_qual, r3_adj_path)
            number_reconcile.write_r3_md(r3_qual, out / "r3_adjudications.md")
        else:
            print(f"  [R3] 裁决无结果（{r3_qual['meta'].get('rpc_health', '-')}）→ 保留既有断点", flush=True)
        if adj_path:
            merged = dict(adj)
            for a in r3_qual["adjudications"]:
                if a.get("verdict") in number_reconcile.R3_VERDICTS:
                    merged[a["token"]] = {"verdict": a["verdict"],
                                          "note": (a.get("justification") or "")[:200],
                                          "context": (a.get("evidence") or "")[:120],
                                          "layer": a.get("layer")}
            state = {
                "_meta": {
                    "usage": "verdict: noise=误报(版本/日期/派生/维度) | supported=人工确认有来源 | critical=真实无支撑 → 一票 Critical | pending=待判",
                    "updated": now(),
                    "pending": sum(1 for v in merged.values() if isinstance(v, dict) and v.get("verdict") == "pending"),
                },
                **merged,
            }
            adj_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    if adj_path:
        state = {
            "_meta": {
                "usage": "verdict: noise=误报 | supported=人工确认有来源 | critical=真实无支撑(一票Critical) | pending=待判",
                "updated": now(),
                "pending": sum(1 for v in rep["adjudications_state"].values()
                               if isinstance(v, dict) and v.get("verdict") == "pending"),
            },
            **rep["adjudications_state"],
        }
        adj_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    s = rep["summary"]
    if not dirs and s.get("critical_adjudicated", 0) == 0:
        # 无证据目录：数字对账无从进行（PDF-only/第三方论文评审）——降级 SKIP 而非 FAIL。
        # "投稿未附证据包"属 R2/R2b 包审计职责；人工裁决 critical 仍然一票 FAIL。
        gate = "SKIP"
        metric = (f"SKIP 无证据目录：数字不可核验（论文小数 {s.get('paper_decimals')}，"
                  f"机械噪音 {s['noise_filtered']}，待复核 {s['pending_review']} 清单备查）")
    else:
        gate = gate_of(s["verdict"])
        metric = f"{s['verdict']}：待复核 {s['pending_review']}，机械噪音 {s['noise_filtered']}，已裁决 {s['adjudicated']}（critical {s['critical_adjudicated']}）"
        if r3_qual:
            q = r3_qual["summary"]
            if q.get("verdict") and q["verdict"] != "SKIP":
                gate = gate_of(q["verdict"])  # 裁决层合成门禁：critical→FAIL，未裁决→维持 WARN，全裁决→PASS
            metric += (f"；裁决 {q.get('verdict', '-')}（mech {q.get('mechanical', 0)} / "
                       f"llm {q.get('llm', 0)} / noise {q.get('noise', 0)} / "
                       f"supported {q.get('supported', 0)} / critical {q.get('critical', 0)} / "
                       f"llm_failed {q.get('llm_failed', 0)}）")
    return rep, gate, metric


# ---------------------------------------------------------------- R4 统计复算

def stage_r4(cfg: dict, out: Path, tex_path: Path, skip_llm: bool = False) -> tuple[dict, str, str]:
    if stats_recompute is None:
        return ({"meta": {"stage": "R4", "timestamp": now()},
                 "summary": {"verdict": None, "reason": "scipy missing"}},
                "SKIP", "stats_recompute 模块不可用（scipy 未安装）")
    dirs = [Path(p) for p in cfg.get("evidence_dirs", [])]
    rep = stats_recompute.recompute(tex_path, dirs)
    stats_recompute.write_md(rep, out / "stats_recompute.md")
    dump_json(rep, out / "stats_recompute.json")
    s = rep["summary"]
    gate = gate_of(s["verdict"])
    metric = (f"{s['verdict']}：统计记录 {s['records']} 条（MATCH {s['match']}，MISMATCH {s['mismatch']}，"
              f"NOT_IN_PAPER {s['not_in_paper']}）——McNemar/Friedman/Wilson 复算")
    # R4 统计定性自动化：口径换算机械层 + LLM 对抗裁决层（config r4_llm 默认开；skip_llm/llm.enabled=false 时跳过）
    llm_cfg = cfg.get("llm") or {}
    if (cfg.get("r4_llm", True) and not skip_llm and llm_cfg.get("enabled", True)
            and (s["mismatch"] or s["not_in_paper"])):
        rpc_url = llm_cfg.get("rpc", "http://127.0.0.1:3080")
        qual = stats_recompute.adjudicate_qualitative(rep, tex_path, rpc_url=rpc_url)
        dump_json(qual, out / "stats_adjudications.json")
        stats_recompute.write_qual_md(qual, out / "stats_adjudications.md")
        q = qual["summary"]
        if q.get("verdict") and q["verdict"] != "SKIP":
            gate = gate_of(q["verdict"])  # 定性层合成门禁：口径换算/噪音→PASS，遗漏/疑似矛盾→WARN，MISMATCH 恒 FAIL
        metric += (f"；定性 {q.get('verdict', '-')}（resolved {q.get('resolved', 0)} / "
                   f"sustained {q.get('sustained', 0)} / llm_failed {q.get('llm_failed', 0)}）")
    return rep, gate, metric


# ---------------------------------------------------------------- R5 诚实性

def stage_r5(cfg: dict, out: Path, tex_path: Path) -> tuple[dict, str, str]:
    dirs = [Path(p) for p in cfg.get("evidence_dirs", [])]
    # 人工 allowlist（治理决议 2026-09-06，用户批准）：config honesty_allowlist 显式路径优先，否则 out/honesty_allowlist.json
    allow, allow_src = [], None
    cand = cfg.get("honesty_allowlist") or (out / "honesty_allowlist.json")
    try:
        if cand and Path(cand).exists():
            allow = json.loads(Path(cand).read_text(encoding="utf-8"))
            allow_src = str(cand)
    except Exception:
        allow = []
    rep = honesty_scan.scan(tex_path, dirs, allowlist=allow)
    rep.setdefault("meta", {})["honesty_allowlist"] = allow_src
    honesty_scan.write_md(rep, out / "honesty_scan.md")
    dump_json(rep, out / "honesty_scan.json")
    s = rep["summary"]
    gate = gate_of(s["verdict"])
    metric = (f"{s['verdict']}：hint 命中 {s['hint_hits']}（有效 {s.get('effective', s['hint_hits'])}）"
              f"，可疑 {s['suspicious']}（一票否决），已披露 {s['disclosed']}（含人工 allowlist {s.get('allowlisted', 0)}）")
    return rep, gate, metric


# ---------------------------------------------------------------- R6 LLM 对抗

def rpc_health(url: str, timeout: float = 4.0) -> tuple[bool, str]:
    try:
        with urllib.request.urlopen(url.rstrip("/"), timeout=timeout) as r:
            return True, f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        return True, f"HTTP {e.code}（服务在监听）"
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


def count_severities(obj) -> dict:
    counts = {"Critical": 0, "Major": 0, "Minor": 0}

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in counts and isinstance(v, list):
                    counts[k] += len(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(obj)
    return counts


def _norm_issue(text: str) -> str:
    """轮间问题匹配键：去空白/标点/前缀标记，小写，截断 120 字符。"""
    t = re.sub(r"^\s*[-*]?\s*(critical|major|minor)\s*[:：]\s*", "", text, flags=re.I)
    t = re.sub(r"[\s\W_]+", "", t.lower())
    return t[:120]


SEV_ORDER = {"Critical": 3, "Major": 2, "Minor": 1}
SIM_JACCARD = 0.50   # 轮间问题匹配：英文技术词元 Jaccard 阈值
SIM_RATIO = 0.62     # 词元贫乏(<3 词)时的字符相似度兜底阈值
_EN_STOP = frozenset(
    "the a an of to in on for and or with without not no is are was were be been "
    "this that these those it its as at by from but only both all any some "
    "may might can could should would will shall must vs".split())


def _issue_tokens(text: str) -> frozenset:
    """问题文本 → 英文技术词元集（≥2 字母词 + 数字，去停用词）。

    刻意不含中文 bigram：实测中文措辞漂移使 Jaccard 分母爆炸（top 对从 143 → 2），
    而英文技术词（模型名/统计量/数字）是 LLM 复述中唯一稳定的锚点。"""
    t = re.sub(r"^\s*[-*]?\s*\**\s*(critical|major|minor)\s*\**\s*[:：]\s*", "", text, flags=re.I)
    return frozenset(w for w in re.findall(r"[a-zA-Z]{2,}|\d+(?:\.\d+)?", t.lower())
                     if w not in _EN_STOP)


def _pair_match(k1: str, t1: frozenset, k2: str, t2: frozenset) -> bool:
    """两问题是否同一：词元丰富走 Jaccard，贫乏走字符 ratio（近逐字复述）。"""
    if len(t1) >= 3 and len(t2) >= 3:
        if len(t1 & t2) / len(t1 | t2) >= SIM_JACCARD:
            return True
    sm = difflib.SequenceMatcher(None, k1, k2)
    return (sm.real_quick_ratio() >= SIM_RATIO and sm.quick_ratio() >= SIM_RATIO
            and sm.ratio() >= SIM_RATIO)


def _fuzzy_merge(rounds_issues: list[dict]) -> dict:
    """跨轮合并问题：模糊匹配（LLM 复述措辞漂移，精确键匹配会漏）+ 传递性聚类。

    实测教训：qwen2.5:7b 三轮各报 ~20 Critical，但措辞每轮重组，规范化精确匹配后
    stable=0 / unstable=185 —— 全部误判为噪声、门禁虚假 PASS。改为英文技术词元
    Jaccard 匹配后，同一问题的不同措辞归并；rounds 取并集、严重度取更差者。
    传递性聚类（alias 表）解决 A~B、B~C 但 A!~C 的链式漂移。"""
    merged: dict[str, dict] = {}
    alias: dict[str, str] = {}       # 任意键 → 代表键（含被吸收的近义键）
    tok: dict[str, frozenset] = {}
    for issues in rounds_issues:
        for key, it in issues.items():
            tok.setdefault(key, _issue_tokens(it["text"]))
            hit = alias.get(key)
            if hit is None:
                best_k, best_score = None, -1.0
                for k in alias:                    # 全量检查：Jaccard 命中或字符兜底命中均可
                    if _pair_match(key, tok[key], k, tok[k]):
                        t1, t2 = tok[key], tok[k]
                        s = len(t1 & t2) / len(t1 | t2) if (t1 and t2) else 0.0
                        if s > best_score:
                            best_k, best_score = k, s
                if best_k is not None:
                    hit = alias[best_k]
            if hit is None:
                merged[key] = dict(it)
                merged[key]["roles"] = set(it.get("roles") or set())
                alias[key] = key
            else:
                merged[hit]["rounds"] |= it["rounds"]
                merged[hit]["roles"] |= set(it.get("roles") or set())
                if SEV_ORDER.get(it["sev"], 0) > SEV_ORDER.get(merged[hit]["sev"], 0):
                    merged[hit]["sev"] = it["sev"]      # 严重度取更差者，代表文本同步
                    merged[hit]["text"] = it["text"]
                alias[key] = hit
    return merged


def _parse_round_json(j: Path, round_no: int) -> dict | None:
    try:
        data = json.loads(j.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None
    counts, issues = {"Critical": 0, "Major": 0, "Minor": 0}, {}
    for rec in data:
        role = rec.get("role") or "unknown"
        for sev in ("Critical", "Major", "Minor"):
            items = (rec.get("issues") or {}).get(sev) or []
            counts[sev] += len(items)
            for it in items:
                key = _norm_issue(it)
                if key not in issues:
                    issues[key] = {"sev": sev, "text": it[:200], "rounds": {round_no},
                                   "roles": {role}}
                else:
                    issues[key]["roles"] |= {role}
    return {"counts": counts, "issues": issues}


def _llm_round(script: Path, tex_path: Path, roles: str, out_round: Path, round_no: int) -> dict:
    j = out_round / "adversarial_review.json"
    if j.is_file():
        try:
            if j.stat().st_mtime >= tex_path.stat().st_mtime:  # 论文修订后旧轮次作废
                cached = _parse_round_json(j, round_no)
                if cached is not None:  # 断点续跑：被中断的多轮收敛可复用已完成轮次
                    return {**cached, "exit_code": 0, "stderr_tail": "resumed from cached round"}
        except OSError:
            pass
    cmd = [sys.executable, str(script), "--input", str(tex_path),
           "--roles", roles, "--out", str(out_round)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800,
                              encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return {"counts": {"Critical": 0, "Major": 0, "Minor": 0}, "issues": {}, "exit_code": -1,
                "stderr_tail": "timeout (>30min)"}
    fresh = _parse_round_json(j, round_no) if j.is_file() else None
    if fresh is None:
        return {"counts": {"Critical": 0, "Major": 0, "Minor": 0}, "issues": {}, "exit_code": proc.returncode,
                "stderr_tail": (proc.stderr or "")[-300:]}
    return {**fresh, "exit_code": proc.returncode, "stderr_tail": (proc.stderr or "")[-300:]}


def stage_r6(cfg: dict, out: Path, skip_llm: bool, converge: int) -> tuple[dict, str, str]:
    llm = {**DEFAULT_LLM, **(cfg.get("llm") or {})}
    tex_path = Path(cfg["_tex_path"])
    report = {"meta": {"stage": "R6", "timestamp": now(), "rpc": llm["rpc"], "rounds": converge}}
    if skip_llm or not llm.get("enabled"):
        # 诊断日志（Critical #1）：曾出现 enabled=true 却命中此分支的未解释案例，
        # 打印实际判定值便于下次定位
        print(f"  [R6] DISABLED: skip_llm={skip_llm} llm.enabled={llm.get('enabled')} "
              f"cfg.llm={cfg.get('llm')}", flush=True)
        report["summary"] = {"verdict": None, "reason": "llm disabled"}
        dump_json(report, out / "r6_llm.json")
        return report, "SKIP", "LLM 审查未启用（--skip-llm 或 llm.enabled=false）"

    ok, detail = rpc_health(llm["rpc"])
    report["rpc_health"] = {"ok": ok, "detail": detail}
    if not ok:
        report["summary"] = {"verdict": None, "reason": f"RPC down: {detail}"}
        dump_json(report, out / "r6_llm.json")
        return report, "SKIP", f"RPC 不可达（{detail}）→ R6 跳过；证据层结论不受影响"

    llm_out = out / "llm"
    llm_out.mkdir(parents=True, exist_ok=True)
    script = Path(llm["script"])
    if not script.is_file():
        report["summary"] = {"verdict": None, "reason": f"script not found: {script}"}
        dump_json(report, out / "r6_llm.json")
        return report, "SKIP", f"adversarial_review.py 不存在：{script}"

    rounds = max(1, int(converge or 1))
    per_round, rounds_issues = [], []
    for k in range(1, rounds + 1):
        print(f"  [R6] round {k}/{rounds} 开始（每轮最长 30min，已完成轮次断点续跑）", flush=True)
        r = _llm_round(script, tex_path, llm.get("roles", "all"), llm_out / f"round_{k}", k)
        if r.get("stderr_tail") == "resumed from cached round":
            print(f"  [R6] round {k}/{rounds}: 命中缓存，跳过重跑", flush=True)
        per_round.append(r["counts"])
        rounds_issues.append(r["issues"])
        print(f"  [R6] round {k}/{rounds}: Critical={r['counts']['Critical']} "
              f"Major={r['counts']['Major']} Minor={r['counts']['Minor']}", flush=True)

    merged = _fuzzy_merge(rounds_issues)

    stable_min = 2 if rounds >= 2 else 1
    stable = {k: v for k, v in merged.items() if len(v["rounds"]) >= stable_min}
    unstable = {k: v for k, v in merged.items() if len(v["rounds"]) < stable_min}
    counts = {"Critical": sum(1 for v in stable.values() if v["sev"] == "Critical"),
              "Major": sum(1 for v in stable.values() if v["sev"] == "Major"),
              "Minor": sum(1 for v in stable.values() if v["sev"] == "Minor")}
    unstable_counts = {"Critical": sum(1 for v in unstable.values() if v["sev"] == "Critical"),
                      "Major": sum(1 for v in unstable.values() if v["sev"] == "Major")}

    report["rounds"] = per_round
    # 互盲编排（E331）：各轮产物落盘即冻结；consensus 须 ≥2 独立角色同指；
    # dissent（devil 席）单列永不淹没；合成只读轮次产物，不回灌个体。
    consensus = sorted(
        ({"text": v["text"], "sev": v["sev"], "roles": sorted(v.get("roles") or set()),
          "rounds": sorted(v["rounds"])}
         for v in stable.values() if len(v.get("roles") or set()) >= 2),
        key=lambda v: v["text"])
    dissent = sorted(
        ({"text": v["text"], "sev": v["sev"], "roles": sorted(v.get("roles") or set()),
          "rounds": sorted(v["rounds"])}
         for v in merged.values() if "devil" in (v.get("roles") or set())),
        key=lambda v: v["text"])
    report["summary"] = {
        "verdict": "MAJOR" if (counts["Critical"] or counts["Major"]) else "PASS",
        "counts": counts,
        "unstable_counts": unstable_counts,
        "stability_rule": f"≥{stable_min} 轮出现才计入门禁" if rounds >= 2 else "单轮",
        "freeze": {"tex_sha256": sha256_file(tex_path), "roles": llm.get("roles", "all"),
                   "note": "各轮 round_k 落盘即冻结；合成只读不回灌"},
        "consensus_n": len(consensus),
        "dissent_n": len(dissent),
    }
    for v in merged.values():
        v["rounds"] = sorted(v["rounds"])
        v["roles"] = sorted(v.get("roles") or set())
    dump_json({**report,
               "stable_issues": sorted((v for v in stable.values()), key=lambda v: v["text"]),
               "unstable_issues": sorted((v for v in unstable.values()), key=lambda v: v["text"]),
               "consensus_issues": consensus,
               "dissent_issues": dissent},
              out / "r6_llm.json")

    gate = "WARN" if (counts["Critical"] or counts["Major"]) else "PASS"
    metric = (f"文本层：Critical {counts['Critical']} / Major {counts['Major']} / Minor {counts['Minor']}"
              f"（{rounds} 轮，RPC {detail}）")
    if rounds >= 2:
        metric += f"；轮间不稳定（噪声候选，不计门禁）：Critical {unstable_counts['Critical']} / Major {unstable_counts['Major']}"
    return report, gate, metric


# ---------------------------------------------------------------- R6b PRISM 四维自评

def stage_r6b(cfg: dict, out: Path, skip_llm: bool) -> tuple[dict, str, str]:
    if prism_review is None:
        return ({"meta": {"stage": "R6b", "timestamp": now()}, "summary": {"verdict": None}},
                "SKIP", "prism_review 模块不可用")
    llm = {**DEFAULT_LLM, **(cfg.get("llm") or {})}
    if skip_llm or not llm.get("enabled"):
        return ({"meta": {"stage": "R6b", "timestamp": now()}, "summary": {"verdict": None, "reason": "llm disabled"}},
                "SKIP", "PRISM 未启用（--skip-llm 或 llm.enabled=false）")
    if not cfg.get("prism", True):
        return ({"meta": {"stage": "R6b", "timestamp": now()}, "summary": {"verdict": None, "reason": "disabled"}},
                "SKIP", "config 设 prism=false 已关闭 PRISM 四维自评")

    tex_path = Path(cfg["_tex_path"])
    rep = prism_review.run_prism(tex_path, rpc_url=llm["rpc"])
    prism_review.write_md(rep, out / "prism_review.md")
    dump_json(rep, out / "prism_review.json")
    s = rep["summary"]
    if s["verdict"] == "SKIP":
        return rep, "SKIP", f"PRISM 跳过：{s.get('detail', '')}"
    gate = gate_of(s["verdict"])
    metric = (f"{s['verdict']}：四维 {s['scores']}（min={s['overall']}，短板 {s['weakest']}）"
              f"——{s.get('detail', '')}")
    return rep, gate, metric


# ---------------------------------------------------------------- R6c 审稿人-作者辩论

def stage_r6c(cfg: dict, out: Path, skip_llm: bool) -> tuple[dict, str, str]:
    if debate is None:
        return ({"meta": {"stage": "R6c", "timestamp": now()}, "summary": {"verdict": None}},
                "SKIP", "debate 模块不可用")
    llm = {**DEFAULT_LLM, **(cfg.get("llm") or {})}
    if skip_llm or not llm.get("enabled"):
        return ({"meta": {"stage": "R6c", "timestamp": now()}, "summary": {"verdict": None, "reason": "llm disabled"}},
                "SKIP", "辩论未启用（--skip-llm 或 llm.enabled=false）")
    if not cfg.get("debate", True):
        return ({"meta": {"stage": "R6c", "timestamp": now()}, "summary": {"verdict": None, "reason": "disabled"}},
                "SKIP", "config 设 debate=false 已关闭辩论")

    # 问题源优先级：R6 稳定清单 > PRISM 弱点 > 无可辩论
    src = None
    for cand in (out / "r6_llm.json", out / "prism_review.json"):
        if cand.is_file():
            src = cand
            break
    if src is None:
        return ({"meta": {"stage": "R6c", "timestamp": now()}, "summary": {"verdict": None, "reason": "no issues"}},
                "SKIP", "无可辩论问题清单（R6/PRISM 均未产出）")
    issues = debate.load_issues(src)
    if not issues:
        # 治理决议 2026-09-06（用户批准）：问题清单为空 = 文本层无异议，记 PASS（vacuous pass）；
        # 此前记 SKIP 会按 6 分封顶，致零问题论文反低于修好重审论文，属计分逻辑 bug。
        return ({"meta": {"stage": "R6c", "timestamp": now()}, "summary": {"verdict": "PASS", "reason": "no issues"}},
                "PASS", f"无可辩论问题（{src.name} 清单为空）= 文本层无异议")

    tex_path = Path(cfg["_tex_path"])
    rep = debate.run_debate(tex_path, src, rpc_url=llm["rpc"])
    debate.write_md(rep, out / "debate.md")
    dump_json(rep, out / "debate.json")
    s = rep["summary"]
    if s["verdict"] == "SKIP":
        return rep, "SKIP", f"辩论跳过：{s.get('detail', '')}"
    gate = gate_of(s["verdict"])
    tr = s.get("truncation") or {}
    metric = (f"{s['verdict']}：辩论后维持 Critical {s['counts_sustained']['Critical']} / "
              f"Major {s['counts_sustained']['Major']}（撤回 {s['n_withdrawn']}，部分成立 {s['n_partial']}）")
    if tr.get("n_truncated"):
        metric += (f"；注：原始 {tr['n_total']} 条中仅严重度前 {tr['n_debated']} 条进入辩论"
                   f"（MAX_ISSUES={tr.get('max_issues')}，截断 {tr['n_truncated']} 条未辩论）")
    return rep, gate, metric


# ---------------------------------------------------------------- R7 综合报告

def suggested_score(results: dict) -> tuple[int, dict, str]:
    """R7 半自动评分（min 维度纪律，不平均）：
    结构(R1/R1b/R1c/R1d) / 证据(R2/R2b/R2c/R2d/R3/R4/R5) / 文本(R6/R6b/R6c) 各维度取最差阶段门禁映射分，
    总分 = min(各维度)。证据层 FAIL → 该维度 4 分 → 总分 cap 4。"""
    dims = {"structure": ["R1", "R1b", "R1c", "R1d"],
            "evidence": ["R2", "R2b", "R2c", "R2d", "R3", "R4", "R5"],
            "text": ["R6", "R6b", "R6c"]}
    scores, notes = {}, []
    for dim, stages in dims.items():
        gates = [results[s]["gate"] for s in stages if s in results]
        if not gates:
            continue
        worst = max(gates, key=lambda g: GATE_ORDER[g])
        scores[dim] = GATE_SCORE[worst]
        if worst == "FAIL":
            notes.append(f"{dim} 维度 FAIL（{', '.join(s for s in stages if s in results and results[s]['gate'] == 'FAIL')}）→ cap 4")
        elif worst == "WARN":
            notes.append(f"{dim} 维度 WARN")
    if not scores:
        return 0, {}, "无可用维度"
    return min(scores.values()), scores, "；".join(notes) or "各维度无 FAIL/WARN"


# ---------------------------------------------------------------- 校准后评分（v2.2，TMLR 官方数据集）

CAL_CEILING = 8.0  # TMLR h_decision 映射上限（Accept as is = 8）：校准不外推超过此值


def calibrated_scoring(score: int, dim_scores: dict, results: dict, cal_dir: Path) -> dict | None:
    """把 TMLR 官方审稿数据集校准结果（v2.2，n=6 已接收论文）应用到本次评分。

    校准实测（cal_results/calibration_report.json）：
    - bias = human − suggested = +1.67（全 WARN/SKIP 剖面测得的 accept 侧保守偏移）
    - PRISM R 是唯一显著排序信号（vs yes_rate ρ=0.89，p=0.018）；P/I 不显著
    - 问题数 null 结果：stable/sustained 的 C/M 计数与 yes_rate ρ≈0（-0.03~+0.09）——
      accept 侧问题密度是噪声，不携带排序信号
    - 门禁-决策一致 6/6（WARN↔accept）；样本中无 FAIL 论文

    应用规则：
    1. 无 FAIL 维度（校准样本同剖面）：calibrated = min(8, suggested + bias)
    2. 有 FAIL 维度：偏移不应用——校准样本无 FAIL 区间数据，外推无依据；cap 4 纪律不变
    3. 文本维评分不因问题密度进一步调幅（null 结果），stable 问题清单维持 WARN 语义
    """
    rep_p = cal_dir / "calibration_report.json"
    cal_p = cal_dir / "calibrations.json"
    if not rep_p.is_file() or not cal_p.is_file():
        return None
    try:
        rep = json.loads(rep_p.read_text(encoding="utf-8"))
        cal = json.loads(cal_p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    metrics = rep.get("metrics") or {}
    bias = metrics.get("bias")
    n = metrics.get("pairs")
    if not isinstance(bias, (int, float)) or not isinstance(n, int):
        return None
    has_fail = any(v.get("gate") == "FAIL" for v in results.values() if isinstance(v, dict))
    if has_fail:
        calibrated = float(score)
        rule = ("证据层 FAIL：校准样本（n=6 全 accept，无 FAIL 论文）不含 FAIL 区间——"
                "偏移不外推，cap 4 纪律不变")
    else:
        calibrated = round(min(CAL_CEILING, score + bias), 1)
        rule = f"无 FAIL 剖面：min(8, {score} + {bias}) = {calibrated}（accept 侧保守偏移修正，上限 8 = Accept-as-is 映射）"
    r6c = (results.get("R6", {}).get("report", {}).get("summary", {}) or {}).get("counts") or {}
    rank = rep.get("rank_consistency") or {}
    issue_rank = rank.get("issue_counts_vs_yesrate") or {}
    prism_r = (rank.get("prism_dims_vs_yesrate") or {}).get("R") or {}
    return {
        "source": str(cal_dir), "n": n, "bias": bias,
        "suggested": score, "calibrated_score": calibrated,
        "offset_applied": not has_fail,
        "profile": "fail-present" if has_fail else "warn-skip-only",
        "rule": rule,
        "issue_counts_this_run": {"stable_C": r6c.get("Critical"), "stable_M": r6c.get("Major")},
        "rank_signals": {
            "prism_R_vs_yesrate": {"spearman": prism_r.get("spearman"), "p": prism_r.get("p"),
                                   "note": "唯一显著维度（严谨性 ↔ claims 投票）"},
            "issue_counts_vs_yesrate": {k: v.get("spearman") for k, v in issue_rank.items()},
            "issue_counts_null": "问题密度与评审投票 ρ≈0（n=6）：文本维不因问题数调幅",
        },
        "disclosure": [
            "accept 侧单侧校准：TMLR 拒稿不公开，FAIL↔reject 方向无标定",
            f"n={n} 小样本：偏移量本身有不确定性，calibrated_score 是排序参考而非绝对分",
            "决议两级（7/8）映射，绝对分校准天然粗糙",
            "claims 投票针对投稿版，与终版 PDF 有版本差",
        ],
    }


def diff_runs(old_dir: Path, cur: dict) -> list[dict]:
    def load(name: str) -> dict | None:
        p = old_dir / name
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            return None

    def metric(name: str, old, new, better: str):
        if old is None or new is None:
            return None
        if old == new:
            trend = "same"
        elif (new < old) if better == "lower" else (new > old):
            trend = "improved"
        else:
            trend = "regressed"
        return {"name": name, "old": old, "new": new, "trend": trend}

    rows = []
    oa = load("audit_report.json")
    if oa and cur.get("R2"):
        s, c = oa["summary"], cur["R2"]["summary"]
        rows.append(metric("R2 引用缺失", s["refs_missing"], c["refs_missing"], "lower"))
        rows.append(metric("R2 路径泄漏", s["leaks"], c["leaks"], "lower"))
        rows.append(metric("R2 tex desync", int(bool(s["tex_desync"])), int(bool(c["tex_desync"])), "lower"))
    ov = load("verify_manifest.json")
    if ov and "summary" in (ov or {}) and cur.get("R2b"):
        s, c = ov["summary"], cur["R2b"]["summary"]
        rows.append(metric("R2b 哈希不符", s["hash_mismatch"], c["hash_mismatch"], "lower"))
        rows.append(metric("R2b 缺失", s["missing"], c["missing"], "lower"))
    on = load("number_reconcile.json")
    if on and cur.get("R3"):
        s, c = on["summary"], cur["R3"]["summary"]
        rows.append(metric("R3 裁决 critical", s.get("critical_adjudicated", 0), c.get("critical_adjudicated", 0), "lower"))
        rows.append(metric("R3 待复核", s.get("pending_review", 0), c.get("pending_review", 0), "lower"))
    os_ = load("stats_recompute.json")
    if os_ and cur.get("R4") and "summary" in cur["R4"]:
        s, c = os_["summary"], cur["R4"]["summary"]
        rows.append(metric("R4 统计 MISMATCH", s.get("mismatch", 0), c.get("mismatch", 0), "lower"))
        rows.append(metric("R4 NOT_IN_PAPER", s.get("not_in_paper", 0), c.get("not_in_paper", 0), "lower"))
    oh = load("honesty_scan.json")
    if oh and cur.get("R5"):
        s, c = oh["summary"], cur["R5"]["summary"]
        rows.append(metric("R5 可疑未披露", s["suspicious"], c["suspicious"], "lower"))
    oc = load("citation_check.json")
    if oc and cur.get("R1b") and "summary" in cur["R1b"] and "ghost_citations" in cur["R1b"]["summary"]:
        s, c = oc["summary"], cur["R1b"]["summary"]
        rows.append(metric("R1b 幽灵引用", s.get("ghost_citations", 0), c.get("ghost_citations", 0), "lower"))
        rows.append(metric("R1b ID 不存在", s.get("not_found", 0), c.get("not_found", 0), "lower"))
    of = load("figure_check.json")
    if of and cur.get("R2c") and "summary" in cur["R2c"]:
        s, c = of["summary"], cur["R2c"]["summary"]
        rows.append(metric("R2c 缺失图", s.get("missing", 0), c.get("missing", 0), "lower"))
        rows.append(metric("R2c 图注无支撑", s.get("unsupported", 0), c.get("unsupported", 0), "lower"))
    onv = load("novelty_check.json")
    if onv and cur.get("R1c") and "summary" in cur["R1c"]:
        s, c = onv["summary"], cur["R1c"]["summary"]
        rows.append(metric("R1c 未引用近重复", s.get("related_uncited", 0), c.get("related_uncited", 0), "lower"))
    oform = load("formula_check.json")
    if oform and cur.get("R1d") and "summary" in cur["R1d"]:
        s, c = oform["summary"], cur["R1d"]["summary"]
        rows.append(metric("R1d 算术不符", s.get("arith_mismatch", 0), c.get("arith_mismatch", 0), "lower"))
        rows.append(metric("R1d 悬空公式引用", s.get("dangling_refs", 0), c.get("dangling_refs", 0), "lower"))
    otab = load("table_check.json")
    if otab and cur.get("R2d") and "summary" in cur["R2d"]:
        s, c = otab["summary"], cur["R2d"]["summary"]
        rows.append(metric("R2d 表格无支撑", s.get("unsupported", 0), c.get("unsupported", 0), "lower"))
        rows.append(metric("R2d \\input 缺失", s.get("missing_inputs", 0), c.get("missing_inputs", 0), "lower"))
    op = load("prism_review.json")
    if op and cur.get("R6b") and "summary" in cur["R6b"]:
        s, c = op["summary"], cur["R6b"]["summary"]
        if isinstance(s.get("overall"), int) and isinstance(c.get("overall"), int):
            rows.append(metric("R6b PRISM min 分", s["overall"], c["overall"], "higher"))
    od = load("debate.json")
    if od and cur.get("R6c") and "summary" in cur["R6c"]:
        s, c = od["summary"], cur["R6c"]["summary"]
        rows.append(metric("R6c 辩论维持 Major", (s.get("counts_sustained") or {}).get("Major", 0),
                           (c.get("counts_sustained") or {}).get("Major", 0), "lower"))
        rows.append(metric("R6c 辩论撤回", s.get("n_withdrawn", 0), c.get("n_withdrawn", 0), "higher"))
    return [r for r in rows if r]


def _merge_prior_stages(out: Path, results: dict) -> dict:
    """增量运行（--stages 子集）时合并上一轮 gates.json：未重跑的阶段保留旧门禁，
    报告从磁盘回载（verdict 进阶段表）。否则子集运行会把 overall 虚假抬成 PASS——
    例：全量跑 R2=FAIL 后仅重跑 R6c,R7，覆盖式落盘会丢掉 R2 的 FAIL。"""
    gp = out / "gates.json"
    if not gp.is_file():
        return results
    try:
        old = json.loads(gp.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return results
    for st, ent in (old.get("stages") or {}).items():
        if st in results or not isinstance(ent, dict) or "gate" not in ent:
            continue
        rep: dict = {}
        rp = out / STAGE_REPORTS.get(st, "")
        if rp and rp.is_file():
            try:
                rep = json.loads(rp.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                rep = {}
        results[st] = {"report": rep, "gate": ent["gate"],
                       "metric": (ent.get("metric", "") + "（上一轮，未重跑）").strip("；")}
    return results


def stage_r7(cfg: dict, out: Path, results: dict, diff_old: Path | None) -> tuple[dict, str, str]:
    name = cfg.get("name", "paper")
    results = _merge_prior_stages(out, results)
    overall, ran = "PASS", False
    for r in results.values():
        if r["gate"] == "SKIP":
            continue
        ran = True
        if GATE_ORDER[r["gate"]] > GATE_ORDER[overall]:
            overall = r["gate"]
    if not ran:
        overall = "SKIP"

    score, dim_scores, score_notes = suggested_score(results)
    gates = {"name": name, "timestamp": now(), "overall": overall,
             "stages": {k: {"gate": v["gate"], "metric": v["metric"]} for k, v in results.items()},
             "suggested_score": score,
             "score_dimensions": dim_scores,
             "score_note": (f"{score_notes}；min 维度纪律（不平均）。"
                            "人工阶段未完成（R3 裁决收敛 / R5 定性 / 终审）前为临时值")}
    calibration = None
    cal_dir = cfg.get("calibration")
    if cal_dir:
        calibration = calibrated_scoring(score, dim_scores, results, Path(cal_dir))
        if calibration:
            gates["calibrated_score"] = calibration["calibrated_score"]
            gates["calibration"] = calibration
        else:
            gates["calibration"] = {"source": str(cal_dir),
                                    "error": "calibration_report.json / calibrations.json 缺失或不可解析"}
    prism_s = (results.get("R6b", {}).get("report", {}).get("summary", {}) or {}).get("scores")
    if prism_s:
        gates["prism_scores"] = prism_s
    dump_json(gates, out / "gates.json")

    lines = [
        f"# 审稿工作流运行摘要：{name}",
        "",
        f"- 时间：{now()}",
        f"- 论文：`{cfg.get('tex') or cfg.get('pdf')}`",
        f"- 投稿包：`{cfg.get('zip')}`",
        f"- 证据目录：{', '.join('`'+p+'`' for p in cfg.get('evidence_dirs', []))}",
        "",
        f"## 总体门禁：**{overall}** | 建议评分：**{score}/10**（min 维度：{dim_scores}）",
        "",
    ]
    if calibration:
        cs = calibration["calibrated_score"]
        lines += [
            f"### 校准后评分：**{cs}/10**（{calibration['rule']}）",
            "",
            f"- 排序信号：PRISM R vs yes_rate ρ={calibration['rank_signals']['prism_R_vs_yesrate']['spearman']}"
            f"（唯一显著维度）；问题数 null（ρ≈0）→ 本次 {calibration['issue_counts_this_run'].get('stable_C') or 0} 条 "
            f"stable Critical 不进一步调幅文本维",
            f"- 边界：{'；'.join(calibration['disclosure'])}",
            "",
        ]
    elif cal_dir:
        lines += ["### 校准后评分：不可用（校准目录缺产物）", ""]
    if overall == "FAIL":
        lines.append("证据层存在 FAIL → 按评分纪律 cap 4；先修 FAIL 项再进入文本层评审。")
    else:
        lines.append("证据层无 FAIL；R3 裁决收敛与 R5 人工定性完成后，终审人工给出最终分（suggested_score 是临时下界参考）。")
    lines += [
        "",
        "## 阶段表",
        "",
        "| 阶段 | 结论 | 门禁 | 关键指标 |",
        "|---|---|---|---|",
    ]
    for st in ALL_STAGES:
        if st not in results:
            continue
        r = results[st]
        verdict = r["report"].get("summary", {}).get("verdict") or "-"
        lines.append(f"| {st} | {verdict} | **{r['gate']}** | {r['metric']} |")

    if diff_old:
        rows = diff_runs(Path(diff_old), {k: v["report"] for k, v in results.items()})
        lines += ["", f"## 与上一轮对比（{diff_old}）", "", "| 指标 | 旧 | 新 | 趋势 |", "|---|---|---|---|"]
        if rows:
            mark = {"improved": "✅ 改善", "regressed": "❌ 恶化", "same": "＝"}
            lines += [f"| {r['name']} | {r['old']} | {r['new']} | {mark[r['trend']]} |" for r in rows]
        else:
            lines.append("| （无可对比数据） | | | |")

    pending = results.get("R3", {}).get("report", {}).get("summary", {}).get("pending_review", 0)
    adj_path = cfg.get("adjudications")
    next_steps = ["**R4 统计定性（已自动化）**：MISMATCH/NOT_IN_PAPER 由口径换算机械层 + LLM 对抗裁决自动定性（stats_adjudications.md）；仅 llm_failed 条目需人工补判；检验选择配对、退化情形披露、功效、多重比较清单见 REVIEW_SOP.md R4"]
    if not cfg.get("citation_online"):
        next_steps.append("**R1b 联网核验（可选）**：config 设 citation_online=true 复跑，核验 arXiv/DOI 真实性")
    if not cfg.get("novelty_online"):
        next_steps.append("**R1c 新颖性对照（可选）**：config 设 novelty_online=true 复跑，arXiv 检索先行工作并比对断言")
    fig_pending = (results.get("R2c", {}).get("report", {}).get("summary", {}) or {}).get("unsupported", 0)
    if fig_pending:
        next_steps.append(f"**R2c 图注数字定性（人工）**：figure_check.md 中 {fig_pending} 个图注小数在图文本/证据/正文中均无支撑，逐条定性（stale figure / 口径不同 / 误报）")
    if results.get("R5", {}).get("report", {}).get("suspicious"):
        next_steps.append("**R5 诚实性定性（人工）**：honesty_scan.md 中 suspicious 逐条判定——论文表述是否如实披露（Critical）")
    if pending:
        next_steps.append(f"**R3 裁决收敛**：{pending} 个待复核数字 → 在 `{adj_path}` 填 verdict(noise|supported|critical) 后重跑")
    if results.get("R6", {}).get("report", {}).get("summary", {}).get("counts"):
        next_steps.append("**R6 收敛**：LLM 意见修复后重跑至一轮无新 Critical/Major；--converge 3 可降轮间噪声")
    prism = (results.get("R6b", {}).get("report", {}).get("summary", {}) or {})
    if prism.get("overall"):
        next_steps.append(f"**R6b PRISM 复盘**：最弱维度 {prism.get('weakest')} = {prism['overall']} 分（P/R/I/S = {prism.get('scores')}），四维证据句见 prism_review.md")
    if results.get("R6c", {}).get("report", {}).get("summary", {}).get("sustained_ids"):
        r6c_tr = (results.get("R6c", {}).get("report", {}).get("summary", {}) or {}).get("truncation") or {}
        tr_note = (f"；另有 {r6c_tr['n_truncated']} 条未进辩论（截断上限 {r6c_tr.get('max_issues')}，见 debate.md 注记）"
                   if r6c_tr.get("n_truncated") else "")
        next_steps.append(f"**R6c 辩论结果**：sustained 条目是作者 rebuttal 后仍成立的问题（修复优先级最高）；withdrawn 为 LLM 单轮假阳性{tr_note}")
    lines += ["", "## 下一步（人工阶段）", ""]
    lines += [f"{i}. {s}" for i, s in enumerate(next_steps, 1)]
    lines += [
        "",
        "## 复跑命令",
        "",
        "```powershell",
        f'python "{SCRIPTS_DIR / "run_review.py"}" --config "{Path(cfg.get("_config_path", "config.json"))}"',
        "```",
    ]
    (out / "run_summary.md").write_text("\n".join(lines), encoding="utf-8")

    metric = f"overall={overall}，score={score}（{', '.join(f'{k}={v}' for k, v in dim_scores.items())}）；" + "，".join(f"{k}={v['gate']}" for k, v in results.items())
    return gates, overall, metric


# ---------------------------------------------------------------- 主流程

def run_one(cfg: dict, stages: list[str], skip_llm: bool, diff_old: Path | None,
             converge: int | None = None) -> tuple[str, int]:
    out = Path(cfg.get("out") or Path("runs") / cfg.get("name", "review"))
    out.mkdir(parents=True, exist_ok=True)
    cfg["_out"] = str(out)
    results: dict[str, dict] = {}

    tex_path, pdf_mode, src_note = resolve_source(cfg, out)
    cfg["_tex_path"] = str(tex_path) if tex_path else ""
    if tex_path is None:
        print(f"[R0] 输入解析失败：{src_note}")
        results["R0"] = dict(zip(("report", "gate", "metric"), stage_r0(cfg, src_note)))
        dump_json(results["R0"]["report"], out / "r0_registration.json")
        print(f"[R0] gate={results['R0']['gate']} {results['R0']['metric']}")
        _, overall, _ = stage_r7(cfg, out, results, diff_old)
        return overall, 1
    if pdf_mode:
        print(f"[R0] {src_note}")

    if "R0" in stages:
        results["R0"] = dict(zip(("report", "gate", "metric"), stage_r0(cfg, src_note)))
        dump_json(results["R0"]["report"], out / "r0_registration.json")
        print(f"[R0] gate={results['R0']['gate']} {results['R0']['metric']}")
    if "R1" in stages:
        results["R1"] = dict(zip(("report", "gate", "metric"), stage_r1(cfg, tex_path, pdf_mode)))
        dump_json(results["R1"]["report"], out / "r1_static.json")
        print(f"[R1] gate={results['R1']['gate']} {results['R1']['metric']}")
    if "R1b" in stages:
        results["R1b"] = dict(zip(("report", "gate", "metric"), stage_r1b(cfg, tex_path, pdf_mode)))
        dump_json(results["R1b"]["report"], out / "citation_check.json")
        print(f"[R1b] gate={results['R1b']['gate']} {results['R1b']['metric']}")
    if "R1c" in stages:
        results["R1c"] = dict(zip(("report", "gate", "metric"), stage_r1c(cfg, tex_path, pdf_mode)))
        print(f"[R1c] gate={results['R1c']['gate']} {results['R1c']['metric']}")
    if "R1d" in stages:
        results["R1d"] = dict(zip(("report", "gate", "metric"), stage_r1d(cfg, out, tex_path, pdf_mode)))
        print(f"[R1d] gate={results['R1d']['gate']} {results['R1d']['metric']}")
    if "R2" in stages:
        results["R2"] = dict(zip(("report", "gate", "metric"), stage_r2(cfg, out, tex_path, pdf_mode)))
        print(f"[R2] gate={results['R2']['gate']} {results['R2']['metric']}")
    if "R2b" in stages:
        results["R2b"] = dict(zip(("report", "gate", "metric"), stage_r2b(cfg, out, tex_path, pdf_mode)))
        print(f"[R2b] gate={results['R2b']['gate']} {results['R2b']['metric']}")
    if "R2c" in stages:
        results["R2c"] = dict(zip(("report", "gate", "metric"), stage_r2c(cfg, out, tex_path, pdf_mode)))
        print(f"[R2c] gate={results['R2c']['gate']} {results['R2c']['metric']}")
    if "R2d" in stages:
        results["R2d"] = dict(zip(("report", "gate", "metric"), stage_r2d(cfg, out, tex_path, pdf_mode)))
        print(f"[R2d] gate={results['R2d']['gate']} {results['R2d']['metric']}")
    if "R3" in stages:
        results["R3"] = dict(zip(("report", "gate", "metric"), stage_r3(cfg, out, tex_path, skip_llm)))
        print(f"[R3] gate={results['R3']['gate']} {results['R3']['metric']}")
    if "R4" in stages:
        results["R4"] = dict(zip(("report", "gate", "metric"), stage_r4(cfg, out, tex_path, skip_llm)))
        print(f"[R4] gate={results['R4']['gate']} {results['R4']['metric']}")
    if "R5" in stages:
        results["R5"] = dict(zip(("report", "gate", "metric"), stage_r5(cfg, out, tex_path)))
        print(f"[R5] gate={results['R5']['gate']} {results['R5']['metric']}")
    if "R6" in stages:
        rounds = converge if converge is not None else int(cfg.get("converge", 1) or 1)
        results["R6"] = dict(zip(("report", "gate", "metric"), stage_r6(cfg, out, skip_llm, rounds)))
        print(f"[R6] gate={results['R6']['gate']} {results['R6']['metric']}")
    if "R6b" in stages:
        results["R6b"] = dict(zip(("report", "gate", "metric"), stage_r6b(cfg, out, skip_llm)))
        print(f"[R6b] gate={results['R6b']['gate']} {results['R6b']['metric']}")
    if "R6c" in stages:
        results["R6c"] = dict(zip(("report", "gate", "metric"), stage_r6c(cfg, out, skip_llm)))
        print(f"[R6c] gate={results['R6c']['gate']} {results['R6c']['metric']}")

    _, overall, _ = stage_r7(cfg, out, results, diff_old)
    print(f"[R7] overall={overall} -> {out / 'run_summary.md'}")
    return overall, (1 if overall == "FAIL" else 0)


def load_config(path: Path) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    cfg["_config_path"] = str(path)
    return cfg


def looks_like_config(p: Path) -> bool:
    """目录批处理时排除裁决文件等非 config JSON：必须含 name 且有 tex/pdf/zip/evidence_dirs 任一。"""
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    if not isinstance(data, dict) or "name" not in data:
        return False
    return any(k in data for k in ("tex", "pdf", "zip", "evidence_dirs", "out"))


def run_batch(batch_path: Path, skip_llm: bool) -> int:
    items: list[dict] = []
    if batch_path.is_dir():
        items = [load_config(p) for p in sorted(batch_path.glob("*.json"))
                 if not p.name.startswith("_") and looks_like_config(p)]
    else:
        data = json.loads(batch_path.read_text(encoding="utf-8"))
        raw = data.get("configs", data) if isinstance(data, dict) else data
        for x in raw:
            items.append(load_config(Path(x)) if isinstance(x, str) else {**x, "_config_path": str(batch_path)})
    if not items:
        print(f"[batch] {batch_path} 下未发现有效 config（需含 name + tex/pdf/zip/evidence_dirs 任一键）")
        return 1

    rows = []
    worst_rc = 0
    for cfg in items:
        try:
            overall, rc = run_one(cfg, ALL_STAGES, skip_llm, None)
        except Exception as e:  # noqa: BLE001
            overall, rc = f"ERROR: {e}", 2
        rows.append({"name": cfg.get("name", "?"), "overall": overall, "rc": rc,
                     "out": str(cfg.get("out") or Path("runs") / cfg.get("name", "review"))})
        worst_rc = max(worst_rc, rc)

    out_md = (batch_path if batch_path.is_dir() else batch_path.parent) / "batch_summary.md"
    lines = [
        "# 批处理审稿摘要",
        "",
        f"- 时间：{now()}；配置 {len(rows)} 份",
        "",
        "| 论文 | 总体门禁 | 输出 |", "|---|---|---|",
    ]
    lines += [f"| {r['name']} | **{r['overall']}** | `{r['out']}` |" for r in rows]
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[batch] {len(rows)} papers -> {out_md}")
    return worst_rc


def write_template(path: Path) -> int:
    template = {
        "name": "paper_v1",
        "tex": "F:/path/to/paper/main.tex",
        "pdf": None,
        "zip": "F:/path/to/submission.zip",
        "evidence_dirs": ["F:/path/to/results"],
        "manifest": None,
        "adjudications": None,
        "bib": None,
        "citation_online": False,
        "novelty_online": False,
        "prism": True,
        "debate": True,
        "r4_llm": True,
        "converge": 1,
        "llm": DEFAULT_LLM,
        "out": "F:/path/to/runs/paper_v1",
    }
    path.write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"template written -> {path}")
    return 0


# ---------------------------------------------------------------- selftest

def selftest() -> int:
    import tempfile
    import zipfile

    tmp = Path(tempfile.mkdtemp())

    # -- 单元：跨轮模糊合并（实测 bug 回归：措辞漂移曾致 stable=0） -----------------
    r1 = {"k1": {"sev": "Critical", "text": "L2 McNemar power 0.0000 at n_d=4，统计功效不足",
                 "rounds": {1}},
          "k2": {"sev": "Major", "text": "seed 管理缺失：未报告 RNG seed，byte-for-byte reproducibility 不可信",
                 "rounds": {1}}}
    r2 = {"k3": {"sev": "Major", "text": "L2 的 McNemar 检验在 N=4 下 power=0.0000，CI 退化",
                 "rounds": {2}},
          "k4": {"sev": "Critical", "text": "未报告 RNG seed，byte-for-byte reproducibility 主张不成立",
                 "rounds": {2}}}
    r3 = {"k5": {"sev": "Critical", "text": "McNemar 功效 0.0000 at n_d=4 无法支持无差异结论",
                 "rounds": {3}}}
    m = _fuzzy_merge([r1, r2, r3])
    mc = [v for v in m.values() if "mcnemar" in v["text"].lower()]
    assert len(m) == 2, f"应合并为 2 簇（McNemar×1 / seed×1），实得 {len(m)} 簇"
    assert len(mc) == 1, f"三轮 McNemar 措辞漂移应归并为一簇，实得 {len(mc)}"
    assert sorted(mc[0]["rounds"]) == [1, 2, 3], "簇内 rounds 应为三轮并集"
    assert mc[0]["sev"] == "Critical", "严重度应取更差者（Critical）"
    sd = [v for v in m.values() if "seed" in v["text"].lower() or "rng" in v["text"].lower()]
    assert len(sd) == 1 and sd[0]["sev"] == "Critical" and sorted(sd[0]["rounds"]) == [1, 2], \
        "seed 簇应跨 2 轮且严重度升级为 Critical"
    diff = {"kd": {"sev": "Critical", "text": "License missing for GAIA2 dataset redistribution",
                   "rounds": {1}}}
    m2 = _fuzzy_merge([r1, diff])
    assert len(m2) == 3, "无关问题不应误合并"
    print("  [unit] _fuzzy_merge 措辞漂移合并/严重度升级/无关隔离: OK")

    from_lo, from_hi = 0.4901, 0.9433  # wilson k=8,n=10（容差内与重算一致）

    tex_body = (
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "\\begin{abstract}We test the review pipeline. Mean goal was $0.1418$.\n\\end{abstract}\n"
        "\\section{Introduction} intro \\cite{good2020}\n"
        "\\section{Related Work} related\n"
        "\\section{Method} data in \\texttt{results/stats.json}\n"
        "\\section{Results} value 0.1418 and version v0.32.1.\n"
        "Exact McNemar $p=0.0215$ ($b=1$, $d=9$); Wilson CI $[0.4901, 0.9433]$;\n"
        "Friedman $\\chi^2=6.0$, $p=0.0498$.\n"
        "\\section{Discussion} discussion\n"
        "\\section{Limitations} limitations\n"
        "\\section{Conclusion} conclusion\n"
        "\\end{document}\n"
    )
    paper = tmp / "paper"
    paper.mkdir()
    tex = paper / "main.tex"
    tex.write_text(tex_body, encoding="utf-8")
    bib = paper / "refs.bib"
    bib.write_text(
        "@article{good2020,\n  title={Attention Is All You Need},\n  author={Vaswani},\n"
        "  eprint={1706.03762},\n  year={2017}\n}\n", encoding="utf-8")

    ev = tmp / "evidence" / "results"
    ev.mkdir(parents=True)
    stats = ev / "stats.json"
    stats.write_text(json.dumps({
        "l2": {"mean_goal_A": 0.14175},
        "mcnemar_pair": {"b": 1, "d": 9, "p": 0.0215, "test": "mcnemar"},
        "wilson_gold": {"k": 8, "n": 10, "ci": [from_lo, from_hi], "method": "wilson"},
        "friedman_pair": {"chi2": 6.0, "df": 2, "p": 0.0498, "test": "friedman"},
    }), encoding="utf-8")

    manifest = {"files": [
        {"path": "main.tex", "sha256": sha256_file(tex), "size": tex.stat().st_size},
        {"path": "results/stats.json", "sha256": sha256_file(stats), "size": stats.stat().st_size},
    ]}
    (ev.parent / "ASSET_MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")

    zp = tmp / "submission.zip"
    with zipfile.ZipFile(zp, "w") as zf:
        zf.write(tex, "main.tex")
        zf.write(stats, "results/stats.json")
        zf.write(ev.parent / "ASSET_MANIFEST.json", "ASSET_MANIFEST.json")

    adj = tmp / "adj.json"
    cfg = {
        "name": "selftest_paper",
        "tex": str(tex),
        "zip": str(zp),
        "evidence_dirs": [str(ev.parent)],
        "adjudications": str(adj),
        "llm": {"enabled": False},
        "out": str(tmp / "run1"),
        "_config_path": "selftest",
    }

    overall, rc = run_one(cfg, ALL_STAGES, skip_llm=True, diff_old=None)
    assert (tmp / "run1" / "run_summary.md").exists(), "run_summary.md 未生成"
    assert adj.exists(), "裁决文件未自动创建"
    # 0.32 是版本号片段 → 自动噪音；无 pending、无缺引用 → 证据层应全 PASS
    gates1 = json.loads((tmp / "run1" / "gates.json").read_text(encoding="utf-8"))
    assert overall == "PASS", f"第一轮应为 PASS，实际 {gates1}"
    assert gates1["stages"]["R1b"]["gate"] == "PASS", gates1["stages"]["R1b"]
    assert gates1["stages"]["R4"]["gate"] == "PASS", gates1["stages"]["R4"]
    # v2.0 新阶段：无图 → R2c PASS；无表 → R2d PASS；无算术错误 → R1d PASS；
    # R1c 未开联网 → SKIP；LLM 关 → R6b/R6c SKIP
    assert gates1["stages"]["R2c"]["gate"] == "PASS", gates1["stages"]["R2c"]
    assert gates1["stages"]["R1d"]["gate"] == "PASS", gates1["stages"]["R1d"]
    assert gates1["stages"]["R2d"]["gate"] == "PASS", gates1["stages"]["R2d"]
    assert gates1["stages"]["R1c"]["gate"] == "SKIP", gates1["stages"]["R1c"]
    assert gates1["stages"]["R6b"]["gate"] == "SKIP", gates1["stages"]["R6b"]
    assert gates1["stages"]["R6c"]["gate"] == "SKIP", gates1["stages"]["R6c"]
    # min 维度评分：R6 SKIP → text 维度 6；R1c SKIP（未开联网）→ structure 6 → suggested = 6
    assert gates1["suggested_score"] == 6, gates1.get("suggested_score")
    assert gates1["score_dimensions"] == {"structure": 6, "evidence": 8, "text": 6}, gates1["score_dimensions"]

    # 裁决闭环：无 pending（0.32 被机械噪音豁免），裁决文件存在且可扩展
    nr1 = json.loads((tmp / "run1" / "number_reconcile.json").read_text(encoding="utf-8"))
    assert nr1["summary"]["pending_review"] == 0, nr1["summary"]

    # 第二轮：tex 加入缺失引用 + 未支撑数字 + 幽灵 cite + 缺失图 + 算术错误 + 悬空公式引用 +
    # 表（\input 缺失 → 编译即断；混精度列）；stats.json 造假 → R2/R2c/R2d/R4 FAIL，R1b/R1d/R3 WARN
    tex.write_text(tex_body.replace("\\section{Results}", "\\section{Results}\\texttt{out_p5/x.json} ")
                             .replace("value 0.1418", "value 0.1418 also 7.77")
                             .replace("intro \\cite{good2020}", "intro \\cite{good2020} \\cite{ghost2020}")
                             .replace("Friedman $\\chi^2=6.0$, $p=0.0498$.",
                                      "Friedman $\\chi^2=6.0$, $p=0.0498$. Arith: 2 + 2 = 5; "
                                      "see Eq.~\\ref{eq:none}.")
                             .replace("\\section{Conclusion} conclusion",
                                      "\\begin{figure}\\includegraphics{missing_fig.pdf}"
                                      "\\caption{Missing figure shows 9.61.}\\end{figure}\n"
                                      "\\begin{table}\\caption{Ablation.}\n"
                                      "\\input{tbl_abl_missing.tex}\n"
                                      "\\begin{tabular}{lcc}\\toprule\n"
                                      "Model & Acc & F1 \\\\ \\midrule\n"
                                      "A & 0.88 & 0.9123 \\\\\n"
                                      "B & 0.77 & 0.9 \\\\\n"
                                      "\\bottomrule\\end{tabular}\\end{table}\n"
                                      "\\section{Conclusion} conclusion"),
                   encoding="utf-8")
    stats.write_text(json.dumps({
        "l2": {"mean_goal_A": 0.14175},
        "mcnemar_pair": {"b": 1, "d": 9, "p": 0.0215, "test": "mcnemar"},
        "wilson_gold": {"k": 8, "n": 10, "ci": [from_lo, from_hi], "method": "wilson"},
        "friedman_pair": {"chi2": 6.0, "df": 2, "p": 0.0498, "test": "friedman"},
        "friedman_fake": {"chi2": 4.0, "df": 1, "p": 0.5, "test": "friedman"},  # 造假：真值 0.0455
        "table_gold": {"A_acc": 0.88, "A_f1": 0.9123, "B_acc": 0.77, "B_f1": 0.9},  # 表格数字有证据支撑
    }), encoding="utf-8")
    cfg2 = {**cfg, "out": str(tmp / "run2")}
    overall2, rc2 = run_one(cfg2, ALL_STAGES, skip_llm=True, diff_old=tmp / "run1")
    gates2 = json.loads((tmp / "run2" / "gates.json").read_text(encoding="utf-8"))
    assert gates2["stages"]["R2"]["gate"] == "FAIL", gates2["stages"]
    assert gates2["stages"]["R3"]["gate"] == "WARN", gates2["stages"]
    assert gates2["stages"]["R1b"]["gate"] == "WARN", gates2["stages"]["R1b"]
    assert gates2["stages"]["R4"]["gate"] == "FAIL", gates2["stages"]["R4"]
    # R2c：缺失图文件 = 编译即断 → FAIL；图注 9.61 无支撑进待复核
    assert gates2["stages"]["R2c"]["gate"] == "FAIL", gates2["stages"]["R2c"]
    fc2 = json.loads((tmp / "run2" / "figure_check.json").read_text(encoding="utf-8"))
    assert any(m["path"] == "missing_fig.pdf" for m in fc2["missing_files"]), fc2["missing_files"]
    assert any(p["token"] == "9.61" for p in fc2["caption_pending_review"]), fc2["caption_pending_review"]
    # R1d：算术不符（2+2=5）→ WARN；悬空公式引用 eq:none 一并报出
    assert gates2["stages"]["R1d"]["gate"] == "WARN", gates2["stages"]["R1d"]
    fm2 = json.loads((tmp / "run2" / "formula_check.json").read_text(encoding="utf-8"))
    assert any(m["reported"] == 5 and m["recomputed"] == 4 for m in fm2["mismatches"]), fm2["mismatches"]
    assert any(d["ref"] == "eq:none" for d in fm2["dangling_refs"]), fm2["dangling_refs"]
    # R2d：表内 \input 缺失 → 编译即断 = FAIL；混精度列（0.9123 vs 0.9）标 INFO
    assert gates2["stages"]["R2d"]["gate"] == "FAIL", gates2["stages"]["R2d"]
    tc2 = json.loads((tmp / "run2" / "table_check.json").read_text(encoding="utf-8"))
    assert any(m["path"] == "tbl_abl_missing.tex" for m in tc2["missing_inputs"]), tc2["missing_inputs"]
    assert tc2["summary"]["precision_anomalies"] >= 1, tc2["summary"]
    assert tc2["summary"]["unsupported"] == 0, tc2["summary"]  # table_gold 支撑了全部 cell
    assert overall2 == "FAIL" and rc2 == 1, (overall2, rc2)
    assert gates2["suggested_score"] == 4, gates2.get("suggested_score")  # 证据层 FAIL cap 4
    diff_md = (tmp / "run2" / "run_summary.md").read_text(encoding="utf-8")
    assert "R2 引用缺失" in diff_md and "恶化" in diff_md, diff_md
    # 7.77 未裁决 → pending 写入裁决文件
    adj_state = json.loads(adj.read_text(encoding="utf-8"))
    assert "7.77" in adj_state and adj_state["7.77"]["verdict"] == "pending", adj_state

    # 增量子集运行回归防护：同一 out 目录仅重跑 R5 → 上一轮 R2 的 FAIL 必须从 gates.json
    # 合并回来（覆盖式落盘曾把 overall 虚假抬成 PASS / 评分抬到 8——真实事故修复）
    overall2b, rc2b = run_one({**cfg, "out": str(tmp / "run2")}, ["R5"], skip_llm=True, diff_old=None)
    gates2b = json.loads((tmp / "run2" / "gates.json").read_text(encoding="utf-8"))
    assert overall2b == "FAIL" and rc2b == 1, (overall2b, rc2b)
    assert gates2b["stages"]["R2"]["gate"] == "FAIL", gates2b["stages"]["R2"]
    assert "未重跑" in gates2b["stages"]["R2"]["metric"], gates2b["stages"]["R2"]
    assert gates2b["suggested_score"] == 4, gates2b.get("suggested_score")

    # 第三轮：裁决 7.77 / 9.61 为 noise → R3 收敛为 PASS；引用仍缺 → overall 仍 FAIL
    adj_state["7.77"] = {"verdict": "noise", "note": "selftest"}
    adj_state["9.61"] = {"verdict": "noise", "note": "selftest figure caption"}
    adj.write_text(json.dumps(adj_state, ensure_ascii=False), encoding="utf-8")
    cfg3 = {**cfg, "out": str(tmp / "run3")}
    overall3, _ = run_one(cfg3, ALL_STAGES, skip_llm=True, diff_old=tmp / "run2")
    nr3 = json.loads((tmp / "run3" / "number_reconcile.json").read_text(encoding="utf-8"))
    assert nr3["summary"]["pending_review"] == 0 and nr3["summary"]["verdict"] == "PASS", nr3["summary"]
    assert overall3 == "FAIL"  # R2 缺引用仍在

    # PDF 模式：伪 tex 供 R1/R3/R4；R2/R2b/R1b SKIP
    if pdf_text is not None:
        import pymupdf

        pdf = tmp / "paper.pdf"
        doc = pymupdf.open()
        page = doc.new_page()
        page.insert_text((72, 96), "Abstract. We review a PDF-only paper.")
        page.insert_text((72, 120), "1. Introduction   2. Related Work")
        page.insert_text((72, 144), "3. Method   4. Results   5. Discussion")
        page.insert_text((72, 168), "6. Limitations   7. Conclusion")
        page.insert_text((72, 192), "Mean goal 0.14175 in the paper.")
        doc.save(str(pdf))
        doc.close()
        (tmp / "evidence" / "results" / "stats.json").write_text(
            json.dumps({"l2": {"mean_goal_A": 0.14175}}), encoding="utf-8")
        cfg_pdf = {"name": "selftest_pdf", "tex": None, "pdf": str(pdf),
                   "evidence_dirs": [str(ev.parent)], "llm": {"enabled": False},
                   "out": str(tmp / "run_pdf"), "_config_path": "selftest"}
        run_one(cfg_pdf, ALL_STAGES, skip_llm=True, diff_old=None)
        gp = json.loads((tmp / "run_pdf" / "gates.json").read_text(encoding="utf-8"))
        assert gp["stages"]["R2"]["gate"] == "SKIP" and gp["stages"]["R2b"]["gate"] == "SKIP", gp["stages"]
        assert gp["stages"]["R1b"]["gate"] == "SKIP", gp["stages"]["R1b"]
        assert gp["stages"]["R2c"]["gate"] == "SKIP" and gp["stages"]["R1c"]["gate"] == "SKIP", gp["stages"]
        assert gp["stages"]["R1d"]["gate"] == "SKIP" and gp["stages"]["R2d"]["gate"] == "SKIP", gp["stages"]
        assert gp["stages"]["R1"]["gate"] == "PASS", gp["stages"]["R1"]  # 标题拆行后 8/8
        assert gp["stages"]["R3"]["gate"] == "PASS", gp["stages"]["R3"]
        assert (tmp / "run_pdf" / "extracted_text.txt").exists()

        # PDF 模式 + 无证据目录（TMLR 校准场景）：R3 降级 SKIP 而非 FAIL（支撑率不可判）
        cfg_pdf2 = {**cfg_pdf, "evidence_dirs": [], "out": str(tmp / "run_pdf_noev")}
        overall_pdf2, _ = run_one(cfg_pdf2, ALL_STAGES, skip_llm=True, diff_old=None)
        gp2 = json.loads((tmp / "run_pdf_noev" / "gates.json").read_text(encoding="utf-8"))
        assert gp2["stages"]["R3"]["gate"] == "SKIP", gp2["stages"]["R3"]
        assert "无证据目录" in gp2["stages"]["R3"]["metric"], gp2["stages"]["R3"]
        nr2 = json.loads((tmp / "run_pdf_noev" / "number_reconcile.json").read_text(encoding="utf-8"))
        assert nr2["summary"]["evidence_absent"] is True, nr2["summary"]
        assert gp2["score_dimensions"]["evidence"] != 4, gp2["score_dimensions"]  # 不再 cap 4
        assert gp2["suggested_score"] >= 6, gp2

        # 校准后评分（v2.2）：无 FAIL 剖面 → min(8, suggested+bias)；FAIL 剖面 → 偏移不外推
        cal_dir = tmp / "cal_results"
        cal_dir.mkdir()
        (cal_dir / "calibration_report.json").write_text(json.dumps({
            "metrics": {"pairs": 6, "bias": 1.67},
            "rank_consistency": {
                "prism_dims_vs_yesrate": {"R": {"spearman": 0.89, "p": 0.018}},
                "issue_counts_vs_yesrate": {"stable_C": {"spearman": -0.03}}}}), encoding="utf-8")
        (cal_dir / "calibrations.json").write_text(
            json.dumps([{"paper": "x", "suggested": 6, "human": 8}]), encoding="utf-8")
        # 单元：FAIL 剖面偏移不外推（从 results 门禁判 FAIL，非分数值）
        fail_res = {"R2": {"gate": "FAIL", "metric": "x", "report": {}}}
        cal_fail = calibrated_scoring(4, {"structure": 6, "evidence": 4, "text": 6}, fail_res, cal_dir)
        assert cal_fail["calibrated_score"] == 4.0 and cal_fail["offset_applied"] is False, cal_fail
        assert "FAIL" in cal_fail["rule"], cal_fail
        # 单元：无 FAIL 剖面 → 6+1.67=7.7；上限 8；缺文件 → None
        cal_ok = calibrated_scoring(6, {"structure": 6, "evidence": 6, "text": 6}, {}, cal_dir)
        assert cal_ok["calibrated_score"] == 7.7 and cal_ok["offset_applied"] is True, cal_ok
        assert calibrated_scoring(8, {"structure": 8}, {}, cal_dir)["calibrated_score"] == 8.0
        assert calibrated_scoring(6, {"structure": 6}, {}, tmp / "no_such_cal") is None
        # 集成：R7 增量跑（合并上一轮门禁）+ calibration 字段 → gates.json 带 calibrated_score
        cfg_cal = {**cfg_pdf2, "calibration": str(cal_dir)}
        run_one(cfg_cal, ["R7"], skip_llm=True, diff_old=None)
        gcal = json.loads((tmp / "run_pdf_noev" / "gates.json").read_text(encoding="utf-8"))
        assert gcal["calibrated_score"] >= 7.0, gcal.get("calibrated_score")
        assert gcal["calibration"]["n"] == 6 and gcal["calibration"]["bias"] == 1.67, gcal["calibration"]
        assert "校准后评分" in (tmp / "run_pdf_noev" / "run_summary.md").read_text(encoding="utf-8")

    print("run_review selftest: OK")
    return 0


def doctor() -> int:
    """环境自检：换机器跑不通时先跑这个，逐项定位缺什么。"""
    import platform
    rows, bad = [], 0

    def check(name: str, ok: bool, detail: str, fix: str = "") -> None:
        nonlocal bad
        if not ok:
            bad += 1
        mark = "OK  " if ok else ("WARN" if fix.startswith("可选") else "FAIL")
        rows.append(f"[{mark}] {name}: {detail}" + (f"\n        修复：{fix}" if (fix and not ok) else ""))

    v = sys.version_info
    check("Python", (v.major, v.minor) >= (3, 10), f"{platform.python_version()}（union 语法需 ≥3.10）",
          "安装 Python ≥3.10 后重跑")
    for mod, why in [("scipy", "R4 统计复算"), ("pymupdf", "PDF 输入模式 / R2c 图内文本")]:
        try:
            __import__(mod)
            check(mod, True, f"已安装（{why}）", f"可选：pip install {mod}")
        except ImportError:
            check(mod, False, f"未安装（{why} 降级 SKIP）", f"可选：pip install {mod}")
    for mod in ["audit_package", "honesty_scan", "number_reconcile", "verify_manifest",
                "citation_check", "figure_check", "formula_check", "table_check",
                "novelty_check", "stats_recompute", "prism_review", "debate", "pdf_text"]:
        m = {"audit_package": audit_package, "honesty_scan": honesty_scan,
             "number_reconcile": number_reconcile, "verify_manifest": verify_manifest,
             "citation_check": citation_check, "figure_check": figure_check,
             "formula_check": formula_check, "table_check": table_check,
             "novelty_check": novelty_check, "stats_recompute": stats_recompute,
             "prism_review": prism_review, "debate": debate, "pdf_text": pdf_text}.get(mod)
        check(f"模块 {mod}", m is not None, "导入成功" if m else "导入失败",
              "与 scripts/ 同目录运行，或 `pip install -r requirements.txt` 后重试")
    script = Path(DEFAULT_LLM["script"])
    check("LLM 脚本", script.is_file(), str(script),
          "设环境变量 REVIEW_LLM_SCRIPT 指向 adversarial_review.py，或把它放在 review-workflow 的上级目录")
    ok, detail = rpc_health(DEFAULT_LLM["rpc"])
    check("LLM RPC", ok, f"{DEFAULT_LLM['rpc']} → {detail}",
          "可选：启动本地 LLM RPC 服务；不可达时 R6/R6b/R6c 自动 SKIP，证据层不受影响")
    print("\n".join(["[doctor] 审稿工作流环境自检", "-" * 60] + rows))
    print("-" * 60)
    print(f"[doctor] {'环境就绪' if bad == 0 else f'{bad} 项异常（见上）'}；"
          f"全部阶段均可降级运行：机械阶段只依赖标准库，LLM/scipy/pymupdf 缺失时自动 SKIP")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=Path, help="单篇配置 JSON")
    ap.add_argument("--stages", type=str, default=",".join(ALL_STAGES), help=f"逗号分隔阶段，默认全部：{','.join(ALL_STAGES)}")
    ap.add_argument("--skip-llm", action="store_true", help="跳过 R6（LLM 对抗审查）")
    ap.add_argument("--converge", type=int, default=None, help="R6 轮数（≥2 启用轮间稳定性过滤；覆盖 config 的 converge）")
    ap.add_argument("--diff", type=Path, help="旧 run 目录：生成与上一轮的对比")
    ap.add_argument("--calibration", type=Path,
                    help="TMLR 校准目录（cal_results，含 calibration_report.json + calibrations.json）："
                         "R7 额外输出 calibrated_score（覆盖 config 的 calibration 字段）")
    ap.add_argument("--batch", type=Path, help="批处理：configs 目录或 list.json")
    ap.add_argument("--init", type=Path, help="生成配置模板")
    ap.add_argument("--doctor", action="store_true", help="环境自检（换机器先跑这个）")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.doctor:
        return doctor()
    if args.init:
        return write_template(args.init)
    if args.batch:
        return run_batch(args.batch, args.skip_llm)
    if not args.config:
        ap.error("--config / --batch / --init / --selftest 至少一个")

    cfg = load_config(args.config)
    if args.calibration:
        cfg["calibration"] = str(args.calibration)
    stages = [s.strip() for s in args.stages.split(",") if s.strip()]
    bad = [s for s in stages if s not in ALL_STAGES]
    if bad:
        ap.error(f"未知阶段 {bad}；可选 {ALL_STAGES}")
    _, rc = run_one(cfg, stages, args.skip_llm, args.diff, args.converge)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
