---
id: P-20261020-claude-interactive.22-02
title: "Light above infinite temperature in coupled-core fibre: the isolated-lattice route to non-Gibbs breather condensation and its length scales"
status: audited
priority: 2
literature_state: open
novelty_confidence: high
target_quantity: "For a specified initial ensemble and graph of isolated Hamiltonian DNLS above the thermodynamic infinite-temperature line: conditional breather exchange, multibreather coarsening or arrest, and first-passage lengths toward localization, retaining finite-background backreaction. Finite coupled-core fibre is a realization subject to a separate Raman/dispersion feasibility gate."
model: "Scalar lossless quasi-CW DNLS on a specified graph G: i dE_j/dz + C sum_{k adjacent to j} E_k + gamma |E_j|^2 E_j = 0. H_f = C sum_{edges (j,k)} (E_j E_k^* + c.c.) + (gamma/2) sum_j |E_j|^4, and total power are conserved. Ring and hexagonal graphs are separate cases. Initially no Raman, dispersion or loss; all must be tested as optical perturbations."
oracle_ready: partial
last_audited: 2026-10-20
audited_by: [claude, gpt]
proposed_by: PI
provenance:
  agent: claude-interactive.22
  model: claude-opus-5-5
  family: claude
claims: []
results: []
last_review:
  agent: gpt-h
  model: gpt-6-astra
  family: gpt
  date: 2026-10-20
  task: T-20261020-claude-interactive-06
---

**Current text added by gpt-h (gpt; gpt-6-astra), 2026-10-20.** Audited; high novelty retained for corrected isolated Hamiltonian collective dynamics, with optical feasibility explicitly unverified. The original scout text is retained below as superseded; the current assessment and source-access ledger are in the [cross-family review](../docs/review-2026-10-20-gpt-h-cross-family-novelty-claude-22-cards.md).

## Target quantity

Predict conditional energy/norm exchange between breathers and their finite background in isolated Hamiltonian DNLS, then collective coarsening or arrest and first-passage distributions. Specify the launch ensemble, actual conserved energy, graph and event criterion; $(a,\delta,N)$ alone need not select a unique prethermal state.

With $A_j=\gamma|E_j|^2/(2C)$ and $t=Cz$, use

$$H=\sum_j A_j^2+2\sum_{(j,k)\in G}\sqrt{A_jA_k}\cos(\phi_j-\phi_k),
\qquad a=N^{-1}\sum_jA_j,\quad h=H/N.$$

The usual thermodynamic reference is $h=2a^2$. This is not an exact localization boundary for every small graph. The historical ground-state expression $a^2-2a$ applies to the degree-two bipartite ring, not every odd ring or hexagonal cluster.

**Launch correction.** Independent random phases imply $\mathbb E[h/a^2]=N/k$ for $k$ equally powered lit sites; they do not imply that value shot by shot. It is exact without the average when occupied sites have no connecting edges, or their hopping energy is controlled. Measure phases or condition on actual $H$ before classifying a launch.

## Longstanding evidence

Primary full-text checks by gpt-h confirm the long-lived-state question in Rasmussen 2000 (DOI:10.1103/PhysRevLett.84.3740), Rumpf 2004 (DOI:10.1103/PhysRevE.69.016618), the 2013 NJP paper (DOI:10.1088/1367-2630/15/2/023032), Mithun 2018 (arXiv:1712.03375), and the 2021 review (arXiv:2103.12572).

**Corrections to the old quotations/context:** the convergence sentence comes from the short arXiv:1203.4162v1 precursor. The NJP density exponent and future-universality discussion refer to stochastic microcanonical Monte Carlo, not full DNLS coarsening. The deterministic simulations show much stronger slowing. The 2021 freezing statement predates the 2022 invariant analysis.

The decisive current source is Iubini–Politi 2025, [DOI:10.1103/PhysRevLett.134.097102](https://doi.org/10.1103/PhysRevLett.134.097102), [arXiv:2406.15140](https://arxiv.org/abs/2406.15140), main text/conclusion read: reservoir metastability is treated, while multibreather statistical constraints and isolated collective evolution remain unresolved.

## Literature state

**Audited by Claude and GPT; high novelty retained for isolated collective dynamics.** This does not certify the original ensemble ansatz, finite-fibre parameter window or novelty of static distributions. A new exponential lifetime fit, entropy calculation or localized optical spot is insufficient.

## Kill search

Equilibrium localization, finite-size corrections and non-Gibbs ensemble distinctions are established prior work. Gradenigo et al. 2021 (arXiv:1910.07461, full relevant text) derives an asymptotic finite-size matching scale; it does not directly calibrate a few-core graph.

**Superseded:** the old account of Iubini 2019 as providing no time-scale law. Its full text reports exponentially increasing lifetimes and hopping times ([arXiv:1811.05798](https://arxiv.org/abs/1811.05798)). Politi 2022 derives adiabatic invariants in a unidirectionally coupled setting ([arXiv:2201.02529](https://arxiv.org/abs/2201.02529), full relevant text). Stochastic surrogate coarsening and reservoir activation do not automatically transfer to the isolated deterministic chain.

Giachello 2025's finite-size microcanonical correlations (arXiv:2503.14364v2) and Giusfredi 2026's mean-field metastability (arXiv:2511.09206), relevant full text read, further restrict a simple bath approximation. Ramos 2020 (DOI:10.1103/PhysRevX.10.031024) and Kabat 2026 (arXiv:2602.13161), full relevant text, do not close isolated non-Gibbs coarsening. Rumpf 2007/2009 full texts remain prior-art gaps; their access levels are explicit in the review.

## Sharpest statement of the gap

A predictive collective exchange/coarsening or arrest law for isolated Hamiltonian DNLS, retaining phase dynamics, microcanonical background backreaction and initial-ensemble dependence. No closure of this corrected target was found in the documented search. Static thermodynamics and single-breather lifetimes are substantial known ingredients, not missing theories.

## Analytical foothold and first derivation target

Derive or falsify a conditional rare-jump kernel for a tall breather's **dressed adiabatic action**, with exact energy/norm exchange and finite-background backreaction. Test when a Markov reduction is valid before combining pair transfers into coarsening.

**Superseded:** instantaneous powers above an arbitrary cutoff as exact constraints, and the assertion that conditioning on them necessarily leaves an ordinary Gibbs background. The 2025 PRL already proposes an MB-GGE as future work; deriving its constraints, weights and validity would be needed. A fit for $A_*$ is not a first-principles prediction.

## Dimensionless groups and regime

Use $a$, $\delta=h/a^2-2$, graph/size $N$, coupling distance $CL$, detuning $\sigma_\varepsilon/C$, and dispersive/Raman/loss perturbations. The historical ranges are proposed scans, not an established observation window. Classify each realization by full $H$ and account for finite-size effects before invoking a thermodynamic phase diagram.

For lit fraction $f=k/N$ and fixed hot-core power, $\gamma P_{\rm hot}=2aC/f$. With the assumptions in run 2026-10-20-claude-interactive.22-resonance-kinematics/raman_budget.json, the quasi-CW Raman estimate gives $CL\lesssim\Phi_{\max}f/(2a)$. Its approximate 25-radian value is setup dependent, not universal (DOI:10.1364/CLEO_SI.2015.SW4L.7, primary abstract read).

**Pulsed correction:** walk-off must precede substantial gain, approximately $\gamma P_{\rm hot}L_W\lesssim\Phi_{\max}$ in the same simplified model. $L_W<L$ and $L\ll L_D$ alone do not establish a safe window. The former claim that the proposed picosecond pulses permit $CL$ of order $10^2$ remains unverified. Track evolving pump/Stokes fields and gain along characteristics.

The illustrative arithmetic [run 2026-10-20-gpt-h-raman-walkoff-check](../runs/2026-10-20-gpt-h-raman-walkoff-check/summary.json) gives a concrete counterexample to an automatic walk-off guarantee: with $N=19$, $k=6$, $a=0.5$, $C=10\,{\rm m}^{-1}$, assumed effective area $80\,\mu{\rm m}^2$ and the scout's 3 ps walk-off estimate, about 16.5 kW per lit core reaches the assumed Raman threshold at $CL\simeq7.76$, before walk-off. This is a fixed-power estimate, not a calibrated fibre or propagation result.

## Oracle

Use a conservative DNLS evaluator with full-energy diagnostics, ensemble and step convergence, then independently check dispersion, Raman and loss. Separate ring and hexagonal graphs. Measure conditional flux, dressed-action jumps and event survival probabilities before extrapolating a late coarsening law. This review made only the arithmetic Raman check above, not a propagation run.

## Lab test

Coupled single-mode cores are credible, but a calibrated coupling/dispersion/nonlinearity model and pulsed Raman calculation must establish an accessible reduced prediction. Measure core powers **and relative phases** versus distance. Early formation or individual exchange may be accessible; late isolated coarsening in the proposed silica fibre has not been demonstrated.

The categorical absence of prior optical entry into this energy region is **superseded**: Iubini 2013 §5 already relates optical localized states to it. Marques Muniz 2023 (DOI:10.1126/science.ade6523, primary abstract/introduction preview read) concerns bounded-band negative-temperature RJ processes, and arXiv:2511.12080 (experimental setup/model read) uses laser-written multicore waveguides. Neither establishes the requested late-time fibre law. No controlled optical measurement of that law was found in this search.

## Relation to existing cards

Recommend **merge into P-20261020-gpt-g-02 as the theoretical home**, carrying this card's corrected optical mapping, phase measurements and feasibility gate into a realization section/task. Preserve both cards and audit history until the PI decides. The GPT card was read on origin/task/T-20261020-claude-interactive-03 and was not edited.

## Superseded scout text

<details>
<summary>Original 2026-10-20 scout formulation, superseded by the review above</summary>

This block preserves the initial hypotheses, evidence interpretations and access history. It is not the current card assessment. The changed metadata was:

- Former status: candidate
- Former last_audited: null
- Former audited_by: [claude]
- Former target_quantity: "For light in an N-core coupled-core fibre (discrete NLS) launched above the infinite-temperature line h = 2a^2: the statistics of the long-lived multi-breather state that forms first (breather number, breather-power distribution, background temperature), the formation length, and the relaxation length towards the single-breather microcanonical equilibrium, as functions of the norm density a, the excess delta = h/a^2 - 2 and N."
- Former model: "Discrete NLS for N identical, evanescently coupled single-mode cores: i dE_j/dz + C (E_{j+1} + E_{j-1}) + gamma |E_j|^2 E_j = 0 (ring or hexagonal graph), conserving the power and H_f = C sum_j (E_j E_{j+1}^* + c.c.) + (gamma/2) sum_j |E_j|^4. Scalar, lossless, quasi-CW (each time slice an independent lattice), no Raman. Extensions: core detuning disorder, dispersion (temporal continuum), Raman, loss."

### Superseded: Target quantity

**Variables.** Write $A_j=\gamma|E_j|^2/(2C)$ and $t=Cz$. The fibre Hamiltonian becomes $H=(\gamma/2C^2)H_f=\sum_jA_j^2+2\sum_j\sqrt{A_jA_{j+1}}\cos(\phi_j-\phi_{j+1})$. This is the convention of Rasmussen et al. (2000) and Iubini et al. (2013). It has:
- norm density $a=\gamma\bar P/(2C)$, where $\bar P$ is the mean core power;
- energy density $h=H/N$;
- an infinite-temperature line at $h=2a^2$;
- a ground state at $h=a^2-2a$.

Above the line, $h>2a^2$, no grand-canonical (Gibbs) measure exists.
- **Large $N$.** The maximum-entropy state is one breather that holds the excess energy, on a background at infinite temperature (Rumpf 2004).
- **Finite $N$.** The microcanonical equilibrium stays extended, a delocalized negative-temperature state, up to a size-dependent localization threshold $\delta_c(N)>0$.
  - Gradenigo et al. (2021; abstract read by claude-interactive.22) put the first-order transition at the line in the large-$N$ limit, with subleading corrections controlling it.
  - Gotti et al. (2021) find a finite-size crossover $N^*\simeq\delta^{-\gamma}$, $\gamma\ge2$, in a stochastic model, which suggests $\delta_c(N)\to0$ as $N$ grows.
  - Iubini & Politi (2025; abstract read by claude-interactive.22) describe the extended states as a large-deviation mechanism that occurs for finite sizes in isolated systems.
- **Dynamics.** It does not reach the localized equilibrium on any observed time scale.

**Wanted.** Three things, as functions of $(a,\delta=h/a^2-2,N)$ for $N$ from 7 to about 61:
1. **The long-lived state.** The core-power distribution and the breather statistics of the multi-breather state that forms first: number of breathers, distribution of their powers, background temperature. The answer should be a constrained-maximum-entropy (generalized Gibbs) ensemble with explicit constraints, or a proof that none describes the state.
2. **The formation length** $z_f$ of that state.
3. **The relaxation length** $z_r$ towards the single-breather equilibrium: a scaling law or an activation law in $\delta$, $a$ and $N$.

**Launch geometry decides the side of the line.** For random relative phases between cores, the hopping term averages to zero, so $h/a^2=\langle P_j^2\rangle/\langle P_j\rangle^2$ over cores. A launch into $k$ of $N$ cores with equal powers has $h/a^2=N/k$. It lies above the line exactly when $k<N/2$, whatever the power; the power sets $a$.

### Superseded: Longstanding evidence

- **Earliest.** Rasmussen, Cretegny, Kevrekidis & Grønbech-Jensen, PRL 84, 3740 (2000), [DOI:10.1103/PhysRevLett.84.3740](https://doi.org/10.1103/PhysRevLett.84.3740). The infinite-temperature line and breather formation beyond it; long transients. **Not accessed** (Crossref record).
- **Explicit statement.** Iubini, Franzosi, Livi, Oppo & Politi, NJP 15, 023032 (2013), [arXiv:1203.4162](https://arxiv.org/abs/1203.4162). Of Rumpf's single-breather equilibrium: "Convergence to such equilibrium states, however, has never been observed". **Full text** (passage read by claude-interactive.22, arXiv HTML). They also measure a breather-density decay $t^{-\alpha}$ with $\alpha\approx0.37$ and leave its universality class "to future investigations".
- **The statistical description is named as missing.** Mithun, Kati, Danieli & Flach, PRL 120, 184101 (2018), [arXiv:1712.03375](https://arxiv.org/abs/1712.03375): in the ergodic part of the non-Gibbs phase, "the Gibbs distribution should be replaced by an unknown modified one". Abstract, read by claude-interactive.22. Kabat et al. (2026) cite this paper as the discovery of the non-Gibbsian thermalization regime.
- **Review restatement.** Baldovin, Iubini, Livi & Vulpiani, Phys. Rep. 923, 1 (2021), [arXiv:2103.12572](https://arxiv.org/abs/2103.12572): "the dynamical origin of the freezing mechanism is not clear at all". **Full text** (DNLS section read by claude-interactive.22). The same section says logarithmic breather coarsening is expected, but "no direct evidence has been found".
- **Most recent restatements.**
  - Iubini & Politi, PRL 134, 097102 (2025), [arXiv:2406.15140](https://arxiv.org/abs/2406.15140): negative-temperature condensation "has challenged statistical mechanics for a long time". Their conclusion says a generalized Gibbs ensemble for multi-breather states needs further work. **Full text** (introduction and conclusions; helper claude-interactive.22.2).
  - Kabat, Mohapatra, Kevrekidis & Kottos, PRL 137, 103803 (2026), [DOI:10.1103/372m-bnpr](https://doi.org/10.1103/372m-bnpr), [arXiv:2602.13161](https://arxiv.org/abs/2602.13161). Their interacting Rayleigh–Jeans theory covers only the Gibbs region, and they name multicore fibres as a platform. On the non-Gibbs region: "Relevant studies are currently in progress and will be reported in future publications." **Full text** (conclusion read by claude-interactive.22).

**Claimed resolutions and why they do not close the problem.**

| Work | What it settles | What it leaves |
|---|---|---|
| Rumpf, PRE 69, 016618 (2004), [DOI:10.1103/PhysRevE.69.016618](https://doi.org/10.1103/PhysRevE.69.016618) (not accessed) | Entropy argument: one breather plus an infinite-temperature background | No dynamics |
| Gradenigo, Iubini, Livi & Majumdar, J. Stat. Mech. (2021) 023201, [arXiv:1910.07461](https://arxiv.org/abs/1910.07461) (abstract only, helper) | Microcanonical large deviations; a first-order localization transition above the line; ensemble inequivalence | Equilibrium only |
| Iubini et al., PRL 122, 084102 (2019), [arXiv:1811.05798](https://arxiv.org/abs/1811.05798) (abstract only, helper) | An adiabatic invariant freezes tall breathers; relaxation proceeds by rare events | Mechanism conjectured; no time-scale law |
| Politi, Politi & Iubini, J. Stat. Mech. (2022), [DOI:10.1088/1742-5468/ac650e](https://doi.org/10.1088/1742-5468/ac650e) (abstract only, helper) | Proves the adiabatic-invariant picture for a unidirectional DNLS with a passive background | Not the full DNLS |
| Iubini & Politi 2025 (above) | Open (grand-canonical) set-ups: negative-temperature states are metastable, with lifetime $\tau\approx e^{\lambda\lvert T\rvert}$ | Isolated multi-breather coarsening and its GGE |
| Gotti, Iubini & Politi, PRE 103, 052133 (2021); Giusfredi et al., J. Stat. Mech. (2025), [DOI:10.1088/1742-5468/add1cd](https://doi.org/10.1088/1742-5468/add1cd) (abstract only, helper) | Finite-size crossover and $N_b\sim\ln t$ coarsening in stochastic models | Stochastic surrogates only |
| Mithun, Kati, Danieli & Flach, PRL 120, 184101 (2018), [arXiv:1712.03375](https://arxiv.org/abs/1712.03375) (abstract, read by claude-interactive.22) | A crossover to weakly non-ergodic dynamics (infinite mean excursion time) inside the non-Gibbs phase, unseen by the largest Lyapunov exponent | Which ensemble replaces Gibbs in the ergodic part; no breather statistics or time scales |

### Superseded: Kill search

By helper claude-interactive.22.2 on 2026-10-20; full log in the review, §5.
- **Forward citations from 2021**, OpenAlex `cites:` filter: Rasmussen 2000 (70 citing works), Iubini 2013 (30), Iubini 2019 (37), Mithun 2018 (37). That is 107 unique titles, scanned.
- **Queries.** Seven WebSearch/WebFetch queries, for example:
  - `discrete nonlinear Schrödinger negative temperature breather condensation relaxation time open problem 2024`;
  - `experimental observation non-Gibbsian negative temperature discrete breathers photonic waveguide array OR fiber loop OR multicore fiber` (extended);
  - `multicore fiber discrete nonlinear Schrödinger thermalization negative temperature localization experiment coupled-core 2024 2025`.

**Second pass, claude-interactive.22, 2026-10-20.**
- **Forward citations from 2022**, OpenAlex:
  - Gradenigo et al., J. Stat. Mech. 2021: 28 citing works;
  - Gradenigo et al., EPJE 2021: 23;
  - Mithun 2018: 24;
  - Iubini & Politi 2025: 8;
  - Kabat 2026: 0.
- **Abstracts read.**
  - Transient ordering after quenches in the 3D Gross–Pitaevskii lattice, PRB 106, L201110 (2022). Slowly relaxing high-energy sites, on the Gibbs side.
  - Gotti, Iubini & Politi (2023), a stochastic model. Extremely large systems are needed to see the asymptotic distribution and the relaxation.
  - PRE (2026), [DOI:10.1103/nfym-zysm](https://doi.org/10.1103/nfym-zysm), a fully nonlinear DNLS variant. Ergodic dynamics outside the Gibbs region indicates "the need for a modified statistical description".
- **None is a kill.**

**Outcome.**
- No theory of the isolated-lattice coarsening, and no multi-breather GGE.
- No optical or fibre experiment in the non-Gibbs region. The optical negative-temperature experiments are all on the Gibbs side, where negative temperature comes from a bounded band:
  - multimode fibre (Baudin et al., PRL 130, 063801 (2023));
  - fibre-loop lattices (Marques Muniz et al., Science 379, 1019 (2023), [DOI:10.1126/science.ade6523](https://doi.org/10.1126/science.ade6523), abstract only);
  - multicore waveguides (Kirsch et al., [arXiv:2511.12080](https://arxiv.org/abs/2511.12080), abstract only).

### Superseded: Signal of hidden simplicity

- The non-Gibbs region is set by two numbers, $a$ and $h/a^2$. The equilibrium in it is known exactly in the large-$N$ limit (Gradenigo et al. 2021).
- Tall breathers are protected by an adiabatic invariant, so on intermediate scales their powers are effectively extra conserved quantities. That is the structure of a generalized Gibbs ensemble.
- The measured breather-density decay has a clean exponent, $\alpha\approx0.37$ (Iubini 2013).

### Superseded: Literature state

See the two tables above. Further context:
- Aceves, Luther, De Angelis, Rubenchik & Turitsyn, PRL 75, 73 (1995), [DOI:10.1103/PhysRevLett.75.73](https://doi.org/10.1103/PhysRevLett.75.73): collapse-type energy localization in fibre arrays, the deterministic ancestor. Bibliographic record only.
- Fibre-loop lattices are not the right platform. Moorcroft et al., [arXiv:2511.08355](https://arxiv.org/abs/2511.08355) (2025), show that Kerr split-step lattices heat to infinite temperature through quasi-energy Umklapp processes; full-text passages read by helper claude-interactive.22.2. Run `2026-10-20-claude-interactive.22-resonance-kinematics` confirms independently that these channels are kinematically open, with weight 0.40–0.51 of the normal channels (not converged). A loop conserves only the norm, so the line $h=2a^2$ is not defined there. Single-site collapse at mW power has been seen in coupled fibre loops (Muniz et al., Sci. Rep. 9, 9518 (2019), [DOI:10.1038/s41598-019-46060-8](https://doi.org/10.1038/s41598-019-46060-8); bibliographic record), but it is a different problem.
- Coupled-core (autonomous) fibre conserves $H$ and is the right platform.

### Superseded: Sharpest statement of the gap

For the isolated, Hamiltonian DNLS above the infinite-temperature line, three things are missing:
1. a statistical description of the multi-breather state that actually forms;
2. a law for its formation length;
3. a law for its relaxation length towards the known microcanonical equilibrium.

Each is missing both for $N\to\infty$ and at the finite $N$ of a fibre. The open-system lifetime (Iubini & Politi 2025) and the equilibrium (Gradenigo et al. 2021) are known; the isolated route between them is not. No optical system has been put in this region.

### Superseded: Analytical foothold and first derivation target

**First target: the multi-breather generalized Gibbs ensemble (MB-GGE).**
- **Construction.** Treat the powers $\{A_b\}$ of breathers above a threshold $A_*$ as conserved; they are adiabatic invariants to the order where the invariant is known. Maximize the background entropy at fixed $A_{\rm bg}=A-\sum_bA_b$ and $H_{\rm bg}=H-\sum_bA_b^2-\dots$.
- **The background is Gibbsian.** The background then sits on the Gibbs side, and Kabat et al.'s transfer-integral and interacting-RJ machinery applies to it.
- **Output.** A core-power distribution, a background temperature that depends on the breather content, and a self-consistency condition fixing $A_*$.
- **Test.** Against ensembles of direct DNLS runs at $N=7$, 19 and 61, on $(a,\delta)$ points not used in the construction.

**Second target: the breather nucleation rate per site from the launched state, which gives $z_f(\delta,a)$.**
- Route: a large-deviation estimate for the local norm of the background.
- Closed form expected when $\delta\gg1$: self-trapping of lit cores.
- Activation-type law expected as $\delta\to0^+$.

**Third target: the slow relaxation length $z_r$ for the isolated finite lattice.**
- Known pieces: the open-system activation law of Iubini & Politi (2025); the finite-size crossover $N^*\simeq\delta^{-\gamma}$ (Gotti et al. 2021).
- Guess: for small $N$ the single-breather state may be reached within fibre lengths.

### Superseded: Dimensionless groups and regime

| Group | Meaning | Card's range |
|---|---|---|
| $a=\gamma\bar P/(2C)$ | nonlinearity relative to coupling | 0.1–3 |
| $\delta=h/a^2-2$ | excess above the line; for random phases $\langle P^2\rangle/\langle P\rangle^2-2$ | 0–5 |
| $N$ | number of cores | 7–61 |
| $CL$ | coupling lengths travelled | 10–500 |
| $\sigma_\varepsilon/C$ | core-to-core detuning (disorder) | $\ll1$ |
| $L/L_D$, $L/L_W$ | dispersion length; pump–Stokes walk-off length | $L\ll L_D$; see Raman budget |
| $\gamma P_{\max}L_{\rm eff}$ | Kerr phase on the hottest core before stimulated Raman threshold | $\lesssim25$ rad (silica) |

**Raman budget** (run `2026-10-20-claude-interactive.22-resonance-kinematics`, `raman_budget.json`). With quasi-CW (ns) pulses in silica, stimulated Raman scattering limits the Kerr phase to about 25 rad at 1064 nm. For a launch into $k/N$ = 0.2–0.45 of the cores, that leaves only $CL\approx$ 2.5–22 coupling lengths for $a$ = 1–0.25. With 3–10 ps pulses, pump–Stokes walk-off ($L_W\approx0.6$ m per ps) caps Raman growth while $L_D$ = 0.45–5 km stays far above the fibre length. That regime allows $CL$ of order $10^2$; this is an estimate to be checked in the oracle runs.

### Superseded: Conjectures

None filed. Working hypothesis for the first target: above $\delta_c(N)$ the long-lived state is the MB-GGE, with a Gibbsian background whose temperature is set by the breather content. Between the line and $\delta_c(N)$ the state is extended, at negative temperature.

### Superseded: Oracle

- **The solver.** FastDifferentiableMMNLO has no coupled-core lattice model. An $N$-core fibre can be entered in the supermode basis, with the Kerr tensor of rank $N$ in the core basis, through the CP-decomposed many-mode backend. This has not been tried; hence `partial`.
- **A dedicated code is enough.** A symplectic (Yoshida 4th-order) DNLS integrator for $N\le61$ and $t\le10^6$ needs well under 1 GB.
- **Cheap test.**
  - Ensembles of 200 random-phase launches at fixed $(a,\delta,N)$, on both sides of $\delta=0$.
  - Record core-power histograms and breather counts against $t$, and compare with the MB-GGE.
  - Convergence: time step, and conservation of $A$ and $H$ to $10^{-8}$.
- **Missing.**
  - Raman and dispersion in a lattice code: needed for the ps lab regime; the solver can supply both if the supermode route works.
  - Core detuning disorder.

### Superseded: Lab test

**Platform.**
- A 7- or 19-core coupled-core fibre with $C\approx5$–$20$ m⁻¹.
- 3–10 ps pulses at 10–50 kW peak per lit core.
- Per-shot random relative phases imposed with an SLM.
- Launch into $k$ cores: $k/N<1/2$ puts the launch above the line, $k/N>1/2$ below it. Scan $a$ with power.

**Measurement.**
- Image the output cores shot by shot, at two or three cut-back lengths.

**Prediction that distinguishes** (the working hypothesis, not yet derived).
- Gibbs-side launches give core-power statistics described by the (interacting) RJ theory of Kabat et al.
- Launches with $0<\delta<\delta_c(N)$ give extended negative-temperature statistics: the modified distribution that Mithun et al. (2018) call unknown.
- Launches with $\delta>\delta_c(N)$ give a heavy-tailed distribution with a breather peak, whose weight and position the MB-GGE would predict.
- **Two changes of shape**, at $\delta=0$ and at $\delta_c(N)$, once $a$ is large enough for the lattice to be chaotic. The threshold in $a$ and the finite-$N$ value $\delta_c(N)$ at $N$ = 7–61 are part of the derivation. The equilibrium $\delta_c(N)$ follows from Gradenigo et al.; whether the dynamics reaches it within the fibre is the open part.
- No theory found in the kill search predicts the shape or the breather fraction on the non-Gibbs side.

### Superseded: How a solution would be recognized

1. **The long-lived state.** A closed-form or quadrature MB-GGE prediction matches simulated core-power histograms within statistical error on held-out $(a,\delta,N)$. It gets the breather fraction to within 10% for $\delta$ = 0.2–5.
2. **The formation length.** A $z_f(\delta,a)$ law whose predicted exponent or activation constant is confirmed by numerics over at least a decade in $\delta$.
3. **The relaxation length.** A $z_r(\delta,N)$ law: either an activation law with a computed constant, or a coarsening exponent with its universality class, consistent with the measured $\alpha\approx0.37$ or explaining it.
4. **The experiment.** It reproduces the changes of shape at $\delta=0$ and $\delta_c(N)$, and the predicted breather fraction, at two or more cut-back lengths.

### Superseded: Risks and must-reads

- **Competition.** The Kottos–Kevrekidis group says non-Gibbs studies are in progress (Kabat et al. 2026). The Iubini/Politi/Livi/Gradenigo group is active. Novelty has to be argued against their next papers.
- **Weak non-ergodicity.** Mithun et al. (2018) find weakly non-ergodic dynamics in part of the non-Gibbs phase. There no ensemble may apply, and the target must first map where an ergodic, modified ensemble holds.
- **Lab test.** It may only reach the formation stage. Coarsening needs far more coupling lengths than silica allows at $a\sim1$ (Raman budget).
- **The "breather" in a 7-core fibre is discrete self-trapping, known since the 1980s.** The statistical content (the shape at $\delta>0$) is what is new. My judgement, not checked, is that it needs $N\gtrsim19$ to be meaningful; check against Gradenigo's finite-$N$ results.
- **Must-reads, not yet accessed:**
  - Rasmussen et al. 2000;
  - Rumpf 2004 and 2008/2009;
  - Gradenigo et al. EPJE 44, 29 (2021);
  - the Mithun et al. 2018 full text and PRE 104, 014218 (2021);
  - the full text of Iubini et al. 2019;
  - the Marques Muniz et al. 2023 supplement (lattice size and round trips).

</details>

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-20 | claude-interactive.22 (claude; claude-opus-5-5) | Created as candidate on the PI's request for longstanding high-novelty thermalization problems; literature_state open; novelty high (explicit open statements 2013, 2021, 2025 and 2026; first-family kill search negative for the isolated-lattice route and for any optical non-Gibbs experiment); priority 2 pending PI decision | `docs/review-2026-10-20-claude-interactive.22-longstanding-optical-thermalization.md`; run `2026-10-20-claude-interactive.22-resonance-kinematics` |
| 2026-10-20 | gpt-h (gpt; gpt-6-astra) | Audited; high novelty retained for corrected isolated Hamiltonian collective dynamics, with optical feasibility explicitly unverified. Current scientific text replaced; superseded scout text retained. | Iubini–Politi 2025, DOI:10.1103/PhysRevLett.134.097102; Iubini 2019, arXiv:1811.05798; Politi 2022, arXiv:2201.02529 (full text); [review](../docs/review-2026-10-20-gpt-h-cross-family-novelty-claude-22-cards.md) |
