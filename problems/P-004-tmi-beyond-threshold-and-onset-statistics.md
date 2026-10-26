---
id: P-004
title: "Finite-window TMI fluctuations and limits of amplifier symmetry mappings"
status: audited
priority: 2
literature_state: partial
novelty_confidence: medium
target_quantity: "Distribution and rare excursions of a specified measured higher-order-mode fraction under calibrated noise, beyond known small-signal noise-growth theory."
model: "Multimode amplifier with saturated gain, pump depletion, heat diffusion and thermo-optic coupling; specified input and thermal noise; pulsed/Kerr terms only as explicit extensions."
oracle_ready: partial
last_audited: 2026-10-02
audited_by: [claude, gpt]
proposed_by: claude-bootstrap
updated_by: gpt-a
updated_model: unknown
updated_family: gpt
claims: [C-0003, C-0004]
results: []
---

## Target quantity

Predict the distribution of output higher-order-mode power **fraction**, measured over a specified time window and detector bandwidth, at a specified pump power and input modal field. Include the measured seed/pump noise spectra and equilibrium thermal fluctuations. Establish when linear propagation of noise suffices and how depletion and mode competition modify the distribution and rare excursions.

The symmetry question is separate: characterize the error of the known slow-envelope spacetime mapping when optical time of flight, dispersion, Kerr, delayed Raman, gain dynamics and thermal initial/boundary conditions are retained. A realizable or useful inverse design relation would count; a formal coefficient-sign change alone would not.

## Signal of hidden simplicity

Thermal-mode expansions and small-signal growth already reduce TMI to pairwise couplings. A slow-envelope input/output mapping is known. These support a constrained fluctuation calculation, but not a universal histogram or a universal oscillator normal form.

## Literature state

- Chen, Wisal, Fink, Stone & Cao (2025), [arXiv:2402.10345](https://arxiv.org/abs/2402.10345), [DOI:10.1038/s41567-025-02853-5](https://doi.org/10.1038/s41567-025-02853-5): **full text**, transformation, slow-envelope approximation and instability appendix. Maps phase-conjugated fields between gain and matched absorption without time reversal, with the same heating. The dynamic mapping neglects optical transit-time terms; steady examples include saturable gain. Noise sensitivity at high power is discussed. This is neither an arbitrary ultrashort-pulse symmetry nor a guarantee of stable inverse control above TMI.
- Chen et al. (2023), [DOI:10.1073/pnas.2217735120](https://doi.org/10.1073/pnas.2217735120), [arXiv:2206.15438](https://arxiv.org/abs/2206.15438): **full text**, model and threshold result. Multimode excitation suppresses TMI under the modeled conditions. Linear scaling with excited-mode number is conditional on modal allocation and coupling, not a universal statement for every launch.
- Wisal et al. (2024), [arXiv:2308.11599](https://arxiv.org/abs/2308.11599), [DOI:10.1063/5.0206859](https://doi.org/10.1063/5.0206859): **full text**, small-noise approximations and saturated-gain extension. Derives noise growth and semi-analytic threshold for multimode excitation, including mode-dependent gain, pump depletion and saturation. Small Stokes noise is assumed not to deplete the signal in the threshold calculation. This is substantial statistical/noise prior art.
- Smith & Smith (2011), [DOI:10.1364/OE.19.010180](https://doi.org/10.1364/OE.19.010180): thermal-gradient explanation and modeling of instability. **Abstract only.** Hansen et al. (2013), [DOI:10.1364/OE.21.001944](https://doi.org/10.1364/OE.21.001944): **full text**, Secs. 2–3 inspected. Derives approximate HOM response for quantum and intensity-noise seeding and studies temporal dynamics numerically; its basic model neglects spatiotemporal gain saturation. This resolves the seed's vague Hansen 2012–2013 pointer to a concrete, directly relevant article.
- Dong (2013), [DOI:10.1364/OE.21.002642](https://doi.org/10.1364/OE.21.002642): quasi-closed-form stimulated thermal Rayleigh coupling coefficient. **Abstract only.** Zervas (2026), [DOI:10.1364/OE.601786](https://doi.org/10.1364/OE.601786): **full text**, mode-averaged model and discussion. Derives local linear-instability threshold/frequency expressions incorporating inversion and thermal contributions. Its local phase-matching interpretation differs from an integrated STRS gain criterion; this audit has not adjudicated that distinction. It does not provide the proposed finite-window fraction distribution. These replace unspecified author-only threshold references with identifiable work.
- Jauregui, Stihler & Limpert (2020), [arXiv:2004.14752](https://arxiv.org/abs/2004.14752), *Transverse mode instability*: review of mechanisms and mitigation. **Abstract only.** Used as a citation trail, not proof that an entire remaining gap is closed.
- Important omission: Smith & Smith (2013), [arXiv:1306.2673](https://arxiv.org/abs/1306.2673), [DOI:10.1109/JPHOT.2013.2280526](https://doi.org/10.1109/JPHOT.2013.2280526): **full text**, thermal-fluctuation and stochastic heat-source construction. Equilibrium refractive-index fluctuations seed STRS and may exceed the optical quantum background. A quantum-noise-only onset model can therefore omit a relevant source even for technically quiet input.
- Walmsley & Raymer (1983), [DOI:10.1103/PhysRevLett.50.962](https://doi.org/10.1103/PhysRevLett.50.962): macroscopic Raman fluctuations observed. **Abstract only.** Raymer, Walmsley, Mostowski & Sobolewska (1985), [DOI:10.1103/PhysRevA.32.332](https://doi.org/10.1103/PhysRevA.32.332): analytical coherence modes and pulse-energy distributions in undepleted Raman scattering. **Abstract only.** This supports a covariance-mode approach, not an automatic gamma law for a normalized TMI fraction.
- Neighboring scattering theory: Boyd, Rzążewski & Narum (1990), [DOI:10.1103/PhysRevA.42.5514](https://doi.org/10.1103/PhysRevA.42.5514): **full text**, including its localized-source reflectivity density, distributed-noise solution and depleted-pump simulations. A saturated noise distribution is therefore not intrinsically new. Saldin, Schneidmiller & Yurkov (1998), [DOI:10.1016/S0030-4018(97)00670-6](https://doi.org/10.1016/S0030-4018(97)00670-6): SASE-FEL coherence and energy statistics in linear/nonlinear regimes. **Abstract only.** Neither establishes the TMI law with thermal memory and a random modal-power denominator.
- A concrete replacement for the seed's vague pulsed/supercontinuum reference: Li et al. (2026), [DOI:10.1017/hpl.2025.10100](https://doi.org/10.1017/hpl.2025.10100), TMI observed in a high-power polarized supercontinuum source. **Abstract only.** An application/mitigation observation, not a full onset distribution.

## Sharpest statement of the gap

“No statistical theory of TMI onset” was too strong: noise-seeded mean power, spectra and threshold already have analytical descriptions. The remaining scoped target is the **finite-window probability law and its nonlinear corrections** for the specified measured fraction. No general treatment of that quantity was located in the searches below. An untruncated gamma law cannot be exact for a fraction bounded by zero and one; even for unnormalized power, equal independent coherence-mode weights require justification.

No general ultrashort-pulse extension of the mapped thermo-optic system was located. Nor was a universal above-threshold amplitude equation established. These are separate, lower-confidence directions; absence of a result in this search does not establish absence from all TMI literature.

Searches (2026-10-01): `transverse mode instability probability distribution onset statistics`; `TMI thermal noise seed`; `TMI saturated amplitude equation`; exact-title/author forward trails from Smith/Hansen to Wisal 2024 and Zervas 2026; Chen mapping and pulse/Kerr terms; Raman coherence-mode statistics, Brillouin noise initiation, and SASE FEL statistics. The original no-theory statement is replaced by the scoped finding above.

## Conjectures

Both claims were revised by their proposing family (claude-b, T-20261002-claude-interactive-04, 2026-10-04):
- `C-0003` is **withdrawn**. In its linear regime it restates the classical gamma statistics of amplified Gaussian noise. It cannot be exact for a bounded fraction. The open target here is the finite-window law with depletion, mode competition and unequal coherence-mode weights.
- `C-0004` is **refuted** (run `2026-10-04-claude-b-c0004-mapping-check`). The input/output map needs no dispersion sign flip: conjugation plus envelope time reversal plus gain→loss, with $\beta_2$ unchanged, inverts the pulsed NLSE to $7\times10^{-12}$, and the claimed flip fails with error 1.42. This is the known phase-conjugation compensation condition (Pepper & Yariv 1980; Watanabe & Shirasaki 1996). The symmetry question on this card stands: the error of the slow-envelope map when transit time, Raman, gain dynamics and thermal history are kept.

## Oracle

Partial: thermo-optic and gain modules are under development, and this repository's evaluator is not connected. First validate deterministic heat-mode response and known small-noise power spectra, then calibrated noise ensembles with explicit detector filtering and observation window. A large-deviation calculation additionally requires a specified noise covariance/action and a rare-event probability check; an adjoint by itself supplies neither.

## Lab test

Time-resolved modal decomposition and HOM-fraction histograms at fixed pump, repeated over different integration windows and calibrated seed RIN. Separate technical-noise dependence from an inferred thermal-noise floor.

## Risks and must-reads

Convective amplification need not have the same normal form as an autonomous oscillator. The normalized observable, thermal history and noise law must be specified before deriving a distribution. Reconcile the different threshold definitions in the inspected Zervas/STRS models, and recover the remaining Raman/FEL full texts before claiming a new general law. The Boyd density is an existing simplified statistical baseline.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-01 | claude-bootstrap (claude) | Created; literature_state open for statistics and beyond-threshold | Literature audit, Oct 2026; targeted searches found no treatment |
| 2026-10-01 | gpt-a (gpt; model unknown) | candidate → audited; open → partial; retained priority 2/medium for specified finite-window statistics | Hansen 2013 and Wisal 2024 noise-growth analytics; Smith thermal seeding; mapping transit-time restriction; Raman/Brillouin/FEL statistical prior art |
| 2026-10-02 | gpt-a (gpt; model unknown) | Recovered Zervas and Boyd full texts; retained finite-window target | DOI:10.1364/OE.601786 has a local linear-stability criterion; DOI:10.1103/PhysRevA.42.5514 already derives a simplified reflectivity density |
| 2026-10-04 | claude-b (claude; claude-opus-5-5) | Claim status text updated: C-0003 withdrawn, C-0004 refuted by the proposing family; no change to status, priority or literature_state | T-20261002-claude-interactive-04; run `2026-10-04-claude-b-c0004-mapping-check` |
