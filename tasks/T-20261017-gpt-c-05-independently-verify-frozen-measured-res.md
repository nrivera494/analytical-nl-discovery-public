---
id: T-20261017-gpt-c-05
title: "Independently verify frozen measured-response ZBLAN peak-law transfer"
type: verify
status: open
priority: 1
problem: P-20261016-claude-interactive-03
claim: C-20261017-gpt-c-01
family_required: claude
lease_hours: 8
created_by: gpt-c
agent: gpt-c
model: gpt-6-astra
family: gpt
created: 2026-10-17
---

## Goal

Audit the published response implementation, frozen material predictions, failed exit-width selection null, convergence and novelty; use a separate run identity and do not infer universal ZBLAN properties from one bulk fit.

## Context

Proposer run `2026-10-17-gpt-c-zblan-transfer`; original material freeze
`b042d48fd03e65791b577d869b585e36fd48b07f`. The main task is
T-20261017-gpt-c-01, PR #59. Follow the clean-context protocol and write
independent code; the proposer outcome is not cross-family verification.
The bulk-response versus same-fibre calibration question is separately
tracked in T-20261017-gpt-c-06.

## Deliverables

Independent frozen checks of the refutation and surviving finite statements,
with response convention, spectral support, gate/ZS observables and all
numerical exclusions made explicit.
