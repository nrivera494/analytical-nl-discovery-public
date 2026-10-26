<!-- agent: gpt-a; model: gpt-6-astra; family: gpt -->

# Independent dispersive-wave audit implementation

The common implementation is `simulate.py`. The sibling run directories
contain configuration files and `run.py` entry points. Those entry points
reuse this implementation; no proposer script is imported.

Run one numerical process at a time. Before launching, check
`memory_pressure | grep 'free percentage'` and wait if the result is below
35 percent. Use `~/agent-work/venv/bin/python`, with
`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`. The implementation checks memory
before each case, waits in short intervals when the threshold is unmet,
keeps only the current complex field, and records peak RSS.
It skips cases already present in a run's summary, preserving failed and
partial work for diagnosis. Only explicitly designated convergence cases
use more than 16384 time samples.

The positive Fourier convention is `q=ifft(u)`, `u=fft(q)`. The propagator
uses a centered RK4 interaction-picture update. A separate exact nonlinear
split step with Yoshida composition is available when shock is absent.
Raman convolution uses the analytic transfer function by default. The
sampled-kernel option records its DC quadrature error and, when requested,
normalizes it before propagation.

No anti-alias damping is applied in this independent code. The separate
`2026-10-16-gpt-a-dw-julia/crosscheck.jl` harness runs the pinned agents'
solver with both a flat nonlinear prefactor and its native frequency window.
That harness must also be run alone, using `JULIA_NUM_THREADS=2`.

Raw fields and scalar strip scans are written outside git under
`~/analytical-nl-discovery-data/<run-id>/`. No full field history
is retained. Configuration, metadata, summary numbers and figures are kept
in the repository. Each propagation records the common source file's hash.

`analyze.py` computes the frozen fits, extrapolations and invariants.
`../2026-10-16-gpt-a-dw-analysis/check_numerics.py` compares convergence runs
and the Julia outputs. Its `plot.py` and `report_tables.py` generate the
scientific figures and data tables. The separate exact-gate-null run uses
high-precision contour residues; it is explicitly a TOD-free background
test and is not labeled as a full-TOD counterexample.
