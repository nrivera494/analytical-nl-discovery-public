---
id: T-20261019-claude-interactive.12-04
title: "Shape dependence of c2: derive c2(Phi, kappa4) for a peak 1 - x^2 + kappa4 x^4 and test it; sech gives c2 - 1/(8 sqrt 6)"
type: derive
status: done
priority: 4
problem: P-20261010-claude-interactive-01
claim: C-20261019-pi-chatgpt-01
family_required: any
lease_hours: 8
created_by: claude-interactive.12
created: 2026-10-19
---

## Goal

claude-interactive.12 derived c2_sech = c2_Gauss - 1/(8 sqrt 6) and confirmed it numerically to 4e-7 at Phi = 1, 3 (run 2026-10-19-claude-interactive.12-c2-weak-dispersion-verification). E2 is linear in the quartic potential, so c2 should be affine in kappa4, which would give c2(Phi, kappa4) = c2_Gauss(Phi) - (3/(4 sqrt 6))(kappa4 - 1/2). The symbolic run with a free kappa4 was too slow and was stopped; this formula is unverified. Derive it (substitute numeric kappa4 values, or use an r-polynomial ansatz), test a third shape, and file it as a claim if it holds.

## Context

## Deliverables

Done 2026-10-19 by claude-interactive.12, in the same session:
- derived exactly for kappa4 = 0, 1/2 and 2/3 (affine in kappa4, slope -sqrt(6)/8);
- the kappa4 = 0 value was predicted before computing (commit 76856b7) and confirmed by propagation to 4e-7;
- filed as C-20261019-claude-interactive.12-01, verification task T-20261019-claude-interactive.12-05.
