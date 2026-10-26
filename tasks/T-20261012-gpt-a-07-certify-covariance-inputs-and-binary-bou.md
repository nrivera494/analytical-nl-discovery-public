---
id: T-20261012-gpt-a-07
title: "Certify covariance inputs and binary bound witnesses"
type: infra
status: open
priority: 2
problem: P-20261010-claude-interactive-01
claim: null
family_required: any
lease_hours: 8
created_by: gpt-a
created: 2026-10-12
agent: gpt-a
model: gpt-6-astra
family: gpt
---

## Goal

Design exact rational or interval PSD witnesses for finite covariance and binary dual certificates, including rounding and truncation enclosures. Preserve the full readout domain and bound mean-amplitude error, especially near dark bins. A floating-point eigenvalue or numerical Cholesky margin is not a formal certificate. The hierarchy and certificates originate in GPT-family PR #28, so formalization is a second layer, not cross-family verification.

## Context

Created by the feasibility assessment in task T-20261012-gpt-a-01 for the PI.
See `docs/lean/2026-10-12-gpt-a-filtered-fano-formalization-assessment.md` for
precise assumptions, source references, and the boundary between model hypotheses
and mathematical conclusions. No Lean installation was authorized in that session.

## Deliverables

- A precise statement with its model assumptions and formalization level.
- A proof or an explicit account of the remaining mathematical obstruction;
  any Lean code must be checked in a PI-authorized, pinned environment.
- An honest evidence log, with no promotion or claim-status change inferred from
  the assessment alone.
