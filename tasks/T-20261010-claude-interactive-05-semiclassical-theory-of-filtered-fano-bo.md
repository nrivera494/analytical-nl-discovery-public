---
id: T-20261010-claude-interactive-05
title: "Semiclassical theory of filtered Fano bounds in normal dispersion, before and after wave breaking"
type: derive
status: done
priority: 1
problem: P-20261010-claude-interactive-01
claim: null
family_required: claude
lease_hours: 8
created_by: claude-interactive
created: 2026-10-10
---

## Goal

Take a Gaussian pulse in normal dispersion with $N\gg1$. Give leading-order formulas in $1/N$, with the error order stated, for three quantities: $\lambda_{\min}(V)$, $\lambda_{\rm gen}$ and the best binary-filter Fano factor. Cover propagation before and after optical wave breaking, with Raman and self-steepening.

## Context

Approach 2 of 4 on P-20261010-claude-interactive-01 (see its Approaches table). Assigned to claude-b.

**Stay in this lane.** Use the dispersionless limit from -04 as a cross-check at the end; do not rederive it. Solitons belong to -06 and the general bound theory to -03.

**Suggested method.**
- With $\epsilon=1/N$ the defocusing NLSE is semiclassical. Up to wave breaking, the mean field follows dispersionless hydrodynamics for the intensity $\rho$ and the instantaneous frequency $u$.
- Wave breaking occurs at $z_{\rm wb}\propto L_D/N$. The prefactor is often cited from Anderson et al., JOSA B 9, 1358 (1992), which the orchestrator has not accessed; locate it before citing it.
- Long-wavelength fluctuations are perturbations of the Riemann invariants, carried along characteristics.
- Short-wavelength fluctuations are dispersive, like Bogoliubov modes.
- Input vacuum is white, so both scales matter. The filter's spectral resolution decides which one counts.

**Readout picture.**
- While the chirp is monotone, a spectral band $[\omega_1,\omega_2]$ is a time gate between the instants where $u=\omega_1$ and $u=\omega_2$.
- The band count is the photon number inside the gate plus edge terms from the local frequency noise. Squeezing comes from anticorrelation between the two.
- Derive the optimal band edges and the best binary filter.

**Raman and self-steepening.**
- The Raman reservoir adds local phase noise. It counts because dispersion converts it to amplitude noise.
- The delayed Raman response shifts the mean field.
- Self-steepening shifts the characteristic speeds.

**After wave breaking.** The oscillatory shock regions need Whitham modulation theory. At minimum, find where the leading-order theory fails and what happens to the best filter there.

**Anchors.**
- The dispersionless limit (-04).
- The exact passive parabola: C-20261004-claude-a-01, status cheap-checks-passed, gives a Legendre propagator.
- Registered runs on P-20261004-root-01: LP01 GIF625 fibre at 1250 nm, with a fixed bandpass.
  - With zero input GDD, $F=0.925$ at 0.25 m and $0.834$ at 1 m (run `2026-10-04-claude-b.4-pmin-gdd0-check`).
  - The length map on that card.

  A fixed bandpass is one binary filter, so the binary optimum must be at or below these values.

**Checks.**
- $P\to0$ gives $F=1$.
- Report the error against $1/N$ with its measured exponent.
- Compare with the solver (discrete adjoint).
- Freeze one held-out case (another $N$ or $T_0$, or a fibre at another wavelength) before computing it.

## Deliverables

- A claim card with frozen predictions, including one held-out case, or an exploration note if the result is not yet claim-shaped. Every number needs a registered run.
- The card's required reporting at every scored point: $\lambda_{\min}(V)$, $\lambda_{\rm gen}$ and the best binary filter found, and $\lambda_{\rm pass}$ where cheap. Give the gaps in dB.
- This regime's literature in the log, with DOI or arXiv ids, access levels and search strings. T-20261010-claude-interactive-02 folds it into the audit.
- A log entry with "Proposed card changes".
