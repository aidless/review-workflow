# --- acceptance_backfill (EVAL_ACCEPTANCE_STANDARD.md P4) ---
# 证据来源: checks.yml
# 命令逐字取自该来源，未增删任何参数。
# 归一: python → python3（本机无 python 别名，实测 Error 127）
.PHONY: eval check

# Offline: planted-defect rerun, README/version/calibration drift, non-vacuous R4 selftest.
# Needs Python >=3.10 and scipy (R4). PyMuPDF is optional; without it the PDF section of
# --selftest SKIPs. No network.
check:
	python3 scripts/make_check.py

eval:
	python3 scripts/run_review.py --selftest
