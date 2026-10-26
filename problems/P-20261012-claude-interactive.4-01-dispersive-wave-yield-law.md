---
id: P-20261012-claude-interactive.4-01
title: Maximum dispersive-wave yield from soliton fission as a law in N·δ3
status: parked
priority: 2
literature_state: partial
novelty_confidence: low
target_quantity: Maximum integrated output energy in the normal-dispersion radiation band for a fixed fiber, finite
  propagation interval and explicitly bounded input family, with initial radiation-band energy bounded and reported.
  Determine which parameters beyond N times delta3 are needed. Physical-photon yield is a separately normalized
  extension.
model: 'Baseline: scalar lossless NLSE with anomalous beta2, cubic dispersion and instantaneous Kerr nonlinearity;
  fixed fiber, bounded input bandwidth/chirp and length. Add Raman, optical shock and higher-order dispersion separately.
  The standard no-shock power-envelope norm is energy, not exact broadband photon number.'
oracle_ready: available
last_audited: '2026-10-13'
audited_by:
- claude
- gpt
proposed_by: claude-interactive.4
provenance:
  agent: claude-interactive.4
  model: claude-fable-5-1
  family: claude
claims: []
results: []
review_provenance:
  agent: gpt-a
  model: gpt-6-astra
  family: gpt
  verdict: open, narrowed
  concurrence: pending
  review: docs/review-2026-10-13-gpt-a-frequency-conversion-novelty.md
---

> **Merged into P-20261016-claude-interactive-01** (dispersive-wave yield ceiling and shaping headroom) by PI decision on 2026-10-16. That card carries this card's premises and its GPT audit in its "Merged cards" section. Continue the work there; this card is kept for its history and is not worked on separately.

## Target quantity

**GPT verdict: open, narrowed.** An analytical radiation law in soliton order and third-order dispersion is already published. The remaining question concerns an **integrated** finite-length yield and a bound over a well-defined input family. Keep **candidate** until Claude agrees to the changed observable and gap.

Use $\eta_{\rm ND}^{E}(z)=E_{\rm in}^{-1}\int_{\Omega>\Omega_{\rm ZD}}|\widetilde A(z,\Omega)|^2d\Omega/(2\pi)$ in the no-shock baseline. State and bound $\eta_{\rm ND}^{E}(0)$; maximizing an output fraction over arbitrary inputs otherwise rewards photons or energy launched in the target region. A subtracted initial fraction is a net redistribution metric, not a tag on individual newly generated photons.

Fix the fiber, $L_{\max}/L_D$, admissible bandwidth, launch centroid, chirp and pulse-shape class. Define $P_0$ and $T_0$ consistently, so $N^2=\gamma P_0T_0^2/|\beta_2|$ is meaningful. The card's convention remains $\delta_3=\beta_3/(|\beta_2|T_0)$. For broadband photon yield, use positive absolute frequencies and a photon-conserving propagation law; energy and photon fractions cannot be interchanged.

## Premise check

[Roy, Bhadra and Agrawal (2009), PRA; 10.1103/PhysRevA.79.023824](https://doi.org/10.1103/PhysRevA.79.023824) (**full text**), Eq. 6, already gives a perturbative radiation-peak-power law for the shortest fission daughter. Its TOD parameter is $\delta_R=\delta_3/6$ and its small parameter is $(2N-1)\delta_R$. Its exponentially small overlap law and numerical peak-power saturation remove the original claim that the paper lacks an $N$–TOD law. The paper's peak-power level cannot be compared to integrated conversion efficiencies as an alleged ceiling violation.

For cubic dispersion $\beta(\Omega)=-b\Omega^2/2+c\Omega^3/6$, a soliton at $\Omega_s=-r$ and radiation offset $x=\Omega_{\rm DW}-\Omega_s$ obey
$$\beta(\Omega_s+x)-\beta(\Omega_s)-\beta'(\Omega_s)x
=-\frac{b+cr}{2}x^2+\frac{c}{6}x^3=q.$$
At zero nonlinear phase $q$, the nonzero root is $x=3b/c+3r$, with laboratory offset $3b/c+2r$. The proposal's $3b/c+4r$ relative detuning is incorrect. Substitution checks are in run **2026-10-13-gpt-a-novelty-premises**. A physical calculation must retain the soliton nonlinear phase and its evolving spectrum.

The assumed compressed-sech tail is a spectral-overlap estimate, not an upper bound on emitted radiation. The zero-dispersion edge and the phase-matched radiation frequency are different. A recoil relation alone does not fix emission duration, depletion or integrated yield. [Austin et al. (2006); 10.1364/OE.14.011997](https://doi.org/10.1364/OE.14.011997) (**abstract only**) already treats compression-window emission and recoil.

## Literature state

All inherited citations have a current access/verification entry in [the review](../docs/review-2026-10-13-gpt-a-frequency-conversion-novelty.md).

| Source and identifier | Access | What was checked |
|---|---|---|
| Roy, Bhadra and Agrawal (2009), PRA, [10.1103/PhysRevA.79.023824](https://doi.org/10.1103/PhysRevA.79.023824) | full text | Equations 2 and 6 provide a TOD/soliton-order radiation-peak-power law. The reported saturation concerns peak power, not integrated photon yield. |
| Austin et al. (2006), [10.1364/OE.14.011997](https://doi.org/10.1364/OE.14.011997) | abstract only | Compression-window emission and recoil-induced blue shift are already identified; they are not missing mechanisms. |
| Modotto et al. (2015), [10.1364/JOSAB.32.001676](https://doi.org/10.1364/JOSAB.32.001676) | full text | Contains an analytical perturbative radiation spectrum, Eq. 4, and an energy-conversion experiment in a multi-zero-dispersion fiber. |
| Webb et al. (2014), [10.1364/OL.39.005850](https://doi.org/10.1364/OL.39.005850) | full text | Effective soliton order, compression and finite fiber length explain efficiency trends for a dual-frequency beat input. |
| Akhmediev and Karlsson (1995), [10.1103/PhysRevA.51.2602](https://doi.org/10.1103/PhysRevA.51.2602) | abstract only | Abstract explicitly promises an analytic amount of radiation, not phase matching alone; full quantitative scope remains to be checked. |
| Skryabin et al. (2003), [10.1126/science.1088516](https://doi.org/10.1126/science.1088516) | abstract only | Negative dispersion slope: red Cherenkov radiation recoils the soliton toward blue and cancels Raman shift. The proposal reversed the relevant radiation direction. |
| Timmerkamp and Fallnich (2026), [10.1364/OE.590355](https://doi.org/10.1364/OE.590355) | abstract only | Integrated silicon-nitride waveguide, orthogonally polarized modes, and probe-photon conversion; not scalar-fiber pump conversion. |

Additional corrections: [Erkintalo, Genty and Dudley (2010); 10.1364/OL.35.000658](https://doi.org/10.1364/OL.35.000658) (**abstract only**) reports numerical collision-enhanced peaks, not measured integrated yields. [Skryabin et al. (2003); 10.1126/science.1088516](https://doi.org/10.1126/science.1088516) (**abstract only**) concerns red radiation and blue soliton recoil in negative dispersion slope. The later finite-order compression-fit constants and the original fission-partition attribution remain unverified. [Mollenauer et al. (1983); 10.1364/OL.8.000289](https://doi.org/10.1364/OL.8.000289) (**full text**) measures compression position in soliton periods. [Zheltikov (2018), SPM theory; 10.1364/OE.26.017571](https://doi.org/10.1364/OE.26.017571) (**full text**), Eq. 6, explicitly includes $\pi/2$ in the leading large-$N$ compression length measured in $L_D$; the proposal omitted this factor. The literature-equation comparison is recorded in run **2026-10-13-gpt-a-novelty-literature**. [Kodama and Hasegawa (1987); 10.1109/JQE.1987.1073392](https://doi.org/10.1109/JQE.1987.1073392) (**not accessed**) was located bibliographically; the partition is independently reproduced in [Kormokar, Shamim and Rochette (2023); 10.1364/JOSAB.478975](https://doi.org/10.1364/JOSAB.478975) (**full text**).

**Searches:** “dispersive wave conversion efficiency analytical maximum”; “Roy Bhadra Agrawal 023824”; “dispersive wave conversion efficiency soliton order third-order dispersion”; “dispersive wave recoil compression window”; “dual frequency beat signal efficiency”; “inverse design dispersive wave efficiency analytical”; exact searches for every inherited DOI.

## Sharpest statement of the gap

No source found in this audit establishes a certified maximum **integrated** radiation-band fraction over a bounded launch family and finite propagation interval in the fixed cubic-dispersion fiber. An asymptotic law is worth pursuing only if it distinguishes integrated yield from the published peak law, reports the initial spectral seed, and identifies the additional parameters required for finite-distance emission.

It is not established that $N\delta_3$ alone controls this maximum. Pulse shape, chirp, length, phase mismatch and the daughter distribution can matter even before Raman and shock corrections. The multi-zero-dispersion experiment and perturbative spectrum in [Modotto et al. (2015); 10.1364/JOSAB.32.001676](https://doi.org/10.1364/JOSAB.32.001676) (**full text**) are a separate geometry, not a violation of Roy's peak-power result. Numerical optimization supplies achievable values, not proof of a maximum.

## Conjectures

The original C1 and its numerical tolerances are **superseded**, not adopted as a claim. First reproduce the published peak-law observable with the correct TOD convention and define the integrated observable. Then formulate a restricted asymptotic hypothesis, including its length and seed dependence, in **T-20261013-gpt-a-05**.

## Oracle

The scalar propagation capability is recorded as available. No new yield simulations were performed here. A future sweep must report separate spectral peak, band-integrated energy and photon fraction, together with launch leakage. Required numerical checks remain walk-off/window containment, aliasing, step-size and frequency-grid convergence. Do not optimize arbitrary inputs before the admissible class is fixed.

## Assessment and next step

**Novelty 2/5:** most proposed scaling mechanisms have close published precursors; the possible addition is a constrained integrated-yield theorem. **Impact 3/5:** a valid finite-length rule could guide specialist fiber-source design. Scores are judgments recorded in run **2026-10-13-gpt-a-novelty-literature**.

Claude reconciliation: **T-20261013-gpt-a-02**. Remaining full texts: **T-20261013-gpt-a-03**, especially Roy 2010 before any new derivation. Priority is unchanged.

## Superseded proposal material

The following is retained to preserve the original proposal. Its gap statements, numerical conjectures and access labels are superseded by the current review above; they are not active premises or independently verified numerical evidence.

<details>
<summary>Original proposal, retained for audit</summary>

```yaml
id: P-20261012-claude-interactive.4-01
title: "Maximum dispersive-wave yield from soliton fission as a law in N·δ3"
status: candidate
priority: 2
literature_state: partial
novelty_confidence: medium
target_quantity: "The maximum fraction of input photons that soliton fission can deliver into the phase-matched resonant-radiation (dispersive-wave) band of a fixed fibre, over all input pulse shapes and chirps at fixed energy and duration, as an upper bound or asymptotic law in the soliton order N, the normalized third-order dispersion δ3 and the Raman fraction f_R, with its gap to the adjoint-optimized input."
model: "Scalar GNLSE: i∂_z A = (β2/2)∂_t² A + i(β3/6)∂_t³ A (optionally β4) − γ(1 + i∂_t/ω0)[(1−f_R)|A|²A + f_R A ∫h_R(t')|A(t−t')|²dt'], β2<0 at the pump, lossless, single mode, coherent input."
oracle_ready: available
last_audited: null
audited_by: [claude]
proposed_by: claude-interactive.4
provenance:
  agent: claude-interactive.4
  model: claude-fable-5-1
  family: claude
claims: []
results: []
```

### Target quantity

Let a pulse of energy $E_{\rm in}$ and duration $T_0$ be launched in the anomalous-dispersion region of a fibre whose zero-dispersion frequency sits at $\Omega_{\rm ZD}=|\beta_2|/\beta_3$ above the pump (for $\beta_3>0$). Define the **normal-side photon fraction**

$$\eta_{\rm ND}(z)=\frac{\int_{\Omega>\Omega_{\rm ZD}}|\tilde A(z,\Omega)|^2\,d\Omega/(\omega_0+\Omega)}{\int|\tilde A(0,\Omega)|^2\,d\Omega/(\omega_0+\Omega)},$$

the fraction of launched photons that sit in normal dispersion at the output (no band width to choose; radiation there cannot be a soliton). A band-resolved version, photons within $\pm\Delta$ of the phase-matched frequency $\Omega_{\rm DW}$, is the secondary target.

The object to derive is $\eta^{\max}_{\rm ND}(N,\delta_3,f_R)=\max_{\rm inputs}\max_z\eta_{\rm ND}(z)$, the maximum over input amplitude and phase profiles at fixed energy and root-mean-square duration, in terms of

- $N^2=\gamma P_0T_0^2/|\beta_2|$ (soliton order),
- $\delta_3=\beta_3/(|\beta_2|T_0)$, so that $\Omega_{\rm ZD}T_0=1/\delta_3$ and $\Omega_{\rm DW}T_0\approx3/\delta_3$,
- $f_R$ and $T_R/T_0$, and the self-steepening parameter $s=1/(\omega_0T_0)$.

**Answer form.** Either (a) an upper bound $\eta^{\max}_{\rm ND}\le B(N\delta_3,f_R)$ that is rigorous within the model, with a known input that reaches a stated fraction of it, or (b) an asymptotic law with a measured error exponent: $\ln\eta^{\max}_{\rm ND}=-a/(N\delta_3)+b+O(N\delta_3)$ for $N\delta_3\ll1$, and a saturation law for $N\delta_3=O(1)$. The regime is given as bounds on $N$ (below the modulation-instability limit), $\delta_3$, $s$ and $T_R/T_0$.

### Signal of hidden simplicity

- **The emission window is short and its shape is universal.** Resonant radiation is shed where the higher-order soliton reaches its first compression point. The compressed duration follows the empirical soliton-compression law $T_c\approx T_0/(4.1N)$ at $z_{\rm opt}\approx(0.32/N+1.1/N^2)L_D$ (Mollenauer, Tomlinson, Stolen & Gordon, Opt. Lett. 8, 289 (1983), DOI [10.1364/OL.8.000289](https://doi.org/10.1364/OL.8.000289), **not accessed**; the law is quoted in textbooks). The overlap of the compressed spectrum with the normal-dispersion side is then a function of the single group $\Omega_{\rm ZD}T_c=1/(4.1N\delta_3)$. For a sech-like compressed spectrum the tail fraction beyond $\Omega_{\rm ZD}$ is $\tfrac12[1-\tanh(\pi/(8.2N\delta_3))]\approx\exp[-\pi/(4.1N\delta_3)]$, which suggests the small-$N\delta_3$ law above with $a\approx\pi/4.1$.
- **Recoil switches the emission off.** By momentum (spectral-centroid) conservation of the NLSE with $\beta_3$, photons emitted at $+\Omega_{\rm DW}$ recoil the emitting soliton to $-\Omega_s$. In the $\beta_3$-only model the resonance detuning measured from the soliton grows as $3|\beta_2|/\beta_3+4|\Omega_s|$, so emission stops once $4|\Omega_s|$ exceeds a few soliton bandwidths $1/T_s$. With the first fission soliton $T_1=T_0/(2N-1)$ this gives $\eta_{\rm ND}\lesssim c\,(2N-1)\delta_3$ with $c=O(1)$, a second law in the same group. The two laws cross near $N\delta_3\sim0.1$–$0.3$, where the literature's highest yields sit. (Self-limiting recoil is the mechanism of self-frequency-shift cancellation: Skryabin, Luan, Knight & Russell, Science 301, 1705 (2003), DOI [10.1126/science.1088516](https://doi.org/10.1126/science.1088516), **not accessed**.)
- **Measured yields span two decades and order themselves by detuning.** More than 40% with 10 fs pumps and a nearby resonance (Chang, Chen & Kärtner, Opt. Lett. 35, 2361 (2010), DOI [10.1364/OL.35.002361](https://doi.org/10.1364/OL.35.002361), **abstract only**); 50% to a long-wavelength dispersive wave in a dual-concentric-core fibre with three zero-dispersion wavelengths (Modotto et al., JOSA B 32, 1676 (2015), DOI [10.1364/JOSAB.32.001676](https://doi.org/10.1364/JOSAB.32.001676), **abstract only**); in gas-filled hollow capillaries above 15% in the deep ultraviolet, about 5% near 170 nm and 0.5% near 120 nm, with $N$ limited to below about 15 by modulation instability (Travers, Grigorova, Brahms & Belli, Nat. Photon. 13, 547 (2019), DOI [10.1038/s41566-019-0416-4](https://doi.org/10.1038/s41566-019-0416-4), **full text of the preprint arXiv:1811.05877**). In the pure third-order-dispersion model, Roy, Bhadra & Agrawal (Phys. Rev. A 79, 023824 (2009), **abstract only**, verified on the publisher's page) report that the radiation peak grows with $\beta_3$ and with $N$ and then "saturates to a relative power level that is typically below 10% of the launched power", with the minimum $\beta_3$ for a peak decreasing with $N$. The few-cycle and multi-zero-dispersion yields above sit far outside that saturation level, which is itself a signal that the ceiling moves with physics the pure model leaves out ($s$, $f_R$, $\beta_4$).
- No registered run yet. The first run on this card should be the $N$–$\delta_3$ sweep described under Oracle.

### Literature state

Searched 2026-10-12 (claude-interactive.4 with helper claude-interactive.4.3): "dispersive wave conversion efficiency soliton fission analytical maximum energy fraction"; "resonant radiation energy fraction scaling soliton order third-order dispersion optimum"; "pulse shaping optimization dispersive wave generation efficiency chirp genetic algorithm"; "soliton recoil dispersive wave energy balance photon number conservation yield bound"; "dispersive wave emission efficiency hollow core fiber pulse duration scaling"; "'dispersive wave' 'conversion efficiency' '50%' photonic crystal fiber"; title searches for the papers below. DOIs checked against Crossref.

Perturbative emission theory (rate, not yield):
- Akhmediev & Karlsson, Phys. Rev. A 51, 2602 (1995), DOI [10.1103/PhysRevA.51.2602](https://doi.org/10.1103/PhysRevA.51.2602). **Not accessed.** Radiation amplitude of a fundamental soliton under $\beta_3$, exponentially small in the detuning.
- Elgin, Brabec & Kelly, Opt. Commun. 114, 321 (1995), DOI [10.1016/0030-4018(94)00602-Q](https://doi.org/10.1016/0030-4018(94)00602-Q). **Not accessed.** Perturbative third-order-dispersion theory.
- Erkintalo, Xu, Murdoch, Dudley & Genty, Phys. Rev. Lett. 109, 223904 (2012), DOI [10.1103/PhysRevLett.109.223904](https://doi.org/10.1103/PhysRevLett.109.223904). **Not accessed.** Cascaded four-wave-mixing picture of dispersive-wave emission.
- Webb, Xu, Erkintalo & Murdoch, Opt. Lett. 38, 151 (2013), DOI [10.1364/OL.38.000151](https://doi.org/10.1364/OL.38.000151). **Not accessed.** Generalized dispersive-wave emission from non-solitonic pulses.

Yield maps and efficiency studies:
- Roy, Bhadra & Agrawal, Phys. Rev. A 79, 023824 (2009), DOI [10.1103/PhysRevA.79.023824](https://doi.org/10.1103/PhysRevA.79.023824). **Abstract only** (publisher page). Analytical and numerical study of dispersive waves from solitons perturbed by third-order dispersion: the radiation-peak amplitude first grows with $|\beta_3|$ and $N$, then saturates at a relative power "typically below 10% of the launched power"; the minimum $\beta_3$ needed for a peak decreases with $N$. No formula for the yield is given in the abstract. **The closest prior work to this card; its full text must be read first.**
- Roy, Bhadra & Agrawal, Opt. Lett. 34, 2072 (2009), DOI [10.1364/OL.34.002072](https://doi.org/10.1364/OL.34.002072). **Not accessed** (abstract withheld from the index used; author copy and institutional copy unavailable). Effects of fourth- and higher-order dispersion on the resonant peak.
- Roy, Ghosh, Bhadra & Agrawal, Opt. Commun. 283, 3081 (2010), DOI [10.1016/j.optcom.2010.04.003](https://doi.org/10.1016/j.optcom.2010.04.003). **Not accessed.** Role of the dispersion profile in dispersive-wave emission.
- Webb, Erkintalo, Xu, Genty & Murdoch, Opt. Lett. 39, 5850 (2014), DOI [10.1364/OL.39.005850](https://doi.org/10.1364/OL.39.005850), arXiv:1607.04945. **Abstract only.** Dispersive-wave efficiency of a dual-frequency beat signal predicted through an effective soliton order per beat cycle: a map in $N$, not a bound.
- Austin, de Sterke, Eggleton & Brown, Opt. Express 14, 11997 (2006), DOI [10.1364/OE.14.011997](https://doi.org/10.1364/OE.14.011997). **Not accessed.** Recoil-driven blue-shift of the dispersive wave.
- Chang, Chen & Kärtner, Opt. Lett. 35, 2361 (2010) (above) and Opt. Express 19, 6635 (2011), DOI [10.1364/OE.19.006635](https://doi.org/10.1364/OE.19.006635). **Abstract only / not accessed.** Few-cycle regime, >40% conversion.
- Modotto et al., JOSA B 32, 1676 (2015) (above). **Abstract only.** 50% to a long-wavelength dispersive wave; three zero-dispersion wavelengths.
- Erkintalo, Genty & Dudley, Opt. Lett. 35, 658 (2010), DOI [10.1364/OL.35.000658](https://doi.org/10.1364/OL.35.000658). **Not accessed.** Giant dispersive-wave generation through soliton collision: a route to yields above the single-soliton law.
- Timmerkamp & Fallnich, Opt. Express 34, 25282 (2026), DOI [10.1364/OE.590355](https://doi.org/10.1364/OE.590355). **Abstract only.** Up to 25% of probe photons converted by intermodal cross-phase modulation during fission; limited by probe chirp and interaction bandwidth.

Hollow-core and capillary sources (achievable points, limits named by the authors):
- Travers et al., Nat. Photon. 13, 547 (2019) (above). **Full text of preprint.** Yields quoted above; ionization losses up to 40% of the energy; $N<15$.
- Brahms, Belli & Travers, Phys. Rev. Research 2, 043037 (2020), DOI [10.1103/PhysRevResearch.2.043037](https://doi.org/10.1103/PhysRevResearch.2.043037). **Abstract only.** Up to 12% (1800 nm, 30 fs pump).
- Brahms, Belli & Travers, Opt. Lett. 45, 4456 (2020), DOI [10.1364/OL.398343](https://doi.org/10.1364/OL.398343). **Not accessed.** Pressure gradients.
- Köttig, Tani, Biersach, Travers & Russell, Optica 4, 1272 (2017), DOI [10.1364/OPTICA.4.001272](https://doi.org/10.1364/OPTICA.4.001272); Mak, Travers, Hölzer, Joly & Russell, Opt. Express 21, 10942 (2013), DOI [10.1364/OE.21.010942](https://doi.org/10.1364/OE.21.010942); Joly et al., Phys. Rev. Lett. 106, 203901 (2011), DOI [10.1103/PhysRevLett.106.203901](https://doi.org/10.1103/PhysRevLett.106.203901). **Not accessed.**

Fission partition and compression:
- Kodama & Hasegawa, IEEE J. Quantum Electron. 23, 510 (1987), DOI [10.1109/JQE.1987.1073392](https://doi.org/10.1109/JQE.1987.1073392). **Not accessed.** Fission into fundamental solitons of durations $T_0/(2N-2k+1)$.
- Mollenauer et al., Opt. Lett. 8, 289 (1983) (above). **Not accessed.**
- Dudley, Genty & Coen, Rev. Mod. Phys. 78, 1135 (2006), DOI [10.1103/RevModPhys.78.1135](https://doi.org/10.1103/RevModPhys.78.1135). **Abstract only** (as recorded on P-013).

**What is solved.** The emission rate of a fundamental soliton (perturbative, exponentially small in $1/\delta_3$); the phase-matching frequency and its recoil shift; numerical maps of yield for specific fibres, including the statement that in the pure $\beta_3$ model the yield saturates below about 10% (Roy et al. PRA 2009, abstract); the mechanisms that raise yield (few-cycle pumps, soliton collisions, multiple zero-dispersion wavelengths, intermodal cross-phase modulation). **Not found:** a bound or scaling law for the maximum yield in $N$ and $\delta_3$, an optimization over input shape, a recoil-based yield bound, or an account of why the pure-model saturation near 10% is exceeded four- to five-fold in the few-cycle and multi-zero-dispersion experiments.

### Sharpest statement of the gap

No published statement bounds the dispersive-wave photon fraction from fission, or gives its asymptotic law in $N$ and $\delta_3$; Roy et al. (PRA 2009) report a numerical saturation "typically below 10%" in the pure $\beta_3$ model without a law or an optimization. The perturbative rate (Akhmediev–Karlsson) applies to a fundamental soliton far from resonance and says nothing about the compression-window burst that produces the measured 10–50% yields. What is open: whether $\eta^{\max}_{\rm ND}$ collapses onto one curve in $N\delta_3$ (at fixed $f_R$, small $s$), what that curve is in the exponential and the recoil-limited regimes, where it saturates, and how far the best shaped input sits below it. The multi-zero-dispersion and collision routes (Modotto 2015; Erkintalo 2010) are outside the single-group law and bound its domain.

### Conjectures

No claim files yet. The refutable conjecture to register first:

**C1.** For $f_R=0$, $s\to0$ and $2\le N\le10$, the maximum normal-side photon fraction over sech inputs with chirp $C\in[-2,2]$ is a function of $N\delta_3$ alone to within 20%, with $\ln\eta^{\max}_{\rm ND}=-a/(N\delta_3)+b$ for $N\delta_3<0.1$, $a=\pi/4.1\pm30\%$, and $\eta^{\max}_{\rm ND}\le c\,(2N-1)\delta_3$ with $c\le1$ for $N\delta_3<0.5$. Refuted if the collapse fails, if the fitted $a$ is outside the stated range, or if an adjoint-optimized input exceeds the recoil line.

Builds on the orchestrator's conservation-law cards: the centroid identity is the recoil ingredient; this card adds the dynamical switch-off and the compression-window argument.

### Oracle

**Available.** The solver's scalar GNLSE with $\beta_3$, $\beta_4$, self-steepening and Raman; adjoint gradients with respect to the input field (`adjoint_mode=:discrete_rk4ip`).

Cheap test (one afternoon of CPU): sweep $N\in\{1.5,2,3,4,6,8\}$ and $\delta_3\in[0.01,0.4]$ for sech inputs, $f_R\in\{0,0.18\}$, record $\max_z\eta_{\rm ND}$ and the output centroid of the remaining solitons; plot against $N\delta_3$. Then run the adjoint optimizer over 20–40 amplitude and phase parameters of the input at fixed energy and root-mean-square duration to raise $\eta_{\rm ND}$; the conjecture fails if the optimized value exceeds the recoil line or breaks the collapse.

Numerical checks required: the dispersive wave walks off quickly, so the time window must hold it without wrap-around (report the window and any absorbing boundary); step-size and grid convergence of $\eta_{\rm ND}$ to 1% at the largest $\delta_3$; aliasing of the $\beta_3$ phase at the grid edge.

Missing: nothing for the single-mode scalar case. Ionization (hollow-core sources) is outside the model and is not a target here.

### Lab test

Solid-core photonic-crystal fibre with $\beta_2$, $\beta_3$ known at the pump. Vary $N$ through the pulse energy at fixed $\delta_3$, and vary $\delta_3$ by tuning the pump wavelength toward the zero-dispersion wavelength at fixed $N$. Measure the photon fraction beyond the zero-dispersion wavelength with a calibrated spectrometer. The law predicts that both sweeps fall on one curve in $N\delta_3$, with the stated exponent at small $N\delta_3$. Any point above the bound, after correcting for loss, refutes it; a pulse shaper on the input tests the maximum.

### Risks and must-reads

- **Roy et al. (PRA 2009) already report saturation below about 10% in the pure $\beta_3$ model**, and their full text (not accessed) may contain the $N$–$\delta_3$ dependence of that level; read it, the OL 2009 and the 2010 papers before deriving. If a law is there, the card narrows to the bound over input shapes and to the physics ($s$, $f_R$, $\beta_4$) that lifts the 10% level to the measured 40–50%. Webb et al. (2014) has an effective-$N$ law for beat signals.
- **The single-group collapse may fail** when $\beta_4$ matters (two zero-dispersion wavelengths, the 50% point of Modotto 2015), when Raman shifts the soliton before compression ($T_R/T_0$ not small), or at $N>10$ where modulation instability seeds fission.
- **"Maximum over inputs" may be ill-posed** without the duration constraint: a chirped input compresses more. The target fixes energy and root-mean-square duration; state this in every run.
- **Must-reads not accessed:** Roy PRA 2009 (full text), Roy OL 2009 and Roy 2010; Erkintalo 2012; Webb 2013; Chang 2011; Travers, J. Opt. 12, 113001 (2010), DOI [10.1088/2040-8978/12/11/113001](https://doi.org/10.1088/2040-8978/12/11/113001); Skryabin & Gorbach, Rev. Mod. Phys. 82, 1287 (2010), DOI [10.1103/RevModPhys.82.1287](https://doi.org/10.1103/RevModPhys.82.1287).
- Overlap: P-20261012-claude-interactive.4-04 (blue-band budget) uses the same recoil identity for trapped waves; P-009 (parked) covers hollow-core Raman states, not this.

</details>

## Audit trail


| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive.4 (claude; claude-fable-5-1) | Created as candidate for the PI's frequency-conversion call; literature searched by helper claude-interactive.4.3 and checked against Crossref; no runs yet | Search strings and sources listed above; task T-20261012-claude-interactive.4-01 |
| 2026-10-13 | gpt-a (gpt; gpt-6-astra) | literature retained partial; novelty confidence → low; added GPT review and revised gap; candidate and priority retained pending Claude concurrence | Cross-family review docs/review-2026-10-13-gpt-a-frequency-conversion-novelty.md; runs 2026-10-13-gpt-a-novelty-literature and 2026-10-13-gpt-a-novelty-premises; follow-ups T-20261013-gpt-a-02, T-20261013-gpt-a-03, T-20261013-gpt-a-05 |
| 2026-10-17 | claude-interactive (claude; claude-opus-5-5) | candidate → parked: merged into P-20261016-claude-interactive-01 (PI decision 2026-10-16); priority unchanged | Task T-20261016-claude-interactive-06, closed in T-20261017-claude-interactive-01; the "Merged cards" section of P-20261016-claude-interactive-01 |
