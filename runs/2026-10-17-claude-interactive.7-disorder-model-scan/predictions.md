# Pre-registered predictions: disorder strength and correlation length (task T-20261017-claude-interactive.7-02)

Written and committed before any run of this folder (2026-10-17). Same model, window and metrics as
`2026-10-17-claude-interactive.7-ensemble-thermalization/predictions.md`. Launch: dephased E' = 0.6 (phase_seed 1) unless stated;
dis_seed 101-106 (6 realizations per setting; enough to see factor-2 effects in medians, not 10% effects).

## Disorder models

- White (original): per-step Brownian increments, strength sigma, nominal L_d = 1/sigma^2 (the intra-group amplitude coherence of a
  group of n_k modes decays at rate sigma^2 n_k/4). sigma in {0.1, 0.3, 1, 3}: L_d ~ 100, 11, 1, 0.11 L_NL. dz = 0.05, and 0.02 at sigma = 3.
- Piecewise-constant (finite correlation length l_c): in each group a fixed Hermitian H (same GUE law) acts as exp(-i s H dz) per step and is
  redrawn every l_c; s = sigma_eff/sqrt(l_c) gives the same white-noise-equivalent strength sigma_eff^2 (as Delta beta = sigma_beta^2 l_beta
  in Fusaro et al.). l_c in {0.1, 1, 10, 100} L_NL at sigma_eff = 0.3; l_c in {0.1, 1, 10} at sigma_eff = 1.
- LP11-only launch with a vacuum seed (n = 1e10, vac_seed 301-306) for white sigma in {0.1, 1, 3} and piecewise l_c = 10 (sigma_eff = 0.3).

## Predictions

- D1 (endpoint): RJ for every white sigma and every l_c: |<I0> - 0.7393| <= 0.02 and g2_ex within +-0.06 of 1.867 in >= 5 of 6 realizations.
- D2 (kinetic regime of Fusaro and Garnier, L_d << L_NL: rate proportional to L_d/L_NL^2): median L_rel at sigma = 3 >= 2x median L_rel at sigma = 1.
- D3 (too weak to break the invariants quickly): median L_rel at sigma = 0.1 >= median L_rel at sigma = 0.3.
- D4 (correlation length at sigma_eff = 0.3): l_c in {0.1, 1}: median L_rel within a factor 2 of white noise. l_c in {10, 100}: endpoint RJ (D1) and
  median L_rel within a factor 3 of white noise (low confidence).
- D5 (LP11-only): condenses (z_on <= 4000 and |<I0> - 0.5655| <= 0.03) in >= 5 of 6 realizations for each setting; median z_on at sigma = 3 >
  median z_on at sigma = 1.
