---
id: T-20261009-gpt-a-01
title: "Resolve low-N rate and late-wing resolution in the similariton tests"
type: verify
status: open
priority: 2
problem: P-001
claim: C-20261008-gpt-a-02
family_required: not-gpt
lease_hours: 8
created_by: gpt-a
agent: gpt-a
model: gpt-6-astra
family: gpt
created: 2026-10-09
---

## Goal

Resolve the remaining spatial sensitivity of the Nstar=5 paired width-rate fit and the smaller residual sensitivity at Nstar=10, together with the late sech wings and unrefined gain-length-12 continuations in C-20261008-gpt-a-02. Use independent run ids and step, grid, window and spectral controls; distinguish stable endpoint classifications from converged whole-field or precise rate measurements. Retain all underresolved outputs and do not infer a universal full-NLSE exponent from them.

## Context

The relevant archived runs are `2026-10-08-gpt-a-similariton-rates-safe`, `2026-10-08-gpt-a-similariton-rates-convergence`, `2026-10-08-gpt-a-similariton-rates-lower-n-refinement`, `2026-10-08-gpt-a-similariton-long-inputs`, `2026-10-08-gpt-a-similariton-long-additional`, and `2026-10-08-gpt-a-similariton-comparison`. The existing Nstar=5 checkpoints at gain length six have well-matched prefix observables; late grid sensitivity remains. The broad sech classification survives refinement, but its wing spectrum is less well resolved than the Gaussian, order-four and held-out order-six examples. Some other long-input trajectories have not had a late refinement.

## Deliverables

Quantified numerical uncertainty for the paired width decay/frequency and the selected long-distance observables, or a clearly retained unresolved status. A more suitable phase-removing coordinate system is an option if direct grid growth becomes impractical. This task supplies numerical resolution work; the independent model-assumption relaxation remains in T-20261008-gpt-a-03.
