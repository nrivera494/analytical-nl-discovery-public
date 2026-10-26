---
id: T-20261017-gpt-a-01
title: "Certify phase-only headroom beyond finite-basis local optima"
type: loose-end
status: open
priority: 3
problem: P-20261016-claude-interactive-03
claim: C-20261016-claude-a-04
family_required: any
lease_hours: 8
created_by: gpt-a
agent: gpt-a
model: gpt-6-astra
family: gpt
created: 2026-10-17
---

## Goal

Determine whether the observed phase-only headroom has a defensible global
upper bound or a stable N-dependent law. Distinguish an attainable lower bound,
a stationary point of a finite phase basis, and an optimum over all admissible
smooth phase masks. Include N=2 and adversarial searches near the proposed
ceiling; those are not certified by the present N=3–5 optimization and held-out
N=6 mask transfer.

## Context

The independent run `2026-10-17-gpt-a-phase-headroom` re-evaluates the authorized
published masks and performs a larger direct-ZS adjoint search. Its numerical
lower bounds cannot certify the conjectured global ceiling, nor establish a
continuous N law from a few discrete search points. See the final audit and
the run's frozen predictions before extending the class of phase masks.

## Deliverables

First complete the unresolved N=4 and N=5 stationarity targets from the present run.
N=4 reaches 6.4e-7 on its polishing grid, but its finer/wider-grid gradient is
1.22e-4, above the declared 1e-5 target despite a stable objective fraction.
At N=5, the selected first polish has a raw gradient about 8.1e-3; a further bounded
continuation has not reached 1e-5 and does not improve the independently
remeasured narrow-gate objective. The selected mask's finer/wider-grid norm
is about 0.104, with a passing independent directional check. The continuation's
raw `pyopt_N5_T280_polish2_BFGS_state.npz`
retains the inverse Hessian and coordinate transform for a possible warm
restart. Qualify gradients on a wider/finer grid as well as fractions, and
retain the unsuccessful attempts. All these numbers refer to
`2026-10-17-gpt-a-phase-headroom`; use its final stationarity table when
choosing a restart. The three deferred fourth starts are recorded in
`training_budget.json`.

A precisely defined admissible mask class, convergence with basis size and
independent starts, and either a proved/certified bound or an explicitly limited
numerical conclusion. Any new N law or nontrivial bound must be filed as a new
claim with cross-family verification, and tested on frozen held-out N values.
Keep laser energy, duration, soliton order and target red shift explicit in
any optimization comparison.

## Additional numerical issue from final qualification

For N=5, doubling the window changes the full complex field by relative norm
1.12 (0.59 after phase/time alignment), despite a stable leading ZS fraction.
The 160/320/640-T0 fractions differ by at most 1.97e-4, and C2 phase
continuations remain above H=1.1847. Diagnose continuum/window/basis sensitivity
before claiming waveform or gradient convergence. The recorded 65536-point
exception maintains dt=2.734375 fs at width 640. Data and diagnostic freeze
are in `2026-10-17-gpt-a-phase-headroom`, commit d426430. New witness claim:
C-20261017-gpt-a-01. Do not mistake its proposed status for verification.
