# Reproducing R-0010

All commands run from the repository root with `~/agent-work/venv/bin/python` (numpy, scipy, matplotlib; mpmath for the exact moments). The original runs used macOS arm64, serial production (run `config.yaml`).

## Figures (no simulation; seconds)

1. **Figure 1** (`runs/2026-10-18-gpt-b-kerr-exact/fig_summary.png`):

   ```sh
   python runs/2026-10-18-gpt-b-kerr-exact/analyse.py
   ```

   - The script reads only committed JSON in the run folder (`exact_summary.json`, `fock_summary.json`, `twa_summary.json`, `sagnac_*.json`, `gaussian_edges.json` and others).
   - It rewrites `summary.json` and `fig_summary.png` in place.
   - On 2026-10-19, claude-interactive.16 ran it with both outputs redirected to a scratch directory. The image was pixel-identical to the committed one. `summary.json` was identical apart from one added entry, `source_hashes.json`, in its component list; that file was committed after the summary was written.

2. **Figure 2** (`docs/manuscripts/2026-10-18-thermalization-statistics/figures/fig3_squeezability.png`):

   ```sh
   python docs/manuscripts/2026-10-18-thermalization-statistics/make_figures.py
   ```

   - The script reads only committed run JSON, here `exact_summary.json` and `extracted_stage.json`.
   - On 2026-10-19 its PNGs and `figure_data.json` were byte-identical to the committed ones.

## Symbolic check (seconds)

```sh
python results/promising/R-0010-displaced-thermal-kerr-squeezing-no-go/repro/derivation.py
```

- The script expands gpt-b's exact displaced-thermal moments with sympy and asserts the leading term $\nu/(4c^2)+2\nu^2c^4$. It prints the optimum coefficient $3\cdot2^{1/3}/4=3/(2\cdot4^{1/3})$ and the next-order relative correction $(\nu/4n_d)^{1/3}$.
- It then compares that correction with the committed exact optima in `runs/2026-10-18-gpt-b-kerr-exact/exact_summary.json`.
- Written and run by claude-interactive.16 on 2026-10-19; no simulation.

## Key numbers

All are in `runs/2026-10-18-gpt-b-kerr-exact/summary.json` unless stated otherwise.

| Number in RESULT.md | Key or file |
|---|---|
| Coefficient error 0.412% | `large_n_prefactor` |
| Exponents at $\nu=10$ | `fits` |
| Nine held-out cases, 0.2173 dB | `original_displaced_thermal_prediction` |
| Mixedness power 1.3344, 1.3336 | `mixedness_scaling_diagnostic` |
| Fock agreement $3.93\times10^{-12}$ | `fock_oracle` |
| TWA errors at the coherent optimum | `twa_exact_optimum_errors` |
| Oriented-Gaussian counterexample | `orientation_edge`, `gaussian_edges.json` |
| No-go checks and the first super-Poissonian counterexample | `no_go`, `no_go.json` |
| Unimodal counterexample | `unimodal_positive_P_counterexample`, `no_go_smooth.json` |
| Bright-reference Sagnac values | `bright_reference_Phi30`, `sagnac_quantum_reference.json` |
| Raw and rescaled formula errors | `bright_reference_gates` |
| External-oscillator baseline | `sagnac_Phi30` (`exact_coherent`), `sagnac_exact.json` |
| External-oscillator refinement | `sagnac_resolution.json` |
| Two-arm and fixed-number Fock checks | `bright_reference_fock_max_error`, `fixed_number_reference_fock_max_error` |
| Extracted GRIN condensates | `runs/2026-10-18-gpt-b-condensate-squeezing/extracted_stage.json` (largest error 0.17549 dB, recomputed from the rows) |

## Full pipeline (exact calculations; no fibre simulation)

- `runs/2026-10-18-gpt-b-kerr-exact/config.yaml` lists the grids, held-out sets and frozen prediction commits.
- The stages are `run.py` (exact moments and Fock), `qmc_completion.py` (TWA), `gaussian_edges.py`, `no_go_smooth.py`, `sagnac.py`, `sagnac_resolution.py` and `sagnac_quantum_reference.py`, then `analyse.py`. Their frozen predictions are the `predictions-*.md` files.
- The extracted-condensate stage is in `runs/2026-10-18-gpt-b-condensate-squeezing` and uses the shared propagation of `runs/2026-10-18-gpt-b-grin-squeezing`.
- The runtime was not recorded separately: gpt-b's 229-minute session covered this run and two others.
