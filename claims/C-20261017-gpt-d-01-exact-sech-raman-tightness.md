---
id: C-20261017-gpt-d-01
problem: P-20261016-claude-interactive-02
title: "Exact sech Raman loss ratio and controlled inverse-cube and saturation expansions"
type: asymptotic-solution
status: promoted
agent: gpt-d
model: gpt-6-astra
family: gpt
proposed_by: gpt-d
proposer_model: gpt-6-astra
proposer_family: gpt
verified_by: claude-interactive.8
verifier_family: claude
audited_by: claude-interactive.8
auditor_family: claude
created: 2026-10-17
updated: 2026-10-19
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: R-0004
---

## Statement

For the scalar, lossless, photon-conserving shock GNLSE with constant effective
area, define $I=|A|^2$, $E=\int I\,dt$,
$\kappa_U=n_2f_R h_R'(0^+)/(2cA_{\rm eff})$ and
$\rho=|dE/dz|/(\kappa_UE^2)$. The physical systems are silica and fluoride
single-mode fiber oscillator models. The measurable prediction is the
instantaneous fractional energy loss of a known sech intensity, independent
of its energy and phase after this normalization. The launch need not be a
fundamental soliton; a fission product need not remain a sech.

For $I(t)=E\,\operatorname{sech}^2(t/T)/(2T)$ and
$h_R(t)=(a^2+b^2)e^{-at}\sin(bt)/b$ for $t>0$, where
$a=1/\tau_2>0$, $b=1/\tau_1>0$, the proposed exact result is

$$\boxed{\rho(T)=\operatorname{Re}\!\left[
\left(1+i\frac ab\right)
\left\{1-s+\frac{s^2}{2}\psi_1(1+s/2)\right\}\right],
\qquad s=(a-ib)T.}$$

Here $\psi_1$ is the trigamma function, $\tau_1$ the inverse Raman angular
resonance frequency, $\tau_2$ the damping time, and $T$ the sech scale,
not intensity FWHM. Equivalently, with
$W(\Omega)=\Omega\operatorname{Im}\widetilde h_R(\Omega)$ and $k=h_R'(0^+)$,

$$\rho=\frac2k\int W(\Omega)
\left[\frac{\pi\Omega T/2}{\sinh(\pi\Omega T/2)}\right]^2
\frac{d\Omega}{2\pi}.$$

For a general real causal response satisfying the core bound's hypotheses,
$\mu_j=\int_0^\infty t^j h_R(t)dt$ and
$\mu_{5,\rm abs}=\int_0^\infty t^5|h_R(t)|dt<\infty$ give

$$\boxed{\rho=\frac{8\mu_1}{15kT^3}
-\frac{16\mu_3}{63kT^5}+R,\qquad
|R|\le\frac{16\mu_{5,\rm abs}}{225kT^7}.}$$

The leading equivalence requires $\mu_1>0$. In
$\rho\sim C_3(\tau_1/T)^3$, the general coefficient is
$C_3=8\mu_1/(15k\tau_1^3)$ for the specified reference time $\tau_1$.
For the oscillator, put $r=\tau_1/\tau_2$, $x=T/\tau_1$:

$$\rho=\frac{16r}{15(1+r^2)^2}x^{-3}
\left[1+\frac{40(1-r^2)}{7(1+r^2)^2}x^{-2}
+O_r(x^{-4})\right],$$
$$\rho=1-2rx+\frac{\pi^2(3r^2-1)}{12}x^2
+2r(1-r^2)\zeta(3)x^3+O_r(x^4).$$

In particular, $1-\rho=2T/\tau_2+O_r((T/\tau_1)^2)$.
This corrects the inverse-square assertion in
C-20261016-claude-interactive.6-02 as a separate claim.

## Regime

- Exact oscillator identity: $0<x<\infty$, $0<r<\infty$, $E>0$,
  under the stated envelope model and regularity assumptions.
- Long-pulse asymptotics: $x^{-1}\to0$ at fixed $r$; short-pulse
  asymptotics: $x\max(1,r)\to0$. The constants are not asserted uniform
  as $r\to0$ or $r\to\infty$. The general-response remainder above is explicit.
- Proposer tests cover $0.2\le r\le1.4$ at five specified response ratios,
  $0.002\le x\le160$; long-error fits use $40\le x\le160$.
  Short fits use $0.002\le x\le0.016$, with a disclosed adaptive
  $0.00025\le x\le0.002$ follow-up at $r=0.6$
  (run 2026-10-17-gpt-d-raman-sharpening).
- The leading short residual cancels at $r=1/\sqrt3$ and the long
  relative correction at $r=1$; a fixed finite-window slope need not
  show the generic order near these values.
- The limit $x\to0$ is formal model sharpness. It is not a calibrated
  subcycle silica/fluoride prediction. Direct RHS snapshots keep
  $\omega_0T=50$ by varying the carrier, rather than claiming a
  fixed-wavelength material scan.

## Assumptions

- Scalar, single spatial mode, deterministic GNLSE; no gain or linear loss.
- Exact photon-conserving shock factor $\omega/\omega_0$, constant
  $A_{\rm eff}$ and $n_2$, real dispersive multiplier.
- Real causal normalized response, $h_R(0^+)=0$, finite positive
  $k=h_R'(0^+)$, integrable passive $W\ge0$ and the regularity needed for
  $\int W\,d\Omega/(2\pi)=k/2$. The closed form and short coefficients
  specifically require the stated single oscillator.
- Sufficient field decay and regularity; positive optical support and
  finite photon norm when assigning a photon-mean interpretation.
- The intensity is sech at the plane where the formula is evaluated.
  Phase is arbitrary. Pulse-shape preservation during propagation is not assumed.
- The general long expansion additionally needs the absolute fifth response
  moment; its leading asymptotic equivalence needs $\mu_1>0$.

## Predictions

Frozen before production in commit 6df0927ef31369add037f36db21643b14d68bf51,
[predictions](../runs/2026-10-17-gpt-d-raman-sharpening/predictions.md).
Held-out response ratios are $r=0.2,0.6,1.4$. Exact-curve/quadrature
agreement target is relative $10^{-8}$ or absolute $10^{-11}$; long decay
exponent $3\pm0.02$, leading relative-error exponent $2\pm0.05$,
corrected relative-error exponent $4\pm0.15$; short gap exponent
$1\pm0.05$. Analytic coefficient extrapolations must agree within 1%.
The original short-linear-residual tolerance $2\pm0.08$ is retained,
including its failure at $r=0.6$.

Additional predictions were separately frozen before their tests in commits
3259dd5be15c597202b52436ff7d5d1918c702dc (cancellation refinement) and
ca03c40b69e09530f57de96863bab3d048df06ea (direct RHS and sampled kernel).
All numbers and tolerances trace to that run's prediction and summary files.

## Derivation

The intensity characteristic function is
$\widetilde I/E=(\pi\Omega T/2)/\sinh(\pi\Omega T/2)$.
Inverting $W$ gives $h_R'(|t|)/2$. The difference of two independent
unit-sech-squared variables has density
$(u\coth u-1)\operatorname{csch}^2u$; its Laplace transform is
$(1-s)/2+s^2\psi_1(1+s/2)/4$. This proves the proposed exact formula.
The long expansion uses the sine Taylor remainder and Parseval for the
first three derivatives of the normalized intensity. The short expansion
uses finite moments of the difference density; a high-frequency expansion
under the spectral integral would be invalid.
Details: [proof note](notes/proof-2026-10-17-gpt-d-raman-sharpening.md).

## Checks

Rows by gpt-d are **proposer checks**; rows by claude-interactive.8 are the
independent cross-family verification and audit.
M denotes run 2026-10-17-gpt-d-raman-sharpening; P denotes
2026-10-17-gpt-d-raman-propagation; L denotes
2026-10-17-gpt-d-raman-literature. S, C and H denote the verifier's runs
2026-10-17-claude-interactive.8-sech-tightness, -concentration and -hc-relaxed.

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units, symmetries | Dimensionless ratio; invariant under energy scaling, phase and time translation at fixed intensity shape | gpt-d (gpt), analytic | M | 2026-10-17 |
| Exact formula | Independent spectral quadrature agrees to $7.84\,10^{-16}$ relative on all frozen ratios/widths | gpt-d (gpt) | M | 2026-10-17 |
| Long limit and coefficient | Silica decay 3.00158; leading and corrected relative-error exponents 2.00170 and 4.00091. $C_3=0.30999923$ extrapolated, fit-window sensitivity $2.13\,10^{-7}$, exact 0.30999947 | gpt-d (gpt) | M | 2026-10-17 |
| Short limit and coefficient | Silica gap exponent 1.00390. Linear coefficient 0.762500043 with fit-window sensitivity $3.38\,10^{-8}$, exact 0.7625. These sensitivities are not statistical intervals | gpt-d (gpt) | M | 2026-10-17 |
| Held-out region | Exact formula, leading gap and all long exponents pass. Original short-linear residual slope at $r=0.6$ is 2.08200, outside $2\pm0.08$; retained failure | gpt-d (gpt) | M | 2026-10-17 |
| Adaptive cancellation check | Smaller-width follow-up yields residual slopes 2.01144 and 2.99929; cubic coefficient agrees to $6.09\,10^{-8}$ relative. Not held out | gpt-d (gpt) | M/followup_summary.json | 2026-10-17 |
| GNLSE RHS | Actual nonlinear RHS agrees with exact curve to $9.06\,10^{-12}$ relative; decay exponent 3.00158. Formal short snapshot reaches 0.96880762 | gpt-d (gpt) | M/followup_summary.json | 2026-10-17 |
| Propagation context | Core and eight held-out launches obey energy ceiling and retention. They depart from sech during compression/fission; maximum ratios are plotted at launch widths, not fitted to the sech curve | gpt-d (gpt) | P | 2026-10-17 |
| Numerical artifacts | Exact response transfer used; sampled-kernel normalization/rate-error orders 2.00026/4.00215 at $dt\le3$ fs | gpt-d (gpt) | M | 2026-10-17 |
| Independent exact formula | Verifier's own derivation and code. Closed form equals spectral and autocorrelation quadratures at 48 held-out points frozen in commit f784fed ($0.1\le r\le5$, $7\times10^{-4}\le x\le600$): max relative difference $3.3\times10^{-25}$. At $r=0.01$ and $20$: $5\times10^{-28}$ | claude-interactive.8 (claude) | S | 2026-10-17 |
| Independent exponents (held out) | Long: decay $-3.0009$ to $-2.9999$; leading relative error $-2.0004$ to $-1.9999$ ($r\ne1$), $-3.999999$ at $r=1$; two-term $-3.9989$ to $-4.0010$. Short: $(1-\rho)/(2rx)-1$ slope 0.991 to 1.000; cubic residual 2.993 to 3.003 ($r\ne1$), 3.998 at $r=1$. General remainder bound holds at 9 points (oscillator) | claude-interactive.8 (claude) | S | 2026-10-17 |
| Independent GNLSE | Own photon-conserving solver. Launch-plane RHS equals the closed form for 16 sech launches, 5 to 300 fs, SMF-28 and fluoride surrogates (11 held out): max relative $1.7\times10^{-11}$; Richardson $dE/dz$ from real propagation $4.1\times10^{-9}$. Sampled kernel at $dt=2.5$ fs: $\le2.3\times10^{-5}$. Propagated $N=1$: $\rho(z)/\rho(T_{\rm eff}=1/3Q)$ in $[0.991,1.056]$ (30 fs) and $[0.99999,1.0010]$ (300 fs). Agents' solver b9fa957 reproduces $E(z)$ within $3.2\times10^{-15}$ | claude-interactive.8 (claude) | S, C | 2026-10-17 |
| Retained failure explained | Gap-ratio slope at $r=0.6$ is 1.080 in $x\in[0.002,0.016]$ and 1.0005 in $[10^{-5},10^{-4}]$; exactly 2 at $r=1/\sqrt3$. Pre-asymptotic window effect, not an expansion error | claude-interactive.8 (claude) | S | 2026-10-17 |
| Relaxed assumption (HC 13-mode silica) | Moment expansion survives: slopes $-1.96$ and $-4.11$ over 0.6 to 3 ps, remainder bound holds. Closed form not applicable. $\rho_{\rm HC}/\rho_{\rm BW}=1.19$ (5 fs), 3.01 (100 fs), 3.07 (300 fs): Blow–Wood is not a calibrated silica prediction beyond about 10 fs | claude-interactive.8 (claude) | H | 2026-10-17 |
| Independent audit | **Pass**, no blockers ([audit](notes/audit-2026-10-17-claude-interactive.8-C-20261017-gpt-d-01.md), committed 6320014 before reading proposer material) | claude-interactive.8 (claude) | S, C, H | 2026-10-17 |
| Novelty (verifier) | The exact sech kernel for arbitrary response is published: arXiv:2603.21734 Eq. (2) (§3 of v2, full text, read by subagent claude-interactive.8.1) equals $\frac{15}{4}(-q')$, the claim's autocorrelation kernel, within $2\times10^{-35}$. Leading law: arXiv:2607.05244 Eq. (17), full text. Trigamma closed form and short coefficients not found | claude-interactive.8 (claude) | S | 2026-10-17 |
| Novelty | Leading inverse-cube energy law is explicit in arXiv:2607.05244 Eq. 18 (full text, energy sections read). Exact trigamma/short-gap expression not found in restricted search; novelty unestablished | gpt-d (gpt) | L | 2026-10-17 |

## Outcome

**Promoted 2026-10-19.** On the PI's decision of 2026-10-19 (task T-20261019-claude-interactive-07), the statement as audited is promising result [R-0004](../results/promising/R-0004-exact-sech-raman-loss-ratio/RESULT.md). Gates G6 (Herrmann–Nazarkin and Gordon full texts, T-20261017-gpt-d-04) and G8 are open.

Filed at cheap-checks-passed by gpt-d. Independently verified and audited by
claude-interactive.8 (claude) on 2026-10-17: verdict pass, status **audited**,
regime unchanged. The analytic identity and asymptotic remainders have
a proof, extensive proposer tests and an independent rederivation with held-out
tests. A generic finite-window residual-slope prediction failed near cancellation
and is explicitly restricted; the verifier traced it to the window.
Original-text prior-art comparison remains open (T-20261017-gpt-d-04). The
exact sech integral for arbitrary responses is published (arXiv:2603.21734 Eq. 2),
so novelty is limited to the trigamma evaluation and the expansion coefficients.
For silica, the Blow–Wood closed form is a model result, not a calibrated
prediction (run H).
Herrmann and Nazarkin, DOI 10.1364/OL.19.002065 (publisher abstract only),
already study the short-pulse crossover; its full-text coefficient comparison
is explicitly pending in T-20261017-gpt-d-04. The independent verification
task T-20261017-gpt-d-02 is done.
See the [PI summary](../docs/summary-2026-10-17-gpt-d-C-20261017-gpt-d-01.md) and the
verifier's PI-format summary, first given in the description of PR #60 and since committed as
[docs/summary-2026-10-17-claude-interactive.8-C-20261017-gpt-d-01.md](../docs/summary-2026-10-17-claude-interactive.8-C-20261017-gpt-d-01.md) (3fd45a8; figure:
`runs/2026-10-17-claude-interactive.8-sech-tightness/fig_summary.png`).

## Audit trail

| Date | Agent (family) | Change and evidence |
|---|---|---|
| 2026-10-17 | gpt-d (gpt), gpt-6-astra | Filed corrected/new content separately from the narrowed Claude bound. No self-verification. Frozen predictions and failed finite-window test retained in M. |
| 2026-10-17 | claude-interactive.8 (claude), claude-opus-5-5 | Independent verification and adversarial audit, T-20261017-gpt-d-02. Held-out predictions frozen in f784fed; audit committed in 6320014 before reading proposer material. Verdict pass, no blockers. Status cheap-checks-passed → audited; verified_by and audited_by set. Statement and regime unchanged. Runs S, C, H. |
| 2026-10-19 | claude-interactive.15 (claude), claude-opus-5-5 | Status audited → promoted; `result: R-0004`. Statement unchanged. G5 met (claude-interactive.8's clean-context audit); G6 and G8 open. The Outcome now points at the committed verifier summary instead of saying it could not be written. Task T-20261019-claude-interactive-08 |
