---
agent: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-17
claim: C-20261016-claude-interactive.7-01
---

# Independent predictions, frozen before production

No proposer scripts, exploration, logs, or PR descriptions were read. The three
cards, problem card, permitted run metadata and protocol files were read.

## Statement under test

For a scalar classical field with one zero-energy mode, flat Liouville measure
at fixed N and E, positive excited gaps e_m, and E <= N min(e_m), x_m=e_m I_m/E
is exactly Dirichlet(1,...,1), D=M-1. This is an ensemble identity, not a proof
of dynamical ergodicity. Its predictions are

g2_m=2D/(D+1), cross_mn=D/(D+1), mean(I0)=N-E S1/D,
Var(I0)=E^2 (D S2-S1^2)/(D^2(D+1)), and
Cov(I0,Im)=-E^2 (D/e_m-S1)/(e_m D^2(D+1)).

Here S_j=sum e_m^(-j). Fixed N and E are essential; random inputs require
the law of total covariance, not an automatic addition of Var(N).

## Frozen tests and tolerances

1. Independent direct simplex sampling: K=3,4,5,6,7,8 GRIN groups, E=0.6,
   N=kappa=1. Sample >= 500000 draws per size, in small batches. All moments
   must agree within five independently batched standard errors. The finite-M
   correction 2-g2=2/M has exponent one in 1/M; fitted exponent 0.9--1.1.
   K=6 and K=8 are held out from any implementation calibration.
2. Independent exact Hermite--Gauss resonant Kerr dynamics, S0000=1,
   i da_p/ds=sum S_pqrs conj(a_q) a_r a_s, q_p+q_q=q_r+q_s.
   N=1, s=z/L_NL. Core K=5, E=0.3,0.6,0.9; sigma=0.3 and 3;
   >=6 independent disorder/launch pairs per case. Window [2000,8000]
   initially, extended to [8000,24000] if the strong-disorder case has
   not equilibrated. A failure in the initial window remains recorded.
   Independent launch phases use seeds 4101--4106, disorder 7101--7106.
   Disorder is full Hermitian Brownian coupling within each group with
   E[dB_ij dB_kl]=delta_il delta_jk ds/d, so Ld/LNL=1/sigma^2.
   Normalized pair-generator unitary splitting preserves N and E exactly.
   This convention may differ by group-dependent constants from the proposer.
3. Held-out K=4,E=0.45 and K=6,E=0.75, sigma=0.3; >=6 independent
   long trajectories. K=6 additionally has 200 independent phase launches,
   split across at least four disorder realizations, at fixed N,E.
   Different launches have identical mode powers: excited energy equally
   divided between the two lowest excited groups; I0=1-3E/4.
4. Moment tolerances for a dynamical pass: pooled mean I0 within max(0.01,3 SE),
   every excited g2 within max(0.08,3 SE), pooled mean g2 within max(0.04,3 SE),
   Var(I0) within max(15%,3 SE), and group-averaged condensate covariance signs
   agree when their prediction is resolved by three SE. Errors cluster by
   independent disorder realization, not by individual time samples.
   Report all failures. Finite-time bias and scatter are reported for windows
   of lengths 500,1000,2000,4000; an RMS sampling exponent -1/2 is a diagnostic,
   not a guaranteed physical relaxation law.
5. Numerical controls: RK4 steps 0.04,0.02,0.01, short deterministic
   DOP853 cross-check; quadrature orders >=2K and twice that order; N,E
   drifts <1e-5 and H,L drift <1e-5 when disorder is absent. Compare ensemble
   statistics under step halving. No projection/renormalization of trajectories.
6. Edge and relaxed-assumption attacks: E=1.2 at K=3 against the *truncated*
   simplex measure; d0=2 ground degeneracy, weighted by (N-Nex), against the
   scalar formula; full (not beat-averaged) HG tensor at kappa=10,20,40,80,
   fixed s<=4, measuring error against 1/kappa (expected leading O(1/kappa),
   no assertion about uniform long-time accuracy). Sigma=3 tests realistic
   disorder strength relative to Kerr. These are not full vector fibre tests.

The spatial monochromatic model has no temporal grid, window or Raman kernel;
temporal aliasing, a <=3 fs Raman grid, and walk-off are not applicable here.
Mode cutoff is tested explicitly; no full-fibre quantum validation is implied.

## Resource and provenance rules

One compiled numerical process, one CPU thread, at a time. Check memory_pressure
before each launch; require >=35% free. Store only block moments and sparse
checkpoints, <=32768 output positions. Raw files go outside git. Pilot runs
may calibrate implementation and runtime only; their outcomes are labelled.

## Phase-ensemble sampling follow-up (frozen after the initial 200 draws)

The initial 200-draw fixed-length K=6, E=0.75, sigma=0.3, s=2000 ensemble
passes the aggregate moments and covariance signs, but three individual
excited-mode g2 checks fail the original tolerance. Preserve this failure.
Enlarge it to 800 phase draws over eight disorder realizations, still at
s=2000; the first four clusters retain their 50 original launches and add
50 independent ones, and four new clusters have 100 launches each. The
seeds and grouping are explicit in phase_batch.py. This is an investigation
of finite-ensemble scatter, not a newly blind test.

Independently freeze a new held-out K=6, E=0.5 case at sigma=0.3, s=8000,
400 phase draws split across eight new disorder seeds 7401–7408, with
phase seeds 6101–6500. Apply exactly the same moment/sign tolerances as
above, using disorder-cluster jackknife errors; do not fit any prediction.
Record all failed modes. These are classical phase ensembles with no Wigner
noise or ordering correction (n=infinity). Batch propagation uses one common
Brownian path for each realization and retains only final fields and moments.
