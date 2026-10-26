---
agent: gpt-h
model: gpt-6-astra
family: gpt
date: 2026-10-20
task: T-20261020-claude-interactive-06
---

# Cross-family novelty review of the three Claude optical-thermalization cards

## Recommendation

Only the **isolated Hamiltonian DNLS dynamics** survives this review as a defensible high-novelty problem. Its optical realization remains a feasibility question. Neither a new fit to a self-cleaning threshold nor the proposed six-wave coefficient calculation clears the PI's bar.

| Card | Verdict and card action | Decisive evidence |
|---|---|---|
| P-20261020-claude-interactive.22-01 | **Novelty lowered: high → medium; candidate retained.** Correct the assertion that no mechanism predicts nonlinear-phase scaling. | Krupa 2017 supplementary mean-field argument [S1]; Ferraro 2023 explicitly discusses power × length [S8]. The two-length experiments do not establish a controlled exponent discrimination. |
| P-20261020-claude-interactive.22-02 | **Audited, high retained for the corrected isolated-dynamics question.** Both families recorded. Replace the automatic-Gibbs-background assumption and qualify optical feasibility. | Iubini–Politi 2025 [D11] supplies reservoir metastability but leaves isolated multibreather statistics/dynamics unresolved. Iubini 2019 [D8] and Politi 2022 [D9] substantially constrain what would count as new. |
| P-20261020-claude-interactive.22-03 | **Novelty lowered: medium → low; candidate retained.** Mark its first coefficient target as pre-empted. | Sutherland–Yim 2026, §§6–7 [F8], already gives the relevant general kernel, cancellation condition and constant-vertex small-cubic-dispersion behavior. |

I do **not** recommend declaring any entire card solved on the evidence read. I recommend removing -01 and -03 from the high-novelty shortlist. The PI decides demotion and card consolidation. No claim/result promotion is involved.

## Protocol and limits

The session began at 17:01 EDT on 2026-10-20. I first read AGENTS.md, the workflow's problem statuses, STATUS.md and automation/policy.yaml, then the three cards' target/model, longstanding-evidence and first-derivation sections. I ran independent kill searches and read primary sources before reading the cards' Kill search sections or the Claude scouting review. Commit b698147 preserves that independent checkpoint, including the Krupa-SI, DNLS-lifetime and Sutherland–Yim findings. I subsequently read the Claude review's relevant S1/S3/S5 sections, comparison, search/source ledgers and relevant appendices, then the GPT review and gpt-g-02 on origin/task/T-20261020-claude-interactive-03.

This is a literature review, not an independent propagation verification. “No closure found” refers to the searches below, not to a proof of absence. The ledger specifies the sections inspected; downloading a PDF does not constitute reading it. Inherited access claims were not treated as my own access.

Direct HTTP requests used the generic User-Agent Mozilla/5.0, without contact fields or identifying requester data. Open PDFs and extracted text are outside the repository at ~/analytical-nl-discovery-data/lit-T-20261020-claude-interactive-06/. Publisher errors and access restrictions were respected. No other clone, private conversation history, claim, result, solver code or generated file was changed. Follow-up through the scouts is distinguished from the independent pass.

## Card -01: self-cleaning threshold and length

### (a) Longstanding evidence

The short Aschieri 2011 quotation is accurate (journal p. 033838-8, with a typographic ligature). It establishes slow multimode equilibration in that model, before the self-cleaning experiments; it is not a statement of an unexplained inverse-length threshold. Fusaro 2019's abstract quotation is also accurate, but that paper's contribution is precisely an acceleration mechanism [S3–S4].

Ferraro 2023's controversy quotation is accurate, as are its discussions of disorder-dependent thresholds and an unresolved launch-angle separatrix. However, the same review already identifies accumulated nonlinear phase as the relevant empirical parameter near its beginning [S8]. Ferraro 2025's limitation of purely spatial kinetics and its mixed coherent–incoherent discussion are accurate [S9]. They support an unfinished quantitative crossover theory, not the title's stronger assertion that no mechanism predicts the power-length scaling.

Krupa's SI is decisive: its p. 5 mean-field argument already links shortening the fibre and raising power; p. 11 invokes the power-length product in discussing the shorter fibre [S1]. The old card used the latter but did not account for the former. The Wright 2022 interpretation was not independently full-text audited here; it is not needed for this verdict.

### (b) Kill search

The weak-disorder collision rate has quadratic dependence on nonlinear strength when its linear disorder statistics are fixed [S4–S5]. That law cannot be extrapolated into the coherent regime. Garnier 2019 already simulates mixed coherent/incoherent behavior and limits quantitative comparison with pulsed experiments. Podivilov's instability threshold is a threshold for growth: detecting substantial conversion after a finite length also involves its growth rate, seed and observation criterion. Listing this as a universal measured exponent zero is misleading [S6].

Baudin 2023 connects coherent-launch cleaning with incipient RJ evolution [S7]. Sidelnikov 2019 studies random coupling models [S11]. Mangini 2023 measures modal phase locking, and Leventoux 2021 resolves intrapulse exchange [S12–S13]. These make phase and time-resolved observables necessary; a clean averaged image and an RJ fit are not interchangeable tests of irreversible equilibration.

The newer candidates do not close the corrected question: Chao 2025 addresses bending/quasi-resonance robustness; Kabat 2025 derives rate dependence on supermode correlations within weak-nonlinearity kinetics; Zitelli develops equilibrium thermodynamics; Zanaglia treats a stationary temporal continuum [S14–S17]. None supports a claim that all rate theory is absent. Liu 2016 was located and its primary abstract read, but its full text remains an access gap [S2].

### (c) Novelty if solved

A controlled, launch- and disorder-resolved crossover with an identifiable irreversible rate could be substantial. The exponent one alone would not be. In a homogeneous cubic resonant equation, $A_m=\sqrt P\,b_m$ and $\zeta=\gamma Pz$ remove power from the dimensionless trajectory for a fixed normalized launch. A fixed trajectory criterion then has fixed nonlinear phase. This is my inference from the model; it proves neither mixing nor an RJ endpoint. Recovering it with an adjustable resonance width is a modest adaptation.

### (d) Foothold

The proposed replacement $\Gamma_{\rm eff}=\max(\Delta\beta,\kappa/L_{\rm NL})$ inserts the desired crossover unless correlation decay and $\kappa$ are independently derived. A positive Lyapunov exponent does not itself supply a mixing time. Static splitting can detune useful resonances; it need not monotonically restore ergodicity.

A better first target is a coherent-to-kinetic crossover for one measured modal tensor and specified launch ensemble: derive a phase-correlation decay law and its relation to an occupation-relaxation criterion, retaining memory when $\Delta\beta L_{\rm NL}\lesssim1$. First test whether a single length controls both observables. The launch needs phases/correlations as well as mode count and mean linear energy. This is narrower than a universal threshold law but more meaningful than assuming a broadening closure.

### (e) Optical relevance and exponent evidence

| Data set | Primary-source check | What it establishes |
|---|---|---|
| Krupa 2017 [S1] | Main figures and SI pp. 5, 11–12; shorter-fibre images and $M^2$ plot visually inspected. Main Fig. 4 is a cut-back at fixed high power. | The 3 m/12 m comparison qualitatively supports the power-length interpretation. The short-fibre $M^2$ plateau and long-fibre FWHM statistic differ in diagnostic and sampling. They are not a common-criterion exponent fit with uncertainty. |
| Pourbeyram 2022 [S10] | Fig. 4/caption, pulse description and associated discussion; figure visually inspected. | The 0.5 m sample reaches the reported RJ-like endpoint by the highest tested power; the 1.5 m curve levels earlier. The short-fibre endpoint bounds a crossing rather than determining it precisely. Ultrashort-pulse evolution complicates comparison with a monochromatic model. |
| Deliancourt 2019 [S18] | Geometry, threshold discussion and Fig. 9 cut-back description. | Small end cut-backs test persistence of an optimized output mode, not a multi-length threshold scan. |

The scout's ratios/exponents are in run 2026-10-20-claude-interactive.22-resonance-kinematics/threshold_exponents.json. I did not digitize new data or assign statistical confidence. I reject describing the Krupa comparison as rigorously like-for-like or claiming that these data decisively exclude $L^{-1/2}$. The literature's nonlinear-phase interpretation is real; the strength of the exponent test is overstated. The illustrative disorder length used to place the experiments in a regime was not measured in either fibre.

A decisive experiment would use a common time-gated modal/phase criterion at several cut-back lengths, fixed launch statistics, measured disorder and propagation-dependent power. That is credible as a new experiment, not as already-existing proof of the proposed paradox.

### (f) Repository fit

P-005 owns joint mode–frequency equilibration; P-010 owns a finite-length, detector-defined cleaning threshold with duration, walk-off, nonlinearity and disorder. A strictly quasi-CW coherent crossover is distinguishable but substantially overlaps P-010. Assign one home before derivation. Validated random linear coupling and phase-sensitive ensemble diagnostics remain oracle needs. I did not inspect or alter linked claim derivations.

## Card -02: isolated non-Gibbs DNLS dynamics

### (a) Longstanding evidence

Rasmussen 2000's transition, long transients and missing high-energy distribution are genuine early motivations [D1]. Rumpf 2004/2008 already derive substantial equilibrium and metastability information [D3–D4]. Describing the former as containing no dynamics is too broad: it discusses pinning, exchange and failure to attain the entropy maximum.

The card's 2013 evidence mixes versions. The sentence about equilibrium convergence never having been observed appears in the short arXiv:1203.4162v1 precursor. I separately read the institutional NJP PDF. Its density exponent and future-universality discussion concern **microcanonical Monte Carlo**, not a measured coarsening law of full Hamiltonian DNLS. The journal's deterministic simulations and conclusion instead emphasize slower, apparently stationary multibreather evolution [D5].

Mithun 2018's unknown-distribution quotation and the 2021 review's freezing statement are accurate in context [D6–D7]. Later finite-size and metastability results must now qualify them. Iubini–Politi 2025 explicitly identifies a generalized statistical description of multibreathers as unfinished [D11]. Kabat 2026's future-work passage follows both non-Gibbs and disorder extensions; it does not establish an isolated coarsening law or an automatically Gibbsian conditioned background [D15]. Together these support the corrected longstanding question.

### (b) Kill search

| Prior result | Consequence |
|---|---|
| Rasmussen; Johansson–Rasmussen; Rumpf 2004/2008; Cherny et al. [D1–D4, D16] | Phase boundaries, localization thermodynamics and ensemble distinctions are old. Optical terminology does not make them new. |
| Rumpf 2007/2009 [D17–D18] | Growth/erosion and metastable entropy are direct prior-art checks for a bath-plus-breather calculation. The 2007 primary full text remains unaccessed; 2009 was checked at primary abstract level. No kill rests on assuming their full contents. |
| Iubini 2013/2017 [D5, D19] | Stochastic surrogate coarsening theories exist. Their clock/exchange rule cannot be relabeled as DNLS propagation. |
| Iubini 2019; Politi 2022 [D8–D9] | Exponential single-breather lifetime/hopping laws and systematic adiabatic-invariant analysis exist. The card's assertion that there is no time-scale law is false. The controlled 2022 construction uses unidirectional coupling; rare jumps and full backreaction remain a gap. |
| Gradenigo 2021; Giachello 2025 [D10, D12] | Finite-size localization and equilibrium distributions are substantial prior theory. Hamiltonian dynamics and nonfactorizing microcanonical subsystems constrain any independent-bath approximation. |
| Iubini–Politi 2025; Giusfredi 2026 [D11, D13] | Reservoir metastability and mean-field negative-temperature states do not supply isolated collective coarsening. The mean-field paper leaves subsequent localization dynamics outside its scope. |
| Ramos 2020; Shi 2021; Kabat 2026 [D14–D15, D20] | Optical networks, band-resolved prethermalization and strong-nonlinearity Gibbs thermodynamics are known, but not the requested isolated non-Gibbs exchange process. |
| Rumpf–Newell 2025 [D21] | The primary abstract concerns driven/damped MMT turbulence and coherent pulses. It does not claim isolated DNLS coarsening; full text unavailable. |

### (c) Novelty if solved

I could not kill a predictive law for **isolated deterministic multibreather exchange, coarsening or arrest**, retaining phase dynamics and finite-background backreaction. It would connect known equilibrium localization to its slow dynamical approach. This is the high-novelty part that I audit. Static entropy maximization, reproduction of an exponential lifetime, or observing a localized optical spot would not meet that bar.

Specify an initial ensemble and graph: $(a,\delta,N)$ do not uniquely determine a prethermal state or first-passage distribution. The answer may include persistent memory or an arrest probability instead of a universal relaxation time.

### (d) Foothold

The original MB-GGE construction is not yet a defensible first result. A breather's **dressed adiabatic action** is not its exact instantaneous power; a fitted cutoff $A_*$ would add a free closure. Fixing several actions does not prove that the remaining finite subsystem lies in the ordinary Gibbs region. The 2025 PRL already proposes the ensemble idea, and Giachello's correlations make the independence issue concrete [D8–D12].

Use the GPT card's narrower target: derive or falsify a conditional rare-jump kernel for one tall breather's dressed action in a specified **microcanonical** background, retaining exact norm/energy exchange and backreaction. Establish when a Markov reduction is valid before composing two-breather transfers into a coarsening law. A conditional flux or first-passage distribution is a discriminating first test.

### (e) Optical relevance, finite size and Raman

The coupled-core mapping is credible; the laboratory window is unestablished. Three corrections precede simulation or experiment:

1. **Actual launch energy.** Random phases remove hopping energy in the ensemble mean, not in each shot. For $k$ equally powered lit sites, $\mathbb E[h/a^2]=N/k$. The per-shot identity holds if occupied sites have no connecting edges, or if hopping is explicitly controlled. Measure phases or condition on the actual conserved $H$; intensities alone do not determine it.
2. **Graph/finite size.** A ring and a hexagonal cluster have different Hamiltonians. The ground state $a^2-2a$ needs the degree-two bipartite ring, not every odd ring or hexagonal graph. The line $2a^2$ is the usual thermodynamic reference, not an exact small-graph localization boundary. Gradenigo's asymptotic matching gives an excess-density scale $N^{-1/3}$ in its regime [D10], not a calibration of the proposed few-core arrays.
3. **Optical novelty.** Iubini 2013 already discusses optical-waveguide localized states as preliminary evidence for this energy region [D5, §5]. The Science 2023 experiment realizes negative-temperature RJ processes in a bounded-band time-synthetic lattice [D22], not the requested full-DNLS coarsening. The later Joule–Thomson experiment uses laser-written multicore waveguide arrays [D23]. Withdraw the categorical claim that no optical system entered this region. No controlled optical measurement of the requested collective law was found in this search.

**Raman check.** The scout's raman_budget.json assumes a small-signal threshold exponent of 16 and specified silica coefficients. Under those assumptions,

$$G_R\simeq \frac{g_RP_{\rm hot}L_{\rm eff}}{A_{\rm eff}},\qquad
\Phi_{\max}\simeq16\frac{2\pi n_2}{\lambda g_R}.$$

Its approximate 25-radian budget is an engineering estimate, not a universal hard limit; the threshold gain factor depends on the setup [D24]. For lit fraction $f=k/N$ and approximately fixed hot-core power, $\gamma P_{\rm hot}=2aC/f$, giving $CL\lesssim\Phi_{\max}f/(2a)$. This explains the scout's short quasi-CW window under its assumptions, not through a propagation calculation.

Short pulses do not automatically permit longer propagation. Walk-off must occur before substantial gain accumulates: approximately $\gamma P_{\rm hot}L_W\lesssim\Phi_{\max}$ in the same simplified model. Merely requiring $L_W<L$ and $L\ll L_D$ is insufficient. The pulsed gain condition is also discussed in Headley–Agrawal [D25]. A real array requires pump/Stokes group velocities and different couplings, evolving localized powers and gain integrated along Stokes characteristics. Spectral broadening and pulse reshaping also matter. The assertion that the proposed pulses permit $CL$ of order $10^2$ is **unverified**.

An arithmetic check makes the problem concrete: [run 2026-10-20-gpt-h-raman-walkoff-check](../runs/2026-10-20-gpt-h-raman-walkoff-check/summary.json) uses $N=19$, $k=6$, $a=0.5$, $C=10\,{\rm m}^{-1}$ and an explicitly assumed $A_{\rm eff}=80\,\mu{\rm m}^2$, with the scout's silica coefficients. It requires about 16.5 kW in a lit core, within the proposed power range. For the scout's 3 ps pulse/walk-off estimate, the assumed small-signal Raman threshold is reached after about 0.776 m ($CL\simeq7.76$), before the 1.81 m walk-off length. Gain accumulated before separation is about 2.33 times the assumed threshold. This is an illustrative fixed-power consistency check, not a calibrated propagation prediction or a proof that every possible fibre fails.

An early formation or individual exchange event may be accessible. The estimates do not demonstrate late coarsening or single-condensate formation inside silica fibre. High novelty is conditional on a physically testable reduced prediction, not on presumed observation of the ultimate asymptote.

### (f) Repository fit

Scalar spatial DNLS is a tractable reduced evaluator. Calibrated coupling, full energy diagnostics, convergence checks and rare-event sampling remain necessary. Dispersion/Raman/loss must relax the ideal assumptions in the lab audit. The existing cheap-oracle task should use phase-dependent energy and distinct graphs before scanning nominal $(a,\delta)$. This is the same central scientific problem as gpt-g-02.

## Card -03: frequency-local invariant relaxation

### (a) Longstanding evidence

Suret 2010 treats a vector optical experiment/model; Michel 2011 explicitly develops the scalar TOD example and its kinetic invariant [F1–F2]. The 2014 quotation is accurate only with its surrounding scope: **experimental observation** of anomalous thermalization, specifically the vector experiment limited by Raman [F3, §6.2.3]. It does not identify this scalar post-plateau decay law as an explicit longstanding theoretical problem.

The Onorato 2023 quotation is accurate in the conclusions but concerns one-dimensional chains and the joint particle-number/nonlinearity limit [F4]. Vassilev asks about kinetic theory where the leading kernel is trivial; its dispersion class differs from the cubic-dispersion pair-exchange plane here [F5]. These motivate methods, not the precise optical gap. The card partly acknowledged this distinction; an implicit question should not become an explicit open-problem quotation.

### (b) Kill search

The first target is substantially pre-empted. Sutherland–Yim [F8, §§6–7] gives the effective six-wave kernel for quadratic-plus-cubic dispersion and a general quartic vertex on the generic resonant set. Its constant-vertex specialization applies directly to instantaneous Kerr nonlinearity. In its notation $B$ is the **local cubic nonlinear coefficient**, not cubic dispersion; $D$ is the nonlocal mean-flow coefficient. The old interpretation of $BD$ is wrong.

The paper supplies a Hirota cancellation relation and the denominator identity, Eq. (7.4). On a fixed compact quadratic-resonance patch with nonzero internal denominators, the pure local-vertex contribution has no term linear in small cubic dispersion and is generically second order. Repeating this cancellation in fibre notation is not new. The paper does not derive the requested near-zero-dispersion kinetic relaxation length.

Onorato 2015 and Lvov–Onorato 2018 already predict/test six-wave-controlled FPUT equipartition times [F6–F7], not this optical model. Barviau 2013 changes the **four-wave** geometry with fourth-order dispersion [F9]; such drift of $J$ must be separated from higher-order collisions. Hirota and Sasa–Satsuma integrability require particular derivative-nonlinearity combinations. Generic optical self-steepening cannot be identified with either just because a third derivative is present [F8, F10].

### (c) Novelty if solved

A uniform mixed four-/six-wave kinetic description at the pair-exchange plane could still be a substantial mathematical advance. The proposed first calculation and quotations establish neither its novelty nor an accessible optical regime. Low confidence applies to this card as a high-novelty optical candidate, not to a claim that all higher-order kinetic theory is solved or easy. A general Hamiltonian result can pre-empt a fibre calculation despite its water-wave motivation.

### (d) Foothold and residual problem

The fixed-band small-$\beta_3$ expansion is nonuniform here: at fixed $\beta_2$, the special plane moves to frequencies of order $1/\beta_3$, while this card needs spectra near that plane. The generic six-wave formula excludes zero internal denominators. A uniform construction must retain resonant quartic channels and avoid double-counting successive four-wave events as a six-wave collision. Specify the limiting procedure, broadening/memory treatment and convergence requirements.

Before derivation, formulate that residual problem and a viable conservative observation window. Define change or projected relaxation of $J$ relative to its initial/equilibrium value, not decay to zero: conserved spectral momentum constrains an odd moment of $J$, and general equilibrium need not be reflection symmetric about $\Omega_z$. Merely finding $J\ne0$ does not distinguish anomalous kinetics from every RJ state.

### (e) Optical relevance and lab test

The original run 2026-10-20-claude-interactive.22-resonance-kinematics/raman_budget.json already puts its nominal six-wave length far beyond the silica Raman budget. Those estimates omit the identified vertex suppression and are not validated predictions. The four-wave experiment tests the old mechanism, not access to the new conservative stage. Hollow-core proposals need actual dispersion, nonlinearity, loss and bandwidth. An amplified loop changes the conservation assumptions and needs a separate model.

A statement that the first observation is still missing in 2026 cannot follow from a 2014 review alone. The documented search found no controlled measurement of the precise conservative post-plateau law; it does not prove the absence of all later anomalous-thermalization observations.

### (f) Repository fit

GNLSE propagation ingredients are available, but long-time $J$ diagnostics need checks of the reflection plane, exact versus approximate invariants, momentum, window, spectral cutoff, step size and nonlinear aliasing. A linear null test cannot validate a tiny nonlinear drift. Integrable controls and separate $\beta_4$/Raman contributions are needed. This remains a scope/feasibility task.

## Overlap with P-20261020-gpt-g-02

**Merge, with P-20261020-gpt-g-02 as the home.** Its central observable, isolated Hamiltonian multibreather coarsening/first-passage time, is the mechanism required for the Claude finite-fibre relaxation length. A finite number of cores does not create a second independent high-novelty problem.

The GPT card already makes dressed-action jumps, backreaction, initial ensembles and possible arrest central. Import the Claude optical normalization, core/phase observables and corrected Raman gate as a realization section or linked task. Preserve both original cards and audit trails until the PI decides how to mark the duplicate. I did not edit the GPT card or interfere with its Claude-family reviewer.

A distinct finite-array problem would need a graph-dependent prediction beyond straightforward application of finite-size equilibrium theory and a viable propagation window. Neither has been shown.

## Comparison with the scouts

| Direction | Added/corrected here | Claude findings beyond my first pass |
|---|---|---|
| Self-cleaning | Original SI mean-field scaling; finite-gain threshold distinction; weaker exponent evidence than claimed; full-text Chao/Kabat checks. | Concentrated two-length evidence, 2025 mixed-regime limitation, phase locking, time-resolved diagnostics and registry ownership issues. The scout already recorded threshold ambiguity; the disagreement is its inference's strength. |
| DNLS | Stochastic origin of the 2013 exponent, existing lifetime laws, nonautomatic Gibbs background, phase-dependent energy, graph dependence and walk-off gain condition. | The 2025 MB-GGE suggestion, 2026 interacting-RJ extension, optical mapping and first Raman budget. |
| Local invariant | Full kernel analysis establishes pre-emption, coefficient misidentification and nonuniformity; primary checks of quotation scope. | The water-wave preprint was already flagged as the closest threat, but only abstract-read. The scout's factorization and Raman scale comparison sharpened the issue. |

The GPT review independently parked -01 and broad six-wave thermalization for overlapping reasons. Agreement is not used as evidence. The GPT card led to the later Giachello 2025 and Giusfredi 2026 checks; these were follow-ups, not independent first-pass discoveries.

## Source ledger: my access, not inherited access

“Full text” means the specified sections were read in a primary manuscript/PDF, not that every equation in a long review was audited. “Abstract only” includes explicitly indicated publisher previews. “Not accessed” is not negative evidence. All access was on 2026-10-20. Numerical observations trace to primary figures or the existing scout run, not a new simulation.

### Self-cleaning

| Key | Primary identifier | Access and inspected material |
|---|---|---|
| S1 | Krupa 2017, [DOI:10.1038/nphoton.2017.32](https://doi.org/10.1038/nphoton.2017.32), [arXiv:1603.02972](https://arxiv.org/abs/1603.02972) | **Full text:** main experimental/mean-field discussion and figures; publisher SI pp. 5, 11–12. |
| S2 | Liu 2016, [DOI:10.1364/OL.41.003675](https://doi.org/10.1364/OL.41.003675) | **Abstract only:** publisher/institutional record. Full PDF unavailable; no assertion about an unseen length scan. |
| S3 | Aschieri 2011, [DOI:10.1103/PhysRevA.83.033838](https://doi.org/10.1103/PhysRevA.83.033838) | **Full text:** model, abstract, p. 8 slow-mode-count passage; APS PDF. |
| S4 | Fusaro 2019, [DOI:10.1103/PhysRevLett.122.123902](https://doi.org/10.1103/PhysRevLett.122.123902), [arXiv:2011.05111](https://arxiv.org/abs/2011.05111) | **Full text:** abstract, disorder model and kinetic-rate equations. |
| S5 | Garnier 2019, [DOI:10.1103/PhysRevA.100.053835](https://doi.org/10.1103/PhysRevA.100.053835), [arXiv:2011.03918](https://arxiv.org/abs/2011.03918) | **Full text:** coherent/mixed regimes, kinetic hypotheses and conclusions. |
| S6 | Podivilov 2019, [DOI:10.1103/PhysRevLett.122.103902](https://doi.org/10.1103/PhysRevLett.122.103902), [arXiv:1811.10239](https://arxiv.org/abs/1811.10239) | **Full text:** main model, instability threshold and conclusion. |
| S7 | Baudin 2023, [arXiv:2309.02215](https://arxiv.org/abs/2309.02215), DOI:10.1016/j.optcom.2023.129716 | **Full text:** abstract and coherent-launch/incipient thermalization discussion; not every simulation checked. |
| S8 | Ferraro et al. 2023, [arXiv:2304.12006](https://arxiv.org/abs/2304.12006), DOI:10.1080/23746149.2023.2228018 | **Full text:** power-length discussion, controversy, threshold/separatrix and equilibrium interpretation. |
| S9 | Ferraro et al. 2025, [arXiv:2505.11299](https://arxiv.org/abs/2505.11299), DOI:10.1016/j.physd.2025.134758 | **Full text:** §§2.2, 2.5, 4 and relevant conclusions; not a full equation audit. |
| S10 | Pourbeyram 2022, [DOI:10.1038/s41567-022-01579-y](https://doi.org/10.1038/s41567-022-01579-y), [arXiv:2012.12110](https://arxiv.org/abs/2012.12110) | **Full text:** main experiment, Fig. 4/caption and pulse/length discussion. |
| S11 | Sidelnikov 2019, [arXiv:1908.07745](https://arxiv.org/abs/1908.07745), DOI:10.1016/j.yofte.2019.101994 | **Full text:** abstract, coupled-mode/random-coupling model. |
| S12 | Leventoux 2021, [arXiv:2010.02159](https://arxiv.org/abs/2010.02159), DOI:10.1364/OL.411868 | **Full text:** method, intrapulse exchange and simulation limitations. |
| S13 | Mangini 2023, [DOI:10.1364/OL.494543](https://doi.org/10.1364/OL.494543) | **Full text:** institutional PDF, phase-locking measurements and interpretation. |
| S14 | Chao–Fang–Yu 2025, [DOI:10.1103/k453-gplh](https://doi.org/10.1103/k453-gplh) | **Full text:** abstract/model and bending/quasi-resonance conclusions; APS PDF. |
| S15 | Kabat et al. 2025, [DOI:10.1103/xqyx-g3tn](https://doi.org/10.1103/xqyx-g3tn) | **Full text:** rate Eqs. (3)–(5), assumptions and comparisons; APS PDF. |
| S16 | Zitelli, online 2024/journal 2025, [arXiv:2404.00480](https://arxiv.org/abs/2404.00480), DOI:10.1002/lpor.202400714 | **Full text:** thermodynamic scope, discussion/conclusion. |
| S17 | Zanaglia et al. 2026, [arXiv:2506.23536](https://arxiv.org/abs/2506.23536), DOI:10.1103/mqzh-w2gh | **Full text:** abstract and spatiotemporal model/scope; numerical rates not independently verified. |
| S18 | Deliancourt 2019, [arXiv:1902.04453](https://arxiv.org/abs/1902.04453), DOI:10.1364/OE.27.017311 | **Full text:** setup, mode thresholds, Fig. 9 cut-back and conclusion. |

### DNLS and feasibility

| Key | Primary identifier | Access and inspected material |
|---|---|---|
| D1 | Rasmussen 2000, [DOI:10.1103/PhysRevLett.84.3740](https://doi.org/10.1103/PhysRevLett.84.3740) | **Full text:** boundary, simulations and conclusion; APS PDF. |
| D2 | Johansson–Rasmussen 2004, [arXiv:cond-mat/0410126](https://arxiv.org/abs/cond-mat/0410126), DOI:10.1103/PhysRevE.70.066610 | **Abstract only:** generalized DNLS thermodynamics/localization. |
| D3 | Rumpf 2004, [arXiv:nlin/0312058](https://arxiv.org/abs/nlin/0312058), DOI:10.1103/PhysRevE.69.016618 | **Full text:** entropy, pinning and exchange, especially pp. 4–5. |
| D4 | Rumpf 2008, [DOI:10.1103/PhysRevE.77.036606](https://doi.org/10.1103/PhysRevE.77.036606) | **Full text:** transition/distribution and conclusions; APS PDF. |
| D5 | Iubini 2013, [DOI:10.1088/1367-2630/15/2/023032](https://doi.org/10.1088/1367-2630/15/2/023032); precursor [arXiv:1203.4162v1](https://arxiv.org/abs/1203.4162v1) | **Full text:** precursor and [institutional NJP PDF](https://strathprints.strath.ac.uk/42959/1/NJP15_23032_13.pdf), §§3–6. Versions distinguished above. |
| D6 | Mithun 2018, [arXiv:1712.03375](https://arxiv.org/abs/1712.03375), DOI:10.1103/PhysRevLett.120.184101 | **Full text:** abstract, excursion-time/weak-nonergodicity interpretation and conclusion. |
| D7 | Baldovin 2021, [arXiv:2103.12572](https://arxiv.org/abs/2103.12572), DOI:10.1016/j.physrep.2021.03.007 | **Full text:** DNLS freezing/coarsening section. |
| D8 | Iubini 2019, [arXiv:1811.05798](https://arxiv.org/abs/1811.05798), DOI:10.1103/PhysRevLett.122.084102 | **Full text:** lifetime/hopping, diffusion, invariant and rare events. |
| D9 | Politi 2022, [arXiv:2201.02529](https://arxiv.org/abs/2201.02529), DOI:10.1088/1742-5468/ac650e | **Full text:** unidirectional model, invariant construction and §6. |
| D10 | Gradenigo 2021, [arXiv:1910.07461](https://arxiv.org/abs/1910.07461), DOI:10.1088/1742-5468/abda26 | **Full text:** model approximation and finite-size matching, §§II–III. |
| D11 | Iubini–Politi 2025, [arXiv:2406.15140](https://arxiv.org/abs/2406.15140), DOI:10.1103/PhysRevLett.134.097102 | **Full text:** main metastability analysis and multibreather conclusion. |
| D12 | Giachello 2025, [arXiv:2503.14364v2](https://arxiv.org/abs/2503.14364v2), DOI:10.1088/1742-5468/ae17ab | **Full text:** finite-size Hamiltonian dynamics, correlations and discussion; GPT-card follow-up. |
| D13 | Giusfredi 2026, [arXiv:2511.09206](https://arxiv.org/abs/2511.09206), DOI:10.1088/1742-5468/ae625e | **Full text:** model, metastability and conclusions; GPT-card follow-up. |
| D14 | Ramos 2020, [DOI:10.1103/PhysRevX.10.031024](https://doi.org/10.1103/PhysRevX.10.031024) | **Full text:** §§II, IV; positive-temperature restriction, phase transitions and finite-size scaling. |
| D15 | Kabat 2026, [arXiv:2602.13161](https://arxiv.org/abs/2602.13161), DOI:10.1103/372m-bnpr | **Full text:** transfer-integral/NIRJ formulation and non-Gibbs/disorder future-work paragraph. |
| D16 | Cherny–Engl–Flach 2019, [arXiv:1809.05371](https://arxiv.org/abs/1809.05371), DOI:10.1103/PhysRevA.99.023603 | **Abstract only:** quantum Bose–Hubbard non-Gibbs existence. |
| D17 | Rumpf 2007, [DOI:10.1209/0295-5075/78/26001](https://doi.org/10.1209/0295-5075/78/26001) | **Not accessed** in primary full text; identity located in primary references. Secondary abstract encountered, not used for a kill. Primary retrieval failed. |
| D18 | Rumpf 2009, [DOI:10.1016/j.physd.2009.08.006](https://doi.org/10.1016/j.physd.2009.08.006) | **Abstract only:** publisher preview; full text unavailable. |
| D19 | Iubini 2017, [arXiv:1701.08636](https://arxiv.org/abs/1701.08636) | **Full text:** abstract/model distinction and stochastic coarsening discussion. |
| D20 | Shi–Kottos–Shapiro 2021, [arXiv:2108.05072](https://arxiv.org/abs/2108.05072), DOI:10.1103/PhysRevResearch.3.033219 | **Full text:** band-gap kinetics and prethermal-state scope. |
| D21 | Rumpf–Newell 2025, [DOI:10.1016/j.physd.2025.134923](https://doi.org/10.1016/j.physd.2025.134923) | **Abstract only:** University of Arizona author publication record. Publisher/SSRN full text unavailable. |
| D22 | Marques Muniz 2023, [DOI:10.1126/science.ade6523](https://doi.org/10.1126/science.ade6523) | **Abstract only plus publisher introduction/Fig. 1 preview:** time-synthetic negative-temperature RJ. Full paper/supplement not read. |
| D23 | Kirsch et al., [arXiv:2511.12080](https://arxiv.org/abs/2511.12080), DOI:10.1038/s41567-024-02736-1 | **Full text:** Joule–Thomson setup and physical/normalized model; laser-written waveguide array. |
| D24 | Engelbrecht 2015, [DOI:10.1364/CLEO_SI.2015.SW4L.7](https://doi.org/10.1364/CLEO_SI.2015.SW4L.7) | **Abstract only:** primary conference page; threshold gain factor 16 is not universal. |
| D25 | Headley–Agrawal 1996, [DOI:10.1364/JOSAB.13.002170](https://doi.org/10.1364/JOSAB.13.002170) | **Full-text excerpt:** indexed author-PDF p. 2176, Eq. (30), and primary abstract. Direct PDF URL returned 404; whole paper not read. |

### Local invariants/higher-order resonances

| Key | Primary identifier | Access and inspected material |
|---|---|---|
| F1 | Suret 2010, [DOI:10.1103/PhysRevLett.104.054101](https://doi.org/10.1103/PhysRevLett.104.054101) | **Full text:** model/experiment, abstract and conclusion; APS PDF. |
| F2 | Michel 2011, [DOI:10.1007/s11005-010-0452-y](https://doi.org/10.1007/s11005-010-0452-y) | **Full text:** author PDF; scalar TOD/local invariant, applicability and conclusion. |
| F3 | Picozzi 2014, [DOI:10.1016/j.physrep.2014.03.002](https://doi.org/10.1016/j.physrep.2014.03.002) | **Full text:** §§6.1–6.2, especially experiment paragraph §6.2.3. |
| F4 | Onorato 2023, [arXiv:2305.18215](https://arxiv.org/abs/2305.18215), DOI:10.1016/j.physrep.2023.09.006 | **Full text:** conclusion p. 62 and relevant chain/resonance context. |
| F5 | Vassilev 2025, [DOI:10.1007/s00220-025-05455-7](https://doi.org/10.1007/s00220-025-05455-7) | **Full text:** abstract, introduction and dispersion assumptions; not a proof audit. |
| F6 | Onorato 2015, [arXiv:1402.1603](https://arxiv.org/abs/1402.1603), DOI:10.1073/pnas.1404397112 | **Full text:** resonant mechanism and numerical time scaling; open preprint after publisher retrieval failed. |
| F7 | Lvov–Onorato 2018, [arXiv:1802.07686](https://arxiv.org/abs/1802.07686), DOI:10.1103/PhysRevLett.120.144301 | **Full text:** weak six-wave regime, crossover and conclusion. |
| F8 | Sutherland–Yim 2026, [arXiv:2609.23175v1](https://arxiv.org/abs/2609.23175v1) | **Full text:** §§1, 6, 7, 11, kernel, theorem and denominator identity. Complete algebra not independently reproduced. |
| F9 | Barviau 2013, [DOI:10.1103/PhysRevA.87.035803](https://doi.org/10.1103/PhysRevA.87.035803) | **Full text:** four-wave resonant band and truncated thermalization; APS PDF. |
| F10 | Bandelow 2018, [DOI:10.1063/1.5030604](https://doi.org/10.1063/1.5030604) | **Full text:** ANU copy, hierarchy and Sasa–Satsuma Eqs. (2)–(4); whole hierarchy not audited. |

## Search log

Cutoff: 2026-10-20. Searches emphasized 2018–2026 while checking older foundations to avoid rediscovery. This is a targeted record, not exhaustive forward-citation coverage. Public titles/identifiers were used without personal requester data. Aggregator hits were used to locate primary copies, not as technical evidence.

| Stage | Query families / distinctive exact terms | Outcome |
|---|---|---|
| Independent, before checkpoint | Kerr beam self-cleaning threshold power fibre length nonlinear phase scaling; self-cleaning threshold inverse length; optical thermalization quasi-resonances 2025; exact Krupa/Fusaro/Garnier/Podivilov identifiers | Original SI scaling argument and coherent/kinetic distinction. Broad self-cleaning queries returned irrelevant surface-cleaning papers; narrowed to Kerr/GRIN. |
| Independent | DNLS non-Gibbs condensation coarsening dynamical freezing; negative-temperature multibreathers; Physica D 2025 wave turbulence coherent structures; coupled-core thermalization Raman | Known lifetimes and bath metastability; separated MMT/Gibbs networks from isolated DNLS. |
| Independent | anomalous thermalization frequency-local invariant; six-wave third-order dispersion; exact 2010/2011/2014 DOIs; arXiv:2609.23175 | Read primary optical papers and water-wave kernel before scout comparison. |
| Required-list/Claude follow-up | Exact DOIs 10.1103/k453-gplh, 10.1103/xqyx-g3tn, 10.1364/OL.494543, 10.1364/OL.411868, 10.1364/OL.41.003675; Deliancourt/Sidelnikov/Zitelli/Zanaglia arXiv IDs | Closed several scout access gaps; Liu remained abstract-only. |
| DNLS primary/version checks | 10.1209/0295-5075/78/26001; 10.1103/PhysRevE.77.036606; 10.1016/j.physd.2009.08.006; Growth and erosion of a discrete breather; 10.1016/j.physd.2025.134923; arXiv:1203.4162 | Read 2000/2004/2008 PDFs and separate NJP PDF; corrected version and stochastic/deterministic distinctions. 2007/2009 full-text gaps remain. |
| GPT-card follow-up | arXiv:2503.14364v2; arXiv:2511.09206 | Finite-size correlations and mean-field/metastability checks. |
| Optical realization | 10.1126/science.ade6523; optical thermalization multicore fibre; arXiv:2511.12080; stimulated Raman scattering 16 threshold; 10.1364/AO.11.002489; Unified description of ultrafast stimulated Raman scattering in optical fibers | Primary optical platforms, gain-factor qualification and walk-off condition. No calibrated late-coarsening fibre window established. Smith's full PDF not obtained; no inaccessible formula presented as my reading. |
| Six-wave/integrability follow-up | 10.1073/pnas.1404397112 arxiv; arXiv:1802.07686; Sasa Satsuma Hirota coefficients 053108; exact Vassilev DOI | Read FPUT scaling, checked model distinctions and derivative nonlinearities. |

Failed full-text routes included restrictions on some Optica, Science and Elsevier pages, an SSRN retrieval and a stale author-PDF URL. No sign-in, captcha bypass, paywall evasion or shadow library was used. Public APS PDFs, arXiv, institutional repositories and author copies supplied the decisive evidence.

## Remaining work

Follow-up tasks cover self-cleaning criterion/ownership and remaining prior art, PI consolidation of the DNLS cards, finite-array phase/graph/Raman feasibility, and the residual near-zero-dispersion kinetic scope. These are prerequisites or future research, not unfinished portions of this three-card literature assessment. One arithmetic Raman sanity check was recorded; no propagation simulation or new numerical law was verified.

| Task | Remaining decision/check |
|---|---|
| [T-20261020-gpt-h-01](../tasks/T-20261020-gpt-h-01-gate-self-cleaning-crossover-scope-and-o.md) | Common criterion and ownership with P-005/P-010; remaining Liu full text, coordinated with the existing scout tasks. |
| [T-20261020-gpt-h-02](../tasks/T-20261020-gpt-h-02-consolidate-duplicate-isolated-dnls-prob.md) | PI consolidation into gpt-g-02; coordinate its Claude review and complete Rumpf 2007/2009 primary checks before microscopic claims. |
| [T-20261020-gpt-h-03](../tasks/T-20261020-gpt-h-03-test-finite-core-dnls-optical-feasibilit.md) | Actual launch energy, graph/finite-size and calibrated Raman/dispersion window; remaining optical supplement check. |
| [T-20261020-gpt-h-04](../tasks/T-20261020-gpt-h-04-scope-residual-local-invariant-kinetics.md) | Residual uniform mixed-resonance problem and a viable optical window, or a recommendation to park. |
