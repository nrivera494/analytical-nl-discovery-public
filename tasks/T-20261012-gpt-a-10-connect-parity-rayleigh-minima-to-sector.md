---
id: T-20261012-gpt-a-10
title: "Connect parity Rayleigh minima to sector eigenvalues"
type: loose-end
status: open
priority: 3
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

Extend the compiled variational corollary in formal/AnalyticalNL/Parity.lean with a Mathlib spectral-theorem bridge: construct the nontrivial even and odd invariant subspaces, establish attained Rayleigh minima, and identify them as the smallest sector eigenvalues. Handle a trivial odd sector explicitly.

## Context

The pilot's `parity_of_sector_rayleigh_minima` already accepts `IsLeast` on
the sets of nonzero even/odd Rayleigh quotients. The missing bridge is existence
and identification with Mathlib eigenvalues, not the parity inequality.
See `docs/lean/2026-10-13-gpt-a-parity-pilot.md` and the assessment in PR #37.

## Deliverables

- Nontrivial-sector hypotheses and restricted self-adjoint operators.
- A theorem constructing each minimum and identifying its smallest eigenvalue.
- A corollary of `parity_lower_bound` using that interface, without proof holes
  or extra axioms; handle the trivial odd sector via the original lower-bound
  interface rather than an artificial minimum of an empty set.
