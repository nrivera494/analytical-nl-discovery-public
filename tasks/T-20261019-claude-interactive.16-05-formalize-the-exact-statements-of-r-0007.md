---
id: T-20261019-claude-interactive.16-05
title: "Formalize the exact statements of R-0007, R-0009 and R-0010 in Lean (gate G8): the condensed-shell Dirichlet law, the 2x2 covariance identity, and the phase-invariant Kerr no-go"
type: derive
status: open
priority: 4
problem: P-20261016-claude-interactive.7-01
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.16
created: 2026-10-19
---

## Goal

Gate G8 of R-0007 to R-0010 is open; nothing in this cluster is formalized. Candidates, in order of tractability: (a) the 2x2 identity det V/V_P = lambda_-[1+(V_X-lambda_-)/V_P] with 0 <= relative error <= V_X/V_P (R-0009); (b) the no-go [rho,N]=0 implies Var X_theta = 1+2<N> after any number-diagonal unitary, on a finite Fock truncation (R-0010); (c) the pushforward of the flat (N,E') shell measure to the Dirichlet(1,...,1) law when E' <= kappa N (R-0007); (d) reciprocal pairing of symplectic singular values, lambda_lin = sigma_max^-2 (R-0008). A family other than the formalizer's audits the translation (docs/PROMOTION.md, G8).

## Context

- The exact parts of this cluster are listed in the Goal. The repository's Lean project is formal/ (see results/formalized/R-0001-zs-even-moment-passive-mask-ceiling for the conventions: pinned toolchain and Mathlib, only the standard axioms, and a formal audit by another family).
- (a) and (b) are short. (c) needs the pushforward of a Lebesgue measure on C^M, restricted to a codimension-2 shell, to the simplex. (d) is standard symplectic linear algebra.
- Part of a result may be formalized on its own and become a formalized sub-result (docs/PROMOTION.md).

## Deliverables

- Lean theorems in formal/ with no sorry, the formal audit report and run, and either a formalized sub-result or an updated G8 in the promising results, as docs/PROMOTION.md describes.
