# Reproducing R-0008

All commands run from the repository root with `~/agent-work/venv/bin/python`. The original runs used macOS arm64, serial production, and at most 3 GB per process (run `config.yaml`).

## Figures (no simulation; seconds)

1. **Figure 1** (`runs/2026-10-18-gpt-b-grin-squeezing/fig_summary.png`):

   ```sh
   python runs/2026-10-18-gpt-b-grin-squeezing/analyse.py
   ```

   - The plotted points come from the committed case files `K*.json` and the fit in `summary.json`.
   - The script also recomputes artefact checks from the raw tangent files at `~/analytical-nl-discovery-data/2026-10-18-gpt-b-grin-squeezing` (about 15 MB of `*_tangent.npz`), so it needs that store.
   - It rewrites `summary.json` and `fig_summary.png` in place.
   - On 2026-10-19, claude-interactive.16 ran it with both outputs redirected to a scratch directory. The image was pixel-identical to the committed one, and `summary.json` identical apart from its list of component files.

2. **Figure 2** (`docs/manuscripts/2026-10-18-thermalization-statistics/figures/fig2_squeezing.png`; panel (a) is this result):

   ```sh
   python docs/manuscripts/2026-10-18-thermalization-statistics/make_figures.py
   ```

   - The script reads only committed run JSON.
   - On 2026-10-19 its PNGs and `figure_data.json` were byte-identical to the committed ones.

## Key numbers

| Number in RESULT.md | File | Run |
|---|---|---|
| $c$, occupation exponent | `summary.json` (`core_quad_scaling`) | `2026-10-18-gpt-b-grin-squeezing` |
| Envelope maximum 0.366 dB (67 and 241 cases) | `summary.json` (`original_rectangle_curvature_gate`, `small_curvature_gate`) | same |
| Held-out quadrature cases | `summary.json` (`original_held_out_quadrature`) | same |
| $\lambda_{\rm lin}$ ranges, $f_0$ of the $E'=0.9$ launch | `summary.json` (`cases[].checkpoints[]`: `linear_quad`, `f0`), selected $K=5$, $\sigma=0.3$, lossless, $10^6\le n\le10^{10}$, $0.55\le f_0\le0.87$ | same |
| Ceiling conjecture | `summary.json` (`multimode_ceiling_conjecture`) | same |
| Three-mode exact benchmark | `summary.json` (`exact_exchange`, `exact_exchange_convergence`) | same |
| Second solver | `solver_check.json` | same |
| Counting resolution | `summary.json` (`counting_resolution*`) | same |
| One-mode excess at $R=0.8$ | `summary.json` (`curvature_gate`) and `exact_summary.json` | `2026-10-18-gpt-b-kerr-exact` |
| Loss ceiling $-7.21$ dB | closed form $10\log_{10}0.19$; the distributed-loss test is `summary.json` (`loss`, `loss_ensemble`) | `2026-10-18-gpt-b-condensate-squeezing` |

## Full pipeline (simulation)

- `runs/2026-10-18-gpt-b-grin-squeezing/config.yaml` lists the model, the steps and the frozen prediction commits.
- The production entry point is `run.py`; the count-resolution and exact-benchmark stages are in `count_resolution.py`, `confirm_counts.py` and `exact_three_mode.py`.
- The second-solver check is `solver_check.jl`, run with `julia --project=solver` at solver commit b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa, then `solver_check.py`.
- The shell sequences gpt-b used are `serial_checks.sh`, `after_checks.sh` and `final_checks.sh`.
- Raw output goes to the store above.
- The runtime was not recorded separately: gpt-b's 229-minute session covered this run and two others.
