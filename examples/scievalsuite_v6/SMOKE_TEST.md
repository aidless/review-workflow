# 冒烟测试记录：SciEvalSuite v6（2026-08-26）

工作流实战：用 SciEvalSuite `submission_scievalsuite_final_v6.zip`（150 条目）+ 磁盘 `paper/main.tex` 验证。
v1.1 起为一键编排（`run_review.py --config config.json`），本目录即该次实跑产物。
v2.0 全量冒烟（14 阶段，含联网新颖性 + PRISM + 辩论）：`config_v2.json` → `run_v2/`。
v2.1 实测（16 阶段）：R6 三轮收敛 `config_v3_converge.json` → `run_v3_converge/`（断点续跑 +
跨轮模糊合并——初版精确匹配实测把全部 185 条误判为噪声，已修复并固化 selftest）；收敛后 R6c
辩论在同目录实跑两轮（裁判语义修正：concede 一律 sustain；38 条稳定问题截断至前 20 条，
截断标注 + 增量 gates 合并验证，见"实测三"）。多篇批处理见
`../batch_multi/`（3 篇不同论文 + dashboard）。

## 命令

```powershell
# v2.0 一键全流程（14 阶段：R0-R7c，novelty_online=true，LLM 三件套全开）
python F:\deepseek\research-kit\review-workflow\scripts\run_review.py `
    --config F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\config_v2.json `
    --diff F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6

# v1.1 一键全流程（R0-R7，含 R6 LLM 对抗审查）
python F:\deepseek\research-kit\review-workflow\scripts\run_review.py `
    --config F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6\config.json

# v1.0 时期单脚本方式（已被编排器取代，保留作独立调用参考）
python F:\deepseek\research-kit\review-workflow\scripts\audit_package.py `
    --zip F:\deepseek\papers\scievalsuite\submission\submission_scievalsuite_final_v6.zip `
    --tex F:\deepseek\papers\scievalsuite\paper\main.tex `
    --out F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6

python F:\deepseek\research-kit\review-workflow\scripts\number_reconcile.py `
    --tex F:\deepseek\papers\scievalsuite\paper\main.tex `
    --evidence-dirs "F:\deepseek\papers\scievalsuite\results,F:\deepseek\scievalsuite\out_p5" `
    --out F:\deepseek\research-kit\review-workflow\examples\scievalsuite_v6
```

## v2.0 全量冒烟结果（run_v2/，14 阶段全跑，2026-08-26）

overall = **FAIL**（预期正确）| 建议评分 **4/10**（min 维度：structure 6 / evidence 4 / text 6）

| 阶段 | 结论 | 门禁 | 关键指标 |
|---|---|---|---|
| R0 输入登记 | MAJOR | WARN | 跨源风险 1：`out_p5` 不在投稿包目录树下（同 v1.1） |
| R1 静态审查 | MAJOR | WARN | 摘要 358 词（>300） |
| R1b 引用核验 | PASS | PASS | 12 条目，幽灵引用 0（offline 结构检查） |
| R1c 新颖性断言 | PASS | PASS | 断言 1 句；**联网检索 arXiv 15 条，近重复 0**（真实 API 调用） |
| R2 包审计 | CRITICAL | **FAIL** | 缺引用 24/58；路径泄漏 139；tex desync=True（与 v1.1 完全一致，零回归） |
| R2b 清单哈希 | CRITICAL | **FAIL** | 清单 165 条：OK 149，缺失 16（同 v1.1） |
| R2c 图表数字 | PASS | PASS | 图 1 幅（矢量 PDF 文本提取成功）；图注小数 1 个全有支撑；figure_only 0 |
| R3 数字对账 | MAJOR | WARN | 待复核 94（同 v1.1） |
| R4 统计复算 | MAJOR | WARN | 6 条记录：MATCH 4 / MISMATCH 0 / NOT_IN_PAPER 1（scipy 重算无造假） |
| R5 诚实性 | MAJOR | WARN | hint 命中 113；可疑 0；已披露 9（同 v1.1） |
| R6 LLM 对抗 | MAJOR | WARN | 文本层 Critical 23 / Major 41 / Minor 19（RPC 实跑，单轮） |
| R6b PRISM 四维 | MAJOR | WARN | P6 / R5 / I5 / S9（min=5，短板=严谨性）→ 文本层 WARN |
| R6c 辩论 | MAJOR | WARN | 21 条进辩论：**维持 Critical 15**（撤回 0，部分成立 5）——R6 噪声经对抗过程过滤 |

v1.1 → v2.0 diff：全部机械指标零变化（24/139/16/94 精确复现），新增 5 个阶段无回归。
R6c 辩论把 R6 的 83 条 stable_issues 按严重度截断为 20 条上限进入辩论（成本控制），
作者 rebuttal + 裁判终裁后 15 条 Critical 维持、5 条部分成立——单轮 LLM 假阳性在辩论后显形。

## v2.1 实测一：多篇批处理（`../batch_multi/`，3 篇不同真实论文，2026-08-26）

```powershell
python ...\run_review.py --batch ...\examples\batch_multi --skip-llm
python ...\dashboard.py --runs ...\examples\batch_multi --out ...\batch_multi\dashboard.html
```

| 论文 | overall | 差异化发现（证明多篇能力非模板复用） |
|---|---|---|
| scievalsuite_v6 | FAIL | 全套已知 Critical 精确复现（24/139/16/94，零回归基准） |
| kg_retrieval | FAIL | R2b 清单缺失 5/69；R3 待复核 31；R2 路径泄漏 52 |
| selfevolve_agent | FAIL | R2 缺引用 4/5；R2b 哈希不符 3 + 缺失 6；R3 待复核 76 |

R1d/R2d 新阶段在三篇上的表现：scievalsuite R1d PASS（行内算术 1 处一致）+ R2d PASS（3 表 / 30 numeric cell 全支撑）；
kg-retrieval 首跑 R1d 误报 `Hit@5 (20.6\%)` → 修复（0-1 比例值约束 + `@` 排除 + `A/B (P%)` 分数检查）后 PASS；
selfevolve R1d/R2d PASS。dashboard.html 1MB 离线单文件渲染 3 论文 × 16 阶段门禁矩阵。

## v2.1 实测二：R6 三轮收敛（`run_v3_converge/`，断点续跑）

```powershell
python ...\run_review.py --config config_v3_converge.json --stages R6,R7 --converge 3
# 被中断（机器负载/超时）后重跑同一命令即可：已完成轮次命中缓存跳过
```

三轮实测（RPC HTTP 200，qwen2.5:7b 经会话管道逐角色串行）：

| 轮次 | Critical | Major | Minor | 耗时 |
|---|---|---|---|---|
| round 1 | 19 | 45 | 18 | ~9 min（实跑） |
| round 2 | 21 | 42 | 20 | ~7.5 min（实跑） |
| round 3 | 20 | 38 | 18 | ~8 min（实跑，断点续跑后） |

**合并结果**：稳定 38 条（Critical 18 / Major 20 / Minor 0；15 条三轮全现、23 条两轮出现），
噪声候选（单轮）119 条；R6 门禁 WARN（文本层 Critical/Major 只计 WARN 的纪律不变）。

**实测 bug 与修复（本轮最重要的发现）**：初版跨轮合并用规范化精确键匹配，
实测把 185 条问题**全部**判为"轮间不稳定"——stable=0 / R6 门禁虚假 PASS。
根因：LLM 复述措辞每轮重组（同一 McNemar 功效问题三轮三种句式），字符级/精确匹配必然落空。
修复：英文技术词元（模型名/统计量/数字，去停用词）Jaccard ≥0.50 + 词元贫乏(<3 词)时字符
相似度 ≥0.62 兜底 + alias 传递性聚类（A~B、B~C 但 A!~C 的链式漂移）。关键设计取舍：
**刻意不含中文 bigram**——实测加入后 Jaccard 分母爆炸（可匹配对从 143 → 2），英文技术词
是复述中唯一稳定锚点。模糊合并已固化进 `run_review.py --selftest` 单元用例。

实测教训：单轮 7 角色约 5-9 分钟（RPC 逐角色串行）；首次分离进程跑法在机器并发
重型负载（本地 LLM qwen2.5:7b + 训练脚本）下被静默杀死、round 1 半途崩溃无输出——
引入轮级断点续跑（`llm/round_k/adversarial_review.json` 存在即复用）后，中断代价从
"全部作废"降为"从断点续传"。另：旧会话遗留的孤儿进程会与新任务并行重跑同一轮并
双写输出目录——续跑前用进程列表确认无同名 `run_review.py`/`adversarial_review.py` 残留。

## v2.1 实测三：R6c 辩论（收敛清单进辩论 + 截断标注 + 裁判语义修正，2026-08-26）

```powershell
# 全量机械阶段 + R6 缓存续跑 + R6c 全新辩论（修正 prompt 后）
python ...\run_review.py --config config_v3_converge.json --stages R0,R1,R1b,R1c,R1d,R2,R2b,R2c,R2d,R3,R4,R5,R6,R6c
# 增量重跑 R6c（验证 gates 合并修复：overall 不被子集运行虚假抬升）
python ...\run_review.py --config config_v3_converge.json --stages R6c
```

收敛后 38 条稳定问题按严重度截断至前 20 条进辩论（MAX_ISSUES=20，截断 18 条在
metric/debate.md 明示）。两轮实跑结果：

| 轮次 | 维持 Critical | 维持 Major | 撤回 | 部分成立 |
|---|---|---|---|---|
| 修正语义第一跑 | 10 | 2 | 4 | 4 |
| 修正语义第二跑（增量） | 8 | 1 | 4 | 7 |

**裁判语义实测 bug 与修复（本轮最重要发现）**：初版辩论把 16/20 条全部撤回（维持 0）——
作者 LLM 用完成时态**虚构**"已新增许可证表"等未发生的修改，裁判把 concede（承诺修改）
误当"已解决"判 withdraw。修复：作者 prompt 强制 fix 用「将/会」未来时表述；裁判 prompt
明确"辩论针对当前版本，concede 一律 sustain，只有 rebut 且引用论文现有内容经核对成立才
withdraw"。修正后撤回的 4 条均为真误报（论文确实已披露 n_d=0<6 not-detectable /
power 0.0000 / d_min 2.1279 等统计局限），concede 类（P5 计数矛盾、46 vs 165 清单口径、
量化精度未报告、seed 缺失、COI 未声明等）全部 sustain——语义正确性两轮稳定复现。

**两个连带修复**：

1. **截断标注不计入统计**：占位行（"另有 18 条超出上限被截断"）曾按缺裁保守计成
   sustained Minor 1——标记 `synthetic` 后不进作者/裁判 prompt、不计入统计，debate.md
   表内单列"截断标注（不计入统计）"。
2. **增量运行覆盖 bug（真实事故）**：`--stages R6c,R7` 曾把 gates.json 覆盖成只剩
   R6c 一项——R2/R2b 的 FAIL 丢失，overall 虚假 PASS、评分抬到 8/10。修复：R7 自动
   合并上一轮 gates.json（未重跑阶段保留旧门禁，阶段表标注"（上一轮，未重跑）"），
   已固化进 `run_review.py --selftest` 回归防护（子集重跑 R5 后 overall 必须仍 FAIL）。

最终 `run_v3_converge/gates.json`：overall=**FAIL**，建议评分 **4/10**（structure 6 /
evidence 4 / text 6），全部机械指标零回归（24 缺引用 / 139 泄漏 / 16 清单缺失 / 94 待复核）。

## v2.2 实测四：TMLR 官方审稿数据集校准（`../tmlr_calibration/`，2026-08-26）

```powershell
# 1) 浏览器桥接抓 dump（直连 API 403 被 Cloudflare 拦 TLS 指纹；Playwright 过验证经 api2.openreview.net）
#    → tmlr_dump.json（85 篇：AE 决议 + claims_and_evidence Yes/No 投票 + PDF base64）
python ...\calibrate.py --tmlr-dump ...\tmlr_calibration\tmlr_dump.json --n 6 --out ...\tmlr_calibration
# 2) decode_pdfs.py 解码 PDF → gen_configs.py 生成 PDF-only 配置 → 批处理全流程（16 阶段）
python ...\run_review.py --batch ...\tmlr_calibration\configs
# 3) 新代码落地后增量重跑 R3+R7（PDF 噪音过滤 + 无证据目录降级 SKIP）
python ...\run_review.py --config ...\configs\<paper>.json --stages R3,R7
# 4) 回填 + 校准报告
python ...\calibrate.py --collect ...\tmlr_calibration\runs --entries ...\tmlr_calibration\tmlr_entries.json --out ...\tmlr_calibration\cal_results
```

分层抽样 6 篇（high yes_rate≥0.99 两篇 / mid 一篇 / low<0.5 两篇 + mid 一篇；决议两级混搭），
PDF-only 批处理全跑 + 增量 R3+R7 重跑后的最终校准结果（`cal_results/calibration_report.md`）：

| 论文 | 决议 | yes_rate | suggested | gate | PRISM P/R/I/S | h_decision |
|---|---|---|---|---|---|---|
| 3i2ZRk8GDN | Accept as is | 1.0 | 6 | WARN | 8/6/7/7 | 8 |
| e0pSqIqwXO | Accept as is | 1.0 | 6 | WARN | 8/7/6/8 | 8 |
| cjU3YbcRr8 | Accept w/ minor rev | 0.75 | 6 | WARN | 8/6/6/7 | 7 |
| Nm7dTogzfa | Accept as is | 0.667 | 6 | WARN | 7/6/7/7 | 8 |
| TupiNRpgHw | Accept as is | 0.333 | 6 | WARN | 8/5/6/7 | 8 |
| JQA0EfQIfj | Accept w/ minor rev | 0.333 | 6 | WARN | 9/5/7/6 | 7 |

- **bias = +1.67 / MAE = 1.67**：min 维度评分在 accept 侧系统性保守（6 篇全 suggested=6）
- **PRISM R vs yes_rate：ρ=0.89（p=0.018）**；mean ρ=0.875（p=0.022）；min ρ=0.853（p=0.031）——
  均显著；P（ρ=-0.26）/I（ρ=-0.10）不显著（n=6 小样本，如实报告）
- **门禁-决策一致性 6/6**：WARN↔accept/weak_accept，无 FAIL 误报
- suggested_score 塌缩为常数（6 篇全 6）——PDF-only 模式已知边界，报告如实披露而非给 NaN 相关

**实测 bug 与修复（本轮重要发现）**：PDF-only + 无证据目录时 R3 曾判 CRITICAL（支撑率 0 < 0.3 触发）——
但"无证据可对账"≠"数字不符"，全 accept 样本上这等于把 6 篇已接收论文全部 FAIL（证据层假阳性）。
修复：`evidence_absent` 时 R3 降级 SKIP（判决理由落盘），评分维度按 SKIP=6 计而非 cap 4。
连带修复：PDF 提取噪音六类过滤（arXiv ID/章节号/交叉引用/模型版本号/连写列表/版本标签）——
JQA0EfQIfj 1081 个小数中 843 条被机械豁免，待复核从 1081 降至 238。

**编码教训**：无 BOM 的 UTF-8 中文 PowerShell 脚本在 PS 5.1 下按 GBK 解析——多字节序列把
`"` 吞掉导致 ParserError（"Missing closing '}'"）；`.ps1` 一律纯 ASCII 或 UTF-8 with BOM。

## 实测五：校准后评分应用到收敛重跑（v2.2 `--calibration`，2026-08-26）

```powershell
# 收敛重跑（R6 三轮缓存命中 + R7 校准评分），cal_results 来自 TMLR 官方数据校准（实测四）
python ...\run_review.py --config config_v3_converge.json --stages R6,R7 --converge 3 `
  --calibration ...\tmlr_calibration\cal_results
```

- **收敛可复现性**：R6 三轮全部命中缓存（round_1/2/3 断点续跑），模糊合并确定性复现——
  轮次 82/83/76 条 → stable 38 条（Critical 18 / Major 20）+ unstable 119 条，与 v2.1 基线零漂移
- **校准后评分 4.0/10**（suggested=4 不变）：FAIL 剖面 → 偏移不外推（校准样本 n=6 全 accept 无 FAIL 论文，
  cap 4 纪律不变）；**38 条 stable issues 对评分的边际贡献为零**（问题数 null 实测：stable/sustained C/M
  vs yes_rate ρ=-0.03~+0.09，p>0.85——accept 侧问题密度是噪声，文本维维持 WARN=6 不因问题数调幅）
- gates.json 新增：`calibrated_score: 4.0`、`calibration` 块（bias/n/profile/rule/rank_signals/disclosure）；
  run_summary.md 新增"校准后评分"段（含 PRISM R ρ=0.89 唯一显著排序信号 + 四条边界披露）
- **样本内算术验证**（6 篇 TMLR 校准样本自身，`../tmlr_calibration/validate_apply.py`）：
  calibrated = min(8, 6+1.67) = 7.7 vs human 均值 7.67 → bias +1.67 → −0.03，MAE 1.67 → 0.43
  （披露：样本内验证偏移算术正确，非泛化证明）

## 实测六：R3/R4 定性自动化（机械层 + LLM 对抗裁决，2026-08-26）

用户需求：R4 统计定性不用人工。实现两层裁决（机械层 + LLM 对抗），R3/R4 的人工定性步骤自动化。

```powershell
# R3 裁决自动化：机械层 + LLM 语义裁决待复核 token，回写 adjudications_v3.json
python ...\number_reconcile.py --tex <main.tex> `
  --evidence-dirs <results,out_p5> --out run_v3_converge `
  --adjudications adjudications_v3.json --llm-adjudicate --rpc http://127.0.0.1:3080

# R4 定性自动化：run_review 集成（config 开 r4_llm，默认 true）
python ...\run_review.py --config config_v3_converge.json --stages R4
```

- **R4 定性 PASS**（`run_v3_converge/stats_adjudications.json`）：NOT_IN_PAPER 1 条
  （`simulated_k4_N12`，chi2=8.2 p=0.042 N=12）——口径换算机械层命中 3 候选（阈值 p<0.05 / 粗精度舍入 0.04 /
  显著性星号），LLM 对抗裁决为**噪音**（high 置信）：JSON 路径与 note 明确标注模拟值，论文实际 Friedman
  为 k=4 N=6 chi2=14.25 p=0.0026、k=3 N=6/16 chi2=6.0/2.0，三个机械候选均错配 → 模拟内部中间量无需报告
- **R3 裁决自动化**（`run_v3_converge/r3_adjudications.md`）：manual_review_list 62 行 / 25 个唯一 token——
  机械层先过滤（证据匹配/噪音形态），剩余 LLM 逐条对抗裁决（noise/supported/critical），结果回写
  adjudications_v3.json（token → verdict+note+layer），重跑自动收敛
- **防虚报纪律实测**：LLM 超时/解析失败 → 维持 recompute 原判 MAJOR（不虚报 PASS）；RPC 不可达 → SKIP
  （不阻塞机械审查）——selftest 固化（mock LLM 全链路 + 超时 + RPC 不可达三条路径）
- **机械层误报回归防护**：COST_RE 只匹配转义 `\$`/`¥€`/`\yen`（不误伤 LaTeX 数学 `$0.1418$`）；
  时间范围正则支持整数起始（2--2.5h）；缩放 100 启发禁用（0.87 不误配 elapsed_s=86.97）——selftest 固化

## v1.1 一键全流程结果（overall=FAIL —— 包确有 Critical，预期正确）

| 阶段 | 结论 | 门禁 | 关键指标 |
|---|---|---|---|
| R0 输入登记 | MAJOR | WARN | 跨源风险 1：`out_p5` 不在投稿包目录树下 → 打包遗漏高风险（自动复现 C1 根因） |
| R1 静态审查 | MAJOR | WARN | 章节 8/8；摘要 358 词（>300 上限） |
| R2 包审计 | CRITICAL | **FAIL** | 缺引用 24/58；路径泄漏 139；tex desync=True（zip 旧版 vs 磁盘修订版） |
| R2b 清单哈希 | CRITICAL | **FAIL** | 清单 165 条：OK 149，缺失 16（out_p5 产物列入清单但不在 zip 内） |
| R3 数字对账 | MAJOR | WARN | 待复核 94；机械噪音 5（版本号/日期自动豁免）；裁决 critical 0 |
| R5 诚实性 | MAJOR | WARN | hint 命中 113；可疑 0；已披露 9 |
| R6 LLM 对抗 | MAJOR | WARN | 文本层 Critical 17 / Major 33 / Minor 23（RPC 3080 实跑） |

## 与人工审稿对照

| 自动发现 | 人工审稿 |
|---|---|
| 24 个引用缺失（out_p5/* 9 处、统计脚本 analysis.py、run.json 等） | ✅ 复现人工 C1，并补充发现统计脚本本体缺失 |
| 139 处路径泄漏（UNC 转义误报修复后；v1.0 为 179） | ✅ 超出人工：包内 manifest 大面积 F:\ / C:\Administrator 泄漏 |
| desync=True + 清单缺失 16 | ✅ 新发现：zip 未重封，磁盘论文已按审稿意见修订 → 需重打包 v7 |
| R0 跨源风险（out_p5 异树） | ✅ 自动定位 C1 根因模式 |
| R5：α=0.894 模拟标注者 → disclosed | ✅ 正确放行：论文已修订补充 "simulated second annotator…real double-annotation pending" 披露 |
| R3 待复核 94 → 裁决闭环 | 人工复核清单从 99（v1.0）降至 94（5 个机械噪音自动豁免） |

## 结论

- 一键编排完整复现人工审稿的 C1/M5，并发现人工遗漏三项（包内 manifest 路径泄漏、封包-磁盘 desync、manifest 缺失 16）
- R6 通过 RPC 探活后实跑 7 角色对抗审查；RPC 不可达时自动跳过不阻塞证据层
- `honesty_scan` 对已披露的模拟标注者正确放行（论文按前轮审稿意见修订后），对未披露情形仍一票否决
- 编排器 selftest 四轮（全 PASS → 注入缺失引用/缺图/统计造假后 FAIL + diff 恶化 → 裁决后 R3 收敛 → PDF 模式）+ 15 模块脚本 selftest 全通过
- v2.0 六个新阶段（R1b/R1c/R2c/R6b/R6c 为新增，R4 由人工转全自动）全部实跑：引用/图表/统计机械核验零回归，联网新颖性检索、PRISM 四维、辩论降噪工作正常
