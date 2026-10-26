---
id: P-20261016-claude-interactive-02
title: "Long-wavelength photon budget of fibre supercontinuum beyond a cutoff, and the headroom of input spectral shaping"
status: candidate
priority: 2
literature_state: partial
novelty_confidence: medium
target_quantity: "A loss-aware ceiling on upstream-normalized photon and energy yield beyond a long-wavelength cutoff over a finite length interval, closed by a controlled bound on complementary reach or propagated peak power, and its headroom under passive spectral shaping of a fixed laser spectrum."
model: "Photon-number-conserving generalized NLSE with beta(omega), gamma(omega), loss alpha(omega) (including a multiphonon edge), causal Raman response, self-steepening; one or two zero-dispersion frequencies; input = laser field after a passive spectral pulse shaper; output photons counted beyond lambda_c."
oracle_ready: available
last_audited: 2026-10-16
audited_by: [claude, gpt]
proposed_by: claude-interactive
claims:
- C-20261016-claude-interactive.6-01
- C-20261016-claude-interactive.6-02
results:
- R-0003
- R-0004
- R-0005
---

## Target quantity

**Current scope, gpt-b (gpt; gpt-6-astra), 2026-10-16.** The GPT review below supersedes conflicting definitions, sketches and negative literature statements preserved in this card. Use upstream laser energy/photon number as the denominator, record mask throughput, and restrict length to a stated finite interval. The nested reference is $\mathcal S_{\le E}$; attenuated passive masks do not belong to an exact-energy $\mathcal S_E$. Physical photon density is the energy spectrum divided by $\hbar\omega$, not unweighted NLSE mass. Input spectral support is not an output support bound. A relative headroom requires a nonzero TL yield under the same constraints.

**The PI's question (2026-10-16).** How much light can be generated in the long-wavelength infrared part of a supercontinuum? How much room do spectral-amplitude and spectral-phase modulation of the input give to increase it?

**Definitions.**
- $\eta_{\rm red}(\lambda_c,L)$ is the fraction of input photons found at $\lambda>\lambda_c$ at the output. The energy fraction is at most $\eta_{\rm red}\,\omega_c/\omega_p$ (quantum defect).
- Input classes $\mathcal S_\phi\subset\mathcal S_{A\phi}$ and reference $\mathcal S_E$, as in P-20261016-claude-interactive-03.
- Targets:
  - $\eta_{\rm red}^{\max}(\mathcal S)$, maximized over the class and $L$;
  - the optimal length $L^*$ against the loss edge;
  - the headroom $H_{\mathcal S}$ over the transform-limited launch.

**Answer form.**
- A closed-form ceiling in a few named quantities:
  - laser energy and spectral width (through the transform-limited peak $\|q_{\rm TL}\|_\infty$);
  - $T_R$ or the full Raman response;
  - $\gamma(\omega)^4/|\beta_2(\omega)|^3$ along the shift;
  - the loss edge $\alpha(\omega)$;
  - $L$.
- Its tightness against adjoint-optimized launches in the GNLSE.

## Signal of hidden simplicity

The following are orchestrator sketches, 2026-10-16. They are not checked and are not claims. Item 2 builds on a remark by the literature subagent.

> **Status of the sketches after round 5 (2026-10-16/17; see "Claims and current results" below).**
> - **Sketch 1 holds in the photon-conserving model.**
>   - Photon number is conserved, and the photon mean frequency falls at every plane. The Raman dissipation identity holds to $2.9\times10^{-5}$ (run `2026-10-16-claude-interactive.6-h1-conservation`).
>   - Only the photon-conserving form may be used. In the same run, a naive $\gamma(\omega)$ prefactor loses 11.8% of the photons in 1 m, and dropping the shock term adds 17.6%.
> - **Sketch 2 needs no peak-power bound.**
>   - For any field, $|dE/dz|\le\kappa_UE^2$ with $\kappa_U=n_2f_Rh_R'(0^+)/(2cA_{\rm eff})$, so a lossless fibre keeps at least $1/(1+\kappa_UE_{\rm in}L)$ of the energy (C-20261016-claude-interactive.6-02).
>   - gpt-d confirms the identity, the passive-response sign, the bound and the retention theorem.
>   - It constrains anything only when $\kappa_UE_{\rm in}L\lesssim1$: about 0.25 m for 4.25 nJ in SMF-28.
> - **Sketch 3's "shaping cannot raise the reach" is refuted as stated.**
>   - After fission, the leading soliton exceeds the input-content cap $2/N$ by 7–53% in six transform-limited SMF-28 launches (run `2026-10-16-claude-interactive.6-h2-fission`). Raman transfer between solitons is published (Kormokar et al. 2023). A reach ceiling must take the post-fission photon number $N_1$ as input.
>   - For the rate, use the full-response sech-overlap law. It is within 1% for $T_s\ge50$ fs, 3–6% high after fission, and 13% high for the shortest post-fission soliton. Gordon's linear-$T_R$ rate is 2–25% low (runs `2026-10-16-claude-interactive.6-h2-fundamental`, `2026-10-16-claude-interactive.6-h2-fission`).
> - **Sketch 4.** The reduced-ODE invariant $N^4=N_0^4-\Lambda(\omega)$ survives. The closed-form optimal length does not (C-20261016-claude-interactive.6-01; below).

1. **Photons are conserved; Raman only lowers the mean.** In the photon-number-conserving GNLSE, Raman makes the mean photon frequency decrease monotonically (Blow & Wood 1989; Bonetti et al. 2020; Huang et al. 2026). Loss removes photons.
2. **The rate of the mean shift is bounded by peak power.** Parseval on the Raman term gives $|d\bar\omega/dz|\le\gamma f_R\,P_{\rm pk}(z)\,\sup_\Omega\Omega\,\mathrm{Im}\,\tilde h_R(\Omega)$. With the blue edge $\omega_{\max}$ bounded, a one-sided Markov argument then gives
   $$\eta_{\rm red}\le\frac{(\omega_{\max}-\omega_p)+\Delta\bar\omega(L)}{\omega_{\max}-\omega_c}.$$
   - **The missing ingredient** is an a-priori bound on $P_{\rm pk}(z)$. For the pure NLSE it follows from the photon number, the Hamiltonian and Gagliardo–Nirenberg. With Raman and higher-order dispersion it is open.
3. **The soliton channel is capped by the input's soliton content.**
   - Photons beyond $\lambda_c$ arrive mainly in Raman solitons; red dispersive waves beyond a second zero-dispersion wavelength are the other route.
   - **Reach of one soliton.** For a fundamental soliton of photon number $N_s$, the adiabatic Gordon rate is $d\omega/dz=-\tfrac{T_R}{30}\gamma(\omega)^4(\hbar\omega N_s)^4/|\beta_2(\omega)|^3$. This was derived by the literature subagent and should be checked; with $N_s$ decaying through loss, it gives a reach $R(N_s,L)$.
   - **Shaping cannot raise the reach.** Inverse scattering bounds every soliton in any passively shaped input by the transform-limited peak (P-20261016-claude-interactive-03, sketch 1). The largest reach is therefore capped by a quantity of the laser spectrum alone.
   - **The ceiling.** It is the number of photons in solitons whose reach exceeds $\omega_p-\omega_c$, plus the red-dispersive-wave channel.
4. **The loss edge gives an optimal length.** Against an exponential multiphonon edge, the reach gained per metre falls while absorption grows. This suggests a closed-form $L^*$ and a closed-form ceiling at $L^*$.

## Merged cards (PI decision 2026-10-16)

This card now carries **P-20261012-claude-interactive.4-04, the Raman-budget bound on blue-band supercontinuum** (claude-interactive.4). Its file stays in PR #41 as the record. The GPT audit (gpt-a, PR #43) narrowed it, and its missing piece is this card's central object, a bound on the red reach.

- **The moment balance.** In a lossless photon-conserving model, take $\eta_b$ the blue fraction beyond $\Omega_b$, $-R$ the mean offset of the complement, and $-D\le0$ the total mean shift. Then $\eta_b\le(R-D)/(\Omega_b+R)$. The inequality is elementary, and it becomes predictive only with a proven $R\le R_{\max}(L,\mathcal A)$. The mirror statement bounds the red fraction beyond $\lambda_c$.
- **Monotone mean frequency.** In the standard photon-conserving shock form with passive Raman, $dE/dz\le0$ at fixed photon number, so the photon mean frequency is non-increasing. This follows Bonetti et al., JOSA B 37, 445 (2020), DOI 10.1364/JOSAB.377891 (**full text**, gpt-a). Without the shock term, photon number is not conserved. Frequency-selective loss can raise the surviving mean, so the lost moment must enter the budget.
- **The bare Gordon reach is not an upper bound.**
  - Trapped radiation accelerates the red shift beyond the bare Raman rate (Gorbach & Skryabin, PRA 76, 053803 (2007), §VI, **full text**, gpt-a).
  - Raman transfer between pulses enhances the leading soliton beyond the inverse-scattering partition (Kormokar, Shamim & Rochette, JOSA B (2023), DOI 10.1364/JOSAB.478975, arXiv:2301.02945, **full text**, gpt-a).
- **Reduced drift law.** Adiabatic fundamental-soliton drift with third-order dispersion, shock and loss: Kormokar, Shamim & Rochette, JOSA B (2021), DOI 10.1364/JOSAB.409240 (**full text**, gpt-a). It omits dispersive radiation.

**Consequences for this card.**
- Sketch 3's reach ceiling must include trapped-radiation backaction and the Raman transfer between pulses, or be stated for a class where both are bounded.
- The first deliverable is to establish or refute a usable $R_{\max}$.

**Added GPT note, 2026-10-16 (gpt-b; gpt-6-astra; gpt).** The merged qualifications remain correct and are now supported by this reviewer's full-text inspection of Bonetti, Gorbach–Skryabin and both Kormokar papers (identifiers/access below). Passivity is required for the Raman sign; the rate bound and surviving-mean loss term are corrected below. The original sketch's statement that shaping cannot raise reach is superseded by the propagated-versus-input distinction and the Rosenberg prechirp experiment.

## Literature state

### GPT-family review, 2026-10-16 — current assessment

Reviewer: **gpt-b; model gpt-6-astra; family gpt**. Verdict: **open, narrowed**. Literature state changes **open → partial**. Priority is unchanged. Novelty **3/5**: a uniform reach estimate would close an established moment method rather than introduce a new moment inequality. Impact **3/5**: a reliable cutoff-yield/loss rule would guide specialist fibre length and source choices. Novelty confidence remains **medium**.

**Premise check.** The merged inequality $\eta_b\le(R-D)/(\Omega_b+R)$ is correct, conditional on a known complementary mean or upper reach bound. The red mirror requires an actual finite upper frequency bound, not the input band or numerical window. In the lossless constant-coefficient photon-conserving shock model, with $\widehat h(\Omega)=\int h(t)e^{i\Omega t}dt$, the sign condition is **passivity** $\Omega\operatorname{Im}\widehat h_R\ge0$; causality alone is insufficient. Then $E'\le0$, $N'=0$, and the photon mean $E/(\hbar N)$ decreases. The peak-rate bound contains an additional factor $\bar\omega/\omega_0$ for a power envelope. With attenuation,

$$\bar\omega'=-Q_R/(\hbar N)-\operatorname{Cov}_N(\omega,\alpha),$$

so preferential red loss can raise the surviving mean. The moment, sign, photon cancellation and loss examples are checked in run `2026-10-16-gpt-b-sclit-premises`, without propagation simulations. The exact quantum-defect factor is $\omega_c/\bar\omega_{\rm laser}$, with $\omega_p$ only a narrowband replacement.

The Gordon coefficient in sketch 3 is correct for an isolated adiabatic sech soliton with short Raman response. It is not an upper bound once trapped radiation, red DWs or Raman transfer change its energy. Input ZS eigenvalues do not bound the propagated fission product. A loss edge does not alone guarantee a unique interior optimal length.

**Sources newly read, upgraded or correcting the original review:**
- Bonetti et al., DOI **10.1364/JOSAB.377891**, **full text**, Eqs. 4–14: the conventional shock equation is photon-conserving in its special linear nonlinear-dispersion case. General $\gamma(\omega)$ requires the symmetric weighted interaction, not an arbitrary multiplier. Linale et al., DOI **10.1109/JQE.2020.3047691**, **abstract only**, is a 2021 journal article published online in 2020; its warning is not that every standard shock model fails.
- Huang et al., arXiv:**2607.05244**, **full text**, Eqs. 17–21: its power-weighted frequency moment has a chirp term and must not be equated with the physical photon mean. Zheltikov, DOI **10.1103/PhysRevA.98.043833**, **full text**, clarifies photon/energy normalization. Vanvincq et al., DOI **10.1103/PhysRevA.84.063820**, **abstract only**, is earlier photon-conservation work for axially varying fibres.
- Kormokar et al., DOI **10.1364/JOSAB.409240**, **full text**, gives a corrected adiabatic drift model; DOI **10.1364/JOSAB.478975**, arXiv:**2301.02945**, **full text**, gives a partly calibrated analytic intersoliton-transfer correction. Gorbach & Skryabin, DOI **10.1103/PhysRevA.76.053803**, arXiv:**0707.1598**, **full text**, §VI, shows trapping backaction. These are prior limitations on a bare Gordon reach cap.
- Petersen et al., DOI **10.1364/OE.25.015336**, **full text**, results/conclusion: pre-taper-length optimization against chalcogenide bandwidth and red loss is published. Judge et al., DOI **10.1364/JOSAB.26.002064**, **abstract only**, and Bendahmane et al., DOI **10.1364/OL.38.003390**, **abstract only**, already optimize taper profiles; Pant et al., DOI **10.1364/JOSAB.27.001894**, **abstract only**, is a close fission-plus-reach model. No certified general cutoff-yield bound was located in these sources.
- Rosenberg et al., DOI **10.1364/OE.383014**, **abstract only** in the primary-source check: negative prechirp experimentally improves few-cycle SSFS and crosses an absorption band. This supersedes the qualitative assertion “shaping cannot raise the reach,” while leaving the input eigenvalue inequality intact.
- Gauthier et al., DOI **10.1038/s41598-022-19658-8**, **full text**, replaces the invalid “full text, via summary” label with direct inspection: the soliton fraction is an output fraction in an amplified source architecture. DOI **10.1364/OL.41.001756**, **abstract only**, Kulkarni DOI **10.1364/JOSAB.28.002486**, **abstract only**, and Martinez DOI **10.1364/OL.43.000296**, **abstract only**, also need their output-power denominators retained rather than interpreted as input conversion.
- Hary et al., DOI **10.1364/OL.492064**, arXiv:**2304.00829**, **full text**, and DOI **10.1038/s41598-024-84567-x**, **full text**, optimize integrated narrow channels with throughput among the controls. Wetzel et al., DOI **10.1038/s41467-018-07141-w**, **full text**, uses a programmable pulse train and amplification. These are substantive control precedents, not the same broad-cutoff passive-mask benchmark.

- Arteaga-Sierra et al., DOI **10.31349/RevMexFis.63.2.111**, **full text**, optimize integrated Raman-channel output using a genetic algorithm over carrier wavelength, peak power and duration (Eqs. 2–3). This is quantitative conversion control with variable input spectrum/energy, not a certified passive fixed-spectrum optimum.

**Status gate.** Both families have reviewed the literature, but Claude assent to the narrowed, loss-aware scope has not yet been recorded. Keep **candidate**, add `gpt` to `audited_by`, and do not infer a simulation verification. [second-family review](../docs/review-2026-10-16-gpt-b-supercontinuum-literature.md) contains the complete ledger, access limitations and derivation details.

**Additional searches:** “photon conserving GNLSE Raman mean frequency energy loss Bonetti”; “Raman spectral moment passive response monotonic frequency”; “mid infrared chalcogenide supercontinuum optimal length loss edge taper”; “fluoride supercontinuum conversion efficiency beyond cutoff”; “negative prechirp soliton self frequency shift”; “inverse design tapered fiber soliton self frequency shift”; “supercontinuum integrated energy cutoff bound”. No uniform closure of the reach/peak bound including the stated transfer and loss mechanisms was found in this search. The original broad negative statements below are superseded where they imply no optimization or reach theory exists.

### Round-5 additions (2026-10-16/17)

- Kormokar, Shamim & Rochette 2023, DOI 10.1364/JOSAB.478975, arXiv:2301.02945: **full text** (claude-interactive.6). Energy transfer during fission, with an $N=5.57$ experiment above $2/N$.
- Boilard, Vallée & Bernier 2021, arXiv:2109.13366: **full text**. Fluoride Sellmeier fits.
- Gauthier et al. 2022, DOI 10.1038/s41598-022-19658-8: **full text**. InF₃ 7.5/125 fibre at NA 0.3; 1 dB/m at 5.4 µm for InF₃ and at 4.2 µm for ZrF₄.

### Original Claude review — retained; conflicting statements superseded above

Claude-family review, 2026-10-16, by a research subagent of claude-interactive (about 25 minutes of web search, with DOIs checked at doi.org). Notes are in the orchestrator's scratchpad.

**Mechanisms of the red edge:**
- Mitschke & Mollenauer, Opt. Lett. 11, 659 (1986), DOI 10.1364/OL.11.000659. **Abstract only.**
- Gordon, Opt. Lett. 11, 662 (1986), DOI 10.1364/OL.11.000662. **Abstract only.**
- Santhanam & Agrawal, Opt. Commun. 222, 413 (2003), DOI 10.1016/S0030-4018(03)01561-X. **Abstract only.** Shift depends on width and chirp; saturates under strong broadening.
- Zheltikov, PRE 75, 037603 (2007), DOI 10.1103/PhysRevE.75.037603. **Abstract only.** Adiabatic SSFS with higher-order dispersion, mode area and loss, and the length scales at which each limit takes over.
- Arteaga-Sierra, Antikainen & Agrawal, arXiv:1707.06258. **Partial full text.** The dispersion of $\gamma$ can enhance or suppress the shift.
- Skryabin, Luan, Knight & Russell, Science 301, 1705 (2003), DOI 10.1126/science.1088516. **Abstract only.** Cancellation of the shift at a second zero-dispersion wavelength by red Cherenkov recoil.
- Biancalana, Skryabin & Yulin, PRE 70, 016615 (2004), DOI 10.1103/PhysRevE.70.016615. **Abstract only.**
- Frosz, Falk & Bang, Opt. Express 13, 6181 (2005), DOI 10.1364/OPEX.13.006181. **Abstract only.**
- Xia et al., Opt. Lett. 31, 2553 (2006), DOI 10.1364/OL.31.002553. **Abstract only.** The ZBLAN edge is set by material loss.
- Xia et al., Opt. Express 15, 865 (2007), DOI 10.1364/OE.15.000865. **Abstract only.** The edge is set "primarily by the peak pump power".

**Reach models and trapping:**
- Pant, Judge, Magi, Kuhlmey, de Sterke & Eggleton, JOSA B 27, 1894 (2010), DOI 10.1364/JOSAB.27.001894. **Abstract only.** Fission plus Gordon's law predicts the final soliton wavelength.
- Judge et al., JOSA B 26, 2064 (2009), DOI 10.1364/JOSAB.26.002064. **Abstract only.** An optimal degree of tapering exists.
- Bendahmane et al., Opt. Lett. 38, 3390 (2013), DOI 10.1364/OL.38.003390. **Abstract only.** Inverse design of taper profiles.
- Gorbach & Skryabin, Nat. Photon. 1, 653 (2007), DOI 10.1038/nphoton.2007.202. **Abstract only.**
- Gorbach & Skryabin, PRA 76, 053803 (2007), DOI 10.1103/PhysRevA.76.053803. **Abstract plus summary.** Trapped radiation accelerates the red shift; group-velocity matching links the edges.
- Skryabin & Gorbach, Rev. Mod. Phys. 82, 1287 (2010). **Partial full text.**
- Dudley, Genty & Coen, Rev. Mod. Phys. 78, 1135 (2006). Fission widths and powers. **Not re-read.**

**Records and reported fractions beyond a cutoff:**
- Gauthier et al., Sci. Rep. 12, 15898 (2022), DOI 10.1038/s41598-022-19658-8. **Full text, via summary.** A 4.8 µm soliton carries 7.5% of output power in InF₃.
- Gauthier et al., Opt. Lett. 41, 1756 (2016), DOI 10.1364/OL.41.001756. **Abstract only.** More than 82% beyond 3 µm.
- Kulkarni et al., JOSA B 28, 2486 (2011), DOI 10.1364/JOSAB.28.002486. **Abstract only.** About 27% beyond 3.8 µm in ZBLAN.
- Martinez et al., Opt. Lett. 43, 296 (2018), DOI 10.1364/OL.43.000296. **Abstract only.** About 17% beyond 7.5 µm.
- Tang et al., Optica 3, 948 (2016), DOI 10.1364/OPTICA.3.000948. **Abstract only.** Solitons tunable over 2–4.3 µm.
- Chen et al., Opt. Lett. 47, 285 (2022), DOI 10.1364/OL.445499. **Abstract only.** Hollow-core fibre efficiency falls from 46% to 8% as the soliton is tuned from 1080 to 1600 nm.
- Petersen et al., Nat. Photon. 8, 830 (2014), DOI 10.1038/nphoton.2014.213. **Not accessed.** Spectrum 1.4–13.3 µm.
- Petersen et al., Opt. Express 25, 15336 (2017). **Abstract only.** A bandwidth–power trade-off.

**Shaping:**
- Efimov et al., Opt. Lett. 29, 271 (2004). **Abstract only.**
- Hary et al., Opt. Lett. 48, 4512 (2023). **Abstract only.**
- Hary et al., Sci. Rep. 15, 377 (2025), DOI 10.1038/s41598-024-84567-x. **Full text.** Gains of 2–10× at the red edge in 7 nm channels, against an unshaped launch.
- Wetzel et al., Nat. Commun. 9, 4884 (2018), DOI 10.1038/s41467-018-07141-w. **Full text.** Up to 7× against the best single pulse at equal power; narrow-band spectral density, limited by loss above 2 µm.
- Kormokar, Nayan & Rochette, Opt. Lett. (2025), DOI 10.1364/OL.551176. **Abstract only.** An optimal pre-chirp for reach and efficiency inside a Tm amplifier.
- Solli, Ropers & Jalali, PRL 101, 233902 (2008). **Abstract only.** A weak seed stimulates coherent red-shifted continuum.

**Conservation structure:**
- Blow & Wood, IEEE JQE 25, 2665 (1989), DOI 10.1109/3.40655. **Abstract only.**
- Bonetti et al., JOSA B 37, 445 (2020), DOI 10.1364/JOSAB.377891. **Abstract only.**
- Linale, Fierens & Grosz, IEEE JQE (2020), DOI 10.1109/JQE.2020.3047691. **Abstract only.** The standard GNLSE violates photon number for short solitons.
- Huang et al., arXiv:2607.05244 (2026). **Abstract only.** A universal monotone red shift in the photon-conserving GNLSE.
- Kibler et al., PRE 84, 066605 (2011), and Michel, Kibler & Picozzi, PRA 83, 023806 (2011). **Abstract only.** Kinetic theory of the red edge for incoherent supercontinuum.

**Searched:**
- quantum-defect and photon-conversion limits;
- upper bounds on the Raman shift;
- Lagrange-duality bounds;
- "energy beyond cutoff" bounds;
- red-edge formulas;
- SSFS with loss;
- optimal fibre length;
- shaping of the mid-IR supercontinuum.

None found a bound on the photon or energy fraction beyond $\lambda_c$, a closed-form $L^*$ against a loss edge, or headroom of integrated energy beyond a cutoff against a transform-limited launch at equal energy.

## Sharpest statement of the gap

**Current gap (gpt-b, 2026-10-16).** Close the conditional moment bound with a loss-aware, a-priori bound on complementary red reach or propagated peak power for a stated launch/fibre regime. Include or quantitatively exclude trapped radiation, Raman energy transfer, red DWs and frequency-selective loss. Derive an upstream-normalized broad-cutoff yield and its finite-length passive-mask headroom with controlled error. Adiabatic reach models, moment algebra, taper/length optimization and chirp gains are prior work. A loss edge alone need not give an interior or unique optimal length.

**Historical gap statement — retained, superseded where it conflicts with the current gap:**

**Known:**
- the mechanisms of the red edge;
- reduced reach models;
- fission energy partition (about $2/N$ in the reddest soliton);
- the monotone red shift in photon-conserving models;
- record spectra, with sparse and inconsistently defined fractions beyond a cutoff;
- shaping gains in narrow-band density against weak baselines.

**Not found:**
- a ceiling on $\eta_{\rm red}(\lambda_c)$ in laser, fibre and length parameters;
- a closed-form optimal length against a loss edge;
- a peak-power a-priori bound that would close the Raman-rate argument of sketch 2;
- the headroom of phase-only and amplitude-and-phase shaping for the integrated energy beyond $\lambda_c$.

## Claims and current results

| Claim | Status | Current reading |
|---|---|---|
| C-20261016-claude-interactive.6-01, loss-edge photon budget of a Raman soliton | refuted (gpt-d, `claims/notes/audit-2026-10-16-gpt-d-C-20261016-claude-interactive.6-01.md`) | **What survives.** The reduced Gordon-ODE invariant; its rate-error exponent is 2.0009 against the predicted 2. **What fails.** The closed-form optimal length, inside the stated regime: 201.7 m predicted against 151 m simulated (run `2026-10-16-gpt-d-cutoff-q03`). The terminal quarter-power exponent is 0.2493 in the ODE and 0.300 in the GNLSE, without a certified terminal asymptote. The proposer's own frozen ZrF₄ tests passed (run `2026-10-16-claude-interactive.6-h3-edge`). **Assumed, not sourced:** the ZrF₄ $n_2$, the edge slope and the fluoride Raman stand-in. |
| C-20261016-claude-interactive.6-02, universal Raman rate bound | refuted as written (gpt-d, `claims/notes/audit-2026-10-16-gpt-d-C-20261016-claude-interactive.6-02.md`) | **What passes.** The energy identity, its coefficient, the passive-response sign, the rate bound and the retention theorem; adjoint optimisation found no violation. **What fails.** The claim's separate long-pulse tightness law: the measured inverse-width exponent is 3.00158, not 2 (run `2026-10-16-gpt-d-c02-rate40`). Keep the bound as an elementary model result. |

**Answer to the PI's question so far.**
- When one Raman soliton carries the light past $\lambda_c$, the budget is set by its post-fission photon number. The reduced invariant then fixes how many of those photons survive the loss edge.
- Simple phase shaping found at most about 9%, in a local search (run `2026-10-16-claude-interactive.6-h4-shaping`):
  - 1.0089× and 1.0075× where the transform-limited launch already reaches $\lambda_c$;
  - 1.044× and up to 1.094× at the reach margin.
  - GDD never helped, TOD gave at most 1.04×, and passive masks did no better than phase-only.
- The universal rate bound is loose by about 4×: the rate reached at most 0.225 of it.

## Conjectures

**Review qualification (gpt-b, 2026-10-16):** the unregistered conjecture below is retained as a refutation target, not endorsed evidence; use the corrected launch classes, denominators and premise limitations above.

None registered. Refutable first conjecture: for a laser whose transform-limited launch already reaches $\lambda_c$, the adjoint-optimized phase-only or passive mask raises $\eta_{\rm red}$ by less than the factor $2N/(2N-1)$ on the reddest soliton's energy (sketch 3), times a reach factor below 1.5, in silica and fluoride fibres with $N=2$–10. Larger optimized gains refute it. Their mechanism, whether Raman collisions, trapped-radiation acceleration or red dispersive waves, names the missing term.

**Outcome after round 5.** Restate the conjecture in post-fission terms. It is not refuted, but the test is weak: the local headroom numbers above come from short local searches and are not a shaping ceiling (gpt-d). Discuss negative-prechirp enhancement (Rosenberg et al., DOI 10.1364/OE.383014) separately, in the few-cycle fission and absorption regime, apart from the longer-pulse lossless tests.

## Oracle

**Available.**
- FastDifferentiableMMNLO provides the GNLSE with $\beta(\omega)$, Raman, self-steepening and loss, plus adjoint gradients of $\eta_{\rm red}$ with respect to input masks.
- Caveats:
  - check the solver's photon-number conservation against the photon-conserving form (Linale et al.);
  - wavelength-dependent $\gamma(\omega)$ and mode area need the solver's $\omega$-dependent options (see `docs/SOLVER.md`);
  - material loss tables for fluoride and chalcogenide fibres must be supplied.
- The reach model (sketch 3) and the Zakharov–Shabat content are short numpy codes.

**Caveats found in round 5** (runs `2026-10-16-claude-interactive.6-h1-conservation`, `2026-10-16-claude-interactive.6-h2-fission`).
- Use only the photon-conserving form.
- The solver's blue-edge window removes about $3\times10^{-4}$ of the photons per metre in the H1 case.
- RK4IP conserves photon number only to third order in $dz$.
- At $dt=3$ fs, 100 fs launches with $N\ge4$ in SMF-28 are aliased: $f_1$ for $N=6$ moved from 0.370 to 0.475 at 1.5 fs. The dissipation identity is a cheap aliasing monitor.
- State the spectral-support and positive-frequency assumptions, and the model calibration, with every physical prediction (gpt-d).

## Lab test

In a fluoride or silica SSFS or supercontinuum setup with a programmable pulse shaper, measure the power beyond a long-pass filter at $\lambda_c$ with a calibrated detector:
- against fibre length (cutback);
- against masks: chirp, then adaptive.

Compare with the ceiling, the predicted $L^*$ and the predicted headroom. The fair baseline is the transform-limited launch at the same energy.

## Risks and must-reads

- The bound may be loose where red dispersive waves or trapped radiation carry many photons. Those channels need their own terms.
- The photon-conserving form matters for short solitons. A standard-GNLSE oracle could fake a violation.
- Fibre parameters at long wavelengths (loss, $\gamma$, dispersion) are uncertain. Ceilings should be stated as functions of them.
- **Must-reads:**
  - Pant et al. 2010;
  - Huang et al. 2026 and Bonetti et al. 2020;
  - Skryabin & Gorbach 2010 with Gorbach & Skryabin 2007;
  - Zheltikov 2007;
  - Wetzel et al. 2018;
  - Gauthier et al. 2016 and 2022.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-16 | claude-interactive (claude; claude-opus-5-5) | Proposed as candidate on the PI's request; Claude-family literature review by a research subagent | PI request in chat, 2026-10-16; sources listed above |
| 2026-10-16 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Merged with overlapping round-4 cards (see Merged cards); scope and literature updated from the GPT audits in PRs #42–#43 | PI message in chat, 2026-10-16; `docs/review-2026-10-13-gpt-a-frequency-conversion-novelty.md` on branch `task/T-20261013-gpt-a-01` |
| 2026-10-16 | gpt-b (gpt; gpt-6-astra) | Second-family review: literature_state open → partial; status candidate retained pending Claude agreement on revised scope; priority unchanged; novelty_confidence medium retained; added gpt to audited_by | [second-family review](../docs/review-2026-10-16-gpt-b-supercontinuum-literature.md); run `2026-10-16-gpt-b-sclit-premises`; source ledger and follow-up tasks in report |
| 2026-10-17 | claude-interactive (claude; claude-opus-5-5) | Applied the round-5 proposed card changes (claude-interactive.6, gpt-d): claims list, status of the sketches, claims and current results, conjecture outcome, oracle caveats, literature additions. Status, priority, literature_state and novelty_confidence unchanged; the Claude-family agreement on gpt-b's revised gap (T-20261016-gpt-b-05) is still open | logs `2026-10-16_claude-interactive.6_T-20261016-claude-interactive-04.md`, `2026-10-16_gpt-d_T-20261016-claude-interactive.6-01.md`; task T-20261017-claude-interactive-01 |
| 2026-10-19 | claude-interactive.15 (claude; claude-opus-5-5), on PI instruction | Results R-0003 (Raman energy-loss ceiling and retention bound, from C-20261016-claude-interactive.6-02 as narrowed), R-0004 (exact sech loss ratio, C-20261017-gpt-d-01) and R-0005 (arctangent concentration ceiling, C-20261017-gpt-d-02) added to `results` as promising results. Status, priority, literature_state and novelty_confidence unchanged: the target quantity, a loss-aware red-yield ceiling closed by an a-priori reach or peak bound, is still open. The claims list and the current-results table of this card are stale (they miss C-20261017-gpt-d-01/-02 and the 2026-10-17 narrowing); left for T-20261019-claude-interactive.15-05 | PI decision 2026-10-19 (T-20261019-claude-interactive-07); task T-20261019-claude-interactive-08 |
