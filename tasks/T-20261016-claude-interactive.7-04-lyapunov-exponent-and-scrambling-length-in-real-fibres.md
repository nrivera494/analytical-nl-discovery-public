---
id: T-20261016-claude-interactive.7-04
title: "Lyapunov spectrum and scrambling length of spatial Kerr thermalization in real GRIN and step-index fibres"
type: explore
status: open
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.7
created: 2026-10-16
---

## Goal

The largest Lyapunov exponent lambda_1 L_NL of the classical spatial multimode dynamics, and so z_E = ln(n_cell/F_in)/(2 lambda_1). Compute it for a GRIN fibre (real overlaps, 5-15 mode groups) and one step-index fibre, with and without weak intra-group disorder. Cover non-condensed and condensed launches (condensate fraction 0.3-0.9), at powers used in self-cleaning experiments. State whether typical metre-scale experiments with a quiet laser are before or after scrambling.

First look (run 2026-10-16-claude-interactive.7-grin-lyapunov-modecount; resonant GRIN model, single trajectories, weak Brownian disorder, fixed thermal f0 = 0.70): lambda_1 L_NL = 0.024, 0.020-0.021, 0.019, 0.016, 0.015-0.016 for 10, 15, 21, 28, 36 modes (two launch seeds at 15 and 36). It falls slowly with M and levels off. Check with realistic disorder, a non-resonant model and more modes.

## Context

In the toy model (random overlap tensor, equidistant groups, M <= 15; run 2026-10-16-claude-interactive.7-rj-toy-thermalization), lambda_1 is about 0.004-0.025 in units of g N in the condensed regime. That would put z_E at thousands of L_NL. A real overlap tensor and degeneracy structure may change this. Use the solver's multimode spatial model (CW, dispersionless) with a shadow trajectory or the tangent map.

## Deliverables

- A run folder with lambda_1 against condensate fraction, mode count, disorder strength and L_beat/L_NL.
- The z_E estimate for two published experiments.
