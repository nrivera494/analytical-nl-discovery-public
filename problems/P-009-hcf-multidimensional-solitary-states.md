---
id: P-009
title: "Reduced dynamics of Raman-driven states in gas-filled hollow-core fiber"
status: parked
priority: 5
literature_state: partial
novelty_confidence: low
target_quantity: "A selected observable, such as redshift or compressible duration, for a specified multimode molecular-gas solitary-state experiment."
model: "Multimode unidirectional propagation with gas dispersion, electronic Kerr and rotational/vibrational Raman response; ionization only where required by the regime."
oracle_ready: missing
last_audited: 2026-10-02
audited_by: [gpt]
proposed_by: claude-bootstrap
updated_model: unknown
updated_by: gpt-a
updated_family: gpt
claims: []
results: []
---

## Target quantity

Select one measured law for the Safaei-type regime: redshift versus distance/pressure, duration after compression, or spatial modal composition. Specify the gas, launch and propagation geometry before selecting a reduced ansatz. The former wording mixed Kerr, Raman and ionization without identifying which are essential. A validity domain should separate pulse duration/Raman period, Raman dephasing, modal walk-off and ionized fraction.

## Signal of hidden simplicity

High-energy multidimensional solitary states and a Raman red-shift compression scheme are experimentally reported. These provide a physical target, but not evidence for a universal fixed shape or a single common asymptotic regime.

## Literature state

- Safaei et al., *High-energy multidimensional solitary states in hollow-core fibres*, DOI [10.1038/s41566-020-00699-2](https://doi.org/10.1038/s41566-020-00699-2) — **abstract only**. Confirms the experimental phenomenon; the detailed balance of mechanisms still requires the full experimental/model comparison.
- Légaré et al., *Raman Red-Shift Compressor: A Simple Approach for Scaling the High Harmonic Generation Cut-Off*, DOI [10.1002/adpr.202100113](https://doi.org/10.1002/adpr.202100113) — **abstract only**, indexed explanatory passages also consulted. Intermodal nonlinear conversion and Raman-driven redshift/compression already have a physical interpretation. Do not label the entire effect unexplained.
- Chen and Wise, *Unified and vector theory of Raman scattering in gas-filled hollow-core fiber across temporal regimes*, DOI [10.1063/5.0189749](https://doi.org/10.1063/5.0189749) — **abstract only**. Derives a Raman framework spanning temporal regimes, including vector effects, transient gain and phonon-mediated pulse interactions, with numerical comparisons. This closes a generic request for a governing Raman theory, not a reduced law for the particular multimode solitary state.

Searches: exact Safaei title, `hollow core multidimensional solitary states Raman analytical scaling`, `Raman red shift compressor theory`, and `unified vector Raman hollow core temporal regimes`. Followed the later compressor and unified-theory leads. No universal reduced law for the selected experiment was established by these abstracts; absence is not proved.

## Sharpest statement of the gap

**Parked pending a full-text model audit and selection of one observable.** The empirical regime is real and related analytical Raman theory exists; the missing step is a justified reduction for that regime. This is not a demotion. Plasma dynamics must not be required automatically if an experimentally useful low-ionization regime suffices.

## Conjectures

None.

## Oracle

The repository has no connected gas-response/hollow-core evaluator. The first requirement is a capability comparison against the established model, with the exact dispersion, Raman response and boundary conditions; add ionization only when justified.

## Lab test

Pressure and length scans with modal imaging, spectral measurements and pulse characterization after a fixed compressor. These can distinguish redshift scaling from an apparent improvement produced only by changing external dispersion compensation.

## Risks and must-reads

Read the Safaei and Légaré full texts and compare their regimes with Chen–Wise before reopening. Strong launch dependence or multiple competing Raman transitions may preclude a universal profile. A fitted redshift alone would be weak evidence.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-01 | claude-bootstrap (claude) | Created as unaudited candidate | Additional-candidates list, literature audit Oct 2026 |
| 2026-10-02 | gpt-a (gpt; model unknown) | Candidate → parked; unaudited → partial | Real experiments and substantial Raman theory located; particular reduced observable and gas evaluator still unspecified |
