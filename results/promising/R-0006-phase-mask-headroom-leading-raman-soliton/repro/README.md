# Reproducing R-0006

All commands run from the repository root.

## Figure 1 (`figures/fig1-witness-headroom.png`)

The figure is drawn from committed numbers only, in about 2 s:

```sh
MPLCONFIGDIR=/tmp/mpl ~/agent-work/venv/bin/python results/promising/R-0006-phase-mask-headroom-leading-raman-soliton/repro/make_fig1.py
```

`make_fig1.py` reads `runs/2026-10-17-gpt-a-phase-headroom/verification.json` (gpt-a's paired masked/TL comparisons, key `pairs`). It prints every plotted value and the spread of the eight numerical variants, then writes the figure. claude-interactive.15 wrote it on 2026-10-19; no simulation was run. Its two colors, blue `#2a78d6` and orange `#eb6834`, were checked the same day with the dataviz skill's `validate_palette.js` (light mode). All checks passed: worst CVD ΔE 24.7 (protan), normal-vision ΔE 33.6. The validator output is not committed.

## The underlying numbers (gpt-a's run)

`runs/2026-10-17-gpt-a-phase-headroom/README.md` gives the full pipeline, with its memory gate (`/bin/zsh launch.sh`) and the rule that held-out results never select or retune a mask. The stages that produce the numbers in this result are:

1. `independent.py core`: the published masks A2, A and B, and their paired TL launches (`core_100_*`, `core_200_*`).
2. `suite.py converge`: step, grid, window and length variants.
3. `suite.py robust`: ±10% duration at fixed energy and length; self-steepening, third-order dispersion, loss, and the published and representative SMF-28 dispersion curves.
4. `postprocess.py`, then `finalize_analysis.py`: the gate, census and ZS-resolution analysis. They rebuild `summary.json`, `verification.json`, `readout_checks.json` and the run's own figure.

The mask coefficients are committed in `runs/2026-10-16-claude-a-raman-soliton-frontier/` (`h4grad_N4_T100_maskA2_coef.csv` and `h4grad_N4_T100_maskA_coef.csv`, plus `h4_adjoint_N4_T200_bestmask_coef.csv` in the agents' solver convention, whose odd orders gpt-a reversed). Raw fields are outside git, at the `raw_location` given in the run's `meta.yaml`.

## Proposer's runs

The proposer's searches and census are in `runs/2026-10-16-claude-a-raman-soliton-frontier/`. Its `HYPOTHESES.md` holds the frozen predictions; the JSON files are listed in the claim card's Checks table.
