---
date: 2026-10-19
agent: claude-interactive.20
model: claude-opus-5-5
family: claude
task: T-20261019-claude-interactive.20-01
duration_min: 45
---

## Did

- Wrote the PI's requested manuscript on quantum-noise bounds in normal-dispersion fibre amplifiers (the amplifier
  similariton): `docs/manuscripts/2026-10-19-amplifier-noise-bounds/` (main.tex with appendix, refs.bib, make_figures.py,
  figures/, build.sh, main.pdf, README.md, checks/). Structure and standards follow
  `docs/manuscripts/2026-10-18-thermalization-statistics/`.
- Read: R-0011 and R-0014 (RESULT.md and audit pointers); the cards C-20261008-claude-a-02 and C-20261019-pi-chatgpt-02 in
  full; the statements and status of C-20261008-claude-a-01, -gpt-a-01, -gpt-a-02; P-001; GPT 6 Pro's review doc; the head
  of gpt-e's audit report and parts of claude-interactive.13's audit note; the Wang et al. (2016) full-text review; the
  metadata and summary JSON of runs `2026-10-18-pi-chatgpt-independent-verification`, `2026-10-19-gpt-e-similariton`,
  `2026-10-19-claude-interactive.13-similariton-lo-verification`, `2026-10-11-gpt-a-highlights-audit-c2`,
  `2026-10-19-claude-interactive-gpt6pro-quick-repro` and `2026-10-08-claude-a-amp-sim-checks`.
- Re-derived every crux before writing it: by hand (the dispersionless linearization and the cancellation of the gain term,
  App. A; the noise projection, App. B; $C_{AA}$, App. D) and with SymPy (`checks/crux_symbolic.py`: elimination to the
  Legendre equation, $A_*^3=18/\Gamma^2$, roots, $B_\ell^2=-\nu_\ell^2I$, $s_\ell=n_\ell+3n_\ell'$, $s_1=3c_2e^{-\tau/3}$,
  $\bar p=p_0-p_2/5$, $\langle P\rangle_P$ for parabola and Gaussian, the first-order slope and the $R=1$ second-order
  coefficient). A minimal independent Legendre-mode integration of the reduced model (`checks/crux_reduced.py`, under
  1 s and 100 MB; memory checked first, 56–59% free) reproduces the recorded reduced-model values to the printed digits
  ($\mu_2/\mu_1$ and $1-r^2$ at $\tau=4$, 12, 15, 18; $C_{AA}$; the $C_{PP}$ prefactor range and the power 2.33350 over
  $12\le\tau\le26$; $G^{-1/3}\lambda_{\min}\in[0.338,0.633]$). No other simulation was run.
- Redrew three figures in one style from committed JSON only (no PNG reused); checked the palette with the dataviz
  validator; checked all 16 DOIs against Crossref and 5 arXiv ids against the arXiv API (metadata only, no paper text).
- Checked every number of the provenance table against the committed files of its run with a grep pass; replaced the
  values that were not in committed files (see Found).

## Found

- All cruxes agree with the record. No derivation in the record disagreed with mine.
- New, derived here, not cross-checked: the closed forms of the $R=1$ second-order coefficient, $n_{sp}^2/7-n_{sp}$ for the
  sharp parabola ($-6/7$, $-10/7$; the record's $-0.85$, $-1.41$ are for a parabola smoothed at $\delta=0.05$) and
  $n_{sp}^2(4/\sqrt3-2)-n_{sp}$ for the Gaussian ($-0.6906$, $-0.7624$, equal to the record's full-field values); for the
  parabola the coefficient is negative only for $n_{sp}<7$.
- Record discrepancies (README items 1–9; none changes a verdict):
  1. R-0011's header and §9 still say C-20261019-pi-chatgpt-02 is under Claude-family verification; it is R-0014.
  2. R-0014's brightness example for the 500 pJ seed divides $\Phi_{NL}^2$ at $\varepsilon_0=0.05$, $\Gamma=\sqrt{18}$ by that
     seed's $N_0$; with the seed's own $\varepsilon_0=0.067$, $\Gamma=4.8$ the leading-order value at $\tau=12$ is about 0.09,
     not 0.17 (my closed-form evaluation). Same conclusion.
  3. P-001's Conjectures and 2026-10-04 update are stale (they predate the amplifier claims and both results).
  4. T-20261008-claude-a-03 (verify C-20261008-claude-a-02, p1) is still open though the claim is verified and audited.
  5. Access levels for four references differ between records (different readers).
  6. gpt-e's and GPT 6 Pro's "photon-normalized" variances use orthonormal Legendre components ($2/(2\ell+1)$ times the
     card's convention); exponents unaffected.
  7. "At $\tau\le8$ the (i) prefactor ratio is 0.86–1.11" (R-0014, claude-interactive.13's note) is not reproduced by the
     committed checkpoints for $\Gamma=1$ (0.766 at $\tau=2$); the manuscript quotes the committed checkpoint values.
  8. R-0011 §5's full-NLSE values at $\varepsilon_0=0.1$ and the core 0.2779053 are not in run P's committed files; the
     manuscript quotes only the committed $\varepsilon_0=0.05$, 0.025 values.
  9. Kruglov et al. (2002): Crossref author order Kruglov, Peacock, Harvey, Dudley.
- Page counts: main text 5 pages (1–5, including Figs. 1–3 and Table I); appendix A–G pages 6–8 (starts on page 6);
  references page 9.

## Changed

- New: `docs/manuscripts/2026-10-19-amplifier-noise-bounds/` (main.tex, refs.bib, make_figures.py, figures/ with
  figure_data.json, build.sh, main.pdf, README.md, checks/, .gitignore).
- New tasks T-20261019-claude-interactive.20-02, -03, -04; task -01 set to done.
- No claim, result or problem file was edited; no status changed.

## Not verified

- The context claims C-20261008-claude-a-01, -gpt-a-01 and -gpt-a-02 are quoted from their cards, labelled as not verified,
  and were not checked here.
- The $R=1$ closed forms and the $n_{sp}<7$ remark (App. E) have Claude-family evidence only (T-20261019-claude-interactive.20-03).
- The experimental outlook is qualitative (no detection-efficiency or technical-noise budget).
- I did not re-run the proposer's `symbolic.py`, gpt-e's finite-volume operator or any full-field code.

## Loose ends

- Record hygiene (README discrepancies 1–4, 7, 8): T-20261019-claude-interactive.20-02.
- Cross-family check of the $R=1$ second-order closed forms: T-20261019-claude-interactive.20-03.
- Revise the manuscript when R-0014's clean-context audit or the G6 searches report, and when the PI sets authors:
  T-20261019-claude-interactive.20-04.
