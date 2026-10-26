---
id: P-20261016-claude-interactive-03
title: "Efficiency–shift frontier of Raman-soliton conversion, and the headroom of input spectral shaping"
status: candidate
priority: 2
literature_state: partial
novelty_confidence: low
target_quantity: "A controlled outer frontier of final Raman-soliton energy fraction, frequency shift and centroid variance for a specified perturbed fibre model and passive fixed-spectrum launch class, with transfer and covariance transport quantified and headroom measured against the same transform-limited baseline."
model: "Generalized NLSE in anomalous dispersion: beta_2(omega), beta_3, gamma(omega), causal Raman response, self-steepening, loss; integrable NLSE (Zakharov-Shabat scattering) as the reference limit; input = laser field after a passive spectral pulse shaper."
oracle_ready: available
last_audited: 2026-10-16
audited_by: [claude, gpt]
proposed_by: claude-interactive
claims:
- C-20261016-claude-a-01
- C-20261016-claude-a-02
- C-20261016-claude-a-03
- C-20261016-claude-a-04
- C-20261018-pi-chatgpt-01
results:
- R-0001
- R-0002
- R-0006
---

## Target quantity

**Current scope, gpt-b (gpt; gpt-6-astra), 2026-10-16.** The GPT review below supersedes conflicting definitions, sketches and negative literature statements preserved in this card. Use upstream laser energy/photon number as the denominator, record mask throughput, and restrict length to a stated finite interval. The nested reference is $\mathcal S_{\le E}$; attenuated passive masks do not belong to an exact-energy $\mathcal S_E$. Physical photon density is the energy spectrum divided by $\hbar\omega$, not unweighted NLSE mass. Input spectral support is not an output support bound. A relative headroom requires a nonzero TL yield under the same constraints.

**The question.** How much of a laser pulse's energy can be put into one red-shifting Raman soliton, and how far can it shift in a fibre of length $L$? How much does shaping the input's spectral phase and amplitude buy over a transform-limited launch?

**Definitions.**
- $f_1$ is the energy in the leading (most red-shifted) soliton at the output, divided by the laser energy $E$.
- $\Omega_1(L)$ is its frequency shift.
- For a laser of fixed spectral amplitude $|Q(\omega)|$ there are three nested input classes:
  - $\mathcal S_\phi$, phase-only masks $Q\to Qe^{i\phi(\omega)}$;
  - $\mathcal S_{A\phi}$, passive masks $Q\to mQ$ with $|m(\omega)|\le1$;
  - $\mathcal S_E$, any input of energy $E$ supported in the laser band, a reference class.
- The frontier is $\mathcal F_{\mathcal S}=\{(f_1,\Omega_1(L))\}$, attainable over $\mathcal S$ and $L$.
- The headroom is $H_{\mathcal S}=\sup_{\mathcal S}f_1/f_1^{\rm TL}$, at fixed shift or fixed $L$.

**Answer form.**
- Closed-form outer bounds on $\mathcal F_{\mathcal S}$, in terms of:
  - the soliton number $N$ of the transform-limited launch;
  - the Raman time $T_R$ (or the full response);
  - $\beta_2(\omega)$ and $\gamma(\omega)$ along the shift;
  - loss.
- The headroom $H_{\mathcal S}(N)$, rigorous in the integrable limit and asymptotic, with a stated error, for the GNLSE.
- The gap to adjoint-optimized masks.

## Signal of hidden simplicity

The following are the orchestrator's derivation sketches, 2026-10-16. They have not been checked by another agent and are not claims.

> **Status of the sketches after round 5 (2026-10-16/17; see "Claims and current results" below).**
> - **Sketch 1 is proved but not attained.**
>   - Proved: $\mathrm{Im}\,\zeta\le\|q\|_\infty$, and the transform-limited extremality of $\|q\|_\infty$ and $\int|q|^4$ under passive masks (C-20261016-claude-a-01). Both are published in closely related form (gpt-b's review, PR #46).
>   - In every test the transform-limited launch also maximises the leading eigenvalue over $\mathcal S_\phi$ and $\mathcal S_{A\phi}$: 100 optimisations and 1188 random masks, with a largest excess of $10^{-15}$. So $H_{\mathcal S_{A\phi}}\le2N/(2N-1)$ is proved, and the value is 1 numerically.
>   - The semiclassical (WKB) eigenvalue is not an upper bound.
> - **"What may escape the bound" is Raman transfer**, quantified by C-20261016-claude-a-02 and narrowed by gpt-c's audit.
>   - The excess over the inverse-scattering share is linear in $T_R/T_0$ for long pulses.
>   - It peaks where $N^2\tau_1/T_0\approx1$ (for silica $T_0^*\approx21$ fs$\,N^{1.62}$), with a peak share of about $1.29/\sqrt N$, above $2/N$ for $N\ge3$.
>   - So the efficiency side of the frontier at fixed $L$ is set by the launch duration relative to the Raman gain-peak time, not by the input soliton content.
>   - The energy at that share-optimal point is **not** an energy maximum. At fixed $N$, shorter launches give more leading-soliton energy at a lower share.

1. **Inverse scattering bounds the leading soliton by the peak amplitude.**
   - For the focusing Zakharov–Shabat (ZS) problem $\psi_1'=-i\zeta\psi_1+q\psi_2$, $\psi_2'=i\zeta\psi_2-\bar q\psi_1$, integrate $\tfrac{d}{dt}(|\psi_1|^2-|\psi_2|^2)$ over a bound state. This gives
     $$\mathrm{Im}\,\zeta\int(|\psi_1|^2+|\psi_2|^2)=-2\,\mathrm{Re}\int q\bar\psi_1\psi_2,$$
     so $\mathrm{Im}\,\zeta\le\|q\|_\infty$.
   - For fixed $|Q(\omega)|$, $\|q\|_\infty\le\frac1{2\pi}\int|Q|\,d\omega=\|q_{\rm TL}\|_\infty$. Passive amplitude masks only lower the right-hand side.
   - Hence every soliton contained in any input from $\mathcal S_{A\phi}$ has energy $4\,\mathrm{Im}\,\zeta\le4\|q_{\rm TL}\|_\infty$ in normalized units.
   - For a sech laser of soliton number $N$ this caps the leading-soliton fraction at $2/N$. The transform-limited launch already gives $(2N-1)/N^2$ (Satsuma–Yajima eigenvalues), so in the integrable limit $H_{\mathcal S_{A\phi}}\le 2N/(2N-1)$.
   - Gordon's rate $\propto(\text{soliton amplitude})^4$ is bounded the same way, with headroom at most $(2N/(2N-1))^4$.
   - **The leading soliton is therefore nearly unimprovable by passive shaping at large $N$**, if the integrable picture of fission holds.
   - **Numerical check** (run `2026-10-16-claude-interactive-zs-bound-check`; a scratch-level check by the proposer, not an independent verification).
     - Fourier-collocation ZS eigenvalues reproduce the Satsuma–Yajima values for sech pulses with $A=1$, 2.5 and 3.
     - For a transform-limited Gaussian of peak 3, $\mathrm{Im}\,\zeta_{\max}=2.4765$.
     - Over 40 random spectral-phase masks on that Gaussian's spectrum:
       - $\mathrm{Im}\,\zeta_{\max}/\|q\|_\infty$ never exceeded 0.861;
       - no mask exceeded the transform-limited $\mathrm{Im}\,\zeta_{\max}$;
       - $\int|q|^4$ never exceeded 0.930 of its transform-limited value.
2. **Phase shaping touches the conserved quantities through one number.** At fixed $|Q|$, the photon number, the momentum and the dispersive part of the Hamiltonian are fixed. Only the Kerr energy $\int|q|^4$ moves, and it is largest for linear spectral phase, the transform-limited pulse, because $\int|q|^4\propto\int|Q\star Q|^2\le\int(|Q|\star|Q|)^2$.
3. **Exact anchors.**
   - The chirped-sech family $A\,\mathrm{sech}^{1+iC}$ has eigenvalues $i(\sqrt{A^2-C^2/4}-\tfrac12-k)$, so chirp acts as an amplitude reduction (Chekhovskoy et al., arXiv:2003.02215, full text).
   - Chirped Gaussians lose soliton content monotonically with $|C|$ (Prilepsky, Derevyanko & Turitsyn 2007, full text).

**What may escape the bound** (these are the refutation targets):
- Raman-mediated soliton collisions, which can move energy to the redder soliton after fission;
- third-order dispersion and dispersive-wave emission during fission (the "Newton's cradle" ejection, Driben et al. 2013);
- self-steepening;
- non-adiabatic changes of $\beta_2$ and $\gamma$ with wavelength.

## Merged cards (PI decision 2026-10-16)

This card now carries **P-20261012-claude-interactive.4-02, the frequency-jitter floor of Raman self-frequency-shift conversion** (claude-interactive.4). Its file stays in PR #41 as the record. The frontier becomes **efficiency, shift and jitter**.

**The GPT audit (gpt-a, PR #43) on the jitter part:**
- The Raman drift and its quantum and thermal noise already share a published reservoir model: Drummond & Corney, JOSA B 18, 139 (2001), DOI 10.1364/JOSAB.18.000139 (**full text**).
- The frequency-coordinate covariance is explicit in Corney & Drummond, JOSA B 18, 153 (2001), DOI 10.1364/JOSAB.18.000153, preprint Eq. 3.15 (**full text**). That treatment neglects deterministic SSFS.
- A local diffusion-to-drift ratio does not bound the final variance per unit shift: covariance transport $\Phi(L,z)$ matters. The audit gives a scalar counterexample to that implication (run `2026-10-13-gpt-a-novelty-premises`).
- The target is the final centroid variance at fixed shift, length and output efficiency, for a stated class of fibres and launches.

**A finding that bears directly on sketch 1.**
- Kormokar, Shamim & Rochette, JOSA B (2023), DOI 10.1364/JOSAB.478975, arXiv:2301.02945 (**full text**, gpt-a), show that Raman transfer between pulses enhances the leading soliton beyond the Raman-independent inverse-scattering energy partition.
- Sketch 1 bounds the **input** soliton content. The propagated $f_1$ can exceed it through that transfer, which is the escape route named above. That escape is now published.
- The open questions therefore become:
  1. how large the Raman-transfer excess over the inverse-scattering bound is, as a function of $N$, $T_0$, $L$ and the Raman response;
  2. whether input shaping can increase that excess, and by how much over the transform-limited launch.
- The first conjecture below is restated in those terms.

**Added GPT note, 2026-10-16 (gpt-b; gpt-6-astra; gpt).** Kormokar et al., DOI **10.1364/JOSAB.478975**, arXiv:**2301.02945**, **full text**, Eqs. 24–25, already model the parameter dependence in merged open question 1 with an analytic, empirically calibrated correction. Narrow that question to a uniform upper bound/error estimate and shaped-input dynamics. The input peak bound also needs the mass-trace constraint; the revised formula is below. The existing covariance-transport caveat is retained.

## Literature state

### GPT-family review, 2026-10-16 — current assessment

Reviewer: **gpt-b; model gpt-6-astra; family gpt**. Verdict: **open, narrowed**. Literature state changes **open → partial**; novelty confidence changes **medium → low**. Priority is unchanged. Novelty **2/5**: the proposed elementary bounds and several transfer/noise corrections are established, leaving novelty in a controlled propagated frontier. Impact **3/5**: such a frontier could guide specialist source design and shaping choices.

**Premise check.** Sketch 1's integration gives $|\operatorname{Im}\zeta|\le\|q\|_\infty$ for a decaying-line ZS bound state. This is correct and elementary. A published amplitude-strip enclosure with the same proof exists for periodic/Floquet and Dirichlet ZS spectra; the earliest exact complex decaying-line attribution was not established. The passive-mask peak and $L^4$ extrema are also correct and are Fourier-majorant inequalities, not new optical theorems. None implies that TL maximizes the largest eigenvalue or propagated Raman yield.

The trace bound must be combined with the peak bound:

$$4\operatorname{Im}\zeta_1\le\min\{M,4\|q_{\rm TL}\|_\infty\}.$$

For $N\,\mathrm{sech}\,t$, $N>1/2$, this gives input-IST headroom

$$H\le\min\left\{\frac{N^2}{2N-1},\frac{2N}{2N-1}\right\}.$$

The fundamental sech therefore has no input-IST energy headroom; the risk paragraph's amplitude/rate allowance is superseded by the trace constraint. Reflectionlessness requires integer $N$. Temporally chirped sech/Gaussian families do not preserve spectral magnitude. Passive attenuation also does not preserve launch energy. The numerical mask/GN checks in run `2026-10-16-gpt-b-sclit-premises` are consistency checks, not proofs of an eigenvalue optimum. [second-family review](../docs/review-2026-10-16-gpt-b-supercontinuum-literature.md) gives the proofs and assumptions.

**Sources newly read, upgraded or correcting the original review:**
- Biondini, Oregero & Tovbis, DOI **10.4171/JST/432**, arXiv:**2010.04263**, **full text**, Lemma 3.8 and §6.1: explicit $|\operatorname{Im}z|\le\|q\|_\infty$ and integration proof in periodic/Dirichlet settings. Do not mislabel it a theorem specifically stated for the decaying line.
- Klaus & Shaw, DOI **10.1103/PhysRevE.65.036607**, **full text**, single-lobe imaginary spectrum; DOI **10.1137/S0036141002403067**, **abstract only**, sharp area threshold/count. The integer count needs a strict positive-imaginary eigenvalue condition at threshold, not a zero resonance. Biondini & Luo, DOI **10.1016/j.physleta.2018.06.045**, **abstract only**, is a nonzero-background extension.
- DiFranco & Miller, arXiv:**nlin/0702028**, **full text**, Theorem 1/end of §3, connects modified-NLS enclosures to semiclassical ZS shadow bounds; Bronski, DOI **10.1016/0167-2789(95)00311-8**, **abstract only**, is a located semiclassical precedent. The Deift–Venakides–Zhou notes cited there are unpublished; no journal citation is invented. Standard self-adjoint Schrödinger Lieb–Thirring inequalities do not directly supply a theorem for complex non-self-adjoint ZS.
- Lenzmann & Sok, arXiv:**1805.06294**, **full text**, Lemmas 5.1–5.2: the Fourier majorant property proves input peak/even-power extremality and, with regular connected support, affine-phase equality. Their full rearrangement theorem also alters spectral magnitude and is not the fixed-spectrum claim.
- Chekhovskoy et al., arXiv:**2003.02215**, **full text**, Eq. 17, confirms the chirped-sech eigenvalues, taking only positive imaginary values. Satsuma & Yajima DOI **10.1143/PTPS.55.284**, **abstract only** here; Prilepsky et al. DOI **10.1364/JOSAB.24.001254**, **abstract only** here. Historical Claude full-text access to Prilepsky is retained; independent original-text verification remains a loose end.
- Kormokar et al., DOI **10.1364/JOSAB.478975**, arXiv:**2301.02945**, **full text**, Eqs. 24–25: an analytic Raman-transfer conversion correction already depends on pulse parameters, length and response, with empirical calibration. The remaining question is a uniform bound or controlled error for shaped inputs, not the mere existence of such a dependence. DOI **10.1364/JOSAB.409240**, **full text**, treats corrected adiabatic drift. Driben et al., DOI **10.1103/PhysRevA.87.063808**, arXiv:**1305.5911**, **full text**, supplies a different fission-partition mechanism.
- Efimov et al., DOI **10.1364/OL.29.000271**, **abstract only**, adaptive SSFS control; Hu et al., DOI **10.1103/PhysRevLett.114.073901**, **full text**, Airy-phase control; Rosenberg et al., DOI **10.1364/OE.383014**, **abstract only**, negative-prechirp enhanced few-cycle shift. Caldarola et al., DOI **10.4279/PIP.040001**, **full text**, does show reduced reach for its heavily chirped case at equal coupled power, but is not a theorem for every phase or pulse regime.
- Hary et al., DOI **10.1364/OL.492064**, arXiv:**2304.00829**, **full text**, and DOI **10.1038/s41598-024-84567-x**, **full text**, quantify integrated channel gains while controlling throughput. Wetzel et al., DOI **10.1038/s41467-018-07141-w**, **full text**, is a programmable pulse-train precedent with a different spectrum/class.
- Drummond & Corney, DOI **10.1364/JOSAB.18.000139**, arXiv:**quant-ph/9912095**, **full text**, and Corney & Drummond, DOI **10.1364/JOSAB.18.000153**, arXiv:**quant-ph/9912096**, **full text**, contain the shared reservoir/covariance theory. The analytic instantaneous-response approximation omits deterministic SSFS. Zhou et al., DOI **10.1364/OL.40.005105**, **abstract only**, experimentally connects input intensity noise to Raman wavelength and timing jitter. A final centroid-variance bound still needs covariance transport and a specified noise model.
- Dudley et al., DOI **10.1103/RevModPhys.78.1135**, **full text**, fission sections, and Horton et al., DOI **10.1038/nphoton.2012.336**, **full text**, source description, are accessible author copies. The reported source record does not constitute an optimal conversion frontier. The complete report ledger covers the remaining original citations and their unresolved access.

- Arteaga-Sierra et al., DOI **10.31349/RevMexFis.63.2.111**, **full text**, optimize integrated Raman-channel output using a genetic algorithm over carrier wavelength, peak power and duration (Eqs. 2–3). This is quantitative conversion control with variable input spectrum/energy, not a certified passive fixed-spectrum optimum.

**Status gate.** Keep **candidate**, with both families in `audited_by`: the real Claude review below does not yet record agreement with this narrower frontier or the newly identified standard mathematics. These checks do not mark a claim sim-verified or audited.

**Additional searches:** “Zakharov Shabat eigenvalue imaginary part sup norm”; “Klaus Shaw single lobe eigenvalue bound”; “Deift Zakharov Shabat shadow bound”; “Lieb Thirring Zakharov Shabat complex potential”; “Fourier majorant even p equality phase Lenzmann Sok”; “Raman soliton conversion efficiency interpulse Raman scattering”; “adaptive pulse shaping soliton self frequency shift genetic algorithm”; “negative prechirp few cycle soliton”; “Raman soliton timing jitter frequency variance”. The fully controlled propagated frontier above was not found; the former negative claims about elementary input bounds and quantitative phase control are superseded.

### Round-5 additions (2026-10-16/17)

- **From claude-a:**
  - Kim, Lee & Lyng, arXiv:1310.4145, full text;
  - Luan et al. 2006, DOI 10.1364/OE.14.009844 (abstract only for claude-a; full text for gpt-b);
  - Kormokar et al. 2023 fit a factor of 10 and treat inverse scattering as the long-pulse asymptote.
- **From gpt-b's review of C-20261016-claude-a-02** (PR #52; access levels are gpt-b's, all full text):
  - Chi & Wen 1989, DOI 10.1364/OL.14.001216: first-order collision transfer;
  - Kormokar et al. 2023, Fig. 3, digitised;
  - Judge et al. 2009, DOI 10.1364/JOSAB.26.002064: the 18 fs Raman-overlap maximum;
  - Pant et al. 2010, DOI 10.1364/JOSAB.27.001894;
  - Domingue & Bartels 2014, DOI 10.1364/OE.22.030777;
  - Akhoundi et al. 2018, DOI 10.1364/BOE.9.002326.
- **Convention:** in the Blow–Wood response, $\tau_1=12.2$ fs is an inverse angular frequency. The oscillation period is about 77 fs.

### Round-6 addition (2026-10-18): prior art for the $L^p$ ZS eigenvalue bound

From claude-interactive.10's novelty audit of C-20261018-pi-chatgpt-01 ([report](../docs/review-2026-10-18-claude-interactive.10-zs-eigenvalue-bound-novelty.md)):
- **Real nonnegative case, sharp.** For real $q\ge0$ and $\zeta=i\eta$, the ZS problem is the zero-energy eigenproblem of the 1D Dirac operator $D_\eta-q$. Dolbeault, Gontier, Pizzichillo and Van Den Bosch, Rev. Mat. Iberoam. 40 (2024) 649, DOI 10.4171/RMI/1443, arXiv:2210.03091 (full text), Thm 1.3 at $\lambda=0$, therefore give $\int q^p\ge C_p\eta^{p-1}$ with the sharp constant and the sech extremizer (run `2026-10-18-claude-interactive.10-zs-novelty-constants`).
- **Complex case, non-sharp.** Cuenin, Laptev and Tretter, DOI 10.1007/s00023-013-0259-3, arXiv:1207.6584 (full text), Cor. 4.6, give the same form for complex potentials with a weaker constant.
- **Not found:** the sharp complex case, and passive-mask TL optimality.

### Original Claude review — retained; conflicting statements superseded above

Claude-family review, 2026-10-16: a research subagent of claude-interactive, about 25 minutes of web search. Notes and PDFs are in the orchestrator's scratchpad.

**Inverse-scattering soliton content.**
- Satsuma & Yajima, Prog. Theor. Phys. Suppl. 55, 284 (1974), DOI 10.1143/PTPS.55.284. **Not accessed**; the content is confirmed through citing papers. Exact sech eigenvalues $i(A-\tfrac12-k)$.
- Trace formula $\int|q|^2=4\sum\mathrm{Im}\,\zeta_k+\int n(\xi)d\xi$, as given in Prilepsky, Derevyanko & Turitsyn, JOSA B 24, 1254 (2007), DOI 10.1364/JOSAB.24.001254. **Full text.** That paper also maps soliton number, power fraction and Hamiltonian fraction for chirped Gaussians.
- Klaus & Shaw, PRE 65, 036607 (2002), DOI 10.1103/PhysRevE.65.036607. **Abstract only.** Real single-lobe potentials: purely imaginary eigenvalues, count $\lfloor\tfrac12+\|q\|_1/\pi\rfloor$.
- Klaus & Shaw, SIAM J. Math. Anal. 34, 759 (2003). **Not accessed**; quoted by Biondini & Luo, PLA 382, 2632 (2018), whose introduction was read in full. No eigenvalues if $\|q\|_1<\pi/2$, sharp.
- Tovbis & Venakides, Physica D 146, 150 (2000), DOI 10.1016/S0167-2789(00)00126-3. **Abstract only.** Solvable chirped potentials.
- Burzlaff, J. Phys. A 21, 561 (1988). The preprint was read in **full text**: exact content of rectangular and exponential pulses.
- **Not accessed:** Hmurcik & Kaup, JOSA 69, 597 (1979); Desaix, Anderson & Lisak, PRE 50, 2253 (1994); Kaup & Malomed, Physica D 84, 319 (1995); Desaix et al., PRE 65, 056602 (2002).

**Fission with Raman.**
- Kodama & Hasegawa, IEEE JQE 23, 510 (1987). **Abstract only.**
- Tai, Hasegawa & Bekki, Opt. Lett. 13, 392 (1988), DOI 10.1364/OL.13.000392. **Abstract only.** Raman fission keeps the inverse-scattering amplitudes.
- Husakou & Herrmann, PRL 87, 203901 (2001). **Abstract only.**
- Dudley, Genty & Coen, Rev. Mod. Phys. 78, 1135 (2006). **Not accessed**, because the PDF was blocked. It is the standard source for the ejected-soliton widths and powers.
- Driben, Malomed, Yulin & Skryabin, PRA 87, 063808 (2013), arXiv:1305.5911. **Abstract only.** With third-order dispersion, the tallest soliton escapes a fission chain by collisions.

**SSFS rate and corrections.**
- Gordon, Opt. Lett. 11, 662 (1986), DOI 10.1364/OL.11.000662. **Abstract only.**
- Mitschke & Mollenauer, Opt. Lett. 11, 659 (1986). **Not accessed.**
- Santhanam & Agrawal, Opt. Commun. 222, 413 (2003). **Abstract only.**
- Skryabin, Luan, Knight & Russell, Science 301, 1705 (2003). **Not accessed.**

**Reported efficiencies.** Definitions differ between papers.
- Liu et al., Opt. Lett. 26, 358 (2001): above 60% in a taper. **Abstract only.**
- Lee, van Howe, Xu & Liu, IEEE JSTQE 14, 713 (2008), a review: up to 57% in higher-order-mode fibre, and energy scaling as $D A_{\rm eff}/n_2$. **Abstract or snippets.**
- Wang et al., Opt. Lett. 42, 3518 (2017): above 90% inside a Tm amplifier, gain included, so not comparable. **Abstract only.**
- Horton et al., Nat. Photon. 7, 205 (2013): 67 nJ at about 1.7 µm. **Abstract only.**
- Tang et al., Optica 3, 948 (2016): 2–4.3 µm in fluoride fibre. **Abstract only.**

**Shaping.**
- Efimov, Taylor, Omenetto & Vanin, Opt. Lett. 29, 271 (2004), DOI 10.1364/OL.29.000271: adaptive phase-only control of the self-frequency shift. **Abstract only.**
- Hu et al., PRL 114, 073901 (2015): Airy (cubic-phase) control of primary and secondary Raman solitons. **Full text, partial.**
- Caldarola et al., Papers in Physics 4, 040001 (2012): chirp delays fission and reduces the shift. **Full text, skimmed.**
- Wetzel et al., Nat. Commun. 9, 4884 (2018). **Abstract only.**

**Searched:** Satsuma–Yajima, Kodama–Hasegawa, Zakharov–Shabat eigenvalue bounds and trace formulas, chirp and soliton content, fission with Raman, SSFS efficiency records, Gordon-law corrections, SSFS pulse-shaping control, "efficiency–shift" and "maximum soliton energy versus shift". **None of these** found a bound on the largest eigenvalue in terms of $\|q\|_\infty$ or $|Q(\omega)|$, a phase-optimality theorem at fixed spectral amplitude, an efficiency–shift frontier, or a reported headroom number.

## Sharpest statement of the gap

**Current gap (gpt-b, 2026-10-16).** For a specified perturbed regime and passive launch class, obtain a controlled outer frontier for final soliton energy fraction, frequency shift and centroid variance, with a stated soliton-extraction rule and input/noise ensemble. Quantify transfer, radiation, quantum defect and covariance transport, and measure the optimization gap against the same TL baseline. The input ZS strip/trace bounds, peak/$L^4$ extremality, Gordon drift and a calibrated Raman-transfer correction are prior work; combining them without an error estimate does not establish the frontier.

**Historical gap statement — retained, superseded where it conflicts with the current gap:**

**Known:**
- the exact soliton content of transform-limited sech and of several solvable profiles;
- the trace formula, area thresholds and the chirp-reduces-content results (exact for one family, numerical for Gaussians);
- that Raman fission keeps the inverse-scattering amplitudes, qualitatively;
- Gordon's rate law and its moment-method corrections;
- scattered efficiency records, with inconsistent definitions;
- qualitative phase-shaping control.

**Not found:**
- the outer bound on the leading soliton's energy and shift rate over passive input shaping, of which sketch 1 is a candidate;
- the efficiency–shift frontier on common axes, combining:
  - the ZS energy fraction;
  - the Gordon rate with $\beta_2(\omega)$, $\gamma(\omega)$ and loss;
  - the fission corrections from third-order dispersion, dispersive waves and Raman collisions;
  - the quantum defect;
- the size of the headroom that phase-only or amplitude-and-phase shaping actually gives in the GNLSE.

## Claims and current results

| Claim | Status | Current reading |
|---|---|---|
| C-20261016-claude-a-01, the transform-limited launch maximises the leading ZS eigenvalue | proposed; verification T-20261016-claude-a-01 not done | See sketch 1 above. The maximality is numerical, not a theorem. |
| C-20261016-claude-a-02, Raman-transfer law | refuted as written (gpt-c, `claims/notes/audit-2026-10-16-gpt-c-C-20261016-claude-a-02.md`) | **What fails.** The "$E_1^{\max}$" corollary confuses the maximum share with a maximum energy: at a share maximum $dE_1/dT_0=-E_1/T_0<0$. Independent shorter-duration counterexamples remain with realistic dispersion and Raman. **What survives**, on the independently checked points ($N\in\{2,3,4,4.5,5,6,7,8,10\}$, $\tau_R\in[0.00168,0.0244]$): the empirical peak-share and peak-position statements. The $N=12$, 16 and Hollenbeck–Cantrell predictions pass at their candidate points, and the weak-Raman exponent at $N=2$ is 1.006. With published SMF-28 dispersion, the Hollenbeck–Cantrell response, shock and loss, the efficient-point energy is about 1.44–1.46 nJ (run `2026-10-16-gpt-c-raman-audit`). **Novelty** (gpt-b, PR #52): partly published. The phenomenon, the duration turnover at $N=6$ (53.0% at 700 fs FWHM) and the $N=5$, 6 peak shares are in Kormokar et al. 2023. An 18 fs Raman-overlap width is in Judge et al. 2009 and Pant et al. 2010. |
| C-20261016-claude-a-03, phase-shaping headroom below 5% | refuted by its proposer | The 11- and 15-parameter searches exceeded 5% (run `2026-10-16-claude-a-raman-soliton-frontier`). |
| C-20261016-claude-a-04, phase-mask headroom of at least 7–9% at $N=4$ | proposed; verification T-20261016-claude-a-03 not done | +9.0% at $T_0=100$ fs and +7.0% at 200 fs, against about 2% at $N=3$. No search converged (run `2026-10-16-claude-a-raman-soliton-frontier`). |

**Answer to the PI's question so far.**
- The main lever on the leading soliton's share is the launch duration, near $T_0^*$.
- Spectral phase adds at least 7–9% at $N=4$, and nothing in the integrable limit.
- The share-optimal operating point delivers about $1.5|\beta_2|/(\gamma\tau_1)$ in the reference model, equivalently a leading soliton of about 18 fs. With the proposer's SMF-28 coefficients that is 1.7–1.8 nJ. With realistic SMF-28 dispersion, the Hollenbeck–Cantrell response, shock and loss it is about 1.45 nJ (gpt-c). It is an efficient operating point, not a ceiling.

**What to measure** (gpt-c). Separate four quantities, and give the output length and spectral support with each physical prediction:
- the maximum conversion share;
- the energy at a share-optimal point;
- the maximum absolute energy under a stated input constraint;
- the corresponding photon fractions.

**Merged jitter part** (exploration `explorations/2026-10-16-claude-a-leading-soliton-jitter.md`, not a claim). At fixed red shift and peak power, the fission source has 5–40× lower quantum-limited timing variance ($N=2$–5) than a direct fundamental-soliton launch. The fixed-efficiency comparison is open (T-20261016-claude-a-04).

## Conjectures

**Review qualification (gpt-b, 2026-10-16):** the unregistered conjecture below is retained as a refutation target, not endorsed evidence; use the corrected launch classes, denominators and premise limitations above.

None registered. Refutable first conjecture: in the GNLSE with Raman and $\delta_3\le0.05$, adjoint-optimized phase masks raise $f_1$ above its transform-limited value by less than the integrable-limit factor $2N/(2N-1)$, times the transform-limited launch's own Raman-transfer enhancement (measured, not assumed), for $N=2$–8. A larger measured headroom means shaping can steer the Raman transfer between pulses, and refutes the conjecture.

**Outcome after round 5.** The conjecture is tested and holding. The largest gains found are 1.090 ($N=4$, 100 fs, against a bound of 1.56) and 1.070 ($N=4$, 200 fs, against 1.68) (C-20261016-claude-a-04).
- The headroom is not small at $N=4$, and small mask bases underestimate it (C-20261016-claude-a-03, refuted). At $N=3$ it is about 2%.
- Restated open question: the converged headroom of phase and passive masks near $T_0^*$, and its $N$-dependence.

## Oracle

**Available.**
- FastDifferentiableMMNLO propagates the GNLSE with Raman, self-steepening and full $\beta(\omega)$.
- Its adjoint gives gradients of $f_1$, or of the energy at a target shift, with respect to the input spectral phase and amplitude. That makes the refutation engine direct: optimize masks and try to beat the bound.
- A short Zakharov–Shabat eigenvalue solver in numpy, for example Fourier collocation or Boffetta–Osborne, computes the soliton content of any shaped input. It checks sketch 1, $\mathrm{Im}\,\zeta_{\max}\le\|q\|_\infty$, directly.

**Cheap tests:**
- the Satsuma–Yajima eigenvalues;
- the trace formula;
- the chirped-sech eigenvalue formula;
- Gordon's rate for a fundamental soliton.

**Caveats found in round 5.** For $N\ge7$ the leading soliton reaches the Nyquist edge of a 16384-point grid over $160T_0$ and is aliased. Those points need at least 32768 points (65536 for $N=10$) (C-20261016-claude-a-02).

## Lab test

Use a fibre SSFS source with a programmable pulse shaper (phase, then amplitude). Measure the leading soliton's energy and centre wavelength at fixed length, against the transform-limited launch, while scanning masks:
- chirp and cubic phase first;
- then an adaptive search.

A measured fractional gain above the bound in the GNLSE regime where the bound is claimed refutes it. A gain close to the bound confirms that shaping cannot do better.

## Risks and must-reads

- **The bound may be easy or already known in inverse-scattering mathematics.** Its novelty would then lie in the optical statement, the frontier, and the measured GNLSE headroom.
- **At $N\approx1$–2 the bound is loose.** At $N=1$ it allows a factor of 2 in amplitude and 16 in rate, and the interesting physics moves into the corrections.
- **Collision-mediated transfer may dominate in long fibres.** The frontier may then be set by dynamics rather than by input content.
- **Must-reads:**
  - Klaus & Shaw 2002/2003;
  - Prilepsky et al. 2007;
  - Lee et al. 2008;
  - Dudley et al. RMP 2006;
  - Driben et al. 2013;
  - Efimov et al. 2004;
  - Hu et al. 2015;
  - the soliton-collision Raman-transfer literature (not yet searched).

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-16 | claude-interactive (claude; claude-opus-5-5) | Proposed as candidate on the PI's request; Claude-family literature review by a research subagent | PI request in chat, 2026-10-16; sources listed above |
| 2026-10-16 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Merged with overlapping round-4 cards (see Merged cards); scope and literature updated from the GPT audits in PRs #42–#43 | PI message in chat, 2026-10-16; `docs/review-2026-10-13-gpt-a-frequency-conversion-novelty.md` on branch `task/T-20261013-gpt-a-01` |
| 2026-10-16 | gpt-b (gpt; gpt-6-astra) | Second-family review: literature_state open → partial; status candidate retained pending Claude agreement on revised scope; priority unchanged; novelty_confidence medium → low; added gpt to audited_by | [second-family review](../docs/review-2026-10-16-gpt-b-supercontinuum-literature.md); run `2026-10-16-gpt-b-sclit-premises`; source ledger and follow-up tasks in report |
| 2026-10-17 | claude-interactive (claude; claude-opus-5-5) | Applied the round-5 proposed card changes (claude-a, gpt-c, gpt-b): claims list, status of the sketches, claims and current results, conjecture outcome, oracle caveats, literature additions. Status, priority, literature_state and novelty_confidence unchanged; the Claude-family agreement on gpt-b's revised gap (T-20261016-gpt-b-05) is still open | logs `2026-10-16_claude-a_T-20261016-claude-interactive-02.md`, `2026-10-16-gpt-c-raman-audit.md`; task T-20261017-claude-interactive-01 |
| 2026-10-18 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Added claim C-20261018-pi-chatgpt-01 (the PI's GPT 6 Pro passive-mask ZS bound) to the claims list; status, priority and literature_state unchanged | Task T-20261018-claude-interactive-01 |
| 2026-10-18 | claude-interactive.10 (claude; claude-opus-5-5) | Added the round-6 literature note: the sharp $L^p$ ZS bound is published for real nonnegative potentials in Dirac form (DGPV 2024), and in non-sharp form for complex potentials (CLT 2014). Status, priority, literature_state and novelty_confidence unchanged | [novelty report](../docs/review-2026-10-18-claude-interactive.10-zs-eigenvalue-bound-novelty.md); task T-20261018-claude-interactive-03 |
| 2026-10-18 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Results R-0001 (formalized) and R-0002 (promising) added from C-20261018-pi-chatgpt-01: the passive-mask ceiling for the integrable reference limit. Status unchanged: the Raman-perturbed frontier, which is the target quantity, is still open | Task T-20261018-claude-interactive-04 |
| 2026-10-19 | claude-interactive.15 (claude; claude-opus-5-5), on PI instruction | Result R-0006 (promising) added: the phase-mask headroom witnesses of C-20261016-claude-a-04 as narrowed by gpt-a, $H\ge1.09016$ (A2, 100 fs) and $H\ge1.06974$ (B, 200 fs) at $N=4$, a lower bound in the Raman-perturbed model. Status, priority, literature_state and novelty_confidence unchanged: the frontier and the true headroom are still open. The current-results row for C-20261016-claude-a-04 and the claims list (missing C-20261017-gpt-a-01) are stale; left for T-20261019-claude-interactive.15-05 | PI decision 2026-10-19 (T-20261019-claude-interactive-07); task T-20261019-claude-interactive-08 |
