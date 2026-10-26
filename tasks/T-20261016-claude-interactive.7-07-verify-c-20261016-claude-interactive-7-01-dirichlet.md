---
id: T-20261016-claude-interactive.7-07
title: "Verify C-20261016-claude-interactive.7-01 (condensed-RJ Dirichlet statistics, g2 = 2 - 2/M) in a fibre model"
type: verify
status: done
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: C-20261016-claude-interactive.7-01
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

An independent simulation check, by a non-Claude family, of the claim's predictions 3 and 4. Use a GRIN fibre with real overlaps, K = 6 groups (M = 21, one polarization) and weak intra-group disorder. Run an ensemble of at least 200 random input-phase draws at fixed (N, E') with E' <= kappa N.

Compare against the claim:
- g2 in each excited mode;
- the cross g2;
- Var(I_0) from the finite-K sums;
- the sign change of Cov(I_0, I_m);
- the failure without disorder.

Relax at least one assumption, for example the Kerr energy in the shell or two polarizations. Measure how the error shrinks with L_beat/L_NL.

## Context

The claim file, and the toy-model evidence in run 2026-10-16-claude-interactive.7-rj-toy-thermalization. Do not read the exploration note's derivation before the verification report is committed (AGENTS.md hard rule 2 applies to audits; it is good practice here too).

Note: the solver has no linear mode coupling. Emulate intra-group disorder with segmented propagation and random block unitaries, or use T-20261016-claude-interactive.7-11.

## Deliverables

- A run folder.
- The claim's checks table updated.

## Completion

Cross-family verification completed in run `2026-10-17-gpt-b-dirichlet`.
C-20261016-claude-interactive.7-01 is sim-verified only for the narrowed scalar
classical measure and tested low-order moments. The initial 200-phase test
fails three modal checks and is retained; its 800-phase enlargement and a
fresh frozen 400-phase energy holdout pass. Full-tensor short-length averaging,
stronger disorder, noncondensed energy and ground degeneracy test the limits.
The quantum/vector/full-fibre extensions are not certified and remain in
T-20261017-gpt-b-01 and -04. See the claim's linked audit and PI summary.
