# 审稿标准流程（REVIEW_SOP）v2.2

> 目标：以 TMLR/顶会审稿人最高标准审阅一篇论文，输出**分级问题清单 + 评分 + 可执行的 Strong Accept 方案**。
> 纪律：先证据、后判断；每个 Critical 必须有可复现的核验命令；评分与方案绑定预算。
> v2.0：8 阶段 → 14 阶段（新增 R1b 引用核验 / R1c 新颖性对照 / R2c 图表核验 / R4 统计复算全自动 /
> R6b PRISM 四维 / R6c 辩论）；半自动 min 维度评分；PDF 输入模式；批处理仪表盘与人工评分校准。
> v2.1：新增 R1d 公式与算术核验 / R2d 表格数字核验；R6 多轮收敛断点续跑；辩论截断明示（MAX_ISSUES=20）；
> 校准人工 dump 降级路径；可移植性（requirements.txt + 路径自动发现 + --doctor）。
> v2.2：R3 无证据目录降级 SKIP（PDF-only/第三方论文评审——支撑率不可判 ≠ 数字不符）；
> R3 机械噪音新增 PDF 提取模式（章节号/交叉引用/arXiv ID/模型版本/连写列表）；
> 校准接入 TMLR 官方审稿数据集（OpenReview API v2 浏览器桥接抓取，替代人工凑分）。

## 一键执行（v2.2）

```powershell
# 配置模板 → 填写 tex/zip/evidence_dirs → 一键跑 R0-R7（16 阶段）
python scripts\run_review.py --init <config.json>
python scripts\run_review.py --config <config.json> [--skip-llm] [--diff <旧run目录>] [--converge 3] [--batch <configs目录>]
```

编排器自动串起全部机械阶段并落盘 `run_summary.md`（阶段表 + 门禁 + diff + 下一步命令）。
门禁：overall = 最差阶段（FAIL > WARN > SKIP > PASS）；证据层 FAIL → R7 评分 cap 4。
PDF-only 论文：config 提供 `"pdf"`（tex 置 null），R2/R2b/R1b/R1c/R2c 自动降级 SKIP；R3 在无 evidence_dirs 时同样降级 SKIP（v2.2，见 R3 节）。
增量运行（`--stages R6c` 之类子集）：R7 自动合并上一轮 gates.json——未重跑阶段保留旧门禁
并在阶段表标注"（上一轮，未重跑）"，overall/评分不会被子集覆盖式落盘虚假抬升
（v2.1 前曾发生：全量 R2=FAIL 后仅重跑 R6c,R7，overall 被覆盖成 PASS、评分抬到 8——已修 + selftest 回归防护）。

## 总原则（从 SciEvalSuite 审稿实践中提炼）

1. **论文声明 ≠ 事实**。凡是"论文说了 X"而 X 可机械核验（文件存在性、数字一致性、哈希、统计量、引用存在性），一律跑脚本核验，不凭信任。
2. **审稿人视角 = 证据审计 + 文本审查**。LLM 攻击（adversarial_review.py）负责文本层；文件级/数字级核验（audit/manifest/figure/number/stats/citation）负责证据层。两层都要跑。
3. **诚实性一票否决**：发现"论文声称 A、产物显示 B"（如模拟标注者被写成 double-annotator）时，该问题自动 Critical，且牵连全篇声明可信度评估。
4. **修改方案必须带预算核算**：每个 Tier 标注成本（写作小时 / GPU 调用数 / 人工标注量），且新调用总数不得突破论文声明的预注册预算（否则本身成为新的审稿问题）。
5. **LLM 单轮输出是噪声源**：文本层 Critical/Major 只计 WARN（不 FAIL）；`--converge N` 取轮间稳定问题；R6c 辩论机制把"哪些问题站得住"交给 rebuttal + 终裁的对抗过程。

## 流程总览（16 阶段）

```
R0 输入登记 → R1 论文静态审查 → R1b 引用核验(脚本) → R1c 新颖性断言(脚本,联网)
→ R1d 公式与算术核验(脚本) → R2 证据包审计(脚本) → R2b 清单哈希核验(脚本)
→ R2c 图表数字核验(脚本) → R2d 表格数字核验(脚本)
→ R3 数字对账(脚本+裁决闭环) → R4 统计复算(脚本,scipy) → R5 诚实性审查(脚本线索+人工)
→ R6 LLM 对抗审查(工具,可收敛,断点续跑) → R6b PRISM 四维(LLM) → R6c 审稿人-作者辩论(LLM)
→ R7 综合评分 + 报告 + Strong Accept 方案
```

- R0-R5 全自动（`run_review.py` 一键；R5 定性部分人工复核 suspicious 清单）
- R6/R6b/R6c：LLM 工具（RPC 探活失败自动 SKIP，不阻塞机械审查）
- R7：用 `templates/` 落盘；半自动评分见下

---

## R0 输入登记

**登记四元组**：

| 项 | 内容 | 示例 |
|---|---|---|
| 论文 | main.tex 路径 + main.pdf（页数） | `paper/main.tex`, 8 页 |
| 投稿包 | zip 路径 + 文件数 + 大小 | `submission_final_v6.zip`, 150 files |
| 产物目录 | results/ 与 out_*/ 的磁盘路径（可多个） | `results/`, `out_p5/` |
| 元数据 | 目标期刊/track、声明的预算、声明的清单哈希数 | TMLR、1000 calls、46-entry manifest |

**判据**：产物目录若与投稿包来源不同父目录，标记为**高风险**（打包遗漏概率高——SciEvalSuite C1 即此模式）。

## R1 论文静态审查

逐项核对（脚本给结构信号，人工读 tex 全文定性）：

- [ ] IMRaD 结构完整：Abstract / Intro / Related / Method / Setup / Results / Discussion / Limitations / Conclusion
- [ ] 期刊必需章节：TMLR 需 Broader Impact、OpenReview checklist 对齐项
- [ ] 缩写首次出现即定义（扫 ECE/TS/CLES/ITT/PCS 等高频缩写）
- [ ] 表格自包含（表注解释所有符号 †/×n）、图注不依赖正文
- [ ] Related Work 中每个对比方法有引用（无 `\citep` 的"家族"行是红旗）
- [ ] 摘要 ≤300 词且数字口径 = 正文最终口径（口径漂移记入 R5）

## R1b 引用核验（脚本：`citation_check.py`）

```powershell
python scripts\citation_check.py --tex <main.tex> --bib <refs.bib> [--online] --out <outdir>
```

- **offline 结构检查**（默认）：幽灵引用（tex 引用 bib 不存在的 key）/ 占位标题（TODO/placeholder/arXiv preprint 空标题）→ WARN
- **联网核验**（`--online` 或 config `citation_online: true`）：bib 条目 arXiv ID 是否存在 / DOI 是否可解析 / 标题相似度比对（防张冠李戴）→ ID 不存在 = FAIL

## R1c 新颖性断言对照（脚本：`novelty_check.py`）

```powershell
python scripts\novelty_check.py --tex <main.tex> --bib <refs.bib> --online --out <outdir>
```

- 抽取论文中 first/novel/we propose/据我们所知 等新颖性断言（含强断言标记）
- 联网检索 arXiv 先行工作（标题+摘要构造查询），与 bib 已引清单比对
- **未引用的近重复先行工作**（title_sim/abstract_sim 超阈值）= WARN：新颖性断言存疑，需人工对照
- offline / API 不可达 → SKIP（不误报）

## R1d 公式与算术核验（脚本：`formula_check.py`）

```powershell
python scripts\formula_check.py --tex <main.tex> --out <outdir>
```

论文推导正确性无法全自动验证（已知边界，与所有知名审稿工具一致），但正文里可机械核验的算术常有真实错误：

| 检查 | 审稿级别 | 说明 |
|---|---|---|
| 行内算术 `45/50 = 0.90`、`12 × 3 = 36`、`X% of Y = Z` | 不符 = **Major**（人工复核清单） | 按结果位数舍入容差重算；无空格减号（区间 3-5）豁免 |
| 括号百分数 `0.894 (89.4%)` | 不符 = **Major** | 单位漂移/手滑改数；只对 0-1 比例值生效——计数 + 百分数（如 `5 (20.6%)`）基数不在本句，跳过不误报 |
| 分数百分数 `35/170 (20.6%)` | 不符 = **Major** | 分子分母直接重算 |
| 指标记法 `Hit@5 (20.6%)` | 跳过 | `@` 后数值是指标参数，非数据 |
| 悬空公式引用 `\eqref{eq:ghost}` | Minor | 编译警告级 |

**不覆盖（诚实边界）**：符号推导、量纲分析、隐式步骤——留给 R6 文本层与人工。
实测校准：kg-retrieval 论文初版误报 `Hit@5 (20.6\%)`（真实算术 35/170=20.6% 正确）→ 引入 0-1 比例值约束后消除。

## R2 证据包审计（脚本：`audit_package.py`）

```powershell
python scripts\audit_package.py --zip <zip> --tex <main.tex> --out <outdir>
```

自动产出四类发现，映射到审稿分级：

| 脚本发现 | 审稿级别 | SciEvalSuite 实例 |
|---|---|---|
| 论文引用的产物文件不在 zip 内 | **Critical**（对可复现性立身的论文） | `out_p5/` 9 处引用全部缺失 |
| Windows 绝对路径泄漏（F:\ 等） | Major（匿名/规范违反） | `P5_MUSE_FINAL.json` 内 `F:\deepseek\_repo_survey\...` |
| 文件数/大小声明 vs zip 实际不符 | Major | "144 files" vs 实际 150 |
| 哈希清单覆盖数 vs 论文声明 | Major | 46-entry manifest 未覆盖 P5 产物 |

**人工追加**：打开 zip 内 evidence_manifest 类文件，抽查 3-5 个哈希条目对应的文件确实在包内。

## R2b 清单哈希核验（脚本：`verify_manifest.py`）

```powershell
python scripts\verify_manifest.py --zip <submission.zip> [--tex main.tex] --out <outdir>
```

| 脚本发现 | 审稿级别 |
|---|---|
| manifest 条目对应文件不在 zip 内 | **Critical**（清单造假/打包遗漏） |
| SHA-256 哈希不符（byte 级） | **Critical**（文件被改过或清单过期） |
| size 不符 | Major |
| 论文声明的 entry/hash 数 vs manifest 实际条数不符 | Major |

## R2c 图表数字核验（脚本：`figure_check.py`）

```powershell
python scripts\figure_check.py --tex <main.tex> --evidence-dirs <dir1,dir2> --out <outdir>
```

| 脚本发现 | 审稿级别 |
|---|---|
| `\includegraphics` 引用的图文件磁盘不存在 | **Critical**（编译即断） |
| 图注小数在图内文本/证据/正文中均无支撑 | Major（stale figure 信号，进 R3 同款裁决闭环） |
| 高精度值只出现在图内、正文与证据均无 | Minor（figure_only，人工抽查） |

矢量 PDF 图自动提取内嵌文本参与比对；位图跳过文本比对（无文本层）。

## R2d 表格数字核验（脚本：`table_check.py`）

```powershell
python scripts\table_check.py --tex <main.tex> --evidence-dirs <dir1,dir2> --out <outdir>
```

`\begin{table}` 内数字与产物的结构化比对（R2c 只覆盖 `\includegraphics`，表格此前只能靠 R3 兜底、无表格语义）：

| 脚本发现 | 审稿级别 |
|---|---|
| 表格 numeric cell 在证据/正文/图内文本中均无支撑 | Major（stale table 信号，进 R3 同款裁决闭环） |
| 表内 `\input{...}` 引用的文件不存在 | **Critical**（编译即断） |
| 同列混精度（小数位差 ≥2） | INFO（人工抽查：口径不一致信号） |

解析 tabular/tabularx/longtable 环境，处理 `\multicolumn`/`\multirow`/`\toprule` 等；表头行自动识别（首个含数值的行之前）。

## R3 数字对账（脚本：`number_reconcile.py`）

```powershell
python scripts\number_reconcile.py --tex <main.tex> --evidence-dirs <dir1,dir2> --out <outdir> `
    [--adjudications adjudications.json] [--llm-adjudicate --rpc http://127.0.0.1:3080]
```

两个方向：

1. **产物 → 论文**（验证论文没改数字）：从产物 JSON 提取统计数字，检查论文中是否出现一致值（容差 0.0005）。
2. **论文 → 产物**（验证论文数字有支撑）：论文中的 p 值/统计量/均值，能否在产物中找到来源；找不到的进**人工复核清单**。

**三层降噪裁决闭环**：机械噪音（版本号 x.y.z 片段 / 日期 / 结构命令花括号内数字 / PDF 提取噪音——独立章节标题行、Section X.Y 交叉引用、arXiv ID、Version X.Y 标注、连字符模型版本 MobileNetV2-0.5、无空格逗号连写 0.5,1.0）自动豁免；人工裁决持久化在 `adjudications.json`（verdict = noise | supported | critical | pending），重跑后清单只显示新增未裁决数字 → 单调收敛。

**R3 裁决自动化（v2.2，`--llm-adjudicate`）**：待复核 token 不再全部依赖人工——两层裁决：
- **机械层**（`mechanical_r3`，高置信规则）：证据直接/比例/2 位舍入容差匹配 → `supported`；明显噪音形态（表格列宽 `p{2.4cm}`、插图宽度 `width=0.98\linewidth`、模型版本 `qwen2.5:7b`、成本 `\yen1.87/h`、时间范围 `2--2.5h`）→ `noise`。刻意**不用**百分数/缩放 100 启发——实测对计数/时间/成本产生大量误报（0.87 误配 elapsed_s=86.97）。
- **LLM 对抗裁决层**：机械层未决的 token 交 LLM judge（对抗性 prompt，必须怀疑）裁决 `noise | supported | critical`，输出 JSON（verdict/confidence/justification/evidence/suggested_action）。
- **门禁合成**：critical ≥1 → CRITICAL；LLM 未裁决（超时/解析失败）→ 维持 recompute 原判 MAJOR（**不虚报 PASS**）；全部裁决且无 critical → PASS。RPC 不可达 → SKIP（不阻塞，门禁维持原判）。
- 裁决结果写 `r3_adjudications.json/md`，并回写 `adjudications.json`（token → verdict+note+layer），重跑自动收敛。

**无证据目录的语义（v2.2）**：PDF-only / 第三方论文评审（无 evidence_dirs）时方向 A/B 均无从对账——R3 门禁降级 **SKIP** 而非 FAIL（支撑率不可判 ≠ 数字不符；"投稿未附证据包"的 FAIL 职责在 R2/R2b 包审计），待复核清单照常落盘备查；人工裁决 critical 仍然一票 FAIL。带证据目录时判定不变（支撑率 <0.3 = CRITICAL）。

**人工复核清单处理**：逐条判定"有支撑 / 无支撑 / 需要跑 recompute 脚本"。出现无支撑数字 ≥1（裁决 critical）→ 直接 Critical。自动化后仅剩 LLM 未裁决或低置信条目需人工。

## R4 统计复算（脚本：`stats_recompute.py`，全自动）

```powershell
python scripts\stats_recompute.py --stats <stats.json> --tex <main.tex> [--evidence-dirs <dirs>] --out <outdir>
```

- 用 scipy 对产物 stats.json 里的关键检验**独立重算**：exact McNemar（b/d）、Friedman（chi2/df/p）、Wilson CI
- 重算值 vs 记录值 MISMATCH = **Critical（FAIL）**——数字不是跑出来的，或事后改过
- 记录值在论文中出现但不在任何产物里（NOT_IN_PAPER 反向）= Major
- 人工仍需复核（脚本不覆盖的部分）：检验选择是否恰当、退化情形诚实性、功效披露、多重比较、garden of forking paths

**R4 统计定性自动化（v2.2，run_review 集成，`r4_llm` 开关）**：NOT_IN_PAPER / MISMATCH 的定性不再全部依赖人工——两层裁决：
- **口径换算机械层**（`mechanical_caliber`）：阈值形式（p<0.05）、百分数（4.2%）、粗精度舍入（0.04）、n.s. 标记、显著性星号——给出低置信候选，标注"需 LLM 复核是否对应本统计量"。
- **LLM 对抗裁决层**（`adjudicate_qualitative`）：逐条复核机械候选并裁决 `口径换算 | 噪音 | 遗漏 | 疑似矛盾`，输出 JSON（verdict/confidence/justification/evidence/suggested_action）。
- **解析容错**（`parse_verdict` + `_repair_json_quotes`）：LLM 常在 justification 里用未转义 ASCII 双引号（如 `"simulated_k4_N12"`）破坏 JSON——状态机按 key/value 上下文把字符串值内的引号转义为 `\"` 后再 `json.loads`，仍失败才降级正则兜底；避免把有效裁决误判为 parse_failed。
- **门禁合成**：口径换算/噪音 → 已解释（不构成门禁）；遗漏/疑似矛盾 → 维持 recompute 原判 Major（文本层 WARN，不 FAIL）；MISMATCH 恒为机械 Critical。LLM 未裁决（超时/解析失败）→ 维持原判，**不虚报 PASS**。RPC 不可达 → SKIP（不阻塞机械审查）。
- 结果写 `stats_adjudications.json/md`；run_review 的 R4 metric 追加定性层结论（resolved/sustained/llm_failed）。

## R5 诚实性审查（脚本线索 + 人工定性）

```powershell
python scripts\honesty_scan.py --tex <main.tex> --evidence-dirs <dir1,dir2> --out <outdir>
```

机械前置：扫描产物 JSON/JSONL/MD 中 honesty hint（simulated/mock/synthetic/pending/TODO/FIXME/placeholder…），提取关联数值，与论文比对——数值出现在论文 + 论文讨论同概念 + 附近无披露词 → **suspicious**（人工定性入口）；全部数值另有干净产物来源 → 交叉佐证降级为 disclosed。

- [ ] **suspicious 逐条定性**（`honesty_scan.md`）："论文声称 A、产物显示 B"成立 → **Critical** 且牵连全篇声明可信度评估
- [ ] **摘要 vs 正文最终口径**：凡正文有 P5/补充实验更新而摘要未跟（gold 数、样本量、CI），记 Major（批量出现记 Critical）。
- [ ] **占位符残留**：TODO/TBD/FIXME/XXX/??? 扫描。
- [ ] **预算账本**：声明的调用总数 = 各层调用之和？模拟调用是否被计入真实预算？
- [ ] **声明-验证状态一致性**：论文说"X 已验证"时，产物里是否有验证记录（recompute checks、α 报告、双标 jsonl 行数）。

## R6 LLM 对抗审查（可收敛）

```powershell
python F:\deepseek\research-kit\adversarial_review.py --input <main.tex 或摘要+结果章节> --roles all --out <outdir>
```

7 角色（方法论/统计/实验/新颖性/可复现/写作/伦理）。注意其 MAX_CHARS=5000 截断——长论文分章节喂或只喂摘要+Intro+Results。

**轮间稳定性过滤**（`--converge N`，N≥2）：跑 N 轮，只保留 ≥2 轮重复出现的问题计入 R6 门禁——单轮生成噪声被过滤。文本层 Critical/Major 只计 WARN。
跨轮匹配用**模糊合并**（英文技术词元 Jaccard ≥0.50 + 词元贫乏时字符相似度 ≥0.62 兜底 + 传递性聚类）：LLM 复述措辞每轮漂移，规范化精确匹配会把全部问题误判为噪声（实测三轮各 ~20 Critical，精确匹配后 stable=0、门禁虚假 PASS；模糊合并后 stable Critical 18 / Major 20）。匹配刻意只锚定英文技术词（模型名/统计量/数字）——中文 bigram 会使 Jaccard 分母爆炸。
**断点续跑**：已完成的轮次（`llm/round_k/adversarial_review.json` 存在）自动复用不重跑——多轮收敛被中断（超时/机器负载）后重跑同一命令即可续传，已跑轮次不浪费。实测单轮 7 角色约 5-9 分钟。

## R6b PRISM 四维自评（LLM-as-judge：`prism_review.py`）

- **P 契合**（Pertinence：是否回答了声称的问题）/ **R 严谨**（Rigor：方法与统计是否站得住）/ **I 贡献**（Impact：增量是否显著）/ **S 诚实**（Sincerity：披露是否完整）
- 每维 1-10 分 + 短理由 + top weakness；总分 = min(四维)（短板纪律，不平均）
- 任一维 ≤6 → 文本层 WARN；RPC 不可达自动 SKIP
- 与 adversarial_review 的关系：R6 攻击具体缺陷，PRISM 给整体画像；两者互补，均不阻塞证据层门禁

## R6c 审稿人-作者辩论（LLM：`debate.py`）

单轮 LLM 审查的 Critical/Major 清单有噪声：有些问题作者一句话就能驳回（假阳性），有些被 rebuttal 后反而暴露更严重（真阳性增强）。三幕结构：

```
第 1 幕  作者   逐条回应：rebut（引用论文具体依据）或 concede（承诺修）
第 2 幕  审稿人 评估 rebuttal：sustain / withdraw / partial
第 3 幕  裁判   终裁：只统计 sustained 的问题；withdrawn 不计入门禁
```

输入：R6 输出（stable_issues）/ PRISM 输出（weaknesses）/ 手写 JSON 数组。缺裁保守维持（sustained）。
**截断明示**：R6 问题超过 20 条（MAX_ISSUES=20）时只取严重度前 20 条进辩论——有意的成本控制，但 report 与 metric 必须明示"原始 N 条中仅前 M 条参与辩论，截断 K 条未辩论"，不允许静默截断。截断标注行标记 `synthetic`：不进作者/裁判 prompt，不计入 sustained/withdrawn 统计（debate.md 表内单列"截断标注（不计入统计）"）。
**裁判语义（v2.1 修正）**：辩论针对投稿**当前版本**——作者 concede（承认+承诺修改）一律 **sustain**（真问题，待修订落地），只有 rebut 且引用论文现有内容、经裁判核对成立才 withdraw（误报）。初版裁判把作者的修改承诺误当"已解决"而撤回了 16/20 条（作者 LLM 用完成时态虚构"新增许可证表"）；修正后 concede 类问题回到 sustained，withdraw 只保留"论文已披露/引用成立"类。作者 prompt 同步要求 fix 用「将/会」表述（承诺，非完成动作）。
**实测验证（run_v3_converge，收敛后 38 条稳定问题截断至 20 条）**：修正语义下两轮实跑分别维持
Critical 10/2 Major 与 Critical 8/1 Major（LLM 非确定性，条数有 ±2 波动；撤回 4 条均为"论文已披露
n_d=0/power=0.0000/d_min=2.1279"类真误报，concede 类全部 sustain）——语义正确性稳定复现。

## R7 综合评分 + 报告 + Strong Accept 方案

**评分标尺（10 分制，与用户历史审稿对齐）**：

| 分 | 含义 |
|---|---|
| 1-3 | Reject：方法错误/证据真空/诚实性问题未披露 |
| 4-5 | Borderline：骨架对但有多个 Critical 或成片 Major |
| 6-7 | Accept：方法稳健、证据齐、诚实披露完整 |
| 8-9 | Strong Accept：+ 显著贡献 + 独立核验全绿 |
| 10 | Outstanding：领域定义级 |

**半自动评分（gates.json `suggested_score`，min 维度纪律）**：

```
结构(R1/R1b/R1c/R1d) / 证据(R2/R2b/R2c/R2d/R3/R4/R5) / 文本(R6/R6b/R6c)
各维度取最差阶段门禁映射分（PASS=8, WARN/SKIP=6, FAIL=4），总分 = min(三维度)
证据层 FAIL → 总分 cap 4；SKIP 阶段按 6 计（宁低勿高）
```

**人工评分校准**（`calibrate.py`）：收集若干篇已有 OpenReview 人工评分的论文跑本流程，比对 suggested_score 与人工分的 MAE / 排序一致性（Spearman），落盘 `openreview_prior.json` 作为前缀先验；终评仍由人工在 `templates/review_report.md` 打 1-10。
OpenReview API 403 时的降级路径：浏览器登录 openreview.net → 目标 venue → 导出/复制评审 JSON 存盘 → `--dump <该文件>` 重跑（示例：`runs/calibrate_smoke/`）。校准未完成前，suggested_score 只能当排序信号用，不能当绝对分用。

**TMLR 官方审稿数据校准（v2.2）**——用真实已接收论文替代人工凑分：

```powershell
# 1) 浏览器桥接抓取 TMLR dump（直连 API 403 被 Cloudflare 拦 TLS 指纹；85 篇含决议+评审投票）
#    Playwright 过验证后经 api2.openreview.net 抓取 → tmlr_dump.json
python scripts\calibrate.py --tmlr-dump examples\tmlr_calibration\tmlr_dump.json --n 6 --out examples\tmlr_calibration
# 2) 下载抽样论文 PDF → gen_configs.py 生成 PDF-only 配置 → 批处理跑全流程
python scripts\run_review.py --batch examples\tmlr_calibration\configs
# 3) 回填 suggested/gate/prism_min/prism_dims 并出校准报告
python scripts\calibrate.py --collect examples\tmlr_calibration\runs --entries examples\tmlr_calibration\tmlr_entries.json --out examples\tmlr_calibration\cal_results
```

TMLR 评审结构与常见 venue 不同：**无数值评分**，评审对 claims_and_evidence 投 Yes/No，AE 决议两级（Accept as is / Accept with minor revision）。
校准映射：h_decision（Accept as is=8 / Accept with minor revision=7）+ yes_rate（Yes 投票比例，连续排序信号）。
已知边界（报告内强制披露）：TMLR 拒稿不公开 → 只能标定 accept 侧；决议仅两级（7/8），绝对分 MAE 天然粗糙；
claims 投票针对投稿版（修订前），与终版 PDF 有版本差；PDF-only 模式下 suggested_score 的 min 维度评分区分度受限
（结构/证据维度多为 SKIP=6，suggested 塌缩为常数列），排序校准主要看 PRISM min/mean 与逐维度
（`--collect` 回填 prism_dims）；常数列不给 NaN 相关，如实报告"塌缩"。

**校准后评分的应用**（`--calibration <cal_results目录>`，或 config `calibration` 字段）：把上述校准实测
应用到任何一次运行的 R7——`gates.json` 新增 `calibrated_score` 与 `calibration` 块，`run_summary.md` 增
"校准后评分"段。规则（v2.2 实测驱动）：

```
无 FAIL 剖面：calibrated = min(8, suggested + bias)        # bias=+1.67，上限 8 = Accept-as-is 映射
有 FAIL 剖面：偏移不外推（校准样本 n=6 全 accept 无 FAIL 论文；cap 4 纪律不变）
问题数 null ：stable/sustained C/M 计数 vs yes_rate ρ≈0（n=6 实测）→ 文本维不因问题密度调幅
```

增量应用（收敛重跑场景，R6 缓存续跑 + R7 校准）：

```powershell
python scripts\run_review.py --config <config.json> --stages R6,R7 --converge 3 --calibration examples\tmlr_calibration\cal_results
```

**报告落盘**（`templates/review_report.md`）：
1. 总评分 + 一句话定位
2. 独立核验清单（本次实际执行的核验项与结果表）
3. Critical / Major / Minor 分级问题（每条附核验命令；R6c 撤回项单独列出并说明撤回理由）
4. Strong Accept 方案（`templates/strong_accept_plan.md`）：Tier 化（零成本写作修复 / 预算内补测 / 冲分项），每 Tier 标注成本与预期分数轨迹

**批处理可视化**（`dashboard.py`）：多篇 run 目录 → 单文件离线 HTML（门禁矩阵 / 总体分布 / 建议分条形 / 三维雷达 / PRISM 雷达），零外网依赖。

---

## 完成判据（Definition of Done）

一次审稿交付物齐全当且仅当：

- [ ] `run_summary.md` + `gates.json`（一键编排产物：阶段表 + 门禁 + suggested_score + 下一步命令）
- [ ] `audit_report.json/md`（R2）+ `verify_manifest.json/md`（R2b）+ `figure_check.json/md`（R2c）
      + `table_check.json/md`（R2d）+ `formula_check.json/md`（R1d）
- [ ] `number_reconcile.json/md`（R3）+ `honesty_scan.json/md`（R5 线索）+ `stats_recompute.json/md`（R4）
- [ ] R3 裁决文件 `adjudications.json` 无 pending（或已注明留待 recompute）
- [ ] R6b/R6c 报告（RPC 可达时）：PRISM 四维 + 辩论撤回清单
- [ ] 审稿报告 md（R7 模板填完，含核验清单表 + 人工终评分）
- [ ] Strong Accept 方案（Tier 化 + 预算核算表 + 分数轨迹）
- [ ] 所有 Critical 附可复现核验命令
- [ ] 若有修改建议，调用总数核算不突破论文声明的预注册预算
- [ ] 批量审稿时：`dashboard.py` 产物（HTML）随交付
