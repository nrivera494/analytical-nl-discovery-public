---
date: 2026-10-16
agent: claude-a
model: claude-opus-5-5
family: claude
task: T-20261016-claude-interactive-02
duration_min: 240
---

## Did

Round 5, full loop, on P-20261016-claude-interactive-03 (efficiency–shift–jitter frontier of Raman-soliton conversion, and the headroom of input shaping). The branch is stacked on PR #44 (`task/T-20261016-claude-interactive-01`), which carries the card.

Everything is in run `2026-10-16-claude-a-raman-soliton-frontier`. Predictions were frozen in its `HYPOTHESES.md` before the matching computation. Each freeze lists what had been seen.

| Freeze | Hypotheses | Commit |
|---|---|---|
| 1 | H1a–c, H2, H3a–d, H4 | 3af8dfa |
| 2 | H3e | 94bd1ac |
| 3 | H3f | d11ec48 |
| 4 | H3g | 5628392 |
| 5 | H3h | fa39dd9 |
| 6 | H1c′ | 4592262 |
| 7 | H2b | 3b5c666 |
| 8 | H3i | 3a4a64a |
| 9 | H3j, H4b | 73e23c6 |
| 10 | H4c | e94b6d7 |
| 11 | H3k | 99ab7d9 |
| 12 | H3m | c2e18dc |
| 13 | H5a | a3e68a1 |
| 14 | H3n | 2f0357e |
| 15 | H3o, H3p | 995962c |
| 16 | H5b | 93284ae |
| 17 | H3q | 4a74fe8 |
| 18 | H5c | f0e1bce |
| 19 | H2c | 9294ffa |
| 20 | H4d | acd072a |
| 21 | H4e | 09ea231 |
| 22 | H3r | 047c44d |
| 23 | H4f, H4g | 5a65a06 |
| 24 | H3s | 81518cc |
| 25 | H4h | e01d626 |

Two disclosures:
- A self-test printed one Gaussian-launch value before any Gaussian freeze, so the peak-4 Gaussian scan is labelled an exploration.
- The H3o freeze text first contained a hand-estimated $T_R$ (0.12 fs instead of the computed 0.21 fs). It was corrected in 500d29b; the predictions do not use it.

Code, in Python 3.9 with numpy/scipy:
- **Solvers.**
  - `zs.py`: ZS eigenvalues by Fourier collocation, shift-invert, analytic gradient, WKB value.
  - `gnlse.py`: soliton-unit GNLSE, RK4IP, exact single-oscillator Raman transfer function, optional self-steepening and $\delta_3$.
- **H1:** `h1_tests.py`, `h1c_lorentz_window.py`, `h1c_narrow.py`.
- **H2:** `h2_opt.py`, L-BFGS-B with analytic gradient over phase-only and passive classes.
- **H3:** `h3_scan.py`, `h3_ext.py` (many modes), `h3_analysis.py`, `h3_beta3_measure.py`, `h3_peaks_diag.py` (soliton census), `figure_collapse.py`.
- **H4:** `h4_opt.py` (Powell), `h4_grad.py` (forward-difference L-BFGS), `h4_scan6.py`, `h4_recheck.py`, `h4_adjoint_measure.py`.
- **Summary:** `make_summary.py`, `figures_h4_h5.py`.

Julia, with FastDifferentiableMMNLO agents' copy b9fa957 (clean, unmodified):
- `solver_check.jl`: second implementation;
- `h5_jitter.jl` and `h5_jitter_fixedshift.jl`: discrete adjoint, symmetrized Raman bath copied from solver branch `task/T-20261004-gpt-b-02`;
- `h4_adjoint.jl`: adjoint-gradient mask optimization, gradient checked against finite differences to $10^{-9}$.

**Memory rules (orchestrator message, received 14:53 EDT).** Acknowledged and applied from then on:
- one heavy process at a time;
- about 3 GB per process;
- check `memory_pressure` before each launch, and wait if free memory is below 35%;
- dense eigenproblems no larger than about 4096²;
- time grids of $2^{14}$ points or fewer unless a convergence test demands more;
- no full z-histories kept in memory;
- mask optimizations one start at a time.

When the message arrived, none of my jobs was running and system free memory was 45%. I launched nothing after it.

Earlier runs that would not meet these rules:
- **Concurrency.** Up to 8 Python jobs and 2 Julia jobs ran at once.
- **Grid size.** 32768- and 65536-point grids were used for $N\ge7$ and $N=10$. Larger grids are needed there because of the aliasing found at $N\ge7$ (`h3_peaks_N8_T400.json`). Follow-ups should state that justification.
- **Eigenproblem size.** The sketch-3 window check used dense $6144\times6144$ eigenproblems (`sketch3_window_check.json`). A shift-invert solver should be used instead.
- **z-histories.** The H5 jitter runs held subsampled z-trajectories in memory: every 4th–8th step, at most about 0.1 GB per array.

## Found

**H1 (ZS bounds).**
- H1a ($\eta\le\|q\|_\infty$) and H1b (TL maximizes $\|q\|_\infty$ and $\int|q|^4$ under passive masks): proved, and hold on every tested potential.
- H1c, the WKB value as an upper bound: **refuted** (Lorentzian, window-converged).
- H1c′, the narrowed form for exponential tails: **refuted** on held-out shapes.
- **The card's sketches.** Sketches 1 and 2 are proved as H1a and H1b. Sketch 3 (chirped-sech eigenvalues $i(\sqrt{A^2-C^2/4}-\tfrac12-k)$) is reproduced numerically. Near-threshold eigenvalues need a wide window (`sketch3_*.json`).

**H2.** Claim C-20261016-claude-a-01. The TL launch maximizes the leading ZS eigenvalue over phase-only and passive masks.
- 100 optimizations: sech and Gaussian at $A=1.5$–6, plus held-out asymmetric and flat-top spectra.
- 1188 random sharp-featured masks (H2c).
- The largest excess over TL is $1.3\times10^{-15}$, so the integrable headroom is 1, not $2N/(2N-1)$.

**H3 (Raman-transfer excess of the leading fission soliton).** Claim C-20261016-claude-a-02. 70 $(N,T_0)$ points for Blow–Wood, 106 with other responses.
- (a) **Long pulses:** $\varepsilon\simeq c_NT_R/T_0$, linear on average. Average exponents are 1.00, 1.12, 1.01 and 1.01 for $N=2$–5 over factor-4–8 ranges of $T_0$.
  - $c_2=4.89$, flat.
  - For $N\ge3$, $c_N$ fluctuates non-monotonically by about ±7% ($c_3\approx18$, $c_4\approx76$, $c_5\approx145$). H3r, which predicted monotone $c_3$ and $c_5$, is refuted.
- (b) **Maximum** where the compressed-soliton bandwidth $N^2/T_0$ meets the Raman gain peak $1/\tau_1$: $N^2\tau_1/T_0^*=0.78$–1.30 for $N=2$–8 and five Raman responses (four single-oscillator, plus Lin–Agrawal). For silica this is $T_0^*\approx21\,{\rm fs}\,N^{1.62}$.
  - $T_0^*$ tracks $\tau_1$, not $T_R$.
  - The $N=8$ peak and the held-out As2S3-like peaks were predicted within 4%.
- (c) **Peak content** $f_1^*\approx1.29/\sqrt N$. $f_1^*\sqrt N=1.27$–1.30 for $N=3$–10. It changes by $-4\%$ to $+2.4\%$ across five Raman responses, including Lin–Agrawal (H3s confirmed), and lies above the passive-mask input bound $2/N$ for $N\ge3$.
  - Corollary: $E_1^{\max}\approx1.5N^{-0.12}|\beta_2|/(\gamma\tau_1)$, about 1.7–1.8 nJ in SMF-28 for $N=3$–6 (against 1.0–1.35 nJ from IST).
- (d) **Self-steepening** acts only through the quantum defect: the photon fraction is unchanged within 1%, and within 0.25% at the maximum (H3q).
- **Checks.**
  - Second implementation (FastDifferentiableMMNLO): agrees to $\le8\times10^{-4}$, including $N=6$ on the transfer maximum ($2.2\times10^{-4}$).
  - Convergence: unchanged to 5–6 digits at $(4,200)$, $(6,400)$ and $(8,200)$.
  - Step convergence at small $\tau_R$.
  - Leading-soliton census at $(5,280)$ and $(6,400)$.
  - Aliasing artefact at $N\ge7$ found and removed with 32768-point grids.
  - $\beta_3$ ($\delta_3\le0.05$): the local-dispersion content rises by 1.6–11%.
- **Refuted along the way:**
  - H3b as a global law;
  - H3c;
  - H3e at $(6,800)$;
  - H3g(iii) ($c_4$);
  - H3i(ii);
  - H3k (position from $T_R$ alone);
  - H3o at $N=4$ (value, by 0.05%);
  - H3p ($c_5=140<150$);
  - H3r ($c_3$ and $c_5$ non-monotone).
- **Held-out N = 10** (the verifier prediction frozen in C-20261016-claude-a-02 at aa10039): $f_1\sqrt{10}=1.269$ at 870 fs, inside the frozen [1.20, 1.38].
- **Confirmed held out:**
  - H3e (3 of 4), H3f, H3g(i–ii), H3h, H3i(i) ($N=7$);
  - H3j ($N=3.5$), H3k (value), H3m ($N=8$ peak);
  - H3n (Gaussian launch);
  - H3o ($N=3$ value; positions);
  - H3q;
  - H3s (Lin–Agrawal).

**H4 (phase-shaping headroom in the GNLSE).** C-20261016-claude-a-03 is **refuted** (filed with status `refuted`), and C-20261016-claude-a-04 is new.
- **Small bases.** Powell over 5 phase coefficients found small gains:
  - $+0.35$, $+1.04$ and $+0.77\%$ for $N=2,3,4$ at 100 fs;
  - $+3.5\%$ at the transfer maximum ($N=4$, 200 fs).

  These, together with a TOD measurement trap (the nominal-$\beta_2$ ZS content rewards masks that reduce the red shift), led to the draft claim "headroom $<5\%$".
- **Larger bases refuted it.**
  - L-BFGS with forward-difference gradients over 11 coefficients at $N=4$, 100 fs: $+6.2\%$ from TL, $+9.0\%$ from the Powell optimum. Both verified saturated in $L$, step-converged, and clean in the census.
  - The solver's discrete-adjoint L-BFGS over 15 coefficients (gradient checked to $10^{-9}$) at $N=4$, 200 fs: $+7.0\%$ (TL start) and $+6.7\%$ (random start). Re-measured in numpy with the ZS content.
  - No search is converged.
  - Together these refute the frozen "$<5\%$ for $N\ge3$", H4b and H4c.
- **C-04.** The achievable headroom is $\ge9.0\%$ (100 fs) and $\ge8.2\%$ (200 fs; two warm-started continuations of the adjoint, with diminishing gains 7.0 → 8.0 → 8.2%) at $N=4$, with explicit masks.
  - Robustness: H4d (masks A, B) holds under self-steepening and in 3 of 4 cases at $\pm10\%$ $T_0$. H4f and H4h (masks A2, B2) hold under self-steepening (photon gains $+8.2\%$, $+8.8\%$) and in all four $\pm10\%$ $T_0$ cases ($+6.5$ to $+9.1\%$).
  - At $N=3$ the gain stays small: $+1.13\%$ (100 fs) and $+1.94\%$ (140 fs), which refutes H4e ($\ge3\%$).
  - At $N=5$ (280 fs) a reduced search finds $+5.6\%$, confirming H4g ($\ge3\%$).
  - With mask A2 the leading soliton also ends further red-shifted, so it improves both efficiency and shift.
  - The card's conjecture (bound 1.48–1.68) holds: the largest gain found is 1.090.
- **Other runs:** the passive class at $N=3$ gives $+1.09\%$; $\delta_3=0.05$, re-measured with the local-dispersion ZS, gives $N=3$ $-0.4$ to $+1.6\%$ and $N=4$ $+2.85\%$.

**H5 (jitter, exploration).** `explorations/2026-10-16-claude-a-leading-soliton-jitter.md`.
- Validated against SPT for $N=1$: vacuum within 1.2%; Raman 8–9% above the thermal-limit formula.
- **Same length and peak power:** $R_{\rm tot}=0.73\to0.54$ for $N=2\to5$ (H5a confirmed).
- **Fixed red shift and peak power** (the card's comparison): the fission-generated leading soliton is 5× ($N=2$) to 40× ($N=5$) quieter than a directly launched fundamental soliton at $T_0=100$ fs ($R_{\rm tot}=0.197$, 0.156, 0.049, 0.023).
  - H5b's power-law windows for $N=4$, 5 are refuted (the advantage grows faster). The qualitative "≥4×" is confirmed.
  - At the transfer maximum: 0.234 ($N=3$, 140 fs) and 0.165 ($N=4$, 200 fs), confirming H5c.
  - Post hoc: $R_{\rm tot}\approx0.55(L/L_b)^3$.

## Changed

- New run folder `runs/2026-10-16-claude-a-raman-soliton-frontier/`: scripts, logs, json, `HYPOTHESES.md`, `meta.yaml`, `config.yaml`, `summary.json`, `h3_summary.json`, figures (`h3_excess.png`, `h3_collapse.png`, `h4_headroom.png`, `h5_jitter_ratios.png`).
- New claims:
  - C-20261016-claude-a-01 (`proposed`);
  - C-20261016-claude-a-02 (`proposed`);
  - C-20261016-claude-a-03 (`refuted` by my own larger-basis searches; kept);
  - C-20261016-claude-a-04 (`proposed`).
- New exploration: `explorations/2026-10-16-claude-a-leading-soliton-jitter.md`.
- New tasks: T-20261016-claude-a-01 … 08.
- `tasks/T-20261016-claude-interactive-02*.md`: `status: done`.
- **Bugs found and fixed during the session**, all recorded with their retained files in `meta.yaml`:
  1. `gnlse.photons` had the wrong sign of $sW$; only a printed diagnostic was affected.
  2. The H2b spectral lasers had the wrong FFT ordering; rerun, broken logs kept.
  3. H5: a z-sample mismatch.
  4. `Optim.only_fg!` was not found.
  5. An unguarded import re-ran a script into a wrongly named file. That duplicate was deleted at once, and the import is now guarded.
- **Stopped run:** the $N=3$ adjoint H4 run, stopped to free a Julia slot, with no result. Recorded in `meta.yaml`.

## Not verified

- No H4 optimization is converged, and the landscape is rugged (different starts reach different optima). The true headroom at $N=4$ is likely above 9%.
- $c_N$ for $N\ge3$ fluctuates with $T_0$. Its asymptotic value, and the cause of the fluctuation, are not established.
- No derivation of $c_N$, of the exponent 1.62, of $y^*\approx1$, or of $1.29/\sqrt N$. There are scaling arguments for the exponent 1 of (a) and for the $\tau_1$ dependence of (b).
- H1a and H1b proofs: no other agent has checked them.
- **Novelty.** Kormokar et al. was read through PDF text extraction; its Fig. 3 was not viewed (task T-20261016-claude-a-07).
- **Physical validity at large $N$, $T_0$.** Red shifts up to 0.4 rad/fs, where the constant-$\beta_2$, single-oscillator model is not credible. The excess saturates at fission, but it has not been checked with full $\beta(\omega)$, $\gamma(\omega)$ and a multi-peak response (task T-20261016-claude-a-08).
- **H5** is not yet at fixed efficiency, and has no theory.

## Loose ends

- T-20261016-claude-a-01: verify C-20261016-claude-a-01 (`family_required: gpt`).
- T-20261016-claude-a-02: verify C-20261016-claude-a-02 (`family_required: gpt`).
- T-20261016-claude-a-03: verify C-20261016-claude-a-04 and the refutation of C-20261016-claude-a-03 (`family_required: gpt`), with a converged large-basis adjoint optimization.
- T-20261016-claude-a-04: H5 follow-up (fixed efficiency, frequency jitter, shaped launches, theory of the $(L/L_b)^3$ law).
- T-20261016-claude-a-05: derive $c_N$ and the peak law.
- T-20261016-claude-a-06: prove or refute TL optimality of $\eta_{\max}$.
- T-20261016-claude-a-07: Kormokar et al. Fig. 3 and the collision-transfer literature (`family_required: not-claude`).
- T-20261016-claude-a-08: realistic fibre (full dispersion, multi-peak Raman, loss).

## Proposed card changes

For P-20261016-claude-interactive-03. I did not edit the card.
1. **Sketch 1.**
   - Add that the bound is not attained: the TL launch maximizes the leading eigenvalue over $\mathcal S_\phi$ and $\mathcal S_{A\phi}$ in every test (C-20261016-claude-a-01).
   - Replace "$H_{\mathcal S_{A\phi}}\le2N/(2N-1)$" with "$\le2N/(2N-1)$ (proved); $=1$ numerically".
   - Note that the WKB value is not an upper bound.
2. **"What may escape the bound."** Quantify the Raman escape by C-20261016-claude-a-02:
   - excess linear in $T_R/T_0$ for long pulses;
   - maximum where $N^2\tau_1/T_0\approx1$;
   - peak fraction $\approx1.29/\sqrt N$, above $2/N$ for $N\ge3$;
   - in physical units, $E_1^{\max}\approx1.5N^{-0.12}|\beta_2|/(\gamma\tau_1)$.

   The efficiency side of the frontier at fixed $L$ is therefore set by the launch duration relative to the Raman gain-peak time, not by input soliton content.
3. **Conjectures.** Record the first conjecture as tested and holding: the largest gain found is 1.070, against a bound of 1.68.
   - Add that the headroom is **not** small at $N=4$: smooth phase masks reach at least 9% (C-20261016-claude-a-04), and small mask bases underestimate it (C-20261016-claude-a-03, refuted). At $N=3$ it is about 2%.
   - Suggest restating the open question as "converged headroom of phase and passive masks near $T_0^*$, and its $N$-dependence".
4. **Merged jitter part.** Add the H5 exploration.
   - At fixed red shift and peak power, the fission source is 5–40× quieter ($N=2$–5) than a direct fundamental-soliton launch.
   - The fixed-efficiency comparison is open (T-20261016-claude-a-04).
5. **Literature:**
   - add Kim, Lee & Lyng, arXiv:1310.4145, full text;
   - add Luan et al., Opt. Express 14, 9844 (2006), DOI 10.1364/OE.14.009844, abstract only;
   - note the fitted factor of 10 in Kormokar et al. (2023), and that they treat IST as the long-pulse asymptote.
6. **`claims:` list:** add C-20261016-claude-a-01, -02, -03 (refuted), -04.

## Literature

- Kormokar, Shamim & Rochette, JOSA B (2023), DOI 10.1364/JOSAB.478975, arXiv:2301.02945. **Full text** (arXiv PDF via text extraction, sections 1–6; figures not viewed).
  - Analytic interpulse-Raman correction to the IST efficiency, with a numerically fitted factor of 10.
  - The excess grows with $N$ and with decreasing duration; IST is the long-duration asymptote.
  - $N=6$: 53.0% at 700 fs FWHM, 50.0% at 400 fs.
  - Experiment: 50.6% at $N=5.57$, 938 fs.
  - Their As2S3 response parameters were used for H3o.
- Kim, Lee & Lyng, arXiv:1310.4145 (2013). **Full text** (text extraction; sections 1–3 read). Klaus–Shaw theorem as quoted there; WKB eigenvalues converge as $O(\epsilon^2)$ for a Gaussian.
- Klaus & Shaw, PRE 65, 036607 (2002), DOI 10.1103/PhysRevE.65.036607. **Not accessed** by me; content as quoted by Kim et al. and the card.
- Luan, Skryabin, Yulin & Knight, Opt. Express 14, 9844 (2006), DOI 10.1364/OE.14.009844. **Abstract only** (search result).
- Drummond & Corney, JOSA B 18, 139 (2001), and Corney & Drummond, JOSA B 18, 153 (2001). **Not accessed** by me. The SPT formulas used for the $N=1$ validation are those coded in the solver's `soliton_jitter.ipynb`.
- **Searched for a stated bound $\mathrm{Im}\,\zeta\le\|q\|_\infty$:** query "Zakharov-Shabat eigenvalues bound imaginary part sup norm potential". Results pointed to Deift–Venakides–Zhou shadow-bound statements, but no explicit statement was found in what I could open.
