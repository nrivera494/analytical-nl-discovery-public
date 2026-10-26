---
id: P-008
title: "Dynamics and onset statistics of soliton self-mode conversion"
status: audited
priority: 3
literature_state: partial
novelty_confidence: low
target_quantity: "Conversion distance, transfer history and their noise dependence for Raman-driven transfer between group-velocity-matched spatial modes."
model: "Multimode GNLSE with measured modal dispersion, delayed Raman response and a specified spontaneous-noise model."
oracle_ready: partial
last_audited: 2026-10-04
audited_by: [gpt, claude]
proposed_by: claude-bootstrap
updated_by: claude-b
updated_model: claude-opus-5-5
updated_family: claude
claims: []
results: []
---

## Target quantity

A collective-coordinate or asymptotic law for the distance at which a specified fraction of energy has transferred, the subsequent depleted-pump conversion trajectory, and the distribution of that distance for a specified noise source. Hold the candidate mode pair and their dispersion fixed first. Regime axes include group-delay mismatch across the pulse, Raman detuning/gain width, nonlinear length and Raman response time/pulse duration.

## Signal of hidden simplicity

Experiments report conversion into a clean soliton in a different spatial mode, including conversion initiated from noise. The target is the transfer history and onset law, not the already known group-index matching condition.

## Literature state

- Rishøj et al., *Soliton self-mode conversion: revisiting Raman scattering of ultrashort pulses*, DOI [10.1364/OPTICA.6.000304](https://doi.org/10.1364/OPTICA.6.000304), arXiv:1805.06037. **Full text of the arXiv version** (claude-b, 2026-10-04).
  - Content: experimental observation establishes the effect, originating from quantum noise, and its group-velocity-matching interpretation.
  - Not covered: the preprint contains no model of the transfer history, no threshold and no onset statistics.
- Antikainen et al., *Fate of a Soliton in a High Order Spatial Mode of a Multimode Fiber*, DOI [10.1103/PhysRevLett.122.023901](https://doi.org/10.1103/PhysRevLett.122.023901) — **abstract only**. Numerical GNLSE study shows noise-induced conversion can outrun intramodal self-frequency shift. A group-index-matched lower-order mode at a frequency with appreciable Raman gain determines the growing pulse's wavelength. The seed card's proposed destination-selection rule is therefore not an unoccupied gap.
- Kabagöz, Antikainen and Ramachandran, *Converting noise into solitons: optical self-organization through intermodal nonlinearity*, DOI [10.1364/OE.424256](https://doi.org/10.1364/OE.424256) — **abstract only**. Experimental noise-seeded conversion yields reproducible soliton output; robust output shape does not by itself imply a universal onset-distance distribution.

Searches: `soliton self mode conversion analytical collective coordinate Raman`, the Rishøj title, the Antikainen title, and forward title/citation searches leading to the 2021 noise-conversion experiment. No controlled depleted-transfer and stochastic-onset law was located. Full methods remain a novelty check.

Added in the claude-b review (2026-10-04, T-20261002-gpt-a-04). Helper claude-b.8 found these; claude-b checked every DOI against Crossref. The helper used Semantic Scholar forward-citation lists of the four SSMC papers (75, 30, 3 and 6 citing works); these lists are incomplete. Access is **abstract only** unless stated.
- **The SSMC follow-ups are experiments or full simulations**, with no reduction:
  - Antikainen, Kabagöz & Ramachandran, OL 45, 5393 (2020), DOI [10.1364/OL.400250](https://doi.org/10.1364/OL.400250): a noise seed in another mode, orders of magnitude weaker than the soliton, destroys shot-to-shot coherence through SSMC;
  - three CLEO abstracts from the same group:
    - noisy origins of SSMC: DOI [10.1364/CLEO_QELS.2020.FTh1A.3](https://doi.org/10.1364/CLEO_QELS.2020.FTh1A.3);
    - electronic control: DOI [10.1364/CLEO_SI.2022.STh4E.3](https://doi.org/10.1364/CLEO_SI.2022.STh4E.3);
    - seeded intermodal Raman scattering: DOI [10.1364/CLEO_SI.2023.STh1P.4](https://doi.org/10.1364/CLEO_SI.2023.STh1P.4);
  - Rishøj et al., Opt. Express 28, 4333 (2020), DOI [10.1364/OE.384395](https://doi.org/10.1364/OE.384395): jitter-free dual-wavelength sources based on SSMC.
- **Closest reduced model in a neighbouring regime:** Liu, Yang, Fan, Yuan & Mei, J. Lightwave Technol. 43, 6894 (2025), DOI [10.1109/JLT.2025.3557847](https://doi.org/10.1109/JLT.2025.3557847). Moment equations for the energy in each mode under intrapulse Raman (higher-order mode to LP01 transfer by Raman soliton trapping in tapered fiber). It treats neither group-velocity-matched pairs nor noise seeding.
- **Polarization analogue:** Stefańska et al., OL 47, 4183 (2022), DOI [10.1364/OL.463643](https://doi.org/10.1364/OL.463643): Raman transfer into the orthogonal polarization at a group-velocity-matched wavelength.
- **Disorder-averaged intermodal Raman coupling for incoherent waves:** Baudin et al., PRA 105, 013528 (2022), DOI [10.1103/PhysRevA.105.013528](https://doi.org/10.1103/PhysRevA.105.013528).
- **Template for onset statistics:** quantum-noise-initiated Stokes growth and macroscopic Stokes-energy fluctuations in single-mode stimulated Raman scattering (Raymer & Mostowski, PRA 24, 1980 (1981), DOI [10.1103/PhysRevA.24.1980](https://doi.org/10.1103/PhysRevA.24.1980); Walmsley & Raymer, PRL 50, 962 (1983), DOI [10.1103/PhysRevLett.50.962](https://doi.org/10.1103/PhysRevLett.50.962)). No application to group-velocity-matched fiber modes was found.

## Sharpest statement of the gap

Destination matching is established. The plausible residual gap is a quantitative dynamical reduction including overlap evolution, depletion and noise-seeded initiation, with an explicit domain of validity. A fixed-shape Raman-gain estimate alone may already describe early growth and is not enough to claim a new law.

**Second-family review (claude-b, 2026-10-04): agreed.**
- **Found:** no published reduction of SSMC giving conversion distance, transfer history or onset statistics.
- **Neighbouring results:**
  - modal energy moment equations for a different Raman transfer (Liu et al. 2025);
  - the polarization analogue;
  - a kinetic theory for incoherent waves.
- **The natural route to the onset law:** the Raymer–Mostowski quantum-initiated Stokes statistics adapted to a group-velocity-matched pulsed mode pair. This is a template, not a published result for fiber modes.

## Conjectures

None.

## Oracle

Deterministic multimode Raman propagation is reported available. Marked partial because calibrated spontaneous Raman noise and its modal covariance have not been verified in the evaluator. First compare a deterministic weak seeded transfer; then assess noise initiation without confusing input vacuum sampling with distributed spontaneous Raman emission.

## Lab test

Use fiber cut-backs and modal/spectral decomposition to measure transfer curves and conversion-distance statistics at fixed launch mode, pulse energy and duration. Deliberately vary a weak Stokes seed to distinguish a noise-controlled delay from subsequent deterministic depletion.

## Risks and must-reads

Full text of the 2019 theory and 2021 experiment is required before claiming novelty. More than one matched destination, evolving overlap or dispersive radiation can invalidate a two-mode closure. No new theory or stochastic run has been performed here.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-01 | claude-bootstrap (claude) | Created as unaudited candidate | Additional-candidates list, literature audit Oct 2026 |
| 2026-10-02 | gpt-a (gpt; model unknown) | Retained candidate; priority 4 → 3; unaudited → partial; oracle → partial | Antikainen 2019 closes the proposed matching-rule novelty; 2021 experiment supports a narrower transfer/onset target |
| 2026-10-04 | claude-b (claude; claude-opus-5-5) | Second-family review (T-20261002-gpt-a-04). Agrees with gpt-a on what is open; Rishøj 2019 read in full (arXiv); adds follow-ups, neighbouring reductions and the Raymer–Mostowski onset template. candidate → audited; audited_by [gpt] → [gpt, claude]; priority 3, literature_state partial and novelty_confidence low unchanged | Rishøj arXiv full text; Crossref records and abstracts for the rest; helper claude-b.8 search. Log `log/2026-10-04_claude-b_T-20261002-gpt-a-04.md` |
