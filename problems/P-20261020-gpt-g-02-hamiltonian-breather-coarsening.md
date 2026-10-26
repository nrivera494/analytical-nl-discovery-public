---
id: P-20261020-gpt-g-02
title: "Condensation time and coarsening of breathers in the isolated Hamiltonian DNLS"
status: candidate
priority: 2
literature_state: open
novelty_confidence: medium
target_quantity: "The deterministic breather-density evolution and finite-size first-passage distribution to a macroscopic energy condensate above the DNLS infinite-temperature line, derived from breather-background exchange with backreaction."
model: "Closed nearest-neighbour focusing DNLS i dpsi_n/dzeta = -2|psi_n|^2 psi_n - psi_(n-1) - psi_(n+1), with conserved norm A and Hamiltonian H; periodic or explicitly specified reflecting boundaries."
oracle_ready: missing
last_audited: 2026-10-20
audited_by: [gpt, claude]
proposed_by: PI
provenance:
  agent: gpt-g
  model: gpt-6-astra
  family: gpt
claims: []
results: []
---

## Target quantity

For the isolated DNLS chain, determine the late evolution of the breather density $n_b(\zeta)$ and the distribution of the time needed to concentrate a fixed fraction of the excess energy in a single site. Use the convention

$$i\dot\psi_n=-2|\psi_n|^2\psi_n-\psi_{n-1}-\psi_{n+1},$$
$$A=\sum_n|\psi_n|^2,\qquad H=\sum_n\left[|\psi_n|^4+\psi_n^*\psi_{n+1}+\psi_n\psi_{n+1}^*\right],$$

with $a=A/M$, $h=H/M$, and $h>h_\infty(a)=2a^2$. This Hamiltonian sign convention is the one used in the cited DNLS statistical-mechanics literature; reversing the Hamiltonian sign also reverses the temperature convention.

One operational target is the distribution and median of

$$\tau_q=\inf\left\{\zeta:\ \max_n|\psi_n(\zeta)|^4\ge qM[h-2a^2]\right\},\qquad 0<q<1,$$

starting from a specified initially extended ensemble conditioned on $A,H$, with no initially macroscopic peak. Report whether threshold crossings are persistent condensates or short resonant bursts. The companion $n_b$ must use an explicitly stated amplitude threshold above the background and demonstrate insensitivity to that threshold in the proposed scaling regime.

The final answer must distinguish algebraic coarsening, activated/logarithmic coarsening, and a nonzero probability of persistent dynamical arrest. State the order of $M\to\infty$ and $\zeta\to\infty$. This card does not assume that every initial condition condenses, nor that an apparent numerical plateau proves arrest.

## Signal of hidden simplicity

The equilibrium problem has only two extensive constraints and a sharp infinite-temperature boundary, yet the deterministic dynamics appears much slower than conservative stochastic models with the same constraints. High breathers rotate rapidly and carry an approximate adiabatic invariant; rare changes of this invariant can dominate energy exchange. This provides a small parameter and a concrete escape mechanism rather than an unspecified search for a relaxation fit. Sources: Iubini et al. 2013, 2019; Baldovin et al. 2021; Politi et al. 2022.

## Literature state

### Longstanding evidence

- **Earliest explicit discrepancy located:** Rumpf, PRE 69, 016618 (2004), DOI [10.1103/PhysRevE.69.016618](https://doi.org/10.1103/PhysRevE.69.016618), [arXiv:nlin/0312058](https://arxiv.org/abs/nlin/0312058). **Full text**, complete preprint read. The entropy maximum is a single large peak, whereas simulations retain many pinned peaks; the conclusion warns that “the thermalization may have extremely long transients.” The paper gives a pinning/entropy explanation, but no quantitative closed-chain escape/coarsening law. This is an early persistent discrepancy, not an assertion that the paper leaves equilibrium unexplained.
- Rumpf (2009), DOI [10.1016/j.physd.2009.08.006](https://doi.org/10.1016/j.physd.2009.08.006), **abstract only**, with publisher-indexed introduction/section snippets also read. It explicitly revisits arrested growth and failure to reach the entropy maximum, and develops thermodynamics of metastable states. The full dynamics assessment remains a PI must-read.
- **Later direct statement:** Iubini, Franzosi, Livi, Oppo and Politi, *Discrete breathers and negative-temperature states*, NJP 15, 023032 (2013), DOI [10.1088/1367-2630/15/2/023032](https://doi.org/10.1088/1367-2630/15/2/023032). **Full text**, discussion/conclusion and model read from the Strathclyde author manuscript. The authors describe quasi-stationary multibreather states and write: “We still expect a final convergence towards the equilibrium state”. The missing quantity is the dynamical approach and its scale, not the entropy-maximizing state.
- Iubini, Politi and Politi, *Relaxation and coarsening of weakly-interacting breathers in a simplified DNLS chain* (2017), [arXiv:1701.08636](https://arxiv.org/abs/1701.08636). **Full text**, abstract, model, Secs. 4–5. The controlled stochastic surrogates connect amplitude-dependent exchange to coarsening, but their rare-transfer rule is imposed rather than derived from Hamiltonian DNLS.
- Baldovin, Iubini, Livi and Vulpiani, *Statistical mechanics of systems with negative temperature*, Phys. Rep. (2021), DOI [10.1016/j.physrep.2021.03.007](https://doi.org/10.1016/j.physrep.2021.03.007), [arXiv:2103.12572](https://arxiv.org/abs/2103.12572). **Full text**, DNLS equilibrium and dynamical sections, especially Sec. VI. It explicitly identifies predicted logarithmic coarsening without direct evidence and the freezing mechanism as open problems.
- Politi, Politi and Iubini, *Frozen dynamics of a breather induced by an adiabatic invariant*, J. Stat. Mech. 043206 (2022), DOI [10.1088/1742-5468/ac650e](https://doi.org/10.1088/1742-5468/ac650e), [arXiv:2201.02529](https://arxiv.org/abs/2201.02529). **Full text**, construction and Sec. 6. After discussing rare jumps of the adiabatic invariant, it states: “this is still an open problem.” The specific unresolved issue is a quantitative identification of the events that change that invariant.
- **Most recent direct multibreather restatement located:** Iubini and Politi, PRL 134, 097102 (2025), DOI [10.1103/PhysRevLett.134.097102](https://doi.org/10.1103/PhysRevLett.134.097102), [arXiv:2406.15140](https://arxiv.org/abs/2406.15140). **Full text**, main paper. After solving a reservoir-driven single-breather metastability problem, its conclusion discusses a multibreather generalized ensemble: “This generalization is, however, not straightforward; it requires further work.”
- Giachello, Iubini, Livi and Gradenigo (2025), DOI [10.1088/1742-5468/ae17ab](https://doi.org/10.1088/1742-5468/ae17ab), [arXiv:2503.14364v2](https://arxiv.org/abs/2503.14364v2). **Full text**, model, finite-size discussion, conclusion and Appendix B. Hamiltonian simulations support equilibrium finite-size predictions, but Appendix B explicitly leaves the type of ergodicity breaking and aging undetermined. The paper also cautions that localized-phase microcanonical correlations preclude treating the remaining sites as a statistically independent infinite-temperature reservoir.
- **Latest adjacent limitation:** Giusfredi, Iubini, Politi and Politi, J. Stat. Mech. 053201 (2026), DOI [10.1088/1742-5468/ae625e](https://doi.org/10.1088/1742-5468/ae625e), [arXiv:2511.09206](https://arxiv.org/abs/2511.09206). **Full text**, model and conclusion. Their mean-field thermodynamics explicitly leaves the metastable-homogeneous to localized-equilibrium transition outside its dynamics. This is supporting evidence about that paper's scope, not an independent proof of the gap.

### Resolution audit

| Located resolution or mechanism | Assessment for this target |
|---|---|
| Rumpf (2004, 2008, 2009), DOI 10.1103/PhysRevE.69.016618, [10.1103/PhysRevE.77.036606](https://doi.org/10.1103/PhysRevE.77.036606), 10.1016/j.physd.2009.08.006; **full text** (2004), **abstract only** (2008/2009, plus 2009 indexed introduction) | Entropy-driven condensation, transition statistics and metastable-state potentials are established prior art. Pinning and balanced peak growth explain finite-time plateaus; they do not supply the later rare-jump kernel or the full Hamiltonian coarsening-time distribution. The 2009 full text is requested before deriving such a kernel. |
| Rumpf (2007), DOI [10.1209/0295-5075/78/26001](https://doi.org/10.1209/0295-5075/78/26001); **not accessed** directly, located via institutional publication list and discussed in the later DNLS literature | Growth/erosion from phonon coupling is established prior art, as described in Rumpf 2009 and the negative-temperature review. Full text is a PI must-read before claiming a new exchange calculation. |
| Conservative stochastic coarsening: Iubini–Politi–Politi, J. Stat. Phys. (2014), DOI [10.1007/s10955-013-0896-4](https://doi.org/10.1007/s10955-013-0896-4), [arXiv:1308.4870](https://arxiv.org/abs/1308.4870); **full text**, abstract/model and coarsening argument | The stochastic model's coarsening exponent is explained. Phase dynamics and amplitude-dependent deterministic decoupling are absent. It is a baseline, not an unresolved result to reclaim. |
| Dynamical freezing: Iubini et al., PRL 122, 084102 (2019), DOI [10.1103/PhysRevLett.122.084102](https://doi.org/10.1103/PhysRevLett.122.084102), [arXiv:1811.05798](https://arxiv.org/abs/1811.05798); **full text**, main mechanism and conclusion | Identifies exponentially slow exchange and an approximate adiabatic invariant. Does not derive a closed-chain multibreather coarsening/first-passage law. |
| Equilibrium condensation and finite-size large deviations: Gradenigo et al. (2021), DOI [10.1088/1742-5468/abda26](https://doi.org/10.1088/1742-5468/abda26), and companion DOI [10.1140/epje/s10189-021-00046-5](https://doi.org/10.1140/epje/s10189-021-00046-5), [arXiv:2106.03698](https://arxiv.org/abs/2106.03698); [arXiv:1910.07461](https://arxiv.org/abs/1910.07461); **full text of both preprints**, introductions and thermodynamic/finite-size discussion | Solves a thermodynamic/ensemble-inequivalence question near infinite temperature. It does not determine Hamiltonian transition times. Finite-size thermodynamics is not proposed as novel here. |
| Giachello et al. (2025), above | Validates equilibrium microcanonical predictions and exposes global correlations; its finite-time correlation plateaus do not determine the asymptotic coarsening law. |
| Onorato et al. (2022), DOI [10.1103/PhysRevE.105.014206](https://doi.org/10.1103/PhysRevE.105.014206); **full text**, CHORUS introduction/model read via web | Negative-temperature wave kinetics is restricted to weak random-phase waves; the authors explicitly exclude solitons/breathers from that closure. |
| 2022 adiabatic invariant | The detailed construction uses unidirectional forcing: the background does not feel the breather. Restoring backreaction and quantifying rare jumps are substantive remaining steps. Merely constructing another low-order invariant is below this card's bar. |
| 2025 effective grand-canonical theory | Derives a temperature-dependent metastable lifetime and incorporates exponentially suppressed diffusion in a single-breather reservoir setup. The proposed problem conserves both global quantities and includes interacting breathers. Re-labelling its Kramers estimate as a new result is excluded. |
| 2026 mean-field DNLS and optical nonideal-RJ thermodynamics, arXiv:2511.09206 and [arXiv:2602.13161](https://arxiv.org/abs/2602.13161); **full text**, relevant theory/conclusions | Thermodynamics and Gibbsian stationary mode populations, not the deterministic non-Gibbs coarsening route. |
| Ebrahimi–Drossel–Just (2025), DOI [10.1016/j.physd.2025.134905](https://doi.org/10.1016/j.physd.2025.134905); **full text**, model and conclusion | Deterministic localized-state thresholds and noisy breather decay are studied; no isolated collective coarsening law is derived. |
| Giusfredi et al. (2025), DOI [10.1088/1742-5468/add1cd](https://doi.org/10.1088/1742-5468/add1cd), [arXiv:2503.04461](https://arxiv.org/abs/2503.04461); **abstract only** | Boundary-driven stochastic peak creation is a different ensemble and process. |
| Kati et al. (2026), DOI [10.1103/nfym-zysm](https://doi.org/10.1103/nfym-zysm), [arXiv:2601.13472](https://arxiv.org/abs/2601.13472); **full text**, Hamiltonian and discussion | A fully nonlinear compacton lattice has no linear hopping; its non-Gibbs thermalization does not close the standard DNLS target. |
| Ebrahimi–Drossel–Just (2026), [arXiv:2512.01448](https://arxiv.org/abs/2512.01448), DOI [10.1088/1402-4896/ae54df](https://doi.org/10.1088/1402-4896/ae54df); **full text**, abstract and model | A stochastic model with detailed balance and noise-dependent coarsening. External noise changes the slow process being asked about. |
| Das et al. (2026), [arXiv:2602.22878](https://arxiv.org/abs/2602.22878), DOI [10.1103/gjkp-21dh](https://doi.org/10.1103/gjkp-21dh); **full text**, abstract/model | Dephasing-induced relaxation of linear/nonlinear defects is a different open/noisy dynamics. |
| Archilla–Bajars–Flach (2025), [arXiv:2411.06044](https://arxiv.org/abs/2411.06044), DOI [10.1016/j.physd.2025.134551](https://doi.org/10.1016/j.physd.2025.134551); **full text**, model descriptions | Thermal lifetimes in other oscillator lattices do not determine the two-conservation-law closed DNLS coarsening process. |

### Kill search

On 2026-10-20, screened 2021–2026 forward citations of Rumpf 2004/2009, the 2019 freezing PRL and the 2022 invariant paper. Followed the 2025 reservoir and 2026 mean-field/stochastic results to their full texts. Targeted queries included:

- `"DNLS" "coarsening" 2024 2025 2026 Hamiltonian`
- `"DNLS" "logarithmic coarsening" 2022 2023 2024 2025 2026`
- `"breather" "coarsening" "deterministic" 2025 2026`
- `"DNLS" "adiabatic invariant" "2025" "2026" -site:researchgate.net -site:scribd.com`

No closed deterministic multibreather condensation-time law was located. The [review](../docs/review-2026-10-20-gpt-g-longstanding-optical-thermalization.md) records exact searches, source versions, indexed citation counts and failures. *Superseded on 2026-10-20 by claude-interactive.23 (novelty_confidence lowered to medium; see the second-family review below):* ~~**High provisional novelty** rests on the explicit longstanding dynamical discrepancy and those surviving model distinctions, not on the novelty of negative-temperature light itself.~~

### Second-family review (added by claude-interactive.23, claude, 2026-10-20)

This is the cross-family novelty review, task T-20261020-claude-interactive-05; the full assessment is in [the review](../docs/review-2026-10-20-claude-interactive.23-cross-family-novelty-gpt-g-cards.md). An independent Claude-family search (claude-interactive.23 and helper .23.2) found:
- no derivation, from the closed Hamiltonian dynamics above $h=2a^2$, of a late-time $n_b$ law or a condensation-time distribution;
- no rigorous arrest theorem for this regime.

The target is open. **Novelty is lowered from high to medium** for the reasons below. The PI decides (task T-20261020-claude-interactive.23-05).

- **The expected answer and its key input are already published.**
  - Iubini, Chirondojan, Oppo, Politi and Politi, PRL 122, 084102 (2019), [arXiv:1811.05798](https://arxiv.org/abs/1811.05798) (**full text**), study a breather on a positive-temperature background held by reservoirs. They fit an adiabatic-invariant diffusion $D\approx e^{-\gamma b}$ with $\gamma=1.13\pm0.09$. For the isolated chain they conclude that condensation "proceeds through a practically unobservable logarithmic coarsening".
  - The mechanism behind that conclusion is in Iubini, Politi and Politi (2017), [arXiv:1701.08636](https://arxiv.org/abs/1701.08636) (**full text**, Sec. 4): an exponentially small breather–background coupling gives logarithmic coarsening.
  - Inserting the fitted rate into that surrogate gives this card's likely answer. A Kramers estimate over the microcanonical large-deviation landscape, with the kinetic prefactor suppressed by the invariant as in Iubini and Politi (2025), gives an exponential first-passage law.
  - Helper .23.2 reached the same "modest adaptation" reading independently.
- **What remains open and would be new:**
  1. a first-principles rate and jump-size law for the events that change the invariant, with backreaction and both conservation laws (the 2022 open problem);
  2. whether the Markov closure behind logarithmic coarsening holds in the isolated chain;
  3. whether stability is super-exponential (Nekhoroshev-like), which would mean genuine arrest;
  4. the order of limits near the finite-size strip above the infinite-temperature line.

  A result on items 1–2 is a new result with clear precedent in the same field, which is level 3 of `docs/RANKING_RUBRIC.md`. It would be high novelty if it overturned the prediction or were rigorous.
- **Additional longstanding evidence.** The 2017 paper states that the macroscopic relaxation law to the single-breather state "is still open". This is a more direct statement than the 2004 caution.
- **Wording of the 2013 quotation.** The 2012 arXiv preprint of Iubini et al. (2013), arXiv:1203.4162v1, reads "a convergence" where the quotation above, from the published manuscript, reads "a final convergence". The meaning is the same.
- **Neighbours not listed above.** None closes the target.
  - Iubini et al. (2013): an isolated chain with $N=4096$ up to $t\sim10^7$ shows a quasi-stationary multibreather state with no visible coarsening (helper, full text).
  - Kalish, Fittipaldi de Castro and Benalcazar, [arXiv:2512.07774](https://arxiv.org/abs/2512.07774): a numerical order parameter for the nonergodic transition (abstract).
  - Johansson and Aubry (2000) and Johansson (2001): the lowest-order breather–phonon channels vanish for large breathers (helper, abstracts).
  - Rigorous metastability with boundary dissipation: Eckmann and Wayne (2018, 2020); Cuneo, Eckmann and Wayne (2017) (abstracts).
  - Gotti, Iubini and Politi (2021, 2024): finite-size thresholds and stochastic coarsening (helper).
- **Platform numbers** (helper .23.2):
  - Femtosecond-written arrays reach about 2–3 coupling lengths on a 37-site domain (Kirsch et al., Nat. Phys. 2025).
  - Two-dimensional fibre-loop meshes have about $100\times100$ sites, with data shown to step 60 (Marques Muniz et al., Sci. Rep. 2019).
  - Moorcroft et al., [arXiv:2511.08355](https://arxiv.org/abs/2511.08355) (abstract), argue that weakly nonlinear discrete-time lattices relax to infinite temperature.
  - No optical observation of breather coarsening was found.

## Sharpest statement of the gap

A quantitative Hamiltonian theory must explain how rare resonant events defeat breather action conservation, how the two conserved quantities redistribute through the background, and how this collective process controls late coarsening and finite-size first-passage times. Equilibrium large deviations, a stochastic surrogate, or a reservoir-imposed temperature do not by themselves supply this dynamics.

A solution would settle a statistical-mechanics question debated since at least 2004 and determine whether negative-temperature optical localization is a transient with a predictable useful lifetime or a dynamically persistent ensemble on specified scales. The question matters to nonlinear-lattice dynamics, condensation theory, and synthetic optical thermodynamics.

## Analytical foothold and first derivation target

Separate a tall breather's fast phase from the background and construct its dressed action using the existing adiabatic-invariant normal form. **First derivation target:** for a specified microcanonical background, derive the conditional rate and size distribution of the rare events that change the dressed breather action, including the background's response to the breather. Test whether a local Markov jump description emerges or whether memory is essential. Retain global microcanonical correlations rather than imposing an independent thermal background, in light of Giachello et al. (2025).

A finite resonant breather–neighbour cluster supplies a tractable inner problem. Match it to the conditional background amplitude/phase distribution and impose conservation of both $A$ and $H$ during the event. The goal is a derived exchange kernel with a validity domain, not an assumed exponential coupling. Next incorporate two separated breathers and the transport time of the intermediate background, and derive the consequences for $n_b$ and $\tau_q$.

A positive-temperature single-breather relaxation problem is a useful calibration of the event kernel; success there alone would not solve the non-Gibbs coarsening problem. An obstruction to Markov closure should be documented rather than hidden in a fitted diffusion constant.

*Added by claude-interactive.23 (2026-10-20):* A sharper first target is to derive the exponent $c$ in $D\propto e^{-cb}$ for the 2022 unidirectional-coupling model.
- Fitted values exist for that model: $c\simeq1.07$ (the slope of $\ln D_{3/2}$ against $b_0$), and a Lévy toy model with tail exponent $\alpha=2.2$ that matches the distribution of invariant changes. Both were checked in the 2022 full text.
- The lowest-order breather–phonon channels vanish (Johansson 2001), so count the order of the first open multi-phonon resonance.
- Decide whether the rate is exponential or super-exponential in $b$.

This gives a usable scaling law, can be checked with a small integrator, and is a prerequisite for both the coarsening and the arrest questions. The card is not audited, so derivation waits for the PI's decision.

## Assumptions, dimensionless groups and regime

- Deterministic, homogeneous nearest-neighbour hopping, scalar on-site cubic Kerr response, no disorder, drive, damping, dephasing or thermal reservoir. Fix the boundary condition and random-phase launch ensemble.
- $M\gg1$, $a>0$ bounded away from zero and infinity in the chosen units, and $\delta=(h-2a^2)/a^2\in[\delta_0,\delta_1]$ with $0<\delta_0<\delta_1<\infty$. Hold $\delta$ fixed as $M$ increases, outside the finite-size transition layer. Require $\max_n|\psi_n(0)|^4/[M(h-2a^2)]\ll1$.
- For the fast-breather calculation, $b=|\psi_b|^2$, $b/a\gg1$, and $\epsilon_b=1/(2b)\ll1$. For a many-breather reduction require separation $\ell_b\gg1$; report the ordering of background equilibration, exchange, and propagation times rather than assuming it.
- An optical chain $i\partial_z A_n=-J(A_{n-1}+A_{n+1})-\gamma|A_n|^2A_n$ maps to these units through $\zeta=Jz$ and $\psi_n=\sqrt{\gamma/(2J)}A_n$. The dimensionless nonlinear rotation is $\gamma P_b/J=2b$. Keep the Kerr/coupled-mode approximation valid at the largest breather power.
- In a proposed experiment require $\alpha z_{\rm obs}\ll1$, phase-noise-induced action diffusion much smaller than the predicted Hamiltonian exchange, and pulse duration much longer than dispersive/walk-off broadening over $z_{\rm obs}$. For a synthetic lattice also require the per-step map parameter $\Delta\zeta\ll1$ and convergence to the Hamiltonian limit. A Floquet quasienergy or a gain-stabilized map must not be silently identified with $H$.

## Conjectures

None. Logarithmic coarsening is a literature-motivated possibility, not a result asserted here.

## Oracle

**Missing for this model.** The present multimode-fibre solver contains Kerr, Raman, self-steepening and modal dispersion, but no ready dedicated nearest-neighbour core-hopping chain evaluator. It also has no random linear coupling, though random coupling is not needed here. An eigenmode-basis mapping might be possible after supplying a physical core-overlap tensor; it is not an existing validated oracle.

Use a small dedicated Hamiltonian DNLS integrator with independently checked conservation of $A,H$. The first future calculation is the conditional action-jump statistics of one tall breather, then two breathers, before attempting coarsening. Numerical checks must separate action changes from integrator drift, use two integration schemes or systematic step convergence, vary background size and phase preparation, and compare distributions rather than only a single lifetime fit. Add weak phase noise as an explicit assumption-relaxation control: noise-assisted decay must extrapolate away if the proposed mechanism is deterministic. No such runs were performed here.

## Lab test

A coupled-core fibre with calibrated fixed nearest-neighbour coupling is the closest continuous-propagation realization. A nonlinear fibre-loop mesh can offer many observation steps, but must first establish the continuous DNLS limit and monitor energy drift. The negative-temperature optical thermodynamics experiment of Marques Muniz et al., Science 379, 1019 (2023), DOI [10.1126/science.ade6523](https://doi.org/10.1126/science.ade6523), is **abstract/accessible indexed article passages only** in this scout; it is a platform lead, not evidence that nonlinear breather condensation has already been measured. Full paper and supplement are requested from the PI.

Prepare a tall peak on a calibrated broad background, then a pair of peaks with variable separation. Measure the peak powers, coherent nearest-neighbour phases (to reconstruct $H$), and the distribution of energy-transfer bursts along propagation. Vary $\gamma P_b/J$ at fixed background invariants. A derived activated exchange law, a power law, and noise-induced erosion give different survival curves and different sensitivity to added phase noise. These local tests can discriminate the mechanism without claiming that a finite fibre observes the infinite-time condensate.

## How a solution would be recognized

A theory derived from the closed DNLS predicts the action-exchange kernel and a nontrivial coarsening or first-passage law over held-out $(a,\delta,M)$ and launch ensembles. It reconciles the known stochastic and reservoir limits while making a distinct prediction for deterministic backreaction. Independent simulations and a feasible survival/transfer experiment support the stated scaling, with numerical drift and external noise demonstrably smaller than the effect. A rigorous probability/time bound deciding arrest or excluding a claimed coarsening law would also qualify if it applies to the physical chain and observable.

## Risks and must-reads

- Obtain Rumpf 2007 and 2009 full texts to audit phonon exchange and metastable potentials before a new rate derivation.
- Initial ensembles can contain long-lived invariant structures; the claim must be probabilistic or ensemble-qualified.
- The background may not be a fast bath. The same rare dynamics that freezes a breather can invalidate standard Kramers or white-noise reductions.
- Finite-size equilibrium localization and finite negative temperatures cannot be interchanged with their thermodynamic limits.
- Work through the technical finite-size asymptotics in the 2021 large-deviation article before choosing a near-transition scaling window; this scout read its framing and relevant thermodynamic discussion, not every saddle-point calculation.
- Download the Science platform paper and supplement before promising a concrete fibre-loop implementation. Optical negative RJ temperature and nonlinear energy condensation are distinct regimes.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-20 | gpt-g (gpt; gpt-6-astra) | Created candidate; high novelty provisional, GPT literature review only | 2004 discrepancy and 2013 restatement; 2021 review; 2022 unresolved rare jumps; 2025 multibreather limitation; 2026 thermodynamic/stochastic kill checks |
| 2026-10-20 | claude-interactive.23 (claude; claude-opus-5-5) | Second-family novelty review (T-20261020-claude-interactive-05). Agrees that the target is open; does not agree that novelty is high. novelty_confidence high → medium; audited_by [gpt] → [gpt, claude]; status candidate, priority and literature_state unchanged. Marked the "high provisional novelty" sentence as superseded; added the second-family subsection and a sharper first target. PI decision requested in T-20261020-claude-interactive.23-05 | Iubini et al., PRL 122, 084102 (2019) and Iubini–Politi–Politi (2017), both full text; [review](../docs/review-2026-10-20-claude-interactive.23-cross-family-novelty-gpt-g-cards.md); helper search .23.2 |
