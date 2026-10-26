---
id: C-20261010-claude-b-03
problem: P-20261010-claude-interactive-01
title: "Raman reservoir floor on lambda_min for a Gaussian in normal dispersion: lambda_min ~ Lambda(Z)/N^2 + 2 c(0) sqrt(Lambda(Z))/N, with c(0) the thermal low-frequency phonon level"
type: scaling-law
status: proposed
proposed_by: claude-b
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-10
updated: 2026-10-10
solver_commit: null
result: null
---

## Statement

**System.** As in C-20261010-claude-b-01, plus the Raman phonon reservoir. The pulse is an unchirped Gaussian, $N^2=\gamma P_0T_0^2/\beta_2$, in normal dispersion, at semiclassical distance $Z=z/\sqrt{L_DL_{NL}}$, with $\Phi=NZ$. The reservoir is the symmetrized (coth) Langevin noise of the Agarwal response, $f_R=0.18$, $\tau_1=12.2$ fs, $\tau_2=32$ fs, at temperature $T$.

**Law.** For $T_0\gtrsim300$ fs, where the pulse bandwidth is well below the Raman band,
$$\lambda_{\min}(V)\simeq\frac{\Lambda(Z)}{N^2}+\rho(Z)\,\frac{\hat c(0)}{\Phi},\qquad \rho(Z)\simeq\sqrt{4Z^2\Lambda(Z)},$$
equivalently
$$\lambda_{\min}\simeq\frac{\Lambda(Z)}{N^2}+\frac{2\hat c(0)\sqrt{\Lambda(Z)}}{N}.$$
- $\Lambda(Z)$ is the Kerr coefficient of C-20261010-claude-b-01.
- $\hat c(0)=4af_Rk_BT/[\hbar(a^2+b^2)]$ with $a=1/\tau_2$, $b=1/\tau_1$. It is the zero-frequency limit of $|{\rm Im}\,h_R(\omega)|\coth(\hbar\omega/2k_BT)$, equal to 0.1148 at 300 K.

**Consequences.**
- The Raman term falls only as $1/N$ at fixed $Z$, so it dominates the Kerr term when $N>\sqrt\Lambda/(2\hat c(0))$, i.e. $\Phi>Z\sqrt\Lambda/(2\hat c(0))\approx3$ at $Z=0.75$.
- At 300 K, the best quadrature squeezing of a Gaussian in normal dispersion, at large $N$, is therefore set by Raman. It is $\lambda_{\min}\approx2\hat c(0)\sqrt{\Lambda(Z)}/N$.
- At fixed $N$ this decreases with $Z$, since $\sqrt\Lambda$ falls from $1/(2Z)$.
- In the dispersionless limit, $\rho\to1$, i.e. $\Delta\lambda_{\min}=\hat c(0)/\Phi$. This is the single-mode estimate: the squeezed quadrature's phase weight $1/(2\Phi)$ squared, times the accumulated phase noise $4\Phi\hat c(0)$.

## Regime

- $5\le N\le20$ ($N=5$ only at $Z=0.76$).
- $0.3\le Z\le3.2$, i.e. $0.3\le z/z_{\rm wb}\le3$.
- $T_0$ = 100 fs to 1 ps. At 100 fs, $\rho$ is 4–9% higher than at 1 ps; at 50 fs, 16% higher at the one point computed.
- $T$ = 300 K.
- Linearized noise; no deterministic delayed Raman response (see Assumptions); no self-steepening.
- Error: within 15% (frozen tolerance); the measured deviations are below.

## Assumptions

1. Everything in C-20261010-claude-b-01 (scalar, single mode, $\beta_2$ only, coherent input, linearized noise), except that the Raman reservoir is included.
2. The reservoir enters as multiplicative phase noise, $dA=i\gamma Am\,dz$, with the coth spectrum of `raman_bath_spectrum.jl` (agents' solver branch `task/T-20261004-gpt-b-02`).
   - In shot-noise units the noise added over $d\xi$ is $4N^2ERE^{\mathsf T}d\xi$. Here $E$ holds the local phase directions times $|u|$, and $R$ is the circulant of $\hat c(\Omega)=|{\rm Im}\,h_R(\Omega/T_0)|\coth(\hbar\Omega/2k_BTT_0)$.
   - $\hbar$ and the photon number drop out.
   - This normalization is validated against FastDifferentiableMMNLO: for the centroid and $\lambda_{\rm gen}$-eigenvector readouts at N10, $z/z_{\rm wb}=0.7$, $T_0=100$ fs, the reservoir parts agree to 0.4% (run `2026-10-10-claude-b.6-solver-weighted-raman`).
3. The deterministic delayed Raman response (Raman shift, gain) is not included in the mean field or the noise map. At $T_0=100$ fs it changes filtered Fano factors by +0.002 to +0.04 (run `2026-10-10-claude-b.6-solver-nd-check`). Its effect on $\lambda_{\min}$ is not computed.
4. Agarwal response parameters and 300 K. Other temperatures enter through $\hat c(0)\propto T$ (thermal part); the zero-point part was not separated.

## Predictions

**Frozen** in commit `bad387c` before computing (`runs/2026-10-10-claude-b-nd-raman/conjecture_predictions.json`). The predictions are $\rho=\sqrt{4Z^2\Lambda(Z)}$, with $\Lambda$ from the $N=200$ reduced curve and tolerance 15%:

| point | $Z$ | predicted $\rho$ | measured $\rho$ ($T_0$ = 1 ps) | deviation |
|---|---|---|---|---|
| N20, $z/z_{\rm wb}=0.3$ | 0.318 | 1.154 | 1.060 | $-8.1\%$ |
| N20, $z/z_{\rm wb}=1.5$ | 1.590 | 1.854 | 1.908 | $+2.9\%$ |
| N10, $z/z_{\rm wb}=3$ | 3.193 | 2.675 | 2.769 | $+3.5\%$ |

All pass (`runs/2026-10-10-claude-b-nd-raman/conjecture_summary.json`).

**Second frozen test** (commit `ff8d25e`; `conjecture2_summary.json`). At $N=28$, $z/z_{\rm wb}=0.7$, $T_0=1$ ps: predicted 1.389, measured 1.311 ($-5.6\%$, tolerance 10%). Pass.

**Points used to form the conjecture** (`summary.json`, `summary_more.json` of the same run; $\rho=\Delta\lambda_{\min}\Phi/\hat c(0)$ at 1 ps):

| point | measured $\rho$ | $\sqrt{4Z^2\Lambda}$ | ratio |
|---|---|---|---|
| N10, $Z=0.32$ | 0.978 | 1.154 | 0.85 |
| N5, $Z=0.76$ | 1.176 | 1.398 | 0.84 |
| N10, $Z=0.75$ | 1.271 | 1.391 | 0.91 |
| N14, $Z=0.74$ | 1.292 | 1.389 | 0.93 |
| N20, $Z=0.74$ | 1.304 | 1.389 | 0.94 |
| N10, $Z=1.60$ | 1.838 | 1.858 | 0.99 |

At $Z\approx0.75$ the ratio rises with $N$: 0.84, 0.91, 0.93, 0.94, 0.944 for $N$ = 5, 10, 14, 20, 28. It appears to level off near 0.95. So the law holds to about 5% at large $N$; whether the limit is exactly $\sqrt{4Z^2\Lambda}$ is not established.

**For the lab.** Take $N=20$, $z=0.7z_{\rm wb}$ in silica at 300 K with $T_0\ge300$ fs. Kerr alone gives $\lambda_{\min}=2.2\times10^{-3}$ ($-26.6$ dB). The law gives $1.29\times10^{-2}$ ($-18.9$ dB), and the oracle with the reservoir at 1 ps gives $1.23\times10^{-2}$ ($-19.1$ dB).

## Derivation

Not derived beyond the dispersionless limit, where the result is $\rho=1$; see Statement.
- **Form.** The form $\rho=\sqrt{4Z^2\Lambda}$ was found by inspection of the six points above, then tested on three frozen points.
- **Interpretation.** A heuristic reading: $2Z\sqrt\Lambda=2Z/\sigma_1(C_Z)$ is the ratio of the dispersionless shear $2Z$ to the actual top singular value of the amplitude-to-phase map. So it measures how much dispersion has reduced the Kerr shear the squeezed mode sees. Why the Raman excess should scale with its first power is not derived.
- **Full notes.** `explorations/2026-10-10-claude-b-semiclassical-normal-dispersion.md`, section 5.3.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | $\hat c(0)$ dimensionless; $\Delta\lambda_{\min}\Phi$ dimensionless | claude-b (claude) | — | 2026-10-10 |
| Known limits | Dispersionless limit $\rho\to1$, the single-mode estimate. Measured $\rho$ = 0.98 (N10) and 1.06 (N20) at $Z=0.32$ | claude-b (claude) | 2026-10-10-claude-b-nd-raman | 2026-10-10 |
| Symmetries | $\lambda_{\rm pass}=\lambda_2$ still holds with the reservoir (parity) | claude-b (claude) | 2026-10-10-claude-b-nd-raman | 2026-10-10 |
| Symbolic residual | Not done | | | |
| Simulation, core regime | Six points ($N$ = 5–20, $Z$ = 0.32–1.6, two pulse widths) | claude-b (claude) | 2026-10-10-claude-b-nd-raman | 2026-10-10 |
| Error-scaling exponent | Not measured: few $N$ per $Z$. At $Z\approx0.75$, $\rho/\sqrt{4Z^2\Lambda}$ = 0.84, 0.91, 0.93, 0.94 for $N$ = 5, 10, 14, 20 | claude-b (claude) | 2026-10-10-claude-b-nd-raman | 2026-10-10 |
| Held-out region | 4 of 4 frozen predictions pass: $-8.1\%$, $+2.9\%$, $+3.5\%$ (tolerance 15%) and $-5.6\%$ at N28 (tolerance 10%). One point is at $Z=3.2$, outside the range used to form the conjecture | claude-b (claude) | 2026-10-10-claude-b-nd-raman | 2026-10-10 |
| Convergence and artefacts | Slice spacing 4/8/16 steps changes $\lambda$'s by $\le3\times10^{-5}$; Kerr part as in C-20261010-claude-b-01 | claude-b (claude) | 2026-10-10-claude-b-nd-raman | 2026-10-10 |
| Second solver or relaxed assumption | Reservoir normalization: solver vs numpy reservoir variance of two weighted readouts agree to 0.4% (N10) and 0.3–1.6% (N20). The deterministic response is not included | claude-b.6 and claude-b (claude) | 2026-10-10-claude-b.6-solver-weighted-raman, 2026-10-10-claude-b-nd-raman | 2026-10-10 |
| Adversarial audit | Not done | | | |
| Novelty search | Raman limits on fibre squeezing are known for solitons and for specific filtered cases (Kärtner et al. 1994; Werner & Friberg; Corney & Drummond, see the problem card). No scaling law of this form for normal-dispersion pulses was found; searches listed in log 2026-10-10_claude-b_T-20261010-claude-interactive-05 | claude-b (claude) | — | 2026-10-10 |

## Outcome

Open.
