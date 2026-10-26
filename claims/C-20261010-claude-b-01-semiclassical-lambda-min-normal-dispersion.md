---
id: C-20261010-claude-b-01
problem: P-20261010-claude-interactive-01
title: "Gaussian pulse in normal dispersion: inverse-square best-quadrature scaling, hydrodynamic before breaking and conditional on a full-NLSE tangent limit after breaking"
type: asymptotic-solution
status: promoted
proposed_by: claude-b
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: pi-chatgpt
verifier_family: gpt
verifier_model: gpt-6-pro
audited_by: gpt-e
auditor_family: gpt
created: 2026-10-10
updated: 2026-10-19
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: R-0013
---

## Statement

> **Clean-context adversarial audit (gpt-e, gpt-6-astra, family gpt, 2026-10-19): pass-reduced-regime.** [Report](notes/audit-2026-10-19-gpt-e-C-20261010-claude-b-01.md), run `2026-10-19-gpt-e-strong-dispersion`.
> - **Additional theorem hypothesis:** the pre-breaking relative $O(\varepsilon^2)$ conclusion requires $C_\varepsilon=C_0+O(\varepsilon^2)$ in operator norm, $\sigma_1(C_0)>0$, and uniformly bounded $A_\varepsilon,B_\varepsilon,D_\varepsilon$ on the stated resolved or smooth sector. Merely having regular block limits is insufficient: the symplectic shear with $C_\varepsilon=1+\varepsilon$ has a relative first-order correction. The old weaker theorem wording below is superseded, not a proved general result.
> - Independent complete-grid hydrodynamics gives $\Lambda(0.45)=1.853725031660$ and $\Lambda(0.9)=0.673749049676$. The full NLSE relative deficit at $Z=0.9$ has fitted power $-1.98796$ over $N=10,20,40$.
> - New post-breaking checks at $Z=1.8,2.3$ support convergence of $N^2\lambda_{\min}$ over $N=10,20,40$. They do not establish an operator-norm limit or a universal correction power. The constrained passive minimum agrees with $\lambda_2$ to $1.1\times10^{-11}$ relative in the sampled unchirped family; this is numerical evidence, not a parity theorem.
> - Sign-off is for the ideal unchirped Gaussian Kerr model and the converged samples, under the card's dimensionless bounds and brightness condition. The shock/Raman extensions are not audited here. Input chirp was tested as a relaxed assumption.

> **As verified (GPT 6 Pro, family gpt, 2026-10-18; filed 2026-10-19 by claude-interactive).** Run `2026-10-18-pi-chatgpt-independent-verification`, [review](../docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md).
> - **Before breaking:** claim (a) is a conditional theorem plus an independent reproduction.
>   - **Superseded hypothesis (gpt-e audit, 2026-10-19):** the original theorem said that regular limits of a symplectic map with blocks $(A_\varepsilon,\varepsilon B_\varepsilon;C_\varepsilon/\varepsilon,D_\varepsilon)$ and $s_1=\sigma_1(C_0)>0$ suffice for $\lambda_{\min}=\varepsilon^2s_1^{-2}[1+O(\varepsilon^2)]$. They do not; use the explicit operator-norm rate and boundedness assumptions above.
>   - The reproduction: $\Lambda(0.75)=0.86284$, $\Pi(0.75)=2.18007$; relative deficits 1.55%, 0.39% and 0.099% at $N=10$, 20, 40, fitted power $-1.986$.
>   - It does not cover white continuum vacuum without a Sobolev or microlocal estimate.
> - **After breaking, narrowed:**
>   - The shallow-water (Euler) tangent map does not exist past the gradient catastrophe. "$C_Z$ = linearized dispersionless hydrodynamics" is therefore replaced, for $Z>Z_b$, by the limit $C_\infty$ of the full-NLSE tangent amplitude-to-scaled-phase block. This is what this card's reduced computation ($N=200$ full-NLSE propagations) actually evaluates.
>   - $N^2\lambda_{\min}\to\|C_\infty\|^{-2}$ follows rigorously if $C_N\to C_\infty$ in operator norm and the other blocks are subdominant; those hypotheses are unproved.
>   - Numerically supported at $Z=1.5$: $N^2\lambda_{\min}=0.36042$, 0.36191 and 0.36227 at $N=10$, 20, 40, converged to $1.2\times10^{-11}$, approaching this card's 0.3625. No universal next-order exponent is established there.
> - **$0<c\le2$** is a data statement. It does not follow from symplecticity, which leaves the sign of the next term undetermined.
> - **Precision of the tabulated coefficients:** the 80-Hermite-function basis biases $\Lambda$ by 0.012% and $\Pi$ by 0.165% at $Z=0.1$.
> - **$\lambda_{\rm pass}=\lambda_2$:** holds in the dense tested cases; parity alone does not prove it. The odd squeezed mode is dark, so bright-field photon counting reaches it only through a small even carrier admixture, or with an external LO.
> - **Not a separate result:** the small-$Z$ coefficient $4Z^2\Lambda=1+\sqrt{2/3}Z$ duplicates the weak-dispersion result of C-20261010-claude-a-01 item 5.

**System.** An unchirped Gaussian, $A(0,T)=\sqrt{P_0}\,e^{-T^2/2T_0^2}$, propagates in lossless single-mode fibre with normal dispersion $\beta_2>0$ and instantaneous Kerr nonlinearity $\gamma$. The input is a coherent state, and noise is linearized about the mean field.

**Notation.**
- $N^2=\gamma P_0T_0^2/\beta_2$ and $\varepsilon=1/N$.
- $Z=z/\sqrt{L_DL_{NL}}=N\,z/L_D$ is the semiclassical distance.
- $\Phi=NZ=\gamma P_0z$ is the peak nonlinear phase.
- $V$ is the output quadrature covariance over all spectral bins (shot noise $=1$).
- $\lambda_{\min}(V)$ and $\lambda_{\rm pass}$ are as defined on the problem card. $\lambda_{\rm pass}$ is $V$ restricted to the hyperplane orthogonal to the global phase direction $i\bar\alpha$.
- $\lambda_2(V)$ is the second-smallest eigenvalue of $V$.

**The map $C_Z$.** Take quadratures relative to the local mean phase:
- the amplitude $X=\delta\rho/(2\sqrt\rho)$;
- the scaled phase $\tilde Y=\varepsilon\sqrt\rho\,\delta\theta$, with $\delta\theta$ the phase fluctuation in radians;
- $\rho=|A|^2/P_0$.

$C_Z$ is the linear map from the input amplitude quadrature $X_0(\tau)$ to the output scaled phase quadrature $\tilde Y(\tau,Z)$, at $\tilde Y_0=0$. At leading order in $\varepsilon$ it is the linearized dispersionless (shallow-water) hydrodynamics of the defocusing NLSE, so it depends on $Z$ only, not on $N$. Let $\sigma_1(C_Z)\ge\sigma_2(C_Z)\ge\dots$ be its singular values, both spaces having the $L^2(d\tau)$ norm.

**Claim (a): $\lambda_{\min}$ at leading order.** For fixed $Z$ as $N\to\infty$,
$$\lambda_{\min}(V)=\frac{\Lambda(Z)}{N^2}\,(1+\delta),\qquad \Lambda(Z)=\frac{1}{\sigma_1(C_Z)^2}.$$
- **Before breaking** ($Z<Z_b\approx1.25$): $\delta=-c(Z)/\Phi^2+o(\Phi^{-2})$, with $c$ independent of $N$ and $0<c\le2$.
- **After breaking:** measured $-2/\Phi^2\le\delta<0$ for $Z\le3.2$ and $N\le24$, decaying as $N^{-1.78}$ (two points). The asymptotic form of $\delta$ there is not established.

The bound on $c$ is from the data. Before breaking, $c$ at fixed $z/z_{\rm wb}$ is constant in $N$ to ±4% for $N$ = 5–40 (run `2026-10-10-claude-b-nd-oracle`, `summary.json`, reduced curve at $N=200$):

| $Z$ | 0.106 | 0.32 | 0.74 | 1.06 | 1.59 | 2.13 | 2.66 | 3.19 |
|---|---|---|---|---|---|---|---|---|
| $c$ | 0.47–0.52 | 0.59–0.63 | 0.83–0.88 | 1.04–1.09 | 1.30–1.52 | 1.24 | 1.33 | 0.64 |

- At $Z=0.106$, $c\to1/2$, which is the dispersionless value.
- After breaking, $c$ drifts upward with $N$: at $Z=1.59$ it is 1.30, 1.30, 1.32 and 1.52 for $N$ = 5, 7, 10 and 20. With the $N=200$ curve the uncertainty in $c$ at $\Phi\approx32$ is about 0.03, so the drift is real. It shows an extra correction after breaking, consistent with the slower measured decay ($N^{-1.78}$).

**Claim (b): small-$Z$ form.**
$$4Z^2\Lambda(Z)=1+\tfrac{2}{\sqrt6}Z+O(Z^2).$$
Likewise $4Z^2\Pi(Z)=1+\sqrt6\,Z+O(Z^2)$.
- The near-peak $C_Z/(-2Z)$ is $1-H$, with $H=\tau^2-\tfrac{Z^2}{6}\partial_\tau^2$ a harmonic oscillator whose levels are $(2n+1)Z/\sqrt6$.
- Its ground state, of width $(Z/\sqrt6)^{1/2}$ about the peak, is the most squeezed input mode. The first excited state, which is odd, gives $\Pi$.
- Data: $4Z^2\Pi=1.279$ at $Z=0.1$ for the Gaussian against $1+\sqrt6Z=1.245$. For the parabola (run `2026-10-10-claude-b-nd-parabola`) it is 1.133 at $\zeta=0.05$ against 1.122.
- For $Z\to0$ this reduces to the dispersionless Kerr anchor $\lambda_{\min}=1/(4\Phi_{\rm peak}^2)$.

**Claim (c): $\lambda_{\rm pass}$ at leading order.**
$$\lambda_{\rm pass}=\lambda_2(V)=\frac{\Pi(Z)}{N^2}\,[1+o(1)],\qquad \Pi(Z)=\frac{1}{\sigma_2(C_Z)^2}.$$
- **Superseded proof claim:** the equality $\lambda_{\rm pass}=\lambda_2(V)$ was attributed to parity. Parity proves only that the odd eigenvectors are orthogonal to the even global phase direction, hence $\lambda_{\rm pass}\le\lambda_{\min}^{\rm odd}$. Equality also requires excluding a better constrained even mode; the audit tests that optimization numerically, without treating it as a theorem.
- Numerically $\lambda_{\rm pass}=\lambda_2(V)$ to $10^{-8}$ relative or better at every point checked (14 points, with and without the Raman reservoir).
- At N10 with $z/z_{\rm wb}$ = 0.7 and 1.5, the eigenvectors of $\lambda_1$, $\lambda_2$, $\lambda_3$ have parity $+1$, $-1$, $+1$ under $\omega\to-\omega$, with overlap $\langle u,Pu\rangle=\pm1.000000$.
- The restricted minimum in the even sector is always higher, but that part is not proved.

**Claim (d): tabulated coefficients** (reduced computation at $N=200$, run `2026-10-10-claude-b-nd-semiclassical`, `curve_N200.json`). Converging as $N^{-2}$ ($N$ = 50 → 100 → 200 changes shrink by about 4 each time), so these are within about $3\times10^{-5}$ of the $N\to\infty$ limit, $10^{-4}$ at $Z=0.1$. Wave breaking: the onset of oscillations in the NLSE is at $Z\approx1.24$–1.25 for $N$ = 40–80, and the dispersionless gradient catastrophe at $Z_b\approx1.27\pm0.02$ (run `2026-10-10-claude-b-nd-meanfield`). The quoted $z_{\rm wb}$ formula corresponds to $Z=1.0585$ and is used here only as the reference scale for $z/z_{\rm wb}$.

| $Z$ | $\Lambda(Z)$ | $4Z^2\Lambda$ | $1+0.8165Z$ | $\Pi(Z)$ |
|---|---|---|---|---|
| 0.10 | 27.234 | 1.0894 | 1.0816 | 32.02 |
| 0.20 | 7.4551 | 1.1928 | 1.1633 | 10.184 |
| 0.30 | 3.6350 | 1.3086 | 1.2449 | 5.7066 |
| 0.50 | 1.5702 | 1.5702 | 1.4082 | 3.1315 |
| 0.75 | 0.8628 | 1.9414 | 1.6124 | 2.1800 |
| 1.00 | 0.5877 | 2.3508 | 1.8165 | 1.7862 |
| 1.25 | 0.4467 | 2.7920 | 2.0206 | 1.5739 |
| 1.50 | 0.3625 | 3.2625 | 2.2247 | 1.4411 |
| 2.00 | 0.2678 | 4.2855 | 2.6330 | 1.2358 |
| 2.50 | 0.2167 | 5.4170 | 3.0412 | 1.1020 |
| 3.00 | 0.1848 | 6.6511 | 3.4495 | 1.0122 |
| 3.30 | 0.1708 | 7.4384 | 3.6944 | 0.9718 |
| 5.00* | 0.1252 | 12.52 | — | 0.8388 |
| 10.0* | 0.0821 | 32.82 | — | 0.7202 |

*From `curve_N50_long.json` ($N=50$, 80 $T_0$ window), which agrees with the 40 $T_0$ curves to $10^{-9}$ where they overlap.

**Wave breaking.** The leading order (a) does not fail at wave breaking. *[Narrowed 2026-10-19 (GPT 6 Pro): supported numerically after breaking, but $C_Z$ there must be the full-NLSE tangent-block limit, not the shallow-water map; see the verified block.]* The most squeezed mode lives in the smooth central region, while the dispersive shock waves form in the tails. In consequence:
- the amplitude block of the noise map grows with $N$ after breaking ($\sigma_1(A)=2.07$, $3.54$, $6.22$ at $N=20,50,100$ for $Z=1.59$, run `2026-10-10-claude-b-nd-semiclassical`, `summary.json`);
- $\Lambda$ stays $N$-independent: it changes by $\le4\times10^{-4}$ from $N=50$ to 100 and by $\le1\times10^{-4}$ from 100 to 200 at $Z\ge0.3$, before and after breaking.
- Two oracle points far beyond the claimed range, at $N=10$ with $z/z_{\rm wb}$ = 5 and 9 ($Z$ = 5.32 and 9.58, $\Phi$ = 53 and 96), still agree, to $+0.04\%$ and $+0.13\%$ (run `2026-10-10-claude-b-nd-oracle`, rows `N10_zr5` and `N10_zr9`, against the $N=50$ long curve). No failure of the leading order was found up to $z/z_{\rm wb}=9$.
- There the comparison is limited by the $N=50$ curve's own accuracy, about $10^{-3}$, so $c$ is not determined.

**Measurable form.**
$$\lambda_{\min}(V)\approx\frac{\Lambda(Z)}{N^2}=\frac{4Z^2\Lambda(Z)}{4\Phi^2}.$$
So dispersion raises the best quadrature variance above the dispersionless $1/(4\Phi^2)$ by the factor $4Z^2\Lambda(Z)$: 1.09 at $Z=0.1$, 1.94 at $Z=0.75$, 3.26 at $Z=1.5$, 6.65 at $Z=3$.

## Regime

**Dimensionless groups and bounds.**
- Normal dispersion: $\beta_2>0$, with $\beta_3=0$.
- Unchirped Gaussian input.
- $0.1\le Z\le3.2$, i.e. $0.1\le z/z_{\rm wb}\le3$ with $z_{\rm wb}=L_D/\sqrt{4N^2e^{-3/2}-1}$.
- $\Phi=NZ\ge5$.
- Tested $5\le N\le40$; the reduced coefficient is computed at $N$ = 50, 100, 200.
- Linearization validity, $\Phi/\sqrt{N_{\rm ph}}\ll1$.
- Self-steepening $s=1/(\omega_0T_0)$ with $sN\le0.16$.
- No Raman (see Assumptions).

**Small parameter and error order.**
- The audited relative second-order theorem has the explicit operator-norm rate hypothesis stated above. It is not inferred from symplecticity or smooth block limits alone. After breaking only the conditional leading-order statement and numerical evidence are signed off.
- The small parameter is $1/\Phi^2=1/(NZ)^2$.
- At fixed $Z$, the relative error of (a) decays as $N^{-2}$ before breaking. Measured exponents: $-1.93$, $-1.98$, $-1.98$ at $z/z_{\rm wb}$ = 0.3, 0.7, 1.0 over $N$ = 10–40.
- After breaking the decay is slower: $-1.78$ at $z/z_{\rm wb}=1.5$, from $N$ = 10, 20 only.
- Run `2026-10-10-claude-b-nd-oracle`, `summary.json`.

## Assumptions

1. Scalar, single-mode, single-polarization field. Lossless fibre.
2. Dispersion $\beta_2$ only (no $\beta_3$).
3. Instantaneous Kerr nonlinearity, with no Raman response and no Raman reservoir in the claim itself.
   - The Raman reservoir adds a positive semidefinite term to $V$ for a given mean-field map. So the Kerr-only values stay lower bounds on the Raman-noisy ones, but only if the map is unchanged.
   - The deterministic delayed response changes the map. Its effect on filtered Fano factors at $N=10$, $T_0=100$ fs is +0.002 to +0.04 (run `2026-10-10-claude-b.6-solver-nd-check`); its effect on $\Lambda$ was not computed.
   - **Raman reservoir, numbers** (run `2026-10-10-claude-b-nd-raman`). Method: the coth reservoir at 300 K added to the Kerr map. It is validated against the solver: the reservoir part of the centroid and $\lambda_{\rm gen}$-eigenvector readouts agrees to 0.4% at N10, $z/z_{\rm wb}=0.7$.

| point | $Z$ | $\Phi$ | $\lambda_{\min}$ Kerr only | with reservoir, 100 fs | 1 ps | $\Delta\lambda_{\min}\Phi$ (1 ps / 100 fs) |
|---|---|---|---|---|---|---|
| N10, 0.3 | 0.32 | 3.2 | 0.0308 | 0.0690 | 0.0659 | 0.112 / 0.122 |
| N20, 0.3 | 0.32 | 6.4 | 0.0081 | 0.0290 | — | — / 0.133 |
| N5, 0.7 | 0.76 | 3.8 | 0.0320 | 0.0691 | 0.0677 | 0.135 / 0.140 |
| N10, 0.7 | 0.75 | 7.5 | 0.0086 | 0.0290 | 0.0282 | 0.146 / 0.152 |
| N14, 0.7 | 0.74 | 10.4 | 0.0044 | 0.0193 | 0.0187 | 0.148 / 0.155 |
| N20, 0.7 | 0.74 | 14.8 | 0.0022 | 0.0127 | 0.0123 | 0.150 / 0.156 |
| N10, 1.5 | 1.60 | 16.0 | 0.0034 | 0.0172 | 0.0166 | 0.211 / 0.222 |

(runs `2026-10-10-claude-b-nd-raman`: `summary.json`, `summary_more.json`; at N10, 0.7 also 0.0314 at 50 fs and 0.0283 at 300 fs.)

   - **Raman reservoir, form of the excess.**
     - At fixed $Z$, $\Delta\lambda_{\min}\Phi$ is nearly independent of $N$ (0.135 → 0.150 from $N=5$ to 20 at $Z\approx0.75$, 1 ps). It depends weakly on $T_0$ above 100 fs.
     - Writing $\Delta\lambda_{\min}\approx\rho(Z)\,\hat c(0)/\Phi$, with $\hat c(0)=4af_Rk_BT/[\hbar(a^2+b^2)]=0.114$ the thermal low-frequency phonon level ($a=1/\tau_2$, $b=1/\tau_1$, 300 K), gives $\rho\approx1.0$–1.2 at $Z=0.32$, 1.2–1.4 at $Z\approx0.75$ and 1.9 at $Z=1.6$. So empirically
$$\lambda_{\min}\approx\frac{\Lambda(Z)}{N^2}+\rho(Z)\,\frac{\hat c(0)}{\Phi}.$$
   - **Raman reservoir, origin.** The squeezed quadrature carries phase weight $1/(2\Phi)$, and the reservoir's accumulated phase-noise variance is $4\Phi\hat c$. Together they give $\hat c/\Phi$, i.e. $\rho\to1$ as $Z\to0$.
   - **Raman reservoir, consequence.** The Raman term decays only as $1/N$ at fixed $Z$. It exceeds the Kerr term once $\Phi\gtrsim4Z^2\Lambda(Z)/(4\rho\hat c(0))$, about 3 at $Z=0.74$. In silica at room temperature this is the case at most points of the regime above. Formula (a) is the Kerr part of a bound that the reservoir raises by 2.1–5.8 times at the points computed.
   - **Raman reservoir, status.** This is not part of this claim. The form $\rho(Z)\simeq\sqrt{4Z^2\Lambda(Z)}$ is proposed separately as C-20261010-claude-b-03 (three frozen predictions pass). The deterministic delayed response is not included.
4. Self-steepening neglected in (a)–(d). Its effect at $sN\le0.16$ is below 0.4% on $\lambda_{\min}$ (oracle points with $s$ = 0.0082, 0.0164).
5. Coherent input, linearized (bright-field) Gaussian noise. Shot-noise normalization with vacuum uniform per frequency bin (photon counting at the carrier; the subagent's case B shows that photon-energy weighting changes filtered $F$ by up to 0.018 at $T_0=100$ fs).
6. Unchirped Gaussian input shape. $\Lambda(Z)$ is shape-dependent, and only the method carries over.
7. The quadrature covariance is taken over all spectral bins of a finite grid. The infinite-dimensional statement assumes the low-lying spectrum of $V$ converges, which is checked numerically (grid, basis and step tests below) but not proved.
8. The leading-order structure, i.e. the $\varepsilon$-independence of the hydrodynamic block $[[A,B],[C,D]]$ and $\varepsilon$-scaling as in the derivation, is derived by formal multiple-scale reasoning. It is not a theorem. For $Z\le1$ it is confirmed numerically: a direct $\varepsilon=0$ hydrodynamic computation reproduces the $N\to\infty$ limit of the NLSE-based $\Lambda$ and $\Pi$ (see Checks).

## Predictions

**Held-out set 1** (frozen in commit `895cc71` before computing; run `2026-10-10-claude-b-nd-heldout`).
- Points: $N=40$ at $z/z_{\rm wb}$ = 0.7 and 1.0.
- Predictions came from an extrapolation of the $N$ = 14, 20 oracle values, not from (a).
- Scored: $\lambda_{\min}$ within 0.2% (tolerance 2%), $\lambda_{\rm pass}$ within 0.4% (3%), $\lambda_{\rm gen}$ within 4.2% (10%). All pass.
- The best single interval passes at 0.7 and fails at 1.0: actual 0.732, predicted 0.827 ± 0.06.
- Formula (a) at these points: $-0.10\%$ and $-0.07\%$ (computed after the fact, not frozen).

**Held-out set 2** (frozen in commit `cdb6951` before computing; run `2026-10-10-claude-b-nd-heldout2`). Predictions use only the reduced curve `curve_N50.json`.

| case | $Z$ | $\Phi$ | $N^2\lambda_{\min}$ predicted | $N^2\lambda_{\rm pass}$ predicted |
|---|---|---|---|---|
| $N=16$, $z/z_{\rm wb}=0.5$ | 0.530 | 8.49 | $1.4332(1-c/\Phi^2)$, $0\le c\le2$ | $2.9498(1-e)$, $0\le e\le0.05$ |
| $N=24$, $z/z_{\rm wb}=1.25$ (at the onset) | 1.324 | 31.8 | $0.41757(1-c/\Phi^2)$ | $1.5307(1-e)$ |
| $N=12$, $z/z_{\rm wb}=2.5$ (after breaking) | 2.657 | 31.9 | $0.20528(1-c/\Phi^2)$ | $1.0696(1-e)$ |

Also predicted: $\lambda_{\rm pass}=\lambda_2(V)$ to $10^{-6}$ relative.

**Held-out set 3** (frozen in `d6ab3a9`; run `2026-10-10-claude-b-nd-heldout3`). At $N=18$, $z/z_{\rm wb}=0.9$: $\lambda_{\min}$ is $-0.35\%$ from the formula ($c=1.02$, within $0\le c\le2$). Pass.

**Held-out set 4** (frozen in `7c6ea32`; run `2026-10-10-claude-b-nd-heldout4`). At $N=28$, $z/z_{\rm wb}=0.5$: $-0.34\%$ ($c=0.75$). Pass.

**Scores** (`runs/2026-10-10-claude-b-nd-heldout2/summary.json`): all pass.

| case | $\lambda_{\min}$ vs formula | measured $c$ | $\lambda_{\rm pass}$ vs $\Pi/N^2$ | $\lambda_{\rm pass}/\lambda_2-1$ |
|---|---|---|---|---|
| N16, 0.5 | $-1.02\%$ | 0.74 | $-1.8\%$ | 0 (to rounding) |
| N24, 1.25 | $-0.15\%$ | 1.51 | $-0.9\%$ | 0 |
| N12, 2.5 | $-0.13\%$ | 1.33 | $-1.5\%$ | 0 |

**For the lab.** At $N=20$ and $z=0.7z_{\rm wb}$ (e.g. $T_0=100$ fs, $\beta_2=20$ ps²/km, $\gamma=10$ /W/km, $P_0=80$ kW, $L_D=0.5$ m, $z_{\rm wb}=2.65$ cm, $z\approx1.86$ cm):
- $\lambda_{\min}(V)=2.18\times10^{-3}$, i.e. $-26.6$ dB;
- $\lambda_{\rm pass}=5.44\times10^{-3}$, i.e. $-22.6$ dB.

These are the limits for any readout, and for passive linear optics plus counting, respectively (oracle row `N20_zr0.7`, run `2026-10-10-claude-b-nd-oracle`). Raman will raise both; see Assumptions.

## Derivation

Full notes: `explorations/2026-10-10-claude-b-semiclassical-normal-dispersion.md`, sections 1–3. In outline:
1. With $\varepsilon=1/N$ and $Z=Nz/L_D$ the NLSE becomes $i\varepsilon u_Z-\tfrac{\varepsilon^2}{2}u_{\tau\tau}+|u|^2u=0$. With $u=\sqrt\rho\,e^{i\theta/\varepsilon}$ the mean field obeys shallow water up to $O(\varepsilon^2)$.
2. Linearize. In $(X,\tilde Y)$ the map $M_h=[[A,B],[C,D]]$ is $\varepsilon$-independent and symplectic. In $(X,Y)$ it is $M=[[A,\varepsilon B],[C/\varepsilon,D]]$.
3. Because $M$ is symplectic, $M^{-1}=\Omega^{\mathsf T}M^{\mathsf T}\Omega=[[D^{\mathsf T},-\varepsilon B^{\mathsf T}],[-C^{\mathsf T}/\varepsilon,A^{\mathsf T}]]$.
   - Its largest singular values are $\sigma_k(C)/\varepsilon+O(1)$ (Weyl).
   - The smallest singular values of $M$ are therefore $\varepsilon/\sigma_k(C)\,[1+O(\varepsilon)]$, so $\lambda_k(V)=\varepsilon^2/\sigma_k(C)^2$ at leading order.
   - The data show the correction is $O(\varepsilon^2)$ rather than $O(\varepsilon)$, consistent with the $O(1)$ blocks entering only at second order.
   - Equivalently, for an output functional $(x,y)$: $\|M^{\mathsf T}(x,y)\|^2=\|A^{\mathsf T}x+C^{\mathsf T}y/\varepsilon\|^2+\|\varepsilon B^{\mathsf T}x+D^{\mathsf T}y\|^2$.
   - $O(\varepsilon^2)$ requires $y=\varepsilon\hat y$ with $A^{\mathsf T}x+C^{\mathsf T}\hat y=0$.
   - With $B-AC^{-1}D=-C^{-\mathsf T}$ (symplecticity) the variance is $\varepsilon^2\|C^{-1}x\|^2$.
   - Minimizing over $\|x\|=1$ gives (a). The $k$-th smallest eigenvalue is $\varepsilon^2/\sigma_k(C)^2$, which gives (c) once parity is used.
4. Small $Z$: expand the linearized hydrodynamics to $O(Z^3)$ near the peak. The operator $C/(-2Z)$ is then the oscillator $1-\tau^2+\tfrac{Z^2}{6}\partial_\tau^2$, whose top eigenvalue is $1-Z/\sqrt6$. This gives (b).
5. Reduced computation: $C_Z$ on the span of the first $M=80$ Hermite functions, from $2M$ central-difference propagations of the full NLSE at large $N$, with the output read as $\mathrm{Im}(\delta u\,e^{-i\arg\bar u})/N$.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Dimensionless; $\Phi=\gamma P_0z$, $Z=z\sqrt{\gamma P_0\beta_2}/T_0$ | claude-b (claude) | — | 2026-10-10 |
| Known limits | Cross-lane: C-20261010-claude-a-01, item 5 (claude-a, unverified, read at 13:34) gives the weak-dispersion correction $\lambda_{\min}/V_{\min}(\Phi)-1=\tfrac{\Phi^{3/2}}{\sqrt{1+\Phi^2}}\sqrt{\tfrac13|p''(0)|\beta_2L}\,[1+c_2\sqrt y]$ with $c_2\simeq1.0$, $y=\Phi L/L_D$. For the Gaussian at large $\Phi$ this is $\sqrt{2/3}\,Z\,(1+c_2Z)$, which is exactly the coefficient $2/\sqrt6$ of (b). Their $c_2\simeq1.0$ agrees with the $Z^2$ coefficient here: extrapolating $(4Z^2\Lambda-1-\tfrac{2}{\sqrt6}Z)/Z^2$ from the exact $\varepsilon=0$ values (`hydro_direct.json`, $Z\le0.5$) gives 0.81–0.83, i.e. $c_2$ = 0.99–1.02. $Z\to0$: $4Z^2\Lambda\to1$, the dispersionless $1/(4\Phi^2)$. Correction $c\to1/2$ matches the exact single-mode $V_{\min}=(\sqrt{1+\Phi^2}-\Phi)^2=\tfrac{1}{4\Phi^2}(1-\tfrac{1}{2\Phi^2}+\dots)$. Small-$Z$ coefficients from the $N=200$ curve (polynomial extrapolation of $(4Z^2\Lambda-1)/Z$, degree 2–3 on $0.1\le Z\le0.3$–0.4): 0.8159, against $2/\sqrt6=0.8165$. For $\Pi$ the same extrapolation gives 2.44–2.50, against $\sqrt6=2.449$. | claude-b (claude) | 2026-10-10-claude-b-nd-semiclassical | 2026-10-10 |
| Symmetries | Parity: $\lambda_{\rm pass}=\lambda_2(V)$ to $<10^{-8}$ at $(N,z/z_{\rm wb})$ = (10, 0.7), (10, 1.5), (7, 0.3) (penalty and exact projection agree to $10^{-14}$) and on held-out set 2 | claude-b (claude) | 2026-10-10-claude-b-nd-oracle, 2026-10-10-claude-b-nd-heldout2 | 2026-10-10 |
| Symbolic residual | Direct $\varepsilon=0$ check: integrating the dispersionless Madelung (shallow-water) equations, with no NLSE, and taking $\sigma_{1,2}$ of the linearized amplitude→phase map gives $\Lambda$ and $\Pi$. They equal the $N=200$ NLSE curve to $1.3\times10^{-4}$ and $4\times10^{-4}$ at $Z=0.1$, and to $\le1\times10^{-5}$ and $\le3\times10^{-5}$ at $Z\ge0.5$. The residual equals the $N\to\infty$ Richardson extrapolation of the NLSE curves ($Z\le1$, grid-converged to $10^{-9}$; `hydro_direct.json`, run 2026-10-10-claude-b-nd-semiclassical). Also a semi-analytic cross-check on the passive parabola: the reduced method reproduces the leading-order $\Lambda$ that follows from the Legendre-block propagator of C-20261004-claude-a-01 to $\le0.11\%$ for $\zeta\le2$ ($N=100$). The odd sector ($\Pi$) differs by up to 1.9% at $\zeta=2$ with $M=80$, falling to 0.9% at $M=240$. That is slow basis convergence at the parabola's hard edge. The Gaussian is converged to $<4\times10^{-7}$ in $M$ | claude-b (claude) | 2026-10-10-claude-b-nd-parabola, 2026-10-10-claude-b-nd-semiclassical | 2026-10-10 |
| Simulation, core regime | 36 oracle points, $N$ = 5–40, $z/z_{\rm wb}$ = 0.1–3. Relative error of (a), reduced curve at $N=200$: $-0.10\%$ ($N=40$, 0.7), $-0.06\%$ (40, 1.0), $-0.15\%$ (20, 1.5), $-0.27\%$ (10, 2.0), $-0.06\%$ (10, 3.0), $+0.04\%$ (10, 5), $+0.13\%$ (10, 9). The largest error is at small $\Phi$: $-30.5\%$ at $\Phi=1.06$, where $c/\Phi^2$ is not small | claude-b (claude) | 2026-10-10-claude-b-nd-oracle | 2026-10-10 |
| Error-scaling exponent | $-1.93$, $-1.98$, $-1.98$ at $z/z_{\rm wb}$ = 0.3, 0.7, 1.0 (before breaking, $N$ = 10–40); $-1.78$ at 1.5 (after breaking, $N$ = 10, 20 only); $\lambda_{\rm pass}$: $-1.91$, $-1.97$, $-1.94$, $-1.42$ (reduced curve at $N=200$) | claude-b (claude) | 2026-10-10-claude-b-nd-oracle | 2026-10-10 |
| Held-out region | Set 1 (frozen `895cc71`, extrapolation-based): passes for $\lambda_{\min},\lambda_{\rm pass},\lambda_{\rm gen}$; the interval fails at 1.0. Set 2 (frozen `cdb6951`, formula-based): 9 of 9 predictions for this claim pass, including one point at the onset of breaking and one after it | claude-b (claude) | 2026-10-10-claude-b-nd-heldout, 2026-10-10-claude-b-nd-heldout2 | 2026-10-10 |
| Convergence and artefacts | Reduced curve: step halving changes $\Lambda$ by $<10^{-6}$; $M$ = 40/80/120 by $<2\times10^{-4}$ at $Z\ge0.1$; $M$ = 80 vs 160 by $<4\times10^{-7}$ for $0.5\le Z\le3$; $N$ = 50 → 100 → 200 by $1.5\times10^{-3}$ then $3.8\times10^{-4}$ at $Z=0.1$, and $\le3.8\times10^{-4}$ then $\le1\times10^{-4}$ at $Z\ge0.3$ (convergence as $N^{-2}$). Oracle: grid resolution flagged by the exact momentum identity of C-20261010-claude-b-02; three points (N14 and N28 at 1.5, N20 at 2) fail it and are excluded from the exponents | claude-b (claude) | 2026-10-10-claude-b-nd-semiclassical, 2026-10-10-claude-b-nd-oracle | 2026-10-10 |
| Second solver or relaxed assumption | FastDifferentiableMMNLO (discrete RK4IP adjoint, commit b9fa957, blind, frozen before comparison) reproduces the numpy oracle at all 12 points of the grid $N$ = 5, 10, 20 × $z/z_{\rm wb}$ = 0.3, 0.7, 1, 1.5. The three readouts derived from the same Jacobian agree: $\lambda_{\rm gen}$ (via its eigenvector) to $\le1.0\times10^{-5}$, the centroid to $\le1.0\times10^{-5}$, the best binary filter to $\le2.6\times10^{-6}$ (run `2026-10-10-claude-b.6-solver-grid`, comparison in `runs/2026-10-10-claude-b-nd-oracle/solver_grid_comparison.json`). $\lambda_{\min}$ itself is not a photon-number observable and was not computed in the solver. Relaxed: self-steepening ($sN\le0.16$) changes $\lambda_{\min}$ by $\le0.4\%$. Raman not yet propagated into $\Lambda$ | claude-b.6 and claude-b (claude) | 2026-10-10-claude-b.6-solver-nd-check, 2026-10-10-claude-b-nd-oracle | 2026-10-10 |
| Adversarial audit | **Pass-reduced-regime**, [report](notes/audit-2026-10-19-gpt-e-C-20261010-claude-b-01.md). Corrected generic theorem hypothesis; independent hydro coefficient, pre-breaking error power -1.98796, new post-breaking distances, actual passive covariance compression. Grid/window/step checks and unchanged-solver adjoint contractions | gpt-e (gpt; gpt-6-astra) | `2026-10-19-gpt-e-strong-dispersion` | 2026-10-19 |
| Novelty search | No paper on quadrature squeezing limits of semiclassical normal-dispersion pulses found. Searched OpenAlex: "quantum noise optical wave breaking normal dispersion squeezing", "quantum fluctuations dispersive shock wave Bogoliubov expanding condensate"; full list and access levels in log 2026-10-10_claude-b_T-20261010-claude-interactive-05 | claude-b (claude) | — | 2026-10-10 |
| Independent verification, before breaking | Independent dispersionless hydrodynamics on a complete grid (DOP853, no Hermite basis): $\Lambda(0.75)=0.86284166134$, $\Pi(0.75)=2.18007053159$. Full-field fourth-order Yoshida Fourier tangent flow, matrix-free and dense: $N^2\lambda_{\min}=0.84948$, 0.85945, 0.86199 at $N=10$, 20, 40 ($Z=0.75$) | pi-chatgpt (gpt) | `2026-10-18-pi-chatgpt-independent-verification` | 2026-10-18 |
| Error-scaling exponent | Relative deficit to $\Lambda(0.75)$: 1.5491%, 0.3935%, 0.0988%; fitted power $-1.98555$ (predicted $-2$) | pi-chatgpt (gpt) | `2026-10-18-pi-chatgpt-independent-verification` | 2026-10-18 |
| After breaking | $Z=1.5$: $N^2\lambda_{\min}=0.360416$, 0.361913, 0.362267 ($N=10$, 20, 40). At $N=20$, grid and window changes leave $\lambda_{\min}$ stable to $1.2\times10^{-11}$; the amplitude block grows (1.66, 2.22, 3.34) | pi-chatgpt (gpt) | `2026-10-18-pi-chatgpt-independent-verification` | 2026-10-18 |
| Basis bias | At $Z=0.1$, complete-grid $\Lambda=27.23396$, $\Pi=31.98003$; projecting onto 80 Hermite functions reproduces this card's `hydro_direct.json` (27.23727, 32.03267): biases 0.012% and 0.165% | pi-chatgpt (gpt) | `2026-10-18-pi-chatgpt-independent-verification` | 2026-10-18 |
| Reproduction before filing | The weak-dispersion cross-check with this lane's solver is rerun on a second platform ($7\times10^{-13}$ relative). The strong-dispersion cases were not rerun | claude-interactive (claude) | `2026-10-19-claude-interactive-gpt6pro-quick-repro` | 2026-10-19 |
| Novelty search | $\Lambda(Z)$ as an optical application is a plausible contribution. Symplectic SVD (Braunstein 2005) and semiclassical defocusing hydrodynamics (Jin–Levermore–McLaughlin 1999) are established. Normal-dispersion squeezing was observed by Krylov, Bergman & Lai (1999; abstract only) | pi-chatgpt (gpt) | — | 2026-10-18 |

## Outcome

**Audited, narrowed (2026-10-19).** gpt-e's separate clean-context audit follows GPT 6 Pro's earlier verification. Independent hydrodynamics and full-field optimization support the pre-breaking scaling and its observed second-order approach. New post-breaking distances support the conditional leading-order statement. The generic theorem now includes the necessary operator-norm rate hypothesis; neither post-breaking convergence nor the passive-equality theorem is proved. The controlling audit scope is stated above.

**Promoted (2026-10-19).** The narrowed statement above is promising result [R-0013](../results/promising/R-0013-strong-normal-dispersion-lambda-over-n2/RESULT.md), on the PI's decision to promote every cross-family verified claim. The post-breaking part and the equality $\lambda_{\rm pass}=\lambda_2$ are stated there as numerical findings; G2 and G5 are open.

**Audit recorded on the result (2026-10-19).** gpt-e's clean-context audit (pass with reduced regime) closes gate G5 of R-0013, whose Adversarial audit section gives the signed-off scope.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-19 | gpt-e (gpt; gpt-6-astra) | Clean-context pass-reduced-regime; sim-verified → audited. Repaired the insufficient generic theorem hypothesis; retained conditional post-breaking and empirical passive-equality scope | [Audit](notes/audit-2026-10-19-gpt-e-C-20261010-claude-b-01.md); run `2026-10-19-gpt-e-strong-dispersion` |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Filed GPT 6 Pro's independent verification. Status proposed → sim-verified (narrowed); the post-breaking definition of $C_Z$ narrowed; precision and readout notes added | Runs `2026-10-18-pi-chatgpt-independent-verification`, `2026-10-19-claude-interactive-gpt6pro-quick-repro`; [review](../docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md) |
| 2026-10-19 | claude-interactive.17 (claude; claude-opus-5-5), task T-20261019-claude-interactive-10, on the PI's promotion decision | Status sim-verified → promoted; result R-0013 (promising tier). Statement unchanged; G5 (clean-context audit, T-20261019-claude-interactive-04) still open | [R-0013](../results/promising/R-0013-strong-normal-dispersion-lambda-over-n2/RESULT.md); PI decision of 2026-10-19 recorded in T-20261019-claude-interactive-07 |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5) | Merged gpt-e's audit (PR #76) with the promotion to R-0013: status stays promoted, audited_by gpt-e; G5 of R-0013 set to met | PR #76; claims/notes/audit-2026-10-19-gpt-e-C-20261010-claude-b-01.md |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5) | Annotation, no change to the Checks row: the cross-lane estimate 0.81–0.83 ("$c_2=0.99$–1.02") in Known limits was extrapolated from 80-Hermite values that carry the basis bias GPT 6 Pro quantified. On GPT 6 Pro's complete grid the same extrapolation gives 0.8021, against 4/5 from the closed form $c_2(\infty)=2\sqrt6/5$ (R-0015). Found by claude-interactive.19 | docs/manuscripts/2026-10-19-normal-dispersion-squeezing-bounds/README.md (discrepancy 3); task T-20261019-claude-interactive.19-03 |
