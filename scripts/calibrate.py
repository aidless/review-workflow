# -*- coding: utf-8 -*-
"""评分校准（calibrate）— 审稿工作流 v2.2。

半自动评分（R7 suggested_score / PRISM min）不是终点——必须对照人工终审与真实
OpenReview 决策做校准，量化系统偏差后才知道怎么读这个分数：

  1. 判读日志 calibrations.json：每条 {paper, date, suggested, human, decision, gate, notes}
     （suggested = 工作流建议分；human = 人工终审分；decision = accept/reject；gate = FAIL/WARN/PASS）
  2. 校准指标：
       bias = mean(human - suggested)   正值 = 系统保守（低估），负值 = 系统高估
       MAE  = mean(|human - suggested|)
       相关性（Spearman/Pearson）仅在 n>=5 时计算，小样本不给
       门禁-决策一致性：FAIL↔reject、PASS↔accept 的混淆矩阵
  3. TMLR 官方审稿数据校准（v2.2，替代人工凑分）：
       浏览器过 Cloudflare 后经 API v2 抓取已接收论文的官方评审
       （TMLR 无数值评分——评审为 claims_and_evidence Yes/No 投票 + AE 分类决议）：
         - h_decision：AE 决议映射（Accept as is=8 / Accept with minor revision=7）
         - yes_rate：claims 投票 Yes 比例（连续信号，排序一致性目标）
       OpenReview API 直连 403（Cloudflare 拦 urllib/curl TLS 指纹）→ 浏览器桥接抓取
  4. 小样本纪律：n<5 只给描述统计并警告；每条 Critical 结论都标注样本量

已知边界（诚实披露）：TMLR 拒稿不公开 → 只能校准 accept 侧；决议仅两级（7/8），
绝对分 MAE 天然粗糙；claims 投票针对投稿版（修订前），与终版 PDF 存在版本差。

试点数据（--init 种子，来源为本项目真实审稿历史，不虚构）：
  - scievalsuite_v6：机械工作流 suggested=4（FAIL）vs 人工 5（未就绪）
  - scievalsuite_v11：PRISM min=5 vs 人工终审 8.0（工具型论文 min 维度偏保守）
  - f_series：人工 4（salami slicing），工作流未跑（suggested=null，提醒补跑）

用法:
    python calibrate.py --init calibrations.json                  # 生成含试点种子的日志
    python calibrate.py --log calibrations.json --out <outdir>     # 校准分析
    python calibrate.py --tmlr-dump tmlr_dump.json --n 6 --out <outdir>   # TMLR 分层抽样
    python calibrate.py --collect <runs_root> --entries tmlr_entries.json --out <outdir>  # 回填建议分
    python calibrate.py --selftest
"""
from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

MIN_N_CORR = 5          # 相关性计算的最小样本
OR_API = "https://api2.openreview.net/notes"
DECISION_BANDS = {      # 决策→分数带（TMLR 语义）
    "accept": (7, 10), "weak_accept": (6, 8), "reject": (1, 6), "withdraw": (1, 10),
}
# TMLR AE 决议 → 10 分制映射（accept 侧两级；reject 不公开，无法标定）
TMLR_DECISION_SCORE = {"Accept as is": 8, "Accept with minor revision": 7}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_log(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):            # 容错：{"entries": [...]}
        data = data.get("entries", [])
    return data


def calibration_metrics(entries: list[dict]) -> dict:
    pairs = [e for e in entries
             if isinstance(e.get("suggested"), (int, float))
             and isinstance(e.get("human"), (int, float))]
    n = len(pairs)
    out = {"pairs": n, "bias": None, "mae": None, "correlation": None,
           "corr_kind": None, "warning": None}
    if n == 0:
        out["warning"] = "无完整配对（suggested 与 human 同时存在的条目为 0）"
        return out
    diffs = [e["human"] - e["suggested"] for e in pairs]
    out["bias"] = round(sum(diffs) / n, 2)
    out["mae"] = round(sum(abs(d) for d in diffs) / n, 2)
    out["per_pair"] = [{"paper": e["paper"], "suggested": e["suggested"],
                        "human": e["human"], "diff": round(d, 2)}
                       for e, d in zip(pairs, diffs)]
    if n < MIN_N_CORR:
        out["warning"] = f"n={n} < {MIN_N_CORR}：只给描述统计，不计算相关性（小样本相关无意义）"
        return out
    try:
        from scipy import stats as sps
        xs = [float(e["suggested"]) for e in pairs]
        ys = [float(e["human"]) for e in pairs]
        if len(set(xs)) < 2 or len(set(ys)) < 2:
            out["warning"] = ("suggested 或 human 为常数（无区分度）——相关性不可计算；"
                              "PDF-only 模式下 min 维度评分塌缩是已知边界")
            return out
        rho, p_rho = sps.spearmanr(xs, ys)
        r, p_r = sps.pearsonr(xs, ys)
        out["correlation"] = {"spearman": round(float(rho), 3), "spearman_p": round(float(p_rho), 4),
                              "pearson": round(float(r), 3), "pearson_p": round(float(p_r), 4)}
    except ImportError:
        out["warning"] = "scipy 未安装：跳过相关性计算"
    return out


def _norm_decision(dec: str) -> str:
    """决议归一化：TMLR 风格（Accept as is / Accept with minor revision）→ accept/weak_accept。"""
    d = (dec or "").lower().strip()
    if d.startswith("accept as is"):
        return "accept"
    if d.startswith("accept with minor"):
        return "weak_accept"
    return d


def gate_consistency(entries: list[dict]) -> dict:
    """门禁-决策混淆：FAIL 应对应 reject，PASS 对应 accept。SKIP 是"该阶段不可判"
    （如 PDF 模式无证据目录），不构成任何方向的一致/不一致证据，不计入分母。"""
    matrix: dict[str, dict[str, int]] = {}
    for e in entries:
        gate, dec = e.get("gate"), _norm_decision(e.get("decision") or "")
        if not gate or not dec or gate == "SKIP":
            continue
        matrix.setdefault(gate, {}).setdefault(dec, 0)
        matrix[gate][dec] += 1
    consistent = sum(v for g, row in matrix.items() for d, v in row.items()
                     if (g == "FAIL" and d in ("reject", "withdraw"))
                     or (g == "PASS" and d in ("accept", "weak_accept"))
                     or (g == "WARN" and d))
    total = sum(v for row in matrix.values() for v in row.values())
    return {"matrix": matrix, "consistent": consistent, "total": total,
            "rate": round(consistent / total, 3) if total else None}


def fetch_openreview(venue: str = "tmlr", dump_path: Path | None = None) -> dict:
    """拉取 OpenReview 决策分布；API 403/不可达时降级为手动 dump 或 SKIP。"""
    if dump_path is not None:
        if not dump_path.is_file():
            return {"status": "SKIP", "detail": f"dump 文件不存在：{dump_path}"}
        data = json.loads(dump_path.read_text(encoding="utf-8"))
        notes = data.get("notes", data) if isinstance(data, dict) else data
        return _decision_prior(notes, source=str(dump_path))
    url = f"{OR_API}?content.venueid={venue}&limit=100"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "review-workflow-calibrate/2.0 (mailto:reviewer@example.org)"})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
        return _decision_prior(data.get("notes", []), source=url)
    except Exception as e:  # noqa: BLE001
        return {"status": "SKIP",
                "detail": (f"OpenReview API 不可达（{type(e).__name__}: {e}）。降级路径：浏览器登录 "
                           "openreview.net → 目标 venue → 导出/复制评审 JSON 存盘，"
                           f"再 --dump <该文件> 重跑")}


def _decision_prior(notes: list, source: str) -> dict:
    """从 OpenReview notes 统计决策分布（decision/recommendation 字段名随 venue 而异）。"""
    counts: dict[str, int] = {}
    for n in notes:
        c = (n.get("content") or {}) if isinstance(n, dict) else {}
        for key in ("decision", "recommendation", "rating"):
            v = c.get(key)
            v = v.get("value") if isinstance(v, dict) else v
            if v:
                counts[str(v)] = counts.get(str(v), 0) + 1
                break
    total = sum(counts.values())
    return {"status": "OK", "source": source, "notes": len(notes),
            "decision_counts": counts, "total_labeled": total,
            "accept_rate": round(sum(v for k, v in counts.items()
                                     if "accept" in k.lower()) / total, 3) if total else None}


def load_tmlr_dump(path: Path) -> list[dict]:
    """解析浏览器桥接抓取的 TMLR dump（含错误条目则剔除，重算 yes_rate）。"""
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, str):                      # 容错：双重编码 dump
        data = json.loads(data)
    papers = data.get("papers", data) if isinstance(data, dict) else data
    out = []
    for p in papers:
        if p.get("error") or not p.get("reviews"):
            continue
        votes = [r for r in p["reviews"] if r.get("ce") in ("Yes", "No")]
        if not votes or not p.get("decision") or not p.get("pdf"):
            continue
        p["yes_rate"] = round(sum(1 for r in votes if r["ce"] == "Yes") / len(votes), 3)
        p["n_reviews"] = len(votes)
        out.append(p)
    return out


def select_tmlr(dump_path: Path, n: int, out_dir: Path) -> list[dict]:
    """按 yes_rate 分层抽样（high ≥0.99 / mid ≥0.5 / low <0.5），band 内按
    yes_rate 降序均匀取点。确定性规则（无随机种子），决策类型尽量混搭。"""
    papers = load_tmlr_dump(dump_path)
    bands: dict[str, list[dict]] = {"high": [], "mid": [], "low": []}
    for p in papers:
        yr = p["yes_rate"]
        bands["high" if yr >= 0.99 else "mid" if yr >= 0.5 else "low"].append(p)
    for b in bands.values():
        b.sort(key=lambda p: (-p["yes_rate"], p.get("cdate") or 0))
    quota = {k: n // 3 for k in bands}
    for k in list(quota):                            # 余数给大 band
        quota[k] += 1 if n % 3 and len(bands[k]) >= quota[k] + 1 else 0
    picked: list[dict] = []
    for k, b in bands.items():
        q = min(quota[k], len(b))
        if q == 0:
            continue
        step = max(len(b) // q, 1)
        picked += [b[min(i * step, len(b) - 1)] for i in range(q)]
    entries = []
    for i, p in enumerate(picked):
        entries.append({
            "paper": p["forum"], "title": p["title"], "pdf": p["pdf"],
            "decision": p["decision"], "yes_rate": p["yes_rate"],
            "n_reviews": p["n_reviews"],
            "human": TMLR_DECISION_SCORE[p["decision"]],
            "suggested": None, "gate": None, "prism_min": None,
            "source": "tmlr", "date": now()[:10],
            "notes": f"OpenReview forum={p['forum']}；{p['n_reviews']} 位评审 "
                     f"claims 投票 Yes 率 {p['yes_rate']}",
        })
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "tmlr_entries.json").write_text(
        json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"dump {len(papers)} 篇有效 -> 分层抽样 {len(entries)} 篇 "
          f"(high {quota['high']}/mid {quota['mid']}/low {quota['low']}) "
          f"-> {out_dir / 'tmlr_entries.json'}")
    for e in entries:
        print(f"  [{e['decision']}] yes={e['yes_rate']} forum={e['paper']} {e['title'][:50]}")
    return entries


def collect_runs(runs_root: Path, entries_path: Path, out_dir: Path) -> list[dict]:
    """从各论文 run 目录的 gates.json / prism_review.json 回填 suggested/gate/prism_min。"""
    entries = json.loads(entries_path.read_text(encoding="utf-8"))
    for e in entries:
        rd = runs_root / f"run_{e['paper']}"
        gp = rd / "gates.json"
        if not gp.is_file():
            print(f"  跳过 {e['paper']}：无 {gp}")
            continue
        g = json.loads(gp.read_text(encoding="utf-8"))
        e["suggested"] = g.get("suggested_score")
        e["gate"] = g.get("overall")
        e["score_dimensions"] = g.get("score_dimensions")
        pp = rd / "prism_review.json"
        if pp.is_file():
            pr = json.loads(pp.read_text(encoding="utf-8"))
            dims = pr.get("dimensions") or {}
            scores = {k: d.get("score") for k, d in dims.items() if isinstance(d, dict)}
            scores = {k: s for k, s in scores.items() if isinstance(s, (int, float))}
            if scores:
                e["prism_min"] = min(scores.values())
                e["prism_dims"] = scores
                e["prism_mean"] = round(sum(scores.values()) / len(scores), 2)
        r6p = rd / "r6_llm.json"
        if r6p.is_file():
            r6 = json.loads(r6p.read_text(encoding="utf-8"))
            c = (r6.get("summary") or {}).get("counts") or {}
            e["stable_C"], e["stable_M"] = c.get("Critical"), c.get("Major")
        dp = rd / "debate.json"
        if dp.is_file():
            db = json.loads(dp.read_text(encoding="utf-8"))
            su = (db.get("summary") or {}).get("counts_sustained") or {}
            e["sust_C"], e["sust_M"] = su.get("Critical"), su.get("Major")
        e["notes"] = (e.get("notes") or "") + (
            f"；工作流 suggested={e['suggested']} ({e['gate']})"
            + (f"，PRISM min={e['prism_min']}" if e.get("prism_min") else ""))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "calibrations.json").write_text(
        json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"回填 {sum(1 for e in entries if e.get('suggested') is not None)}/{len(entries)} 条 "
          f"-> {out_dir / 'calibrations.json'}")
    return entries


def rank_metrics(entries: list[dict]) -> dict:
    """排序一致性（对照 TMLR 连续信号 yes_rate）：suggested / PRISM min / PRISM mean
    及 PRISM 逐维度各自的 Spearman。常数列（无区分度）不计算相关——NaN 相关不可读，
    如实报告塌缩（PDF-only 模式下 suggested 三维度全 6 是已知边界，PRISM 逐维度
    是该模式下仅存的排序信号）。"""
    out = {"n": 0, "suggested_vs_yesrate": None, "prism_vs_yesrate": None,
           "prism_mean_vs_yesrate": None, "prism_dims_vs_yesrate": None,
           "issue_counts_vs_yesrate": None, "warning": None}
    try:
        from scipy import stats as sps
    except ImportError:
        out["warning"] = "scipy 未安装：跳过排序一致性"
        return out
    pairs = [e for e in entries if isinstance(e.get("yes_rate"), (int, float))
             and isinstance(e.get("suggested"), (int, float))]
    out["n"] = len(pairs)
    if len(pairs) < MIN_N_CORR:
        out["warning"] = f"n={len(pairs)} < {MIN_N_CORR}：排序一致性样本不足"
        return out
    ys = [e["yes_rate"] for e in pairs]

    def _spearman(xs: list[float], ys_: list[float], label: str) -> dict:
        d = {"n": len(xs), "spearman": None, "p": None}
        if len(set(xs)) < 2:
            d["warning"] = (f"{label} 为常数（无区分度）——min 维度评分在该模式下塌缩，"
                            "排序校准不可用；请用 PRISM min 或带证据包的完整跑")
            return d
        if len(set(ys_)) < 2:
            d["warning"] = "yes_rate 为常数，排序目标无方差"
            return d
        rho, p = sps.spearmanr(xs, ys_)
        d.update({"spearman": round(float(rho), 3), "p": round(float(p), 4)})
        return d

    out["suggested_vs_yesrate"] = _spearman([e["suggested"] for e in pairs], ys, "suggested")
    out["prism_vs_yesrate"] = _spearman([e["prism_min"] for e in pairs], ys, "PRISM min") \
        if all(isinstance(e.get("prism_min"), (int, float)) for e in pairs) else None
    out["prism_mean_vs_yesrate"] = _spearman([e["prism_mean"] for e in pairs], ys, "PRISM mean") \
        if all(isinstance(e.get("prism_mean"), (int, float)) for e in pairs) else None
    dims_out: dict[str, dict] = {}
    for dim in ("P", "R", "I", "S"):
        vals = [(e.get("prism_dims") or {}).get(dim) for e in pairs]
        if all(isinstance(v, (int, float)) for v in vals):
            dims_out[dim] = _spearman([float(v) for v in vals], ys, f"PRISM-{dim}")
    out["prism_dims_vs_yesrate"] = dims_out or None
    # 问题数排序一致性（校准的关键 null 检验：accept 侧问题密度是否携带信号）
    issue_out: dict[str, dict] = {}
    for key, label in (("stable_C", "stable Critical"), ("stable_M", "stable Major"),
                       ("sust_C", "sustained Critical"), ("sust_M", "sustained Major")):
        vals = [e.get(key) for e in pairs]
        if all(isinstance(v, (int, float)) for v in vals):
            issue_out[key] = _spearman([float(v) for v in vals], ys, label)
    out["issue_counts_vs_yesrate"] = issue_out or None
    return out


def write_seed(path: Path) -> int:
    seed = [
        {"paper": "scievalsuite_v6", "date": "2026-08-26", "suggested": 4, "human": 5,
         "decision": "reject", "gate": "FAIL",
         "notes": "机械工作流 FAIL（24 缺引用/139 路径泄漏/16 manifest 缺失/94 pending 数字）；"
                  "v6 时点人工判断同样未就绪——方向一致，绝对值保守 1 分"},
        {"paper": "scievalsuite_v11_prism", "date": "2026-08-26", "suggested": 5, "human": 8.0,
         "decision": "accept", "gate": "WARN",
         "notes": "PRISM min=5（R=5：L2 零功效/选择性报告，与人工终审 limitation 清单一致）；"
                  "人工终审 8.0——measurement instrument 价值抵消统计弱功效。"
                  "结论：min 维度对工具型/benchmark 论文系统性偏保守"},
        {"paper": "f_series_6volumes", "date": "2026-08-26", "suggested": None, "human": 4,
         "decision": "reject", "gate": None,
         "notes": "人工最高标准审阅：salami slicing，6 卷等效 1.5-2 篇 TMLR；"
                  "工作流未跑（TODO：补跑后填 suggested）"},
    ]
    path.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"种子日志（含试点数据 {len(seed)} 条，其中完整配对 2 条）-> {path}")
    return 0


def analyze(log_path: Path, out_dir: Path) -> dict:
    entries = load_log(log_path)
    metrics = calibration_metrics(entries)
    gates = gate_consistency(entries)
    ranks = rank_metrics(entries)
    tmlr = [e for e in entries if e.get("source") == "tmlr"]
    report = {"meta": {"log": str(log_path), "entries": len(entries),
                       "timestamp": now()},
              "metrics": metrics, "gate_consistency": gates,
              "rank_consistency": ranks,
              "tmlr_entries": len(tmlr)}

    lines = [
        "# 评分校准报告（v2.2）",
        "",
        f"- 判读日志：`{log_path}`（{len(entries)} 条，完整配对 {metrics['pairs']} 条）",
        "",
        "## 校准指标",
        "",
    ]
    if metrics["pairs"]:
        lines += [
            f"- **bias = {metrics['bias']}**（human − suggested，正 = 系统保守/低估）",
            f"- MAE = {metrics['mae']}",
        ]
        if metrics.get("correlation"):
            c = metrics["correlation"]
            lines.append(f"- Spearman ρ={c['spearman']}（p={c['spearman_p']}），"
                         f"Pearson r={c['pearson']}（p={c['pearson_p']}）")
    else:
        lines.append("- 无完整配对，无法计算偏差")
    if metrics.get("warning"):
        lines.append(f"- ⚠ {metrics['warning']}")
    if metrics.get("per_pair"):
        lines += ["", "## 逐条配对", "", "| 论文 | suggested | human | 差 |", "|---|---|---|---|"]
        lines += [f"| {p['paper']} | {p['suggested']} | {p['human']} | {p['diff']:+} |"
                  for p in metrics["per_pair"]]
    if ranks.get("n") or ranks.get("warning"):
        lines += ["", "## 排序一致性（对照 TMLR claims 投票 yes_rate）", ""]

        def _rank_line(label: str, d: dict | None) -> list[str]:
            if not d:
                return []
            n = d.get("n", ranks.get("n"))
            if d.get("spearman") is not None:
                return [f"- {label} vs yes_rate：Spearman ρ={d['spearman']}"
                        f"（p={d['p']}，n={n}）"]
            if d.get("warning"):
                return [f"- ⚠ {label} vs yes_rate：{d['warning']}"]
            return []

        lines += _rank_line("suggested_score", ranks.get("suggested_vs_yesrate"))
        lines += _rank_line("PRISM min", ranks.get("prism_vs_yesrate"))
        lines += _rank_line("PRISM mean", ranks.get("prism_mean_vs_yesrate"))
        for dim, d in (ranks.get("prism_dims_vs_yesrate") or {}).items():
            lines += _rank_line(f"PRISM {dim}", d)
        for key, d in (ranks.get("issue_counts_vs_yesrate") or {}).items():
            lines += _rank_line(f"问题数 {key}", d)
        if ranks.get("warning"):
            lines.append(f"- ⚠ {ranks['warning']}")
    if tmlr:
        lines += ["", "## TMLR 官方审稿数据校准", "",
                  f"- {len(tmlr)} 条来自 OpenReview API v2（已接收论文；h_decision 映射：",
                  "  Accept as is=8 / Accept with minor revision=7）",
                  "", "| 论文 | 决议 | yes_rate | suggested | gate | PRISM P/R/I/S | h_decision |",
                  "|---|---|---|---|---|---|---|"]
        for e in tmlr:
            dims = e.get("prism_dims") or {}
            dimstr = "/".join(str(dims.get(k, "—")) for k in ("P", "R", "I", "S")) \
                if dims else "—"
            lines.append(f"| {e['paper']} | {e.get('decision')} | {e.get('yes_rate')} "
                         f"| {e.get('suggested') if e.get('suggested') is not None else '—'} "
                         f"| {e.get('gate') or '—'} | {dimstr} "
                         f"| {e.get('human')} |")
        lines += ["", "**边界**：TMLR 拒稿不公开（无法标定 FAIL↔reject 一侧）；AE 决议仅 accept 侧",
                  "两级（7/8），绝对分 MAE 天然粗糙；claims 投票针对投稿版，与终版 PDF 存在版本差。",
                  "全 accept 样本上的 FAIL 门禁 = 证据层假阳性（对已接收论文误报），须逐条复核。", ""]
    lines += ["", "## 门禁-决策一致性", ""]
    if gates["total"]:
        lines += [f"- 一致率 {gates['consistent']}/{gates['total']} = {gates['rate']}",
                  "", "| 门禁 | 决策计数 |", "|---|---|"]
        lines += [f"| {g} | {row} |" for g, row in gates["matrix"].items()]
    else:
        lines.append("- 无带 gate+decision 的条目")
    missing = [e["paper"] for e in entries if e.get("suggested") is None]
    if missing:
        lines += ["", "## 待补跑（suggested 缺失）", ""]
        lines += [f"- {p}：工作流未跑或未记录建议分" for p in missing]
    lines += ["", "## 解读纪律", "",
              "- suggested_score 是**下界参考**（min 维度纪律天然保守），不是点估计",
              "- bias>0 时：人工普遍高于系统——用于工具型论文时在终审上浮 bias 分",
              "- 每新增一条人工终审都应回填本日志，n>=10 后相关性才有参考价值",
              ""]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "calibration_report.md").write_text("\n".join(lines), encoding="utf-8")
    (out_dir / "calibration_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"pairs={metrics['pairs']} bias={metrics['bias']} mae={metrics['mae']} "
          f"gate_consistent={gates['consistent']}/{gates['total']} -> {out_dir / 'calibration_report.md'}")
    return report


def selftest() -> int:
    import tempfile

    tmp = Path(tempfile.mkdtemp())

    # 1) metrics：bias/MAE 正确
    entries = [
        {"paper": "a", "suggested": 4, "human": 5},
        {"paper": "b", "suggested": 5, "human": 8},
        {"paper": "c", "suggested": 6, "human": 6},
    ]
    m = calibration_metrics(entries)
    assert m["pairs"] == 3 and m["bias"] == round((1 + 3 + 0) / 3, 2) == 1.33, m
    assert m["mae"] == round((1 + 3 + 0) / 3, 2) == 1.33, m
    assert m["correlation"] is None and "n=3" in m["warning"], m   # 小样本不给相关

    # 2) n>=5 时给相关（scipy 若装）
    big = [{"paper": f"p{i}", "suggested": i % 10, "human": (i % 10) + (1 if i % 2 else 0)}
           for i in range(8)]
    m2 = calibration_metrics(big)
    if m2["correlation"] is not None:
        assert "spearman" in m2["correlation"]
    else:
        assert "scipy" in (m2["warning"] or "")

    # 3) 门禁一致性
    ge = gate_consistency([
        {"gate": "FAIL", "decision": "reject"},
        {"gate": "PASS", "decision": "accept"},
        {"gate": "FAIL", "decision": "accept"},      # 不一致：FAIL 却 accept
        {"gate": None, "decision": "accept"},        # 缺 gate 不计
    ])
    assert ge["total"] == 3 and ge["consistent"] == 2 and ge["rate"] == round(2 / 3, 3), ge

    # 4) 种子日志 + 端到端分析
    log = tmp / "cal.json"
    assert write_seed(log) == 0
    seed = load_log(log)
    assert len(seed) == 3
    rep = analyze(log, tmp / "out")
    assert rep["metrics"]["pairs"] == 2, rep["metrics"]        # v6 与 v11_prism 完整配对
    assert rep["metrics"]["bias"] == round((1 + 3.0) / 2, 2), rep["metrics"]
    assert "f_series_6volumes" not in [e["paper"] for e in rep["metrics"]["per_pair"]]
    assert (tmp / "out" / "calibration_report.md").exists()
    md = (tmp / "out" / "calibration_report.md").read_text(encoding="utf-8")
    assert "下界参考" in md and "min 维度" in md

    # 5) fetch 降级：不存在的 dump → SKIP 且给手动路径提示
    r = fetch_openreview(dump_path=tmp / "nope.json")
    assert r["status"] == "SKIP" and "dump 文件不存在" in r["detail"], r
    # API 403 → SKIP + 手动导出指引（不依赖网络也测）
    r2 = fetch_openreview()
    assert r2["status"] in ("OK", "SKIP"), r2

    # 6) decision prior 解析
    notes = [{"content": {"decision": {"value": "Accept"}},
              }, {"content": {"decision": {"value": "Reject"}}},
             {"content": {"decision": {"value": "Accept"}}}]
    prior = _decision_prior(notes, "test")
    assert prior["accept_rate"] == round(2 / 3, 3) and prior["total_labeled"] == 3, prior

    # 7) TMLR dump 解析 + 分层抽样 + 回填 + 排序一致性（端到端，全离线）
    dump = {"papers": [
        {"forum": f"f{i}", "title": f"t{i}", "pdf": f"/pdf/{i}.pdf", "cdate": 1000 + i,
         "decision": "Accept as is" if i % 2 else "Accept with minor revision",
         "reviews": [{"ce": "Yes"}] * (i % 4 + 1) + [{"ce": "No"}] * (3 - i % 4)}
        for i in range(12)] + [{"forum": "bad", "error": "fetch failed"}]}
    dp = tmp / "dump.json"
    dp.write_text(json.dumps(dump), encoding="utf-8")
    papers = load_tmlr_dump(dp)
    assert len(papers) == 12 and papers[0]["yes_rate"] == 0.25, len(papers)
    entries = select_tmlr(dp, 6, tmp / "sel")
    es = json.loads((tmp / "sel" / "tmlr_entries.json").read_text(encoding="utf-8"))
    assert len(es) == 6 and all(e["source"] == "tmlr" for e in es)
    assert all(e["human"] in (7, 8) for e in es)           # 决议→分数映射只有 accept 侧两级
    # 回填：伪造三个 run 目录（含 gates.json + prism_review.json）
    runs = tmp / "runs"
    for e in es[:3]:
        rd = runs / f"run_{e['paper']}"
        rd.mkdir(parents=True)
        (rd / "gates.json").write_text(json.dumps(
            {"suggested_score": 6, "overall": "WARN",
             "score_dimensions": {"structure": 8, "evidence": 6, "text": 6}}), encoding="utf-8")
        (rd / "prism_review.json").write_text(json.dumps(
            {"dimensions": {"P": {"score": 7}, "R": {"score": 5}, "I": {"score": 6}, "S": {"score": 8}}}),
            encoding="utf-8")
        (rd / "r6_llm.json").write_text(json.dumps(
            {"summary": {"counts": {"Critical": 3, "Major": 4}}}), encoding="utf-8")
        (rd / "debate.json").write_text(json.dumps(
            {"summary": {"counts_sustained": {"Critical": 2, "Major": 1}}}), encoding="utf-8")
    filled = collect_runs(runs, tmp / "sel" / "tmlr_entries.json", tmp / "cal")
    assert sum(1 for e in filled if e.get("suggested") is not None) == 3
    assert all(e["prism_min"] == 5 for e in filled[:3])     # PRISM min 取四维最小
    assert all(e["prism_mean"] == 6.5 for e in filled[:3])  # 四维均值 (7+5+6+8)/4
    assert all(e["prism_dims"] == {"P": 7, "R": 5, "I": 6, "S": 8} for e in filled[:3])
    assert all(e["stable_C"] == 3 and e["stable_M"] == 4 for e in filled[:3])   # v2.2 问题数回填
    assert all(e["sust_C"] == 2 and e["sust_M"] == 1 for e in filled[:3])
    rep = analyze(tmp / "cal" / "calibrations.json", tmp / "cal")
    assert rep["tmlr_entries"] == 6
    assert rep["rank_consistency"]["n"] == 3                # n<5 → 只警告不算相关
    assert rep["rank_consistency"]["warning"], rep["rank_consistency"]
    md = (tmp / "cal" / "calibration_report.md").read_text(encoding="utf-8")
    assert "TMLR 官方审稿数据校准" in md and "拒稿不公开" in md and "yes_rate" in md
    # 8) 排序一致性：n>=5 时给 Spearman（构造单调数据）
    mono = [{"paper": f"m{i}", "suggested": i, "yes_rate": i / 10, "human": 7}
            for i in range(6)]
    rm = rank_metrics(mono)
    assert rm["n"] == 6 and rm["suggested_vs_yesrate"]["spearman"] == 1.0, rm
    assert rm["prism_vs_yesrate"] is None and rm["prism_dims_vs_yesrate"] is None, rm
    # 8b) PRISM 均值/逐维度排序一致性 + suggested 塌缩守卫（PDF-only 真实形态）
    mono2 = [{"paper": f"q{i}", "suggested": 6, "yes_rate": i / 10, "human": 7,
              "prism_min": 5 + i % 2, "prism_mean": round(6 + i * 0.2, 2),
              "prism_dims": {"P": 8, "R": 6, "I": 6 + i, "S": 7}}
             for i in range(6)]
    rm2 = rank_metrics(mono2)
    assert "常数" in rm2["suggested_vs_yesrate"]["warning"], rm2   # suggested 恒 6
    assert rm2["prism_mean_vs_yesrate"]["spearman"] == 1.0, rm2
    assert rm2["prism_dims_vs_yesrate"]["I"]["spearman"] == 1.0, rm2
    assert "常数" in rm2["prism_dims_vs_yesrate"]["P"]["warning"], rm2  # P 恒 8
    # 9) 常数列守卫：suggested 恒 6（PDF-only 塌缩）→ 不算相关，报塌缩
    flat = [{"paper": f"f{i}", "suggested": 6, "yes_rate": i / 10, "human": 7}
            for i in range(6)]
    rf = rank_metrics(flat)
    assert rf["suggested_vs_yesrate"]["spearman"] is None, rf
    assert "常数" in rf["suggested_vs_yesrate"]["warning"], rf
    mf = calibration_metrics(flat)
    assert mf["correlation"] is None and "常数" in mf["warning"], mf
    # 10) 问题数排序一致性（null 检验路径：问题数与 yes_rate 无关时不给假信号）
    noisy = [{"paper": f"n{i}", "suggested": 6, "yes_rate": (5 - i) / 10, "human": 7,
              "stable_C": 10 + (i % 3), "stable_M": 20, "sust_C": 5 - i, "sust_M": 8}
             for i in range(6)]
    rn = rank_metrics(noisy)
    assert "issue_counts_vs_yesrate" in rn and rn["issue_counts_vs_yesrate"], rn
    assert rn["issue_counts_vs_yesrate"]["sust_C"]["spearman"] == 1.0, rn  # 与 yes_rate 同向递减 → 完全正相关
    assert "常数" in rn["issue_counts_vs_yesrate"]["stable_M"]["warning"], rn  # 恒 20 → 塌缩
    # 11) TMLR 决议归一化：Accept as is→accept；SKIP 门禁不入分母
    gt = gate_consistency([
        {"gate": "WARN", "decision": "Accept as is"},
        {"gate": "PASS", "decision": "Accept with minor revision"},
        {"gate": "SKIP", "decision": "Accept as is"},   # SKIP 不计
        {"gate": "FAIL", "decision": "Accept as is"},   # 不一致
    ])
    assert gt["total"] == 3 and gt["consistent"] == 2, gt
    assert gt["matrix"].get("PASS", {}).get("weak_accept") == 1, gt
    print("calibrate selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--init", type=Path, help="生成含试点种子的判读日志")
    ap.add_argument("--log", type=Path, help="判读日志 JSON（分析入口）")
    ap.add_argument("--tmlr-dump", type=Path,
                    help="浏览器桥接抓取的 TMLR dump JSON（分层抽样入口）")
    ap.add_argument("--n", type=int, default=6, help="TMLR 抽样篇数（默认 6）")
    ap.add_argument("--collect", type=Path,
                    help="各论文 run 目录的根（run_<forum>/gates.json），回填 suggested")
    ap.add_argument("--entries", type=Path, help="TMLR entries JSON（--collect 配套）")
    ap.add_argument("--fetch-tmlr", action="store_true", help="拉取 TMLR 决策先验")
    ap.add_argument("--dump", type=Path, help="手动导出的 OpenReview JSON（API 403 的降级路径）")
    ap.add_argument("--out", type=Path, default=Path("audit_out"))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.init:
        return write_seed(args.init)
    if args.tmlr_dump:
        select_tmlr(args.tmlr_dump, args.n, args.out)
        return 0
    if args.collect:
        if not args.entries:
            ap.error("--collect 需要 --entries <tmlr_entries.json>")
        collect_runs(args.collect, args.entries, args.out)
        analyze(args.out / "calibrations.json", args.out)
        return 0
    if args.log:
        analyze(args.log, args.out)
        return 0
    if args.fetch_tmlr:
        r = fetch_openreview(dump_path=args.dump)
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "openreview_prior.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({k: v for k, v in r.items() if k != "source"},
                         ensure_ascii=False, indent=2)[:800])
        print(f"-> {args.out / 'openreview_prior.json'}")
        return 0
    ap.error("--log / --tmlr-dump / --collect / --fetch-tmlr / --init / --selftest 至少一个")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
