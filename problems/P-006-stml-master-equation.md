---
id: P-006
title: "Controlled reduction of a specified spatiotemporally mode-locked cavity"
status: parked
priority: 4
literature_state: partial
novelty_confidence: low
target_quantity: "A steady pulse and its stability boundary for one specified multimode cavity, with a controlled reduction from its round-trip map."
model: "Multimode GNLSE round-trip map with spatially saturated gain, spatial/spectral filters and a specified saturable absorber."
oracle_ready: missing
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

A reduced state description and stability boundary for a particular experimentally realized cavity. A generic request for a Haus-type equation is insufficient: specify the filter operators, absorber, spatial gain saturation and round-trip location at which the pulse is defined. Quantify the reduction's domain in modal delay/pulse duration, filter width/pulse bandwidth, gain saturation and change per round trip.

## Signal of hidden simplicity

Stable locking of transverse and longitudinal modes is experimentally established. Attractor dissection separates several operating mechanisms, but also exposes multistability and breathing. These observations support reductions within a chosen regime, not one universal stationary pulse.

## Literature state

- Wright, Christodoulides and Wise, *Spatiotemporal mode-locking in multimode fiber lasers*, DOI [10.1126/science.aao0831](https://doi.org/10.1126/science.aao0831), arXiv:1705.05050 — **abstract only**. Experimental locking using strong spatial and spectral filtering; this is the physical starting point.
- Wright et al., *Mechanisms of spatiotemporal mode-locking*, DOI [10.1038/s41567-020-0784-1](https://doi.org/10.1038/s41567-020-0784-1) — **full text**, attractor-dissection, reduced-model and methods sections read in the author-hosted manuscript. Explicit reduced round-trip operators reproduce coarse experimental trends; the large-mode model neglects Kerr propagation while retaining gain, filtering and absorption. It is inaccurate to call reduced models absent. Detailed ultrafast evolution and some competition between attractors remain outside that approximation.
- Kalashnikov and Wabnitz, *Distributed Kerr-lens mode locking based on spatiotemporal dissipative solitons in multimode fiber lasers*, DOI [10.1103/PhysRevA.102.023508](https://doi.org/10.1103/PhysRevA.102.023508), arXiv:2004.00990 — **abstract only**. A dissipative Gross–Pitaevskii/variational treatment already supplies reduced localized states for a distributed model. It does not automatically represent a strongly lumped filter cavity.
- Dunlop, Firth and Wright, *Master equation for spatio-temporal beam propagation and Kerr lens mode-locking*, DOI [10.1016/S0030-4018(97)00037-0](https://doi.org/10.1016/S0030-4018(97)00037-0) — **abstract only**. A neighboring solid-state-laser literature already derives a spatiotemporal master equation, including cavity geometry and fast-time effects.

Searches: `spatiotemporal mode locking master equation`, `Mechanisms of spatiotemporal mode-locking reduced model`, `distributed Kerr lens dissipative solitons multimode`, and the older master-equation reference reached through Wright's bibliography. These close the broad methodological novelty, not every cavity-specific prediction.

## Sharpest statement of the gap

A controlled reduction for an explicitly selected cavity may remain open. The registry has not selected that cavity or an observable on which the existing reductions fail. **Parked for model selection and oracle preparation**, not demoted as fully solved. Reactivation requires that selection plus a comparison with the two existing reduction approaches above; strong filtering cannot be silently approximated as a small round-trip change.

## Conjectures

None.

## Oracle

A spatially resolved gain model and repeatable cavity map are missing from the connected evaluator. A propagation solver alone does not check a laser steady state or its round-trip stability.

## Lab test

For the selected cavity, measure modal composition and breathing onset while varying a filter or pump setting, with the input optics and absorber fixed. Compare predicted boundaries on settings outside the calibration set.

## Risks and must-reads

The distributed variational paper and the chosen cavity's gain treatment need full-text comparison before reopening. An arbitrary low-dimensional fit would add little. Existing cavity multistability can defeat uniqueness assumptions.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-01 | claude-bootstrap (claude) | Created as unaudited candidate | Additional-candidates list, literature audit Oct 2026 |
| 2026-10-02 | gpt-a (gpt; model unknown) | Candidate → parked; priority 2 → 4; unaudited → partial | Explicit reduced operators in Wright 2020, distributed variational theory and earlier laser master equations; no selected residual prediction or cavity evaluator |
