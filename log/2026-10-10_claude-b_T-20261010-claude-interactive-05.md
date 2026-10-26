---
date: 2026-10-10
agent: claude-b
model: claude-opus-5-5
family: claude
task: T-20261010-claude-interactive-05
duration_min: 202
---

## Did

Approach 2 of P-20261010-claude-interactive-01: an unchirped Gaussian in normal dispersion with $N\gg1$, before and after optical wave breaking. All work is on branch `task/T-20261010-claude-interactive-05`.

1. **Literature (≤ 30 min).** Listed below with access levels and search strings.
2. **Mean field** (run `2026-10-10-claude-b-nd-meanfield`).
   - Measured the onset of oscillations in semiclassical units, $Z=z/\sqrt{L_DL_{NL}}$: $Z_b$ = 1.21, 1.23, 1.2375 and 1.244 at $N$ = 10, 20, 40, 80.
   - The often-quoted $z_{\rm wb}$ formula gives $Z\to1.0585$. I used it only as a reference scale for $z/z_{\rm wb}$.
   - The dispersionless ($\varepsilon=0$) gradient catastrophe of the Gaussian, computed directly, is at $Z_b\approx1.27\pm0.02$ (`gradient_catastrophe.json`). This agrees with the extrapolated onset of oscillations, not with the quoted formula.
3. **Fluctuation theory** (`explorations/2026-10-10-claude-b-semiclassical-normal-dispersion.md`).
   - In quadratures relative to the local mean phase, with the phase scaled by $\varepsilon=1/N$, the linearized map is the $\varepsilon$-independent symplectic hydrodynamic map $[[A,B],[C,D]]$.
   - A Schur-complement argument gives $\lambda_k(V)=\varepsilon^2/\sigma_k(C_Z)^2+o(\varepsilon^2)$.
   - Small-$Z$ oscillator expansion: $4Z^2\Lambda=1+(2/\sqrt6)Z+O(Z^2)$.
   - Parity gives $\lambda_{\rm pass}=\lambda_2(V)$.
   - Weighted-counting functionals, and why binary filters cannot cancel the $O(1)$ part.
   - The spectral-centroid identity from momentum conservation.
4. **Oracle** (run `2026-10-10-claude-b-nd-oracle`).
   - Method: full linearized covariance by central differences of the split-step map. It gives $\lambda_{\min}$, $\lambda_{\rm pass}$, $\lambda_{\rm gen}$ and a three-stage binary-filter search.
   - 36 points: $N$ = 5–40 at $z/z_{\rm wb}$ = 0.1–3, plus $N=10$ at $z/z_{\rm wb}$ = 5 and 9. Two of them have self-steepening.
   - Scoring script `analyze.py` writes `summary.json` and `fig_bounds.png`.
5. **Reduced computation of $C_Z$** (run `2026-10-10-claude-b-nd-semiclassical`).
   - Central differences of the full NLSE on 80 Hermite functions at $N$ = 50, 100, 200.
   - Records $\Lambda(Z)$, $\Pi(Z)$ and $K(Z)$ up to $Z=3.3$, plus an $N=50$ curve to $Z=10$ on an 80 $T_0$ window.
   - Basis check: $M$ = 80 vs 160.
6. **Held-out set 1** (run `2026-10-10-claude-b-nd-heldout`): $N=40$, frozen in `895cc71` before computing.
7. **Held-out set 2** (run `2026-10-10-claude-b-nd-heldout2`): three points, one at the onset of breaking and one after it. Frozen in `cdb6951` before computing, from the reduced curve only.
8. **Second solver** (subagent claude-b.6, run `2026-10-10-claude-b.6-solver-nd-check`).
   - FastDifferentiableMMNLO at commit `b9fa957`, discrete RK4IP adjoint, blind, frozen before comparison.
   - Kerr-only filtered $F$ for my binary and interval filters.
   - Self-steepening and Raman (deterministic plus coth reservoir at 300 K) at $T_0=100$ fs.
   - A follow-up on weighted readouts (centroid, $\lambda_{\rm gen}$ eigenvector, binary) with Raman: run `2026-10-10-claude-b.6-solver-weighted-raman`.
9. **Cross-check with C-20261004-claude-a-01** (passive parabola), run `2026-10-10-claude-b-nd-parabola`. From claude-a's Legendre-block propagator I derived the parabola's $C$-block, $m_l(\mu)=P_l(0)Q_l(\mu)-Q_l(0)P_l(\mu)$. I compared $\Lambda_{\rm par}(\zeta)$ and $\Pi_{\rm par}(\zeta)$ with my reduced numerics on a parabolic input.
10. **Raman floor** (run `2026-10-10-claude-b-nd-raman`). I added the coth Raman reservoir to the numpy oracle as phase noise accumulated through the inverse slice Jacobians. It is validated against the solver.
11. **Convergence and robustness.**
    - Run `2026-10-10-claude-b-nd-convergence`: grid, window and step.
    - A long binary search (`long_search.json`).
    - Band/comb anatomy of the best filters (`comb_diagnostic.json`).
    - Root-01 anchor analogues (run `2026-10-10-claude-b-nd-anchor-map`).
    - A Kerr-only discrete-adjoint comparison over the requested grid $N$ = 5, 10, 20 × $z/z_{\rm wb}$ = 0.3, 0.7, 1, 1.5, by subagent claude-b.6 (run `2026-10-10-claude-b.6-solver-grid`).
12. **Write-up.** Three claim cards (C-20261010-claude-b-01, -02, -03) and seven loose-end tasks.

## Found

**1. $\lambda_{\min}(V)$ at leading order** (C-20261010-claude-b-01; asymptotic, not rigorous).
- **Formula.** $\lambda_{\min}=\Lambda(Z)/N^2\,[1-c(Z)/\Phi^2]$ with $\Lambda=\sigma_1(C_Z)^{-2}$, tabulated for $Z$ = 0.1–10.
- **Direct check.** For $Z\le1$, a direct computation from the dispersionless ($\varepsilon=0$) Madelung equations, with no NLSE, reproduces the NLSE-based $\Lambda$ and $\Pi$ at $N\to\infty$ (Richardson) to $\le10^{-5}$–$10^{-4}$ (`hydro_direct.json`).
- **The correction coefficient.** At fixed $z/z_{\rm wb}$ before breaking, $c$ is constant in $N$ to ±4% for $N$ = 5–40: 0.5 at $Z=0.1$ (the dispersionless value $1/2$), 0.62 at 0.32, 0.87 at 0.74, 1.07 at 1.06.
- **Error exponents** in $N$ (against the $N=200$ reduced curve): −1.93, −1.98, −1.98 before breaking; −1.78 after breaking ($N$ = 10, 20). After breaking, $c$ drifts from 1.30 ($N\le10$) to 1.52 ($N=20$) at $Z=1.59$, so there is an extra correction there.
- **After breaking.** The formula holds through $Z=3.2$ ($z/z_{\rm wb}=3$) on the grid. Two further $N=10$ points at $z/z_{\rm wb}$ = 5 and 9 ($Z$ = 5.3, 9.6) agree to $+0.04\%$ and $+0.13\%$, scored against the $N=50$ long curve to $Z=10$. The amplitude block grows with $N$ after breaking, but $\Lambda$ does not. The squeezed mode lives in the smooth centre while the shocks form in the tails, so no Whitham treatment is needed for $\lambda_{\min}$. Up to $z/z_{\rm wb}=9$, I did not find where the leading order fails.

**2. $\lambda_{\rm pass}$ at leading order.**
- $\lambda_{\rm pass}=\lambda_2(V)$ to $\le10^{-8}$ at every point where $\lambda_2$ was computed: 14 points, with and without the Raman reservoir.
- $\lambda_{\rm pass}=\Pi(Z)/N^2$ with $\Pi=\sigma_2(C_Z)^{-2}$ (odd sector), error exponent ≈ −2 before breaking.

**3. Spectral-centroid identity** (C-20261010-claude-b-02).
- **Statement.** For Kerr-only NLSE with any dispersion, $F$ of the weight $w=\omega-\bar\omega$ equals $\langle\Delta\omega^2\rangle_{\rm in}/\langle\Delta\omega^2\rangle_{\rm out}$ exactly. So $\lambda_{\rm gen}$ is at most that ratio.
- **Gaussian, $\beta_2$ only.** The ratio is $1/(1+2N^2K(Z))$, with $K$ from energy conservation.
- **How tight.** $\lambda_{\rm gen}$ sits 0.03–0.87 dB below it on every resolved point.
- **Resolution test.** The identity holds to $\le1.1\times10^{-5}$ on resolved grids, so it serves as a check on under-resolved oracle grids. Three points fail it and are flagged.
- **Generality.** It also holds for anomalous dispersion and with $\beta_3$, to $\le2\times10^{-6}$ (run `2026-10-10-claude-b-nd-centroid-general`).
- **Coefficient sandwich.** $\Pi(Z)\le\Gamma(Z)\le1/(2K(Z))$ for the coefficient of $\lambda_{\rm gen}$. The two sides are 4.5 dB apart at $Z=0.3$ and 0.12 dB apart at $Z=3$.

**4. Binary filters (the third target).**
- **No formula.** I have no leading-order formula for the binary optimum.
- **What the search finds.** The best filters found (three search stages) lie:
  - 10.3–22.2 dB above $\lambda_{\rm gen}$ for $N\ge14$, $\Phi\ge4$;
  - 19.5–28.5 dB above the formula and above $\lambda_{\min}$.
- **Scaling.** They decrease only as $N^{-0.36}$ to $N^{-0.47}$ at fixed $z/z_{\rm wb}$, while all quadratic-form bounds scale as $N^{-2}$. The chain is therefore not tight for filters in this regime; the gap grows with $N$.
- **Structure.** One broad band plus narrow bands near the centre on the scale of the centre–tail interference fringes. Each part alone is super-Poissonian ($F$ = 2–10), but their counts are anticorrelated (−0.88 to −0.96, growing with $N$): a self-homodyne pair (`comb_diagnostic.json`).
- **Search robustness.** A further 8 × 2500-step search moves the best value by 0 (N20) and $-0.08\%$ (N40), and finer bins move it by $-0.2\%$ to $-0.6\%$. A parity-seeded search (84 starts plus ILS at five points; `parity_search.json`) finds nothing better. So the values are stable, though not certified global optima.
- **Non-negative weights.** A heuristic minimum over $w\ge0$ (not a bound) sits 0.3–4.7 dB below the binary filters and 6–17.5 dB above $\lambda_{\rm gen}$. So the sign constraint, not binary-ness, accounts for most of the gap.

**4b. Few-detector signed readouts** (`few_detectors.json`).
- **Split detector.** A split detector at the centroid is useless: $F>1$ at five of six points.
- **Quantized centroid.** $K$ equal-photon bands, weighted by their mean detuning, give $-7.7$, $-11.8$ and $-15.7$ dB at N20, $z/z_{\rm wb}=0.7$ for $K$ = 4, 8, 16. The best binary filter gives $-4.7$ dB and $\lambda_{\rm gen}$ $-20.6$ dB there.
- **Reading.** So about 16 signed detectors recover 9–11 dB over any binary filter found. This is relevant to the card's rung 5.

**Summary figure.** `runs/2026-10-10-claude-b-nd-oracle/fig_chain.png` shows the whole chain against $N$ at $z/z_{\rm wb}$ = 0.7 and 1.0.

**5. Scored gaps in dB** (best binary found against each quantity):

| point | vs formula | vs $\lambda_{\rm gen}$ | vs $\lambda_{\min}$ | vs $\lambda_{\rm pass}$ |
|---|---|---|---|---|
| N10, 0.7 | 17.1 | 11.3 | 17.2 | 13.3 |
| N20, 0.7 | 21.9 | 16.0 | 21.9 | 18.0 |
| N40, 0.7 (held out) | 26.5 | 20.4 | 26.5 | 22.5 |
| N40, 1.0 (held out) | 28.5 | 22.2 | 28.5 | 23.6 |
| N20, 1.5 | 26.9 | 20.3 | 27.0 | 20.9 |
| N10, 3.0 | 23.9 | 16.4 | 23.9 | 16.5 |
| N16, 0.5 (held out 2) | 19.5 | 14.0 | 19.5 | 16.4 |
| N24, 1.25 (held out 2) | 26.5 | 20.1 | 26.6 | 20.9 |
| N12, 2.5 (held out 2) | 24.9 | 17.6 | 24.9 | 17.7 |

Sources: run `2026-10-10-claude-b-nd-oracle` (`summary.json`) and run `2026-10-10-claude-b-nd-heldout2` (`summary.json`). Binary search method: see C-20261010-claude-b-02, part (d).

**6. Held-out results.**
- **Set 1** ($N=40$).
  - $\lambda_{\min}$, $\lambda_{\rm pass}$ and $\lambda_{\rm gen}$ pass at both points.
  - The best-single-interval extrapolation passes at 0.7 and **fails** at 1.0: actual 0.732, predicted 0.827 ± 0.06. The interval trend in $N$ is not understood.
  - Measured afterwards (`interval_edges.json`): for large $N$ the best band is symmetric, cutting near the outer spectral ears ($|v|$ ≈ 0.6–0.74, about 2% of photons removed), and its $F$ saturates near 0.73–0.82. At small $N$ it is asymmetric. That change of regime is why a steady-rise extrapolation failed.
- **Set 2.** 18 of 18 frozen predictions pass:
  - $\lambda_{\min}$ within $2/\Phi^2$ (measured $c$ = 0.74, 1.51, 1.33);
  - $\lambda_{\rm pass}$ within 5%, and $=\lambda_2$;
  - centroid ratio within 1%;
  - $\lambda_{\rm gen}$ within 1 dB of it;
  - binary gap ≥ 10 dB.

**6b. Held-out set 3** (frozen in `d6ab3a9`; $N=18$, $z/z_{\rm wb}=0.9$). 4 of 4 pass:
- formula $-0.35\%$;
- centroid $-0.33\%$, with $\lambda_{\rm gen}$ 0.32 dB below it;
- parity bound 12.5 dB above $\lambda_{\rm gen}$;
- best binary 4.6 dB above the parity bound (frozen bracket 2–6.5 dB).

**6c. Held-out set 4** (frozen in `7c6ea32`; $N=28$, $z/z_{\rm wb}=0.5$). 4 of 4 pass:
- formula $-0.34\%$;
- centroid $-0.10\%$, with $\lambda_{\rm gen}$ 0.41 dB below it;
- parity bound 12.1 dB above $\lambda_{\rm gen}$;
- best binary 5.5 dB above the parity bound.

**7. Second solver.**
- **Kerr only.** It reproduces my numpy filtered $F$ to $\le1.4\times10^{-6}$.
- **Self-steepening** ($T_0=100$ fs, 1550 nm, $N=10$) changes the best binary filter's $F$ by +0.01 to +0.02. Photon-energy weighting alone moves $F$ by up to 0.018.
- **Raman** at 300 K (coth spectrum) raises the best binary $F$ from 0.451 to 0.504. The reservoir part is 0.038, and 0.11 for the interval.

**7a. Discrete-adjoint comparison over the requested grid** (run `2026-10-10-claude-b.6-solver-grid`, blind, frozen 12:53:19).
- **Points.** $N$ = 5, 10, 20 × $z/z_{\rm wb}$ = 0.3, 0.7, 1, 1.5.
- **Agreement.** FastDifferentiableMMNLO reproduces $\lambda_{\rm gen}$ (via its eigenvector weight) to $\le1.0\times10^{-5}$, the centroid readout to $\le1.0\times10^{-5}$ and the best binary filters to $\le2.6\times10^{-6}$.
- **Identity.** The full-grid centroid identity holds to $\le2.4\times10^{-6}$, and to about $10^{-13}$ at most points.
- **Source of the differences.** My Strang step: halving it moves the numpy values by 1–2$\times10^{-6}$, while the solver is converged to $10^{-12}$.
- **Not covered.** $\lambda_{\min}$ and $\lambda_{\rm pass}$ come from the same validated Jacobian but are not photon-number observables, so the solver did not compute them directly.
- **Resolution caveat.** At N10 and N20 for $z/z_{\rm wb}=1.5$, the spectra reach 0.86–0.88 of the Nyquist frequency on my grid. Doubling $N_t$ moves the solver values there by $\le2\times10^{-6}$ relative, which is negligible for every statement here.

**7b. Weighted readouts in the solver, with Raman** (run `2026-10-10-claude-b.6-solver-weighted-raman`).
- **Identity.** The centroid identity holds in FastDifferentiableMMNLO to $2\times10^{-12}$ when the weight covers all bins.
- **$\lambda_{\rm gen}$.** The $\lambda_{\rm gen}$ eigenvector weights reproduce the numpy $\lambda_{\rm gen}$ to $10^{-8}$.
- **Raman at $T_0=100$ fs, 300 K.**
  - The reservoir adds about 0.036 to the centroid and to the $\lambda_{\rm gen}$-optimal weighted readouts, roughly doubling them (0.035 → 0.073).
  - The deterministic delayed response breaks the identity by 7–10%.
  - The best binary filter rises only from 0.451 to 0.490 (0.504 with self-steepening).
- **Fragile weight.** At N20, $z/z_{\rm wb}=0.3$, the Kerr-optimal eigenvector is fragile under self-steepening and Raman (0.029 → 0.107), while the centroid weight is robust (0.035 → 0.074).

**7c. Raman floor on the bounds** (run `2026-10-10-claude-b-nd-raman`, numpy oracle plus the coth reservoir at 300 K).
- **Validation.** Against the solver, the reservoir part of the centroid and eigenvector readouts agrees to 0.4%.
- **Size of the floor.** It raises $\lambda_{\min}$ by 2.1–5.8 times at the seven points computed: $N$ = 5–20, $z/z_{\rm wb}$ = 0.3, 0.7, 1.5, $T_0$ = 50 fs to 1 ps.
- **Form of the excess.** $\Delta\lambda_{\min}\approx\rho(Z)\,\hat c(0)/\Phi$, with $\hat c(0)=0.1148$ the thermal low-frequency phonon level. It depends weakly on $T_0\ge100$ fs.
- **The law.** On six points, $\rho\approx\sqrt{4Z^2\Lambda(Z)}$, i.e. $\lambda_{\min}\approx\Lambda/N^2+2\hat c(0)\sqrt\Lambda/N$. Three frozen predictions (commit `bad387c`) then passed: $-8.1\%$ at $Z=0.32$, $+2.9\%$ at $Z=1.59$, $+3.5\%$ at $Z=3.19$ (tolerance 15%). A fourth at N28 passed at $-5.6\%$ (commit `ff8d25e`, tolerance 10%). This is claim C-20261010-claude-b-03. The ratio $\rho/\sqrt{4Z^2\Lambda}$ at $Z\approx0.74$ levels off near 0.95 with $N$.
- **Slopes.** $N^2\Delta\lambda/\Phi$ is constant from N10 to N20 at fixed $Z$: 0.27 ($\lambda_{\min}$), 0.38 ($\lambda_{\rm pass}$), 0.46 ($\lambda_{\rm gen}$, centroid) at $Z=0.74$.
- **Crossover.** Raman dominates once $\Phi\gtrsim3$.
- **Binary filters.** Raman adds only 0.025–0.035 to the best binary filter. So with Raman, the binary filter sits 14.6 dB above $\lambda_{\min}$ at N20, $z/z_{\rm wb}=0.7$, instead of 21.9 dB.

**7d. Dispersionless limit** (run `2026-10-10-claude-b-nd-dispersionless`; cross-check numbers for T-20261010-claude-interactive-04).
- **Model.** Pure SPM of the Gaussian at $\Phi$ = 1, 2, 5, 10.
- **$\lambda_{\min}$.** It equals $V_{\min}(\Phi)=(\sqrt{1+\Phi^2}-\Phi)^2$ to 6 digits, and $\lambda_{\rm pass}\approx\lambda_{\min}$. These are the $Z\to0$ limits of claim 01.
- **Centroid.** The readout equals $1/(1+0.770\Phi^2)$ to $10^{-6}$.
- **$\lambda_{\rm gen}$.** 0.456, 0.231, 0.0446, 0.0114: 0.25–0.93 dB below the centroid, and $\approx1.14/\Phi^2$ at large $\Phi$, i.e. 6.6 dB above $\lambda_{\min}$.
- **Binary filters.** The best found are 0.849, 0.702, 0.679, 0.580. The best single interval goes to 1 at $\Phi=10$.

**8. Parabola cross-check** (run `2026-10-10-claude-b-nd-parabola`).
- **Comparison.** The reduced numerics on a parabolic input were compared with the leading-order $C$-block that I derived from claude-a's Legendre propagator (C-20261004-claude-a-01, statement (a)).
- **Even sector ($\Lambda_{\rm par}$).** At $N=100$ the agreement is $-0.04\%$, $-0.02\%$, $-0.01\%$, $+0.02\%$ and $+0.11\%$ at $\zeta$ = 0.1, 0.25, 0.5, 1, 2. At $N=50$ it is within 0.27% up to $\zeta=4.74$.
- **Odd sector ($\Pi_{\rm par}$).** The agreement is within 0.06% for $\zeta\le0.5$, but the numerics are 0.54% higher at $\zeta=1$ and 1.93% higher at $\zeta=2$, at both $N=50$ and $100$.
  - It does not shrink with $N$, but it does shrink with the size of the Hermite basis used for the input perturbations ($N=50$, `basis_check.json`). At $\zeta=2$ the $\Pi$ excess is 2.0%, 1.1% and 0.88% for $M$ = 80, 160, 240, and the $\Lambda$ excess is 0.14%, 0.10% and 0.075%.
  - So the difference is slow basis convergence at the parabola's hard (square-root) edge, not an error in the propagator. For the smooth Gaussian, $M$ = 80 vs 160 changes $\Lambda$ and $\Pi$ by $<4\times10^{-7}$ (`curve_N50_M160.json`).
  - The $l=1$ block was also checked by hand: $|m_1|=\mu$, the apparent phase of a timing shift on the chirped pulse.
- **By-product (not a claim).** A closed-form leading order $\lambda_{\min}$ for the parabolic pulse: $4\zeta^2\Lambda_{\rm par}$ = 1.091, 1.263, 1.640, 2.674, 5.523 and 17.11 at $\zeta$ = 0.1, 0.25, 0.5, 1, 2 and 4.737. This is larger than the Gaussian's at equal $Z$.

**9. Root-01 anchors** (run `2026-10-10-claude-b-nd-anchor-map`).
- **Mapping.** The two zero-GDD anchors are at $N$ = 4.26 and 3.15, $\Phi$ = 1.36 and 2.97, $z/z_{\rm wb}$ = 0.29 and 0.84.
- **Gaussian Kerr-only analogue at the same $N$ and $\xi$:**

| anchor | anchor bandpass here | registered $F$ (minus its Raman term) | best binary | $\lambda_{\rm gen}$ | $\lambda_{\rm pass}$ | $\lambda_{\min}$ |
|---|---|---|---|---|---|---|
| 0.25 m | 0.864 | 0.925 (0.909) | 0.790 | 0.377 | 0.198 | 0.136 |
| 1 m | 0.721 | 0.834 (0.798) | 0.639 | 0.202 | 0.145 | 0.058 |

- **Reading.** The binary optimum lies below the fixed bandpass, as it must. The remaining 0.05–0.08 difference from the anchors reflects the measured, non-Gaussian input spectrum, which was not modelled.
- **Parity bracket** (`anchor_parity.json`). The binary optimum of these Gaussian analogues lies in [0.455, 0.790] at 0.25 m and [0.439, 0.639] at 1 m: a bracket of 2.4 dB and 1.6 dB.

**11. Cross-check with T-20261010-claude-interactive-04** (claude-a, branch `task/T-20261010-claude-interactive-04`, read at 13:34 as unverified work in progress).
- **Centroid bound: concurrent overlap.** Their C-20261010-claude-a-02 states the same centroid bound as my C-20261010-claude-b-02(a). Both were found independently in this round.
  - Their dispersionless Gaussian form $(1+\tfrac{4}{3\sqrt3}\Phi^2)^{-1}$ equals my $1/(1+0.770\Phi^2)$.
  - Their tightness $\lambda_{\rm gen}/\lambda_P$ = 0.81 ($\Phi=1$) and 0.89 ($\Phi=10$, threshold $10^{-9}$) matches mine: 0.807 and 0.888 (run `2026-10-10-claude-b-nd-dispersionless`).
- **Weak-dispersion coefficient.** Their C-20261010-claude-a-01, item 5, reduces for the Gaussian at large $\Phi$ to a relative correction $\sqrt{2/3}\,Z(1+c_2Z)$. That is exactly my small-$Z$ coefficient $2/\sqrt6$, and their $c_2\simeq1.0$ matches my next coefficient from the exact $\varepsilon=0$ values ($c_2$ = 0.99–1.02). Two independent methods agree.
- **Parity bound.** Their C-20261010-claude-a-03 states that for parity-symmetric problems every non-negative filter has $F\ge(\lambda_{\rm odd}+\lambda_{\rm even})/2$. I checked the proof sketch and evaluated it on my 33 resolved normal-dispersion points (`parity_bound.json`).
  - $\lambda_{\rm odd}=\lambda_{\rm gen}$ at every point, so the optimal weighted mode is odd (centroid-like).
  - $F_{\rm par}$ is 7–16 dB above $\lambda_{\rm gen}$ for $N\ge10$, growing with $N$, and 2.2–6.3 dB below the best binary found.
  - So most of the binary gap in my regime is certified, and the open part (T-20261010-claude-b-04) shrinks to 2–6 dB.
  - **Independent reproduction.** My own dispersionless oracle reproduces their reported parity numbers at $\Phi=20$: $F_{\rm par}$ = 0.1519, 0.1437, 0.0614 against their 0.152, 0.144, 0.061 for thresholds $10^{-6}$, $10^{-9}$, $10^{-12}$ (run `2026-10-10-claude-b-nd-dispersionless`, `parity_phi20.json`). This is an independent code but the same family, so it is not a cross-family verification.
  - **With Raman.** With the 300 K reservoir the best binary filters are only 3.1–4.1 dB above $F_{\rm par}$ (`parity_raman.json`). For room-temperature silica, $F_{\rm par}$ is thus a fast lower bound on binary filters that is tight to about 4 dB at these points.
  - **Bin-set sensitivity.** Unlike the dispersionless case reported on the -04 branch, $F_{\rm par}$ here barely depends on dark bins: +6–12% from threshold $10^{-12}$ to $10^{-4}$ (`parity_threshold.json`).
  - **Where the rest goes** (`parity_anatomy.json`).
    - The best binary filters put a near-maximal odd fraction into the odd sector: $f$ = 0.34–0.46 against the bound's 0.5, at $Z\le1.06$.
    - Their odd part's Rayleigh quotient is 7–136 times $\lambda_{\rm odd}$; a binary pattern cannot reproduce the smooth, centroid-like odd mode.
    - Their even part's quotient is about 2 times $\lambda_{\rm even}$.
    - At N10, $z/z_{\rm wb}=2$ the filter hardly uses the odd sector ($f=0.10$).

**10. Self-steepening in the oracle.**
- At $sN\le0.16$ the change is ≤ 0.4% on $\lambda_{\min}$ and ≤ 0.5% on $\lambda_{\rm gen}$.
- The oracle's self-steepening model does not conserve $\sum\omega|\alpha|^2$ or $\sum\omega|\alpha|^2/(1+s\omega)$. The centroid identity therefore needs a photon-and-energy-conserving model when $s\ne0$; untested.

## Literature (this regime)

Access levels: "abstract" means the abstract was read via OpenAlex or the publisher page; nothing here was read in full.

**Wave breaking in normal dispersion.**
- Anderson, Desaix, Lisak & Quiroga-Teixeiro, JOSA B 9, 1358 (1992), [DOI:10.1364/JOSAB.9.001358](https://doi.org/10.1364/JOSAB.9.001358): wave breaking in nonlinear-optical fibres. Abstract only (OpenAlex reconstruction; closed access). It is the usual source of $z_{\rm wb}=L_D/\sqrt{4N^2e^{-3/2}-1}$, but I could not confirm the formula in the text.
- Finot, Kibler, Provost & Wabnitz, JOSA B 25, 1938 (2008), [DOI:10.1364/JOSAB.25.001938](https://doi.org/10.1364/JOSAB.25.001938): optical wave breaking, revisited. Abstract only: the HAL copy is behind an Anubis bot check, which I did not bypass, and the Southampton repository returned 403.

**Dispersive hydrodynamics and quantum fluctuations.**
- El & Hoefer, Physica D 333, 11 (2016), [DOI:10.1016/j.physd.2016.04.006](https://doi.org/10.1016/j.physd.2016.04.006), arXiv:1602.06163: dispersive shock waves and modulation theory. Abstract only.
- Larré & Carusotto, PRA 92, 043802 (2015), [DOI:10.1103/PhysRevA.92.043802](https://doi.org/10.1103/PhysRevA.92.043802): propagation of a quantum fluid of light in a cavityless nonlinear medium. Abstract only.
- Urilyon, Scopa & Del Vecchio, PRB 111, 045401 (2025), [DOI:10.1103/PhysRevB.111.045401](https://doi.org/10.1103/PhysRevB.111.045401): quantum fluctuations around dispersive shock waves. Abstract only.

**Filtered squeezing in fibre.**
- König et al., J. Mod. Opt. 45, 2425 (1998), [DOI:10.1080/09500349808230495](https://doi.org/10.1080/09500349808230495). Abstract only (from the card).
- Nishizawa et al., JJAP 38, 1961 (1999), [DOI:10.1143/JJAP.38.1961](https://doi.org/10.1143/JJAP.38.1961). Abstract only.
- Nishizawa, Higuchi, Mori, Yamane & Goto, JJAP 39, 5842 (2000), [DOI:10.1143/JJAP.39.5842](https://doi.org/10.1143/JJAP.39.5842): band-pass and band-rejection filtering, anomalous dispersion, 23 dB intensity-noise reduction. Abstract only.
- Kannari, Ohno, Furumochi & Nakazawa, EQEC 2003, [DOI:10.1109/EQEC.2003.1314209](https://doi.org/10.1109/EQEC.2003.1314209): input spectral-phase shaping improves filtered squeezing, including in normal dispersion. Abstract only.

**General quantum-noise theory.**
- Ng, Yanagimoto, Jankowski, Fejer & Mabuchi, [arXiv:2307.05464](https://arxiv.org/abs/2307.05464): Gaussian split-step method for quantum noise. Abstract only.
- Corney & Drummond, JOSA B 18, 153 (2001), [DOI:10.1364/JOSAB.18.000153](https://doi.org/10.1364/JOSAB.18.000153): Raman jitter of solitons from the phonon reservoir. Abstract only.

**Hidden squeezing and mode decompositions.**
- Gouzien, Labonté, Etesse, Zavatta, Tanzilli & D'Auria, PRR 5, 023178 (2023), [DOI:10.1103/PhysRevResearch.5.023178](https://doi.org/10.1103/PhysRevResearch.5.023178): pulsed microresonators; optimal squeezing is "hidden" from standard homodyne detection. This is the same kind of gap as $\lambda_{\min}(V)$ versus a restricted readout. Abstract only.
- Konyukhov, Konyukhova & Melnikov, Laser Phys. (2024), [DOI:10.1088/1555-6611/ad2447](https://doi.org/10.1088/1555-6611/ad2447): squeezing in dispersion-oscillating fibres via Karhunen–Loève modes. Abstract only.

**Searches (OpenAlex API).** None of these returned a treatment of quadrature or filtered squeezing limits of semiclassical normal-dispersion pulses, or a statement of the spectral-centroid identity.
- "quantum noise optical wave breaking normal dispersion squeezing"
- "quantum fluctuations dispersive shock wave Bogoliubov expanding condensate"
- "dispersive shock waves modulation theory review"
- "momentum conservation quantum nonlinear Schrodinger squeezing spectral centroid"
- "soliton momentum squeezing frequency fluctuations conserved quantum"
- "photon number squeezing spectral filtering normal dispersion fiber pulse"
- "mean frequency noise pulse quantum nonlinear fiber conserved momentum"
- "quadrature squeezing optical pulse normal dispersion fiber optimal squeezing limit"
- "pulsed Kerr squeezing dispersion covariance eigenvalue optimal mode fiber"
- "squeezing self-phase modulation normal dispersion fiber broadband multimode squeezed modes"
- "optimal squeezing Kerr pulse dispersion supermode decomposition"

The conservation of soliton momentum in the quantum NLSE is standard (e.g. the Lai–Haus line of work, not accessed here), so part (a) of C-20261010-claude-b-02 may be known in another form. Its novelty confidence is low.

## Proposed card changes

For P-20261010-claude-interactive-01; I did not edit the card.

1. **Approaches table, approach 2: add results.**
   - $\lambda_{\min}$ and $\lambda_{\rm pass}$ have leading-order formulas $\Lambda(Z)/N^2$ and $\Pi(Z)/N^2$ (C-20261010-claude-b-01), valid before and after wave breaking to $z/z_{\rm wb}=3$.
   - $\lambda_{\rm gen}$ is within 0.9 dB below the closed form $\langle\Delta\omega^2\rangle_{\rm in}/\langle\Delta\omega^2\rangle_{\rm out}$ (C-20261010-claude-b-02).
   - No formula for binary filters. The best found are 10–22 dB above $\lambda_{\rm gen}$ for $N\ge14$.
1b. **Merge or cross-reference.** C-20261010-claude-b-02 and C-20261010-claude-a-02 state the same centroid bound and were found concurrently. Their regimes are complementary: normal dispersion with $N\gg1$ here, and the dispersionless case with Raman there.
2. **"What the gaps mean": add a third case.** A large $\min_TF/\lambda_{\rm gen}$ can come from the sign constraint rather than from binary-ness. In normal dispersion the $\lambda_{\rm gen}$ minimizer is close to the spectral-centroid weight, which changes sign. Weighted multi-pixel counting with signed weights recovers it; binary or non-negative masks with one detector cannot.
   - Consequence for the card's goal: a tight fast bound on binary filters in this regime must use non-negativity. Relaxations that only use $T_i^2=T_i$ on top of $\lambda_{\rm gen}$ will inherit a gap that grows with $N$.
   - Suggest adding $\lambda_{\rm gen}^{+}=\min_{w\ge0}w^{\mathsf T}\Sigma w/w^{\mathsf T}{\rm diag}(\bar n)w$ to the hierarchy: $\lambda_{\rm gen}\le\lambda_{\rm gen}^{+}\le\min_TF$.
   - For parity-symmetric problems, the parity bound of C-20261010-claude-a-03 is a cheap rigorous lower bound on $\lambda_{\rm gen}^{+}$. In normal dispersion it certifies most of the binary gap (Found 11).
3. **"Signal of hidden simplicity": add a bullet.** Momentum conservation gives an exact Fano factor for the spectral-centroid readout in any Kerr-only scalar fibre, equal to the squared ratio of input to output rms bandwidths.
   - It extends to several modes (total momentum, derivation only, untested).
   - In the dispersionless limit it gives $\lambda_{\rm gen}\le1/(1+2\Phi^2\langle\rho_\tau^2\rangle_\rho)=1/(1+0.770\Phi^2)$ for a Gaussian. This is a cross-check for T-20261010-claude-interactive-04.
4. **Oracle section: add a resolution check.** On any Kerr-only covariance, the centroid identity is a free test of grid resolution; it caught three under-resolved grids here.
4a. **Readout hierarchy: correct the expectation that $\lambda_{\rm pass}$ "usually sits close to $\lambda_{\min}(V)$".**
   - Supporting data first: the chain $\lambda_{\min}\le\lambda_{\rm pass}\le\lambda_{\rm gen}\le$ best binary holds at all 54 points computed in this lane, with no violation. That is 38 oracle, 3 held-out, 7 Raman-reservoir, 4 dispersionless and 2 anchor points. This is evidence for T-20261010-claude-interactive-03, not a proof.
   - For a symmetric pulse, parity makes $\lambda_{\rm pass}=\lambda_2(V)$, the smallest odd-sector eigenvalue. This was observed at 14 points.
   - The global-phase constraint removes the even, most-squeezed mode, which in this regime is the correlation between total photon number and global phase.
   - In normal dispersion at $N\gg1$, $\lambda_{\rm pass}/\lambda_{\min}=\Pi(Z)/\Lambda(Z)$ = 2.0 dB at $Z=0.3$, 4.0 dB at 0.75, 4.8 dB at 1.0, 6.0 dB at 1.5, 7.4 dB at 3 and 9.4 dB at 10. It tends to 0 dB only in the dispersionless limit.
4b. **"Raman sets the floor": confirm and sharpen it for normal dispersion.**
   - For the bounds themselves, the reservoir term is about $\rho(Z)\hat c(0)/\Phi$ with $\rho$ = 1.1–1.9, against the Kerr term's $\Lambda(Z)/N^2$. Here $\hat c(0)=4af_Rk_BT/[\hbar(a^2+b^2)]$ is the thermal low-frequency phonon level (0.114 at 300 K).
   - Raman dominates $\lambda_{\min}$, $\lambda_{\rm pass}$ and $\lambda_{\rm gen}$ once $\Phi\gtrsim3$ (run `2026-10-10-claude-b-nd-raman`).
   - Binary filters move only by 0.03.
   - A fast formula for the card in this regime is therefore $\Lambda(Z)/N^2+\rho(Z)\hat c(0)/\Phi$ for $\lambda_{\min}$ (empirical $\rho$; still a lower bound only if the deterministic response is negligible).
5. **Anchors.** The registered root-01 bandpass values (F = 0.925 at 0.25 m, 0.834 at 1 m, zero GDD) map to $(N,Z,\Phi)$ = (4.26, 0.319, 1.36) and (3.15, 0.942, 2.97).
   - For a Gaussian, Kerr only, the same bandpass gives 0.864 and 0.721, and the best binary filter 0.790 and 0.639 (run `2026-10-10-claude-b-nd-anchor-map`).
   - So at the anchors the binary optimum gains about 0.07–0.08 over the fixed bandpass.
   - The anchors are below $N=5$; the formulas of C-20261010-claude-b-01 apply only roughly there.
6. **Literature state.** Add the entries above, and the wave-breaking caveat: the quoted $z_{\rm wb}$ corresponds to $Z=1.0585$, while the measured onset of oscillations is $Z\approx1.24$–$1.25$ and the dispersionless gradient catastrophe is $Z_b\approx1.27\pm0.02$.

## Changed

**New files.**
- The meanfield and semiclassical runs have no raw data; their `summary.json` and curve files hold all output.
- `claims/C-20261010-claude-b-01-semiclassical-lambda-min-normal-dispersion.md`
- `claims/C-20261010-claude-b-02-spectral-centroid-bound.md`
- `claims/C-20261010-claude-b-03-raman-floor-normal-dispersion.md`
- `explorations/2026-10-10-claude-b-semiclassical-normal-dispersion.md`

**Runs.** Each folder has `meta.yaml` and `summary.json`; raw data is in `~/analytical-nl-discovery-data/<run-id>/` on COECIS-G3FLW49YGQ.
- `2026-10-10-claude-b-nd-oracle`
- `2026-10-10-claude-b-nd-heldout`
- `2026-10-10-claude-b-nd-heldout2`
- `2026-10-10-claude-b-nd-meanfield`
- `2026-10-10-claude-b-nd-semiclassical`
- `2026-10-10-claude-b-nd-parabola`
- `2026-10-10-claude-b.6-solver-nd-check`
- `2026-10-10-claude-b.6-solver-weighted-raman`
- `2026-10-10-claude-b.6-solver-grid`
- `2026-10-10-claude-b-nd-raman`, `2026-10-10-claude-b-nd-convergence`, `2026-10-10-claude-b-nd-anchor-map`
- `2026-10-10-claude-b-nd-dispersionless`, `2026-10-10-claude-b-nd-centroid-general`, `2026-10-10-claude-b-nd-heldout3`, `2026-10-10-claude-b-nd-heldout4`

**Tasks.** New tasks T-20261010-claude-b-01 to -07; T-20261010-claude-interactive-05 set to done.

## Not verified

- **Leading-order structure** of C-20261010-claude-b-01. Its $\varepsilon$-independence is argued formally and checked numerically, not proved. The bound $c\le2$ is empirical. After breaking, the error exponent comes from two resolved $N$ values only, and $c$ drifts upward with $N$ (1.31 to 1.62 at $z/z_{\rm wb}=1.5$). That drift is within the reduced curve's own uncertainty at $\Phi\approx32$.
- **$\lambda_{\rm pass}=\lambda_2$** is proved only as $\le$. Equality is observed numerically at 6 points.
- **Binary filters.** All binary numbers are best found by heuristic search, not certified optima. The non-negative-weight numbers are heuristic too. Check: T-20261010-claude-b-04.
- **Raman.** Raman is not part of either claim's formula. The reservoir floor (Found 7c) is from seven points with my own normalization, validated against the solver for weighted readouts only. The deterministic delayed response is left out of it. Check: T-20261010-claude-b-03.
- **Mapping to root-01.** Only approximately checked; see Found 9. The anchors use a measured non-Gaussian spectrum with Raman at $N$ = 3–4, below this claim's regime. A reproduction would need that spectrum and Raman in the full covariance.
- **Card hierarchy.** The hierarchy $\lambda_{\min}\le\lambda_{\rm pass}\le\lambda_{\rm gen}$ was used as given; its proof is T-20261010-claude-interactive-03.
- **Independence.** Both claims are by the claude family, and the solver comparison was by a claude subagent, so neither claim can be marked sim-verified. Checks: T-20261010-claude-b-01 and -02 (non-claude).

## Loose ends

- T-20261010-claude-b-01: non-claude verification of C-20261010-claude-b-01.
- T-20261010-claude-b-02: non-claude verification of C-20261010-claude-b-02, including Raman and self-steepening breaking of the identity.
- T-20261010-claude-b-03: Raman floor on $\lambda_{\min}$, $\lambda_{\rm pass}$, $\lambda_{\rm gen}$.
- T-20261010-claude-b-04: certify a lower bound on non-negative-weight counting; is the binary gap real? The parity bound (Found 11) already certifies 7–16 dB of it; 2–6 dB remain.
- T-20261010-claude-b-05: asymptotic theory of fringe-comb binary filters.
- T-20261010-claude-b-06: full texts for the wave-breaking prefactor and normal-dispersion filtered-squeezing experiments.
- T-20261010-claude-b-07: non-claude verification of C-20261010-claude-b-03, with the deterministic Raman response.
- Not tasked, because it belongs to the dispersionless lane: the dispersionless closed form $\lambda_{\rm gen}\le1/(1+0.770\Phi^2)$ is offered to T-20261010-claude-interactive-04 as a cross-check.
- Not tasked, because it belongs to the soliton lane: the centroid bound holds in anomalous dispersion too. For a Gaussian at soliton order $N=3$, $\xi=0.5$, it gives $\lambda_{\rm gen}\le0.178$, against a computed $\lambda_{\rm gen}=0.127$ on the resolved 1024-point grid (run `2026-10-10-claude-b-nd-centroid-general`). It is offered to T-20261010-claude-interactive-06 as a cheap upper bound on $\lambda_{\rm gen}$.

## Stop

**Time.** Session from 10:34 to about 13:56 EDT (202 min). That is about 23 minutes before the 3 h 45 min mark.

**Not every item is done.** The leading-order formula for the best binary filter, the third target, was not obtained. In its place this session provides:
- the certified parity bracket (claude-a's bound evaluated in this regime: 2–6 dB wide Kerr-only, 3–4 dB with Raman, 1.6–2.4 dB at the anchor analogues);
- the empirical scaling;
- the filter anatomy;
- tasks T-20261010-claude-b-04 and -05.

**Why I stopped early.** The remaining minutes were not enough to make progress on that item. Every other item of the suggested order (literature, mean field, fluctuations, solver comparison on the requested grid, Raman and self-steepening, after wave breaking, cross-checks with -04 and the parabola, held-out tests) was carried out.
