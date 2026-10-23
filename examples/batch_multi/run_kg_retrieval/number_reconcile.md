# 数字对账报告（R3）

- 论文：`F:\deepseek\papers\kg-retrieval\paper\main.tex`，证据目录：`F:\deepseek\papers\kg-retrieval\results`, `F:\deepseek\papers\kg-retrieval\evidence`
- 结论：**CRITICAL**（裁决 critical 0，待复核 31，机械噪音 2，已裁决 0）

## 方向 A：产物统计数字 → 论文出现（论文未改数字）

- 核心统计数字 23 个，其中 5 个在论文中找到一致值（命中率 0.2174）

| json_path | 值 | 论文 token | 来源 |
|---|---|---|---|
| `w/o cross-encoder.p_mcnemar` | 0.25000000000000006 | `0.25` | `ablation_stats.json` |
| `w/o Graph.p_mcnemar` | 0.0004882812500000003 | `0.00048` | `ablation_stats.json` |
| `w/o Graph` | 1.0 | `1.0` | `true_ablation_v8.json` |
| `w/o Graph.p_wilcoxon` | 0.0005320055051392492 | `0.00048` | `ablation_stats.json` |
| `w/o RRF.p_wilcoxon` | 0.00010751117672950055 | `0.00048` | `ablation_stats.json` |

## 方向 B：论文小数 → 产物支撑

- 论文小数 42 个，有支撑 9 个（支撑率 0.2143）
- 机械噪音 2 个（版本号片段/日期/结构行，自动豁免）
- 已裁决 0 个（人工 verdict：noise/supported/critical）

### 人工复核清单（未裁决且非噪音）

- L13 `20.6`：We present a self-evolving knowledge graph retrieval system that unifies document ingestion, entity-
- L13 `0.007`：We present a self-evolving knowledge graph retrieval system that unifies document ingestion, entity-
- L13 `1.5`：We present a self-evolving knowledge graph retrieval system that unifies document ingestion, entity-
- L13 `0.12`：We present a self-evolving knowledge graph retrieval system that unifies document ingestion, entity-
- L13 `0.05`：We present a self-evolving knowledge graph retrieval system that unifies document ingestion, entity-
- L22 `58.02`：We build on Microsoft GraphRAG (community), LightRAG v1.2.5, HippoRAG2, and Agent Memory (MemoraX 58
- L25 `0.88`：\textbf{KG construction}: Rule/LLM extractor, NetworkX, linker threshold 0.88. \textbf{Embedding}: B
- L25 `0.5`：\textbf{KG construction}: Rule/LLM extractor, NetworkX, linker threshold 0.88. \textbf{Embedding}: B
- L25 `0.3`：\textbf{KG construction}: Rule/LLM extractor, NetworkX, linker threshold 0.88. \textbf{Embedding}: B
- L25 `0.2`：\textbf{KG construction}: Rule/LLM extractor, NetworkX, linker threshold 0.88. \textbf{Embedding}: B
- L42 `34.2`：Full Hybrid & 34.2\textpm1.0 & --- & --- \\
- L43 `23.6`：w/o Graph & 23.6\textpm1.5 & +10.6 & 0.00048* \\
- L43 `1.5`：w/o Graph & 23.6\textpm1.5 & +10.6 & 0.00048* \\
- L43 `10.6`：w/o Graph & 23.6\textpm1.5 & +10.6 & 0.00048* \\
- L44 `0.6`：w/o RRF & 20.0\textpm0.6 & +14.2 & 0.00006* \\
- L44 `14.2`：w/o RRF & 20.0\textpm0.6 & +14.2 & 0.00006* \\
- L45 `25.8`：w/o BM25 & 25.8\textpm1.6 & +8.4 & 0.007* \\
- L45 `1.6`：w/o BM25 & 25.8\textpm1.6 & +8.4 & 0.007* \\
- L45 `8.4`：w/o BM25 & 25.8\textpm1.6 & +8.4 & 0.007* \\
- L45 `0.007`：w/o BM25 & 25.8\textpm1.6 & +8.4 & 0.007* \\
- L46 `1.4`：w/o Community & 27.0\textpm1.4 & +7.2 & 0.007* \\
- L46 `7.2`：w/o Community & 27.0\textpm1.4 & +7.2 & 0.007* \\
- L46 `0.007`：w/o Community & 27.0\textpm1.4 & +7.2 & 0.007* \\
- L47 `32.6`：w/o cross-encoder & 32.6\textpm1.0 & +1.6 & 0.25 \\
- L47 `1.6`：w/o cross-encoder & 32.6\textpm1.0 & +1.6 & 0.25 \\
- L54 `0.8`：\includegraphics[width=0.8\linewidth]{fig_ece.png}
- L55 `0.12`：\caption{ECE 0.12$\to$0.05 over G091-G1334 (1261 points).}
- L55 `0.05`：\caption{ECE 0.12$\to$0.05 over G091-G1334 (1261 points).}
- L59 `0.60`：Community and cross-encoder are discussed as NDCG gains ($0.60\to0.67$, $p=4e-10$, Fig.~\ref{fig:ece
- L59 `0.67`：Community and cross-encoder are discussed as NDCG gains ($0.60\to0.67$, $p=4e-10$, Fig.~\ref{fig:ece
- L68 `0.05`：Hybrid + community + self-evolution (Ornith 1-file-6-fix, $p<0.05$) yields discriminative 5-60\% evo

### 机械噪音（自动豁免）

- `1.2`（version-fragment）：We build on Microsoft GraphRAG (community), LightRAG v1.2.5, HippoRAG2, and Agent Memory (MemoraX 58
- `3.12`（version-fragment）：v8 170 tasks (I10 II12 III148), TopK=5 strict Hit@5 + NDCG, 5 seeds, Holm $m=5$, Python 3.12.7, seed