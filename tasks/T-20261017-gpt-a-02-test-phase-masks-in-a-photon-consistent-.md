---
id: T-20261017-gpt-a-02
title: "Test phase masks in a photon-consistent broadband SMF-28 model"
type: loose-end
status: open
priority: 3
problem: P-20261016-claude-interactive-03
claim: C-20261016-claude-a-04
family_required: any
lease_hours: 8
created_by: gpt-a
agent: gpt-a
model: gpt-6-astra
family: gpt
created: 2026-10-17
---

## Goal

Test the independently selected phase masks using a sourced broadband SMF-28
model with dispersion, effective mode area, frequency-dependent nonlinearity,
and wavelength-dependent attenuation over the actual output spectrum. Use a
nonlinear formulation with the appropriate photon invariant, and compare both
energy and red shift against paired transform-limited launches.

## Context

Run `2026-10-17-gpt-a-phase-headroom` uses a published dispersion Taylor curve
from arXiv:2301.02945 (full text) and a representative zero-dispersion-slope
curve. These are controlled material-model attacks, not measured broadband
data for a fibre sample. Its optional polynomial-gamma output multiplier does
not exactly conserve physical photon number and is explicitly excluded from
the validated photon-model interpretation. The manufacturer datasheet's
attenuation range does not certify constant loss across arbitrary red shifts.

## Deliverables

Source/access records and a declared wavelength validity interval; an invariant
and numerical-convergence check; fixed-energy phase-only comparisons using
gated soliton energy, local ZS diagnostics where justified, and red shift.
Freeze held-out cases before evaluating the masks, and report which measured
material assumptions limit a laboratory prediction. Do not retune masks on
held-out robustness results.
