---
agent: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-17
---

# Reproduction and frozen references

Use the shared independent evaluator from the repository root, with the full
run-directory prefix on scripts. `config.yaml` lists the stages. `shell.py`
creates the direct reference sample and refuses to overwrite it. `conditioned.py`
and `conditioned.py --refine` generate the kernel-conditioned MCMC estimates.
`collect_predictions.py` checks that the frozen final file selects the documented
refined cases and leaves all others unchanged. Numerical predictions were
committed before the first deterministic trajectory; do not silently replace
them with values fitted to the simulation.

`run.py deterministic`, `convergence` and `memory` are the original dynamical
stages. `long_time.py` is the explicitly post-initial-data length diagnostic.
`sector.py shell` computes the reflection-sector predictions; those were
committed before `sector.py dynamics`. The latter compares an exact canonical
symmetry reduction with explicitly perturbed full-space launches. It does not
project or renormalize trajectories. The original nominally symmetric full-space
runs are retained and diagnosed for roundoff-amplified symmetry leakage.

`summarize.py` reports both endpoint comparisons and time-window stability.
For long trajectories its uncertainty diagnostic includes block lengths through
40000, to expose slow correlations. `plot.py` uses long trajectories and the
controlled 1e-4 phase perturbation for aligned launches; reference curves remain
the frozen full-shell predictions. The perturbation's actual invariant changes
are recorded. Figures and pass flags must be read with the audit's caveats.

Raw arrays are under
`~/analytical-nl-discovery-data/2026-10-17-gpt-b-gge/`.
The problem card is not edited by this verification.

`resolution.py` is the final bounded post-audit diagnostic. Run `shell`,
commit its numerical references, then run `dynamics`, `memory`, and `summarize`
serially. The plan and numerical-reference commit hashes are in `meta.yaml`.
The summary explicitly distinguishes compatibility from passing every frozen
sampler, precision, time-window, invariant and paired-step gate. Its `complete`
flag requires all planned trajectories; plots use the new endpoints only
after that flag is true. The figure keeps the original frozen finite-width
GGE curves, so later reference refinement does not erase an earlier mismatch.

After the first long-sector endpoint mismatch, one extra `sector_step` stage
was frozen before execution. It repeats only the exact reflection sector at
step 0.005, after the original disorder ensemble. The final complete flag
also requires that check; `base_plan_complete` records the original plan
separately. This diagnostic is not a new blind holdout.
