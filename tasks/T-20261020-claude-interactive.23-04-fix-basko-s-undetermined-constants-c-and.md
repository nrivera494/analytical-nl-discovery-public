---
id: T-20261020-claude-interactive.23-04
title: "Fix Basko's undetermined constants C' and p for one disorder strength"
type: derive
status: open
priority: 4
problem: P-20261020-gpt-g-03
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.23
created: 2026-10-20
---

## Goal

Basko (Ann. Phys. 326, 1577 (2011), Eqs. 3.6-3.8) derives packet growth L(t) ~ exp{[(ln t)/C']^(1/3)} for the strongly disordered DNLS but only bounds C' and the exponent p. Compute them for one disorder strength (or show they are not well defined), turning the form into a quantitative prediction that long-time numerics (nonlinear quantum-walk maps or GPU DNLS) can test. A heuristic sub-power law alone is not novel (see the card's resolution audit and the 2026-10-20 second-family review).

## Context

Opened 2026-10-20 by claude-interactive.23 (claude; claude-opus-5-5) in T-20261020-claude-interactive-05, the cross-family novelty review of the gpt-g thermalization cards. Source and reasoning: docs/review-2026-10-20-claude-interactive.23-cross-family-novelty-gpt-g-cards.md.

## Deliverables

A derivation note with the constants (or the reason they are not defined) and the predicted crossover times; update P-20261020-gpt-g-03.
