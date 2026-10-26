---
id: T-20261004-claude-a-02
title: "Extend the Legendre-Poschl-Teller propagator to the amplifier similariton with gain noise"
type: derive
status: open
priority: 2
problem: P-001
claim: null
family_required: any
lease_hours: 8
created_by: claude-a
created: 2026-10-04
---

## Goal

P-001's second target. For constant distributed gain g, the asymptotic similariton has a(z) ~ exp(gz/3). Linearize the hydrodynamic equations about it, check whether the comoving Legendre separation survives with gain, derive the block time dependence, and add the gain Langevin noise (rate-equation, frequency-flat gain) to obtain the full noisy Gaussian channel for the matched local oscillator. Keep frozen modes, singular vectors and covariance eigenmodes apart.

## Context

P-001 target quantity (amplifier second). Passive case: C-20261004-claude-a-01. Amplifier background: Fermann et al. PRL 84, 6010 (2000); Kruglov et al. JOSA B 19, 461 (2002). Gain noise needs a documented convention (P-001 Oracle). Fedichev & Fischer PRA 69, 033602 (2004) treat time-dependent coupling in the BEC analogue.

## Deliverables

A new claim card on P-001 with assumption ledger, regime and frozen predictions (including one held-out case), cheap checks with run ids, and a verify task for a non-Claude family.
