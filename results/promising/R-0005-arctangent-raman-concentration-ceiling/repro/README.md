# Reproducing R-0005

The commands are those listed in `runs/2026-10-17-claude-interactive.8-concentration/config.yaml`. They run from that folder with the agents' venv (`~/agent-work/venv`: numpy 2.0.2, scipy 1.13.1, matplotlib 3.9.4), except the Julia line, which runs from the repository root. Check `memory_pressure | grep 'free percentage'` before each heavy command and run one at a time.

## Figure 1 (`runs/2026-10-17-claude-interactive.8-concentration/fig_summary.png`)

The figure needs the raw propagation output (written to `~/analytical-nl-discovery-data/2026-10-17-claude-interactive.8-concentration`, about 40 MB) and the committed `summary_static.json`:

```sh
cd runs/2026-10-17-claude-interactive.8-concentration
~/agent-work/venv/bin/python -W ignore check_bound.py           # bathtub, 315 profiles, optimizer -> summary_static.json
~/agent-work/venv/bin/python -W ignore run_propagation.py       # no arguments: every case in its CASES table (A1-A8, B1, convergence variants)
~/agent-work/venv/bin/python -W ignore make_figure.py
```

The recorded wall times are 9 s for `check_bound.py` and about 900 s for the propagation in total (`meta.yaml`).

## Key numbers

| Numbers | Command (in the concentration folder unless noted) | Output |
|---|---|---|
| Bathtub $1.6\times10^{-10}$, profiles 0.99592, optimizer table | `check_bound.py` (seed 20261017) | `summary_static.json` |
| Refined optimizer 0.5195–0.5268 | `optimizer_refine.py` (seed 20261018) | `summary_optimizer_refine.json` |
| 26,507 planes, maxima, retention, artefacts | `run_propagation.py` (cases in its CASES table; post-freeze `A7_postfreeze A7_postfreeze_halfstep A8_postfreeze A8_postfreeze_halfstep`) | `summary_propagation.json` |
| Second solver | from the repository root: `JULIA_NUM_THREADS=1 julia --heap-size-hint=2G --project=solver runs/2026-10-17-claude-interactive.8-concentration/julia_crosscheck.jl`; then `julia_analysis.py` | `summary_julia.json` |
| Hollenbeck–Cantrell relaxation | `hc_checks.py --prop`, `hc_convention_check.py` and `hc_optimizer.py` in `runs/2026-10-17-claude-interactive.8-hc-relaxed` | that folder's summaries |
| Proposer's checks | `analyze.py` in `runs/2026-10-17-gpt-d-raman-sharpening`, `propagate.py` in `runs/2026-10-17-gpt-d-raman-propagation`, then `report.py` (writes `runs/2026-10-17-gpt-d-raman-conditional`) | those folders' summaries |

The aggregate `summary.json` of the concentration run collects these outputs.
