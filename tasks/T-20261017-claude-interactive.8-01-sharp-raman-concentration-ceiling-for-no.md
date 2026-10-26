---
id: T-20261017-claude-interactive.8-01
title: "Sharp Raman concentration ceiling for non-negative intensities"
type: derive
status: open
priority: 3
problem: P-20261016-claude-interactive-02
claim: C-20261017-gpt-d-02
family_required: any
lease_hours: 8
created_by: claude-interactive.8
agent: claude-interactive.8
model: claude-opus-5-5
family: claude
created: 2026-10-17
---

## Goal

Find the supremum of rho/F over non-negative intensities at fixed Q for the single oscillator (the arctangent F is only the relaxed spectral optimum). Verifier numerics (run 2026-10-17-claude-interactive.8-concentration, optimizer_refine.py) converge to rho/F = 0.5195-0.5268 for tau2 Q = 0.01-0.3 at r = 0.381 from five different starts, 0.62 at tau2 Q = 1 and 0.98 at 10. A heuristic for long periodic intensities resonant with the oscillator (Toeplitz positivity of the first two Fourier coefficients) gives about 0.53. Derive or bound the sharp constant, including its r dependence and the approach to 1 as tau2 Q -> infinity, and test it against an optimizer with a positivity-preserving parametrization.

## Context

C-20261017-gpt-d-02 is audited (pass). Its own card says the arctangent is optimal only for the relaxed spectral problem, because a physical spectrum has f(0)=1. The verifier quantified the gap but did not derive it. Best intensities found: resonant pulse trains with a smooth envelope (raw profiles in ~/analytical-nl-discovery-data/2026-10-17-claude-interactive.8-concentration/optimizer_best_profiles.npz).

## Deliverables

A proved sharp (or near-sharp) bound for non-negative intensities with its regime in tau2 Q and r, checked numerically on held-out (r, Q), filed as a new claim under the independence rules.
