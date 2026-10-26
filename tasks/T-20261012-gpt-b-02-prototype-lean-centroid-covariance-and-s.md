---
id: T-20261012-gpt-b-02
title: "Prototype Lean centroid covariance and similariton noise integrals"
type: infra
status: open
priority: 2
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

After the PI authorizes a Lean environment, prove the finite covariance shear formula, photon-number ODE, compression contraction and three explicit similariton integrals with assumptions and input references stated. Resolve the chirped-seed linear-amplifier compressor comparator.

## Context

First recommendation in `docs/lean/2026-10-12-gpt-b-amplifier-similariton-noise-formalization-assessment.md`. Sources are the narrowed Candidate 2 in PR #34 and C-20261008-claude-a-01 on PR #21, pinned in the assessment. This is mathematical checking of a Claude-family claim; it does not confer a simulation/audit status.

No Lean environment was installed during the assessment. Toolchain installation is a separate PI decision. Start with deterministic calculus; the Gaussian-process extension is T-20261012-gpt-b-06.

## Deliverables

- Checked Lean definitions and proofs for the supplied covariance ODE and its shear integral, the scalar photon law, and compression as a covariance quadratic form.
- The three parabolic-seed integral identities and their exact large-gain remainders, with a proved reduction from the supplied rank-one mean covariance.
- The linear-amplifier comparator for a chirped seed, distinguishing added-dispersion compensation from rms-optimal compression.
- Explicit physical assumptions, source ordering, input/output reference conventions and a conditional mean-covariance error-transfer bound.
- Reproducible build, pinned dependencies and theorem-axiom report. No unsupported full-field or uniform short-length accuracy claim.
