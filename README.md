# 审稿工作流（review-workflow）

> 版本 v2.2 · 2026-08-26 · 落地于 research-kit
> 源起：SciEvalSuite v6 审稿实践（2026-08-26），把人工核验流程固化为可复用工具。
> v1.1：清单哈希核验、诚实性扫描、数字裁决闭环、一键编排器（门禁/diff/批处理/RPC 探活）。
> v2.0：引用核验（R1b）、新颖性断言对照（R1c）、图表数字核验（R2c）、统计复算（R4 全自动）、
> PRISM 四维自评（R6b）、审稿人-作者辩论（R6c）、批处理仪表盘（dashboard）、OpenReview 校准（calibrate）、
> PDF 输入模式；14 阶段 R0-R7 一条命令。
> v2.1：公式与算术核验（R1d）、表格数字核验（R2d）、辩论截断明示（MAX_ISSUES=20）、
> 评分校准人工 dump 降级路径（OpenReview 403 时）、可移植性（requirements.txt + 路径自动发现 + --doctor）、
> --batch/--converge 3 真实论文实测；16 阶段 R0-R7 一条命令。
> v2.2：R3 无证据目录降级 SKIP（PDF-only/第三方论文评审）+ PDF 提取噪音六类过滤；
> 校准接入 TMLR 官方审稿数据集（85 篇浏览器桥接 dump，替代人工凑分）。

## 定位：与现有工具的关系

| 工具 | 层面 | 覆盖 |
|---|---|---|
| `adversarial_review.py`（已有） | 文本层 | 7 角色 LLM 攻击（方法论/统计/实验/新颖性/可复现/写作/伦理） |
| `review_loop.py`（已有） | 文本层 | 多轮审查-回应-再审收敛循环 |
| **`review-workflow/`（本目录）** | **证据层 + 结构层 + 编排** | **包审计、清单哈希、图表核验、数字对账（裁决闭环）、统计复算、诚实性扫描、引用/新颖性核验、PRISM、辩论、仪表盘** |

核心洞察：LLM 文本审查再强，也发现不了"论文引用了 `out_p5/P5_MUSE_FINAL.json` 但投稿包里根本没有这个文件"——这类问题只能靠**文件级/数字级机械核验**。本工作流补上这一层，并编排完整审稿流水线（v2.0 起文本层也纳入：PRISM 打分 + 辩论降噪）。

## 快速开始（推荐：一键编排）

```powershell
# 0. 换机器先自检（可选依赖缺失会明示，缺失自动降级 SKIP 不阻塞）
python scripts/run_review.py --doctor

# 1. 生成配置模板并填写
python scripts/run_review.py --init path/to/config.json

# 2. 一键跑 R0-R7（16 阶段：证据层全自动 + R6/R6b/R6c LLM，RPC 探活失败自动跳过）
python scripts/run_review.py --config path/to/config.json

# 常用变体
python scripts/run_review.py --config <config.json> --skip-llm           # 只跑机械阶段
python scripts/run_review.py --config <config.json> --stages R2,R3       # 只跑指定阶段
python scripts/run_review.py --config <config.json> --diff <旧run目录>    # 与上一轮对比
python scripts/run_review.py --config <config.json> --converge 3         # R6 跑 3 轮取稳定问题
python scripts/run_review.py --batch path/to/configs_dir                 # 批处理多篇

# 3. 批处理结果可视化（单文件离线 HTML + ECharts）
python scripts/dashboard.py --runs path/to/runs --out dashboard.html
```

**可移植性**：核心机械阶段零第三方依赖（Python ≥3.10 标准库）；`requirements.txt` 只列可选件
（scipy→R4、PyMuPDF→PDF 模式/R2c）。LLM 脚本路径自动发现：`REVIEW_LLM_SCRIPT` 环境变量 →
review-workflow 上级目录 → 历史盘符，无硬编码路径。

配置 schema（`--init` 模板同款）：

```json
{
  "name": "paper_x",
  "tex": "path/to/main.tex",            // 与 "pdf" 二选一
  "pdf": null,                           // PDF-only 审稿：提供后 tex 可为 null
  "zip": "F:/.../submission.zip",
  "evidence_dirs": ["F:/.../results"],
  "manifest": null,                      // 可选：zip 内 manifest 相对路径（默认自动发现）
  "adjudications": "F:/.../adj.json",    // 可选：R3 人工裁决持久化文件
  "bib": null,                           // 可选：R1b 显式指定 bib（默认从 tex 同目录发现）
  "citation_online": true,               // R1b 联网核验 arXiv/DOI（默认 false 仅结构检查）
  "novelty_online": false,               // R1c 联网检索 arXiv 先行工作对照新颖性断言
  "prism": true,                         // R6b PRISM 四维自评（LLM；默认开，RPC 不可达自动 SKIP）
  "debate": true,                        // R6c 审稿人-作者辩论（LLM；默认开）
  "converge": 1,                         // R6 轮数（≥2 时启用轮间稳定性过滤）
  "llm": {"enabled": true, "script": "/path/to/research-kit/adversarial_review.py",
           "rpc": "http://127.0.0.1:3080", "roles": "all"},
  "out": "F:/.../runs/name"
}
```

产出：`<out>/run_summary.md`（阶段表 + 门禁 + diff + 下一步）、`gates.json`（含 `suggested_score` 三维度 min 评分）、各阶段 JSON/MD 报告。
门禁纪律：overall = 最差阶段（FAIL > WARN > SKIP > PASS）；证据层 FAIL → 评分 cap 4。

**PDF 输入模式**：config 只提供 `"pdf"` 时自动提取文本为伪 tex 供 R1/R3/R4/R5/R6；R2/R2b/R1b/R1c/R2c 降级 SKIP（无源码无法审计包内一致性、bib 结构与图表引用）；R3 在无 evidence_dirs 时同样降级 SKIP（支撑率不可判 ≠ 数字不符，v2.2）。

## 阶段一览（16 阶段）

| 阶段 | 脚本 | 层 | 核验内容 | 关键发现 |
|---|---|---|---|---|
| R0 输入登记 | run_review 内置 | 机械 | 存在性/大小/sha256/跨源风险 | 产物目录在包目录树外 = 打包遗漏高风险 |
| R1 论文静态审查 | run_review 内置 | 结构 | 章节完整性/占位符/摘要词数/环境配对 | 缺 IMRaD 章节 = WARN |
| R1b 引用核验 | `citation_check.py` | 结构 | 幽灵引用/占位标题；`--online` 核验 arXiv/DOI 存在性 | ID 不存在 = FAIL |
| R1c 新颖性断言 | `novelty_check.py` | 结构 | first/novel/据我们所知 断言抽取；联网比对 arXiv 先行工作 | 未引用近重复 = WARN |
| R1d 公式与算术 | `formula_check.py` | 结构 | 行内算术重算（2+2=5 型手滑）、括号百分数一致性、悬空公式引用 | 算术不符 = WARN；符号推导/量纲是已知边界（R6+人工兜底） |
| R2 包审计 | `audit_package.py` | 证据 | tex 引用 vs zip 内容、路径泄漏、声明数、desync | 引用缺失 = FAIL(Critical) |
| R2b 清单哈希 | `verify_manifest.py` | 证据 | manifest 存在性/SHA-256/size/条目数 | 哈希不符 = FAIL(Critical) |
| R2c 图表数字 | `figure_check.py` | 证据 | 图文件缺失；图注小数支撑（图内文本/证据/正文）；figure_only 高精度值 | 缺图 = FAIL；图注无支撑 = WARN |
| R2d 表格数字 | `table_check.py` | 证据 | 表内 \input 存在性；numeric cell 三层支撑链（证据/表格外正文/无）；列内混精度 | \input 缺失 = FAIL（编译即断）；无支撑 cell = WARN |
| R3 数字对账 | `number_reconcile.py` | 证据 | 双向数字对账 + 三层降噪裁决闭环（含 PDF 提取噪音：章节号/交叉引用/arXiv ID/模型版本）；`--llm-adjudicate` 机械层（证据匹配/噪音形态）+ LLM 对抗裁决待复核 token | 裁决 critical = FAIL；待复核 = WARN；无证据目录 = SKIP（v2.2） |
| R4 统计复算 | `stats_recompute.py` | 证据 | McNemar/Friedman/Wilson 用 scipy 重算 vs 产物记录；NOT_IN_PAPER 定性自动化（口径换算机械层 + LLM 对抗裁决） | MISMATCH = FAIL(Critical) |
| R5 诚实性扫描 | `honesty_scan.py` | 证据 | 产物 hint（simulated/mock/TODO…）与论文披露比对、交叉佐证降级 | 未披露模拟 = FAIL（一票否决） |
| R6 LLM 对抗审查 | adversarial_review.py | 文本 | 7 角色攻击；`--converge N` 轮间稳定性过滤 | Critical/Major = WARN |
| R6b PRISM 四维 | `prism_review.py` | 文本 | P 契合/R 严谨/I 贡献/S 诚实（LLM-as-judge，min 纪律） | 任一维 ≤6 = WARN |
| R6c 辩论 | `debate.py` | 文本 | R6/PRISM 问题经作者 rebuttal + 裁判终裁，撤回假阳性；concede 一律 sustain（辩论针对当前版本，承诺≠已修）；仅严重度前 20 条进辩论（MAX_ISSUES=20，截断数在 metric/report 明示） | sustained Critical/Major = WARN |
| R7 综合报告 | run_review 内置 | — | run_summary.md + gates.json + suggested_score（min 维度） | — |

## 半自动评分（R7，min 维度纪律）

```
结构(R1/R1b/R1c/R1d) / 证据(R2/R2b/R2c/R2d/R3/R4/R5) / 文本(R6/R6b/R6c)
各维度取最差阶段门禁映射分（PASS=8, WARN/SKIP=6, FAIL=4），总分 = min(三维度)
证据层 FAIL → 总分 cap 4
```

校准：`calibrate.py` 把 suggested_score 与人工评分对齐（bias/MAE/排序一致性，n≥5 才给相关系数）。
OpenReview API 常返回 403：从 openreview.net 手动导出评审 JSON 后 `--dump <文件>` 传入
（降级路径内置）。校准日志 `calibrations.json` 每条 {paper, suggested, human, decision, gate}；
**n≥5 前只当排序信号用，不当绝对分用**。另配 `templates/review_report.md` 人工填 1-10 终评。
v2.2 起支持 **TMLR 官方审稿数据集校准**（替代人工凑分）：浏览器桥接抓取 85 篇已接收论文的
决议 + claims 投票（`--tmlr-dump` 分层抽样 → PDF-only 批处理 → `--collect` 回填），h_decision
映射 Accept as is=8 / Accept with minor revision=7，yes_rate 作连续排序信号；边界（拒稿不公开、
决议两级、PDF-only 区分度受限）在报告中强制披露（示例：`examples/tmlr_calibration/`）。

## 实战验证（SciEvalSuite v6，2026-08-26 实跑）

详见 `examples/scievalsuite_v6/SMOKE_TEST.md` 与 `examples/scievalsuite_v6/run_summary.md`：

- **overall=FAIL**（包确有 Critical）：R2 缺引用 24/58 + 路径泄漏 139 + desync；R2b 清单缺失 16/165；R3 待复核 94；R5 已披露 9（含 α=0.894 模拟标注者——论文已按此前审稿意见补充披露，扫描器正确放行）；R6 文本层 Critical 17 / Major 33（RPC 实跑）
- R0 跨源风险自动复现 C1 根因（`out_p5` 不在投稿包目录树下 → 打包遗漏高风险）
- UNC 转义误报修复后，泄漏数从 179 → 139（剔除 JSON 转义假阳性 40 处）
- 编排器 selftest 覆盖四轮：全 PASS → 注入缺失引用/缺图/统计造假后 FAIL+diff 恶化 → 裁决后 R3 收敛 → PDF 模式
- v2.0 全量冒烟（`examples/scievalsuite_v6/config_v2.json` → `run_v2/`）：R1c 联网新颖性 + R6b PRISM + R6c 辩论实跑，见 `run_v2/run_summary.md`

## 实战验证 v2.1（真实论文多轮收敛 + 多篇批处理，2026-08-26 实跑）

- **--batch 多篇批处理**（`examples/batch_multi/`）：3 篇**不同**论文（scievalsuite / kg-retrieval / selfevolve-agent）各带独立 zip+evidence 一键跑 16 阶段 → `batch_summary.md` + `dashboard.html`（1MB 离线单文件，门禁矩阵/分数/三维雷达）。结果有区分度：kg-retrieval R2b 缺失 5 + R3 待复核 31；selfevolve R2 缺引用 4/5 + R2b 哈希不符 3；scievalsuite 全套已知 Critical 复现（零回归）
- **--converge 3 多轮收敛**（`examples/scievalsuite_v6/run_v3_converge/`）：单轮 7 角色约 5-9 分钟；三轮实测 Critical=19/21/20、Major=45/42/38。轮间稳定性过滤（`r6_llm.json` stable vs unstable 分层）依赖**模糊合并**——首轮实测发现精确键匹配把 185 条全部误判为噪声（stable=0、门禁虚假 PASS），改用英文技术词元 Jaccard ≥0.50 + 传递性聚类后：**稳定 38 条（Critical 18 / Major 20，其中 15 条三轮全现），噪声候选 119 条**；模糊合并逻辑有单元回归用例（selftest 固化）
- **R1d 误报校准**：kg-retrieval 首跑误报 `Hit@5 (20.6\%)`（指标参数被当数值；真实算术 35/170=20.6% 正确）→ 引入 0-1 比例值约束 + `@` 排除后消除，selftest 固化该案例
- **R6 断点续跑**：多轮收敛被中断（机器负载/超时）后重跑同一命令，已完成轮次命中缓存跳过——单轮 9 分钟 × 3 轮的流程不再因单次中断全部作废
- **R6c 辩论语义实测**（同目录两轮实跑）：初版裁判把作者 LLM 虚构的"已完成修改"当真，16/20 条全部误撤回（维持 0）；prompt 修正（作者 fix 强制「将/会」未来时；concede 一律 sustain）后两轮实跑维持 Critical 10/2 Major 与 8/1 Major，撤回 4 条均为"论文已披露 n_d=0/power=0.0000"类真误报。连带修复：截断标注行（synthetic）不计入统计；**增量运行覆盖 bug**（`--stages` 子集曾把 gates.json 覆盖成只剩子集阶段 → overall 虚假 PASS/评分 8）→ R7 自动合并上一轮门禁 + selftest 回归防护

## 实战验证 v2.2（TMLR 官方审稿数据集校准，2026-08-26 实跑）

用 TMLR 真实已接收论文替代人工凑分，全流程 `examples/tmlr_calibration/`（dump 85 篇 → 分层抽样 6 篇 →
PDF-only 批处理 → 增量 R3+R7 → `--collect` 校准）：

- **排序一致性（核心结果，n=6）**：PRISM **R（严谨性）vs claims 投票 yes_rate：Spearman ρ=0.89（p=0.018）**；
  PRISM mean ρ=0.875（p=0.022）、PRISM min ρ=0.853（p=0.031）——均显著正相关。机制自洽：TMLR 评审投的是
  claims_and_evidence（论断是否有证据支撑），正对 PRISM 的 Rigor 维度
- **绝对分校准**：bias = +1.67（human − suggested），MAE = 1.67——6 篇已接收论文全部 suggested=6/WARN，
  min 维度评分在 accept 侧系统性保守（如实披露：PDF-only 模式下 suggested 塌缩为常数列，无排序区分度）
- **门禁-决策一致性 6/6 = 1.0**（WARN↔accept/weak_accept，无 FAIL 误报——R3 无证据目录降级 SKIP 修复后）
- **PDF 提取噪音过滤实测**：JQA0EfQIfj 1081 个小数 → 843 条机械噪音豁免（版本号/章节号/arXiv ID 等
  六类模式），待复核 238；R3 从旧代码的 FAIL（1081 待复核）降为 SKIP（无证据目录，支撑率不可判 ≠ 数字不符）
- **边界（报告强制披露）**：TMLR 拒稿不公开 → 仅标定 accept 侧；AE 决议两级（7/8）→ 绝对分 MAE 天然粗糙；
  claims 投票针对投稿版与终版 PDF 有版本差；PRISM P/I 维度 vs yes_rate 不显著（ρ=-0.26/-0.10，n=6 小样本）

## 校准后评分的应用（v2.2，`--calibration`）

校准产物不止于报告——`run_review.py --calibration <cal_results目录>`（或 config `calibration` 字段）把
TMLR 校准实测应用到任何一次运行的 R7 评分（`gates.json` 新增 `calibrated_score` + `calibration` 块，
`run_summary.md` 增"校准后评分"段）：

```powershell
python scripts\run_review.py --config <config.json> --stages R7 --calibration examples\tmlr_calibration\cal_results
```

- **偏移规则**：无 FAIL 剖面 → `calibrated = min(8, suggested + bias)`（bias=+1.67，上限 8=Accept-as-is 映射）；
  有 FAIL 剖面 → 偏移不外推（校准样本无 FAIL 论文，cap 4 纪律不变）
- **问题数 null 结果（关键实测，n=6）**：stable/sustained 的 Critical/Major 计数与 yes_rate 的 Spearman
  ρ=-0.03~+0.09（p>0.85）——**accept 侧问题密度是噪声**：文本维不因问题数进一步调幅，stable 问题清单维持
  WARN 语义；`--collect` 已把 stable_C/stable_M/sust_C/sust_M 回填进 calibrations.json，null 检验进报告
- **实测（scievalsuite_v6 收敛重跑）**：R6 三轮缓存命中复现（轮 82/83/76 → stable 38：C18/M20，模糊合并
  确定性可复现）；R7 校准后评分 4.0/10（FAIL 剖面，偏移不外推——38 条 stable issues 的边际贡献为零，
  评分由证据层 FAIL 决定）；样本内验证 6 篇 TMLR：bias +1.67→−0.03，MAE 1.67→0.43（披露：样本内算术验证，
  非泛化）

## R3/R4 定性自动化（v2.2，机械层 + LLM 对抗裁决）

把 R3 数字对账与 R4 统计定性的**人工定性步骤**自动化（用户需求：R4 统计定性不用人工）：

- **R3 `--llm-adjudicate`**：待复核 token 两层裁决——机械层（证据直接/比例/2 位舍入匹配 → supported；
  表格列宽/插图宽度/模型版本/成本/时间范围 → noise）→ 剩余交 LLM 对抗 judge 裁决 noise/supported/critical。
  门禁：critical ≥1 → CRITICAL；LLM 未裁决 → 维持原判 MAJOR（不虚报 PASS）；RPC 不可达 → SKIP。
  结果写 `r3_adjudications.json/md` 并回写 `adjudications.json` 自动收敛。
- **R4 定性自动化**（run_review 集成，`r4_llm` 开关）：NOT_IN_PAPER/MISMATCH 两层裁决——口径换算机械层
  （阈值 p<0.05/百分数/粗精度舍入/n.s./星号）→ LLM 对抗裁决（口径换算/噪音/遗漏/疑似矛盾）。
  口径换算/噪音 → 已解释（不构成门禁）；遗漏/疑似矛盾 → 维持原判 Major；MISMATCH 恒为机械 Critical。
  结果写 `stats_adjudications.json/md`。
- **实测（scievalsuite_v6）**：R4 定性 PASS（NOT_IN_PAPER 1 条 LLM 裁决为模拟内部量噪音，high 置信）；
  R3 机械层 25 个唯一待复核 token 先机械过滤 + LLM 逐条裁决（见 `run_v3_converge/r3_adjudications.md`）。
- **防虚报纪律**：LLM 超时/解析失败一律维持 recompute 原判（MAJOR），绝不因"定性层没跑完"而 PASS——
  与 R6c 辩论"concede 一律 sustain"同源的对抗纪律。

## 目录

```
review-workflow\
├── README.md                  # 本文件
├── REVIEW_SOP.md               # 16 阶段审稿标准流程（核心文档）
├── requirements.txt            # 可选依赖（scipy/PyMuPDF；核心零第三方依赖）
├── scripts\
│   ├── run_review.py           # 编排器：一键 R0-R7 + 门禁 + diff + 批处理 + 收敛 + PDF 模式
│   ├── audit_package.py        # R2  包审计
│   ├── verify_manifest.py      # R2b 清单哈希核验
│   ├── figure_check.py         # R2c 图表数字核验（PyMuPDF 提取矢量图内文本）
│   ├── table_check.py          # R2d 表格数字核验（tabular 解析 + cell 三层支撑链）
│   ├── formula_check.py        # R1d 公式与算术核验（行内算术/括号百分数/悬空引用）
│   ├── number_reconcile.py     # R3  数字对账 + 裁决闭环
│   ├── stats_recompute.py      # R4  统计复算（scipy）
│   ├── honesty_scan.py         # R5  诚实性扫描
│   ├── citation_check.py       # R1b 引用核验（offline 结构 + online arXiv/DOI）
│   ├── novelty_check.py        # R1c 新颖性断言对照（arXiv API）
│   ├── prism_review.py         # R6b PRISM 四维 LLM-as-judge
│   ├── debate.py               # R6c 审稿人-作者辩论（rebuttal → 终裁）
│   ├── dashboard.py            # 批处理离线 HTML 仪表盘（ECharts：门禁矩阵/分数/雷达）
│   ├── calibrate.py            # OpenReview 人工评分校准（含 --dump 降级路径）
│   └── pdf_text.py             # PDF → 伪 tex 提取（PDF 输入模式）
├── templates\
│   ├── review_report.md        # 审稿报告模板（含评分卡）
│   ├── strong_accept_plan.md   # Tier 化修改方案模板
│   └── echarts.min.js           # 仪表盘离线依赖（全量内嵌）
├── runs\                       # 各模块冒烟产物（novelty/prism/debate/calibrate）
└── examples\
    ├── scievalsuite_v6\        # 单篇实跑（config.json + config_v2.json + run_v2/ + run_v3_converge/）
    ├── batch_smoke\            # 同篇 offline/online 变体批处理冒烟
    └── batch_multi\            # 3 篇不同论文批处理实测（scievalsuite/kg-retrieval/selfevolve）+ dashboard.html
```

## 全部脚本 selftest

```powershell
python scripts\run_review.py --selftest       # 端到端四轮（PASS → FAIL+diff → 裁决收敛 → PDF 模式）
python scripts\audit_package.py --selftest
python scripts\verify_manifest.py --selftest
python scripts\figure_check.py --selftest
python scripts\table_check.py --selftest       # R2d（含 Hit@5 类误报回归用例）
python scripts\formula_check.py --selftest     # R1d（含指标记法/计数百分数误报回归用例）
python scripts\number_reconcile.py --selftest
python scripts\stats_recompute.py --selftest
python scripts\honesty_scan.py --selftest
python scripts\citation_check.py --selftest
python scripts\novelty_check.py --selftest
python scripts\prism_review.py --selftest
python scripts\debate.py --selftest
python scripts\dashboard.py --selftest
python scripts\calibrate.py --selftest
python scripts\pdf_text.py --selftest     # PDF 输入模式
```

全部 15 模块脚本 + 编排器 selftest 通过（2026-08-26 实测）。
