---
id: P-20261012-claude-interactive-02
title: "Maximum single-photon nonlinear phase in a non-dissipative Kerr medium"
status: candidate
priority: 2
literature_state: partial
novelty_confidence: low
target_quantity: "A resource-qualified phase-fidelity-bandwidth limit for a specified passive bulk-Kerr gate architecture; first resolve the material, geometry and interaction-time resources."
model: "Causal few-photon channel for a fixed bulk chi(3) response and passive time-independent architecture, with explicit finite geometry, feature scale, input/output modes, dwell-time resources and unconditional fidelity."
oracle_ready: missing
last_audited: 2026-10-13
audited_by: [gpt]
proposed_by: claude-interactive
claims: []
results: []
last_review:
  agent: gpt-b
  model: gpt-6-astra
  family: gpt
  document: docs/review-2026-10-13-gpt-b-frequency-conversion-novelty.md
---

## Target quantity

**PI question retained:** what limits the single-photon nonlinear phase in a nondissipative Kerr medium?

**Review scope (gpt-b; gpt-6-astra; gpt; 2026-10-13).** The current all-material/all-geometry formulation does not yet define a resource-bounded optimization. Keep this card as a candidate for an architecture-specific, high-fidelity two-photon gate bound. A phase estimated on a weak/coherent probe and a conditional phase of a two-photon quantum channel are different observables; they cannot share a fidelity constraint without a specified operational definition.

For a gate, specify input temporal modes, the output channel, allowed deterministic linear corrections, loss/leakage, and a fidelity metric. Conditional phase is periodic modulo $2\pi$; asking for its unwrapped maximum is not an operational gate objective. A useful formulation fixes a target phase and asks for the maximum unconditional gate fidelity or the minimum interaction resource required. If postselection is permitted, its success probability must be an explicit resource.

For a material/geometry bound, specify the microscopic response class or full causal response kernel, material spectra and transparency window, finite design domain, minimum feature size/nonlocal regularization, input bandwidth **and** allowed delay/storage/interaction length or round trips. A photon bandwidth does not by itself fix its dwell time. The original assumption that every structure has interaction time of order the inverse input bandwidth is unsupported. This audit does not prove that the strictly passive, time-independent bulk class is unbounded; it establishes that the proposed finite ceiling was not derived from the listed assumptions.

Keep three distinct subproblems: a material bound on the relevant third-order response; a geometric/temporal bound on the properly normalized interaction; and a quantum-channel fidelity bound in a fixed architecture. The classical overlap functional for distinct photon modes is generally a tensor-weighted product of their intensities/fields, not automatically a single-mode $\int|E_1|^4$. A nonlinear field-overlap estimate is not a gate-fidelity theorem.

## Literature state

**Verdict: open, narrowed; keep `candidate`.** The original orchestrator scan was explicitly unaudited. A combined resource-qualified bulk-Kerr bound was not located, but the universal gap as written is not established. This GPT review does not supply Claude-family agreement on the reformulated problem. Literature state changes from `unaudited` to `partial`; novelty confidence remains `low`.

The most consequential omitted material reference is Kuzyk's **third-order** molecular paper, DOI [10.1364/OL.25.001183](https://doi.org/10.1364/OL.25.001183), **abstract only**, with erratum DOI 10.1364/OL.28.000135 (**not accessed** beyond the publisher correction listing). The originally cited preprint physics/0510199 mainly develops second-order susceptibility and explicitly postpones a full third-order treatment (**full text**). Molecular few-level bounds are not automatically rigorous bulk-density bounds: Shafei and Kuzyk, [arXiv:1306.0937](https://arxiv.org/abs/1306.0937), **full text**, discuss formal many-state pathologies and the extra ansatz. That is a warning about sufficiency of sum rules, not proof of divergent response in a physically realizable bulk dielectric.

The linear-index analogy also needs qualification. Shim, Monticone and Miller, [arXiv:2103.15697](https://arxiv.org/abs/2103.15697), **full text**, constrain index using electron density **and** dispersion/bandwidth. Koutserimpas et al., [arXiv:2410.02002](https://arxiv.org/abs/2410.02002), **full text**, explain that causality does not give single-variable analyticity for every nonlinear frequency path, and that nonlinear oscillator strengths need not be positive. One cannot import the linear positive-oscillator extremum directly into degenerate Kerr response.

| Source and verified identifier | Access | Audit finding |
|---|---|---|
| Shapiro, DOI [10.1103/PhysRevA.73.062305](https://doi.org/10.1103/PhysRevA.73.062305) | abstract only | Exists and supports a causal-response-model fidelity obstruction; full text not obtained. Avoid extending the abstract's language to every dielectric architecture. |
| Shapiro and Razavi, [arXiv:quant-ph/0612086](https://arxiv.org/abs/quant-ph/0612086), DOI 10.1088/1367-2630/9/1/016 | full text | Continuous-time XPM response and phase-noise model; probe/parity-gate analysis is not an architecture-independent phase maximum. |
| Gea-Banacloche, [arXiv:0911.4682](https://arxiv.org/abs/0911.4682), DOI 10.1103/PhysRevA.81.043823 | full text | Local multimode interaction and bandwidth/fidelity tradeoff; stated assumptions matter. |
| Viswanathan and Gea-Banacloche, [arXiv:1712.03914](https://arxiv.org/abs/1712.03914), DOI 10.1103/PhysRevA.97.032314 | full text | Analytical high-fidelity conditional phase in a nonlocal, chi(2)-equivalent model with unequal velocities; not a counterexample inside strict local bulk Kerr. |
| Brod and Combes, [arXiv:1604.04278](https://arxiv.org/abs/1604.04278), DOI 10.1103/PhysRevLett.117.080502 | full text | Discrete atom-mediated counter-propagating architecture; fidelity allows specified single-photon distortion corrections. Not a transparent-bulk material bound. |
| Heuck, Jacobs and Englund, [arXiv:1909.05751](https://arxiv.org/abs/1909.05751), DOI 10.1103/PhysRevLett.124.160501 | full text | Memory citation verified. Strong classical controls change cavity coupling; storage and incident pulse duration are independent resources. This is outside a passive time-independent architecture. |
| Tian and Chen, [arXiv:2312.10719](https://arxiv.org/abs/2312.10719) | full text | Emitter/cavity photon-transport gate; does not establish a bound for transparent bulk chi(3). |
| Shim, Monticone and Miller, [arXiv:2103.15697](https://arxiv.org/abs/2103.15697), DOI 10.1002/adma.202103946 | full text | Index bound has dispersion/bandwidth conditions; no automatic nonlinear extension. |
| Kuzyk, DOI [10.1103/PhysRevLett.85.1218](https://doi.org/10.1103/PhysRevLett.85.1218), correction DOI 10.1103/PhysRevLett.90.039902 | abstract only; correction not accessed | Original source and correction metadata located. Molecular hyperpolarizability, not a universal bulk Kerr theorem. |
| Kuzyk, [arXiv:physics/0510002](https://arxiv.org/abs/physics/0510002) | full text | Truncation/ansatz assumptions are part of the theory, not consequences of macroscopic transparency alone. |
| Kuzyk, [arXiv:physics/0510199](https://arxiv.org/abs/physics/0510199) | full text | Main calculation concerns second-order molecular response; third-order response is proposed as subsequent work. |
| Kuzyk, DOI [10.1364/OL.25.001183](https://doi.org/10.1364/OL.25.001183), correction DOI 10.1364/OL.28.000135 | abstract only; correction not accessed | Omitted direct third-order molecular bound. Full corrected derivation remains to be checked. |
| Shafei and Kuzyk, [arXiv:1306.0937](https://arxiv.org/abs/1306.0937) | full text | Few-level ansatz and formal many-state catastrophe; does not prove a physically attainable bulk divergence. |
| Sheik-Bahae, Hagan and Van Stryland, DOI [10.1103/PhysRevLett.65.96](https://doi.org/10.1103/PhysRevLett.65.96) | full text | Located specific band-gap-scaling paper. Model/dispersion prediction, not a universal upper bound. |
| Sheik-Bahae et al., DOI [10.1109/3.89946](https://doi.org/10.1109/3.89946) | abstract only | Located the detailed bound-electronic-refraction paper; replaces the unidentifiable Handbook-chapter citation as an active source. |
| Shim, Fan, Johnson and Miller, DOI [10.1103/PhysRevX.9.011043](https://doi.org/10.1103/PhysRevX.9.011043) | full text | Vague memory citation resolved. Bandwidth-averaged response/LDOS limits do not directly bound the internal energy-normalized quartic interaction. |
| **Chen et al., 2018**, DOI [10.1038/s41467-017-02487-z](https://doi.org/10.1038/s41467-017-02487-z), [arXiv:1612.07427](https://arxiv.org/abs/1612.07427) | full text | Article year is **2018**, despite the DOI's 2017 string. Fiber XPM metrology with mixed probes/postselection; not a demonstrated high-fidelity two-photon gate. |
| Choi, Heuck and Englund, DOI [10.1103/PhysRevLett.118.223605](https://doi.org/10.1103/PhysRevLett.118.223605) | full text | Memory citation verified. Self-similar dielectric concentration is feature-size sensitive; peak-energy mode volume differs from nonlinear interaction volume. |
| Chang, Vuletić and Lukin, DOI [10.1038/nphoton.2014.192](https://doi.org/10.1038/nphoton.2014.192) | full text | Review located; covers resonant platforms outside the strict bulk-transparent class as well as general quantum nonlinear optics. |
| Yanagimoto et al., [arXiv:2203.11909](https://arxiv.org/abs/2203.11909), DOI 10.1364/OPTICA.473276 | full text | Vague Mabuchi-group lead resolved: auxiliary trap pulse and dispersion engineering; demonstrated model uses chi(2)-mediated gate dynamics. Additional control resources must be counted. |
| Li et al., [arXiv:2409.20351](https://arxiv.org/abs/2409.20351), DOI 10.1021/acsphotonics.4c01892 | full text | Resonant quantum-well second/third-order bounds, not the proposed general off-resonant bulk Kerr limit. |
| Koutserimpas et al., [arXiv:2410.02002](https://arxiv.org/abs/2410.02002) | full text | Clarifies nonlinear analyticity and signed sum-rule strengths; closes a logical shortcut in the proposed combination. |
| Zhao, Zhang and Miller, [arXiv:2008.13241](https://arxiv.org/abs/2008.13241) | full text | Fabrication-constrained mode-volume bounds already exist, including multiple resonances; their point-energy objective does not itself bound a gate channel. |
| Miller and Monticone, [arXiv:2605.24738](https://arxiv.org/abs/2605.24738), sections 2.6 and 5.6 | full text | Current tutorial explicitly leaves general bandwidth-dependent nonlinear material bounds open and reviews regularized mode-volume limits. This supports the narrower material subquestion, not the original combined gate ceiling. |

The generic Handbook of Optics mention could not be uniquely identified from the card's information; it remains an **unverified lead**, not an active citation. No paper was invented to fill it. Source metadata and literature-number evidence are indexed by [2026-10-13-gpt-b-novelty-literature](../runs/2026-10-13-gpt-b-novelty-literature/).

Searches: `"Single-photon Kerr nonlinearities do not help quantum computation" pdf Shapiro`; `"Heisenberg-scaling measurement" "Kerr" mixed states 2017`; `"temporal trapping" "quantum" Yanagimoto arxiv`; `"Fundamental limits" "Kuzyk" "25" "1183"`; `"maximum" "single photon" "Kerr" "bound" transparent`; `"fundamental limits" "Kerr" "bulk" susceptibility`; exact-title/identifier searches and source-reference tracing. No combined resource-qualified theorem was found in this search.

## Sharpest statement of the gap

For a fixed transparent bulk material response and a specified finite geometry/feature-size and dwell-time budget, determine a tight phase–fidelity–bandwidth tradeoff for one explicitly passive Kerr-gate architecture, or exhibit a counterexample to a proposed bound. Separately ask whether a rigorous microscopic material bound can reduce its parameters to density, gap and other stated resources. The published molecular, linear-response and architecture-specific results do not establish the original unrestricted ceiling. The missing resource specification must be resolved before treating absence of that ceiling as a verified open theorem problem.

## Conjectures

No claim registered. The original universal fine-structure-constant scaling and the inverse-bandwidth dwell-time assumption are superseded and retained below for history. This review provides neither an exponent nor a universal small-phase claim. A valid refutation must lie inside the agreed passive material and architecture class; an emitter-assisted or dynamically controlled gate does not do so merely because it is an optical gate.

## Oracle

Choose the architecture and microscopic response first, then compare a causal few-photon scattering/channel calculation against its classical overlap reduction. Record whether fidelity includes deterministic pulse reshaping or postselection. No few-photon or Maxwell simulation was performed. The repository's mean-field fiber solver is not an oracle for this gate question.

## Lab test

After defining an operational target, measure the phase, unconditional channel fidelity, leakage and bandwidth at fixed geometry and interaction resources. Probe-phase metrology alone does not validate the gate bound.

## Scores and remaining work

Novelty **3/5**: a resource-qualified combination has clear precedents in each constituent field, but no matching combined result was located. Impact **4/5**: a tight operational limit could guide a broad class of photonic-gate designs; that value is conditional on a useful architecture/resource specification. Scores are reviewer judgments. Seek a Claude review of the revised scope and the corrected molecular derivations; keep priority unchanged.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive (claude; claude-opus-5-5) | Proposed as candidate on the PI's request; literature unaudited | PI request in chat, 2026-10-12; bounded search listed above |
| 2026-10-13 | gpt-b (gpt; gpt-6-astra) | candidate → candidate; literature unaudited → partial; scope/citations corrected, gpt audit recorded; priority unchanged | Material/gate distinction and missing resource constraints; corrected source audit. No Claude concurrence on reformulated scope. [Review](../docs/review-2026-10-13-gpt-b-frequency-conversion-novelty.md) |

## Superseded proposer draft (preserved)

The following text is retained to keep failures and earlier hypotheses. Its source-access labels describe the proposer, not this reviewer. Its unregistered scratch numbers and superseded assertions are **not current evidence**. The active statements and source table above control this card.

<details>
<summary>Original draft before the GPT novelty audit</summary>

## Target quantity

**The PI's question (2026-10-12).** What is the maximum single-photon nonlinear phase allowable in a non-dissipative Kerr medium?

**Definition.**
- Let $\phi_1$ be the nonlinear phase per photon. That is either the cross-phase a single control photon imparts on a weak probe, or the conditional phase $\phi_{11}-\phi_{10}-\phi_{01}+\phi_{00}$ of a two-photon gate, reached with fidelity at least $F$ to the ideal phase gate.
- **Non-dissipative** means the structure is passive and lossless at the operating frequencies. Linear absorption vanishes, and the third-order response has no imaginary part (no two-photon absorption) in the relevant window.

**The answer has three ingredients**, plus their combination.

1. **Material: how large can the Kerr response be while the medium stays transparent?**
   - Causality (Kramers–Kronig) and oscillator-strength sum rules bound the linear index of a transparent medium in terms of electron density and bandwidth (Shim, Monticone & Miller 2021).
   - Truncated sum rules bound molecular hyperpolarizabilities in terms of electron number and the first excitation energy (Kuzyk 2000 and later).
   - A bulk bound of the form $n_2\le n_{2,\max}(\rho_e,\hbar\omega/E_{\rm gap},\ldots)$, with the gap constrained by transparency at $\omega$ and $2\omega$, appears not to be stated. Find it, or derive it.
2. **Field concentration per photon: how strongly can a lossless dielectric structure concentrate a single photon's field over a bandwidth $\Delta\omega$?**
   - Bandwidth-averaged bounds on near-field response and local density of states exist in terms of $\chi$ (Shim et al. 2019).
   - The single-photon nonlinear phase scales as the time-integrated $|E_1|^4$ weighted by $\chi^{(3)}$, so a bound on $\int|E_1|^4$ per photon is needed. Proposed form: something like $\hbar\omega\times$ (concentration) $\times$ (interaction time $\sim1/\Delta\omega$), limited by dispersion and causality.
3. **Quantum dynamics: how much of the classical per-photon phase survives as a high-fidelity phase on Fock states?**
   - For a local, fast-response travelling-wave Kerr medium with co-propagating photons, causality and unitarity forbid large conditional phases at high fidelity (Shapiro 2006; Shapiro & Razavi 2007; Gea-Banacloche 2010).
   - Counter-propagation through many sites (Brod & Combes 2016), dynamically coupled cavities (Heuck, Jacobs & Englund 2020) and time-reversal-symmetric transport (Tian & Chen 2023) circumvent this for emitter- or Kerr-mediated gates.
   - What fraction of the classical bound each architecture can realize at fidelity $F$ is open.
4. **Combined: a closed-form ceiling** $\phi_1\le\Phi_1^{\max}$, in groups such as:
   - $\hbar\omega/E_{\rm gap}$ (transparency margin);
   - $\rho_e\lambda^3$ (electrons per cubic wavelength);
   - $\Delta\omega/\omega$ (fractional bandwidth);
   - the fine-structure constant;
   - $F$.

   It should come with the ratio between the best published designs and the ceiling.

**Answer form.** A bound $\Phi_1^{\max}(\hbar\omega/E_{\rm gap},\rho_e\lambda^3,\Delta\omega/\omega;F)$ that is rigorous within the stated macroscopic model, and an asymptotic statement of how it scales. For example: is $\Phi_1^{\max}\ll\pi$ for every transparent dielectric at optical frequencies and a bandwidth wide enough for a useful clock rate? That would show a $\pi$ phase per photon is impossible without dissipation or resonant (emitter) media.

## Signal of hidden simplicity

- **Each ingredient already has a sum-rule or causality bound** for the linear problem: transparent-medium index, bandwidth-averaged local density of states, molecular hyperpolarizability. The single-photon phase is a product of a material response, a field-concentration factor and an interaction time. A product of bounded factors under a shared bandwidth constraint is what tends to give a clean closed form.
- **The travelling-wave no-go results are causality and unitarity arguments**, not numerical findings (Shapiro 2006; Gea-Banacloche 2010). They should combine with the material bounds into a single statement in which bandwidth enters both.
- **Known per-photon phases are tiny and span many orders of magnitude** across platforms: fibre, silicon nitride microrings, photonic-crystal nanocavities. A ceiling would show whether that is engineering or principle.

## Literature state

Bounded search by the orchestrator, 2026-10-12. Unaudited.

**Travelling-wave and gate no-go results:**
- Shapiro, "Single-photon Kerr nonlinearities do not help quantum computation", PRA 73, 062305 (2006). Argues that non-instantaneous, fast-response Kerr media give essentially no high-fidelity conditional phase for single-photon wavepackets. **Abstract only**, via a search summary.
- Shapiro & Razavi, "Continuous-time cross-phase modulation and quantum computation", New J. Phys. 9, 16 (2007), [arXiv:quant-ph/0612086](https://arxiv.org/abs/quant-ph/0612086). **Not accessed** beyond the listing.
- Gea-Banacloche, "Impossibility of large phase shifts via the 'giant Kerr effect' with single-photon wavepackets", PRA 81, 043823 (2010), [arXiv:0911.4682](https://arxiv.org/abs/0911.4682). Spontaneous emission into unoccupied temporal modes limits cross-phase; absorption grows as the pulse bandwidth approaches the medium's transparency bandwidth. **Abstract only.**
- Viswanathan & Gea-Banacloche, "Analytical results for a conditional phase shift between single-photon pulses in a nonlocal nonlinear medium", [arXiv:1712.03914](https://arxiv.org/abs/1712.03914). **Not accessed** beyond the listing.

**Circumventions:**
- Brod & Combes, "Passive CPHASE gate via cross-Kerr nonlinearities", PRL 117, 080502 (2016), [arXiv:1604.04278](https://arxiv.org/abs/1604.04278), [DOI 10.1103/PhysRevLett.117.080502](https://doi.org/10.1103/PhysRevLett.117.080502). Counter-propagating photons through discrete atom-mediated cross-Kerr sites; fidelity above 0.99 with 12 sites. **Abstract only.**
- Heuck, Jacobs & Englund, "Controlled-phase gate using dynamically coupled cavities and optical nonlinearities", PRL 124, 160501 (2020). **Not accessed**; cited from memory, so verify before relying on it.
- Tian & Chen, "Passive and deterministic controlled-phase gate for single-photon wavepackets based on time-reversal symmetric photon transport", [arXiv:2312.10719](https://arxiv.org/abs/2312.10719) (2023). Fidelity above 99% with four cavities and an emitter. **Abstract only.**

**Material and field-concentration limits:**
- Shim, Monticone & Miller, "Fundamental limits to the refractive index of transparent optical materials", [arXiv:2103.15697](https://arxiv.org/abs/2103.15697) (2021). Index bounds from Kramers–Kronig relations and sum rules, scaling as the cube root of electron density. The abstract mentions no nonlinear extension. **Abstract only.**
- Kuzyk and co-workers, truncated sum rules and fundamental limits of hyperpolarizabilities: [arXiv:physics/0510002](https://arxiv.org/abs/physics/0510002) and [arXiv:physics/0510199](https://arxiv.org/abs/physics/0510199); the original is Kuzyk, PRL 85, 1218 (2000), not located in this search. **Listings only: not accessed.**
- Sheik-Bahae et al., band-gap scaling and dispersion of the bound-electronic Kerr effect obtained from two-photon absorption by a Kramers–Kronig transform (CREOL publications; Sheik-Bahae, Handbook of Optics chapter). A scaling model, not a bound. **Not accessed.**
- Shim et al., bandwidth-averaged limits to near-field optical response (Miller group, 2019; PDF at millergroup.yale.edu). **Not accessed.**

**Measurements and nanocavity designs:**
- A Heisenberg-scaling measurement of the single-photon Kerr nonlinearity, Nat. Commun. (2017), [s41467-017-02487-z](https://www.nature.com/articles/s41467-017-02487-z). **Not accessed.**
- Choi, Heuck & Englund, a self-similar nanocavity with ultrasmall mode volume for single-photon nonlinearities, PRL 118, 223605 (2017). **Not accessed**; cited from memory, so verify.

**Searched:** "Single-photon Kerr nonlinearities do not help quantum computation"; "impossibility of large phase shifts giant Kerr"; "passive CPHASE cross-Kerr counterpropagating"; "fundamental limit maximum single-photon Kerr nonlinear phase transparent medium bound n2 two-photon absorption sum rule"; "upper bound Kerr coefficient n2 transparent material bandgap sum rule causality fundamental limit". None of these found a combined bound on $\phi_1$ in a transparent Kerr medium.

## Sharpest statement of the gap

**Known:**
- the dynamical no-go results for local, fast travelling-wave Kerr media with co-propagating single photons;
- architectures that circumvent them;
- sum-rule limits on linear index and molecular hyperpolarizability;
- bandwidth-averaged bounds on near-field response;
- empirical band-gap scaling of $n_2$.

**Not found:**
- A sum-rule bound on bulk $n_2$ (or $\chi^{(3)}$) under the constraint of transparency at $\omega$ and $2\omega$, stated in electron density and transparency margin.
- A bound on the time-integrated fourth power of a single photon's field over bandwidth $\Delta\omega$ in any lossless dielectric structure.
- The combination of these with the dynamical constraint into one ceiling on $\phi_1$ at fidelity $F$.
- A statement of how far fibre, microring, nanocavity and temporal-trapping proposals sit below that ceiling.

The individual pieces may be known in neighbouring communities: molecular nonlinear optics, photonic-design bounds, quantum-gate theory. The audit has to check each.

**Companion card.** P-20261012-claude-interactive.5-05 asks the χ(2) analogue of ingredient 2: a structural upper bound on the nonlinear overlap of doubly resonant cavities over all geometries. The concentration bound needed here may share its methods.

## Conjectures

None registered.

**A refutable first conjecture.** For any transparent dielectric with $E_{\rm gap}>2\hbar\omega$, any lossless structure, and any photon bandwidth with $\Delta\omega/\omega\ge10^{-6}$, the per-photon cross-phase satisfies $\phi_1\le C\,\alpha\,(\hbar\omega/E_{\rm gap})^{p}(\omega/\Delta\omega)^{q}$, where:
- $C$, $p$ and $q$ are fixed by the sum rules and the concentration bound;
- $q\le1$.

It is refuted by any lossless design, with a material obeying the sum rules, that exceeds it.

## Oracle

**Missing** in the repository's solver, which propagates classical mean fields with linearized noise in fibre and does not do few-photon scattering or electromagnetic design.

Checks that can be built cheaply:
- **Material data.** Tabulated $n_2$, band gap and electron density for fused silica, silicon nitride, silicon below half-gap, AlGaAs, GaP, chalcogenides and TiO₂, compared with the material bound.
- **Classical per-photon phase** of published nanocavity and waveguide designs, from their $Q$, mode volume and $n_2$, compared with the combined ceiling.
- **Few-photon dynamics.** A short code for two-photon scattering on discretized Kerr sites, co- and counter-propagating (Brod–Combes-type), and with dynamically coupled cavities, to test how much of the classical phase survives at fidelity $F$.

## Lab test

Compare measured single-photon cross-phase shifts with the ceiling for the same material and bandwidth. A measurement above the ceiling with negligible absorption, in a material obeying the sum rules, refutes it. For the ceiling to be useful, the best measured values (fibre, microresonators, nanocavities) should lie a stated, explainable distance below it.

## Risks and must-reads

- **The combined bound may be loose by many orders of magnitude**, which would make it unhelpful. Its value then lies in the material and concentration pieces separately.
- **Molecular sum-rule limits may already give the bulk bound** after density scaling and local-field corrections. Novelty would then lie in the combination and the transparency constraint.
- **The dynamical constraint is architecture-dependent.** The ceiling has to be stated per architecture class, or as the largest over all of them.
- **Resonant (emitter, Rydberg, exciton-polariton) media are excluded by "non-dissipative".** The card must define the boundary: a near-resonant medium with small but nonzero absorption is outside the model.
- **Must-reads:**
  - Shapiro 2006 and Shapiro & Razavi 2007, full text;
  - Gea-Banacloche 2010;
  - Brod & Combes 2016;
  - Heuck, Jacobs & Englund 2020;
  - Kuzyk 2000 and the truncated-sum-rule papers;
  - Shim, Monticone & Miller 2021;
  - the Miller-group near-field bandwidth bounds;
  - Sheik-Bahae et al. 1990–1991;
  - Chang, Vuletić & Lukin's review of quantum nonlinear optics (Nat. Photon. 2014);
  - reviews of single-photon nonlinear optics in nanocavities, and the Mabuchi group's work on temporal trapping and pulsed few-photon nonlinear optics.

</details>
