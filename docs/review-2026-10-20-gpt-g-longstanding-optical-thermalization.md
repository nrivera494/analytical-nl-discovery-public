---
agent: gpt-g
model: gpt-6-astra
family: gpt
date: 2026-10-20
task: T-20261020-claude-interactive-03
---

# Longstanding problems in optical thermalization: independent GPT scouting

## Recommendation and scope

This is a literature assessment, not a derivation or a verification. No propagation campaign, new numerical result, claim, or result promotion was made. The candidate cards require the already scheduled independent Claude novelty review. The other scout's branch and review were not accessed. The existing registry and the two preceding reviews on origin/task/T-20261020-claude-interactive-02 were read to avoid duplicating their scope.

The search cutoff is 2026-10-20. “No closure found” below means no closure in the documented targeted searches and bounded forward-citation screens; it is not a proof that no such work exists. Access levels are this scout's own. Reading a previous review did not confer its authors' full-text access on this scout. The source and query ledgers below distinguish full-text reading of specified sections, abstract-only checks, metadata, and failed retrievals.

## Ranked shortlist

| Rank | Target | Why a solution would matter | Main risk |
|---|---|---|---|
| 2 | Closed Hamiltonian DNLS breather coarsening and condensation time | Resolves the long-running discrepancy between a single-condensate equilibrium and apparently frozen multibreather dynamics. | Stochastic surrogates and reservoir escape laws already exist. A new law must retain deterministic phase dynamics and backreaction. |
| 3 | Finite-norm nonlinear Anderson spreading versus arrest | Resolves a recognized conflict between power-law numerical spreading and much slower analytical transport mechanisms. | This is the hardest target. Existing bounds for related chains are not a solution of the standard optical DNLS; a routine transfer of a bound would not meet the novelty bar. |

Both are provisionally high-novelty targets if solved at the stated scope. This rating concerns the remaining problem, not the novelty of its first calculation. An isolated-soliton spectrum, a fitted exponential breather lifetime, or another finite-time fit of the Anderson spreading exponent would not qualify.

## Long list

Each entry assesses age, value, analytical entry, and testability, then records the attempt to kill it. N1–N4 are outside the orchestrator's seed list. N2 is an existing registry problem; N3 and N4 were killed rather than repackaged as new cards.

### S1. A parameter-free self-cleaning length in GRIN fibre — park

The rapid-cleaning/slow-kinetics discrepancy is an established motivation for disorder-assisted kinetics, but the seed's blanket statement that theory remains orders of magnitude too slow cannot be retained after Fusaro et al. (2019), strong-disorder kinetics, and Ferraro et al. (2025). A launch- and disorder-resolved length would be useful to multimode-fibre experiments. The concrete entry is the collision operator with measured coupling statistics; the test is a cut-back measurement of modal relaxation versus power and disorder, using a stochastic linear-coupling evaluator that the present solver lacks. However, this scout did not establish an explicit, still-open longstanding *quantitative* discrepancy after those theories. The weak-/strong-disorder comparison and the distinction between cleaning and RJ thermalization are already developed. **Kill search:** the 2021–2026 forward citations of Fusaro's PRL, targeted rate searches, and Ferraro's treatment led to Berti (2022), Baudin (2023), and newer kinetic work. **Deciding sources:** Ferraro 2025 and Baudin 2023. **Verdict:** park; finite-pulse and walk-off versions belong to P-005/P-010. Do not upgrade either card on the unverified premise in the seed.

### S2. Full invariant set and GGE of ideal GRIN — park

The harmonic-oscillator resonant equation has substantial mathematical structure, and an exact account of nonergodic optical states would matter. A derivation can start from the resonant Hamiltonian and its symmetry generators; a mode-resolved correlation/occupation experiment would compare ideal recurrence with controlled disorder. Yet the broad request for *all* invariants is not, by itself, an explicitly longstanding optical open question established by this search. Germain–Hani–Thomann already analyzed the resonant equation in 2015–2016; Biasi–Evnin–Malomed (2023) explain an obstruction to ergodicity. The repository already has C-20261016-claude-interactive.7-03 and its parent quantum-RJ problem. **Kill search:** forward citations of Germain–Hani–Thomann and targeted 2021–2026 resonant-system searches found the 2023 obstruction paper and tensorial thermalization work. **Deciding source:** arXiv:2304.10308 / PRE 108, 034204. **Verdict:** park; a genuinely new complete classification would need a more precise physical target and a separate proof of longstanding status. Do not file another extra-invariant observation.

### S3. Deterministic DNLS breather coarsening — shortlist, rank 2

The problem is the dynamical route from many breathers to the microcanonical condensate, not the existence of negative temperature. Rumpf (2004) already describes a single-peak entropy maximum that simulations fail to reach; Rumpf (2009) and Iubini et al. (2013) explicitly revisit metastable multibreather dynamics. The 2021 negative-temperature review still contrasts unobserved deterministic coarsening with solved stochastic coarsening. Politi–Politi–Iubini (2022) leave the rare events that change the adiabatic invariant quantitatively unresolved. Iubini–Politi (2025) leave the multiple-breather extension for further work, Giachello et al. (2025) leave the type of dynamical arrest/aging unresolved, and Giusfredi et al. (2026) separate their mean-field equilibrium theory from transition dynamics. A first calculation is a conditional jump/escape law for a tall breather's dressed action with a finite Hamiltonian background. It would feed a coarsening law and condensation-time distribution. Coupled-core fibre or a calibrated synthetic lattice could measure survival and transfer events; a dedicated DNLS oracle is needed. **Kill search:** 2021–2026 citers of Rumpf 2004/2009, the freezing PRL and the 2022 invariant paper, plus deterministic-coarsening queries, found equilibrium large deviations, reservoir metastability, noisy dynamics and a fully nonlinear lattice variant. None closes the isolated standard-chain target. **Deciding sources:** the 2021 review, 2022 Sec. 6, 2025 PRL conclusion and Giachello Appendix B. **Verdict:** shortlist, high provisional novelty.

### S4. Soliton plus thermal radiation from only N, H, and mode count — park

Coherent-structure equilibrium is an old statistical-mechanical subject, so a general predictive multimode theory could be valuable. A constrained Gibbs/large-deviation or variational calculation is an analytical entry, and a fibre measurement could compare pulse energy fraction and radiation spectrum at equal invariants. But the requested reduction must specify ultraviolet truncation, focusing collapse regularization, and which additional invariants survive. Jordan–Josserand (2000) already treat coherent structure plus fluctuations; the registry's P-002/P-008 and the preceding reviews cover multimode soliton capture, Raman conversion, and 2024 weighted-Bose–Einstein entropy work. **Kill search:** Jordan–Josserand forward citations through 2026, Ferraro's review, and targeted searches for recent soliton thermodynamics. **Deciding sources:** Jordan–Josserand and the 2024 Zitelli work as assessed in the preceding reviews. **Verdict:** park. The assertion that weighted-BE fits have no statistical derivation is not a valid novelty premise. A sharper multimode/collapse question may deserve an upgrade of P-002, not a duplicate card.

### S5. Single-mode thermalization after degenerate four-wave resonances — park

Picozzi et al. (2014), Sec. 6.2, explain frequency-local kinetic invariants for third-order dispersion; this is a concrete old obstruction, and a controlled six-wave collision integral is a plausible entry. A quantitative length could matter to incoherent-fibre experiments, with power and dispersion scans distinguishing collision orders. However, the seed groups together perturbations with very different integrability properties. The preceding GPT review shows that the scalar Kerr-plus-shock-only model has an integrable derivative-NLS mapping. Four-wave degeneracy alone does not establish a still-open physical six-wave thermalization law, nor does adding a sixth-order term establish its relevance to silica fibre. **Kill search:** targeted 2021–2026 six-wave/TOD/shock queries and forward citations of the earlier frequency-local-invariant work; recent spatiotemporal kinetics was also checked through the preceding reviews. **Deciding source:** Picozzi 2014 plus the explicitly recorded integrability result in the preceding GPT review. **Verdict:** park until a precise nonintegrable fibre Hamiltonian and an explicit unresolved old length-scaling question are established. No card at low novelty confidence.

### S6. Universal condensation exponents in a discrete fibre spectrum — park

Condensation kinetics and nonthermal fixed points are longstanding subjects, but transferring their language to a finite discrete mode set does not by itself identify a longstanding unresolved question. A kinetic boundary layer between discrete low modes and a quasi-continuum high-mode bath is a concrete entry; the possible observable is scaling collapse of modal occupations under independent launch families, checked against mode-count and recurrence effects. **Kill search:** Sun et al. (2012) forward citations, targeted 2021–2026 fibre universality queries, and the current spatiotemporal papers. The 2026 guided-wave cooling theory already supplies a self-similar temporal law; its existence defeats a generic claim that no universal fibre scaling theory exists. **Deciding sources:** Sun 2012, Ferraro 2025, Zanaglia et al. 2026. **Verdict:** park. Need an explicitly old, unsolved exponent selection or finite-spectrum crossover, not an unspecified universality search. A new oracle would require convergence in mode count and, for disordered fibres, linear mode coupling.

### S7. Standard local-Kerr nonlinear Anderson problem — shortlist, rank 3

Pikovsky–Shepelyansky (2008) leave the exact asymptotic exponent and very slow subthreshold spreading unresolved; Fishman–Krivolapov–Soffer (2012) explicitly list the asymptotic time scale and experiment–theory reconciliation as open. De Roeck and coauthors restate the tension in 2024–2026. The high-value target is an asymptotic law or decisive bound for a typical finite-norm packet at fixed nonzero linear hopping, with participation and peak power measured alongside width. An entry is a rare-resonance normal form and escape-time estimate in the localized linear-mode basis, retaining self-consistent dilution rather than assuming a white bath. A multicore/synthetic fibre lattice can test its density dependence; a finite experiment cannot certify infinite-time arrest. **Kill search:** 2021–2026 citers of the 2008 PRL plus targeted 2025–2026 resolution searches uncovered stronger rigorous bounds and an explicit screening-based localization claim. The former concern KG decorrelation or quartic-coupling atomic-limit chains; the latter changes the local-Kerr model and uses an additional phenomenological self-screening argument. These distinctions are examined below. **Deciding sources:** Fishman 2012, De Roeck et al. 2024 and 2025/2026, Milovanov–Iomin 2025. **Verdict:** shortlist, high provisional novelty for the standard model and specified ensemble.

### N1. Dense focusing-NLS gas: nonlinear spectrum to ordinary optical spectrum — shortlist, rank 1

### N2. Modal phase locking compatible with RJ occupations — park in existing home

Ferraro et al. (2025) explicitly identify the need to extend statistical descriptions to phase locking. Occupations alone do not determine coherence, so a joint occupation/phase-order theory would be useful and could start from anomalous correlators or a reduced phase-sensitive closure. It is directly testable by interferometric mode decomposition, but an oracle must retain degeneracies and coupling statistics. **Kill search:** Mangini et al. (2023) forward citations and targeted correlator searches found existing phase-locking work and the 2026 reversible-dynamics/anomalous-correlator theory. The registry already contains P-20261002-gpt-a-03 with precisely this target. **Deciding sources:** Ferraro 2025 and the 2026 anomalous-correlator paper. **Verdict:** park in the existing card. No evidence gathered here justifies changing its low novelty rating; propose further audit only if a specific old unresolved phase-selection law survives.

### N3. A microscopic random-fibre-laser model of replica symmetry breaking — kill as framed

The route from 2016 random-fibre-laser observations to a microscopic, experimentally discriminating statistical model is a natural nonseed candidate: it concerns glassy light, has a coupled forward/backward propagation model as an entry, and is testable through spectral overlap distributions and controlled Rayleigh phase fluctuations. **Kill search:** 2021–2026 forward citations of Gomes et al. (2016) and targeted RFL theory searches led directly to Qi et al. (2024), which presents a Rayleigh-scattering phase-variation model and experimental validation, including mode-dependent behaviour. **Deciding source:** DOI 10.1038/s41377-024-01475-5 / arXiv:2312.10898, full text selected sections. **Verdict:** kill the broad missing-microscopic-model claim. This does not assert that every interpretation of photonic RSB is settled. A narrower equilibrium-versus-driven-glass diagnostic needs its own longstanding evidence. The present solver also lacks distributed bidirectional random feedback.

### N4. Optical thermodynamics beyond weak nonlinearity in a nearest-neighbour Kerr chain — kill as framed

The weak-interaction restriction of optical thermodynamics is an established limitation, and a nonideal equation of state would be consequential. Transfer-integral statistical mechanics is a concrete analytical foothold; a coupled-core or synthetic lattice could measure modal powers and nonlinear energy while varying the interaction/bandwidth ratio. **Kill search:** forward citations of Wu–Hassan–Christodoulides (2019), targeted beyond-weak-nonlinearity searches, and the 2026 PRL. Kabat et al. (2026) already use a transfer integral operator and a self-consistent nonideal RJ description to predict the equation of state and modal redistribution in the Gibbsian nearest-neighbour setting. **Deciding source:** DOI 10.1103/372m-bnpr / arXiv:2602.13161, full text main theory and conclusion. **Verdict:** kill this generic proposal. This result does not close the isolated non-Gibbs coarsening problem in S3, nor all strong-nonlinearity multimode geometries.

## Resolution audit for the shortlist

The tables below cover the claimed or plausible resolutions located in this search. They are not a claim to have read every citing paper. The cards contain the governing equations, assumption ledgers, dimensionless validity bounds, observables, and laboratory/oracle protocols. None of the cards is promoted or independently audited.

### Rank 2: isolated deterministic DNLS coarsening

Card: [P-20261020-gpt-g-02](../problems/P-20261020-gpt-g-02-hamiltonian-breather-coarsening.md).

| Closest work | Resolution actually provided | Remaining distinction |
|---|---|---|
| Rumpf 2004/2007/2008/2009 [D1–D4] | Entropic condensation, pinning, a growth/erosion criterion, transition statistics and metastable potentials. | These are real mechanisms and early explanations. A quantitative collective escape/coarsening law is not established by the accessed text; D2 and D4 require full-text follow-up. |
| Iubini et al. 2014/2017 [D6–D7] | Coarsening in conservative stochastic surrogates, including amplitude-dependent exchange. | The exchange rule does not derive from the closed Hamiltonian phase dynamics. |
| Iubini et al. 2019; Politi et al. 2022 [D8, D10] | Dynamical freezing and an adiabatic invariant, with a particularly detailed construction for unidirectional forcing. | The 2022 discussion explicitly leaves quantitative rare jumps unresolved. Backreaction and collective transfer remain necessary. |
| Gradenigo et al. 2021 [D11–D12]; Giachello et al. 2025 [D13] | Microcanonical condensation/finite-size scaling and numerical thermodynamic correlations. | D13 Appendix B expressly leaves the type of ergodicity breaking and aging unresolved. It also warns against treating the background as a statistically independent infinite-temperature bath. |
| Iubini–Politi 2025 [D14] | Effective grand-canonical single-breather metastability and reservoir lifetime theory. | Global norm and energy conservation, interacting breathers and the closed-chain condensation time are additional physics. Reusing its lifetime formula is not a solution. |
| Onorato et al. 2022 [D15] | Negative-temperature wave-kinetic equilibria and relaxation. | The introduction explicitly excludes coherent solitons/breathers from its random-phase weak-wave approximation. |
| Ebrahimi et al. 2025/2026; Das et al. 2026 [D16–D18] | Localized-state thresholds and relaxation with multiplicative/additive noise, microscopic stochastic dynamics and dephasing. | Noise changes the rare transfer process and may remove energy conservation. The deterministic parts concern localized initial conditions/stability, not collective non-Gibbs coarsening. |
| Giusfredi et al. 2025/2026 [D19–D20] | Boundary-driven stochastic localization and mean-field equilibrium phase structure. | Neither is a closed deterministic multibreather rate law. |
| Kati et al. 2026 [D21] | Thermalization and compacton localization in a fully nonlinear toy lattice. | Its coupling is nonlinear and it has no linear dispersive term. It is not the standard nearest-neighbour DNLS. |
| Kabat et al. 2026 [O12]; Archilla et al. 2025 [D22]; Chen–Rumpf 2021 [D23] | Gibbsian nonideal optical thermodynamics, other-lattice breather lifetimes, and coherent-structure growth/erosion with random waves. | None supplies the requested isolated DNLS multibreather first-passage distribution. D23 is an abstract-only adjacent check, not a fully audited rate theory. |

The first derivation target is a **conditional rare-jump kernel for a tall breather's dressed action, with microcanonical background backreaction**. A first-passage law at fixed excess-energy density and a consistent breather-density evolution would resolve the long-lived plateau problem. The theory must distinguish persistent condensates from transient peaks and permit a nonzero arrest probability if the dynamics demands it. The laboratory prediction is the dependence of survival/transfer statistics on power and separation, with noise calibrated below the Hamiltonian rate. A stochastic surrogate or the mere observation of negative-temperature RJ light does not meet this target.

### Rank 3: nonlinear Anderson spreading at fixed linear hopping

Card: [P-20261020-gpt-g-03](../problems/P-20261020-gpt-g-03-asymptotic-nonlinear-anderson-spreading.md).

| Closest work | Resolution actually provided | Remaining distinction |
|---|---|---|
| Kopidakis et al. 2008 [A15] | A strong-nonlinearity obstruction to complete dilution, with bounded participation in simulations. | The generalization to arbitrary launches is an additional assumption. The card excludes a universal-for-all-states assertion and explicitly separates self-trapping. |
| Pikovsky–Shepelyansky 2008 and Flach–Krimer–Skokos 2009 [A1–A2] | Numerical spreading and resonance-based power-law predictions. | The persistence of an effective chaotic forcing as density vanishes is not controlled at arbitrarily late time. |
| Johansson–Kopidakis–Aubry 2010 [A3] | Empirical arguments and numerical evidence for nonspreading KAM-like trajectories. | These constrain any universal assertion. They do not give the probabilities and asymptotic transport law for the card's broad random-phase launch ensemble. |
| Basko 2011 [A4] | Rare chaotic-spot transport and the explicit finite-packet estimate $L(t)\sim\exp[(c^{-1}\log t)^{1/3}]$ in Appendix B. | The appendix acknowledges a macroscopic equilibration length larger than the packet, then argues that short-scale fluctuations change only a coefficient. This extrapolation is the issue to control. Its finite-energy activation constraint is argued to improve at long time, so finite norm alone does not invalidate the proposal. |
| Vakulchyk–Fistul–Flach 2019 [A7] | Very long numerical spreading without observed slowdown in a nonlinear discrete-time quantum walk. | Important contrary evidence, but a different map and a finite time horizon. |
| De Roeck–Huveneers–Prośniak 2024/2025 [A8–A9] | Nonperturbatively slow equilibrium decorrelation/transport in disordered KG chains, including harmonic coupling. | The weak-anharmonicity limit does not itself decide a diluting finite-norm DNLS packet at fixed hopping or prove permanent localization. |
| De Roeck–Giacomin–Hannani–Huveneers 2025/2026 [A10] | An all-time sub-power bound on decay of the packet maximum. | The displayed chain has quartic intersite coupling and no harmonic hopping; the DNLS-type extension also has nonlinear intersite coupling. Peak decay and width are different observables. |
| Milovanov–Iomin 2025 [A11] | A screening-induced localization mechanism, with a further self-screening proposal. | The main model changes the local Kerr response. Its self-screening discussion of the original problem additionally uses a Cayley-tree reduction, a Boltzmann chaos probability and percolative conductivity. Their validity for the stated ensemble is unproved in the accessed account. |

The last column records this scout's assessment, not a claim that a theorem or screening calculation is false in its own domain. The target is to **derive or bound rare-cluster transfer times in the localized eigenbasis while retaining the finite packet's backreaction and dilution**. A controlled law, or a bound that rules out one of the competing asymptotes at fixed $J/W>0$, would be consequential. A copied Basko law, an exponent fit, or a mechanical translation of a related-chain theorem would not be enough. The laboratory can test local rate/crossover predictions and bulk dilution; finite propagation cannot prove an infinite-time statement.

## Source ledger

Access labels refer to this session. **Full text** means that a legitimate full-text version was available and the specified sections were read; it does not mean every technical proof was audited. **Abstract only** includes cases where a publisher indexed some additional introduction/conclusion passages; those are identified. **Not accessed** means the source was located but the assessment uses the stated review, not an unread original. Quotes appear only in the cards, each under 15 words and at most once per source.

### Reviews and nonseed discovery

| ID | Source and identifier | Access and role |
|---|---|---|
| R1 | Picozzi et al. (2014), *Optical wave turbulence*, [10.1016/j.physrep.2014.03.002](https://doi.org/10.1016/j.physrep.2014.03.002) | **Full text**, author PDF; introduction, kinetic regimes, Sec. 6.2 and outlook. Baseline for S1/S5 and coherent-structure limitations. |
| R2 | Wright et al. (2022), *Physics of highly multimode nonlinear optical systems*, [10.1038/s41567-022-01691-z](https://doi.org/10.1038/s41567-022-01691-z) | **Abstract only**; publisher full text unavailable. PI download for review coverage. |
| R3 | Ferraro et al. (2025), *Wave turbulence, thermalization and multimode locking in optical fibers*, [10.1016/j.physd.2025.134758](https://doi.org/10.1016/j.physd.2025.134758), [arXiv:2505.11299](https://arxiv.org/abs/2505.11299) | **Full text**, arXiv and author version; disorder, thermalization, phase locking, open issues. N2 and seed screening. |
| R5 | Baldovin et al. (2021), *Statistical mechanics of systems with negative temperature*, [10.1016/j.physrep.2021.03.007](https://doi.org/10.1016/j.physrep.2021.03.007), [arXiv:2103.12572](https://arxiv.org/abs/2103.12572) | **Full text**, DNLS thermodynamics and dynamical/freezing discussion. D9 below refers to this source. |

### DNLS condensation and its alternatives

| ID | Source and identifier | Access |
|---|---|---|
| D1 | Rumpf (2004), [10.1103/PhysRevE.69.016618](https://doi.org/10.1103/PhysRevE.69.016618), [arXiv:nlin/0312058](https://arxiv.org/abs/nlin/0312058) | **Full text**, complete preprint. Earliest located persistent single-condensate/multipeak discrepancy. |
| D2 | Rumpf (2007), growth/erosion with RJ phonons, [10.1209/0295-5075/78/26001](https://doi.org/10.1209/0295-5075/78/26001) | **Not accessed** at primary full text; located on author institution's publication list and in D4/D5/R5. Publisher link denied access. Do not infer a rate kernel from its title. |
| D3 | Rumpf (2008), [10.1103/PhysRevE.77.036606](https://doi.org/10.1103/PhysRevE.77.036606) | **Abstract only**, indexed primary abstract via PubMed. Transition thermodynamics. |
| D4 | Rumpf (2009), [10.1016/j.physd.2009.08.006](https://doi.org/10.1016/j.physd.2009.08.006) | **Abstract only**, plus publisher-indexed introduction/section snippets. Metastable potentials; PI download. |
| D5 | Iubini et al. (2013), [10.1088/1367-2630/15/2/023032](https://doi.org/10.1088/1367-2630/15/2/023032) | **Full text**, Strathclyde manuscript; model and discussion/conclusion. |
| D6 | Iubini–Politi–Politi (2014), [10.1007/s10955-013-0896-4](https://doi.org/10.1007/s10955-013-0896-4), [arXiv:1308.4870](https://arxiv.org/abs/1308.4870) | **Full text**, stochastic model, coarsening argument and abstract. |
| D7 | Iubini–Politi–Politi (2017), [arXiv:1701.08636](https://arxiv.org/abs/1701.08636) | **Full text**, abstract, amplitude-dependent exchange models and Secs. 4–5. |
| D8 | Iubini et al. (2019), [10.1103/PhysRevLett.122.084102](https://doi.org/10.1103/PhysRevLett.122.084102), [arXiv:1811.05798](https://arxiv.org/abs/1811.05798) | **Full text**, freezing mechanism and main conclusion. |
| D9 | Negative-temperature review (2021) | Same source as R5; not an additional paper. |
| D10 | Politi–Politi–Iubini (2022), [10.1088/1742-5468/ac650e](https://doi.org/10.1088/1742-5468/ac650e), [arXiv:2201.02529](https://arxiv.org/abs/2201.02529) | **Full text**, invariant construction and Sec. 6. |
| D11 | Gradenigo et al. (2021), [10.1088/1742-5468/abda26](https://doi.org/10.1088/1742-5468/abda26), [arXiv:1910.07461](https://arxiv.org/abs/1910.07461) | **Full text**, introduction, finite-size condensation and temperature discussion. Technical contour asymptotics not audited. |
| D12 | Gradenigo et al. (2021), [10.1140/epje/s10189-021-00046-5](https://doi.org/10.1140/epje/s10189-021-00046-5), [arXiv:2106.03698](https://arxiv.org/abs/2106.03698) | **Full text**, introductory thermodynamic account. |
| D13 | Giachello–Iubini–Livi–Gradenigo (2025), [10.1088/1742-5468/ae17ab](https://doi.org/10.1088/1742-5468/ae17ab), [arXiv:2503.14364v2](https://arxiv.org/abs/2503.14364v2) | **Full text**, model, finite-size initial-condition dependence, conclusion and Appendix B. |
| D14 | Iubini–Politi (2025), [10.1103/PhysRevLett.134.097102](https://doi.org/10.1103/PhysRevLett.134.097102), [arXiv:2406.15140](https://arxiv.org/abs/2406.15140) | **Full text**, main effective-grand-canonical theory and multibreather limitation. |
| D15 | Onorato et al. (2022), [10.1103/PhysRevE.105.014206](https://doi.org/10.1103/PhysRevE.105.014206) | **Full text**, CHORUS manuscript through web access; introduction and weak-wave model. Local download failed. |
| D16 | Ebrahimi–Drossel–Just (2025), [10.1016/j.physd.2025.134905](https://doi.org/10.1016/j.physd.2025.134905) | **Full text**, Rostock manuscript, model and conclusion. |
| D17 | Ebrahimi–Drossel–Just (2026), [10.1088/1402-4896/ae54df](https://doi.org/10.1088/1402-4896/ae54df), [arXiv:2512.01448](https://arxiv.org/abs/2512.01448) | **Full text**, abstract and stochastic model. |
| D18 | Das et al. (2026), [10.1103/gjkp-21dh](https://doi.org/10.1103/gjkp-21dh), [arXiv:2602.22878](https://arxiv.org/abs/2602.22878) | **Full text**, abstract and dephasing/defect model. |
| D19 | Giusfredi et al. (2025), [10.1088/1742-5468/add1cd](https://doi.org/10.1088/1742-5468/add1cd), [arXiv:2503.04461](https://arxiv.org/abs/2503.04461) | **Abstract only**; boundary-driven stochastic chain. |
| D20 | Giusfredi et al. (2026), [10.1088/1742-5468/ae625e](https://doi.org/10.1088/1742-5468/ae625e), [arXiv:2511.09206](https://arxiv.org/abs/2511.09206) | **Full text**, mean-field model and conclusion. |
| D21 | Kati et al. (2026), [10.1103/nfym-zysm](https://doi.org/10.1103/nfym-zysm), [arXiv:2601.13472v3](https://arxiv.org/abs/2601.13472v3) | **Full text**, introduction, toy Hamiltonian, discussion/conclusion. Publication dates differ between index and issue; version accessed is 17 August 2026. |
| D22 | Archilla–Bajars–Flach (2025), [10.1016/j.physd.2025.134551](https://doi.org/10.1016/j.physd.2025.134551), [arXiv:2411.06044](https://arxiv.org/abs/2411.06044) | **Full text**, abstract and oscillator-model descriptions. |
| D23 | Chen–Rumpf (2021), [10.1103/PhysRevE.104.034213](https://doi.org/10.1103/PhysRevE.104.034213) | **Abstract only**, primary abstract. Nonintegrable noncollapsing NLS coherent-structure/thermal-wave interaction. |
| D24 | Marques Muniz et al. (2023), *Observation of photon-photon thermodynamic processes under negative optical temperature conditions*, [10.1126/science.ade6523](https://doi.org/10.1126/science.ade6523) | **Abstract only**, plus indexed primary platform passages. Full experiment/supplement requested; no assertion of a breather condensate. |

### Anderson localization and optical platforms

| ID | Source and identifier | Access |
|---|---|---|
| A1 | Pikovsky–Shepelyansky (2008), [10.1103/PhysRevLett.100.094101](https://doi.org/10.1103/PhysRevLett.100.094101), [arXiv:0708.3315](https://arxiv.org/abs/0708.3315) | **Full text**, model and conclusion. |
| A2 | Flach–Krimer–Skokos (2009), [10.1103/PhysRevLett.102.024101](https://doi.org/10.1103/PhysRevLett.102.024101), [arXiv:0805.4693](https://arxiv.org/abs/0805.4693) | **Full text**, scaling mechanism and its assumptions, main paper. |
| A3 | Johansson–Kopidakis–Aubry (2010), [10.1209/0295-5075/91/50001](https://doi.org/10.1209/0295-5075/91/50001), [arXiv:1007.1912](https://arxiv.org/abs/1007.1912) | **Full text**, abstract and discussion. Empirical KAM arguments are not described as a general proof. |
| A4 | Basko (2011), [10.1016/j.aop.2011.02.004](https://doi.org/10.1016/j.aop.2011.02.004), [arXiv:1005.5033](https://arxiv.org/abs/1005.5033) | **Full text**, introduction, scope, Appendix B and adjacent thermodynamic conditions. Full high-order derivation not audited. |
| A5 | Fishman–Krivolapov–Soffer (2012), [10.1088/0951-7715/25/4/R53](https://doi.org/10.1088/0951-7715/25/4/R53), [arXiv:1108.2956](https://arxiv.org/abs/1108.2956) | **Full text**, analytic/numerical comparison and explicit open questions in Sec. 5.1. |
| A6 | Laptyeva–Ivanchenko–Flach (2014), [10.1088/1751-8113/47/49/493001](https://doi.org/10.1088/1751-8113/47/49/493001), [arXiv:1407.1441](https://arxiv.org/abs/1407.1441) | **Full text**, selected synthesis/outlook. Supporting context, not a new closure. |
| A7 | Vakulchyk–Fistul–Flach (2019), [10.1103/PhysRevLett.122.040501](https://doi.org/10.1103/PhysRevLett.122.040501), [arXiv:1806.06345](https://arxiv.org/abs/1806.06345) | **Full text**, model and long-time numerical conclusion. |
| A8 | De Roeck–Huveneers–Prośniak (2024), [10.1103/PhysRevE.109.044207](https://doi.org/10.1103/PhysRevE.109.044207), [arXiv:2308.10572](https://arxiv.org/abs/2308.10572) | **Full text**, introduction, KG model and stated bound; accessed revised preprint. |
| A9 | Same authors, rigorous companion (2025), [10.1007/s00220-025-05336-z](https://doi.org/10.1007/s00220-025-05336-z), [arXiv:2308.11243](https://arxiv.org/abs/2308.11243) | **Full text**, introduction/model and theorem statement, not complete proof. |
| A10 | De Roeck–Giacomin–Hannani–Huveneers (2025 preprint/2026 journal), [10.1088/1361-6544/ae56ad](https://doi.org/10.1088/1361-6544/ae56ad), [arXiv:2502.02344](https://arxiv.org/abs/2502.02344) | **Full text**, preprint model and all-time peak bound; journal text not assumed identical. |
| A11 | Milovanov–Iomin (2025), [10.1103/svxt-wsk7](https://doi.org/10.1103/svxt-wsk7), [arXiv:2502.08463](https://arxiv.org/abs/2502.08463) | **Full text**, preprint and journal PDF through web, especially II–VI including self-screening. Local publisher download failed. |
| A12 | Mafi–Ballato (2021), [10.3389/fphy.2021.736774](https://doi.org/10.3389/fphy.2021.736774) | **Full text**, web introduction and Secs. 4.2–4.3. TAL-fibre context and nonlocal thermal caveat. |
| A13 | Vatnik et al. (2017), [10.1038/s41598-017-04059-z](https://doi.org/10.1038/s41598-017-04059-z) | **Abstract only**, plus indexed conclusion; PMC CAPTCHA not bypassed. Linear fibre-loop demonstration. |
| A14 | Flach–Krimer–Skokos (2009), erratum [10.1103/PhysRevLett.102.209903](https://doi.org/10.1103/PhysRevLett.102.209903) | **Full text**, one-page author-hosted PDF. Corrects the generalized-dimensional exponent; not an asymptotic-resolution claim. |
| A15 | Kopidakis et al. (2008), [10.1103/PhysRevLett.100.084103](https://doi.org/10.1103/PhysRevLett.100.084103), [arXiv:0710.2621](https://arxiv.org/abs/0710.2621) | **Abstract only**, primary publisher/arXiv. Strong-nonlinearity proof and conditional extrapolation distinguished. |

### Other long-list prior art

| ID | Source and identifier | Access and use |
|---|---|---|
| O1 | Fusaro et al. (2019), [10.1103/PhysRevLett.122.123902](https://doi.org/10.1103/PhysRevLett.122.123902), [arXiv:2011.05111](https://arxiv.org/abs/2011.05111) | **Abstract only**; mechanism also read in full R3. S1 citation anchor. |
| O2 | Berti et al. (2022), [10.1103/PhysRevLett.129.063901](https://doi.org/10.1103/PhysRevLett.129.063901), [arXiv:2207.08680](https://arxiv.org/abs/2207.08680) | **Not accessed** directly; located and assessed through R3 and preceding repository reviews. |
| O3 | Baudin et al. (2023), [10.1016/j.optcom.2023.129716](https://doi.org/10.1016/j.optcom.2023.129716), [arXiv:2309.02215](https://arxiv.org/abs/2309.02215) | **Not accessed** directly; located through preceding reviews. Not used as independent proof of a rate paradox. |
| O4 | Germain–Hani–Thomann (2016), [10.1016/j.matpur.2015.10.002](https://doi.org/10.1016/j.matpur.2015.10.002), [arXiv:1501.03760](https://arxiv.org/abs/1501.03760) | **Full text**, introduction/structural overview; mathematical resonant-system baseline and citation anchor. |
| O5 | Biasi–Evnin–Malomed (2023), [10.1103/PhysRevE.108.034204](https://doi.org/10.1103/PhysRevE.108.034204), [arXiv:2304.10308](https://arxiv.org/abs/2304.10308) | **Abstract only**; ergodicity obstruction. PDF downloaded but not treated as proof-audited. |
| O6 | Sardelis et al. (2025), tensorial symmetries, [10.1017/jnw.2025.10025](https://doi.org/10.1017/jnw.2025.10025) | **Abstract only**, plus primary indexed introductory passages. Does not establish all GRIN invariants. |
| O7 | Jordan–Josserand (2000), [10.1103/PhysRevE.61.1527](https://doi.org/10.1103/PhysRevE.61.1527) | **Abstract only**; coherent-structure statistical mechanics and citation anchor. |
| O8 | Zitelli et al. (2024), [10.1038/s41467-024-45185-3](https://doi.org/10.1038/s41467-024-45185-3); weighted-BE work [10.1002/lpor.202400714](https://doi.org/10.1002/lpor.202400714), [arXiv:2404.00480](https://arxiv.org/abs/2404.00480) | **Not accessed** directly; located through the preceding two reviews. Their entropy assessment is reused with that limitation. |
| O9 | Michel et al. (2010), third-order dispersion of incoherent light, [10.1364/OL.35.002367](https://doi.org/10.1364/OL.35.002367) | **Not accessed** directly; located metadata and full discussion in R1. Citation anchor for S5. |
| O10 | Sun et al. (2012), kinetic condensation, [10.1038/nphys2278](https://doi.org/10.1038/nphys2278) | **Abstract only**; S6 citation anchor. |
| O11 | Zanaglia et al. (2026), spatiotemporal thermalization/cooling, [10.1103/mqzh-w2gh](https://doi.org/10.1103/mqzh-w2gh), [arXiv:2506.23536](https://arxiv.org/abs/2506.23536) | **Not accessed** directly; located through the preceding reviews. Reused to reject a generic absence-of-scaling premise, not to declare the discrete-mode exponent problem solved. |
| O12 | Kabat et al. (2026), *Optical Thermodynamics beyond the Weak Nonlinearity Limit*, [10.1103/372m-bnpr](https://doi.org/10.1103/372m-bnpr), [arXiv:2602.13161](https://arxiv.org/abs/2602.13161) | **Full text**, transfer integral, nonideal RJ/EOS and conclusion. Decides N4. |
| O13 | Mangini et al. (2023), modal phase locking, [10.1364/OL.494543](https://doi.org/10.1364/OL.494543) | **Abstract only**; N2 citation anchor. |
| O14 | Torres et al. (2026), anomalous correlators, [10.1103/tgtw-qnyq](https://doi.org/10.1103/tgtw-qnyq), [arXiv:2512.17777](https://arxiv.org/abs/2512.17777) | **Full text**, abstract and model; two-polarization coherent single-mode setting. Adjacent theory, not a complete multimode phase-locking solution. |
| O15 | Gomes et al. (2016), glassy CW erbium random-fibre laser, [10.1103/PhysRevA.94.011801](https://doi.org/10.1103/PhysRevA.94.011801), [arXiv:1601.01369](https://arxiv.org/abs/1601.01369) | **Full text**, abstract/experimental introduction; journal and preprint titles differ. N3 citation anchor. |
| O16 | Qi et al. (2024), *Replica symmetry breaking in 1D Rayleigh scattering system: theory and validations*, [10.1038/s41377-024-01475-5](https://doi.org/10.1038/s41377-024-01475-5), [arXiv:2312.10898](https://arxiv.org/abs/2312.10898) | **Full text**, microscopic model, validation and conclusion in OA preprint. Decides N3. Publisher request failed; no login attempted. |
| O17 | Wu–Hassan–Christodoulides (2019), [10.1038/s41566-019-0501-8](https://doi.org/10.1038/s41566-019-0501-8) | **Abstract only**, primary publisher metadata/abstract; N4 citation anchor and weak-interaction baseline. |

## PI download list and remaining limits

The essential unavailable full texts are listed below. Download only through institutional or legitimate author access, and place them in the external literature directory. Each item has a follow-up task recorded in the final section of this review.

| Paper | Why it is needed | Consequence of the access gap |
|---|---|---|
| Wright et al. 2022, DOI 10.1038/s41567-022-01691-z | Read the major multimode review's full outlook and challenge the scout's coverage. | The review-mining coverage is incomplete; R1/R3/R4 were available in full. |
| Sun–Yu–Feng 2025, DOI 10.1007/s10773-025-06079-2 | Exclude an unadvertised ordinary-spectrum/correlation closure in its periodic-box analysis. | Residual novelty risk for rank 1; abstract alone is not a full kill audit. |
| Rumpf 2007, DOI 10.1209/0295-5075/78/26001 | Inspect the precise phonon–breather exchange calculation before proposing a rare-event kernel. | First-derivation novelty cannot rely on a known growth/erosion criterion. |
| Rumpf 2009, DOI 10.1016/j.physd.2009.08.006 | Inspect metastable-state potentials and dynamical assumptions beyond indexed passages. | Needed before translating a metastable entropy barrier into a new coarsening claim. |
| Marques Muniz et al. 2023, DOI 10.1126/science.ade6523, main text and supplement | Check nonlinear loop map, invariants, noise and attainable observation window. | A fibre-loop DNLS limit is a proposed feasibility path, not yet demonstrated by this scout. |

The main Gradenigo 2021 paper was initially inaccessible but a legitimate arXiv preprint was subsequently located and read; it is **not** on the PI download list. The Milovanov journal text and Onorato CHORUS text were readable through the web despite failed local downloads; those are also not download blockers.

## Search log

All searches below were performed on 2026-10-20. Search engines and citation indexes are discovery tools; scientific assessments use primary papers or identified reviews. Returned ResearchGate, Scribd, Wikipedia, aggregator and unrelated results were not treated as scientific authority. No inaccessible paper was silently counted as read. The external directory is `~/analytical-nl-discovery-data/lit-T-20261020-claude-interactive-03/`; downloaded PDFs, extracted text and raw API records are not committed.

### Exact web search queries

The group labels preserve the working log (one early label range overlaps); the query numbers below are newly assigned in actual recorded order. No date filter was implicit: years shown are literal query terms. All used the web search service, without login.

| Query | Working group | Exact submitted string | Outcome |
|---|---|---|---|
| Q001 | Q001-Q003 | `Picozzi Garnier Hansson Suret Randoux Millot Christodoulides optical wave turbulence 2014 542 1 review` | Located R1–R3 and author/preprint versions. |
| Q002 | Q001-Q003 | `Wright optical thermodynamics Nature Physics 18 1018 2022 outstanding questions` | Located R1–R3 and author/preprint versions. |
| Q003 | Q001-Q003 | `Ferraro Physica D 2025 2505.11299 optical thermalization open problems` | Located R1–R3 and author/preprint versions. |
| Q004 | Q004-Q007 | `"Optical wave turbulence" "physrep" pdf Garnier 2014` | Located review copies and newer Anderson/DNLS leads; Wright full text remained unavailable. |
| Q005 | Q004-Q007 | `"Physics of highly multimode nonlinear optical systems" pdf Wright Wise` | Located review copies and newer Anderson/DNLS leads; Wright full text remained unavailable. |
| Q006 | Q004-Q007 | `"nonlinear" "Anderson" "spreading" "2025" thermalization` | Located review copies and newer Anderson/DNLS leads; Wright full text remained unavailable. |
| Q007 | Q004-Q007 | `"discrete nonlinear Schrödinger" "coarsening" "2025"` | Located review copies and newer Anderson/DNLS leads; Wright full text remained unavailable. |
| Q012 | Q012-Q014/O002 | `DNLS "dynamical freezing" "adiabatic" 2024 2025 2026` | Located adiabatic-invariant work and modern localization/restatement sources. |
| Q013 | Q012-Q014/O002 | `"nonlinear Anderson" "open problem" 2024 2025 2026` | Located adiabatic-invariant work and modern localization/restatement sources. |
| Q014 | Q012-Q014/O002 | `"integrable turbulence" "open problem" "stationary" 2024 2025 2026` | Located adiabatic-invariant work and modern localization/restatement sources. |
| Q015 | Q015-Q017/O003 | `Iubini Politi "adiabatic" "2023" breather` | Found 2021 negative-temperature review; generic six-wave queries did not establish the exact physical gap. |
| Q016 | Q015-Q017/O003 | `"Discrete nonlinear Schrödinger" "2021" review negative temperatures 2021 100343` | Found 2021 negative-temperature review; generic six-wave queries did not establish the exact physical gap. |
| Q017 | Q015-Q017/O003 | `"six-wave" "thermalization" "optical" "2025" "2026"` | Found 2021 negative-temperature review; generic six-wave queries did not establish the exact physical gap. |
| Q018 | Q018-Q021 | `"focusing" "solitons" "radiation" "generalized" "2025" hydrodynamics` | Found recent attractive-NLS/GHD and DNLS lifetime/mean-field candidates for full-text follow-up. |
| Q019 | Q018-Q021 | `"integrable turbulence" "statistics" "2026" soliton radiation` | Found recent attractive-NLS/GHD and DNLS lifetime/mean-field candidates for full-text follow-up. |
| Q020 | Q018-Q021 | `"DNLS" "coarsening" "2026"` | Found recent attractive-NLS/GHD and DNLS lifetime/mean-field candidates for full-text follow-up. |
| Q021 | Q018-Q021 | `"Frozen dynamics of a breather" citations 2025` | Found recent attractive-NLS/GHD and DNLS lifetime/mean-field candidates for full-text follow-up. |
| Q023 | Q022-Q025 | `"soliton" "radiation" "generalized hydrodynamics" nonlinear Schrödinger` | Located focusing classical-NLS GHD; no generic six-wave fibre closure identified. |
| Q024 | Q022-Q025 | `"optical" "thermalization" "six-wave" 2021 2022 2023 2024 2025 2026` | Located focusing classical-NLS GHD; no generic six-wave fibre closure identified. |
| Q025 | Q022-Q025 | `"optical wave turbulence" "local invariants" thermalization` | Located focusing classical-NLS GHD; no generic six-wave fibre closure identified. |
| Q028 | Q026-Q029 | `"Integrable turbulence and formation of rogue waves" arxiv` | Located 2015 integrable-turbulence baseline and newer gas spectral/correlation work. |
| Q030 | Q030-Q033 | `"Mean-field theory of the DNLS equation at positive and negative absolute temperatures"` | Located 2025 reservoir theory, 2026 mean-field/dephasing papers and newest Anderson bounds. |
| Q031 | Q030-Q033 | `"Effective Grand Canonical Description of Condensation in Negative-Temperature Regimes"` | Located 2025 reservoir theory, 2026 mean-field/dephasing papers and newest Anderson bounds. |
| Q032 | Q030-Q033 | `"Dephasing-induced relaxation in tight-binding chains" arxiv` | Located 2025 reservoir theory, 2026 mean-field/dephasing papers and newest Anderson bounds. |
| Q033 | Q030-Q033 | `"nonlinear Anderson" 2026 spreading localization asymptotic` | Located 2025 reservoir theory, 2026 mean-field/dephasing papers and newest Anderson bounds. |
| Q034 | Q034-Q039 | `"optical thermalization" "six-wave"` | Broad six-wave, anomalous-correlation, condensation and BKT screen; no BKT card supported. |
| Q035 | Q034-Q039 | `"anomalous thermalization" "2025" OR "2026"` | Broad six-wave, anomalous-correlation, condensation and BKT screen; no BKT card supported. |
| Q036 | Q034-Q039 | `"third-order dispersion" "thermalization" six` | Broad six-wave, anomalous-correlation, condensation and BKT screen; no BKT card supported. |
| Q037 | Q034-Q039 | `"universal" "condensation dynamics" multimode fiber` | Broad six-wave, anomalous-correlation, condensation and BKT screen; no BKT card supported. |
| Q038 | Q034-Q039 | `"soliton" "thermal equilibrium" "Jordan" "Josserand" 2000` | Broad six-wave, anomalous-correlation, condensation and BKT screen; no BKT card supported. |
| Q039 | Q034-Q039 | `"Rayleigh-Jeans" "Berezinskii" optical 2024 2025` | Broad six-wave, anomalous-correlation, condensation and BKT screen; no BKT card supported. |
| Q040 | Q040-Q043 | `"Pikovsky" "Shepelyansky" "2008" "Destruction" arxiv` | Resolved primary identifiers for Anderson, resonant-system, kinetic-condensation and TOD citation anchors. |
| Q041 | Q040-Q043 | `"Faou" "Germain" "Hani" "resonant" 2016 DOI` | Resolved primary identifiers for Anderson, resonant-system, kinetic-condensation and TOD citation anchors. |
| Q042 | Q040-Q043 | `"Sun" "2012" "470" "condensation" light Nature Physics` | Resolved primary identifiers for Anderson, resonant-system, kinetic-condensation and TOD citation anchors. |
| Q043 | Q040-Q043 | `"Influence of third-order dispersion on the propagation of incoherent light" DOI` | Resolved primary identifiers for Anderson, resonant-system, kinetic-condensation and TOD citation anchors. |
| Q044 | Q044-Q046 | `"discrete breathers and negative-temperature states" 023032 arxiv` | Located DNLS 2013 and Anderson 2012/2014 review full-text routes. |
| Q045 | Q044-Q046 | `"nonlinear Schrodinger equation with a random potential" "results and puzzles" arxiv` | Located DNLS 2013 and Anderson 2012/2014 review full-text routes. |
| Q046 | Q044-Q046 | `"nonlinear lattice waves in heterogeneous media" Flach Laptyeva Ivanchenko 2014` | Located DNLS 2013 and Anderson 2012/2014 review full-text routes. |
| Q047 | Q047-Q049 | `"Sub-Power Law Decay of the Wave Packet Maximum in Disordered Anharmonic Chains"` | Located newest packet-maximum bound; BKT query did not yield a qualifying fibre problem. |
| Q048 | Q047-Q049 | `"Discrete breathers and negative-temperature states" arxiv Iubini` | Located newest packet-maximum bound; BKT query did not yield a qualifying fibre problem. |
| Q049 | Q047-Q049 | `"Berezinskii" "optical" "2025" "thermalization"` | Located newest packet-maximum bound; BKT query did not yield a qualifying fibre problem. |
| Q050 | Q050-Q053 | `"random fiber" "replica symmetry breaking" "2016" Gomes DOI` | Located RFL 2016 observation, Qi 2024 model and Jordan–Josserand baseline; N3 kill lead. |
| Q051 | Q050-Q053 | `"Replica symmetry breaking in 1D Rayleigh scattering system: theory and validations"` | Located RFL 2016 observation, Qi 2024 model and Jordan–Josserand baseline; N3 kill lead. |
| Q052 | Q050-Q053 | `"Berezinskii" "thermalization" "light" "open"` | Located RFL 2016 observation, Qi 2024 model and Jordan–Josserand baseline; N3 kill lead. |
| Q053 | Q050-Q053 | `"coherent structures" "statistical equilibrium" "Jordan" "Josserand" 1527` | Located RFL 2016 observation, Qi 2024 model and Jordan–Josserand baseline; N3 kill lead. |
| Q054 | Q054-Q057 | `"Thermal lifetime of breathers" 2025` | Located other-lattice breather lifetimes and KG persistence theorem; no focusing-gas field-spectrum closure found. |
| Q055 | Q054-Q057 | `"Long Persistence of Localization in a Disordered Anharmonic Chain Beyond the Atomic Limit"` | Located other-lattice breather lifetimes and KG persistence theorem; no focusing-gas field-spectrum closure found. |
| Q057 | Q054-Q057 | `"one-dimensional wave kinetic theory" Vassilev 2025 nonlinear Schrodinger` | Located other-lattice breather lifetimes and KG persistence theorem; no focusing-gas field-spectrum closure found. |
| Q058 | Q058-Q061 | `"Destruction of Anderson Localization by a Weak Nonlinearity" arxiv.org` | Located original Anderson papers and Basko long calculation for model comparison. |
| Q059 | Q058-Q061 | `"Universal Spreading of Wave Packets" Flach Krimer Skokos arxiv` | Located original Anderson papers and Basko long calculation for model comparison. |
| Q060 | Q058-Q061 | `"Johansson" "Kopidakis" "Aubry" "2010" 50001` | Located original Anderson papers and Basko long calculation for model comparison. |
| Q061 | Q058-Q061 | `"Basko" "2011" "326" "1577" arxiv` | Located original Anderson papers and Basko long calculation for model comparison. |
| Q062 | Q062-Q065 | `"Marques Muniz" "Science" "379" "1019" 2023` | Located Science negative-temperature optical experiment and fibre-loop/disorder platform leads. |
| Q063 | Q062-Q065 | `"optical" "negative temperature" "breather" 2024 2025 2026` | Located Science negative-temperature optical experiment and fibre-loop/disorder platform leads. |
| Q064 | Q062-Q065 | `"fibre-loop" "nonlinear" "Anderson localization" 2024 2025` | Located Science negative-temperature optical experiment and fibre-loop/disorder platform leads. |
| Q065 | Q062-Q065 | `"coupled-core" "thermalization" optical negative temperature` | Located Science negative-temperature optical experiment and fibre-loop/disorder platform leads. |
| Q066 | Q066-069 | `"resonant" "harmonic" Germain Hani Thomann 2016 continuous resonant equation DOI` | Resolved metadata/preprint IDs and original Anderson source. |
| Q067 | Q066-069 | `"random fiber laser" "replica symmetry breaking" 2016 doi Gomes` | Resolved metadata/preprint IDs and original Anderson source. |
| Q068 | Q066-069 | `"Observation of photon-photon thermodynamic" negative optical temperature Science 2023 Muniz fibre loops` | Resolved metadata/preprint IDs and original Anderson source. |
| Q069 | Q066-069 | `"Universal Spreading of Wave Packets" 2009 arxiv Flach Krimer Skokos` | Resolved metadata/preprint IDs and original Anderson source. |
| Q072 | Q066-073 | `"DNLS" "coarsening" 2024 2025 2026 Hamiltonian` | Focused gas/coarsening queries found near-target progress, not the stated closure. |
| Q073 | Q066-073 | `"negative temperature" "metastable" Giusfredi 2026 dynamics DNLS` | Focused gas/coarsening queries found near-target progress, not the stated closure. |
| Q076 | Q074-077 | `"focusing" "nonlinear Schrödinger" "field correlations" thermodynamics` | Identified 2026 ballistic correlations and further gas inverse-scattering work; distinguished field from intensity correlations. |
| Q078 | Q078-081 | `"Nonlinear Spectra" "Integrable Turbulence" "Periodic Box" 2025` | Located Sun periodic-box paper, Giusfredi journal metadata and newest peak-bound journal version. |
| Q079 | Q078-081 | `"Mean-field theory" "DNLS" "2026" journal` | Located Sun periodic-box paper, Giusfredi journal metadata and newest peak-bound journal version. |
| Q080 | Q078-081 | `"negative temperatures" Baldovin Iubini Livi Vulpiani 2021 arxiv` | Located Sun periodic-box paper, Giusfredi journal metadata and newest peak-bound journal version. |
| Q081 | Q078-081 | `"wave packet maximum" "2025" "2026" De Roeck` | Located Sun periodic-box paper, Giusfredi journal metadata and newest peak-bound journal version. |
| Q082 | Q082-085 | `"Observation of photon-photon thermodynamic processes" pdf` | Science full text remained unavailable; found tensorial-symmetry paper and screening claim. |
| Q083 | Q082-085 | `"10.1126/science.ade6523" fiber` | Science full text remained unavailable; found tensorial-symmetry paper and screening claim. |
| Q084 | Q082-085 | `"Tensorial symmetries and thermalization of nonlinear lattices" 2025` | Science full text remained unavailable; found tensorial-symmetry paper and screening claim. |
| Q085 | Q082-085 | `"Asymptotic localization" "10.1103/svxt-wsk7"` | Science full text remained unavailable; found tensorial-symmetry paper and screening claim. |
| Q086 | Q086-089 | `"10.1016/j.pquantelec.2026.100632"` | Checked newer rogue-wave review and integrable wave–mean/defocusing papers; no target closure advertised. |
| Q087 | Q086-089 | `"Exactly Solvable Model of Wave-Mean Field Interaction in Integrable Turbulence" arxiv` | Checked newer rogue-wave review and integrable wave–mean/defocusing papers; no target closure advertised. |
| Q088 | Q086-089 | `"Characterizing far from equilibrium states" "nonlinear Schrödinger" 2025` | Checked newer rogue-wave review and integrable wave–mean/defocusing papers; no target closure advertised. |
| Q090 | Q090-093 | `"Optical Thermodynamics beyond the Weak Nonlinearity Limit" arxiv 2026` | Located Kabat 2026 nonideal theory (N4 kill) and Saha–Dubessy preprint route; Sun full text unavailable. |
| Q091 | Q090-093 | `"thermodynamic theory" "highly multimoded" Wu Hassan Christodoulides 2019` | Located Kabat 2026 nonideal theory (N4 kill) and Saha–Dubessy preprint route; Sun full text unavailable. |
| Q092 | Q090-093 | `"Nonlinear Spectra of Integrable Turbulence in a Periodic Box" arxiv` | Located Kabat 2026 nonideal theory (N4 kill) and Saha–Dubessy preprint route; Sun full text unavailable. |
| Q093 | Q090-093 | `"Characterizing far from equilibrium states of the one-dimensional nonlinear Schrödinger equation" arxiv` | Located Kabat 2026 nonideal theory (N4 kill) and Saha–Dubessy preprint route; Sun full text unavailable. |
| Q094 | Q094-097 | `"Optical rogue" "100632" 2026` | Confirmed baseline identifiers; no legitimate Science preprint located. |
| Q095 | Q094-097 | `"Observation of photon-photon" "arxiv"` | Confirmed baseline identifiers; no legitimate Science preprint located. |
| Q096 | Q094-097 | `"Observation of Replica Symmetry Breaking" "1601.01369" "10."` | Confirmed baseline identifiers; no legitimate Science preprint located. |
| Q097 | Q094-097 | `"On the continuous resonant equation for NLS" "10." deterministic` | Confirmed baseline identifiers; no legitimate Science preprint located. |
| Q098 | Q098-101 | `"Characterizing far from equilibrium states" "arXiv"` | Located 2023 resonant obstruction and defocusing diagnostic. A six-wave thesis indexed in 2026 was older work, not a new solution. |
| Q099 | Q098-101 | `"Obstruction to ergodicity in nonlinear Schrödinger equations with resonant potentials" arxiv` | Located 2023 resonant obstruction and defocusing diagnostic. A six-wave thesis indexed in 2026 was older work, not a new solution. |
| Q100 | Q098-101 | `"Critical disorder inflating thermal relaxation" arxiv` | Located 2023 resonant obstruction and defocusing diagnostic. A six-wave thesis indexed in 2026 was older work, not a new solution. |
| Q101 | Q098-101 | `"Six-wave systems in one-dimensional wave turbulence" 2026` | Located 2023 resonant obstruction and defocusing diagnostic. A six-wave thesis indexed in 2026 was older work, not a new solution. |
| Q102 | Q102-105 | `"DNLS" "logarithmic coarsening" 2022 2023 2024 2025 2026` | Focused deterministic coarsening/Anderson/gas search retained the three narrowly stated gaps. |
| Q103 | Q102-105 | `"breather" "coarsening" "deterministic" 2025 2026` | Focused deterministic coarsening/Anderson/gas search retained the three narrowly stated gaps. |
| Q104 | Q102-105 | `"nonlinear Anderson" "asymptotic" "2026" -site:researchgate.net -site:scribd.com` | Focused deterministic coarsening/Anderson/gas search retained the three narrowly stated gaps. |
| Q106 | Q106-109 | `"thermalization" "six-wave" "fiber" 2024 2025 2026 -site:scribd.com -site:researchgate.net` | No controlled exact-target six-wave/coarsening replacement located; newest adiabatic developments checked. |
| Q108 | Q106-109 | `"coarsening" "DNLS" 2026 Hamiltonian -site:researchgate.net -site:scribd.com` | No controlled exact-target six-wave/coarsening replacement located; newest adiabatic developments checked. |
| Q109 | Q106-109 | `"DNLS" "adiabatic invariant" "2025" "2026" -site:researchgate.net -site:scribd.com` | No controlled exact-target six-wave/coarsening replacement located; newest adiabatic developments checked. |
| Q113 | Q110-113 | `"nonlinear Schrödinger" "classical" "correlation functions" attractive gas` | Searched field-correlation/Fredholm routes; returned GHD and deterministic constructions, not finite-density microscopic field spectrum. |
| Q114 | Q114-117 | `"ade6523" "fiber" "loops"` | Science/Wright access search failed to locate a legitimate OA copy; found Gelash 2019 preprint. |
| Q115 | Q114-117 | `"Observation of photon-photon thermodynamic processes" "pdf" Muniz Peschel` | Science/Wright access search failed to locate a legitimate OA copy; found Gelash 2019 preprint. |
| Q116 | Q114-117 | `"Physics of highly multimode nonlinear optical systems" Wright 2022 pdf` | Science/Wright access search failed to locate a legitimate OA copy; found Gelash 2019 preprint. |
| Q122 | Q122-125 | `Rumpf DNLS coarsening 2008 2004 breather relaxation entropy dynamics` | Found earlier Rumpf trail, OA Gradenigo paper, linear fibre-loop localization and nonlinear quantum-walk study. |
| Q123 | Q122-125 | `"10.1088/1742-5468/abda26" arxiv` | Found earlier Rumpf trail, OA Gradenigo paper, linear fibre-loop localization and nonlinear quantum-walk study. |
| Q124 | Q122-125 | `"nonlinear" "Anderson" "fiber loops" experiment` | Found earlier Rumpf trail, OA Gradenigo paper, linear fibre-loop localization and nonlinear quantum-walk study. |
| Q125 | Q122-125 | `"wave packet spreading" "discrete time quantum walks" 2019 nonlinear` | Found earlier Rumpf trail, OA Gradenigo paper, linear fibre-loop localization and nonlinear quantum-walk study. |
| Q126 | Q126-Q129 | `Rumpf 2008 relaxation localized nonlinear Schrodinger coarsening breathers 2004 entropy` | Located Rumpf 2004/2009 and old plateau discrepancy; no new field-spectrum closure. |
| Q127 | Q126-Q129 | `"Basko" "2011" "spreading" "2025" logarithmic` | Located Rumpf 2004/2009 and old plateau discrepancy; no new field-spectrum closure. |
| Q129 | Q126-Q129 | `"classical" "attractive" "nonlinear Schrödinger" "one-body" correlation` | Located Rumpf 2004/2009 and old plateau discrepancy; no new field-spectrum closure. |
| Q130 | Q130-Q133/O011 | `"Stable and metastable states" "Rumpf" pdf` | Located Rumpf 2004 OA; 2009 publisher direct request denied. Found additional DNLS/optical-gas leads. |
| Q131 | Q130-Q133/O011 | `"A simple statistical explanation" "Rumpf" 2004 DOI` | Located Rumpf 2004 OA; 2009 publisher direct request denied. Found additional DNLS/optical-gas leads. |
| Q132 | Q130-Q133/O011 | `"classical nonlinear Schrödinger" "correlation functions" "attractive" spectral` | Located Rumpf 2004 OA; 2009 publisher direct request denied. Found additional DNLS/optical-gas leads. |
| Q134 | Q134-Q137 | `site:tu-chemnitz.de/physik/KSND/benno/ "2009"` | Located Ebrahimi 2025 and Onorato 2022; Rumpf 2009 OA search unsuccessful. |
| Q135 | Q134-Q137 | `"Rumpf" "Stable and metastable states" "pdf" -site:researchgate.net -site:scribd.com` | Located Ebrahimi 2025 and Onorato 2022; Rumpf 2009 OA search unsuccessful. |
| Q136 | Q134-Q137 | `"Dynamics of localised states in the stochastic discrete nonlinear Schrödinger equation" 2025 doi` | Located Ebrahimi 2025 and Onorato 2022; Rumpf 2009 OA search unsuccessful. |
| Q137 | Q134-Q137 | `"Equilibrium and nonequilibrium description of negative temperature states"` | Located Ebrahimi 2025 and Onorato 2022; Rumpf 2009 OA search unsuccessful. |
| Q138 | Q138-Q141 | `"Thermalization in a nonlinear variant of the discrete nonlinear Schrödinger equation"` | Located 2026 fully nonlinear variant, 2025 microcanonical correlations and boundary-driven thermostats. |
| Q139 | Q138-Q141 | `"Localization and" "classical entanglement" "Schrödinger" 2025` | Located 2026 fully nonlinear variant, 2025 microcanonical correlations and boundary-driven thermostats. |
| Q140 | Q138-Q141 | `"Growth or decay of a coherent structure interacting with random waves"` | Located 2026 fully nonlinear variant, 2025 microcanonical correlations and boundary-driven thermostats. |
| Q141 | Q138-Q141 | `"Infinite-temperature thermostats by energy localization"` | Located 2026 fully nonlinear variant, 2025 microcanonical correlations and boundary-driven thermostats. |
| Q142 | Q142-Q144/O012 | `"Growth or decay of a coherent structure interacting with random waves" Chen Rumpf 2021 pdf` | Located Chen–Rumpf abstract, Onorato CHORUS copy and Giachello preprint; distinguished model scopes. |
| Q143 | Q142-Q144/O012 | `"Equilibrium and nonequilibrium description" Onorato arxiv 2021` | Located Chen–Rumpf abstract, Onorato CHORUS copy and Giachello preprint; distinguished model scopes. |
| Q144 | Q142-Q144/O012 | `"Localization and" "classical entanglement" arxiv` | Located Chen–Rumpf abstract, Onorato CHORUS copy and Giachello preprint; distinguished model scopes. |
| Q145 | Q145-Q148 | `"Growth and erosion of a discrete breather interacting with Rayleigh-Jeans distributed phonons" pdf` | Located Rumpf 2007 institutional link; gas first-order/power-spectrum searches found no closure of the specified ensemble. |
| Q146 | Q145-Q148 | `"Rumpf" "26001" "pdf"` | Located Rumpf 2007 institutional link; gas first-order/power-spectrum searches found no closure of the specified ensemble. |

| Q151 | Q149-Q152 | `"10.1103/PhysRevLett.102.209903" erratum spreading` | Located deterministic condensate and KdV numerical work; no random-ensemble field-spectrum closure. Erratum/review access checked next. |
| Q152 | Q149-Q152 | `"Nonlinear waves in optical fibers and photonic waveguides" "2026"` | Located deterministic condensate and KdV numerical work; no random-ensemble field-spectrum closure. Erratum/review access checked next. |
| Q153 | Q153-Q155 | `"Flach" "209903" erratum pdf` | Located legitimate author-hosted erratum; broad 2026 review title query did not locate usable primary text. |
| Q154 | Q153-Q155 | `"Universal Spreading" "Erratum" "2009" corrected` | Located legitimate author-hosted erratum; broad 2026 review title query did not locate usable primary text. |
| Q155 | Q153-Q155 | `"Nonlinear waves in optical fibers and photonic waveguides: theoretical advances and modern applications"` | Located legitimate author-hosted erratum; broad 2026 review title query did not locate usable primary text. |
| Q156 | Q156-Q157 | `"Absence of Wavepacket Diffusion in Disordered Nonlinear Systems" arxiv` | Located the 2008 strong-nonlinearity no-dilution theorem; scope distinguished from weak broad packets. |
| Q157 | Q156-Q157 | `"10.1103/PhysRevLett.100.084103" selftrapping` | Located the 2008 strong-nonlinearity no-dilution theorem; scope distinguished from weak broad packets. |

### Direct web opens, text searches and link follows

| Group | Action and target | Outcome/access |
|---|---|---|
| O001 | open [source](https://arxiv.org/html/2505.11299v1) | See source ledger for the final access level; selected relevant text inspected. |
| O001 | open [source](https://www.nature.com/articles/s41567-022-01691-z) | Abstract only; full text unavailable. |
| O001 | open [source](https://josselin-garnier.org/wp-content/uploads/2025/12/physd2025.pdf) | See source ledger for the final access level; selected relevant text inspected. |
| Q012-Q014/O002 | open [source](https://josselin-garnier.org/list-of-publications/papers/) | See source ledger for the final access level; selected relevant text inspected. |
| Q015-Q017/O003 | find `Optical wave turbulence: Toward` in [source](https://josselin-garnier.org/list-of-publications/papers/) | See source ledger for the final access level; selected relevant text inspected. |
| Q015-Q017/O003 | find `4 Conclusions` in [source](https://arxiv.org/html/2505.11299v1) | See source ledger for the final access level; selected relevant text inspected. |
| Q015-Q017/O003 | find `open` in [source](https://arxiv.org/html/2505.11299v1) | See source ledger for the final access level; selected relevant text inspected. |
| O004 | open [source](https://arxiv.org/abs/2201.02529) | See source ledger for the final access level; selected relevant text inspected. |
| O004 | open [source](https://arxiv.org/abs/2304.06541) | See source ledger for the final access level; selected relevant text inspected. |
| O004 | open [source](https://arxiv.org/abs/2502.08463) | See source ledger for the final access level; selected relevant text inspected. |
| O004 | open [source](https://arxiv.org/abs/2308.10572) | See source ledger for the final access level; selected relevant text inspected. |
| O004 | follow author publication-list PDF link [source](https://josselin-garnier.org/wp-content/uploads/2014/08/physrep14.pdf) | See source ledger for the final access level; selected relevant text inspected. |
| O005 | open [source](https://arxiv.org/abs/1501.03760) | See source ledger for the final access level; selected relevant text inspected. |
| O005 | open [source](https://arxiv.org/abs/1601.01369) | See source ledger for the final access level; selected relevant text inspected. |
| O005 | open [source](https://www.science.org/doi/10.1126/science.ade6523) | Full text unavailable/denied; abstract and indexed primary passages only. |
| O006 | open [source](https://link.aps.org/pdf/10.1103/svxt-wsk7) | Journal full text read through web, including self-screening section; local download failed. |
| O006 | open [source](https://doi.org/10.1126/science.ade6523) | Full text unavailable/denied; abstract and indexed primary passages only. |
| O006 | open [source](https://link.springer.com/article/10.1007/s10773-025-06079-2) | Abstract only; no legitimate OA full text found. |
| O007 | open at indexed line 115 [source](https://link.aps.org/pdf/10.1103/svxt-wsk7) | Journal full text read through web, including self-screening section; local download failed. |
| O007 | open at indexed line 275 [source](https://link.aps.org/pdf/10.1103/svxt-wsk7) | Journal full text read through web, including self-screening section; local download failed. |
| O007 | open at indexed line 450 [source](https://link.aps.org/pdf/10.1103/svxt-wsk7) | Journal full text read through web, including self-screening section; local download failed. |
| O007 | open [source](https://doi.org/10.1016/j.pquantelec.2026.100632) | Located 2026 rogue-wave review; abstract-level scope screen, not used as a novelty premise. |
| O007 | open [source](https://scipost.org/SciPostPhysCore.8.1.028) | Access challenge/Anubis page; not bypassed. Used the arXiv abstract. |
| O008 | open [source](https://arxiv.org/abs/2210.09812) | See source ledger for the final access level; selected relevant text inspected. |
| O008 | open [source](https://arxiv.org/abs/2606.08321) | See source ledger for the final access level; selected relevant text inspected. |
| O008 | open [source](https://journals.aps.org/prl/abstract/10.1103/372m-bnpr) | See source ledger for the final access level; selected relevant text inspected. |
| O009 | open [source](https://link.aps.org/pdf/10.1103/PhysRevLett.123.234102) | Publisher route led to abstract/indexed text; OA arXiv preprint subsequently read. |
| O009 | open [source](https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2021.736774/full) | See source ledger for the final access level; selected relevant text inspected. |
| O009 | open [source](https://www.nature.com/articles/s41377-024-01475-5) | Publisher request failed/redirected toward login; no login. OA arXiv version read. |
| O010 | find `nonlinear` in [source](https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2021.736774/full) | See source ledger for the final access level; selected relevant text inspected. |
| O010 | find `doi:` in [source](https://pmc.ncbi.nlm.nih.gov/articles/PMC5487357/) | CAPTCHA/recaptcha blocked full-text access; not bypassed. |
| O010 | find `nonlinear` in [source](https://pmc.ncbi.nlm.nih.gov/articles/PMC5487357/) | CAPTCHA/recaptcha blocked full-text access; not bypassed. |
| Q130-Q133/O011 | open [source](https://arxiv.org/abs/nlin/0312058) | See source ledger for the final access level; selected relevant text inspected. |
| Q130-Q133/O011 | open [source](https://www.sciencedirect.com/science/article/pii/S0167278909002541) | Direct open returned HTTP 403; publisher-indexed abstract/introduction available via search. |
| Q142-Q144/O012 | open [source](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.104.034213) | See source ledger for the final access level; selected relevant text inspected. |
| Q142-Q144/O012 | open [source](https://journals.aps.org/pre/abstract/10.1103/nfym-zysm) | See source ledger for the final access level; selected relevant text inspected. |
| O013 | open [source](https://www.tu-chemnitz.de/physik/KSND/forschung/publikationen.html) | See source ledger for the final access level; selected relevant text inspected. |
| O013 | open [source](https://link.aps.org/accepted/10.1103/PhysRevE.105.014206) | CHORUS full text readable via web; local HTTP retrieval failed. |
| O014 | find `Stable and` in [source](https://www.tu-chemnitz.de/physik/KSND/forschung/publikationen.html) | See source ledger for the final access level; selected relevant text inspected. |
| O014 | find `Growth and Erosion` in [source](https://www.tu-chemnitz.de/physik/KSND/forschung/publikationen.html) | See source ledger for the final access level; selected relevant text inspected. |
| O015 | follow institutional publication-list link [source](https://epljournal.edpsciences.org/10.1209/0295-5075/78/26001) | HTTP 403; no primary full text accessed. |

| O016 | open [Flach erratum publisher page](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.102.209903) | Tool access failed; subsequently found legitimate author PDF. |
| O016 | open [Gkogkou et al. preprint](https://arxiv.org/abs/2502.14749) | Abstract/version metadata read; v3 dated 28 January 2026. |
| O016 | open [2026 broad optical-wave review DOI](https://doi.org/10.1088/1402-4896/aeb196) | Tool access failed; index-only lead not used as scientific evidence. |

### Forward-citation screens

For each anchor, the first request was `https://api.openalex.org/works/https://doi.org/<DOI>`. The second was the works endpoint with `filter=cites:<OpenAlex ID>,from_publication_date:2021-01-01,to_publication_date:2026-10-20`, `per-page=200`, `sort=publication_date:desc`, and `select=id,doi,title,publication_date,abstract_inverted_index,primary_location`. All returned sets fitted one page. These are metadata/title screens, with focused abstract and full-text follow-up of plausible resolutions; not full-text reading of every citer. Counts overlap between anchors and include index duplicates. Index dates were checked against paper versions when relevant.

| Anchor | DOI | OpenAlex ID | Retrieved / indexed in date window | Follow-up outcome |
|---|---|---|---|---|
| Frozen dynamics of a breather induced by an adiabatic invariant | 10.1088/1742-5468/ac650e | W4221149523 | 5 / 5 | D14/D20 and related papers; rare jumps remain explicit gap. |
| Destruction of Anderson Localization by a Weak Nonlinearity | 10.1103/PhysRevLett.100.094101 | W2040358363 | 105 / 105 | A7–A11; model-by-model resolution audit above. |
| Dramatic Acceleration of Wave Condensation Mediated by Disorder in Multimode Fibers | 10.1103/PhysRevLett.122.123902 | W2923649000 | 72 / 72 | Disorder kinetics and later review; no new broad rate-paradox card. |
| Modal phase-locking in multimode nonlinear optical fibers | 10.1364/OL.494543 | W4381333009 | 13 / 13 | Phase-locking and adjacent correlator work; existing card retained. |
| Influence of third-order dispersion on the propagation of incoherent light in optical fibers | 10.1364/OL.35.002367 | W1984424087 | 2 / 2 | No validated six-wave physical-fibre gap established. |
| Dynamical Freezing of Relaxation to Equilibrium | 10.1103/PhysRevLett.122.084102 | W2901250678 | 37 / 37 | D10–D23; separate reservoir/noisy/equilibrium advances. |
| On the continuous resonant equation for NLS. I. Deterministic analysis | 10.1016/j.matpur.2015.10.002 | W1828618774 | 23 / 23 | O5/O6 and mathematical work; no complete new optical target established. |
| Thermodynamic theory of highly multimoded nonlinear optical systems | 10.1038/s41566-019-0501-8 | W2967343525 | 171 / 171 | O12 directly addresses generic beyond-weak-nearest-neighbour thermodynamics. |
| Glassy behavior in a one-dimensional continuous-wave erbium-doped random fiber laser | 10.1103/PhysRevA.94.011801 | W2221996257 | 55 / 55 | O16 supplies microscopic model/validation; N3 killed as framed. |
| Simple statistical explanation for the localization of energy in nonlinear lattices with two conserved quantities | 10.1103/PhysRevE.69.016618 | W2026891627 | 24 / 24 | D13/D15–D21 and equilibrium literature; exact-target coarsening not closed. |
| Stable and metastable states and the formation and destruction of breathers in the discrete nonlinear Schrödinger equation | 10.1016/j.physd.2009.08.006 | W1987082546 | 22 / 22 | D13/D15–D23; old metastability and latest variants checked. |
| Self-organization in nonlinear wave turbulence | 10.1103/PhysRevE.61.1527 | W1987202682 | 18 / 18 | Later coherent-structure/statistical work; existing registry home. |
| Integrable turbulence and formation of rogue waves | 10.1088/0951-7715/28/8/2791 | W1700452290 | 74 / 74 | G2–G11; finite-density microscopic field spectrum not found. |
| Observation of the kinetic condensation of classical waves | 10.1038/nphys2278 | W2076280943 | 50 / 50 | Recent kinetics and reviews; generic universality proposal parked. |

The exact URL-encoded requests and returned metadata are saved externally in `citers-*.json`. Additional OpenAlex work lookups used the same DOI endpoint for 10.1126/science.ade6523, 10.1038/s41567-022-01691-z, 10.1007/s10773-025-06079-2, 10.1088/1742-5468/abda26, 10.1103/PhysRevLett.122.040501 and 10.1103/PhysRevLett.123.234102 to check publication identifiers and legitimate OA locations. Science, Wright and Sun had no usable OA copy located by this process. Direct arXiv metadata reads additionally checked `/abs/1601.01369`, `/abs/1501.03760`, `/abs/2312.10898`, `/abs/2511.09206` and `/abs/1005.5033`; these confirmed titles/identifiers and did not substitute for full-text reading.

### Direct PDF retrieval manifest, including failures

`HTTP 200` below means an actual PDF was saved outside git. A successful download alone does not imply it was read; the source ledger states the reading depth. Failed publisher requests were not bypassed; separate legitimate author/arXiv copies were used where located.

| Local key | Requested URL | Result |
|---|---|---|
| `picozzi2014` | [request](https://josselin-garnier.org/wp-content/uploads/2014/08/physrep14.pdf) | HTTP 200; PDF saved |
| `ferraro2025` | [request](https://arxiv.org/pdf/2505.11299) | HTTP 200; PDF saved |
| `suret2024` | [request](https://arxiv.org/pdf/2304.06541) | HTTP 200; PDF saved |
| `politi2022` | [request](https://arxiv.org/pdf/2201.02529) | HTTP 200; PDF saved |
| `milovanov2025` | [request](https://arxiv.org/pdf/2502.08463) | HTTP 200; PDF saved |
| `deroeck2024` | [request](https://arxiv.org/pdf/2308.10572) | HTTP 200; PDF saved |
| `iubini2019` | [request](https://arxiv.org/pdf/1811.05798) | HTTP 200; PDF saved |
| `ebrahimi2026` | [request](https://arxiv.org/pdf/2512.01448) | HTTP 200; PDF saved |
| `iubini2013` | [request](https://strathprints.strath.ac.uk/42959/1/NJP15_23032_13.pdf) | HTTP 200; PDF saved |
| `fishman2012` | [request](https://arxiv.org/pdf/1108.2956) | HTTP 200; PDF saved |
| `laptyeva2014` | [request](https://arxiv.org/pdf/1407.1441) | HTTP 200; PDF saved |
| `deroeck2025` | [request](https://arxiv.org/pdf/2502.02344) | HTTP 200; PDF saved |
| `iubini2025` | [request](https://arxiv.org/pdf/2406.15140) | HTTP 200; PDF saved |
| `giusfredi2026` | [request](https://arxiv.org/pdf/2511.09206) | HTTP 200; PDF saved |
| `das2026` | [request](https://arxiv.org/pdf/2602.22878) | HTTP 200; PDF saved |
| `agafontsev2015` | [request](https://arxiv.org/pdf/1409.4692) | HTTP 200; PDF saved |
| `elliptic2025` | [request](https://arxiv.org/pdf/2411.06922) | HTTP 200; PDF saved |
| `ballistic2026` | [request](https://arxiv.org/pdf/2601.21085) | HTTP 200; PDF saved |
| `koch2022` | [request](https://arxiv.org/pdf/2110.14574) | HTTP 200; PDF saved |
| `lifetime2025` | [request](https://arxiv.org/pdf/2411.06044) | HTTP 200; PDF saved |
| `persistence2025` | [request](https://arxiv.org/pdf/2308.11243) | HTTP 200; PDF saved |
| `pikovsky2008` | [request](https://arxiv.org/pdf/0708.3315) | HTTP 200; PDF saved |
| `johansson2010` | [request](https://arxiv.org/pdf/1007.1912) | HTTP 200; PDF saved |
| `basko2011` | [request](https://arxiv.org/pdf/1005.5033) | HTTP 200; PDF saved |
| `rfl2024` | [request](https://arxiv.org/pdf/2312.10898) | HTTP 200; PDF saved |
| `negative_review2021` | [request](https://arxiv.org/pdf/2103.12572) | HTTP 200; PDF saved |
| `flach2009` | [request](https://arxiv.org/pdf/0805.4693) | HTTP 200; PDF saved |
| `germain2016` | [request](https://arxiv.org/pdf/1501.03760) | HTTP 200; PDF saved |
| `gomes2016` | [request](https://arxiv.org/pdf/1601.01369) | HTTP 200; PDF saved |
| `nonideal2026` | [request](https://arxiv.org/pdf/2602.13161) | HTTP 200; PDF saved |
| `milovanov_journal` | [request](https://link.aps.org/pdf/10.1103/svxt-wsk7) | HTTP Error 403: Forbidden |
| `tensorial2025` | [request](https://resolve.cambridge.org/core/services/aop-cambridge-core/content/view/FB5A246A81E51323B7D3A0C2F41068A7/S3033426825100259a.pdf/tensorial_symmetries_and_thermalization_of_nonlinear_lattices.pdf) | HTTP Error 403: Forbidden |
| `coarsen2014` | [request](https://arxiv.org/pdf/1308.4870) | HTTP 200; PDF saved |
| `coarsen2017` | [request](https://arxiv.org/pdf/1701.08636) | HTTP 200; PDF saved |
| `gradenigo2021` | [request](https://arxiv.org/pdf/2106.03698) | HTTP 200; PDF saved |
| `biasedgrin2023` | [request](https://arxiv.org/pdf/2304.10308) | HTTP 200; PDF saved |
| `anomalous2026` | [request](https://arxiv.org/pdf/2512.17777) | HTTP 200; PDF saved |
| `gelash2019` | [request](https://arxiv.org/pdf/1907.07914) | HTTP 200; PDF saved |
| `gradenigo_full2021` | [request](https://arxiv.org/pdf/1910.07461) | HTTP 200; PDF saved |
| `walk2019` | [request](https://arxiv.org/pdf/1806.06345) | HTTP 200; PDF saved |
| `rumpf2004` | [request](https://arxiv.org/pdf/nlin/0312058) | HTTP 200; PDF saved |
| `stochastic25` | [request](https://www.math.uni-rostock.de/~wj/ms/pre_25.pdf) | HTTP 200; PDF saved |
| `grandcanonical25` | [request](https://research-portal.uea.ac.uk/files/196144549/Accepted_Manuscript.pdf) | HTTP Error 403: Forbidden |
| `entanglement2025` | [request](https://iris.cnr.it/retrieve/3a4ab138-9369-465a-b2e1-94942c306df1/jstat25_Giachello.pdf) | HTTP Error 403: Forbidden |
| `variant2026` | [request](https://arxiv.org/pdf/2601.13472) | HTTP 200; PDF saved |
| `entanglement2025` | [request](https://arxiv.org/pdf/2503.14364) | HTTP 200; PDF saved |
| `onorato2022` | [request](https://link.aps.org/accepted/10.1103/PhysRevE.105.014206) | HTTP Error 403: Forbidden |
| `flach_erratum2009` | [request](https://pcs.ibs.re.kr/~sflach/publications.DIR/2009/prl_102_209903_2009.pdf) | HTTP 200; PDF saved and read |

The complete web request objects are saved externally as `web-query-log.json`. The old six-wave repository hit assigned a 2026 index date was not treated as newly published research. Direct source access, publication date, preprint version, and index crawl date were kept distinct. No numerical propagation, symbolic derivation, or new scientific numerical estimate was performed, so no run folder was created. Citation-screen counts are bibliographic bookkeeping, not simulation results.

## Follow-up tasks and completion

| Task | Purpose |
|---|---|
| [T-20261020-gpt-g-01](../tasks/T-20261020-gpt-g-01-pi-download-wright-2022-multimode-review.md) | PI download: Wright 2022 multimode review |
| [T-20261020-gpt-g-02](../tasks/T-20261020-gpt-g-02-pi-download-sun-2025-nonlinear-spectra.md) | PI download: Sun 2025 nonlinear spectra |
| [T-20261020-gpt-g-03](../tasks/T-20261020-gpt-g-03-pi-download-rumpf-2007-phonon-exchange.md) | PI download: Rumpf 2007 phonon exchange |
| [T-20261020-gpt-g-04](../tasks/T-20261020-gpt-g-04-pi-download-rumpf-2009-metastable-states.md) | PI download: Rumpf 2009 metastable states |
| [T-20261020-gpt-g-05](../tasks/T-20261020-gpt-g-05-pi-download-science-2023-optical-loop.md) | PI download: Science 2023 optical loop |
| [T-20261020-gpt-g-06](../tasks/T-20261020-gpt-g-06-scope-oracle-and-analytical-preflight-af.md) | Scope oracle and analytical preflight after audit |

The scouting review and three candidate cards are complete; the session log and task completion note record final repository checks and PR delivery. The five downloads and conditional technical preflight remain explicitly queued; they do not imply that those sources were fully audited here. No new cross-family review task was created.
