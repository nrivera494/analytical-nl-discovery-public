---
id: T-20261006-claude-interactive-05
title: "Converged squeezing of the Raman-soliton spectral filter"
type: explore
status: open
priority: 2
problem: P-20261004-root-03
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-06
---

## Goal

The squeezing of squeezing_spectral_filter.ipynb's setup is reported on a resolved grid (dt <= 3 fs, discrete adjoint, corrected Raman spectrum), with the filter re-optimized on that grid, and with a convergence table.

## Context

squeezing_spectral_filter.ipynb (anomalous-dispersion Raman soliton, binary spectral filter from `benchmark_data/squeezing_spectral_filter/optimal_filter.csv`) reports −5.48 dB with the corrected Raman spectrum. With the same filter bins, the discrete adjoint and dz = 1 mm give −5.44, −4.72, −5.27 and −5.32 dB at $2^{12}$ to $2^{15}$ points (50 ps window). The non-monotonic vacuum term suggests the filter is tuned to the under-resolved model. Most of the residual noise comes from input vacuum at 1600–1650 nm, on the Raman Stokes side (run `2026-10-05-claude-interactive-raman-stochastic`, `convergence/sensitivity_vs_wavelength.png`). This is the single-mode limit of P-20261004-root-03.

## Deliverables

- The filter re-optimized on a resolved grid (dt ≤ 3 fs, discrete adjoint, corrected Raman spectrum, with and without the self-steepening factor of T-20261006-claude-interactive-04).
- A convergence table in time step, window and dz, and the squeezing level with its uncertainty, in a registered run.
