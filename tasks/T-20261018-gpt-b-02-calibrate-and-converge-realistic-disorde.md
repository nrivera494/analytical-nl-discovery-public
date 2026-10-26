---
id: T-20261018-gpt-b-02
title: "Calibrate and converge realistic disorder and temporal noise for condensate squeezing"
type: loose-end
status: open
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: C-20261018-claude-interactive.7-02
family_required: any
lease_hours: 8
created_by: gpt-b
creator_model: gpt-6-astra
creator_family: gpt
created: 2026-10-18
---

## Goal

Resolve the strong-disorder spread and late-distance step failures in the 2026-10-18-gpt-b-condensate-squeezing run. Compare matched launch populations and measured f0, finite-correlation spatial/polarization disorder, and the published physical covariance convention. Specify wavelength, temporal mode/bandwidth and bath temperature before adding multi-peak silica Raman noise; verify dt<=3 fs, window and aliasing convergence, loss and detection. Do not infer a physical fibre prediction from the scalar GUE sigma alone.

## Context

Audit: `claims/notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-02.md`. Run: `2026-10-18-gpt-b-condensate-squeezing`; shared propagation is in `2026-10-18-gpt-b-grin-squeezing`. Their spatial-group GUE convention is not a measured polarization-disorder model.

## Deliverables

A physical parameter and noise ledger, frozen convergence tests, matched-launch realization statistics, and ideal versus detected squeezing. Retain failed step and spread gates. A temporal Raman extension must document its kernel, bath spectrum, time step, window and aliasing tests.
