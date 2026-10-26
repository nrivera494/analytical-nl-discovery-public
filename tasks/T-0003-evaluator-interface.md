---
id: T-0003
title: "Implement the evaluator interface against the solver"
type: infra
status: open
priority: 2
problem: null
claim: null
family_required: any
lease_hours: 12
created_by: claude-bootstrap
created: 2026-10-01
---

## Goal

`evaluator/` can take a claim's prediction function and a parameter grid and return the cascade results described in `evaluator/README.md`, using the solver as an external dependency pinned by commit.

## Context

`evaluator/README.md`, `docs/SOLVER.md`. The solver is the Julia package in the `solver/` submodule; do not copy it in. Choose the evaluator's language with that in mind: Julia, or Python that calls Julia. Missing solver capabilities may be added under `docs/SOLVER.md`.

## Deliverables

Working cascade stages 1–4 for a 1D NLSE claim, with the fundamental soliton as the smoke test; a `runs/` entry produced by it; documentation of how to add a stage.
