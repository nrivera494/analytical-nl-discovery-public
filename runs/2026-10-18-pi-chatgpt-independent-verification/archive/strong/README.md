# Strong normal-dispersion verification: reproducibility

Repository inspected: `nrivera494/analytical-nl-discovery`, snapshot commit `970bfe756b131094872de351ff91ab46a537d9b2`. No repository files were edited or executed as the independent solver.

Read `strong_report.md` for derivations, results, uncertainty, postbreaking scope and primary-literature access levels.

## Requirements

Python 3.11 or later; tested with Python 3.12.14. Recorded library versions: NumPy 2.3.5; SciPy 1.17.0. All numerical runs used `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`.

## Scripts

- `verify_strong.py`: fourth-order symplectic Fourier split flow plus exact tangent/adjoint, complete quadrature covariance; all input grid modes retained. `--dense` additionally forms the complete tangent matrix and computes the exact global-phase-hyperplane projection. `lambda_min` from reciprocal anti-squeezed eigenvalues is independently checked by direct covariance Rayleigh quotient.
- `verify_hydro.py`: independent epsilon=0 mean and exact tangent shallow-water equations, DOP853, complete odd Fourier grid. A window at least 32 additionally reports a projection of the resulting exact map onto 80 orthonormal Hermite functions, isolating the repository's basis bias.
- `verify_weak_cross.py`: quick crosscheck at Phi=3, y=1e-4. Only the relevant covariance maximum is computed, avoiding the much harder nearly-degenerate amplitude-block diagnostic.
- `build_summary.py`: collates the recorded JSON data into `summary.json` and produces `strong_comparison.png` / `.pdf` (Matplotlib optional). The figure's postbreaking horizontal reference is explicitly a repository finite-N comparison.

## Representative commands

Run from this directory:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_strong.py --N 10 --Z 0.75 --n 256 --steps 300 --dense --out N10_Z075_n256_s300.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_strong.py --N 20 --Z 0.75 --n 256 --steps 300 --out N20_Z075_n256_s300.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_strong.py --N 40 --Z 0.75 --n 512 --steps 600 --out N40_Z075_n512_s600.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_strong.py --N 10 --Z 1.5 --n 256 --steps 300 --dense --out N10_Z150_n256_s300.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_strong.py --N 20 --Z 1.5 --n 512 --steps 600 --out N20_Z150_n512_s600.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_strong.py --N 40 --Z 1.5 --n 1024 --steps 1200 --out N40_Z150_n1024_s1200.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_strong.py --N 20 --Z 1.5 --n 1024 --window 16 --steps 1200 --out N20_Z150_n1024_w16_s1200.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_strong.py --N 20 --Z 1.5 --n 1024 --window 32 --steps 1200 --out N20_Z150_n1024_w32_s1200.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_hydro.py --n 225 --out hydro_n225.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_hydro.py --n 441 --out hydro_n441.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_weak_cross.py
```

To reproduce the isolated Hermite-bias check:

```python
import json
from pathlib import Path
from verify_hydro import run
r = run(n=441, window=32.0, targets=(0.1, 0.2, 0.3))
Path('hydro_n441_w32_basis.json').write_text(json.dumps(r, indent=2))
```

The JSON files contain parameters, minima, reduced coefficients, parity, and diagnostics. Companion `.npz` files contain temporal grids, complex means, the first three squeezed physical-quadrature vectors and top input amplitude modes of the reduced block. Euclidean normalization on a uniform grid is equivalent to L2 normalization after a common sqrt(dt) factor.

One redundant attempt to use the full strong diagnostic for the weak crosscheck was interrupted because its nearly-unit amplitude-block eigenvalue was slow to converge. No result from that interrupted diagnostic is used. The dedicated weak crosscheck completed independently and is the retained JSON result.

## Interpretation

The minimum covariance eigenvalues have strong convergence evidence. After breaking, finite-N reduced C and A block extrema are more cutoff-sensitive than the covariance minimum. The epsilon=0 coefficients are smooth prebreaking hydrodynamic coefficients. The postbreaking value around 0.3625 is a finite-N NLSE asymptotic comparison, not a globally defined classical shallow-water operator.
