---
id: T-20261010-claude-interactive.2-05
title: "Recompute the held-out gL=2 spectral ratio of C-20261008-claude-a-02 P5"
type: derive
status: open
priority: 2
problem: P-001
claim: null
family_required: any
lease_hours: 4
created_by: claude-interactive.2
created: 2026-10-10
---

## Goal

The full NLSE gives lambda2/lambda1 = 0.387, 0.386, 0.385, 0.390 at eps0 = 0.1, 0.05, 0.025, 0.0125 for the held-out case (Gamma = 1, gL = 2), against the frozen 0.4257 of C-20261008-claude-a-02 P5: a deviation of -8.4% to -9.5% that barely changes over a factor 8 in eps0 (run 2026-10-10-claude-interactive.2-moment-noise). The other held-out gL = 2 entries (s_0, s_2, 1-r^2) converge, and the main case converges at gL = 4 and 6. Recompute the P5 gL = 2 ratio from the claim's own formulas (b), with an independent ODE solve and the L2 metric on l <= 4, to decide whether the frozen value or the leading-order theory is at fault. If the frozen value is right, identify the term the leading order misses at gL = 2. Second item, same readout: the main-case N0 Var(s_1) ASE entry of P3 comes out 14-19% above the frozen value at every gL and does not shrink with eps0, although in the leading order it is 4/5 of the C-01 Var(Omega_c) entry, which the centroid functional reproduces. Decide whether the Legendre projection over the core picks up edge noise the leading order drops, or whether the claim defines s_l differently, and state the readout exactly.

## Context

The claim C-20261008-claude-a-02 is on branch `origin/task/T-20261008-claude-a-01` (not yet merged), so the `claim` field is left null. Spectral functional definitions: `runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl` and `analyze_lib.py` (Legendre components over the core $|\omega-\Omega_c|\le\sqrt5\sigma_\omega$, $L^2$ metric). Moving the core cut to the chirp edge changes the ratio by 0.1% (core-sensitivity entries in that run's summary.json). Validation note: `explorations/2026-10-10-claude-interactive.2-similariton-validation.md` (task T-20261010-claude-interactive.2-01).

## Deliverables

- A short script that recomputes the P5 entries ($s_0$, $s_2$, $\lambda_2/\lambda_1$, $1-r^2$) at $gL=2,4,6$ from the claim's formulas, with its output.
- A log entry stating whether 0.4257 is reproduced, and if so, what the leading-order theory misses at $gL=2$.
