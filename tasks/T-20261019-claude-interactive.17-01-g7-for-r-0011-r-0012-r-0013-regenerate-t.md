---
id: T-20261019-claude-interactive.17-01
title: "G7 for R-0011, R-0012, R-0013: regenerate the GPT 6 Pro verification figures from committed code"
type: loose-end
status: open
priority: 3
problem: null
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.17
created: 2026-10-19
---

## Goal

The figures of R-0011 to R-0013 are renders of the PDFs in run 2026-10-18-pi-chatgpt-independent-verification. Their build scripts (archive/similariton/build_figures.py, archive/weak/build_summary.py, archive/strong/build_summary.py) read raw .json/.npz files kept at the run's raw_location, so they fail on the committed files alone (checked by claude-interactive.17 on 2026-10-19 in a scratch copy). Rerun the full suites listed in each result's repro/README.md on a copy of the archive, record runtimes and any differences from the committed numbers as a new run, and make each figure regenerable with one documented command (commit the small inputs the build scripts need, within AGENTS.md rule 9, or change the scripts). Then G7 can be set to met in the three RESULT.md files (PI-approved PR).

## Context

## Deliverables
