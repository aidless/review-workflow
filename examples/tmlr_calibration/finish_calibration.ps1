# TMLR calibration finisher: wait for batch runs, incremental R3+R7 rerun, collect + report.
# Usage:  powershell -NoProfile -ExecutionPolicy Bypass -File finish_calibration.ps1
#         (run AFTER launching: run_review.py --batch ...\tmlr_calibration\configs)
# ASCII-only: PS 5.1 parses no-BOM UTF-8 .ps1 as GBK (Chinese breaks parsing).
param(
    [int]$TimeoutMin = 60
)
$ErrorActionPreference = "Stop"
$rf = "F:\deepseek\research-kit\review-workflow\examples\tmlr_calibration"
$scripts = "F:\deepseek\research-kit\review-workflow\scripts"
$papers = @("3i2ZRk8GDN", "cjU3YbcRr8", "e0pSqIqwXO", "JQA0EfQIfj", "Nm7dTogzfa", "TupiNRpgHw")

Write-Host "[wait] polling for all $($papers.Count) run_<paper>/gates.json"
$deadline = (Get-Date).AddMinutes($TimeoutMin)
while ((Get-Date) -lt $deadline) {
    $done = ($papers | Where-Object { Test-Path "$rf\runs\run_$($_)\gates.json" } | Measure-Object).Count
    if ($done -ge $papers.Count) { Write-Host "[wait] all $done papers done"; break }
    Start-Sleep -Seconds 30
}
if ((Get-Date) -ge $deadline) { Write-Host "[wait] TIMEOUT ${TimeoutMin}min, continuing with $done papers" }

Write-Host "[rerun] incremental R3+R7 (PDF noise filter + evidence-absent SKIP)"
foreach ($p in $papers) {
    if (-not (Test-Path "$rf\runs\run_$p\gates.json")) { Write-Host "=== $p SKIPPED (no gates.json) ==="; continue }
    Write-Host "=== $p ==="
    python "$scripts\run_review.py" --config "$rf\configs\$p.json" --stages R3,R7
}

Write-Host "[calibrate] backfill + analysis"
python "$scripts\calibrate.py" --collect "$rf\runs" --entries "$rf\tmlr_entries.json" --out "$rf\cal_results"

Write-Host "[done] final calibration report:"
Get-Content "$rf\cal_results\calibration_report.md"
