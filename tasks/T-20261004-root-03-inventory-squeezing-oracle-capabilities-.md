---
id: T-20261004-root-03
title: "Inventory squeezing oracle capabilities and provenance"
type: loose-end
status: open
priority: 3
problem: null
claim: null
family_required: any
lease_hours: 8
created_by: /root
created: 2026-10-04
agent: /root
model: unknown
family: gpt
---

## Goal

Document which existing solvers and saved runs can test the new multimode squeezing candidates, including missing vector, asymmetric-mode, acoustic, and readout capabilities; propose any implementation separately for PI agreement.

## Context

The active candidates are P-20261004-root-01, P-20261004-root-03, P-20261004-claude-interactive-01 and P-20261004-claude-interactive-02. All use `oracle_ready: partial`. root-02 and root-04 are parked. The two new cards add requirements: non-axisymmetric modes (LP11), distributed gain with spontaneous-emission noise, and overlap tensors computed from the measured GIF625 index profile. See `docs/multimode-squeezing-scope.md` for original archive paths and distinctions between experimental fitting, surrogate theory, and proposed physical readouts. The archive is outside this repository and was not imported. This checkout's evaluator is a contract; do not confuse a planned interface with an available capability.

## Deliverables

- A read-only capability matrix for scalar, radial and non-axisymmetric spatial modes, degenerate orientations, vector polarization, matched Raman tensor noise, low-frequency acoustic noise, distributed loss/random coupling, finite-reference readout, and RF versus pulse-count observables.
- Identify existing configs, seeds, solver commits, and stored outputs that could support registered runs. Do not copy raw data into git or retroactively treat campaign reports as independently verified claims.
- Identify convergence controls and an independent/relaxed-assumption solver for each proposed test; document missing capabilities and a bounded implementation plan for PI agreement.
- List required experimental constraints such as pulse phase, input calibration, modal/polarization launch, and collection geometry. No new fit or simulation is requested by this inventory.
