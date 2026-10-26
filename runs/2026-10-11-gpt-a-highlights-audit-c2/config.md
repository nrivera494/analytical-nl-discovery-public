# Candidate 2 audit configuration

Agent: gpt-a. Model: gpt-6-astra. Family: gpt. Task: T-20261011-gpt-a-01.
All commands below run from the repository root with `PY=~/agent-work/venv/bin/python`; this is a task-local shell variable. Python calculations use Float64/complex128. Each per-case JSON records the actual grid, step count and parameters; scripts contain the deterministic case lists. Raw outputs stay outside git. No tests below are automatically launched by reading this config.

## Independent implementation

`gain.py` implements scalar normal-dispersion gain-NLSE propagation, exact discrete tangent transpose and trapezoidal integration of continuous white ASE. The frequency sign is minus numpy's FFT frequency. Covariance blocks are input-photon-normalized; the total is C_in+(2*nsp-1)*C_ASE. Flat unsaturated gain, no Raman/TOD/self-steepening. For finite gain curvature, the positive local ASE strength follows the magnitude of the gain profile; the audit claims only a local robustness check on this deliberately relaxed model.

P8: beta2=0.025 ps^2/m, gamma=0.005 W^-1 m^-1, g=1.9/m, L=3.2 m, Gaussian intensity FWHM 0.25 ps, energy 10 pJ, Nt=2048, window=12 ps, 4000 steps. `p8_lin` sets gamma=0. Dimensionless similariton cases use beta2=gamma=T0=1, P0=eps^-2, g=Gamma/eps, L=U/g. Gamma=sqrt(18) except heldout Gamma=1; launch chirp q=1/3 for asym, zero for main/heldout. Smoothed intensity is delta*log(1+exp((1-t^2)/delta)); delta=0.5*eps or 0.5*eps^(2/3). The scripts choose resolved grids/windows and bound linear step phase; every actual choice is saved.

```sh
$PY runs/2026-10-11-gpt-a-highlights-audit-c2/gain.py closed
$PY runs/2026-10-11-gpt-a-highlights-audit-c2/gain.py full --case p8 --output runs/2026-10-11-gpt-a-highlights-audit-c2/p8.json
$PY runs/2026-10-11-gpt-a-highlights-audit-c2/gain.py full --case p8_lin --output runs/2026-10-11-gpt-a-highlights-audit-c2/p8_lin.json
$PY runs/2026-10-11-gpt-a-highlights-audit-c2/sweep.py
$PY runs/2026-10-11-gpt-a-highlights-audit-c2/convergence.py
```

`asym_e05_u4.json` is an earlier eps=0.05,U=4 asymptotic-seed diagnostic with default e1 edge. `closed.json` has direct quadrature of the closed forms, transient width ODE and a five-mode Legendre stochastic covariance; it is not a full-NLSE large-gain computation. Modes 0..4, Gauss-Legendre quadrature order 80, solve_ivp tolerances stated in the script. These runs are deterministic.

## Solver reproductions

The unchanged Claude-family scripts and source attribution are under `reproduced/`. The audit reran them with solver b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa from FastDifferentiableMMNLO-agents, Float64, JULIA_NUM_THREADS=2. The centroid check explicitly sets adjoint_mode=:discrete_rk4ip and the same fixed forward/adjoint step. The large artificial carrier omega0=1e8 suppresses the solver's self-steepening; compare after N0 normalization, not its artificial absolute photon number. Never interpret this carrier as the physical P8 experiment.

```sh
JULIA_NUM_THREADS=2 julia --project=solver runs/2026-10-11-gpt-a-highlights-audit-c2/reproduced/2026-10-10-claude-interactive.2-moment-noise/contract.jl p8 0.05 6.08 TW runs/2026-10-11-gpt-a-highlights-audit-c2/p8_solver.json
JULIA_NUM_THREADS=2 julia --project=solver runs/2026-10-11-gpt-a-highlights-audit-c2/reproduced/2026-10-10-claude-interactive.2-shape-modes/shapemodes.jl 0.05 6 0.0001 ~/analytical-nl-discovery-data/2026-10-11-gpt-a-highlights-audit-c2/c2-shape-e05-u6.json
$PY runs/2026-10-11-gpt-a-highlights-audit-c2/analyze_shape.py
```

Shape reproduction: paired +/- phase/intensity perturbations, l=0..4, 61 output planes, eps=0.05,U=6,eta=1e-4,Nt=8192,nsteps=11370. `analyze_shape.py` independently computes hydrodynamic transfer and late-time rates. The source measurement scripts were permitted same-family validation material; independent Python propagation is the distinct implementation. Early numpy matrix-product warnings did not yield nonfinite saved entries; later equivalent explicit-einsum contractions and held-out convergence checks remove that diagnostic concern.
