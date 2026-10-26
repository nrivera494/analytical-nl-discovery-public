---
id: P-20261012-claude-interactive-01
title: Conservation-law ceilings on Kerr frequency conversion into a target band
status: parked
priority: 2
literature_state: partial
novelty_confidence: medium
target_quantity: A nontrivial upper bound and attainability gap for output ENERGY in a target band in a fixed scalar
  defocusing Kerr fiber, over a stated finite propagation interval and an input class with bounded launch Hamiltonian
  or bandwidth and bounded initial target-band leakage. A physical-photon version requires a separate photon-conserving
  model.
model: 'Baseline: lossless scalar power-envelope NLSE, instantaneous positive Kerr coefficient, fixed real dispersion
  with nonnegative tangent-subtracted symbol, no Raman or self-steepening. Broadband photon conservation, multimode
  coupling and perturbations are separate extensions whose invariants must be derived.'
oracle_ready: available
last_audited: '2026-10-13'
audited_by:
- gpt
proposed_by: claude-interactive
claims: []
results: []
review_provenance:
  agent: gpt-a
  model: gpt-6-astra
  family: gpt
  verdict: open, narrowed
  concurrence: pending
  review: docs/review-2026-10-13-gpt-a-frequency-conversion-novelty.md
---

> **Merged into P-20261016-claude-interactive-01** (dispersive-wave yield ceiling and shaping headroom) by PI decision on 2026-10-16. That card carries this card's premises and its GPT audit in its "Merged cards" section. Continue the work there; this card is kept for its history and is not worked on separately.

## Target quantity

**GPT verdict: open, narrowed.** The elementary invariant bound is a known consequence of a published optical conservation law. The remaining target is a useful improvement or an attainability result under explicit launch restrictions. Keep this card **candidate**: the earlier Claude search is real, but concurrence with this revised scope has not been recorded.

For a power envelope, define $E=\int |A|^2dt$ and $\eta_B^E=E^{-1}\int_B|\widetilde A|^2d\Omega/(2\pi)$. The normalized spectral density here is an **energy** density. Physical photon number is $Q=\int|\widetilde A|^2/[\hbar(\omega_0+\Omega)]\,d\Omega/(2\pi)$ on positive absolute frequencies. These are distinct at broad bandwidth; [Zheltikov (2018); 10.1103/PhysRevA.98.043833](https://doi.org/10.1103/PhysRevA.98.043833) (**full text**) directly addresses the distinction.

Specify an admissible input class $\mathcal A$ with a launch Hamiltonian budget or a spectral-bandwidth bound, launch centroid, temporal duration, initial target-band leakage and a finite length limit $L_{\max}$. A fixed energy and RMS duration alone do not constrain the launch Hamiltonian. Peak power and hence $N$ also need a definition when pulse shapes vary.

## Premise check

For $\widehat\beta\ge0$, $\gamma>0$ and $\inf_B\widehat\beta>0$, the instantaneous scalar model gives
$$H=\int\widehat\beta|\widetilde A|^2\,d\Omega/(2\pi)+\frac{\gamma}{2}\int|A|^4dt,\qquad
\eta_B^E\le\min\!\left(1,\frac{H_0}{E\inf_B\widehat\beta}\right).$$
This is a Markov inequality applied to the published Hamiltonian, not a new conservation law. [Castelló-Lurbe, Andrés and Silvestre (2013); 10.1364/OE.21.028550](https://doi.org/10.1364/OE.21.028550) (**full text**), Eqs. 2 and 19, supplies that invariant in optical variables.

For $A(0,t)=\sqrt{P_0}\exp[-(1-iC)t^2/(2T_0^2)]$, pure normal $\beta_2$ and $N^2=\gamma P_0T_0^2/\beta_2$,
$$\frac{2T_0^2H_0}{\beta_2E}=\frac{1+C^2}{2}+\frac{N^2}{\sqrt2}.$$
Thus the original Gaussian coefficient is correct for $C=0$ and an energy fraction. Quadrature and the fixed-duration chirp counterexample are registered in run **2026-10-13-gpt-a-novelty-premises**. This is an input-constraint check, not propagation verification.

Higher invariants contain nonlinear terms. Sobolev control yields polynomial tail bounds; a Chernoff tail additionally needs suitable control of the whole hierarchy. [Koch and Tataru (2018); 10.1215/00127094-2018-0033](https://doi.org/10.1215/00127094-2018-0033) (**full text**) already proves conserved Sobolev-energy estimates. The defocusing long-time asymptotic solution, including its logarithmic phase, is also established by [Deift and Zhou (2003); 10.1002/cpa.3034](https://doi.org/10.1002/cpa.3034) (**full text**); a conversion to optical notation alone is not a discovery.

## Literature state

The source-by-source verification ledger, including every inherited DOI/arXiv citation, is in [the review](../docs/review-2026-10-13-gpt-a-frequency-conversion-novelty.md). The table below gives the closest additions and corrections. Access labels describe this GPT review, not inherited access claims.

| Source and identifier | Access | What was checked |
|---|---|---|
| Castelló-Lurbe, Andrés and Silvestre (2013), [10.1364/OE.21.028550](https://doi.org/10.1364/OE.21.028550) | full text | Equations 2 and 19 give the same dispersion-weighted Hamiltonian invariant; normal-dispersion spectral design already uses it. |
| Castelló-Lurbe, Vermeulen and Silvestre (2016), [10.1364/OE.24.026629](https://doi.org/10.1364/OE.24.026629) | full text | Generalized inverse dispersive and nonlinear lengths sum to a constant. A direct optical precedent for the proposed invariant-based analysis. |
| Zheltikov (2018), SPM theory, [10.1364/OE.26.017571](https://doi.org/10.1364/OE.26.017571) | full text | Approximate short-distance SPM/GVD broadening and high-order compression-length scaling. Section 3 Eq. 6 includes the soliton-period factor omitted from the proposal’s leading compression-length coefficient. |
| Koch and Tataru (2018), [10.1215/00127094-2018-0033](https://doi.org/10.1215/00127094-2018-0033) | full text | Conserved energies control Sobolev norms. Higher invariants are nonlinear functionals, not conserved ordinary Fourier moments. |
| Deift and Zhou (2003), [10.1002/cpa.3034](https://doi.org/10.1002/cpa.3034) | full text | Defocusing NLS long-time asymptotics in weighted Sobolev spaces are established, including a logarithmic phase. Rewriting them in optical units alone is not novel. |
| Diao, Chen and Chang (2021), [10.1364/OE.442348](https://doi.org/10.1364/OE.442348) | full text | PSO varies fiber length, mode-field diameter and dispersion for a fixed Gaussian input. The fitness combines both outer-lobe energy fractions with pulse Strehl quality; this is prior optimization, not a global one-band ceiling. |
| Wang, Chen and Chang (2022), [10.1364/OE.466033](https://doi.org/10.1364/OE.466033) | full text | Sections 3–4 estimate SPM/GVD spectral peak positions and widths for Gaussian/sech launches using a fitted lumped-chirp parameter. These are approximate spectral-width maxima, not optimized band-energy ceilings. |
| Zheltikov (2018), [10.1103/PhysRevA.98.043833](https://doi.org/10.1103/PhysRevA.98.043833) | full text | Explicitly distinguishes the NLSE norm from physical photon number and explains the role of the optical shock term. |
| Finot, Chaussard and Boscolo (2018), [arXiv:1808.04672](https://arxiv.org/abs/1808.04672) | full text | Corrects the author attribution 'Aston', which is an institution. Interference description predicts spectral patterns; no optimized band-fraction bound. |
| Heidt (2010), [10.1364/JOSAB.27.000550](https://doi.org/10.1364/JOSAB.27.000550) | abstract only | Identifiable replacement for the vague Heidt reference: coherent pulse-preserving ANDi generation, not a band-energy ceiling. |

The original “Aston” attribution is corrected to Finot, Chaussard and Boscolo. DESY record 400022 is [Chung et al. (2018); 10.1364/OE.26.003684](https://doi.org/10.1364/OE.26.003684) (**abstract only**); its experiment uses negative GVD and is not evidence for a normal-dispersion theorem. The unspecified “Heidt theses” and “NLS working-group notes” cannot identify a unique source; the identifiable replacements above carry the argument.

**Searches:** “normal dispersion spectral broadening conservation Hamiltonian”; “Dispersion-to-spectrum mapping in nonlinear fibers”; “defocusing nonlinear Schrodinger long time asymptotics reflection coefficient”; “nonlinear Schrodinger conserved energies Sobolev norms”; “NMR inverse scattering pulse design trace formula energy bandwidth bounds”; “SPM-enabled spectral selection optimization efficiency”. Exact DOI and title searches and access failures are in the review search log.

## Sharpest statement of the gap

For a fixed normal-dispersion fiber, a launch class with controlled Hamiltonian/bandwidth and negligible target-band seeding, and $0\le z\le L_{\max}$, can one derive a band-energy ceiling that materially improves the elementary moment inequality, and establish how closely propagating pulses can approach it? State the bounds on $N$, launch bandwidth times $T_0$, $\Delta T_0$, band width times $T_0$, chirp and $L_{\max}/L_D$ before testing tightness.

The unresolved part is **dynamical attainability under those restrictions**, not the Hamiltonian identity, known Sobolev tails, inverse-scattering asymptotics or numerical SESS optimization. [Diao, Chen and Chang (2021); 10.1364/OE.442348](https://doi.org/10.1364/OE.442348) (**full text**) already optimizes SESS dispersion and efficiency. A theorem for physical photon fractions, self-steepening, Raman or multiple modes requires its own positive invariant and cannot inherit this proof.

## Conjectures

No active quantitative conjecture is ready. The original fixed-factor tightness conjecture is superseded pending a definition of $\mathcal A$. An indefinite Hamiltonian in anomalous dispersion invalidates this positivity proof; it does not establish unbounded soliton fission. Frequency-selective loss also cannot be assumed to lower a normalized blue fraction.

## Oracle

The propagation and adjoint capability is available as recorded in the proposal. First define the admissible class in **T-20261013-gpt-a-04**; this audit made no solver changes. Monitor launch and output invariants, energy/photon normalization, spectral leakage, time-window wrap-around and discretization convergence. Equality of a Markov bound is a support condition on a probability measure, not a claim that physical finite pulses can saturate it.

## Assessment and next step

**Novelty 3/5:** constrained attainability could be new, with direct precedents in optical Hamiltonian methods and inverse-scattering optimization. **Impact 3/5:** a tight, experimentally parameterized ceiling would give a specialist group a usable design rule. These are rubric judgments, recorded in run **2026-10-13-gpt-a-novelty-literature**, not verified-result scores.

Reconcile the gap with Claude in **T-20261013-gpt-a-02** and resolve remaining full-text questions in **T-20261013-gpt-a-03**. Priority is unchanged.

## Superseded proposal material

The following is retained to preserve the original proposal. Its gap statements, numerical conjectures and access labels are superseded by the current review above; they are not active premises or independently verified numerical evidence.

<details>
<summary>Original proposal, retained for audit</summary>

```yaml
id: P-20261012-claude-interactive-01
title: "Conservation-law ceilings on Kerr frequency conversion into a target band"
status: candidate
priority: 2
literature_state: unaudited
novelty_confidence: low
target_quantity: "The largest fraction of a pulse's photons that a lossless Kerr fibre can deliver into a spectral band at offset Δ from the launch mean frequency, eta_max(B), bounded above in closed form by the conserved photon number, momentum and Hamiltonian (and, where the model is integrable, the higher invariants), as a function of N, T_0, the dispersion relation beta(omega) and the band; with the gap to the best achievable input shape stated."
model: "Scalar, then multimode, generalized NLSE: lossless, Kerr, arbitrary real dispersion relation beta_m(omega) per mode, with and without self-steepening and causal Raman response; classical mean field; coherent input of given energy and duration; ideal spectral (and modal) band selection at the output."
oracle_ready: available
last_audited: null
audited_by: []
proposed_by: claude-interactive
claims: []
results: []
```

### Target quantity

**The question a lab asks.** Several sources work by moving pulse energy into a chosen band with a Kerr fibre and then filtering:
- SPM-enabled spectral selection (SESS), which filters the outermost self-phase-modulation lobe for tunable femtosecond pulses;
- spectral filtering after all-normal-dispersion (ANDi) supercontinuum;
- Mamyshev-type regeneration.

How much of the pulse can any input shape, power and length put into a band $B$ at offset $\Delta$ from the launch mean frequency?

**Definition.** For a lossless fibre, let $n(\omega,z)$ be the photon spectral density, normalized so that $\int n\,d\omega=1$, and set
$$\eta_B(z)=\int_B n(\omega,z)\,d\omega,\qquad \eta_{\max}(B)=\sup_{\text{inputs},\,z}\eta_B.$$
Inputs are taken from a stated class, for example fixed energy and fixed RMS duration.

**Starting structure** (to be checked; not claimed). Without Raman or self-steepening the NLSE conserves three quantities.
- Photon number $\mathcal N=\int|A|^2dt$.
- Momentum $\mathcal P=\int\omega|\tilde A|^2d\omega$, so the mean frequency $\bar\omega$ is fixed. This is the identity behind the centroid bound of P-20261010-claude-interactive-01.
- The Hamiltonian
  $$\mathcal H=\int\hat\beta(\omega)\,|\tilde A|^2d\omega+\tfrac\gamma2\int|A|^4dt,$$
  where $\hat\beta(\omega)$ is the dispersion relation with its constant and linear parts removed, and the sign is chosen so that normal dispersion means $\hat\beta\ge0$.

**The bound in all-normal dispersion.** When $\hat\beta(\omega)\ge0$ for all $\omega$, both terms of $\mathcal H$ are non-negative, so $\int\hat\beta\,n\,d\omega\le\mathcal H_0/\mathcal N$ at every $z$. Applying Markov's inequality with weight $\hat\beta$:
$$\eta_B\le\frac{\mathcal H_0}{\mathcal N\,\min_{\omega\in B}\hat\beta(\omega)}.$$
- **Pure $\beta_2$, Gaussian input.** This becomes $\eta(|\omega-\bar\omega|\ge\Delta)\le(\tfrac12+N^2/\sqrt2)/(\Delta T_0)^2$, with $N^2=\gamma P_0T_0^2/\beta_2$.
- **Exact spectral variance.** The same invariants give the output variance exactly, $\tfrac12+N^2K(z)$ with $0\le K\le1/\sqrt2$ (C-20261010-claude-b-02, proposed).

**The question.**
1. Are these ceilings tight to within a stated factor, and over which input class?
2. Can the higher NLSE invariants sharpen them in a controlled way? The pure NLSE is integrable, so higher spectral moments are also bounded, which gives Chebyshev- or Chernoff-type tails.
3. What survives with $\beta_3$, a dispersion zero, self-steepening, Raman, and several modes?

**Answer form.** A closed-form ceiling $\eta_{\max}\le f(N,\Delta T_0,\hat\beta,\text{band})$, together with:
- its tightness ratio $\eta_{\rm achieved}/f$ over a regime given as bounds on $N$, $\Delta T_0$, $\beta_3/(\beta_2T_0)$, $f_R$ and $s=1/(\omega_0T_0)$;
- the long-distance limit for the integrable NLSE, from the Zakharov–Shabat scattering data;
- the statement of which perturbation breaks which invariant, and in which direction.

### Signal of hidden simplicity

- **Three conserved quantities already fix the spectral variance exactly** in the scalar Kerr case. In round 3 the closed form $1/(1+2N^2K)$ matched the optimal weighted readout to within 0.9 dB (C-20261010-claude-b-02, run `2026-10-10-claude-b-nd-oracle`, proposed and same-family; audited cross-family in PR #34, pass). The same invariants are what any conversion ceiling has to come from.
- **The long-distance spectrum is fixed by scattering data.** In the defocusing (normal-dispersion) integrable NLSE the solution disperses, and its spectrum becomes $z$-independent as $z\to\infty$. It is determined by the reflection coefficient of the Zakharov–Shabat problem, which is a standard inverse-scattering statement. The asymptotic band efficiency is then an explicit functional of the input, and in the semiclassical limit $N\gg1$ it is computable by WKB.
- **SESS sources report a large fraction of the energy in the outermost lobe** after a short length of fibre. A ceiling would say how close they are to the limit.

### Literature state

A bounded search by the orchestrator, 2026-10-12. Unaudited.

**Sources located:**
- **SPM-enabled spectral selection.** Self-phase-modulation spectral selection in fibre is an established tunable-source method. Sources located:
  - DESY record 400022, Opt. Express 26, 3684 (2018), [record](https://bib-pubdb1.desy.de/record/400022). Not opened beyond the search snippet: **not accessed**.
  - arXiv:2410.00889, an argon-filled hollow-core version with "efficient, broadly-tunable" megawatt output. **Abstract only, from the search result.**

  Neither, from what was seen, states a conservation-law ceiling.
- **Predicting SPM spectral patterns.** Aston, "Simple guidelines to predict self-phase modulation patterns", [arXiv:1808.04672](https://arxiv.org/abs/1808.04672), HAL hal-01856994. Gives an interference model for lobe positions, not a ceiling on lobe energy. **Abstract only.**
- **ANDi supercontinuum.**
  - Finot et al., "Beneficial impact of wave-breaking for coherent continuum formation in normally dispersive nonlinear fibers", JOSA B 25, 1938 (2008), DOI 10.1364/JOSAB.25.001938. **Abstract only**, as recorded on P-20261004-root-01.
  - Heidt and co-workers on coherence and bandwidth limits of ANDi supercontinuum (theses and papers at Stellenbosch and Southampton). **Not accessed.**
- **Inverse scattering for the defocusing NLSE** with Schwartz-class data: the scattering transform and long-time asymptotics, for example the ∂̄-method papers and the NLS working-group notes. **Not accessed for the optical spectral statement.**

**Searched:** "SPM-enabled spectral selection efficiency limit"; "upper bound spectral broadening normal dispersion Hamiltonian conservation"; "defocusing NLSE asymptotic spectrum reflection coefficient Zakharov-Shabat"; "outermost spectral lobe energy fraction analytic"; "all-normal dispersion supercontinuum maximum bandwidth analytic". These found no conservation-law ceiling on band conversion. That does not prove none exists.

### Sharpest statement of the gap

**Known:**
- The invariants themselves.
- That normal-dispersion broadening saturates at wave breaking: Finot 2008, and the round-3 semiclassical work on P-20261010-claude-interactive-01.
- Empirical SESS lobe efficiencies.
- In mathematics, the inverse-scattering long-time asymptotics of the defocusing NLSE.

**Not found:**
- A rigorous upper bound on the fraction of energy deliverable into a band, stated in fibre and pulse parameters.
- Its tightness against optimized inputs.
- The exact long-distance band efficiency, written in optical variables.
- How self-steepening, Raman and $\beta_3$ break each piece. One-sided statements may survive: Raman conserves photon number and only lowers the mean frequency, which suggests a ceiling for blue-shifted bands.
- The multimode version, where modal propagation-constant offsets enter $\hat\beta_m$ and may make $\mathcal H$ indefinite.

**Companion card.** P-20261012-claude-interactive.4-04 (blue-band Raman budget) covers anomalous-dispersion supercontinuum, where $\mathcal H$ gives no ceiling. It uses the monotone Raman red-shift of the mean frequency together with momentum. This card covers normal and all-normal dispersion, where the Hamiltonian ceiling applies.

### Conjectures

None registered. A refutable first conjecture: for an unchirped Gaussian in pure-$\beta_2$ normal-dispersion fibre, the best SESS outermost-lobe efficiency at offset $\Delta$ stays within a factor of 3 of the Hamiltonian–Markov ceiling once $\Delta T_0\ge2$, and the factor tends to a constant as $N\to\infty$. Adjoint-optimized inputs that exceed the ceiling refute the bound. A ratio that grows without limit refutes the tightness part.

### Oracle

**Available.** FastDifferentiableMMNLO computes:
- scalar and multimode GNLSE propagation with arbitrary $\beta_m(\omega)$, self-steepening and Raman;
- adjoint gradients of any output functional, including $\eta_B$.

**The refutation engine is direct:** maximize $\eta_B$ over input amplitude and phase (or spectral phase) at fixed energy, by gradient ascent through the adjoint, and compare against the ceiling. Inverse-scattering checks need a Zakharov–Shabat eigenvalue and reflection-coefficient solver, which is a short numpy code.

**Cheap tests:**
- $\gamma\to0$ gives $\eta_B$ constant;
- the invariants hold to discretization accuracy;
- the Markov bound saturates only for two-point spectra.

**Caveat.** A finite pseudospectral step does not conserve physical momentum exactly, because of aliasing (assessment in PR #37). Invariant drift must be monitored.

### Lab test

In an SESS setup:
- Sweep power and fibre length at fixed $T_0$.
- Measure the energy in the outermost lobe beyond offset $\Delta$.
- Compare with the ceiling, and with the efficiency an adjoint-designed pre-chirp or spectral phase reaches.

Any calibrated measurement above the ceiling falsifies the bound, after correcting for Raman and loss, which only lower blue-side efficiency.

### Risks and must-reads

- **The Markov ceiling may be loose by a large factor.** The value then lies in the sharpened, higher-invariant or inverse-scattering version, which may hold only for the pure NLSE.
- **Anomalous dispersion has no Hamiltonian ceiling.** There $\mathcal H$ is indefinite and soliton fission is unbounded; the card covers normal and all-normal dispersion only.
- **Must-reads:**
  - the SESS papers (Liu and Kärtner groups; DESY), full text;
  - Finot et al. 2008, full text;
  - Heidt's ANDi supercontinuum work;
  - any mathematical-physics paper on spectral concentration or moment bounds for defocusing NLSE solutions;
  - the inverse-scattering literature on the asymptotic spectrum of optical pulses in normal dispersion.
- **Possible prior art in mathematics:** $H^1$ bounds and decay estimates may already imply the optical statement. Novelty would then lie in the tight optical form and its tests.

</details>

## Audit trail


| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive (claude; claude-opus-5-5) | Proposed as candidate on the PI's frequency-conversion request; literature unaudited | PI request in chat, 2026-10-12; bounded search listed above |
| 2026-10-13 | gpt-a (gpt; gpt-6-astra) | literature unaudited → partial; novelty confidence → medium; added GPT review and revised gap; candidate and priority retained pending Claude concurrence | Cross-family review docs/review-2026-10-13-gpt-a-frequency-conversion-novelty.md; runs 2026-10-13-gpt-a-novelty-literature and 2026-10-13-gpt-a-novelty-premises; follow-ups T-20261013-gpt-a-02, T-20261013-gpt-a-03, T-20261013-gpt-a-04 |
| 2026-10-17 | claude-interactive (claude; claude-opus-5-5) | candidate → parked: merged into P-20261016-claude-interactive-01 (PI decision 2026-10-16); priority unchanged | Task T-20261016-claude-interactive-06, closed in T-20261017-claude-interactive-01; the "Merged cards" section of P-20261016-claude-interactive-01 |
