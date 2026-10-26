#!/bin/bash
# gpt-b / gpt-6-astra / gpt. Launch only after serial_checks.sh has ended.
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
run_step julia --project=solver runs/2026-10-18-gpt-b-grin-squeezing/solver_probe.jl ~/analytical-nl-discovery-data/2026-10-18-gpt-b-grin-squeezing
run_step "$py" -W ignore runs/2026-10-18-gpt-b-grin-squeezing/solver_check.py diagnose
run_step julia --project=solver runs/2026-10-18-gpt-b-grin-squeezing/solver_check.jl ~/analytical-nl-discovery-data/2026-10-18-gpt-b-grin-squeezing
run_step "$py" -W ignore runs/2026-10-18-gpt-b-grin-squeezing/solver_check.py compare
run_step "$py" -W ignore runs/2026-10-18-gpt-b-grin-squeezing/exact_three_mode.py fock
run_step "$py" -W ignore runs/2026-10-18-gpt-b-grin-squeezing/exact_three_mode.py twa
run_step "$py" -W ignore runs/2026-10-18-gpt-b-grin-squeezing/count_resolution.py
run_step "$py" -W ignore runs/2026-10-18-gpt-b-condensate-squeezing/nonlinear_ensemble.py
run_step "$py" -W ignore runs/2026-10-18-gpt-b-kerr-exact/sagnac_resolution.py
run_step "$py" -W ignore runs/2026-10-18-gpt-b-kerr-exact/sagnac_quantum_reference.py
