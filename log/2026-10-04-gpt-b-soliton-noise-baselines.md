---
date: 2026-10-04
agent: gpt-b
model: gpt-6-astra
family: gpt
task: T-20261004-claude-interactive-08
duration_min: 40
---

## Did

Claimed the assigned scalar baseline task after committing and opening the
independent literature review (T-20261004-claude-interactive-01, PR #6).
Used the pinned solver's RK4IP step, complete field perturbations, dual
collective-coordinate projections, and existing noise samplers. Compared
an independent Fourier-collocation Bogoliubov exponential and split-step
propagation. Ran 2048 trajectories per primary source and a same-noise
coordinate comparison at separate parameters. No solver code changed.

Read the accessible Corney–Drummond full text and the normalization and
reservoir sections of Drummond–Corney I. Access levels and exact identifiers
are in the exploration note. No parallel Claude review branch or PR was
read during the independent literature task.

## Found

Run `2026-10-04-gpt-b-soliton-baselines` reproduces the leading vacuum
covariances, gain cubic timing term and explicit-Wigner Raman jitter,
including coefficients. The long-pulse mean Raman shift approaches the
inverse-fourth-power duration law; its error decreases quadratically with
inverse pulse duration. Window, resolution, step and probe-size checks,
plus the second integration methods, support these conclusions.

The default Raman spectrum, when given the correct response, supplies half
the Wigner zero-point diffusion. The sampler itself agrees with its input
spectrum; an explicit Wigner spectrum passes. The legacy input-noise default
is also not the half-photon Wigner convention, so the run explicitly uses
`noise_scale=0.5`. These are source-convention checks, not fitted corrections.

Finite stochastic ensembles give less reliable powers after subtraction of
lower-order terms. Run `2026-10-04-gpt-b-noise-pathwise` shows the field and
same-noise reduced model agree even when both fitted powers differ from the
ensemble power. All such fits remain in the summaries. The full delayed
Raman ensemble is consistent in final variance with the leading stationary
theory, but an exact cubic law at long distances is not established.

## Changed

- Added the Julia projection/propagation evaluator and independent Python
  analysis under `evaluator/`.
- Added both registered run folders, configurations, metadata, summary numbers
  and a small figure; arrays and logs remain in local raw storage.
- Completed the exploration note, added the problem audit row, and marked
  T-20261004-claude-interactive-08 done.
- Created T-20261004-gpt-b-02. The task generator initially reused suffix 01
  because the literature task exists on another branch; advanced it to 02
  without changing that earlier task.
- Preserved the initial Julia entry-point parse-error log. That attempt ran
  no propagation. Added a guard preventing raw-array overwrites.

Both repository validation commands pass. The dual-mode and overwrite-guard
smoke checks pass. The solver CPU suite was not rerun because the solver
tree and pin are unchanged. No generated files were edited, no branch was
merged, and task T-20261004-claude-interactive-09 was not started.

## Not verified

No claim was independently sim-verified or promoted. The full multimode
problem, uncompensated net gain, gain saturation, all automatic facade
kernel/discretization choices, combined optical shock and Raman noise,
multi-phonon silica response and GAWBS are outside these scalar checks.
The stock Raman normalization finding needs independent-family review
before changing shared solver behavior. Main-run noise formulas are leading
weak-noise results; the ensembles do not establish exact quantum evolution.

## Loose ends

- T-20261004-gpt-b-02: independent audit of the Raman Wigner normalization,
  followed by a minimal opt-in solver repair, tests and separate pin bump if
  confirmed. Existing explicit-source interfaces already support this task.
- T-20261004-gpt-b-01 (on PR #6): remaining primary-text access from the
  literature task. No duplicate task was created here.
- T-20261004-claude-interactive-09 remains unstarted under the session's
  explicit block; no replacement derivation task was created.
