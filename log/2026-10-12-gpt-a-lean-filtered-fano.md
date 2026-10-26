---
date: 2026-10-12
agent: gpt-a
model: gpt-6-astra
family: gpt
task: T-20261012-gpt-a-01
duration_min: 49
---

## Did

Assessed highlighted results 1 and 3 for problem
P-20261010-claude-interactive-01, using the narrowed wording in PRs #33 and #34.
Read the claim cards, permitted derivations and GPT-family dependency in draft
PR #28 through remote branch objects. Created and claimed the explore task on
its task branch; no other clone was edited.

The initial session began at 20:50 EDT. Server disconnections interrupted the
read-only research; the orchestrator resumed the session at 21:11 EDT with a
fresh time budget. The duration above is elapsed wall time including the
interruption, recorded when this log was written. Pushed the recovered draft
immediately and checkpointed the report and follow-up tasks during the session.

Used the codex-research skill and read-only Astra Max CLI subagents gpt-a.1
(finite algebra and sketches), gpt-a.2 (conservation and asymptotics), and gpt-a.3
(live library sources). Restarted their bounded synthesis after the connection
failure, reviewed their final reports, and incorporated corrections. The parent
spot-checked load-bearing declarations and source limitations. Reports and tool
logs stayed in this task's temporary directory; they are not experimental data.

## Found

The piecewise parity bound and loss-port attenuation correction are the strongest
first Lean target. The differentiated-invariant covariance identity is a useful
second target. Shear covariance and polarization reductions are practical next
steps. The hierarchy and binary certificates come from GPT-family work and would
receive a second verification layer, not new cross-family verification.

Precise statements expose the omitted parity sector-order case, the binary-only
last rung of the unmodified hierarchy, the distinction between exact continuum
subflows and aliased collocation momentum, the unproved passive even-sector
ordering, and the fixed-bath thermal expansion's second coefficient. The scaled
symplectic block law has an elementary conditional error enclosure; its physical
continuum hypotheses remain unproved. The weak-dispersion and small-distance
laws need localization and remainder estimates. The optimized Raman interpolation
remains empirical.

Mathlib supplies finite Hermitian/PSD and symplectic algebra, Rayleigh endpoints,
Fréchet derivatives, matrix exponentials, ODE estimates, Fourier isometries,
Gaussian measures and asymptotic notation. The report gives exact located names,
URLs and how they were checked. External min-max and oscillator code has relevant
support but distinct assumptions and version pins. Williamson and a completed
Itô formula were not located in the bounded searches; this is not a universal
absence claim.

## Changed

- Added the full assessment under `docs/lean/`, including the summary table,
  modelling ledger, precise propositions, error regimes, source survey, unchecked
  Lean sketches, lemma lists and dependency graphs.
- Added the exploration pointer and this log.
- Created tasks T-20261012-gpt-a-02 through -08 for the recommended proof targets
  and unresolved mathematical/data obligations.
- Marked only this newly created assessment task done. No problem, claim, result,
  generated file, solver code or existing task status was changed.

## Not verified

No Lean toolchain, elan, lake or Mathlib checkout was installed or downloaded.
No Lean statement was elaborated and no theorem was kernel-checked. Source
inspection does not establish compatible imports or absence of transitive axioms.
Every Lean block is explicitly an unchecked sketch.

No numerical experiment was performed. The report references existing registered
runs only and does not certify their floating-point values. Exact symbolic
constants and effort estimates are not experimental measurements. The assessment
does not prove discretization convergence, PDE existence/smoothness, quantum
model validity, asymptotic uniformity, or the empirical Raman prefactor.

The completed assessment passed:

- `~/agent-work/venv/bin/python scripts/validate.py` — `ok`.
- `~/agent-work/venv/bin/python scripts/check_generated.py origin/main` — `ok`.
- `git diff --check` — clean.

The generated-file check is also repeated on the final committed HEAD before
push, because it compares committed trees.

## Loose ends

- T-20261012-gpt-a-02: PI-approved Lean pin and parity/attenuation pilot.
- T-20261012-gpt-a-03: differentiated conservation, centroid units and the actual
  discrete map's invariant defect.
- T-20261012-gpt-a-04: shear spectrum, reservoir uncertainty, polarization and
  thermal-slice algebra.
- T-20261012-gpt-a-05: scaled-block limit/error, passive-sector ordering and
  continuum assumptions.
- T-20261012-gpt-a-06: weak-dispersion/small-distance localization remainders and
  symbolic quartic ground-state scaling.
- T-20261012-gpt-a-07: exact or interval covariance/PSD witnesses and discretization
  transfer for the GPT binary certificates.
- T-20261012-gpt-a-08: Raman variational bounds, optimizer changes and a valid
  joint finite-pulse thermal window.
