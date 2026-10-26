---
id: T-20261018-claude-interactive.7-02
title: "Verify C-20261018-claude-interactive.7-01 (pre-scrambling squeezing: photon counting robust, quadrature squeezing curvature-bounded)"
type: verify
status: done
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: C-20261018-claude-interactive.7-01
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

Independent cross-family verification of claim C-20261018-claude-interactive.7-01 against its frozen predictions.

Check the claim against its five frozen predictions with independent code (another family's implementation of the resonant GRIN model, exact
Hermite-Gauss tensor, K = 5, or the solver with emulated intra-group disorder; the solver has no linear mode coupling, see T-20261016-claude-interactive.7-11):
- the Gaussian-validity boundary sigma_max^6 ~ n0 of the multimode quadrature squeezing (predictions 1-2, held-out E' and n);
- the error-scaling exponent of the curvature excess, n^-1 (prediction 3);
- photon-counting robustness at z = 200, 300 (prediction 4);
- the curvature ceiling of the best multimode quadrature squeezing at n = 1e10 (prediction 5).
Relax at least one assumption (for example, finite-correlation-length disorder, or more modes).

## Context

- Claim card: claims/C-20261018-claude-interactive.7-01-*.md. Per docs/AUDIT_PROTOCOL.md, read only the claim card and evaluator code before your report is committed.
- Background for the boundary: gpt-b's review of C-20261016-claude-interactive.7-02 (exact one-mode Kerr is non-Gaussian at s ~ n^(1/6)).

## Deliverables

- A run folder with config, seeds and summary; a verdict on each frozen prediction; the claim card's Checks table filled in.
- Status change of the claim (sim-verified, narrowed, or refuted) in the same PR.

## Completion

Cross-family verification completed with an early-quadrature `sim-verified` narrowing. Original counting assertions remain unverified, and numerical attacks failing the frozen refinement gate are not accepted as physical counterexamples. See [audit](../claims/notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-01.md) and [PI summary](../docs/summary-2026-10-18-gpt-b-C-20261018-claude-interactive.7-01.md). Follow-up: T-20261018-gpt-b-01.
