# Configuration

agent: gpt-b; model: gpt-6-astra; family: gpt.

Each TOML in this folder fully specifies a physical case. Times are ps,
lengths m, wavelength nm, and dispersion coefficients ps^n/m. Unless marked
otherwise the launch is a coherent fundamental sech, with
$P_0=|\beta_2|/(\gamma T_0^2)$, effective area $\pi(9.2\,\mu m/2)^2$,
and $n_2=2.3\times10^{-20}$ m²/W. Raman uses the default Agarwal oscillator
with 12.2 fs and 32 fs response times, the declared fraction and temperature.

Run native checks with:

```
JULIA_NUM_THREADS=2 julia --project=solver scripts/soliton_native_check.jl <config.toml>
```

The fixed-step forward RK4IP is Float64; every native adjoint explicitly uses
`adjoint_mode=:discrete_rk4ip` at the identical step. Native Raman cases use
time steps no greater than 3 fs. The source includes the shock multiplier.
The coth helper is the unchanged file
`example_notebooks/raman_bath_spectrum.jl` fetched from private solver commit
`d79f150c4dabac6f461f0302eb06b1ec7900bd4e`; its absolute raw path is in each
configuration. No original-solver repository was modified.

The native check exports the exact sampled deterministic kernel, shock
multiplier and symmetrized bath spectrum. The batch evaluator uses those
exports, not a replacement Raman implementation:

```
OPENBLAS_NUM_THREADS=2 VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 \
~/agent-work/venv/bin/python scripts/soliton_batch_adjoint.py <config.toml> --band 6 --source-stride 4
```

Band is the dimensionless spectral halfwidth around the output mean frequency.
The actual band, source stride and all CLI overrides are recorded in each
batch result. The pilot additionally uses band 8. The fine pilot uses band 6,
twice the temporal samples and forward steps, and source stride 2. Native
checks of the batch masks compare their vacuum and bath terms separately.
Raw queue scripts merely sequence these commands and preserve stdout logs.

Every quartet is for the declared output subspace; enlargement tests determine
whether its Ritz eigenvalues have converged. Binary search is the same
seeded interval/multistart/annealing search described in the Kerr run. A found
mask is not a global-optimality certificate.
