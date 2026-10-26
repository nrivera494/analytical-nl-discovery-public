# Reproducing R-0002

All commands run from the repository root. Each run folder's `config.yaml` lists its cases and grids.

- **Ceilings (closed forms) and the frozen held-out values.** `python runs/2026-10-18-claude-interactive-zs-moment-bound-check/check.py`.
- **Solver validation, real-exponent checks of (A′), limits, and (F) against (E).** The scripts in `runs/2026-10-18-claude-interactive.9-zs-solver-validation/` (`validate_solver.py`, `majorant_realp.py`; solver in `zs.py`).
- **The figure** (`runs/2026-10-18-claude-interactive.9-mask-adversary/fig_summary.png`), the adversarial searches and the held-out Gaussian and sech tests. `run_adversary.py` produces the per-case JSON files, then `make_figure.py` draws the figure.
- **Counterexample to C-20261016-claude-a-01.** The scripts in `runs/2026-10-18-claude-interactive.9-asym-counterexample/`.
- **Gaussian ceilings at even exponents only** (for comparison with R-0001). `runs/2026-10-18-claude-interactive-zs-lean-audit/gaussian_even_ceiling.py`.
