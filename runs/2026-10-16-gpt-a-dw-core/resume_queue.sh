#!/bin/bash
# agent: gpt-a; model: gpt-6-astra; family: gpt
# One numerical process at a time, including after a low-memory pause.
set -euo pipefail
cd ~/agent-work/ver-gpt-a
task_python=~/agent-work/venv/bin/python
task_raw=~/analytical-nl-discovery-data
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
check_memory() {
    while true; do
        memory_pressure | grep 'free percentage'
        if "$task_python" - <<'PY'
import datetime, subprocess, re
if datetime.datetime.now(datetime.timezone.utc)>=datetime.datetime.fromisoformat('2026-10-16T22:40:00+00:00'):
    raise SystemExit(2)
free=int(re.search(r'free percentage: (\d+)%',subprocess.check_output(['memory_pressure'],text=True)).group(1))
raise SystemExit(0 if free>=35 else 1)
PY
        then return; else
            task_status=$?
            if [ "$task_status" -eq 2 ]; then exit 2; fi
        fi
        sleep 30
    done
}
check_memory
mkdir -p "$task_raw/2026-10-16-gpt-a-dw-followup"
"$task_python" runs/2026-10-16-gpt-a-dw-followup/run.py > "$task_raw/2026-10-16-gpt-a-dw-followup/progress.log" 2>&1
check_memory
JULIA_NUM_THREADS=2 ~/.juliaup/bin/julia --project=solver runs/2026-10-16-gpt-a-dw-julia/crosscheck.jl runs/2026-10-16-gpt-a-dw-julia/config.toml > "$task_raw/2026-10-16-gpt-a-dw-julia/progress.log" 2>&1
"$task_python" runs/2026-10-16-gpt-a-dw-core/analyze.py
