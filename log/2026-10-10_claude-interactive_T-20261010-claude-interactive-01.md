---
date: 2026-10-10
agent: claude-interactive
model: claude-opus-5-5
family: claude
task: T-20261010-claude-interactive-01
duration_min: 60
---

## Did

- Created P-20261010-claude-interactive-01 on the PI's instruction: a fast, tight lower bound on the Fano factor reachable by spectral filtering (mode-selective or not), and by other readouts, in fibre with general dispersion, self-steepening, polarization, several modes and Raman.
- Recorded a starting structure in linearized theory: $\lambda_{\min}(V)\le\lambda_{\rm gen}\le\min_TF[T]$, using $T_i^2=T_i$ for binary filters. Also a closed-form dispersionless Kerr anchor and the computed LP01 cases where Raman sets the floor.
- Created T-20261010-claude-interactive-02 (literature audit) and -03 (reference bounds for single-mode fibre).

## Found

Nothing new; the card collects structure and starting points.

## Changed

- New: `problems/P-20261010-claude-interactive-01-fast-lower-bounds-filtered-fano.md`.
- Tasks T-20261010-claude-interactive-01 (done), -02 and -03 (open).

## Not verified

- The bound chain and the Kerr anchor are standard linearized-theory relations stated without a check in this setting. T-20261010-claude-interactive-03 checks them numerically.
- The literature is unaudited. Entries carry the access levels recorded on other cards.

## Revision after PI feedback (same day)

The PI's decisions are recorded on the card.
- The card supersedes P-20261004-root-04. Root-04 stays parked with a pointer, and its readout subtargets move to rung 5.
- The order of work is approved.
- Bounds must beat $\lambda_{\min}(V)$, but its position is always reported.
- Four agents for four hours.

Changes:
- Card priority 2 → 1.
- A readout hierarchy added to the card as a statement to prove: $\lambda_{\min}(V)\le\lambda_{\rm pass}\le\lambda_{\rm gen}\le\min_TF$, where $\lambda_{\rm pass}$ is the passive-linear-optics plus counting limit.
- A required-reporting rule.
- An Approaches section.

The orchestrator checked the hierarchy, including that one port of a suitable passive network reaches $\lambda_{\rm pass}$, on one random six-mode mixed covariance in a scratch script. This is not a registered run, and the card states no numbers from it.

Tasks after the revision:

| Task | Lane | Family |
|---|---|---|
| -03, rewritten | Hierarchy proof, binary-specific bounds above $\lambda_{\rm gen}$, certificates and the reference table | gpt |
| -04 | Exact dispersionless theory | claude |
| -05 | Semiclassical normal dispersion | claude |
| -06 | Soliton perturbation theory with Raman | gpt |

The card's statement that spectral filtering *needs* dispersion was unproven and is softened: the filter itself mixes differently chirped instants.

## Loose ends

- T-20261010-claude-interactive-02 to -06.
