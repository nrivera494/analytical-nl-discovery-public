# Evaluator

Not implemented yet (task T-0003). This file is the contract.

A claim supplies a prediction: a function from physical parameters to the quantity claimed (a field profile, a scalar, a spectrum, a distribution). The evaluator runs a cascade, cheapest first, and stops at the first failure.

| Stage | Check | Cost |
|---|---|---|
| 1 | Units and dimensional consistency | none |
| 2 | Known limits and symmetries listed in the claim | none |
| 3 | Symbolic residual in the reduced model, where applicable | seconds |
| 4 | 1D solver, core regime | seconds to minutes |
| 5 | Error-scaling: sweep the small parameter, fit the exponent | minutes |
| 6 | Held-out region fixed in the claim before running | minutes |
| 7 | Convergence: window, step, mode count | minutes |
| 8 | Modal solver against full-field solver, or relaxed assumption | minutes to hours |
| 9 | Adjoint consistency: claimed parameter sensitivities against solver gradients | minutes |

Output: one `runs/` folder per stage with a `summary.json` containing pass or fail, the metric, and the tolerance used. Tolerances live in the claim, fixed before the run.

Known ways an evaluator gets fooled, each needing a guard: reflections from the time window that mimic a stationary state; step-size-induced attractors; truncated mode bases; metrics that reward matching at the fitted points only; per-instance fitted constants. The solver is FastDifferentiableMMNLO (Julia), held as the submodule `solver/` and pinned by commit in every `meta.yaml`; see `docs/SOLVER.md`.
