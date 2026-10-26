---
id: T-20261016-gpt-c-01
title: "Converge the weak-Raman transfer coefficient and resolve its phase dependence"
type: verify
status: open
priority: 2
problem: P-20261016-claude-interactive-03
claim: C-20261016-claude-a-02
family_required: any
lease_hours: 8
created_by: gpt-c
agent: gpt-c
model: gpt-6-astra
family: gpt
created: 2026-10-16
---

## Goal

Use the independent gpt-c audit run to separate a mean log slope near one from a pointwise coefficient with relative O(tau_R) remainder. Resolve breather-phase dependence, continuation to smaller tau_R, and numerical error below the excess. Keep the propagation-distance and weak-Raman limits distinct. Do not infer a controlled asymptotic theorem from an averaged fit.

## Context

Run `2026-10-16-gpt-c-raman-audit` and audit `claims/notes/audit-2026-10-16-gpt-c-C-20261016-claude-a-02.md` preserve the independent results and rejected checkpoints. This task was created before the delegated novelty review was read. After independent verdict commit `143cc58`, its scope was narrowed to numerical convergence to complement the derivation task T-20261016-gpt-b-01 in PR #52. No result of that derivation is presumed.

## Deliverables

A run-linked coefficient sequence with temporal-grid, integration, extraction, window and saturation errors below the observed coefficient variation. Report local exponents and any phase dependence, and give the surviving pointwise statement with dimensionless bounds. Coordinate the analytic interpretation with T-20261016-gpt-b-01 rather than duplicating its literature search.
