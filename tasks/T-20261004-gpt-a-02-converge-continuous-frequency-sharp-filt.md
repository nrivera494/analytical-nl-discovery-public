---
id: T-20261004-gpt-a-02
title: "Converge continuous-frequency sharp-filter noise readouts"
type: loose-end
status: open
priority: 3
problem: P-20261004-claude-interactive-01
claim: null
family_required: any
lease_hours: 8
created_by: gpt-a
agent: gpt-a
model: gpt-6-astra
family: gpt
created: 2026-10-04
---

## Goal

Resolve the continuous-frequency limits of the fixed band and edge Fano readouts in T-20261004-claude-interactive-02. Propagation step and temporal resolution are controlled, but a binary spectral mask samples its discontinuity differently when the time window changes. Compare successively larger windows or a documented endpoint/cell quadrature with the matching filter-vacuum term, preserve the original frozen readout results, and establish approximately 0.1 percent accuracy in each Fano factor and an absolute 0.001 accuracy in rho for the two Raman responses and Kerr control.

## Context

Use `2026-10-04-gpt-a-noise` and `2026-10-04-gpt-a-noise-convergence`. Their covariance controls preserve total counts. This follow-up addresses numerical integration of fixed sharp filters; it does not authorize filter optimization.

## Deliverables

Registered convergence runs, a readout-convention explanation including rejected-port vacuum for fractional transmission, and updated numerical uncertainty intervals.
