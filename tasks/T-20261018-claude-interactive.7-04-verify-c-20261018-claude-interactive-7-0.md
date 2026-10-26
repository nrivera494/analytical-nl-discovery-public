---
id: T-20261018-claude-interactive.7-04
title: "Verify C-20261018-claude-interactive.7-03 (Kerr squeezability of the equilibrated condensate: (nu^4/n0)^(1/3), Fock-diagonal no-go, Sagnac floor)"
type: verify
status: done
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: C-20261018-claude-interactive.7-03
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

Independent cross-family verification of claim C-20261018-claude-interactive.7-03 against its frozen predictions.

Check the claim against its four frozen predictions:
- exact (Fock-basis) single-mode Kerr of displaced thermal inputs, nu = 3, 10, 30, n = 1e4-1e6 (prediction 1): the curvature-limited law 0.945 (nu^4/n)^(1/3);
- its n^(-1/3) scaling at fixed nu (prediction 2);
- a truncated-Wigner simulation of a balanced fibre Sagnac pumped by a Dirichlet-thermalized condensate (prediction 3): floor -25.9 +- 1 dB;
- the Fock-diagonal no-go (prediction 4).
Search the single-mode Kerr-squeezing and Sagnac literature for prior statements of the n^(-1/3) law and of the pump-noise floor.

## Context

- Claim card: claims/C-20261018-claude-interactive.7-03-*.md. Per docs/AUDIT_PROTOCOL.md, read only the claim card and evaluator code before your report is committed.
- Background for the boundary: gpt-b's review of C-20261016-claude-interactive.7-02 (exact one-mode Kerr is non-Gaussian at s ~ n^(1/6)).

## Deliverables

- A run folder with config, seeds and summary; a verdict on each frozen prediction; the claim card's Checks table filled in.
- Status change of the claim (sim-verified, narrowed, or refuted) in the same PR.

## Completion

Cross-family verification completed with a narrowed `sim-verified` statement; the original wording is preserved. See [audit](../claims/notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-03.md) and [PI summary](../docs/summary-2026-10-18-gpt-b-C-20261018-claude-interactive.7-03.md). Remaining state, readout and novelty work is T-20261018-gpt-b-03.
