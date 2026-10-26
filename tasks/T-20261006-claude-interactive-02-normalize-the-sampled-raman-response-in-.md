---
id: T-20261006-claude-interactive-02
title: "Normalize the sampled Raman response in the solver"
type: infra
status: open
priority: 1
problem: null
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-06
---

## Goal

The discrete Raman kernel used by the MMGNLSE solver and by agarwal_raman_response integrates to 1 (or the solver documents and checks a maximum dt), as an opt-in option with a test, in the agents' copy.

## Context

`PulsePropagation._mmgnlse_raman_kernels` (src/mmgnlse_solver.jl) and `agarwal_raman_response` (src/backend/adjoint.jl) sample $h_R(t)$ and take a plain Riemann sum, with no normalization. With the Agarwal model, $dt\sum h_R$ is 0.904, 0.976, 0.994, 0.9985 and 0.9996 at dt = 12.2, 6.1, 3.05, 1.53 and 0.76 fs (error $\propto dt^2$), so the delayed nonlinearity is 10% low at the 12.2 fs step of squeezing_spectral_filter.ipynb. On that notebook the filtered photon number moves by 0.8% between $2^{12}$ and $2^{13}$ points and the squeezing by up to 0.7 dB (run `2026-10-05-claude-interactive-raman-stochastic`, `convergence/`).

## Deliverables

- An opt-in normalization (for example rescaling the sampled kernel so that $dt\sum h_R = 1$, or exact integration over each sample interval), leaving the default unchanged, on a solver branch in the agents' copy with a test against the analytic $\int h_R\,dt = 1$ and the Raman gain peak.
- A ledger row in `docs/solver-upstream/LEDGER.md`.
- A statement in `docs/SOLVER.md` of the largest dt that keeps the error below 1% without the option.
