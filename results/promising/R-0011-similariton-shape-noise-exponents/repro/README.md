# Reproducing R-0011

All paths are relative to the repository root. No repository solver is involved.

## The figure

`figures/fig1-similariton-verification.png` is page 1 of the verifier's committed PDF, rendered with Ghostscript 10.07.0:

    gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r110 -dFirstPage=1 -dLastPage=1 \
      -sOutputFile=results/promising/R-0011-similariton-shape-noise-exponents/figures/fig1-similariton-verification.png \
      runs/2026-10-18-pi-chatgpt-independent-verification/archive/similariton/similariton_verification.pdf

**Regenerating the PDF from computation (G7, open).** `archive/similariton/build_figures.py` reads `results_fv.json` and `results_nlse_extended.json` from its own folder. These are raw outputs kept at the run's `raw_location` (`meta.yaml`), not in git. To regenerate them, work on a copy of the archive so that the committed files stay byte-identical:

    cp -R runs/2026-10-18-pi-chatgpt-independent-verification/archive /tmp/verification
    cd /tmp/verification
    OPENBLAS_NUM_THREADS=1 python similariton/reproduce.py --suite all --output-dir similariton
    MPLCONFIGDIR=/tmp/mpl python similariton/build_figures.py
    python similariton/analyze_results.py

- The archive pins Python 3.11 or later, NumPy, SciPy and Matplotlib (`archive/requirements.txt`). The verifier used Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0.
- The archive README says the full suite takes several minutes, and the high-resolution full-NLSE suites take longer.
- This sequence has not been run end to end outside the verifier's session (task T-20261019-claude-interactive.17-01).

## Key numbers

| Numbers in RESULT.md | Source (committed) |
|---|---|
| Reduced-model exponents, equal-phase fits, short-gain counterexample | `runs/2026-10-18-pi-chatgpt-independent-verification/summary.json` (key `similariton`), `archive/similariton/analysis_summary.json` |
| Reduced-model tables, full-NLSE shape response and $\tau=4$ covariances | `archive/similariton/TECHNICAL_NOTES.md` section 7 and `archive/similariton/README.md` |
| The claim's own predictions (tables P1–P5) | `runs/2026-10-08-claude-a-amp-sim-checks/numeric.json` (`python runs/2026-10-08-claude-a-amp-sim-checks/numeric.py`); symbolic separation check `symbolic.py` |
| Full-field held-out ratios at $\Gamma=1$, $gL=2,4,6$ | `runs/2026-10-10-claude-interactive.2-moment-noise/summary.json` (keys `runs/heldout_e*_g*_all/lambda2_over_lambda1_L2`) |
| gpt-a's reduced-model and full-field numbers | `runs/2026-10-11-gpt-a-highlights-audit-c2/summary.json`; commands in its `config.md` |

**Quick second-platform check.** `OPENBLAS_NUM_THREADS=1 python similariton/reproduce.py --suite quick`, run from a copy of the archive, reproduces the short-gain counterexample $\lambda_{\rm LO}=0.8964864655$ in seconds (run `2026-10-19-claude-interactive-gpt6pro-quick-repro`). That number belongs to C-20261019-pi-chatgpt-02, not to this result.
