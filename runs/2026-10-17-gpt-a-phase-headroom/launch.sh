#!/bin/zsh
# agent: gpt-a; model: gpt-6-astra; family: gpt
set -eu
pct=$(memory_pressure | awk '/free percentage/ {gsub("%", "", $NF); print $NF}')
print "System-wide memory free percentage: ${pct}%"
if (( pct < 35 )); then print 'Launch deferred: below 35% free.'; exit 75; fi
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 JULIA_NUM_THREADS=1
exec "$@"
