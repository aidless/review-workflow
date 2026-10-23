import json
from pathlib import Path

root = Path(r"F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration")
es = json.loads((root / "tmlr_entries.json").read_text(encoding="utf-8"))
cfgdir = root / "configs"
cfgdir.mkdir(parents=True, exist_ok=True)

for e in es:
    fid = e["paper"]
    cfg = {
        "name": f"tmlr_{fid}",
        "tex": None,
        "pdf": str(root / "pdfs" / f"{fid}.pdf"),
        "zip": None,
        "evidence_dirs": [],
        "manifest": None,
        "adjudications": None,
        "bib": None,
        "citation_online": False,
        "novelty_online": False,
        "prism": True,
        "debate": True,
        "converge": 1,
        "llm": {
            "enabled": True,
            "script": "F:\\deepseek\\research-kit\\adversarial_review.py",
            "rpc": "http://127.0.0.1:3080",
            "roles": "all",
        },
        "out": str(root / "runs" / f"run_{fid}"),
    }
    (cfgdir / f"{fid}.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    print("config ->", cfgdir / f"{fid}.json")
