---
id: T-20261004-claude-interactive-10
title: "Derive the walk-off correction to the noise of a weakly multimode soliton"
type: derive
status: blocked
priority: 2
problem: P-20261004-root-03
claim: null
family_required: claude
lease_hours: 12
created_by: claude-interactive
created: 2026-10-04
---

## Goal

For a weakly multimode soliton launch (LP01 plus an LP02 fraction $p_2$), derive two things:
- the filtered-count and coherent-reference-readout Fano factors to first order in $p_2$, with walk-off $\delta$ treated exactly;
- the statement, if it holds, that the walk-off-free joint count maps onto the scalar soliton at the same $\zeta$.

Give the correction in $\delta$ that the archive's failed $P\to P/\kappa$ rescaling missed.

## Context

**Blocked** until two things are done:
- P-20261004-root-03 has been reviewed by two families: T-20261004-root-02 (Claude) and T-20261004-claude-interactive-01 (GPT, extended to root-03);
- T-20261004-claude-interactive-02 (first-order capture test) has reported.

Use the baselines from T-20261004-claude-interactive-06. Read AGENTS.md, `docs/plan-2026-10-round1.md`, the problem card, `docs/SOLVER.md` and, for the squeezing cards, `docs/multimode-squeezing-scope.md`. Raw data: follow the interim local-storage rule in `runs/README.md`. Raw output goes to `~/analytical-nl-discovery-data/<run-id>/`, and its path is recorded as `raw_location` in `meta.yaml`. For this round's four problems, such runs may be cited by claims. Do not verify your own claim.

## Deliverables

- A claim with frozen predictions, including a held-out $(p_2,\delta)$ case.
- Cheap checks with run ids.
- A session log and a pull request.
