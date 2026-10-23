# -*- coding: utf-8 -*-
"""构建 R3 裁决文件 adjudications_v3.json：机械层 10 个 + 语义层 17 个（RPC 不可达时的 LLM 兜底裁决）。

语义裁决依据（全部经证据文件核对）：
- noise: 版本号/成本/时间范围/派生参数（qwen2.5、llama3.1、muse-spark-1.2、ARS v3.11、Python 3.12、
  ¥1.87/h、$0.007、$0.64、2--2.5h、power 0.4600 派生参数）
- supported: 实质断言且有来源（0.355 ITT 均值可复算、0.42 CI 下界 p3_effects.json、2.3333 均值差
  P5_MUSE_FINAL.json、0.27 舍入 L2_gemma2_9b.json、0.87 CROSS_LAYER_ANALYSIS.md、0.2400 舍入
  L2_qwen2.5_14b.json invalid_rate=0.237）
- critical: 实质断言但无来源（5.2/0.074 = fail=NaN 敏感性分析 chi2/p，无脚本无 JSON）
"""
import json, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, r'F:/deepseek/research-kit')
sys.path.insert(0, r'F:/deepseek/research-kit/review-workflow/scripts')
import number_reconcile as nr

REPORT = Path(r'F:/deepseek/research-kit/review-workflow/examples/scievalsuite_v6/run_v3_converge/number_reconcile.json')
OUT = Path(r'F:/deepseek/research-kit/review-workflow/examples/scievalsuite_v6/adjudications_v3.json')

report = json.load(open(REPORT, encoding='utf-8'))
st = report.get('adjudications_state', {})
evidence = report.get('_evidence', [])
evidence_nums = []
for it in evidence:
    if isinstance(it, dict) and 'value' in it:
        src = it.get('source', '?')
        path = it.get('json_path', '?')
        evidence_nums.append((src + ':' + path, it['value']))

# 语义层裁决（RPC 不可达 → 主 LLM 兜底，人工核对证据后落盘）
SEMANTIC = {
    '2.5':     ('noise',     '时间范围 2--2.5h 及模型版本 qwen2.5:7b，非实质断言', 'L164 GPU time ~2--2.5h at ¥1.87/h', 'high'),
    '0.355':   ('supported', 'TextSimilarity ITT 均值可复算：(0+0.533048+0.533048)/3=0.3554≈0.355（t1 exec-fail 计 0）', 'A1_l1a_gemma2_9b_t3b_console.log [0.533,0.533] + t1=exec-fail', 'high'),
    '1.2':     ('noise',     '模型版本 muse-spark-1.2-contributor，非实质断言', 'L169 muse-spark-1.2-contributor (opencode)', 'high'),
    '3.1':     ('noise',     '模型版本 llama3.1:8b 中的 3.1，非实质断言', 'L79 L1b text-judge was llama3.1:8b', 'high'),
    '3.11':    ('noise',     'ARS v3.11 版本号，非实质断言', 'L79 ARS v3.11: FNR<0.15 and FPR<0.10', 'high'),
    '0.007':   ('noise',     '成本 $0.007 per task，非实质断言', 'L164 $0.007 per task vs API baseline $0.04', 'high'),
    '1.87':    ('noise',     '成本 ¥1.87/h，非实质断言', 'L164 GPU time ~2--2.5h at ¥1.87/h', 'high'),
    '0.4600':  ('noise',     '派生功率参数（N=16,d=0.5 的 paired t power），披露性计算非结果断言', 'L89 paired t with N=16 tasks achieves power 0.4600 for d=0.5', 'medium'),
    '3.12':    ('noise',     'Python 3.12 版本号，非实质断言', 'L91 Environment: Python 3.12', 'high'),
    '0.42':    ('supported', 'CI 下界幅值：p3_effects.json 7b→gemma ci95_approx[0]=-0.4221（符号翻转匹配）', 'L126 95% CIs approximately ±0.42--0.69', 'medium'),
    '2.3333':  ('supported', '均值差：P5_MUSE_FINAL.json mean_ranks 3.3333-1.0=2.3333（muse vs 7b）', 'L158 muse vs. 7b diff 2.3333 > CD', 'medium'),
    '0.64':    ('noise',     '成本 ~$0.64 total，非实质断言', 'L164 ~$0.64 total at ¥1.87/h', 'high'),
    '0.074':   ('critical',  'fail=NaN 敏感性 p 值无来源：无脚本/JSON 复现（仅附录报告值），实质统计断言无支撑', 'L227 fail=NaN (exclude) → chi2=5.2 p=0.074', 'medium'),
    '0.27':    ('supported', 'L2 goal 0.275 舍入：L2_gemma2_9b.json goal_rate=0.275', 'L175 L2 0.14→0.27', 'medium'),
    '0.87':    ('supported', '跨层 Spearman ρ=0.87：out_p5/CROSS_LAYER_ANALYSIS.md 原文', 'L175 shows ρ=0.87 trend (n=3)', 'medium'),
    '0.2400':  ('supported', 'invalid rate 上界：L2_qwen2.5_14b.json invalid_rate=0.237→0.24（2 位舍入）', 'L182 invalid rates 0.0000--0.2400', 'medium'),
    '5.2':     ('critical',  'fail=NaN 敏感性 chi2 无来源：无脚本/JSON 复现（仅附录报告值），实质统计断言无支撑', 'L227 fail=NaN (exclude) → chi2=5.2 p=0.074', 'medium'),
}

merged = {}
mech_count = 0
sem_count = 0
crit_count = 0

for token, entry in st.items():
    ctxs = [entry.get('context', '')]
    mech_verdict, mech_note = nr.mechanical_r3(token, ctxs, evidence_nums)
    if mech_verdict:
        merged[token] = {
            'verdict': mech_verdict,
            'note': mech_note[:200],
            'context': ctxs[0][:120],
            'layer': 'mechanical',
        }
        mech_count += 1
    elif token in SEMANTIC:
        v, note, ev, conf = SEMANTIC[token]
        merged[token] = {
            'verdict': v,
            'note': note[:200],
            'context': ev[:120],
            'layer': 'semantic',
            'confidence': conf,
        }
        sem_count += 1
        if v == 'critical':
            crit_count += 1
    else:
        merged[token] = {'verdict': 'pending', 'note': '', 'context': ctxs[0][:120], 'layer': 'unknown'}

state = {
    '_meta': {
        'usage': 'verdict: noise=误报(版本/日期/派生/维度) | supported=人工确认有来源 | critical=真实无支撑 → 一票 Critical | pending=待判',
        'updated': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'pending': sum(1 for v in merged.values() if isinstance(v, dict) and v.get('verdict') == 'pending'),
        'mechanical': mech_count,
        'semantic': sem_count,
        'critical': crit_count,
        'note': 'RPC 不可达（session.create/list 超时）→ 17 个语义 token 由主 LLM 兜底裁决（证据核对后落盘）；RPC 恢复后可重跑 LLM 层复核',
    },
    **merged,
}

OUT.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
print('written:', OUT)
print('mechanical=%d semantic=%d critical=%d pending=%d' % (
    mech_count, sem_count, crit_count,
    sum(1 for v in merged.values() if isinstance(v, dict) and v.get('verdict') == 'pending')))
for t, v in merged.items():
    print('  %-10s %-10s %s' % (repr(t), v.get('verdict'), v.get('note', '')[:60]))
