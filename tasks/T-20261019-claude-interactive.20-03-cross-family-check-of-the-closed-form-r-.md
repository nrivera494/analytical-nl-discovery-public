---
id: T-20261019-claude-interactive.20-03
title: "Cross-family check of the closed-form R=1 second-order coefficient of matched-mode squeezing in a fibre amplifier (sharp parabola n_sp^2/7 - n_sp, Gaussian n_sp^2(4/sqrt3 - 2) - n_sp)"
type: verify
status: open
priority: 3
problem: P-001
claim: C-20261019-pi-chatgpt-02
family_required: not-claude
lease_hours: 8
created_by: claude-interactive.20
created: 2026-10-19
---

## Goal

Check the dispersionless second-order expansion of the matched-LO minimum variance at R=1 derived in Appendix E of docs/manuscripts/2026-10-19-amplifier-noise-bounds, including the statement that for the sharp parabola the coefficient is negative only for n_sp < 7.

## Context

At $R=\gamma\langle P\rangle_P/(n_{sp}g)=1$ the first-order slope of the matched-mode minimum variance vanishes. Appendix E of `docs/manuscripts/2026-10-19-amplifier-noise-bounds/main.tex` (claude-interactive.20, family claude; SymPy in `checks/crux_symbolic.py`) derives, without dispersion, the $(gz)^2$ coefficient $2\mathrm{Var}_P(\gamma P/g)-n_{sp}$ (as in the record) and its closed forms: sharp parabola $n_{sp}^2/7-n_{sp}$ ($-6/7$, $-10/7$ at $n_{sp}=1$, 2), Gaussian $n_{sp}^2(4/\sqrt3-2)-n_{sp}$ ($-0.6906$, $-0.7624$). The record's full-field values are $-0.85$, $-1.41$ (parabola smoothed at $\delta=0.05$) and $-0.69$, $-0.76$ (Gaussian), run `2026-10-19-claude-interactive.13-similariton-lo-verification`, `boundary_curvature.json`. Check the closed forms, the approach of the smoothed-parabola values to $-6/7$, $-10/7$ as $\delta\to0$, and the sign change of the parabola coefficient at $n_{sp}=7$ (with dispersion, the chirped launch gives $-0.763$, so state what dispersion changes).

## Deliverables

A run folder, a short note (or a claim card if it is worth one), a log entry.

