---
date: 2026-10-08
agent: claude-interactive
model: claude-opus-5-5
family: claude
task: T-20261008-claude-interactive-01
duration_min: 40
---

## Did

- Retargeted P-001 to the amplifier similariton on the PI's instruction (2026-10-08): noise with gain and spontaneous emission, and whether the similariton is an attractor or needs a basin condition. The passive claim stays as the $g\to0$ limit.
- Added to P-001 the orchestrator's dispersionless sketch from the 2026-10-06 chat, marked unverified: invariant parabolic family, width ODE with a Lyapunov function, Legendre-block equation for any parabolic background, decay rates on the asymptote, and the implied phase-sensitive amplification of shape modes.
- Recorded the PI's directions on P-20261004-claude-interactive-02 (Raman- and gain-driven covariance first; Manakov/vector not equivalent without a quantitative comparison) and on P-20261004-root-03 (Find item 4: an inequality between filtered Manakov/LP01 and GRIN soliton noise).
- Wrote `docs/plan-2026-10-round2.md` with the four agent assignments and the round's rules.

## Found

- Quick literature search (strings in P-001's gap section): no analytical single-pass noise theory of the amplifier similariton with spontaneous emission; similariton-laser noise computed numerically (Zweck & Menyuk, DOI:10.1364/JOSAB.35.001200, abstract only); no published convergence spectrum or Lyapunov argument located. One possibly relevant paper could not be accessed and is listed as a must-read.

## Changed

`problems/P-001-noise-around-nonsoliton-attractors.md`, `problems/P-20261004-claude-interactive-02-multimode-soliton-collective-noise.md`, `problems/P-20261004-root-03-anomalous-dispersion-multimode-squeezing.md`, `docs/plan-2026-10-round2.md`; task T-20261008-claude-interactive-01 (done).

## Not verified

- Every statement in the P-001 orchestrator sketch. It is a leading-order hydrodynamic derivation done in chat, without numerics or a second family. gpt-a checks it under T-20261008-gpt-a-01.
- The literature search was quick and does not establish novelty.

## Loose ends

- The four round-2 tasks are created by the agents themselves (see the plan).
