---
id: C-20261016-claude-a-01
problem: P-20261016-claude-interactive-03
title: "At fixed laser spectrum, the transform-limited pulse maximizes the leading Zakharov–Shabat eigenvalue over phase-only and passive masks; the integrable headroom is 1, not 2N/(2N−1)"
type: bound
status: refuted
proposed_by: claude-a
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-16
updated: 2026-10-18
solver_commit: null
result: null
---

## Statement

**System.** A laser of spectral amplitude $|Q(k)|$ passes a passive spectral pulse shaper, $Q\to mQ$ with $|m(k)|\le1$, and is launched into a fibre described in the integrable limit by the NLSE $iq_\xi+\tfrac12q_{\tau\tau}+|q|^2q=0$. Here $q$ is in soliton units, so its Zakharov–Shabat (ZS) bound states $\zeta_k=\xi_k+i\eta_k$ carry soliton energies $4\eta_k$. The transform-limited (TL) launch is $q_{\rm TL}=\mathcal F^{-1}|Q|$, with peak $A=\|q_{\rm TL}\|_\infty=\frac1{2\pi}\int|Q|\,dk$.

**Claim.** For smooth unimodal laser spectra,
$$\eta_{\max}\!\left[\mathcal F^{-1}(mQ)\right]\le\eta_{\max}\!\left[q_{\rm TL}\right]\qquad\text{for all }|m|\le1 .$$
So the leading soliton's energy fraction $f_1=4\eta_{\max}/E$ (with $E$ the laser energy) is largest for the TL launch. The headroom in the integrable limit is
$$H_{\mathcal S_\phi}=H_{\mathcal S_{A\phi}}=1 .$$
The card's sketch 1 allows up to $2N/(2N-1)$ for a sech laser; that bound is not attained by any mask found.

**Proven parts** (proofs under Derivation):
- (i) $\eta\le\|q\|_\infty$ for every bound state.
- (ii) $\|q\|_\infty\le\|q_{\rm TL}\|_\infty$ and $\int|q|^4\le\int|q_{\rm TL}|^4$ for every $|m|\le1$.
- (iii) For a real even $q_{\rm TL}$, every phase mask leaves a simple imaginary $\eta_{\max}$ stationary at first order.

The maximality itself is a numerical result, not a theorem.

**Refuted sharpening.** The semiclassical (WKB) value $\eta_{\rm WKB}$, defined by $\int(|q|^2-\eta^2)_+^{1/2}=\pi/2$, is not an upper bound on $\eta_{\max}$. It is violated by:
- Lorentzian pulses, by 0.014–0.032;
- $\mathrm{sech}^{1/2}$ pulses, by 0.003–0.008;
- asymmetric sech pulses, by $\le0.0025$;
- $e^{-|t|^{3/2}}$ pulses, by 0.007–0.028.

It holds for Gaussian, $\mathrm{sech}^2$, $\mathrm{sech}^3$ ($A\ge2$), super-Gaussian, chirped Gaussians and random-phase Gaussians (H1c and H1c′, both refuted as general statements).

## Regime

- Lasers tested:
  - sech and Gaussian at $A\in\{1.5,2,3,4\}$;
  - held out: $A=6$ (sech and Gaussian), and two further spectra (asymmetric $\mathrm{sech}(\pi k/2)(1+\tfrac12\tanh k)$ and flat-top $e^{-(k/1.5)^8}$, whose TL pulse has side lobes) at $A=2,4$.
- Mask classes:
  - phase $\phi=\sum_{m=2}^{10}c_mP_m(k/k_{\rm sup})$ (Legendre, on the support $|Q|>10^{-4}\max$);
  - amplitude $\mathrm{sigmoid}(d_0+\sum_{m=1}^{10}d_mP_m)$.

  Random sharp-featured masks were also tested (H2c): binary $0/\pi$ segments, spectral holes, and piecewise-linear pulse-splitting phase, 1188 masks on sech and Gaussian lasers at $A=3,4$. Optimization over large bases with sharp features is untested.
- Small parameter: none. This is a global statement; the numerical tolerance is $10^{-3}$ relative.
- Integrable limit only. With Raman, the propagated $f_1$ exceeds the input content (C-20261016-claude-a-02), and shaping is treated in C-20261016-claude-a-04 (C-20261016-claude-a-03, refuted).

## Assumptions

1. Integrable NLSE: scalar field, $\beta_2$ only, Kerr only. No Raman, no $\beta_3$, no self-steepening, no loss.
2. Passive, lossless-at-most shaper ($|m|\le1$). The laser energy $E$ is the normalization, so amplitude masks can only lower $f_1$ through $\eta$.
3. Smooth masks in the finite bases above.
4. Fourier-collocation ZS eigenvalues on a periodic grid. Checked on two grids, and against the Satsuma–Yajima values $A-\tfrac12-k$ for sech.

## Predictions

Frozen before computing in `runs/2026-10-16-claude-a-raman-soliton-frontier/HYPOTHESES.md`. The commits are:
- 3af8dfa: H1a, H1b, H1c, H2;
- 4592262: H1c′;
- 3b5c666: H2b;
- 9294ffa: H2c.

| Frozen prediction | Outcome | Run file |
|---|---|---|
| H1a: no eigenvalue above $\|q\|_\infty$ | confirmed: max $\eta/\|q\|_\infty=0.950$ over 62 potentials | `h1_tests.json` |
| H1b: no mask raises $\|q\|_\infty$ above the TL value | confirmed: random masks $\le0.9994A$; all optimized masks $\le A$ | `h1_tests.json`, `h2_*.json` |
| H1c: $\eta_{\max}\le\eta_{\rm WKB}[|q|]+10^{-3}$, single-humped | **refuted**: Lorentzian, $A=1$–4, window-converged | `h1_tests.json`, `h1c_lorentz_window.json` |
| H1c′: same for exponential or faster tails (held-out shapes) | **refuted**: $\mathrm{sech}^{1/2}$, asymmetric sech, $e^{-|t|^{1.5}}$. The low-confidence guess that algebraic tails violate it at $A=1$ is also wrong: $1/(1+t^4)$ satisfies it ($+0.05$); $1/(1+t^2)^2$ at $A=1$ is unresolved (two-grid error 0.25) | `h1c_narrow.json` |
| H2: TL maximizes $\eta_{\max}$ over $\mathcal S_\phi$ and $\mathcal S_{A\phi}$ within $10^{-3}$, sech and Gaussian, $A\in\{1.5,2,3,4,6\}$ | confirmed: 76 optimizations, largest $\eta_{\rm opt}/\eta_{\rm TL}-1=3\times10^{-15}$ | `h2_sech.json`, `h2_gauss.json`, `h2_A6_*.json` |
| H2b: same on asymmetric and flat-top spectra, $A=2,4$ (held out) | confirmed: 24 optimizations, none above TL | `h2b_asym.json`, `h2b_flattop.json` |
| H2c: no random sharp-featured mask (600 planned, 1188 evaluated) exceeds TL by $10^{-6}$ | confirmed: largest ratio $1+1.3\times10^{-15}$ | `h2c_sharp.json` |

**Prediction for a verifier.** An adjoint or L-BFGS search with 50 or more mask parameters per class, including masks with sharp features, finds no $\eta_{\max}$ above the TL value by more than $10^{-3}$ relative, for any smooth unimodal laser spectrum with $A\le8$. Random sharp-featured masks were already checked (H2c).

**Lab test.**
- Choose launches long enough that Raman transfer is negligible. By C-20261016-claude-a-02, $\varepsilon\approx c_N\tau_R<1\%$ for $T_0\gtrsim3$ ps at $N\le3$.
- Measure the energy of the largest output soliton for shaped and TL launches of the same laser.
- No mask beats TL by more than the measurement error.

## Derivation

**(i)** Let $\psi$ be a bound state, $w=|\psi_1|^2+|\psi_2|^2$. Then
$$\frac{d}{dt}(|\psi_1|^2-|\psi_2|^2)=2\eta\,w+4\,\mathrm{Re}(q\bar\psi_1\psi_2).$$
Integrating over $\mathbb R$ gives $\eta\int w=-2\,\mathrm{Re}\int q\bar\psi_1\psi_2\le\int|q|w$. This is the card's sketch 1, checked: a numerical-range bound.

**(ii)**
- The first inequality: $|q(t)|=\frac1{2\pi}\big|\int mQe^{ikt}\big|\le\frac1{2\pi}\int|Q|$.
- The second: $\widetilde{q^2}=(mQ)\star(mQ)/2\pi$ satisfies $|\widetilde{q^2}|\le(|Q|\star|Q|)/2\pi=\widetilde{q_{\rm TL}^2}$ pointwise. Then use Parseval.

**(iii)**
- For real even $q_0$, the symmetry $q\to\bar q$ maps $\zeta\to-\bar\zeta$, so $\eta$ is even in the imaginary part of a perturbation.
- A phase mask $e^{i\epsilon\phi}$ perturbs $q$ by $\epsilon\,\mathcal F^{-1}(i\phi Q)$. For even $\phi$ this is purely imaginary. For odd $\phi$ it is a real, odd function, which moves $\eta$ only at second order by the parity of the bound state.
- The analytic gradient used by the optimizer confirms that the gradient vanishes at TL.

**Why TL is the maximum** has no proof here. The optimizer evidence is that every start, with random phases up to scale 2, returns to TL ($\|q\|_\infty\to A$).

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Soliton units throughout | claude | — | 2026-10-16 |
| Known limits | Satsuma–Yajima sech eigenvalues reproduced, $\eta_{\rm TL}=A-\tfrac12$ to $10^{-6}$ at $A=1.5,2,3,4,6$; two-grid error $\le1.6\times10^{-11}$. The card's sketch 3 (chirped sech $A\,\mathrm{sech}^{1+iC}$, eigenvalues $i(\sqrt{A^2-C^2/4}-\tfrac12-k)$) is reproduced for $A=2,3$ and $C\le3$. Leading eigenvalues match to $\le10^{-7}$. Near-threshold ones need a wide window (width 160: 0.09808 against 0.0981 at $A=C=3$), and the chirped tails create spurious near-axis pairs that shrink as the window grows (`sketch3_chirped_sech.json`, `sketch3_window_check.json`) | claude | `2026-10-16-claude-a-raman-soliton-frontier` (`h1_tests.json`, `h2_*.json`) | 2026-10-16 |
| Symmetries | Gradient vanishes at TL for every phase start at scale 0 (0 iterations) | claude | same (`h2_*.json`) | 2026-10-16 |
| Symbolic residual | (i), (ii) proved above | claude | — | 2026-10-16 |
| Simulation, core regime | 100 optimizations in total, every one returning to TL; largest excess $3\times10^{-15}$ | claude | same (`summary.json`) | 2026-10-16 |
| Error-scaling exponent | n/a (global bound) | | | |
| Held-out region | $A=6$ sech and Gaussian; asymmetric and flat-top spectra at $A=2,4$: all starts $\le$ TL | claude | `h2_A6_sech.json`, `h2_A6_gauss.json`, `h2b_*.json` | 2026-10-16 |
| Convergence and artefacts | Two grids ($n$ and $1.5n$) for every eigenvalue in H1; $n=512$–1024 for H2 | claude | same | 2026-10-16 |
| Second solver or relaxed assumption | With Raman, the propagated content exceeds this bound (C-20261016-claude-a-02). The claim is restricted to the integrable limit | claude | — | 2026-10-16 |
| Adversarial audit | — | | | |
| Novelty search | Searched Klaus & Shaw (2002, 2003), Prilepsky et al. (2007), Kim–Lee–Lyng (arXiv:1310.4145, WKB versus true eigenvalues for a Gaussian), and "Zakharov–Shabat eigenvalue bound sup norm". No phase-optimality theorem at fixed $|Q|$ was found. (i) is elementary and likely known; the card's search found no statement of it | claude | — | 2026-10-16 |
| Counterexample (PI's GPT 6 Pro session, 2026-10-18) | **Reported, not yet reproduced in-repo.** For the smooth, asymmetric, unimodal source $S(k)=\pi\cos(1)e^k\,\mathrm{sech}(\pi k/2)$, a passive mask raises $\eta_{\max}$ by about 1% above the TL value. If confirmed, the claim as stated ('for smooth unimodal laser spectra') is false. This is consistent with the asymmetric held-out cases above not having been searched exhaustively. The mask and eigenvalue values were not supplied, so reproduction with a run id is part of task T-20261018-claude-interactive-02. The same source proves TL optimality for integer-order sech sources and bounds the Gaussian headroom at about 0.015% for $N=4$ (claim C-20261018-pi-chatgpt-01). | pi-chatgpt (gpt; gpt-6-pro); recorded by claude-interactive | — (reproduction pending) | 2026-10-18 |
| Counterexample reproduced (2026-10-18) | **Reproduced; the claim fails.** Source $S(k)=\pi\cos(1)e^k\mathrm{sech}(\pi k/2)$ (smooth, log-concave, so unimodal; TL pulse exactly $\cos(1)\,\mathrm{sech}(t-i)$, peak $A=1$). TL has one bound state, $\zeta=-0.3839594+0.2142789i$. Passive masks raise $\eta_{\max}$, values on the line (Boffetta–Osborne, Romberg) confirmed by Fourier collocation to $\le9\times10^{-7}$: phase-only Chebyshev mask (23 parameters) $+2.646\%$; per-bin amplitude and phase (484 parameters, throughput 0.9998) $+2.776\%$, $\eta=0.2202282$. The explicit phase-only mask $m(k)=\exp[-0.5\,i\,(k-1)^3/6]$ gives $\eta=0.2166695$, $+1.116\%$. Each is above this card's frozen tolerance of $10^{-3}$, for a smooth unimodal spectrum with $A=1\le8$ | claude-interactive.9 (claude; claude-opus-5-5), as verifier of C-20261018-pi-chatgpt-01 | `2026-10-18-claude-interactive.9-asym-counterexample` | 2026-10-18 |

## Outcome

**Refuted (2026-10-18).** The failing statement is the main claim: "for smooth unimodal laser spectra, the TL pulse maximizes $\eta_{\max}$ over phase-only and passive masks" (and with it $H_{\mathcal S_\phi}=H_{\mathcal S_{A\phi}}=1$ as a general statement). For the asymmetric unimodal source $S=\pi\cos(1)e^k\mathrm{sech}(\pi k/2)$, phase-only masks raise $\eta_{\max}$ by at least 2.6% and passive masks by at least 2.8% (run `2026-10-18-claude-interactive.9-asym-counterexample`; first reported from the PI's GPT 6 Pro session). The frozen verifier prediction (no gain above $10^{-3}$ for any smooth unimodal spectrum with $A\le8$) fails at $A=1$.

What survives:
- The proven parts (i)–(iii) are unaffected.
- **The sech part is settled by C-20261018-pi-chatgpt-01 (C):** for integer-order sech lasers the TL pulse is globally optimal over all passive masks, $\sup_{|m|\le1}\eta_{\max}=N-\tfrac12$, by a proof, not a search. For non-integer sech and Gaussian lasers that claim bounds the possible gain (at most 0.44% for sech $N\ge2.5$, at most 0.28% for Gaussian $N\ge1.5$), and 13 adversarial searches per case found no gain over TL (run `2026-10-18-claude-interactive.9-mask-adversary`), consistent with H2 above.
- On this card's own mildly asymmetric held-out spectrum $\mathrm{sech}(\pi k/2)(1+\tfrac12\tanh k)$ at $A=2$ and 4, the same optimiser finds no gain over TL either (largest $+7\times10^{-16}$; script `mild_asym.py`, run `2026-10-18-claude-interactive.9-asym-counterexample`), consistent with H2b. TL optimality therefore fails for strongly asymmetric spectra such as $e^k\mathrm{sech}(\pi k/2)$ (one-sided decay rates 0.57 and 2.57), not for every asymmetric one; where the boundary lies is open (T-20261018-claude-interactive.9-02).
- H1c and H1c′ (WKB as an upper bound) are refuted and kept in this card as a negative result.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-18 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Recorded a counterexample reported in the PI's GPT 6 Pro session; status unchanged (proposed) pending reproduction | Shared chat https://chatgpt.com/s/t_6ad4b5574cc48191946a991871e10790 (final answer read in full); claim C-20261018-pi-chatgpt-01 |
| 2026-10-18 | claude-interactive.9 (claude; claude-opus-5-5) | Status proposed → refuted: the reported asymmetric-source counterexample was reproduced with a run id; Outcome records that the sech part is settled by C-20261018-pi-chatgpt-01 (C) | Run `2026-10-18-claude-interactive.9-asym-counterexample`; task T-20261018-claude-interactive-02; audit report `notes/audit-2026-10-18-claude-interactive.9-C-20261018-pi-chatgpt-01.md` |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5) | Rounding: the passive-mask gain is $+2.776\%$ ($\eta=0.2202282$ against TL 0.2142789), not 2.777%; found by the 2026-10-19 manuscripts | Task T-20261019-claude-interactive-15 |
