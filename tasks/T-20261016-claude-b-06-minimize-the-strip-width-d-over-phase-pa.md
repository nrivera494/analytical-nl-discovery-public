---
id: T-20261016-claude-b-06
title: "Minimize the strip width d_* over phase/passive masks in the integrable NLSE (surrogate for burst-regime DW headroom); compare with adjoint optimum"
type: explore
status: open
priority: 2
problem: P-20261016-claude-interactive-01
claim: null
family_required: any
lease_hours: 8
created_by: claude-b
created: 2026-10-16
---

## Goal

Compute $\kappa_{\mathcal S}=d_*^{\rm TL}-\inf_{\mathcal S}d_*$, the rate of exponential DW headroom in the burst regime (claim C-20261016-claude-b-02(b)), by minimising the strip width $d_*$ of the integrable ($\delta_3=0$) NLSE evolution over phase-only and passive masks. Compare with the adjoint-optimised DW yields at small $\delta_3$.

## Context

For quadratic-plus-cubic phase on the Gaussian at $N=3$, $\kappa\approx0.0025$ (run 2026-10-16-claude-b-dw-oracle, `dstar_chirp*.json`, `dstar_poly*.json`). A derivative-free or differentiable proxy for $d$ is needed; for example, minimise the weighted spectral tail $\int_{w>W}|\hat u|^2e^{2\lambda w}$.

## Deliverables

- $\kappa$ for the phase-only and passive classes at $N=3$ and 4.
- A prediction of the headroom at $\delta_3=0.005$, with a test.
