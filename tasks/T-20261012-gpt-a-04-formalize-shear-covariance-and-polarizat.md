---
id: T-20261012-gpt-a-04
title: "Formalize shear covariance and polarization reductions"
type: derive
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

Prove the finite shear covariance spectrum, the quantum uncertainty Schur condition for a nonsymmetric Raman shear, and the two specified Kerr polarization reductions. Include the exact thermal slice formula and its fixed-bath-coefficient asymptotic expansion. Keep continuum spectral infimum and detector reachability separate; use Lean only after the PI chooses a toolchain.

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
