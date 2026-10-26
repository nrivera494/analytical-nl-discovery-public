---
agent: claude-interactive.20
model: claude-opus-5-5
family: claude
task: T-20261019-claude-interactive.20-01
date: 2026-10-19
---

# Manuscript draft: quantum noise around the amplifier similariton

A short manuscript requested by the PI on 2026-10-19. It covers what this repository has established about quantum-noise
bounds in normal-dispersion fibre amplifiers (the amplifier similariton): the shape-mode variance exponents, the
five-component spectral ratio, the phase–energy deficit (result R-0011), and the matched-mode squeezing criterion, the
$G^{7/3}$ phase growth and the $G^{1/3}$ floor (result R-0014). It is a docs artifact. It does not change the status of any
claim, result or problem, and nothing in it is a result in the sense of `docs/PROMOTION.md`.

**Status of the content.** R-0011 and R-0014 are promising results (not formalized, not peer reviewed). Every statement
in the main text is either part of one of them, as narrowed or sharpened, or explicitly labelled as refuted, superseded or
not verified. Authors are left to the PI.

## Files and build

| File | What it is |
|---|---|
| `main.tex` | revtex4-2, `aps,pra,twocolumn,superscriptaddress`. Main text, `\appendix` (A–G), bibliography |
| `refs.bib` | 18 references, all recorded in the repository with DOI or arXiv id; bibliographic fields checked against Crossref (16 DOIs) and the arXiv API (5 ids) on 2026-10-19 |
| `make_figures.py` | Regenerates `figures/` from committed run summaries; runs no simulation; writes `figures/figure_data.json` with every plotted number |
| `figures/` | `fig1_shape`, `fig2_short`, `fig3_large` (PDF for LaTeX, PNG for preview), `figure_data.json` |
| `checks/` | My re-derivation of the cruxes: `crux_symbolic.py` (SymPy), `crux_reduced.py` (a seconds-long reduced-model integration, under 100 MB) and their output `crux_output.txt`. Not a run; no number in the manuscript comes from it |
| `build.sh` | Runs `make_figures.py`, then `latexmk -pdf`, then prints the appendix start page from `main.aux` |
| `main.pdf` | Compiled output |

Build: `./build.sh` (uses `~/agent-work/venv/bin/python` unless `PYTHON` is set, and `/Library/TeX/texbin`).

**Page counts** (from `main.aux`, label `appendixstart`; 9 pages in all):
- main text, including Figs. 1–3 and Table I: pages 1–5 (5 pages; page 5 is about 60% full);
- appendix (A–G, including the provenance Table II): pages 6–8, starting on page 6 after a `\clearpage`;
- references: page 9.

## Results, claims and runs used

| Item | Status (as of 2026-10-19) | How it is used |
|---|---|---|
| R-0011 (C-20261008-claude-a-02 as narrowed) | promising; G1–G5 met, G6–G8 open. Proposer claude-a (claude); verifiers GPT 6 Pro (pi-chatgpt, gpt) and gpt-a (gpt); clean-context audit gpt-e (gpt), pass with reduced regime | Secs. III, IV; Apps. A–D |
| R-0014 (C-20261019-pi-chatgpt-02 as verified) | promising; G1–G4 met, G5–G8 open. Proposer GPT 6 Pro (gpt); verifier claude-interactive.13 (claude); no clean-context audit | Secs. IV B, V; Apps. D, E |
| C-20261008-claude-a-02, original wording | $C_{PP}\propto G/\varepsilon_0^2$ and "with ASE there is no squeezing" superseded (refuted by GPT 6 Pro); uniform edge remainder and P6 not verified; some finite-gain tables fail | Table I, Sec. VI, as failures only |
| C-20261019-pi-chatgpt-02, original "if and only if" | superseded by claude-interactive.13 (fails at $R=1$) | Sec. V A, Table I |
| C-20261008-claude-a-01 (collective-coordinate moments) | cheap-checks-passed (not verified) | Sec. VI "Context, not verified" and the 500 pJ example seed of Sec. VII |
| C-20261008-gpt-a-01, C-20261008-gpt-a-02 (attraction) | cheap-checks-passed (not verified) | Sec. VI "Context, not verified" |
| P-001 | audited | Model and target |

Sources read: both RESULT.md files and their audit pointers; the two claim cards in full; the statements of
C-20261008-claude-a-01, -gpt-a-01 and -gpt-a-02; P-001; the GPT 6 Pro review doc
`docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md`; the head and section list of gpt-e's
audit report and claude-interactive.13's audit note (Parts 1 and 3 in part); the full-text review
`docs/review-2026-10-19-claude-interactive-spie2016-fulltext.md`; the run metadata and summary JSON listed below.

| Run | Used for | Agent (family) |
|---|---|---|
| `2026-10-18-pi-chatgpt-independent-verification` [P] | Fig. 1 (period-matched rows), Fig. 2b (counterexample); fitted powers, full-NLSE rates and $\tau=4$ table, brightness example, reduced values at $\tau=12$ (`archive/similariton/README.md`) | pi-chatgpt (gpt; GPT 6 Pro) |
| `2026-10-19-gpt-e-similariton` [E] | Figs. 1, 2b, 3; compensated envelopes; $\lambda_{\rm LO}=0.436717$ at $\tau=0.2$ | gpt-e (gpt; gpt-6-astra) |
| `2026-10-19-claude-interactive.13-similariton-lo-verification` [V] | Figs. 2, 3; every number of R-0014's verification | claude-interactive.13 (claude) |
| `2026-10-11-gpt-a-highlights-audit-c2` [A] | Fig. 1b; full-field rates; held-out $gL=2$ failure | gpt-a (gpt; gpt-6-astra) |
| `2026-10-19-claude-interactive-gpt6pro-quick-repro` [Q] | second-platform reproduction of the counterexample | claude-interactive (claude) |
| `2026-10-08-claude-a-amp-sim-checks` [S] | the 500 pJ example seed ($N_0=2.6\times10^9$, $P_0=125$ W) | claude-a (claude) |

Appendix G (Table II of the PDF) lists every number with its run and agent. Values marked "fig." there were computed by
`make_figures.py` from committed numbers of the cited run (gpt-e's compensated-envelope extrema, $R=3.76$ from the run's
$\langle P\rangle_P/P_0$). Closed-form evaluations ($R\approx3.8$, $\gamma P_0/g=3.1$, $R=2.5/n_{sp}$, $\nu_\ell$, the periods
$\pi/\nu_2$ and $2\pi/\nu_2$, the second-order coefficients of App. E) are not from runs.

## Figures

| Figure | Panels | Data (file, selection) | Run ids |
|---|---|---|---|
| Fig. 1 | (a) photon-normalized shape variances $\ell=2,3,4$ vs $\ln G$; (b) $\mu_2/\mu_1$ and $1-r^2$ vs $\ln G$ | `reduced-main.json` ($\Gamma=\sqrt{18}$, $n_{sp}=1$, asymptotic launch, 9 checkpoints); `archive/similariton/analysis_summary.json` (`period_matched_l2`); `closed.json` (`shape`) | `2026-10-19-gpt-e-similariton`, `2026-10-18-pi-chatgpt-independent-verification`, `2026-10-11-gpt-a-highlights-audit-c2` |
| Fig. 2 | (a) initial slope $/2n_{sp}g$ vs $R$; (b) $\lambda_{\rm LO}$ vs $\tau$ at short length | `slopes_summary.json` (6 cases × 7 $R$); `curve_summary.json` (`curve`, $\varepsilon_0=0.05$, 0.025); `fullfield-short.json`, `fullfield-main.json` (chirped, unsmoothed, $\varepsilon_0=0.05$); `summary.json` (`short_gain_counterexample`) | `2026-10-19-claude-interactive.13-similariton-lo-verification`, `2026-10-19-gpt-e-similariton`, `2026-10-18-pi-chatgpt-independent-verification` |
| Fig. 3 | (a) error of the $C_{PP}$ prefactor vs $\ln G$; (b) $G^{-1/3}\lambda_{\min}(C_{\rm LO})$ vs $\ln G$ | `reduced_summary.json` (`ratio_err_envelope`, `lam_lead_at`, ranges), `source_seed_summary.json`; gpt-e `reduced-main.json` (ratio and $\lambda_{\min}$ computed from `CPP`, `CAA`, `Phi_NL`, `phase_energy_deficit`), `fullfield-main.json` | `2026-10-19-claude-interactive.13-similariton-lo-verification`, `2026-10-19-gpt-e-similariton` |

All figures were redrawn in one style (that of `docs/manuscripts/2026-10-18-thermalization-statistics`) from committed
JSON; no committed PNG or PDF was reused. Colours: the three categorical slots pass the dataviz validator for colour-vision
deficiency (worst adjacent ΔE 9.2, deutan); aqua is below 3:1 contrast, so every colour is doubled by a marker shape and a
legend. gpt-e's and GPT 6 Pro's photon-normalized variances use the same orthonormal Legendre normalization (505.69 and
505.65 at $\tau=18$), so they share axes in Fig. 1(a).

## Where each statement is derived

| Statement | Crux in the main text | Full derivation |
|---|---|---|
| Legendre blocks and $G^{1/3}$, $G^{5/3}$ (R-0011a) | Sec. III: gain cancels against background growth; Legendre operator; Eq. (4) and its roots; $(u,w)$ rotation with $B^2=-\nu^2I$; noise $\propto e^{-\tau/3}$ in $u$; multiply by $N_{\rm out}$ | App. A (separation, asymptote, propagator, two-sided bounds), App. B (noise projection, metric $B_{\ell m}$, edge-singular phase quadrature) |
| Spectral ratio (R-0011b) | Sec. IV A: $s_\ell=n_\ell+3n_\ell'$; $s_1=3c_2e^{-\tau/3}$; block form and Schur complement | App. C |
| $C_{AA}$ exact, $C_{PP}\propto G^{7/3}$, $1-r^2$ (R-0011c, R-0014i) | Sec. IV B: photon-number conservation; $p_0=\Phi_{NL}n_0+R_0$; ${\rm Var}R_0=O(G^{1/3})$; shape phase $p_2/5$ dominates the residual | App. D ($C_{AA}$ integration, $\ell=0$ formula, the $O(G^{-1/3})$ cross term, regression, $\lambda_{\min}$) |
| Short-length criterion (R-0014ii) | Sec. V A: first-order covariance expansion at $z=0^+$; passive generators vanish on vacuum; Kerr shear weighted by $P/\int P$ | App. E (second order; the $R=1$ coefficient) |
| $\lambda_{\min}=\Theta(G^{1/3})$ (R-0014iii) | Sec. V B: $\det C/\lambda_{\max}\simeq C_{AA}(1-r^2)$ | App. D |
| Why amplifier noise does not forbid squeezing | Sec. V A (isotropic noise rate $2n_{sp}g$ against shear rate $2\gamma\langle P\rangle_P$; Caves' theorem concerns phase-insensitive linear amplifiers) and Sec. V B (energy noise amplified as $G$, locked only to $G^{-2/3}$) | — |

I re-derived each crux before writing it (`checks/`, and the log entry). All agree with the record:
- SymPy confirms the elimination to $q''+2(a'/a)q'+\ell(\ell+1)(a''/2a)q=0$, $A_*^3=18/\Gamma^2$, the roots, $B_\ell^2=-\nu_\ell^2I$, $s_\ell=n_\ell+3n_\ell'$, $s_1=3c_2e^{-\tau/3}$, the $-1/5$ in $\bar p$, $\langle P\rangle_P=4P_0/5$ and $P_0/\sqrt2$, the first-order slope and the $R=1$ coefficient $2{\rm Var}_P(\gamma P/g)-n_{sp}$.
- A minimal Legendre-mode integration of the reduced model ($\ell\le4$, exact Legendre modes, DOP853) reproduces the recorded reduced-model values to the printed digits: $\mu_2/\mu_1$ and $1-r^2$ at $\tau=4$, 12, 15, 18 (gpt-a's and claude-interactive.13's values), $C_{AA}$, the $C_{PP}$ prefactor range and power over $12\le\tau\le26$, and the $[0.338,0.633]$ range of $G^{-1/3}\lambda_{\min}$. Fixed-window fitted exponents differ in the third or fourth decimal from GPT 6 Pro's (e.g. 0.32443 against 0.32461), as expected for fits over an oscillating envelope with a different sampling.
- I derived the separation (App. A) by hand from the dispersionless phase and continuity equations; the proposer's `symbolic.py` and gpt-e's finite-volume operator were not re-run.

New in this manuscript, derived here and not checked by another family: the closed forms of the $R=1$ second-order
coefficient for the sharp parabola, $n_{sp}^2/7-n_{sp}$ ($-6/7$, $-10/7$), and for the Gaussian,
$n_{sp}^2(4/\sqrt3-2)-n_{sp}$ ($-0.6906$, $-0.7624$, equal to the record's full-field values); and the remark that for the
parabola the coefficient is negative only for $n_{sp}<7$. The record's parabola values ($-0.85$, $-1.41$) are for a parabola
smoothed at $\delta=0.05$; they are close to, and consistent with, the sharp-edge closed forms. Task
T-20261019-claude-interactive.20-03.

## Literature and access levels

This session read no paper text. It retrieved bibliographic metadata from Crossref (all 16 DOIs) and the arXiv API
(cond-mat/0201158, cond-mat/0303063, quant-ph/9912095, physics/0211097, 2603.11574). The access levels below are those
recorded in the repository, with the reader named.

| Reference | Id | Access as recorded (reader; where) |
|---|---|---|
| Fermann et al., PRL 84, 6010 (2000) | 10.1103/PhysRevLett.84.6010 | full text (GPT 6 Pro; R-0011 §7); abstract only (P-001 audit) |
| Kruglov, Peacock, Harvey, Dudley, JOSA B 19, 461 (2002) | 10.1364/JOSAB.19.000461 | primary text through a public transcription, publisher PDF not obtained (GPT 6 Pro); abstract only (P-001 audit) |
| Finot, Millot, Dudley, OL 29, 2533 (2004) | 10.1364/OL.29.002533 | abstract only (claude-a.2); author-accessible primary text (GPT 6 Pro) |
| Wabnitz, IEEE PTL 19, 507 (2007) | 10.1109/LPT.2007.893823 | abstract only (claude-a.2, gpt-a, GPT 6 Pro) |
| Wabnitz, QELS 2007 | 10.1109/QELS.2007.4431461 | full text (GPT 6 Pro, R-0011 §7); "abstract only plus indexed body excerpts" in another record (see Discrepancies) |
| Menotti & Stringari, PRA 66, 043610 (2002) | arXiv:cond-mat/0201158 | full text (claude-a.2, gpt-a, GPT 6 Pro) |
| Fedichev & Fischer, PRA 69, 033602 (2004) | arXiv:cond-mat/0303063 | full text (claude-a.1, gpt-a, GPT 6 Pro) |
| Caves, PRD 26, 1817 (1982) | 10.1103/PhysRevD.26.1817 | abstract only (GPT 6 Pro); introduction and theorem summary (P-001 audit) |
| Drummond & Corney, JOSA B 18, 139 (2001) | 10.1364/JOSAB.18.000139, arXiv:quant-ph/9912095 | full preprint (GPT 6 Pro) |
| Gordon & Mollenauer, OL 15, 1351 (1990) | 10.1364/OL.15.001351 | abstract only (gpt-a) |
| Ho & Kahn, J. Lightwave Technol. 22, 779 (2004) | arXiv:physics/0211097 | targeted full text, Sec. II and start of Sec. III (gpt-a) |
| Shirasaki & Haus, JOSA B 7, 30 (1990) | 10.1364/JOSAB.7.000030 | abstract only (P-001 audit) |
| Doerr, Shirasaki, Khatri, JOSA B 11, 143 (1994) | 10.1364/JOSAB.11.000143 | abstract only (P-001 audit) |
| Zweck & Menyuk, JOSA B 35, 1200 (2018) | 10.1364/JOSAB.35.001200 | full text (gpt-a); abstract only (P-001 gap section) |
| Wang, Liu, Song, Hu, Proc. SPIE 9893, 98930J (2016) | 10.1117/12.2227743 | full text (claude-interactive, PI download, 2026-10-19) |
| Wang et al., OL 41, 5286 (2016) | 10.1364/OL.41.005286 | full text (claude-interactive, PI download, 2026-10-19) |
| Haviv, Kozlov, Krüger, Sidorenko, OL 51, 1812 (2026) | 10.1364/OL.591606 | abstract only (claude-interactive.14) |
| Ren et al. (2026) | arXiv:2603.11574 | abstract only (claude-interactive.14) |

The novelty sentences in the manuscript are bounded-search statements copied from the record (R-0011 §7, R-0014 §7); they
are not novelty clearances. Gate G6 is open for both results: the full journal text of Wabnitz (2007) for R-0011
(T-20261008-claude-a-05) and a targeted search for (ii) for R-0014 (T-20261019-claude-interactive.14-03).

## Discrepancies and stale statements found in the record

None of these changes a verdict. I did not edit any claim, result or problem file. Task T-20261019-claude-interactive.20-02
collects items 1–4, 7 and 8.

1. **R-0011 still says R-0014's claim is under verification.** The header bullet and §9 of
   `results/promising/R-0011-*/RESULT.md` say that C-20261019-pi-chatgpt-02 is "still under Claude-family verification"
   (T-20261019-claude-interactive-03). claude-interactive.13 verified it and it is now R-0014.
2. **R-0014's brightness example mixes parameters.** Its regime table gives $\Phi_{NL}^2/N_0=3\times10^{-6}$, 0.17 and
   $2\times10^7$ at $\tau=4$, 12, 26 "for a 500 pJ seed". These divide $\Phi_{NL}^2$ computed at $\varepsilon_0=0.05$,
   $\Gamma=\sqrt{18}$ (run [V]) by the 500 pJ seed's $N_0=2.6\times10^9$; that seed has $\varepsilon_0=0.067$, $\Gamma=4.8$
   (run [S]). With the seed's own parameters on the asymptote, the leading-order formula gives $\Phi_{NL}^2/N_0\approx0.09$ at
   $\tau=12$ (my closed-form evaluation). Same order, same conclusion. The manuscript quotes the $\varepsilon_0=0.05$
   values of $\Phi_{NL}^2$ and the seed's $N_0$ separately.
3. **P-001's narrative sections are stale.** The "Conjectures" section lists only C-20261004-claude-a-01 and C-0001, and the
   2026-10-04 update says "The amplifier case (gain with Langevin noise) is untouched". The frontmatter lists the newer
   claims and R-0011, R-0014, but the text does not.
4. **A verification task looks superseded.** T-20261008-claude-a-03 (verify C-20261008-claude-a-02, priority 1, open) is
   still open although the claim was verified by GPT 6 Pro and audited by gpt-e; its P1–P6 scope is only partly covered
   (P6 and the finite-gain tables are outside the narrowed result). The PI may want to close or narrow it.
5. **Access levels differ between records** for Fermann et al. (2000), Kruglov et al. (2002), Wabnitz QELS (2007) and
   Zweck & Menyuk (2018), because different agents read different versions (table above). Not an error; reported with the
   reader.
6. **Normalization of the shape variances.** gpt-e's and GPT 6 Pro's "photon-normalized" variances use orthonormal
   Legendre components, $\sqrt{2/(2\ell+1)}\,n_\ell$, so they are $2/(2\ell+1)$ times $N_{\rm out}{\rm Var}\,n_\ell$ in the claim
   card's coefficient convention. The exponents are unaffected. The Fig. 1 caption says "orthonormal".
7. **A range in R-0014 is not reproduced by the committed checkpoints.** R-0014 (regime table) and claude-interactive.13's
   audit note say that "below about 8" (or "at $\tau\le8$") the (i) prefactor ratio is 0.86–1.11. The committed checkpoints
   in `reduced_summary.json` of run [V] give 1.098, 1.106, 1.024 at $\tau=2$, 4, 6 for $\Gamma=\sqrt{18}$, but 0.766, 0.855,
   0.935 for the held-out $\Gamma=1$ (unchirped). The range presumably refers to $\Gamma=\sqrt{18}$ on the dense (raw) curve.
   The manuscript quotes the committed checkpoint values.
8. **Values that exist only in raw files.** R-0011 §5 quotes full-NLSE values at $\varepsilon_0=0.1$ (0.3317394, 0.03153063)
   and the core value 0.2779053 from run [P]; they are not in the run's committed files (the committed report has the
   $\varepsilon_0=0.05$, 0.025 values and "about 0.278", "approximately 0.02804"). The manuscript quotes only the committed
   values.
9. **Kruglov et al. (2002) author order.** Crossref gives Kruglov, Peacock, Harvey, Dudley; the repository cites it only as
   "Kruglov et al.". The bibliography uses Crossref's order.

No derivation in the record disagreed with my re-derivation.

## Not verified in this manuscript

- The context claims C-20261008-claude-a-01, -gpt-a-01 and -gpt-a-02 are quoted from their cards and labelled as not
  verified; I did not check them.
- The closed forms of the $R=1$ second-order coefficient (App. E) are mine (item above).
- The experimental outlook (Sec. VII) is qualitative; no detection-efficiency budget or technical-noise estimate is given.
  The statement that the 500 pJ seed has $R=2.5/n_{sp}$ is a closed-form evaluation from its card's parameters.
- No full-NLSE noise computation exists in the asymptotic range $\tau\ge12$ (T-20261010-claude-interactive.2-02); the
  manuscript says so.
