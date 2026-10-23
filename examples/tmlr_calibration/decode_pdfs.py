import base64
import json
from pathlib import Path

src = Path(r"C:\Users\Administrator")
root = Path(r"F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration")
dst = root / "pdfs"
dst.mkdir(parents=True, exist_ok=True)

es = json.loads((root / "tmlr_entries.json").read_text(encoding="utf-8"))
for e in es:
    p = src / f"tmlr_pdf_{e['paper']}.b64"
    data = base64.b64decode(p.read_text().strip())
    (dst / f"{e['paper']}.pdf").write_bytes(data)
    ok = data[:4] == b"%PDF"
    print(e["paper"], len(data), "PDF-ok" if ok else "BAD", (e["title"] or "")[:40])
