# Reproducing R-0009

All commands run from the repository root with `~/agent-work/venv/bin/python`. The original runs used macOS arm64, serial production, and at most 3 GB per process (run `config.yaml`).

## Figures (no simulation; seconds)

1. **Figure 1** (`runs/2026-10-18-gpt-b-condensate-squeezing/fig_summary.png`):

   ```sh
   python runs/2026-10-18-gpt-b-condensate-squeezing/analyse.py
   ```

   - The script reads the committed component JSON of the run (`ensemble_summary.json`, `refinement_summary.json`, `nonlinear_ensemble.json`, `final_resolution.json` and others).
   - It reads some tangent files from the raw store of the shared propagation run, `~/analytical-nl-discovery-data/2026-10-18-gpt-b-grin-squeezing`, so it needs that store.
   - It rewrites `summary.json` and `fig_summary.png` in place.
   - On 2026-10-19, claude-interactive.16 ran it with both outputs redirected to a scratch directory. The image was pixel-identical to the committed one, and `summary.json` identical apart from its list of component files.

2. **Figure 2** (`docs/manuscripts/2026-10-18-thermalization-statistics/figures/fig2_squeezing.png`; panel (b) is this result):

   ```sh
   python docs/manuscripts/2026-10-18-thermalization-statistics/make_figures.py
   ```

   - The script reads only committed run JSON, here `refinement_summary.json`.
   - On 2026-10-19 its PNGs and `figure_data.json` were byte-identical to the committed ones.

## Key numbers

All are in `runs/2026-10-18-gpt-b-condensate-squeezing/summary.json` unless stated otherwise.

| Number in RESULT.md | Key |
|---|---|
| Identity error, $V_X/V_P$, residual, 1177 states | `algebra` |
| 12-path means, SDs, $f_0$ ranges | `ensembles` (name `weak-disorder`, $h=0.0025$) |
| In-range subset, curvature ratio $r$ | `weak_signoff_domain` |
| Step changes | `resolution` |
| Strong-disorder finest pair | `final_resolution` |
| Curvature exponents, coefficients, sagitta ratios | `curvature_scaling` |
| Frozen nonlinear ensembles | `nonlinear_ensembles`, `nonlinear_ensemble_convergence` |
| Card predictions 1–2 | `original_ensemble_predictions` |
| Self-phase reference ratio | `SPM_reference` |
| Loss stress test | `loss`, `loss_ensemble` |

- The lower-$n$ departures (prediction 3) are in the case files of `runs/2026-10-18-gpt-b-grin-squeezing`.
- The mean $1/V_P$ at $z=10$ ($-24.97$ dB) was computed by the manuscript's `make_figures.py` from `refinement_summary.json`; see `figure_data.json`.

## Full pipeline (simulation)

- The propagation is shared with `runs/2026-10-18-gpt-b-grin-squeezing` (`run.py`).
- This run's stages are `refine.py`, `scaling.py`, `nonlinear_ensemble.py`, `final_resolution.py` and `mechanism.py`, then `analyse.py`. Their frozen predictions are the `predictions-*.md` files in the run folder.
- Raw output goes to `~/analytical-nl-discovery-data/2026-10-18-gpt-b-condensate-squeezing` and the store of the shared run.
- The runtime was not recorded separately: gpt-b's 229-minute session covered this run and two others.
