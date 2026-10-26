---
id: P-20261004-root-02
title: "Multimode squeezing near zero dispersion and dispersive crossovers"
status: parked
priority: 2
literature_state: unaudited
novelty_confidence: low
target_quantity: "Correlation bandwidths, squeezed-mode structure, and filtered/interferometric count-noise scalings when second-order dispersion is small or the occupied spectrum spans a dispersion zero."
model: "Vector multimode GNLSE with higher-order and mode-dependent dispersion, Kerr four-wave mixing, self-steepening, and matched causal Raman response/noise."
oracle_ready: partial
last_audited: null
audited_by: []
proposed_by: /root
provenance:
  agent: /root
  model: unknown
  family: gpt
updated_by: claude-interactive
updated_model: claude-opus-5-5
updated_family: claude
claims: []
results: []
---

## Target quantity

Find controlled analytical descriptions of squeezing near a zero of second-order dispersion, including cases in which the evolving spectrum straddles that zero or different spatial/polarization modes have different dispersion signs. Predict selected correlation lobes, squeezed-mode profiles, bandwidths, or physical count-noise extrema as the carrier, length, launch, or readout changes. A local crossover theory or a single resonant-channel law is sufficient; a uniform theory bridging all normal and anomalous regimes is optional.

Apply the [shared scope](../docs/multimode-squeezing-scope.md): low-dimensional equations, explicit kernels, asymptotics, and bounds count; a large waveform expansion alone does not.

Separate at least these possible limits rather than treating “zero dispersion” as one model:

1. Weak total dispersion on the actual occupied bandwidth: nonlinear phase dynamics with controlled dispersive corrections.
2. Small $\beta_2$ with third- or higher-order dispersion dynamically important: derive the surviving balance and its physical readout.
3. Isolated, nearly phase-matched intermodal or polarization four-wave-mixing channels: derive a small coupled fluctuation model and its breakdown when more resonances enter or the pump depletes.

## Signal of hidden simplicity

Phase mismatch and walk-off may isolate a small set of coupled mode/frequency sectors even when the full field is broad. This is a hypothesis to test, not an observation establishing low rank. The archived crossover calculations have incomplete reduced-model coverage; that failure motivates explicit regime boundaries rather than interpolation between successful neighboring wavelengths.

## Literature state

All entries are **abstract only**, from a targeted intake. Their coverage of a particular reduced limit has not been audited.

- Tomaru, “Femtosecond pulse squeezing limited by stimulated Raman process in optical fibers,” DOI [10.1016/j.optcom.2006.12.030](https://doi.org/10.1016/j.optcom.2006.12.030). The publisher abstract covers positive, zero, and negative group-velocity dispersion with interferometric readout and Raman-related limitations. It establishes that comparing these regimes is not itself new. Publisher search record read; direct page access was blocked.
- Wright et al., [arXiv:1708.05324](https://arxiv.org/abs/1708.05324), DOI 10.1109/JSTQE.2017.2779749. Starting framework for multimode nonlinear propagation and examples in GRIN and step-index fibers.
- Ng et al., “Quantum noise dynamics in nonlinear pulse propagation,” [arXiv:2307.05464](https://arxiv.org/abs/2307.05464). Self-consistent Gaussian numerical evolution of broadband quantum correlations, including soliton and supercontinuum examples; useful methodological prior art.
- Drummond and Corney, [arXiv:quant-ph/9912095](https://arxiv.org/abs/quant-ph/9912095). Quantum fiber model with frequency-dependent Raman reservoirs.

## Sharpest statement of the gap

**Parked 2026-10-04.** The PI narrowed the multimode-squeezing set to four problems on 2026-10-04, and this one is not among them. If reactivated, the sharpest version is a single question: is the dip in best passive squeezing near the zero-dispersion wavelength real? In the archive the best F found with a passive filter was 0.65, 0.90, 0.97, 0.88 and 0.70 at 1200, 1250, 1300, 1350 and 1400 nm (`research_runs/2026-09-28_theory_campaign/REPORT.md`), but the 1300 nm search was restricted to weak power. The isolated intermodal four-wave-mixing channel would be a separate parametric problem.

The requested output is a physically realizable local reduction with a predictive crossover or scaling, not the statement that small carrier $\beta_2$ improves squeezing. It remains unknown from this intake which such reductions already exist. Review the cited papers and their four-wave-mixing, higher-order-dispersion, and quantum-noise references before novelty claims.

This card concerns propagating pulse correlations and count readout near a dispersion crossover. [P-011](P-011-generalized-dispersion-soliton-noise.md) concerns noise of generalized-dispersion solitary states; a special soliton limit can be shared without requiring this whole problem to be a soliton theory. [P-013](P-013-supercontinuum-noise-immune-observables.md) overlaps with selected robust observables but does not define this dispersion-resolved squeezing target.

## Regime and scaling targets

Use $d_{k,m}=\beta_{k,m}L/(k!T_0^k)$ directly. Bound dispersion phases over the broadened spectrum as well as at launch. Do not normalize by a vanishing $\beta_2$ or equate a zero carrier coefficient with negligible dispersion. Retain the first relevant higher-order terms and justify truncating the rest.

Seek scaling with carrier detuning from each relevant mode's dispersion zero, $\Phi_{\rm NL}$, $L$, bandwidth, $\Delta\beta_{abcd}L$, and spatial/polarization walk-off. Determine when a resonant pair is sufficient, how additional accessible modes alter the result, and where a bright-pulse linearization ceases to be reliable. Test self-steepening and the Raman response/bath in the same balance. Wavelength studies must use a realizable family of mode dispersions and overlaps; retuning every coefficient independently is not a laboratory scaling law.

## Conjectures

None registered. Dominance by an isolated resonant sector is a possible starting assumption to verify, not an accepted result.

## Oracle

Existing scalar/radial surrogate calculations are partial support only. Full vector, asymmetric-mode, and high-order-dispersion convergence capabilities need assessment in T-20261004-root-03. In addition to standard zero-length and linear checks, recover the dispersionless limit where controlled and the far-from-resonance suppression of the proposed channel. Check commutators and the Raman covariance of any eliminated sector.

Freeze a carrier-detuning or length prediction before full calculations. Compare both mean power and count noise, resolve growing correlation bandwidth, and vary temporal window, sampling, dispersion truncation, and spatial cutoff independently. A close total Fano factor with wrong power or wrong noise components is not sufficient evidence. Relax at least one assumption, for example polarization degeneracy, a two-channel truncation, or fixed launch phase.

## Lab test

Scan carrier wavelength across a measured dispersion zero at fixed stated pulse-energy and preparation conditions. Measure noise correlations between predicted spectral/modal sectors and their conversion by a fixed filter or scanned interferometer phase. A shift or splitting of a noise feature with controlled modal content is a sharper discriminator than a best-found minimum at one wavelength.

## Risks and must-reads

Single-mode parametric-amplifier theory may already solve a proposed sublimit. Broadening may invalidate a carrier-only expansion, and overlapping resonances may defeat a few-coordinate model. Optical Raman and low-frequency acoustic noise require different response models. Preserve a failed reduction as a regime boundary rather than increasing the waveform basis until agreement is obtained.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-04 | /root (gpt) | Created as priority-2 candidate; literature unaudited | PI request; located all-dispersion and quantum-propagation abstracts; independent review T-20261004-root-02 |
| 2026-10-04 | claude-interactive (claude; claude-opus-5-5), on PI instruction | candidate → parked | PI's four-problem set in chat, 2026-10-04; reason and reactivation question under the gap statement |
