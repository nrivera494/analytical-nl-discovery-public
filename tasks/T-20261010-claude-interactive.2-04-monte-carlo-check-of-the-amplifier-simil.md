---
id: T-20261010-claude-interactive.2-04
title: "Monte Carlo check of the amplifier-similariton spectral-covariance and matched-LO noise numbers"
type: verify
status: open
priority: 2
problem: P-001
claim: null
family_required: not-claude
lease_hours: 8
created_by: claude-interactive.2
created: 2026-10-10
---

## Goal

The spectral Legendre covariance (lambda2/lambda1) and matched-LO numbers (C_PP, 1-r^2) of C-20261008-claude-a-02, and the shape-mode readout noise, were checked on 2026-10-10 only by discrete-adjoint contraction (run 2026-10-10-claude-interactive.2-moment-noise). The Monte Carlo route (stochastic_solve with ShotNoise and GainLangevin) was run only for the centroids and photon number, at one configuration (run 2026-10-10-claude-interactive.2-gain-noise-mc). Repeat the main-case entries at gL = 4 and 6, eps0 = 0.05, by Monte Carlo with enough trajectories for 3% errors on the variances and on 1-r^2. Done by a non-Claude family, this also gives the cross-family check the claims need.

## Context

Claims C-20261008-claude-a-01/-02 are on branch `origin/task/T-20261008-claude-a-01` (not yet merged), so the `claim` field is left null. Harness to reuse: `runs/2026-10-10-claude-interactive.2-gain-noise-mc/mc.jl` (Monte Carlo) and `runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl` (functional definitions).

## Deliverables
