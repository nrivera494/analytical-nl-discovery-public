---
id: P-002
title: "Multimode solitons with internal modal dynamics in GRIN fiber"
status: audited
priority: 2
literature_state: partial
novelty_confidence: low
target_quantity: "A controlled phase-aware reduction for modal evolution inside a bound pulse, with a launch-dependent walk-off boundary and a measurable fundamental-mode capture length."
model: "Multimode GNLSE in graded-index fiber with Kerr and Raman terms; separately specified random mode coupling."
oracle_ready: available
last_audited: 2026-10-02
audited_by: [claude, gpt]
proposed_by: claude-bootstrap
updated_by: gpt-a
updated_model: gpt-6-astra
updated_family: gpt
claims: [C-0002, C-20261004-gpt-a-01]
results: []
---

## Target quantity

Derive a reduced evolution for a temporally bound pulse's modal amplitudes or coherence matrix, and specify the additional averaging limit in which occupations alone close. Predict the longitudinal transfer into the fundamental mode and a capture length defined by a fixed modal-fraction criterion. Separate this from the pulse's Raman frequency drift and from loss of radiation outside the measured pulse.

A second target is the existence/formation boundary and selected duration of walk-off solitons, including launch modal weights and frequency shifts. The answer must state its dimensionless regime in self-imaging, dispersion, walk-off, nonlinear, Raman and random-coupling lengths. A universal duration or prefactor depending only on the fiber is not supported by the cited work.

## Signal of hidden simplicity

Published experiments and simulations show temporally aligned multimode pulses, duration selection in the walk-off regime, and long-distance transfer toward a fundamental-mode soliton. These are distinct observations, not evidence that all bound pulses share a Rayleigh–Jeans attractor. The seed's unreferenced 120-mode/1,035-mode simulation anecdote is removed because no source or run was supplied.

The weak-admixture exploration now supplies a parameter-derived finite-distance response map with self-phase, pump response and generated LP03 kept at the same order. Its corrected minority-field error scales with exponents 3.99635–4.00076 against the minority amplitude, versus 1.99408–2.00087 before correction (`2026-10-04-gpt-a-nextorder-full`). This is proposer evidence for C-20261004-gpt-a-01, not an independently verified modal-kinetic closure. The operational half-retention threshold is distinct from a literal zero-capture scattering boundary.

## Literature state

- Renninger & Wise (2013), [DOI:10.1038/ncomms2739](https://doi.org/10.1038/ncomms2739): **full text**, coupled-field, variational and experimental sections. Besides observations and simulations, it gives an approximate variational fixed point and tests energy–duration/Raman trends. Calling it “observation and numerics” missed analytical prior work. Its reduced single-field model neglects modal group-velocity differences.
- Wright et al. (2015), [DOI:10.1364/OE.23.003492](https://doi.org/10.1364/OE.23.003492), *Spatiotemporal dynamics of multimode optical solitons*: formation, fission and Raman dynamics from experiments and multimode simulations. **Abstract only.**
- Zitelli et al. (2021), [DOI:10.1038/s42005-021-00687-0](https://doi.org/10.1038/s42005-021-00687-0), *Conditions for walk-off soliton generation in a multimode fiber*: **full text**, walk-off theory and discussion. Gives a length-balance duration law using modal-weighted group delay and an empirical constant; that constant and the selected pulse depend on input coupling. This is a useful semi-analytic prediction, not a parameter-free universal formation boundary.
- Zitelli et al. (2021), [DOI:10.1364/PRJ.419235](https://doi.org/10.1364/PRJ.419235), *Single-mode spatiotemporal soliton attractor in multimode GRIN fibers*: **full text**, Sec. 2.A and experimental/conclusion sections. Already approximates fundamental-mode energy transfer by an exponential with an energy-dependent rate. The rate is not derived from launch/overlap parameters there. The coupled-mode simulations include Raman and wavelength-dependent loss but omit random linear coupling. This provides a phenomenological capture baseline, not only an observation.
- Zitelli, Mangini & Wabnitz (2024), [DOI:10.1038/s41467-024-45185-3](https://doi.org/10.1038/s41467-024-45185-3): **full text**, statistical derivation and fitting procedure. Derives a weighted Bose–Einstein form by entropy maximization and fits thermodynamic parameters. It is not an unexplained empirical fit, but it is not a longitudinal coherent-pulse kinetic closure either. Zitelli, [DOI:10.1002/lpor.202400714](https://doi.org/10.1002/lpor.202400714), online 2024/volume 2025, [arXiv:2404.00480](https://arxiv.org/abs/2404.00480): **full text of the preprint**, theory, methods and discussion. Adds state/entropy equations and a consistency metric under conserved or proportionally scaled power/internal energy. It reanalyzes output distributions and discusses dispersion/Raman limits, without deriving a longitudinal capture rate.
- [arXiv:2605.02511](https://arxiv.org/abs/2605.02511), *Influence of Refractive Index Distribution on Multimode Soliton Dynamics and Condensation in GRIN-MMFs*: **full text**, model and conclusion inspected. GMMNLSE simulations including Raman and self-steepening show profile-dependent transfer, including flow toward higher-order modes in some cases. This supports the seed's reversal attribution, but not a universal analytical rate.
- Wu, Bender, Christodoulides & Wise (2023), [arXiv:2307.09554](https://arxiv.org/abs/2307.09554), [DOI:10.1063/5.0166177](https://doi.org/10.1063/5.0166177): highly multimode step-index solitons with complex spatial spectra, experiment and numerical modeling. **Full text**, introduction/results accessed. The paper demonstrates formation; its introductory question must not be quoted as if the paper left existence unanswered. Step-index observations do not establish a GRIN capture law.
- Mecozzi, Antonelli & Shtaif (2012), [arXiv:1203.6275](https://arxiv.org/abs/1203.6275): generalized Manakov averaging for strong random coupling. **Abstract only.** Mumtaz, Essiambre & Agrawal (2013), [arXiv:1207.6645](https://arxiv.org/abs/1207.6645), [DOI:10.1109/JLT.2012.2231401](https://doi.org/10.1109/JLT.2012.2231401): weak/strong coupling averaging regimes. **Abstract only.** Neither licenses replacing phase-sensitive overlap contractions by occupations for every coherent soliton.
- Resolved the seed's author-only reduced-model references: Karlsson, Anderson & Desaix (1992), [DOI:10.1364/OL.17.000022](https://doi.org/10.1364/OL.17.000022), variational spatial dynamics; Raghavan & Agrawal (2000), [DOI:10.1016/S0030-4018(00)00727-6](https://doi.org/10.1016/S0030-4018(00)00727-6), variational spatiotemporal stabilization; Conforti et al. (2017), [arXiv:1707.09223](https://arxiv.org/abs/1707.09223), effective 1+1D GNLSE with periodic nonlinearity; Ahsan & Agrawal (2018), [DOI:10.1364/OL.43.003345](https://doi.org/10.1364/OL.43.003345), averaging when dispersion length exceeds self-imaging period. **Abstract only for each.** These are existing reductions, not evidence that reduction itself is new.
- Menyuk (1988), [DOI:10.1364/JOSAB.5.000392](https://doi.org/10.1364/JOSAB.5.000392), and Steiglitz & Rand (2009), [DOI:10.1103/PhysRevA.79.021802](https://doi.org/10.1103/PhysRevA.79.021802): **full text** read for the new derivation. Menyuk was accessed through public paper OCR with equation-rendering limitations; the latter through the author PDF. Access details, model distinctions and targeted novelty searches are in [the next-order exploration](../explorations/2026-10-04-gpt-a-next-order-capture.md). Weak-probe trapping itself is established prior work.
- Soffer & Weinstein (2005), [DOI:10.1103/PhysRevLett.95.213905](https://doi.org/10.1103/PhysRevLett.95.213905), [arXiv:nlin/0512059](https://arxiv.org/abs/nlin/0512059): **full text**, author PDF. Radiative master equations and algebraic ground-state selection are established mechanisms; applicability to the moving GRIN soliton still needs derivation. The [radiative-onset exploration](../explorations/2026-10-04-gpt-a-radiative-boundary-lead.md) treats that distinction explicitly.

## Sharpest statement of the gap

The remaining opportunity is a **controlled closure for evolving modal content inside a localized coherent pulse**, and a predictive capture/formation law beyond existing fixed-profile, self-imaging-averaged or random-coupling limits. The 2021 exponential capture approximation is a baseline to predict and delimit, not a novel functional form to propose. No general parameter-derived capture law was located in this audit. The seed's occupation-only effective-nonlinearity formula is an assumption to test, not the definition of a valid reduction. Relative phases and mode-dependent carrier frequencies may be indispensable variables. Equilibrium maximum-entropy distributions do not by themselves prove relaxation inside a soliton.

Searches (2026-10-01): `multimode soliton modal kinetics capture rate`; `walk-off soliton duration prefactor`; `GRIN variational effective nonlinear Schrodinger equation`; Manakov strong-coupling and vector-soliton trapping; exact-title/author trails from Renninger–Wise through Conforti/Ahsan and the Zitelli 2021–2026 papers; step-index soliton formation. BEC/Gross–Pitaevskii variational descriptions were checked as neighboring models. Access remains incomplete for several journal articles, so confidence is low.

## Conjectures

`C-0002` was **withdrawn** by its proposing family (claude-b, T-20261002-claude-interactive-04, 2026-10-04). Its motivating 120-mode anecdote was unsourced. Its occupation-only closure is the assumption this card says must be tested. For the GRIN overlap matrix no equal-width common-sech multimode soliton exists even at frozen occupations (review of P-20261004-root-03). A future claim should start from this card's target and the round-1 capture tests (T-20261004-claude-interactive-02 and -07).

`C-20261004-gpt-a-01` is `cheap-checks-passed`, with proposer comparisons of a finite-time weak-LP02 response expansion, an operational half-retention level set, and a spectral detuning bound. It does not claim a zero-capture boundary at infinite distance or a universal exponential transfer law. Independent Claude verification is `T-20261004-gpt-a-03`; the unresolved scattering boundary is `T-20261004-gpt-a-04`.

The separate radiative-onset exploration supplies a stationary outgoing-wave coefficient and a closed gamma-function evaluation. Its driven-source checks do not establish a full nonlinear capture boundary. Higher-mode channels and pulse motion make that identification premature (`2026-10-04-gpt-a-radiation-onset-response`, `2026-10-04-gpt-a-radiation-onset-closed-form`, `2026-10-04-gpt-a-radiation-onset-pilot`).

## Oracle

The rotating-wave scalar radial Kerr evaluator has now been exercised against an independent response solver, with window, step, temporal resolution, modal dispersion and a fourth-mode check (`2026-10-04-gpt-a-nextorder-full`, `2026-10-04-gpt-a-nextorder-response-checks`, `2026-10-04-gpt-a-nextorder-convergence`). This establishes a limited starting oracle; it does not establish the full Raman/random-coupling target model.

The cheap phase test needs a populated independent phase invariant. A two-mode launch is an exact symmetry null control in this model. Seeding LP03 at fixed power and varying its phase changes subsequent transfer, excluding an instantaneous deterministic occupation-only closure for those launches (`2026-10-04-gpt-a-nextorder-phase`). An averaged closure under explicit phase mixing remains a separate question. Reference bound-channel projection, finite-window energy and infinite-distance captured energy must continue to be distinguished.

## Lab test

Cut-back modal decomposition and pulse characterization with controlled launch weights and phases. Measure a stated fundamental-mode fraction versus length and frequency-resolved temporal locking, not only the final beam waist.

## Risks and must-reads

The capture observable needs a pulse window and a launch ensemble. Conservative Kerr dynamics alone need not generate irreversible universal relaxation. Compare any rate prediction against the inspected 2021 capture fit and thermodynamic descriptions; check the 2026 index-profile simulations independently before using them as a benchmark. Entropy maximization and a state-equation residual do not independently establish a kinetic closure. A reduction that simply repeats existing self-imaging averaging is not novel.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-01 | claude-bootstrap (claude) | Created; literature_state partial | Literature audit, Oct 2026 |
| 2026-10-01 | gpt-a (gpt; model unknown) | candidate → audited; medium → low novelty confidence; retained priority 2; narrowed to phase-aware kinetics/capture | Variational fixed point in 2013; launch-dependent 2021 walk-off law; entropy derivation in 2024; established effective-NLS/Manakov reductions |
| 2026-10-02 | gpt-a (gpt; model unknown) | Recovered attractor and thermodynamics full texts; retained disposition and narrowed capture novelty | DOI:10.1364/PRJ.419235 Sec. 2.A gives an exponential approximation without a parameter-derived decay rate; arXiv:2404.00480 gives state/entropy equations rather than capture kinetics |
| 2026-10-04 | claude-b (claude; claude-opus-5-5) | Claim status text updated: C-0002 withdrawn by the proposing family; no change to status, priority or literature_state | T-20261002-claude-interactive-04 |
| 2026-10-04 | gpt-a (gpt; gpt-6-astra) | Added a next-order finite-distance claim and phase-sensitive oracle checks; retained audited status, partial literature and low novelty confidence | C-20261004-gpt-a-01; `2026-10-04-gpt-a-nextorder-full`, `2026-10-04-gpt-a-nextorder-boundary`, `2026-10-04-gpt-a-nextorder-phase`; two required trapping papers read with access recorded in the exploration |
