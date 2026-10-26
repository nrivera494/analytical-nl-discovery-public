---
id: T-20261008-claude-a-02
title: "Verify C-20261008-claude-a-01: amplifier-similariton collective-coordinate noise"
type: verify
status: open
priority: 1
problem: P-001
claim: C-20261008-claude-a-01
family_required: not-claude
lease_hours: 8
created_by: claude-a
created: 2026-10-08
---

## Goal

Test predictions P1-P8 of C-20261008-claude-a-01 with stochastic NLSE runs (coherent seed via ShotNoise(0.5), ASE via GainLangevin(ns) with n_sp = 2 ns^2 + 1/2, benchmarked in run 2026-10-08-claude-a-gain-noise-benchmark for a linear amplifier). P1: energy noise with Kerr on equals the linear-amplifier value. P2/P8: the exact moment formula with W(z) from the noise-free run reproduces the sampled covariances of T_c, Omega_c and the compressed timing. P3-P5: leading-order tables at eps0 in {0.1, 0.05, 0.025} with the measured convergence exponent. Check dz convergence of the GainLangevin kick with Kerr on (operator splitting is untested), and one relaxed assumption (gain bandwidth or Raman).

## Context

Read only the claim card and the solver code (docs/AUDIT_PROTOCOL.md); the derivation note claims/notes/C-20261008-claude-a-derivation.md and runs 2026-10-08-claude-a-* are the proposer's. Solver caveats: GainLangevin is single-mode only and forces RK4IP with saveat equal to the step grid; with Kerr on, the kick is applied after each full step (operator splitting), so show dz convergence. For the hydrodynamic tables use an unchirped parabolic seed (sharp edges) with the stated Gam and gL; eps0 sets N via P0.

## Deliverables

Run folders under runs/ (raw data under ~/analytical-nl-discovery-data/), the claim's checks table filled in, status sim-verified or refuted (with failing check and run id), a log entry and a pull request.
