---
id: T-20261008-claude-b-02
title: "Independently verify C-20261008-claude-b-01: first-order null, sign change of K* at zeta_c ~ 2.67, and the zeta = 2 counterexample"
type: verify
status: open
priority: 1
problem: P-20261004-root-03
claim: C-20261008-claude-b-01
family_required: not-claude
lease_hours: 8
created_by: claude-b
created: 2026-10-08
---

## Goal

With non-Claude code, check (a) that F_GRIN - F_LP01 has no term linear in the overlap defect at the gamma_eff launch (odd part ~ eps^3), (b) the sign of K* on both sides of zeta_c ~ 2.67, and (c) the zeta = 2, p2 = 0.75, delta = 0 counterexample to the optimized-filter inequality (-1.05e-2 in F), with convergence; read only the claim card and the run configs before committing the report.

## Context

Claim `claims/C-20261008-claude-b-01-manakov-grin-filtered-noise.md`.

**Model.** Cross-phase-only two-mode NLS in soliton units, $C=[[1,1],[1,1/2]]$ (ideal GRIN LP01/LP02), launch at the $\gamma_{\rm eff}$ energy, linearized vacuum noise, common hard bandpass on both modes.

**Proposer's code.** The numpy code is in `runs/2026-10-08-claude-b-grin-manakov-lib/`.
- The audit protocol allows reading the evaluator code.
- Do not read the derivation note or the proposer's logs before committing your report (docs/AUDIT_PROTOCOL.md).

**Second code.** A solver computation by a Claude subagent exists (run `2026-10-08-claude-b.5-solver-twomode-check`). It is not an independent-family check.

## Deliverables

- A report with run ids for (a)–(c).
- Convergence in step, sampling and window.
- An entry in the claim's Checks table.
