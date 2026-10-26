---
agent: /root
model: unknown
family: gpt
date: 2026-10-04
revised_by: gpt-b
revised_model: gpt-6-astra
revised_family: gpt
revised: 2026-10-04
---

# Multimode squeezing problems: shared definitions

The PI chose four problems on 2026-10-04. This page holds the definitions they share. The rules for evidence, audits and promotion are in AGENTS.md and `docs/PROMOTION.md` and are not repeated here.

| Card | Problem |
|---|---|
| [P-20261004-root-01](../problems/P-20261004-root-01-normal-dispersion-multimode-squeezing.md) | Minimum noise under spectral filtering in normal dispersion |
| [P-20261004-root-03](../problems/P-20261004-root-03-anomalous-dispersion-multimode-squeezing.md) | Minimum noise for a multimode soliton launch in anomalous dispersion |
| [P-20261004-claude-interactive-01](../problems/P-20261004-claude-interactive-01-weak-admixture-soliton-noise.md) | Noise of an LP01 soliton with a weak LP02 or LP11 admixture (subcase of root-03) |
| [P-20261004-claude-interactive-02](../problems/P-20261004-claude-interactive-02-multimode-soliton-collective-noise.md) | Vacuum-, gain- and Raman-driven noise of a multimode soliton's energy, phase, timing and frequency |

Two of the original cards are parked, each with its reactivation question:
- [P-20261004-root-02](../problems/P-20261004-root-02-near-zero-dispersion-multimode-squeezing.md): near-zero dispersion.
- [P-20261004-root-04](../problems/P-20261004-root-04-squeezing-structure-and-readout.md): readout theory.

## Fields and readouts

Use photon-normalized fields $b_a(\omega)$, where $a=(m,\sigma)$ labels spatial mode and polarization. Fluctuation kernels are $G_{ab}(\omega,\omega')=\langle\delta b_a^\dagger(\omega)\delta b_b(\omega')\rangle$ and $H_{ab}(\omega,\omega')=\langle\delta b_a(\omega)\delta b_b(\omega')\rangle$.

For a readout $D$, predict the selected mean photon number $n_D$, the optical power $P_D$ (computed with the actual photon energies), and the count Fano factor $F_D=\operatorname{Var}(\hat n_D)/\langle\hat n_D\rangle$. Every readout includes the vacuum entering each rejected or combined port.

- **Bandpass.** Transmission $T(\omega)$ between 0 and 1. All spatial modes are collected unless the count is mode-resolved.
- **Coherent reference.** Interference with a coherent copy of the input, $C=\sqrt\eta A_{\rm fiber}+\sqrt{1-\eta}\,re^{i\psi}A_{\rm input}$, giving $F=1-\eta+\eta\,v_\theta^TQv_\theta$. The reference power counts toward the source budget.

These are different observables, and none of them stands in for another:
- quadrature variance;
- Stokes (polarization) variance;
- count Fano factor;
- a covariance eigenvalue.

The minimum and maximum of a Fano-against-power curve are not conjugate quadratures of one state.

## Dimensionless groups

| Group | Meaning |
|---|---|
| $\zeta=L/L_D$, $L_D=T_0^2/|\beta_2|$ | Length in dispersion lengths |
| $N^2=L_D/L_{NL}=\gamma_{\rm eff}P_{\rm pk}T_0^2/|\beta_2|$ | Soliton number, or its normal-dispersion analogue |
| $C=\mathrm{GDD}/T_0^2$ | Input chirp |
| $\delta_m=\Delta\beta_{1,m}T_0/|\beta_2|$ | Modal walk-off in soliton units (anomalous dispersion) |
| $w_m=\Delta\beta_{1,m}L/T_0$ | Modal walk-off over the fiber (normal dispersion) |
| $p_m$, $M_{\rm occ}=1/\sum_mp_m^2$ | Modal fractions and occupied-mode participation |
| $\Omega_eT_0$ | Filter edge relative to the input bandwidth |
| $f_R$, $\hbar\Omega/k_BT$ | Raman fraction; thermal against zero-point phonon occupation |

Each claim states bounds on the groups it needs.

## Nonlinear overlaps in an ideal parabolic profile

These ratios were computed by claude-interactive on 2026-10-04 from exact Laguerre–Gauss and Hermite–Gauss integrals, normalized to $S_{01,01}=1$. They hold for an infinite parabolic profile; compute the real GIF625 values from its measured index profile.

| Overlap | Value |
|---|---|
| $S_{01,02}$, $S_{01,11}$ (cross) | 1/2 |
| $S_{02,02}$ (self) | 1/2 |
| $S_{11a,11a}$ (self) | 3/4 |
| $S_{11a,11b}$ (phase-matched within the LP11 group) | 1/4 |
| $S_{01,03}$ (cross) | 3/8 |
| 01+03 ↔ 02+02 mixing (phase-matched by equal spacing) | 1/4 |
| 02+02 ↔ 21+21 mixing (LP21 is degenerate with LP02; added by claude-b, 2026-10-04) | 1/4 |
| 01+02 ↔ 11+11 mixing (phase-matched by equal spacing; added by claude-b, 2026-10-04) | 0 |

claude-b re-derived every row by exact symbolic integration on 2026-10-04; the script is in `log/2026-10-04_claude-b_T-20261004-root-02.md`.

With the factor 2 for cross-phase modulation between distinct modes, the coefficient matrix for an LP01/LP02 pair is $C=\begin{pmatrix}1&1\\1&1/2\end{pmatrix}$. For a 70/30 launch, $\sum C_{mn}p_mp_n=0.955$, which matches the archive's effective drive of $0.955P$. A weak LP02 or LP11 admixture sees exactly LP01's self-phase potential ($\sigma=1$); see P-20261004-claude-interactive-01. That is the Manakov condition $C_{21}=C_{11}$, so to first order in the admixture amplitude the problem is the linearized Manakov system. The GRIN matrix differs from the Manakov matrix only in $C_{22}$ (1/2 for LP02, 3/4 for LP11).

### Qualifications from the independent GPT review

The ideal overlap ratios were independently reproduced in [2026-10-04-gpt-b-overlap-capture](../runs/2026-10-04-gpt-b-overlap-capture/summary.json), with the basis and integration in the [review](review-2026-10-04-gpt-b-soliton-noise.md). This does not validate measured-fiber overlaps.

$\gamma_{\rm eff}=\gamma p^TCp$ is an averaged launch parameter. A common-sech stationary solution with equal modal GVD requires $(Cp)_m$ equal on occupied modes. The displayed LP01/LP02 matrix fails that condition at finite LP02 fraction. Define the actual bound family or label the launch an evolving near-soliton. A single participation number cannot replace the overlap matrix and modal delays.

The simple weak-probe capture expression additionally assumes equal GVD, no Raman, an undepleted pump and no resonant anomalous coupling. It is a spectral bound-state projection, not a finite time gate. With a prescribed pump the minority undergoes passive linear evolution and remains coherent, including after passive filtering with vacuum ports. Nonzero quantum corrections require the coupled fluctuation problem.

## Noise sources

Keep these separate, with their own covariances:
- input vacuum;
- Raman, as a causal response with its matching thermal and zero-point reservoir;
- spontaneous emission from gain;
- guided acoustic-wave Brillouin scattering (Shelby et al., DOI 10.1103/PhysRevB.31.5244) in the detection RF band;
- classical input noise and mode or phase disorder;
- detection loss.

Do not tune any of them with a free multiplier.

## Archive

Background calculations are in `~/Desktop/fall2026_research/ai driven lab work`, outside this repository:
- `research_runs/2026-09-26_analytics/report.md`: near-soliton analytics, coherent-reference designs and failed extensions;
- `research_runs/2026-09-28_theory_campaign/REPORT.md`: normal-dispersion reductions, length forecasts, wavelength table;
- `research_runs/2026-09-29_joint_fit/REPORT.md`: experimental joint power and noise fit.

These are provenance pointers, not repository results. Numbers quoted from them in the cards are not registered runs until T-20261004-root-03 registers them.

## Plotting convention

For power sweeps, plot output optical power in blue on the left axis and noise in dB in red on the right axis, with analytical predictions overlaid.
