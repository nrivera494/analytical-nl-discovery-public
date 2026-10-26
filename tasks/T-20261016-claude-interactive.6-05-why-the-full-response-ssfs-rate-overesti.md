---
id: T-20261016-claude-interactive.6-05
title: "Why the full-response SSFS rate overestimates the GNLSE shift for solitons shorter than 30 fs"
type: explore
status: open
priority: 3
problem: P-20261016-claude-interactive-02
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.6
created: 2026-10-16
---

## Goal

Run 2026-10-16-claude-interactive.6-h2-fundamental: the sech-overlap (full Raman response) rate overestimates the GNLSE shift by 7%, 17%, 20% at T0 = 30, 20, 15 fs in SMF-28, while the linear-T_R rate underestimates. Identify the mechanism (self-steepening deceleration, cf. Voronin & Zheltikov 2008; soliton reshaping; radiation) and give the correction with its error order.

## Context

The creating session (claude-interactive.6, 2026-10-16) already excluded self-steepening and higher-order dispersion (`runs/2026-10-16-claude-interactive.6-h2-fundamental/summary_noshock.json`). The overestimate persists and grows in the pure NLSE with Raman: 39%, 30% and 10% at $T_0=15$, 20 and 30 fs, and −0.6% at 50 fs. The next step is a second-order (non-adiabatic) soliton perturbation theory of the Raman term, or a variational ansatz with chirp and asymmetry, checked against those numbers.

## Deliverables
