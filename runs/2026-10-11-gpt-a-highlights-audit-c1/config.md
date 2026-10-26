# Candidate 1 audit configuration

Agent: gpt-a. Model: gpt-6-astra. Family: gpt. Task: T-20261011-gpt-a-01.
All commands below run from the repository root with `PY=~/agent-work/venv/bin/python`; this is a task-local shell variable. Python calculations use Float64/complex128. Each per-case JSON records the actual grid, step count and parameters; scripts contain the deterministic case lists. Raw outputs stay outside git. No tests below are automatically launched by reading this config.

## Model and cases

`audit.py` implements an independent unitary Fourier split step and its exact tangent/transpose. Soliton units: time T0, distance LD, nonlinearity N^2; propagation length is Z/N. Default input amplitude exp(-t^2/2), window 24. Eigensolver seed 20261011. Refined runs bound the largest linear phase increment by 0.25 in addition to the nonlinear phase step; actual steps are saved. No solver anti-alias window is present.

- `centroid.json`: Gaussian N=3,Z=0.8, chirp 0.7, shift 1.3, normal/anomalous sign and beta3=0 or 0.1. The fifth loss-only row is retained from an initial diagnostic and excluded: it has no compensating vacuum bath. The current script omits that row.
- `refined.json`: Z=0.5,1.5 at N=12,20,32,48; reduced maps at N=192. Small-Z maps: Z=0.01,0.02,0.04,0.08,0.16 at N=400,800.
- `convergence.json`: grid/step refinements and independent quartic/sech centroid cases, fully enumerated by the script.
- `raman.json`: N=10,Z=N*0.7/sqrt(4*N^2*exp(-1.5)-1), T0=1 ps, 300 K, fR=0.18, Blow-Wood tau1=12.2 fs,tau2=32 fs. Only reservoir covariance is added to the Kerr trajectory. The symmetrized coth spectrum is evaluated analytically in frequency; no temporal Raman-kernel sampling is used. The time grid here resolves the retained smooth mode, not the full Raman response. `raman.py` records three grid/step/injection refinements and writes full covariance arrays to the raw directory.

## Reproduction

```sh
$PY runs/2026-10-11-gpt-a-highlights-audit-c1/audit.py --mode centroid --output runs/2026-10-11-gpt-a-highlights-audit-c1/centroid.json
$PY runs/2026-10-11-gpt-a-highlights-audit-c1/refine.py
$PY runs/2026-10-11-gpt-a-highlights-audit-c1/convergence.py
$PY runs/2026-10-11-gpt-a-highlights-audit-c1/raman.py
$PY runs/2026-10-11-gpt-a-highlights-audit-c1/summarize.py
```

`summarize.py` consolidates existing c1-c3 files without launching propagation. Earlier exploratory `scaling.json` and `reduced.json` are preserved, generated with the corresponding `--mode`; report values use the refined files. For exact preservation of failed rows, rerun to a separate output before replacing any registered JSON. The error fits explicitly identify the packet reference Lambda; they are not fits to the same independent finite-N series. `input-manifest.json` pins permitted copied inputs and `searches.json` records bounded independent searches. Literature PDFs are outside git under `2026-10-11-gpt-a-highlights-audit-literature/`.

## Additional limiting check

`limits.py`/`limits.json` independently check the Gaussian Hamiltonian expansion at N=20,80 and Z=0.01,0.02,0.04, with Nt1024,window24,nonlinear phase step0.001 and linear phase guard0.25. The finite-N coefficient includes 1/(2*sqrt(2)*N^2). Run with `$PY runs/2026-10-11-gpt-a-highlights-audit-c1/limits.py`.
