---
date: 2026-10-09
agent: gpt-b
model: gpt-6-astra
family: gpt
task: T-20261009-gpt-b-01
problem: P-001
---

# Amplifier-similariton attraction and noise: prior-art review

## Summary for the PI

The strongest novelty risk is S1: arbitrary-pulse energy, timing and frequency noise equations already appear in Grigoryan–Menyuk–Mu (1999), and arbitrary-shape timing/frequency kick covariances appear explicitly in McKinstrie–Santhanam–Agrawal (2002), before its Gaussian specialization [N1–N2, full text]. Describing the latter paper as a Gaussian-only result misses material prior art.

Analytical attraction of the parabolic family is also published. Wabnitz (2007) supplies a hydrodynamic parameter model, spiraling width–chirp trajectories, and convergence-distance optimization [A7, abstract only; A8, full text]. The precise S6 Lyapunov formula and the complete S5 spectrum were not located, but neither a reduced attraction model nor breathing transients should be presented as new.

I did not locate the specific similariton noise-figure expressions in S2, the quadrature power exponents in S3, or the covariance-rank asymptotics in S4. These are bounded search findings, not certification of novelty or correctness. In particular, S3 needs a distinction between deterministic perturbation gain and a complete quantum amplifier channel [N8–N10].

Two further attribution issues matter. Conditional convergence through convex energy/transport methods has substantial damped-Euler antecedents [M1–M3]. Finot and Wu already report phase-imprinted dark structures on a parabolic background [A11, abstract only plus indexed body excerpts]; that is relevant physical prior art for S9, although I did not find its exact parity/orthogonality statement.

This review does not validate the claims mathematically. No derivations, simulations, or new numerical results were produced. The published optical phrase “arbitrary input” must be read alongside the ansatz, tested launch classes, approximation and convergence observable, rather than as an established full-NLSE global-attraction theorem.

## Scope and reading convention

The target is the constant, unsaturated, spectrally flat gain model supplied by the PI, with normal second-order dispersion and Kerr nonlinearity. Single-pass amplifiers, passive parabolic propagation, and periodically stationary laser cavities are distinguished throughout.

The target equation is $\partial_z A=-i\beta_2 A_{TT}/2+i\gamma|A|^2A+gA/2+F$, with $\beta_2>0$ and $G=e^{gL}$. S1 specifies $D=g(n_{sp}-1/2)\hbar\omega_0$ and increment covariance $(2D/E)W$. These are the claim's conventions, not a normalization newly derived here.

The comparison uses the supplied S1–S9 statements and the four claim cards on PRs [21](https://github.com/nrivera494/analytical-nl-discovery/pull/21) and [24](https://github.com/nrivera494/analytical-nl-discovery/pull/24), at inspected branch heads 1f766ac814b39705697cfd108e5d6d3f32bb0667 and 1e4d02fddc688343e9f614ff162f2e12e9c8a5d4 respectively. This is literature review, not an independence-gate audit.

“Full text” means the article body was accessed and the relevant sections inspected; the ledger specifies those sections. It does not mean every equation was independently checked. “Abstract only” includes cases where a few indexed body excerpts were also visible but the article was not adequately accessible. Downloading a file alone did not earn full-text status. “Not found” means not located in the searches and source set documented below.

## A. Attraction, transients, spectra and basin limits

### Asymptotic solution and wings

Fermann et al. establish the normal-dispersion amplifier similariton, its exponential amplitude/width scaling, linear chirp, numerical evolution from several launch conditions, and experimental pulse characterization [A1, full text]. The compact parabola is an asymptotic description; finite-distance pulses have low-amplitude wings.

Kruglov et al. (2000) extend the high-power parabolic construction to longitudinally varying gain [A2, abstract only]. Their 2002 paper explicitly treats the constant-gain asymptotic core, intermediate exponential wings and practical launch design [A3, full text, §§2–3]. Its calculation assumes a self-similar amplitude and quadratic phase, then neglects the core amplitude-curvature term asymptotically. It is not a spectral or nonlinear PDE stability proof for every complex initial field.

Boscolo et al. match the semiclassical parabolic core through Painlevé functions to linear low-amplitude tails [A4, abstract only]. This is significant edge-layer prior art; citing only the compact parabola misses it. Kruglov–Harvey (2006) address varying parameters [A5, abstract only]; their inaccessible body prevents a definitive equation-level comparison here. The 2003 PRL instead concerns exact solutions with distributed coefficients, including anomalous-dispersion cases [A6, abstract only]; its title alone does not establish the target constant-gain attraction claim.

Finot–Millot–Dudley, OL 29, 2533 (2004), is indeed titled *Asymptotic characteristics of parabolic similariton pulses in optical fiber amplifiers* [A10, full text]. It experimentally tests fixed-energy launches with different durations and profiles in a Raman amplifier, finding nearly identical output parabolic intensity/chirp and agreement with the asymptotic prediction. It does not measure a universal relaxation exponent or a perturbation spectrum. Billet et al. subsequently resolve intermediate wings experimentally using high-dynamic-range FROG [A12, abstract only; PDF located].

### Approach to the asymptotic state and reduced models

There is already more than an existence solution:

- Kruglov et al. give launch-width/energy optimization and a characteristic entry length, Eq. (31), based on a specified core nonlinear-to-amplitude-curvature ratio [A3, full text]. This is an approximate design criterion supported by their simulations, not a uniform error bound for arbitrary initial shape. Their Gaussian, sech and super-Gaussian examples have different transients.
- Finot et al. (2006) distinguish early SPM-dominated amplification from subsequent similariton formation [A9, full text, §§2–3]. Long inputs can stay almost unchanged in width initially; their parabolic-fit error need not decrease monotonically. A short initially parabolic pulse can lose its shape when dispersion is important. Negative launch chirp permits spectral recompression before the asymptotic regime.
- Wabnitz's full conference paper inserts parabolic intensity and linear frequency into the semiclassical hydrodynamic equations and obtains three parameter ODEs, with energy removing one degree of freedom [A8, full text]. Its Fig. 2 shows normalized width–chirp spirals towards the same sink for different initially unchirped widths. The journal abstract explicitly claims an analytical attraction model [A7, abstract only].
- Wabnitz–Finot (2008) explicitly attribute the two-ODE description to that earlier work and use it to estimate entry length and optimal initial width in dispersion-decreasing amplifiers [A13, full text, introduction and §3]. Their model is useful prior art even though the longitudinal dispersion differs from the target model.
- Hammani–Boscolo–Finot experimentally characterize the Gaussian-to-parabolic transition and distinguish linear, SPM and reshaping regimes [A14, full text, §§1–3]. Their wave-breaking boundary helps identify reshaping in the studied high-power launches.

Thus energy, duration, chirp and shape dependence of the transient is published. I did not locate a theorem assigning one convergence length or one error-decay exponent to all seed shapes. A phase portrait showing a spiral does not by itself establish the exact damping/frequency constants claimed in S5.

### Linear spectra and condensate analogues

The closest inspected optical evidence for damped width/chirp oscillations is Wabnitz [A8]. I did not find the entire displayed S5 eigenvalue sequence in the optical sources inspected.

Menotti–Stringari treat hydrodynamic collective oscillations of a trapped one-dimensional Bose gas, including the mean-field parabolic-density limit [M4, full text]. Their polynomial collective-mode frequency law is relevant antecedent to the Legendre structure. Fedichev–Fischer use scaling coordinates and separate quantum phase fluctuations into spatial modes and time-dependent oscillators, particularly their Eqs. (22)–(25) [M5, full text]. Neither includes the target distributed optical gain plus spontaneous-emission reservoir. The modal framework has prior art; the gain-dependent optical rates still require a precise comparison.

A frozen Thomas–Fermi spectral problem or a trapped ground-state spectrum must not be silently identified with the nonautonomous full-NLSE similariton spectrum. The retargeted problem card's Gallo–Pelinovsky leads were not independently read during this session and are not used as evidence for a novelty verdict.

### Basin and physical-model limitations

| Limitation | Published evidence and its scope |
|---|---|
| Wave breaking and shape | Finot et al. show launch-shape-dependent transients [A9, full text]; Hammani et al. discuss wave breaking along Gaussian-to-parabolic evolution [A14, full text]. Loss of smooth dispersionless flow and failure of eventual coarse intensity reshaping are different assertions. |
| Phase structure | Finot–Wu study initial linear chirp and phase jumps; dark structures can accompany an otherwise parabolic envelope [A11, abstract only plus excerpts]. This is directly relevant to broad “all inputs become the same field” language. |
| Finite gain bandwidth | Soh–Nilsson–Grudinin Part II analytically treat finite Lorentzian gain bandwidth and resulting chirp/envelope distortion and compression limits [A16, abstract only]. |
| Raman | Part I treats Stokes growth, depletion and compression degradation [A15, abstract only]. Deliberate Raman pumping used to create gain is distinct from intrapulse stimulated Raman scattering that distorts the amplified signal. |
| Third-order dispersion | Bale–Boscolo derive a forced perturbation correction and compare structural changes with simulation [A17, abstract only]. This is not automatically a homogeneous shape-mode stability spectrum. |
| Gain saturation | The core asymptotic papers explicitly exclude saturation [A3, full text]. Saturated gain and filtering occur in the cavity noise model [N4, full text]; those results do not supply a universal single-pass saturation basin. No such theorem was located here. |

The finite-bandwidth and Raman studies are operating-limit analyses, not proofs that every departure from their assumptions prevents all useful parabolic pulse generation. Nor does a dispersionless shock prove blow-up or permanent nonattraction of the dispersive optical field.

### Rigorous mathematics and dissipative similaritons

Huang–Marcati–Pan prove convergence of finite-mass entropy weak solutions of one-dimensional damped compressible Euler to the corresponding porous-medium Barenblatt profile, with norm-dependent rates and explicit assumptions [M1, full text, theorem and remarks]. Luo–Zeng prove global smooth physical-vacuum free-boundary evolution and convergence for small perturbations of the Barenblatt solution [M2, abstract only; full PDF located]. These are real convergence theorems, not merely resemblance between profiles. Their coordinates, damping, pressure law, norms and solution classes must be matched before importing a rate into the optical problem.

Carrillo–Choi–Tse construct Lyapunov functionals using free energy, Wasserstein distance and its derivative for damped Euler with confinement/interactions [M3, full text, §§1–2]. They assume global energy-decaying solutions with specified regularity rather than proving unrestricted existence. Their general convergence statement is not a universal exponential-rate theorem; explicit exponential estimates are available for particular cases. This is close methodological prior art for S7, but I did not locate its exact optical functional and $e^{-gz/3}$ bound there.

Bale–Kutz derive a leading porous-medium equation and a Barenblatt profile for rapidly dispersion-managed dissipative pulse dynamics [A18, full text, §§2–4]. They explicitly distinguish that leading profile from the attracting state once dissipative corrections matter. A cavity with alternating dispersion, nonlinear gain/loss and filtering is a different equation from the target uniform single-pass amplifier. The porous-medium connection is published, but cannot alone settle S5–S7.

## B. Classical noise, laser noise and spectral fluctuations

### What the arbitrary-pulse noise literature already gives

Grigoryan–Menyuk–Mu start from a gain/loss NLSE with a Langevin source and derive central-time/frequency dynamics for arbitrary pulse shape, including chirp-dependent cross terms [N1, full text, §IIA]. Their §IIC gives the pulse-energy variance without a Kerr-dependent energy-noise term. Their Gaussian-statistics conclusion is a linearization result: ASE–ASE beating is neglected and deterministic pulse functions enter the coefficients.

McKinstrie–Santhanam–Agrawal Eqs. (10)–(12) explicitly give arbitrary-shape frequency, time–frequency and time kick covariances, and credit Grigoryan et al. [N2, full text]. Only afterwards does Eq. (13) introduce a Gaussian pulse. Writing these moment overlaps as a Wigner covariance is a useful packaging of existing quantities, not sufficient evidence of a new noise law.

There is an important bibliographic correction: Santhanam–Agrawal, *Optics Communications* 222, 413 (2003), is *Raman-induced spectral shifts in optical fibers: general theory based on the moment method*, DOI 10.1016/S0030-4018(03)01561-X [N3, abstract only]. It concerns deterministic Raman frequency shifts and chirp/width history, not a similariton ASE covariance calculation.

### Similariton laser noise is published

Zweck–Menyuk compute timing jitter, phase jitter and comb linewidths in an amplifier-similariton laser with a round-trip map, gain saturation and filtering [N4, full text]. They distinguish centroid timing from definitions of phase, for which different projections need not agree. These are cavity observables, not the single-pass centre-frequency noise figure of S2.

Song–Jung–Kim experimentally compare ASE-limited timing-jitter spectra in soliton, stretched-pulse and self-similar laser regimes [N5, full text]. They separate directly driven timing noise from frequency noise converted to timing noise by cavity dispersion, and show dependence on pulse dynamics even at equal net cavity dispersion. Their comparison does not establish that similariton formation universally reduces noise.

Ilday et al. demonstrate self-similar evolution in a laser resonator [N6, abstract only]. Liao et al. analyze ASE-driven energy, phase, timing, duration and chirp fluctuations using a semiclassical Gaussian-pulse model [N7, full text, introduction and model]. Neither should be cited as the specific single-pass formulas in S2–S4.

Ashraf–Manjunath–Sugavanam's 2026 preprint analyzes the Jacobian of a soliton–similariton laser's round-trip map and connects stability margin to simulated timing jitter and RIN [N11, full text, §§I–II]. Its stabilizing anomalous-dispersion cavity segment is essential to its comparison. It does not supply a universal stability spectrum of the amplifier segment.

### Single-shot spectra and coherence

Real-time dispersive-Fourier-transform measurements of a soliton–similariton laser have already resolved buildup, bound-state phase dynamics and intermittent instabilities [N12, abstract only]. Such measurements are not evidence that the stationary single-pass spectral covariance becomes rank one. I did not locate a paper reporting that rank limit or the $G^{-2/3}$ suppression law.

The asymptotic invariance experiment [A10] concerns repeatably reconstructed intensity and chirp for selected seeds. It is not a shot-to-shot coherence or quantum-noise measurement. Hammani et al. likewise characterize a transition using averaged characterization [A14]. Claims about coherence need an explicit observable: first-order mutual coherence, timing/phase stability of a pulse train, spectral-intensity covariance and quadrature squeezing are not interchangeable. The located cavity noise work addresses some of these separately [N4–N5, N7].

Within this search, no full quantum-noise/squeezing calculation specifically for the constant-gain parabolic amplifier similariton was found. The much broader quantum theory of nonlinear fibres does exist [N8–N10].

## Input (seed) quantum noise versus spontaneous emission

Drummond–Corney explicitly separate input-state sampling from noise injected continuously by gain/loss and Raman reservoirs [N8, full text, §6B–D of the arXiv version]. For a coherent seed, the Wigner initial condition contains vacuum fluctuations; the gain/loss noise is a separate additive term. They also explain the different noise and measurement conventions in Wigner and positive-P representations. An ASE-only calculation with a noiseless classical seed is therefore not the complete output quantum covariance of a coherently seeded amplifier.

Corney–Drummond make this distinction concrete for solitons [N9, full text, §§II–IV]: their timing variance separates initial vacuum fluctuations, amplifier noise and Raman noise. This is close prior art for the *question of propagating seed noise alongside reservoir noise*, but it is not an amplifier-similariton evaluation.

Caves gives the phase-insensitive added-noise limit and the different quadrature constraints for phase-sensitive amplification [N10, abstract only; full PDF located]. Accordingly, a reduced gain of one perturbation component relative to a linear amplifier is not by itself a demonstration of sub-shot-noise squeezing. The input quadrature covariance, conjugate quadrature, added noise and measured output mode all matter. A squeezed seed cannot be represented merely by changing the scalar spontaneous-emission factor.

For the exact requested physical setting—an already squeezed seed passing through a doped or Raman *similariton* amplifier—I found no directly matching experiment or complete quantum transfer calculation. Two related leads should not be conflated with it:

- Sawai et al. study photon-number squeezing using a noisy femtosecond fibre-amplifier source and balanced detection [N13, abstract only]. That is not evidence that a pre-squeezed input survives amplification in the gain fibre.
- A 2026 paper explicitly proposes low-noise amplification of squeezed states using cascaded fibre four-wave mixing [N14, abstract only plus system-description excerpts]. Its parametric amplifier and filtered EDFA pump have different roles; it is not the target Kerr-plus-incoherent-gain channel. Experimental validation was not established in this review.

The literature supports keeping separate accounting for seed fluctuations and reservoir fluctuations. Whether S2 includes the former correctly, and whether S3's quadrature envelopes define a physically complete quantum channel, remain claim-validation questions; this review does not answer them by extrapolating the classical asymptotic field.

## S1–S9 novelty verdicts

Verdicts concern published content, not mathematical validity. “Partly published” identifies substantive overlap while preserving the precise component not located. Confidence concerns this bibliographic judgment.

| Statement | Closest located prior work; identifier and access | Verdict | Confidence and justification |
|---|---|---|---|
| **S1:** seed-independent energy-noise law; Gaussian time/frequency process with pulse covariance | Grigoryan–Menyuk–Mu, **10.1109/50.779156**, full text, §§IIA/IIC; McKinstrie et al., **10.1364/JOSAB.19.000640**, full text, Eqs. (10)–(12); Drummond–Corney, **arXiv:quant-ph/9912095**, full text, §6 | **Published**, for the leading-order moment/noise content | **High:** arbitrary-shape moment covariances, Kerr-independent energy noise and linearized Gaussian statistics predate the claims; the Wigner notation and exact ordering convention need translation, not a new universality claim. |
| **S2:** frequency noise figure $1+3(2n_{sp}-1)(1-G^{-1/3})$, versus linear $1+(2n_{sp}-1)(1-G^{-1})$; compressed timing variance proportional to $(gL)^2$ | McKinstrie et al., **10.1364/JOSAB.19.000640**, full text; Zweck–Menyuk, **10.1364/JOSAB.35.001200**, full text | **Not found** | **Medium:** general chirped-pulse noise/dispersion conversion and similariton-cavity noise are known, but neither displayed single-pass similariton noise figure nor the stated compression asymptotic was located. |
| **S3:** $G^{1/3}$ intensity-shape and $G^{5/3}$ phase-shape power gains | Drummond–Corney, **10.1364/JOSAB.18.000139**, full text; Fedichev–Fischer, **arXiv:cond-mat/0303063**, full text; Caves, **10.1103/PhysRevD.26.1817**, abstract only | **Not found** | **Medium:** quantum fibre evolution, quadrature-sensitive amplification and scaled-background modes are published, but these similariton exponents and their claimed quantum-channel interpretation were not located. |
| **S4:** asymptotically rank-one spectral covariance and $G^{-2/3}$ residual | DFT study, **10.1038/s41598-019-50022-5**, abstract only; Zweck–Menyuk, **10.1364/JOSAB.35.001200**, full text | **Not found** | **Medium:** single-shot spectra and laser noise are established topics, but no matching rank/exponent result was found; the inspected claim's finite spectral-core mode truncation must remain explicit. |
| **S5:** $\lambda_l=(g/3)[-1\pm\sqrt{1-l(l+1)/2}]$ and breathing | Wabnitz, **10.1109/QELS.2007.4431461**, full text; Menotti–Stringari, **arXiv:cond-mat/0201158**, full text; journal Wabnitz **10.1109/LPT.2007.893823**, abstract only | **Partly published** | **Medium:** parabolic-family spiral attraction and the related polynomial collective-mode structure are published; the full stated optical sequence and exact width-mode constants were not located. |
| **S6:** all positive-width, positive-energy parabolic hydrodynamic launches converge; $\ddot s+(2/3)\dot s+s/9=1/(9s^2)$ and Lyapunov function $\dot s^2/2+s^2/18+1/(9s)$ | Wabnitz, **10.1109/LPT.2007.893823**, abstract only; conference **10.1109/QELS.2007.4431461**, full text; Wabnitz–Finot, **10.1364/JOSAB.25.000614**, full text | **Partly published** | **High for overlap, medium for residual novelty:** the same reduced attraction problem is explicitly prior art, while an equation-by-equation comparison of the rescaled width equation, arbitrary chirp and exact Lyapunov proof remains unresolved. |
| **S7:** conditional mass-coordinate convex-energy decay $e^{-gz/3}$ | Carrillo–Choi–Tse, **10.1007/s00220-018-3276-8**, full text; Huang–Marcati–Pan, **10.1007/s00205-004-0349-y**, full text; Luo–Zeng, **arXiv:1407.6111**, abstract only | **Partly published** | **Medium:** damped-Euler convergence and conditional convex-energy/transport arguments are established, but the exact optical functional and rate were not located and global smoothness cannot be imported without checking hypotheses. |
| **S8:** steep compression breaks before smooth attraction; basin needs shape constraints | Wabnitz, **10.1109/QELS.2007.4431461**, full text; Hammani et al., **10.1088/2040-8978/15/2/025202**, full text; Finot et al., **10.1364/OE.14.003161**, full text | **Partly published** | **Medium–high:** semiclassical shock restrictions and shape-sensitive transient breaking are published, but the precise “fixed energy/duration/chirp yet arbitrarily early catastrophe” construction was not located. |
| **S9:** odd-field invariant sector excludes strong global attraction; weaker density question open | Finot–Wu, **10.1142/S0218863509004944**, abstract only plus indexed body excerpts; Kruglov et al., **10.1364/JOSAB.19.000461**, full text | **Partly published** | **Medium:** phase-imprinted dark structures on a parabolic envelope are prior art, but the exact parity/orthogonality proof and topology-specific exclusion were not located. |

Several qualifications in the inspected cards are essential to these verdicts. S1 is linearized in noise, not an exact Gaussian law for the fully stochastic field. S3 reports gain envelopes, not necessarily monotone gains at every length. S4 is presently a finite-mode, stationary-phase, spectral-core statement. S5–S7 are dispersionless statements; S6 is restricted to the invariant parabolic family. S8 concerns loss of classical hydrodynamic smoothness. S9 distinguishes complex-field and uniform-core convergence from weaker density convergence. None of these qualifications is a new result from this review.

## Search and access ledger

### Searches performed

Live web search and direct public repository access were used on 2026-10-09. Searches included:

- Exact titles/DOIs for every PI starting point; author/repository searches at UCL Discovery, Southampton ePrints, HAL, Aston, arXiv and author publication pages.
- “analytical dynamics parabolic pulses”, “similariton convergence distance chirp”, “pulse transition similaritons”, “similariton Legendre stability”, “parabolic pulse perturbation spectrum”, and “similariton Barenblatt”.
- “compressible Euler damping Barenblatt physical vacuum”, “damped Euler convex energy Lagrangian exponential convergence”, and the named condensate papers.
- “similariton quantum noise squeezing”, “parabolic pulse quantum noise”, “similariton spectral covariance”, “similariton dispersive Fourier transform”, “parabolic pulses coherence”, and exact-title searches for the supplied laser-noise papers.
- “squeezed seed fiber amplifier”, “squeezed states erbium-doped amplification”, “quantum noise optical fibers Drummond Corney”, and “amplification of a squeezed quadrature”.

Reference chains were followed from McKinstrie to Grigoryan, from Wabnitz–Finot to Wabnitz's conference paper, and from the transition papers to bandwidth/Raman, phase-profile and dissipative-similariton work. OpenAlex location metadata and the HAL API were used to find author-copy URLs, not as substitutes for article evidence. Search results for laser pumps feeding squeezers were excluded as evidence of squeezed-seed amplification.

Access was uneven: several Optica downloads were denied, Southampton's identified 2002/2006 files returned authorization errors, and HAL document requests returned a bot-check page instead of PDFs. No paywall or access control was bypassed. Publicly indexed author-uploaded bodies were used where available. For A3, a publicly readable reproduction of the journal article was used after the author-repository download failed; its hosting site's generated synopsis was not used as evidence.

### Source register

Every substantive external attribution above resolves to a located source below. F = full text, A = abstract only, N = not accessed. Entries classified A despite a located PDF indicate that only the abstract/body excerpts were actually inspected sufficiently for the statements made.

| ID | Source and persistent identifier | Access; inspected content / access route |
|---|---|---|
| A1 | Fermann et al. (2000), *Self-similar propagation and amplification of parabolic pulses in optical fibers*, [10.1103/PhysRevLett.84.6010](https://doi.org/10.1103/PhysRevLett.84.6010) | **F**; theory, simulation and experiment; [UCL author copy](https://discovery.ucl.ac.uk/97897/1/97897.pdf), read through web extraction. |
| A2 | Kruglov et al. (2000), *Self-similar propagation of high-power parabolic pulses in optical fiber amplifiers*, [10.1364/OL.25.001753](https://doi.org/10.1364/OL.25.001753) | **A**; publisher/indexed author record. |
| A3 | Kruglov et al. (2002), *Self-similar propagation of parabolic pulses in normal-dispersion fiber amplifiers*, [10.1364/JOSAB.19.000461](https://doi.org/10.1364/JOSAB.19.000461) | **F**; §§2A–C and wing discussion in §3; [public journal reproduction](https://www.scribd.com/document/1034463404/2-Self-similar-Propagation-of-Parabolic-Pulses-in-Normal-dispersion-Fiber-Amplifiers-figure1-3). [Southampton record](https://eprints.soton.ac.uk/46862/) located; PDF restricted. |
| A4 | Boscolo, Turitsyn, Novokshenov & Nijhof (2002), *Self-similar parabolic optical solitary waves*, [10.4213/tmf405](https://doi.org/10.4213/tmf405); English [10.1023/A:1021402024334](https://doi.org/10.1023/A:1021402024334) | **A**; [MathNet](https://www.mathnet.ru/eng/tmf405), Aston record and indexed author manuscript fragments; no complete inspected body. |
| A5 | Kruglov & Harvey (2006), *Asymptotically exact parabolic solutions of the generalized nonlinear Schrödinger equation with varying parameters*, [10.1364/JOSAB.23.002541](https://doi.org/10.1364/JOSAB.23.002541) | **A**; publisher and author record; full-text comparison remains open. |
| A6 | Kruglov, Peacock & Harvey (2003), *Exact self-similar solutions of the generalized nonlinear Schrödinger equation with distributed coefficients*, [10.1103/PhysRevLett.90.113902](https://doi.org/10.1103/PhysRevLett.90.113902) | **A**; publisher/[Southampton](https://eprints.soton.ac.uk/46861/). |
| A7 | Wabnitz (2007), *Analytical dynamics of parabolic pulses in nonlinear optical fiber amplifiers*, [10.1109/LPT.2007.893823](https://doi.org/10.1109/LPT.2007.893823) | **A**; [Sapienza record](https://iris.uniroma1.it/handle/11573/1214370); archive-staff-only PDF. HAL record has no public file. |
| A8 | Wabnitz (2007), *Analytical Dynamics of Optical Similaritons*, JWA71, [10.1109/QELS.2007.4431461](https://doi.org/10.1109/QELS.2007.4431461) | **F**; both pages, Eqs. (1)–(3), Figs. 1–2, conclusion; [indexed author upload](https://www.researchgate.net/publication/238087766_Analytical_Dynamics_of_Optical_Similaritons). “A. Savary” in aggregator metadata is part of the address, not a coauthor. |
| A9 | Finot, Parmigiani, Petropoulos & Richardson (2006), *Parabolic pulse evolution in normally dispersive fiber amplifiers preceding the similariton formation regime*, [10.1364/OE.14.003161](https://doi.org/10.1364/OE.14.003161) | **F**; introduction, §§2–3 and indexed chirp discussion; [author upload](https://www.researchgate.net/publication/26282596_Parabolic_pulse_evolution_in_normally_dispersive_fiber_amplifiers_preceding_the_similariton_formation_regime). |
| A10 | Finot, Millot & Dudley (2004), *Asymptotic characteristics of parabolic similariton pulses in optical fiber amplifiers*, [10.1364/OL.29.002533](https://doi.org/10.1364/OL.29.002533) | **F**; theory, experiment, Figs. 1–3; [author manuscript](https://www.researchgate.net/publication/8144220_Asymptotic_characteristics_of_parabolic_similariton_pulses_in_optical_fiber_amplifiers). |
| A11 | Finot & Wu (2009), *Influence of the initial phase profile on the asymptotic self-similar parabolic dynamics*, [10.1142/S0218863509004944](https://doi.org/10.1142/S0218863509004944) | **A**, with indexed setup/figure excerpts; [HAL](https://hal.science/hal-00469842), author-upload record and abstract located. HAL deposit date is not journal publication year. |
| A12 | Billet, Dudley, Joly & Knight (2005), *Intermediate asymptotic evolution and photonic bandgap fiber compression of optical similaritons around 1550 nm*, [10.1364/OPEX.13.003236](https://doi.org/10.1364/OPEX.13.003236) | **A**; [institutional PDF](https://pure.mpg.de/rest/items/item_3608865_1/component/file_3608866/content) located; abstract/introduction inspected. |
| A13 | Wabnitz & Finot (2008), *Theory of parabolic pulse propagation in nonlinear dispersion-decreasing optical fiber amplifiers*, [10.1364/JOSAB.25.000614](https://doi.org/10.1364/JOSAB.25.000614) | **F**; introduction, model and §3; [author manuscript](https://www.researchgate.net/publication/43165547_Theory_of_parabolic_pulse_propagation_in_nonlinear_dispersion-decreasing_optical_fiber_amplifiers). |
| A14 | Hammani, Boscolo & Finot (2013), *Pulse transition to similaritons in normally dispersive fibre amplifiers*, [10.1088/2040-8978/15/2/025202](https://doi.org/10.1088/2040-8978/15/2/025202) | **F**; introduction, propagation regimes, experiment discussion and references; [Aston PDF](https://publications.aston.ac.uk/id/document/36307). Online manuscript/deposit dates precede volume year. |
| A15 | Soh, Nilsson & Grudinin (2006), *Efficient femtosecond pulse generation using a parabolic amplifier combined with a pulse compressor. I. Stimulated Raman scattering effects*, [10.1364/JOSAB.23.000001](https://doi.org/10.1364/JOSAB.23.000001) | **A**; [Southampton manuscript](https://eprints.soton.ac.uk/411466/1/3216.pdf) abstract. |
| A16 | Same authors (2006), Part II, *Finite gain-bandwidth effect*, [10.1364/JOSAB.23.000010](https://doi.org/10.1364/JOSAB.23.000010) | **A**; publisher/author-upload abstract. |
| A17 | Bale & Boscolo (2010), *Impact of third-order fibre dispersion on the evolution of parabolic optical pulses*, [10.1088/2040-8978/12/1/015202](https://doi.org/10.1088/2040-8978/12/1/015202) | **A**; [Aston record](https://research.aston.ac.uk/en/publications/impact-of-third-order-%EF%AC%81bre-dispersion-on-the-evolution-of-parabol/). Related SPIE paper [10.1117/12.854782](https://doi.org/10.1117/12.854782) located but not substituted for journal full-text access. |
| A18 | Bale & Kutz (2009), *Analytic theory of self-similar mode-locking with rapidly varying, mean-zero dispersion*, [10.1117/12.837774](https://doi.org/10.1117/12.837774) | **F**; §§2–4; [Aston PDF](https://publications.aston.ac.uk/id/eprint/33270/1/73860M_1_.pdf). |
| A19 | Dudley, Finot, Richardson & Millot (2007), *Self-similarity in ultrafast nonlinear optics*, [10.1038/nphys705](https://doi.org/10.1038/nphys705) | **A**; publisher and author record; used as a literature-map lead, not primary proof of a theorem. |
| M1 | Huang, Marcati & Pan (2005), *Convergence to the Barenblatt solution for the compressible Euler equations with damping and vacuum*, [10.1007/s00205-004-0349-y](https://doi.org/10.1007/s00205-004-0349-y) | **F**; introduction, Theorem 1.1 and remarks; [author PDF](https://panrh.math.gatech.edu/publications/Damping/baren4.pdf). |
| M2 | Luo & Zeng (2016), *Global existence of smooth solutions and convergence to Barenblatt solutions for the physical vacuum free boundary problem of compressible Euler equations with damping*, [arXiv:1407.6111](https://arxiv.org/abs/1407.6111), [10.1002/cpa.21562](https://doi.org/10.1002/cpa.21562) | **A**; abstract read, arXiv full PDF obtained but proof not inspected. |
| M3 | Carrillo, Choi & Tse, *Convergence to equilibrium in Wasserstein distance for damped Euler equations with interaction forces*, [10.1007/s00220-018-3276-8](https://doi.org/10.1007/s00220-018-3276-8) | **F**; §§1–2, theorem scope and explicit-rate caveats; [public PDF](https://d-nb.info/1171286597/34). |
| M4 | Menotti & Stringari (2002), *Collective oscillations of a 1D trapped Bose gas*, [arXiv:cond-mat/0201158](https://arxiv.org/abs/cond-mat/0201158) | **F**; hydrodynamic linearization and mean-field profiles; arXiv PDF. |
| M5 | Fedichev & Fischer (2004), *“Cosmological” quasiparticle production in harmonically trapped superfluid gases*, [arXiv:cond-mat/0303063](https://arxiv.org/abs/cond-mat/0303063) | **F**; scaling equations and §IV mode expansion; arXiv PDF. |
| M6 | Zeng, *Time-asymptotics of physical vacuum free boundaries for compressible inviscid flows with damping*, [arXiv:2003.14072](https://arxiv.org/abs/2003.14072) | **A**; later free-boundary asymptotics lead; not used to assign the optical rate. |
| N1 | Grigoryan, Menyuk & Mu (1999), *Calculation of timing and amplitude jitter in dispersion-managed optical fiber communications using linearization*, [10.1109/50.779156](https://doi.org/10.1109/50.779156) | **F**; §§I–II, Gaussian-statistics discussion; [UMBC PDF](https://photonics.umbc.edu/wp-content/uploads/sites/688/2022/02/PAJ123.pdf). Pages 1348/1350 visually checked. |
| N2 | McKinstrie, Santhanam & Agrawal (2002), *Gordon–Haus timing jitter in dispersion-managed systems with lumped amplification: analytical approach*, [10.1364/JOSAB.19.000640](https://doi.org/10.1364/JOSAB.19.000640) | **F**; §§2–3, conclusion and references; [author PDF via web cache](https://labsites.rochester.edu/agrawal/wp-content/uploads/2019/08/paper_2002_03.pdf); direct download failed. |
| N3 | Santhanam & Agrawal (2003), *Raman-induced spectral shifts in optical fibers: general theory based on the moment method*, [10.1016/S0030-4018(03)01561-X](https://doi.org/10.1016/S0030-4018(03)01561-X) | **A**; [publisher](https://www.sciencedirect.com/science/article/pii/S003040180301561X). |
| N4 | Zweck & Menyuk (2018), *Computation of the timing jitter, phase jitter, and linewidth of a similariton laser*, [10.1364/JOSAB.35.001200](https://doi.org/10.1364/JOSAB.35.001200) | **F**; introduction, cavity model, timing/phase definitions; [UMBC PDF](https://photonics.umbc.edu/wp-content/uploads/sites/688/2022/02/PAJ284.pdf). |
| N5 | Song, Jung & Kim (2011), *Impact of pulse dynamics on timing jitter in mode-locked fiber lasers*, [arXiv:1102.1046](https://arxiv.org/abs/1102.1046), [10.1364/OL.36.001761](https://doi.org/10.1364/OL.36.001761) | **F**; experiment and interpretation; arXiv author manuscript. |
| N6 | Ilday et al. (2004), *Self-similar evolution of parabolic pulses in a laser*, [10.1103/PhysRevLett.92.213902](https://doi.org/10.1103/PhysRevLett.92.213902), [arXiv:physics/0402013](https://arxiv.org/abs/physics/0402013) | **A**; arXiv/publisher abstract; author full PDF located. |
| N7 | Liao et al. (2020), *Spontaneous emission noise in mode-locked lasers and frequency combs*, [10.1103/PhysRevA.102.013506](https://doi.org/10.1103/PhysRevA.102.013506), [arXiv:2004.00763](https://arxiv.org/abs/2004.00763) | **F**; introduction and Gaussian model setup; arXiv PDF. |
| N8 | Drummond & Corney (2001), *Quantum noise in optical fibers. I. Stochastic equations*, [10.1364/JOSAB.18.000139](https://doi.org/10.1364/JOSAB.18.000139), [arXiv:quant-ph/9912095](https://arxiv.org/abs/quant-ph/9912095) | **F**; initial states, Wigner/positive-P noise, operator ordering; §6 of arXiv PDF. |
| N9 | Corney & Drummond (2001), *Quantum noise in optical fibers. II. Raman jitter in soliton communications*, [arXiv:quant-ph/9912096](https://arxiv.org/abs/quant-ph/9912096) | **F**; §§II–IV, particularly Eq. (3.18); seed versus reservoir terms. |
| N10 | Caves (1982), *Quantum limits on noise in linear amplifiers*, [10.1103/PhysRevD.26.1817](https://doi.org/10.1103/PhysRevD.26.1817) | **A**; abstract/intro excerpts; [Caltech PDF](https://painterlab.caltech.edu/wp-content/uploads/2019/06/qe_caves_limits_amplifiers.pdf) obtained. |
| N11 | Ashraf, Manjunath & Sugavanam (2026), *Stability analysis and quantum-limited noise properties of the soliton-similariton fiber laser*, [arXiv:2603.08467](https://arxiv.org/abs/2603.08467) | **F**; §§I–II and indexed noise-results discussion; v1 preprint, not treated as a journal theorem. |
| N12 | *Real-time characterization of spectral instabilities in a mode-locked fibre laser exhibiting soliton-similariton dynamics* (2019), [10.1038/s41598-019-50022-5](https://doi.org/10.1038/s41598-019-50022-5) | **A**; abstract and conclusion excerpts; [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6764988/). |
| N13 | Sawai et al. (2013), *Photon-number squeezing with a noisy femtosecond fiber laser amplifier source using a collinear balanced detection technique*, [10.1364/OE.21.025099](https://doi.org/10.1364/OE.21.025099) | **A**; publisher/PubMed abstract. |
| N14 | *Low-noise amplification of coherent single-mode squeezed states* (2026), [10.3390/photonics13010051](https://doi.org/10.3390/photonics13010051) | **A**, plus indexed §2.1 system-description excerpts; [publisher](https://www.mdpi.com/2304-6732/13/1/51); full-page request rate-limited. |
| N15 | Gordon & Haus (1986), *Random walk of coherently amplified solitons in optical fiber transmission*, [10.1364/OL.11.000665](https://doi.org/10.1364/OL.11.000665) | **A**; [publisher abstract](https://opg.optica.org/ol/abstract.cfm?uri=ol-11-10-665) independently read; foundational soliton frequency-to-timing random walk, not a similariton calculation. |

### Limits of the negative findings

The unresolved full texts with greatest potential to change S5–S6 are Wabnitz's journal paper and Kruglov–Harvey (2006). Finot–Wu requires a complete body/figure comparison before sharpening S9. The seed-noise search found general quantum propagation and adjacent parametric schemes, but did not exhaust theses, non-English literature or all citation descendants. These access and coverage limits warrant follow-up; they are not evidence that the corresponding work does not exist.
