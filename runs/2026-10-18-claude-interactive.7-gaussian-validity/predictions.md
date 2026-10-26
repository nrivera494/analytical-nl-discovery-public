# Pre-registered predictions: Gaussian-validity checks of the squeezing results (task T-20261018-claude-interactive.7-01)

Written and committed before any run of this folder (2026-10-18). Motivation: gpt-b's review of C-20261016-claude-interactive.7-02
(docs/summary-2026-10-17-gpt-b-C-20261016-claude-interactive.7-02.md on branch task/T-20261016-claude-interactive.7-07): in exact one-mode Kerr,
at n = 4096 and s = chi n z = 4, the coherence is 0.996 but det V = 2.51 against 1/4 for a pure Gaussian. Leading-order estimate used here:
the crescent curvature adds V'^2/(8 n) to the narrow-direction variance and V'^3/(8 n) to det V (vacuum-1 units, V' = phase-quadrature
variance); this gives det V ~ 2.25 (vacuum-1/2 units) at their point. Units: vacuum variance 1 unless stated; n0 = condensate photons per cell.

## G1 Single-mode Kerr stage on a mixed Gaussian input (exact classical map of Wigner samples = truncated Wigner, error O(1/n0))
Inputs: the condensate covariances [[V_X, C], [C, V_P]] of runs/2026-10-17-claude-interactive.7-condensate-kerr-squeezability/cond_kerr.json
(E' = 0.3, sigma = 0.3, z = 10, 50, 100) and of three Q-dis members of runs/2026-10-17-claude-interactive.7-ensemble-squeezing (dis_seed 101, 104,
107; z = 10, 50), and the coherent state V = I; n0 in {1e8, 1e10}; 2e5 samples; Kerr phase Phi scanned.
- G1a: for V = I the best variance is 0.945 n0^(-1/3) within 0.3 dB (the exact Fock result of kerr_curvature.py).
- G1b: for every mixed input, the best variance agrees with the best_squeezing.py optimum (exact 2x2 shear plus V'^2/(8 n0)) within 1 dB.
- G1c: where V_P < (4 n0 nu^2)^(1/3), it agrees with 0.945 (nu^4/n0)^(1/3) within 1.5 dB.

## G2 Multimode quadrature squeezing (tangent map against a truncated-Wigner ensemble on the same trajectory)
GRIN resonant model, K = 5, E' = 0.6, sigma = 0.3, phase_seed 1, dis_seed 7, dz = 0.02 (the case of runs/2026-10-16-claude-interactive.7-grin-gaussian-state),
512 trajectories, n in {1e6, 1e10}, z in {5, 10, 20, 50, 100}. Measured: the Wigner variance along the tangent map's most-squeezed direction u_min.
- G2a: agrees with lambda_lin = 1/sigma_max^2 within 1 dB wherever sigma_max^6 < 0.8 n0.
- G2b: exceeds lambda_lin by more than 3 dB wherever sigma_max^6 > 8 n0.
  With sigma_max^2 = 69, 276, 1097, 7044, 25848 at z = 5, 10, 20, 50, 100 and n0 ~ 0.7 n:
  - n = 1e10: agreement at z = 5, 10, 20, failure at z = 50, 100;
  - n = 1e6: agreement at z = 5, failure at z >= 10.

## G3 Photon-counting squeezing lambda_gen (same runs)
Measured: Var(sum_p w_p N_p) / (sum_p w_p^2 <N_p>) with N_p = n|A_p|^2 and the tangent map's optimal weights.
- G3a: agrees with lambda_gen,lin within 1 dB wherever V_P,0^2 < 0.8 lambda_gen n0.
- G3b: exceeds it by more than 3 dB wherever V_P,0^2 > 8 lambda_gen n0.
  V_P,0 is the condensate's phase-quadrature variance from the tangent map, evaluated at the same z.

## G4 The condensate's own squeezing (thresholds only, no new run)
For all 12 Q-dis realizations at E' = 0.3, the curvature threshold n0* = V_P^2/(0.8 lambda_own) is below 1e9 at z <= 50, so the
-8 to -10 dB ensemble values are inside the Gaussian regime at n0 ~ 1e10.
