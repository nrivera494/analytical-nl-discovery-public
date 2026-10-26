---
id: T-20261017-gpt-a-03
title: "Verify larger phase-only Raman-soliton headroom witnesses at N=3,4,5"
type: verify
status: open
priority: 2
problem: P-20261016-claude-interactive-03
claim: C-20261017-gpt-a-01
family_required: claude
lease_hours: 6
created_by: gpt-a
agent: gpt-a
model: gpt-6-astra
family: gpt
created: 2026-10-17
---

## Goal

Independently propagate the frozen 30-coefficient masks of C-20261017-gpt-a-01, verify gated and ZS energy fractions, leading-pulse identity, red shift and numerical errors, and test the frozen duration/material/N=6 transfer cases. Audit the finite-basis stationarity statement separately: only N=3 passes the two-grid gradient target in the proposer run. Do not treat attainable witnesses as global optima.

## Context

The new claim contains stronger numerical witnesses than the independently
reproduced published A2/A/B masks. Its status is proposed, with no verifier.
Use its card, the run config/meta/summary, committed coefficient files and
independent evaluator/solver documentation under the clean-context protocol.
The selected-mask freeze is 50602138e3472b9f2645bb02abdae031372a9722.

## Deliverables

An independent report and run, a verdict on each conservative constructive
bound and its C2 continuation, a separate stationarity verdict, frozen
held-out tests, numerical error estimates and a documented energy/shift
comparison. Update the claim only according to the cross-family gates.

## Required adversarial check

Use a second propagation implementation for N=5 and test its window/basis
sensitivity. In the proposer run, the energy fraction is stable over three
windows, while the full complex field is not established as converged. Verify
the conservative bound for the C2 phase continuation and distinguish it from
stationarity of the original clipped-coordinate basis. Follow the repository's
clean-context audit protocol; do not read proposer exploration or audit notes
until your independent report is committed. Every numerical statement above
refers to run `2026-10-17-gpt-a-phase-headroom`.
