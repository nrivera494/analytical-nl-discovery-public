---
id: T-20261006-claude-interactive-06
title: "Resolve the Monte Carlo vs adjoint Raman ratio tension"
type: verify
status: open
priority: 3
problem: null
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-06
---

## Goal

The squeezing corrected/legacy paired variance ratio from Monte Carlo (1.290 +- 0.010 from 85 seeds) is either brought into agreement with the discrete-adjoint value 1.317 by more seeds, or the cause of the difference is found.

## Context

Monte Carlo with `stochastic_solve_raman` (Raman noise only, paired random streams) gave, for the squeezing setup at 300 K, a corrected/legacy variance ratio of 1.290 ± 0.010 from 85 seeds, against 1.317 from the discrete adjoint (2.7σ). The absolute Monte Carlo/adjoint ratio was 1.40 ± 0.21. For the jitter setup everything agreed (ratio 1.0040–1.0048 against 1.0043). A deterministic kick test and the sampler covariance both match the adjoint contraction exactly, so the Monte Carlo is expected to agree. The run stopped early at a time limit (run `2026-10-05-claude-interactive-raman-stochastic`, `summary_partial.txt`).

## Deliverables

- At least 400 squeezing seeds (`example_notebooks/raman_stochastic_check.jl mc squeezing ...` in the agents' copy at `d79f150` or later, run in batches that fit the session limit), the summary compared with the discrete-adjoint values, and either agreement or the cause of the difference.
