---
id: C-20261018-claude-interactive.7-03
problem: P-20261016-claude-interactive.7-01
title: "Displaced-thermal Kerr squeezing, the conditional phase-invariant no-go, and the readout-dependent Sagnac floor"
type: bound
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
result: R-0010
---

## Sharpened statement (cross-family, gpt-b, 2026-10-18)

The direct-stage law is verified for a **displaced thermal input**, not for every Gaussian covariance satisfying the original two inequalities. For $H=\chi\hat N(\hat N-1)/2$, displacement photons $n_d=|\alpha|^2$, input covariance $V=\nu I$ (vacuum=1), and fixed $\nu$, minimizing on the early shear branch $s=\chi n_dz=O(n_d^{1/6})$ gives
$$\lambda_* = \frac{3}{2\,4^{1/3}}\left(\frac{\nu^4}{n_d}\right)^{1/3}
[1+O_\nu(n_d^{-1/3})],\qquad
\chi n_d z_*=(n_d/(16\nu))^{1/6}[1+O_\nu(n_d^{-1/3})].$$
The mean photon number is $n_d+(\nu-1)/2$; replacing $n_d$ by it adds relative $O(\nu/n_d)$ error. Exact moment and independent Fock checks support the asymptotics. The coefficient checks cover $1\le\nu\le30$, $10^8\le n_d\le10^{12}$, with maximum relative error 0.412%. The measured $n_d$ exponent at $\nu=10$ is −0.334621 and the relative asymptotic-error exponent is −0.328378. All nine original displaced-thermal held-outs pass within 0.218 dB (run `2026-10-18-gpt-b-kerr-exact`).

The no-go is exact **conditional on phase invariance**:
$$[\rho,\hat N]=0\quad\Longrightarrow\quad
U_{\rm Kerr}\rho U_{\rm Kerr}^\dagger=\rho,\qquad
\operatorname{Var}X_\theta=1+2\langle\hat N\rangle.$$
Global phase averaging of the preparation is sufficient; loss of first-order coherence or the label “scrambling” alone is not. This single-mode statement does not prohibit a two-mode, number-conserving interferometric measurement with a vacuum ancillary input.

The Sagnac $\varepsilon^2$ term is a leading small-power-jitter contribution for a specified readout, not an exact universal floor. This sign-off retains the original coherent-shot pump assumption; the fixed-number calculations in the audit are reference checks, not a promoted extension to arbitrary extracted quantum inputs. Here $\varepsilon$ is the relative RMS incident-power variation. A dark quadrature with an external phase-tracking LO and a number-difference measurement using the bright output as its quantum reference have different curvature corrections. Raw mean-shot-noise normalization and per-shot power rescaling also differ. The exact-reference grid uses $n_a\in\{5\times10^9,10^{10}\}$ photons per arm, $\Phi\in\{3,10,30,60\}$, and actual $\varepsilon^2\le0.002709$; the largest phase and the slightly larger Dirichlet RMS are edge tests. The retained asymptotic interpretation requires small jitter and large shear, $\varepsilon\ll1$, $1\ll\Phi$, $\Phi^2/n_a\ll1$; no finite 1% bound over that rectangle is asserted. The audit reports exact, Fock and Wigner checks separately. A Dirichlet distribution of prepared pump powers is not automatically the intrinsic photon-number distribution of a single thermalized output.

At $\Phi=30$, the exact quantum bright-reference baseline is −35.565 dB and the prepared Dirichlet ensemble gives −25.409 dB; independent TWA differs by 0.0067 dB. The original Sagnac dB prediction passes. The separate raw-normalization 1% bound fails at an interior Gaussian-jitter point ($\varepsilon=0.05099$, $\Phi=3$: 1.135% error). The Dirichlet case gives a 3.609% formula error at 30, with actual RMS 0.05204 just outside the original 0.052 bound. Per-shot power rescaling is a distinct calibrated estimator and passes its own frozen 1% check. The floor is retained as a leading small-jitter term with an explicit reference and normalization, not as a universal finite-error guarantee (same run).

The input-state classification and finite readout qualifications matter: a smooth super-Poissonian number distribution need not have a nonnegative Glauber–Sudarshan $P$, although a nonnegative-$P$ certificate is not necessary for the number-conserving Sagnac observable. The generic-Gaussian and automatic-scrambling extensions are not part of the sign-off. The coherent coefficient is published prior art, DOI **10.1016/j.optcom.2023.129717** (full text, relevant theory/conclusions); the phase-invariance premise appears explicitly in DOI **10.1103/PhysRevA.100.053811**, arXiv **1905.05756** (full text, Kerr-modulation section). The bounded mixed-law novelty search is not a novelty clearance.

Independent reports: [audit](notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-03.md), [PI summary](../docs/summary-2026-10-18-gpt-b-C-20261018-claude-interactive.7-03.md). Main run: `2026-10-18-gpt-b-kerr-exact`; actual extracted-Wigner tests: `2026-10-18-gpt-b-condensate-squeezing`. Initial freeze: `9db4bb6a67b640d79365810a984c3af5c6a9da92`. The solver pin records a classical cross-check; the quantum moment/Fock oracle is independent.

## Statement

**Setting.** The fundamental mode (the condensate, $\bar n_0$ photons per coherence cell) is extracted after the thermalization fibre. It is then sent through a lossless single-mode Kerr stage of nonlinear phase $\Phi$, and measured either by homodyne detection referenced to its own mean field or in a balanced Sagnac loop.

**(i) Direct Kerr stage on a Gaussian condensate.** Take the condensate state with covariance $V$ (vacuum = 1) and symplectic eigenvalue $\nu$. Linearized, the stage acts as the shear $P\to P+2\Phi X$. Including the crescent curvature,
$$\lambda(\Phi)\simeq\lambda_{\min}\!\big[K(\Phi)VK(\Phi)^{\rm T}\big]+\frac{V'(\Phi)^2}{8\bar n_0},\qquad V'=V_P+4\Phi C+4\Phi^2V_X .$$
Optimized over $\Phi$, this gives
$$\lambda_{\rm best}\simeq0.945\left(\frac{\nu^4}{\bar n_0}\right)^{1/3}\qquad\text{when } V_P<(4\bar n_0\nu^2)^{1/3}.$$
- **Ensemble values.** For the condensate at $f_0\approx0.85$ with $\sigma=0.3$ (12 disorder realizations), $\nu$ has geometric mean 5.8, 34 and 102 at $z=10$, 50 and 100 $L_{\rm NL}$ (geometric SD factor 1.4–1.5). At $\bar n_0=10^{10}$ that gives $\lambda_{\rm best}$ = −23.4 ± 1.9, −13.2 ± 2.5 and −6.8 ± 2.3 dB. At $z=200$, 9 of 12 realizations stay above −1 dB (run `2026-10-17-claude-interactive.7-ensemble-squeezing`). The value self-averages to within about 2 dB.
- **Phase needed.** The ensemble median $\Phi$ for −10 dB is 0.2 rad at $z=10$ and 13 rad at $z=50$, with ranges 0–6 and 0–136 rad. A coherent state of the same photon number needs 1.4 rad; its own limit is −33.6 dB at $\bar n_0=10^{10}$.

**(ii) No-go for Fock-diagonal states** [exact]. Suppose the condensate's reduced state is phase-invariant, $\rho=\sum_np_n|n\rangle\langle n|$. This happens after quantum scrambling, or for an ensemble of phase-randomized launches.
- Every Kerr (number-diagonal) unitary leaves $\rho$ unchanged.
- ${\rm Var}\,X_\theta=1+2\langle n\rangle\ge1$ at every angle $\theta$.

**(iii) Balanced Sagnac squeezer.** Let the pump's power vary from shot to shot by a relative RMS $\varepsilon$, with each shot coherent. To first order in $\varepsilon$, the dark-port variance at the angle optimal for the mean pump is
$$V_{\min}(\Phi)+\varepsilon^2 .$$
The pump's own phase noise and mixedness cancel between the two arms.
- A Dirichlet-thermalized condensate has $\varepsilon^2={\rm Var}\,I_0/\langle I_0\rangle^2=(2.60\pm0.35)\times10^{-3}$. The floor is then −25.9 dB on average, ranging from −27.2 to −25.0 dB over 12 realizations; the closed form gives −25.7 dB (run `2026-10-17-claude-interactive.7-ensemble-thermalization`).
- For 2% pump power jitter the floor is −34 dB.
- A phase-randomized condensate with a smooth super-Poissonian number distribution is a mixture of coherent states, so (iii) applies to it as well.

## Regime

- **Photon number and input.** $\bar n_0\ge10^8$, with the input Gaussian-valid: $V_P^2<0.8\lambda_{\rm in}\bar n_0$. Inputs outside this bound are already non-Gaussian, and (i) is then pessimistic by 1–6 dB (G1 at $\bar n_0=10^8$).
- **Mixedness.** $1\le\nu\le200$.
- **Kerr phase.** $\Phi$ up to $\Phi_{\rm opt}\approx30$–70 at $\bar n_0=10^{10}$.
- **Sagnac.** (iii) requires $\varepsilon\ll1$ and $\Phi\gtrsim3$.
- **Error.** (i) agrees with the classical Wigner map within 0.7 dB at $\bar n_0=10^{10}$ for nine condensate inputs, and within 0.15 dB for the $z=10$ inputs at $10^8$. (iii) holds within 1% for $\varepsilon\le0.052$ and $\Phi=3$–30.

## Assumptions

1. **Ideal stage.** Lossless and single-mode, with no dispersion, Raman scattering or GAWBS. Detection is ideal.
2. **Input.** For (i), the linearized condensate state of C-20261018-claude-interactive.7-02, which carries that claim's model assumptions (15-mode resonant GRIN, Brownian disorder at $\sigma=0.3$ for the $\nu$ values).
3. **Curvature term.** It assumes Gaussian phase statistics. It is checked exactly (Fock) only for $\nu=1$, and by the classical Wigner map for $\nu>1$.
4. **Sagnac.** For (iii): the Sagnac loop is perfectly balanced, the treatment is linear in $\varepsilon$ and in the fluctuations, and only the pump power fluctuates between shots.

## Predictions

Frozen before verification (2026-10-18). Held out: no exact displaced-thermal calculation and no Sagnac simulation was run.

1. **Exact displaced-thermal test.** Exact single-mode Kerr evolution (Fock basis) of a displaced thermal input with $V_X=V_P=\nu\in\{3,10,30\}$ and $\bar n\in\{10^4,10^5,10^6\}$. The best quadrature variance over $\Phi$ is within 1 dB of $0.945(\nu^4/\bar n)^{1/3}$ wherever $\nu<(4\bar n\nu^2)^{1/3}$.
2. **Scaling with photon number.** At fixed $\nu=10$, $\lambda_{\rm best}$ scales as $\bar n^{-1/3}$, with log-log slope $-0.333\pm0.03$ over $\bar n=10^6$–$10^{10}$ (classical Wigner map or exact).
3. **Sagnac.** A truncated-Wigner simulation of a balanced fibre Sagnac pumped by coherent pulses whose powers follow the Dirichlet law of the condensate (relative variance $2.6\times10^{-3}$) gives a dark-port floor of $-25.9\pm1$ dB at $\Phi=30$, against $-35.6$ dB at $\varepsilon=0$.
4. **No-go.** For any Fock-diagonal $\rho$ with $\langle n\rangle\ge1$, the minimum over $\theta$ and $\Phi$ of ${\rm Var}\,X_\theta$ after the Kerr stage equals $1+2\langle n\rangle$.

## Derivation

Exploration note §6.8 (with §6.11 for the validity).
- The sagitta of a phase spread $V'$ on a circle of radius $2\sqrt{\bar n_0}$ has variance $V'^2/(8\bar n_0)$. Minimizing $\nu^2/V'+V'^2/(8\bar n_0)$ gives $V'^*=(4\bar n_0\nu^2)^{1/3}$ and $\lambda_{\rm best}=1.5\cdot4^{-1/3}\nu^{4/3}\bar n_0^{-1/3}$.
- (ii): $[\hat n,\hat\rho]=0$.
- (iii): the angle error $\delta\psi\approx\varepsilon/(2\Phi)$, times the anti-squeezed variance $4\Phi^2$, gives $\varepsilon^2$.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Pass | claude-interactive.7 (claude) | — | 2026-10-18 |
| Known limits | Pass. $\nu=1$: exact Fock evolution gives $0.945\,\bar n^{-1/3}$ (slope −0.337, $\bar n=10^2$–$10^6$); the classical Wigner map gives the same within 0.02 dB at $10^8$ and $10^{10}$. The orchestrator independently found $\lambda_{\rm best}\bar n^{1/3}\to0.945$ from exact moments (review of PR #55; same family). | claude-interactive.7 (claude) | 2026-10-17-claude-interactive.7-condensate-kerr-squeezability; 2026-10-18-claude-interactive.7-gaussian-validity | 2026-10-18 |
| Symmetries | (ii) is exact by phase invariance. | claude-interactive.7 (claude) | — | 2026-10-17 |
| Symbolic residual | Pass. (iii): the Gaussian average over the pump spread equals $V_{\min}+\varepsilon^2$ within 1%. | claude-interactive.7 (claude) | 2026-10-17-claude-interactive.7-condensate-kerr-squeezability | 2026-10-17 |
| Simulation, core regime | Proposer family only; does not count. Classical Wigner map (exact up to $O(1/\bar n_0)$) on nine mixed condensate inputs: within 0.7 dB of (i) at $\bar n_0=10^{10}$ (G1b, G1c pass). At $10^8$, four of nine inputs are within 1 dB; for the others (i) is pessimistic by 1.1–6.3 dB, because those inputs are outside their own Gaussian regime (G1b, G1c fail there). | claude-interactive.7 (claude) | 2026-10-18-claude-interactive.7-gaussian-validity | 2026-10-18 |
| Error-scaling exponent | Exact displaced-thermal exponent -0.334621 at nu=10; relative asymptotic-error exponent -0.328378. Exact prefactor 3/(2*4^(1/3)); finite-range fitted intercepts are not substituted for it. | gpt-b (gpt) | 2026-10-18-gpt-b-kerr-exact | 2026-10-18 |
| Held-out region | All nine original exact displaced-thermal predictions pass, largest error0.218 dB; additional frozen occupations/mixedness test the asymptotic coefficient. | gpt-b (gpt) | 2026-10-18-gpt-b-kerr-exact | 2026-10-18 |
| Convergence and artefacts | $2\times10^5$ samples per point, with a fixed sample set across $\Phi$ so the scan is smooth. | claude-interactive.7 (claude) | 2026-10-18-claude-interactive.7-gaussian-validity | 2026-10-18 |
| Second solver or relaxed assumption | Independent Fock density matrices calibrate exact moments and TWA. Non-Gaussian/oriented Gaussian edges and extracted nonlinear-Wigner inputs relax the input assumptions. | gpt-b (gpt) | 2026-10-18-gpt-b-kerr-exact; 2026-10-18-gpt-b-condensate-squeezing | 2026-10-18 |
| Adversarial audit | Generic-Gaussian bounds and the super-Poissonian-to-positive-P implication are insufficient. The conditional phase-invariant no-go holds. Sagnac counting, external-LO quadrature and shot normalization must be distinguished. | gpt-b (gpt) | 2026-10-18-gpt-b-kerr-exact | 2026-10-18 |
| Novelty search | Not done. This session did not search the single-mode Kerr-squeezing literature: compare its photon-number exponent with the $n^{-1/3}$ found here. Also not searched: the mixed-state form $(\nu^4/\bar n)^{1/3}$ and the literature on pump-noise rejection in Sagnac squeezers. Left to the verifier. | claude-interactive.7 (claude) | — | 2026-10-18 |
| Cross-family exact reference | Displaced-thermal moment formula agrees with independent Fock propagation within 4e-12; high-occupation TWA moment accuracy is tested separately rather than assumed. | gpt-b (gpt) | 2026-10-18-gpt-b-kerr-exact | 2026-10-18 |
| Cross-family extracted inputs | Twelve frozen extracted-Wigner cases agree with the mixedness law within 0.176 dB, with phase/direction trained and tested on separate batches. This does not classify the exact GRIN reduced state. | gpt-b (gpt) | 2026-10-18-gpt-b-condensate-squeezing | 2026-10-18 |
| Cross-family novelty search | Coherent coefficient is explicit prior art: DOI 10.1016/j.optcom.2023.129717 (full text, relevant theory). Phase-invariance premise: DOI 10.1103/PhysRevA.100.053811 (full text, Kerr section). Mixed-coefficient novelty is not established. | gpt-b (gpt) | 2026-10-18-gpt-b-kerr-exact | 2026-10-18 |

## Outcome

**Verified as sharpened:** `cheap-checks-passed` → `sim-verified`. The status applies to the narrowed section only. It is not `audited`: actual extracted-state classification, calibrated physical noise and mixed-law novelty remain open in T-20261018-gpt-b-03. No new claim was filed.

**Promoted (2026-10-19):** `sim-verified` → `promoted`. The sharpened statement (the displaced-thermal optimum, the conditional no-go and the leading Sagnac term) is the promising result [R-0010](../results/promising/R-0010-displaced-thermal-kerr-squeezing-no-go/RESULT.md), under the PI's decision of 2026-10-19 that cross-family verified claims become promising results. Gate G5 is open: gpt-b's report is a cross-family verification, not a clean-context adversarial audit (T-20261019-claude-interactive.16-01). The Statement above is unchanged.

## Audit trail

| Date | Agent (family/model) | Verdict and status | Evidence |
|---|---|---|---|
| 2026-10-18 | gpt-b (gpt, gpt-6-astra) | Original generic covariance sufficiency and super-Poissonian-to-coherent-mixture implication refuted as general statements; automatic scrambling-to-diagonality unproved. Raw-normalization 1% bound fails an interior point. Conditional displaced-thermal law, no-go and leading specified-readout Sagnac term verified as sharpened; cheap-checks-passed → sim-verified. Original Statement preserved. | 2026-10-18-gpt-b-kerr-exact; 2026-10-18-gpt-b-condensate-squeezing; linked audit and summary above. |
| 2026-10-19 | claude-interactive.16 (claude, claude-opus-5-5) | `sim-verified` → `promoted`: result R-0010 (promising) written for the sharpened statement. Statement unchanged. G5 open (verification, not a clean-context audit). Record slips found: the Checks row calls 0.218 dB the largest held-out error, but the run maximum is 0.21732 dB ("within 0.218 dB" in the sharpened statement is a valid bound); and the auditor fields name gpt-b although no audit was completed (T-20261019-claude-interactive.16-06). | results/promising/R-0010-displaced-thermal-kerr-squeezing-no-go; task T-20261019-claude-interactive-09 |
