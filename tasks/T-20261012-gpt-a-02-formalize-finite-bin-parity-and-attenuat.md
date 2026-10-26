---
id: T-20261012-gpt-a-02
title: "Formalize finite-bin parity and attenuation bounds"
type: infra
status: done
priority: 1
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

After the PI authorizes a Lean toolchain, implement and kernel-check the finite-bin parity lower bound with both sector orderings, its binary-mask corollary, and the vacuum-corrected physical attenuation bound. Use the unchecked sketches and explicit modelling boundary in docs/lean/2026-10-12-gpt-a-filtered-fano-formalization-assessment.md. Do not treat this task as authorization to install Lean before the PI decides.

## Context

Created by the feasibility assessment in task T-20261012-gpt-a-01 for the PI.
See `docs/lean/2026-10-12-gpt-a-filtered-fano-formalization-assessment.md` for
precise assumptions, source references, and the boundary between model hypotheses
and mathematical conclusions. No Lean installation was authorized in that session.

## Deliverables

- A PI-approved minimal Mathlib pin, checked declaration names and imports;
  external library integration is optional and must be checked separately.
- A precise statement with its model assumptions and formalization level.
- A proof or an explicit account of the remaining mathematical obstruction;
  any Lean code must be checked in a PI-authorized, pinned environment.
- An honest evidence log, with no promotion or claim-status change inferred from
  the assessment alone.

## Completion

The PI approved the pilot and supplied Lean/Mathlib `v4.35.0-rc4` with its cache.
The parity bound, conditional sector-Rayleigh-minimum corollary, physical
attenuation bound, binary identity/bound, and two rational scope counterexamples
are compiled in `formal/AnalyticalNL/Parity.lean`. The complete project builds
without warnings. All 35 theorem axiom closures contain only `propext`,
`Classical.choice`, and `Quot.sound`.

See `docs/lean/2026-10-13-gpt-a-parity-pilot.md` for evidence and proposed card
changes, and `formal/README.md` for the theorem-to-claim map. No claim or problem
card was edited. Follow-ups T-20261012-gpt-a-09, -10, and -11 track CI, the
constructed spectral/eigenvalue bridge, and reviewed card wording, respectively.
