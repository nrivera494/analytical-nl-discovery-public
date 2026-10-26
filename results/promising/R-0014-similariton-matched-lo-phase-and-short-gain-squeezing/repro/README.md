# Reproducing R-0014

All commands run from the repository root. The run uses independent numpy and scipy code and no repository solver.

| Item | Run id | Scripts |
|---|---|---|
| (ii) initial slopes, thresholds, held-out $n_{sp}=2$ | `2026-10-19-claude-interactive.13-similariton-lo-verification` | `fullfield.py`, `slopes.py`, `ff_tests.py`, `explicit.py`; summaries `slopes_summary.json`, `ff_tests.json`, `explicit_summary.json` |
| (i) $C_{PP}$ power and prefactor, $\Gamma$ scan | same | `reduced.py`, `reduced_analysis.py`, `reduced_gamma_scan.py`; `reduced_summary.json`, `reduced_gamma_scan.json` |
| (iii) $G^{-1/3}\lambda_{\min}$ | same | `reduced.py`, `curve.py`; `curve_summary.json` |
| Proposer's launch values (0.8964864655, 3.1592358) | same | `source_seed.py`; `source_seed_summary.json` |
| Truncated-Wigner check | same | `twa.py`; `twa_summary.json` |
| Figure | same | `fig_summary.py` |

`fig_summary.py` reads `slopes_summary.json` and `curve_summary.json`, which are committed, and the reduced-model arrays `reduced_*_nsp1_lo.npz`, which are kept at the run's `raw_location`. Rerunning `reduced.py` regenerates the arrays; see the run's `config.yaml` for settings. This was not repeated for the write-up, so G7 is open.

The proposer's original calculation is in run `2026-10-18-pi-chatgpt-independent-verification` (`archive/similariton/`).
