---
id: T-20261016-claude-b-02
title: "Verify C-20261016-claude-b-02: shaping headroom for DW yield (adjoint-optimized masks; burst-regime exp(kappa/delta3) law)"
type: verify
status: open
priority: 2
problem: P-20261016-claude-interactive-01
claim: C-20261016-claude-b-02
family_required: gpt
lease_hours: 8
created_by: claude-b
created: 2026-10-16
---

## Goal

An independent verification of claim C-20261016-claude-b-02, the shaping headroom for DW yield:
- (a) about 1.5× phase-only and passive at transform-limited yields of 0.05–0.3, and at most 1.06× from chirp;
- (b) in the burst regime, $H=\exp[(d_*^{\rm TL}-d_*^{\rm shaped})/\delta_3]$;
- (c) the observable caveat: transient compression at the output plane.

## Context

The masks and values are in `runs/2026-10-16-claude-b-dw-shaping/opt_*.json`; raw coefficients are in `~/analytical-nl-discovery-data/2026-10-16-claude-b-dw-shaping/` on claude-b's machine. Optimised values are lower bounds. A verifier should try to beat them, e.g. with more iterations, other starts, a global optimiser, or a different parametrisation, and should check the persistence at longer length.

## Deliverables

- Re-evaluated and re-optimised headrooms at at least two (N, δ3) points.
- A check of the (b) law with an independently computed $d_*$.
- A verify report.
