---
id: P-20261012-claude-interactive.5-04
title: "Energy-conversion ceiling for pulsed three-wave mixing with walk-off and depletion: from the integrable limit to dispersion-engineered waveguides"
status: candidate
priority: 2
literature_state: partial
novelty_confidence: low
target_quantity: "The maximum fraction of input pulse energy convertible to the sum-frequency (or second-harmonic, or signal-plus-idler) wave in a single pass of a chi(2) waveguide with group-velocity walk-off and full depletion, over all crystal lengths and over input pulse shapes of fixed energy and duration, as a closed-form or asymptotic law in the walk-off group and the energy ratio, with the integrable three-wave limit as the anchor and group-velocity dispersion, Kerr and loss as the corrections."
model: "1+1D three-wave resonant interaction (coupled-wave) equations with first-order group-velocity mismatch and no dispersion (integrable; degenerate SHG case included); then second-order dispersion, cascaded chi(2) (effective Kerr) phase, higher-order modes and loss; thin-film lithium niobate parameters as the reference platform."
oracle_ready: missing
last_audited: null
audited_by: [claude]
proposed_by: claude-interactive.5
provenance:
  agent: claude-interactive.5
  model: claude-fable-5-1
  family: claude
claims: []
results: []
---

## Target quantity

**Setting.** Three envelopes $A_1,A_2,A_3$ with group velocities $v_1<v_2<v_3$ obey $(\partial_z+v_j^{-1}\partial_t)A_j=i\kappa_jA_kA_l^*$-type equations (the three-wave resonant interaction, TWRI); SHG is the degenerate case with $A_1=A_2$. Inputs are a pump pulse of energy $U_p$ and duration $\tau_p$ and a signal of energy $U_s$ (or, for SHG, one fundamental pulse). Dimensionless groups: the walk-off number $W=\delta L/\tau_p$ with $\delta$ the group-delay mismatch per unit length, the drive strength $\Gamma=\kappa\sqrt{P_p}L$ or equivalently the pulse "area" $\theta=\kappa\sqrt{P_p}\,\tau_p/\delta$ (independent of $L$: the only intrinsic strength parameter in the walk-off-dominated limit), and the energy ratio $r=U_s/U_p$.

**Targets.**
1. $\eta_{\max}(W,\theta,r)=\sup$ over $L$ of the converted energy fraction for given input shapes (Gaussian first), and the law of the ceiling as $W\to\infty$ at fixed $\theta$ (walk-off dominated): the fraction that is never converted, as a function of $\theta$ and $r$. The integrable theory says that in the long-interaction limit the unconvertible part is set by the soliton content of the inputs (the discrete spectrum of the associated $3\times3$ scattering problem). Target: that fraction as a closed form or a scaling law in $\theta$ (number of solitons grows with $\theta$).
2. $\sup$ over input shapes of fixed energy and duration (including chirp) of $\eta_{\max}$: whether shaping can remove the soliton content, and the best shape family.
3. For degenerate SHG with walk-off (Kaup 1978; Riemann–Hilbert treatments), the same ceiling, which is the quantity thin-film lithium niobate SHG experiments measure.
4. Corrections: group-velocity dispersion $D=\beta_2L/\tau_p^2$, cascaded-$\chi^{(2)}$ phase, loss and higher-order modes, each as a first-order correction to the ceiling.

**Answer form.** $1-\eta_{\max}=F(\theta,r)+O(1/W)+O(D)$ with $F$ derived from scattering data, plus the optimal-shape statement of target 2.

## Signal of hidden simplicity

- The dispersionless TWRI is integrable (Zakharov–Manakov; Kaup). Pump depletion in the long-time limit proceeds by soliton transfer only, with an $N$-soliton formula (Kaup, Reiman & Bers 1979). So the asymptotic conversion is fixed by discrete scattering data, which is a small set of numbers.
- Dispersion-engineered thin-film lithium niobate reaches near-zero walk-off and quasi-static femtosecond SHG at femtojoule energies (Jankowski et al. 2020), so both limits $W\ll1$ and $W\gg1$ are now accessible in one platform.
- Experiments at large conversion show saturation with spectral and temporal distortion (Bell Labs 2002 PPLN waveguides), consistent with a ceiling set by the inputs' structure rather than by length.

## Literature state

Search strings (claude-interactive.5, 2026-10-12): Kaup 1978 "simple harmonic generation" exact; three-wave resonant interaction inverse scattering conversion efficiency walk-off; Ibragimov Struthers Kaup optical parametric amplification solitons; Degasperis Conforti Baronio Wabnitz three-wave solitons; femtosecond SHG PPLN pump depletion walk-off; Jankowski ultrabroadband nanophotonic PPLN; OPCPA maximum conversion efficiency back-conversion quasi-parametric.

- D. J. Kaup, "Simple harmonic generation: an exact method of solution," Stud. Appl. Math. 59, 25 (1978). **Not accessed** (located through citations). Inverse-scattering solution of SHG with walk-off.
- D. J. Kaup, "Applications of the inverse scattering transform II: the three-wave resonant interaction," Rocky Mountain J. Math. 8, 283 (1978), DOI 10.1216/RMJ-1978-8-1-283. **Abstract only.**
- D. J. Kaup, A. Reiman & A. Bers, "Space-time evolution of nonlinear three-wave interactions. I. Interaction in a homogeneous medium," Rev. Mod. Phys. 51, 275 (1979), DOI 10.1103/RevModPhys.51.275. **Abstract only.** Pump depletion by soliton transfer only, with an $N$-soliton formula; thresholds for explosive instabilities; conditions for optimal energy transfer in two-pump interactions.
- D. J. Kaup, Stud. Appl. Math. 55, 9 (1976), DOI 10.1002/sapm19765519. **Abstract only.** All solitons of the middle-velocity envelope split and join the fast and slow envelopes; radiation does not convert.
- E. Ibragimov, A. A. Struthers & D. J. Kaup, Opt. Commun. 152, 101 (1998), DOI 10.1016/S0030-4018(98)00148-5. **Abstract only.** "The output is determined solely by the intensity of any TWI-solitons contained in the pump." The structural statement behind target 1, without a law in $\theta$.
- E. Ibragimov & A. A. Struthers, Opt. Lett. 21, 1582 (1996), DOI 10.1364/OL.21.001582. **Abstract only.** Soliton solutions with energy conversion close to 100% and small satellites in numerics.
- R. J. Buckingham, R. M. Jenkins & P. D. Miller, arXiv:1609.05416 (Commun. Math. Phys. 354, 1015 (2017)). **Full text** (subagent). Semiclassical soliton ensembles of the TWRI; the soliton number of a smooth envelope is its area over $\pi$ (their eq. 4.6); no energy-partition or conversion formula, and the long-time limit is said to carry no additional information.
- H. Steudel, C. Figueira de Morisson Faria, M. G. A. Paris, A. M. Kamchatnov & O. Steuernagel, Opt. Commun. 150, 363 (1998). **Abstract only.** The 1D SHG initial-value problem for an amplitude-modulated fundamental is solved through a Schrödinger problem whose potential is the pulse shape, with several exact examples; the closest SHG item, conversion fraction not visible in the abstract.
- A. Degasperis, M. Conforti, F. Baronio, S. Wabnitz & S. Lombardo, Lett. Math. Phys. 96, 367 (2011): also gives an explicit spectral representation of the Manley–Rowe invariants, which is the route to the converted fraction from scattering data.
- A.-Y. Jin & R. Guo, "Breather interactions and limit analysis in the second harmonic generation process via Riemann–Hilbert approach," arXiv:2512.19242 (2025). **Abstract only.** Soliton and breather solutions of the phase-matched SHG system; no conversion-efficiency statement.
- E. Ibragimov, A. A. Struthers, D. J. Kaup, J. D. Khaydarov & K. D. Singer, "Three-wave interaction solitons in optical parametric amplification," Phys. Rev. E 59, 6122 (1999), DOI 10.1103/PhysRevE.59.6122. **Abstract only.** TWRI-soliton theory applied to a synchronously pumped OPA; explains compression limits.
- M. Conforti, F. Baronio, A. Degasperis & S. Wabnitz, "Inelastic scattering and interactions of three-wave parametric solitons," arXiv:physics/0609034 (Phys. Rev. E 74, 065602 (2006)). **Abstract only.** Velocity-locked three-wave solitons; frequency conversion controlled by a CW background (also arXiv:0706.3577, **abstract only**).
- A. Degasperis, M. Conforti, F. Baronio, S. Wabnitz & S. Lombardo, "The three-wave resonant interaction equations: spectral and numerical methods," Lett. Math. Phys. 96, 367 (2011), DOI 10.1007/s11005-010-0430-4. **Abstract only.** Numerical direct spectral problem (continuum plus discrete eigenvalues).
- E. Sidick, A. Knoesen & A. Dienes, J. Opt. Soc. Am. B 12, 1704 (1995), DOI 10.1364/JOSAB.12.001704, and E. Sidick, A. Dienes & A. Knoesen, J. Opt. Soc. Am. B 12, 1713 (1995), DOI 10.1364/JOSAB.12.001713. **Abstracts only.** Numerical ultrashort-pulse SHG with GVM and GVD; overall conversion efficiency and optimum length discussed; no ceiling law.
- H. J. Bakker, P. C. M. Planken, L. Kuipers & A. Lagendijk, Phys. Rev. A 42, 4085 (1990), DOI 10.1103/PhysRevA.42.4085. **Abstract only.** Phase modulation in SHG with mismatch and GVM.
- A. M. Weiner, "Effect of group velocity mismatch on the measurement of ultrafast optical pulses via second harmonic generation," IEEE J. Quantum Electron. 19, 1276 (1983). **Not accessed** (PDF located, not read). Undepleted SHG with walk-off.
- Bell Labs (Nokia) record, "Femtosecond second-harmonic generation in periodically poled lithium niobate waveguides with simultaneous strong pump depletion and group-velocity walk-off," Opt. Lett. (2002). **Abstract only** (publisher record not opened; authors not confirmed). Strong saturation of SHG with pump distortion; cascaded $\chi^{(2)}$ and multimode effects invoked.
- M. Jankowski, C. Langrock, B. Desiatov, A. Marandi, C. Wang, M. Zhang, C. R. Phillips, M. Lončar & M. M. Fejer, "Ultrabroadband nonlinear optics in nanophotonic periodically poled lithium niobate waveguides," Optica 7, 40 (2020), arXiv:1909.08806. **Abstract only.** Dispersion-engineered, quasi-static femtosecond SHG; the reference platform.
- Quasi-parametric amplification (idler absorption) and hybridized schemes for complete pump depletion: arXiv:2207.04147, "High quantum efficiency parametric amplification via hybridized nonlinear optics." **Not accessed** (listing). Shows that idler loss removes back-conversion, so the ceiling in target 1 is for lossless idlers.

What is settled (second search by subagent claude-interactive.5.5, 2026-10-13): the integrable machinery; the structural law that only the pump's soliton content converts while radiation does not (Kaup 1976; Ibragimov, Struthers & Kaup 1998); the soliton count of a smooth envelope as area over $\pi$ (Buckingham, Jenkins & Miller); velocity-locked simultons; undepleted walk-off theory. What was not found: an explicit $\eta_{\max}(\theta,r)$ for Gaussian or sech inputs, any SHG walk-off ceiling in $\theta$ from the inverse scattering transform, the optimal-shape question, or any ceiling for the dispersion-engineered SHG regime with depletion. For a sech pump the discrete spectrum of the associated scattering problem may be classical (Satsuma–Yajima type), which would give the converted fraction in closed form; this was not verified.

## Sharpest statement of the gap

The asymptotic conversion in the integrable TWRI is determined by the pump's soliton content, and the soliton number of a smooth pulse is its area over $\pi$; but the converted *energy* fraction for standard shapes, $\eta_{\max}(W,\theta,r)$, has never been written as a closed form or scaling law (the discrete-spectrum share of the Manley–Rowe invariant), nor has the optimal-shape statement, nor the corrections from dispersion, cascaded phase and loss that decide what a thin-film lithium niobate device can reach.

## Conjectures

No claim files yet. The refutable conjecture: **in the walk-off-dominated limit $W\gg1$ with a weak signal ($r\ll1$), $1-\eta_{\max}$ for a sech pump of area $\theta$ equals the continuous-spectrum share of the pump's Manley–Rowe invariant, a closed form in $\theta$ from the sech-potential discrete spectrum, with jumps in slope at $\theta=(n+\tfrac12)\pi$ where solitons appear; for a Gaussian of the same area the floor is higher, and a shape with the same energy and duration but more soliton content converts more.** A refutation is a TWRI simulation with $W\gg1$ in which the converted fraction tends to one as $L$ grows for a Gaussian pump, or in which shaping does not change the floor.

## Oracle

**Missing in the repository, cheap to add.** A $1+1$D split-step integrator for three coupled envelopes with walk-off (and optional dispersion) is a few hundred lines; the repository's $\chi^{(3)}$ solver does not apply. Checks: energy (Manley–Rowe) conservation to machine precision, time-window size against the walk-off, and step convergence. The adjoint-optimization pattern of the main solver can be reproduced to maximize conversion over input shapes (target 2).

## Lab test

Thin-film lithium niobate SHG or SFG waveguides of several lengths on one chip, fed by pulses of fixed energy and duration, with the converted energy measured against length and pump energy. A measured conversion above the predicted ceiling at large $W$, or complete conversion in the walk-off-dominated regime, falsifies the conjecture; a plateau at the predicted floor supports it.

## Risks and must-reads

- **The answer may be in the integrable literature already** (Kaup, Reiman & Bers in full; the Degasperis–Conforti–Baronio–Wabnitz series; Buckingham–Jenkins–Miller for the semiclassical limit). If the unconvertible fraction for Gaussian inputs has been tabulated, the card narrows to targets 2 and 4. All of these are must-reads in full.
- **Low novelty confidence** for that reason.
- **Non-integrable corrections may dominate** in real devices (cascaded phase at femtojoule energies in nanophotonic waveguides), in which case the integrable ceiling is only a starting point.
- **Fit.** $\chi^{(2)}$ pulses, no fibre; the pulse-propagation and convergence-testing habits of the repository transfer directly.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive.5 (claude; claude-fable-5-1) | Created as candidate; literature searched by the proposer | Searches listed above |
| 2026-10-13 | claude-interactive.5 (claude; claude-fable-5-1) | Literature state sharpened after a second search (subagent claude-interactive.5.5): structural soliton-content law found published; explicit conversion law still absent | Sources added above |
