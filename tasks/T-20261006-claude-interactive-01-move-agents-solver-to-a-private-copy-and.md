---
id: T-20261006-claude-interactive-01
title: "Move agents' solver to a private copy and record the Raman spectrum correction"
type: infra
status: done
priority: 1
problem: null
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-06
---

## Goal

Agents never modify the original FastDifferentiableMMNLO. The submodule points at the private agents' copy, docs/SOLVER.md and AGENTS.md say so, the Raman spectrum correction and squeezing-notebook review are recorded with runs and follow-up tasks, and docs/solver-upstream/ holds what the PI needs to carry solver changes to the original.

## Context

The PI ruled on 2026-10-06 that agents may clone and read the original solver repository, github.com/nrivera494/FastDifferentiableMMNLO (public), but must never modify it. The submodule set up in T-20261002-claude-interactive-01 pointed at the original, and `docs/SOLVER.md` told agents to push solver branches there. Nothing had been pushed to it (its only branch was `main` at `9c12887`, no pull requests, checked 2026-10-06).

The PI's local copy `FastDifferentiableMMNLO for agents/` could not serve as the agents' remote: its `origin` is the original, it exists only on the laptop, and its history is 16.5 GiB, over GitHub's 2 GB push limit. The agents' copy therefore starts at a seed commit with the original's `9c12887` tree.

## Deliverables

- Private repository nrivera494/FastDifferentiableMMNLO-agents, seeded at `b9fa957` (tree identical to the original's `9c12887`).
- `.gitmodules` and the pin point at it; `docs/SOLVER.md`, AGENTS.md (session step 1, new hard rule 14, Solver section), `automation/run_session.sh` and `automation/README.md` updated.
- `docs/solver-upstream/` with a ledger and the note for the Raman spectrum change.
- Run record `runs/2026-10-05-claude-interactive-raman-stochastic/`, log entry and follow-up tasks -02 to -08.
