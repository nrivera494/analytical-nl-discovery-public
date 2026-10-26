---
id: C-20261016-claude-a-04
problem: P-20261016-claude-interactive-03
title: "Smooth spectral-phase masks raise the leading Raman soliton's energy by at least 8–9% over the transform-limited launch at N = 4 (explicit masks), far below the card's conjectured bound; at N = 3 the gain found is only about 2%, at N = 5 at least 5.6%"
type: bound
status: promoted
proposed_by: claude-a
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: gpt-a
verifier_family: gpt
audited_by: null
auditor_family: null
created: 2026-10-16
updated: 2026-10-19
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: R-0006
---

## Statement

**System.** A transform-limited sech laser with $N=4$ passes a smooth spectral phase mask $Q\to Qe^{i\phi(\omega)}$, with $\phi=\sum_mc_mP_m(\omega/\omega_c)$ (Legendre polynomials on the support $|Q|>10^{-4}\max$). It is launched into the Raman GNLSE of C-20261016-claude-a-02: Blow–Wood response, $\beta_2$ only, no self-steepening, no loss. The leading output soliton's energy fraction $f_1$ is measured at $L=4L_D/N$ by its ZS content.

**Claim.** The phase-shaping headroom $H_\phi=\max_\phi f_1/f_1^{\rm TL}$ is bracketed:

$$1.090\le H_\phi(N=4,T_0=100\,{\rm fs}),\qquad 1.082\le H_\phi(N=4,T_0=200\,{\rm fs}),$$
$$H_\phi<\frac{2N}{2N-1}\,(1+\epsilon^{\rm TL})=1.56\ \text{and}\ 1.68\quad\text{(the card's conjecture)}.$$

**Lower bounds.** They are achieved by explicit masks:
- **Mask A2** ($+9.0\%$ at 100 fs; orders 2–12; `h4grad_N4_T100_maskA2_coef.csv`): forward-difference L-BFGS started from the best Powell mask. It is dominated by a large quadratic term ($c_2=9.2$ rad) plus structured higher orders.
- **Mask A** ($+6.2\%$ at 100 fs; `h4grad_N4_T100_maskA_coef.csv`): the same search started from TL. Not converged ($|g|=0.22$).
- **Mask B3** ($+8.2\%$ at 200 fs; orders 2–16; `h4_adjoint_N4_T200_maskB3_coef.csv`, solver convention): a second 30-iteration continuation from B2. Saturated in $L$ ($4\to6\,L_D/N$: $-0.06\%$). Gains are diminishing (B, B2, B3: $+7.0$, $+8.0$, $+8.2\%$), so the 15-coefficient optimum is likely near 8–9%.
- **Mask B2** ($+8.0\%$ at 200 fs; `h4_adjoint_N4_T200_maskB2_coef.csv`): the adjoint L-BFGS continued for 30 more iterations from mask B. It is still not converged ($|g|=4\times10^{-3}$). Mask B2 is the one robustness-tested (H4f, H4h).
- **Mask B** ($+7.0\%$ at 200 fs; `h4_adjoint_N4_T200_bestmask_coef.csv`): L-BFGS with the solver's discrete adjoint from TL. A random start reached $+6.7\%$.

None of the searches is converged, and different starts reach different optima (a rugged landscape). The true headroom is likely larger.

**N-dependence.**
- At $N=3$ the same 11-parameter search found only $+1.13\%$ (100 fs, converged) and $+1.94\%$ (140 fs, near the transfer maximum). H4e, which predicted $\ge3\%$ there, is refuted.
- At $N=5$ near its transfer maximum (280 fs), a reduced search (orders 2–8, 12 iterations, from TL) found $+5.6\%$ (H4g, which predicted $\ge3\%$, confirmed). The mask is in `h4grad_N5_T280_mask_coef.csv`. The result is saturated between $L=4$ and $6\,L_D/N$; at $8\,L_D/N$ the soliton wraps around the periodic window and that row is discarded.

So the large headroom appears from $N=4$ on and persists at $N=5$.

With mask B3 at the Raman-transfer maximum ($T_0=200$ fs, $N^2\tau_1/T_0=0.98$), the leading-soliton fraction reaches 0.697, i.e. $f_1\sqrt N=1.39$. This is 8% above the TL peak law $1.29/\sqrt N$ of C-20261016-claude-a-02. With mask A2 at 100 fs the fraction is 0.651, above even the TL optimum over pulse duration (0.644 at 200 fs).

**Robustness** (held out; frozen as H4d, H4f, H4h):
- With self-steepening the photon-number gains are $+6.6\%$ (A) and $+8.0\%$ (B) (H4d). For the later masks they are $+8.2\%$ (A2) and $+8.8\%$ (B2) (H4f).
- At $\pm10\%$ $T_0$ (H4h), mask A2 gives $+7.4\%$ (90 fs) and $+8.4\%$ (110 fs), and mask B2 gives $+6.5\%$ (180 fs) and $+9.1\%$ (220 fs).
- At $\pm10\%$ pulse duration with the mask fixed, mask B gives $+5.5\%$ and $+8.2\%$. Mask A gives $+3.0\%$ ($-10\%$) and $+6.6\%$ ($+10\%$).

**Small bases mislead.** Powell over 5 coefficients found only $1.008$ (100 fs) and $1.035$ (200 fs), with cubic-dominated masks. The large-basis optima carry 1–3 rad of structured phase over many orders.

## Sharpened statement (cross-family, gpt-a, 2026-10-17)

**The `sim-verified` status applies only to this narrowed constructive statement.**
For the authorized published masks, independent propagation and gated ZS
shooting give

$$f_1=\frac{2\operatorname{Im}\zeta_1}{N^2},\qquad
H_\phi\ge H(A2)=1.09016\pm0.00005\quad(100\,{\rm fs}),$$
$$H_\phi\ge H(B)=1.06974\pm0.00005\quad(200\,{\rm fs}).$$

The uncertainties are conservative observed numerical discrepancies, not
confidence intervals or rigorous interval bounds. Here $q=Nu$ has input mass
$2N^2$, $\zeta_1$ belongs to the isolated leading soliton, and $H$ compares the
same input spectrum and energy with and without phase. The discrete regime is
$N=4$, $N^2\tau_1/T_0\in\{1.952,0.976\}$, $NL/L_D=4$, $f_R=0.18$,
$\tau_2/\tau_1=32/12.2$, with zero higher dispersion, shock, loss and noise.
No interpolation over that enclosing Raman-parameter interval is asserted.
The tallest pulse is the reddest resolved soliton above a 1% input-energy
census floor. The C2 phase continuations reproduce the same gains.

The corresponding fractions are 0.651078 and 0.689078; B has
$f_1\sqrt N=1.37816$. A independently gives $H=1.061806$.
At the specified output plane A2 and B increase energy but reduce red shift;
this qualification is necessary for a fair experimental comparison.
B's “7.0%” is rounded: the literal strict $\ge7.000\%$ interpretation is
refuted by the measured 6.974%, whereas the rounded reproduction passes.

All frozen published-mask reproduction, saturation, grid/window/step,
input-energy and held-out duration/shock/TOD/loss checks pass. RK4IP field
errors scale with measured order 3.88–3.97; ZS transfer errors have order
approximately 2. These are numerical-method orders, not a physical
asymptotic law for headroom. The published dispersion curve is a controlled
material-model test, not validated broadband SMF-28 performance.

The original upper bracket, B2/B3 witnesses and universal optimum remain
unverified here. B2/B3 coefficient files were outside the authorized input
list. Stronger masks found by gpt-a are **new proposer content** in
C-20261017-gpt-a-01, with Claude-family verification task T-20261017-gpt-a-03;
they do not supply self-verification through this card.
All numbers above cite run `2026-10-17-gpt-a-phase-headroom`, especially
`verification.json`, `readout_checks.json` and `summary.json`.

## Regime

- $N=4$: $T_0=100$ fs (masks A, A2, both also at 90 and 110 fs) and $T_0=200$ fs (masks B, B2, both also at 180 and 220 fs); $L=4L_D/N$.
- $N=5$: $T_0=280$ fs (one reduced search).
- At $N=2$ only Powell was run (1.0035 at 100 fs). At $N=3$ the 11-parameter search gives 1.011 (100 fs) and 1.019 (140 fs). Neither is part of the claim beyond the $N$-dependence statement.
- $\delta_3=0$; self-steepening as a relaxation.
- No small parameter. The lower bounds are demonstrations, and the upper bound is the card's conjecture, tested.

## Assumptions

1. The model and measurement assumptions of C-20261016-claude-a-02: scalar field, Blow–Wood Raman, $\beta_2$ only, no loss or noise; leading soliton = tallest peak, checked by the census.
2. The fixed length $L=4L_D/N$. The masked launches are saturated in $L$: $4\to8\,L_D/N$ changes $f_1$ by 0.13% (A) and 0.07% (A2), and $4\to6\,L_D/N$ by 0.015% (B). The census confirms the leading soliton is the reddest (`h4_verify_N4_T100_maskA_TLstart.json`, `h4_verify_N4_T100_best.json`, `h4_verify_maskB.json`). With mask A2 the leading soliton is also further red-shifted than with TL ($W_c=70.9$ against 65.3 at $L=8L_D/N$).
3. Mask B was optimized in FastDifferentiableMMNLO on the windowed energy, with self-steepening suppressed ($\omega_0\times10^3$, $n_2\times10^{-3}$). It was re-measured with the numpy ZS content in the $s=0$ model. Rebuilding it from its coefficients in numpy reproduces the gain (+6.97%), which checks the convention mapping between the codes.

## Predictions

Frozen in `runs/2026-10-16-claude-a-raman-soliton-frontier/HYPOTHESES.md`:
- 3af8dfa: the card's conjecture (H4);
- acd072a: H4d;
- 09ea231: H4e;
- 5a65a06: H4f, H4g;
- e01d626: H4h.

| Prediction | Outcome | Run file |
|---|---|---|
| Card's conjecture: $H_\phi<\frac{2N}{2N-1}(1+\epsilon^{\rm TL})$ | holds: 1.062 against 1.56; 1.070 against 1.68 | `h4grad_N4_T100.json`, `h4_adjoint_measure_N4_T200.json` |
| H4d(i): with self-steepening, photon-content gain $\ge4\%$ (both masks) | confirmed: $+6.6\%$, $+8.0\%$ | `h4_robust.json` |
| H4d(ii): at $\pm10\%$ $T_0$, gain $\ge4\%$ | 3 of 4 confirmed ($+6.6$, $+5.5$, $+8.2\%$). **Refuted** for mask A at 90 fs ($+3.0\%$) | `h4_robust.json` |
| H4e: at $N=3$, 140 fs, the 11-parameter search finds $\ge3\%$ | **refuted**: $+1.94\%$ | `h4grad_N3_T140.json` |
| H4f: with self-steepening, photon-content gain $\ge5\%$ for masks A2 and B2 | confirmed: $+8.24\%$, $+8.78\%$ | `h4_robust_best2.json` |
| H4g: $N=5$, 280 fs, reduced search finds $\ge3\%$ | confirmed: $+5.6\%$ (saturated at $L=4$–$6\,L_D/N$, $h/2$ identical; $8\,L_D/N$ discarded for window wrap-around) | `h4grad_N5_T280.json`, `h4_verify_N5_T280.json` |
| H4h: masks A2 and B2 at $\pm10\%$ $T_0$ give $\ge4\%$ | confirmed, all four: $+7.4$, $+8.4$, $+6.5$, $+9.1\%$ | `h4_robust_detune2.json` |

**Predictions for a verifier.**
- A converged adjoint search (more iterations, at least 30 coefficients, several starts) at $N=4$, $T_0=200$ fs finds $H_\phi\in[1.07,1.25]$. At 100 fs, mask A2 already gives 1.090; at 200 fs, mask B3 gives 1.082.
- At $N=6$ near its transfer maximum ($T_0\approx380$ fs), a similar search finds $H_\phi\ge1.05$.

**Lab test.**
- Setting: SMF-28 at 1550 nm, an $N=4$ sech laser at $T_{\rm FWHM}\approx350$ fs (about 2.7 nJ), a programmable phase shaper.
- Apply mask B, mapped to the laser's spectral support and with odd orders sign-flipped to the experiment's Fourier convention.
- Prediction: the energy of the most red-shifted soliton at $L\approx1.8$ m rises by about 7% over the transform-limited launch.

## Derivation

None. The masks are numerical optima. The census shows how they work:
- at $N=4$, 100 fs (mask A), the second soliton's content falls from 0.254 to 0.209, and the leading soliton's rises from 0.597 to 0.634;
- at 200 fs (mask B), the second soliton falls from 0.198 to 0.075, and the leading soliton rises from 0.643 to 0.688. Shaping thus redistributes the fission products toward the leading soliton beyond what the TL launch's Raman transfer achieves.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Soliton units (numpy); SI (solver) | claude | — | 2026-10-16 |
| Known limits | TL rows reproduce `h3_main` | claude | `2026-10-16-claude-a-raman-soliton-frontier` | 2026-10-16 |
| Symmetries | — | | | |
| Symbolic residual | — | | | |
| Simulation, core regime | Mask A2: $+9.02\%$; mask A: $+6.18\%$; mask B3: $+8.18\%$ (ZS), $+8.25\%$ (windowed energy); mask B2: $+7.96\%$ (ZS), $+8.02\%$ (windowed energy, solver); mask B: $+6.97\%$ (ZS), $+7.08\%$ (windowed energy); random-start B: $+6.56\%$ (ZS) | claude | `h4grad_N4_T100.json`, `h4_adjoint_N4_T0200_M16.log`, `h4_adjoint_measure_N4_T200.json` | 2026-10-16 |
| Error-scaling exponent | n/a | | | |
| Held-out region | H4d: self-steepening and $\pm10\%$ $T_0$ (5 of 6 conditions $\ge4\%$, masks A, B). H4f, H4h: masks A2, B2 under self-steepening and $\pm10\%$ $T_0$ (all 6 conditions $\ge4\%$). H4g: $N=5$ | claude | `h4_robust.json`, `h4_robust_best2.json`, `h4_robust_detune2.json`, `h4grad_N5_T280.json` | 2026-10-16 |
| Convergence and artefacts | Masks A and A2: saturated in $L$ ($4\to8\,L_D/N$: $-0.13\%$, $-0.07\%$), $h/2$ identical to 5 digits, census clean. Masks B, B2, B3: saturated in $L$ ($4\to6\,L_D/N$: $-0.015\%$, $-0.06\%$, $-0.06\%$), census clean (`h4_verify_maskB.json`, `h4_verify_maskB2.json`, `h4_verify_maskB3.json`). Adjoint gradient checked against finite differences (relative error $10^{-9}$) | claude | `h4_verify_N4_T100_maskA_TLstart.json`, `h4_verify_N4_T100_best.json`, `h4_adjoint_N4_T0200_M16.log` | 2026-10-16 |
| Second solver or relaxed assumption | Mask B found in FastDifferentiableMMNLO, confirmed in the numpy GNLSE; self-steepening relaxation (H4d i) | claude | same | 2026-10-16 |
| Adversarial audit | — | | | |
| Novelty search | Efimov et al. (2004), adaptive phase control of SSFS, abstract only; Hu et al. (2015), Airy control, partial (both from the card). Neither reports a headroom for the leading soliton's energy | claude | — | 2026-10-16 |
| Independent published-mask reproduction | A2 H=1.090163, A 1.061806, B 1.069737; gated energy and input-energy checks pass | gpt-a (gpt) | 2026-10-17-gpt-a-phase-headroom | 2026-10-17 |
| Independent numerical errors | Four-level RK4IP order 3.88–3.97; ZS order approximately 2; window, grid, dt ≤3 fs, aliasing and invariant checks pass | gpt-a (gpt) | 2026-10-17-gpt-a-phase-headroom | 2026-10-17 |
| Independent held-outs and relaxed assumptions | Fixed energy/length/physical-mask ±10% duration: H ≥1.020; shock, TOD and loss retain positive gated-energy gain; sourced dispersion model also positive | gpt-a (gpt) | 2026-10-17-gpt-a-phase-headroom | 2026-10-17 |
| Independent adversarial scope | Lower witnesses qualified; strict 7.000% reading fails, global ceiling unproved, broadband material certificate absent; no audited status | gpt-a (gpt) | 2026-10-17-gpt-a-phase-headroom | 2026-10-17 |

## Outcome

**Promoted 2026-10-19.** On the PI's decision of 2026-10-19 (task T-20261019-claude-interactive-07), the cross-family sharpened statement (masks A2 and B, $H\ge1.09016$ and $1.06974$) is promising result [R-0006](../results/promising/R-0006-phase-mask-headroom-leading-raman-soliton/RESULT.md). The proposer's statement, its upper bracket, B2/B3 and the $N=3$, 5 parts are not part of the result. G5 is open: there is no clean-context audit (T-20261019-claude-interactive.15-01). G6 (T-20261019-claude-interactive.15-02) and G8 (T-20261019-claude-interactive.15-04) are also open.

**Verified as narrowed; proposed → sim-verified.** Only the cross-family
statement above carries this status. The proposer's statement is preserved.
See [independent report](notes/audit-2026-10-17-gpt-a-C-20261016-claude-a-04.md)
and [PI summary](../docs/summary-2026-10-17-gpt-a-C-20261016-claude-a-04.md).

## Audit trail

| Date | Agent (family) | Decision | Evidence |
|---|---|---|---|
| 2026-10-17 | gpt-a (gpt), gpt-6-astra | Narrowed to independently reproduced A2/A/B witnesses; literal strict 7.000% reading refuted; full upper bracket unverified. Stronger GPT witnesses filed separately. | 2026-10-17-gpt-a-phase-headroom; independent report above |
| 2026-10-19 | claude-interactive.15 (claude), claude-opus-5-5 | Status sim-verified → promoted; `result: R-0006` (the sharpened statement only). Statement unchanged. G5 open: gpt-a's report is a verification; audit task T-20261019-claude-interactive.15-01 | Task T-20261019-claude-interactive-08 |
