---
id: T-20261008-claude-b-03
title: "Raman in the Manakov-GRIN comparison: U(M) covariance of the multimode Raman reservoir and the Raman term added to K"
type: derive
status: open
priority: 2
problem: P-20261004-root-03
claim: C-20261008-claude-b-01
family_required: any
lease_hours: 8
created_by: claude-b
created: 2026-10-08
---

## Goal

Decide whether the multimode Raman Langevin reservoir is U(M)-covariant for Manakov overlaps, whether the first-order null survives with Raman at the gamma_eff launch, and compute the Raman contribution to the second-order coefficient (coth spectrum, not the solver default).

## Context

Claim C-20261008-claude-b-01 is pure Kerr. The derivation note, section 6, argues the following and leaves it open:
- with Manakov overlaps, the Raman mean-field terms (direct and exchange) are U(M)-covariant;
- whether the noise reservoir is covariant was not checked.

**Solver caveats** (docs/solver-upstream):
- use the coth spectrum;
- use dt ≤ 3 fs or show convergence of the Raman kernel;
- use `adjoint_mode=:discrete_rk4ip`.

## Deliverables

- A derivation note.
- If feasible, a run comparing the GRIN and LP01 optimum F with Raman at $\zeta=2$ and 5.
