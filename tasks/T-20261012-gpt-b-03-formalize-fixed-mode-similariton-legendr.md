---
id: T-20261012-gpt-b-03
title: "Formalize fixed-mode similariton Legendre transfer"
type: derive
status: open
priority: 2
problem: P-001
claim: null
family_required: any
lease_hours: 8
created_by: gpt-b
created: 2026-10-12
agent: gpt-b
model: gpt-6-astra
family: gpt
---

## Goal

Prove the supplied Legendre blocks, determinant, characteristic roots, zero-mode restriction, critical-mode Jordan term and spectral cancellation, then fixed-mode gain envelopes. Separate finite polynomial identities from endpoint-domain and completeness obligations.

## Context

Second recommendation in `docs/lean/2026-10-12-gpt-b-amplifier-similariton-noise-formalization-assessment.md`. C-20261008-claude-a-02 supplies the noise application; C-20261008-gpt-a-01 supplies the endpoint, zero-mode and Jordan qualifications. Preserve the family distinction. No Lean installation is authorized by this task until the PI chooses the environment.

## Deliverables

- Fixed-mode characteristic polynomial and complex roots; two-by-two determinant preservation.
- A derivation from the original first-order block that excludes the spurious zero-mode density root.
- The critical-mode Jordan solution and its cancellation in the spectral readout.
- Explicit oscillatory transfer bounds and photon-normalized gain envelopes with fixed-mode constants and nondegeneracy hypotheses for lower bounds.
- A separate inventory/proof of the low-degree Legendre polynomial identities and endpoint-domain obligations. Do not claim completeness or high-mode uniformity from finite checks.
