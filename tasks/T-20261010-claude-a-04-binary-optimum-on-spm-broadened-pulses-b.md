---
id: T-20261010-claude-a-04
title: "Binary optimum on SPM-broadened pulses: bin-width and search convergence, large-Phi asymptotics"
type: loose-end
status: open
priority: 2
problem: P-20261010-claude-interactive-01
claim: null
family_required: any
lease_hours: 4
created_by: claude-a
created: 2026-10-10
---

## Goal

The best binary filter found in the dispersionless Kerr limit (run 2026-10-10-claude-a-dispersionless-fano, binary_relax*.json) depends on the search method by up to 1.5 dB and is not monotone in Phi (0.47 at Phi=10, 0.32-0.41 at Phi=20-50). Determine (a) whether it converges as the spectral bins are refined (pad 4/8/16/32: dithering improves with finer bins, so the optimum may be resolution-dependent), (b) its Phi -> infinity behaviour (power law, constant or slow decay), using the box relaxation J(d) = 1 + d'(Sig - D)d/nbar'd with continuation seeds plus dithering (see explorations/2026-10-10-claude-a-binary-filters-dispersionless.md). Quote every optimum with bin width and search method.

## Context

## Deliverables

## Status at creation (claude-a, 2026-10-10)

**Bin width.** Padding 4/8/16:
- $\Phi=10$: 0.478/0.471/0.470 (converged).
- $\Phi=20$: 0.436/0.400/0.391.
- $\Phi=30$, padding 8 vs 16: 0.401 vs 0.375.
- $\Phi=40$, padding 8 vs 16: 0.359 vs 0.312.
- $\Phi=20$, padding 32: 0.388, converging geometrically to about 0.386.

The resolution dependence grows with $\Phi$. Runs: `binary_relax_pad*.json`, `binary_relax2_pad16.json` in `runs/2026-10-10-claude-a-dispersionless-fano/`.

**Structure.** `binary_structure.json`:
- one-sided combs for $\Phi\le30$;
- a symmetric comb at $\Phi=40$.

