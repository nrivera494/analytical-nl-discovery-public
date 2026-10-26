---
id: T-20261010-claude-a-01
title: "Verify C-20261010-claude-a-01: dispersionless lambda_min closed forms and the sqrt(Phi L/L_D) law"
type: verify
status: open
priority: 2
problem: P-20261010-claude-interactive-01
claim: C-20261010-claude-a-01
family_required: not-claude
lease_hours: 6
created_by: claude-a
created: 2026-10-10
---

## Goal

Independently check the claim card C-20261010-claude-a-01 (read only the card and the evaluator code, per docs/AUDIT_PROTOCOL.md). (1) Kerr: lambda_min(V) = V_min(Phi) for Gaussian and sech on a converged grid. (2) Weak normal dispersion: measure lambda_min/V_min(Phi) - 1 against y = Phi L/L_D for 1e-6 <= y <= 1e-2 at Phi in {3, 30} with the solver (FastDifferentiableMMNLO, adjoint_mode=:discrete_rk4ip) or another independent propagator; compare with sqrt(2/3) Phi/sqrt(1+Phi^2) sqrt(y) and report the exponent. The optimal mode has rms width T0 (y/24)^(1/4), so dt <= 0.01 T0 is needed. (3) Raman 300 K: check that the band-limited lambda_min approaches 1/(4Phi^2) + fR H(0)/(2Phi) for long pulses (T0 = 1 and 5 ps).

## Context

## Deliverables
