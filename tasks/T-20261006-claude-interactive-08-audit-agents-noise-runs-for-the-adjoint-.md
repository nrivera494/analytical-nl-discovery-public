---
id: T-20261006-claude-interactive-08
title: "Audit agents' noise runs for the adjoint, Raman-kernel and Raman-spectrum issues"
type: audit
status: open
priority: 2
problem: null
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-06
---

## Goal

Every registered run or open claim that computes noise with the solver is checked for the default continuous adjoint, a time step above about 3 fs with Raman, and the legacy Raman Langevin spectrum (including the public RamanLangevin path), and each affected number is flagged or recomputed.

## Context

Three solver issues found on 2026-10-05/06 can bias noise numbers:
- the default continuous adjoint (T-20261006-claude-interactive-03);
- the under-resolved Raman kernel at time steps above about 3 fs (T-20261006-claude-interactive-02);
- the legacy Raman Langevin spectrum, with half the zero-point part and no DC term. This is used by `stochastic_solve_raman` whenever no `Cω` is passed and always by the public `RamanLangevin` stochastic path (T-20261004-gpt-b-02).

Runs and claims from round 1 (P-001, P-002, P-20261004-root-03, P-20261004-claude-interactive-02) have not been checked.

## Deliverables

- A table of every registered run and open claim that computes noise with the solver, with which of the three issues apply, and the affected numbers flagged in their claim cards or recomputed.
