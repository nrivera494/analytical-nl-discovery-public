# Reproducing R-0015

All commands run from the repository root.

| Item | Run id | Command or file |
|---|---|---|
| Closed form, symbolic | `2026-10-19-claude-interactive.12-c2-weak-dispersion-verification` | `python derive_c2.py` (outputs `derive_c2.json`, `derive_c2_gq.json`, `derive_c2_sech.json`, `derive_c2_ablation_no_mean_reshaping.json`, all committed) |
| Propagation sweep | same | `sweep.py` with `lam_min.py`; settings in `config.yaml`; raw `.jsonl` written to the run's `raw_location` |
| Fits and figure | same | `python analyse.py <raw_dir>` (reads `main.jsonl`, `conv.jsonl`, `tight.jsonl`; writes `summary.json` and `fig_summary.png`) |
| Proposer's derivation and solver | `2026-10-18-pi-chatgpt-independent-verification` | `archive/weak_theory/second_order_symbolic.py`, `archive/strong/verify_weak_cross.py` |
| Second-platform reproduction of the proposer's numbers | `2026-10-19-claude-interactive-gpt6pro-quick-repro` | see its `config.yaml` |

The figure needs the raw `.jsonl` files, which are not in git, or a rerun of the sweep (not repeated for this write-up), so G7 is open.
