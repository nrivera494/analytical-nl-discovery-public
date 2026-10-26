# Reproducing R-0004

All commands run from the named run folder with the agents' venv (`~/agent-work/venv`: numpy 2.0.2, scipy 1.13.1, mpmath 1.3.0, matplotlib 3.9.4). The commands are those listed in each run's `config.yaml`. Check `memory_pressure | grep 'free percentage'` first and run one heavy process at a time.

## Figure 1 (`runs/2026-10-17-claude-interactive.8-sech-tightness/fig_summary.png`)

The plotted launch-plane points come from the committed `summary_snapshots.json`. The script also recomputes a sech-tracking check from the raw fields of run `2026-10-17-claude-interactive.8-concentration`, so that run's propagation must exist first:

```sh
cd runs/2026-10-17-claude-interactive.8-concentration
~/agent-work/venv/bin/python -W ignore run_propagation.py            # no arguments: every case in its CASES table; single cases can be named
cd ../2026-10-17-claude-interactive.8-sech-tightness
~/agent-work/venv/bin/python -W ignore run_sech_snapshots.py         # 20 snapshots (16 launch planes, 4 sampled-kernel repeats) -> summary_snapshots.json
~/agent-work/venv/bin/python -W ignore make_figure.py                # figure and summary_tracking.json
```

## Key numbers

All are in the sech-tightness folder unless noted.

| Numbers | Command | Output |
|---|---|---|
| Held-out closed-form agreement (48 points, $3.3\times10^{-25}$), extreme $r$, exponents, $C_3$, remainder bound | `python check_exact.py` (after `freeze_predictions.py`, which wrote the frozen predictions in f784fed) | `summary_static.json`. The verifier collected all the per-script outputs into the aggregate `summary.json` (commit d8cb883); no script writes that file |
| Solver self-test | `python solver_selftest.py` | `summary_solver_selftest.json` |
| Sampled kernel and other checks | `python extra_checks.py` | `summary_extra.json` |
| Cancellation windows at $r=0.6$ and $r=1/\sqrt3$ | `python cancellation_check.py` | `summary_cancellation.json` |
| Hollenbeck–Cantrell relaxation | `python hc_checks.py --prop` and `python hc_convention_check.py` in `runs/2026-10-17-claude-interactive.8-hc-relaxed` | that folder's summaries |
| Second solver ($E(z)$ within $3.2\times10^{-15}$) | `JULIA_NUM_THREADS=1 julia --heap-size-hint=2G --project=solver runs/2026-10-17-claude-interactive.8-concentration/julia_crosscheck.jl` from the repository root, then `python julia_analysis.py` in that folder | `summary_julia.json` |
| Proposer's checks | `analyze.py` and `followup.py` in `runs/2026-10-17-gpt-d-raman-sharpening` | `summary.json`, `followup_summary.json` |

The recorded wall times are 18 s for `check_exact.py`, 24 s for `solver_selftest.py`, about 60 s for `extra_checks.py`, about 20 s for `make_figure.py`, and about 900 s for the concentration run's propagation (each run's `meta.yaml`).
