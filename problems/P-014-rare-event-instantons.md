---
id: P-014
title: "Rare-event rates for a selected fiber-system failure"
status: parked
priority: 5
literature_state: partial
novelty_confidence: low
target_quantity: "A rate function and testable tail probability for one specified failure event under a calibrated input or distributed noise law."
model: "A specified stochastic GNLSE or cavity map with its noise covariance; a large-deviation formulation appropriate to that model."
oracle_ready: partial
last_audited: 2026-10-02
audited_by: [gpt]
proposed_by: claude-bootstrap
updated_by: gpt-a
updated_model: unknown
updated_family: gpt
claims: []
results: []
---

## Target quantity

Select one event, its threshold and observation interval: for example a calibrated output pulse-energy failure or a specified timing excursion. Specify whether randomness enters the initial pulse, the distributed gain/Raman reservoirs, or both. Seek a rate function, its regime of asymptotic validity and a probability estimate. Closed form is optional; a well-conditioned low-dimensional boundary-value problem would be useful.

## Signal of hidden simplicity

Large fluctuations can concentrate around reproducible optimal wave histories. Optical-soliton communication theory and water-wave experiments establish this possibility, but do not show that three unrelated ultrafast failure mechanisms share one instanton family.

## Literature state

- Falkovich, Kolokolov, Lebedev and Turitsyn, *Statistics of soliton-bearing systems with additive noise*, DOI [10.1103/PhysRevE.63.025601](https://doi.org/10.1103/PhysRevE.63.025601) — **abstract only**. Analytical non-Gaussian soliton statistics already exist in an additive-noise fiber-communication setting. Merely applying an optimal-fluctuation method is not a new result.
- Falkovich et al., *Non-Gaussian error probability in optical soliton transmission*, DOI [10.1016/j.physd.2004.01.044](https://doi.org/10.1016/j.physd.2004.01.044) — **abstract only**, introductory full-text passages also consulted. Extends the communication-system error-probability treatment; its observable and noise assumptions must be compared with any proposed ultrafast application.
- Dematteis, Grafke, Onorato and Vanden-Eijnden, *Experimental Evidence of Hydrodynamic Instantons: The Universal Route to Rogue Waves*, [arXiv:1907.01320](https://arxiv.org/abs/1907.01320) — **abstract only**. Water-tank experiments support numerically determined action-minimizing wave histories. This is a useful neighboring-field method and experimental test, not a closed solution for a noisy fiber amplifier or cavity.

Searches: `Falkovich Kolokolov Lebedev Turitsyn soliton noise instanton`, `non Gaussian error probability optical soliton transmission`, `supercontinuum large deviation instanton`, `hydrodynamic instantons rogue waves`, and forward title leads to the 2004 and 2019 studies. No event-specific closed law for the seed's unspecified ultrafast applications was located; that does not establish novelty for any one of them.

## Sharpest statement of the gap

**Parked because an event and noise model have not been selected.** The original card named a method and several applications rather than one scientific question. Existing communication and water-wave results do not close a properly specified ultrafast target. Reactivation requires a robust measured/simulated tail, a chosen event functional, and a noise law that can be independently calibrated.

## Conjectures

None.

## Oracle

Downgraded to partial. Adjoint capability supplies sensitivities for an optimization; it does not directly solve the instanton boundary-value problem or certify a probability. Rare-event sampling, constrained optimization, multiple-minimizer checks and comparison with direct ensembles remain to be specified. No optimizer or simulation was implemented here.

## Lab test

Collect repeated single-shot measurements of the selected failure event and its precursor waveform. Compare the predicted tail and conditional precursor away from the parameters used to calibrate noise. A best-fit extreme waveform without a probability test is insufficient.

## Risks and must-reads

Input-noise and distributed-noise actions differ. A local optimum need not dominate the tail; prefactors and competing routes may matter at accessible probabilities. Read the two communication papers in full after choosing the physical application.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-01 | claude-bootstrap (claude) | Created as unaudited candidate | Additional-candidates list, literature audit Oct 2026 |
| 2026-10-02 | gpt-a (gpt; model unknown) | Candidate → parked; priority 4 → 5; unaudited → partial; oracle → partial | Existing non-Gaussian soliton theory; no selected event/noise law; corrected the assertion that an adjoint automatically computes instantons |
