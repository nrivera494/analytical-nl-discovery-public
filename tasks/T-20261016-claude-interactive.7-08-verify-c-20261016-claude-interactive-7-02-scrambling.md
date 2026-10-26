---
id: T-20261016-claude-interactive.7-08
title: "Verify C-20261016-claude-interactive.7-02 (scrambling length of coherent vs dephased input) with the stochastic multimode solver"
type: verify
status: done
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: C-20261016-claude-interactive.7-02
family_required: not-claude
lease_hours: 8
created_by: claude-interactive.7
created: 2026-10-16
completed: 2026-10-17
completed_by: gpt-b
completion_model: gpt-6-astra
completion_family: gpt
---

## Goal

An independent check of claim predictions 1-4 in a fibre model:
- GRIN overlaps, 4-6 groups, weak intra-group disorder, CW single cell (dispersionless);
- truncated-Wigner ensembles at photons per cell from 1e4 to 1e10;
- the classical Lyapunov exponent from the tangent map;
- the Hartree-Fock ballistic coefficient A.

Report:
- the measured slope of z_E against ln n, compared with 1/(2 lambda_1);
- the sqrt(n) prefactor on the ballistic branch;
- the n-independence of the dephased route.

Relax at least one assumption, e.g. add dispersion and walk-off so that neighbouring cells couple.

## Context

Claim file; toy evidence in run 2026-10-16-claude-interactive.7-rj-toy-twa-scrambling. Respect the TWA validity criterion E' >> E'_vac (claim regime).

## Deliverables

- A run folder.
- The claim's checks table updated.

## Completion

Completed the authorized partial verification in run
`2026-10-17-gpt-b-scrambling`. C-20261016-claude-interactive.7-02 is refuted as
written by the pure-Gaussian-lifetime assertion in its own exact Kerr limit.
The exact ballistic collapse and frozen photon-number holdouts pass; the GRIN
TWA logarithmic trend has partial support but a stochastic convergence blocker.
The corrected occupied-mode dephased photon-variance clock supports
n-independence; the all-mode clock is inconclusive on initial vacuum modes.
The physical multimode Hartree–Fock coefficient, exact chaotic quantum law,
walk-off and coupled cells remain untested, explicitly transferred to
T-20261017-gpt-b-03 and -04 (physical-fibre effects also -01).
See the claim's linked audit and PI summary. This task's completion does not
certify its untested original subgoals.
