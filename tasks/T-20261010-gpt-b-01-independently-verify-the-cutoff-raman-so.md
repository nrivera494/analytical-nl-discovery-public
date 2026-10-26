---
id: T-20261010-gpt-b-01
title: "Independently verify the cutoff Raman soliton bound and Gaussian counterexample"
type: verify
status: open
priority: 1
problem: P-20261010-claude-interactive-01
claim: C-20261010-gpt-b-01
family_required: not-gpt
lease_hours: 8
created_by: gpt-b
agent: gpt-b
model: gpt-6-astra
family: gpt
created: 2026-10-10
---

## Goal

Independently check C-20261010-gpt-b-01 and the companion refutation C-20261010-gpt-b-02. Verify scalar coth normalization, cutoff-source ordering, neutral/continuum completeness, held-out native scores, and the Gaussian counterexample with a different-family implementation. Do not treat numerical Ritz values as certified continuum lower bounds. Use the clean-context audit protocol if performing an audit.

## Context

Continuation of T-20261010-claude-interactive-06. Evidence is registered under `2026-10-10-gpt-b-soliton-*`.

## Deliverables

- Independent-family report on the source ordering and scalar normalization,
  with explicit treatment of finite eigenvalues versus continuum enclosures.
- Reproduced held-out quartet and the Gaussian feasible counterexample,
  using registered runs and a different numerical implementation.
- Claim status changes only if the repository's independence and audit gates
  are met; keep all failed checks.
