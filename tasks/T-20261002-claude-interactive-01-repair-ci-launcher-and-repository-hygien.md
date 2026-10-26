---
id: T-20261002-claude-interactive-01
title: "Repair CI, launcher and repository hygiene for unattended sessions"
type: infra
status: done
priority: 1
problem: null
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-02
---

## Goal

Unattended sessions can run on the PI's Mac and leave a repository that stays consistent without the PI rebuilding anything by hand.

## Context

The bootstrap described CI, CODEOWNERS and a result-notification workflow, but `.github/` was never committed, so generated files went stale on `main`. The PI asked for this repair on 2026-10-02 and added the solver (FastDifferentiableMMNLO) for agents to use and edit.

## Deliverables

- `.github/`: CODEOWNERS; workflows that validate pull requests, reject hand edits to generated files, rebuild generated files on `main`, and flag result candidates.
- `.gitignore`; `.DS_Store` removed from the index.
- `solver/` git submodule pinned to a FastDifferentiableMMNLO commit, plus `docs/SOLVER.md` covering how agents use and change it.
- Launcher works on macOS: Python with PyYAML, `timeout`/`gtimeout`, `caffeinate`, a separate configuration directory per account, unattended permission flags.
- STATUS dashboard lists the items waiting on the PI.
- Follow-up tasks for the loose ends.
