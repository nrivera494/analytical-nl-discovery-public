---
id: P-20261004-root-04
title: "Spatial, frequency, and polarization squeezing structure and intensity readout"
status: parked
priority: 2
literature_state: unaudited
novelty_confidence: low
target_quantity: "Derived criteria, bounds, and scaling laws connecting multimode covariance structure to intensity squeezing accessible through physical filters, collection, polarization optics, or finite-reference interference."
model: "Quantum fluctuation kernels of regime-specific vector multimode propagation, followed by passive linear optical channels and coherent-reference mixing with complete vacuum and phonon covariance."
oracle_ready: partial
last_audited: null
audited_by: []
proposed_by: /root
provenance:
  agent: /root
  model: unknown
  family: gpt
updated_by: claude-interactive
updated_model: claude-opus-5-5
updated_family: claude
claims: []
results: []
---

## Target quantity

Develop a theory of which multimode squeezing is accessible to a specified intensity measurement, and why filtering or interferometry can expose or lose it. Predict the relevant spatial/frequency/polarization correlation pattern, its observable projection, and a scaling or bound for the achievable Fano factor at finite transmitted power and finite reference resources.

This is independent of finding a universal propagation law. It may take a controlled kernel from any one of the three dispersion-specific problems and solve a restricted readout question. Apply the [shared analytical criteria and definitions](../docs/multimode-squeezing-scope.md). Merely diagonalizing a large numerically supplied covariance or optimizing it numerically is a diagnostic, not the requested analytical result.

Independent subtargets include:

1. Derived symmetry sectors or a small correlation kernel: when do correlations between spatial modes, spectral bands, or polarizations improve joint counting, and when does discarding one sector remove squeezing?
2. Passive masks and apertures: bounds or constructive filter laws at a declared output-power constraint, including non-diagonal spatial collection and readout vacuum.
3. Finite coherent references: required power, phase, delay, spectral shaping, and spatial/polarization overlap to access a predicted squeezed direction, including the combiner's vacuum floor.
4. Phonon and disorder limits: identify correlated reservoir directions, possible cancellation in a specified observable, and bounds on any residual floor. Treat coherent-input vacuum, shared phonon noise, and classical phase/mode disorder separately.

## Signal of hidden simplicity

The archived studies distinguish propagation-generated covariance from readout alignment, and report that joint modal counts can differ qualitatively from separately collected counts. Their physical reference recipes and failed passive-mask interpretations motivate resource-constrained theory. Neither the smallest covariance eigenvalue nor accurate mean power specifies the noise of a realizable selected beam.

## Literature state

All entries were located and read at **abstract only** level. No complete literature audit or novelty claim is made.

- Opatrný, Korolkova and Leuchs, [arXiv:quant-ph/0204131](https://arxiv.org/abs/quant-ph/0204131), DOI 10.1103/PhysRevA.66.053813. Nonmonochromatic mode descriptions and correlation/homodyne characterization are established prior art.
- Corney et al., [arXiv:quant-ph/0603280](https://arxiv.org/abs/quant-ph/0603280), DOI 10.1103/PhysRevLett.97.023606. Quantum dynamics and experiments for polarization squeezing in birefringent fiber.
- Dong et al., [arXiv:0709.2280](https://arxiv.org/abs/0709.2280), DOI 10.1364/OL.33.000116. Experimental and numerical evidence for Raman limitations in pulsed polarization squeezing.
- Tomaru, DOI [10.1016/j.optcom.2006.12.030](https://doi.org/10.1016/j.optcom.2006.12.030). Interferometric squeezing across dispersion signs; publisher abstract read via search record, direct access blocked.
- Drummond and Corney, [arXiv:quant-ph/9912095](https://arxiv.org/abs/quant-ph/9912095). Matched quantum reservoirs provide the starting constraint on phonon-noise reductions.

## Sharpest statement of the gap

**Superseded 2026-10-10.** The PI made [P-20261010-claude-interactive-01](P-20261010-claude-interactive-01-fast-lower-bounds-filtered-fano.md) (fast, tight lower bounds on filtered Fano factors) take precedence over this card. Its readout hierarchy covers the covariance-to-accessible-squeezing question, and its rung 5 carries the subtargets below. This card stays parked as the record.

**Parked 2026-10-04.** The PI narrowed the multimode-squeezing set to four problems on 2026-10-04. The readout definitions now live in `docs/multimode-squeezing-scope.md` and in P-20261004-root-01 and P-20261004-root-03. If reactivated, the sharpest version is one variational question: the minimum F over spectral masks with transmission between 0 and 1 at fixed transmitted power, and when a single edge filter is optimal. The archive motivates it: an 8.8 dB covariance bound against F = 1.07 for the best single window on the same state, and two-window masks gaining about 1 dB (`research_runs/2026-09-26_analytics/report.md`).

The useful target is a derived, physically constrained relation between a regime's correlation structure and a measurable selected count, with finite power and an explicit validity range. General covariance methods and interferometric squeezing are already established. The open portion could be a particular spatial/polarization selection rule, modal-count scaling, realizability bound, or phonon-limited optimum; full-text review must decide which.

[P-013](P-013-supercontinuum-noise-immune-observables.md) overlaps in its search for robust observables. This card specifically separates quantum intensity squeezing from immunity to classical input jitter and includes vacuum and reference-resource accounting. Results can be shared without claiming that classical noise rejection creates quantum squeezing.

## Regime and scaling targets

Declare whether the mean is bright enough for linearized photon-count noise, whether a Gaussian approximation is used, and which omitted orders could matter. Predict how the readout depends on $M_{\rm occ}$, correlation bandwidth, mode overlap, filter width/edge, aperture geometry, polarization mixing, and $P_{\rm ref}/P_{\rm sig}$. Map any length, power, or wavelength dependence through a specified propagation regime; do not conceal unknown dynamics in fitted covariance entries.

Treat deterministic mode mixing, ensemble-averaged random coupling, and shot-to-shot drift as distinct physical cases. Include polarization-resolved versus polarization-insensitive collection. Explain when cross-mode or cross-polarization Raman correlations matter; assess low-frequency acoustic noise separately if needed for the detector band. All comparisons must include the same physical losses and readout resource constraints.

## Conjectures

None registered. A positive-semidefinite covariance or favorable eigenvalue is a consistency check or bound, not a new physical filter design.

## Oracle

Saved scalar/radial covariance and readout calculations are partial comparison material. General vector covariance, non-axisymmetric apertures, acoustic reservoirs, and RF/count correspondence must be inventoried in T-20261004-root-03; no current availability is assumed.

Cheap tests include a coherent state through the entire optical network ($F=1$), independent vacuum at every input port, zero/blocked reference limits, photon accounting, and invariance under a simultaneous basis change of field and readout. Check uniform passive attenuation against $F_{\rm after}=1-\eta+\eta F_{\rm before}$ in its applicable channel, rather than applying that scalar rule to an unmodeled mode-selective aperture.

Freeze a physically implementable filter/combiner setting, including minimum selected power and total source budget, before testing another launch, power, or length. Compare power and Fano curves, covariance components, and physically collected mode profiles. Converge the full noise observable over empty as well as occupied spatial/polarization sectors. A relaxed-assumption test can add mismatch, birefringence, or an uncollected mode without refitting the readout at each point.

## Lab test

Measure a small predicted covariance block by splitting selected spectral bands and spatial/polarization channels; then compare separate and joint counts. At fixed fiber conditions, scan filter edge, aperture position, polarization projection, or coherent-reference phase. Measure power simultaneously. Distinguish a quadrature/Stokes measurement from direct photon counting and state the RF band. These tests can establish a restricted selection rule without reconstructing the entire quantum field.

## Risks and must-reads

Known Gaussian-optics optimization may already solve the abstract readout problem; novelty must come from a derived physical kernel, accessible constraint, or scaling. Signed weights, free local oscillators, negligible selected power, or omitted combiner vacuum can create misleading optima. Scalar Raman alternatives cannot substitute for polarization dynamics. An experimental power-axis or collection calibration error cannot be repaired by declaring a new quantum noise term.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-04 | /root (gpt) | Created as priority-2 candidate; literature unaudited | PI request; mode-structure/polarization/Raman abstract intake; independent review T-20261004-root-02 |
| 2026-10-04 | claude-interactive (claude; claude-opus-5-5), on PI instruction | candidate → parked | PI's four-problem set in chat, 2026-10-04; reason and reactivation question under the gap statement |
| 2026-10-10 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Superseded by P-20261010-claude-interactive-01; stays parked | PI message in chat, 2026-10-10 |
