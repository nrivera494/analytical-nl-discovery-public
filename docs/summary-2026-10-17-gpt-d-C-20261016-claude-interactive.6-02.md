---
agent: gpt-d
model: gpt-6-astra
family: gpt
date: 2026-10-17
claim: C-20261016-claude-interactive.6-02
task: T-20261017-gpt-d-01
---

# Raman energy loss: verified core

$$\boxed{
0\le-E'=\frac{n_2f_R}{cA_{\rm eff}}
\int\Omega\operatorname{Im}H_R\,|\widetilde I|^2\frac{d\Omega}{2\pi}
\le\kappa_UE^2,\quad
\kappa_U=\frac{n_2f_Rh_R'(0^+)}{2cA_{\rm eff}},\quad
\frac{E(L)}{E_0}\ge\frac1{1+\kappa_UE_0L}.}$$

$I=|A|^2$ is power, $E=\int I\,dt$ energy, $z$ distance, $L$ fiber
length and $E_0=E(0)$. $n_2$ is nonlinear index, $f_R$ Raman fraction,
$c$ light speed and $A_{\rm eff}$ constant mode area.
$H_R=\widetilde h_R$ uses $\widetilde f=\int f e^{i\Omega t}dt$.

**Regime.** Scalar deterministic photon-conserving shock GNLSE, real
dispersion, no loss/gain; $E>0$ and $0\le\kappa_UE_0L<\infty$.
The normalized causal response has $h_R(0^+)=0$,
$0<h_R'(0^+)<\infty$, passive integrable
$\Omega\operatorname{Im}H_R\ge0$ and Fourier-inversion regularity.
Positive optical support is required for the conserved photon interpretation.

**Proof.** Integration by parts removes Kerr and real dispersion from the
energy balance. Positivity gives $|\widetilde I|\le E$. The response sum
rule integrates its spectral weight to $h_R'(0^+)/2$. Integrating the
resulting differential inequality proves retention. These are exact model
statements, not fits.

![Sech tightness and propagation maxima](../runs/2026-10-17-gpt-d-raman-sharpening/fig_summary.png)

Exact sech curves, quadrature circles and asymptotes; triangles/diamond are propagation maxima at **launch** width, with held-out cases open. Evolved fields need not be sech. Runs: 2026-10-17-gpt-d-raman-sharpening and 2026-10-17-gpt-d-raman-propagation.

**Verification.** Core plus eight held-out launches, $N=1$--6,
30--300 fs intensity FWHM, silica and fluoride surrogates: no rate or
retention violation. Maximum accepted $\rho=|E'|/(\kappa_UE^2)=0.31037732$.
Direct-RHS identity residual is below $5.59\,10^{-14}$ of the bound;
step-error exponent is 4.972. Julia/Python retention differs by at most
$1.04\,10^{-10}$ (propagation run above). Loss and passive-response-mixture
checks also pass.

**Verdict: verified as sharpened; refuted -> audited for the narrowed core.**
The original inverse-square corollary remains refuted.
C-20261017-gpt-d-01/-02 contain the new content and await independent
verification. Novelty and calibrated broadband material applicability are
not established. [Audit and proof](../claims/notes/audit-2026-10-17-gpt-d-C-20261016-claude-interactive.6-02.md).
