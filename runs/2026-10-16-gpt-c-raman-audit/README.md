Agent: gpt-c. Model: gpt-6-astra. Family: gpt.

Independent verification of C-20261016-claude-a-02. The audit report is
`claims/notes/audit-2026-10-16-gpt-c-C-20261016-claude-a-02.md`.

`independent.py` and `zs_shoot.c` contain the independent forward model and
scattering measurement. `run_audit.py` executes case lists sequentially and
checks memory pressure before each case. Each completed checkpoint saves a
field outside git and a pulse census in its case JSON. `summary.json` retains
quality exclusions; it is not a table of successful points only. The precise
configurations, distances, meshes and integration tolerances are in the case
files. No proposer script was read to implement these checks.

The most useful entry points are `frozen_checks.json`, `quality_metrics.json`,
`extraction_checks.json`, `shock_measurement.json`, `regime_metrics.json` and
`library_comparison.json`. Read their case names alongside the per-case
reports. The plots show fixed-distance measurements and do not declare all
short-pulse points saturated.

`execution_inventory.json` distinguishes completed, stopped and failed cases
from registered configurations that were not run. `post_controls.json` collects
the later boundary and convergence controls, including diagnostic flags. A
flag-free checkpoint still needs an explicit saturation comparison before it
can be called an asymptotic soliton share. The independent fail verdict was
committed before the delegated novelty review and exact repository-window
inspection; their provenance is recorded in the audit's post-commit section.

Raw fields are in the location recorded in `meta.yaml`. The runner skips
already completed or explicitly stopped cases. To regenerate fields without
overwriting retained evidence, use a fresh scratch copy containing the source
scripts and selected case-list JSON, but no per-case output JSON, and set the
`RAW` path in that scratch copy of `independent.py` to a new raw-data folder.
Compile the shooting helper before running:

```sh
cc -O3 -shared -fPIC zs_shoot.c -o /tmp/gpt-c-zs-shoot.so
memory_pressure | grep 'free percentage'
```

Launch only when at least 35% is free, with one heavy process at a time:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  ~/agent-work/venv/bin/python run_audit.py core_cases.json
```

Use the other case-list files for the documented extensions. A configuration
file alone does not mean that a case completed; check the corresponding
per-case report and the final audit's limitations. `measurement_failed`,
`intentionally_interrupted` and `terminated_for_edge` records are retained,
not silently rerun into successful-looking reports.
