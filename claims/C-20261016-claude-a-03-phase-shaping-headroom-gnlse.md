---
id: C-20261016-claude-a-03
problem: P-20261016-claude-interactive-03
title: "Spectral-phase shaping raises the leading Raman soliton's content by at most a few percent (< 5%) over the transform-limited launch (GNLSE, N = 2–6)"
type: bound
status: refuted
proposed_by: claude-a
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: gpt-a
auditor_family: gpt
created: 2026-10-16
updated: 2026-10-17
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: null
---

## Statement

**System.** A transform-limited sech laser, $|Q|$ fixed, $N=\sqrt{\gamma P_0T_0^2/|\beta_2|}$, passes a smooth spectral phase mask $Q\to Qe^{i\phi(\omega)}$. It is then launched into the Raman GNLSE of C-20261016-claude-a-02:
- Blow–Wood response, $f_R=0.18$;
- $\delta_3=\beta_3/(6|\beta_2|T_0)\in\{0,0.05\}$;
- no self-steepening, no loss.

The objective is the leading output soliton's content $f_1(L)$ at $L=4L_D/N$. It is measured by:
- the ZS eigenvalue as in C-20261016-claude-a-02, using the local-dispersion time scaling when $\delta_3\ne0$;
- cross-checked by the windowed energy.

**Claim.** The headroom $H=\max_\phi f_1(L)/f_1^{\rm TL}(L)$ of smooth phase masks satisfies $H-1<0.05$ for $N=2$–6, $T_0\in\{100,200\}$ fs and $\delta_3\le0.05$. The best masks found:

| Case | Best gain over TL |
|---|---|
| $T_0=100$ fs, $\delta_3=0$, $N=2$ | $+0.35\%$ |
| $T_0=100$ fs, $\delta_3=0$, $N=3$ | $+1.13\%$ |
| $T_0=100$ fs, $\delta_3=0$, $N=4$ | $+0.77\%$ |
| $T_0=100$ fs, $\delta_3=0$, $N=6$ (cubic-phase scan) | $+0.56\%$ |
| $N=4$ at the Raman-transfer optimum, $T_0=200$ fs ($x=N^2T_R/T_0=0.117$) | $+3.5\%$ |
| $N=3$, $\delta_3=0.05$ | $-0.4\%$ (local-dispersion ZS) to $+1.6\%$ (windowed energy) |
| $N=4$, $\delta_3=0.05$ | $+2.85\%$ (local-dispersion ZS), $+2.73\%$ (windowed energy) |
| $N=2$, $\delta_3=0.05$ | $+1.08\%$ (nominal ZS only; not re-measured) |

The best masks are dominated by cubic spectral phase. Chirp alone never helps.

So the card's conjecture holds with a wide margin. The conjecture is $\max_{\mathcal S_\phi}f_1<f_1^{\rm TL}\,\frac{2N}{2N-1}(1+\epsilon^{\rm TL})$, which allows 1.48–1.57. Shaping steers the interpulse Raman transfer only weakly, most where that transfer is strongest.

**A measurement trap found on the way.** With $\delta_3\ne0$, the ZS content computed with the nominal $\beta_2$ rewards masks that reduce the soliton's red shift, because the local dispersion $1+6\delta_3W_c$ then deviates less from 1. The optimizer found an apparent $+4.8\%$ ($N=3$) and $+4.2\%$ ($N=4$) this way. The local-dispersion content shows no real gain at $N=3$ and $+2.85\%$ at $N=4$.

## Regime

- $N\in\{2,3,4\}$ by optimization: Powell over 5 parameters; L-BFGS with forward-difference gradients over 11 parameters; L-BFGS with the solver's discrete adjoint over 15 parameters (see Checks). $N=6$ by one-parameter chirp and cubic-phase scans only.
- $T_0=100$ fs, i.e. $x=N^2T_R/T_0=0.058$, 0.13 and 0.23 for $N=2,3,4$. Plus $N=4$ at $T_0=200$ fs, near the maximum $x^*$ of C-20261016-claude-a-02.
- $\delta_3\in\{0,0.05\}$.
- Mask class: $\phi=\sum_{m=2}^{M}c_mP_m(\omega/\omega_c)$, $M=6$, 12 or 16, Legendre polynomials on the spectral support.
- No small parameter. The claim is a measured upper bound, and every optimizer gives only an achievable lower bound. A better mask refutes the claim.

## Assumptions

1. The model and measurement assumptions of C-20261016-claude-a-02 (scalar field, single-oscillator Raman, no self-steepening or loss, leading soliton = tallest peak).
2. Fixed length $L=4L_D/N$, where the transform-limited excess has saturated.
3. Smooth phase masks for the claim. The passive class (phase plus amplitude $\mathrm{sigmoid}(d_0+d_2P_2)$) was tried once ($N=3$, 100 fs). It gave $+1.09\%$ against its own TL launch, about the same as phase-only ($+1.04\%$ Powell, $+1.13\%$ gradient) (`h4_N3_T100_d0_Aphi.json`).
4. The adjoint optimization maximizes the windowed energy, a smooth proxy for $f_1$. Its optimum is re-measured with the ZS content.

## Predictions

Frozen in `runs/2026-10-16-claude-a-raman-soliton-frontier/HYPOTHESES.md`. The commits are:
- 3af8dfa: H4, the card's conjecture and "$<5\%$ for $N\ge3$";
- 73e23c6: H4b;
- e94b6d7: H4c.

| Prediction | Outcome | Run file |
|---|---|---|
| H4 conjecture, $N=2$–4 ($T_0=100$ fs, $\delta_3\in\{0,0.05\}$), $N=6$ (scans) | confirmed; largest ratio 1.035 against bounds $\ge1.48$ | `h4_*.json`, `h4_recheck.json` |
| Sharper: $<5\%$ for $N\ge3$ | confirmed: largest real gain $+3.5\%$ ($N=4$, 200 fs), then $+2.85\%$ ($N=4$, $\delta_3=0.05$). The nominal-measure $+4.8\%$ at $N=3$, $\delta_3=0.05$ is an artefact (see Statement) | same, `h4_recheck_N4d005.json` |
| H4b: $<3\%$ at the Raman optimum ($N=4$, $T_0=200$ fs) | **refuted**: $+3.5\%$ (ratios 1.0347, 1.0350 from two starts) | `h4_N4_T200_d0_phi.json` |
| H4c: 11-parameter gradient search stays below 2% ($N=3,4$, 100 fs) | $N=3$: confirmed, $+1.13\%$ (converged, $|g|=5\times10^{-5}$). $N=4$: see Checks | `h4grad_N3_T100.json`, `h4grad_N4_T100.json` |

**Prediction for a verifier.** No smooth phase mask, of any number of parameters, raises the leading soliton's ZS content (local-dispersion form when $\delta_3\ne0$) by more than 5% over TL, for $N=2$–6 and $T_0$ between 100 fs and $2T_0^*$ (C-20261016-claude-a-02). The largest gains are found near $T_0^*$.

**Lab test.**
- Use an SSFS source with a programmable phase shaper: SMF-28 at 1550 nm, $N=3$–4, $T_0\approx100$–200 fs.
- Measure the energy of the most red-shifted soliton under chirp, cubic phase and an adaptive search.
- Prediction: at most a few percent above TL. The largest gain is near the duration that maximizes the TL soliton energy.

## Sharpened statement (cross-family, gpt-a, 2026-10-17)

The claimed universal 5% ceiling is independently **refuted**, not repaired:

$$H_\phi\ge H(A2)=1.09016\pm0.00005>1.05.$$

The counterexample uses $f_1=2\operatorname{Im}\zeta_1/N^2$ for $q=Nu$,
input mass $\int|u|^2d\tau=2$, $N=4$, $N^2\tau_1/T_0=1.952$,
$NL/L_D=4$, $f_R=0.18$, $\tau_2/\tau_1=32/12.2$, and zero higher dispersion,
shock and loss. The uncertainty is an observed numerical discrepancy estimate.
These parameters lie inside the original claimed regime. Phase-only input
energy is unchanged; gated energy also rises by 9.065%. Independently
reproduced A and B each exceed 5% as well. No optimizer convergence is needed
to disprove a universal ceiling with these explicit witnesses.

All numbers cite `2026-10-17-gpt-a-phase-headroom`; the independent report is
[here](notes/audit-2026-10-17-gpt-a-C-20261016-claude-a-03.md), and the
[PI summary](../docs/summary-2026-10-17-gpt-a-C-20261016-claude-a-03.md)
contains the equation and plot. Status remains **refuted**.

## Derivation

No analytic derivation. Two reasons to expect small headroom:
- In the integrable limit the TL launch is optimal (C-20261016-claude-a-01).
- The Raman transfer (C-20261016-claude-a-02) is set by $N$ and $T_0$. A phase mask lengthens the pulse but lowers its soliton content, so it cannot move a launch along $x$ at fixed content.

The cubic phase the optimizers find is consistent with the Airy-launch control of Raman solitons in Hu et al. (2015). Here it buys about 1%, and 3.5% near the transfer maximum.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Soliton units (numpy); SI (solver) | claude | — | 2026-10-16 |
| Known limits | TL launch reproduces $f_1^{\rm TL}(L)$ of `h3_main` | claude | `2026-10-16-claude-a-raman-soliton-frontier` | 2026-10-16 |
| Symmetries | — | | | |
| Symbolic residual | — | | | |
| Simulation, core regime | Powell 2–3 starts ($N=2,3,4$); forward-difference L-BFGS, 11 parameters ($N=3,4$); adjoint L-BFGS, 15 parameters ($N=3$, see below) | claude | `h4_*.json`, `h4grad_*.json`, `h4_adjoint_*.log` | 2026-10-16 |
| Error-scaling exponent | n/a | | | |
| Held-out region | $N=6$ scans; $\delta_3=0.05$; $T_0=200$ fs | claude | same | 2026-10-16 |
| Convergence and artefacts | Same grid and step as `h3_main` (converged at $(4,200)$ and $(6,400)$). TOD measurement artefact identified and removed | claude | `h3_conv`, `h4_recheck.json` | 2026-10-16 |
| Second solver or relaxed assumption | Adjoint optimization in FastDifferentiableMMNLO (b9fa957, discrete RK4IP adjoint; self-steepening suppressed by $\omega_0\times10^3$, $n_2\times10^{-3}$), gradient checked by finite differences: status in the log and the run summary | claude | `h4_adjoint_*.log` | 2026-10-16 |
| Adversarial audit | — | | | |
| Novelty search | Efimov et al. (2004), adaptive phase control of SSFS, abstract only (from the card); Hu et al. (2015), Airy control, partial full text (from the card). Neither reports a headroom number for the leading soliton's content | claude | — | 2026-10-16 |
| Independent counterexample | Published A2: H=1.090163; A: 1.061806; B: 1.069737. All exceed 1.05 at fixed laser energy | gpt-a (gpt) | 2026-10-17-gpt-a-phase-headroom | 2026-10-17 |
| Independent adversarial audit | Gated ZS extraction, output-pulse census, four-step/grid/window checks and held-out relaxations preserve the counterexample | gpt-a (gpt) | 2026-10-17-gpt-a-phase-headroom | 2026-10-17 |

## Outcome

**Refuted by my own larger-basis searches before filing (2026-10-16).** The statement "$H-1<0.05$" is false at $N=4$:
- 11-parameter L-BFGS with forward-difference gradients at $T_0=100$ fs: $H=1.062$ (`h4grad_N4_T100.json`).
  - Verified saturated in $L$ ($L=4,6,8\,L_D/N$), step-converged ($h/2$ identical to 5 digits), $\mathrm{Re}\,\zeta_1\approx0$.
  - The census confirms the leading soliton is isolated (`h4_verify_N4_T100_maskA_TLstart.json`).
- 15-parameter adjoint L-BFGS (solver, discrete adjoint) at $T_0=200$ fs: $H=1.070$, re-measured with the numpy ZS content (`h4_adjoint_N4_T0200_M16.log`, `h4_adjoint_measure_N4_T200.json`). It was not converged.

So the frozen sharper prediction ($<5\%$ for $N\ge3$), H4b ($<3\%$ at the Raman optimum) and H4c ($<2\%$ with the 11-parameter search, $N=4$) are all refuted. The card's conjecture itself (bound 1.48–1.68) still holds.

**What was learned:**
- Small mask bases badly underestimate the headroom. Powell over 5 coefficients found 1.008 (100 fs) and 1.035 (200 fs).
- The cubic-dominated optima of the small basis are not representative. The large-basis optima carry 1–3 rad of phase across Legendre orders up to 12–16.
- The demonstrated achievable headroom, with robustness checks, is claim C-20261016-claude-a-04.
- The other content of this card stays valid as a record: the Powell values, the TOD measurement trap, the passive-class run, and the $N=6$ scans.

## Audit trail

| Date | Agent (family) | Decision | Evidence |
|---|---|---|---|
| 2026-10-17 | gpt-a (gpt), gpt-6-astra | Independently confirmed refutation; refuted → refuted. The separate loose global conjecture remains unproved. | 2026-10-17-gpt-a-phase-headroom |
