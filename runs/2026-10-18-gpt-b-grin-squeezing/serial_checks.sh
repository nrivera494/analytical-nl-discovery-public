#!/bin/bash
# gpt-b / gpt-6-astra / gpt. Exactly one numerical child at a time.
set -euo pipefail
cd ~/agent-work/ver-gpt-b
py=~/agent-work/venv/bin/python
grin=runs/2026-10-18-gpt-b-grin-squeezing
cond=runs/2026-10-18-gpt-b-condensate-squeezing
kerr=runs/2026-10-18-gpt-b-kerr-exact
run_step() {
  local line free
  while true; do
    line=$(memory_pressure | grep 'free percentage')
    echo "$line"
    free=$(echo "$line" | sed -E 's/.*: ([0-9]+)%.*/\1/')
    if [ "$free" -ge 35 ]; then break; fi
    sleep 30
  done
  echo "START $(date -u '+%Y-%m-%dT%H:%M:%SZ') $*"
  "$py" evaluator/serial_numerical.py "$@"
  echo "DONE $(date -u '+%Y-%m-%dT%H:%M:%SZ') $*"
}
run_step "$py" -W ignore "$kerr/sagnac.py"
run_step "$py" -W ignore "$kerr/gaussian_edges.py"
run_step "$py" -W ignore "$grin/exact_three_mode.py" fock
run_step "$py" -W ignore "$grin/exact_three_mode.py" twa
run_step "$py" -W ignore "$cond/scaling.py"
run_step "$py" -W ignore "$cond/refine.py"
run_step "$py" -W ignore "$grin/solver_check.py" prepare
run_step julia --project=solver "$grin/solver_check.jl" ~/analytical-nl-discovery-data/2026-10-18-gpt-b-grin-squeezing
run_step "$py" -W ignore "$grin/solver_check.py" compare
run_step "$py" -W ignore "$cond/mechanism.py" spm
run_step "$py" -W ignore "$cond/mechanism.py" diagonal
run_step "$py" -W ignore "$cond/mechanism.py" extracted
run_step "$py" -W ignore "$grin/confirm_counts.py"
run_step "$py" -W ignore "$grin/run.py" convergence
run_step "$py" -W ignore "$grin/run.py" loss
