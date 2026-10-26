---
agent: claude-interactive.11
model: claude-opus-5-5
family: claude
task: T-20261018-claude-interactive.11-01
date: 2026-10-18
---

# Manuscript draft: statistics of Kerr-thermalized light in multimode fibre

A short manuscript requested by the PI on 2026-10-18. It summarizes what this repository has
established about the statistics of light thermalizing in multimode fibre: the Dirichlet law of the
condensed Rayleigh–Jeans state and the squeezing results. It is a docs artifact. It does not change
the status of any claim or problem, and nothing in it is a result in the sense of `docs/PROMOTION.md`.

**Status of the content.** Every statement is either sim-verified as narrowed by gpt-b (GPT-6-astra),
refuted, or explicitly marked as not verified. Nothing is formalized or peer reviewed. Authors are
left to the PI.

## Files and build

| File | What it is |
|---|---|
| `main.tex` | revtex4-2, `aps,pra,twocolumn,superscriptaddress`. Main text, `\appendix` (A–G), bibliography |
| `refs.bib` | 28 references, all recorded in the repository with DOI or arXiv id; bibliographic fields checked against Crossref or the arXiv API |
| `make_figures.py` | Regenerates `figures/` from committed run summaries; runs no simulation; writes `figures/figure_data.json` with every plotted number |
| `figures/` | `fig1_dirichlet`, `fig2_squeezing`, `fig3_squeezability` (PDF for LaTeX, PNG for preview), `figure_data.json` |
| `build.sh` | Runs `make_figures.py`, then `latexmk -pdf`, then prints the appendix start page from `main.aux` |
| `main.pdf` | Compiled output |

Build: `./build.sh` (uses `~/agent-work/venv/bin/python` unless `PYTHON` is set, and `/Library/TeX/texbin`).

**Page counts** (from `main.aux`, label `appendixstart`; 10 pages in all):
- main text, including Figs. 1–3 and Table I: pages 1–5 (5 pages);
- appendix (A–G, including the provenance Tables II–III): pages 6–9, starting on page 6 after a `\clearpage`;
- references: page 10.

The references follow the appendix (PRA order), so the 5-page main text does not include them.

## Claims used, as they now stand

| Claim | Status (verifier) | How it is used |
|---|---|---|
| C-20261016-claude-interactive.7-01 | sim-verified as narrowed (gpt-b) | Sec. III and App. A: exact scalar classical measure identity and the verified moments |
| C-20261018-claude-interactive.7-01 | sim-verified as sharpened, early window only (gpt-b) | Sec. IV A and App. B: $\lambda_{\rm lin}=\sigma_{\max}^{-2}$, curvature correction $cR$, checked envelope |
| C-20261018-claude-interactive.7-02 | sim-verified as sharpened (gpt-b) | Sec. IV B and App. C: $\lambda_-\simeq\det V/V_P$ identity and the early weak-disorder ensemble |
| C-20261018-claude-interactive.7-03 | sim-verified as sharpened (gpt-b) | Sec. V and Apps. D–E: displaced-thermal optimum, conditional no-go, leading Sagnac term |
| C-20261016-claude-interactive.7-02 | refuted (gpt-b) | Sec. IV A: purity does not imply Gaussianity; sets the Gaussian windows. The $\ln n$ trend is quoted as partial support only |
| C-20261016-claude-interactive.7-03 | not verified (cheap-checks-passed) | Sec. VI: open question only |

Each claim is used in its sharpened form. Original wording that gpt-b refuted or did not sign off is
reported as failed or narrowed (Table I), never as a result. Sources read: the problem card, the six
claim cards, the six gpt-b audit reports, the gpt-b PI summaries, the exploration note
`explorations/2026-10-16-claude-interactive.7-quantum-rj-state.md` (§§1–2, 4, 6.5, 6.8, 6.10, 6.11),
`docs/multimode-squeezing-scope.md`, gpt-b's logs `log/2026-10-18-gpt-b-squeezing-audit.md` and
`log/2026-10-17-gpt-b_T-20261016-claude-interactive.7-07.md`, and the Found sections of the proposer's logs
of 2026-10-17 and 2026-10-18.

## Runs used

| Run | Used for | Agent |
|---|---|---|
| `2026-10-17-gpt-b-dirichlet` | Fig. 1; Dirichlet moments, held-out sizes, failed 200-launch sample, fresh holdout, strong disorder, finite-$M$ exponent, beat-averaging check, non-condensed attack | gpt-b |
| `2026-10-17-gpt-b-scrambling` | exact one-mode Kerr coherence and $\det V$ at $n=4096$; TWA half-collapse 331–383 $L_{\rm NL}$ | gpt-b |
| `2026-10-17-gpt-b-gge` | phase memory up to $1.2\times10^6L_{\rm NL}$ (open question) | gpt-b |
| `2026-10-18-gpt-b-grin-squeezing` | Fig. 2(a); $\lambda_{\rm lin}$ values, $c$, exponent, envelope, held-outs, counting discrepancy, loss ceiling | gpt-b |
| `2026-10-18-gpt-b-condensate-squeezing` | Fig. 2(b), Fig. 3(b) stars; identity error, 12-path ensemble, curvature ratio, step changes, SPM reference ratio, extracted-condensate cases | gpt-b |
| `2026-10-18-gpt-b-kerr-exact` | Fig. 2(a) single-mode check, Fig. 3; exact moments, coefficient, exponents, held-outs, counterexamples, Sagnac numbers | gpt-b |
| `2026-10-16-claude-interactive.7-rj-toy-thermalization` | the proposer's failed toy prediction ($g^{(2)}=1.74,1.70,1.67$), quoted as a failure | claude-interactive.7 |

Appendix G (Tables II and III of the PDF) lists every number with its run and agent. Values marked
"fig." there were computed by `make_figures.py` from per-path data of the cited run (the mean of
$1/V_P$ and the $f_0$ range at $z=10L_{\rm NL}$). Closed-form evaluations of displayed formulas
($28/15$, $40/21$, $D/S_1$, $0.945$, $s_*\approx20$–30 rad, $f_0\ge0.57$) and the unit conversion
$n\approx5\times10^{10}$ for 10 kW in 1 ps at 1 µm are not from runs.

## Figures

| Figure | Panels | Data (file, selection) | Run ids |
|---|---|---|---|
| Fig. 1 | (a) excited-mode $g^{(2)}$ vs $M$; (b) $\varepsilon_q^2{\rm Cov}(I_0,I_q)/c$ vs $\varepsilon_q$, $K=5$ | `summary.json` groups ($K=5$, $\sigma=0.3$, dt 0.04, window to 8000; held-out rows; `phase_followup` fresh holdout); `mc_summary.json` rows (excited modes only) | `2026-10-17-gpt-b-dirichlet` |
| Fig. 2 | (a) $V_{\rm fixed}/\lambda_{\rm lin}-1$ vs $R=\sigma_{\max}^6/n_0$; (b) $\lambda_-$ and $1/V_P$ vs $z$ | (a) `summary.json` cases ($K=5$, $\sigma=0.3$, launch 4201, dt 0.02, 2048 shots, lossless), $z=5,10,20$, points with excess > 2 SE; fit coefficient `core_quad_scaling`; (b) `refinement_summary.json`, 12 paths, $E'=0.3$, $\sigma=0.3$, dt 0.0025 | `2026-10-18-gpt-b-grin-squeezing`, `2026-10-18-gpt-b-kerr-exact`, `2026-10-18-gpt-b-condensate-squeezing` |
| Fig. 3 | (a) exact $\lambda_*$ vs $n_d$, $\nu=1,3,10,30$; (b) $\lambda_*n_d^{1/3}/\nu^{4/3}$ with extracted GRIN condensates | `exact_summary.json` rows ($n_d\ge10^4$); `extracted_stage.json` rows | `2026-10-18-gpt-b-kerr-exact`, `2026-10-18-gpt-b-condensate-squeezing` |

All figures were regenerated in one style from committed JSON; no committed PNG was reused. Colours:
categorical slots validated for colour-vision deficiency, each colour doubled by a marker shape; the
$\nu$ ramp is a single-hue ordinal ramp.

## Where each statement is derived

| Statement | Crux in the main text | Full derivation |
|---|---|---|
| Dirichlet law and its moments | Sec. III: $d^2A=\frac12dI\,d\phi$; integrating $I_0$ leaves $I_0\ge0$, which cannot bind when $E'\le\kappa N$; constant Jacobian to the simplex | App. A (measure, moments $g^{(k)}$, Var $I_0$, Cov, GRIN sums, large-$K$ limit, B-spline remark, fluctuating invariants, two polarizations) |
| Coherence is not a Gaussianity clock | Sec. IV A (exact one-mode numbers) | quoted from run `2026-10-17-gpt-b-scrambling`; not re-derived |
| Tangent-map squeezing and curvature correction | Sec. IV A: $V=SS^{\mathsf T}$, symplectic pairs give $\sigma_{\max}^{-2}$; sagitta variance $V'^2/(8n_0)$ gives $R/8$ | App. B (linearization, one-mode shear, sagitta, independence of $h$ and $u$) |
| Condensate identity | Sec. IV B: $\lambda_-\lambda_+=\det V$, $\lambda_-+\lambda_+={\rm tr}V$ | App. C (bounds, Schur complement, SPM reference) |
| Kerr-stage optimum | Sec. V: balance $\nu/(4s^2)$ against $2\nu^2s^4/n_d$ | App. D (minimization; exact moment formula used by the verifier; mixedness counterexample) |
| No-go | Sec. V: $[\rho,\hat N]=0\Rightarrow{\rm Var}X_\theta=1+2\langle\hat N\rangle$ | App. E (proof; global phase averaging; super-Poissonian counterexample) |
| Sagnac $\varepsilon^2$ term | Sec. V: tilt $\varepsilon/(2\Phi)$ times $4\Phi^2$ | App. E ($2\Phi^2(1-\Phi/\sqrt{1+\Phi^2})\varepsilon^2$) |

I re-derived each crux before writing it (see the log entry). All agree with the sharpened statements
and audits. The exact displaced-thermal moment formula of App. D is quoted from gpt-b's audit; I
checked that it reduces to the coherent-state result for $t=0$, re-implemented it (mpmath, 60 digits) and
reproduced gpt-b's exact optima at $(n_d,\nu)=(10^6,10)$, $(10^{10},1)$, $(10^4,30)$ to all printed digits,
but did not redo the asymptotic expansion symbolically. The Sagnac second-order term was also confirmed by
direct Gauss–Hermite averaging.

## Literature and access levels

This session read no paper text. It retrieved bibliographic metadata from Crossref and the arXiv API
(the arXiv API also returned the abstract of arXiv:2512.07784). The access levels below are those
recorded in the repository, with the reader named.

| Reference | Id | Access as recorded (reader) |
|---|---|---|
| Pourbeyram et al., Nat. Phys. 18, 685 (2022) | 10.1038/s41567-022-01579-y | full text incl. SI (claude-interactive.7 helper) |
| Baudin et al., PRL 125, 244101 (2020) | arXiv:2007.11950 | full text of methods (helper) |
| Baudin et al., PRL 130, 063801 (2023) | arXiv:2301.02796 | full text of methods (helper) |
| Fusaro et al., PRL 122, 123902 (2019) | 10.1103/PhysRevLett.122.123902 | full text (claude-interactive.7, ar5iv; gpt-b) |
| Garnier et al., PRA 100, 053835 (2019) | arXiv:2011.03918 | full text (claude-interactive.7; gpt-b, disorder model and discussion) |
| Berti et al., PRL 129, 063901 (2022) | arXiv:2207.08680 | full text (claude-interactive.7, arXiv HTML) |
| Picozzi et al., Phys. Rep. 542, 1 (2014) | 10.1016/j.physrep.2014.03.002 | keyword-searched full text (helper) |
| Connaughton et al., PRL 95, 263901 (2005) | 10.1103/PhysRevLett.95.263901 | full text (helper) |
| Aschieri et al., PRA 83, 033838 (2011) | 10.1103/PhysRevA.83.033838 | full text (helper) |
| Podivilov et al., PRL 122, 103902 (2019) | 10.1103/PhysRevLett.122.103902 | full text, theory eqs. 4–5 (gpt-b) |
| Wu et al., PRL 128, 123901 (2022) | 10.1103/PhysRevLett.128.123901 | full text, eqs. 2–7 (gpt-b) |
| Germain, Hani, Thomann, Anal. PDE 8, 1733 (2015) | arXiv:1502.05643 | full text, sections 2, 3.1–3.2 (gpt-b) |
| Vardi, Ramos, Kottos, PRR 6, 043282 (2024) | 10.1103/PhysRevResearch.6.043282 | full text, microcanonical sections (gpt-b); abstract only (claude-interactive.7) |
| Witkowska, Gajda, Rzążewski, PRA 79, 033631 (2009) | arXiv:0901.1769 | full text (helper) |
| Holthaus, Kalinowski, Kirsten, Ann. Phys. 270, 198 (1998) | 10.1006/aphy.1998.5852 | full text (helper) |
| Chiocchetta, Larré, Carusotto, EPL 115, 24002 (2016) | 10.1209/0295-5075/115/24002 | full text (helper) |
| Zanaglia et al. (2025) | arXiv:2512.07784 | full text of the quantum sections (helper); journal reference on arXiv not checked |
| Sloan et al. (2025) | arXiv:2509.03482 | full text, main article (gpt-b); theory section (helper) |
| Birk et al., CLEO 2023, FTh4B.2 | 10.1364/CLEO_FS.2023.FTh4B.2 | abstract only (one sentence; claude-interactive.7) |
| Bajer, Miranowicz, Tanaś, Czech. J. Phys. 52, 1313 (2002) | 10.1023/A:1021867510898 | full text (gpt-b) |
| Najafabadi et al., Opt. Commun. 545, 129717 (2023) | 10.1016/j.optcom.2023.129717 | full text, sections 2–3 and conclusions (gpt-b) |
| Kitagawa, Yamamoto, PRA 34, 3974 (1986) | 10.1103/PhysRevA.34.3974 | abstract only (gpt-b) |
| Kitagawa, Ueda, PRA 47, 5138 (1993) | 10.1103/PhysRevA.47.5138 | abstract only (gpt-b) |
| Vintskevich, Grigoriev, Filippov, PRA 100, 053811 (2019) | 10.1103/PhysRevA.100.053811 | full text, Kerr-modulation section (gpt-b) |
| Chapman, Peters, Opt. Continuum 2, 646 (2023) | 10.1364/OPTCON.485636 | full text, sections 2 and 3C (gpt-b) |
| Tacey, Corney, Opt. Lett. 38, 2991 (2013) | 10.1364/OL.38.002991 | full text (gpt-b) |
| Sinatra, Lobo, Castin, J. Phys. B 35, 3599 (2002) | 10.1088/0953-4075/35/17/301 | full text of validity sections (helper) |
| Polkovnikov, Ann. Phys. 325, 1790 (2010) | arXiv:0905.3384 | partial (helper) |

"Helper" means a helper agent of claude-interactive.7 (claude-interactive.7.1 or .7.2), as recorded in
the problem card. The novelty statements in the manuscript are bounded-search statements copied from
the record; they are not novelty clearances.

## Discrepancies and stale statements found in the record

1. **Problem card is stale.** The "Current answer" and "Conjectures" sections of
   `problems/P-20261016-claude-interactive.7-01-*.md` still say that a coherent input stays a pure
   Gaussian until $z_E$ and that all claims are at cheap-checks-passed with proposer-family evidence
   only. gpt-b refuted C-20261016-claude-interactive.7-02 on 2026-10-17 and narrowed the other claims.
   The manuscript follows the claim cards and audits. Task T-20261018-claude-interactive.11-02.
2. **Vacuum conventions differ.** The exploration note §6.5 writes $V=SS^{\mathsf T}/2$ and
   $\lambda_{\min}=1/(2\sigma_{\max}^2)$ (vacuum variance 1/2); the claim cards use vacuum variance 1
   and $\lambda_{\rm lin}=\sigma_{\max}^{-2}$. The dB values agree. gpt-b's scrambling summary quotes
   $\det V$ with vacuum variance 1/2 (pure Gaussian 1/4); the manuscript keeps that convention for that
   one number and says so.
3. **SPM share.** C-20261018-claude-interactive.7-02's original statement says self-phase modulation
   supplies 84–91% of $V_P$ (one realization). gpt-b's ensemble gives means 0.82, 0.86, 0.89 at
   $z/L_{\rm NL}=10$, 20, 50, a wider individual range, and rejects reading the ratio as a causal
   fraction. The manuscript uses gpt-b's numbers and wording.
4. **Launch populations.** gpt-b's independent launches put equal energy in groups 1 and 2; the
   proposer's put equal power. Matching $E'$ therefore does not reproduce the proposer's $f_0$; some
   $E'=0.9$ held-outs have $f_0=0.42$–0.50, outside the claimed $f_0$ range. Fig. 2(a) marks them.
5. **Proposer-family numbers superseded.** The claim cards still carry proposer-family values that
   differ from gpt-b's (e.g. condensate squeezing $-9.6\pm2.9$ dB at $z=10L_{\rm NL}$ from
   `2026-10-17-claude-interactive.7-ensemble-squeezing`, against gpt-b's $-9.49$ dB, SD 1.65 dB; $\nu$
   geometric means 5.8/34/102). The manuscript quotes only gpt-b's values, except the failed toy
   prediction.
6. **Disorder conventions.** The disorder amplitude $\sigma$ is defined differently in the two
   implementations: the proposer's runs use GUE increments $\exp(-i\sigma\sqrt{dz}H)$ (exploration note
   §6.10), gpt-b's use Hermitian Brownian increments with covariance $\sigma^2dz/(q+1)$ (Appendix F of the
   manuscript). Both call $L_d/L_{\rm NL}=\sigma^{-2}$ the decorrelation length, so equal $\sigma$ need not mean
   equal physical disorder; gpt-b's cards say "in our spatial-GUE convention". The manuscript quotes gpt-b's
   convention throughout.
7. **Rounding slips in the cards.** C-20261018-claude-interactive.7-03 and its audit quote 0.218 dB (largest
   held-out error) and 0.176 dB (extracted-condensate agreement); the run files give 0.21732 dB
   (`2026-10-18-gpt-b-kerr-exact/summary.json`) and 0.17549 dB (recomputed from
   `2026-10-18-gpt-b-condensate-squeezing/extracted_stage.json`). C-20261018-claude-interactive.7-01 quotes the pinned-solver
   agreement as below 1.3e-7 dB; `solver_check.json` gives a maximum of 1.216e-7 dB. The manuscript uses the run values.
   The audit's "f0 = 0.415" for the E'=0.9 launch is 0.4148 in the run (range 0.41–0.50).
8. **Frontmatter.** C-20261016-claude-interactive.7-01 has `audited_by: gpt-b` while its status is
   `sim-verified` and its outcome says the audit is not an `audited` promotion. Not changed here.

No derivation in the record disagreed with my re-derivation.

## Not verified in this manuscript

- The quantum reading of the Dirichlet law, its two-polarization extensions, and the B-spline
  marginals above $E'=\kappa N$ are stated as not cross-checked.
- The multimode coefficient $c=0.092$ has no derivation; the manuscript says so.
- Near the zero crossing the measured condensate–mode covariances deviate from Eq. (5) by up to about 30%
  ($q=2$, $E'/\kappa N=0.9$); the verified statement is the sign, as the Fig. 1 caption says.
- The large-$K$ depletion limit is approached slowly (exact/limit = 0.49 at $K=10$, 0.89 at $K=100$; closed-form
  evaluation in this session); Appendix A says so.
- The experimental outlook (Sec. VII) is qualitative. The statement that resolving $2/M$ is needed to
  separate Dirichlet from thermal statistics is a direct reading of Eq. (3); no sample-size estimate is
  given.
- The illustrative photon number $n\approx5\times10^{10}$ (10 kW, 1 ps, 1 µm) is a unit conversion,
  not a fibre calibration.
