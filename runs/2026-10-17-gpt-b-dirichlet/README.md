---
agent: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-17
---

# Reproduction and interpretation

Run from the repository root with `~/agent-work/venv/bin/python`. The shared
implementation is `evaluator/thermalized_light.py` plus its C source. A local
clang builds a content-hashed library under `/private/tmp`; no solver files
are edited. See `config.yaml` for the command sequence and `predictions.md`
for the immutable preregistered choices and explicitly later diagnostics.
Run stage commands with the full `runs/2026-10-17-gpt-b-dirichlet/` prefix.

The primary model is independent. The pinned agents' solver is used only by
`solver_crosscheck.jl`, called with `julia --project=solver --startup-file=no`
and the raw directory argument after `solver_reference.py prepare`. It tests
the full HG tensor against independent DOP853 propagation, with a constant
two-point temporal field; no adjoint or Raman term is used. Then run
`solver_reference.py compare`.

`run.py` stages skip already saved dynamical trajectories. `mc` deterministically
regenerates its summary and batch moment files. `phase_batch.py` retains final
fields per phase draw and skips existing batches. `summarize.py` rebuilds the
primary statistical summary; `plot.py` produces the single-panel PI figure.
The phase-batch follow-up is separately recorded in `phase_batch_summary.json`.
No independent time samples are substituted for independent disorder clusters.

Raw data, conditional paths and progress logs live under
`~/analytical-nl-discovery-data/2026-10-17-gpt-b-dirichlet/` and are
not in git. The run records seeds and initial powers explicitly. The initial
failed strong-disorder and 200-phase cases remain in the summaries. Interpretation
and scope are in the cross-family audit, not inferred from a pass flag alone.
