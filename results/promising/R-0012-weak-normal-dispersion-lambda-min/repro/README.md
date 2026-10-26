# Reproducing R-0012

All paths are relative to the repository root.

## Figure 1 (GPT 6 Pro's verification figure)

`figures/fig1-weak-dispersion-verification.png` is page 1 of the committed PDF, rendered with Ghostscript 10.07.0:

    gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r110 -dFirstPage=1 -dLastPage=1 \
      -sOutputFile=results/promising/R-0012-weak-normal-dispersion-lambda-min/figures/fig1-weak-dispersion-verification.png \
      runs/2026-10-18-pi-chatgpt-independent-verification/archive/weak/weak_verification.pdf

**Regenerating the PDF from computation (G7, open).** `archive/weak/build_summary.py` reads the committed `weak_results.json`, `second_order_*.json` and theory JSON files. It also needs the Gaussian mode arrays `mode_*.npz`, which are raw files kept at the run's `raw_location`, so it fails on the committed files alone; this was checked on 2026-10-19 in a scratch copy. The full sequence, on a copy of the archive (from `archive/weak/README.md`), is:

    cp -R runs/2026-10-18-pi-chatgpt-independent-verification/archive /tmp/verification
    cd /tmp/verification/weak
    OPENBLAS_NUM_THREADS=1 python run_suite.py
    OPENBLAS_NUM_THREADS=1 python run_second_order.py
    OPENBLAS_NUM_THREADS=1 python verify_weak.py --phi 10 --y 1e-6 --n 3072 --support .24 --rtol 2e-13 --output second_order_phi10.json
    python ../weak_theory/effective_oscillator.py
    python ../weak_theory/second_order_symbolic.py
    MPLCONFIGDIR=/tmp/mpl python build_summary.py

The archive README says the full weak suite takes several minutes. It has not been run end to end outside the verifier's session (task T-20261019-claude-interactive.17-01).

**Quick check.** From a copy of the archive, `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python strong/verify_weak_cross.py` gives $\lambda_{\min}=0.02654003090685$ at $\Phi=3$, $y=10^{-4}$ in about 2 s. `python weak_theory/effective_oscillator.py` and `python weak_theory/second_order_symbolic.py` regenerate the oscillator constants and the symbolic coefficients. claude-interactive reran all three on a second platform (run `2026-10-19-claude-interactive-gpt6pro-quick-repro`).

## Figure 2 (the proposer's summary figure)

`runs/2026-10-10-claude-a-dispersionless-fano/summary.png` is drawn by `make_figure.py` in that run folder, from its committed JSON files (`config.yaml` lists the scripts that produce them). Panel (c) is item 5.

## Key numbers

| Numbers in RESULT.md | Source (committed) |
|---|---|
| Item 5 exponents, ratios, oscillator prefactors, Fourier cross-check | `runs/2026-10-18-pi-chatgpt-independent-verification/summary.json` (key `weak_dispersion`); `archive/weak/summary.json`; `archive/weak/README.md` (convergence) |
| Items 1–5 by gpt-a, including the 3(b) counterexample | `runs/2026-10-11-gpt-a-highlights-audit-c3/summary.json`; commands in its `config.md` (`audit.py algebra`, `audit.py dispersion`, `raman_band.py`, `raman_convergence.py`) |
| The proposer's held-out scores and the $y=0.1$ value | `runs/2026-10-10-claude-a-dispersionless-fano/` (`HELDOUT.md`, `lam_min_dispersion*.json`, `heldout_results.json`) |
| FastDifferentiableMMNLO check at $\Phi=5$, $y=0.02$ | run `2026-10-10-claude-a-solver-dispersion-check` (solver commit b9fa957) |
