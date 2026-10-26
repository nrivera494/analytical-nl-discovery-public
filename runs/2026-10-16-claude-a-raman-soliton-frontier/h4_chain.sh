#!/bin/sh
# H4 queue (after the N=2, N=3 phase-only runs at d3=0). Thread-limited; one job at a time.
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
PY=~/agent-work/venv/bin/python
while kill -0 67808 2>/dev/null; do sleep 20; done
$PY -W ignore h4_opt.py h4_N4_T100_d0_phi.json 4 100 0 phi 6 2 100 > h4_N4_T100_d0_phi.log 2>&1
$PY -W ignore h4_opt.py h4_N3_T100_d005_phi.json 3 100 0.05 phi 6 2 100 > h4_N3_T100_d005_phi.log 2>&1
$PY -W ignore h4_opt.py h4_N4_T100_d005_phi.json 4 100 0.05 phi 6 2 100 > h4_N4_T100_d005_phi.log 2>&1
$PY -W ignore h4_opt.py h4_N3_T100_d0_Aphi.json 3 100 0 Aphi 6 2 100 > h4_N3_T100_d0_Aphi.log 2>&1
$PY -W ignore h4_opt.py h4_N2_T100_d005_phi.json 2 100 0.05 phi 6 2 100 > h4_N2_T100_d005_phi.log 2>&1
