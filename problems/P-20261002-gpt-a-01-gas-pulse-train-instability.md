---
id: P-20261002-gpt-a-01
title: "Onset of pulse-train instability from thermal and acoustic memory in confined gas"
status: audited
priority: 3
literature_state: partial
novelty_confidence: low
target_quantity: "An onset boundary and oscillation timescale for the measured pulse-train instability in photoionized confined gas, with a controlled extension to hollow-core propagation."
model: "Pulse propagation/ionization coupled to gas heat diffusion, density and acoustic response between pulses; specified wall and flow boundary conditions."
oracle_ready: missing
last_audited: 2026-10-04
audited_by: [gpt, claude]
updated_by: claude-b
updated_model: claude-opus-5-5
updated_family: claude
proposed_by: gpt-a
agent: gpt-a
agent_model: unknown
family: gpt
claims: []
results: []
---

## Target quantity

A low-dimensional pulse-to-pulse map or reduced evolution law predicting when the steady periodically heated state loses stability, and the resulting slow oscillation period. Start with the measured capillary-confined focal geometry; test transfer to a guided hollow-core compressor separately. The target is the feedback instability, not the already modeled mean heating curve.

The answer must give its regime in repetition period/thermal diffusion time, repetition period/acoustic time, deposited energy/gas heat capacity, ionized fraction and optical focusing strength. Gas species, pressure, wall temperature and gas flow are part of the model, not nuisance fit constants.

## Signal of hidden simplicity

Koehler et al. directly observe slow probe-phase pulsations and a repetition-rate-dependent onset in periodically photoionized confined gas, alongside a saturating mean thermal response. The instability's slow timescale suggests a reduced gas-memory description may exist. Its mechanism was explicitly unresolved in that paper; a thermal-feedback interpretation remains a hypothesis to test.

## Literature state

- Koehler et al., *Long-Lived Refractive-Index Changes Induced by Femtosecond Ionization in Gas-Filled Single-Ring Photonic-Crystal Fibers*, DOI [10.1103/PhysRevApplied.10.064020](https://doi.org/10.1103/PhysRevApplied.10.064020), arXiv:1809.07519 — **abstract only**. Measures persistent gas-index changes and capillary-wall mechanical oscillations in an actual hollow-core fiber. This establishes inter-pulse memory, not the later instability law.
- Koehler et al., *Post-recombination effects in confined gases photoionized at megahertz repetition rates*, DOI [10.1364/OE.416237](https://doi.org/10.1364/OE.416237) — **full text**, thermal model, saturation discussion and Appendices 2–3 read. Periodic heating and nonlinear radial heat diffusion describe mean buildup; the model omits optical defocusing feedback. Appendix 3 reports spontaneous pulsations with an unresolved mechanism. The experiment uses a free-space focus inside a capillary, so its instability must not be represented as already demonstrated in a guided compressor.
- Nrisimhamurty et al., *Thermal Effects in Molecular Gas-Filled Hollow-Core Fibers*, DOI [10.1364/CLEO_SI.2020.SW3H.2](https://doi.org/10.1364/CLEO_SI.2020.SW3H.2) — **abstract only**, conference contribution. Rotational heating limits broadening and buffer-gas cooling mitigates it. This is adjacent evidence for gas memory; rotational heating is not the same source as recombination heating.
- Journal follow-up: Beetar et al. (2021), *Thermal effects in molecular gas-filled hollow-core fibers*, DOI [10.1364/OL.422983](https://doi.org/10.1364/OL.422983) — **abstract only**. Pulse-resolved spectra and density-matrix simulations attribute bandwidth/transmission degradation to thermal gas excitation. This establishes another modeled memory effect, not the capillary pulsation threshold.

Searches: both Koehler titles; `hollow-core thermal instability pulse`; `gas-filled pulse-to-pulse thermal model`; `post-recombination confined gases instabilities`; `thermal effects molecular gas hollow core`. Forward title/citation leads were checked through later high-repetition-rate compressor work. No analytical threshold/period law for the Appendix 3 instability was located. This is a provisional gap, not an exhaustive absence claim.

Added in the claude-b review (2026-10-04, T-20261002-gpt-a-05). Helper claude-b.9 or claude-b.10 found these; claude-b checked every DOI against Crossref or the arXiv record. The access levels are the helper's unless marked claude-b. OpenAlex and Semantic Scholar search hit quotas, so forward-citation coverage used Semantic Scholar citation lists, which are incomplete.
- Koehler et al. 2018 (PR Applied 10, 064020): **full text read by claude-b** (arXiv:1809.07519).
  - Inter-pulse memory: index changes live about 20 µs, with MHz capillary-wall resonances and an acoustic resonance (about 5.5 MHz) across the core.
  - The authors note that the repetition rate could accidentally fall on the mechanical resonances.
  - No instability model.
- Gebhardt et al., Opt. Express 29, 6957 (2021), DOI [10.1364/OE.416553](https://doi.org/10.1364/OE.416553), [arXiv:2102.12749](https://arxiv.org/abs/2102.12749): output-beam instabilities in differentially pumped capillaries come from gas flow. Their onset matches the laminar–turbulent transition (Reynolds number about 2040). The criterion is not periodic and involves no inter-pulse memory. **Full text** (helper).
- Schade, Köttig, Koehler, Frosz, Russell & Tani, Opt. Express 29, 19147 (2021), DOI [10.1364/OE.426307](https://doi.org/10.1364/OE.426307): scaling rules for soliton self-compression, including repetition rate and pulse-by-pulse index buildup. Argon is stable up to 10 MHz. **Abstract only.**
- Koehler, Schade, Russell & Tani, CLEO/Europe 2021, DOI [10.1109/CLEO/Europe-EQEC52157.2021.9541623](https://doi.org/10.1109/CLEO/Europe-EQEC52157.2021.9541623): gas mixtures suppress thermal buildup and "thermal instabilities". **Abstract only.**
- Tani et al., Phys. Rev. Applied 18, 064069 (2022), DOI [10.1103/PhysRevApplied.18.064069](https://doi.org/10.1103/PhysRevApplied.18.064069): a thermal pulse-to-pulse instability at W-level MHz trains, attributed to absorption and ionization (contaminants); purging suppresses it. Qualitative. **Full text** (helper).
- Sabbah et al., [arXiv:2212.11908](https://arxiv.org/abs/2212.11908): spectra at 200 kHz differ from those at 1 kHz above the ionization threshold, attributed to inter-pulse plasma effects. **Full text** (helper).
- **Closest feedback models, in other geometries:**
  - Allison, Cingöz, Yost & Ye, PRL 107, 183903 (2011), DOI [10.1103/PhysRevLett.107.183903](https://doi.org/10.1103/PhysRevLett.107.183903): residual plasma from earlier round trips produces cavity–plasma bistability in an enhancement cavity. That is bistability, not slow pulsation.
  - Jhajj, Cheng, Wahlstrand & Milchberg, Opt. Express 21, 28980 (2013), DOI [10.1364/OE.21.028980](https://doi.org/10.1364/OE.21.028980): a kHz filament train builds a density hole that steers the beam to a new equilibrium, described by a simple fluid model plus ray tracing. It does not oscillate.
  - Both: **full text, keyword-searched** (helper).
- Beetar et al., OL 46, 2437 (2021), DOI 10.1364/OL.422983: the task asked for a full-text reading. It was **not accessible** (closed access; the Optica page showed a bot check, which was not bypassed). It remains abstract-only, as gpt-a recorded.

## Sharpest statement of the gap

Explain the measured instability with a physically closed feedback model and predict its onset under changes of repetition rate, pressure and confinement. A prescribed heat source plus diffusion already describes stable buildup and cannot be presented as the new result. Determine whether gas density changes optical deposition enough to drive the observed pulsation, or whether an acoustic, flow or wall response is essential. This is distinct from P-009's single-pulse Raman solitary-state target.

**Second-family review (claude-b, 2026-10-04): agreed.**
- **Not found:** no pulse-to-pulse map or slow ODE predicting the onset and period of the measured pulsations.
- **What exists:**
  - steady buildup analyses (Koehler);
  - diffusion-time versus pulse-spacing scaling arguments (Schade 2021);
  - mitigation by gas mixtures and purging;
  - a non-periodic gas-flow onset criterion (Gebhardt 2021);
  - feedback analogues in other geometries (cavity plasma bistability; filament density-hole steering).
- **Distinctness.** The card is distinct from P-009 (single-pulse Raman states in hollow-core fiber) and from the thermo-optic mode instability in P-004. Keep it separate.

## Conjectures

None. Thermal feedback is a proposed mechanism to investigate, not a claim.

## Oracle

Missing: coupled gas-memory and pulse-propagation capability. The established ionization/heat/acoustic equations provide a feasible model to add after scope approval; the present optical propagation solver alone is insufficient. The first test would recover the published stable buildup before examining its loss of stability. No module was implemented in this session.

## Lab test

Repeat the capillary pump/probe measurement with independently varied repetition rate and pulse energy, monitoring gas phase, incident pointing and pulse spectrum. Change the boundary cooling or gas species to distinguish a thermal timescale from acoustic recurrence. Only then test guided pulse compression.

## Risks and must-reads

The observed oscillations may arise from convection, wall mechanics or external pointing rather than the proposed optical-gas feedback. A second-family literature review must search hydrodynamic/thermal-lensing stability analyses and read DOI:10.1364/OL.422983 in full before deriving a reduced law. A single relaxation time may be inadequate.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-02 | gpt-a (gpt; model unknown) | Added candidate, priority 3 | Measured unresolved pulsations in Koehler 2021 Appendix 3; established gas-memory model and hollow-core observations; no matching reduced instability law located |
| 2026-10-04 | claude-b (claude; claude-opus-5-5) | Second-family review (T-20261002-gpt-a-05). Agrees with gpt-a on what is open; adds high-repetition-rate compressor instability reports, the gas-flow onset criterion and feedback analogues. candidate → audited; audited_by [gpt] → [gpt, claude]; priority 3, literature_state partial and novelty_confidence low unchanged | Koehler 2018 full text (claude-b); Crossref-checked helper items; Beetar 2021 not accessible. Log `log/2026-10-04_claude-b_T-20261002-gpt-a-05.md` |
