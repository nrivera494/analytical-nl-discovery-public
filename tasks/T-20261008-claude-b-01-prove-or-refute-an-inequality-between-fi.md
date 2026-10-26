---
id: T-20261008-claude-b-01
title: "Prove or refute an inequality between filtered Manakov (LP01) and GRIN soliton noise"
type: derive
status: done
priority: 1
problem: P-20261004-root-03
claim: C-20261008-claude-b-01
family_required: any
lease_hours: 8
created_by: claude-b
created: 2026-10-08
---

## Goal

A precisely stated inequality between the spectrally filtered noise of the Manakov/LP01 soliton and the GRIN multimode soliton (or a statement that GRIN can never beat LP01-only), proved or refuted, with its normalization, readout and regime explicit.

## Context

PI direction of 2026-10-08, P-20261004-root-03 Find item 4, assigned by the orchestrator claude-interactive in round 2.

## Deliverables

- A claim card with the inequality proved, refuted or narrowed.
- Frozen predictions and a held-out case.
- Runs, and a log entry with proposed card changes.

## Outcome (claude-b, 2026-10-08)

Claim `claims/C-20261008-claude-b-01-manakov-grin-filtered-noise.md` (proposed); derivation in `explorations/2026-10-08-claude-b-manakov-grin-inequality.md`. All results are for the pure-Kerr cross-phase model, each launch at its own soliton energy.

**Refuted: "GRIN can never beat LP01-only".**
- At a fixed filter it fails at every $\zeta$ studied.
- At the optimal filter it fails at $\delta=0$ for $\zeta<\zeta_c=2.67$. Converged counterexample at $\zeta=2$, $p_2=0.75$: $-1.05\times10^{-2}$ in $F$. The independent solver code agrees with the numpy $\Delta F$ to $10^{-8}$.

**Proved:**
- the Manakov equivalence;
- parity in $\delta$;
- the first-order null in the overlap defect (any number of modes).

**Narrowed, at second order:** $\Delta F=K\|q\|^2+W\|r\|^2$ with universal $K$ and $W$, so the GRIN advantage is at most about $10^{-2}$ in $F$ and vanishes for $\delta>\delta_c$.

**Held-out predictions:** the signs were right everywhere, but most frozen tolerances failed because third-order terms are larger than assumed. This is recorded in the claim.

Loose ends: T-20261008-claude-b-02 to -05.
