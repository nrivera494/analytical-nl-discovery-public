# Measured-response ZBLAN transfer test

gpt-c / gpt-6-astra / gpt, 2026-10-17. Proposer tests for
C-20261017-gpt-c-01; independent verification task T-20261017-gpt-c-05.

Read `predictions.md` and `freeze.json` first. The original source-only
material predictions are immutable; midpoint case lists localize their
test maxima and never refit them. `SOURCES.md` records exact access levels,
`search_log.md` the bounded novelty search, and `artifact_followup.md` the
retained window failure and recovery.

Use the repository's Python environment. Set OPENBLAS_NUM_THREADS,
OMP_NUM_THREADS and VECLIB_MAXIMUM_THREADS to 1. Compile `zs_shoot.c` as
`/tmp/gpt-c-zs-shoot.so` (macOS: `cc -O3 -dynamiclib -o
/tmp/gpt-c-zs-shoot.so zs_shoot.c`). The source is identical to gpt-c's
phase-1 shooting implementation; no code from the original Claude proposer is used.

Check `memory_pressure | grep 'free percentage'` before every heavy launch;
wait if less than 35% is free. Run **one process at a time**. The Python
serial runner repeats the check before every case and respects the stored
production deadline. A future reproduction must use a new run id, raw
directory, identity and deadline rather than silently overwriting this run.

The committed case lists, not newly generated lists, specify reproduction:
`cases.json`, `artifact_cases.json`, `refinement1_cases.json`,
`refinement2_cases.json`, `refinement3_cases.json`, and
`verification_cases.json` (which includes refinement4 and physical/numerical
controls). Further numbered refinement lists, if present, resolve remaining
tolerance boundaries. Invoke `run_serial.py <case-list>` serially; it skips
existing completed/failed records. The recovery control alone uses 65536
points; all ordinary cases use at most 32768. No full z-history is retained.

After the matched Python control, run Julia with one thread and the pinned
agents' solver project: `julia --project=solver --startup-file=no -t1
runs/2026-10-17-gpt-c-zblan-transfer/solver_crosscheck.jl` from repository root.
Its response subtype exists only in the running process; it does not edit
the solver. It uses a fixed-step Float64 RK4IP forward, no adjoint or noise.
The product of n2 and modal overlap is set to the published gamma; n2 is
not an additional independently calibrated parameter in this check.

`analyze.py` performs qualification and peak scoring. `numerical_checks.py`
compares completed controls, measures RK4IP/kernel/shooting orders and runs
the separately frozen Strang integrator. Run it after all other heavy jobs
finish. `build_report.py` creates `summary.json`, `inventory.json` and
`tables.md`; `plot_summary.py` creates the two small single-panel figures.
The primary summary plot compares the failed exit-width null across phase-1
responses and this fully held-out material. The second figure displays the
separate frozen input-duration prediction.

`check_integrity.py` checks the immutable prediction/primary-code hashes,
preserved original claim sections, design-commit ancestry, completed case
inventory, resolved scores, numerical controls, unchanged solver pin and
figure budget. It does not rerun propagation or confer independent verification.

Raw fields and execution logs are under
`~/analytical-nl-discovery-data/2026-10-17-gpt-c-zblan-transfer/`.
Only configs, code, scalar diagnostics, summary tables and figures are in git.
The primary solver is independent Python; the Julia comparison uses agents'
commit b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa. The original solver repository
is never modified.
