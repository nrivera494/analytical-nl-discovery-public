---
id: T-20261012-gpt-b-04
title: "Prove finite similariton covariance asymptotic bounds"
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

For the explicitly defined finite modal covariance ODE, prove shape trace and rank-one eigenvalue-ratio bounds and the phase-energy regression residual bound. State every nondegeneracy and cutoff dependence; distinguish envelopes from asymptotic equivalents and identify the unproved full-field error bridge.

## Context

Follow-up to T-20261012-gpt-b-01 and the mode-block target T-20261012-gpt-b-03. The assessment defines an autonomous finite covariance ODE, its intensity-source Gram matrix and the orthonormal Legendre readout metric. PR #34 restricts rank one and phase/energy locking to that reduced model.

The existing audit follow-up T-20261011-gpt-a-03, on PR #34, concerns full-field validation. Do not duplicate its simulation campaign. Coordinate the missing full-field error bridge with that task; fixed-cutoff formal asymptotics are a different deliverable.

## Deliverables

- A fully specified finite covariance system, including cross-mode source correlations and initial conditions.
- An explicit shape-trace upper bound and the positive-semidefinite block lemma giving the second-to-first eigenvalue ratio.
- A phase/energy regression-residual bound, preserving the accumulated-phase coefficient and the matched-LO reference.
- Lower-envelope assumptions, or a clear statement that only an upper bound is proved; no unjustified constant-prefactor asymptotic equivalent.
- A list of assumptions still needed for a smooth-edge full-field comparison, cutoff-uniformity and a physically admissible joint large-gain/small-noise limit.
