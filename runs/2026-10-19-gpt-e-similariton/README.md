# Independent similariton ASE audit

Agent `gpt-e`, model `gpt-6-astra`, family `gpt`, 2026-10-19.

`reduced.py` discretizes the hydrodynamic spatial operator independently and
integrates its covariance with white ASE. Its output projection is explicitly
orthonormal on the numerical grid. `fullfield.py` uses the auditor's new
Fourier tangent solver to contract initial vacuum and distributed ASE onto
moment and matched-field readouts. Both full noise and amplitude-only source
contractions are recorded. `optimize.py` searches for a vanishing normalized
phase–energy deficit inside the reduced regime.

Run the Python scripts with `~/agent-work/venv/bin/python -W ignore`,
serially, after checking memory. Reduced suites are `main` and `checks`;
full-field suites are `main`, `checks`, `edge-resolution`, and `short`.
`summarize.py` produces the tracked audit metrics and keeps only selected
checkpoints in the tracked reduced-model JSON files. Dense scalar curves,
field arrays, and covariance trajectories live in the raw-data directory.

The initial projection and current-readout attempts are retained with
`initial-` names. They document numerical artefacts and are not evidence for
a physical failure of the reduced exponents. The sharp-edge full-field
moments remain cutoff-sensitive after the discrete readout is corrected.

For the independent Julia check, run `prepare_crosscheck.py`, then use the
auditor's `solver_crosscheck.jl` in the weak-dispersion run with this run's
`crosscheck.npz` and the desired step count. Set `JULIA_NUM_THREADS=2` and
`--project=solver`. That harness uses the unchanged pinned solver's discrete
RK4IP adjoint and integrates its ASE contraction along the amplifier.
