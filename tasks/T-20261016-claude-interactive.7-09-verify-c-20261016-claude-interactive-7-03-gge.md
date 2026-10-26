---
id: T-20261016-claude-interactive.7-09
title: "Verify C-20261016-claude-interactive.7-03 (generalized Gibbs endpoint with the resonant Kerr energy; input-phase memory) in a GRIN fibre model"
type: verify
status: done
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: C-20261016-claude-interactive.7-03
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

An independent check of claim prediction 2: GRIN fibre with real overlaps, 4-6 groups, no disorder, the same mode powers launched with random and with aligned phases.
- Does the long-z condensate fraction differ by the amount the GGE shell predicts?
- Does RJ fail for both launches?
- Do both relax to RJ once weak intra-group disorder is added?

Ideal GRIN conserves L_z, and has exact Kohn and breathing modes. Either include them in the shell, or break them with a weak perturbation of the index profile, and say which was done.

Also check the toy-scale statement that the effect does not shrink as L_beat/L_NL -> 0.

## Context

Claim file; toy evidence in run 2026-10-16-claude-interactive.7-rj-toy-gge. Literature to check first: Podivilov et al., PRL 122, 103902 (2019) (resonant GRIN model).

Note: the solver has no linear mode coupling. Emulate intra-group disorder with segmented propagation and random block unitaries, or use T-20261016-claude-interactive.7-11.

## Deliverables

- A run folder.
- The claim's checks table updated.

## Completion

Cross-family verification completed in run `2026-10-17-gpt-b-gge` with a
negative endpoint-verification verdict. N/E/H/L invariants and phase memory
are reproduced; independently frozen conditioned-shell predictions improve
several comparisons, including held-out geometry. Selected extensions to
1200000 nonlinear lengths, narrower shell samplers and exact reflection-sector
runs still fail endpoint or precision gates. C-20261016-claude-interactive.7-03
therefore remains cheap-checks-passed, with its conditional stationary-measure
theorem distinguished from an unverified mixing assertion.

The disorder scan finds sufficient tested windows for ±0.02 equivalence of
mean condensate fractions, including the sigma=3 extension at both step sizes.
It does not prove zero residual memory or a universal relaxation length.
Short full/resonant comparisons test the weak-nonlinearity scaling, not its
validity uniformly over the long endpoint windows. Those remaining questions
are recorded in T-20261017-gpt-b-01 and -02; the quantum extension is in -04.
See the claim's linked audit and PI summary. Original failed runs are retained.
