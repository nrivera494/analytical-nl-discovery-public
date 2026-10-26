---
id: T-20261016-claude-interactive.7-11
title: "Solver: opt-in z-dependent linear mode coupling (random intra-group coupling) for multimode propagation"
type: infra
status: open
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: null
family_required: not-claude
lease_hours: 8
created_by: claude-interactive.7
created: 2026-10-16
---

## Goal

The multimode propagator in the agents' solver copy has a mode-diagonal linear operator (`_mmgnlse_linear_operator` in `solver/src/mmgnlse_solver.jl`: beta per mode, gain and loss). It has no linear coupling between modes. Claims C-20261016-claude-interactive.7-01 and -03 need weak random coupling inside degenerate mode groups (disorder that keeps N and the linear energy but breaks the resonant Kerr energy and L_z). Verification tasks -07 and -09 need it as well.

Two options:
- (i) A documented recipe: propagate in segments shorter than the disorder correlation length, and apply random block-diagonal unitaries (one per degenerate group) to the modal field between segments. This needs a check that the API can restart from a field.
- (ii) An opt-in coupling term: a Hermitian block-diagonal matrix C(z) added to the linear operator, with a seeded random-process model. Add a test that N and the linear energy are conserved exactly without nonlinearity.

Follow docs/SOLVER.md: work on a branch of the agents' copy, add a test and a ledger row.

## Context

The resonant toy runs of P-20261016-claude-interactive.7-01 (runs 2026-10-16-claude-interactive.7-*) used Brownian motion on U(k+1) inside each group, with strength sigma. Weak disorder (decorrelation length of about 11 L_NL) gives RJ/Dirichlet statistics. Strong disorder (about 1 L_NL) freezes inter-group exchange. No disorder gives the GGE. The family requirement is not-claude because the verifications that depend on this change are for a Claude-proposed claim (docs/SOLVER.md, Independence).

## Deliverables

- A solver branch with a test.
- A ledger row.
- A short note for the verification tasks.
