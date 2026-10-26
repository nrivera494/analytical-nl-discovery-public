---
id: P-005
title: "Finite-pulse limits of multimode optical thermalization"
status: audited
priority: 5
literature_state: partial
novelty_confidence: low
target_quantity: "A finite-duration, finite-length crossover law for joint mode-frequency relaxation, distinct from known spatial equilibrium and stationary-wave kinetic theory."
model: "Weakly nonlinear multimode GNLSE with specified temporal envelope, dispersion, modal walk-off and random coupling; gain/loss only in a separately defined driven model."
oracle_ready: available
last_audited: 2026-10-01
audited_by: [claude, gpt]
proposed_by: claude-bootstrap
updated_by: gpt-a
updated_model: unknown
updated_family: gpt
claims: []
results: []
---

## Target quantity

Predict whether a pulse reaches an approximately local joint mode-frequency distribution before dispersion and modal walk-off dilute the interaction, and the occupied bandwidth at a finite output length. State an asymptotic regime through pulse duration/coherence time, dispersion/nonlinear/walk-off lengths and modal detunings. The answer should predict a measurable crossover or scaling, not choose a numerical FFT cutoff and call it a physical equilibrium.

Two secondary ideas remain unready: detuning-controlled prethermal lifetimes require a specified approximately conserved quantity and plateau diagnostic; a driven steady distribution requires a specified saturating gain, loss and boundary model. Mode-dependent gain alone does not define a stationary thermodynamic problem.

## Signal of hidden simplicity

Spatial Rayleigh–Jeans laws successfully describe measurements made with pulsed sources, often with time integration or spectral filtering. This must be distinguished from equilibration over the entire temporal-frequency continuum. Weighted Bose–Einstein distributions have published entropy-based derivations; the seed's “pulsed fits with no derivation” was inaccurate.

## Literature state

- Wu, Hassan & Christodoulides (2019), [DOI:10.1038/s41566-019-0501-8](https://doi.org/10.1038/s41566-019-0501-8): equilibrium thermodynamic framework/equations of state for highly multimoded nonlinear systems. **Abstract only.** Pourbeyram et al. (2022), [DOI:10.1038/s41567-022-01579-y](https://doi.org/10.1038/s41567-022-01579-y): measured modal RJ relaxation, Hamiltonian conservation and degenerate-mode equipartition. **Abstract only.** Neither should be summarized as evidence applying only to CW experiments.
- Baudin et al. (2020), [DOI:10.1103/PhysRevLett.125.244101](https://doi.org/10.1103/PhysRevLett.125.244101): experimental condensation transition and thermodynamic characterization. **Abstract only.** Ferraro et al. (2024), [DOI:10.1103/PhysRevX.14.021020](https://doi.org/10.1103/PhysRevX.14.021020): calorimetry and heat-capacity interpretation of nonlinear multimode light. **Abstract only.** These establish substantial equilibrium theory, not a general time-resolved pulse closure.
- Zitelli, Mangini & Wabnitz (2024), [DOI:10.1038/s41467-024-45185-3](https://doi.org/10.1038/s41467-024-45185-3): **full text**, weighted-Bose–Einstein entropy derivation and fitting method; see P-002 for its coherent-soliton limitations.
- Ferraro et al., [arXiv:2505.11299](https://arxiv.org/abs/2505.11299), *Wave turbulence, thermalization and multimode locking in optical fibers* (Physica D 481, 134758, 2025): **full text**, kinetic assumptions, disorder regimes and Secs. 3–4. Derives/reviews kinetic rates and makes explicit that the spatial theory neglects temporal dynamics; experiments include femtosecond-to-nanosecond sources and finite detection bandwidth. Weak disorder can assist relaxation; strong-disorder behavior has a separate derivation. This is not a blanket statement that every disorder accelerates thermalization.
- Berti et al. (2022), [arXiv:2207.08680](https://arxiv.org/abs/2207.08680), [DOI:10.1103/PhysRevLett.129.063901](https://doi.org/10.1103/PhysRevLett.129.063901): theory, simulations and experiments on thermalization with **strong** disorder. **Abstract only.** Its regime should not be conflated with the weak-disorder result.
- Major missing prior work: Zanaglia et al., [arXiv:2506.23536](https://arxiv.org/abs/2506.23536), [DOI:10.1103/mqzh-w2gh](https://doi.org/10.1103/mqzh-w2gh) (PRL 136, 053802, 2026): **full text**, model, hybrid discrete/continuous kinetic equation and cooling discussion. Treats temporally stationary incoherent light, derives joint mode-frequency kinetic dynamics and local RJ behavior, and analyzes ultraviolet spectral expansion as intrinsic adiabatic cooling. Thus “no resolution of the temporal ultraviolet problem” is not defensible. Its stationary input assumption does not resolve an isolated finite pulse's dilution/collision-time competition.
- [arXiv:2512.17777](https://arxiv.org/abs/2512.17777), *Irreversible thermalization vs reversible dynamics mediated by anomalous correlators*: **full text**, normal/anomalous correlator equations and conclusions. Derives an instability criterion and reversible phase-correlation dynamics for coupled polarization waves, with experiments; explicitly distinguishes those from irreversible wave kinetics. Occupations need not form a closed description. This is specific analytical prior art, not merely a warning that standard kinetics might fail.
- Bastianello et al., [arXiv:2503.16526](https://arxiv.org/abs/2503.16526), [DOI:10.1103/xz2w-hndp](https://doi.org/10.1103/xz2w-hndp) (PRA 113, 013514, 2026): GGE observed in defocusing single-mode fiber, including a rapidity density of states and predicted power statistics. **Abstract only.** It is an integrable-limit benchmark, not multimode RJ equilibrium.
- Kalashnikov, Rudenkov & Sorokina, [arXiv:2307.16571](https://arxiv.org/abs/2307.16571): dissipative-soliton thermodynamic analogy. **Abstract only.** Churkin et al. (2015), [DOI:10.1038/ncomms7214](https://doi.org/10.1038/ncomms7214): nonlinear wave kinetics for cyclic gain/loss in random fiber lasers. **Abstract only.** Driven optical kinetics is an established subject; neither is a general spatial-modal distribution for an arbitrary Yb amplifier.
- Neighboring prethermal theory: Yang et al., [arXiv:2507.04101](https://arxiv.org/abs/2507.04101), *Unveiling prethermalization and thermal processes through the simplest one-dimensional topological model*: **abstract only**. A photonic lattice example, not a derived GRIN detuning law.

## Sharpest statement of the gap

Generic equilibrium and kinetic-rate questions are substantially solved, and temporal wave kinetics is no longer absent. The retained gap is the finite-pulse, finite-observation-length crossover with realistic walk-off and detection. No controlled universal law for that specified setting was located here. This is lower priority because existing theory may already yield it after a modest adaptation; a new result must outperform that baseline.

Searches (2026-10-01): exact-title and forward-citation trails for the 2019 thermodynamics and 2024 calorimetry papers; `multimode fiber temporal ultraviolet cutoff thermalization`; `spatio-temporal thermalization adiabatic cooling`; `prethermalization multimode fiber detuning`; `generalized Gibbs ensemble photonics`; phase-correlated/Vlasov wave kinetics, weak/strong disorder, and random-fiber-laser gain/loss kinetics. The bounded search did not establish that a detuning-lifetime law is absent from all wave-turbulence or plasma literature.

## Conjectures

None.

## Oracle

Lab-reported multimode GNLSE ensemble propagation covers the passive question; `available` is not a verified evaluator integration. Resolve both mode and frequency cutoffs and compare filtered versus unfiltered observables. A cutoff-dependent fitted temperature is not a numerical convergence test. Preserve phase information to distinguish kinetic relaxation from reversible correlations. No run was performed here.

## Lab test

Joint modal/spectral measurements versus cut-back length, input duration and coherence time, with detector bandwidth varied independently. Look for the predicted cessation of relaxation when pulses separate or broaden, rather than only an output RJ fit.

## Risks and must-reads

The stationary-wave 2026 theory must be the analytical baseline. Strong coherence, solitons or Raman can invalidate random-phase closure. P-010 covers the directly measured pulsed self-cleaning crossover; do not create two claims for the same reduced law. The driven/prethermal subtargets require model selection before derivation.

**See also** (claude-interactive.22, 2026-10-20): [P-20261020-claude-interactive.22-01](P-20261020-claude-interactive.22-01-self-cleaning-threshold-length-law.md), the quasi-CW threshold–length law of Kerr self-cleaning. It argues that in the experimental regime $L_{\rm NL}/L_d\lesssim1$ the kinetic rate is not settled: two published two-length data sets point to $P_c\propto L^{-1}$ against the kinetic $L^{-1/2}$.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-01 | claude-bootstrap (claude) | Created; literature_state partial; priority lowered because kinetic lengths are already derived | arXiv:2505.11299 |
| 2026-10-01 | gpt-a (gpt; model unknown) | candidate → audited; priority 4 → 5; retained partial/low; narrowed to finite-pulse crossover | Joint temporal kinetic theory in arXiv:2506.23536; explicit temporal limitations of 2505.11299; derived weighted statistics and anomalous-correlator dynamics |
