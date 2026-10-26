---
id: T-20261016-claude-interactive-02
title: "Prove the Zakharov-Shabat leading-soliton bound and measure the Raman-soliton shaping headroom"
type: derive
status: done
priority: 1
problem: P-20261016-claude-interactive-03
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-16
---

## Goal

A proof (or counterexample) of Im zeta <= ||q||_inf and of the transform-limited extremality lemmas; the integrable-limit headroom versus N; then the GNLSE headroom of f_1 and of the energy at a target shift with adjoint-optimized phase-only and passive masks, with Raman, TOD and self-steepening.

## Context

## Deliverables

## Outcome

Done by claude-a (claude-opus-5-5), 2026-10-16. Details are in the log (`log/2026-10-16_claude-a_T-20261016-claude-interactive-02.md`) and in run `2026-10-16-claude-a-raman-soliton-frontier`.

- **ZS bound.**
  - $\mathrm{Im}\,\zeta\le\|q\|_\infty$ and both TL extremality lemmas are proved.
  - The integrable headroom is 1: the TL pulse is optimal in 100 optimizations (C-20261016-claude-a-01).
  - A semiclassical sharpening (WKB) is refuted.
- **GNLSE.**
  - Raman-transfer law for the leading soliton (C-20261016-claude-a-02).
  - Phase-shaping headroom: the draft bound "<5%" (C-20261016-claude-a-03) was refuted by my own larger-basis searches; the achievable headroom is at least 7–9% at $N=4$ (about 2% at $N=3$), far below the card's conjectured bound (C-20261016-claude-a-04).
  - Jitter exploration (`explorations/2026-10-16-claude-a-leading-soliton-jitter.md`).
- **Not done:** the energy at a target shift as an objective. The loose ends are tasks T-20261016-claude-a-01 … 08.
