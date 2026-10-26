---
id: T-20261019-claude-interactive.16-07
title: "Cross-family check of the next-order term of the displaced-thermal Kerr optimum, lambda_* = 0.94494 (nu^4/n_d)^(1/3) [1 + (nu/4n_d)^(1/3) + O(n_d^(-2/3))]"
type: verify
status: open
priority: 4
problem: P-20261016-claude-interactive.7-01
claim: C-20261018-claude-interactive.7-03
family_required: not-claude
lease_hours: 8
created_by: claude-interactive.16
created: 2026-10-19
---

## Goal

A sympy expansion of gpt-b's exact displaced-thermal moments (results/promising/R-0010-displaced-thermal-kerr-squeezing-no-go/repro/derivation.py, claude-interactive.16, the proposer's family) gives the relative correction to the R-0010 optimum as (nu/4n_d)^(1/3), with no n_d^(-1/2) or n_d^(-5/6) term at fixed c. gpt-b's exact optima in run 2026-10-18-gpt-b-kerr-exact agree with it: the ratio of the measured to the predicted correction is 0.977-0.9996 over 1 <= nu <= 30, 1e8 <= n_d <= 1e12. A non-Claude agent re-derives the term independently and checks it against exact Fock or moment evaluations at held-out (nu, n_d). If it holds, the PI may sharpen R-0010 (i) to include it.

## Context

- The verified statement of R-0010 (i) is lambda_* = (3/(2*4^(1/3))) (nu^4/n_d)^(1/3) [1 + O_nu(n_d^(-1/3))] on the early shear branch (gpt-b, 2026-10-18).
- The CAS script expands lambda at s = c n_d^(1/6): lambda = n_d^(-1/3) nu(1 + 8 nu c^6)/(4c^2) + n_d^(-2/3) nu(28 nu c^6 - 1)/(8c^4) + O(n_d^(-1)).
- At the leading-order optimum c^6 = 1/(16 nu), this gives the relative correction (nu/(4 n_d))^(1/3). The shift of the optimum enters only at relative order n_d^(-2/3).
- It was found by the proposer's family, so it is not part of the verified result.

## Deliverables

- An independent derivation or a held-out exact check, with run ids.
- If it holds, a note to the PI proposing to sharpen R-0010 (i); otherwise the failing check.
