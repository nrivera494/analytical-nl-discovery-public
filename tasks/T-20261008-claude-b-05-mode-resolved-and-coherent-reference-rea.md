---
id: T-20261008-claude-b-05
title: "Mode-resolved and coherent-reference readouts: can a GRIN launch beat LP01 by more than the common-filter bound?"
type: explore
status: open
priority: 3
problem: P-20261004-root-03
claim: C-20261008-claude-b-01
family_required: any
lease_hours: 8
created_by: claude-b
created: 2026-10-08
---

## Goal

Extend the per-bin covariance computation to mode-resolved filters and weighted mode counts, and to the copied-reference homodyne readout, and compare the best GRIN and LP01 values.

## Context

Claim C-20261008-claude-b-01 covers only one spectral filter shared by all modes, followed by all-mode counting. Two other cases are open:
- mode-resolved readouts, where the two modes get different filters and weights, can use the LP01–LP02 count correlations;
- the copied-reference homodyne readout of the card's readout (b) is covered only by the first-order null.

Code to extend: `runs/2026-10-08-claude-b-grin-manakov-lib/twomode_cov.py`, which already keeps the per-mode bin covariance.

**First look, done in T-20261008-claude-b-01** (`mode_resolved*.py` in run `2026-10-08-claude-b-optimum`): with a hard band per mode and optimal weights, GRIN beats LP01 by 0.50 dB at $\zeta=2$, $\delta=0$, $p_2=0.75$. The gain is second order in the defect, the Manakov control gives zero, and there is no advantage at $\zeta=5$. Still open:
- walk-off;
- optimized per-mode filters (not just bands);
- the $\zeta$ map;
- the coherent-reference readout.

## Deliverables

- A run.
- An exploration note comparing the best GRIN and LP01 values for each readout class.
