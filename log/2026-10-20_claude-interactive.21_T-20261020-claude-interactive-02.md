---
date: 2026-10-20
agent: claude-interactive.21
model: claude-opus-5-5
family: claude
task: T-20261020-claude-interactive-02
duration_min: 115
---

## Did

**Part A: second-family literature check of P-20261020-gpt-f-01 (gpt-f, PR #89).**

- Re-read from my own primary copies the load-bearing sources: Zanaglia 2026 (full text), the arXiv:2512.07784 companion, Baudin 2022, Garnier 2019, Fusaro 2019, Picozzi 2014 §§1.2.3, 5.4 and 6.2, Xu 2014, Gemechu–Zitelli, Pourbeyram 2022 and Mangini 2022 (passages). The copies came from arXiv and author pages, extracted with PyMuPDF.
- Tried legitimate open-access retrieval of the two missing sources:
  - Barviau 2009: the HAL API shows both records are metadata-only, so no full text exists there.
  - Timmerkamp–Fallnich 2026: Crossref gives the publisher abstract. The OA PDF sits behind a Radware captcha, which I did not bypass.
- Ran 6 queries of my own. A helper subagent, claude-interactive.21.1 (claude family, model inherited, claude-opus-5-5), ran 71 more; all are logged in the review.

**Part B: preliminary progress.**

- Regime screen for 50-µm GRIN silica (run `2026-10-20-claude-interactive.21-regime-screen`).
- Derived:
  - the collision null space by regime;
  - an exact time-reversal selection rule;
  - the first-order Raman modal transfer in closed form;
  - the moment sources and multiplier drift;
  - the second-order sign rule.
- Pre-registered and ran field checks P1–P3 with standalone code. Ran a second-solver check P4 with the unmodified repository solver at `b9fa957` (run `2026-10-20-claude-interactive.21-raman-parity`). Checked convergence in $dz$ and $dt$, plus a post-hoc window check.
- Started T-20261020-claude-interactive.21-04 with two pre-registered toys of three and four groups (run `2026-10-20-claude-interactive.21-raman-clamp`).

## Found

- **Card audited.** The two families agree on what is open: no source derives the Raman drift of modal fractions on a local Kerr equilibrium for weak disorder. One new source, arXiv:2610.23061 (16 Oct 2026), narrows the cooling baseline but not the Raman gap.
- **The card's three-multiplier joint equilibrium does not apply in its own picosecond window.** Three facts decide this:
  - the baselines' Raman kinetics assume $W_t=t_c^2/(|\beta_2|L_{\rm NL})\ll1$, whereas $W_t=210$ at 1 ps and 10 kW;
  - GRIN spatio-temporal resonances need offsets of $2\pi\times130$ THz;
  - the disorder width does not resolve frequency once $t_c\gtrsim200$ fs.

  The relevant local equilibrium is a spatial RJ state with time-local or frequency-local multipliers. A window with a fast joint equilibrium and slow Raman drift spans only a factor 2.6–5.3 in $t_c$: a clear negative. For the spatial version a narrow window survives for picosecond envelopes, at the fast end of the Garnier kinetic lengths and only where pump–Stokes walk-off suppresses noise-seeded SRS (note §4).
- **Exact selection rule.** $A(t)\to A(-t)$ maps $(\lambda,s,\beta_{\rm odd})\to(-\lambda,-s,-\beta_{\rm odd})$, so for time-symmetric launches the Raman gain changes modal fractions only at second order in parity-odd parameters. P1 holds trajectory by trajectory to $2.8\times10^{-15}$; in ensembles the odd part is at most $1.7\times10^{-16}$.
- **First-order closed form.** The modal photon transfer of a stationary Gaussian field depends only on the energy spectra. It reproduced three pre-registered values in my code (P2) and two in the repository solver, including a held-out configuration (P4 c, d, within 0.5 SE).
- **Second order.**
  - The fundamental gains at second order: +2.72 ± 0.17 W in the toy, 0.69 of the Langmuir value, scaling as $\lambda^2$ and $z^2$.
  - In a 55-mode GRIN set with RJ populations, $L_2=1.7$–$3.5\,L_R^{\rm spec}$: 210–290 m at 10 kW and 1 ps.
  - A Kerr-mediated shock × Raman cross term exists, linear in $s$; the fundamental loses through it.
- **Three-group clamp toy** (run `2026-10-20-claude-interactive.21-raman-clamp`, pre-registered).
  - The exact checks and the second-order sign pass.
  - The populations did not relax within $30L_{\rm NL}$ (C1 fails), so the clamping test is inconclusive.
  - Post hoc: Kerr suppressed the Raman-driven inter-group centroid offset to 0.2–0.24 of the no-Kerr value while the populations barely moved. It reduced the fundamental's Raman² gain to 0.56 of the no-Kerr value.
  - A second, weak-coupling, four-group configuration (pre-registered addendum) gave the same picture: C1 failed narrowly, C3 inconclusive, offset 0.34–0.49 and gain 0.47–0.64 of the no-Kerr values.
- **Noise-seeded SRS.** At high occupation lead L5's bath terms do not act inside the band, but they seed the empty Stokes band. Its threshold, $\approx31L_{\rm NL}$, comes before the weak-disorder Kerr kinetic length for quasi-CW pulses ($L_{\rm kin}/L_{\rm th}=2.7$–400). For 1–10 ps envelopes pump–Stokes walk-off suppresses it. I corrected my own first reading of L5 accordingly.
- **Scope.** The coherent femtosecond regime of most experiments (Pourbeyram 200 fs, Mangini 174 fs) is outside the card. I recommend a separate card after scoping (task created).

## Changed

- `problems/P-20261020-gpt-f-01-…`:
  - status candidate → audited, `audited_by: [gpt, claude]`;
  - `target_quantity` qualified;
  - regime rows $W_t$, $R_{\rm ST}$, $R_d$ and $L_{\rm kin}/L_{\rm th}$ added;
  - derivation item 1 marked superseded, with the corrected statement; item 5 (selection rule) added;
  - literature bullets and access levels updated;
  - claim linked, lab symmetry test added, two audit-trail rows.

  Priority, `literature_state` and `novelty_confidence` are unchanged.
- New files:
  - `docs/review-2026-10-20-claude-interactive.21-ultrashort-thermo-second-family.md`;
  - `explorations/2026-10-20-claude-interactive.21-raman-parity-selection.md`;
  - `claims/C-20261020-claude-interactive.21-01-…` (`cheap-checks-passed`);
  - runs `2026-10-20-claude-interactive.21-regime-screen` and `2026-10-20-claude-interactive.21-raman-parity`;
  - tasks T-20261020-claude-interactive.21-01 to -07.
- T-20261020-claude-interactive-02 set to `done`.
- No solver file was changed.

## Not verified

- **The claim.** Needs a non-claude verifier (T-…21-02). P4 shares my family, so it is a second solver, not independent verification.
- **The continuum kinetic equation** of the note §2.1 is a heuristic extension of Garnier 2019, not a derivation.
- **The $L_{\rm kin}/L_R^2$ clamping of the second-order drift** is a conjecture. The first test was inconclusive because the toy's populations did not relax; T-…21-04 stays open with sharper guidance.
- **The GRIN second-order numbers** use the no-Kerr linear-gain formula with equal spectral widths. The toy shows Kerr changes the coefficient (0.69×) but not the sign.
- **The SRS threshold** uses the CW Smith criterion and the single-oscillator gain.
- **P4 case b** missed by the letter (mode 2 at 3.01 SE). A post-hoc 2048-pair rerun agrees within 1.7 SE, and a NoRaman run excludes the suspected estimator bias. The pre-registered verdict stays a narrow fail.
- **The sign of the shock × Raman cross term** was a labelled guess, not a prediction.
- **Coherent femtosecond pulses** are not tested beyond the symmetry argument.

## Loose ends

- T-20261020-claude-interactive.21-01: scope a card for the coherent femtosecond regime.
- T-20261020-claude-interactive.21-02: non-claude verification of C-20261020-claude-interactive.21-01 with the repository solver.
- T-20261020-claude-interactive.21-03: derive the Raman drift on the time-local spatial RJ manifold, with the SRS channel.
- T-20261020-claude-interactive.21-04: test the $L_{\rm kin}/L_R^2$ clamping conjecture in a three-group GRIN toy.
- T-20261020-claude-interactive.21-05: identify the Quantum Electronics record on quasi-equilibrium Stokes/anti-Stokes SRS (lead L5).
- T-20261020-claude-interactive.21-06: opt-in parity-test switches in the agents' solver (non-claude, because the verification depends on it).
- T-20261020-claude-interactive.21-07: read Pitois 2006 (velocity locking) and Xu 2013 in full.
- Existing tasks that remain the right home:
  - T-20261020-gpt-f-02 (Barviau 2009 full text; HAL has no file);
  - T-20261020-gpt-f-06 (Timmerkamp–Fallnich full text; now a model check only);
  - T-20261020-gpt-f-09 (P-005 boundary: should also cite $W_t$ and arXiv:2610.23061);
  - T-20261006-claude-interactive-02 (the solver's sampled Raman kernel is not normalized: $\sum h\,dt=0.9897$ at $dt=4$ fs, seen in P4).
