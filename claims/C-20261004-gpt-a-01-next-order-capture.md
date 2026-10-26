---
id: C-20261004-gpt-a-01
problem: P-002
title: "A three-mode response expansion predicts finite-distance weak-LP02 retention to next order"
type: asymptotic-solution
status: cheap-checks-passed
proposed_by: gpt-a
proposer_model: gpt-6-astra
proposer_family: gpt
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-04
updated: 2026-10-04
solver_commit: 9c1288712ea9cd7ef858d4e6dff9dea350e9291a
result: null
---

## Statement

Consider the rotating-wave scalar radial-mode Kerr system, normalized to the LP01 fundamental soliton $u=f e^{i\zeta/2}$, $f=\operatorname{sech}\tau$. Launch $(a_1,a_2,a_3)=(f,\sqrt r f,0)$, where $r=E_{02}/E_{01}$ and $p_2=r/(1+r)$. The proposed expansion is

$$a_1=u+rU+O(r^2),\qquad a_2/\sqrt r=v+rV+O(r^2),\qquad a_3=r w+O(r^2).$$

Define $D_j=\tfrac12 b_j\partial_\tau^2+i\delta_j\partial_\tau+\mu_j$, with $(b_1,\delta_1,\mu_1)=(1,0,0)$ and $\mu_2=0$. Write $\sigma=2S_{12}/S_{11}$, $\alpha_2=S_{22}/S_{11}$, $\sigma_{13}=2S_{13}/S_{11}$ and $\kappa=S_{1223}/S_{11}$. The coefficients are the unique solutions of the triangular response equations

$$i v_\zeta+(D_2+\sigma|u|^2)v=0,$$
$$i U_\zeta+\tfrac12 U_{\tau\tau}+2|u|^2U+u^2U^*+\sigma|v|^2u=0,$$
$$i w_\zeta+(D_3+\sigma_{13}|u|^2)w+\kappa v^2u^*=0,$$
$$i V_\zeta+(D_2+\sigma|u|^2)V+
 \sigma(u^*U+uU^*)v+\alpha_2|v|^2v+2\kappa u w v^*=0,$$

with $(v,U,w,V)|_{\zeta=0}=(f,0,0,0)$. This keeps minority self-phase, pump back-action and generated LP03 on the same perturbative order. It is a response calculation without a fitted finite-admixture coefficient.

The measurable retained fraction is explicitly the **reference bound-channel projection**

$$B(r,\delta,\zeta)=\frac{|\langle\psi,a_2\rangle|^2}{2r}
 =B_0+rB_1+O(r^2),\qquad
 B_1=\operatorname{Re}\{\langle\psi,v\rangle^*\langle\psi,V\rangle\},$$

where $\psi=e^{-i\delta\tau/b_2}\operatorname{sech}^{\nu}\tau/\sqrt{I(2\nu,0)}$, $\nu(\nu+1)=2\sigma/b_2$ and $I(a,k)=2^{a-1}|\Gamma((a+ik)/2)|^2/\Gamma(a)$. Thus $B_0=I(\nu+1,\delta/b_2)^2/[2I(2\nu,0)]$ is independent of distance. In the ideal LP02 case it is $[\pi\delta/(2\sinh(\pi\delta/2))]^2$. A fixed time gate has the separate formula $W=W_0+r\operatorname{Re}\int_{-5}^{5}v^*V\,d\tau+O(r^2)$, with $W_0=\tfrac12\int_{-5}^{5}|v|^2d\tau$; it must not be replaced by $B_0$.

For a fixed retained-fraction criterion $q$ with $B_0'(\delta_q^{(0)})\ne0$,

$$\delta_q(r;\zeta)=\delta_q^{(0)}
 -r\,\frac{B_1(\delta_q^{(0)},\zeta)}{B_0'(\delta_q^{(0)})}+O(r^2).$$

We choose $q=1/2$ before testing. This is an operational retention boundary, **not** a boundary beyond which all minority energy is untrapped. The literal zero-capture boundary requested by the task does not follow from a regular expansion on a bounded walk-off interval: $B_0>0$ at every finite $\delta$. Infinite-distance depletion or a walk-off growing with $1/r$ is a different, unresolved limit.

At ideal zero walk-off, $L_3=\tfrac12\partial_\tau^2+\tfrac34f^2$ gives the useful specialization

$$w=f e^{i\zeta/2}-e^{iL_3\zeta}f,\qquad
B=1-rK(\zeta)+O(r^2),\qquad K=\|w\|_2^2,\quad 0\le K\le8.$$

This bounded, oscillatory correction is incompatible with interpreting the conservative short-distance dynamics as a universal irreversible exponential capture law.

There is also an explicit detuning bound on this zero-walk-off coefficient. For $\mu\le0$, let $H=L_3+\mu$, $\nu_3=(\sqrt7-1)/2$, $\lambda_3=\nu_3^2/2$, $d=1/2-\lambda_3$ and $b^2=I(\nu_3+1,0)^2/I(2\nu_3,0)$. Then

$$w_\mu=\kappa(e^{i\zeta/2}-e^{iH\zeta})(1/2-H)^{-1}f^3,$$
$$K_b=\frac{4d^2b^2}{(d-\mu)^2}\sin^2((d-\mu)\zeta/2),$$
$$0\le K_\mu-K_b\le\min\left\{4(2-b^2),\frac{4\kappa^2(16/15)-4d^2b^2}{(1/2-\mu)^2}\right\}.$$

The proof projects onto the single LP03 temporal bound state and its orthogonal continuum. This bounds the leading coefficient at every distance and implies $K_\mu=O(|\mu|^{-2})$ for large negative mismatch. The full-field small-$r$ remainder is still asserted only on the compact domain below; no uniform two-parameter remainder as $\mu\to-\infty$ is claimed. This corollary had a separate prediction freeze after the main comparisons, before its own checks (`2026-10-04-gpt-a-nextorder-detuning-prediction`).

## Regime

The assertion is asymptotic as $r\to0$ on the compact domain $0\le\zeta\le20$, $0\le\delta\le1.6$, $-0.02\le\sigma-1\le0$, $1\le b_2\le1.02$, $1\le b_3\le1.04$, $0\le\delta_3\le3.5$, and $-50\le\mu_3\le0$. The ideal overlap values are $\alpha_2=1/2$, $\sigma_{13}=3/4$, $\kappa=1/4$; the remaining rotating-wave overlaps are the analytical GRIN values. The preregistered comparison domain was $0<r\le0.003$, hence $p_2\le0.003/1.003$; the completed held-out grid samples $r=0.0002,0.0006,0.002$ (`2026-10-04-gpt-a-nextorder-full`). The upper domain limit is not a proved uniform numerical error constant, and the completed grid does not test every point in that domain.

The minority-normalized field and retained-fraction errors after the correction are $O(r^2)=O(\varepsilon^4)$, versus $O(r)$ before it. Pump and LP03 field remainders are $O(r^2)$. Coefficients can vanish at special parameters. No estimate uniform at $\zeta\sim1/r$, in an infinite-distance scattering limit, or across a vanishing spectral gap is asserted. The stated coefficient range has a single LP02 temporal bound state because $\sigma/b_2\le1$.

## Assumptions

- A prescribed fundamental sech LP01 input and a weak coherent, co-launched LP02 copy; no initial LP03 for the capture claim. The phase experiment uses a separately stated seeded input.
- Scalar, axisymmetric, deterministic propagation; ideal radial overlap integrals. The archive's analytical GIF625 calibration is a physical reference, not a measured index profile.
- Rotating-wave spatial coupling; the affine part of carrier propagation constants has been removed. The residual $\mu_3$ is retained, including the archive value. Equal carrier spacing is not assumed in the general formula.
- Only second-order chromatic dispersion. Raman, self-steepening, attenuation, gain and random mode coupling are absent. Their dimensionless strengths are zero in this claim; finite neglected strengths add model error and are not absorbed into the $O(r^2)$ remainder.
- LP03 is needed at this order. An initially empty LP04 first appears at $O(\varepsilon^3)$ and feeds LP02 at $O(\varepsilon^5)$, so a four-mode run is an appropriate relaxation check.
- The projection uses the specified *reference* pulse and frequency phase. It is not an instantaneous nonlinear eigenmode fit, nor the asymptotic energy of all parts of a Raman-shifting real pulse.

## Predictions

Freeze the response equations, full nonlinear comparison grid and fourth-power error before the new nonlinear runs. The earlier task's grid and outcomes are disclosed in [the derivation note](../explorations/2026-10-04-gpt-a-next-order-capture.md); they are not held out here.

New held-out launch ratios are $r\in\{0.0002,0.0006,0.002\}$. New walk-offs are $\delta\in\{0.35,0.85,1.35\}$, with a zero-walk-off identity check, and output planes $\zeta\in\{7,13,19\}$. All three ratios and all three nonzero ideal walk-offs were absent from the preceding exploration. Additional checks retain actual archive modal dispersion and use $(\sigma,b_2,b_3,\delta_3,\mu_3)=(0.98,1.015,1.03,2.1\delta,-10)$.

The functional prediction freeze is commit `751cddf`; the numerical table is commit `6d5b1ff`, pushed before the full nonlinear production runs. At $\zeta=13$, the frozen prediction is

$$\delta_{1/2}(r)=0.949476098481-1.446486251515r+O(r^2)
=0.949476098481-1.446486251515p_2+O(p_2^2).$$

Its numbers trace to `2026-10-04-gpt-a-nextorder-prediction`. The full solver evaluated the predicted level set without fitting its coefficient; the expected residual exponent was 4 against $\varepsilon=\sqrt r$. The source-ablation and phase predictions are in the linked exploration. The supplemental detuning intervals were frozen in `8cb0b5b`, with the later design disclosed; they were not part of the original preregistration.

## Derivation

Substitution and collection of powers of $\varepsilon$ produce the hierarchy. Its field remainders follow from smooth finite-time dependence of the cubic one-dimensional evolution on its initial amplitudes and the rotating-wave phase selection. The independent symbolic check expands the full three-mode cubic polynomial, including the conjugate terms.

The projection formula is the cross term in $|\langle\psi,v+rV\rangle|^2/2$. The boundary formula is the implicit-function expansion at a simple level crossing. At zero walk-off, $(1/2-L_3)f=(1/4)f^3$ solves the forced LP03 equation explicitly; the Manley–Rowe identity $N_2+2N_3=2r$ then gives $B_1=-\|w\|^2$. Self-phase and pump back-action remain in the field equations even though their first-order projection-probability contributions vanish in this special case.

Novelty is limited to the proposed GRIN-specific next-order coefficient and its predictive domain. Weak-probe trapping, vector locking, perturbation theory and phase-sensitive four-wave mixing are established ideas. The two required papers were read in full; details and access qualifications are in the exploration. This is not yet an independently verified claim.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units, order counting and symbolic residual | All three cubic coefficient residuals vanish; finite-time argument uses the rescaled variables | gpt-a (gpt) | `2026-10-04-gpt-a-nextorder-prediction` | 2026-10-04 |
| Proposer's held-out comparison | Minority-field error exponents 3.99635–4.00076; projection 3.98844–4.00936; gate 3.98829–4.04554. Before correction, field exponents 1.99408–2.00087 | gpt-a (gpt) | `2026-10-04-gpt-a-nextorder-full` | 2026-10-04 |
| Half-retention level set | Criterion residual exponent 3.99724; residual magnitude at the largest tested ratio is $5.25024\times10^{-5}$ | gpt-a (gpt) | `2026-10-04-gpt-a-nextorder-boundary` | 2026-10-04 |
| Source ablation | Removing any of self-phase, pump response or LP03 returns field-error exponents to 1.99808–2.03549; projection cancellation obscures a pure exponent for the weakest source on this grid | gpt-a (gpt) | `2026-10-04-gpt-a-nextorder-response-checks` | 2026-10-04 |
| Conservation and numerical edges | Total-energy drift at most $2.35\times10^{-12}$; temporal edge fraction at most $1.97\times10^{-13}$ | gpt-a (gpt) | `2026-10-04-gpt-a-nextorder-full` | 2026-10-04 |
| Refinements at $r=0.002$ | Ideal projection changes: half-step $1.94\times10^{-11}$, double window $1.10\times10^{-14}$, double resolution $7.78\times10^{-16}$; fourth-mode change $4.18\times10^{-7}$. Endpoint-corrected gate resolution change $3.19\times10^{-7}$ | gpt-a (gpt) | `2026-10-04-gpt-a-nextorder-convergence` | 2026-10-04 |
| Dispersion and overlap perturbation | Full next-order exponents remain near four for the perturbed and archive-dispersion cases; archive half-step projection change $9.85\times10^{-13}$ | gpt-a (gpt) | `2026-10-04-gpt-a-nextorder-full`, `2026-10-04-gpt-a-nextorder-convergence` | 2026-10-04 |
| Detuning bound | Every supplemental response value lies in its frozen interval; full LP03 energy-error exponents 5.93122–6.05528, predicted six | gpt-a (gpt) | `2026-10-04-gpt-a-nextorder-detuning-response`, `2026-10-04-gpt-a-nextorder-detuning-full` | 2026-10-04 |
| Phase symmetry and initial flux | Two-mode launch symmetry holds to roundoff; seeded opposite quadratures give opposite initial flux in ideal and archive-dispersion cases | gpt-a (gpt) | `2026-10-04-gpt-a-nextorder-phase` | 2026-10-04 |
| Independent verification and audit | Required, not performed by proposer | — | — | — |

## Outcome

Cheap checks passed; all numerical comparisons here were run by the proposer and do not constitute independent verification. `T-20261004-gpt-a-03` assigns that work to Claude. No result folder is created.

The literal infinite-distance zero-capture threshold remains unresolved and is not relabeled as the finite-distance half-retention criterion. `T-20261004-gpt-a-04` records this missing part of the parent task, which remains open. Novelty of the specific correction still needs a second-family audit.
