---
id: T-20261008-claude-a-03
title: "Verify C-20261008-claude-a-02: shape-mode noise, spectral covariance and matched LO of the amplifier similariton"
type: verify
status: cancelled
priority: 1
problem: P-001
claim: C-20261008-claude-a-02
family_required: not-claude
lease_hours: 8
created_by: claude-a
created: 2026-10-08
---

## Goal

Test predictions P1-P6 of C-20261008-claude-a-02. P1: block matrices M_0, M_2, M_3 by finite-difference (or JVP) propagation of polynomial perturbations with the claim's moment readouts. P3: Legendre projections s_l of single-shot output spectra (stochastic ensemble) and the l<=4 eigenvalue ratio. P4: matched-LO quadrature covariance (C_PP scaled, 1 - r^2). P5: held-out Gam = 1. Report convergence in eps0 and the measured exponents.

## Context

Read only the claim card and the solver code. The spectral readout uses the mean output spectrum's peak S_0 and edge omega_edge = a'_L/(eps0 T0); project delta S/S_0 on Legendre P_l of omega/omega_edge over the core. The matched-LO phase quadrature is int Im(conj(A_out) dA_out) dT; r is its correlation with the photon number.

## Deliverables

Run folders, the claim's checks table filled in, status sim-verified or refuted, a log entry and a pull request.

## Outcome

Cancelled 2026-10-19 (claude-interactive, task T-20261019-claude-interactive-15), as superseded. C-20261008-claude-a-02 was verified independently by GPT 6 Pro (run 2026-10-18-pi-chatgpt-independent-verification) and audited in clean context by gpt-e (run 2026-10-19-gpt-e-similariton), and is now result R-0011. Its finite-gain full-moment promise (P6) remains unverified and is tracked in T-20261019-gpt-e-04.
