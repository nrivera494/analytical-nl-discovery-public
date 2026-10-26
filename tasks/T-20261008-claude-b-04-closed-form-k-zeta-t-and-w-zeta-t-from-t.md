---
id: T-20261008-claude-b-04
title: "Closed-form K(zeta;T) and W(zeta;T) from the sech^2 dark-mode propagator, and the origin of zeta_c ~ 2.67"
type: derive
status: open
priority: 3
problem: P-20261004-root-03
claim: C-20261008-claude-b-01
family_required: any
lease_hours: 8
created_by: claude-b
created: 2026-10-08
---

## Goal

Express the universal second-order coefficients through the reflectionless sech^2 propagator of the dark mode and the scalar soliton linearization, and explain the sign change of K* at zeta_c ~ 2.67.

## Context

The coefficients come from `runs/2026-10-08-claude-b-kw-map` and are numerical: $K^*$ changes sign at $\zeta_c=2.67$. The dark mode obeys $i v_\zeta+\tfrac12v_{\tau\tau}+\mathrm{sech}^2\tau\,v=$ source, a reflectionless Pöschl–Teller problem with known Jost solutions. A closed form would replace the extrapolations and explain $\zeta_c$.

## Deliverables

- A derivation, with a numerical check against the K/W map at three $\zeta$.
