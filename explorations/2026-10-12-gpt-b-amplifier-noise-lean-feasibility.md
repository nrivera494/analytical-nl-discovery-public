---
date: 2026-10-12
agent: gpt-b
model: gpt-6-astra
family: gpt
task: T-20261012-gpt-b-01
problem: P-001
---

# Amplifier-noise Lean feasibility

The assessment is in [the requested document](../docs/lean/2026-10-12-gpt-b-amplifier-similariton-noise-formalization-assessment.md). It reads the narrowed PR #34 statements and pinned source branches, separates physical assumptions from exact reduced mathematics, and records live Mathlib and external-library source checks.

The first recommendation is the deterministic centroid covariance propagator and its frequency/timing integrals. The next is the fixed Legendre block with zero-mode and Jordan restrictions. Rank-one and phase-locking statements need fixed-cutoff covariance bounds; full-field large-gain behavior remains outside the proposed proofs. Width attraction is a GPT-family dependency and would receive a second verification layer.

This is a documentation-only feasibility exploration. There was no simulation or numerical algebra experiment, so no new run folder or raw data was produced. Existing empirical evidence is cited by run id in the assessment. Every Lean block is an unchecked sketch; no toolchain or library was installed.

Follow-up tasks T-20261012-gpt-b-02 through -06 cover the recommended pilot, modal reduction, finite asymptotics/full-field bridge, positive-width ODE, and Gaussian-process dependencies. Existing T-20261011-gpt-a-03 covers the full-field simulation discrepancy and large-gain checks.
