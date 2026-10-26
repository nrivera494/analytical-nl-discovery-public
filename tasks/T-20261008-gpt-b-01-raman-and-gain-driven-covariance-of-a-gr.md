---
id: T-20261008-gpt-b-01
title: "Raman- and gain-driven covariance of a GRIN or step-index multimode soliton's collective coordinates"
type: derive
status: done
priority: 1
problem: P-20261004-claude-interactive-02
claim: C-20261008-gpt-b-01
family_required: any
lease_hours: 8
created_by: gpt-b
model: gpt-6-astra
family: gpt
created: 2026-10-08
---

## Goal

An analytical formula, with its regime and checks, for the Raman- and gain-induced covariance growth of a bound multimode soliton's energy, phase, timing and frequency, and of its modal fractions and relative modal phases, in GRIN and step-index fibre.

## Context

Explicit PI round-two assignment, overriding the problem's stale candidate
status while leaving the card unchanged. The PR #20 card, round-one
baseline, review, solver capability and normalization caveats were read.
T-20261004-claude-interactive-09 is related and was not claimed.

## Deliverables

- Proposed claim C-20261008-gpt-b-01, with an unpropagated step-index
  prediction frozen in commit `dc16c67`.
- Full derivation in `explorations/2026-10-08-gpt-b-multimode-covariance.md`.
- Evaluator and reproduction guide in `evaluator/mm_soliton_covariance_README.md`.
- Source-specific covariance matrices and proposer checks in the registered
  `2026-10-08-gpt-b-covariance-*` and gain-calibration runs.
- Follow-up tasks T-20261008-gpt-b-02 through -04 for independent verification,
  evolving-mean closure, and physical-fibre qualification.
