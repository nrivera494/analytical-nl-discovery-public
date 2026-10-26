---
id: T-20261004-claude-interactive-07
title: "Derive the walk-off boundary of a weakly multimode GRIN soliton beyond first order"
type: derive
status: open
priority: 1
problem: P-002
claim: C-20261004-gpt-a-01
family_required: gpt
lease_hours: 12
created_by: claude-interactive
updated_by: gpt-a
updated_model: gpt-6-astra
updated_family: gpt
created: 2026-10-04
---

## Goal

Extend the first-order weak-admixture structure of P-20261004-claude-interactive-01 to a **finite** LP02 fraction $p_2$, and turn it into a P-002 result. Deliver:
- the walk-off boundary $\delta_c(p_2)$, beyond which the minority is not captured;
- the captured fraction to next order in $p_2$.

Include:
- the minority's own self-phase ($S_{02,02}/S_{01,01}=1/2$ in an ideal parabolic profile);
- its back-action on the soliton;
- leakage into LP03 through the phase-matched 01+03↔02+02 channel.

Also run P-002's cheap discriminating test: launches with equal modal powers but different relative phases, to see whether an occupation-only description fails.

## Context

Read AGENTS.md, `docs/plan-2026-10-round1.md`, the problem card, `docs/SOLVER.md` and, for the squeezing cards, `docs/multimode-squeezing-scope.md`. Read the results of T-20261004-claude-interactive-02 (first-order capture test) first. If it is not finished, run it before this task, since it is the first-order check this task builds on.

Read Menyuk, JOSA B 5, 392 (1988), and Steiglitz & Rand, PRA 79, 021802 (2009), in full. Soliton trapping under walk-off and weak-probe trapping are known, so state exactly what is new. The audited gap on P-002 is a controlled closure for modal content inside a bound pulse and a parameter-derived capture law; the Zitelli 2021 exponential capture fit is the baseline to predict, not to re-propose.

Raw data: follow the interim local-storage rule in `runs/README.md`. Raw output goes to `~/analytical-nl-discovery-data/<run-id>/`, and its path is recorded as `raw_location` in `meta.yaml`. For this round's four problems, such runs may be cited by claims. Do not verify your own claim; a Claude agent will.

## Deliverables

- A claim file `C-<date>-<agent>-NN` on P-002 containing:
  - statement, regime bounds on $(p_2,\delta,\zeta,\sigma-1)$, assumption ledger;
  - frozen predictions with a held-out $(p_2,\delta)$ region;
  - the predicted error exponent.
- Cheap checks with run ids.
- An exploration note on the phase test.
- A session log and a pull request.

## Partial delivery by gpt-a

Agent `gpt-a`, model `gpt-6-astra`, family `gpt`, 2026-10-04: delivered C-20261004-gpt-a-01, the frozen response and half-retention predictions, proposer error-scaling/convergence checks, a spectral bound on detuning-suppressed LP03 generation, and the phase experiment. The claim is only `cheap-checks-passed`; Claude verification is T-20261004-gpt-a-03.

**This task remains open.** The finite-distance half-retention level set is not the requested literal boundary beyond which none of the minority is captured. The leading projection is positive at every finite walk-off, so a regular compact-domain correction cannot supply that boundary. Resolving the infinite-distance observable and order of limits is T-20261004-gpt-a-04. The finite-distance correction and discriminating phase test are complete within their stated Kerr model.
