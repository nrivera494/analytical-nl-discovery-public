# Candidate 3 audit configuration

Agent: gpt-a. Model: gpt-6-astra. Family: gpt. Task: T-20261011-gpt-a-01.
All commands below run from the repository root with `PY=~/agent-work/venv/bin/python`; this is a task-local shell variable. Python calculations use Float64/complex128. Each per-case JSON records the actual grid, step count and parameters; scripts contain the deterministic case lists. Raw outputs stay outside git. No tests below are automatically launched by reading this config.

## Algebra, parity and polarization

`audit.py algebra`: random generator seed 20261011; 500 eight-dimensional positive parity-symmetric covariances, all 255 nonempty binary masks and 100 positive random weight vectors each. The physical attenuator counterexamples add loss-port vacuum explicitly. The Kerr counterexample uses Phi=5, window=24, grids 256/512/1024, spectral bins +/-1 and transmissions [0.25,0]. Arbitrary-shear tests have dimensions 2,7,19. Polarization: Phi=1,5,20; angles 0,pi/8,pi/4; central difference 1e-6 in four real field coordinates; exact isotropic/strong-birefringence flow.

## Dispersion

`audit.py dispersion` imports the independent c1 map, not proposer code. Shape Gaussian/quartic; Phi=2,5,10,20; y=1e-6,4e-6,1e-5,4e-5,1e-4,0.001,0.01. N=Phi/sqrt(y),Z=sqrt(y),window=16; Nt=4096 for y<=1e-4 and 1024 otherwise. Nonlinear phase step 0.025 plus maximum linear phase step 0.25. Three Nt-doubled/nonlinear-step-halved rows check Gaussian Phi5 at y=1e-6,0.01 and quartic Phi5 at y=1e-6. All 59 rows completed. Eigensolver seed inherited from c1. The script resumes existing rows; use an empty output copy for a full rerun. `dispersion-initial-underresolved.json` preserves a failed initial sweep without the linear-phase guard, excluded from report fits.

## Raman

`raman_band.py` uses the analytic Fourier transform of causal Blow-Wood response (tau1=12.2 fs,tau2=32 fs), fR=0.18 and symmetrized coth noise. Time-grid spacing is at most 2.5 fs, well within the requested 3 fs. The field mean phase, exact shear transpose, band projector, vacuum covariance and Raman covariance are constructed independently. The uncertainty check uses V+i*Omega with shot noise one. The saved field called `centroid` is the uncentered momentum weight omega for comparison with the card's displayed formula; deterministic Raman can shift the mean, so it is not a centered-frequency statistic in that case.

Cases in the two scripts specify T0=200 fs to 5 ps, Phi5/10, temperatures0/77/150/300 K, the packet's adaptive pulse band or explicit Omega_b*T0=30/44, and refinements in dt and window. The converged finite-regime counterexample is T0=200 fs,Phi10,300 K,band30. No solver anti-alias window is applied.

```sh
$PY runs/2026-10-11-gpt-a-highlights-audit-c3/audit.py algebra
$PY runs/2026-10-11-gpt-a-highlights-audit-c3/audit.py dispersion
$PY runs/2026-10-11-gpt-a-highlights-audit-c3/raman_band.py
$PY runs/2026-10-11-gpt-a-highlights-audit-c3/raman_convergence.py
$PY runs/2026-10-11-gpt-a-highlights-audit-c1/summarize.py
```

## Shared momentum specialization

`momentum.py`/`momentum.json` check the shared instantaneous-Kerr momentum identity directly at zero dispersion for Gaussian/quartic/sech pulses, Phi1/5/10,Nt2048,window32. These are signed electronic readouts, not passive masks. Run with `$PY runs/2026-10-11-gpt-a-highlights-audit-c3/momentum.py`.
