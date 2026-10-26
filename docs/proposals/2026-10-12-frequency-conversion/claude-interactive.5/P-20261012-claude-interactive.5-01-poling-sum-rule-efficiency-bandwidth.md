---
id: P-20261012-claude-interactive.5-01
title: "Sum-rule bound on the efficiency–bandwidth trade-off of poled three-wave mixing, and its fate under depletion, walk-off and loss"
status: candidate
priority: 1
literature_state: partial
novelty_confidence: medium
target_quantity: "The reachable set of conversion spectra eta(Delta k) of a quasi-phase-matched sum-frequency (or difference-frequency, or parametric-gain) device of length L and maximum coupling kappa over all poling profiles, in particular the largest band over which eta >= 1-epsilon, bounded through the log-area integral of ln[1/(1-eta)] over phase mismatch, with the undepleted-pump CW theorem as the anchor and the depleted, pulsed-walk-off and lossy extensions as the open part."
model: "Coupled-mode equations for signal and sum-frequency (or signal and idler) fields in a chi(2) waveguide with a poling profile g(z), |g| <= 1, phase mismatch Delta k linear in detuning (first-order group-velocity mismatch), undepleted CW pump as the anchor; then full three-wave equations with pump depletion, pulsed pump with walk-off, second-order dispersion and propagation loss."
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

**Setting.** A $\chi^{(2)}$ waveguide of length $L$ with a quasi-phase-matching (QPM) profile $g(z)$, $|g(z)|\le1$ ($g=\pm1$ for binary poling; $|g|<1$ for duty-cycle apodization). With an undepleted CW pump the signal $A_1$ and sum-frequency $A_2$ photon-flux amplitudes obey
$$\partial_zA_1=i\kappa g(z)A_2e^{i\Delta k z},\qquad \partial_zA_2=i\kappa g(z)A_1e^{-i\Delta k z},$$
with $|A_1|^2+|A_2|^2$ conserved. $\kappa$ is the coupling at full poling, so a uniform device gives $\eta=\sin^2(\kappa L)$ at $\Delta k=0$. The conversion spectrum is $\eta(\Delta k)=|A_2(L)|^2$ for $A_1(0)=1$. Over the usual bandwidths $\Delta k=\delta\,\Omega$ with $\delta$ the group-delay mismatch per unit length, so bounds in $\Delta k$ are bounds in frequency.

**Anchor (a known theorem transcribed).** The gauge $u=A_1e^{i\Delta kz/2}$, $v=A_2e^{-i\Delta kz/2}$ turns the system into the Zakharov–Shabat (ZS) scattering problem with potential $q=\kappa g$ and spectral parameter $\xi=\Delta k/2$, of the sign that conserves $|u|^2+|v|^2$ (the "focusing" ZS, scattering matrix in SU(2)). The first trace formula of that problem reads
$$\int_{-\infty}^{\infty}\ln\frac{1}{1-\eta(\Delta k)}\,d\Delta k\;=\;2\pi\kappa^2\!\int_0^L g^2dz\;-\;8\pi\sum_k\mathrm{Im}\,\xi_k\;\le\;2\pi\kappa^2L,$$
where $\xi_k$ are the discrete eigenvalues (bound states) of the potential in the upper half plane. A scratch check in this session (not a registered run) confirmed the $8\pi\sum_k\mathrm{Im}\,\xi_k$ normalization on uniform boxes carrying one and two bound states, whose eigenvalues solve $\cot(sL)=-\mathrm{Im}\,\xi/s$ with $s=\sqrt{\kappa^2-(\mathrm{Im}\,\xi)^2}$; the deficit of the log-area below $2\pi\kappa^2L$ matched the eigenvalue sum to the truncation error of the $\Delta k$ window. The first bound state appears at $\kappa L=\pi/2$, that is, exactly when a uniform device over-rotates at $\Delta k=0$. Call the left side the **log-area** $\mathcal A[g]$. Consequences:
- A flat-top band of width $B$ (in $\Delta k$) at efficiency $\ge1-\epsilon$ needs $B\ln(1/\epsilon)\le2\pi\kappa^2L$, i.e. $\Delta\Omega\le2\pi\kappa^2L/(\delta\ln(1/\epsilon))$.
- A linear chirp (adiabatic, Landau–Zener) design with sweep rate $\alpha=B/L$ gives $\epsilon=\exp(-2\pi\kappa^2/\alpha)$, hence $B\ln(1/\epsilon)=2\pi\kappa^2L$: it saturates the bound asymptotically. So the Landau–Zener line is the achievable point, and the bound is tight in the limit $B\gg\kappa$.
- For parametric gain (signal–idler, SU(1,1), the "defocusing" ZS, no bound states) the identity is an equality for every design: $\int\ln G(\Delta k)\,d\Delta k=2\pi\kappa^2\int g^2dz$ with $G$ the signal power gain. Every poling of the same length and coupling has the same gain log-area; chirped QPM only redistributes it.

**The targets (what is not a transcription).**
1. **Reachable set at finite length.** Beyond the first trace formula, the higher trace formulas constrain the moments $\int\Delta k^{2n}\ln[1/(1-\eta)]\,d\Delta k$ through $\int|g'|^2$, $\int g^4$ and so on. Target: the Pareto frontier $B_{\max}(\kappa L,\epsilon)$ over all $g$ with $|g|\le1$, and separately over binary $g=\pm1$ with a minimum domain length, with its gap to the Landau–Zener design as a function of $\kappa L$ and $\epsilon$. Answer form: $B_{\max}\,\ln(1/\epsilon)/(2\pi\kappa^2L)=1-c(\epsilon)/(\kappa L)^p+\dots$ with $c$ and $p$ derived.
2. **Pump depletion.** With a depleted CW pump the problem is the full three-wave system (Jacobi-elliptic CW solutions; adiabatic complete conversion exists, Porat & Arie 2013). Target: whether $\mathcal A\le2\pi\kappa_0^2L$ still holds with $\kappa_0$ the coupling at the input pump flux, and the corrected sum rule in the group $r=N_s/N_p$ (signal to pump photon-flux ratio). A conjecture is below.
3. **Pulsed pump with walk-off.** For a pump pulse of duration $\tau_p$ with group-delay mismatch $\delta_{ps}$ to the signal, the conversion is a linear operator with Schmidt efficiencies $\eta_n$. Target: the generalization of the log-area to $\sum_n\ln[1/(1-\eta_n)]$ in terms of pump energy, $\kappa_{\rm pk}^2L$ and $\delta_{ps}L/\tau_p$, and whether it is saturated by any known pulse gate.
4. **Loss.** With propagation loss $\alpha_1,\alpha_2$ the scattering is not unitary. Target: the lossy sum rule to first order in $\alpha L$, and whether loss ever helps the flat-top bandwidth (it cannot increase the log-area, but it may remove bound states).
5. **Second-order dispersion** ($\Delta k$ quadratic in $\Omega$): the same identity holds in $\Delta k$; the open question is only the mapping to frequency bandwidth, which is immediate. Listed for completeness.

**Answer form.** Inequalities and equalities in the dimensionless groups $\kappa L$, $B/\kappa$ (or the adiabaticity parameter $2\pi\kappa^2/\alpha$), $\epsilon$, $r=N_s/N_p$, $\delta_{ps}L/\tau_p$, $\alpha_{1,2}L$, with the Landau–Zener and uniform designs as reference points.

## Signal of hidden simplicity

- The undepleted CW problem is integrable in $z$ for every $g$, so the whole spectrum $\eta(\Delta k)$ is constrained by an infinite hierarchy of exact sum rules, the first of which fixes a single scalar.
- The Landau–Zener formula, which is exact for an infinite linear sweep, saturates the first sum rule exactly. The chirped-QPM optical parametric amplifier (OPA) design formulas of Charbonneau-Lefort, Afeyan & Fejer (gain $\propto\exp(2\pi\kappa^2/\alpha)$ over bandwidth $\alpha L$) also give a gain log-area of exactly $2\pi\kappa^2L$, as the SU(1,1) identity requires. Two independent design results sit on the same line.
- A scratch check in this session (transfer-matrix evaluation of $\eta(\Delta k)$; not a registered run, to be repeated as one) found the uniform-poling log-area equal to $2\pi\kappa^2L$ within the truncation error of the $\Delta k$ window for $\kappa L<\pi/2$, a sharp deficit as soon as $\kappa L>\pi/2$ (the first bound state appears when the device over-rotates at $\Delta k=0$), and linear-chirp designs within one percent of equality with in-band efficiencies tracking the Landau–Zener value.
- The same identity governs NMR pulse design, where it is the minimum-energy theorem for a prescribed inversion profile (Epstein 2004; Epstein & Magland 2009). There, the "no bound states" solution is the minimum-energy pulse. That is a ready-made construction for optimal poling profiles.

## Literature state

Search strings (claude-interactive.5 and subagent claude-interactive.5.1, 2026-10-12): "trace formula" Zakharov-Shabat "sum frequency"; "sum rule" quasi-phase-matching bandwidth; "Zakharov-Shabat" "quasi-phase matching"; "inverse scattering" QPM grating design; "layer peeling" quasi-phase-matched; "nonlinear Fourier transform" frequency conversion poling; "efficiency-bandwidth product" frequency conversion limit; FBG ln(1-R) sum rule; "area theorem" grating; Bode-Fano grating mirror; codirectional coupler inverse scattering; Epstein minimum energy inverse scattering; Kobzar Glaser limits broadband inversion; Li Khaneja ensemble control; adiabatic frequency conversion Suchowski Porat Arie; Charbonneau-Lefort chirped QPM OPA; "fundamental limit" bandwidth frequency conversion arXiv.

- C. L. Epstein, "Minimum energy pulse synthesis via the inverse scattering transform," J. Magn. Reson. 167, 185 (2004), DOI 10.1016/j.jmr.2003.12.014. **Not accessed** (located through citations). States the SU(2) trace formula as a minimum-energy theorem for NMR pulses.
- C. L. Epstein & J. Magland, "Discrete inverse scattering theory for NMR pulse design," arXiv:0903.4363. **Full text** (subagent). Theorem 1.7.1: pulse energy $=\frac4\pi\int\log(1+|r|^2)d\xi+16\sum\mathrm{Im}\,\xi_k$ in their normalization; $1+|r|^2=1/(1-\eta)$. This is the anchor identity, with the bound-state term. Not connected to optics there.
- A. Mafi, "Anderson localization in a partially random Bragg grating and a conserved area theorem," arXiv:1507.04284. **Full text** (subagent). A conserved log-transmittance area for lossless 1D stacks (counter-propagating analogue), stated as a redistribution theorem, not a design limit.
- M. A. Kats, "Lower bound on the thickness of broadband dielectric mirrors," arXiv:2608.26633. **Abstract only.** A causality sum rule on $\int\ln T\,d\lambda$ gives a minimum mirror thickness; the reflective (counter-propagating) analogue of target 1.
- K. N. Rozanov, IEEE Trans. Antennas Propag. 48, 1230 (2000). **Not accessed** (secondary sources). Bode–Fano-type thickness bound for absorbers.
- D. A. B. Miller, Phys. Rev. Lett. 99, 203903 (2007), DOI 10.1103/PhysRevLett.99.203903. **Abstract only.** Delay–bandwidth limit for linear 1D structures.
- X. Xiong, C.-L. Zou, X.-F. Ren, Q. Guo et al., "Broadband frequency conversion via adiabatically tapered χ(2) waveguide," arXiv:1609.09221. **Full text** (subagent). States an "area law" $\int\eta\,d\lambda\propto|g|^2L/(d\Delta\beta/d\lambda)$ derived in the low-efficiency (Parseval) limit and says explicitly that it fails at saturation. The log form above is the saturating version.
- H. Suchowski, D. Oron, A. Arie & Y. Silberberg, Phys. Rev. A 78, 063821 (2008), DOI 10.1103/PhysRevA.78.063821. **Abstract only.** Bloch-sphere picture of SFG and adiabatic conversion. Specific designs, no bound over designs.
- G. Porat & A. Arie, J. Opt. Soc. Am. B 30, 1342 (2013), DOI 10.1364/JOSAB.30.001342. **Abstract only.** Adiabatic complete conversion with pump depletion (fully nonlinear). Relevant to target 2.
- A. A. Rangelov & N. V. Vitanov, Phys. Rev. A 85, 045804 (2012), arXiv:1111.1333. **Full text** (subagent). Cascaded chirped-QPM three-wave mixing; adiabaticity condition only.
- G. T. Genov, A. A. Rangelov & N. V. Vitanov, J. Opt. 16, 062001 (2014). **Not accessed** (listing only). Composite-pulse designs for frequency conversion.
- M. Charbonneau-Lefort, B. Afeyan & M. M. Fejer, J. Opt. Soc. Am. B 25, 463 (2008), DOI 10.1364/JOSAB.25.000463. **Abstract only.** Chirped-QPM OPA gain and bandwidth formulas; no bound over designs.
- C. R. Phillips, C. Langrock, D. Chang, Y. W. Lin, L. Lin & M. M. Fejer, J. Opt. Soc. Am. B 30, 1551 (2013), DOI 10.1364/JOSAB.30.001551. **Abstract only.** Apodization of chirped gratings.
- K. Kobzar, T. E. Skinner, N. Khaneja, S. J. Glaser & B. Luy, J. Magn. Reson. 170, 236 (2004), DOI 10.1016/j.jmr.2004.06.017, and J. Magn. Reson. 194, 58 (2008), DOI 10.1016/j.jmr.2008.05.023. **Abstracts only.** Numerical limits of broadband inversion pulses; no analytic bound.
- J.-S. Li & N. Khaneja, Phys. Rev. A 73, 030302(R) (2006), arXiv:quant-ph/0510012. **Abstract only.** Ensemble controllability; no quantitative bound.
- V. E. Zakharov & A. B. Shabat, Sov. Phys. JETP 34, 62 (1972). **Not accessed** this session; standard origin of the ZS problem and its conserved quantities.

What is settled: the undepleted-pump CW identity (as an NMR theorem), the linear-regime area law for $\chi^{(2)}$ tapers, and the adiabatic designs. What was not found: any statement of the log-area bound for frequency conversion or parametric gain, any statement that Landau–Zener designs saturate it, and anything on targets 1–4.

## Sharpest statement of the gap

Known: for an undepleted CW pump, $\mathcal A[g]\le2\pi\kappa^2\int g^2dz$ follows from a published trace formula, though it has not been written down for frequency conversion. Not known: (i) the finite-length frontier $B_{\max}(\kappa L,\epsilon)$ and its gap to the linear chirp, including the binary-poling and minimum-domain constraints; (ii) whether any sum rule bounds the log-area once the pump is depleted, and in what group; (iii) the pulsed-pump, walk-off generalization over Schmidt modes; (iv) the lossy correction. The OPA equality is a known-in-principle identity whose consequence (every design has the same gain log-area) has not been stated or tested.

## Conjectures

No claim files yet. The refutable conjecture to register first: **with pump depletion, $\mathcal A\le2\pi\kappa_0^2L$ still holds for every poling profile and every signal-to-pump flux ratio $r$, with $\kappa_0$ evaluated at the input pump flux.** A refutation is a single three-wave simulation (any $g$, any $r$) whose log-area, computed over a wide $\Delta k$ window, exceeds $2\pi\kappa_0^2L$. A second conjecture, for the undepleted case: the Landau–Zener design is within a factor $1+O(1/(\kappa L))$ of $B_{\max}$ at fixed $\epsilon$.

## Oracle

**Missing in the repository, cheap to add.** The undepleted problem is two ODEs per $\Delta k$ (a transfer-matrix product for piecewise-constant $g$, vectorized over $\Delta k$, runs in seconds). The depleted problem is three coupled ODEs per $\Delta k$. The pulsed walk-off problem is a $1+1$D linear coupled-wave PDE whose Green function is obtained column by column, followed by a singular-value decomposition. None of this is in FastDifferentiableMMNLO; a standalone Julia or Python module of a few hundred lines suffices and should live under `runs/` with the usual config and seed records.

**Refutation engine.** Parametrize $g(z)$ (piecewise constant, or Fourier modes clipped to $|g|\le1$) and maximize the flat-top bandwidth, or directly $\mathcal A$, by adjoint gradients or by annealing over binary profiles. Any design beating the bound refutes it; the best found design measures the gap to the Landau–Zener line.

**Cheap tests.** (1) Reproduce the scratch check as a registered run. (2) OPA: verify that uniform, linearly chirped and random binary gratings of equal $\kappa^2L$ have equal $\int\ln G\,d\Delta k$. (3) Depleted CW three-wave mixing at $r=0.1,1,10$ with uniform and chirped $g$: compute $\mathcal A$.

## Lab test

Fabricate on the same thin-film lithium niobate (TFLN) or PPLN chip a uniform, a linearly chirped and an apodized SFG device of equal length and duty cycle. Calibrate $\kappa$ from the uniform device at $\Delta k=0$. Sweep $\Delta k$ by tuning the pump wavelength or the temperature while keeping the pump power fixed, record $\eta(\Delta k)$ over a window wide enough to capture the tails, and integrate $\ln[1/(1-\eta)]$. The bound fails if any device's log-area exceeds $2\pi\kappa^2L$ beyond the calibration error. The OPA version repeats this with the parametric gain spectrum and should give the same log-area for all three devices. Raising the pump into depletion tests the conjecture of target 2.

## Risks and must-reads

- **The anchor may already be in the frequency-conversion literature** under a name not searched (for example in the inverse-scattering design of co-directional couplers or in integrated-photonics "mode converter" synthesis). If so, the card narrows to targets 1–4. Must-reads: Epstein 2004 (full text); the Song & Shin 1985 and Feced, Zervas & Muriel 1999 grating-synthesis papers; Brenne & Skaar 2003 on co-directional coupler synthesis; Kats 2026 (full text).
- **Target 2 may have no clean sum rule.** With depletion the $z$-problem is not a linear scattering problem. The conjecture could be refuted in the first run, which is itself a result worth having (it would mean depletion can beat the undepleted bandwidth limit).
- **Target 3 may reduce to target 1** when the pump is much longer than the walk-off, and may be dominated by the time-ordering effects studied in quantum pulse gates (see the companion card P-20261012-claude-interactive.5-03).
- **Fit.** This is a $\chi^{(2)}$ problem with no fibre content; the repository's solver does not apply. Its strengths here are the small, exact models and a refutation engine that is cheap to build.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive.5 (claude; claude-fable-5-1) | Created as candidate; literature searched with one subagent (claude-interactive.5.1); scratch numerical checks of the anchor identity, of Landau–Zener saturation and of the bound-state term's normalization | Searches listed above; scratch checks in the session's scratchpad, not registered runs |
