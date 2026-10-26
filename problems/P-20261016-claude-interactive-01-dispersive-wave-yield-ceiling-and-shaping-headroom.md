---
id: P-20261016-claude-interactive-01
title: "Dispersive-wave yield ceiling of fibre supercontinuum, and the headroom of input spectral shaping"
status: candidate
priority: 2
literature_state: partial
novelty_confidence: medium
target_quantity: "A continuum-certified ceiling on integrated DW-band energy or physical photon yield over a finite length interval and fixed upstream laser spectrum, for phase-only masks, passive amplitude-and-phase masks and a band-limited at-most-energy reference class, with a controlled transient-yield law and fair transform-limited shaping headroom."
model: "Generalized NLSE in anomalous dispersion with arbitrary real dispersion relation D(Omega) (beta_2 < 0 at the pump, one or more zero-dispersion frequencies), Kerr, then causal Raman response and self-steepening; lossless first, loss later; input = laser field after a passive spectral pulse shaper; output photons counted in the dispersive-wave band B."
oracle_ready: available
last_audited: 2026-10-16
audited_by: [claude, gpt]
proposed_by: claude-interactive
claims:
- C-20261016-claude-b-01
- C-20261016-claude-b-02
- C-20261016-claude-b-03
results: []
---

## Target quantity

**Current scope, gpt-b (gpt; gpt-6-astra), 2026-10-16.** The GPT review below supersedes conflicting definitions, sketches and negative literature statements preserved in this card. Use upstream laser energy/photon number as the denominator, record mask throughput, and restrict length to a stated finite interval. The nested reference is $\mathcal S_{\le E}$; attenuated passive masks do not belong to an exact-energy $\mathcal S_E$. Physical photon density is the energy spectrum divided by $\hbar\omega$, not unweighted NLSE mass. Input spectral support is not an output support bound. A relative headroom requires a nonzero TL yield under the same constraints.

**The PI's question (2026-10-16).**
- How much light can be generated in the dispersive-wave (DW) part of a supercontinuum?
- How much room is there to increase it by simple spectral-amplitude and spectral-phase modulation of the input?

**Definitions.**
- $\eta_B$ is the fraction of input photons found in the DW band $B$ at the fibre output.
- The three nested input classes are those of P-20261016-claude-interactive-03:
  - $\mathcal S_\phi$: phase-only masks on the laser spectrum $|Q(\omega)|$;
  - $\mathcal S_{A\phi}$: passive masks $|m|\le1$;
  - $\mathcal S_E$: any input of the laser's energy in its band.
- Targets:
  - the ceiling $\eta_B^{\max}(\mathcal S)$ over the class and the fibre length;
  - the headroom $H_{\mathcal S}=\eta_B^{\max}(\mathcal S)/\eta_B^{\rm TL}$.

**Answer form.**
- A rigorous, computable ceiling within the Kerr-plus-dispersion model, ideally in closed form in $N$, $\delta_3=\beta_3/(6|\beta_2|T_0)$ (or the full $D(\Omega)$) and the pump-to-ZDW detuning. It should become one-sided when Raman is added.
- An asymptotic law for the achieved yield.
- The measured headroom of phase-only and amplitude-and-phase shaping in the GNLSE.

## Signal of hidden simplicity

The following are the orchestrator's derivation sketches, 2026-10-16. They are not checked and are not claims. Sketch 1 develops a remark made by the literature subagent.

> **Status of the sketches after round 5 (2026-10-16/17; see "Claims and current results" below).**
> - **Sketch 1 is refuted as a ceiling** (C-20261016-claude-b-03; gpt-b's review in PR #46 reaches the same conclusion). With $\beta_3>0$ the linear energy $K(w)=w^2/2-\delta_3w^3$ is unbounded below on the band side, so a vanishing photon fraction far out in the band can balance any Hamiltonian deficit, and the supremum is 1. The Gagliardo–Nirenberg control does not help. On the simulation windows the program gives 0.57–0.95, which is 2.9 to 837 times the transform-limited yield (run `2026-10-16-claude-b-dw-program`). In normal dispersion with pure $\beta_2$ it reduces to the Cantelli bound $\sigma^2/(\sigma^2+w_B^2)$, with $\sigma^2=2|\mathcal H_{\rm in}|/\mathcal N$. With $\beta_3\ne0$ it is vacuous there too.
> - **Sketch 2 is moot as a ceiling** for the same reason. Where the yield is exponentially small, phase shaping acts instead through the strip width $d_*$ below (C-20261016-claude-b-02).
> - **Sketch 3 is replaced by the minimum-strip law** (C-20261016-claude-b-01). The burst yield of a transform-limited launch scales as $e^{-d_*/\delta_3}$, where $d_*$ is the narrowest analyticity strip of the $\delta_3=0$ evolution up to the fibre end. For the $N=2$ sech, $d_*=\tfrac12\arccos(\sqrt3-1)=0.374734$; the claim card prints 0.374664, a decimal slip noted by gpt-a.
>   - Roy et al.'s Eq. 6 (DOI 10.1103/PhysRevA.79.023824) is a spectral-peak estimate built on the ejected-soliton strip $\pi/(2(2N-1))$. Roy et al. validated it against Raman-inclusive simulations and themselves reported its deviation from Raman-free (TOD-only) data.
>   - At $N=2$ that TOD-only gap is 39.5, 12.8 and −0.4 dB at $\delta_3=0.02$, 0.03 and 0.04 (run `2026-10-16-claude-b-dw-oracle`).
>   - Emission concentrated at the compression point is published (Austin et al. 2006; Demircan et al. 2007; Driben, Yulin & Efimov 2015; see Literature state).
>   - gpt-a's audit narrows the law to a finite-range calibrated law.

1. **A conservation-law program bounds band yield.**
   - **Invariants.** Without Raman, self-steepening or loss, the GNLSE conserves three quantities:
     - photon number $\mathcal N=\int n\,d\Omega$;
     - momentum $\mathcal P=\int\Omega\,n\,d\Omega$;
     - the Hamiltonian $\mathcal H=\int D(\Omega)n\,d\Omega-\tfrac\gamma2\int|A|^4dt$.

     Here $n$ is the photon spectrum.
   - **Bounding the Kerr term.** The sharp Gagliardo–Nirenberg inequality (Weinstein's constant, attained by the soliton) bounds the Kerr energy by the spectrum itself: $\int|A|^4\le C\,\mathcal N^{3/2}(\int\Omega^2n)^{1/2}$.
   - **The program.** Every reachable output spectrum therefore lies in a convex set:
     - $n\ge0$;
     - fixed $\int n$ and $\int\Omega n$;
     - $\int Dn-\tfrac\gamma2C\mathcal N^{3/2}(\int\Omega^2n)^{1/2}\le\mathcal H_{\rm in}$.

     Maximizing $\int_Bn$ over this set is a convex program. Its value is a rigorous ceiling on $\eta_B$, for every input with those invariants.
   - **The mechanism it encodes** is the spectral recoil of Akhmediev & Karlsson (1995). Blue DW photons must be balanced in momentum by red-shifted photons. On the recoil side $D(\Omega)$ grows, so the Hamiltonian and the Kerr-energy bound cap how far the remainder can recoil.
2. **Phase shaping enters only through $\mathcal H_{\rm in}$.**
   - At fixed $|Q(\omega)|$, the quantities $\mathcal N$, $\mathcal P$ and $\int Dn_{\rm in}$ are fixed. Only $\int|A_{\rm in}|^4$ changes, and the transform-limited pulse maximizes it (P-20261016-claude-interactive-03, sketch 2).
   - So the whole phase class maps onto a one-parameter family of programs. For phase-only shaping, the ceiling is determined by the range of $\int|A_{\rm in}|^4$ the laser spectrum allows. Run `2026-10-16-claude-interactive-zs-bound-check` found that random phase masks on a Gaussian never exceeded 0.93 of the transform-limited value.
   - Whether this ceiling is tight, and whether the transform-limited launch is the binding case, is the open question.
3. **The yield is a transient at maximum compression,** set by the compressed pulse's spectral tail at the resonance. Akhmediev & Karlsson give the amplitude as proportional to the soliton's spectral amplitude at $\omega_{\rm DW}$. Webb et al. (2014) organize efficiency by an effective soliton order. This suggests the achieved yield depends on the laser mostly through the compressed spectrum, which shaping can tailor.

## Merged cards (PI decision 2026-10-16)

This card now carries two round-4 cards. Their files stay in PR #41 as the record and will be marked merged once that PR lands.

**P-20261012-claude-interactive.4-01, dispersive-wave yield law** (claude-interactive.4). The GPT audit (gpt-a, PR #43) narrowed it.
- Roy, Bhadra & Agrawal (2009), Eq. 6 (**full text**, gpt-a), already gives a perturbative peak-power law for the radiation of the shortest fission daughter. Its small parameter is $(2N-1)\delta_3/6$. Its saturation concerns peak power, not integrated yield.
- Austin et al., Opt. Express 14, 11997 (2006), DOI 10.1364/OE.14.011997 (**abstract only**, gpt-a), already treats compression-window emission and recoil.
- Modotto et al., JOSA B 32, 1676 (2015), DOI 10.1364/JOSAB.32.001676 (**full text**, gpt-a), gives a perturbative radiation spectrum and an energy-conversion experiment in a fibre with several zero-dispersion wavelengths.
- **Corrected detuning.** For cubic dispersion $\beta(\Omega)=-b\Omega^2/2+c\Omega^3/6$ and a soliton at $\Omega_s=-r$, the resonance at zero nonlinear phase lies at laboratory offset $3b/c+2r$ from the soliton (run `2026-10-13-gpt-a-novelty-premises`).
- **The observable to use** is the integrated band fraction, with the initial band leakage $\eta_B(0)$ stated, over a fixed launch class and a finite $L_{\max}$. A compressed-spectrum overlap estimate is not a bound.

**P-20261012-claude-interactive-01, conservation-law ceilings** (orchestrator). The GPT audit narrowed it.
- The Hamiltonian–Markov ceiling $\eta_B^E\le H_0/(E\inf_B\hat\beta)$ for normal dispersion is a direct consequence of the optical invariant in Castelló-Lurbe, Andrés & Silvestre, Opt. Express 21, 28550 (2013), DOI 10.1364/OE.21.028550 (**full text**, gpt-a). Related: Castelló-Lurbe, Vermeulen & Silvestre (2016), DOI 10.1364/OE.24.026629 (**full text**).
- Higher-invariant (Sobolev) control: Koch & Tataru, Duke Math. J. (2018), DOI 10.1215/00127094-2018-0033 (**full text**).
- Long-time asymptotics of the defocusing NLSE: Deift & Zhou, CPAM (2003), DOI 10.1002/cpa.3034 (**full text**). Restating these in optical units alone is not novel.
- For a chirped Gaussian, $2T_0^2H_0/(\beta_2E)=(1+C^2)/2+N^2/\sqrt2$ (run `2026-10-13-gpt-a-novelty-premises`).
- The admissible class $\mathcal A$ needs a Hamiltonian or bandwidth budget, because fixed energy and duration alone do not bound $H_0$.

**Consequences for this card.**
- Sketch 1's convex program, with the Gagliardo–Nirenberg control of the Kerr term in anomalous dispersion, is the useful improvement over the known Markov ceiling.
- In normal dispersion the program reduces to that ceiling.
- Energy and photon fractions must be kept distinct (Zheltikov, PRA 98, 043833 (2018), **full text**, gpt-a).

**Added GPT note, 2026-10-16 (gpt-b; gpt-6-astra; gpt).** Preserve the merged review above. Its Roy small-parameter expression uses a different convention: with this card's $\delta_3=\beta_3/(6|\beta_2|T_0)$, the shortest daughter's parameter is $(2N-1)\delta_3$, without another factor of $1/6$ (DOI **10.1103/PhysRevA.79.023824**, **full text**, Eq. 6 and definitions). The convex-program improvement and its asserted normal-dispersion reduction remain proposals until sign, coercivity, both Hamiltonian inequalities and continuum certification are supplied; see the current GPT review below.

## Literature state

### GPT-family review, 2026-10-16 — current assessment

Reviewer: **gpt-b; model gpt-6-astra; family gpt**. Verdict: **open, narrowed**. Literature state changes **open → partial**. Priority remains unchanged. Novelty **3/5**: a certified anomalous-dispersion band ceiling would extend established invariant and convex-bound methods. Impact **3/5**: a useful tightness guarantee would give specialist fibre groups a practical shaping/design rule. Novelty confidence remains **medium**.

**Premise check.** In $iA_z=K(i\partial_t)A-\gamma|A|^2A$, $K=-\beta$ for the usual $A_z=i\beta A+i\gamma|A|^2A$ convention. Write $n=|\widehat A|^2/(2\pi)$, $M=\int n$, $P=\int\Omega n$, and $M_K=\int Kn$. These are energy-envelope quantities. The sharp GN inequality gives the necessary convex constraints

$$H\le M_K,\qquad M_K-\frac{\gamma M^{3/2}}{2\sqrt3}\sqrt{M_2-P^2/M}\le H.$$

The sketch's second constraint alone is an outer relaxation, but can allow almost all mass in the target band with an arbitrarily distant compensating tail for cubic dispersion. The first inequality excludes the explicit sequence in run `2026-10-16-gpt-b-sclit-premises`; it does not by itself establish a nontrivial bound for arbitrary real dispersion. A continuum dual certificate or tail enclosure is needed: a finite-grid primal optimum is not automatically an upper bound for the continuum. TL maximizes input $\int|A|^4$ and hence minimizes this signed Hamiltonian; it does not automatically maximize the relaxed ceiling over phases. The full derivation and limitations are in [second-family review](../docs/review-2026-10-16-gpt-b-supercontinuum-literature.md).

**Sources newly read, upgraded or correcting the original review:**
- Castelló-Lurbe et al., DOI **10.1364/OE.21.028550**, **abstract only** here, and DOI **10.1364/OE.24.026629**, **full text**, invariant formulation: optical Hamiltonian restrictions are established prior work; historical gpt-a full-text access remains recorded below.
- Weinstein, DOI **10.1007/BF01208265**, **full text**, §§I–III: sharp interpolation and invariant control. The normalization is checked on sech in run `2026-10-16-gpt-b-sclit-premises`.
- Akhmediev & Karlsson, DOI **10.1103/PhysRevA.51.2602**, **full text**, stationary-soliton flux and recoil; Roy et al., DOI **10.1103/PhysRevA.79.023824**, **full text**, Eq. 6 is peak spectral power, not integrated band yield. Roy's fourth-order-dispersion paper is DOI **10.1016/j.optcom.2009.06.018**, **abstract only**.
- Li et al., DOI **10.1016/j.rinp.2020.103518**, **full text**, model and efficiency sections: integrated DW conversion under quadratic/cubic phase is already studied, but peak-power rescaling changes pulse energy across masks. Li et al., DOI **10.1002/andp.202200601**, **abstract only**, also study enhanced DW conversion with sinusoidal phase.
- Liu et al., DOI **10.34133/ultrafastscience.0107**, arXiv:**2411.14410**, **full text**, optimization pipeline and Eq. 5: gradient-controlled DW efficiency/frequency/bandwidth is published. An amplifier follows the shaper, and efficiency uses a measured-window output denominator; this is not the proposed passive upstream-normalized ceiling.
- Lefevre et al., DOI **10.1364/OE.22.019423**, **full text**, nonlinear coupled-mode adjoint optimization, including silicon Raman conversion: a relevant control-method precedent, not a fibre mask bound. Mohajan et al., arXiv:**2307.06414**, **full text**, formulation: convex bounds for undepleted-pump second-harmonic generation are a neighbouring photonic-bound precedent, not a solution of depleted Kerr supercontinuum.
- Hary et al., DOI **10.1364/OL.492064**, arXiv:**2304.00829**, **full text**, and DOI **10.1038/s41598-024-84567-x**, **full text**: the objectives include integrated narrow-channel energy, and throughput/power is also a control. Calling them only spectral-density optimization is incomplete. Wetzel et al., DOI **10.1038/s41467-018-07141-w**, **full text**, use a programmable pulse train and amplification, with a different launch class.
- Petty, DOI **10.17630/sta/690**, **full text**, chapter 4: chirp-dependent visible conversion is real, but the asserted matched-TL headroom ratio is not established by the quoted record comparison. Distinguish output fraction from coupled-input and coupling-inclusive efficiency. The thesis's record-table originals are identified in the report; full denominator harmonization remains incomplete; the tellurite entry is Cheng et al., DOI **10.1109/JPHOT.2014.2381662**, **abstract only**.
- Babushkin et al., DOI **10.1038/lsa.2016.218**, **full text**, results: a few-cycle, two-ZDW breakdown regime transfers nearly all energy outside anomalous dispersion without ordinary compression/fission. This rules out treating the quoted experimental records as a universal ceiling; it is not a proved one-band bound.

**Status gate.** There is a substantive Claude review below and this independent GPT review. The revised gap and corrected relaxation have not yet received recorded Claude agreement, so the card remains **candidate**, with `audited_by: [claude, gpt]`. No simulation or claim-audit status is conferred. [second-family review](../docs/review-2026-10-16-gpt-b-supercontinuum-literature.md) contains the complete source-by-source ledger, unresolved access and search log.

**Additional searches:** “gradient descent dispersive wave conversion efficiency pulse shaper”; “adjoint nonlinear coupled mode Raman optimization”; “Li quadratic cubic spectral phase dispersive wave conversion efficiency”; “Hamiltonian spectral band bound nonlinear Schrodinger Gagliardo Nirenberg”; “fundamental limits nonlinear frequency conversion convex”; “higher order soliton compression complex singularity radiation exponential asymptotics”. The narrower certified ceiling above was not found in these searches; the old broad negative statements below are superseded.

### Round-5 additions (2026-10-16/17)

- **Roy, Bhadra & Agrawal 2009**, DOI 10.1103/PhysRevA.79.023824: **full text**, read by claude-b and by gpt-a (with vector extraction of Fig. 3(b)). Eq. 6 is a spectral-peak estimate. The authors validated it against their Raman-inclusive simulations and reported its deviation from Raman-free data.
- **From gpt-b's novelty review** (PR #49; access levels are gpt-b's):
  - Austin et al. 2006, DOI 10.1364/OE.14.011997, full text: compression-region emission and integrated DW energy;
  - Demircan, Pietrzyk & Bandelow 2007, DOI 10.34657/2265, full text;
  - Driben, Yulin & Efimov 2015, DOI 10.1364/OE.23.019112, arXiv:1505.02716, full text: radiation from the oscillating breather;
  - Wai, Chen & Lee 1990, DOI 10.1103/PhysRevA.41.426, full text;
  - Karpman 1993, DOI 10.1103/PhysRevE.47.2073, full text;
  - Moston-Duggan, Porter & Lustri 2023, DOI 10.1007/s00332-022-09834-5, full text;
  - McCue et al. 2026, DOI 10.1017/jnw.2026.10033, arXiv:2509.07397, full text: the closest method, in KdV;
  - Sulem, Sulem & Frisch 1983, DOI 10.1016/0021-9991(83)90045-1, abstract only.

### Original Claude review — retained; conflicting statements superseded above

Claude-family review, 2026-10-16, by a research subagent of claude-interactive (about 25 minutes of web search). Notes and texts are in the orchestrator's scratchpad.

**Emission theory:**
- Akhmediev & Karlsson, PRA 51, 2602 (1995), DOI 10.1103/PhysRevA.51.2602. **Full text** (pp. 1–4). Resonance $\omega_0\approx-\varepsilon^{-1}[\tfrac12+2(\varepsilon A)^2]$. Radiated flux $Q\propto\varepsilon^{-3}e^{-\pi/(2\varepsilon A)}$. Amplitude proportional to the soliton's spectral amplitude at resonance. Momentum recoil drives the soliton to a quasi-stationary state.
- Skryabin & Gorbach, Rev. Mod. Phys. 82, 1287 (2010), arXiv:1005.2777. **Full text**, Cherenkov section. Amplitude $\propto e^{-a^2|\Delta|}$. With $\beta_3>0$ and Raman, emission is front-loaded.
- Roy, Bhadra & Agrawal, PRA 79, 023824 (2009), DOI 10.1103/PhysRevA.79.023824. **Abstract only.** A minimum third-order dispersion for a DW peak; saturation at a relative level "typically below 10%". The abstract does not say whether this is energy or peak.
- Roy et al., Opt. Commun. 282, 3798 (2009), fourth-order dispersion: sidebands above 10%. **Abstract only.**
- Webb, Erkintalo, Xu, Genty & Murdoch, Opt. Lett. 39, 5850 (2014), DOI 10.1364/OL.39.005850, arXiv:1607.04945. **Full text**, first pages. DW as cascaded four-wave mixing; efficiency set by an effective soliton order $N(\Delta)$.
- Erkintalo, Genty & Dudley, Opt. Lett. 35, 658 (2010), DOI 10.1364/OL.35.000658. **Abstract only.** Soliton collisions raise DW peak power about tenfold.

**Gas-filled hollow-core fibre:**
- Travers, Grigorova, Brahms & Belli, Nat. Photon. 13, 547 (2019), DOI 10.1038/s41566-019-0416-4, arXiv:1811.05877. **Full text**, relevant sections. Scaling rules; $N$ capped near 15; conversion of 0.5% near 120 nm and over 15% in the deep UV.
- Brahms et al., Opt. Lett. 44, 2990 (2019), arXiv:1903.12103. **Full text.** 9–11%.
- Brahms & Travers, J. Phys. Photonics 3, 025004 (2021), arXiv:2101.04014. **Full text.** Yield saturates with pump energy; once saturated, DW energy noise is low.

**Records:**
- Chang, Chen & Kärtner, Opt. Lett. 35, 2361 (2010): above 40%. **Abstract only.**
- Petty, PhD thesis, St Andrews (2024), DOI 10.17630/sta/690. **Full text**, relevant sections.
  - 55% into one peak below 600 nm, chirp-optimized.
  - The literature table lists 20–67%, up to 67% in tellurite near the zero-dispersion wavelength (ZDW). Those entries are cited from his table and **not accessed**.
- Si₃N₄: Grassani et al., Nat. Commun. 10, 1553 (2019), DOI 10.1038/s41467-019-09590-3. **Abstract only, plus a grep of the arXiv text.** Up to 35% (30% in the arXiv version).
- Gas fibre: Chen et al., Opt. Express 28, 17076 (2020), DOI 10.1364/OE.393959. **Full text, skimmed.** 19%.

**Shaping:**
- **Petty (2024).** The only clean measured headroom: a group-delay-dispersion scan raises yield from about 40% to 55% inside a ±50 fs² window.
- **Lei et al.**, Chin. Phys. Lett. 26, 064213 (2009), DOI 10.1088/0256-307X/26/6/064213. **Abstract only.** In simulation, either sign of chirp lowered DW energy.
- **Li et al.**, Results in Physics 19, 103518 (2020), DOI 10.1016/j.rinp.2020.103518. **Snippet only.** Cubic plus quadratic phase "strongly enhances" DW energy.
- **Hary et al.**
  - Opt. Lett. 48, 4512 (2023), DOI 10.1364/OL.492064. **Abstract only.** Genetic-algorithm phase shaping gives 5–160× in narrowband spectral density, mostly in the Raman-soliton region; that is not a DW energy fraction.
  - Sci. Rep. 15, 377 (2025), DOI 10.1038/s41598-024-84567-x. **Abstract only.** A comparison of optimizers.
- **Wetzel et al.**, Nat. Commun. 9, 4884 (2018). **Abstract only.**

**Not found:**
- any paper optimizing a pulse shaper for DW yield by gradient or adjoint;
- any rigorous bound on band energy in the GNLSE;
- any use of the Hamiltonian or conservation laws to cap DW yield.

**Searched:**
- "upper limit dispersive wave conversion efficiency momentum conservation / Manley–Rowe";
- "rigorous bound spectral bandwidth NLSE conservation laws";
- "Zakharov–Shabat soliton content radiation fraction";
- "optimal control / adjoint NLSE";
- "differentiable GNLSE".

**Overlap.** This card absorbs P-20261012-claude-interactive.4-01 (dispersive-wave yield law), which is in PR #41. Its GPT novelty audit (PR #43) narrowed the gap to the integrated, finite-length yield beyond Roy's peak law. This card adds the shaping classes and the conservation-law program.

## Sharpest statement of the gap

**Current gap (gpt-b, 2026-10-16).** For a stated physical dispersion, finite output band and finite propagation interval, obtain a nontrivial continuum-certified upper bound on integrated DW yield over $\mathcal S_\phi$, $\mathcal S_{A\phi}$ and $\mathcal S_{\le E}$. Specify energy versus photon weighting, Hamiltonian sign, output tails and initial leakage. Then give an achieved transient-yield approximation and a fair passive-mask/TL optimization gap with controlled error. Optical invariants, stationary exponential emission, fission-daughter peak laws, integrated-yield shaping and gradient-based DW control are prior work. The sources and limits of the negative search are in the current literature review above.

**Historical gap statement — retained, superseded where it conflicts with the current gap:**

**Known:**
- the DW frequency (phase matching);
- the exponentially small emission rate of a stationary soliton and its spectral-overlap form;
- scaling rules that keep the dynamics fixed;
- record yields of 10–67%, by platform;
- one chirp scan giving 1.4× headroom.

**Not found:**
- a rigorous ceiling on the integrated DW fraction over any input class (sketch 1 is a candidate);
- a law for the achieved transient yield in $N$, $\delta_3$ and pulse shape;
- the true headroom of general phase-only or amplitude-and-phase shaping over a transform-limited launch, measured with gradient-based optimal control.

## Claims and current results

| Claim | Status | Current reading |
|---|---|---|
| C-20261016-claude-b-01, minimum-strip DW yield law | refuted as written (gpt-a, `claims/notes/audit-2026-10-16-gpt-a-C-20261016-claude-b-01.md`) | **What survives.** A finite-range calibrated law, about $30\le d_*/\delta_3\le48$, for the launches and endpoints tested, with explicit gate and band stability. The frozen Raman held-out case passes. **What fails.** The literal fixed-gate $\delta_3\to0$ limit: a fixed smooth gate keeps the core's complex singularities, whose tail decays at $d_*/3$. At sech $N=2$, $\xi_f=2.25$, $\delta_3=0.003$, the gate-15 band yield and the gate-20 resonant-band yield differ by a factor 114 (runs `2026-10-16-gpt-a-dw-highprecision`, `2026-10-16-gpt-a-gate-null`). **In Roy et al.'s full model** (Raman with $f_R=0.245$; self-steepening $s=1/(\omega_0T_0)$), the strip is fixed at 0.4655 from the TOD-free Raman evolution and two constants are calibrated below visibility. The law then predicts the observable peaks at $\delta_3=0.016$–0.03 with RMS error 0.40 dB, against 8.0 dB for parameter-free Eq. 6. Both fail once the DW saturates ($\delta_3\ge0.04$) (run `2026-10-16-gpt-a-dw-analysis`). **Novelty:** partly published (gpt-b, PR #49). |
| C-20261016-claude-b-02, shaping headroom | proposed; verification T-20261016-claude-b-02 not done | **Large yields** (transform-limited 0.05–0.32): persistent phase-mask gains of 1.54, 1.40, 1.17 and 1.01; passive masks add at most 3%; GDD alone gives at most 1.06. **Small yields:** an optimised mask lowers $d_*$ from 0.1922 to 0.1858 and gives 2.04× at $N=3$, $\delta_3=0.01$. A frozen transfer test gave 2.38× and 3.07× at $\delta_3=0.0075$ and 0.006. **With Raman** ($f_R=0.18$, $T_0=50$ fs) the same mask *reduces* the yield, to 0.03–0.08× transform-limited. **Measurement:** a compression at the output plane can inflate the band count by up to about 2000× (runs `2026-10-16-claude-b-dw-shaping`, `2026-10-16-claude-b-dw-oracle`). |
| C-20261016-claude-b-03, the conservation program is vacuous | cheap-checks-passed; verification T-20261016-claude-b-03 not done | See sketch 1 above. |

**Answer to the PI's question so far** (model without Raman unless stated):
- Transform-limited Gaussians put 0.1–32% of launched photons past the zero-dispersion frequency at $\xi=2$, for $N=3$–10 and $\delta_3=0.01$–0.05. The yields are organised by $d_*/\delta_3$.
- Simple spectral shaping adds at most about 1.5× where the yield is already 5–16%, and almost nothing at 30%. Large relative gains exist only where the yield is tiny, and there Raman removes them.
- No useful ceiling follows from the invariants alone. A ceiling has to come from the dynamics, for example a lower bound on the strip width over the input class (T-20261016-claude-b-04).

**What to measure.**
- Distinguish band photons at the output plane from radiated DW photons, and say how the latter are measured: persistence over length plus soliton-centred gating, or another justified outgoing-radiation measure.
- Fixed temporal gates fail as $\delta_3\to0$ (gpt-a).
- Distinguish the conserved envelope norm from the broadband physical photon number.

## Conjectures

**Review qualification (gpt-b, 2026-10-16):** the unregistered conjecture below is retained as a refutation target, not endorsed evidence; use the corrected launch classes, denominators and premise limitations above.

None registered. A refutable first conjecture: for a Gaussian laser at $N=3$–10 and $\delta_3=0.01$–0.05, the adjoint-optimized phase-only mask raises $\eta_B$ above the transform-limited value by at most a factor of 2. The conservation-law ceiling of sketch 1 then lies within a factor of 3 of the optimized yield. Either part fails if optimization finds more headroom, or if the ceiling is loose by more.

**Outcome after round 5.**
- "Phase-only at most 2×" holds at large transform-limited yields.
- It fails where the yield is exponentially small: 2.04× at $N=3$, $\delta_3=0.01$, rising as $e^{\kappa/\delta_3}$ to 3.07× at 0.006 (C-20261016-claude-b-02). That gain does not survive Raman at $T_0=50$ fs.
- "Ceiling within 3×" fails because the program is vacuous (C-20261016-claude-b-03).

## Oracle

**Available.**
- **FastDifferentiableMMNLO** gives GNLSE propagation with full $D(\Omega)$, Raman and self-steepening. Its adjoint gives $\partial\eta_B/\partial\phi(\omega)$ and $\partial\eta_B/\partial m(\omega)$, so a mask can be optimized by gradient ascent.
- **The convex program** of sketch 1 is a small second-order-cone problem over a discretized output spectrum, using cvxpy or a hand-written solver. The Weinstein constant is known in closed form.

**Cheap tests:**
- the invariants hold to discretization accuracy (but see the aliasing caveat in PR #37's assessment);
- Akhmediev–Karlsson flux for a single soliton;
- the program's value for an input that is already a soliton.

**Caveats found in round 5.**
- A fixed temporal gate does not isolate radiation as $\delta_3\to0$, because it keeps the core's complex singularities (run `2026-10-16-gpt-a-gate-null`). Use a resonant band with demonstrated gate and band stability, or persistence over length.
- A compression at the output plane can inflate the band count by orders of magnitude (C-20261016-claude-b-02).
- Roy et al.'s self-steepening coefficient is $s=1/(\omega_0T_0)$ (their Eq. 7), not $2/(\omega_0T_0)$ (run `2026-10-16-gpt-a-roy-reference`).

## Lab test

Use a Ti:sapphire or Yb laser, a programmable pulse shaper (phase, then amplitude) and a PCF or taper with a known $D(\Omega)$. Measure the DW-band energy fraction with an absolute power meter behind a band filter while scanning the masks: chirp, cubic phase, adaptive. Compare with the transform-limited launch, with the adjoint-predicted optimum and with the ceiling. Above-ceiling yields in the Kerr-dominated regime refute the bound. A gap smaller than the predicted headroom refutes the optimization picture.

## Risks and must-reads

- The convex ceiling may be loose by a large factor. Its value would then be qualitative, and the work would move to the achieved-yield law.
- Raman breaks momentum conservation and helps the recoil. The ceiling then needs a Raman momentum budget, as in P-20261012-claude-interactive.4-04 and P-20261016-claude-interactive-02.
- Near-ZDW pumping (the 67% record) may violate the assumptions behind any "fission" picture.
- **Must-reads:**
  - Akhmediev & Karlsson 1995;
  - Petty 2024;
  - Travers et al. 2019 and Brahms & Travers 2021;
  - Roy et al. 2009 (full text read in round 5; see Round-5 additions);
  - Biancalana, Skryabin & Yulin, PRE 70, 016615 (2004) (**not accessed**);
  - Weinstein's sharp Gagliardo–Nirenberg constant (Comm. Math. Phys., 1983; **not accessed**; check the citation).

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-16 | claude-interactive (claude; claude-opus-5-5) | Proposed as candidate on the PI's request. Claude-family literature review by a research subagent. Absorbs P-20261012-claude-interactive.4-01. | PI request in chat, 2026-10-16; sources listed above |
| 2026-10-16 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Merged with overlapping round-4 cards (see Merged cards); scope and literature updated from the GPT audits in PRs #42–#43 | PI message in chat, 2026-10-16; `docs/review-2026-10-13-gpt-a-frequency-conversion-novelty.md` on branch `task/T-20261013-gpt-a-01` |
| 2026-10-16 | gpt-b (gpt; gpt-6-astra) | Second-family review: literature_state open → partial; status candidate retained pending Claude agreement on revised scope; priority unchanged; novelty_confidence medium retained; added gpt to audited_by | [second-family review](../docs/review-2026-10-16-gpt-b-supercontinuum-literature.md); run `2026-10-16-gpt-b-sclit-premises`; source ledger and follow-up tasks in report |
| 2026-10-17 | claude-interactive (claude; claude-opus-5-5) | Applied the round-5 proposed card changes (claude-b, gpt-a): claims list, status of the sketches, claims and current results, conjecture outcome, oracle caveats, literature additions. Status, priority, literature_state and novelty_confidence unchanged; the Claude-family agreement on gpt-b's revised gap (T-20261016-gpt-b-05) is still open | logs `2026-10-16_claude-b_T-20261016-claude-interactive-03.md`, `2026-10-16-gpt-a-dw-audit.md`; task T-20261017-claude-interactive-01 |
