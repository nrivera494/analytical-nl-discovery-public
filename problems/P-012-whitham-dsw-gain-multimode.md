---
id: P-012
title: "A specified dispersive-shock problem with realistic gain or modal coupling"
status: parked
priority: 5
literature_state: partial
novelty_confidence: low
target_quantity: "Shock-edge trajectories and local oscillation parameters for a selected amplifier or coupled-mode initial-value problem."
model: "Normal-dispersion Kerr propagation with a specified gain model, or a specified coupled-mode system; these are separate regimes."
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

Choose one experimentally preparable pulse/front and predict shock-edge positions and oscillation scales. Specify either spectral gain with saturation or an explicit small set of interacting modes. State a small-dispersion limit, the gain variation relative to the modulation scale, and the modal walk-off/coupling ratios. Combining every gain and multimode effect in one target gives no definite asymptotic problem.

## Signal of hidden simplicity

Optical dispersive shocks have reproducible expanding fronts and envelope structure. Amplifier spectral shocks and polarization-induced shocks are observed or simulated, but they are not automatically instances of the same modulation system.

## Literature state

- El and Hoefer, *Dispersive shock waves and modulation theory*, DOI [10.1016/j.physd.2016.04.006](https://doi.org/10.1016/j.physd.2016.04.006) — **abstract only**, introduction also consulted. Integrable and nonintegrable modulation/edge-fitting methods, including perturbed settings, are established. Whitham averaging itself is not a novelty claim.
- Turitsyn et al., spectral-shock/shallow-water study, DOI [10.1103/PhysRevLett.131.153802](https://doi.org/10.1103/PhysRevLett.131.153802) — **full text**, model and reduction read. Derives a dispersionless dissipative shallow-water description with spectral gain and studies spectral shocks. This is substantial analytical prior work, but not a complete modulation theory of a rapidly oscillating dispersive-shock fan. Its linear-in-frequency gain approximation must be bandwidth-limited physically.
- Nuño et al., *Vectorial dispersive shock waves in optical fibers*, DOI [10.1038/s42005-019-0241-6](https://doi.org/10.1038/s42005-019-0241-6) — **abstract only**, introduction also consulted. An orthogonally polarized pump drives shock fronts on a probe through cross-phase modulation. This closes generic novelty for observing coupled/vectorial shocks, not arbitrary spatial-mode Whitham closure.
- *Theory of dispersive shock waves induced by the Raman effect in optical fibers*, DOI [10.1103/94zy-78my](https://doi.org/10.1103/94zy-78my), arXiv:2507.23406 — **abstract only**. Gives a Raman-perturbed Whitham description and comparison with the generalized NLSE. A generic claim that nonintegrable Raman perturbations preclude such theory is false.

Searches: `Whitham nonlinear Schrodinger gain loss Kamchatnov`, `dispersive shock amplifier spectral gain`, `vectorial dispersive shock optical fibers`, and title/citation leads to Raman-perturbed theory. The seed's author-only Conforti/Trillo reference was not identifiable as one particular paper and is not retained as evidence.

## Sharpest statement of the gap

A specific realistic-gain or spatial-mode closure may remain open. **Parked until one initial-value problem, measurable failure of existing theory, and compatible evaluator configuration are selected.** Related vectorial experiments and shallow-water theory do not close every such target; they do remove the rationale for a broad undifferentiated proposal.

## Conjectures

None.

## Oracle

Scalar propagation is reported available, but realistic gain and the intended coupled-mode diagnostic need specification. Compare shock edges and local wavelengths with the same initial/front conditions, including convergence in temporal resolution and window size.

## Lab test

Prepare a calibrated pump/probe front or amplified chirped pulse and measure its time-frequency structure versus length. Select the mechanism before choosing the observable; a smooth envelope measurement cannot alone test oscillatory modulation theory.

## Risks and must-reads

Read full Raman-Whitham and vectorial papers before choosing a gap. Nonintegrability alone is not a reason that a new formalism is needed. A chosen simple gain model may reduce to existing perturbative Whitham theory.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-01 | claude-bootstrap (claude) | Created as unaudited candidate | Additional-candidates list, literature audit Oct 2026 |
| 2026-10-02 | gpt-a (gpt; model unknown) | Candidate → parked; unaudited → partial | Mature modulation theory, spectral-gain reduction and vectorial/Raman extensions; no selected residual initial-value problem |
