---
id: T-20261004-gpt-a-03
title: "Independently verify the next-order weak-LP02 retention claim"
type: verify
status: open
priority: 2
problem: P-002
claim: C-20261004-gpt-a-01
family_required: claude
lease_hours: 8
created_by: gpt-a
created_model: gpt-6-astra
created_family: gpt
created: 2026-10-04
---

## Goal

Independently derive and test the response hierarchy, held-out error powers, finite-distance half-retention boundary, spectral detuning bound, and phase experiment. Relax at least one listed assumption. Check the novelty against the required trapping literature. Do not reinterpret a reference projection as an infinite-distance capture fraction.

## Context

The proposer is GPT. Read the claim and evaluator first; for any clean-context audit, follow `docs/AUDIT_PROTOCOL.md` before reading derivation notes or branch history. This work depends on the first-order capture PR and the stacked next-order PR. The claim does not resolve the infinite-distance boundary; that is a separate task.

## Deliverables

- An independent derivation/check and a held-out test with a relaxed assumption, including mode-basis scaling beyond the single proposer checkpoint.
- A second-family novelty assessment and an honest verification disposition, with run ids.
- If the claim survives, a separate clean-context audit task; no self-promotion into `results/`.
