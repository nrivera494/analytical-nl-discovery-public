---
id: R-0002
title: "Beyond the formalized core: the real-exponent ZS eigenvalue inequality, passive-mask ceilings for arbitrary masks, Gaussian-laser ceilings by sharp Hausdorff–Young (≤ 0.015% headroom at N = 4), and the spectral-norm bound"
claim: C-20261018-pi-chatgpt-01
problem: P-20261016-claude-interactive-03
tier: promising
status: accepted
type: bound
proposer: pi-chatgpt
proposer_model: gpt-6-pro
proposer_family: gpt
verifier: claude-interactive.9
verifier_family: claude
auditor: claude-interactive.9
auditor_family: claude
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
promoted: 2026-10-18
pi_score: null
gates:
  G1: met
  G2: met
  G3: met
  G4: met
  G5: met
  G6: open
  G7: met
  G8: open
---

# Passive-mask ceilings at real exponents, for arbitrary masks, and for Gaussian lasers

This result holds the parts of claim C-20261018-pi-chatgpt-01 that are verified across families and approved by the PI (2026-10-18) but are **not** formalized. The even-exponent core for Schwartz masks is formalized as [R-0001](../../formalized/R-0001-zs-even-moment-passive-mask-ceiling/RESULT.md), which the statements here extend.

## 1. Problem

A passive spectral mask shapes a laser pulse before an anomalous-dispersion fibre; the leading soliton's energy is $4\eta$, where $\zeta=\xi+i\eta$ is the largest Zakharov–Shabat (ZS) eigenvalue of the launched field. R-0001 bounds $\eta$ at even exponents for smooth masks. This result covers:
- the inequality at every real exponent;
- masks of any regularity, including the hard-edged and pixelated masks that real pulse shapers produce;
- the sharp ceiling for Gaussian lasers.

Problem: [P-20261016-claude-interactive-03](../../../problems/P-20261016-claude-interactive-03-raman-soliton-efficiency-shift-frontier.md).

## 2. Result

Notation as in R-0001. For real $p>1$ let
$$C_p=\frac{p^p}{(p-1)^{p-1}}\frac{J_p}{2},\qquad J_p=\int{\rm sech}^pt\,dt=\frac{\sqrt\pi\,\Gamma(p/2)}{\Gamma((p+1)/2)},$$
and let $p'=p/(p-1)$.

**(A′) Real-exponent eigenvalue inequality.** For every $q\in L^1(\mathbb R)$, every eigenvalue and every real $p>1$,
$$\int|q|^p\,dt\ \ge\ C_p\,\eta^{p-1},$$
with equality for $q_*(t)=\frac{p\eta}{p-1}{\rm sech}\frac{2\eta(t-t_0)}{p-1}$ up to constant phase and carrier. The limits are:
- $p=2$: $\eta\le\|q\|_2^2/4$;
- $p\to\infty$: $\eta\le\|q\|_\infty$;
- $p\to1$: the area condition $\|q\|_1\ge\pi/2$.

**(B′) Passive-mask ceiling for arbitrary masks.** For $S\ge0$ with $q_0=\mathcal F^{-1}S\in L^{2n}$, every measurable $|m|\le1$, every integer $n\ge1$ and every eigenvalue of $q_m=\mathcal F^{-1}(mS)$,
$$\eta\le\Big[\int|q_0|^{2n}/C_{2n}\Big]^{1/(2n-1)} .$$
Hence, for integer-order sech lasers, $f_{1,\rm opt}=(2N-1)/N^2$ over all passive masks, and the non-integer ceilings of R-0001 also hold without the Schwartz condition. The real-exponent version of (B′) is false for general spectra.

**(E) Gaussian lasers.** For $q_0=Ne^{-t^2/2}$, sharp Hausdorff–Young (Beckner), which Gaussians attain, gives $\|q_m\|_p\le\|q_0\|_p$ for every real $p\ge2$. Hence
$$f_{1,\rm opt}\le\frac{4}{\sqrt\pi N^2}\inf_{p\ge2}\Big[\frac{N^p\sqrt{2\pi/p}}{C_p}\Big]^{1/(p-1)} .$$
The headroom over TL is at most:

| $N$ | Headroom over TL |
|---|---|
| 1.5 | 0.283% |
| 4 | 0.0150% (TL 0.4912507580; ceiling 0.4913243554) |
| 5 | 0.00745% |
| 8 | 0.00172% |

**(F) Spectral-norm bound for any source.** For $p\ge2$,
$$\eta\le\frac{\sqrt{p'}}{2\pi}\Big(\frac1{\sqrt p\,C_p}\Big)^{1/(p-1)}\int S^{p'}dk .$$

## 3. Regime of validity

| Dimensionless group | Definition | Lower bound | Upper bound | What fails outside |
|---|---|---|---|---|
| $p$ | Moment exponent | (A′): $>1$; (E), (F): $\ge2$ | none | At $p\le1$ the inequality degenerates to the area condition |
| $N$ | Soliton order of the TL pulse | $>0$ | none | — |
| $\|m\|_\infty$ | Mask transmission amplitude | 0 | 1 | Gain media are not passive |
| $T_R/T_0$ | Raman time over pulse width | 0 | not bounded | Raman lifts the propagated leading soliton above the ceiling (+10.4% at $T_0=65$ fs, TL $N=2$) |

There is no small parameter: these are exact inequalities for the input scattering data of the integrable NLSE. The assumption ledger is that of R-0001, with the Schwartz conditions replaced by $q\in L^1$, $q_0\in L^{2n}$ and $S\ge0$, plus:
- **(E)** uses Beckner's sharp Hausdorff–Young constant, which Gaussians attain.
- **The TL baselines quoted in (E)** are numerical: two independent solvers agree to $10^{-10}$, but the values are not interval-certified.

## 4. Derivation

The claim's [derivation note](../../../claims/notes/C-20261018-pi-chatgpt-01-derivation.md) proves (A′) with the spinor angle $\theta=\arctan(|v_2|/|v_1|)$, which satisfies $\theta'\le|q|-\eta\sin2\theta$, together with a sharp convexity (Young-type) inequality and an antiderivative in $\theta$. For $q\in L^1$ the angle is absolutely continuous, with $\theta(-\infty)=0$ and $\theta(+\infty)=\pi/2$. At even $p$ this is the argument of R-0001 in a different variable.

The rest follows from (A′):
- **(B′):** the even-moment Fourier majorant (Lenzmann–Sok, Lemma 5.1) for $L^2$ spectra.
- **(E) and (F):** Beckner's sharp Hausdorff–Young inequality $\|\mathcal F f\|_p\le A_p\|f\|_{p'}$, with equality for Gaussians.

claude-interactive.9 proved (A′)–(C) independently before reading the note. It rederived the Hausdorff–Young constants of (E) and (F), and checked that (F) equals (E) at equal $p$ for Gaussians, to $5\times10^{-12}$ (run `2026-10-18-claude-interactive.9-zs-solver-validation`).

## 5. Validation against numerics

![Gain over TL against soliton number](../../../runs/2026-10-18-claude-interactive.9-mask-adversary/fig_summary.png)
*Ceilings on the gain in leading ZS eigenvalue over TL against $N$. The dashed Gaussian curve is (E); the solid sech curve is (B′)/(D). Points are the best of 13 adversarial passive-mask searches per case (open = held out). Run `2026-10-18-claude-interactive.9-mask-adversary` (claude-interactive.9, family claude; no fibre solver).*

All numbers below are from claude-interactive.9 (family claude).

- **(A′) at real exponents.**
  - Equality at $q_*$ holds to 13 digits for $p=1.5$, 2, 3 and 7.
  - On 69 eigenvalues of 60 random complex, multi-lobe, chirped potentials, the smallest ratio $\int|q|^p/(C_p\eta^{p-1})$ over $p\in[1.2,12]$ is 1.022.
  - The limits check: $C_2=4$; $C_p\to\pi/2$ as $p\to1$; $C_p^{1/(p-1)}\to1$ as $p\to\infty$ (run `2026-10-18-claude-interactive.9-zs-solver-validation`).
- **(B′) for rough masks.** The adversarial searches included per-bin masks with up to 274 free parameters and sharp multi-step masks. No search exceeded the ceiling at integer $N$ beyond the solver error of $2.3\times10^{-12}$.
- **(E), held out.** The TL fractions are reproduced to $10^{-10}$ (0.491250757965 at $N=4$). No mask beats TL at all:

  | $N$ | Best gain found | Ceiling |
  |---|---|---|
  | 1.5 | $-7\times10^{-16}$ | 0.28343% |
  | 4 | $-2\times10^{-16}$ | 0.01498% |
  | 5 (held out) | $-8\times10^{-15}$ | 0.00745% |
  | 8 (held out) | $-1\times10^{-16}$ | 0.00172% |

  The $N=1.5$ values were marked held out on the card but appear in the source's table, so they were not held out.
- **Convergence.** Every optimized mask was re-evaluated on a twice-finer grid, on the full line, and with a doubled window; the spreads were at most $8\times10^{-12}$.

The ceilings are valid but loose against everything found: no search approached them. Error scaling (expected figure 2) is n/a for an exact inequality.

## 6. Adversarial audit

[audit-2026-10-18-claude-interactive.9.md](audit/audit-2026-10-18-claude-interactive.9.md) (claude; verdict pass). Gaps noted as non-blocking:
- state $q\in L^1$;
- state that the spinor angle is absolutely continuous.

The audit also reproduced the claim's counterexample to C-20261016-claude-a-01: for the asymmetric spectrum $S=\pi\cos(1)e^k{\rm sech}(\pi k/2)$, passive masks raise $\eta_{\max}$ by up to 2.78% over TL. So TL optimality does not extend to general spectra, and the even-moment hierarchy gives only $f_1\le1$ there.

## 7. Novelty

From claude-interactive.10's novelty audit ([report](../../../docs/review-2026-10-18-claude-interactive.10-zs-eigenvalue-bound-novelty.md), family claude):
- **(A′), partly published.** For real $q\ge0$ and purely imaginary eigenvalues, the sharp constant and the extremizer are in Dolbeault, Gontier, Pizzichillo & Van Den Bosch (2024), DOI 10.4171/RMI/1443, at all real $p$ (full text). A weaker constant for complex potentials is in Cuenin, Laptev & Tretter (2014), DOI 10.1007/s00023-013-0259-3 (full text).
- **Not found:** the sharp complex and off-axis case, and (B′), (E), (F). Their ingredients (Lenzmann–Sok majorant, Satsuma–Yajima, Beckner) are published. Confidence medium.

G6 is open: only one family has searched (task T-20261018-claude-interactive-05).

## 8. Experimental test

- **Setup.** A laser with a near-Gaussian spectrum at launch soliton order $N=4$, a programmable passive pulse shaper, and an anomalous-dispersion fibre in the integrable regime: picosecond pulses and a few dispersion lengths, so that Raman is negligible.
- **Prediction.** No mask setting gives a leading soliton above 49.132% of the unshaped laser energy; the TL launch gives 49.125%. Shaping a Gaussian laser can gain at most 0.015%.
- **Hard-edged masks.** Per (B′), a hard-edged bandpass on a sech laser also cannot beat $(2N-1)/N^2$.
- **Falsification.** Any measured gain above these ceilings, beyond the measurement error, with the soliton content taken from the FROG-retrieved launched field or from the separated output soliton, falsifies the result.

## 9. Open questions

- A second-family novelty audit (G6): T-20261018-claude-interactive-05.
- Formalization in Lean (G8), which would move parts of this result to the formalized tier:
  - rough masks: T-20261018-claude-interactive-06;
  - real exponents and Hausdorff–Young: T-20261018-claude-interactive-07.
- A certified enclosure of the TL Gaussian eigenvalue, so that the 0.015% is a proved number rather than a numerical one: part of T-20261018-claude-interactive-07.
- G8 is open because none of (A′), (B′) beyond Schwartz masks, (E) or (F) is formalized. R-0001 lists exactly what is.
