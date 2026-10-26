---
id: T-20261012-gpt-a-08
title: "Bound Raman optimization and thermal-slice limits"
type: derive
status: open
priority: 3
problem: P-20261010-claude-interactive-01
claim: null
family_required: any
lease_hours: 8
created_by: gpt-a
created: 2026-10-12
agent: gpt-a
model: gpt-6-astra
family: gpt
---

## Goal

Replace the empirical normal-dispersion Raman interpolation with conditional variational bounds for a specified bath covariance. Determine whether a gap or coercivity hypothesis supports a first-order coefficient, including optimizing-mode changes and deterministic delayed response. Establish a quantitative joint low-frequency and temporal-localization regime for a finite pulse approaching the thermal slice; do not restore the audited finite-band tolerance.

## Context

Created by the feasibility assessment in task T-20261012-gpt-a-01 for the PI.
See `docs/lean/2026-10-12-gpt-a-filtered-fano-formalization-assessment.md` for
precise assumptions, source references, and the boundary between model hypotheses
and mathematical conclusions. No Lean installation was authorized in that session.

## Deliverables

- A precise statement with its model assumptions and formalization level.
- A proof or an explicit account of the remaining mathematical obstruction;
  any Lean code must be checked in a PI-authorized, pinned environment.
- An honest evidence log, with no promotion or claim-status change inferred from
  the assessment alone.
