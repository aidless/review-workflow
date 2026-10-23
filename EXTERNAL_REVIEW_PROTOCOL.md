# EXTERNAL_REVIEW_PROTOCOL — 外部评审闭环（S7 前置硬门）

> 制定：2026-09-05 流水线评测轮。背景：calibration-self-improvement 的双模型终评
> 实测暴露——本地 judge（qwen2.5:7b / deepseek-r1:7b）系统性偏松（均值 4.175 vs
> 3 位独立评审员一致分 2.95），且换 prompt 后 4.17→3.82 漂移（UNSTABLE）。
> **写作者与审稿者同属一个生态时，任何"内部 Accept"都不构成发表依据。**

## 硬性规则

1. **S7（封包）前必须完成 ≥1 次外部评审**，机器门 `check_external_review.py` 未过不得封包。
2. 合格的外部评审人，满足其一：
   - **真人**：非本项目作者与合作者（知情且自愿，可匿名化处理其身份）；
   - **异源模型**：训练谱系独立于本地模型家族（qwen/deepseek/llama/mistral/gemma/phi
     系 + 本地 ollama/RPC 均不合格）的前沿云模型，通过其官方 API 调用，`id` 记录
     模型名 + API 来源 + 调用日期。
3. 评审输入至少包含：投稿 PDF（或 main.tex）+ evidence_manifest 入口；允许评审人
   追问证据，**禁止单轮 5 分钟式走过场**——真人评审须留对话记录，模型评审须留完整
   transcript。
4. **transcript 必须落盘**在 `papers/<paper>/external_review/`，record.json 逐文件
   记 sha256（脚本校验）。禁止"评审说很好"式的口头结论而无原文。
5. 外部评审发现的 Critical/Major 进入 S6 返修循环正常处置，**不得因"外部"而降权**。
6. 评审人独立性声明（independence 字段）必填：与本文作者、本工作区的关系说明。

## 建议的异源模型评审提示词框架

```
你是 TMLR 审稿人。请评审附带的论文。
要求：批评必须引用论文中的具体声明/数字/章节；每条意见标注 Critical/Major/Minor/Nit；
不确定的事明确说不确定；不要因为文章"看起来完整"而放行——检查数字是否自洽、
声称是否有证据支撑、统计口径是否统一。最后按 TMLR 四维打分
（证据/兴趣/清晰 1-10，min 纪律）并给出 accept/reject 倾向。
```

## 配套：M5 judge 校准缺口（gold set）

本协议解决"评审独立性"，不解决"本地 judge 校准"。后者见
`research-kit/judge-calibration/M5_GOLDSET_PLAN.md`（用 TMLR OpenReview 公开
评审记录构建 gold set，校准本地 judge 的 FNR/FPR）。两条线互补，都做。

## 机器门用法

```bash
python research-kit/review-workflow/scripts/check_external_review.py <paper_dir>
# 已接入 papers/<paper>/gates_config.json 的 expected_fail 检查：
# 完成外部评审后，把该检查的 expected_fail 删掉（此时它应真实 PASS）
```
