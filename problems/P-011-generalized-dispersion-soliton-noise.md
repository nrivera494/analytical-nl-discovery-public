---
id: P-011
title: "Fluctuation modes and squeezing of generalized-dispersion solitons"
status: audited
priority: 4
literature_state: partial
novelty_confidence: low
target_quantity: "A fluctuation-mode and measurable quadrature-covariance theory for quartic-dominated solitons, including controlled residual quadratic dispersion."
model: "Scalar Kerr propagation with quartic/mixed dispersion and specified quantum reservoirs; a cavity version requires explicit gain and loss operators."
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

The fluctuation modes, quadrature covariance and optimum measurable detection mode of a physically realized quartic-dominated pulse. Separate passive propagation from a gain/loss cavity. Report dependence on residual quadratic/quartic dispersion, nonlinear length, propagation distance and reservoir strength. The pure-quartic idealization must tolerate a stated nonzero dispersion error; a result only at exactly vanishing lower orders is inadequate.

## Signal of hidden simplicity

Pure-quartic pulses have a reproducible profile family and distinctive energy-width scaling. Their oscillatory tails and internal mode suggest a compact perturbation structure, but do not guarantee that timing alone captures all fluctuations.

## Literature state

- Blanco-Redondo et al., *Pure-quartic solitons*, DOI [10.1038/ncomms10427](https://doi.org/10.1038/ncomms10427) — **abstract only**, introductory passages also consulted. Experimental and numerical evidence for quartic-dominated solitons and an approximate Gaussian shape. The Gaussian is not an exact profile.
- Tam et al., *Stationary and dynamical properties of pure-quartic solitons*, DOI [10.1364/OL.44.003306](https://doi.org/10.1364/OL.44.003306) — **abstract only**. Numerically computes a family and linear eigenspectrum; analytically explains oscillatory tails. Stability spectra and an internal mode are already known, so computing a numerical spectrum alone is not the gap.
- Zou et al., *Quantum diffusion of pure-quartic solitons in a laser cavity*, DOI [10.1364/OE.545988](https://doi.org/10.1364/OE.545988) — **full text**, cavity/noise model and timing-noise analysis read in the publisher-supplied full text. ASE-driven cavity simulations are compared with the standard analytical direct timing-diffusion formula, Eq. (3), in a near-zero-net-dispersion regime. Indirect Gordon–Haus noise is reported suppressed there. This closes a generic claim that quartic-pulse timing noise lacks an analytical description; it does **not** derive a complete mixed-dispersion Gordon–Haus theory or quantum squeezing covariance. The attribution of high-frequency noise to tail interactions is a numerical interpretation, not a proven universal law.

Searches: `pure quartic soliton quantum noise squeezing Gordon Haus`, exact Tam and Zou titles, and forward citation/title leads from the original quartic-soliton work. No complete physically measured covariance/squeezing law with residual dispersion was located. This search does not certify its absence.

Added in the claude-b review (2026-10-04, T-20261002-gpt-a-04). Helper claude-b.8 found these; claude-b checked every DOI or arXiv record. Access is **abstract only** unless stated. The helper's forward-citation lists (Semantic Scholar: 5, 104, 206 and 220 citing works of Zou, Tam, Runge and Blanco-Redondo) are incomplete.
- **Building blocks without noise:**
  - Widjaja et al., "Absence of Galilean invariance for pure-quartic solitons," PRA 104, 043526 (2021), DOI [10.1103/PhysRevA.104.043526](https://doi.org/10.1103/PhysRevA.104.043526). A PQS moving at another group velocity requires nonzero $\beta_2,\beta_3$ and has an asymmetric spectrum. The frequency-to-velocity map that converts frequency noise into timing jitter (the Gordon–Haus mechanism) is therefore not the simple Galilean one. This is the ingredient a PQS Gordon–Haus theory must use.
  - Tam et al., "Generalized dispersion Kerr solitons," PRA 101, 043822 (2020), DOI [10.1103/PhysRevA.101.043822](https://doi.org/10.1103/PhysRevA.101.043822): the mixed $\beta_2$–$\beta_4$ soliton family.
  - Deng, Ma, Zhang, Malomed, Fan, He & Liu, "Internal dynamics and fission of pure-quartic soliton molecules," PRA (2025), DOI [10.1103/mzs4-944y](https://doi.org/10.1103/mzs4-944y), [arXiv:2505.17376](https://arxiv.org/abs/2505.17376): tail-mediated interactions, relevant to the tail-induced noise Zou et al. report.
- **No noise result in the laser paper:** Runge et al., "The pure-quartic soliton laser," Nat. Photon. (2020), DOI [10.1038/s41566-020-0629-6](https://doi.org/10.1038/s41566-020-0629-6), [arXiv:1910.10314](https://arxiv.org/abs/1910.10314). Per the helper's full-text search it has no noise or jitter results. **Not read by claude-b.**
- **Method templates for noise of non-sech solitons:**
  - Li, Spiller & Biondini, PRA 75, 053818 (2007), DOI [10.1103/PhysRevA.75.053818](https://doi.org/10.1103/PhysRevA.75.053818): noise-induced perturbations of dispersion-managed solitons.
  - Grigoryan, Menyuk & Mu, J. Lightwave Technol. 17, 1347 (1999), DOI [10.1109/50.779156](https://doi.org/10.1109/50.779156): timing and amplitude jitter of arbitrary pulse shapes by linearization.
  - Shamailov & Erkintalo, [arXiv:2605.29321](https://arxiv.org/abs/2605.29321) (2026): quantum and classical noise of parametrically driven cavity solitons (quadratic dispersion).
  - Gustin, Yanagimoto, Ng & Mabuchi, [arXiv:2605.17025](https://arxiv.org/abs/2605.17025) (2026): open-system quantum soliton dynamics beyond linearization.

## Sharpest statement of the gap

Retain the covariance/squeezing target and a controlled extension beyond the already treated timing-diffusion limit. A direct ASE timing formula dressed with a fitted pulse-shape factor is not new. Quantifying residual-dispersion coupling and internal-mode contributions may be worthwhile, but first compare against the existing spectrum and general adjoint methods in P-001.

**Second-family review (claude-b, 2026-10-04): agreed.**
- **Not found:** no squeezing or quadrature-covariance theory, and no frequency-to-timing (Gordon–Haus) jitter theory, for pure-quartic or mixed-dispersion solitons. The internal mode and residual $\beta_2$ have not been treated as noise channels.
- **Sharpest new ingredient:** the broken Galilean invariance of PQS (Widjaja 2021). The frequency-to-velocity coefficient of the moving PQS family replaces the Gordon–Haus factor $\beta_2$. A PQS Gordon–Haus coefficient therefore cannot be copied from the sech case.
- **Still to read:** Zou et al. 2025 full text, to check that its analytic model is direct diffusion only. gpt-a read it; claude-b and its helper could not access it (Optica bot check).

## Conjectures

None.

## Oracle

Downgraded to partial. Higher-order-dispersion propagation and Jacobians are reported; a quantum covariance implementation must establish field normalization, vacuum and Raman/loss reservoirs, and measurement-mode normalization. A classical additive-noise simulation by itself cannot verify squeezing below shot noise.

## Lab test

Use dispersion-shaped pulses or a programmable cavity with a measured transfer function. Measure timing noise and homodyne quadrature noise in specified temporal modes while varying residual quadratic dispersion; account for detector efficiency and cavity loss.

## Risks and must-reads

The cavity timing result must be reproduced as a known limit before extending it. Full Tam methods and mixed-dispersion work remain required reading. Radiation tails, filtering and gain noise can erase any practical squeezing advantage.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-01 | claude-bootstrap (claude) | Created as unaudited candidate | Additional-candidates list, literature audit Oct 2026 |
| 2026-10-02 | gpt-a (gpt; model unknown) | Retained candidate; unaudited → partial; oracle → partial; removed broad timing-noise novelty | Zou 2025 gives analytical direct ASE timing diffusion plus simulations; general covariance and residual-dispersion target remains distinct |
| 2026-10-04 | claude-b (claude; claude-opus-5-5) | Second-family review (T-20261002-gpt-a-04). Agrees with gpt-a on what is open; adds broken Galilean invariance (the Gordon–Haus ingredient), the mixed-dispersion family, PQS tail interactions and noise-method templates. candidate → audited; audited_by [gpt] → [gpt, claude]; priority 4, literature_state partial and novelty_confidence low unchanged | Crossref/arXiv records and abstracts; helper claude-b.8 search; Zou 2025 full text not accessible to the Claude review. Log `log/2026-10-04_claude-b_T-20261002-gpt-a-04.md` |
