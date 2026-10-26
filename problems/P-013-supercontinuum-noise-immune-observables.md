---
id: P-013
title: "Useful noise-rejecting measurements of a specified supercontinuum"
status: parked
priority: 4
literature_state: partial
novelty_confidence: low
target_quantity: "A calibrated finite-bandwidth observable that retains sensitivity to a chosen signal while rejecting specified source-noise channels."
model: "Stochastic scalar GNLSE with measured input covariance, Raman and higher-order dispersion, followed by a specified detector."
oracle_ready: available
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

Choose a useful signal to estimate, require a fixed nonzero response to it, and constrain detector bandwidth, accessible spectral weights and measurement noise. Then seek residual noise or a sensitivity bound for that observable. Without those constraints a constant observable, arbitrary rescaling or a conserved total quantity makes “noise immunity” trivial. A soliton-fission timing-gain law is a separate, potentially valid target requiring a defined pulse branch and timing estimator.

## Signal of hidden simplicity

Experiments resolve correlations between spectral bands, and correlated-reference normalization reduces supercontinuum intensity noise in imaging. The untraced numerical anecdote about input energy noise in the seed card has been removed; it had no run id and is not evidence.

## Literature state

- Dudley, Genty and Coen, *Supercontinuum generation in photonic crystal fiber*, DOI [10.1103/RevModPhys.78.1135](https://doi.org/10.1103/RevModPhys.78.1135) — **abstract only**. Established supercontinuum/coherence theory and modeling; the review must not be reduced to a claim that only numerical rules of thumb exist.
- Corwin et al., *Fundamental Noise Limitations to Supercontinuum Generation in Microstructure Fiber*, DOI [10.1103/PhysRevLett.90.113904](https://doi.org/10.1103/PhysRevLett.90.113904) — **abstract only**. Quantum input and spontaneous Raman fluctuations are studied with experiment and stochastic propagation. Noise rejection of one technical channel does not remove these reservoirs.
- Wetzel et al., *Real-time full bandwidth measurement of spectral noise in supercontinuum generation*, DOI [10.1038/srep00882](https://doi.org/10.1038/srep00882), arXiv:1211.6757 — **full text**, noise/correlation results read. Measures wavelength-dependent moments and spectral correlations; these do not imply a globally noise-free observable at arbitrary distance.
- Niemeier, Simmons and Rogers, *Noise reduction in supercontinuum sources for OCT by single-pulse spectral normalization*, DOI [10.1364/AO.393141](https://doi.org/10.1364/AO.393141) — **full text**, normalization and noise discussion read. Demonstrates an application-specific correlated-reference measurement. The reference contributes its own uncorrelated noise; classical normalization is not quantum squeezing.

Searches: `supercontinuum noise immune observable adjoint`, `supercontinuum spectral correlations noise cancellation`, `supercontinuum energy timing jitter sweet spot`, and forward leads from the noise measurements to OCT normalization. No universal immunity theorem was located, but such a theorem is not a well-posed target as written.

## Sharpest statement of the gap

**Parked for measurement and signal selection.** The generic unconstrained criterion is ill-posed, and correlated-reference cancellation is established. A useful residual question is a noise floor or a parameter-dependent jitter law for a specified source/detector, with independent distributed noise included. An adjoint sensitivity calculation alone is a general method, not a new physical result.

## Conjectures

None.

## Oracle

Propagation, adjoints and Langevin capability are reported available. Define the input/distributed noise channels and detector before evaluation. Use out-of-sample parameter regions and compare first-order sensitivity with finite-noise ensembles; no such runs were made in this audit.

## Lab test

Simultaneously acquire the proposed signal and reference on single shots, calibrate their response to a known perturbation, and compare residual noise against ordinary normalization at equal detection resources.

## Risks and must-reads

Fission can switch which pulse a timing estimator labels; a smooth local derivative may then miss the dominant error. Detector shot noise and the useful-signal response can eliminate an apparent source-noise advantage. Full-text review of the chosen regime is a reactivation requirement.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-01 | claude-bootstrap (claude) | Created as unaudited candidate | Additional-candidates list, literature audit Oct 2026 |
| 2026-10-02 | gpt-a (gpt; model unknown) | Candidate → parked; priority 3 → 4; unaudited → partial | Unconstrained immunity is not operational; spectral correlation and useful normalization already measured; removed unsupported simulation number |
