---
id: T-20261012-gpt-b-06
title: "Check Lean Gaussian-process dependencies for amplifier noise"
type: infra
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

After PI approval of a Lean environment, pin and check the Mathlib Gaussian and external Brownian/Wiener-integral dependencies, inspect theorem axioms, and prove the deterministic-kernel joint Gaussian centroid construction. Do not assume a covariance ODE proves Gaussianity.

## Context

The deterministic pilot is T-20261012-gpt-b-02. The assessment locates Mathlib Gaussian-process support and external BrownianMotion/MathFin deterministic Wiener-integral sources; source inspection is not a build or a transitive axiom audit. Do not install Lean or additional packages without the PI's later environment decision.

## Deliverables

- Compatible pinned dependencies, a minimal build and axiom checks for the precise imported theorems; distinguish merged Mathlib from external projects.
- A deterministic-kernel construction of the centroid process with joint Gaussian finite-dimensional laws and two-time covariance.
- Input/noise independence and circular Gaussian source assumptions, plus integrability and positive-semidefinite covariance hypotheses.
- An explicit boundary between finite projections, continuum white noise, and the full stochastic NLSE. General Itô calculus is optional and must not become an unnecessary dependency.
