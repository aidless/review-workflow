import os
"""Convert Windows-path S5 configs to Linux paths for the round-2 rerun.

Chain 1: selfevolve-agent -> scievalsuite -> 10paradigm-os -> codeact-vs-fc
Chain 2: mem0 (fresh config) -> just-agent-60 -> kg-retrieval
"""
import json
from pathlib import Path

ROOT = Path(os.environ.get("QONE_PAPERS_DIR", "."))
OUT = ROOT / "research-kit/review-workflow/configs_linux"
OUT.mkdir(parents=True, exist_ok=True)

CHAIN1 = ["selfevolve-agent", "scievalsuite", "10paradigm-os", "codeact-vs-fc"]
CHAIN2 = ["mem0", "just-agent-60", "kg-retrieval"]


def fix(v):
    if isinstance(v, str):
        s = v.replace("F:/deepseek", str(ROOT)).replace("F:\\deepseek", str(ROOT))
        s = s.replace("\\", "/")
        if s.startswith("papers/") or s.startswith("research-kit/"):
            s = str(ROOT / s)
        return s
    if isinstance(v, list):
        return [fix(x) for x in v]
    if isinstance(v, dict):
        return {k: fix(x) for k, x in v.items()}
    return v


for name in CHAIN1 + CHAIN2:
    src = ROOT / f"papers/{name}/reviews/pipeline_S5/config.json"
    if src.exists():
        cfg = json.loads(src.read_text(encoding="utf-8"))
    else:
        template = json.loads(
            (ROOT / "papers/agent-comparison/reviews/pipeline_S5/config.json")
            .read_text(encoding="utf-8")
        )
        cfg = template
        cfg["name"] = name
        cfg["tex"] = f"papers/{name}/paper/main.tex"
        cfg["evidence_dirs"] = [
            f"papers/{name}/results", f"papers/{name}/evidence"
        ]
        cfg["out"] = f"papers/{name}/reviews/pipeline_S5"
    cfg = fix(cfg)
    dest = OUT / f"{name}.json"
    dest.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")
    print(name, "->", dest, "| tex:", cfg.get("tex"), "| out:", cfg.get("out"))
print("done")
