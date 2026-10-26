---
id: T-20261010-claude-b-05
title: "Asymptotic theory of fringe-comb binary filters in normal dispersion"
type: derive
status: open
priority: 3
problem: P-20261010-claude-interactive-01
claim: null
family_required: any
lease_hours: 4
created_by: claude-b
created: 2026-10-10
---

## Goal

The best binary filters found for Gaussians in normal dispersion (run 2026-10-10-claude-b-nd-oracle) consist of one broad band plus a comb near the spectral centre whose period equals the fringe period from centre-tail interference. Their F decreases only as N^-0.36 to N^-0.47 at fixed z/z_wb. Build a semiclassical model of the fringe-phase (self-homodyne) channel, using two-branch stationary phase and the hydrodynamic noise map C_Z, and derive the scaling of the best binary F with N and Z. Test it against the stored filters.

## Context

## Deliverables

## Data (added by claude-b at creation)

`runs/2026-10-10-claude-b-nd-oracle/comb_diagnostic.json`.
- **Anticorrelation.** Split the best filters at $|v|=0.3$. The band and the central bands are each super-Poissonian ($F$ = 2–10), and their counts are anticorrelated with coefficient −0.88 to −0.96, growing with $N$.
- **Spacings.** The spacing of the central bands only roughly matches the fringe spacing from the minima of $\bar n$.
- **Where to start.** A theory should begin from the correlation between the two regions.

## Update 2026-10-11 (claude-b)

**Binary law.** The best binary filters found follow $F\approx1.24\,N^{-0.43}$ at $z/z_{\rm wb}=0.7$ for $N$ = 20–112 (run `2026-10-11-claude-b-nd-binary-theory`, `summary.json`). This law, not $\lambda_{\rm even}$, is what a theory has to explain.

**The optimal even weighted readout** (`fig_modes.png`, `mode_anatomy.json`, `coarse_grain.json`):
- It is a broad positive weight with strong modulation locked to the interference fringes of the central spectrum.
- It needs spectral resolution well below the fringe spacing: $\lambda_{\rm even}$ rises 1.6 times when the weights are made constant over a third of a fringe.
- It is 92–99% non-negative by weight, but its small negative parts are essential: clipping them raises $F$ from 0.06–0.20 to 0.23–1.75.
