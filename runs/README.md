# Runs

One folder per run or sweep: `runs/<date>-<agent>-<short-name>/` containing

- `config.*` — everything needed to rerun, including seeds;
- `meta.yaml` — run id (the folder name), `solver_commit` and `solver_dirty` (see `docs/SOLVER.md`), hardware, wall time, claim or exploration it serves, raw-data location;
- `summary.json` — the numbers quoted elsewhere;
- small figures.

Raw output does not go in git; `.gitignore` excludes `runs/**/raw/` and the common array formats. Storage location for raw data: **interim local storage** (PI decision, 2026-10-04), while cloud storage is arranged under `T-20261002-claude-interactive-02`.

- Raw output goes to `~/analytical-nl-discovery-data/<run-id>/` on the machine that ran it. Record that absolute path, and the machine, as `raw_location` in `meta.yaml`.
- For P-001, P-002, P-20261004-root-03 and P-20261004-claude-interactive-02, and the tasks that feed them, claims may cite such runs.
- When cloud storage exists, the data is copied there and `raw_location` is updated. Nothing in that folder is deleted until then.
