---
id: T-20261006-claude-interactive-04
title: "Decide whether the Raman Langevin term carries the self-steepening factor"
type: derive
status: open
priority: 2
problem: P-20261004-claude-interactive-02
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-06
---

## Goal

A short derivation states whether the Raman Langevin force enters the GNLSE through the same (1 + i d/dt / w0) operator as the deterministic nonlinear term, and the adjoint contraction and the stochastic solver default agree with it.

## Context

The solver multiplies the whole nonlinear term by $(\omega_0+\Omega)/\omega_0$, but the Raman noise contraction in the notebooks and `stochastic_solve_raman` (default `include_self_steepening=false`) inject the Langevin term without it. Including it raises the Raman part of the squeezing Fano factor by 7.0–7.5% (run `2026-10-05-claude-interactive-raman-stochastic`, `convergence/`). The two codes agree with each other, so this is a modelling question, not an inconsistency between them.

## Deliverables

- A derivation from the nonlinear polarization showing whether the Langevin term carries the factor, with a citation (DOI or arXiv id and how much was read) for the standard stochastic GNLSE form.
- If it does: the adjoint contraction and the stochastic default changed accordingly in the agents' copy, opt-in first, with a ledger row.
