#!/bin/bash
# Rebuild every summary, figure, table and generated text from the raw outputs (run from anywhere).
set -e
R=$(cd "$(dirname "$0")/.." && pwd)
PY=~/agent-work/venv/bin/python
for d in 2026-10-10-claude-interactive.2-attraction 2026-10-10-claude-interactive.2-shape-modes 2026-10-10-claude-interactive.2-moment-noise 2026-10-10-claude-interactive.2-gain-noise-mc; do
  (cd "$R/$d" && $PY summarize.py > /dev/null)
done
cd "$R/2026-10-10-claude-interactive.2-simval-lib"
$PY make_figures.py 2>&1 | grep -v Warn | grep -v "^ "
$PY fill_tables.py
$PY collect_configs.py
$PY fill_walltimes.py
echo "summaries, figures, tables, configs and wall times rebuilt"
