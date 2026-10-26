---
id: C-20261010-gpt-b-01
problem: P-20261010-claude-interactive-01
title: "A cutoff linear-coth reservoir gives a one-sided frozen-soliton Fano bound"
type: bound
status: proposed
proposed_by: gpt-b
proposer_model: gpt-6-astra
proposer_family: gpt
agent: gpt-b
model: gpt-6-astra
family: gpt
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-10
updated: 2026-10-10
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: null
---

## Statement

Consider a coherently launched fundamental scalar soliton in the linearized
focusing NLSE, with an added symmetrized Raman reservoir and a **frozen Kerr
mean and propagator**. This is a reduced model for a weakly drifting bright
soliton in an anomalous-dispersion silica fibre, not the full deterministic
Raman GNLSE.

For the damped-oscillator response with $\tau_2>\tau_1$, define

$$T_R=\frac{2f_R\tau_1^2\tau_2}{\tau_1^2+\tau_2^2},\qquad
\Omega_c=\sqrt{2(\tau_1^{-2}-\tau_2^{-2})},\quad K_c=T_0\Omega_c,$$
$$S_L(k)=\frac{T_R}{T_0}|k|\coth\left(
\frac{\hbar|k|}{2k_BT T_0}\right)1_{|k|\le K_c}.$$

Use the thermal limit at the DC point and coth equal to one at zero
temperature. Let $q=\operatorname{sech}x$, $M_\zeta$ be the complete
neutral-mode plus squared-Jost-continuum Kerr propagator, and $\mathcal C_L$
the Fourier multiplier $S_L$. In vacuum-normalized real quadratures put

$$V_L=M_\zeta M_\zeta^*+
4\int_0^\zeta M_s\operatorname{diag}(0,q\mathcal C_Lq)M_s^*ds,$$
$$B_L=\inf\operatorname{spec}(\mathcal R_q^*V_L\mathcal R_q).$$

Here $\mathcal R_q$ inserts a real spectral-amplitude readout with the mean
field's phase. The exact oscillator source is $S_R=f_R|\operatorname{Im}
H_R(k/T_0)|\coth(\hbar|k|/(2k_BT T_0))$. Then

$$0\le S_L\le S_R,\qquad
V_L\preceq V_{\rm fr},\qquad
\boxed{B_L\le\lambda_{\rm gen}(V_{\rm fr})\le
\min_{T(k)\in\{0,1\}}F_{\rm fr}[T].}$$

This bound is rigorous **within the stated linear frozen model**. Its
numerical implementation is a converging approximation, not a certified
continuum eigenvalue enclosure. It is a soliton/material specialization
of the shared readout hierarchy, not a new general readout theorem.
Taking the maximum with $\lambda_{\min}(V_{\rm fr})$ remains a lower bound.
The reported soliton cases have $B_L$ above that full-field bound.

The observable prediction is a limit on the variance-to-mean ratio of
photons transmitted through any binary spectral mask in this model.
An explicit Jost Gram integral evaluates the source without a longitudinal
nonlinear propagation. The deterministic Raman shift, shock and third-order
dispersion are addressed as perturbations in the exploration; a uniform
one-sided physical remainder is **not** part of this claim.

## Regime

- $N=1$, $\beta_2<0$, $T_0>0$, $T\ge0$, $0\le f_R\le1$ and
  $0<\tau_1<\tau_2$; finite normalized distance
  $\zeta=z|\beta_2|/T_0^2$. The core model has $s=\delta_3=0$ and no
  deterministic Raman drift.
- Physical comparison: $\zeta\le6$ and
  $\zeta\max\{T_R/T_0,|s|,|\delta_3|\}\le0.06$, where
  $s=(\omega_0T_0)^{-1}$ and $\delta_3=\beta_3/(6|\beta_2|T_0)$.
  These bounds describe the tested domain, not a universal guarantee.
  The tested material has $f_R=0.18$ and
  $\max(\tau_1,\tau_2)/T_0\le0.256$; using the first-moment deterministic
  expansion additionally requires that response-width ratio to be small.
- An even mask or an isolated parity eigenvalue has a formal second-order
  correction from the odd first-moment Raman, shock and beta3 forcings.
  The exact delayed response also has an even correction of order
  $f_R(\max\{\tau_1,\tau_2\}/T_0)^2$; the order is in response width
  at fixed $f_R$, not uniformly in $T_R/T_0$ under arbitrary material
  changes. Crossings and symmetry-broken binary optima are excluded
  from that perturbation statement.
- The positive-temperature, long-pulse source tends to
  $\rho_T=2k_BT T_R/\hbar$ on every fixed frequency range; its quadratic
  forms on fixed regular readouts have corrections of order $T_0^{-2}$.
  At zero temperature the leading source scales as $T_R|k|/T_0$.
  Neither order is asserted uniformly over arbitrary frequency supports.

## Assumptions

1. One scalar spatial/polarization mode, lossless propagation, no gain,
   no GAWBS, no detector noise and a bright coherent input.
2. Linearized quantum fluctuations; the exact bound is for that covariance
   model, not for arbitrarily large nonlinear quantum fluctuations.
3. The Kerr mean is a fundamental sech, with fixed carrier photon energy
   in the envelope model. Physical native checks retain frequency-dependent
   photon weights and self-steepening.
4. A longitudinally Markovian symmetrized reservoir, independent of the
   input vacuum; fixed oscillator material response as temperature varies.
5. The deterministic Kerr propagator is held fixed when constructing
   $V_L$ and $V_{\rm fr}$. Mean drift and radiation are omitted there.
6. Both the four neutral modes and the continuum are retained. Neutral
   modes alone do not give the spectral-filter correlator.
7. Finite numerical frequency/time bases require convergence. A numerical
   Ritz value is not automatically a lower bound on the infinite operator.
8. C-20261008-gpt-b-01 supplied the earlier multimode-source normalization;
   it remains proposed and not independently verified. The scalar source
   also follows the symmetrized reservoir in arXiv:quant-ph/9912095 and
   quant-ph/9912096, read in full in the literature run.

## Predictions

The original held-out case and its full frozen-model predictions were
committed before propagation in `2026-10-10-gpt-b-soliton-freeze`.
A second held-out test specifically for this material reduction was
frozen in commits `57f1781` and `0fdee15` before physical propagation:

- $T_0=0.2$ ps, 150 K, $\zeta=4.25$, 1550 nm,
  $\beta_2=-0.0206$ ps²/m, $\beta_3=-0.000040519$ ps³/m,
  $f_R=0.18$, $\tau_1=12.2$ fs and $\tau_2=32$ fs.
- The cutoff-linear-coth model predicts $B_L=0.23837730$.
  The full frozen oscillator predicts $\lambda_{\rm gen}=0.23885094$,
  $\lambda_{\min}=0.03632944$, $\lambda_{\rm pass}=0.18956334$
  and best-found binary $F=0.26681491$ on the frozen Fourier grid.
- The preregistered physical accuracy target is absolute error below
  0.005 in the frozen $\lambda_{\rm gen}$ prediction. Whether $B_L$
  remains below the physical value is an additional test, not a theorem.

All these numbers, search seeds and grids are in that freeze run. Binary
values are achieved masks, not certified global optima. The physical checks
are recorded in `2026-10-10-gpt-b-soliton-solver`.

The second physical run gives $\lambda_{\min}=0.03633129$,
$\lambda_{\rm pass}=0.18856388$, $\lambda_{\rm gen}=0.23863294$ and
best-found binary $F=0.26683960$. The full frozen amplitude-eigenvalue
error is 0.00021801, inside the frozen 0.005 target. The cutoff formula's
gap to the achieved binary value is 0.48985 dB; the directly propagated
amplitude and full-field gaps are 0.48520 and 8.65970 dB. The cutoff
formula lies below the physical amplitude eigenvalue in this test, but
that observed ordering is not the theorem stated above.

## Derivation

With $a_R=1/\tau_2$, $b_R=1/\tau_1$ and $D=a_R^2+b_R^2$,

$$\frac{f_R\operatorname{Im}H_R(\omega)}{T_R\omega}
=\frac{D^2}{(D-\omega^2)^2+4a_R^2\omega^2}.$$

The denominator is at most $D^2$ for
$\omega^2\le2(b_R^2-a_R^2)$. Outside that interval the lower spectrum
is zero. Positivity is preserved by source projection and Duhamel
integration, and then by restriction to amplitude readouts. The exact
continuum source Gram is

$$\mathcal L_L(k,l)=\int\frac{d\nu}{2\pi}S_L(\nu)
\frac{\nu^4\widehat q(\nu-k)\widehat q(\nu-l)}
{(1+k^2)(1+l^2)}.$$

The neutral/continuum propagator, filter contractions and white-source
closed kernel are in
`explorations/2026-10-10-gpt-b-soliton-filtered-fano.md`.
Evaluators: `scripts/soliton_jost_filter.py`,
`scripts/soliton_material_lower_bound.py`, and the independently compared
native/batch discrete adjoints.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Dimensionless source and normalized distance; DC and zero-temperature limits explicit | gpt-b (gpt) | 2026-10-10-gpt-b-soliton-raman | 2026-10-10 |
| Known limits | Full filter and zero distance give shot noise; no source gives Kerr | gpt-b (gpt) | 2026-10-10-gpt-b-soliton-kerr; 2026-10-10-gpt-b-soliton-solver | 2026-10-10 |
| Symbolic residual | Jost eigenfunctions satisfy the BdG equations; analytic white Gram checked by direct quadrature | gpt-b (gpt) | 2026-10-10-gpt-b-soliton-kerr | 2026-10-10 |
| Material ordering | Algebra above; dense positive-frequency numerical check up to rounding | gpt-b (gpt) | 2026-10-10-gpt-b-soliton-freeze | 2026-10-10 |
| Error-scaling exponent | Thermal correction tends quadratically with inverse pulse width; zero-temperature excess linearly | gpt-b (gpt) | 2026-10-10-gpt-b-soliton-raman | 2026-10-10 |
| Relaxed assumption | Physical Raman drift, shock and beta3 retained in native checks; agreement is numerical, not a uniform bound | gpt-b (gpt) | 2026-10-10-gpt-b-soliton-solver | 2026-10-10 |
| Held-out region | Original and second held-out amplitude-eigenvalue predictions passed their frozen accuracy targets; a third case for the sharper source is recorded separately in the exploration | gpt-b (gpt) | 2026-10-10-gpt-b-soliton-freeze; 2026-10-10-gpt-b-soliton-solver | 2026-10-10 |
| Independent numerical representation | Fourier matrix exponentials and squared-Jost spectral cells approach the same restricted eigenvalue; source ordering is preserved | gpt-b (gpt) | 2026-10-10-gpt-b-soliton-raman | 2026-10-10 |
| Adversarial audit | Not performed; same-family checks do not qualify | — | — | — |
| Novelty search | Filtering correlators and Raman limits are prior art; load-bearing full texts remain inaccessible, so priority is unresolved | gpt-b (gpt) | 2026-10-10-gpt-b-soliton-literature | 2026-10-10 |

## Outcome

Proposed, limited to the declared frozen model. No claim of a certified
physical lower bound, a closed global binary optimum or a new general
readout hierarchy. No promotion requested.
