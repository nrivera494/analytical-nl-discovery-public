# Configuration

agent: gpt-b; model: gpt-6-astra; family: gpt.

The reference is `2026-10-05-claude-interactive-raman-stochastic`, especially
its `convergence/` raw folder. Launch: 3655.7 W sech, 0.22 ps intensity FWHM,
1550 nm, 10 m fibre, beta2 -0.0206 ps²/m, beta3 0.000081038 ps³/m,
Raman fraction 0.18 at 300 K. The conversion to sech width and soliton number
is recorded in `../2026-10-10-gpt-b-soliton-solver/anchor_50ps.toml`.
This is an N approximately 1.969 pulse, not a fundamental soliton.

Native commands use `soliton_native_check.jl` and the solver run's conventions.
The 50 ps case preserves the original archived binary filter on the exact
original frequency bins and uses 32768 temporal samples. Its batch command is
`soliton_batch_adjoint.py <anchor_50ps.toml> --band 12 --bin-width .3
--source-stride 5 --omit-adjoint --output-suffix batch_cells03`.
The batch eigenvalues are restricted to the declared spectral-cell basis.

`soliton_readout_check.py <anchor_50ps.toml> --columns 2 --nsteps 5000
--stride 2 --output <raw>/readout_2mm.json` checks the original mask with
a smaller propagation step and finer bath quadrature.

The initial 10 ps check and its interrupted full covariance are retained.
Its window, Raman sampling and resampled mask all differed from the archive;
the discrepancy is not attributed to any one of those changes without a
controlled comparison. The archived -5.322 dB total omits the shock multiplier
in its Raman contraction; compare both published bath columns before scoring.

The saved broader optimized mask is evaluated natively with
`anchor_optimized.toml`, `anchor_optimized_fine.toml` and
`anchor_optimized_finest.toml` in the solver run. They preserve the same
frequency-bin pattern while refining temporal sampling; the latter two
use 2 mm propagation steps. Bath quadrature settings are explicit in each
configuration. `anchor_optimized_window100ps.toml` doubles the window at
the fine-grid time sample. Its mask preserves the old physical-bin
intervals, assigning shared endpoints to the upper interval; this also
halves the output frequency-bin spacing. It is a combined window/frequency
sampling check, not an identical finite-dimensional readout.
