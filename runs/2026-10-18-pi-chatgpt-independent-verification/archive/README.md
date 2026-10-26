# Independent verification of nonlinear-fiber claims

Prepared 18 October 2026 by ChatGPT (GPT-6 Astra Pro), with parallel independent derivation and implementation tasks.

Repository examined: <https://github.com/nrivera494/analytical-nl-discovery>, pinned commit `970bfe756b131094872de351ff91ab46a537d9b2`.

The main deliverable is `report/independent_verification_report.pdf`; the LaTeX source is in the same directory. The calculations in this archive were written independently for the verification and do not import a repository solver. `repository_inventory.json` records the inspected source paths and hashes. Original repository files are not redistributed.

## Main results

1. **Similariton exponents survive within leading hydrodynamics.** Fixed low-order shape modes have photon-normalized density and phase **variance envelopes** proportional to `G^(1/3)` and `G^(5/3)`. The rms powers are `G^(1/6)` and `G^(5/6)`. These modal variables require their actual quantum metric and edge regularization; reduced intensity suppression relative to a linear amplifier is not itself squeezing below vacuum.
2. **The specified finite spectral covariance and phase-energy deficit have `G^(-2/3)` envelopes.** Logarithmic-gain oscillations prevent interpreting every rescaled curve as convergence to a constant. Complete-field finite-gain checks support the leading mechanism, but do not prove the sharp-edge uniform error bounds.
3. **Two corrections are necessary.** The matched-LO phase variance has power `G^(7/3)/epsilon^2` at fixed parameters, not `G/epsilon^2`. Full amplifier-added noise does not forbid all Kerr squeezing: an explicitly computed short-distance example has matched-LO minimum `0.8964864655` in vacuum units. Within the reduced large-gain model, that matched mode instead eventually has minimum variance with envelope `G^(1/3)`.
4. **The weak normal-dispersion law and its coefficient are independently reproduced.** With `Phi=gamma*P0*L`, `y=Phi*L/LD` and a Gaussian intensity `exp(-(t/T0)^2)`, the relative covariance excess is asymptotic to `sqrt(2/3)*Phi/sqrt(1+Phi^2)*sqrt(y)`. The mode-intensity rms width is `T0*(y/24)^(1/4)` for every fixed positive Phi. Quartic and sextic maxima reproduce excess powers `2/3` and `3/4`.
5. **A new local second-order coefficient refines the empirical fit.** The full rescaled mean/tangent expansion gives an explicit `c2(Phi)`, tending to `2*sqrt(6)/5` at large Phi. This is a formal local expansion with numerical support, not a proved global uniform remainder theorem.
6. **Strong-dispersion `Lambda(Z)/N^2` survives with conditions.** A finite-dimensional symplectic lemma proves the law under regular block limits. Independent hydrodynamics and full NLSE reproduce it before breaking; converged full-NLSE results support it at a tested postbreaking distance. The smooth Euler tangent map cannot simply be continued through wave breaking.

`lambda_min` denotes the optimum arbitrary-mode **homodyne quadrature variance**. It bounds passive-filter photon-counting Fano factors; equality needs a separate detection-mode construction. At zero dispersion for an isolated Gaussian peak it is an unattained continuum infimum. Fixed optical bandwidth, fixed grid, nonzero material response, and finite brightness affect the limiting problem.

## Contents

| Directory | Independent method and evidence |
|---|---|
| `similariton` | Real-space finite-volume hydrodynamic operator, covariance Lyapunov integration, exact lens-coordinate full NLSE tangent/adjoint with both vacuum and ASE quadratures; detailed notes and raw convergence records |
| `weak` | Eighth-order finite differences in time and DOP853 propagation of the mean and exact tangent; Gaussian, quartic and sextic sweeps; full/support/grid/window/tolerance checks; CSV and figure |
| `weak_theory` | Direct rescaled optical-generator derivation, effective oscillator calculations, and symbolic time-ordered second-order coefficient |
| `strong` | Fourth-order symplectic Fourier flow with exact tangent/adjoint; full-grid covariance, direct hydrodynamics, passive readout checks, and an independent crosscheck of the weak result |
| `report` | Integrated technical report, LaTeX source, and build instructions |

The per-directory READMEs give exact commands. Files containing results are retained so that the figures and tables can be regenerated without rerunning propagation. Original data and any diagnosed numerical artifacts are labeled explicitly; they are not silently replaced by theoretical predictions.

## Installation and quick reproduction

The recorded environment used Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 and Matplotlib 3.10.8. The pinned dependencies require Python 3.11 or later. `environment.json` also records the symbolic dependency. A normal environment with these libraries is sufficient; no remote application or repository access is needed to run the calculations.

From the extracted `verification` directory:

```bash
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python strong/verify_weak_cross.py
OPENBLAS_NUM_THREADS=1 python similariton/reproduce.py --suite quick
python weak_theory/effective_oscillator.py
python weak_theory/second_order_symbolic.py
```

The first propagation should give `lambda_min` approximately `0.02654003090685` for `Phi=3, y=1e-4`; the short amplifier should give `0.89648647`. The similariton quick suite writes to a separate `similariton/reproduced` directory. The other commands regenerate their named result files, so copy the archive before rerunning if you want to retain the exact original byte-level hashes.

An independent finite-difference check, writing new files, is:

```bash
OPENBLAS_NUM_THREADS=1 python weak/verify_weak.py --phi 3 --y 1e-4 --n 1024 --support .4 --rtol 2e-11 --output weak_cross_fd.json --save-mode weak_cross_fd_mode.npz
```

The complete weak suite takes several minutes on the recorded CPU; the high-resolution full amplifier suites take longer. The per-directory READMEs list the complete settings. Runtime is not a correctness criterion.

## Regenerate summaries and figures from stored data

```bash
MPLCONFIGDIR=/tmp/fiber-verification-mpl python weak/build_summary.py
MPLCONFIGDIR=/tmp/fiber-verification-mpl python strong/build_summary.py
python similariton/analyze_results.py
MPLCONFIGDIR=/tmp/fiber-verification-mpl python similariton/build_figures.py
```

The readout scripts use their own file locations and can be run from any working directory. `report/BUILD.md` gives the PDF build command. SHA-256 hashes for archive files are in `SHA256SUMS.txt`. Hashes describe supplied files, not hypothetical future reruns; small rounding and timing differences are expected across platforms.

## Interpreting evidence and limits

The report distinguishes exact reduced-model proofs, formal local asymptotics, numerical evidence, and unverified global hypotheses. Symplectic diagnostics establish a physically consistent finite-grid lossless tangent map; they do not prove continuum convergence. A restricted-input tangent computation gives an upper estimate via reciprocal largest singular value and is not a covariance with missing vacuum modes. The full amplifier calculations include reservoir commutator restoration and both reservoir quadratures.

Some raw finite-volume JSON files use `NaN` for quantities undefined at zero distance or at an unchirped stationary-phase singularity. Python's JSON parser accepts these values; they are excluded from fitted results. All quoted fits are deterministic descriptive fits, not statistical confidence intervals.

The literature assessment is a bounded search with access limitations identified in the report. The strongest candidate novelty is the explicit singular weak-dispersion asymptotic and localization coefficient. The background similariton, classical attraction, amplifier quantum limits, covariance optimization, normal-dispersion squeezing, and harmonic approximation are established ingredients.
