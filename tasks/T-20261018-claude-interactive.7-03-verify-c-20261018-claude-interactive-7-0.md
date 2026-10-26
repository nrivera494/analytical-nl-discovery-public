---
id: T-20261018-claude-interactive.7-03
title: "Verify C-20261018-claude-interactive.7-02 (the condensate's own squeezing after the thermalization fibre, ensemble values)"
type: verify
status: done
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: C-20261018-claude-interactive.7-02
family_required: gpt
lease_hours: 8
created_by: claude-interactive.7
created: 2026-10-18
completed: 2026-10-18
completed_by: gpt-b
completer_model: gpt-6-astra
completer_family: gpt
---

## Goal

Independent cross-family verification of claim C-20261018-claude-interactive.7-02 against its frozen predictions.

Check the claim against its four frozen predictions with independent code:
- held-out E' = 0.45 and sigma = 2 ensembles (predictions 1-2), including the realization spread and its shrinking at strong disorder;
- truncated Wigner at n = 1e8 and 1e6 against the tangent map (prediction 3), i.e. the Gaussian-validity threshold n0* = V_P^2/(0.8 lambda_own);
- the formula V_X V_P|X / V_P against the exact minimum eigenvalue (prediction 4).
Relax at least one assumption (for example, finite-correlation-length disorder of realistic strength).

## Context

- Claim card: claims/C-20261018-claude-interactive.7-02-*.md. Per docs/AUDIT_PROTOCOL.md, read only the claim card and evaluator code before your report is committed.
- Background for the boundary: gpt-b's review of C-20261016-claude-interactive.7-02 (exact one-mode Kerr is non-Gaussian at s ~ n^(1/6)).

## Deliverables

- A run folder with config, seeds and summary; a verdict on each frozen prediction; the claim card's Checks table filled in.
- Status change of the claim (sim-verified, narrowed, or refuted) in the same PR.

## Completion

Cross-family verification completed with a covariance/early weak-disorder `sim-verified` narrowing. Strong-disorder step failures and the failed literal late spread gate are retained. See [audit](../claims/notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-02.md) and [PI summary](../docs/summary-2026-10-18-gpt-b-C-20261018-claude-interactive.7-02.md). Follow-up: T-20261018-gpt-b-02.
