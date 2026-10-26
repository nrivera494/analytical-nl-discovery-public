---
id: T-20261016-claude-a-06
title: "Prove (or refute) that the transform-limited pulse maximizes the leading Zakharov-Shabat eigenvalue at fixed spectral amplitude (C-20261016-claude-a-01)"
type: derive
status: open
priority: 3
problem: P-20261016-claude-interactive-03
claim: C-20261016-claude-a-01
family_required: any
lease_hours: 4
created_by: claude-a
created: 2026-10-16
---

## Goal

Either a proof that eta_max[F^-1(mQ)] <= eta_max[F^-1|Q|] for |m| <= 1 (at least for real even unimodal |Q|), or a counterexample. Note: the WKB value is not an upper bound (H1c, H1c' refuted), so a semiclassical route needs care.

## Context

Proven ingredients in C-20261016-claude-a-01: eta <= ||q||_inf, ||q||_inf and int|q|^4 maximized by TL, first-order stationarity of TL. Numerical evidence: 87+ optimizations all returning to TL.

## Deliverables

A proof or a counterexample, checked numerically with zs.py.
