#!/bin/sh
# Build the manuscript: regenerate the figures from committed run summaries, then compile main.pdf.
# agent: claude-interactive.20; model: claude-opus-5-5; family: claude.
set -e
cd "$(dirname "$0")"
PY="${PYTHON:-$HOME/agent-work/venv/bin/python}"
export PATH="/Library/TeX/texbin:$PATH"
# Fixed timestamps so that rebuilding the same sources gives the same PDF bytes.
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1792411200}" FORCE_SOURCE_DATE=1
MPLCONFIGDIR="${MPLCONFIGDIR:-${TMPDIR:-/tmp}/mpl-manuscript}" "$PY" -W ignore make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
# Report the page on which the appendix starts (label 'appendixstart').
grep -o 'newlabel{appendixstart}{{[^}]*}{[0-9]*}' main.aux | sed 's/.*{\([0-9]*\)}$/appendix starts on page \1/'
