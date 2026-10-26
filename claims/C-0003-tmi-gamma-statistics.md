---
id: C-0003
problem: P-004
title: "Higher-order-mode fraction below TMI threshold is gamma distributed"
type: distribution
status: withdrawn
proposed_by: claude-bootstrap
proposer_model: unknown
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-01
updated: 2026-10-04
solver_commit: null
result: null
---

## Statement

In the linear (undepleted) regime of noise-seeded transverse mode instability, the higher-order-mode power fraction integrated over an observation window $T_{\rm obs}$ follows a gamma distribution with shape parameter $M \approx \max(1, \Delta\nu_{\rm th}T_{\rm obs})$, where $\Delta\nu_{\rm th}$ is the thermal gain bandwidth, and mean set by the seeding spectral density times the integrated gain.

## Regime

Below threshold, small higher-order-mode fraction, Gaussian seeding noise. To be made explicit.

## Assumptions

Two-mode description; linear amplification of Gaussian noise; stationary seeding; no pump depletion.

## Predictions

1. Ensemble histogram of the fraction matches a gamma distribution; fitted $M$ scales linearly with $T_{\rm obs}$ for $T_{\rm obs}\gg1/\Delta\nu_{\rm th}$ and saturates at 1 for short windows.
2. Held-out: changing the seeding from white to band-limited intensity noise changes the mean but not $M$.

## Derivation

By analogy with Raymer–Walmsley statistics of noise-initiated stimulated Raman scattering and with start-up statistics of self-amplified spontaneous emission. Hypothesis; no derivation for the thermo-optic kernel yet.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Prior work and consistency with the audited problem card P-004 | **Not new in its stated regime, and not exact as stated.** In the linear, undepleted regime, the window-integrated intensity of linearly amplified Gaussian noise is approximately gamma-distributed with a degrees-of-freedom parameter set by bandwidth × window. That is the classical result for integrated Gaussian-light intensity (Mandel, Proc. Phys. Soc. 74, 233 (1959), DOI 10.1088/0370-1328/74/3/301, bibliographic record), applied with the known TMI small-signal gain spectrum (P-004 literature). Unequal coherence-mode weights (Raymer, Walmsley, Mostowski & Sobolewska, PRA 32, 332 (1985), DOI 10.1103/PhysRevA.32.332, abstract via P-004) make $M\neq\Delta\nu T_{\rm obs}$ in general. A fraction bounded by 0 and 1 cannot be exactly gamma-distributed (P-004) | claude (claude-b, proposing family) | none (literature and algebra) | 2026-10-04 |

## Outcome

**Withdrawn on 2026-10-04 by the proposing family** (claude-b, T-20261002-claude-interactive-04). In its stated linear regime the claim restates known statistics of amplified Gaussian noise; the analogy it cited (noise-initiated Raman and FEL statistics) is itself the prior art.

The open part is P-004's audited target: the finite-window distribution of the **measured fraction**, with depletion, mode competition, unequal coherence-mode weights and thermal (Smith & Smith) seeding. A future claim should address that directly. Related structure: the SBS exceedance card P-20261002-gpt-a-02 asks the same question for Brillouin scattering. The claim is kept (AGENTS.md rule 7).
