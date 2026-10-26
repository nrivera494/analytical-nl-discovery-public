# Independent weak-normal-dispersion verification

These calculations test claim C-20261010-claude-a-01 in `nrivera494/analytical-nl-discovery`, snapshot commit `970bfe756b131094872de351ff91ab46a537d9b2`. The propagation code was independently written for this verification. It imports no solver or numerical output from that repository.

## Results and files

`weak_verification.pdf` is the vector figure; `weak_verification.png` is its raster version. The four panels compare the covariance excess, its ratio to the leading prediction, temporal localization, and representative Gaussian mode shapes. `numerical_results.csv` contains all 31 recorded runs. `summary.json` contains deterministic fitted exponents, source hashes, convergence comparisons, and stringent second-order checks. The source records are `weak_results.json`, `second_order_results.json`, and `second_order_phi10.json`; saved `mode_*.npz` files contain the corresponding output mode arrays.

The detailed independent derivation, including its mathematical limits and detector qualifications, is in `../weak_theory/weak_dispersion_derivation.md`. The scripts in that directory independently compute the effective oscillator constants and the Gaussian second-order coefficient. No vendored dependencies are needed or intended for distribution.

Fits below use the three points `y = 1e-6, 1e-5, 1e-4`. They are descriptive regressions of deterministic calculations, not statistical estimates with confidence intervals.

| Input intensity | Phi | Excess exponent, measured | Predicted | Mode rms exponent, measured | Predicted |
|---|---:|---:|---:|---:|---:|
| `exp(-x^2)` | 3 | 0.501914 | 1/2 | 0.250240 | 1/4 |
| `exp(-x^2)` | 10 | 0.501899 | 1/2 | 0.250148 | 1/4 |
| `exp(-x^4)` | 3 | 0.667219 | 2/3 | 0.166609 | 1/6 |
| `exp(-x^6)` | 3 | 0.750317 | 3/4 | 0.124926 | 1/8 |

At `y = 1e-6`, the excess divided by the independently predicted leading coefficient is 1.000990 and 1.000977 for the two Gaussian series, 1.000137 for the quartic maximum, and 1.000089 for the sextic maximum. For `y <= 1e-4`, the largest relative rms-width deviation in any of these series is about 0.122%. The systematic finite-y excess is consistent with higher-order terms; it is not evidence of a different leading exponent.

## Model and normalization

Write `s=z/L`, `x=t/T0`, `delta=beta2*L/T0^2>0`, `Phi=gamma*P0*L`, and `y=Phi*delta`. The propagation equation and initial field are

```text
du/ds = -i delta/2 d²u/dx² + i Phi |u|² u,
u(0,x) = exp(-x^(2m)/2).
```

Thus the stated Gaussian is an **intensity** profile `exp(-x^2)`. The complex tangent field obeys

```text
dv/ds = -i delta/2 d²v/dx² + i Phi (2 |u|² v + u² v*).
```

Both equations are propagated to `s=1`. The shot-noise quadrature covariance is the identity. The dispersionless covariance infimum at the pulse maximum is evaluated stably as

```text
lambda0 = 1 / (sqrt(1+Phi²) + Phi)².
```

For a Gaussian and fixed positive Phi, the leading prediction is

```text
lambda/lambda0 - 1 ~ sqrt(2/3) Phi/sqrt(1+Phi²) sqrt(y),
rms(mode intensity)/T0 ~ (y/24)^(1/4).
```

For `m=2,3`, the leading coefficient and rms constant come from the independently solved scalar oscillator `-d²/dq² + q^(2m)` in `../weak_theory/oscillator_constants.json`. The summary preserves the original solver's prediction column and separately supplies `theory_prediction` from the more accurate Richardson-extrapolated constants.

## Independent numerical method

`verify_weak.py` discretizes the second derivative with the centered eighth-order finite-difference stencil on a periodic window `[-half_window, half_window)`. Adaptive DOP853 integration evolves the mean field and then its real tangent map, using a dense interpolant for the mean. The mean integration uses relative tolerance `rtol/5`; the tangent uses `rtol`. This method is distinct from Fourier split-step propagation.

All output grid coordinates are retained. By default, the input tangent columns are restricted to both quadratures in `abs(x)<=support`; `--full` retains all input columns. If `S` denotes the full finite-grid symplectic tangent map and `P` is the selected input embedding, the code constructs `T=S P` and reports

```text
lambda_min_upper = 1 / largest_eigenvalue(T.T @ T).
```

For the full symplectic map, reciprocity gives `lambda_min(S S.T)=1/||S||²`. Since `||S P||<=||S||`, the restricted estimate is a **variational upper estimate** of the full finite-grid minimum covariance eigenvalue. It is not a lower bound. The rectangular `T T.T` is not being interpreted as a physical covariance after removal of unused vacuum inputs. The restriction only reduces the search space for the largest singular value.

The stored output mode is `J` times the normalized largest output singular vector. This is exactly an optimal squeezed mode for the full symplectic map and is an approximation for restricted input columns. Support convergence is consequently relevant to mode shapes as well as to eigenvalues. Uniform grid-cell normalization makes the Euclidean covariance convention equivalent to normalized temporal bins; the uniform factor `dx` cancels in the reported rms width.

## Reproduce from the supplied results

With NumPy and Matplotlib installed, regenerate the summary, CSV, and both figures without running any propagation:

```bash
cd verification/weak
MPLCONFIGDIR=/tmp/fiber-audit-mpl python build_summary.py
```

This reads the existing numerical records, saved mode arrays, and the two supplied theory JSON files. It does not import or run `verify_weak.py`.

## Reproduce all calculations

The recorded propagation environment used NumPy 2.3.5 and SciPy 1.17.0. The plotting environment used Matplotlib 3.10.8. A Python environment with NumPy, SciPy, Matplotlib, and SymPy is sufficient; no repository package is required. For example, install them in a virtual environment:

```bash
python -m pip install numpy scipy matplotlib sympy
```

Then, from `verification/weak`, run:

```bash
OPENBLAS_NUM_THREADS=1 python run_suite.py
OPENBLAS_NUM_THREADS=1 python run_second_order.py
OPENBLAS_NUM_THREADS=1 python verify_weak.py --phi 10 --y 1e-6 --n 3072 --support .24 --rtol 2e-13 --output second_order_phi10.json
python ../weak_theory/effective_oscillator.py
python ../weak_theory/second_order_symbolic.py
MPLCONFIGDIR=/tmp/fiber-audit-mpl python build_summary.py
```

The first command runs 27 cases and overwrites `weak_results.json` after every completed case; it also recreates the Gaussian mode files. `run_second_order.py` records three more stringent cases. The standalone command generates the fourth stringent case. The two theory scripts regenerate the numerical oscillator constants and symbolic second-order calculation. `OPENBLAS_NUM_THREADS=1` makes the many narrow tangent/Gram computations efficient and reproducible; hardware and library versions can still alter runtimes and final rounding.

A single representative case can be reproduced without the full suite:

```bash
OPENBLAS_NUM_THREADS=1 python verify_weak.py --phi 3 --y 1e-4 --n 1024 --support .4 --rtol 2e-11 --output case.json --save-mode case_mode.npz
```

A full-map reciprocity check on the finite grid is:

```bash
OPENBLAS_NUM_THREADS=1 python verify_weak.py --phi 3 --y 1e-3 --n 512 --full --rtol 2e-11 --output full_check.json
```

## What the convergence checks establish

The supplied suite resolves several concrete numerical risks:

- Refining the most localized Gaussian case at `Phi=3, y=1e-6` from 2048 to 3072 points changes the estimated eigenvalue by about `1.52e-10` relative.
- Increasing the central input half-support from 0.6 to 1.2 at `Phi=3, y=1e-3, n=512` changes the eigenvalue by about `6.64e-13` relative. Using all input columns on the same grid changes it by about `1.21e-12` relative. The small reversal of ideal variational monotonicity is at the integration/rounding scale.
- Enlarging the temporal window from width 8 to width 12 while retaining the same grid spacing changes the representative eigenvalue by about `3.79e-12` relative. This comparison also uses a larger, independently converged input support.
- Tightening the tangent tolerance at `Phi=10, y=1e-4` while widening its already adequate input support changes the eigenvalue by about `3.80e-10` relative.
- Across all stored cases, the maximum entrywise error in `T.T J T = J_selected` is about `1.04e-10`, and the maximum mean-energy relative error is about `2.89e-12`. The full-map direct minimum and reciprocal maximum agree to about `4.78e-14` relative in the representative full-map case.

These checks support the reported leading asymptotics in the sampled parameter ranges. They are not interval-certified error bounds or a proof for every gain, dispersion, grid, support, or temporal window. The flat-maximum series have a less restrictive localization length than the Gaussian series, but do not each have a dedicated full-map refinement ladder. A symplectic defect alone cannot establish continuum convergence: a spatially truncated model can be exactly symplectic and still omit the optimum mode.

## Second-order refinement and its precision limit

Let `A=sqrt(2/3)*Phi/sqrt(1+Phi²)`. The independent local Duhamel calculation predicts

```text
lambda/lambda0 - 1 = A sqrt(y) [1 + c2(Phi) sqrt(y) + O(y)],
c2(Phi) = sqrt(6) (45 + 81 Phi² + 56 Phi⁴ + 40 Phi³ sqrt(1+Phi²))
          / (240 Phi² (1+Phi²)).
```

This is a formal local refinement independently derived during the verification, not an inherited repository result or a proved global remainder theorem. The tight-tolerance runs support its magnitude and dependence on Phi. For example, at `Phi=3, y=1e-7`, the extracted coefficient is approximately 0.989433 versus the predicted 0.989465. At `Phi=10, y=1e-6`, it is approximately 0.979976 versus 0.980342. Extraction subtracts the much larger dispersionless anchor and leading square-root term; errors in the eigenvalue are therefore amplified when divided by `y`. The `Phi=10, y=1e-7` value is not more accurate than the `y=1e-6` value, so decreasing y alone does not constitute a useful precision check for the second-order coefficient.

## Mathematical and physical scope

The scalar oscillator reduction establishes its own ground-state coefficient and localization law exactly. The local optical expansion constructs corresponding asymptotic quasimodes. A full continuum theorem needs a matching lower bound excluding competing modes at all frequencies; the numerical calculations do not replace that proof.

The observable here is the infimum of the full quadrature covariance over arbitrary homodyne modes. It is a lower bound for more restricted detector families. It is not, without a separate detector optimization, the optimal binary spectral-filter photon-counting Fano factor. Filter loss must include its vacuum input, and an experimental mode must be accessible to its local oscillator or detection optics.

The asymptotic statement takes `y -> 0` at fixed positive Phi while resolving a mode whose optical bandwidth grows as `y^(-1/4)` for a Gaussian. A fixed optical bandwidth, fixed time grid, joint `Phi -> 0` limit, finite response time, or quantum depletion can change the asymptotic regime. The instantaneous Kerr model has an ultraviolet difficulty in its dispersionless all-mode limit. The results establish the ideal lossless Bogoliubov-model law and should not be read as an unrestricted statement about an arbitrary real fiber or detector.
