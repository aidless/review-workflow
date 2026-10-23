# 公式与算术核验报告（R1d）

- 论文：`F:\deepseek\papers\scievalsuite\paper\main.tex`
- 结论：**MINOR**（行内算术 1 处：不符 0（含括号百分数 0）；悬空引用 2）

覆盖边界：行内算术重算 + 括号百分数一致性 + 公式引用完整性；符号推导与量纲分析不在机械覆盖内（见 R6 文本层与人工审）。


## 悬空引用（\ref 指向不存在的 label）

- L158 `\ref{app:zinc}`
- L171 `\ref{app:zinc}`