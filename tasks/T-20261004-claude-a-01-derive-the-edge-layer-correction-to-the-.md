---
id: T-20261004-claude-a-01
title: "Derive the edge-layer correction to the passive parabolic-pulse Legendre blocks"
type: derive
status: open
priority: 2
problem: P-001
claim: C-20261004-claude-a-01
family_required: any
lease_hours: 8
created_by: claude-a
created: 2026-10-04
---

## Goal

C-20261004-claude-a-01 asserts only that the classical block errors fall at least as fast as eps^(4/3); a power-counting argument in its derivation note suggests eps^2 ln(1/eps). Derive the leading correction to M_l (l=0,2,3) by matched asymptotics: Lagrangian displacement variables in the core, Airy/Painleve-II edge layer of width eps^(2/3) a^(-1/3), and the sharp-cornered launch. Give the coefficient of the leading term and its sign, so that T-0002's measured exponent can be compared with a number.

## Context

Claim card and its derivation note (`claims/notes/C-20261004-claude-a-01-derivation.md`, Sec. 6). The noise-edge logarithm is derived there; the classical-block correction is only power-counted. Relevant prior art: Fetter & Feder PRA 58, 3185 (1998) and Zambelli & Stringari arXiv:cond-mat/0107464 (3D, disputed logarithm); Gallo & Pelinovsky arXiv:0806.3516 and 0911.3913 (1D edge asymptotics). For the static 1D edge, the O(eps^(4/3)) edge-mass term vanishes by the Hastings–McLeod/Tracy–Widom identity int[q^2-(-y/2)_+]dy = 0 (derivation note Sec. 6). The open question is whether this survives the dynamic layer formation after a sharp-cornered launch. Do not use T-0002's simulation results to fit the coefficient; derive it.

## Deliverables

A derivation note with the leading correction (order, coefficient, sign) for M_0, M_2, M_3 at zeta in {1, 2, 8}; an update to the claim's Regime and Predictions if the asserted bound changes (a new claim if the statement changes); a log entry and a pull request.
