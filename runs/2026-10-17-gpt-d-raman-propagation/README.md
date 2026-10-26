---
agent: gpt-d
model: gpt-6-astra
family: gpt
date: 2026-10-17
---

# Frozen serial propagation suite

The initial freeze is commit 6df0927ef31369add037f36db21643b14d68bf51.
config.yaml contains every material, launch, grid, step and relaxation
parameter. Widths are intensity FWHM. The material models are declared local
surrogates: the fluoride oscillator/index/mode-size parameters are sourced,
but neither fiber uses a calibrated broadband dispersion/area curve.

propagate.py is an independently written Float64 fixed-step interaction-picture
RK4 implementation. It evaluates the actual nonlinear RHS energy derivative
and the separate spectral identity at every stage and accepted plane.
Only scalar plane diagnostics and initial/final/maximum field snapshots are
stored. The exact analytic response and shock prefactor are supplied, with an
orthogonal optical support cutoff; the default solver blue-edge window is not used.

Before each heavy launch, require at least 35% free memory. Run only one
heavy process at a time; the script also checks memory between cases.
No run exceeds 32,768 time points.

    memory_pressure | grep 'free percentage'
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 ~/agent-work/venv/bin/python runs/2026-10-17-gpt-d-raman-propagation/propagate.py

The script preserves completed raw cases and accepts case names as arguments.
For an intentional fresh reproduction, preserve the existing raw run first;
do not overwrite failed evidence. Raw results live at
~/analytical-nl-discovery-data/2026-10-17-gpt-d-raman-propagation/.

The agents' Julia solver is pinned to
b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa, with no solver modifications.
The low-level interface follows evaluator/soliton_noise_baselines.jl.
For a serial independent implementation comparison:

    memory_pressure | grep 'free percentage'
    JULIA_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 ~/.juliaup/bin/julia --heap-size-hint=2G --project=solver runs/2026-10-17-gpt-d-raman-propagation/julia_crosscheck.jl core h6_100

Both numerical Julia cases completed. The original surrounding time -l
wrapper returned exit 1 because a macOS sysctl for resource statistics was
denied after execution; it is omitted from the reproduction command.
No observed maximum RSS is available. The memory gate remained above the
specified threshold; arrays are bounded and no full field history is kept.

Run the sharpening/report.py aggregation after both implementations finish.
It preserves raw diagnostic fields, adds accepted-plane checks, compares
solver outputs and creates the summary figures. Julia uses 4,000 steps;
floating-point ceil selects 4,001 for the corresponding Python cases.
Thus maxima are sampled at slightly different positions. The Julia ratio is
the spectral identity evaluated on Julia fields; the independent actual-RHS
test is performed by Python.

No new adjoint or stochastic-noise run was performed. The assignment-authorized
2026-10-16 discrete-RK4IP adjoint audit is cited prior evidence.
