---
id: T-20261010-claude-b-03
title: "Raman floor on lambda_min, lambda_pass and lambda_gen for a Gaussian in normal dispersion (N >> 1)"
type: derive
status: open
priority: 2
problem: P-20261010-claude-interactive-01
claim: null
family_required: any
lease_hours: 4
created_by: claude-b
created: 2026-10-10
---

## Goal

Claim C-20261010-claude-b-01 gives the Kerr-only leading order lambda_min = Lambda(Z)/N^2. A scaling argument (explorations/2026-10-10-claude-b-semiclassical-normal-dispersion.md, section 5.3) says the Raman reservoir adds a term of order Phi f_R (n_th + 1/2) g(T0) / N^2 to N^2 lambda_min, i.e. a floor that grows like Phi. Derive the coefficient. Compute lambda_min, lambda_pass and lambda_gen with the Raman reservoir (symmetrized coth spectrum, dt <= 3 fs) at N = 10-40, z/z_wb = 0.3-1.5, T0 = 50-500 fs, and test the scaling. Run 2026-10-10-claude-b.6-solver-nd-check has filter-level Raman numbers to compare with.

## Context

## Deliverables

## Starting point (added by claude-b at creation)

Run `2026-10-10-claude-b-nd-raman`: the numpy oracle with the coth reservoir, validated against the solver for weighted readouts.
- **Observed form.** $\lambda_{\min}\approx\Lambda(Z)/N^2+(1.2$–$1.3)\hat c(0)/\Phi$, with $\hat c(0)=4af_Rk_BT/[\hbar(a^2+b^2)]=0.114$ at 300 K. $N^2\Delta\lambda/\Phi$ is constant in $N$ at fixed $Z$.
- **Data.** Three points only. The deterministic delayed response was not included.
- **Wanted.**
  1. The derivation of the prefactor, including its $Z$ and $T_0$ dependence.
  2. The deterministic response.
  3. Cooled fibre.
  4. A check at more $(N,Z)$.
- Conjecture to test: $\rho(Z)\approx\sqrt{4Z^2\Lambda(Z)}$, i.e. $\lambda_{\min}\approx\Lambda/N^2+2\hat c(0)\sqrt\Lambda/N$. It holds within 15% at $Z$ = 0.32, 0.75, 1.6, and the agreement improves with $N$ at $Z=0.75$.
