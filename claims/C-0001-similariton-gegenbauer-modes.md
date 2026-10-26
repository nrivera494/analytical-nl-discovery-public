---
id: C-0001
problem: P-001
title: "Fluctuation modes of a parabolic pulse are Gegenbauer polynomials with spectrum 2n(n+1)"
type: noise-formula
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
superseded_by: C-20261004-claude-a-01
solver_commit: null
result: null
---

## Statement

For a parabolic pulse in normal dispersion in the hydrodynamic limit (effective semiclassical parameter $\varepsilon\to0$), the density-fluctuation eigenmodes in the scaled time coordinate $\xi = t/T(z)$ are polynomials (Gegenbauer $C^{-1/2}_{n+1}(\xi)$, equivalently Legendre for the density), with squared scaled frequencies $\gamma_n = 2n(n+1)$. The right singular vectors of the linearized propagator converge to these modes as $\varepsilon\to0$.

## Regime

$\varepsilon \ll 1$, before wave breaking, Raman and gain-bandwidth effects neglected. Predicted eigenvalue error $O(\varepsilon^{p})$ with $p$ between $1/3$ (proved bound, Gallo–Pelinovsky) and $2$ (their numerics). Bounds on dimensionless groups to be made explicit by the first agent to work on this claim.

## Assumptions

Scalar 1D NLSE; instantaneous Kerr; second-order dispersion only; for the amplifier case, constant frequency-independent gain; boundary layers at $|\xi|\to1$ neglected.

## Predictions

1. Overlap of the $n$-th singular vector with the $n$-th predicted mode approaches 1 as $\varepsilon\to0$, for $n\le 5$.
2. Ratios of mode frequencies $\sqrt{\gamma_n/\gamma_1} = \sqrt{n(n+1)/2}$.
3. Held-out: same statements for a passively expanding parabolic pulse with no gain.

## Derivation

By analogy with Stringari's hydrodynamic modes of a 1D Thomas–Fermi condensate; frozen-$\varepsilon$ spectrum from Gallo & Pelinovsky, arXiv:0806.3516. No derivation for the time-dependent, gain-driven case exists yet. This is a hypothesis.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Novelty search | Boscolo–Turitsyn Gegenbauer paper not accessed | claude | | 2026-10-01 |
| Novelty search (update) | [BT] is a 2007 private communication cited on p. 43 of arXiv:0806.3516, not a paper. The PI treats it as unobtainable; it does not close P-001. Gallo–Pelinovsky's Gegenbauer result is for a Thomas–Fermi model problem, not an evolving similariton (see P-001). The derivation basis above needs revising | gpt (finding, T-0001); PI (disposition) | | 2026-10-02 |
| Derivation (T-20261004-claude-interactive-05) | Passive case derived in the hydrodynamic limit. The propagator is exactly block-diagonal in Legendre $P_l(\xi)$ for the (density, phase) pair, with $\mathrm{sech}^2$ (Pöschl–Teller) time dependence. The frozen ratios $\sqrt{l(l+1)/2}$ of prediction 2 are the instantaneous generator's, but the passive pulse never oscillates at them. Prediction 1 (singular vectors converge to Gegenbauer modes) is not supported: the vacuum metric mixes Legendre blocks. Superseded by C-20261004-claude-a-01 | claude (claude-a) | 2026-10-04-claude-a-c01-cheap-checks | 2026-10-04 |

## Outcome

Withdrawn 2026-10-04 by claude-a under T-20261004-claude-interactive-05; superseded by `C-20261004-claude-a-01`. What was learned:

- The Gegenbauer/Legendre structure survives, but in a different role. In comoving variables the passive (and frozen) linearized dynamics is exactly block-diagonal in Legendre $P_l$ for the (density, phase) pair. The displacement fields are $P_l'$, the Gegenbauer $C^{3/2}_{l-1}$, and $C^{-1/2}_{l+1}=(1-\xi^2)P_l'/l(l+1)$ is the mass displacement $\bar\rho u$ (up to $1/a$). The separation constant is $l(l+1)$, so the frozen ratios $\sqrt{l(l+1)/2}$ (prediction 2) belong to the instantaneous generator. The finite-distance blocks are Legendre functions $P_l,Q_l$ of $\tanh(\varepsilon\Phi_{NL})$, not oscillations at those frequencies.
- The separation itself is a special case of Fedichev & Fischer, PRA 69, 033602 (2004), arXiv:cond-mat/0303063, Eqs. (22)–(25).
- Prediction 1 conflated frozen eigenmodes with finite-distance singular vectors. In the field (vacuum) metric the phase covariance is $\propto1/(1-\xi^2)$, which mixes blocks, so neither the singular vectors nor the covariance eigenmodes are Legendre modes. The rewrite predicts the covariance of one specified measurement mode (matched local oscillator) instead.
- The amplifier case (constant gain) was C-0001's main case, and its held-out prediction 3 was the passive case treated in the rewrite. The amplifier case is not covered by the rewrite. It needs the gain Langevin noise, and remains open under P-001.
