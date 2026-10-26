---
id: T-20261016-claude-interactive.7-10
title: "Derive and test the photon-counting squeezing law lambda_gen(z) of the thermalizing multimode field before scrambling"
type: derive
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

In the linearized (pre-scrambling) state of a Kerr-thermalizing multimode CW field, the best real-weighted, mode-resolved photon-count Fano factor lambda_gen falls about 10 dB per decade of z/L_NL. In the GRIN resonant model it reaches -20 to -27 dB at 400 L_NL, ideal and lossless (run 2026-10-16-claude-interactive.7-grin-gaussian-state).

Deliverables of the derivation:
- the law lambda_gen(z), first conjectured as about c/(z/L_NL), with its mechanism. The optimal weights are mostly on the fundamental's photon number, corrected by higher-order-mode photon numbers, with 3-8 sub-shot-noise directions (gauss_weights.json); they are not twin-beam differences. Treat the shear stage and the chaotic stage separately;
- its dependence on condensate fraction, mode count and disorder;
- how loss (detection efficiency) and Raman noise bound it.

Check against the solver's linearized covariance for a real GRIN fibre (CW or long pulse), with lambda_min(V) and the readout hierarchy of P-20261010-claude-interactive-01.

The effect is robust to mode count: K = 4, 5, 6 (10-21 modes) give nearly the same lambda_gen(z) (gauss_modecount_summary.txt). Hypothesis to test: the excitations act as a meter of the condensate number. XPM imprints the input number fluctuation on the excitation phases with a gain proportional to z; FWM converts phase to population; a weighted count subtracts it. lambda_gen ~ 1/z would follow if the meter noise grows like sqrt(z). In the minimal 3-mode integrable model (HG00, HG10, HG20), lambda_gen saturates at -5 to -8 dB (minimal_lgen_summary.txt), so the continued improvement needs many exchange channels. Strong lead (gauss_structure.json): for z >= 50, 95-99% of the optimal weight vector lies in the span of the amplitude projections of grad N, grad E' and grad H_res, but neither that span alone (-2 to -9 dB) nor its complement (-1 to -5 dB) reaches the optimum (-13 to -27 dB). Start the derivation from the conservation of H_res: its amplitude part is measured, and the small admixture cancels its phase part. Partial mechanism (exploration note 6.5). A conserved, intensity-only quantity keeps its input noise sum (dC/dI_p)^2 I_p(0), while its shot-noise normalization is sum (dC/dI_p)^2 I_p(z). Weights a + b eps_p + c omega_p that emphasize modes empty at launch therefore give Fano < 1. That saturates at -2 to -9 dB once the populations stop moving. The roughly 1/z part must come from the admixture (shear-built phase-amplitude correlations); derive that part.

## Context

- Exploration note explorations/2026-10-16-claude-interactive.7-quantum-rj-state.md, sections 3 and 6.5. The conjecture that photon counting cannot reach the Lyapunov squeezing was refuted there.
- Related: P-20261010-claude-interactive-01, the filtered-Fano bounds and the readout hierarchy.

## Deliverables

- An exploration note with the derivation.
- A run with the solver.
- A claim if a law survives.
