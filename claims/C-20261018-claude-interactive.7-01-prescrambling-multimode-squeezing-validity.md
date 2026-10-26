---
id: C-20261018-claude-interactive.7-01
problem: P-20261016-claude-interactive.7-01
title: "Early multimode quadrature squeezing has an inverse-occupation curvature correction; late counting accuracy remains unresolved"
type: noise-formula
status: promoted
proposed_by: claude-interactive.7
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: gpt-b
verifier_model: gpt-6-astra
verifier_family: gpt
audited_by: gpt-b
auditor_model: gpt-6-astra
auditor_family: gpt
created: 2026-10-18
updated: 2026-10-19
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: R-0008
---

## Sharpened statement (cross-family, gpt-b, 2026-10-18)

The cross-family sign-off is restricted to the early quadrature prediction and its measured curvature correction. The original statement below is retained; its exact-Gaussian and unrestricted counting interpretations are not signed off.

For the classical symplectic tangent map $S$, vacuum covariance $V_{\rm lin}=SS^T$, and largest singular value $\sigma_{\max}$,
$$\lambda_{\rm lin}=\sigma_{\max}^{-2},\qquad
\frac{V_{\rm fixed}}{\lambda_{\rm lin}}-1
\simeq (0.0920\pm0.0039)\,\frac{\sigma_{\max}^6}{n_0}.$$
Here $V_{\rm fixed}$ is the nonlinear Wigner variance along the preselected tangent squeezed direction; $n$ is the coherent launch occupation per cell and $n_0=n|a_0|^2$. The coefficient is measured at $E'=0.6$, disorder $\sigma=0.3$, $z=10L_{\rm NL}$, launch 4201/disorder 7601, with between-scramble SE. Its measured occupation exponent is $-0.9947\pm0.0103$ on the frozen $3\times10^5$–$3\times10^6$ scan. It is a trajectory-specific calibration, not a universal coefficient (run `2026-10-18-gpt-b-grin-squeezing`).

The checked early envelope is the original scalar, electronic-Kerr, 15-mode model, $10^6\le n\le10^{10}$, $5\le z/L_{\rm NL}\le20$, $0.55\le f_0\le0.87$, $\sigma=0.3$ ($L_d/L_{\rm NL}=\sigma^{-2}$), and $R=\sigma_{\max}^6/n_0\le0.8$, on the frozen launches. The fixed-direction variance is within 1 dB of the tangent prediction at tested interior points. Here $E'=\sum_pq_p|a_p|^2$, $\sum_p|a_p|^2=1$, and $q_p$ is the mode-group index. The independent launch uses equal energy in groups 1 and 2; the proposer config uses equal power. Consequently some prescribed $E'=0.9$ held-outs lie outside the original $f_0$ bound and are recorded as edge tests.

The exact single-mode large-shear correction is $\Delta V/\lambda_{\rm lin}\sim R/8$; $R=0.8$ is an asymptotic 10% criterion, not an exact Gaussianity boundary. Exact Kerr/Fock and three-mode exchange tests calibrate TWA; no uniform 15-mode quantum error theorem is claimed. The corresponding counting formula $\lambda_{\min}(P_aSS^TP_a^T)$ is a leading approximation, with $P_a$ the local amplitude projection. Pure-SPM number conservation does not establish its robustness under intensity exchange. Late counting and strong-disorder resolution failures are retained in the audit, with fixed and reoptimized weights distinguished.

Independent reports: [audit](notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-01.md), [PI summary](../docs/summary-2026-10-18-gpt-b-C-20261018-claude-interactive.7-01.md). Runs: `2026-10-18-gpt-b-grin-squeezing`, `2026-10-18-gpt-b-kerr-exact`, `2026-10-18-gpt-b-condensate-squeezing`. Initial freeze: `9db4bb6a67b640d79365810a984c3af5c6a9da92`; all subsequent frozen extensions are recorded in run metadata.

## Statement

**Setting.** A coherent CW launch into a graded-index fibre whose $K$ equidistant mode groups exchange power through the resonant Kerr terms. A single coherence cell holds $n$ photons, $\bar n_0$ of them in the fundamental, and $z$ is in units of $L_{\rm NL}$. Before the quantum state scrambles ($z<z_E(n)$), fluctuations about the deterministic classical trajectory obey the classical tangent map $S(z)$. That map gives a Gaussian state with covariance $V=SS^{\rm T}$ (vacuum = 1).

**(a) Photon-counting squeezing.** With mode-resolved photon counts weighted optimally, the noise relative to shot noise is
$$\lambda_{\rm gen}(z)=\lambda_{\min}\big(P_aVP_a^{\rm T}\big),$$
where $P_a$ projects on the amplitude quadratures at the local mean phases. The weights are $w_p=c_p/\sqrt{\bar N_p}$, with $c$ the eigenvector belonging to $\lambda_{\rm gen}$.
- In the 15-mode GRIN model, over the six launch and disorder cases of the reference set, $\lambda_{\rm gen}$ is −1.6 to −4.2 dB at $z=5$, −3.9 to −9.1 dB at 10, −5.3 to −10.7 dB at 20, −10.6 to −14.3 dB at 50, and −11.4 to −17.0 dB at 100 (run `2026-10-16-claude-interactive.7-grin-gaussian-state`).
- The value is **not limited by the curvature of the Kerr crescent**. Photon numbers do not depend on phase, and the curvature is a phase rotation at fixed $|a|$. A truncated-Wigner ensemble on the same trajectory reproduces $\lambda_{\rm gen}$ within 0.5 dB at every checkpoint $z\le100$, at $n=10^{10}$ and also at $n=10^6$. At $n=10^6$ the quadrature squeezing has failed by up to 63 dB (run `2026-10-18-claude-interactive.7-gaussian-validity`, G3).

**(b) Quadrature squeezing.** The tangent map gives the multimode minimum quadrature variance $\lambda_{\rm lin}=1/\sigma_{\max}(z)^2$, where $\sigma_{\max}$ is the largest singular value of $S$. That is −17.3 to −19.3 dB at $z=5$, −23.5 to −25.3 dB at 10, and −29.3 to −31.3 dB at 20 (same run as (a)).
- This describes the true state only while the per-mode shear stays below the curvature scale:
$$\sigma_{\max}(z)^6<0.8\,\bar n_0 .$$
- Beyond that bound the crescent curvature adds roughly $\sigma_{\max}^4/(8\bar n_0)$ to the squeezed direction's variance. The value along the linearized squeezed direction then degrades: in the truncated-Wigner check at $n=10^{10}$ it is −30.8 dB at $z=50$ (linearized −38.5) and −20.6 dB at 100 (linearized −44.1).
- **Withdrawn.** The earlier card statements "−55 to −100 dB by $400L_{\rm NL}$ (ideal)" for multimode squeezing and "−20 to −27 dB at $400L_{\rm NL}$" for photon counting are withdrawn. The first would need $\bar n_0\gtrsim10^{16}$–$10^{30}$ photons per cell. The second is untested beyond $z=100$.

## Regime

- $10^6\le n\le10^{10}$ (tested); $1\le z/L_{\rm NL}\le100$ and $z<z_E(n)$.
- $M=15$ ($K=5$ groups); $f_0\approx0.55$–0.87 ($E'/\kappa N=0.3$–0.9).
- Intra-group disorder $L_d/L_{\rm NL}\approx11$ ($\sigma=0.3$), or none.
- (b) only where $\sigma_{\max}^6<0.8\bar n_0$. For example, at $n=10^{10}$ ($\bar n_0\approx6$–$8\times10^9$, $E'=0.6$) the bound holds at $z=20$ ($\sigma_{\max}^2\approx1100$, $\sigma_{\max}^6/\bar n_0=0.21$) and fails by $z=50$ ($\sigma_{\max}^6/\bar n_0=45$).
- Error in (b) within the bound: the curvature term relative to $\lambda_{\rm lin}$ is about $0.09\,\sigma_{\max}^6/\bar n_0$. The fit is one point: at $n=10^6$, $z=10$ the excess is a factor 3.1 at $\sigma_{\max}^6/\bar n_0=35$.

## Assumptions

1. **Model.** Resonant (beat-averaged) Kerr model with exactly equidistant degenerate groups, a scalar field (one polarization), the exact Hermite–Gauss overlap tensor, and 15 modes.
2. **One cell.** A single CW coherence cell, with no dispersion or walk-off coupling to neighbouring cells.
3. **Ideal detection.** No loss, Raman scattering, GAWBS or detector inefficiency. All 15 modes are resolved ideally, and ideal local oscillators are available for (b).
4. **Input.** Coherent and quantum-limited; no technical noise.
5. **Disorder.** Brownian (white-noise) intra-group disorder at $\sigma=0.3$ ($L_d\approx11L_{\rm NL}$), or none. PR #56 (task T-20261017-claude-interactive.7-02) found this 30–500 times weaker than published estimates.
6. **Approximation.** Linearization about the classical trajectory. Where it fails, truncated Wigner is the reference: its error is $O(1/n)$ on the ballistic branch, checked against exact dynamics on four modes (run `2026-10-16-claude-interactive.7-exact-vs-twa-4mode`). Note that gpt-b's review of C-20261016-claude-interactive.7-02 shows exact one-mode Kerr leaves the Gaussian regime at $s\sim n^{1/6}$, long before coherence collapse.
7. **Realizations.** One launch (phase_seed 1) and one disorder realization (dis_seed 7) for $\lambda_{\rm gen}$ and for the truncated-Wigner check. The six reference cases differ in $E'$ and $\sigma$.

## Predictions

Frozen before verification (2026-10-18). The truncated-Wigner check used $E'=0.6$, $\sigma=0.3$. Everything below is held out.

1. **$E'=0.9$, $\sigma=0.3$, $n=10^{10}$.** Along the tangent map's most-squeezed direction, the Wigner variance is within 1 dB of $\lambda_{\rm lin}$ at $z=5$, 10 and 20, and more than 3 dB above it at $z=50$ and 100.
2. **$E'=0.3$, $\sigma=0.3$, $n=10^8$.** Within 1 dB at $z=5$ and 10; more than 3 dB above at $z=20$ and 50.
3. **Error scaling.** At $E'=0.6$, $\sigma=0.3$, $z=10$, the excess $\lambda_{\rm TWA}/\lambda_{\rm lin}-1$ along that direction scales as $n^{-1}$, with log-log slope $-1.0\pm0.25$ over $n=3\times10^5$–$3\times10^6$.
4. **Photon counting at larger $z$.** At $E'=0.6$, $\sigma=0.3$, $n=10^{10}$, the Wigner photon-number estimate is within 1 dB of the linearized $\lambda_{\rm gen}$ at $z=200$ and 300, below $z_E\approx510$.
5. **Curvature ceiling** (conjecture, not derived for many modes). At $n=10^{10}$ the smallest eigenvalue of the Wigner quadrature covariance of all 15 modes, the best direction at each $z$, stays above −35 dB for every $z\in[5,100]$. The single-mode analogue is $0.945\,\bar n^{-1/3}=-33.6$ dB.

## Derivation

- Linearized state: exploration note §6.5.
- Validity boundary: note §6.11. The crescent's sagitta for a phase-quadrature spread $V'$ on a circle of radius $2\sqrt{\bar n}$ has variance $V'^2/(8\bar n)$. With $V'\approx\sigma_{\max}^2$ and $\lambda_{\rm lin}=1/\sigma_{\max}^2$, the correction is small while $\sigma_{\max}^6\ll8\bar n$.
- Photon numbers: $|a|^2$ is invariant under the phase rotation that produces the crescent, so the linear photon-number fluctuations carry no curvature correction at this order.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Pass. Variances in vacuum units; $\sigma_{\max}^6/\bar n_0$ dimensionless. | claude-interactive.7 (claude) | — | 2026-10-18 |
| Known limits | Pass. Single-mode coherent Kerr: exact Fock evolution gives the best squeezing $0.945\,\bar n^{-1/3}$ (slope −0.337), as the curvature balance predicts. | claude-interactive.7 (claude) | 2026-10-17-claude-interactive.7-condensate-kerr-squeezability | 2026-10-18 |
| Symmetries | Pass. Total photon number has Fano factor 1.000 at every checkpoint. | claude-interactive.7 (claude) | 2026-10-16-claude-interactive.7-grin-gaussian-state | 2026-10-16 |
| Symbolic residual | n/a | | | |
| Simulation, core regime | Proposer family only; does not count. 512-trajectory truncated-Wigner ensemble on the same trajectory, $E'=0.6$, $\sigma=0.3$. **(b)** Within 0.4 dB of $\lambda_{\rm lin}$ wherever $\sigma_{\max}^6<0.8\bar n_0$ ($n=10^{10}$: $z=5$, 10, 20; $n=10^6$: $z=5$); 6–63 dB above it wherever $\sigma_{\max}^6>8\bar n_0$. **(a)** The photon-number $\lambda_{\rm gen}$ is within 0.5 dB at every $z\le100$ for both $n$. The pre-registered G3b, which expected breakdown at $n=10^6$, $z=50$ and 100, failed in this favourable direction. | claude-interactive.7 (claude) | 2026-10-18-claude-interactive.7-gaussian-validity | 2026-10-18 |
| Error-scaling exponent | Pass for the narrowed quadrature correction: exponent -0.9947 ± 0.0103 at fixed z=10; coefficient 0.0920 ± 0.0039 is trajectory-specific. | gpt-b (gpt) | 2026-10-18-gpt-b-grin-squeezing | 2026-10-18 |
| Held-out region | Frozen Eprime=.3 and .9 quadrature predictions pass; actual f0 is reported, and the .9 cases are also outside-f0 edge tests. The late counting prediction is scored separately with paired convergence gates. | gpt-b (gpt) | 2026-10-18-gpt-b-grin-squeezing | 2026-10-18 |
| Convergence and artefacts | Tangent map: $dz=0.02$ and 0.01 agree to 0.01 dB ($\sigma=0$). Wigner variances: bootstrap errors 0.2–0.6 dB. | claude-interactive.7 (claude) | 2026-10-17-claude-interactive.7-condensate-kerr-squeezability; 2026-10-18-claude-interactive.7-gaussian-validity | 2026-10-18 |
| Second solver or relaxed assumption | Truncated Wigner relaxes the linearization; see above. | claude-interactive.7 (claude) | 2026-10-18-claude-interactive.7-gaussian-validity | 2026-10-18 |
| Adversarial audit | Original exact-Gaussian/pre-scrambling interpretation refuted. Pure-SPM count invariance does not prove exchange-model accuracy. Coarse late-count attacks are retained but not accepted without convergence; no universal multimode ceiling proved. | gpt-b (gpt) | 2026-10-18-gpt-b-grin-squeezing; 2026-10-18-gpt-b-kerr-exact | 2026-10-18 |
| Novelty search | First family only. Linearized multimode-fibre quantum noise is in Sloan et al., arXiv:2509.03482 (full text of the theory section, read by a helper agent). Per the helper, it does not state when linearization fails. No statement of the curvature boundary, or of photon-counting robustness beyond it, was found for thermalizing multimode light. | claude-interactive.7 (claude) | — | 2026-10-18 |
| Cross-family core simulation | Independent exact-HG tangent/nonlinear propagation, matched quenched disorder and cross-fitted detectors. Early curvature envelope passes; exact Kerr/Fock benchmarks limit the interpretation. | gpt-b (gpt) | 2026-10-18-gpt-b-grin-squeezing; 2026-10-18-gpt-b-kerr-exact | 2026-10-18 |
| Cross-family convergence/second solver | Fock-cutoff change below 5.6e-11; corrected pinned RK4IP comparison below 1.3e-7 dB. Failed Float32 and tensor-convention pilots retained. Count/strong-noise step failures remain explicit. | gpt-b (gpt) | 2026-10-18-gpt-b-grin-squeezing | 2026-10-18 |
| Cross-family relaxed assumptions | Full nonlinear vacuum ensembles, stronger spatial disorder, changed launch/mode cutoff, and specified distributed loss plus 90% detection. These do not calibrate Raman or physical polarization noise. | gpt-b (gpt) | 2026-10-18-gpt-b-condensate-squeezing; 2026-10-18-gpt-b-grin-squeezing | 2026-10-18 |

## Outcome

**Verified as sharpened:** `cheap-checks-passed` → `sim-verified`. The status covers only the early quadrature statement above. Exact Gaussianity until coherence collapse is refuted; general late counting accuracy and a universal multimode curvature ceiling remain unverified. These blockers are retained in T-20261018-gpt-b-01, so the claim is not marked `audited`. No new claim was filed.

**Promoted (2026-10-19):** `sim-verified` → `promoted`. The sharpened statement (the early quadrature prediction and its measured curvature correction) is the promising result [R-0008](../results/promising/R-0008-early-multimode-squeezing-curvature/RESULT.md), under the PI's decision of 2026-10-19 that cross-family verified claims become promising results. Gate G5 is open: gpt-b's report is a cross-family verification, not a clean-context adversarial audit (T-20261019-claude-interactive.16-01). The Statement above is unchanged.

## Audit trail

| Date | Agent (family/model) | Verdict and status | Evidence |
|---|---|---|---|
| 2026-10-18 | gpt-b (gpt, gpt-6-astra) | Original exact-Gaussian premise refuted; unrestricted curvature-free counting not established. Early quadrature correction and frozen held-outs pass as narrowed; cheap-checks-passed → sim-verified. Original Statement preserved. Coarse counting discrepancies are not accepted counterexamples: the fresh optimized error changes from 2.590 to 0.402dB under the final step refinement. | 2026-10-18-gpt-b-grin-squeezing; 2026-10-18-gpt-b-kerr-exact; linked audit and summary above. |
| 2026-10-19 | claude-interactive.16 (claude, claude-opus-5-5) | `sim-verified` → `promoted`: result R-0008 (promising) written for the sharpened statement. Statement unchanged. G5 open (verification, not a clean-context audit). Record slip found: the auditor fields name gpt-b although no audit was completed (T-20261019-claude-interactive.16-06). | results/promising/R-0008-early-multimode-squeezing-curvature; task T-20261019-claude-interactive-09 |
