---
agent: gpt-a
model: gpt-6-astra
family: gpt
---

# Material evidence read during the independent audit

- Corning, SMF-28 Ultra product information PI-1424-AEN, issued July 2025,
  **full text** (2 pages), no DOI assigned to this manufacturer datasheet.
  https://www.corning.com/content/dam/corning/media/worldwide/coc/documents/Fiber/product-information-sheets/PI-1424-AEN.pdf
  Specifies zero-dispersion wavelength 1304–1324 nm, slope <=.092 ps/(nm² km),
  dispersion <=18 ps/(nm km) at 1550 nm and <=23.7 at 1625 nm, attenuation
  <=.18 dB/km at 1550 and <=.20 at 1625. It does not certify the extrapolated
  long-wavelength curve used here or constant loss throughout the output band.
- Lüpken and Fallnich, Applied Physics B 126, 183 (2020), DOI
  [10.1007/s00340-020-07538-w](https://doi.org/10.1007/s00340-020-07538-w),
  **full text** accessed on the publisher page. Their SMF28 dispersion was
  calculated by a mode solver, with approximately 18 ps/(nm km) at 1550 nm.
  This is contextual support for wavelength-dependent dispersion, not data
  fitted or digitized for this run.

The robustness curve is a representative G.652-type zero-dispersion-slope
model D(lambda)=S0/4 [lambda-lambda0^4/lambda^3], lambda0=1310 nm, normalized
to beta2(1550 nm)=-21.7 ps²/km. It is not a measured sample curve. Its
wavelength extrapolation and constant gamma/loss remain limitations.

Searches (2026-10-17): "Corning SMF-28 Ultra dispersion slope 0.092 1310
datasheet"; "SMF-28 dispersion curve Raman soliton 2000 nm measured
dispersion Sellmeier". No absence-of-prior-theory claim is made.

- Kormokar, Shamim and Rochette, arXiv:**2301.02945**, **full text**, including
  Table 1: https://arxiv.org/pdf/2301.02945 . The published SMF-28 dispersion
  and nonlinear Taylor coefficients are now an additional material attack.
  The paper establishes interpulse Raman enhancement for unshaped pulses;
  it does not certify the present phase-mask optimum. Its constant-loss
  measurement covers approximately 1.5–1.8 micrometres, not all wavelengths.
- Efimov et al., DOI **10.1364/OL.29.000271**, **abstract only**, via PubMed:
  https://pubmed.ncbi.nlm.nih.gov/14759048/ . Adaptive spectral-phase control
  of SSFS is prior work. This audit asserts no novelty for that phenomenon.

## Bounded novelty check during the serial optimization

Searches (2026-10-17): `"Raman soliton" "spectral phase" "energy"
optimization`; `"soliton" "phase-only" "Raman" optimization energy`;
`"Adaptive control" "Raman" "soliton" Efimov 2004`;
`"phase" "Raman soliton" "maximum" energy chirp optimization bound`.
These searches do not establish absence of prior theory.

- Hu et al., DOI **10.1103/PhysRevLett.114.073901**, **full text** of the
  accepted manuscript, including the main text and figure captions:
  https://link.aps.org/accepted/10.1103/PhysRevLett.114.073901 . Cubic spectral
  phase and chirp control primary/secondary Raman solitons in experiments and
  simulations; the paper discusses energy captured from the main lobe and
  subsequent tails. Energy redistribution by phase shaping is therefore not
  itself a new mechanism established by this audit. Supplementary material
  was not read.
- Rosenberg et al., DOI **10.1364/OE.383014**, **abstract only** verified via
  https://pubmed.ncbi.nlm.nih.gov/32121985/ . The abstract reports enhanced
  few-cycle SSFS with negative prechirp and attributes it to redistribution
  among fission products. The publisher full-text request failed; secondary
  search snippets were not used to claim a full-text assessment.

These papers concern phase/chirp control in other pulse and fibre regimes.
They do not supply a global certificate for the present optimization in the
material accessed here. No novelty claim for the exact numerical headroom,
and no exhaustive absence-of-an-upper-bound claim, is made.
