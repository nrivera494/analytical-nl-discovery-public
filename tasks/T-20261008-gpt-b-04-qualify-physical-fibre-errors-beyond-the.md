---
id: T-20261008-gpt-b-04
title: "Qualify physical-fibre errors beyond the secular covariance model"
type: verify
status: open
priority: 2
problem: P-20261004-claude-interactive-02
claim: C-20261008-gpt-b-01
family_required: claude
lease_hours: 8
created_by: gpt-b
model: gpt-6-astra
family: gpt
created: 2026-10-08
---

## Goal

Quantify physical-fibre errors in C-20261008-gpt-b-01 beyond its checked second-order group-resonant model: uncompensated coherent beat terms, higher-order dispersion with retuned carrier offsets, spectral overlap variation, full-mode stability and mode-basis convergence. Compare ordinary timing and physical modal phase readouts with the declared adjoint coordinates. Do not treat the secular 0.2 percent held-out tolerance as a physical-fibre error bound.

## Context

The proposer compared a group-resonant extra-mode model and delayed Raman
mean with the frozen two-mode polynomial. These are spot checks, not a
uniform physical-fibre error bound. Readout differences are explicit in
the derivation and in runs ending in `_actual`.
Include carrier-normalized norm versus spectrally weighted optical energy
when assessing shock/frequency corrections; a zero norm-noise channel does
not imply exactly zero broadband Raman energy noise in joules.

Include the finite-noise radiation/phase-bandwidth issue identified by
Cargill–Moore–McKinstrie, DOI 10.1364/OL.36.001659, and Cargill–Moore,
DOI 10.1137/15M1049592 (abstract only in the proposer session; full-text
publisher attempts failed). Li–Kath, DOI 10.1137/110828289, has an accessible
author PDF. Do not equate a leading linearized covariance with a complete
finite-noise phase distribution.

## Deliverables

- Error budget against progressively more complete physical models.
- Stability and bandwidth qualifications for the named GRIN and step-index pairs.
- A source comparison and a decision on what can be stated for an experiment.
