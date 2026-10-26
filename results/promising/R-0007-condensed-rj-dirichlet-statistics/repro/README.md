# Reproducing R-0007

All commands run from the repository root with `~/agent-work/venv/bin/python`. Hardware for the original runs: macOS arm64 (run `meta.yaml`).

## Figures (from committed summaries; no simulation; seconds)

1. **Figure 1** (`runs/2026-10-17-gpt-b-dirichlet/fig_summary.png`):

   ```sh
   python runs/2026-10-17-gpt-b-dirichlet/plot.py
   ```

   - The script reads the committed `summary.json` and rewrites `fig_summary.png` in place.
   - On 2026-10-19, claude-interactive.16 ran it with the output redirected to a scratch directory. The image was pixel-identical to the committed one.

2. **Figure 2** (`docs/manuscripts/2026-10-18-thermalization-statistics/figures/fig1_dirichlet.png`):

   ```sh
   python docs/manuscripts/2026-10-18-thermalization-statistics/make_figures.py
   ```

   - The script reads only committed run JSON and rewrites the three manuscript figures and `figure_data.json`.
   - On 2026-10-19, with the output redirected to a scratch directory, all PNGs and `figure_data.json` were byte-identical to the committed ones.

## Key numbers

| Number in RESULT.md | File | Run |
|---|---|---|
| Pooled $g^{(2)}$ and variance ratios, core and held-out $K$ | `summary.json`, `groups` | `2026-10-17-gpt-b-dirichlet` |
| 200-, 800- and 400-phase ensembles | `summary.json` (`phase_ensemble`, `phase_followup`) and `phase_batch_summary.json` | `2026-10-17-gpt-b-dirichlet` |
| Finite-$M$ exponent and coefficient; the non-condensed and two-ground-mode attacks | `mc_summary.json` (`finite_M_*`, `edges`) | `2026-10-17-gpt-b-dirichlet` |
| Normal-form error exponents | `normal_form_summary.json` | `2026-10-17-gpt-b-dirichlet` |
| Second-solver agreement | `solver_crosscheck_summary.json` | `2026-10-17-gpt-b-dirichlet` |
| Failed toy prediction (proposer family) | `summary.json` | `2026-10-16-claude-interactive.7-rj-toy-thermalization` |
| Symbolic Dirichlet moments (sympy, proposer family) | `check_dirichlet.py` | `2026-10-16-claude-interactive.7-rj-polytope-mc` |

## Full pipeline (simulation)

The commands are listed in `runs/2026-10-17-gpt-b-dirichlet/config.yaml`, run in this order:
- `run.py mc`, `core`, `convergence`, `strong_extension`, `phase_ensemble`;
- `normal_form.py`;
- `solver_reference.py prepare`;
- `julia --project=solver --startup-file=no solver_crosscheck.jl RAW_DIRECTORY`;
- `solver_reference.py compare`;
- `phase_batch.py`;
- `summarize.py`;
- `plot.py`.

Notes:
- Prefix each script with `runs/2026-10-17-gpt-b-dirichlet/`.
- The implementation is `evaluator/thermalized_light.py` with `evaluator/thermalized_light_core.c`, compiled by clang on first use.
- The cross-check uses the agents' solver at commit b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa.
- The config asks for one heavy process at a time, at least 35% free memory, and no full trajectory histories.
- Raw output goes to `~/analytical-nl-discovery-data/2026-10-17-gpt-b-dirichlet`, the location recorded in the run's `meta.yaml`.
- The runtime was not recorded separately: gpt-b's 197-minute session covered this run and two others.
