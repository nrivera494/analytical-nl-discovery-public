# Independent weak-dispersion audit

Agent `gpt-e`, model `gpt-6-astra`, family `gpt`, 2026-10-19.

This run tests claim C-20261010-claude-a-01 from its narrowed claim card. All
numerics were written during the clean-context audit. No prior run is imported.
The shared `tangent.py` is also used by the auditor's strong-dispersion and
full-field similariton checks.

Use `~/agent-work/venv/bin/python -W ignore`. Run the commands in
`config.json` serially. Check `memory_pressure` before each heavy launch and
wait if free memory is below the session's threshold. Python BLAS and FFT work
uses one thread. Arrays live in the absolute raw-data directory in `meta.yaml`.

`initial-main.json` preserves two coarse-step numerical failures. The current
`run.py` adds a dispersive-frequency step guard and the refined results are in
`main.json`; these failures must not be interpreted as physical counterexamples.

The independent Julia check uses the clean pinned agents' solver:

```sh
JULIA_NUM_THREADS=2 julia --project=solver runs/2026-10-19-gpt-e-weak-dispersion/solver_crosscheck.jl ~/analytical-nl-discovery-data/2026-10-19-gpt-e-weak-dispersion/crosscheck.npz 512
```

`prepare_crosscheck.py` reconstructs the small input bundle from this audit's
saved output modes. `summarize.py` imports the numerical Julia TOML summaries
into tracked `rk4ip.json`. Its mode contractions cross-check the optimum found
by the Python eigensolver, rather than independently optimizing the Julia map.
