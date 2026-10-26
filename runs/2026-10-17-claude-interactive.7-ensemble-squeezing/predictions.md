# Pre-registered predictions: squeezing ensembles (task T-20261017-claude-interactive.7-02)

Written and committed before any run of this folder (2026-10-17). Tangent-map Gaussian state as in
`2026-10-17-claude-interactive.7-condensate-kerr-squeezability/cond_kerr.py` (K = 5, dz = 0.02, white disorder), checkpoints z in
{1, 2, 5, 10, 20, 50, 100, 200}. own = the condensate's smallest quadrature variance in dB (vacuum 0 dB); lambda_best at n0 = 1e10 as in
best_squeezing.py (shear plus crescent curvature, optimized over Phi). Reference realization (phase_seed 1, dis_seed 7), E' = 0.3:
own = -4.9, -5.7, -5.7, -7.9, -5.8, -5.6, -1.4, +7.0 dB; lambda_best(1e10) = -22.2 (z = 10), -11.4 (50), -4.5 (100), +4.5 dB (200).

## Ensembles

- Q-dis: E' in {0.3, 0.6}, sigma = 0.3, phase_seed 1, dis_seed 101-112.
- Q-launch: E' in {0.3, 0.6}, sigma = 0.3, dis_seed 7, phase_seed 201-212.
- Q-strong: E' = 0.3, sigma in {1, 3} (L_d ~ 1 and 0.11 L_NL, the range estimated for real fibres by Garnier et al.), phase_seed 1, dis_seed 101-106.

## Predictions

- Q1 (Q-dis, E' = 0.3): own at z = 1, 2, 5 within 0.5 dB of the reference in all 12; at z = 10, 20, 50 the ensemble mean lies in [-7.5, -4.5] dB
  and every realization is below -2 dB.
- Q2 (Q-launch, E' = 0.3): at z = 10, 20, 50 the ensemble mean lies in [-9, -4] dB, and >= 9 of 12 draws are below -3 dB at each of these z.
- Q3 (E' = 0.6, both ensembles): the ensemble median of own is above -3 dB at z = 5, 10 and 20 (mostly not squeezed).
- Q4 (Q-dis, E' = 0.3): ensemble mean lambda_best(1e10) = -22 +- 3 dB (z = 10), -11 +- 3 dB (z = 50), -4.5 +- 4 dB (z = 100); at z = 200
  lambda_best > -1 dB in >= 9 of 12. The geometric SD of nu across realizations is <= a factor 2 for z <= 50.
- Q5 (Q-strong; low confidence, no theory): the ensemble mean of own at z = 10, 20, 50 is within 3 dB of the Q-dis mean, and lambda_best(1e10)
  at z = 50 within 4 dB.
- Q6 (Sagnac floor of a Dirichlet-thermalized condensate, from ensemble-thermalization E1, E' = 0.6): ensemble mean relvar0 within +-20% of the
  Dirichlet value 2.71e-3, i.e. floor -25.7 +- 0.8 dB, and every realization within +-1.5 dB.
