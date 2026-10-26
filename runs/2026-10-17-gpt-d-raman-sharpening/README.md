---
agent: gpt-d
model: gpt-6-astra
family: gpt
date: 2026-10-17
---

# Reproduce the Raman sharpening checks

Run from the repository root on task/T-20261017-gpt-d-01.
This directory contains independent mathematical/profile checks, GNLSE RHS
snapshots and sampled-kernel convergence. Its solver_commit is null because
these calculations do not invoke the repository propagation solver.

The initial predictions were committed as
6df0927ef31369add037f36db21643b14d68bf51 before analyze.py or propagation.
The cancellation follow-up was committed as
3259dd5be15c597202b52436ff7d5d1918c702dc before execution.
The RHS/kernel follow-up was committed as
ca03c40b69e09530f57de96863bab3d048df06ea before execution.
The independent audit was committed as bcecbc6 before the requested
gpt-b review was read. The initial finite-window failure remains in
summary.json; followup_summary.json records its adaptive follow-up.

Use the existing agent venv (NumPy, SciPy, mpmath, Matplotlib and tomli on
Python versions before 3.11). Before each numerical command, check
memory_pressure and proceed only at at least 35% free. Run serially:

    memory_pressure | grep 'free percentage'
    ~/agent-work/venv/bin/python runs/2026-10-17-gpt-d-raman-sharpening/analyze.py
    memory_pressure | grep 'free percentage'
    ~/agent-work/venv/bin/python runs/2026-10-17-gpt-d-raman-sharpening/followup.py

After completing the propagation run and its Julia cross-check, aggregate
saved scalar diagnostics and generate both figures:

    memory_pressure | grep 'free percentage'
    MPLCONFIGDIR=/private/tmp/gpt-d-matplotlib ~/agent-work/venv/bin/python runs/2026-10-17-gpt-d-raman-sharpening/report.py

Raw arrays are outside git under
~/analytical-nl-discovery-data/2026-10-17-gpt-d-raman-sharpening/.
No raw array or copyrighted source text is committed. The plotted analytic
curves are computed from trigamma; quadrature markers are independently
integrated. Propagation maxima use the launch width on the horizontal axis,
not a fitted sech width of the evolved field. Error bars smaller than the
markers are omitted; deterministic fit-window sensitivities are reported
in the summaries rather than presented as statistical confidence intervals.

report.py also writes the derived concentration run and its figure. It
reconstructs accepted-plane photon drift from the preserved scalar CSVs;
it does not overwrite the raw first-core failure caused by including RK
internal stages in an invariant diagnostic.
