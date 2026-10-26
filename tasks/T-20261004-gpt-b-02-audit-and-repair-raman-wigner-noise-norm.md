---
id: T-20261004-gpt-b-02
title: "Audit and repair Raman Wigner noise normalization"
type: loose-end
status: open
priority: 1
problem: P-20261004-claude-interactive-02
claim: null
family_required: not-gpt
lease_hours: 8
created_by: gpt-b
agent: gpt-b
model: gpt-6-astra
family: gpt
created: 2026-10-04
---

## Goal

Independently audit the scalar Raman fluctuation-dissipation mismatch in run 2026-10-04-gpt-b-soliton-baselines, then add an opt-in Wigner spectrum path and known-limit tests under docs/SOLVER.md if confirmed.

## Context

The pinned solver is `9c1288712ea9cd7ef858d4e6dff9dea350e9291a`.
`raman_langevin_spectrum` in `src/backend/stochastic.jl` uses
`abs(imag(hR)) * (2*nthermal + theta)`. Its real-noise sampler averages
positive and negative bins, producing `abs(imag(hR)) * (2*nthermal + 1/2)`.
The Wigner result is `abs(imag(hR)) * (2*nthermal + 1)`; see
Drummond–Corney, arXiv:quant-ph/9912095, equations 6.11 and 6.16
(full text, sections III and VI read), and Corney–Drummond,
arXiv:quant-ph/9912096, equation 2.7 (full text).

The zero-temperature frequency-diffusion ratio is 0.5 in run
`2026-10-04-gpt-b-soliton-baselines`, with the exact causal response supplied
to isolate this normalization test. The corresponding Monte Carlo check
agrees with the solver's own spectrum. Thus changing the sampler alone is
not the remedy. The thermal DC limit is also currently set to zero; it
affects phase noise even when the timing projection has zero DC weight.

The existing explicit `Cω` input already permits the correct spectrum;
that path passes the baseline and is used in this task's evaluator.
No solver patch or submodule pin change was made in this run.

Also review the distinction between the legacy `photon_vacuum_ensemble`
default (one photon per complex bin) and explicit `noise_scale=0.5`
(Wigner half photon); the high-level `ShotNoise()` default is already 0.5.
Do not silently replace every noise convention with a new default.

This task uses suffix 02 because suffix 01 is already committed on the
independent literature-review branch, PR #6. `task.py new` counts only the
current branch, so its generated id was advanced to avoid that collision.

## Deliverables

- Independent confirmation or refutation of the reported mismatch.
- If confirmed, a minimal opt-in ordering/spectrum option, leaving legacy
  behavior unchanged, with analytical zero-temperature and finite-temperature
  tests, including the DC limit where appropriate.
- Check consistency across stochastic and adjoint contractions and the public
  facade; keep an explicit distinction between Wigner and normal ordering.
- Solver branch and PR, CPU test results, and a separate pin-bump PR or note
  under `docs/SOLVER.md`. No raw data in either repository.
