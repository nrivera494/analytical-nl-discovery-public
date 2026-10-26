---
id: C-20261019-pi-chatgpt-02
problem: P-001
title: "Amplifier similariton, matched local oscillator: the phase-quadrature variance grows as (32 n_sp/9) G Phi_NL^2 ∝ G^(7/3)/eps0^2; despite full ASE a matched mode is squeezed at short gain iff gamma ∫P^2/∫P > n_sp g, while at large gain its minimum variance grows as G^(1/3)"
type: noise-formula
status: promoted
proposed_by: pi-chatgpt
proposer_model: gpt-6-pro
proposer_family: gpt
verified_by: claude-interactive.13
verifier_family: claude
verifier_model: claude-opus-5-5
audited_by: null
auditor_family: null
created: 2026-10-19
updated: 2026-10-19
solver_commit: "none: verification used independent Python solvers (run 2026-10-19-claude-interactive.13-similariton-lo-verification)"
result: R-0014
---

> **Provenance.** This result comes from the PI's ChatGPT session (GPT 6 Pro, family gpt) of 2026-10-18, which independently verified C-20261008-claude-a-02 and found two of its statements incorrect. These are the corrected statements. The orchestrator claude-interactive filed them on the PI's instruction. Sources: run [`2026-10-18-pi-chatgpt-independent-verification`](../runs/2026-10-18-pi-chatgpt-independent-verification/) (report sections 4.2–4.3; `archive/similariton/`), and the [review summary](../docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md).

## Statement

> **As verified (claude-interactive.13, family claude, 2026-10-19).** Run [`2026-10-19-claude-interactive.13-similariton-lo-verification`](../runs/2026-10-19-claude-interactive.13-similariton-lo-verification/), [audit report](notes/audit-2026-10-19-claude-interactive.13-C-20261019-pi-chatgpt-02.md).
> - **(i) verified.** Reduced model, independent Legendre covariance code: fitted power of $\varepsilon_0^2C_{PP}$ 2.33350 over $12\le\tau\le26$ ($\Gamma=\sqrt{18}$, asymptotic seed, $n_{sp}=1$), 2.333333 over 26–40. Held-out $\Gamma=1$: 2.33175 over 12–26, 2.333314 over 26–40; the ratio $C_{PP}/[(32n_{sp}/9)G\Phi_{NL}^2]$ lies in [0.99981, 1.00130] over 12–26 and within $3\times10^{-7}$ of 1 over 40–80. The ratio converges as $1+O(G^{-1/3})$, oscillating in $\ln G$ (measured envelope exponent $-0.334$; the $p_0$–$p_2$ cross-covariance). At $\tau\le8$ it is 0.86–1.11. The same holds at $\Gamma=0.5$, 2 and 10 with unchirped and chirped seeds: power 2.3309–2.3348 over 12–26, 2.33333 over 40–60.
> - **(ii) verified, with a boundary correction.** Full-field linearized code with both vacuum and both reservoir quadratures: the initial slope equals $2n_{sp}g(1-R)$, $R=\gamma\int P^2/(n_{sp}g\int P)$, to $7\times10^{-7}$, with its root within $3.3\times10^{-9}$ of $R=1$, for smoothed parabolas, a Gaussian and $n_{sp}=1,2$. Held-out thresholds: $2\sqrt2$ (Gaussian, 2.828427) and $5/2$ (parabola, reached as the smoothing $\delta\to0$: 2.50699, 2.50030, 2.500076 at $\delta=0.05$, 0.01, 0.005). The commutator is restored by the reservoir to $\le4\times10^{-13}$. Source counterexample reproduced: 0.8964864646–0.8964864653 on the source's launch. A truncated-Wigner (nonlinear) simulation at $N_0=10^6$ reproduces the linearized squeezing within $1\sigma$ ($\lambda_{\rm LO}=0.4729\pm0.0013$ at $\tau=0.3$, Gaussian).
>   - *Superseded wording:* "squeezed at short length **if and only if** $R>1$". At $R=1$ the slope vanishes and the $(gz)^2$ coefficient $2\mathrm{Var}_P(\gamma P/g)-n_{sp}$ (dispersionless) is negative for both shapes at $n_{sp}=1,2$ (full field: $-0.85$, $-1.41$, $-0.69$, $-0.76$), so the mode is squeezed there too. Read: squeezed at short length if $R>1$; not squeezed at short length if $R<1$.
> - **(iii) verified.** Reduced model: $G^{-1/3}\lambda_{\min}(C_{\rm LO})\in[0.338,0.633]$ over $12\le\tau\le26$ and [0.338, 0.625] over 26–80 ($\Gamma=\sqrt{18}$, $n_{sp}=1$; [0.247, 0.797] at $\Gamma=1$). Full field at $\tau=4$, $\varepsilon_0=0.05$: 3.1592357 on the source's launch (prediction 5: 3.159), 3.161 on mine; the matched mode stays squeezed up to $\tau\approx1.6$ ($\lambda_{\min}=0.38$ at $\tau=0.3$, $\varepsilon_0=0.05$).
> - **Not verified:** a rate for the full field's approach to the reduced model in $\varepsilon_0$ (apparent exponent about 1.6 at $\tau=4$). Accuracy of the linearization at moderate brightness: at $N_0\le10^4$ truncated Wigner gives less squeezing ($1/N_0$ shift, not separated from the method's validity limit), although $\Phi_{NL}^2/N_0\le3\times10^{-4}$ there. At $\varepsilon_0=0.05$, $\Phi_{NL}^2=4.4\times10^8$ at $\tau=12$ and $5.7\times10^{16}$ at $\tau=26$, so (i) and (iii) at large gain are statements about the linearized model.

**Setting.** As in C-20261008-claude-a-01/-02: normal-dispersion fibre amplifier, $\partial_zA=-\tfrac{i\beta_2}2\partial_t^2A+i\gamma|A|^2A+\tfrac g2A$, power gain $G=e^{gz}$. The amplifier is frequency-flat and unsaturated, with distributed ASE (factor $n_{sp}\ge1$) whose reservoir restores the commutator. The input is a coherent seed of $N_0$ photons. Quadratures have vacuum covariance $I$. The matched LO is the output mean field, giving the photon-number quadrature $X_A$ and the intensity-weighted phase quadrature $P_{\rm LO}=2\sqrt{N_{\rm ph}}\,\bar p$, with $\bar p=p_0-p_2/5$. $\Phi_{NL}=\int_0^z\gamma P_{\rm pk}\,dz'$.

**(i) Phase-quadrature growth.** In the parabolic similariton regime (reduced hydrodynamic model, fixed $\Gamma$ and $\varepsilon_0$), early-injected energy noise dominates the phase: $\mathrm{Var}(p_0)\sim\tfrac{8n_{sp}}{9N_0}\Phi_{NL}^2$. With $\Phi_{NL}\sim\tfrac{3}{2\Gamma\varepsilon_0A_G}G^{2/3}$ and $A_G=(18/\Gamma^2)^{1/3}$,
$$C_{PP}\sim\frac{32n_{sp}}{9}\,G\,\Phi_{NL}^2\ \propto\ \frac{G^{7/3}}{\varepsilon_0^2}.$$
This replaces $C_{PP}\propto G/\varepsilon_0^2$ in C-20261008-claude-a-02. The exact number variance $C_{AA}=2n_{sp}G-(2n_{sp}-1)$ is unchanged.

**(ii) Squeezing despite complete amplifier noise, at short gain.** For a smooth coherent mean and its matched LO, the smallest matched-LO covariance eigenvalue satisfies
$$\frac{d\lambda_{\rm LO}}{dz}\Big|_{0^+}=2n_{sp}g-2\gamma\frac{\int P^2dt}{\int P\,dt}.$$
So a matched mode is squeezed below vacuum at short length if and only if $\gamma\int P^2/\int P>n_{sp}g$ *[superseded 2026-10-19: "only if" fails at equality, where the second-order term decides; read "if $>$, and not if $<$"; see the verified block]*:
- a parabolic profile needs $\gamma P_0>5n_{sp}g/4$;
- a Gaussian $P_0e^{-t^2/T_0^2}$ needs $\gamma P_0>\sqrt2\,n_{sp}g$.

Phase-insensitive amplifier noise therefore does not forbid squeezing in a nonlinear amplifier.

**(iii) No squeezing of the matched mode at large gain.** In the reduced asymptotic model, $\lambda_{\min}(C_{\rm LO})=\det C_{\rm LO}/\lambda_{\max}\sim C_{AA}(1-r^2)=\Theta(G^{1/3})$. This is a statement about this specified mode, not about every optical detection mode.

## Regime

- (i) and (iii): parabolic hydrodynamic interior, $\varepsilon_0\le0.1$, low-order projections, $\Gamma$ of order 1 (tested at $\Gamma=\sqrt{18}$) *[verified 2026-10-19 for $0.5\le\Gamma\le10$, unchirped and $\Gamma/3$-chirped parabolic seeds, $n_{sp}=1$ (also $n_{sp}=2$ at $\Gamma=1$, $\sqrt{18}$); run `2026-10-19-claude-interactive.13-similariton-lo-verification`]*, log gain $12\le\tau\le26$. The prefactors oscillate in $\ln G$. Bright-field linearization needs $\Phi_{NL}^2/N_0\ll1$, which is not uniform in gain.
- (ii): any smooth coherent mean, at $z\to0^+$. The literal sharp square-root parabola is outside the classical $H^2$ domain; the statement uses smooth approximations, which preserve the strict inequality.
- Not bounded here: Raman, gain saturation and finite gain bandwidth. Fixed gain bandwidth makes the asymptotics an intermediate regime.

## Assumptions

1. Linearized (Bogoliubov) noise with a complete Langevin reservoir: $\langle dF^\dagger dF\rangle=gn_{sp}\,\delta\,dz$, $\langle dF\,dF^\dagger\rangle=g(n_{sp}-1)\,\delta\,dz$.
2. Instantaneous Kerr, one polarization and mode, unsaturated flat gain, no loss.
3. (i) and (iii) use the leading parabolic hydrodynamics with Legendre-mode separation, and early injection of the energy noise.
4. Generic nondegenerate covariance for the $\Theta(\cdot)$ envelope statements.

## Predictions

Frozen by the orchestrator on 2026-10-19 before any Claude-family verification. Values marked † are the source's; values marked ‡ are new.
1. **(i), source†.** Over $12\le\tau\le26$ ($\Gamma=\sqrt{18}$, $n_{sp}=1$, asymptotic seed), the fitted power of $\varepsilon_0^2C_{PP}$ against $G$ is $2.3335$ (prediction $7/3$). The card table P4 of C-20261008-claude-a-02 ($\varepsilon_0^2C_{PP}/G=3.81, 61.8, 701$ at $gL=2,4,6$) grows, consistent with $G^{4/3}$ before the asymptote.
2. **(i), held out‡.** At $\Gamma=1$ (the held-out amplifier of C-20261008-claude-a-02), the ratio $C_{PP}/[(32n_{sp}/9)G\Phi_{NL}^2]$ tends to 1, and the fitted power tends to $7/3$, as $\tau$ grows.
3. **(ii), source†.** Complete-ASE full-field calculation, smoothed parabola, $\varepsilon_0=0.05$, $\Gamma=\sqrt{18}$, $n_{sp}=1$, $\tau=0.02$: $\lambda_{\rm LO}=0.8964864655$.
4. **(ii), held out‡.** With $n_{sp}=2$, the initial slope changes sign at $\gamma P_0/g=5/2$ (smoothed parabola) and $2\sqrt2$ (Gaussian). It is negative above these thresholds and positive below.
5. **(iii), source†.** $\lambda_{\rm LO}\simeq3.159$ at $\tau=4$, $\varepsilon_0=0.05$ (full field). In the reduced model, $G^{-1/3}\lambda_{\min}(C_{\rm LO})$ stays bounded above and away from zero, oscillating in $\ln G$, for $12\le\tau\le26$‡.

## Derivation

The derivation is report sections 4.2–4.3 and `archive/similariton/TECHNICAL_NOTES.md` in the run. Auditors do not read these until their report is committed.
- **(i):** number conservation plus the reservoir gives $C_{AA}$ exactly; $p_0\simeq\Phi_{NL}n_0$ with the early energy noise.
- **(ii):** at $z=0$, passive dispersion has zero symmetric part at vacuum, gain drift plus ASE contribute $2n_{sp}gI$, and Kerr supplies an off-diagonal shear weighted by $\int P^2/\int P$ on the matched mode.
- **(iii):** the Schur complement.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Rates in $z^{-1}$; $\gamma P$ and $g$ are commensurate | claude-interactive (claude) | — | 2026-10-19 |
| Known limits | (ii) without Kerr gives $2n_{sp}g>0$ (a linear amplifier never squeezes). Without gain it gives $-2\gamma\langle P\rangle_P$ (Kerr squeezing). Checked by hand: $\int P^2/\int P=4P_0/5$ (parabola) and $P_0/\sqrt2$ (Gaussian) | claude-interactive (claude) | — | 2026-10-19 |
| Symbolic residual | (i) follows from C-20261008-claude-a-02's own $l=0$ formula, whose large-$G$ limit is $\mathrm{Var}(p_0)\to\tfrac{8n_{sp}}{9}\Phi_{NL}^2/N_0$. With $C_{PP}\simeq4N_{\rm ph}\mathrm{Var}(\bar p)$, $\bar p\simeq p_0$ and $N_{\rm ph}=N_0G$, this gives $\tfrac{32n_{sp}}{9}G\Phi_{NL}^2$. So that card's $G/\varepsilon_0^2$ contradicted its own formula | claude-interactive (claude) | — | 2026-10-19 |
| Simulation, core regime | Source: finite-volume covariance fit 2.33351 for the matched-LO phase power; the full-field counterexample 0.8964864655, with the commutator restored to $7\times10^{-14}$ | pi-chatgpt (gpt) | `2026-10-18-pi-chatgpt-independent-verification` | 2026-10-18 |
| Simulation, core regime | Independent codes. (i)/(iii): reduced Legendre covariance (reproduces C-20261008-claude-a-02 P4 to every digit); power of $\varepsilon_0^2C_{PP}$ 2.33350 over 12–26, 2.333333 over 26–40 ($\Gamma=\sqrt{18}$, asymptotic seed, $n_{sp}=1$); $G^{-1/3}\lambda_{\min}\in[0.338,0.633]$. (ii): full-field linearized NLSE, both vacuum and both reservoir quadratures, exact discrete adjoint; slope $=2n_{sp}g(1-R)$ to $7\times10^{-7}$, root within $3.3\times10^{-9}$ of $R=1$; on the source's launch $\lambda_{\rm LO}(0.02)=0.8964864646$–53; commutator restored to $\le4\times10^{-13}$ (without the reservoir it would be $G$) | claude-interactive.13 (claude) | `2026-10-19-claude-interactive.13-similariton-lo-verification` | 2026-10-19 |
| Error-scaling exponent | (i): $|C_{PP}/[(32n_{sp}/9)G\Phi_{NL}^2]-1|$ envelope $\propto G^{-0.334}$ ($\Gamma=\sqrt{18}$) and $G^{-0.332}$ ($\Gamma=1$), against $-1/3$ from the $p_0$–$p_2$ cross-covariance (derived in the audit report). Full field to reduced model at $\tau=4$: $\lambda_{\min}$ 4.2% above at $\varepsilon_0=0.05$, 1.3% at 0.025 (rate not established) | claude-interactive.13 (claude) | `2026-10-19-claude-interactive.13-similariton-lo-verification` | 2026-10-19 |
| Held-out region | (i) $\Gamma=1$: ratio in [0.99981, 1.00130] over 12–26 and $1\pm3\times10^{-7}$ over 40–80; power 2.33175 (12–26), 2.333314 (26–40), 2.3333331–2.3333334 (equal phase, 40–80). (ii) $n_{sp}=2$: sign change at 2.828427 (Gaussian) and $2/\kappa_\delta$ = 2.50699, 2.50030, 2.500076 ($\delta=0.05$, 0.01, 0.005; $\to5/2$ as $\delta^{1.98}$); negative above, positive below. (iii) $G^{-1/3}\lambda_{\min}\in[0.338,0.633]$ ($\Gamma=\sqrt{18}$), [0.247, 0.797] ($\Gamma=1$) over 12–26 | claude-interactive.13 (claude) | `2026-10-19-claude-interactive.13-similariton-lo-verification` | 2026-10-19 |
| Convergence and artefacts | Source: grid and step refinement changes $\lambda_{\rm LO}$ by $3.5\times10^{-9}$. Rerun by claude-interactive on a second platform: 0.8964864655 | pi-chatgpt (gpt); claude-interactive (claude) | `2026-10-18-pi-chatgpt-independent-verification`, `2026-10-19-claude-interactive-gpt6pro-quick-repro` | 2026-10-19 |
| Convergence and artefacts | Reduced: rtol $10^{-9}\to10^{-13}$ changes the power by $10^{-14}$; $C_{AA}$ exact to $7\times10^{-15}$. Full field: $N$ 2048–8192, window 8–12, steps ×4 change $\lambda_{\rm LO}(\tau=0.02)$ by $\le10^{-9}$; at $\tau=4$ steps ×2 change it by $8\times10^{-7}$, $N$ and window by $10^{-11}$; $C_{AA}=2n_{sp}G-(2n_{sp}-1)$ to $10^{-11}$ | claude-interactive.13 (claude) | `2026-10-19-claude-interactive.13-similariton-lo-verification` | 2026-10-19 |
| Second solver or relaxed assumption | (a) The full field relaxes the hydrodynamic leading order, the sharp edge and the dropped phase-quadrature noise: at $\tau\le4$, $\varepsilon_0^2C_{PP}/G$ is within 0.2% of the reduced model and $\lambda_{\min}$ approaches it as $\varepsilon_0$ and the edge smoothing shrink. (b) Truncated Wigner (nonlinear, stochastic; $2\times10^5$ trajectories, $N_0=10^6$, Gaussian, $\tau=0.3$): $\lambda_{\rm LO}=0.4729\pm0.0013$ against linearized 0.4729 ($n_{sp}=1$) and $0.7999\pm0.0024$ against 0.7978 ($n_{sp}=2$). At $N_0=10^4$ and $10^3$ it gives 0.488–0.492 and 0.63–0.69 (dependent on grid modes; not separated from the TWA validity limit) | claude-interactive.13 (claude) | `2026-10-19-claude-interactive.13-similariton-lo-verification` | 2026-10-19 |
| Adversarial audit | | | | |
| Novelty search | Source: established ingredients are Kerr conversion of amplitude to phase noise (Gordon–Mollenauer 1990) and the amplifier quantum limit (Caves 1982). The similariton-specific powers and the short-gain criterion were not located (bounded search) | pi-chatgpt (gpt) | — | 2026-10-18 |
| Novelty search | Wang, Liu, Song & Hu, Proc. SPIE 9893, 98930J (2016), DOI 10.1117/12.2227743, and Opt. Lett. 41, 5286 (2016), DOI 10.1364/OL.41.005286, read at abstract level (no open full text found). Both report classical total-power RIN only, with no phase, homodyne, shot-noise or squeezing content. (i), (ii) and (iii) are not anticipated. A bounded arXiv and web search found no fibre squeezing-with-gain criterion. The nearest conceptual neighbour is a two-mode Kerr amplifier, arXiv:2603.11574 (abstract only). A targeted search is open (T-20261019-claude-interactive.14-03). [Review](../docs/review-2026-10-19-claude-interactive.14-spie2016-similariton-noise.md) | claude-interactive.14 (claude) | — | 2026-10-19 |
| Novelty search | Full-text check (PI download, 2026-10-19) of Wang et al., Proc. SPIE 9893, 98930J (2016) and Opt. Lett. 41, 5286 (2016). Classical total-power RIN at a single gain; no quantum noise, phase noise or gain law; (i)–(iii) not anticipated. Verdicts of the abstract-level check confirmed: [review](../docs/review-2026-10-19-claude-interactive-spie2016-fulltext.md) | claude-interactive (claude) | — | 2026-10-19 |

## Outcome

**Sim-verified (2026-10-19)** by claude-interactive.13 (family claude) with independent codes; verdict pass ([audit report](notes/audit-2026-10-19-claude-interactive.13-C-20261019-pi-chatgpt-02.md), [summary](../docs/summary-2026-10-19-claude-interactive.13-C-20261019-pi-chatgpt-02.md)). (i)–(iii) hold. The wording of (ii) is narrowed: "if and only if" fails on the boundary $R=1$, where the second-order term squeezes the mode. (i) and (iii) at large gain are linearized-model statements ($\Phi_{NL}^2/N_0\ll1$ fails above $\tau\approx12$ for realistic seeds). Not done: a clean-context adversarial audit for status audited, and Raman, saturation or gain-bandwidth checks (excluded by the card).

**Promoted (2026-10-19).** As verified, the claim is promising result [R-0014](../results/promising/R-0014-similariton-matched-lo-phase-and-short-gain-squeezing/RESULT.md), on the PI's instruction. G5 (clean-context audit) is open: task T-20261019-claude-interactive.13-01.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Filed from GPT 6 Pro's verification report (proposer family gpt) with status cheap-checks-passed; held-out predictions frozen | Runs `2026-10-18-pi-chatgpt-independent-verification`, `2026-10-19-claude-interactive-gpt6pro-quick-repro` |
| 2026-10-19 | claude-interactive.14 (claude; claude-opus-5-5) | Novelty check of the SPIE 2016 lead (task T-20261019-claude-interactive-05); Novelty search row added; status unchanged | [Review](../docs/review-2026-10-19-claude-interactive.14-spie2016-similariton-noise.md) |
| 2026-10-19 | claude-interactive.13 (claude; claude-opus-5-5) | Claude-family verification. cheap-checks-passed → sim-verified; verified_by claude-interactive.13 (claude). Verified block added; "if and only if" in (ii) marked superseded (fails at $R=1$); Checks rows filled | Run `2026-10-19-claude-interactive.13-similariton-lo-verification`; [audit report](notes/audit-2026-10-19-claude-interactive.13-C-20261019-pi-chatgpt-02.md) |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Status sim-verified → promoted; result R-0014 (promising tier) | Task T-20261019-claude-interactive-12 |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5) | Full-text novelty check of the Wang et al. (2016) papers; verdicts unchanged; R-0014 Novelty updated | [review](../docs/review-2026-10-19-claude-interactive-spie2016-fulltext.md); task T-20261019-claude-interactive.14-02 |
