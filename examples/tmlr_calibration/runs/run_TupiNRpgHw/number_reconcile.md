# 数字对账报告（R3）

- 论文：`F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration\runs\run_TupiNRpgHw\extracted_text.txt`，证据目录：（无）
- 结论：**MAJOR**（裁决 critical 0，待复核 1295，机械噪音 202，已裁决 0）
- 无证据目录：是——方向 A/B 均无从对账，支撑率不可判（PDF-only/第三方论文评审）

## 方向 A：产物统计数字 → 论文出现（论文未改数字）

- 核心统计数字 0 个，其中 0 个在论文中找到一致值（命中率 None）

| json_path | 值 | 论文 token | 来源 |
|---|---|---|---|

## 方向 B：论文小数 → 产物支撑

- 论文小数 1497 个，有支撑 0 个（支撑率 0.0）
- 机械噪音 202 个（版本号片段/日期/结构行，自动豁免）
- 已裁决 0 个（人工 verdict：noise/supported/critical）

### 人工复核清单（未裁决且非噪音）

- L277 `4.1`：Assumption 4.1. There exists ϵ > 0 such that ∥Psrc(·|s, a) −Ptar(·|s, a)∥≤ϵ, ∀(s, a).
- L278 `4.2`：Assumption 4.2. The estimated inverse policy model ˆπinv well approximates the true empirical invers
- L282 `4.3`：Assumption 4.3. The reward function is bounded and is Lr-smooth, i.e., ∀(s, a), ∥∇ar(s, a)∥
- L285 `4.1`：Assumption 4.1 requires that the dynamics discrepancy between the source domain and the target domai
- L286 `4.2`：is bounded, and Assumption 4.2 assumes that the estimated inverse policy model well-fit the target d
- L287 `4.4`：Theorem 4.4 depicts the dynamics discrepancy between the corrected source domain dataset and the tar
- L289 `4.4`：Theorem 4.4. Denote the corrected source domain transition dynamics as ePsrc, then under Assumption 
- L289 `4.1`：Theorem 4.4. Denote the corrected source domain transition dynamics as ePsrc, then under Assumption 
- L290 `4.2`：and 4.2, the deviation between the corrected dynamics and the empirical target domain dynamics bPtar
- L295 `4.5`：Theorem 4.5. Given Assumption 4.3 and assume that the source domain rewards are corrected via
- L295 `4.3`：Theorem 4.5. Given Assumption 4.3 and assume that the source domain rewards are corrected via
- L314 `4.5`：Theorem 4.5 shows that the deviation of Q-values on c
- L322 `4.6`：the true target domain in Theorem 4.6.
- L323 `4.6`：Theorem 4.6 (Finite data bound). Denote f
- L328 `4.1`：2(1−γ)2 , C2 = |S × A × S|. Then under Assumption 4.1-4.3, for
- L328 `4.3`：2(1−γ)2 , C2 = |S × A × S|. Then under Assumption 4.1-4.3, for
- L491 `39.6`：39.6±3.3
- L491 `3.3`：39.6±3.3
- L492 `41.2`：41.2±3.9
- L492 `3.9`：41.2±3.9
- L493 `38.9`：38.9±4.0
- L493 `4.0`：38.9±4.0
- L494 `36.9`：36.9±4.5
- L494 `4.5`：36.9±4.5
- L495 `36.6`：36.6±5.5
- L495 `5.5`：36.6±5.5
- L496 `40.7`：40.7±7.7
- L496 `7.7`：40.7±7.7
- L497 `42.4`：42.4±5.3
- L497 `5.3`：42.4±5.3
- L500 `20.1`：20.1±5.0
- L500 `5.0`：20.1±5.0
- L501 `17.6`：17.6±6.2
- L501 `6.2`：17.6±6.2
- L502 `20.0`：20.0±4.9
- L502 `4.9`：20.0±4.9
- L503 `17.5`：17.5±5.2
- L503 `5.2`：17.5±5.2
- L504 `14.4`：14.4±2.2
- L504 `2.2`：14.4±2.2
- L505 `21.5`：21.5±6.5
- L505 `6.5`：21.5±6.5
- L506 `26.7`：26.7±2.2
- L506 `2.2`：26.7±2.2
- L509 `38.6`：38.6±6.0
- L509 `6.0`：38.6±6.0
- L510 `37.8`：37.8±3.3
- L510 `3.3`：37.8±3.3
- L511 `41.8`：41.8±5.1
- L511 `5.1`：41.8±5.1
- L512 `42.5`：42.5±2.3
- L512 `2.3`：42.5±2.3
- L513 `37.7`：37.7±7.3
- L513 `7.3`：37.7±7.3
- L514 `39.5`：39.5±3.5
- L514 `3.5`：39.5±3.5
- L515 `39.2`：39.2±4.2
- L515 `4.2`：39.2±4.2
- L518 `11.2`：11.2±1.1
- L518 `1.1`：11.2±1.1
- L519 `17.3`：17.3±3.8
- L519 `3.8`：17.3±3.8
- L520 `15.2`：15.2±3.3
- L520 `3.3`：15.2±3.3
- L521 `12.4`：12.4±1.0
- L521 `1.0`：12.4±1.0
- L522 `15.3`：15.3±3.5
- L522 `3.5`：15.3±3.5
- L523 `32.4`：32.4±8.0
- L523 `8.0`：32.4±8.0
- L524 `43.4`：43.4 ±6.1
- L524 `6.1`：43.4 ±6.1
- L527 `13.9`：13.9±2.9
- L527 `2.9`：13.9±2.9
- L528 `10.7`：10.7±4.3
- L528 `4.3`：10.7±4.3
- L529 `3.3`：3.3±1.9
- L529 `1.9`：3.3±1.9
- L530 `14.0`：14.0±2.6
- L530 `2.6`：14.0±2.6
- ……共 1295 个，见 JSON

### 机械噪音（自动豁免）

- `4.1`（section-heading）：4.1
- `4.2`（section-heading）：4.2
- `4.3`（section-heading）：4.3
- `4.4`（section-heading）：4.4
- `5.1`（section-heading）：5.1
- `677.6`（section-heading）：677.6
- `670.9`（section-heading）：670.9
- `549.8`（section-heading）：549.8
- `681.1`（section-heading）：681.1
- `660.8`（section-heading）：660.8
- `818.1`（section-heading）：818.1
- `1045.2`（section-heading）：1045.2
- `561.6`（section-heading）：561.6
- `580.2`（section-heading）：580.2
- `535.8`（section-heading）：535.8
- `556.1`（section-heading）：556.1
- `571.7`（section-heading）：571.7
- `723.3`（section-heading）：723.3
- `820.8`（section-heading）：820.8
- `5.2`（section-heading）：5.2
- `5.3`（section-heading）：5.3
- `5.4`（section-heading）：5.4
- `234.9`（section-heading）：234.9
- `243.9`（section-heading）：243.9
- `206.5`（section-heading）：206.5
- `242.3`（section-heading）：242.3
- `267.0`（section-heading）：267.0
- `312.4`（section-heading）：312.4
- `421.3`（section-heading）：421.3
- `0.0`（section-heading）：0.0
- `0.5`（section-heading）：0.5
- `1.0`（section-heading）：1.0
- `1.5`（section-heading）：1.5
- `2.0`（section-heading）：2.0
- `0.0`（section-heading）：0.0
- `0.5`（section-heading）：0.5
- `1.0`（section-heading）：1.0
- `1.5`（section-heading）：1.5
- `2.0`（section-heading）：2.0
- `2.5`（section-heading）：2.5
- ……共 202 个