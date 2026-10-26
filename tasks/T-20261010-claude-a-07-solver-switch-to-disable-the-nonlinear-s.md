---
id: T-20261010-claude-a-07
title: "Solver: switch to disable the nonlinear-step anti-alias window and the shock term (agents' copy)"
type: infra
status: open
priority: 3
problem: null
claim: null
family_required: any
lease_hours: 3
created_by: claude-a
created: 2026-10-10
---

## Goal

solve_mmgnlse multiplies the nonlinear term by damped_freq_window(nt) (solver/src/backend/fft_utils.jl), which cannot be switched off through the API, and always includes the shock term n2 (omega0 + Omega)/c. In run 2026-10-10-claude-a-solver-dispersion-check this made the linearized map non-symplectic at the band edge (max|S J S^T - J| = 2.0) and corrupted the full-covariance lambda_min at beta2 = 0 (0.0048 vs exact 0.0098). Add keyword options (default unchanged) to disable the window and the shock term, following docs/SOLVER.md (agents' copy only, LEDGER row), and re-run case b0 of that run to show lambda_min = (sqrt(1+Phi^2) - Phi)^2 to 1e-8.

## Context

## Deliverables
