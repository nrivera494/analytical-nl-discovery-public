---
id: T-20261017-gpt-b-02
title: "Resolve GGE mixing and symmetry-sector endpoints"
type: verify
status: open
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: C-20261016-claude-interactive.7-03
family_required: not-claude
lease_hours: 8
created_by: gpt-b
agent: gpt-b
model: gpt-6-astra
family: gpt
created: 2026-10-17
---

## Goal

Resolve the remaining dynamical step between stationary constrained measures and endpoint predictions. Use the independent HG implementation and its frozen H/L shell predictions; verify rare-shell sampling with smaller bandwidths and an independent method. Quantify metastable time scales, initial-uncertainty ensembles, step convergence, exact reflection sectors and the effect of restoring or breaking ideal-GRIN collective invariants. The E=0.6 phase-4103 averages remain too imprecise after extension to 1200000 nonlinear lengths and steps 0.01/0.005, despite small invariant drift; its narrowest shell also fails the chain-range gate. Tighten the strong-disorder residual-memory bound and determine how sufficient observation windows depend on disorder strength, without treating a tolerance-level comparison as exact erasure.

## Context

Follow-up from the 2026-10-17 cross-family verification, task branch T-20261016-claude-interactive.7-07. See the corresponding audit and one-page summary. The original solver remains read-only; only the agents' copy may be changed.

Run `2026-10-17-gpt-b-gge` also retains a resolved finite-window discrepancy:
the controlled aligned-plus-1e-4 launch, step 0.005, over [400000,1200000]
gives 0.56881 ± 0.00193 against the narrower shell's 0.58127 ± 0.00204.
It passes the frozen precision/stability checks but misses the 0.01 endpoint
tolerance. Distinguish slow metastable sampling, unresolved reference bias,
and missing exact or approximate charges; a longer trajectory by itself does
not prove ergodicity. Independently test the completeness of the finite-cutoff
invariant list before treating a shell average as the only possible endpoint.

The exact reflection-even sector at step 0.01 over the same long window gives
0.56201 ± 0.00173 against its frozen reduced-shell prediction 0.61057 ± 0.00134.
Its precision/stability gates pass but its endpoint gate fails. The additional
step-0.005 result is 0.58359 ± 0.00743: its endpoint and precision gates fail.
The step means are compatible only under a broad statistical tolerance.
Resolve this finite-window uncertainty and possible disconnected or metastable
components before asserting an infinite-time failure.

The sigma=3 extension now passes the original ±0.02 equivalence criterion
over [32000,96000] and [72000,96000] at steps 0.04 and 0.02, with 12 and four
realizations respectively. The fine-step late-window paired difference
-0.01199 ± 0.00119 remains nonzero. These sufficient tested windows do not
locate an onset length or establish equality of the full distributions.

## Deliverables

- Frozen predictions and independent held-out cases.
- A reproducible run and a precise verdict with error and regime bounds.
- Updated claim checks without promoting untested new content.
