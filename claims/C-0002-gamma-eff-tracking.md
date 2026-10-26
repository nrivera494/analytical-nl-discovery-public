---
id: C-0002
problem: P-002
title: "Multimode soliton energy–duration product tracks an effective nonlinearity set by relaxing modal occupations"
type: reduced-model
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

A highly multimode temporal soliton in GRIN fiber obeys $E(z)\,\tau(z) = 2|\beta_2|/\gamma_{\rm eff}(z)$ with $\gamma_{\rm eff}(z) = \gamma\sum_{pq} n_p(z)n_q(z)S_{pq}$, where $n_p$ are normalized modal occupations that relax toward a Rayleigh–Jeans distribution at fixed power and internal energy on a length long compared with the soliton period.

## Regime

Modal relaxation length much longer than the soliton period; Raman shift over the relaxation length small compared with the bandwidth. To be made explicit.

## Assumptions

Scalar field; ideal parabolic index; no linear mode coupling; Raman neglected in the first test; intermodal group-velocity differences within the trapping range.

## Predictions

1. $E\tau\gamma_{\rm eff}/(2|\beta_2|) = 1 \pm$ a tolerance that shrinks with the ratio of soliton period to relaxation length.
2. Limits: equal occupations give the Manakov-averaged coefficient; all power in the fundamental mode gives the single-mode soliton.
3. Held-out: a step in launch conditions that changes the initial modal distribution at fixed energy changes $\tau(z)$ as predicted from the measured $n_p(z)$.

## Derivation

None yet. Hypothesis motivated by the effective-waist picture of walk-off solitons (Zitelli et al. 2021). The earlier mention of a simulated 120-mode soliton is removed: no source or run id was ever supplied (AGENTS.md rule 3), and P-002 removed the same anecdote.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Consistency with the audited problem card P-002 and with the review of P-20261004-root-03 | **Fails as stated.** (1) The occupation-only $\gamma_{\rm eff}$ closure is the assumption P-002 says must be tested, not assumed; relative phases and mode-dependent carrier frequencies may be indispensable. (2) For the ideal parabolic overlap matrix, no co-propagating equal-width sech multimode soliton exists at finite fractions, even with frozen occupations (equal widths would need $C_{11}p_1+C_{12}p_2=C_{21}p_1+C_{22}p_2$); $E\tau=2|\beta_2|/\gamma_{\rm eff}$ is a variational estimate, not an identity. (3) Modal walk-off is equivalent to a modal carrier-frequency offset, which the claim's prediction omits. (4) The regime is still 'to be made explicit' (rule 6) | claude (claude-b, proposing family) | none (algebraic) | 2026-10-04 |

## Outcome

**Withdrawn on 2026-10-04 by the proposing family** (claude-b, T-20261002-claude-interactive-04). It is superseded by:
- the audited target of P-002: a controlled closure for evolving modal content, with phases and carrier frequencies;
- the round-1 tasks that test it from the bottom up: T-20261004-claude-interactive-02 (first-order capture law, gpt-a) and T-20261004-claude-interactive-07 (walk-off boundary beyond first order, gpt-a);
- the structural facts recorded in the review of P-20261004-root-03 (PR #7): the Manakov limit, the walk-off gauge, and the absence of an exact common-sech soliton for the GRIN overlap matrix.

A future claim about modal relaxation inside a multimode soliton should start from those. The claim is kept, not deleted (AGENTS.md rule 7).
