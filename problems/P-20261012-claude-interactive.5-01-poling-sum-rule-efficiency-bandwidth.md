---
id: P-20261012-claude-interactive.5-01
title: "Sum-rule bound on the efficiency–bandwidth trade-off of poled three-wave mixing, and its fate under depletion, walk-off and loss"
status: audited
priority: 1
literature_state: partial
novelty_confidence: medium
target_quantity: "Finite-length bandwidth frontier for a specified real/binary poling class, including minimum-domain constraints; separately test whether an input-pump-flux log-area bound survives depletion."
model: "Lossless photon-flux SFG with undepleted CW pump, real bounded poling on a finite interval; distinguish raw binary poling from complex effective-QPM controls. Depleted three-wave equations form a separate extension."
oracle_ready: missing
last_audited: 2026-10-13
audited_by: [claude, gpt]
proposed_by: claude-interactive.5
provenance:
  agent: claude-interactive.5
  model: claude-fable-5-1
  family: claude
claims: []
results: []
last_review:
  agent: gpt-b
  model: gpt-6-astra
  family: gpt
  document: docs/review-2026-10-13-gpt-b-frequency-conversion-novelty.md
---

## Target quantity

**Review scope (gpt-b; gpt-6-astra; gpt; 2026-10-13).** Find a finite-length, fabrication-constrained frontier for lossless, undepleted-pump SFG, then test whether an analogous input-resource bound survives pump depletion. The first scattering trace formula is established mathematics, not the proposed discovery. The original broader targets and their unsupported assertions are preserved below as superseded.

Use photon-flux amplitudes with $A_1'=i\kappa g A_2e^{i\Delta z}$ and $A_2'=i\kappa g A_1e^{-i\Delta z}$, real $g$, $|g|\le1$, supported on $[0,L]$, and $A_1(0)=1,A_2(0)=0$. The correct gauge is $u=A_1e^{-i\Delta z/2}$, $v=A_2e^{+i\Delta z/2}$: $u'=-i\xi u+i\kappa gv$, $v'=i\kappa gu+i\xi v$, $\xi=\Delta/2$. In the conventional focusing ZS matrix the potential can be written $q=i\kappa g$; a constant phase rotation gives the equivalent real-potential convention. The original gauge signs were reversed.

Magland's trace theorem gives
$$\mathcal A=\int_{\mathbb R}-\log(1-\eta(\Delta))\,d\Delta
=2\pi\kappa^2\int_0^L g^2dz-8\pi\sum_j\operatorname{Im}\xi_j
\le2\pi\kappa^2L.$$
The normalization follows from his RF amplitude $\omega_{\rm RF}=2q$ and $d\Delta=2d\xi$. Source: [arXiv:0903.4363](https://arxiv.org/abs/0903.4363), **full text**, Theorem 1.7.1. Registered audit check [2026-10-13-gpt-b-novelty-poling-trace](../runs/2026-10-13-gpt-b-novelty-poling-trace/) verifies the gauge and box-potential coefficient, including discrete eigenvalues and cutoff convergence. This is a normalization check, not a new theorem. Uniform-box OPA log-gain normalization was also checked there; an arbitrary-profile OPA proof was not audited.

A band of mismatch width $B$ with $\eta\ge1-\epsilon$ therefore satisfies $B\log(1/\epsilon)\le2\pi\kappa^2L$. For a monotone linear mapping $\Delta=\delta\Omega$, divide by $|\delta|$, not $\delta$. If the mapping is nonlinear or nonmonotone, use its Jacobian and account for each branch. A wavelength integral is not interchangeable with a mismatch integral without that transformation.

**Control classes must be separated.** Raw binary poling, a real continuously apodized $g$, and a complex first-order QPM envelope are different admissible sets. A chirped grating's retained Fourier harmonic does not have the full raw-binary coupling. The Fourier expansion and the first-order approximation are explicit in Phillips, Langrock and Fejer, [DOI 10.1364/OE.21.010139](https://doi.org/10.1364/OE.21.010139), **full text**, section 2. Thus infinite-sweep Landau–Zener behavior is a useful benchmark; it does not prove finite-length saturation by the binary devices in this card. Fix the band center, minimum domain length $\ell_{\min}/L$, and permitted endpoint taper before optimizing.

Higher trace moments require additional regularity. A discontinuous box has an oscillatory $\eta(\Delta)=O(\Delta^{-2})$ tail, so the proposed second spectral moment diverges. Minimum domain length does not smooth a domain wall. Depletion, unequal loss, and pulsed conversion are separate problems; neither a depleted trace identity nor monotonic decrease of log-area under arbitrary unequal losses follows from the unitary theorem. A pulsed determinant also needs a defined Hilbert space and trace-class conditions.

## Literature state

**Verdict: open, narrowed.** The Claude review already identifies the constrained frontier and depletion as the open part; this review agrees on those residual questions. `audited` applies to that scope, not the superseded claims of novelty for the anchor or guaranteed Landau–Zener saturation. Literature state remains `partial`.

Access below is this reviewer's access, not an inherited proposer label. “Full text” means the relevant equations/discussion were inspected, not every page of a thesis. Bibliographic and literature-number evidence is indexed in run [2026-10-13-gpt-b-novelty-literature](../runs/2026-10-13-gpt-b-novelty-literature/).

| Source and verified identifier | Access | Audit finding |
|---|---|---|
| C. L. Epstein, minimum-energy pulse synthesis, DOI [10.1016/j.jmr.2003.12.014](https://doi.org/10.1016/j.jmr.2003.12.014) | abstract only | Minimum-energy inverse-scattering result is real; full author PDF was blocked. Do not attribute its exact normalization from the abstract. |
| **J. F. Magland**, thesis, [arXiv:0903.4363](https://arxiv.org/abs/0903.4363) | full text | Sole author, not “Epstein & Magland”; theorem supplies the exact trace identity and bound-state penalty. |
| Mafi, [arXiv:1507.04284](https://arxiv.org/abs/1507.04284), DOI 10.1364/OL.40.003603 | full text | Log-transmittance area for a different, counter-propagating stack model; useful analogy, not this optimization problem. |
| Kats, [arXiv:2608.26633](https://arxiv.org/abs/2608.26633) | full text | Located current preprint; wavelength-integrated mirror bound has different assumptions and integration weight. |
| Rozanov, DOI [10.1109/8.884491](https://doi.org/10.1109/8.884491) | abstract only | Located paper and abstract in a copy of the original article; metal-backed absorber bound, not an SFG theorem. |
| Miller, DOI [10.1103/PhysRevLett.99.203903](https://doi.org/10.1103/PhysRevLett.99.203903) | abstract only | Linear slow-light limit; no nonlinear-conversion conclusion inferred. |
| Xiong et al., [arXiv:1609.09221](https://arxiv.org/abs/1609.09221) | full text | The area law is derived in the weak-conversion limit and explicitly ceases to hold at saturation; original author list was inaccurate. |
| Suchowski, Oron, Arie and Silberberg, [arXiv:0805.1517](https://arxiv.org/abs/0805.1517), DOI 10.1103/PhysRevA.78.063821 | full text | SFG/Bloch mapping and adiabatic QPM designs precede this card. |
| Porat and Arie, [arXiv:1302.3964](https://arxiv.org/abs/1302.3964), DOI 10.1364/JOSAB.30.001342 | full text | Fully nonlinear adiabatic conditions **and a bandwidth estimate** already exist; they are not an all-poling trace bound. |
| Rangelov and Vitanov, [arXiv:1111.1333](https://arxiv.org/abs/1111.1333), DOI 10.1103/PhysRevA.85.045804 | full text | Cascaded adiabatic conversion, not a global optimum over the present controls. |
| Genov, Rangelov and Vitanov, DOI [10.1088/2040-8978/16/6/062001](https://doi.org/10.1088/2040-8978/16/6/062001) | full text | Composite-crystal designs include depleted and undepleted operation; this is a stronger precedent than the original listing conveyed. |
| Charbonneau-Lefort, Afeyan and Fejer, DOI [10.1364/JOSAB.25.000463](https://doi.org/10.1364/JOSAB.25.000463) | abstract only | Frequency-domain WKB design formulas for chirped OPA; exact coefficients and edge corrections not independently audited here. |
| Phillips et al., DOI [10.1364/JOSAB.30.001551](https://doi.org/10.1364/JOSAB.30.001551) | abstract only | Apodization paper exists; coauthor is **L. Gallmann**, not L. Lin. |
| Kobzar et al., DOI [10.1016/j.jmr.2004.06.017](https://doi.org/10.1016/j.jmr.2004.06.017) and DOI [10.1016/j.jmr.2008.05.023](https://doi.org/10.1016/j.jmr.2008.05.023) | abstract only, both | Numerical optimal-control studies constrain amplitude and RF power separately; do not interpret their numerical limits as a global impossibility theorem. |
| Li and Khaneja, [arXiv:quant-ph/0510012](https://arxiv.org/abs/quant-ph/0510012), DOI 10.1103/PhysRevA.73.030302 | full text | Ensemble control is established; admissible controls differ from binary QPM. |
| Song and Shin, DOI [10.1364/JOSAA.2.001905](https://doi.org/10.1364/JOSAA.2.001905) | abstract only | The previously vague lead is located: inverse scattering of corrugated filters. |
| Feced, Zervas and Muriel, DOI [10.1109/3.777209](https://doi.org/10.1109/3.777209) | abstract only | Located institutional abstract: exact differential layer-peeling synthesis of fiber Bragg gratings; no new conversion theorem attributed to it. |
| Feced and Zervas, DOI [10.1364/JOSAA.17.001573](https://doi.org/10.1364/JOSAA.17.001573) | abstract only | Omitted close precedent: inverse synthesis of **codirectional** coupling spectra. |
| Brenne and Skaar, DOI [10.1109/JLT.2003.808648](https://doi.org/10.1109/JLT.2003.808648) | abstract only | Necessary/sufficient realizability constraints and inverse synthesis are already claimed for a discrete coupler model. Full text needed before claiming novelty for an unconstrained reachable set. |
| Chern and Wang, DOI [10.1364/JOSAA.19.000772](https://doi.org/10.1364/JOSAA.19.000772) | full text | Omitted binary-grating precedent: inverse scattering plus a transfer-matrix genetic optimization, including corrections to the effective-envelope approximation. An achieved flat-band design is not a certified global bandwidth frontier. |
| Phillips, Langrock and Fejer, DOI [10.1364/OE.21.010139](https://doi.org/10.1364/OE.21.010139) | full text | Omitted close precedent: convex QPM design under stated linear/first-order-QPM approximations, including fabrication constraints. Does not establish the exact high-conversion binary frontier. |
| Li, Ruths and Glaser, DOI [10.1038/s41467-017-00441-7](https://doi.org/10.1038/s41467-017-00441-7) | full text | Main article supplies analytical minimum-energy and bounded-amplitude bang–bang designs through a spin–spring projection with an additional feasibility condition. The supplement's control optimization remains to be audited; do not equate it with a worst-band-error frontier under minimum-domain constraints. |

The historical Zakharov–Shabat paper was located in the publisher's [JETP scan](https://jetp.ras.ru/cgi-bin/dn/e_034_01_0062.pdf), **abstract only**; no DOI/arXiv identifier was found. Use the identified Magland theorem above for the active mathematical statement rather than inventing an identifier.

Searches: `"sum rule" "frequency conversion" "inverse scattering"`; `"Zakharov" "minimum" "binary" pulse`; `"Song" "Shin" inverse scattering optical filters`; `"Design of grating-assisted codirectional couplers"`; `"Apodization of chirped quasi-phasematching" Phillips pdf`; `"Efficient, Broadband and Robust Frequency Conversion by Fully Nonlinear"`; exact-title searches for each source. The review document records the wider search log. No proof of the exact constrained frontier was found in these searches; this is not a claim of exhaustive absence.

## Sharpest statement of the gap

For a specified raw-binary or continuous-envelope control class, fixed $\kappa L$, $\ell_{\min}/L$ and error tolerance, find a rigorous finite-length bandwidth frontier or a certified gap to it. Separate this from the known trace budget and existing inverse synthesis/convex approximations. Independently, test whether a log-area bound in **input pump flux** survives fully depleted, lossless SFG with specified input phases and signal-to-pump ratio. The pulsed and unequal-loss variants remain exploratory and require a precise operator/resource definition before a claim is registered.

## Conjectures

No claim registered. The original depletion conjecture remains unproved; this audit did not integrate depleted equations. The original finite-length Landau–Zener rate and unequal-loss monotonicity are withdrawn as unsupported premises, with the text retained below.

## Oracle

Use exact transfer matrices for undepleted piecewise-constant real $g$ and direct three-wave integration for depletion, with Manley–Rowe and mismatch-window checks. The registered box run checks only normalization. No new solver has been implemented. Include binary-domain convergence, effective-versus-raw coupling calibration and spectral tails before comparing a design with a trace bound.

## Lab test

Compare calibrated conversion spectra of equal-length poled devices using the same photon-flux efficiency and raw/effective coupling convention. The most useful new prediction would be the finite-domain penalty, followed by an independently tested depletion correction.

## Scores and remaining work

Novelty **3/5**: a constrained high-conversion frontier has clear NMR and inverse-scattering precedents but was not found in the exact binary class. Impact **4/5**: a tight length–bandwidth–efficiency rule could guide several QPM platforms. These are reviewer judgments on the narrowed problem, not computed results. Full-text coupler and pulse-control comparisons, and depleted/pulsed/loss premise checks, remain follow-up work.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive.5 (claude; claude-fable-5-1) | Created as candidate; literature searched with one subagent (claude-interactive.5.1); scratch numerical checks of the anchor identity, of Landau–Zener saturation and of the bound-state term's normalization | Searches listed above; scratch checks in the session's scratchpad, not registered runs |
| 2026-10-13 | gpt-b (gpt; gpt-6-astra) | candidate → audited; literature partial → partial; scope/citations corrected, gpt audit recorded; priority unchanged | Magland theorem and registered trace check; corrected gauge/control class; both reviews identify constrained frontier and depletion as open. [Review](../docs/review-2026-10-13-gpt-b-frequency-conversion-novelty.md) |

## Superseded proposer draft (preserved)

The following text is retained to keep failures and earlier hypotheses. Its source-access labels describe the proposer, not this reviewer. Its unregistered scratch numbers and superseded assertions are **not current evidence**. The active statements and source table above control this card.

<details>
<summary>Original draft before the GPT novelty audit</summary>

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

</details>
