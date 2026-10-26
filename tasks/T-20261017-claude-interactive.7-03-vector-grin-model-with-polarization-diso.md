---
id: T-20261017-claude-interactive.7-03
title: "Vector GRIN model with polarization disorder (Fusaro-Garnier) and inter-group coupling (Berti): test the scalar intra-group disorder conclusions"
type: explore
status: open
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.7
created: 2026-10-17
---

## Goal

Repeat the thermalization and condensate-squeezing tests of note sections 6.8-6.10 in a two-polarization GRIN model with Ornstein-Uhlenbeck polarization disorder of realistic strength (L_d/L_NL ~ 0.02-0.4, l_c ~ 0.5-30 cm) and a weak inter-group coupling, and say which conclusions of the scalar intra-group model survive.

Why: the scalar model of runs 2026-10-17-claude-interactive.7-ensemble-thermalization, -disorder-model-scan and -ensemble-squeezing
(note section 6.10) has random coupling only among the degenerate spatial modes of each group. The literature's "weak disorder"
(Fusaro et al., PRL 122, 123902 (2019); Garnier et al., PRA 100, 053835 (2019)) is random coupling of the two polarizations of each mode,
an Ornstein-Uhlenbeck process with l_beta ~ 0.5-30 cm and L_d = 1/(sigma_beta^2 l_beta) ~ 2-40 cm, against L_nl ~ 1 m.
Their "strong disorder" (Berti et al., PRL 129, 063901 (2022)) also couples non-degenerate modes and pulls toward equipartition of power.
Neither is in the scalar model.

Steps:
- Vector Kerr tensor for two polarizations (XPM 2/3, four-wave mixing 1/3, or the circular basis), with polarization disorder of
  realistic strength and correlation length. Check against Garnier et al.'s discrete kinetic equation.
- Repeat the ensemble tests: the Dirichlet statistics with D = 2M - 1 (two polarizations; S_z not conserved), the Kerr-only endpoint,
  and the all-LP11 launch.
- Add a weak inter-group coupling (Berti et al.). Find the fibre length at which equipartition overtakes RJ, against L_NL and the
  inter-group coupling length.
- Repeat the condensate-squeezing numbers (own squeezing, nu, lambda_best) at realistic disorder.

## Context

- Note sections 6.8-6.10; problem card P-20261016-claude-interactive.7-01 (literature on disorder, current answer items 4-6).
- The solver's multimode model has no linear mode coupling (T-20261016-claude-interactive.7-11).

## Deliverables
