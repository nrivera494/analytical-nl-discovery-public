---
id: T-20261006-claude-interactive-03
title: "Use the discrete adjoint for noise contractions"
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

Noise contractions in the notebooks and in agents' runs use adjoint_mode=:discrete_rk4ip, or the inaccuracy of the default continuous adjoint for noise observables is documented with a measured error and a rule for when it is acceptable.

## Context

`solve_adjoint` defaults to `adjoint_mode=:continuous`, which interpolates the forward field linearly between saved points. For the optimal-filter photon number in squeezing_spectral_filter.ipynb at dz = 1 mm, single-kick responses at z = 3 m are off by 20–60%, the vacuum Fano factor by −4.8% and the Raman term by +14%. The errors shrink about as $dz^2$. `adjoint_mode=:discrete_rk4ip` matches finite differences to $10^{-6}$ and is already converged at dz = 1 mm. For soliton_jitter.ipynb the two modes agree to $10^{-5}$ (run `2026-10-05-claude-interactive-raman-stochastic`, `convergence/kick_test.log`, `round1_continuous_adjoint.log`, `round2_discrete_adjoint.log`, `jitter_adjoint_mode.log`).

## Deliverables

- The noise notebooks in the agents' copy use the discrete adjoint where they contract noise, with outputs re-executed and a ledger row.
- A paragraph in `docs/SOLVER.md`: when the continuous adjoint is acceptable, with the measured error.
- Optionally an opt-in solver change that makes noise observables use the discrete adjoint by default.

## Outcome (2026-10-10, claude-interactive)

On the PI's instruction the discrete adjoint became the default of `solve_adjoint` in the agents' copy (`7f3bfd1`, PR #2 there; CPU tests 24/24). `docs/SOLVER.md` says to use it; the ledger has the row for the original. Still open: moving the pin after PR #2 merges (a separate PR), and re-executing `step_index_squeezing.ipynb`. The backend adjoint used by the problem API is unchanged.
