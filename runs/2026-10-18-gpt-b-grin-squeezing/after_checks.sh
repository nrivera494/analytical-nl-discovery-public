#!/bin/bash
# gpt-b / gpt-6-astra / gpt. Invoke only after final_checks.sh has completed.
set -euo pipefail
cd ~/agent-work/ver-gpt-b
py=~/agent-work/venv/bin/python
run_step() {
  local line free
  while true; do
    line=$(memory_pressure | grep 'free percentage'); echo "$line"
    free=$(echo "$line" | sed -E 's/.*: ([0-9]+)%.*/\1/')
    if [ "$free" -ge 35 ]; then break; fi
    sleep 30
  done
  echo "START $(date -u '+%Y-%m-%dT%H:%M:%SZ') $*"
  "$py" evaluator/serial_numerical.py "$@"
  echo "DONE $(date -u '+%Y-%m-%dT%H:%M:%SZ') $*"
}
run_step "$py" -W ignore runs/2026-10-18-gpt-b-kerr-exact/no_go_smooth.py
run_step "$py" -W ignore runs/2026-10-18-gpt-b-kerr-exact/qmc_completion.py
run_step "$py" -W ignore runs/2026-10-18-gpt-b-grin-squeezing/count_resolution.py last
run_step "$py" -W ignore runs/2026-10-18-gpt-b-condensate-squeezing/final_resolution.py
run_step "$py" -W ignore runs/2026-10-18-gpt-b-grin-squeezing/refresh.py
run_step "$py" -W ignore runs/2026-10-18-gpt-b-grin-squeezing/analyse.py
run_step "$py" -W ignore runs/2026-10-18-gpt-b-condensate-squeezing/analyse.py
run_step "$py" -W ignore runs/2026-10-18-gpt-b-kerr-exact/analyse.py
