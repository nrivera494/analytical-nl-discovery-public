---
id: C-20261008-claude-a-01
problem: P-001
title: "Amplifier similariton: the energy, centre-frequency, timing and compressed-timing noise follow exact moment equations driven by the pulse's own time-frequency covariance"
type: noise-formula
status: cheap-checks-passed
proposed_by: claude-a
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-08
updated: 2026-10-08
solver_commit: null
result: null
---

## Statement

**System.** A normally dispersive fibre amplifier with frequency-flat distributed power gain $g$ and spontaneous-emission (ASE) noise:
$$\partial_zA=-\tfrac i2\beta_2\partial_T^2A+i\gamma|A|^2A+\tfrac g2A+F,$$
with $\beta_2>0$, $\langle F^\dagger F\rangle=g\,n_{sp}\hbar\omega_0\delta(z-z')\delta(T-T')$ and a coherent seed of $N_0$ photons.

Covariances are symmetric-ordered (Wigner), with ASE strength $D=g(n_{sp}-\tfrac12)\hbar\omega_0$. Every variance below has the form $I_{\rm in}+(2n_{sp}-1)I_{\rm ase}$. Let $G=e^{gL}$, and let $E(z)$, $\Omega_c(z)$ and $T_c(z)$ be the pulse energy, centroid frequency and centroid time.

**(a) Exact moment structure (any seed shape and power; no hydrodynamic approximation).**
- Kerr and $\beta_2$ conserve energy and momentum, so without noise $E=E_0e^{gz}$, $d\Omega_c/dz=0$ and $dT_c/dz=\beta_2\Omega_c$.
- To first order in the noise:
  - the photon-number noise is that of a linear amplifier, $\mathrm{Var}(N)/\langle N\rangle^2=[1+(2n_{sp}-1)(1-1/G)]/N_0$;
  - $(T_c,\Omega_c)$ is a Gaussian process with drift $(\beta_2\Omega_c,0)$ and increment covariance $\tfrac{2D}{E(z)}W(z)\,dz$;
  - $W$ is the noise-free pulse's own time–frequency covariance: rms width², the symmetrized time–instantaneous-frequency covariance, and rms bandwidth² including the transform-limited part;
  - the input vacuum adds $W(0)/N_0$.
- A linear compressor of group-delay dispersion $D_c$ gives $T_{\rm comp}=T_c+D_c\Omega_c$. We use $D_c=-C_L/\sigma_{\omega L}^2$, the rms-optimal value.

The amplifier acts on the collective coordinates only through $W(z)$. The attraction to the similariton enters the collective-coordinate noise only by shaping $W(z)$.

**(b) Similariton evaluation (leading order in $\varepsilon_0$).** With a parabolic background of half-width $T_p(z)$, the chirp dominates. Then $W=\tfrac{T_p^2}{5}\begin{pmatrix}1&\kappa\\\kappa&\kappa^2\end{pmatrix}$ with $\kappa=\dot T_p/(\beta_2T_p)$. In units $x=T/T_0$, $\zeta=z/\sqrt{L_DL_{NL}}$, with $a=T_p/T_0$ and $\Gamma=g\sqrt{L_DL_{NL}}$:
- the background obeys $a''=2e^{\Gamma\zeta}/a^2$;
- $X(\zeta)=a+a'(\zeta_L-\zeta)$ is the width extrapolated to the output, and $h=X-a'a_L/a'_L$;
- then
$$N_0\mathrm{Var}(T_c)=\tfrac{T_0^2}5\Big[X(0)^2+(2n_{sp}-1)\Gamma\!\!\int_0^{\zeta_L}\!\!e^{-\Gamma\zeta}X^2d\zeta\Big],\qquad N_0\mathrm{Var}(T_{\rm comp})=\tfrac{T_0^2}5\Big[h(0)^2+(2n_{sp}-1)\Gamma\!\!\int\!e^{-\Gamma\zeta}h^2\Big],$$
$$N_0\mathrm{Var}(\Omega_c)=\tfrac1{5\varepsilon_0^2T_0^2}\Big[a'(0)^2+(2n_{sp}-1)\Gamma\!\!\int\!e^{-\Gamma\zeta}a'^2\Big].$$

**(c) Closed forms for a seed launched on the similariton asymptote.** Let the seed have rms width $\sigma_{T0}$ and rms bandwidth $\sigma_{\omega0}=\tfrac g{3\beta_2}\sigma_{T0}$. Then:
- centroid frequency: $N_0\mathrm{Var}(\Omega_c)/\sigma_{\omega0}^2=1+3(2n_{sp}-1)(1-G^{-1/3})$;
- output timing: $N_0\mathrm{Var}(T_c)/\sigma_{T0}^2=(1+\tfrac{gL}3)^2+(2n_{sp}-1)(3+\tfrac{(gL)^2}3-3G^{-1/3})$;
- compressed timing: $N_0\mathrm{Var}(T_{\rm comp})/\sigma_{T0}^2=\tfrac{(gL)^2}9+(2n_{sp}-1)(\tfrac{(gL)^2}3-2gL+6(1-G^{-1/3}))$.

For comparison, a linear amplifier gives $1+(2n_{sp}-1)(1-G^{-1})$ for both the centre frequency and the compressed timing (ideal dispersion compensation).

So, against linear amplification:
- the energy noise is unchanged;
- the centroid-frequency noise figure rises from $2n_{sp}$ to $6n_{sp}-2$, because the spectrum broadens as $G^{1/3}$;
- the compressed-pulse timing variance grows as $(gL)^2$ instead of saturating.

**Mechanism for the compressed timing.** An ASE kick at $z'$ moves time and frequency together along the local chirp. On the asymptote it reaches the compressed output as $\delta T\cdot\tfrac g3(L-z')$.

## Regime

The moment structure (a) holds exactly within the model below for every $N_0$ and seed. The evaluations (b) and (c) are leading order in $\varepsilon_0$.

- $\varepsilon_0=\sqrt{\beta_2/(\gamma P_0T_0^2)}\le0.1$. The relative error of (b) and (c) is $O(\varepsilon_0^2\ln(1/\varepsilon_0))$: the dropped transform-limited bandwidth of the sharp-edged parabola.
- $0.5\le\Gamma\le10$ and $gL\le12$.
- $N_0\ge10^4$ and $N_0\gg n_{sp}$ (linearization).
- The detected ASE in the centroid window is small against the signal: $n_{sp}GM_w\ll GN_0$, with $M_w$ the number of modes in the window.
- Gain flatness: $gL(\omega_{\rm edge}(L)/\Omega_g)^2\le0.05$. Here $\omega_{\rm edge}(L)=\kappa_LT_p(L)$ is the output spectral half-width, and $\Omega_g$ the curvature scale of $g(\omega)=g[1-(\omega/\Omega_g)^2]$.
  - At the bound, gain filtering adds a restoring drift $\approx-2g\sigma_\omega^2\Omega_c/\Omega_g^2$. This damps the centroid-frequency noise by roughly 10%.
- Raman: the deterministic Raman shift $\Delta\Omega_R=2T_R\int\gamma P_{\rm peak}/T_p^2\,dz\le0.01\,\omega_{\rm edge}(L)$, and $T_R/T_p(0)\le0.01$.
  - Raman would couple energy noise into $\Omega_c$, because the Raman shift depends on energy, and would add spontaneous-Raman noise. Both are neglected.
- Third-order dispersion: $\delta_3=\beta_3\omega_{\rm edge}(L)/(3\beta_2)\le0.02$.
- Self-steepening: $\omega_{\rm edge}(L)/\omega_0\le0.01$.
- Gain saturation: output energy much smaller than the saturation energy.

**Example systems** (run `2026-10-08-claude-a-amp-sim-checks`, `example_systems`; $\beta_2=25$ ps²/km, $\gamma=5$ W⁻¹km⁻¹, 1.03 µm).
- **Typical short, low-energy seed** ($T_0=0.2$ ps, 10 pJ, $g=1.9$ m⁻¹, 3.2 m):
  - $\varepsilon_0=1.83$, $\Gamma=5.6$, $gL=6.1$;
  - outside (b) at launch, because it is not semiclassical;
  - only (a) applies, with $W(z)$ taken from simulation or measurement.
- **Energetic parabolic seed** ($T_0=3$ ps, 500 pJ, $g=0.2$ m⁻¹, 30 m):
  - $\varepsilon_0=0.067$, $\Gamma=4.8$, $gL=6$, $N_0=2.6\times10^9$;
  - inside (b), but the output spectral half-width is 9.7 THz;
  - Yb gain filtering would then break the gain-flatness bound unless $gL$ is reduced.
- In practice, similariton amplifiers are limited by gain bandwidth and by a non-semiclassical launch. Part (a) is the lab-usable statement.

## Assumptions

1. Scalar 1D NLSE, one polarization and mode (inherited).
2. Instantaneous Kerr response; no Raman, self-steepening or third-order dispersion.
3. Frequency-flat, unsaturated, distributed gain $g$ (rate-equation gain with fixed inversion).
4. ASE is white (delta-correlated in $z$ and $T$), with spontaneous-emission factor $n_{sp}$. The symmetric ordering is as stated. ASE–ASE beat terms are neglected.
5. Linearization in the noise (Gaussian channel).
6. For (b) and (c): the background is the dispersionless parabolic solution with sharp edges. Its transform-limited bandwidth is dropped (leading order in $\varepsilon_0$). The hydrodynamic width $a(\zeta)$ is used in place of the true rms width.
7. The compressor is lossless, linear, and set to the rms-optimal $D_c$ for the mean output.

## Predictions

Frozen 2026-10-08. All numbers are from run `2026-10-08-claude-a-amp-sim-checks` (`numeric.json`). Each entry is (input-vacuum part $I_{\rm in}$, ASE part $I_{\rm ase}$); the variance is $I_{\rm in}+(2n_{sp}-1)I_{\rm ase}$.

**P1. Energy (exact).** $N_0\mathrm{Var}(N)/\langle N\rangle^2=1+(2n_{sp}-1)(1-1/G)$ for any $\gamma$, $\beta_2$ and seed, with Kerr on or off.

**P2. Exact moment formula.** Take the noise-free simulated pulse, compute $W(z)$ from it, and insert it into (a). This must reproduce the simulated centroid covariances at every $\varepsilon_0$. The discrepancy should be at the level of the linearization ($O(n_{sp}G/N_{\rm out})$) and of the finite gain bandwidth, if any.

**P3. Main case, leading order.** $\Gamma=\sqrt{18}$ (seed width equal to the asymptotic width constant), unchirped parabolic seed. The table gives the hydrodynamic background ($a_L$, $a'_L$) and the scaled variances:
- $N_0\mathrm{Var}(T_c)/\sigma_{TL}^2$, with $\sigma_{TL}^2=a_L^2T_0^2/5$;
- $N_0\mathrm{Var}(T_{\rm comp})/T_0^2$;
- $N_0\mathrm{Var}(\Omega_c)/\sigma_{\omega L}^2$, with $\sigma_{\omega L}^2=a_L'^2/(5\varepsilon_0^2T_0^2)$;
- $N_0\varepsilon_0\mathrm{Cov}(T_c,\Omega_c)$.

| $gL$ | $a_L$ | $a'_L$ | $N_0\mathrm{Var}(T_c)/\sigma_{TL}^2$ | $N_0\mathrm{Var}(T_{\rm comp})/T_0^2$ | $N_0\mathrm{Var}(\Omega_c)/\sigma_{\omega L}^2$ | $N_0\varepsilon_0\mathrm{Cov}$ |
|---|---|---|---|---|---|---|
| 2 | 1.4154 | 2.2098 | (0.4991, 0.5964) | (0.2, 0.1242) | (0, 0.1051) | (0, 0.1224) |
| 4 | 3.3747 | 6.2614 | (0.0878, 0.2529) | (0.2, 0.2484) | (0, 0.05348) | (0, 0.4169) |
| 6 | 7.5181 | 11.6806 | (0.01769, 0.1073) | (0.2, 0.4557) | (0, 0.02294) | (0, 0.7899) |

**P4. Asymptotic seed (closed forms).** Formulas (c), checked against numerics to $10^{-7}$ (C4). For example, at $gL=6$ and $n_{sp}=1$:
- $N_0\mathrm{Var}(T_{\rm comp})/\sigma_{T0}^2=4+5.19$;
- $N_0\mathrm{Var}(\Omega_c)/\sigma_{\omega0}^2=1+2.59$.

**P5. Held-out case (not used to build anything above).** $\Gamma=1$, unchirped parabolic seed. The pulse first expands almost passively and approaches the asymptote late.

| $gL$ | $a_L$ | $a'_L$ | $N_0\mathrm{Var}(T_c)/\sigma_{TL}^2$ | $N_0\mathrm{Var}(T_{\rm comp})/T_0^2$ | $N_0\mathrm{Var}(\Omega_c)/\sigma_{\omega L}^2$ | $N_0\varepsilon_0\mathrm{Cov}$ |
|---|---|---|---|---|---|---|
| 2 | 4.4735 | 2.8631 | (0.04997, 0.4347) | (0.2, 0.1815) | (0, 0.2435) | (0, 0.8106) |
| 4 | 11.5923 | 4.2846 | (0.007441, 0.3484) | (0.2, 0.8832) | (0, 0.1808) | (0, 2.465) |
| 6 | 22.1913 | 6.5861 | (0.002031, 0.2364) | (0.2, 3.923) | (0, 0.08558) | (0, 4.124) |

**P6. Against linear amplification** (same seed, $\gamma=0$, ideal compression). Compressed timing $N_0\mathrm{Var}(T_{\rm comp})/T_0^2=0.2[1+(2n_{sp}-1)(1-1/G)]$; at $n_{sp}=1$, $gL=6$ this is 0.3995. The similariton gives:
- main case: 0.656, i.e. ×1.64;
- held-out case: 4.12, i.e. ×10.3.

**P8. Realistic seed, outside the semiclassical regime: tests (a) only.**

*Inputs.*
- Seed: Gaussian, 250 fs intensity FWHM, 10 pJ, 1030 nm, so $N_0=5.19\times10^7$.
- Amplifier: $\beta_2=25$ ps²/km, $\gamma=5$ W⁻¹km⁻¹, $g=1.9$ m⁻¹, $L=3.2$ m ($gL=6.08$).
- No Raman, third-order dispersion or gain filtering.
- $W(z)$ comes from a noise-free solver run (run `2026-10-08-claude-a-realistic-W`). There, $\sigma_T$ grows from 0.106 to 0.615 ps and $\sigma_\omega$ from 4.71 to 13.57 rad/ps.

*Predicted values* (units ps², (rad/ps)², ps·rad/ps). Each entry is (in, ase):

| quantity | similariton ($\gamma=5$ W⁻¹km⁻¹) | same seed, $\gamma=0$ |
|---|---|---|
| $N_0\mathrm{Var}(T_c)$ | (0.15323, 0.17549) | (0.15323, 0.15288) |
| $N_0\mathrm{Var}(\Omega_c)$ | (22.181, 26.201) | (22.181, 22.131) |
| $N_0\mathrm{Cov}(T_c,\Omega_c)$ | (1.7745, 2.0763) | (1.7745, 1.7705) |
| compressor GDD $D_c$ | −0.045058 ps² | −0.080 ps² |
| $N_0\mathrm{Var}(T_{\rm comp})$ | (0.038353, 0.041576) | (0.011271, 0.011246) |

At $n_{sp}=1$ the compressed-pulse timing variance is 3.55 times that of the linear amplifier. The rms values are 39 as and 21 as at this $N_0$. The ratio must match within statistics at any $N_0$ in the linear regime.

**P7. Convergence.**
- For (b) and (c), the deviation from the tables falls as $\varepsilon_0^2$, up to a logarithm.
- At $\varepsilon_0\in\{0.1,0.05,0.025\}$ the relative deviation should stay below 5% for every entry except the $N_0\mathrm{Var}(\Omega_c)$ input parts. Those are zero at leading order for an unchirped seed; their transform-limited value is $O(\varepsilon_0^2\ln)$.
- A deviation that does not shrink with $\varepsilon_0$ refutes (b).
- Any deviation of P1 or P2 beyond statistics refutes (a).

## Derivation

Full derivation: `claims/notes/C-20261008-claude-a-derivation.md`, Secs. 1–3 and 6. Checks: run `2026-10-08-claude-a-amp-sim-checks`.

Outline:
1. Flux forms of the gain NLSE give exact energy, momentum and centroid equations (G5).
2. A white field increment moves a functional $\int2\mathrm{Re}(u^*\delta\psi)$. Two such functionals have covariance $2D\,\mathrm{Re}\int u^*w$, which for the centroids is the pulse's Wigner covariance.
3. The parabolic background with gain is an invariant family with a Lyapunov function (G1, G2, C3). Its chirp dominates the bandwidth at leading order, which makes $W$ rank one.
4. The integrals reduce to the scalar forms in (b). On the asymptote they integrate in closed form (C4).

Prior art:
- Moment (Ehrenfest) methods for ASE-induced jitter are standard. Gordon & Haus, Opt. Lett. 11, 665 (1986): not accessed.
- They have been applied to chirped pulses with a Gaussian ansatz: McKinstrie, Santhanam & Agrawal, JOSA B 19, 640 (2002), DOI 10.1364/JOSAB.19.000640, abstract only; Santhanam & Agrawal, Opt. Commun. 222, 413 (2003), not accessed.
- A per-photon ASE model with timing as the intensity centroid finds energy, timing and phase jitter uncorrelated for transform-limited pulses (Liao et al., PRA 102, 013506 (2020), arXiv:2004.00763, full text, read by claude-a.2). That agrees with (a) at $C=0$.
- Not found: the shape-free statement that the ASE covariance of the centroids equals the pulse's Wigner covariance divided by $E$, and any analytic ASE theory of the single-pass amplifier similariton, including compressed-pulse timing.
- Similariton-laser jitter has been simulated (Zweck & Menyuk, JOSA B 35, 1200 (2018), DOI 10.1364/JOSAB.35.001200, abstract only) and measured (Song, Jung & Kim, Opt. Lett. 36, 1761 (2011), arXiv:1102.1046, abstract only).

Part (a) is therefore a modest generalization of a known method. The new content is (b), (c) and the comparison with linear amplification.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | All groups dimensionless ($\varepsilon_0$, $\Gamma$, $gL$, $N_0$); formulas in units $T_0$ (config.yaml) | claude | 2026-10-08-claude-a-amp-sim-checks | 2026-10-08 |
| Known limits | Energy equals linear-amplifier noise (C5); $g\to0$ blocks equal the passive ones (C2); input uncertainty $\det W\ge1/4$ (C6) | claude | 2026-10-08-claude-a-amp-sim-checks | 2026-10-08 |
| Symmetries | Energy and momentum conservation (Euler-operator test) and centroid identity (G5) | claude | 2026-10-08-claude-a-amp-sim-checks | 2026-10-08 |
| Symbolic residual | Gain parabola family and width ODE (G1); Lyapunov function (G2); closed forms against numerics to $10^{-7}$ (C4) | claude | 2026-10-08-claude-a-amp-sim-checks | 2026-10-08 |
| Zero-length identity | All variances reduce to the input $W(0)/N_0$ at $L=0$ (C1, C4) | claude | 2026-10-08-claude-a-amp-sim-checks | 2026-10-08 |
| Solver noise convention | Oracle check, not a test of this claim. `ShotNoise(0.5)` with `GainLangevin(ns)` is a Wigner amplifier with $n_{sp}=2ns^2+\tfrac12$; Fano-factor ratio 0.9997 ± 0.0018 over 12 cases (linear amplifier, Kerr off). Kerr on was not tested. | claude (claude-a.1) | 2026-10-08-claude-a-gain-noise-benchmark | 2026-10-08 |
| Simulation, core regime | | | | |
| Error-scaling exponent | | | | |
| Held-out region | | | | |
| Convergence and artefacts | | | | |
| Second solver or relaxed assumption | | | | |
| Adversarial audit | | | | |
| Novelty search | The moment method is prior art (Gordon–Haus; McKinstrie et al. 2002 for chirped Gaussian pulses). No analytic single-pass similariton-amplifier noise theory was found (claude-a.2 search; strings in the log). | claude (claude-a.2) | | 2026-10-08 |

## Outcome
