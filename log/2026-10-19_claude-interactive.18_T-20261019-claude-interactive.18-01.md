---
date: 2026-10-19
agent: claude-interactive.18
model: claude-opus-5-5
family: claude
task: T-20261019-claude-interactive.18-01
duration_min: 45
---

## Did

- Wrote the PI's requested manuscript on passive spectral shaping and the leading soliton:
  `docs/manuscripts/2026-10-19-phase-shaper-soliton-bounds/` (`main.tex` with appendix, `refs.bib`, `make_figures.py`,
  `figures/`, `crux_checks.py`, `build.sh`, `main.pdf`, `README.md`). Structure and standards follow
  `docs/manuscripts/2026-10-18-thermalization-statistics/`.
- Read R-0001, R-0002, R-0006 and their audit reports; the cards C-20261018-pi-chatgpt-01, C-20261016-claude-a-01, -03,
  -04, C-20261017-gpt-a-01 and P-20261016-claude-interactive-03; the derivation note; claude-interactive.9's audit;
  claude-interactive.10's novelty review; gpt-a's summary for C-a-04; the ZSFormalization PROVENANCE file; and the
  summaries of the eight runs listed in the README.
- Re-derived each main-text crux before writing it and wrote `crux_checks.py` (sympy and closed forms; no eigenvalue
  solves, no propagation): polarization identity, sharp scalar inequality, $J_{2n}$ identity, $p=2N$ cancellation,
  extremizer spinor, Gaussian Hausdorff–Young equality, sech-source autocorrelation, a random even-moment majorant test,
  all closed-form ceilings, and the asymmetric source's $M_0$, phase and hierarchy.
- Redrew three figures in one style from committed JSON (no PNG reused). Checked Crossref and arXiv metadata for every
  reference. No simulation was run; each Python job was small and ran after a `memory_pressure` check (51–59% free).

## Found

- Every crux agrees with the record: residuals at most $3\times10^{-15}$, ceilings to every printed digit.
- **Discrepancy (R-0001 §8).** "At non-integer $N$ the headroom is at most 0.44%" holds only for $N\ge2.5$. Between
  integers the best ceiling peaks where consecutive exponents cross: 0.671% at $N\approx2.40$, 0.205% at
  $N\approx3.43$, 0.088% at $N\approx4.45$, 5.60% at $N\approx1.30$ (closed form; the committed curve of run
  `2026-10-18-claude-interactive.9-mask-adversary` gives 0.66868% at $N=2.4$). R-0001's experiment uses $N=2$–4.
  Task T-20261019-claude-interactive.18-02.
- **Rounding slips.** The asymmetric gains quoted as +2.777% (per-bin) and +2.643% (amplitude-and-phase Chebyshev) are
  2.776% and 2.642% in `verify_summary.json`. Folded into T-20261019-claude-interactive.18-02.
- **New derivation (mine, unverified).** The equality case of the $L^p$ inequality is unique: extremizers are exactly
  $q_*$ times a constant phase and the carrier $e^{-2i\xi t}$, shifted in time (a.e. equality, a Lipschitz argument that
  $\theta$ stays in $(0,\pi/2)$, and $\alpha'=-\xi$, $\beta'=\xi$ from the alignment). Corollary: the even-moment chain
  certifies TL optimality only for integer-order sech lasers; for any other laser every ceiling is strictly above the TL
  value. The manuscript uses this to explain the asymmetric counterexample and labels it "our derivation".
- The integrable ceiling is far below the Raman-model output: at $N=4$ the TL launch's leading soliton carries 0.597
  (100 fs) and 0.644 (200 fs) of the laser energy against $7/16$ (ratios formed from run
  `2026-10-17-gpt-a-phase-headroom`).
- The problem card's results table is stale; already covered by T-20261018-claude-interactive.9-03 and
  T-20261019-claude-interactive.15-05.

## Changed

- Added `docs/manuscripts/2026-10-19-phase-shaper-soliton-bounds/` (all files above, plus the folder's `.gitignore`).
- Added tasks T-20261019-claude-interactive.18-01 (this task, now done), -02 and -03.
- No claim, result or problem status changed; no file under `results/`, `claims/` or `problems/` edited.
- Page counts: main text pages 1–5 (ends half-way down page 5), appendix pages 6–8 (starts on page 6), references page 9.

## Not verified

- The equality-case uniqueness and its corollary (above): to be checked by a GPT-family agent,
  T-20261019-claude-interactive.18-03.
- The between-integer maxima of the sech headroom: closed form by me, consistent with the committed curve, not checked
  by another family (T-20261019-claude-interactive.18-02 asks for the R-0001 wording, which will re-check them).
- The Raman crux (the lowest-order Raman term conserves $\int|q|^2$ but not the ZS spectrum, so only $f_1\le1$ survives)
  is standard perturbation reasoning, stated without a new computation.
- The duration at which Raman becomes negligible for the integrable test is not computed; the manuscript says so.
- Literature: I read no paper text; every access level in the README is the one recorded in the repository.

## Loose ends

- T-20261019-claude-interactive.18-02: amend R-0001 §8 (non-integer precision) and note two rounding slips.
- T-20261019-claude-interactive.18-03: cross-family check of the equality case and its corollary.
- Existing, referenced: T-20261018-claude-interactive.9-03 and T-20261019-claude-interactive.15-05 (stale problem card),
  T-20261018-claude-interactive-05 (G6 for R-0001/R-0002), T-20261019-claude-interactive.15-01/-02 (G5/G6 for R-0006),
  T-20261017-gpt-a-03 (verification of C-20261017-gpt-a-01), T-20261018-claude-interactive.9-01 (exact optimality at
  non-integer sech and Gaussian lasers), T-20261018-claude-interactive.9-02 (asymmetric headroom).
