---
id: T-20261012-gpt-a-09
title: "Add pinned Lean CI and axiom checks"
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

Add CI for the pinned formal/ Lake project after review of T-20261012-gpt-a-02. Build the library, fail on proof holes or unapproved axioms, and preserve the Mathlib pin and cache exclusions.

## Context

The parity pilot supplies a pinned Lean/Mathlib project and kernel-checked
theorems, but no CI integration. See
`docs/lean/2026-10-13-gpt-a-parity-pilot.md`. Reuse the existing repository CI
conventions; do not change toolchain or Mathlib revisions as part of adding CI.

## Deliverables

- A CI build of `formal/AnalyticalNL.lean` using the committed manifest.
- A checked allowlist of `propext`, `Classical.choice`, and `Quot.sound`, and
  rejection of `sorryAx`, project axiom declarations, and unsafe proof shortcuts.
- Cache handling that never commits `formal/.lake` or calls `lake update`.
- A demonstrated failure on a temporary proof hole and success on the pilot.
