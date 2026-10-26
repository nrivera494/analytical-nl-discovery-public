---
id: T-20261012-gpt-b-05
title: "Formalize positive-width similariton attraction"
type: derive
status: open
priority: 3
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

Formalize the width Lyapunov identity, positive compact energy sublevels, global ODE continuation and attraction inside the parabolic hydrodynamic family. Test the proposed shifted-energy proof route and record that a GPT proof is a second layer for GPT-family claims.

## Context

Dependency assessment in `docs/lean/2026-10-12-gpt-b-amplifier-similariton-noise-formalization-assessment.md`. The width and broader attraction statements are in GPT-family C-20261008-gpt-a-01 and -02 (PR #24). A GPT formalization is an additional formal layer, not cross-family verification. The exact-asymptote noise pilot does not depend on completing this task.

## Deliverables

- Lyapunov derivative, unique minimum, positive-width compact sublevels and global ODE existence from positive finite initial data.
- An attraction proof, preferably using the assessment's shifted energy if its symbolic identity checks, or a fully stated invariance/compactness argument.
- Separate sharp linearized rates from nonsharp nonlinear convergence estimates.
- Explicit exclusion of arbitrary-input/full-NLSE attraction and of unproved continuum regularity.
- Checked Lean build only after PI selection of an environment, with dependency and axiom provenance.
