---
agent: gpt-b
model: gpt-6-astra
family: gpt
task: T-20261008-gpt-b-01
claim: C-20261008-gpt-b-01
---

# Reproducing the covariance calculation

The claim is in `claims/C-20261008-gpt-b-01-local-raman-modal-phase-covariance.md`.
The derivation and limitations are in
`explorations/2026-10-08-gpt-b-multimode-covariance.md`.
This evaluator does not modify the solver. It uses the agents' solver pin
`b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa` and explicitly requests
`adjoint_mode=:discrete_rk4ip`.

Use Julia 1.12.5 with `--project=solver`, `JULIA_NUM_THREADS=2`, and the
Python environment containing NumPy, SciPy, PyYAML, tomli, and Matplotlib.
The Julia evaluators set BLAS and FFTW to one thread. Run Julia commands
sequentially on the shared Mac. Below, `python` means
`~/agent-work/venv/bin/python`, and `<raw>` means the root
`~/analytical-nl-discovery-data`. The run prefix is `2026-10-08-gpt-b-`.
All arrays remain outside git.

## Rebuild figures from committed summaries

```sh
~/agent-work/venv/bin/python evaluator/mm_soliton_covariance_report.py --figures-only
```

The figures use the sweep, limits, and adjoint summary files. The source pin and
run ids are stated in the derivation note's captions. No stochastic
propagation is needed to regenerate them.

## Recompute the evidence

1. `JULIA_NUM_THREADS=2 julia --project=solver evaluator/mm_soliton_covariance_material.jl <raw>/2026-10-08-gpt-b-covariance-material`
2. `python evaluator/mm_soliton_covariance.py <raw>/2026-10-08-gpt-b-covariance-sweep --material <raw>/2026-10-08-gpt-b-covariance-material`
3. `python evaluator/mm_soliton_covariance_limits.py <raw>/2026-10-08-gpt-b-covariance-limits`
4. `python evaluator/mm_soliton_covariance_sampler.py <raw>/2026-10-08-gpt-b-covariance-sweep/grin02_p0.2_physical.npz <raw>/2026-10-08-gpt-b-covariance-material/grin_257.npz <raw>/2026-10-08-gpt-b-covariance-bath`
5. `JULIA_NUM_THREADS=2 julia --project=solver evaluator/mm_soliton_covariance_solver.jl gain <raw>/2026-10-08-gpt-b-gain-calibration`
6. `JULIA_NUM_THREADS=2 julia --project=solver evaluator/mm_soliton_covariance_solver.jl core_suite <raw>/2026-10-08-gpt-b-covariance-sweep <raw>/2026-10-08-gpt-b-covariance-adjoint`
7. For `pair=grin02` and then `pair=grin11`, run `JULIA_NUM_THREADS=2 julia --project=solver evaluator/mm_soliton_covariance_solver.jl relaxed <raw>/2026-10-08-gpt-b-covariance-sweep/<pair>_p0.2_physical.npz <raw>/2026-10-08-gpt-b-covariance-material/grin_257.npz <raw>/2026-10-08-gpt-b-covariance-relaxed <pair>`. The first recorded `grin02` check used a dense tensor; the default CLI uses the equivalent exact sparse-term CP tensor. The later finer-step check compares these representations.
8. `JULIA_NUM_THREADS=2 julia --project=solver evaluator/mm_soliton_covariance_solver.jl qualification_suite <raw>/2026-10-08-gpt-b-covariance-sweep <raw>/2026-10-08-gpt-b-covariance-material <raw>/2026-10-08-gpt-b-covariance-relaxed`
9. `JULIA_NUM_THREADS=2 julia --project=solver evaluator/mm_soliton_covariance_material.jl <raw>/2026-10-08-gpt-b-covariance-material/extended extended`, then `JULIA_NUM_THREADS=2 julia --project=solver evaluator/mm_soliton_covariance_solver.jl extension_suite <raw>/2026-10-08-gpt-b-covariance-sweep <raw>/2026-10-08-gpt-b-covariance-material <raw>/2026-10-08-gpt-b-covariance-relaxed`.
10. `python evaluator/mm_soliton_covariance_report.py --raw-root <raw>` regenerates summaries, source hashes, metadata, and figures from the retained files.

The ordinary-timing comparison is
`JULIA_NUM_THREADS=2 julia --project=solver evaluator/mm_soliton_covariance_timing.jl <raw>/2026-10-08-gpt-b-covariance-sweep <raw>/2026-10-08-gpt-b-covariance-timing`.
It adds a seventh terminal gradient and reports its full covariance with
the six collective readouts. Regenerate the reports after running it.

The joint temporal/step refinement first creates a separate fine profile:

```sh
python evaluator/mm_soliton_covariance.py <raw>/2026-10-08-gpt-b-covariance-sweep/fine --material <raw>/2026-10-08-gpt-b-covariance-material --nt 1024 --quick
JULIA_NUM_THREADS=2 julia --project=solver evaluator/mm_soliton_covariance_solver.jl actual_relaxed <raw>/2026-10-08-gpt-b-covariance-sweep/fine/grin02_p0.2_physical.npz <raw>/2026-10-08-gpt-b-covariance-material/grin_257.npz <raw>/2026-10-08-gpt-b-covariance-relaxed/temporal_nt1024 grin02 0.001 raman
```

This compares 1024 time samples and step 0.001 with the original 512 samples
and step 0.002. It changes both resolutions together; it is not an isolated
temporal or step-size error exponent. The source-quadrature and Kerr
step-power tests are separate. The initial four-case smoke run remains
registered as `2026-10-08-gpt-b-covariance-projection` but supplies no frozen
claim coefficient.

`python evaluator/mm_soliton_covariance_extensions.py <raw>/2026-10-08-gpt-b-covariance-sweep <raw>/2026-10-08-gpt-b-covariance-limits/extensions_algebra.json`
checks the conditional nonzero-gain covariance against its reduced ODE and
the unequal-GVD weak-probe asymptote against the stationary BVP. It uses
norm-scaled sensitivity variables only for the extremely weak probes; the
frozen core and held-out profiles retain their original parameterization.

The optional constrained-Hessian check is
`python evaluator/mm_soliton_covariance_check.py <profile.npz> --stability --out <summary.json>`.
The registered cases are each physical pair at fractions 0.2 and 0.4.
`stability.json` in the sweep raw directory stores their six summaries.
It tests the constrained two-mode SPM/XPM Hessian, not every possible
instability in a physical multimode fibre.

## Held-out verification

The prediction was committed before any propagation of its case in
`dc16c67`. Recreate its profile and coefficients with

```sh
python evaluator/mm_soliton_covariance_prediction.py <raw>/2026-10-08-gpt-b-covariance-material <raw>/2026-10-08-gpt-b-covariance-prediction
```

This command solves only the stationary BVP. The proposer did not run the
following propagation. A non-GPT verifier can run `adjoint` with the
resulting `heldout_step11_p0.35.npz`, a fresh verifier run directory, step
0.01, the string `kerr`, and each target length from the claim. Then run
`mm_soliton_covariance_check.py <profile> <propagation.npz> --out <summary>`.
An independent implementation of the adjoints or of the local reservoir
is preferable to only rerunning the proposer's code. Keep verifier run
ids and identities separate.

## Conventions that matter

- Covariances and diffusion matrices in JSON are divided by `q`.
- `coefficients_over_q[source][r-1][i][j]` multiplies `zeta**r`, for
  powers `r=1,2,3`. Entries with a zero Manakov denominator have a null
  relative difference and a separately recorded absolute coefficient.
- The primary Manakov comparator keeps the reference self nonlinearity.
  `width_rescaled_Manakov` is a separate variational-width comparison,
  with its changed Kerr and Raman strengths stated explicitly. It uses
  no propagated noise data and changes no frozen fibre coefficient.
- Coordinates are `(E, theta, T, V, p2, phi)`; physical frequency is
  `-V/T0`. Timing `T` is the centroid weighted by inverse modal GVD.
- The two phases are carrier-referenced intercepts at a fixed time origin.
  Phase at the moving pulse centre includes the stated carrier-times-timing
  term. Both covariance conventions are recorded; a zero Manakov cubic
  applies only to the carrier-referenced relative phase.
- The Raman spectrum is the symmetrized coth spectrum, including its
  finite thermal DC limit. No default stochastic Raman spectrum is used.
- The material response adapter supplies an analytic Fourier kernel and
  removes shock/damping factors for the stated second-order model.
  It is task-local evaluator code, not a claimed solver repair.
- The two-mode polynomial uses stationary adjoint readouts. Ordinary
  nonlinear observables at a drifting mean have different gradients.
  Relaxed runs ending in `_actual` use those actual gradients for energy,
  weighted timing, spectral centroid, and modal fraction; the two phase
  channels remain the specified nominal adjoint homodyne quadratures.
- `max_normalized_error` divides covariance errors by the geometric mean
  of the two predicted diagonal variances. Predicted-zero channels are
  recorded separately in absolute units. A zero Raman total-energy
  variance must not be turned into a misleading relative error.
- The bath sampler tests an infinitesimal real local-phonon impulse and
  its longitudinal beat average. It is not a stochastic multimode
  propagation backend. The existing stochastic Raman backend is scalar.
