---
id: R-0014
title: "Fibre amplifier with a matched local oscillator: despite full ASE the matched mode is squeezed at short length when gamma∫P²/∫P > n_sp g, while in the similariton regime its phase variance grows as (32 n_sp/9) G Phi_NL² ∝ G^(7/3) and its minimum variance as G^(1/3)"
claim: C-20261019-pi-chatgpt-02
problem: P-001
tier: promising
status: accepted
type: noise-formula
proposer: pi-chatgpt
proposer_model: gpt-6-pro
proposer_family: gpt
verifier: claude-interactive.13
verifier_family: claude
auditor: null
auditor_family: null
solver_commit: "none: the verification used independent Python codes (run 2026-10-19-claude-interactive.13-similariton-lo-verification)"
promoted: 2026-10-19
pi_score: null
gates:
  G1: met
  G2: met
  G3: met
  G4: met
  G5: open
  G6: open
  G7: open
  G8: open
---

# Squeezing and phase noise of a fibre amplifier's matched mode

This result holds claim C-20261019-pi-chatgpt-02 **as verified on 2026-10-19**. GPT 6 Pro (family gpt) proposed it in the PI's ChatGPT session while verifying C-20261008-claude-a-02. claude-interactive.13 (family claude) verified it with its own two codes.

The superseded "if and only if" wording of part (ii) is not part of this result. Nor is the finite-length threshold claude-interactive.13 found beyond the claim, which is unverified by another family (task T-20261019-claude-interactive.13-03).

## 1. Problem

A normal-dispersion fibre amplifier adds phase-insensitive noise (ASE) while Kerr nonlinearity shears the field's quadratures. Problem [P-001](../../../problems/P-001-noise-around-nonsoliton-attractors.md) asks how the noise around the amplifier similariton, a non-soliton attractor, behaves.

The repository's earlier similariton claim, C-20261008-claude-a-02 (now [R-0011](../R-0011-similariton-shape-noise-exponents/RESULT.md)), made two statements that GPT 6 Pro found incorrect:
- that the matched-LO phase variance grows as $G/\varepsilon_0^2$;
- that "with ASE there is no squeezing".

This result is the corrected pair, plus the large-gain behaviour of the matched mode.

## 2. Result

**Model.** $\partial_zA=-\tfrac{i\beta_2}{2}\partial_t^2A+i\gamma|A|^2A+\tfrac g2A$, with $\beta_2>0$, power gain $G=e^{gz}$, and frequency-flat unsaturated gain with distributed ASE (factor $n_{sp}\ge1$) whose reservoir restores the commutator. The seed is a coherent state of $N_0$ photons, and the noise is linearized about the bright mean field. The **matched LO** is the output mean field. It reads the photon-number quadrature $X_A$ and the intensity-weighted phase quadrature $P_{\rm LO}=2\sqrt{N_{\rm ph}}\,\bar p$, with vacuum covariance $I$. $\Phi_{NL}=\int_0^z\gamma P_{\rm pk}\,dz'$.

**(ii) Short length, any smooth pulse and any dispersion.**
$$\boxed{\;\frac{d\lambda_{\rm LO}}{dz}\Big|_{0^+}=2n_{sp}g-2\gamma\frac{\int P^2\,dt}{\int P\,dt}=2n_{sp}g\,(1-R),\qquad R\equiv\frac{\gamma\int P^2dt}{n_{sp}g\int P\,dt}.\;}$$
The matched mode is squeezed at short length if $R>1$, and not if $R<1$. The thresholds are $\gamma P_0>\tfrac54n_{sp}g$ for a parabola and $\gamma P_0>\sqrt2\,n_{sp}g$ for a Gaussian $P_0e^{-t^2/T_0^2}$. At $R=1$ the $(gz)^2$ term, $2\,\mathrm{Var}_P(\gamma P/g)-n_{sp}$, decides; it is negative for both shapes at $n_{sp}=1$ and 2.

**(i) Large gain, parabolic similariton (reduced hydrodynamic model).** The number variance $C_{AA}=2n_{sp}G-(2n_{sp}-1)$ is exact. The phase variance is
$$\boxed{\;C_{PP}=\frac{32n_{sp}}{9}\,G\,\Phi_{NL}^2\,\big[1+O(G^{-1/3})\big]\ \propto\ \frac{G^{7/3}}{\varepsilon_0^2},\qquad \Phi_{NL}\sim\frac{3}{2\Gamma\varepsilon_0A_G}G^{2/3},\ A_G=(18/\Gamma^2)^{1/3}.\;}$$

**(iii) Large gain, minimum variance of the matched mode (same model).** $\lambda_{\min}(C_{\rm LO})=\det C_{\rm LO}/\lambda_{\max}\simeq C_{AA}(1-r^2)=\Theta(G^{1/3})$, so this mode ends up noisier than vacuum. This is a statement about this mode, not about every detection mode.

## 3. Regime of validity

| Dimensionless group | Definition | Lower bound | Upper bound | What fails outside |
|---|---|---|---|---|
| $R$ | $\gamma\int P^2/(n_{sp}g\int P)$ | — | — | (ii) decides the sign of the initial slope; $R=1$ needs the second-order term |
| $\tau=gz$ | Log power gain | (i), (iii): 12 | 80 (tested) | Below about 8 the (i) prefactor ratio departs from 1: 1.098, 1.106, 1.024 at $\tau=2$, 4, 6 for $\Gamma=\sqrt{18}$, and 0.766, 0.855, 0.935 for $\Gamma=1$ (`reduced_summary.json` of run `2026-10-19-claude-interactive.13-similariton-lo-verification`; corrected 2026-10-19) |
| $\Gamma$ | $g\sqrt{L_DL_{NL}}$ | 0.5 | 10 | Tested range for (i) and (iii) |
| $\varepsilon_0$ | $\sqrt{L_{NL}/L_D}$ at launch | — | 0.1 | The hydrodynamic reduction for (i) and (iii) |
| $\Phi_{NL}^2/N_0$ | Brightness | — | $\ll1$ | The linearization. With $\Phi_{NL}$ at $\varepsilon_0=0.05$, $\Gamma=\sqrt{18}$ (run `2026-10-19-claude-interactive.13-similariton-lo-verification`) and $N_0=2.6\times10^9$ it is $3\times10^{-6}$ at $\tau=4$, 0.17 at $\tau=12$ and $2\times10^{7}$ at $\tau=26$. The 500 pJ seed's own parameters ($\varepsilon_0=0.067$, $\Gamma=4.8$, run `2026-10-08-claude-a-amp-sim-checks`) give about 0.09 at $\tau=12$ at leading order (claude-interactive.20's check, `docs/manuscripts/2026-10-19-amplifier-noise-bounds/`). Either way, (i) and (iii) at large gain hold for the linearized model only |
| $n_{sp}$ | Spontaneous-emission factor | 1 | 2 (tested) | — |

There is no single small parameter. (ii) is exact at first order in $z$. (i) carries an $O(G^{-1/3})$ correction; the measured envelope exponent is $-0.334$.

**Assumption ledger:**
- scalar field, one mode, instantaneous Kerr;
- frequency-flat, unsaturated gain with a complete Langevin reservoir;
- no Raman, loss, higher-order dispersion or self-steepening;
- bright-field linearization with coherent input;
- for (i) and (iii), the parabolic hydrodynamic interior with Legendre shape modes and nondegenerate conditional noise;
- for (ii), a smooth launch (the sharp square-root parabola is reached as a limit of smoothed launches).

## 4. Derivation

- **(ii)** Expand the full linearized covariance equation at $z=0^+$, starting from the coherent input ($V=I$). Gain drift plus ASE add $2n_{sp}gI$. Passive dispersion has zero symmetric part at vacuum, so it drops out. Kerr adds a symmetric shear $2\gamma P(t)$ between amplitude and phase, which on the matched pair (mode $\propto\sqrt P$) has weight $2\gamma\int P^2/\int P$ and lowers the smaller eigenvalue at that rate. For a parabola, $\int P^2/\int P=4P_0/5$.
- **(i)** $C_{AA}$ follows exactly from photon-number conservation with the reservoir. On the asymptotic similariton, integration by parts gives $p_0=\Phi_{NL}n_0+R_0$, so $\mathrm{Var}\,p_0\sim\frac{8n_{sp}}{9N_0}\Phi_{NL}^2$, and $C_{PP}\simeq4N_{\rm ph}\mathrm{Var}\,\bar p$ with $N_{\rm ph}=N_0G$. The card of C-20261008-claude-a-02 already contained this $l=0$ formula; its stated $G/\varepsilon_0^2$ misread it.
- **(iii)** The leftover $l=2$ shape phase has variance of order $G^{2/3}/\varepsilon_0^2$, against $G^{4/3}/\varepsilon_0^2$ for the energy-driven phase, so $1-r^2=\Theta(G^{-2/3})$. Multiplying by $C_{AA}\propto G$ gives $G^{1/3}$.

claude-interactive.13 derived (ii) and the $O(G^{-1/3})$ rate of (i) before reading the proposer's material (commit 4ff455f), then checked the proposer's notes line by line: [audit note](../../../claims/notes/audit-2026-10-19-claude-interactive.13-C-20261019-pi-chatgpt-02.md), Parts 1 and 3. The proposer's derivation is in run `2026-10-18-pi-chatgpt-independent-verification` (`archive/similariton/TECHNICAL_NOTES.md`, sections 4–5).

## 5. Validation against numerics

![Matched-LO verification](../../../runs/2026-10-19-claude-interactive.13-similariton-lo-verification/fig_summary.png)

*Left: the full-field initial slope of $\lambda_{\rm LO}$, divided by $2n_{sp}$, against $R$ for smoothed parabolas and a Gaussian at $n_{sp}=1$ and 2 (open: held-out $n_{sp}=2$). Every point lies on $1-R$. Middle: the (i) prefactor ratio $C_{PP}/[(32n_{sp}/9)G\Phi_{NL}^2]$ against $\tau$ (dashed: held-out $\Gamma=1$). Right: $G^{-1/3}\lambda_{\min}(C_{\rm LO})$, reduced model (lines) and full field (points). Run `2026-10-19-claude-interactive.13-similariton-lo-verification` (claude-interactive.13, family claude); independent Python codes, no repository solver.*

- **(ii)** The initial slope equals $2n_{sp}g(1-R)$ to $7\times10^{-7}$, and its root lies within $3.3\times10^{-9}$ of $R=1$. The reservoir restores the commutator to $4\times10^{-13}$. Held-out $n_{sp}=2$ thresholds in $\gamma P_0/g$: 2.828427 for the Gaussian ($2\sqrt2$); for the parabola, 2.50699, 2.50030 and 2.500076 as the edge smoothing goes to zero ($5/2$). On the proposer's launch ($\varepsilon_0=0.05$, $\Gamma=\sqrt{18}$, $n_{sp}=1$, $\tau=0.02$), $\lambda_{\rm LO}=0.8964864646$–53, against the proposer's 0.8964864655.
- **(i)** The fitted power of $\varepsilon_0^2C_{PP}$ is 2.33350 over $12\le\tau\le26$ ($\Gamma=\sqrt{18}$) and 2.333333 over 26–40. Held-out $\Gamma=1$ gives 2.33175 and then 2.333314. The prefactor ratio lies in [0.99981, 1.00130] over 12–26 and within $3\times10^{-7}$ of 1 over 40–80. Its error shrinks as $G^{-0.334}$, against a predicted $-1/3$. The law also holds at $\Gamma=0.5$, 2 and 10.
- **(iii)** $G^{-1/3}\lambda_{\min}\in[0.338,0.633]$ over $12\le\tau\le26$ ($\Gamma=\sqrt{18}$) and $[0.247,0.797]$ at $\Gamma=1$, out to $\tau=80$. Full field at $\tau=4$: 3.1592357, against the proposer's 3.1592358.
- **Nonlinear check.** Truncated Wigner at $N_0=10^6$ agrees with the linearized squeezing within $1\sigma$. At $N_0\le10^4$ it shows less squeezing; whether that is physical or a limit of the method is unresolved.

Error scaling (expected figure 2) is shown by the (i) prefactor convergence in the middle panel.

## 6. Adversarial audit

- [verification-2026-10-19-claude-interactive.13.md](audit/verification-2026-10-19-claude-interactive.13.md) (claude; verdict pass). The verifier worked in an adapted clean context: Parts 1–2 were committed before any of the proposer's material was read. It found the "if and only if" boundary failure, which narrowed (ii). Because it was a verification task with no optimization-based search for counterexamples, it is filed as a verification, not as a G5 audit.
- **G5 is open:** a clean-context adversarial audit by a non-gpt family is task T-20261019-claude-interactive.13-01.
- A related clean-context GPT audit (gpt-e, run `2026-10-19-gpt-e-similariton`) of the parent claim C-20261008-claude-a-02 independently found the matched mode squeezed under complete ASE at $\tau=0.2$ ($\lambda=0.436717$). That supports (ii), but gpt-e shares the proposer's family, so it cannot count as this result's audit.

## 7. Novelty

- **Established ingredients:** Kerr conversion of amplitude to phase noise (Gordon & Mollenauer 1990, DOI 10.1364/OL.15.001351, abstract only); the amplifier quantum limit and reservoir (Caves 1982, DOI 10.1103/PhysRevD.26.1817; Drummond & Corney, arXiv:quant-ph/9912095). These are as recorded in the source report's bounded search.
- **Not located:** the similariton-specific powers $G^{7/3}$ and $G^{1/3}$, and the short-length criterion (ii), per GPT 6 Pro's bounded search.
- **claude-interactive.14's check** ([review](../../../docs/review-2026-10-19-claude-interactive.14-spie2016-similariton-noise.md)): Wang et al., Proc. SPIE 9893, 98930J (2016) and its journal version, Opt. Lett. 41, 5286 (2016) were first read at abstract level, then **in full** on 2026-10-19 after the PI's download ([full-text review](../../../docs/review-2026-10-19-claude-interactive-spie2016-fulltext.md)). Both measure classical total-power RIN only, with no quantum noise, phase noise or gain law. They anticipate none of (i)–(iii). A short search for (ii) found a related non-fibre proposal (arXiv:2603.11574, abstract only).
- **G6 is open** for one remaining item: a targeted prior-art search for (ii) (T-20261019-claude-interactive.14-03). The full texts are now read (.14-02, done).

## 8. Experimental test

**Short-length squeezing despite gain (ii).**
- **Setup:** seed a normal-dispersion Yb amplifier with a near-parabolic or Gaussian pulse at $R>1$; the 500 pJ parabolic seed of C-20261008-claude-a-01 has $R=2.5/n_{sp}$. Measure the output quadrature noise by homodyne detection with an LO derived from the output mean field, over a short gain length.
- **Prediction:** the matched-mode variance falls below shot noise at short length when $R>1$. Its initial slope is $2n_{sp}g(1-R)$, so lowering $\gamma P_0$ below the threshold, or raising $n_{sp}$, makes it rise.
- **Falsified by:** no sub-shot-noise matched-mode variance at $R$ clearly above 1 after correcting for detection efficiency, or no sign change of the slope near $R=1$.

**Large gain (i), (iii).** The phase-quadrature variance relative to shot noise should grow about as $G^{7/3}$ along a long similariton amplifier, and the matched mode should not be squeezed at large gain. Bright-field validity limits the gain over which this holds (section 3).

## 9. Open questions

- **G5:** a clean-context adversarial audit by a non-gpt family (T-20261019-claude-interactive.13-01).
- **The $\varepsilon_0$ rate** of the full field's approach to the reduced model (apparent exponent about 1.6): T-20261019-claude-interactive.13-02.
- **The finite-length threshold** beyond the claim (squeezing for $R>0.78$, parabola, or $R>0.90$, Gaussian, at $n_{sp}=1$; Claude-family only): whether to file it as a claim, T-20261019-claude-interactive.13-03.
- **Low photon number:** the truncated-Wigner shift at $N_0\le10^4$ is unresolved (recorded in the verification note).
- **G6:** a targeted prior-art search for (ii) (T-20261019-claude-interactive.14-03).
- **G7:** the figure script reads raw arrays kept at the run's `raw_location`. Regenerating them means rerunning the reduced-model propagation, which this write-up did not do.
- **G8:** not formalized. Part (ii) is a finite first-order covariance calculation and a candidate for Lean.
