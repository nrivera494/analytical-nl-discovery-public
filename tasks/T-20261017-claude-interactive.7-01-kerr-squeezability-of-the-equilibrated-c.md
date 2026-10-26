---
id: T-20261017-claude-interactive.7-01
title: "PI follow-up questions of 2026-10-17: Kerr squeezability of the equilibrated condensate; what drives thermalization in the model, seen directly"
type: explore
status: done
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.7
created: 2026-10-17
---

## Goal

Answer the PI's follow-up questions of 2026-10-17. (1) After equilibration to a condensed state at large n, can the condensate be squeezed by subsequent Kerr, or has it lost phase coherence or gained excess intensity noise? (2) How was the condensate's own squeezing established? (3) Is thermalization in the model from nonlinearity alone? Show the thermalization and the thermalized state directly from the simulation.

Answered in exploration note section 6.8 (run 2026-10-17-claude-interactive.7-condensate-kerr-squeezability). Summary:
- Before scrambling (large n, z < z_E), the condensate keeps its phase and near-shot-noise intensity noise. It is a mixed Gaussian whose mixedness nu (entanglement with the cloud) limits a subsequent single-mode Kerr stage to about 0.95 (nu^4/n0)^(1/3), including crescent curvature: -11 to -22 dB at n0 = 1e10 for z = 10-50 L_NL, none by about 200 L_NL.
- After scrambling, or for a phase-randomized ensemble, the condensate is Fock-diagonal and Kerr leaves it unchanged.
- A balanced Sagnac (self-referenced) squeezer rejects the pump's noise to first order, with floor (relative pump power spread)^2.
- Laser amplitude jitter becomes condensate phase jitter through the fibre's own Kerr, so the local oscillator must come from the condensate.
- The condensate's own squeezing (-4.9 to -7.9 dB at f0 ~ 0.85, z = 1-50) was confirmed by a step-size test and an independent 768-trajectory Wigner ensemble (within 0.2-0.4 dB). The shear is 84-91% self-phase modulation, and the cloud's cross-phase noise limits it.
- Thermalization seen directly (note section 6.9; run 2026-10-17-claude-interactive.7-grin-thermalization-visual). Power moves between groups only through Kerr, but RJ is reached only with weak linear intra-group coupling. Kerr alone gives a generalized Gibbs state, or no thermalization for an LP11-only launch.

## Context

- Problem card P-20261016-claude-interactive.7-01 (current answer, Lab test).
- Builds on runs 2026-10-16-claude-interactive.7-grin-gaussian-state (same trajectories) and -grin-shot-statistics.

## Deliverables

- Exploration note section 6.8, the run folder, card updates (done).
- Open: a check beyond the linearized model, with loss, Raman and the subsequent stage's dispersion (no task yet; listed in the log).
