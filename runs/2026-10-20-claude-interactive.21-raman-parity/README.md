# Run 2026-10-20-claude-interactive.21-raman-parity

Field checks of the time-reversal selection rule and the first-order Raman modal-transfer closed form (claim
C-20261020-claude-interactive.21-01; exploration `explorations/2026-10-20-claude-interactive.21-raman-parity-selection.md`, §6).

| File | What |
|---|---|
| `mmfield.py` | standalone three-mode (HG00, HG10, HG01) stationary random-field GNLSE: Kerr, Raman with scalable odd part $\lambda$, shock $s$, walk-off, intra-group white-noise coupling; exact time-mirror on the grid |
| `run_tests.py` | P1 (exact identity), P2 (first-order slopes), P3 (finite $z$), P3s05, convergence (`conv_dz`, `conv_dt`, post-hoc `conv_window`) |
| `predictions.md`, `predictions.json` | pre-registered predictions: P1–P3 (commit `4721994`), P4 (commit `3d27bc5`) |
| `solver_check.jl`, `predictions_solver.txt` | P4: the closed form against the repository solver (unmodified, `b9fa957`); post-hoc `noraman` and `rerun_b` |
| `analyze.py`, `summary.json` | decomposition into $\lambda$-odd and $\lambda$-even parts, standard errors, Langmuir references |
| `fig_p3.py`, `fig_p3.png` | P3 figure |
| `results/` | P1/P2 JSON, run metadata, solver-check outputs |

Raw per-realization arrays: `~/analytical-nl-discovery-data/2026-10-20-claude-interactive.21-raman-parity/` on host COECIS-G3FLW49YGQ.
