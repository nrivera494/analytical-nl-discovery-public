---
id: C-20261018-claude-interactive.7-02
problem: P-20261016-claude-interactive.7-01
title: "Condensate covariance squeezing in the early weak-disorder regime, with an explicit approximation error"
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
result: R-0009
---

## Sharpened statement (cross-family, gpt-b, 2026-10-18)

The retained result is the covariance approximation and the tested early weak-disorder squeezing. It does not assert exact Gaussianity, a unique decomposition into cloud noise, or a universal realization spread.

For the physical fundamental-mode covariance $V=\left(\begin{smallmatrix}V_X&C\\C&V_P\end{smallmatrix}\right)$, with eigenvalues $\lambda_-\le\lambda_+$ and vacuum variance one,
$$\lambda_- = \frac{\det V}{\lambda_+}\simeq\frac{V_X(V_P-C^2/V_X)}{V_P},\qquad
0\le\frac{\det V/V_P}{\lambda_-}-1
=\frac{V_X-\lambda_-}{V_P}\le\frac{V_X}{V_P}.$$
The identity is exact even for non-Gaussian states. $X,P$ are amplitude and phase quadratures in the fundamental's mean-field frame; $V_{P|X}=V_P-C^2/V_X$ is a linear-regression residual, not a post-measurement phase variance or uniquely cloud XPM noise. The approximation errs by at most 0.062 dB in the recorded ensemble (run `2026-10-18-gpt-b-condensate-squeezing`).

The dynamical sign-off is narrower: the scalar 15-mode electronic-Kerr model, $\sigma=0.3$ ($L_d/L_{\rm NL}=11.1$ in our spatial-GUE convention), $5\le z/L_{\rm NL}\le20$, $n=10^{10}$ coherent photons per cell, $0.6\le f_0\le0.87$, and tangent curvature ratio $V_P^2/(8nf_0\lambda_-)\le0.1$. The exact-Hermite–Gauss implementation and frozen nonlinear/held-out tests are independent. This does not establish that those early states have reached an RJ equilibrium.

At $E'=0.3,z=10$, twelve independent disorder paths give a mean −9.487 dB, realization SD 1.651 dB, and mean SE 0.477 dB. At 20, the full ensemble gives −9.547±2.906 dB, but four paths exceed the original upper $f_0$ bound; the eight in-range paths give −7.952±1.978 dB. The latter subset is domain bookkeeping, not an unbiased new population. The independent launch uses equal energy in groups 1 and 2, rather than the proposer's equal power. The frozen fixed-direction curvature scan at 10 gives $\Delta V_{\rm own}\simeq(14826\pm612)/n$, exponent $-0.999928\pm0.000004$, with held-out occupations passing. These are numerical Wigner results with separate exact quantum benchmarks, not an exact 15-mode quantum error bound (same run; propagation in `2026-10-18-gpt-b-grin-squeezing`).

Strong-disorder and later-distance statistics remain separately subject to resolution checks. An SPM reference ratio is not an additive causal percentage. With specified output transmission and detector efficiency both0.9, the exact attenuation rule is $\lambda_{\rm det}=0.19+0.81\lambda$; distributed-loss tests are also recorded. A calibrated polarization/temporal/Raman model is outside this sign-off.

Independent reports: [audit](notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-02.md), [PI summary](../docs/summary-2026-10-18-gpt-b-C-20261018-claude-interactive.7-02.md). Initial freeze: `9db4bb6a67b640d79365810a984c3af5c6a9da92`; extensions and seeds are in run metadata.

## Statement

**Setting.** As in C-20261018-claude-interactive.7-01: a coherent CW launch into the resonant GRIN model (15 modes), before scrambling. The fundamental (condensate) carries $\bar n_0=f_0n$ photons.

**Claim.** The condensate's reduced state is Gaussian, with covariance $\begin{pmatrix}V_X&C\\C&V_P\end{pmatrix}$ in its own amplitude and phase quadratures (vacuum = 1) and symplectic eigenvalue $\nu$. Its smallest quadrature variance is
$$\lambda_{\rm own}=\lambda_{\min}(V)\simeq\frac{\nu^2}{V_P}=\frac{V_X\,V_{P|X}}{V_P},\qquad V_{P|X}=V_P-\frac{C^2}{V_X}.$$
- The condensate's own self-phase modulation supplies 84–91% of $V_P$. The cross-phase noise of the fluctuating excited modes (the cloud) is the part $V_{P|X}$ that is uncorrelated with its photon number, and it sets the level.
- Self-phase modulation alone would give −18 to −38 dB at $z=5$–50 (run `2026-10-17-claude-interactive.7-condensate-kerr-squeezability`, own_squeezing_checks).

**Values** (dB, mean ± SD over realizations; run `2026-10-17-claude-interactive.7-ensemble-squeezing`):

| Case | $z=10$ | 20 | 50 |
|---|---|---|---|
| $f_0\approx0.85$ ($E'=0.3$), $\sigma=0.3$, 12 disorder realizations | −9.6 ± 2.9 | −9.8 ± 3.0 | −8.4 ± 3.9 |
| same, 12 launch draws | −9.1 ± 2.9 | −8.7 ± 3.3 | −8.5 ± 3.3 |
| same, strong disorder $\sigma=1$ ($L_d\approx L_{\rm NL}$), 6 realizations | −8.0 ± 1.1 | −9.4 ± 0.9 | −10.6 ± 1.3 |
| same, $\sigma=3$ ($L_d\approx0.1L_{\rm NL}$), 6 realizations | −7.4 ± 0.5 | −7.1 ± 1.0 | −8.8 ± 1.4 |
| $f_0\approx0.6$–0.77 ($E'=0.6$), disorder seeds / launch draws | −3.7 ± 2.5 / −5.8 ± 2.6 | −5.1 ± 3.4 / −5.8 ± 3.1 | −2.4 ± 2.4 / −1.9 ± 4.1 |

- **Realization dependence.** The value does not self-average at $\sigma=0.3$: the SD is about 3 dB and individual realizations range from −3 to −15 dB. At strong disorder the SD is three to six times smaller.
- **Superseded value.** The earlier single-realization value, −4.9 to −7.9 dB at $z=1$–50 (phase_seed 1, dis_seed 7), was on the weak side.
- **Larger $z$.** By $z=100$ the mean is −4.8 ± 3.2 dB ($\sigma=0.3$), and at 200 it is anti-squeezed on average. At strong disorder the squeezing persists: −8.5 ± 3.1 dB ($\sigma=1$) and −8.7 ± 5.8 dB ($\sigma=3$) at $z=100$.

## Regime

- **Gaussian validity.** The crescent's curvature term $V_P^2/(8\bar n_0)$ must stay below 10% of $\lambda_{\rm own}$, i.e. $\bar n_0>\bar n_0^*(z)=V_P^2/(0.8\lambda_{\rm own})$. Over the 12 realizations ($\sigma=0.3$, $f_0\approx0.85$) the median (maximum) of $\bar n_0^*$ is $1.2\times10^6$ ($3\times10^6$) at $z=10$, $1.8\times10^7$ ($4.6\times10^7$) at 20, and $5\times10^8$ ($3.1\times10^9$) at 50. At $z=100$ it reaches $5.6\times10^9$, so $z=100$ is marginal at $\bar n_0\approx10^{10}$ (run `2026-10-18-claude-interactive.7-gaussian-validity`, thresholds). At $f_0\approx0.6$–0.77 the thresholds are about ten times lower.
- **Other bounds.** $5\le z/L_{\rm NL}\le50$ and $z<z_E(n)$; $M=15$; $f_0\in[0.6,0.87]$; $0.1\le L_d/L_{\rm NL}\le11$.

## Assumptions

1. Model, one-cell restriction, ideal lossless detection and quantum-limited input as in C-20261018-claude-interactive.7-01, assumptions 1–4.
2. **Disorder.** Brownian intra-group disorder at $\sigma=0.3$, 1 and 3. Only $\sigma\gtrsim1.6$ is in the range published for real fibres (Garnier et al., PRA 100, 053835 (2019), arXiv:2011.03918). Polarization and inter-group coupling are absent (task T-20261017-claude-interactive.7-03).
3. **Detection.** Homodyne detection at the optimal angle with a local oscillator phase-locked to the condensate's own mean field. With a laser-referenced local oscillator, 1% laser amplitude jitter turns into 0.2–0.9 rad of condensate phase jitter at $z=10$–50 (run `2026-10-17-claude-interactive.7-condensate-kerr-squeezability`, phase_jitter), which destroys the measurement.
4. **Linearization.** Within the regime above. Where truncated Wigner is the reference: its error is $O(1/n)$ (four-mode exact check, run `2026-10-16-claude-interactive.7-exact-vs-twa-4mode`). It captures the classical crescent curvature. It fails only in the few-quanta regime $E'\lesssim E'_{\rm vac}$, which is irrelevant at $\bar n_0\sim10^{10}$.

## Predictions

Frozen before verification (2026-10-18). None of these parameters were run.

1. **$E'=0.45$** ($f_0\approx0.8$), $\sigma=0.3$, 12 disorder realizations: the ensemble mean of $\lambda_{\rm own}$ at $z=10$ and 20 lies in $[-11,-6]$ dB, with a realization SD of at least 1.5 dB.
2. **$\sigma=2$** ($L_d\approx0.25L_{\rm NL}$), $E'=0.3$, 6 realizations: the ensemble mean at $z=20$ and 50 lies in $[-11,-6]$ dB, with an SD of at most 1.5 dB.
3. **Truncated Wigner at lower $n$** (the reference realization, $E'=0.3$, $\sigma=0.3$). At $n=10^8$, 512 trajectories reproduce the tangent-map value within 1 dB at $z=10$ and 20. At $n=10^6$ they deviate by more than 1 dB at $z=20$ and 50, where $\bar n_0<\bar n_0^*$.
4. **The formula** $V_XV_{P|X}/V_P$ is within 0.3 dB of the exact minimum eigenvalue at every $z\ge5$ in every realization of the 12-member ensemble.

## Derivation

Exploration note §6.8 and §6.10; checks in run `2026-10-17-claude-interactive.7-condensate-kerr-squeezability` (own_squeezing_checks).
- For an elongated ellipse, $\lambda_{\min}=\det V/\lambda_{\max}\approx\nu^2/V_P$.
- The single-mode self-phase reference with the condensate's accumulated phase $\Phi_{\rm self}=\int_0^z|A_0|^2dz'$ has $V_P=1+4\Phi^2$.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Pass. Vacuum units throughout. | claude-interactive.7 (claude) | — | 2026-10-18 |
| Known limits | Pass. Self-phase only: $V_P=1+4\Phi_{\rm self}^2$ accounts for 84–91% of the computed $V_P$. | claude-interactive.7 (claude) | 2026-10-17-claude-interactive.7-condensate-kerr-squeezability | 2026-10-17 |
| Symmetries | n/a | | | |
| Symbolic residual | Pass. $V_XV_{P|X}/V_P$ matches the exact minimum within 0.3 dB for $z\ge2$ (one realization). | claude-interactive.7 (claude) | 2026-10-17-claude-interactive.7-condensate-kerr-squeezability | 2026-10-17 |
| Simulation, core regime | Proposer family only; does not count. Over 12 disorder realizations and 12 launch draws the values are those above. Pre-registered Q1–Q3 failed in the direction of more squeezing and more realization dependence than predicted; Q5 (strong disorder within 3 dB) passed. | claude-interactive.7 (claude) | 2026-10-17-claude-interactive.7-ensemble-squeezing | 2026-10-17 |
| Error-scaling exponent | Fixed-direction Wigner curvature excess: -0.999928 ± 0.000004 at z=10, with coefficient 14826 ± 612 divided by total occupation; held-out occupation errors below 0.059%. This is not TWA quantum truncation error. | gpt-b (gpt) | 2026-10-18-gpt-b-condensate-squeezing | 2026-10-18 |
| Held-out region | Eprime=.45 mean/spread and lower-n departure predictions pass. Sigma 2,z50 literal six-path SD gate fails (1.616 dB versus 1.5 dB); its continuum limit remains unresolved. | gpt-b (gpt) | 2026-10-18-gpt-b-condensate-squeezing; 2026-10-18-gpt-b-grin-squeezing | 2026-10-18 |
| Convergence and artefacts | Pass. $dz=0.02$ and 0.01 agree to 0.01 dB ($\sigma=0$). | claude-interactive.7 (claude) | 2026-10-17-claude-interactive.7-condensate-kerr-squeezability | 2026-10-17 |
| Second solver or relaxed assumption | Proposer family only; does not count. 768-trajectory truncated Wigner at $n=10^{10}$ with full nonlinear propagation, one realization: −5.1, −6.1, −6.0, −8.1, −5.7, −5.6, −1.0 dB (±0.2–0.25) against the tangent map's −4.9, −5.7, −5.7, −7.9, −5.8, −5.6, −1.4 dB at $z=1$–100. | claude-interactive.7 (claude) | 2026-10-17-claude-interactive.7-condensate-kerr-squeezability | 2026-10-17 |
| Adversarial audit | Covariance approximation passes; unique cloud-noise attribution and universal spread rejected. Weak early paths converge; later strong paths require further resolution. Four z20 core paths exceed the original f0 upper bound. | gpt-b (gpt) | 2026-10-18-gpt-b-condensate-squeezing | 2026-10-18 |
| Novelty search | First family only. Kerr squeezing of a self-cleaned beam's fundamental by its own propagation was not found in the searched literature (card, literature state). | claude-interactive.7 (claude) | — | 2026-10-18 |
| Cross-family core simulation | Weak-disorder z10 mean -9.487 dB, realization SD 1.651 dB; nonlinear and tangent ensembles are compared pathwise. Full z20 ensemble and the in-range subset are separately reported. | gpt-b (gpt) | 2026-10-18-gpt-b-condensate-squeezing | 2026-10-18 |
| Cross-family covariance algebra | Exact Schur-complement/eigenvalue relation; maximum recorded approximation error0.062 dB. No Gaussianity or causal cloud decomposition follows from this identity. | gpt-b (gpt) | 2026-10-18-gpt-b-condensate-squeezing | 2026-10-18 |
| Cross-family relaxed assumptions | Exact small quantum references and nonlinear Wigner evolution; strong disorder, launch ensembles, output/detection attenuation and distributed vacuum loss. Calibrated silica Raman remains outside the model. | gpt-b (gpt) | 2026-10-18-gpt-b-condensate-squeezing; 2026-10-18-gpt-b-grin-squeezing | 2026-10-18 |

## Outcome

**Verified as sharpened:** `cheap-checks-passed` → `sim-verified`. The status applies only to the covariance approximation and specified early weak-disorder ensemble. The broad mean/spread and unique cloud-noise interpretation are not signed off. Strong-disorder convergence and physical calibration remain open in T-20261018-gpt-b-02, so the claim is not marked `audited`. No new claim was filed.

**Promoted (2026-10-19):** `sim-verified` → `promoted`. The sharpened statement (the covariance identity and the early weak-disorder squeezing) is the promising result [R-0009](../results/promising/R-0009-condensate-squeezing-covariance-identity/RESULT.md), under the PI's decision of 2026-10-19 that cross-family verified claims become promising results. Gate G5 is open: gpt-b's report is a cross-family verification, not a clean-context adversarial audit (T-20261019-claude-interactive.16-01). The Statement above is unchanged.

## Audit trail

| Date | Agent (family/model) | Verdict and status | Evidence |
|---|---|---|---|
| 2026-10-18 | gpt-b (gpt, gpt-6-astra) | Covariance approximation and early weak-disorder squeezing verified as sharpened; cheap-checks-passed → sim-verified. Original universal spread interpretation rejected; the literal sigma=2,z=50 spread prediction fails, with continuum uncertainty retained. Unique cloud attribution is unsupported. Even the final sigma=3,z=20 step comparison changes the mean by 0.378dB versus a0.3dB tolerance. Original Statement preserved. | 2026-10-18-gpt-b-condensate-squeezing; 2026-10-18-gpt-b-grin-squeezing; linked audit and summary above. |
| 2026-10-19 | claude-interactive.16 (claude, claude-opus-5-5) | `sim-verified` → `promoted`: result R-0009 (promising) written for the sharpened statement. Statement unchanged. G5 open (verification, not a clean-context audit). Record slip found: the auditor fields name gpt-b although no audit was completed (T-20261019-claude-interactive.16-06). | results/promising/R-0009-condensate-squeezing-covariance-identity; task T-20261019-claude-interactive-09 |
