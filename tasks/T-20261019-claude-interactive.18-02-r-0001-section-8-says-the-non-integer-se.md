---
id: T-20261019-claude-interactive.18-02
title: "R-0001 section 8 says the non-integer sech headroom is at most 0.44%; that holds only for N >= 2.5 (0.671% at N~2.40, 5.60% at N~1.30): amend the wording, and fix two rounding slips of the asymmetric gains"
type: loose-end
status: done
priority: 3
problem: P-20261016-claude-interactive-03
claim: C-20261018-pi-chatgpt-01
family_required: any
lease_hours: 8
created_by: claude-interactive.18
created: 2026-10-19
---

## Goal

R-0001 section 8 (Experimental test, 'Precision needed') states the corrected bound: the best even-moment ceiling exceeds the TL eigenvalue by at most 0.437% for N >= 2.5 and by up to 0.671% for 2 <= N <= 4 (maximum where the ceilings of consecutive exponents cross, N~2.40); the PI approves the change (results/ is PI-merged). Optionally, the C-20261016-claude-a-01 Checks row and claude-interactive.9's audit note the run values 2.776% (per-bin) and 2.642% (amplitude-and-phase Chebyshev) for the quoted +2.777% and +2.643%, as a typo note.

## Context

Found by claude-interactive.18 while writing the manuscript `docs/manuscripts/2026-10-19-phase-shaper-soliton-bounds/` (task T-20261019-claude-interactive.18-01); see its README, "Discrepancies" 1 and 2.

- The largest headroom between consecutive integers is where U_2n and U_2n+2 cross, slightly below the half-integer: 5.60% at N~1.30, 0.671% at N~2.40, 0.205% at N~3.43, 0.088% at N~4.45 (closed form, `crux_checks.json` in that folder). The committed curve `runs/2026-10-18-claude-interactive.9-mask-adversary/figure_curves.json` gives 0.66868% at N=2.4 on its grid.
- The half-integer values of R-0001 (D) and the claim card are correct; only the "at most 0.44%" sentence of section 8 is too strong for the proposed N = 2-4 experiment.
- Rounding: `runs/2026-10-18-claude-interactive.9-asym-counterexample/verify_summary.json` gives gain_over_TL 0.0277646 (passive-bins) and 0.0264248 (passive-cheb).

## Deliverables

A PI-approved edit of R-0001 section 8 (and optional typo notes), with an audit-trail entry; no status change.

## Outcome

Done in PR #86 (R-0001 section 8 corrected; between-integer maxima confirmed by the orchestrator).
