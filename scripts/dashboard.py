# -*- coding: utf-8 -*-
"""批处理仪表盘（dashboard）— 审稿工作流 v2.0。

扫描一批 run 目录（每个含 gates.json），生成**单文件离线 HTML 仪表盘**：
  - KPI 行：论文数 / FAIL / WARN / PASS / 平均建议分
  - 门禁矩阵表：论文 × R0-R7 阶段，色块（FAIL 红 / WARN 黄 / SKIP 灰 / PASS 绿）
  - ECharts 图（echarts.min.js 全量内嵌，零外网依赖）：
      1. 总体门禁分布饼图
      2. 各论文建议分横向条形图（按 overall 着色）
      3. 三维度评分雷达图（结构/证据/文本，min 纪律可视化）
  - 同名论文多轮 run：--latest 只保留最新一轮，默认全部展示（趋势对比）

用法:
    python dashboard.py --runs <runs目录> [--out dashboard.html] [--latest] [--title "标题"]
    python dashboard.py --selftest
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ECHARTS_PATH = Path(__file__).resolve().parents[1] / "templates" / "echarts.min.js"
GATE_COLOR = {"FAIL": "#e5484d", "WARN": "#f5a524", "SKIP": "#8b8d98", "PASS": "#30a46c"}
STAGE_ORDER = ["R0", "R1", "R1b", "R1c", "R1d", "R2", "R2b", "R2c", "R2d", "R3", "R4",
               "R5", "R6", "R6b", "R6c", "R7"]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def collect_runs(root: Path) -> list[dict]:
    entries = []
    for g in sorted(root.rglob("gates.json")):
        try:
            d = json.loads(g.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        stages = d.get("stages") or {}
        entries.append({
            "name": d.get("name", g.parent.name),
            "path": str(g.parent).replace("\\", "/"),
            "overall": d.get("overall", "?"),
            "score": d.get("suggested_score"),
            "dims": d.get("score_dimensions") or {},
            "prism": d.get("prism_scores") or {},
            "timestamp": d.get("timestamp", ""),
            "stages": {k: (v or {}).get("gate") for k, v in stages.items()},
            "metrics": {k: (v or {}).get("metric", "") for k, v in stages.items()},
        })
    return sorted(entries, key=lambda e: (e["name"], e["timestamp"]))


def keep_latest(entries: list[dict]) -> list[dict]:
    best: dict[str, dict] = {}
    for e in entries:
        best[e["name"]] = e      # 已按 (name, timestamp) 排序，后者覆盖
    return sorted(best.values(), key=lambda e: e["name"])


def build_html(entries: list[dict], title: str) -> str:
    echarts_js = ""
    if ECHARTS_PATH.is_file():
        echarts_js = ECHARTS_PATH.read_text(encoding="utf-8")

    n = len(entries)
    n_fail = sum(1 for e in entries if e["overall"] == "FAIL")
    n_warn = sum(1 for e in entries if e["overall"] == "WARN")
    n_pass = sum(1 for e in entries if e["overall"] == "PASS")
    scores = [e["score"] for e in entries if isinstance(e["score"], (int, float))]
    avg_score = round(sum(scores) / len(scores), 1) if scores else "-"

    # 门禁矩阵表
    head = "".join(f"<th>{s}</th>" for s in STAGE_ORDER)
    rows = []
    for e in entries:
        cells = "".join(
            f'<td><span class="chip" style="background:{GATE_COLOR.get(e["stages"].get(s), "#ddd")}"'
            f' title="{(e["metrics"].get(s) or "")[:160]}">{e["stages"].get(s, "·")}</span></td>'
            for s in STAGE_ORDER)
        score = e["score"] if e["score"] is not None else "-"
        rows.append(
            f'<tr><td class="name">{e["name"]}</td>'
            f'<td><span class="chip" style="background:{GATE_COLOR.get(e["overall"], "#8b8d98")};'
            f'color:#fff">{e["overall"]}</span></td>'
            f'<td class="score">{score}</td>{cells}</tr>')
    matrix = ("<table class='matrix'><tr><th>论文</th><th>overall</th><th>分</th>" + head + "</tr>"
              + "".join(rows) + "</table>")

    # 图数据
    pie_data = [{"name": g, "value": sum(1 for e in entries if e["overall"] == g)}
                for g in ("PASS", "WARN", "FAIL") if any(e["overall"] == g for e in entries)]
    bar_names = [e["name"] for e in entries]
    bar_scores = [e["score"] if isinstance(e["score"], (int, float)) else 0 for e in entries]
    bar_colors = [GATE_COLOR.get(e["overall"], "#8b8d98") for e in entries]
    radar_papers = [e["name"] for e in entries][:8]          # 雷达最多 8 个系列防糊
    dims_keys = ["structure", "evidence", "text"]
    radar_series = [{"name": e["name"],
                     "value": [e["dims"].get(k) if isinstance(e["dims"].get(k), (int, float)) else 0
                               for k in dims_keys],
                     "areaStyle": {"opacity": 0.08}}
                    for e in entries if e["name"] in radar_papers]

    # PRISM 四维雷达（仅当有 PRISM 评分的论文才渲染）
    prism_entries = [e for e in entries if e["prism"]]
    prism_card = prism_js = ""
    if prism_entries:
        prism_papers = [e["name"] for e in prism_entries][:8]
        prism_series = [{"name": e["name"],
                         "value": [e["prism"].get(k, 0) for k in ("P", "R", "I", "S")],
                         "areaStyle": {"opacity": 0.08}}
                        for e in prism_entries if e["name"] in prism_papers]
        prism_card = ('<div class="card"><h2>PRISM 四维雷达（P 契合 / R 严谨 / I 贡献 / S 诚实）</h2>'
                      '<div id="radar2" class="chart"></div></div>')
        prism_js = (
            "const radar2 = echarts.init(document.getElementById('radar2'));\n"
            "radar2.setOption({tooltip:{}, legend:{type:'scroll', bottom:0},\n"
            " radar:{indicator:[{name:'P 契合', max:10}, {name:'R 严谨', max:10}, "
            "{name:'I 贡献', max:10}, {name:'S 诚实', max:10}], radius:'62%'},\n"
            f" series:[{{type:'radar', data:{json.dumps(prism_series, ensure_ascii=False)}}}]}});\n"
            "window.addEventListener('resize', () => radar2.resize());")

    return f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8">
<title>{title}</title>
<style>
 body{{font-family:'Segoe UI',system-ui,sans-serif;margin:0;background:#f6f7f9;color:#1b1f24}}
 header{{background:#1b1f24;color:#fff;padding:18px 28px}}
 header h1{{margin:0;font-size:20px}} header small{{color:#9aa0aa}}
 .wrap{{max-width:1180px;margin:0 auto;padding:20px}}
 .kpis{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:20px}}
 .kpi{{background:#fff;border-radius:10px;padding:14px 16px;box-shadow:0 1px 3px rgba(0,0,0,.08)}}
 .kpi .v{{font-size:26px;font-weight:700}} .kpi .l{{color:#6b7280;font-size:12px}}
 .card{{background:#fff;border-radius:10px;padding:16px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,.08)}}
 .card h2{{font-size:15px;margin:0 0 12px;color:#374151}}
 .charts{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
 .charts2{{display:grid;grid-template-columns:1fr;gap:20px}}
 .chart{{height:320px}}
 table.matrix{{border-collapse:collapse;width:100%;font-size:12px;background:#fff}}
 table.matrix th,table.matrix td{{border:1px solid #e5e7eb;padding:5px 8px;text-align:center}}
 table.matrix th{{background:#f3f4f6;position:sticky;top:0}}
 td.name{{text-align:left;font-weight:600;white-space:nowrap}}
 td.score{{font-weight:700;font-size:14px}}
 .chip{{display:inline-block;min-width:38px;padding:2px 6px;border-radius:9px;color:#fff;font-size:11px;font-weight:600}}
 footer{{text-align:center;color:#9aa0aa;font-size:12px;padding:16px}}
</style></head><body>
<header><h1>{title}</h1><small>生成于 {now()} · {n} 篇论文 · min 维度评分纪律（不平均）</small></header>
<div class="wrap">
<div class="kpis">
 <div class="kpi"><div class="v">{n}</div><div class="l">论文</div></div>
 <div class="kpi"><div class="v" style="color:{GATE_COLOR['FAIL']}">{n_fail}</div><div class="l">FAIL</div></div>
 <div class="kpi"><div class="v" style="color:{GATE_COLOR['WARN']}">{n_warn}</div><div class="l">WARN</div></div>
 <div class="kpi"><div class="v" style="color:{GATE_COLOR['PASS']}">{n_pass}</div><div class="l">PASS</div></div>
 <div class="kpi"><div class="v">{avg_score}</div><div class="l">平均建议分</div></div>
</div>
<div class="card"><h2>门禁矩阵（论文 × 阶段，悬停看指标）</h2><div style="overflow:auto;max-height:420px">{matrix}</div></div>
<div class="charts">
 <div class="card"><h2>总体门禁分布</h2><div id="pie" class="chart"></div></div>
 <div class="card"><h2>建议分（min 维度）</h2><div id="bar" class="chart"></div></div>
</div>
<div class="charts2"><div class="card"><h2>三维度评分雷达（结构/证据/文本）</h2><div id="radar" class="chart"></div></div>
{prism_card}
</div>
<footer>review-workflow v2.0 · 离线单文件（ECharts 已内嵌）· 证据层 FAIL → 评分 cap 4</footer>
<script>{echarts_js}</script>
<script>
const pie = echarts.init(document.getElementById('pie'));
pie.setOption({{tooltip:{{}}, series:[{{type:'pie', radius:['38%','68%'], label:{{formatter:'{{b}} {{c}}'}},
 data:{json.dumps(pie_data, ensure_ascii=False)}
}}]}});
const bar = echarts.init(document.getElementById('bar'));
bar.setOption({{tooltip:{{}}, grid:{{left:150, right:30, top:10, bottom:24}},
 xAxis:{{type:'value', min:0, max:10}}, yAxis:{{type:'category', data:{json.dumps(bar_names, ensure_ascii=False)}}},
 series:[{{type:'bar', data:{json.dumps([{'value': s, 'itemStyle': {'color': c}} for s, c in zip(bar_scores, bar_colors)], ensure_ascii=False)}}}]
}});
const radar = echarts.init(document.getElementById('radar'));
radar.setOption({{tooltip:{{}}, legend:{{type:'scroll', bottom:0}},
 radar:{{indicator:[{{name:'结构 Structure', max:10}}, {{name:'证据 Evidence', max:10}}, {{name:'文本 Text', max:10}}], radius:'62%'}},
 series:[{{type:'radar', data:{json.dumps(radar_series, ensure_ascii=False)}}}]
}});
{prism_js}
window.addEventListener('resize', () => [pie, bar, radar].forEach(c => c.resize()));
</script></body></html>"""


def selftest() -> int:
    import tempfile

    tmp = Path(tempfile.mkdtemp())
    runs = tmp / "runs"

    def mk(name: str, out: str, overall: str, score: int, dims: dict, stages: dict,
           prism: dict | None = None) -> None:
        d = runs / out
        d.mkdir(parents=True, exist_ok=True)
        data = {
            "name": name, "timestamp": f"2026-08-26T00:0{len(out) % 10}:00Z",
            "overall": overall, "suggested_score": score, "score_dimensions": dims,
            "stages": {s: {"gate": g, "metric": f"{s} metric {g}"} for s, g in stages.items()},
        }
        if prism:
            data["prism_scores"] = prism
        (d / "gates.json").write_text(json.dumps(data), encoding="utf-8")

    mk("alpha", "run1", "FAIL", 4, {"structure": 8, "evidence": 4, "text": 6},
       {"R0": "PASS", "R1": "PASS", "R1b": "PASS", "R1c": "SKIP", "R1d": "WARN", "R2": "FAIL",
        "R2b": "PASS", "R2c": "FAIL", "R2d": "FAIL", "R3": "WARN", "R4": "FAIL", "R5": "PASS",
        "R6": "SKIP", "R6b": "WARN", "R6c": "SKIP", "R7": "FAIL"},
       prism={"P": 6, "R": 5, "I": 5, "S": 9})
    mk("beta", "run2", "PASS", 8, {"structure": 8, "evidence": 8, "text": 8},
       {"R0": "PASS", "R1": "PASS", "R1b": "SKIP", "R1c": "SKIP", "R1d": "PASS", "R2": "PASS",
        "R2b": "PASS", "R2c": "PASS", "R2d": "PASS", "R3": "PASS", "R4": "PASS", "R5": "PASS",
        "R6": "SKIP", "R6b": "SKIP", "R6c": "SKIP", "R7": "PASS"})
    # 同名论文第二轮（趋势对比场景）
    mk("alpha", "run3", "WARN", 6, {"structure": 8, "evidence": 6, "text": 6},
       {"R0": "PASS", "R1": "PASS", "R1b": "PASS", "R1c": "SKIP", "R1d": "PASS", "R2": "PASS",
        "R2b": "PASS", "R2c": "PASS", "R2d": "PASS", "R3": "PASS", "R4": "PASS", "R5": "PASS",
        "R6": "WARN", "R6b": "PASS", "R6c": "PASS", "R7": "WARN"},
       prism={"P": 7, "R": 6, "I": 6, "S": 9})

    entries = collect_runs(runs)
    assert len(entries) == 3, entries
    assert [e["name"] for e in entries] == ["alpha", "alpha", "beta"], entries
    latest = keep_latest(entries)
    assert len(latest) == 2 and [e["name"] for e in latest] == ["alpha", "beta"], latest

    html = build_html(entries, "自测仪表盘")
    out = tmp / "dash.html"
    out.write_text(html, encoding="utf-8")
    assert out.exists() and len(html) > 1000
    for marker in ("alpha", "beta", "门禁矩阵", "三维度评分雷达", "平均建议分"):
        assert marker in html, marker
    # PRISM 雷达按需渲染（有 prism_scores 的论文才出现）
    assert "PRISM 四维雷达" in html and "radar2" in html
    # 无 prism 的论文清单不渲染 PRISM 卡片
    html_no_prism = build_html([e for e in entries if e["name"] == "beta"], "无 PRISM")
    assert "radar2" not in html_no_prism
    # 门禁矩阵含 FAIL/WARN 色块与阶段表头
    assert ">FAIL</span>" in html and ">WARN</span>" in html
    assert "<th>R2b</th>" in html and "<th>R7</th>" in html
    assert "<th>R1c</th>" in html and "<th>R2c</th>" in html and "<th>R6c</th>" in html
    assert "<th>R1d</th>" in html and "<th>R2d</th>" in html
    # 离线自包含：无外网 script src
    assert 'src="http' not in html and "src='http" not in html
    # KPI 数字
    assert ">3<" in html            # 3 篇
    assert ">1<" in html            # 1 FAIL
    # ECharts 内嵌（templates 有 echarts.min.js 时）
    if ECHARTS_PATH.is_file():
        assert len(html) > 500_000, len(html)
    else:
        assert "echarts" in html    # 无本地库时仍生成（图缺 JS 静默降级）
    print("dashboard selftest: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--runs", type=Path, help="run 目录（递归找 gates.json）")
    ap.add_argument("--out", type=Path, default=Path("review_dashboard.html"))
    ap.add_argument("--latest", action="store_true", help="同名论文只保留最新一轮")
    ap.add_argument("--title", default="审稿工作流批处理仪表盘")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.runs:
        ap.error("--runs required (or --selftest)")
    entries = collect_runs(args.runs)
    if not entries:
        print(f"未在 {args.runs} 下找到任何 gates.json")
        return 1
    if args.latest:
        entries = keep_latest(entries)
    html = build_html(entries, args.title)
    args.out.write_text(html, encoding="utf-8")
    n = len(entries)
    fails = sum(1 for e in entries if e["overall"] == "FAIL")
    print(f"papers={n} fail={fails} -> {args.out}（{len(html) // 1024} KB，离线单文件）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
