---
id: P-20261004-claude-interactive-02
title: "Vacuum-, gain- and Raman-driven noise of a multimode soliton's energy, phase, timing and frequency"
status: candidate
priority: 2
literature_state: partial
novelty_confidence: low
target_quantity: "Corrections to known scalar and Manakov collective-coordinate covariance (energy, phase, timing and centre frequency, and modal fractions and relative modal phases) of a verified bound multimode soliton in unequal-overlap spatial modes with finite walk-off, driven separately by calibrated input-vacuum, gain/spontaneous-emission and Raman reservoirs; in particular the channels with no single-mode or Manakov counterpart: whether a modal-partition timing term survives frequency compensation, and Raman- or acoustic-driven exchange of photons between modes."
model: "Multimode GNLSE in anomalous dispersion with Kerr overlap tensor, modal group-velocity differences, distributed gain with spontaneous-emission noise, causal Raman response with thermal and zero-point reservoir; soliton perturbation theory for the collective coordinates."
oracle_ready: partial
last_audited: 2026-10-04
audited_by: [claude, gpt]
proposed_by: PI
provenance:
  agent: claude-interactive
  model: claude-opus-5-5
  family: claude
updated_by: claude-b
updated_model: claude-opus-5-5
updated_family: claude
claims: []
results: []
---

## Target quantity

**PI direction (2026-10-08).** Priority is an analytical formula for the Raman- and gain-induced contributions to the covariance of energy, phase, timing and frequency, and of the modal fractions and relative modal phases, for a bound multimode soliton in GRIN fibre, with step-index fibre in scope too. Vector and Manakov soliton results are baselines only: they may stand in for the GRIN or step-index case only where a quantitative comparison shows the difference is small, and that comparison must be stated.

**Coordinates.** For a coherently launched multimode soliton (P-20261004-root-03), the collective coordinates are energy $E$, phase $\theta$, timing $T$ and centre frequency $\Omega$. A multimode soliton adds modal fractions $p_m$ and relative modal phases $\phi_m$. Only phase combinations protected by the actual coupling symmetries are neutral. Modal fractions are not automatically neutral shape coordinates; the family and its linearized spectrum must be established first.

**Derive beyond the published scalar and Manakov baselines** the covariance growth $\langle\delta X_i\delta X_j\rangle(z)$ for these coordinates, separately for three sources:
1. **input vacuum**: the multimode counterpart of Haus–Lai. The two-component Manakov case without walk-off is already solved (Rand, Steiglitz & Prucnal 2005, below). What remains is the GRIN case: unequal overlaps $C$, walk-off, and more than two modes.
2. **distributed gain with spontaneous emission**: the counterpart of Gordon–Haus, set by gain $g$ and inversion factor $n_{sp}$. For a two-component Manakov soliton driven by additive white noise, without walk-off, the variances of all parameters are known (Derevyanko, Prilepsky & Yakushev 2006; Doktorov & Kuten 2001, below).
3. **Raman**: the deterministic self-frequency shift together with thermal and zero-point phonon noise.

An answer gives each coefficient in closed form with its power of $z$. It must show explicit dependence on the overlap matrix $C$, the modal group delays $\Delta\beta_{1,m}$, the soliton energy and $T_0$.

**Channels with no single-mode counterpart:**
- **Modal-partition timing jitter.** This is the multimode form of birefringence-mediated timing jitter (Mollenauer & Gordon 1994; Baker & Elgin 1998; below). Fluctuations of the modal fractions shift the bound soliton's group velocity through $\sum_m\Delta\beta_{1,m}\delta p_m$. Fiber modes have large, deterministic group delays, with $\delta_m=\Delta\beta_{1,m}T_0/|\beta_2|\sim1$; residual birefringence in single-mode fiber has small, random ones.
- **Raman- and acoustic-driven intermodal exchange.** Thermal phonons are local in the fiber cross-section, so spontaneous Raman scattering and GAWBS can move photons between spatial modes. That makes the fractions random-walk even in passive fiber, which would add $z^3$ timing jitter through the partition channel. claude-b proposed this channel during the review.
  - GAWBS-mediated coupling between LP modes has been measured and modelled for linear signals in few-mode fiber (Yoshida et al. 2025, below).
  - Its effect on soliton collective coordinates, and any Raman counterpart, was not found.

**Caveat from the GPT review** (gpt-b, 2026-10-04), kept as written:

A specific channel to test (an unverified hypothesis with a polarization precedent). Suppose a bound multimode soliton moves at the power-weighted bare modal group velocity. Then fluctuations of the modal fractions shift its group velocity by $\sum_m\Delta\beta_{1,m}\delta p_m$. This would be a *modal-partition* timing jitter:
- growing as $z^2$ when the fraction fluctuations are frozen in at launch;
- growing as $z^3$ when gain noise drives the fractions as a random walk.

The velocity assumption can fail: bound components acquire frequency offsets that compensate bare walk-off, and the centroid of pulse plus radiation differs from the bound-pulse timing. Mollenauer–Gordon already identify polarization-noise conversion through birefringence as timing jitter (10.1364/OL.19.000375; **abstract only**). A new spatial-mode coefficient must survive comparison with that mechanism and be projected from the actual bound family. No independent additive partition contribution is established.

Its putative ratio to Gordon–Haus jitter involves the same walk-off parameter $\delta_m=\Delta\beta_{1,m}T_0/|\beta_2|$ as P-20261004-claude-interactive-01.

## Reductions found in the review

claude-b recorded these on 2026-10-04.

**Self-check of reduction 1 (same family, not the solver).** Run `2026-10-04-claude-b-centroid-selfcheck` uses independent numpy code with $d=0.8$, $p_b=0.2$ and the GRIN overlap matrix. It finds:
- $T_c(z)$ is linear to $10^{-13}$;
- the launch-noise variance of $(T_c(z)-T_c(0))/z$ equals that of the initial velocity at every $z$;
- the partition and momentum parts equal $d^2p_ap_b/N$ and $1/(3N)$ exactly, with ratio $3d^2p_ap_b$.

An independent check by another family is still needed.

1. **Centroid theorem.** Take the cross-phase-only multimode model with walk-off and equal $\beta_2$. It conserves the photon number $N_m$ in each mode and the total momentum $J$ (Sun et al. 2024, Eqs. 54–56). The equation for the energy-weighted centroid $T_c=\sum_m\int t|A_m|^2dt/N$ then closes exactly:

   $$\frac{dT_c}{dz}=\frac{1}{N}\Big(\sum_m\Delta\beta_{1,m}N_m+\beta_2 J\Big)=\text{const}.$$

   Here $J$ is in the frequency convention, up to the sign set by the Fourier convention. With a coherent launch and the composite bound, two parts of the timing variance grow as $z^2$:
   - modal partition: $z^2\Delta\beta_1^2p_1p_2/N$ for two modes;
   - the Haus–Lai frequency term: $z^2\beta_2^2/(3NT_0^2)$.

   Their ratio is $3\delta^2p_1p_2$. For example, $\delta=1$ and $p_2=0.2$ give 0.48.

   The centroid includes any radiation the launch sheds. It equals the bound pulse's timing only when all components stay captured; for partial capture, the timing of the bound pulse must come from the bound family and its dual modes. gpt-b's review (T-20261004-claude-interactive-01) makes the same caution.

   With distributed gain, $N_m$ and $J$ random-walk, giving $z^3$ terms whose ratio has the same structure. So the passive and gain-driven partition jitter of item "modal-partition timing jitter" follows from two conservation laws. It is unlikely to be a substantial result by itself. Its value is as a check and as a baseline for Raman, intermodal exchange and $C$-dependent corrections.
2. **Fractions are frozen without exchange.** In the same model each $N_m$ is exactly conserved. Fraction noise therefore stays at its launch value, consistent with the $z$-independent polarization-angle variance $1/(4A_0)$ that Rand et al. find for the Manakov soliton. Fraction noise can grow only through gain, Raman, GAWBS, phase-matched four-wave mixing, or linear mode coupling.

## Signal of hidden simplicity

- **Single-mode limits exist.** Each noise source has a known single-mode collective-coordinate theory, listed below. Corney & Drummond give all three in one framework. In their normalization, the bright-soliton timing variance is
  $$\langle\Delta\tau^2\rangle=\frac{\pi^2}{24n}+\frac{\pi^2\alpha_G}{12n}\zeta+\frac{A^3}{6n}\zeta^2+\Big[\frac{\alpha_GA^3}{9n}+\frac{2A^4I(t_0)}{3n}\Big]\zeta^3,$$
  with $N=2n$ photons. The terms are vacuum ($\zeta^2$), gain ($\zeta^3$) and Raman ($\zeta^3$). The ratio of Raman to Gordon–Haus jitter is about $8F(0)/(5Gx_0)$.
- **The multimode soliton family adds only a few coordinates**, and the fractions among them are frozen without exchange processes. The reduced description is therefore low-dimensional.
- **A multimode soliton carries more energy.** At fixed $T_0$, its energy scales as $1/\gamma_{\rm eff}$. Per-photon noise sources such as Gordon–Haus would then be reduced by the factor $\gamma_{\rm eff}/\gamma$, unless a channel with no single-mode counterpart takes over. Deciding which wins is the point of this problem.
- **Energy alone is insufficient.** The average $\gamma_{\rm eff}$ does not construct a finite-fraction vector soliton or specify how reservoir noise projects onto it. A scalar rescaling is a baseline to test after solving the mean family, not an established multimode benefit. (GPT review)
- **The weak-admixture limit** (P-20261004-claude-interactive-01) is the Manakov linearization at first order. It supplies a concrete multimode soliton family on which to compute the coefficients first. (GPT review) Its bound eigenfunction is a useful leading-order seed. It does not establish a nonlinear finite-fraction soliton family or its adjoint modes.

## Literature state

Reviewed by claude-b on 2026-10-04 (T-20261004-root-02).

**Single-mode collective coordinates:**
- Haus & Lai, JOSA B 7, 386 (1990), DOI [10.1364/JOSAB.7.000386](https://doi.org/10.1364/JOSAB.7.000386): uncertainties in soliton number, phase, position and momentum. **Abstract only.**
- Gordon & Haus, "Random walk of coherently amplified solitons in optical fiber transmission," OL 11, 665 (1986), DOI [10.1364/OL.11.000665](https://doi.org/10.1364/OL.11.000665): amplifier noise drives a random walk of group velocity. **Abstract only** (OpenAlex record). The publisher page returned a CAPTCHA, which was not bypassed. The $\zeta^3$ formula above is from Corney & Drummond's full text.
- Gordon, "Theory of the soliton self-frequency shift," OL 11, 662 (1986), DOI [10.1364/OL.11.000662](https://doi.org/10.1364/OL.11.000662). **Abstract only.**
- Corney & Drummond, "Quantum noise in optical fibers II: Raman jitter in soliton communications," JOSA B 18, 153 (2001), [arXiv:quant-ph/9912096](https://arxiv.org/abs/quant-ph/9912096). **Full text.**
  - Model: single mode, single polarization, truncated Wigner. Analytic results use an instantaneous Raman approximation; numerics use a multi-Lorentzian Raman response with a GAWBS Lorentzian.
  - Results: the timing variance above; Raman jitter exceeds Gordon–Haus jitter for soliton periods below about 1.5 km in their example; dark solitons have half the vacuum and gain terms and a quarter of the Raman term.
  - It cites Moores, Wong & Haus (Opt. Commun. 113, 153 (1994)) for the combined Gordon–Haus and self-frequency-shift term growing as $z^5$; that paper was **not accessed**.
- Drummond & Corney, "Quantum noise in optical fibers I," JOSA B 18, 139 (2001), DOI [10.1364/JOSAB.18.000139](https://doi.org/10.1364/JOSAB.18.000139): Hamiltonian and stochastic equations with Raman reservoirs. **Abstract only.**
- Kärtner & Boivin, PRA 53, 454 (1996), DOI [10.1103/PhysRevA.53.454](https://doi.org/10.1103/PhysRevA.53.454). **Abstract only.**
- Shelby, Levenson & Bayer, "Guided acoustic-wave Brillouin scattering," PRB 31, 5244 (1985), DOI [10.1103/PhysRevB.31.5244](https://doi.org/10.1103/PhysRevB.31.5244): thermal acoustic modes scatter light from about 20 MHz upward, a phase-noise source outside the Raman model. **Abstract only.**

**Two-component and polarization analogues:**
- Rand, Steiglitz & Prucnal, "Quantum theory of Manakov solitons," PRA 71, 053805 (2005), DOI [10.1103/PhysRevA.71.053805](https://doi.org/10.1103/PhysRevA.71.053805). **Full text** (author copy). It covers the **vacuum-driven part of item 1 for two Manakov components without walk-off**:
  - six coordinates (amplitude, position, momentum, polarization angle, two phases);
  - the polarization-angle variance $1/(4A_0)$ is independent of $z$; the phase and position variances grow as $z^2$;
  - no gain or Raman, and the continuum is neglected.
- Derevyanko, Prilepsky & Yakushev, "Statistics of a noise-driven Manakov soliton," J. Phys. A 39, 1297 (2006), DOI [10.1088/0305-4470/39/6/006](https://doi.org/10.1088/0305-4470/39/6/006), [arXiv:nlin/0509024](https://arxiv.org/abs/nlin/0509024). **Full text, skimmed.** This covers the **gain-driven part of item 2 for two Manakov components without walk-off**.
  - Model: a Manakov soliton with vector additive white Gaussian noise (the ASE model), treated by adiabatic perturbation theory, Langevin equations and Fokker–Planck.
  - Results: variances of amplitude, frequency, timing (terms in $z$ and $z^3$), polarization angle and relative phase.
  - For isotropic noise, a unitary transformation reduces the soliton to the scalar NLS soliton; anisotropic noise makes the jitters depend on the initial polarization and phase.
  - Its timing-jitter formula is credited to Doktorov & Kuten, Nonlinear Phenom. Complex Syst. 4, 1 (2001), **not accessed**.
- Evangelides, Mollenauer, Gordon & Bergano, "Polarization multiplexing with solitons," J. Lightwave Technol. 10, 28 (1992), DOI [10.1109/50.108732](https://doi.org/10.1109/50.108732): ASE-driven spread of soliton polarization states in birefringent fiber with amplifiers. **Abstract only.**
- Mollenauer & Gordon, "Birefringence-mediated timing jitter in soliton transmission," OL 19, 375 (1994), DOI [10.1364/OL.19.000375](https://doi.org/10.1364/OL.19.000375): arrival-time jitter "initiated by noise modulation of the polarization states of the pulses and mediated by the birefringence". This is the polarization form of the modal-partition channel. **Abstract only.**
- Baker & Elgin, "Solitons in randomly varying birefringent fibre," Quantum Semiclass. Opt. 10 (1998), DOI [10.1088/1355-5111/10/1/028](https://doi.org/10.1088/1355-5111/10/1/028): random birefringence perturbs the polarization, hence the velocity, hence the arrival time; analytic perturbation theory. **Abstract only.**
- Baker, Elgin & Harvey, "Soliton jitter in birefringent fibres," Opt. Commun. (1999), DOI [10.1016/S0030-4018(99)00197-2](https://doi.org/10.1016/S0030-4018(99)00197-2). **Not accessed** (no abstract in OpenAlex).
- Bergano & Davidson, "Polarization-scrambling-induced timing jitter in optical-amplifier systems," OFC 1995, DOI [10.1364/OFC.1995.WG3](https://doi.org/10.1364/OFC.1995.WG3): timing jitter from PMD combined with polarization scrambling. **Abstract only.**
- Konyukhov, PRA 111, 013508 (2025), [arXiv:2412.09208](https://arxiv.org/abs/2412.09208): linearized quantum fluctuations of vector solitons with differential group delay. It reports correlations, not collective-coordinate jitter. **Full text, keyword-scanned.**

**Multimode:**
- Sun, Parra-Rivas, Agrawal, Hansson, Antonelli & Mecozzi, Photonics Res. 12, 2581 (2024), DOI [10.1364/PRJ.531393](https://doi.org/10.1364/PRJ.531393): conservation of power per mode, of total momentum and of energy (Eqs. 53–58); a multimode soliton's group velocity is set by its modal composition. No noise. **Full text**, sections 3–4.
- Sloan et al., [arXiv:2509.03482](https://arxiv.org/abs/2509.03482): in a multimode fiber the dominant excess-noise mechanism is SPM and XPM converting input power noise into noise in the relative intermodal phase. This uses classical input noise, not a soliton. **Full text** of the main paper.
- Yoshida et al., "Guided acoustic-wave Brillouin scattering noise in few-mode fiber," Opt. Express 33, 34586 (2025), DOI [10.1364/OE.570713](https://doi.org/10.1364/OE.570713). **Abstract only.**
  - Content: GAWBS couples different LP modes through acoustic modes with axial wavenumber. Intermodal GAWBS phase noise is converted into intensity noise by the modal group-velocity differences. The GAWBS noise coefficient is 3–4 dB above standard single-mode fiber.
  - Scope: linear signals, no solitons.
- Zitelli, Ferraro, Mangini & Wabnitz, "Characterization of multimode soliton self-frequency shift," J. Lightwave Technol. (2022), DOI [10.1109/JLT.2022.3205846](https://doi.org/10.1109/JLT.2022.3205846). **Full text (author postprint), keyword-scanned.**
  - Content: Raman self-frequency-shift theory for GRIN multimode solitons, with 1 km experiments. The measured Raman-delay jitter is Gaussian, with a standard deviation of 0.03–0.28 ns that saturates with energy. The authors attribute it to peak-power fluctuations through the self-frequency shift; their Gordon–Haus estimate is below 0.2 ps.
  - Not covered: modal-partition noise is not considered. This is classical laser noise, a possible test case for reduction 1.
- Renninger & Wise (2013), DOI [10.1038/ncomms2739](https://doi.org/10.1038/ncomms2739): multimode soliton mean field. **Full text, keyword-scanned.**
- Zitelli 2024 review, [arXiv:2404.00991](https://arxiv.org/abs/2404.00991): no jitter or noise analysis of multimode solitons. **Full text, keyword-scanned.**

**Searches** (claude-b, 2026-10-04):
- OpenAlex forward citations of Gordon & Haus 1986 (the first 100 of 891, by title) and of Mollenauer & Gordon 1994 (all 48).
- OpenAlex searches: "birefringence-mediated timing jitter soliton", "multimode soliton timing jitter", "soliton stability and trapping in multimode fibers".
- Keyword scans of the 2024 reviews.
- Helper claude-b.2 searched polarization and multimode soliton jitter, multimode Raman noise and multimode GAWBS; its results are in the review log.

**Independent GPT review** (gpt-b, 2026-10-04), kept as written; it reads several of the same sources with its own access levels:

- Rand, Steiglitz & Prucnal, [10.1103/PhysRevA.71.053805](https://doi.org/10.1103/PhysRevA.71.053805), **full text**: vector input-vacuum coordinate fluctuations already exist, including component phases and population angle.
- Derevyanko, Prilepsky & Yakushev, [arXiv:nlin/0509024](https://arxiv.org/abs/nlin/0509024), DOI [10.1088/0305-4470/39/6/006](https://doi.org/10.1088/0305-4470/39/6/006), **full text**: additive-noise Manakov Langevin equations, a covariance matrix integral and coordinate variances. Isotropic-noise timing reduces to the scalar result; anisotropic noise changes the coefficients.
- Mollenauer & Gordon, [10.1364/OL.19.000375](https://doi.org/10.1364/OL.19.000375), **abstract only**: birefringence converts polarization-state noise into timing jitter. Full-text comparison is T-20261004-gpt-b-01.
- Zitelli et al., [10.1109/JLT.2022.3205846](https://doi.org/10.1109/JLT.2022.3205846), **abstract only** (repository full text returned 403): multimode Raman self-frequency-shift theory and delay jitter. Its noise-source assumptions have not been established here.
- Corney & Drummond, [arXiv:quant-ph/9912096v2](https://arxiv.org/abs/quant-ph/9912096v2), **full text**: calibrated scalar input-vacuum, balanced gain/loss and Raman-reservoir timing/frequency baselines. Raman reservoir jitter is distinct from amplitude noise converted through deterministic Raman shift.
- Haus & Lai, [10.1364/JOSAB.7.000386](https://doi.org/10.1364/JOSAB.7.000386); Gordon & Haus, [10.1364/OL.11.000665](https://doi.org/10.1364/OL.11.000665); Gordon, [10.1364/OL.11.000662](https://doi.org/10.1364/OL.11.000662); Kärtner & Boivin, [10.1103/PhysRevA.53.454](https://doi.org/10.1103/PhysRevA.53.454): **abstract only** for each original. Use accessible primary derivations and independent dual projections for precise coefficients.

## Sharpest statement of the gap

**Known:**
- single-mode vacuum, Gordon–Haus and Raman collective-coordinate noise (Haus–Lai; Gordon–Haus; Corney–Drummond);
- vacuum-driven noise of a two-component Manakov soliton without walk-off (Rand et al. 2005);
- ASE-driven noise of a two-component Manakov soliton without walk-off (Derevyanko et al. 2006; Doktorov & Kuten 2001);
- the mechanism of partition-mediated timing jitter, in its polarization form for randomly birefringent fiber (Mollenauer & Gordon; Baker & Elgin);
- intermodal GAWBS for linear signals in few-mode fiber (Yoshida et al. 2025).

**Reducible:** the passive and gain-driven modal-partition jitter of a bound multimode soliton follows from the conservation laws of the cross-phase-only model (reduction 1).

**Not found:**
- collective-coordinate noise of a GRIN multimode soliton with unequal overlaps and deterministic walk-off $\delta\sim1$;
- multimode Raman noise, meaning thermal and zero-point phonon noise with its intermodal structure, including Raman-driven exchange of photons between modes;
- the effect of intermodal GAWBS on a soliton's modal fractions, relative phases and timing.

The distinctive and possibly non-trivial part is the last two items and their competition with Gordon–Haus and single-mode Raman jitter under GRIN parameters. Partition jitter by itself is not.

**Related cards.** P-011 uses the same machinery for a different soliton family (higher-order dispersion). P-002 supplies the mean multimode soliton for launches that are not weak. T-20261004-claude-interactive-09 (modal-partition timing jitter) should start from reduction 1 and Mollenauer & Gordon 1994.

**GPT review's statement** (gpt-b, 2026-10-04):

A general vector Haus–Lai or Gordon–Haus theory is not missing. Population/polarization noise converted through group-delay differences also has prior precedent. The searched sources did not resolve the source-separated covariance for a physically verified unequal-overlap GRIN spatial-mode bound pulse, including frequency compensation, Raman coupling and bound/continuum separation. Whether this yields a distinct low-dimensional partition-jitter correction remains open with low novelty confidence. Multimode Raman delay theory already exists; its quantum-reservoir content needs full-text comparison.

First solve the stable mean family and identify its dual modes. Require a bounded small-noise regime, stated $p_m$, $\delta_m$, GVD ratios, nonlinear overlap differences, Raman timescale relative to $T_0$, and gain/loss assumptions. A constant-coefficient cubic law requires approximately stationary soliton parameters; pure uncompensated gain is not the stationary Gordon–Haus benchmark. Relative phases near an empty component require separate treatment.

Related cards: P-011 studies a different mean family with higher-order dispersion; P-002 supplies finite-fraction mean-field dynamics. Task -08 is scalar baseline work, not authorization to begin the blocked multimode derivation -09.

Note added when the two reviews were merged (claude-interactive, 2026-10-06): with T-20261004-root-02 merged, the Claude-family review is also complete and `audited_by` is `[claude, gpt]`. Status, and whether derivation may begin, were not changed here.

## Conjectures

None registered.

## Oracle

For high mode counts, the solver's CP backend implements the parallel-factor decomposition of the overlap tensor in Rivera, [arXiv:2609.16502](https://arxiv.org/abs/2609.16502) (full text, keyword-scanned). It reports over 1,000 modes on current hardware, including multimode solitons in GRIN fiber. Its noise example is classical: 0.1% pulse-energy noise, about 60 dB above vacuum, in the fission of a 20-mode soliton. It reports no quantum-noise result. Stochastic and linearized-noise propagation are in `solver/`. Two capabilities must be confirmed or added under `docs/SOLVER.md`:
- distributed gain with spontaneous-emission noise;
- a multimode Raman reservoir with the correct intermodal correlations.

From the GPT review: The pinned solver supplies deterministic and stochastic propagation. Confirm reservoir normalization and the four dual projections in T-20261004-claude-interactive-08. Distributed gain with matching spontaneous-emission noise must be checked or proposed under `docs/SOLVER.md`. No multimode oracle result is asserted by the GPT review.

Cheap tests:
- The single-mode limit reproduces Haus–Lai, Gordon–Haus scaling and Corney–Drummond Raman jitter.
- With gain off and Raman off, the photon number in each mode is conserved, and the centroid velocity is exactly constant (reduction 1).
- In a two-mode run at $\delta=1$, $p_2=0.2$, the passive centroid jitter matches $z^2[\Delta\beta_1^2p_1p_2+\beta_2^2/(3T_0^2)]/N$.
- The covariance growth exponents in $z$ are measured and compared with the predicted powers.

## Lab test

**Passive case.** GIF625 at 1550 nm.
- Measure timing jitter (balanced optical cross-correlation or RF phase noise), centre-frequency noise (spectral-edge detection) and energy noise, for LP01 and for a launch with a controlled LP02/LP11 fraction, at several lengths.
- Relative modal phase noise can be measured by interfering mode-sorted outputs.
- Reduction 1 predicts how the passive partition jitter scales with $\delta$ and $p_2$. A larger measured jitter would point to exchange processes (Raman, GAWBS, mode coupling).

**Gain case.** The gain medium must work in anomalous dispersion, for example a multimode Er-doped GRIN fiber near 1550 nm. Yb at 1030 nm is in normal dispersion in silica, so it cannot support these solitons.

## Risks and must-reads

- **Full texts not read.** Mollenauer & Gordon 1994 and Baker & Elgin 1998/1999 may already contain the partition formula in a form that carries over directly (T-20261004-claude-b-02).
- **Triviality.** Away from the exchange processes, the answer reduces to the scalar result with $\gamma_{\rm eff}$ plus reduction 1, so the problem's interest rests on Raman and acoustic intermodal exchange. Those need a multimode reservoir model that the solver may not have.
- **Competing noise in real fiber.** Random mode coupling and GAWBS can dominate relative-phase noise.
- (GPT review) A scalar/Manakov reduction or frequency-compensation cancellation may remove the proposed new term. Establish this before treating partition jitter as a distinct contribution.
- (GPT review) Corney–Drummond has now been read in full. Missing originals and the close Mollenauer–Gordon/Zitelli comparisons are tracked in T-20261004-gpt-b-01.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-04 | claude-interactive (claude; claude-opus-5-5) | Created as candidate on PI instruction | PI's four-problem set in chat, 2026-10-04; targeted literature search |
| 2026-10-04 | claude-b (claude; claude-opus-5-5) | Claude-family full-text review (T-20261004-root-02). Vacuum part narrowed: two-component Manakov case is in Rand et al. 2005. Modal-partition jitter recognized as the multimode form of birefringence-mediated jitter (Mollenauer & Gordon 1994) and as following from conservation laws (reduction 1). Target refocused on Raman/acoustic intermodal exchange and on GRIN-specific coefficients. Status, priority, literature_state (partial) and novelty_confidence (low) unchanged | Full texts: Corney & Drummond; Rand et al. 2005; Derevyanko et al. 2006 (skimmed); Sun et al. 2024; Sloan et al.; Zitelli et al. 2022 (scanned). Abstracts: Gordon & Haus; Mollenauer & Gordon; Baker & Elgin; Yoshida et al. 2025. Log `log/2026-10-04_claude-b_T-20261004-root-02.md` |
| 2026-10-04 | gpt-b (gpt; gpt-6-astra) | Completed independent GPT scope review; retained candidate and narrowed beyond published vector covariance and polarization jitter | Full-text Rand, Derevyanko and Corney; Mollenauer–Gordon and Zitelli abstracts; docs/review-2026-10-04-gpt-b-soliton-noise.md. Added only gpt to audited_by; task -09 remains blocked |
| 2026-10-04 | gpt-b (gpt; gpt-6-astra) | Reproduced scalar dual-coordinate vacuum, balanced gain/loss and explicit-Wigner Raman baselines; retained default Raman normalization failure and assigned independent audit T-20261004-gpt-b-02. No multimode claim or status promotion. | Runs `2026-10-04-gpt-b-soliton-baselines`, `2026-10-04-gpt-b-noise-pathwise`; [exploration](../explorations/2026-10-04-gpt-b-soliton-noise-baselines.md); Corney–Drummond arXiv:quant-ph/9912096 (full text), Drummond–Corney arXiv:quant-ph/9912095 (full text, sections III and VI) |
| 2026-10-08 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Recorded the PI's direction: Raman- and gain-driven covariance first; Manakov/vector results not equivalent to GRIN or step-index without a quantitative comparison. No other change | PI direction in chat, 2026-10-08 |
