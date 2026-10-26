# Configuration

Solver: agents' copy `d79f150` (tree `ccc8227a`), equivalently `2f632d9` on the original's history. Scripts in `example_notebooks/` of that commit; the rest are in `convergence/` of the raw-data folder (`meta.yaml`, `raw_location`). Paths below are relative to the solver root unless they start with `$D`, the raw-data folder.

## Physical setups

Both copied exactly from the notebooks.

| | squeezing_spectral_filter.ipynb | soliton_jitter.ipynb |
|---|---|---|
| Grid | $N_t = 2^{12}$, 50 ps window | $N_t = 2^{15}$, 100 ps window |
| Wavelength | 1550 nm | 1550 nm |
| Effective area | $\pi(9.2\,\mu\mathrm{m}/2)^2$ | same |
| Nonlinearity | $n_2 = 2.3\times10^{-20}$ m²/W | Silica default $n_2$ |
| Dispersion | $\beta_2 = -0.0206$ ps²/m, $\beta_3 = 8.1038\times10^{-5}$ ps³/m | $\beta_2 = -0.0206$ ps²/m |
| Raman | Agarwal ($f_R$ 0.18, 12.2 fs, 32 fs) | same |
| Pulse | sech, 0.22 ps FWHM, 3655.7 W peak | sech, 4 ps FWHM, fundamental soliton |
| Length and step | 10 m, dz = 1 mm | $L = (0.1{:}1{:}8)\,L_D$; adjoint step $L/201$; Monte Carlo step $0.025\,L_D$ |
| Observable | photon number through the binary filter `benchmark_data/squeezing_spectral_filter/optimal_filter.csv` on bins 1196:2371 (reversed) | centre of gravity (`TemporalMoment`) |

## Commands and seeds

| Stage | Command | Wall time |
|---|---|---|
| 1. Adjoint values | `julia --project=. example_notebooks/raman_stochastic_check.jl adjoint {squeezing,jitter} $D` | a few minutes |
| 2. Monte Carlo | `... raman_stochastic_check.jl mc squeezing <seed0> 125 $D` with seed0 = 5000, 5125, 5250, 5375, and `... mc jitter <seed0> 150 $D` with seed0 = 1000, 1150, 1300, 1450; 8 processes; `MersenneTwister(seed)`; the same seed for all four (spectrum, T) variants | about 45 min, then stopped by the session's background time limit |
| 3. Notebook re-execution | `nbexec.jl` on both notebooks | jitter cell 7: 319 s |
| 4. Convergence | `julia --project=. $D/convergence/sq_convergence.jl <Nt> <dz> [adjoint_mode] [adjoint saveat]`; arguments as in `round1_continuous_adjoint.log` and `round2_discrete_adjoint.log` | 38–1318 s per case, printed in the logs |
| 5. Kick test and sampler | `julia --project=. $D/convergence/kick_test.jl`; sampler `MersenneTwister(7)`, 4000 draws; kick amplitude $\gamma\varepsilon = 10^{-6}$, central differences | about 10 min |
| 6. Sensitivity spectra | `$D/convergence/sensitivity_plots.jl $D/convergence`, then `sensitivity_replot.jl` | about 8 min |
| 7. Jitter adjoint modes | `$D/convergence/jitter_adjoint_mode.jl` | about 5 min |

Summary: `julia raman_stochastic_summary.jl $D`, output in `$D/summary_partial.txt`.
