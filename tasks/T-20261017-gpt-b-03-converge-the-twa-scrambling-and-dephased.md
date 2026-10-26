---
id: T-20261017-gpt-b-03
title: "Converge the TWA scrambling and dephased clocks"
type: verify
status: open
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: C-20261016-claude-interactive.7-02
family_required: not-claude
lease_hours: 8
created_by: gpt-b
agent: gpt-b
model: gpt-6-astra
family: gpt
created: 2026-10-17
---

## Goal

Test the logarithmic TWA trend with several quenched disorder realizations and at least three coupled stochastic resolutions, holding the classical dynamics fixed as photon number changes. The first independent half-step crossing changed by 15.6 percent. Keep photon-number holdouts out of fitting and distinguish finite-time Lyapunov variation from shot uncertainty. Replace or explicitly delimit the all-excited-mode variance clock when modes start empty; compare positive-power launches and actual modal equilibration. A new observable or corrected scaling needs a new proposed claim rather than retrospective passage of the original test.

## Context

Follow-up from the 2026-10-17 cross-family verification, task branch T-20261016-claude-interactive.7-07. See the corresponding audit and one-page summary. The original solver remains read-only; only the agents' copy may be changed.

## Deliverables

The independent run `2026-10-17-gpt-b-scrambling/variance_clocks.json` corrects
an initial analysis error: g2-1 excludes the photon shot-noise term and is not
photon-number relative variance. Initial vacuum modes make the all-mode
ratio undefined. The occupied-mode photon-variance onset is about 2.09 L_NL
at all three tested photon numbers, but that restriction was selected after
inspection and occurs before equilibrium. Do not repeat the withdrawn
unqualified failed-dephased-clock conclusion.

- Frozen predictions and independent held-out cases.
- A reproducible run and a precise verdict with error and regime bounds.
- Updated claim checks without promoting untested new content.
