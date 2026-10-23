# 诚实性扫描报告（R5b）

- 论文：`F:\deepseek\papers\selfevolve-agent\paper\main.tex`；证据目录：`F:\deepseek\papers\selfevolve-agent\results`, `F:\deepseek\papers\selfevolve-agent\evidence`
- 结论：**MAJOR** —— 关键词命中 27，可疑（论文数值+无就近披露）0，已就近披露 0

## 可疑命中（论文引用了被标记产物的数值，需人工定性）

- 无

## 全部关键词命中（按文件）

### `F:\deepseek\papers\selfevolve-agent\results\run_records\20260818-210405-67220b4c.json`
- `exit_status` [pending] sealed_pending
### `F:\deepseek\papers\selfevolve-agent\results\runs\20260818-210405-67220b4c\run_record.json`
- `exit_status` [pending] sealed_pending
### `F:\deepseek\papers\selfevolve-agent\results\verified\bundle-20260818-selfevolve\run_record.json`
- `exit_status` [pending] sealed_pending
### `F:\deepseek\papers\selfevolve-agent\evidence\cloud\cloud_skills_library.json`
- `constraints` [pending] When buffer is full, drop oldest item before appending; return False if item was dropped, True if ad
### `F:\deepseek\papers\selfevolve-agent\evidence\cloud\estimate_core_k5.py`
- `L57` [simulated] # Simulate k=5 majority vs k=3: bootstrap resample reps
- `L65` [simulated] # Simulate k=5 by sampling with replacement from empirical per-task Bernoulli(p)
- `L81` [simulated] print(f"k={k} simulated majority resolved: mean {sum(sim)/len(sim):.1f} sd { (sum((x - sum(sim)/len(
### `F:\deepseek\papers\selfevolve-agent\evidence\cloud\full_T1.4_PREPARATION.md`
- `L52` [simulated] 2. Report **local bootstrap estimate for core k=5** (see §5) as a tighter CI illustration: resamplin
- `L53` [pending] 3. Mark full as **pending** in Limitations with quantitative tightening forecast (see §6 paragraph s
- `L113` [pending] > **Full probe pending (T1.4).** The 100-task core probe reported here used majority vote over k=3 r
- `L126` [pending] - [ ] If cloud remains unavailable before deadline: keep core as primary, add the pending sentence a
### `F:\deepseek\papers\selfevolve-agent\evidence\frozen\skills_library.json`
- `constraints` [pending] When buffer is full, drop oldest item before appending; return False if item was dropped, True if ad
### `F:\deepseek\papers\selfevolve-agent\evidence\harness\agent\ledger.py`
- `L32` [pending] # Re-read the last hash from disk before appending so concurrent
### `F:\deepseek\papers\selfevolve-agent\evidence\harness\agent\skills.py`
- `L45` [placeholder] # Amendment G: placeholder-insertion actions conflict with "skip failed items"
- `L46` [placeholder] # semantics (tool_04 harm: skills pushed the model to append None / placeholders).
- `L47` [placeholder] PLACEHOLDER_ACTION_PATTERNS = (
- `L49` [placeholder] "append a placeholder",
- `L51` [placeholder] "insert a placeholder",
- `L52` [placeholder] "add a placeholder",
- `L166` [placeholder] for pattern in PLACEHOLDER_ACTION_PATTERNS:
- `L170` [placeholder] f"placeholder-insertion pattern conflicts with skip semantics (amendment G): {pattern}",
### `F:\deepseek\papers\selfevolve-agent\evidence\preregistration\PREREGISTRATION_V1_AMENDMENT_G.md`
- `L7` [placeholder] - 新增 `PLACEHOLDER_ACTION_PATTERNS`（append none / placeholder / default 占位等 8 条）；
- `L9` [placeholder] "placeholder-insertion pattern conflicts with skip semantics (amendment G)"；
### `F:\deepseek\papers\selfevolve-agent\evidence\protocol.md`
- `L39` [pending] - 全文统一口径：base=77/100（云端 post-fix）、skills 与 resample 待 core 重跑确认（C10/C11 PENDING-EVIDENCE）。
### `F:\deepseek\papers\selfevolve-agent\evidence\raw_ledgers\state_round5\ledger.jsonl`
- `L39:event.payload.round5` [placeholder] None placeholder on exception (graceful-degradation skills over-applied), 1/3
- `L42:event.type` [placeholder] curator_placeholder_rule_applied
### `F:\deepseek\papers\selfevolve-agent\evidence\REVIEW.md`
- `L238` [mock] - **本地验证**（mock 端到端，无 LLM）：臂调度 9 次调用正确、3 个随机客户端 t=0.7/种子 1000-1002、主客户端 t=0/seed=42、噪声底与 McNemar 数值全