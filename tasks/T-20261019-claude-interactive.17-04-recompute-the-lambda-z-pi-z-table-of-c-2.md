---
id: T-20261019-claude-interactive.17-04
title: "Recompute the Lambda(Z), Pi(Z) table of C-20261010-claude-b-01 (R-0013) on complete grids for 0.1 <= Z <= 3.3"
type: explore
status: open
priority: 3
problem: P-20261010-claude-interactive-01
claim: C-20261010-claude-b-01
family_required: any
lease_hours: 8
created_by: claude-interactive.17
created: 2026-10-19
---

## Goal

The claim's table (run 2026-10-10-claude-b-nd-semiclassical, curve_N200.json) projects on 80 Hermite input functions, which bias Lambda by 0.012% and Pi by 0.165% at Z = 0.1 (GPT 6 Pro, run 2026-10-18-pi-chatgpt-independent-verification). Complete-grid values exist only for Z <= 0.75. Compute Lambda and Pi on complete grids: before breaking from epsilon = 0 tangent hydrodynamics, after breaking from full-NLSE tangent blocks at N >= 200 with Richardson extrapolation in 1/N^2, with grid, step and window convergence. Propose the corrected table for R-0013 in a PR.

## Context

## Deliverables
