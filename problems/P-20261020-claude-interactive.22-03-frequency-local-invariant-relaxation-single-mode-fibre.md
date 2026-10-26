---
id: P-20261020-claude-interactive.22-03
title: "Beyond anomalous thermalization: what relaxes the frequency-local invariant of incoherent light near zero dispersion in single-mode fibre, and how slowly"
status: candidate
priority: 3
literature_state: open
novelty_confidence: low
target_quantity: "A uniformly defined change or projected relaxation of the four-wave kinetic invariant J(w)=n(w)-n(2w_z-w) near the cubic-dispersion pair-exchange plane, separating resonant quartic dynamics, higher-order collisions, beta4 effects and Raman drift. The first generic six-wave vertex calculation is pre-empted; a physical conservative observation window remains to be established."
model: "Scalar 1D GNLSE for one axis of a PM fibre: dispersion beta2, beta3 (optionally beta4), instantaneous Kerr gamma |psi|^2 psi; optional self-steepening and delayed Raman response; statistically stationary random-phase incoherent light with spectral width dw comparable to the distance of its centre from w_z."
oracle_ready: available
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

**Current text added by gpt-h (gpt; gpt-6-astra), 2026-10-20.** Novelty lowered medium → low; status remains candidate; original first six-wave coefficient target marked pre-empted. The original scout text is retained below as superseded; the current assessment and source-access ledger are in the [cross-family review](../docs/review-2026-10-20-gpt-h-cross-family-novelty-claude-22-cards.md).

## Target quantity

For scalar Kerr propagation with quadratic-plus-cubic dispersion, four-wave kinetics preserves $J(\Omega)=n(\Omega)-n(2\Omega_z-\Omega)$, where $\Omega_z=-\beta_2/\beta_3$. The residual target is a uniformly defined slow change of this quantity near the nontrivial pair-exchange plane, separating higher-order collisions from $\beta_4$-modified four-wave processes and Raman drift.

Define relaxation relative to an initial/equilibrium profile or a projection off exact invariants. **Superseded:** the assertion that RJ equilibrium necessarily erases $J$. Conserved momentum constrains an odd moment, and generic equilibrium need not be reflection symmetric about $\Omega_z$. Pure cubic dispersion also requires a stated physical bandwidth/regularization before specifying an equilibrium.

## Longstanding evidence

Suret 2010 (DOI:10.1103/PhysRevLett.104.054101) concerns a vector experiment/model; Michel 2011 (DOI:10.1007/s11005-010-0452-y) explicitly develops the scalar TOD kinetic invariant. Relevant primary full text read by gpt-h.

Picozzi 2014 §6.2.3 (DOI:10.1016/j.physrep.2014.03.002) contains the quoted open-problem phrase, but it concerns **experimental observation** in the vector/Raman discussion. Onorato 2023 (arXiv:2305.18215) concerns kinetic limits in chains; Vassilev 2025 (DOI:10.1007/s00220-025-05455-7) treats a different dispersion class with a trivial leading kernel. Their primary wording was checked, but none is a direct declaration of this precise scalar post-plateau length law as longstanding and open.

## Literature state

Open in the narrower residual kinetic sense, but **novelty confidence low**, lowered from medium. The proposed first result is substantially pre-empted and the new optical observation window is unestablished. This card does not qualify for the PI's high-novelty shortlist on the evidence available.

## Kill search

**Decisive correction added by gpt-h:** Sutherland–Yim, [arXiv:2609.23175v1](https://arxiv.org/abs/2609.23175v1), §§6–7 read in full relevant text, gives a general six-wave kernel for quadratic-plus-cubic dispersion, a cancellation theorem, and the constant-vertex denominator identity Eq. (7.4). The pure Kerr specialization is direct. On fixed compact quadratic-resonance patches with nonzero internal denominators, its local-vertex contribution starts generically at second order in small cubic dispersion.

The old coefficient identification is **superseded**: $B$ denotes local cubic nonlinearity, not cubic dispersion; $D$ denotes nonlocal mean flow. Recomputing the generic coefficient/first-order cancellation in fibre notation is not a new result. The paper does not supply the near-zero-dispersion kinetic relaxation length.

Onorato 2015 (arXiv:1402.1603) and Lvov–Onorato 2018 (arXiv:1802.07686), relevant full text read, already predict/test six-wave-controlled FPUT relaxation. Barviau 2013 (DOI:10.1103/PhysRevA.87.035803, full text) changes four-wave geometry through $\beta_4$. Hirota and Sasa–Satsuma manifolds need their specific derivative nonlinearities; generic optical self-steepening is not interchangeable with either (Sutherland–Yim; DOI:10.1063/1.5030604, hierarchy equations read).

## Sharpest statement of the gap

Can resonant quartic evolution and irreducible higher-order collisions be combined uniformly near the pair-exchange plane, with a controlled projected $J$ rate and a viable optical regime? The generic nonresonant-normal-form coefficient is known; the limiting kinetic construction and experimental relevance are not established here.

## Analytical foothold and first derivation target

The former first coefficient target is **pre-empted**, not an unchecked novel hypothesis. At fixed $\beta_2$, $\Omega_z$ moves as $1/\beta_3$, so a fixed-band small-$\beta_3$ expansion is nonuniform in the proposed regime. Generic kernel formulas exclude vanishing internal denominators. Specify a mixed four-/six-wave limit that keeps resonant quartic channels and avoids double-counting successive four-wave events before attempting a closure.

A scope/feasibility task should first define the projection, boundary/dispersion model, limiting parameters, and how a conservative change of $J$ could exceed Raman and numerical drift. Do not proceed on a naive collision-order estimate alone.

## Dimensionless groups and regime

Retain weak-nonlinearity ratio $\varepsilon$, position relative to zero dispersion $\nu$, $\beta_4\Delta\omega/\beta_3$, self-steepening and Raman strength. The regime must specify the distance to Hirota/Sasa–Satsuma conditions in the full coefficient space, not just a nonzero third derivative. Require an independently justified window $L_4\ll L_J\ll L_R$ and small loss over $L_J$.

The earlier scale estimates in run 2026-10-20-claude-interactive.22-resonance-kinematics/raman_budget.json already place the nominal six-wave length far beyond the silica Raman budget. They are dimensional estimates without prefactors; they do not validate a measured law.

## Oracle

GNLSE ingredients are available, but the tiny long-time drift needs convergence in step, window, spectral cutoff, reflection-plane placement and nonlinear aliasing. Track exact momentum as well as $J$. Use integrable controls and isolate $\beta_4$/Raman contributions. A linear null test alone does not validate nonlinear invariant drift. No new propagation verification was made.

## Lab test

The suggested PM-fibre four-wave test concerns the old anomalous-thermalization mechanism. It does not establish access to the new conservative relaxation stage. A Raman-free guide needs calibrated dispersion/nonlinearity/loss; an amplified recirculating loop changes the model.

The 2014 experimental open statement cannot establish that no observation exists in 2026. The documented search found no controlled optical measurement of this precise conservative post-plateau law, not proof of an absence of every later anomalous-thermalization experiment.

## Superseded scout text

<details>
<summary>Original 2026-10-20 scout formulation, superseded by the review above</summary>

This block preserves the initial hypotheses, evidence interpretations and access history. It is not the current card assessment. The changed metadata was:

- Former novelty_confidence: medium
- Former last_audited: null
- Former target_quantity: "The relaxation length L_J of the frequency-local invariant J(w) = n(w) - n(2w_z - w), which four-wave kinetics conserves for incoherent light around the zero-dispersion frequency w_z of a polarization-maintaining single-mode fibre. That is, the length on which the anomalous (non-Rayleigh–Jeans) state decays, as a law L_J ~ L_NL eps^-p in the weak-turbulence parameter eps and the integrability-breaking parameters, together with the Raman-driven drift of J that competes with it."

### Superseded: Target quantity

**The degeneracy.** With $k(\Omega)=\beta_2\Omega^2/2+\beta_3\Omega^3/6$, the four-wave mismatch on the frequency shell factorizes (run `2026-10-20-claude-interactive.22-resonance-kinematics`, `summary.json`):

$$\Delta k=-\tfrac12(\Omega_1-\Omega_3)(\Omega_2-\Omega_3)\,[2\beta_2+\beta_3(\Omega_1+\Omega_2)].$$

So every non-trivial resonance has $\Omega_1+\Omega_2=\Omega_3+\Omega_4=2\Omega_z$, with $\Omega_z=-\beta_2/\beta_3$. The four-wave kinetic equation therefore conserves $J(\Omega)=n(\Omega)-n(2\Omega_z-\Omega)$ at every $\Omega$: an infinite family of local invariants, and the cause of the anomalous, non-RJ end state (Suret et al. 2010; Picozzi et al. 2014, §6.2).

**Wanted.**
1. **The relaxation length.** $L_J$ on which $J$ decays through processes beyond four-wave kinetic order, as a scaling law $L_J\simeq C\,L_{\rm NL}\,\varepsilon^{-p}$ with $\varepsilon=L_{\rm lin}/L_{\rm NL}$.
   - The exponent $p$ and the coefficient $C$ must be computed, together with their dependence on the integrability-breaking terms: $\beta_4$, self-steepening, and the distance from the integrable Hirota equation.
2. **The competing Raman drift.** The length $L_R$ on which the delayed Raman response changes $J$ at first order.
3. **The condition for the conservative stage to exist,** $L_4\ll L_J\ll L_R$.
4. **The end state.** It must be defined: with pure $\beta_3$ the dispersion is unbounded below and RJ is not normalizable, so the target is a truncated RJ state (Barviau et al. 2013) or a stated band.

### Superseded: Longstanding evidence

- **Defined.** Suret, Randoux, Jauslin & Picozzi, PRL 104, 054101 (2010), [DOI:10.1103/PhysRevLett.104.054101](https://doi.org/10.1103/PhysRevLett.104.054101). Relaxation to a state of a different nature than RJ, caused by a local invariant. Abstract only (helper claude-interactive.22.3). Kinetic theory in Michel, Garnier, Suret, Randoux & Picozzi, Lett. Math. Phys. 96, 415 (2011), [DOI:10.1007/s11005-010-0452-y](https://doi.org/10.1007/s11005-010-0452-y); not accessed.
- **Open as an experiment.** Picozzi et al., Phys. Rep. 542, 1 (2014), [DOI:10.1016/j.physrep.2014.03.002](https://doi.org/10.1016/j.physrep.2014.03.002), §6.2.3: "anomalous thermalization still constitutes an open challenging problem". Full text read by claude-interactive.22 (author-hosted PDF).
  - The same section says stimulated Raman scattering kept the vector-fibre experiment from reaching the predicted local equilibrium (paraphrase, helper .22.3).
  - §6.2 presents the anomalous state as the end state at four-wave order. It does not discuss what relaxes $J$ afterwards, so the theoretical question is implicit there.
- **Open as theory.**
  - Onorato, Lvov, Dematteis & Chibbaro, Phys. Rep. 1040 (2023), [arXiv:2305.18215](https://arxiv.org/abs/2305.18215). For 1D chains, the six-wave kinetic equation "now is basically written as a conjecture". Full text, conclusions (helper .22.3).
  - Vassilev, Commun. Math. Phys. 406, 293 (2025), [DOI:10.1007/s00220-025-05455-7](https://doi.org/10.1007/s00220-025-05455-7). For 1D NLS-type dynamics with a trivial four-wave kernel, the right kinetic theory is an open question ("begging the question of what is the appropriate kinetic theory in that setting"). Abstract and introduction (helper .22.3).

**Claimed resolutions and why they do not close the problem.**

| Work | What it gives | Gap |
|---|---|---|
| Suret 2010; Michel 2011; Picozzi 2014 §6.2 | The four-wave end state with fixed $J$ | Not its decay |
| Barviau et al., PRA 87, 035803 (2013), [DOI:10.1103/PhysRevA.87.035803](https://doi.org/10.1103/PhysRevA.87.035803) (full text, helper .22.3) | With $\beta_4$, four-wave resonances fill a finite band: truncated thermalization | Outside the band, and for $\beta_3$-dominated spectra, the question remains |
| Bastianello et al., PRA 113, 013514 (2026), [arXiv:2503.16526](https://arxiv.org/abs/2503.16526) | A GGE observed in defocusing single-mode fibre; integrability-breaking corrections negligible | No breaking rate |
| Torres et al., PRL 136, 173801 (2026), [arXiv:2512.17777](https://arxiv.org/abs/2512.17777) | Two polarizations thermalize through vector four-wave processes | The scalar problem needs a PM fibre on one axis |
| Banks, Buckmaster, Korotkevich, Kovačič & Shatah, PRL 129, 034101 (2022), [arXiv:2109.02477](https://arxiv.org/abs/2109.02477) (abstract) | Six-wave kinetic equation verified for the quintic NLS | Different model |
| Sutherland & Yim, [arXiv:2609.23175](https://arxiv.org/abs/2609.23175) (Sept. 2026; abstract, helper .22.3) | Effective six-wave coefficient of Hamiltonian Dysthe equations with a small cubic-dispersion correction, $W_6\propto\varepsilon BD$ (cubic dispersion × mean-flow coefficient); vanishing sets classified | Water waves; no kinetic equation; no thermalization length; no fibre model. **Closest pre-emption.** |
| Durnin, Bhaseen & Doyon, PRL 127, 130601 (2021); Panfil, Gopalakrishnan & Konik, PRL 130, 030401 (2023) (abstracts) | Collision integrals for weakly broken integrability | Quantum gases; not applied to classical fibre NLS |

### Superseded: Kill search

**Helper claude-interactive.22.3, 2026-10-20** (review §5, queries Q-D2-1 to Q-D2-14).
- **Forward citations from 2021**, OpenAlex:
  - Suret 2010: 11 citing works;
  - Michel LMP 2011: 0;
  - Michel OL 2010: 2;
  - Barviau 2013: 6;
  - Suret, Picozzi & Randoux OE 2011: 13;
  - Laurie et al. Phys. Rep. 2012: 37;
  - Lvov & Onorato 2018: 41;
  - Onorato PNAS 2015: 80, filtered;
  - Picozzi 2014: 109, filtered;
  - plus three integrable-turbulence sets.
- **Outcome.**
  - No paper derives a kinetic or GHD-collision law with an exponent for the thermalization length of scalar single-mode-fibre NLS with weak integrability breaking.
  - No paper revisits the scalar $\beta_3$ problem after 2014.
  - No fibre measurement of such an exponent was found.

**Second pass, claude-interactive.22, 2026-10-20.**
- **Forward citations from 2024**, OpenAlex:
  - Vassilev 2025: 1 citing work;
  - Suret 2010: 8;
  - Barviau 2013: 4;
  - Picozzi 2014: 53;
  - Onorato et al. Phys. Rep. 2023: 26;
  - Banks et al. 2022: 8.

  That is 88 unique titles, scanned by keyword.
- **Relevant hits are mathematics or chains:** the kinetic equation of the FPUT chain (J. Éq. Dériv. Partielles, 2026) and an inhomogeneous six-wave kinetic equation (SIAM, 2026).
- **Outcome.** No fibre six-wave or $J$-relaxation result.

### Superseded: Signal of hidden simplicity

- The degeneracy is exact and low-dimensional: one factor, $2\beta_2+\beta_3(\Omega_1+\Omega_2)$.
- The four-wave dynamics is therefore a pair-exchange process about $\Omega_z$, with a closed-form stationary family: $1/n(\Omega)+1/n(2\Omega_z-\Omega)={\rm const}$ at fixed $J$.
- With $\beta_4$, the extra factor $12\beta_2+\beta_4(2\Omega_1^2+3\Omega_1\Omega_2-\Omega_1\Omega_3+2\Omega_2^2-\Omega_2\Omega_3+\Omega_3^2)$ (run `summary.json`) opens a two-dimensional resonant manifold. That gives a second, separately tunable relaxation channel.

### Superseded: Literature state

See the tables above. Also:
- Laurie, Bortolozzo, Nazarenko & Residori, Phys. Rep. 514, 121 (2012), [DOI:10.1016/j.physrep.2012.01.004](https://doi.org/10.1016/j.physrep.2012.01.004): six-wave optical wave turbulence in 1D for a nonlocal (liquid-crystal) model. Not accessed in this session.
- Onorato, Vozella, Proment & Lvov, PNAS 112, 4208 (2015), [DOI:10.1073/pnas.1404397112](https://doi.org/10.1073/pnas.1404397112): the FPUT analogue, with a six-wave time scale $\propto\varepsilon^{-8}$ in that model's parameter. Not accessed in this session.

### Superseded: Sharpest statement of the gap

The four-wave stage is understood: anomalous thermalization at fixed $J(\Omega)$. Two things are not:
1. which process relaxes $J$, at what order, and with what exponent $p$;
2. whether that conservative relaxation can ever beat the first-order Raman drift of $J$ in a silica fibre.

The first observation of the four-wave stage itself is still missing (Picozzi 2014).

### Superseded: Analytical foothold and first derivation target

**First target: the leading non-vanishing order of the effective six-wave vertex on the six-wave resonant manifold,** for $\beta_2+\beta_3$ NLS.
- **Method.** A canonical transformation that removes the non-resonant four-wave terms but keeps the resonant pair-exchange terms about $\Omega_z$.
- **The subtlety (my hypothesis, unchecked).** NLS with $\beta_3$ differs from the integrable Hirota equation only by derivative cubic terms of order $\beta_3\gamma$. So $W_6$ may vanish at first order in $\beta_3$, as in the Dysthe classification of Sutherland & Yim, where $W_6\propto BD$. The exponent $p$ then depends on which perturbations are present: $\beta_3$ alone, $\beta_3$ with self-steepening, or $\beta_4$. Settling this is the first result.

**A framework for the first target.** Vanovac, McCarthy, Surace & Motrunich, [arXiv:2603.11712](https://arxiv.org/abs/2603.11712) (March 2026; abstract read by claude-interactive.22).
- They build weak-integrability-breaking (WIB) perturbations of classical integrable lattice models, which keep a tower of quasi-conserved quantities. For example, α-FPUT is a WIB of the harmonic chain, through the Toda integrals.
- Such perturbations are expected to delay thermalization beyond Fermi's-golden-rule time scales.
- The fibre analogue is a hypothesis: whether $\beta_3$-NLS is a WIB of NLS through the Hirota hierarchy. If it is, the exponent $p$ is larger than naive six-wave counting gives.
- Not a kill: the paper treats lattice models (Toda, Ishimori, harmonic chain), not NLS or fibre.

**Second target: the six-wave kinetic equation projected onto the odd part of $n$ about $\Omega_z$.** It gives $dJ/dz$, and hence $L_J$ and $p$.

**Third target: the first-order Raman contribution to $dJ/dz$** from the Raman gain at detunings below 1 THz. This gives $L_R$ and the window $L_4\ll L_J\ll L_R$.

### Superseded: Dimensionless groups and regime

| Group | Meaning | Card's range |
|---|---|---|
| $\varepsilon=L_{\rm lin}/L_{\rm NL}$, $L_{\rm lin}=1/(\lvert\beta_3\rvert\Delta\omega^3)$ | weak turbulence | 0.01–0.3 |
| $\nu=(\omega_c-\omega_z)/\Delta\omega$ | spectral centre relative to zero dispersion | $-2$ to 2 |
| $b=\beta_4\Delta\omega/\beta_3$; $s=\Delta\omega/\omega_0$ | $\beta_4$; self-steepening | $\ll1$ |
| $R=L_4/L_R$ | Raman drift against four-wave rate | to be computed; must be $\ll1$ |
| $\Lambda=\gamma PL$ | Kerr phase | $\lesssim25$ rad in silica before stimulated Raman threshold (run `raman_budget.json`) |
| cross-axis coupling | PM extinction | negligible |

**Scale estimates without prefactors** (run `raman_budget.json`). A PM dispersion-shifted fibre with $\gamma=2$ W⁻¹km⁻¹, $\beta_3=0.1$ ps³/km and 1 W of 1 THz-wide light has $\varepsilon\approx0.08$:
- $L_4\sim L_{\rm NL}/\varepsilon\approx6$ km, about 12 rad, so within the Raman budget.
- A six-wave length $\sim L_{\rm NL}/\varepsilon^3$ would be $\sim10^3$ km, far beyond it.
- **Consequence.** In silica the lab can see the four-wave stage and the Raman drift. The six-wave relaxation is a numerical target, or one for Raman-free media such as noble-gas-filled hollow-core fibre.

### Superseded: Conjectures

None filed.

### Superseded: Oracle

- **Available.** The solver integrates the single-mode GNLSE with arbitrary dispersion, Kerr, self-steepening and Raman (switchable). Ensembles of random-phase incoherent fields are set by initial conditions.
- **Cheap test.**
  - 100–200 realizations of a stationary random-phase field centred near $\Omega_z$, with an asymmetric spectrum, so $J\ne0$.
  - Raman off.
  - Measure $J(\Omega,z)$ against $z$ for $\varepsilon$ = 0.05–0.3. Check that $J$ stays constant on the four-wave scale, and fit the slow decay exponent $p$.
  - Repeat with self-steepening, with $\beta_4$, and with Raman on.
- **Artefacts to rule out.**
  - Time-window periodicity and spectral resolution: $J$ needs symmetric resolution about $\Omega_z$.
  - Aliasing, and step size: report the $J$ drift against $\Delta z$ when $\gamma=0$.
  - Finite ensemble size.
- **Long runs.** These are 1D, so $10^3$–$10^4\,L_{\rm NL}$ is feasible on a CPU.

### Superseded: Lab test

**Platform.**
- A PM dispersion-shifted fibre launched on one axis.
- Filtered ASE of about 1 THz, spectrally shaped to be asymmetric about the zero-dispersion wavelength, so that $J\ne0$.
- Cut-back or power scan within $\Lambda\le12$.

**Prediction that distinguishes.**
- **Four-wave stage.** The spectrum reshapes while $J(\Omega)$ stays fixed. This is the first observation of anomalous thermalization, open since 2014. RJ relaxation would instead erase $J$.
- **Raman.** With Raman, $J$ drifts at the computed $L_R$, with the sign set by the Raman gain slope.
- **Six-wave stage.** Accessible only in a Raman-free guide or in a recirculating loop with Raman suppressed.

### Superseded: How a solution would be recognized

1. An analytic $p$ and $C$, with stated dependence on $\beta_3$, $\beta_4$ and self-steepening, that reproduce the simulated decay of $J$ within 20%. The fitted exponent should match the predicted one within 0.2 over at least a decade of $\varepsilon$, on parameters not used to build the theory.
2. A computed $R$ that correctly predicts whether a given fibre shows the conservative stage.
3. A defined end state: truncated RJ, or a stated band.

### Superseded: Relation to existing cards

- **P-005, P-010, P-20261020-gpt-f-01.** Multimode; no overlap.

### Superseded: Risks and must-reads

- **Pre-emption.** Sutherland & Yim (Sept. 2026) are one step from the fibre six-wave coefficient. Check for a fibre follow-up before derivation.
- **Ill-posed end state.** The pure-$\beta_3$ problem may be ill-posed; pose it with $\beta_4$ or a band.
- **Lab relevance.** Raman may dominate any conservative relaxation in silica, which would make the six-wave law of numerical interest only.
- **Novelty is medium:** the four-wave theory exists, and a cross-family critic may call the six-wave step an adaptation of FPUT wave turbulence. The Hirota-proximity question (does $W_6$ vanish at first order?) is what would lift it.
- **Must-reads:**
  - Michel et al., LMP 2011;
  - the experimental reference [140] of Picozzi 2014;
  - Laurie et al., Phys. Rep. 2012;
  - Onorato et al., PNAS 2015 and Lvov & Onorato, PRL 2018;
  - the Sutherland & Yim full text.

</details>

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-20 | claude-interactive.22 (claude; claude-opus-5-5) | Created as candidate on the PI's request for longstanding high-novelty thermalization problems; literature_state open; novelty medium (four-wave stage known; relaxation law open per Picozzi 2014, Onorato 2023 and Vassilev 2025; closest pre-emption in water waves); priority 3 pending PI decision | `docs/review-2026-10-20-claude-interactive.22-longstanding-optical-thermalization.md`; run `2026-10-20-claude-interactive.22-resonance-kinematics` |
| 2026-10-20 | gpt-h (gpt; gpt-6-astra) | Novelty lowered medium → low; status remains candidate; original first six-wave coefficient target marked pre-empted. Current scientific text replaced; superseded scout text retained. | Sutherland–Yim 2026, arXiv:2609.23175v1 §§6–7; Picozzi 2014, DOI:10.1016/j.physrep.2014.03.002 §6.2.3 (full relevant text); [review](../docs/review-2026-10-20-gpt-h-cross-family-novelty-claude-22-cards.md) |
