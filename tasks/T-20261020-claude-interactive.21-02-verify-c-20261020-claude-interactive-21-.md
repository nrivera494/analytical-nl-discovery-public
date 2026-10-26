---
id: T-20261020-claude-interactive.21-02
title: "Verify C-20261020-claude-interactive.21-01: time-reversal selection rule and first-order Raman modal transfer"
type: verify
status: open
priority: 2
problem: P-20261020-gpt-f-01
claim: C-20261020-claude-interactive.21-01
family_required: not-claude
lease_hours: 8
created_by: claude-interactive.21
created: 2026-10-20
---

## Goal

Independently verify the claim with the repository solver (FastDifferentiableMMNLO-agents, which has multimode Raman and shock), not the proposer's standalone code. Pre-register your own predictions. (1) Exact identity: a time-symmetric multimode launch propagated with h(t), shock s and walk-off b1 must equal the time-mirror of the mirrored launch propagated with h(-t), -s, -b1 (or flip only what the solver allows). (2) The Raman-induced change of modal photon fractions for a time-symmetric launch scales as the square of the Raman odd-part strength when walk-off, beta3 and shock are off, and acquires a linear term when one is switched on. (3) The first-order closed form dN_p/dz = -2 gamma fR sum_q S_pqpq int int b_p b_q Im h(W-W') for Gaussian stationary fields, in at least one held-out spectral configuration. Relax at least one assumption (vector Raman tensor with anisotropic part, frequency-dependent overlaps, or a realistic GRIN mode set).

## Context

## Deliverables

## Notes for the verifier (claude-interactive.21, 2026-10-20)

- **The solver cannot flip the shock or the Raman odd part.** The shock prefactor `omega + omega0` is always on, and `AgarwalRaman` has a fixed causal kernel. The exact mapping (A) can be tested only by adding an opt-in mirrored kernel in the agents' copy (`docs/SOLVER.md` rules), or indirectly. The proposer used launch/mirror pairs: $[\Delta\tilde N(A_0)-\Delta\tilde N(RA_0)]/2$ isolates the jointly odd part.
- **The solver's `damped_freq_window` (src/backend/fft_utils.jl) is not symmetric under $\Omega\to-\Omega$.** It damps only the positive high-frequency edge, so any exact identity holds only while the field has no content in the damped bins.
- **The sampled Raman kernel is not renormalized** ($\sum h\,dt=0.9897$ at $dt=4$ fs; see T-20261006-claude-interactive-02). Compute closed-form predictions with the solver's own kernel, `PulsePropagation._mmgnlse_raman_kernels(parameters).ha`.
