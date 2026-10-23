import re

with open(r'F:\deepseek\papers\scievalsuite\paper\main.tex', encoding='utf-8') as f:
    tex = f.read()

m = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S)
if not m:
    print('NO ABSTRACT FOUND')
    raise SystemExit(1)
text = m.group(1)
text = re.sub(r'\\(?:textbf|texttt|emph)\{([^}]*)\}', r'\1', text)
text = re.sub(r'\$[^$]*\$', ' ', text)
text = re.sub(r'\\(?:citep|ref|label)\{[^}]*\}', ' ', text)
text = re.sub(r'[{}]', ' ', text)
words = re.findall(r'[A-Za-z0-9][A-Za-z0-9\\.:/-]*', text)
print('abstract word count:', len(words))
