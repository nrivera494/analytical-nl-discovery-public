---
id: T-20261020-claude-interactive.21-04
title: "Test whether fast Kerr relaxation clamps the second-order Raman modal drift (L_kin/L_R^2 conjecture) in a three-group GRIN toy"
type: explore
status: open
priority: 3
problem: P-20261020-gpt-f-01
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.21
created: 2026-10-20
---

## Goal

Conjecture (exploration note 2026-10-20-claude-interactive.21-raman-parity-selection, section 3.4): once Kerr exchange between groups relaxes mode-dependent spectral tilts, the Raman^2 modal drift grows like z L_kin/L_R^2 instead of the no-Kerr (z/L_R)^2. The three-mode test of run 2026-10-20-claude-interactive.21-raman-parity has no resonant inter-group exchange, so it cannot test this. Use at least three equidistant groups (resonant g0+g2 <-> g1+g1) with intra-group random coupling. Propagate many L_kin with lambda = +-1, 0 Raman odd-part and mirror-closed ensembles (the exact identity cancels all lambda-odd parts). Pre-register the z-scaling exponent of the lambda-even modal change before and after L_kin, and check step, grid and window convergence.

## Context

## Deliverables

## First attempt (2026-10-20, claude-interactive.21; task stays open)

Run `runs/2026-10-20-claude-interactive.21-raman-clamp`, with predictions frozen in commit `12d49a1`. Six-mode toy with three groups: $\delta\beta L_{\rm NL}=30$, $D_d=30$ m⁻¹, $30L_{\rm NL}$, 8 mirror pairs.

- **Outcome.** The exact checks pass. The fundamental gains at second order. The group populations did not relax: fraction of group 1 went from 0.104 to 0.117 against an RJ value of 0.339. So the clamping test was inconclusive under its own rule.
- **Garnier's scaling** $L_{\rm kin}/L_{\rm NL}\sim\Delta\beta L_{\rm NL}/\bar S^2$ predicts 50–100 for this toy, and at least about 20–30 even at $\Delta\beta L_{\rm NL}\sim1$. A successful test needs $\gtrsim100L_{\rm NL}$, more groups (larger resonant overlaps), or direct integration of the kinetic equation.
- **Post hoc.** Kerr suppressed the Raman-driven inter-group centroid offset (0.20–0.24 of the no-Kerr value at 20–30 $L_{\rm NL}$) long before the populations relaxed. Exploration note §6b.
- **Second configuration `g4_weak`** (10 modes, weak coupling $D_d=1$ m⁻¹, pre-registered in `31aba86`): populations relaxed only 30% of the way within $30L_{\rm NL}$. C1 failed narrowly (0.423 against <0.40) and C3 was inconclusive. Post hoc it showed the same Kerr suppression: centroid offset 0.34–0.49 and $E_0$ 0.47–0.64 of the no-Kerr values, with $E_0$ still growing about as $z^2$. Next attempt: about 100 $L_{\rm NL}$ with the weak coupling, or five or more groups.
