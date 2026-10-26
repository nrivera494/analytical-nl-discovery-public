#!/bin/bash
# agent: gpt-a; model: gpt-6-astra; family: gpt
set -euo pipefail
cd ~/agent-work/ver-gpt-a
task_raw=~/analytical-nl-discovery-data/2026-10-16-gpt-a-dw-highprecision
while read -r task_name task_delta task_n task_window task_steps task_xi; do
    if [ -f "$task_raw/$task_name.toml" ]; then continue; fi
    while true; do
        memory_pressure | grep 'free percentage'
        if ~/agent-work/venv/bin/python - <<'PY'
import subprocess,re
free=int(re.search(r'free percentage: (\d+)%',subprocess.check_output(['memory_pressure'],text=True)).group(1))
raise SystemExit(0 if free>=35 else 1)
PY
        then break; fi
        sleep 30
    done
    AUDIT_DEADLINE=2026-10-16T22:46:00 JULIA_NUM_THREADS=2 ~/.juliaup/bin/julia --project=runs/2026-10-16-gpt-a-dw-highprecision runs/2026-10-16-gpt-a-dw-highprecision/precision.jl "$task_name" "$task_delta" "$task_n" "$task_window" "$task_steps" "$task_xi" > "$task_raw/$task_name.log" 2>&1
done <<'CASES'
primary 0.003 16384 256 8192
halfstep 0.003 16384 256 16384
window 0.003 32768 512 8192
propagated_null 0 16384 256 8192
upper 0.0032 16384 256 8192
lower 0.0028 16384 256 8192
precompression 0.003 16384 256 9216 2.25
precompression_halfstep 0.003 16384 256 18432 2.25
precompression_window 0.003 32768 512 9216 2.25
precompression_grid 0.003 32768 256 4096 2.25
CASES
