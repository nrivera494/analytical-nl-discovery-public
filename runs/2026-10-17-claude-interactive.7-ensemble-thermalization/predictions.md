# Pre-registered predictions: thermalization ensembles (task T-20261017-claude-interactive.7-02)

Written and committed before any run of this folder (2026-10-17). Basis: the single-realization results of
`2026-10-16-claude-interactive.7-grin-lyapunov`, `-grin-gge`, `-grin-shot-statistics` and `2026-10-17-claude-interactive.7-grin-thermalization-visual`
(phase_seed 1, dis_seed 7), and the kinetic theory of Fusaro et al., PRL 122, 123902 (2019), arXiv:2011.05111 (full text via ar5iv),
and Garnier et al., PRA 100, 053835 (2019), arXiv:2011.03918 (full text via ar5iv).

## Model and metrics (fixed now)

- Resonant GRIN model, exact Hermite-Gauss Kerr tensor, K = 5 (15 modes, D = 14 excited), N = 1, z in L_NL, RK4 dz = 0.05, z_max = 4000.
- Disorder "white": per step U = exp(-i sigma sqrt(dz) H) in each degenerate group, H GUE with E|H_ij|^2 = 1/2, redrawn every step
  (the original quenched Brownian model; nominal L_d = 1/sigma^2). sigma = 0.3 unless stated.
- Window W = [1000, 4000] L_NL, mode powers sampled every 0.5 L_NL.
- <I0>, Var I0 over W; g2_ex = mean over the 14 excited modes of <I^2>/<I>^2; P_k = group-k power averaged over W;
  D_RJ = max_{k=1..4} |P_k/P_k^RJ - 1|; relvar0 = Var I0/<I0>^2.
- Block error of <I0>: SD of 8 consecutive block means over W divided by sqrt(8).
- L_rel = smallest z such that |mean of I0 over [z, z+50]| - <I0>_D| <= 0.02. z_on (LP11-only launch) = first z with I0 > 0.3.
- Dirichlet references (condensed regime, K = 5): <I0>_D = 1 - 0.43452 E'  (0.8696, 0.7393, 0.6089, 0.5655 for E' = 0.3, 0.6, 0.9, 1);
  Var I0_D = 0.004113 E'^2 (3.70e-4, 1.481e-3, 3.33e-3, 4.11e-3); g2_ex = 2D/(D+1) = 1.8667; P_k^RJ = (E'/14)(k+1)/k.

## Ensembles (12 members each; 12 gives the mean to +-0.3 SD and the SD to about +-21%)

- E1, disorder realizations: white sigma = 0.3, dis_seed 101-112, launch phase_seed 1, dephased (fundamental + equal power in groups 1, 2), E' in {0.3, 0.6, 0.9}.
- E2, launch draws: white sigma = 0.3, dis_seed 7, phase_seed 201-212, dephased, E' in {0.3, 0.6, 0.9}.
- E3, Kerr only: sigma = 0, phase_seed 201-212, dephased, E' in {0.3, 0.6, 0.9}.
- E4, LP11-only (all power in HG10, HG01) plus one vacuum-noise sample at n = 1e10 in every mode:
  sigma = 0.3 with dis_seed 101-112 and vac_seed 301-312 (launch phase_seed 1); sigma = 0 with phase_seed 201-212 and vac_seed 301-312.
- E5, centre-focused (modes with psi_p(0,0) != 0 phased to add at the centre; odd modes keep phase_seed phases): sigma = 0.3, dis_seed 101-112,
  phase_seed 1, E' in {0.6, 0.9}; and sigma = 0, phase_seed 1 (one run each; deterministic).

## Predictions

- T1 (RJ with weak white disorder, E' = 0.6, 0.9; ensembles E1 and E2):
  |<I0> - <I0>_D| <= 0.015 in >= 11 of 12 runs; ensemble SD of <I0> <= 0.01; ensemble mean g2_ex within +-0.03 of 1.867 and every run within +-0.06;
  ensemble mean Var I0 within +-15% of Var I0_D and every run within +-35%; D_RJ <= 0.15 in >= 11 of 12.
- T1b (E' = 0.3, f0 ~ 0.87, slow chaos): |<I0> - 0.8696| <= 0.03 in >= 11 of 12; D_RJ <= 0.25 in >= 11 of 12.
- T2 (self-averaging, E1 and E2, all E'): the ensemble SD of <I0> is at most 2x the median within-run block error.
- T3 (Kerr only, E3): for each E', D_RJ > 0.15 in >= 9 of 12 draws; the ensemble SD of <I0> is >= 2x that of E2 at the same E'.
- T4 (LP11-only, E4): sigma = 0.3: all 12 condense, z_on <= 1500 and |<I0> - 0.5655| <= 0.02.
  sigma = 0: none condenses (I0 < 0.01 for all z <= 4000) in all 12 draws. Low confidence: the stability was seen for one draw only.
- T5 (centre-focused, E5): sigma = 0.3: |<I0> - <I0>_D| <= 0.015 in >= 11 of 12 (weak disorder erases the C-03 phase memory);
  sigma = 0: <I0> within +-0.01 of the C-03 values 0.700 (E' = 0.6) and 0.582 (E' = 0.9).
