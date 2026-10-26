---
date: 2026-10-13
agent: gpt-a
model: gpt-6-astra
family: gpt
task: T-20261012-gpt-a-02
duration_min: 17
---

## Did

Claimed the assigned task in the dedicated `lean-pilot` clone and stacked its
task branch on PR #37 using the PI's setup commands. Read AGENTS.md, STATUS.md,
automation policy, the assessment's parity sections, the claim card from PR #29,
and the candidate-3/parity sections of PR #34. Used the provided Lean installation,
Mathlib pin, and cache without reinstalling or updating them. No other clone or
conversation history was accessed; no subagents were used.

Implemented the piecewise parity proof, Rayleigh and physical attenuation
corollaries, binary denominator identity, and exact rational scope counterexamples.
Built the project cleanly and checked all public theorem axiom closures through
the root import. The pilot note records the successful build and main axiom output.

## Found

The corrected finite-bin parity and attenuation implications compile. All 35
theorems depend only on `propext`, `Classical.choice`, and `Quot.sound`; there are
no proof holes or project axioms. The variational minimum corollary was cheap;
constructing and identifying the sector eigenvalues is a separate follow-up.
The exact two-bin counterexamples establish the sector-order and partial-mask
scope errors. Their rational constants are formal identities, not measurements.

The initial build exposed only ordinary elaboration issues and then Mathlib's
module/header style warnings. These were resolved by using Lean's module system
and disabling only the Mathlib-specific copyright/license-header template check
for this repository; kernel checking and the remaining standard linters stay on.

## Changed

Added the pinned `formal/` project, with `AnalyticalNL/Parity.lean`, a public root
import, complete theorem-to-claim map, build instructions, manifest, toolchain,
Lake configuration, and cache exclusion. Removed the unused generated template
`Basic.lean`. Added `docs/lean/2026-10-13-gpt-a-parity-pilot.md` and follow-up tasks
-09, -10, -11. No claim, problem, generated registry, result, or solver was edited.

Marked T-20261012-gpt-a-02 done after the proofs, documentation, public-import
axiom checks, and repository checks passed. The checked implementation was
committed and pushed as `83818d6`; a final task/log update follows on the same
branch. `validate.py` and `check_generated.py origin/main` both report `ok`.

## Not verified

The optical interpretation of the covariance, actual parity symmetry of the
dynamics, linearized counting validity, and loss-port vacuum law remain outside
the finite proof. No floating-point input, simulation, continuum approximation,
empirical scaling, Kerr realization of the rational stand-in, or claim promotion
is certified. The `IsLeast` corollary assumes sector minima; it does not construct
an eigensystem or prove their existence. No external literature claim is made.

## Loose ends

- T-20261012-gpt-a-09: Lean CI and automatic axiom enforcement.
- T-20261012-gpt-a-10: spectral bridge from sector Rayleigh minima to eigenvalues.
- T-20261012-gpt-a-11: card scope corrections after PI review.
- Existing T-20261012-gpt-a-03 and -04: next centroid and shear/polarization targets.
- Existing T-20261012-gpt-a-07: covariance certification and transfer errors.
