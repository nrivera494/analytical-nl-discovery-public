#!/bin/bash
# agent: gpt-a; model: gpt-6-astra; family: gpt
# Sequential audit queue. The Roy process is the only numerical process at entry.
set -euo pipefail
cd ~/agent-work/ver-gpt-a
task_python=~/agent-work/venv/bin/python
task_sim=runs/2026-10-16-gpt-a-dw-core/simulate.py
task_raw=~/analytical-nl-discovery-data
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MPLCONFIGDIR=/private/tmp/gpt-a-mpl

# meta.yaml is replaced only after the entire Roy sweep has returned.
while grep -q '^status: configured$' runs/2026-10-16-gpt-a-dw-roy/meta.yaml; do
    sleep 5
done
sleep 3

check_memory() {
    memory_pressure | grep 'free percentage'
    "$task_python" - <<'PY'
import datetime, subprocess, re
text=subprocess.check_output(['memory_pressure'],text=True)
free=int(re.search(r'free percentage: (\d+)%',text).group(1))
assert free>=35, 'PI memory threshold: stop queue and resume after recovery'
assert datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat('2026-10-16T22:40:00+00:00'), 'Reserve closure time'
PY
}

check_memory
"$task_python" runs/2026-10-16-gpt-a-gate-null/null_residues.py
for task_slug in dw-heldout-strips dw-law dw-heldout dw-convergence dw-length; do
    check_memory
    mkdir -p "$task_raw/2026-10-16-gpt-a-$task_slug"
    "$task_python" "$task_sim" "runs/2026-10-16-gpt-a-$task_slug/config.yaml" > "$task_raw/2026-10-16-gpt-a-$task_slug/progress.log" 2>&1
done
check_memory
mkdir -p "$task_raw/2026-10-16-gpt-a-dw-julia"
JULIA_NUM_THREADS=2 julia --project=solver runs/2026-10-16-gpt-a-dw-julia/crosscheck.jl runs/2026-10-16-gpt-a-dw-julia/config.toml > "$task_raw/2026-10-16-gpt-a-dw-julia/progress.log" 2>&1
"$task_python" runs/2026-10-16-gpt-a-dw-core/analyze.py
