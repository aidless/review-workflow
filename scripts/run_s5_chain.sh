#!/bin/bash
# S5 round rerun chain runner (Linux migration).
# Usage: run_s5_chain.sh <note> <paper> [<paper>...]
# Runs run_review (all stages, RPC via shim 3081) then logs the round.
NOTE="$1"; shift
cd research-kit/review-workflow/scripts || exit 1
PY="research-kit/review-workflow/.venv-review/bin/python"
LOGDIR="research-kit/review-workflow/chain_logs"
mkdir -p "$LOGDIR"

ensure_shim() {
  if ! curl -s -m 3 -X POST http://127.0.0.1:3081/api/session.history -d '{}' 2>/dev/null | grep -q '"ok": true'; then
    echo "$(date -Iseconds) shim dead, restarting" >> "$LOGDIR/shim_watch.log"
    pkill -f opencode_shim.py 2>/dev/null; sleep 1
    nohup python3 research-kit/review-workflow/scripts/opencode_shim.py --port 3081 >> /tmp/shim_stdout.log 2>&1 &
    sleep 2
  fi
}

for PAPER in "$@"; do
  ensure_shim
  echo "=== $(date -Iseconds) START $PAPER ==="
  $PY run_review.py --config "research-kit/review-workflow/configs_linux/$PAPER.json" \
    >> "$LOGDIR/$PAPER.log" 2>&1
  rc=$?
  echo "=== $(date -Iseconds) run_review rc=$rc; logging round for $PAPER ==="
  ensure_shim
  $PY log_s5_round.py --out "papers/$PAPER/reviews/pipeline_S5" \
    --note "$NOTE" >> "$LOGDIR/$PAPER.log" 2>&1
  echo "=== $(date -Iseconds) DONE $PAPER ==="
done
