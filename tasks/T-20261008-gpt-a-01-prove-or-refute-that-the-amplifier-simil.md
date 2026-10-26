---
id: T-20261008-gpt-a-01
title: "Prove or refute that the amplifier similariton is an attractor, and state its basin"
type: derive
status: done
priority: 1
problem: P-001
claim: C-20261008-gpt-a-01
family_required: any
lease_hours: 8
created_by: gpt-a
agent: gpt-a
model: gpt-6-astra
family: gpt
created: 2026-10-08
---

## Goal

A statement, proved where possible and otherwise sharply qualified, of whether the normal-dispersion NLSE-with-gain similariton attracts inputs, in which model, for which inputs, at which rate; or a refutation.

## Context

Assigned by the PI for round 2 of P-001. Read the updated problem and plan from PR #20, independently checked the Claude-family orchestrator sketch, and read the requested merged passive claim and note. The current claude-a noise branch was not read. The deliverable is a proved or explicitly qualified statement, including a narrowed basin or refutation where appropriate; it does not require pretending that an unresolved PDE theorem has been proved.

## Deliverables

- `claims/C-20261008-gpt-a-01-gain-similariton-conditional-attraction.md`: global attraction within the parabolic hydrodynamic family, regular Legendre blocks, conditional nonlinear energy decay, and a sufficient compressive exclusion from the global classical basin.
- `claims/C-20261008-gpt-a-02-gain-nlse-attraction-scope.md`: exact odd-field obstruction to strong attraction, exact lens-energy identity, formal interior/edge orders, and a qualified finite-length density/moment map.
- Linked derivation, literature-access and numerical notes; frozen predictions and held-out inputs; dedicated evaluators and archived run records with grid, step, window, coordinate-system and restart controls.
- Session log with proposed P-001 card changes. No problem card or generated file changed; no result promotion requested.

## Outcome

The two proposer claims remain `cheap-checks-passed`, awaiting independent audit and verification. The unconditional all-input classical and strong-field interpretations are refuted in the explicitly stated senses. General weak-density attraction, an input-only physical-vacuum basin, exact published precedence of some reduced rates, and remaining lower-N/wing precision are unresolved and assigned to T-20261008-gpt-a-02 through T-20261008-gpt-a-06 and T-20261009-gpt-a-01. The conditional theorem must not be read as a global-existence proof, and the sampled finite-length acceptance set must not be called an asymptotic basin.
