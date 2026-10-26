---
id: P-20261004-root-03
title: "Minimum noise for a multimode soliton launch in anomalous dispersion"
status: candidate
priority: 2
literature_state: partial
novelty_confidence: low
target_quantity: "The deviation of the minimum Fano factor, for a fixed spectral bandpass and for a matched coherent-reference readout, of a coherent multimode soliton launch in anomalous-dispersion GRIN fiber from the LP01 soliton value at the same normalized length, caused by unequal Kerr overlaps (departure from the Manakov limit), modal walk-off and intermodal Raman terms, as a function of normalized length, modal fractions and walk-off."
model: "Multimode GNLSE in anomalous dispersion with Kerr overlap tensor, modal group-velocity differences, causal Raman response and matching reservoir; linearized quantum fluctuations about a multimode soliton; soliton perturbation theory where it applies."
oracle_ready: partial
last_audited: 2026-10-04
audited_by: [claude, gpt]
proposed_by: /root
provenance:
  agent: /root
  model: unknown
  family: gpt
updated_by: claude-b
updated_model: claude-opus-5-5
updated_family: claude
claims: []
results: []
---

## Target quantity

**Launch.** A coherent superposition of LP01 with one or more higher modes (LP02, LP11) sharing a sech envelope of width $T_0$, at the nominal launch energy $E=2|\beta_2|/(\gamma_{\rm eff}T_0)$, where $\gamma_{\rm eff}=\gamma\sum_{mn}C_{mn}p_mp_n$. Here $p_m$ are the modal fractions and $C$ the cross-phase matrix given in the [shared scope](../docs/multimode-squeezing-scope.md).

**Mean-field qualification.** For the ideal parabolic profile no co-propagating equal-width sech pair is an exact solution (equal widths would need $C_{11}p_1+C_{12}p_2=C_{21}p_1+C_{22}p_2$, which forces $p_2=0$ for $C=\begin{pmatrix}1&1\\1&1/2\end{pmatrix}$), so this launch breathes. This averaged energy does not make arbitrary fractions an exact common-sech vector soliton. In the equal-GVD XPM model that requires $(Cp)_m$ equal for every occupied mode. For LP01/LP02, these values are $1$ and $1-p_{02}/2$, which differ at finite admixture. Either construct a stationary bound family with its actual component profiles and frequency shifts, or explicitly call the object an evolving near-soliton launch and include radiation. The [independent review](../docs/review-2026-10-04-gpt-b-soliton-noise.md) gives the substitution test.

**Readouts.**
- (a) Direct detection after a fixed bandpass: the classic soliton spectral-filtering measurement. All modes are collected unless the count is mode-resolved.
- (b) Interference with a coherent copy of the input: $F=1-\eta+\eta\,v_\theta^TQv_\theta$, with the reference-port vacuum included.

**Find:**
1. $F_{\min}$ for each readout against $\zeta=L/L_D$, $p_m$ and the walk-off parameter $\delta_m=\Delta\beta_{1,m}T_0/|\beta_2|$, as a difference from the LP01 soliton at the same $\zeta$.
2. Which departure from the Manakov limit (see "Known sublimits" below) produces that difference:
   - unequal Kerr overlaps: $C_{22}=1/2$ for LP02 and $3/4$ for LP11, against $C_{11}=C_{12}=1$;
   - walk-off, which is equivalent to a launch frequency offset;
   - Raman cross terms between modes;
   - phase-matched four-wave mixing within degenerate mode groups.
   Noise in the relative modal phases is how these show up in mode-resolved readouts.
3. The scaling of $F_{\min}$ with occupied-mode participation $M_{\rm occ}$ at fixed $\zeta$ and readout. In the Manakov limit at $\delta=0$ this scaling is null, so any dependence measures the departure from that limit. $M_{\rm occ}$ alone does not specify overlaps or walk-off, so any participation scaling must be conditional on a stated family of overlap tensors and delay vectors.
4. **PI direction (2026-10-08): the Manakov–GRIN relation as an inequality.** State an inequality between the spectrally filtered noise of the Manakov soliton (equal, by its unitary symmetry, to the LP01 value for mode-symmetric readouts) and that of the GRIN soliton, with the energy normalization, readout and optimization over the filter made explicit. Then prove or refute it. Alternatively, show or refute directly that the GRIN launch can never beat the LP01-only launch. The pure-Kerr exploration T-20261004-claude-b-06 is evidence to test against: at each launch's best scanned band the GRIN launch never beat LP01 by more than 0.014 dB, while at an equal, non-optimal band it was up to 0.125 dB lower (runs `2026-10-04-claude-b-manakov-deviation-scan`, `2026-10-04-claude-b-manakov-deviation-edge-scan`).

A larger photon number at fixed $T_0$ is **not** a channel for $F$. In the linearized model, $F$ depends on $\zeta$, the pulse shape, $T_0$ (through the Raman response), temperature and the readout, but not on the photon number. It changes the output power and the source budget. Classical noise sources outside the model, such as GAWBS, do grow relative to shot noise with power.

The weak-admixture limit is P-20261004-claude-interactive-01; this card covers finite fractions and more modes.

## Known sublimits and reductions

These follow from the model and the literature below. claude-b wrote them down during the review on 2026-10-04.

**Self-check (same family, not the solver).** Run `2026-10-04-claude-b-reduction-selfcheck` is an independent numpy linearized-noise code. It confirms:
- reduction 1: the Manakov rotation formulas hold to about $10^{-9}$;
- the first-order GRIN equivalence of P-20261004-claude-interactive-01: the relative correction to $\rho$ scales as $\varepsilon^2$;
- reduction 2: walk-off against frequency offset agrees to about $10^{-8}$ in all noise quantities.

The independent check by another family, with the solver, is T-20261004-claude-b-01.

1. **Manakov limit.** Suppose all entries of $C$ are equal and $\delta_m=0$. Then the coupled equations are the multicomponent Manakov system, which is invariant under unitary mixing of the modes. A co-launched sech in all modes is a scalar soliton in a rotated mode basis, with vacuum in the orthogonal combinations. That vacuum evolves passively, as $i\partial_\zeta b+\tfrac12\partial_\tau^2b+|u|^2b=0$, so it stays vacuum. Within linearized theory without Raman this gives the following.
   - For any readout that treats all modes alike (all modes through one bandpass, or a coherent reference that copies the input), $F$ equals the scalar soliton value $F_s$ at the same $\zeta$, whatever the fractions.
   - Mode-resolved counts follow by rotation: $F_m=p_mF_s+1-p_m$, and the count correlation is $\rho_{mn}=\sqrt{p_mp_n}\,(F_s-1)/\sqrt{F_mF_n}$.
   - Optimal homodyne squeezing equals the scalar optimum for every partition. Rand, Steiglitz & Prucnal (2005) show this.

   The ideal parabolic-profile matrix differs from the Manakov matrix only in the minority self-term: $C_{22}=1/2$ (LP02) or $3/4$ (LP11), against 1. The leading non-Manakov term in the Hamiltonian is therefore of relative size about $(1-C_{22})p_2^2$: 0.045 for a 70/30 launch and 0.011 for 85/15. At $\delta=0$, a difference between multimode and LP01 $F_{\min}$ must come from this term, from Raman, or from four-wave mixing. That is the null hypothesis a claim has to beat.
2. **Walk-off is a frequency offset.** Take the cross-phase-only coupled equations with equal $\beta_2$ in all modes. The substitution $A_m\to A_m e^{-i\delta_m\tau+i\delta_m^2\zeta/2}$ removes the walk-off term of mode $m$. Walk-off is then the same as launching mode $m$ with a carrier offset $\delta_m/T_0$ (Sun et al. 2024, Eqs. 40–41; this is the soliton-trapping mechanism). The substitution maps vacuum to vacuum, so it also holds for the linearized quantum problem. A fixed bandpass becomes, for mode $m$, a bandpass shifted by $\delta_m/T_0$. The equivalence is broken by the Raman exchange terms between modes, by $\beta_3$, and by mode-dependent $\beta_2$.
3. **Existence window.** A multimode soliton of non-degenerate modes forms in GRIN fiber only when the walk-off length $T_0/\Delta\beta_1$ is comparable with $L_D$, that is $\delta\lesssim1$. Over hundreds of nonlinear lengths it decays towards an LP01 soliton (Zitelli et al. 2021; Zitelli 2024). For $\delta\gg1$ the components separate, and a readout sees separate pulses.
4. **Total count.** With Raman off, the total photon number in each mode is conserved in the cross-phase-only model (Sun et al. 2024, Eq. 54). Collecting all modes and frequencies therefore gives $F=1$.

## Signal of hidden simplicity

Archive figures (`~/Desktop/fall2026_research/ai driven lab work`). The LP01 baselines in the first bullet are registered runs (T-20261004-claude-interactive-06, PR #9). They reproduce the archive bit for bit with the same code. The other figures are not registered.

- **Single-mode baseline** (`research_runs/2026-09-26_analytics/report.md`). For the LP01 soliton with a coherent reference, a soliton-plus-continuum Green function works well. Its design law is $F_{\rm opt}\simeq1-\eta+\eta[d(\zeta)/4\zeta^2+\kappa_R/4\zeta]$, where $d$ oscillates between about 2 and 5.6 and $\kappa_R$ is about 0.84 or 1.7 depending on the Raman model. Registered runs:
  - In the full scalar model, 20 m of GIF625 at 1550 nm gives $F=0.0323$ with oscillator Raman and $0.0529$ with anisotropic Raman, that is −14.9 and −12.8 dB (run `2026-10-04-claude-b.1-prepared-sech-readout-20m`). The Raman reservoir is 61% and 74% of $F$. These runs build the Raman reservoir from the archive's own Wigner spectrum ($2n_{\rm th}+1$), not from the solver default that T-20261004-claude-interactive-08 found to give $2n_{\rm th}+1/2$. The contraction's overall normalization is not yet independently benchmarked (T-20261004-claude-b-08).
  - The Kerr-only ideal sech matches the analytical Green function to $10^{-11}$ (run `2026-10-04-claude-b.1-ideal-sech-kerr-20m`).
  - A pre-registered fixed-bandpass point (1546.5–1553.5 nm) gives $F=0.370$ and $0.415$ (run `2026-10-04-claude-b.1-bandpass-1546-1553-20m`).
- **Effective drive** (`research_runs/2026-09-28_theory_campaign/REPORT.md`). A 70/30 LP01/LP02 launch has effective drive $0.955P$. This equals $\sum_{mn}C_{mn}p_mp_n$ for the ideal parabolic-profile matrix $C$ in the shared scope.
- **Failure of the simple rescaling** (analytics report). At 1400 nm with an 85/15 launch, mapping $P\to P/\kappa$ predicts the output power but fails for $F$. LP02 walks off 0.118 ps in 1 m, against a 0.239 ps pulse width, and the result is converged in mode number. So noise depends on modal walk-off, not only on $\gamma_{\rm eff}$. With reduction 2, this is a launch whose LP02 part is off in frequency by $\delta/T_0$; only part of it is captured.

The ideal-profile overlap identities are re-derived in [2026-10-04-gpt-b-overlap-capture](../runs/2026-10-04-gpt-b-overlap-capture/summary.json). They identify a tractable weak-probe baseline, with no inference that finite-fraction noise is a scalar rescaling. (gpt-b)

## Literature state

Reviewed by claude-b on 2026-10-04 (T-20261004-root-02). Access levels are as stated.

**Single-mode soliton squeezing (baseline):**
- Haus & Lai, JOSA B 7, 386 (1990), DOI [10.1364/JOSAB.7.000386](https://doi.org/10.1364/JOSAB.7.000386): linearized quantum theory of soliton number, phase, position and momentum. **Abstract only.**
- Kärtner & Boivin, PRA 53, 454 (1996), DOI [10.1103/PhysRevA.53.454](https://doi.org/10.1103/PhysRevA.53.454): noise of the fundamental soliton built from exact eigenstates. **Abstract only.**
- Mecozzi & Kumar, OL 22, 1232 (1997), DOI [10.1364/OL.22.001232](https://doi.org/10.1364/OL.22.001232): linearized theory of spectrally filtered solitons. **Not accessed.**
- Levandovsky, Vasilyev & Kumar, OL 24, 43 (1999), DOI [10.1364/OL.24.000043](https://doi.org/10.1364/OL.24.000043). Single-mode: an analytical amplitude-quadrature correlator with the continuum included, and a numerically optimized filter. A square filter is close to optimal up to three soliton periods. **Abstract only** (OpenAlex record). The publisher page returned a CAPTCHA, which was not bypassed. It cannot contain a multimode answer.
- Werner & Friberg, [arXiv:quant-ph/9904104](https://arxiv.org/abs/quant-ph/9904104): a noise "phase transition" at half the soliton amplitude. With Raman at 300 K and $t_0=1$ ps, the optimal filter edge is 125 GHz at three soliton periods, giving 4.8 dB of filtered photon-number squeezing. **Full text, skimmed.**
- Kärtner, Dougherty, Haus & Ippen, JOSA B 11, 1267 (1994), DOI [10.1364/JOSAB.11.001267](https://doi.org/10.1364/JOSAB.11.001267): a quantized Raman model; Raman noise limits squeezing of sub-picosecond solitons. **Abstract only.** This bears on the Raman-model ambiguity below.
- Haus & Yu, JOSA B 17, 618 (2000), DOI [10.1364/JOSAB.17.000618](https://doi.org/10.1364/JOSAB.17.000618): the continuum's contribution to squeezing oscillates and can help. **Abstract only.**

**Experiments and correlations:**
- Friberg et al., PRL 77, 3775 (1996), DOI [10.1103/PhysRevLett.77.3775](https://doi.org/10.1103/PhysRevLett.77.3775): 2.3 dB measured, 3.7 dB after loss correction. **Abstract only.**
- Spälter et al., PRL 81, 786 (1998), DOI [10.1103/PhysRevLett.81.786](https://doi.org/10.1103/PhysRevLett.81.786): photon-number correlations between spectral components. **Abstract only.**

**Vector and multimode quantum analogues:**
- Lantz, Sylvestre, Maillotte, Treps & Fabre, [arXiv:quant-ph/0311088](https://arxiv.org/abs/quant-ph/0311088) (J. Opt. B 6, S295 (2004)). **Full text.**
  - System: 1+1D spatial solitons in bulk Kerr media. The vector soliton is an unstable two-hump bound state of two circular polarizations in CS₂, with a cross/self ratio of 7.
  - Result: best-quadrature homodyne squeezing of the whole vector soliton is close to the scalar value at the same distance. It comes from near-perfect anticorrelation of the two components; each component alone is weakly squeezed.
  - Not covered: filtered direct detection is treated only for the scalar soliton (reproducing Mecozzi & Kumar, Quantum Semiclass. Opt. 10, L21 (1998)). There is no dispersion, walk-off or fiber.
- Rand, Steiglitz & Prucnal, "Quantum theory of Manakov solitons," PRA 71, 053805 (2005), DOI [10.1103/PhysRevA.71.053805](https://doi.org/10.1103/PhysRevA.71.053805). **Full text** (author copy, cs.princeton.edu/~ken).
  - Method: Haus–Lai linearization of the two-component Manakov soliton (equal self- and cross-phase, no walk-off), with the continuum neglected.
  - Results: the polarization-angle variance is $1/(4A_0)$, independent of $z$; the phase variances grow as $z^2$; optimal homodyne squeezing equals the scalar optimum for any partition.
  - Not covered: filtered or direct detection is left as future work. The linearization is stated valid for $1^\circ<\phi<89^\circ$, which excludes the weak-admixture limit.
- Konyukhov, PRA 111, 013508 (2025), DOI [10.1103/PhysRevA.111.013508](https://doi.org/10.1103/PhysRevA.111.013508), [arXiv:2412.09208](https://arxiv.org/abs/2412.09208): linearized quantum fluctuations of vector solitons, using Manakov and coupled-NLS models with differential group delay and birefringence. Readout is polarization-diversity homodyne and photon-number correlation maps of pulse pairs from soliton splitting. There is no spectral filtering and no bound two-component soliton with walk-off. **Full text, keyword-scanned.** A related paper is Konyukhov, Konyukhova & Melnikov, Laser Phys. Lett. (2024), DOI [10.1088/1612-202X/ad9d25](https://doi.org/10.1088/1612-202X/ad9d25), on fission of chirped Manakov solitons. **Abstract only**; an open-access full text exists but was not read.
- Lee, Lai & Malomed, PRA 71, 013816 (2005), [arXiv:quant-ph/0405138](https://arxiv.org/abs/quant-ph/0405138): negative photon-number correlation between the x and y components of interacting temporal vector solitons. The model uses the circular basis with cross/self ratio 2 and no walk-off; there is no filtering. **Full text.**
- Hirosawa, Kannari, Takeoka & Sasaki, PRA 76, 043817 (2007), DOI [10.1103/PhysRevA.76.043817](https://doi.org/10.1103/PhysRevA.76.043817): a soliton and a pulse trapped across the zero-dispersion wavelength. Cross-phase modulation gives strong negative photon-number correlation between the soliton and parts of the trapped pulse. **Abstract only.**
- König, Zielonka & Sizmann, PRA 66, 013812 (2002), DOI [10.1103/PhysRevA.66.013812](https://doi.org/10.1103/PhysRevA.66.013812): transient spectral correlations between colliding solitons with different group velocities. **Abstract only.**
- Polarization squeezing in fiber. These papers treat the two polarizations as independent or as walking through each other; none treats a bound vector soliton.
  - Corney et al., [arXiv:quant-ph/0603280](https://arxiv.org/abs/quant-ph/0603280) (PRL 97, 023606 (2006)): polarization squeezing in birefringent fiber. **Abstract only** (gpt intake). Helper claude-b.3 reports that its model has no cross-polarization coupling.
  - Kalinin et al., Adv. Quantum Technol. 6, 2200143 (2023), DOI [10.1002/qute.202200143](https://doi.org/10.1002/qute.202200143): robust all-fiber polarization squeezing, more than 5 dB. **Abstract only** (checked by claude-b). Helper claude-b.3 read the full text: the model includes walk-off and cross-phase modulation for pulses that overlap only briefly.
- Sloan et al., [arXiv:2509.03482](https://arxiv.org/abs/2509.03482). **Full text** of the main paper; the supplement was not accessed.
  - Content: wavefront shaping in a multimode fiber brings pixel noise 12 dB below linear attenuation, near shot noise. The optimization simulations are near-CW; simulated squeezing reaches at most about 0.5 dB.
  - Mechanism identified: SPM and XPM convert input power noise into noise in the relative intermodal phase.
  - Not covered: solitons and filtered soliton squeezing.
- Uddin et al., Nat. Photon. 19, 751 (2025), DOI [10.1038/s41566-025-01677-2](https://doi.org/10.1038/s41566-025-01677-2). **Abstract only** (see `docs/references.md`).

**Multimode solitons (mean field):**
- Renninger & Wise, Nat. Commun. 4, 1719 (2013), DOI [10.1038/ncomms2739](https://doi.org/10.1038/ncomms2739): GRIN multimode solitons whose modes align to a common group velocity. No noise. **Full text, keyword-scanned.**
- Buch & Agrawal, OL 40, 225 (2015), DOI [10.1364/OL.40.000225](https://doi.org/10.1364/OL.40.000225): solitons in different modes trap each other by spectral shifts despite their differential group delay. **Abstract only.**
- Zitelli, Mangini, Ferraro, Sidelnikov & Wabnitz, Commun. Phys. (2021), DOI [10.1038/s42005-021-00687-0](https://doi.org/10.1038/s42005-021-00687-0): multimode solitons decay over hundreds of nonlinear lengths into LP01 solitons. In GRIN fiber, multimode solitons of non-degenerate modes longer than a few hundred femtoseconds cannot form. **Abstract only.**
- Zitelli, [arXiv:2404.00991](https://arxiv.org/abs/2404.00991) (2024 review). It has no noise, jitter or squeezing analysis. **Full text, keyword-scanned.**
- Sun, Parra-Rivas, Agrawal, Hansson, Antonelli & Mecozzi, "Multimode solitons in optical fibers: a review," Photonics Res. 12, 2581 (2024), DOI [10.1364/PRJ.531393](https://doi.org/10.1364/PRJ.531393). **Full text** (repository copy), sections 3–4 read and the rest keyword-scanned.
  - Content: walk-off is removed by a gauge transformation (Eqs. 40–41); the power in each mode is conserved; a multimode soliton's group velocity is tied to its modal composition.
  - Not covered: no quantum or noise analysis.

**Searches** (claude-b, 2026-10-04):
- OpenAlex forward citations of Levandovsky et al. 1999 (49 works), Steiglitz & Rand 2009 (28), Rand et al. 2005 (21) and Gordon & Haus 1986 (the first 100 of 891), screened by title.
- OpenAlex searches: "walk-off soliton multimode fiber", "soliton stability and trapping in multimode fibers", "multimode soliton timing jitter", "soliton trapping multimode fibers random mode coupling".
- Keyword scans of both 2024 multimode-soliton reviews.
- Two helper searches by subagents claude-b.2 and claude-b.3 on vector and multimode soliton noise and multimode-fiber squeezing; their results are in the review log `log/2026-10-04_claude-b_T-20261004-root-02.md`.

**Independent GPT review** (gpt-b, 2026-10-04), kept as written; it reads several of the same sources with its own access levels:

- Rand, Steiglitz & Prucnal, [10.1103/PhysRevA.71.053805](https://doi.org/10.1103/PhysRevA.71.053805), **full text**: Manakov vacuum covariance and scalar-equivalent squeezing with a local oscillator formed from the discrete dual modes. This does not automatically solve a fixed bandpass or a reference constrained to be a copy of the launch.
- Lantz et al., [arXiv:quant-ph/0311088](https://arxiv.org/abs/quant-ph/0311088), **full text**: vector spatial-soliton squeezing and component correlations with a different coupling matrix and an unstable mean family. Its diffraction equation maps to a temporal NLSE, so the spatial-versus-temporal label alone cannot establish novelty.
- Sloan et al., [arXiv:2509.03482](https://arxiv.org/abs/2509.03482), **full text of main paper**, supplementary information **not accessed**: general multimode quantum-noise propagation, spatial filtering and relative-phase conversion. The main paper does not give the target soliton law.
- Haus & Lai, [10.1364/JOSAB.7.000386](https://doi.org/10.1364/JOSAB.7.000386), **abstract only**: scalar coordinate noise and tailored homodyne readout.
- Kärtner & Boivin, [10.1103/PhysRevA.53.454](https://doi.org/10.1103/PhysRevA.53.454), **abstract only**: dependence on the initial quantum soliton state and limits of linearization.
- Levandovsky, Vasilyev & Kumar, [10.1364/OL.24.000043](https://doi.org/10.1364/OL.24.000043), **abstract only** plus indexed author-upload excerpts, not a full-text review: continuum-aware scalar spectral filtering. The scalar full-text access loose ends are T-20261004-gpt-b-01.
- Corney & Drummond, [arXiv:quant-ph/9912096v2](https://arxiv.org/abs/quant-ph/9912096v2), **full text**: source-separated scalar timing/frequency noise and matching Raman reservoir, relevant to the nuisance-coordinate and Raman baselines.

## Sharpest statement of the gap

**Known:**
- Single-mode soliton squeezing, under both filtering and reference readout.
- For a two-component Manakov soliton without walk-off, optimal homodyne squeezing is the scalar value (Rand et al. 2005). By the unitary symmetry of the Manakov system, so is every readout that treats the modes alike (reduction 1).
- Walk-off is equivalent to a launch frequency offset (reduction 2).
- Multimode solitons exist only for $\delta\lesssim1$ and decay towards LP01 (reduction 3).
- Lantz et al. found the vector spatial-soliton analogue: whole-beam squeezing close to scalar, carried by anticorrelated components.

**Not found:** a calculation of filtered or reference-readout noise for a fiber soliton whose components have unequal Kerr overlaps or walk-off, or any quantum-noise treatment of GRIN multimode solitons.

**The open quantity is narrower than first stated.** It is the deviation of $F_{\min}$ from the LP01 value at the same $\zeta$ caused by:
- the non-Manakov part of $C$;
- $\delta_m$, equivalently a launch frequency offset, inside the existence window $\delta\lesssim1$;
- intermodal Raman terms;
- degenerate-group four-wave mixing.

Whether this deviation is large enough to matter is not known. At $\delta=0$ the non-Manakov perturbation is small for $p_2\lesssim0.3$, so a sizeable effect, if any, is most likely to come from walk-off and Raman.

**GPT review's statement** (gpt-b, 2026-10-04):

Multicomponent soliton squeezing already exists, and the integrable Manakov optimum for a particular homodyne family equals the scalar optimum. The searched sources did not yield a controlled correction for physically distinct, unequal-overlap spatial modes with walk-off, a qualified bound/near-soliton mean field, and either of the two specified readouts. Novelty must reside in that correction and its measurable limits, rather than in adding components or claiming an energy-only advantage.

Fix spectral transmission and reference power/loss before optimizing. Retain continuum fluctuations whenever the readout is not a discrete dual-mode projection. The limiting model must recover the published Manakov/scalar baselines where applicable. Two completed family reviews are still required before task -10 begins; this GPT review adds only `gpt`.

Note added when the two reviews were merged (claude-interactive, 2026-10-06): with T-20261004-root-02 merged, the Claude-family review is also complete and `audited_by` is `[claude, gpt]`. Status and whether task -10 may begin were not changed here.

## Conjectures

None registered.

## Oracle

For high mode counts, the solver's CP backend implements the parallel-factor decomposition of the overlap tensor in Rivera, [arXiv:2609.16502](https://arxiv.org/abs/2609.16502) (full text, keyword-scanned). It reports over 1,000 modes on current hardware, including multimode solitons in GRIN fiber. Its noise example is classical: 0.1% pulse-energy noise, about 60 dB above vacuum, in the fission of a 20-mode soliton. The paper reports no quantum-squeezing result, although its code-feature table lists squeezing and birefringent-soliton examples. The solver (`solver/`) supports multimode GNLSE, adjoints and stochastic propagation. The archive's runs cover only axisymmetric radial modes, so LP11 needs non-axisymmetric modes; check this in T-20261004-root-03. Use the pinned solver for the qualified mean trajectory and its linearized/stochastic noise. Axisymmetric archive coverage does not establish LP11 capability; that remains a solver-capability check. The GPT review is analytical/literature work, not a propagation verification.

Cheap tests:
- $p_{m\neq01}\to0$ recovers the LP01 soliton.
- Collecting all modes and frequencies gives $F=1$ with Raman off.
- **Manakov test.** Set all $C_{mn}=1$ and $\delta=0$ in a two-mode run. The all-mode bandpass $F$ must equal the LP01 $F$ at the same $\zeta$. The mode-resolved $F_m$ and $\rho$ must follow the rotation formulas in reduction 1.
- **Gauge test.** A run with walk-off $\delta$ must equal a run with $\delta=0$, a launch frequency offset of $\delta/T_0$ and a correspondingly shifted filter, with Raman off.
- The weak-admixture limit matches P-20261004-claude-interactive-01.

## Lab test

GIF625 at 1550 nm with the archive's prepared 0.4 ps sech and 20 m of fiber.
- Add a controlled LP02 or LP11 fraction (phase plate or SLM) at the energy given by $\gamma_{\rm eff}$, qualified by the measured or solved mean family (see the mean-field qualification above).
- At the same $T_0$ and $\zeta$, measure $F$ against power for the fixed bandpass and for the reference readout, with and without the admixture, and compare with the LP01-only launch. Mode-resolved detection is optional.

From reduction 1, the expected result for the all-mode bandpass at $\delta\approx0$ is no change from LP01. A measurable difference needs $\delta\sim1$, unequal overlaps or Raman.

**Walk-off of this configuration.** These numbers are from the solver's nominal GIF625 model, an ideal parabolic profile (run `2026-10-04-claude-b-gif625-walkoff`). At 1550 nm:
- $\beta_2=-28.1$ ps²/km;
- the walk-off relative to LP01 is $\Delta\beta_1=0.073$ ps/m for LP11 and $0.151$ ps/m for LP02/LP21.

For the 0.4 ps (FWHM) sech this gives:
- $\delta=0.59$ for LP11, with weak-admixture captured fraction 0.76;
- $\delta=1.22$ for LP02, with captured fraction 0.33.

So the LP02 launch sits just outside the existence window $\delta\lesssim1$, consistent with Zitelli et al.'s statement that non-degenerate multimode solitons longer than a few hundred femtoseconds do not form. $\delta\le1$ for LP02 needs pulses of at most 0.33 ps FWHM, and $\delta\le0.5$ needs at most 0.16 ps. LP11 reaches $\delta\le1$ up to 0.68 ps.

A measured index profile can change these values (T-20261004-claude-b-03).

## Risks and must-reads

- (gpt-b) Lantz and Rand were read in full and materially narrow the target. Levandovsky full text and Sloan supplementary information remain access loose ends under T-20261004-gpt-b-01.
- **Unread full texts that could narrow the walk-off part further** (T-20261004-claude-b-02):
  - Hirosawa et al. (2007): a trapped pulse with quantum correlations.
  - Menyuk, JOSA B 5, 392 (1988), DOI [10.1364/JOSAB.5.000392](https://doi.org/10.1364/JOSAB.5.000392): soliton trapping. Not accessed.
- **The problem could turn out minor.** If the non-Manakov and walk-off corrections are small inside the existence window, the answer is "the LP01 value", and the problem is a short exercise rather than a result.
- **Unchecked physics.**
  - Random mode coupling in a real GIF625 can scramble relative modal phases over 20 m; measure the coupling length.
  - The Raman-model ambiguity carried over from the single-mode case remains.
  - Phase-matched channels in the ideal profile:
    - LP02 and LP21 are degenerate, and 02+02↔21+21 mixing has overlap 1/4;
    - 01+03↔02+02 has overlap 1/4;
    - 01+02↔11+11 has overlap 0.

    The first two are second order in the minority amplitude. These are exact Laguerre–Gauss integrals; the script is in the review log.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-04 | /root (gpt) | Created as priority-2 candidate; literature unaudited | PI request; soliton/noise abstract intake; archived successes and failures read; independent review T-20261004-root-02 |
| 2026-10-04 | claude-interactive (claude; claude-opus-5-5) | Rewritten on PI instruction to one target, the minimum noise for a multimode soliton launch; weak admixture moved to P-20261004-claude-interactive-01; unaudited → partial | PI's four-problem set in chat, 2026-10-04; archive baselines; targeted literature search. Not a completed audit |
| 2026-10-04 | claude-b (claude; claude-opus-5-5) | Claude-family full-text review (T-20261004-root-02). Target narrowed to the deviation from the Manakov/LP01 value; added reductions 1–4; removed photon number as a channel for $F$; literature updated with access levels; status, priority, literature_state (partial) and novelty_confidence (low) unchanged. Later the same day, after reading T-20261004-claude-interactive-08's Raman default-spectrum finding, a normalization caveat was added to the single-mode baseline bullet (T-20261004-claude-b-08) | Full texts: Lantz et al.; Rand, Steiglitz & Prucnal 2005; Lee, Lai & Malomed 2005; Konyukhov 2025 (scanned); Sloan et al.; Werner & Friberg; Sun et al. 2024; Rivera 2026 (scanned). Abstracts for the rest; searches listed above. Log `log/2026-10-04_claude-b_T-20261004-root-02.md` |
| 2026-10-04 | gpt-b (gpt; gpt-6-astra) | Completed GPT scope review; retained candidate, qualified the mean family and removed an unsupported universal participation target | Full-text Rand, Lantz, Sloan and Corney; common-sech substitution test and ideal-overlap run 2026-10-04-gpt-b-overlap-capture; docs/review-2026-10-04-gpt-b-soliton-noise.md |
| 2026-10-04 | claude-b (claude; claude-opus-5-5) | Exploration T-20261004-claude-b-06; no card text changed, because three review PRs rewrite this card. Model: pure-Kerr two-mode, ideal GRIN overlaps ($C_{22}=1/2$), launch at the $\gamma_{\rm eff}$ energy, hard bandpass (edges 0.55–1.18; $p_2$ = 0.3 and 0.15). At $\delta=0$ the all-mode filtered Fano factor is within 0.016 dB of LP01 at $\zeta=2$ and 0.03–0.31 dB above it at $\zeta=5$. Walk-off ($\delta=0.94$) traps the components at carriers $+p_2\delta$ and $-p_1\delta$. At each launch's best scanned band (the card's minimum $F$), walk-off costs 0.40 dB at $\zeta=2$ and 1.7–2.5 dB at $\zeta=5$. At best band the GRIN launch never beats LP01 by more than 0.014 dB. At equal band the deviation ranges from +3.6 dB (narrow) to $-0.125$ dB ($p_2=0.15$, widest band, where LP01 is 4.3 dB from its own best). Mode-resolved bands centred on the trapped carriers are worse. The mode-resolved LP01–LP02 count correlation is $-0.10$ to $-0.57$ and follows the Manakov rotation within 2–6% at $\delta=0$. Same family as the reductions it tests | Runs `2026-10-04-claude-b-manakov-deviation-scan`, `2026-10-04-claude-b-manakov-deviation-edge-scan`; `explorations/2026-10-04-claude-b-manakov-deviation.md`; log `log/2026-10-04_claude-b_T-20261004-claude-b-06.md` |
| 2026-10-04 | claude-b.1 (claude; claude-opus-5-5) | Registered LP01 baselines as runs: archive ideal-sech Kerr control, 20 m prepared-sech reference readout (both Raman models) and one pre-registered 1546.5–1553.5 nm bandpass point, all reproduced bit for bit with the pinned solver; card text otherwise unchanged | runs `2026-10-04-claude-b.1-ideal-sech-kerr-20m`, `2026-10-04-claude-b.1-prepared-sech-readout-20m`, `2026-10-04-claude-b.1-bandpass-1546-1553-20m`; `explorations/2026-10-04-claude-b.1-lp01-soliton-baselines.md` |
| 2026-10-08 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Added Find item 4: prove or refute an inequality between filtered Manakov (LP01) and GRIN soliton noise, or whether GRIN can ever beat LP01. No other change | PI direction in chat, 2026-10-08 |
