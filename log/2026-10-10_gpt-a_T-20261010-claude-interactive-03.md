---
date: 2026-10-10
agent: gpt-a
model: gpt-6-astra
family: gpt
task: T-20261010-claude-interactive-03
duration_min: 0
---

## Did

Started at 10:32:55 EDT, with a 240-minute budget. Synchronized the dedicated
clone and private solver submodule, claimed the assigned task, and stacked
the branch on PR #27. Read the repository rules, solver guidance and run
storage policy. The PI's explicit round-3 assignment authorizes this work
while the problem remains candidate; the literature audit is still pending.
This session does not promote or independently verify a claim.

Proved the readout hierarchy with brightness, vacuum-ancilla and weighted
counting qualifications. Derived a binary eigenvector mismatch certificate
and a homogeneous binary moment/RLT relaxation. Started a full covariance
evaluator using the existing discrete adjoint, with a task-local no-shock
adapter and the prescribed fetched coth Raman spectrum.

## Found

Initial covariance assembly had a Julia closure-scope race: variables also
assigned later in the enclosing function were shared across worker calls.
The Kerr eigenvalue gate detected duplicated covariance columns. Explicit
local bindings fixed it; both failed outputs remain in the run's raw data.
The weak-power, Kerr and discrete-notebook contraction gates then passed;
all values are registered in run `2026-10-10-gpt-a-readout-reference`.

The full-grid binary relaxation can be much tighter than the amplitude
eigenvalue. However, some formal binary optima select essentially dark
spectral bins. Gaussian quadratic count noise invalidates treating those
linearized values as measurable upper values. A separate counting
diagnostic and step/grid/window tests are in progress. A matrix-free
covariance action reproduces dense covariance products to floating-point
accuracy and makes these refinements affordable. Further findings will be
filled in after the reference sweep.

## Changed

Added the proof note, covariance and bound evaluators, and run registration.
No problem card, other agent's task, generated file, solver source or solver
pin was edited.

## Not verified

The reference sweep and convergence are in progress. No novelty is claimed
for the readout reduction or for applying standard moment relaxations.

## Loose ends

To be finalized before stopping.

## Proposed card changes

- One-port passive counting reaches only directions with nonzero coherent
  overlap; a dark minimizer is an asymptotic infimum requiring a brightness
  limit. Weighted bright difference channels can reach dark-to-one-port
  directions without that particular singularity.
- State whether vacuum ancillary modes are included. With them the passive
  infimum is capped by the vacuum variance.
- Specify the hardware meaning of passive: the displayed limit permits
  arbitrary photon-number-preserving mode unitaries. A stationary
  frequency-preserving network with resolved spectral counting has one
  phase-orthogonality constraint per frequency block; in a scalar mode it
  reaches only the generalized amplitude-counting limit.
- Real weighted counting is normalized by its weighted shot-noise variance,
  not by its potentially signed or zero mean count.
- Interlacing by itself does not justify saying the two lowest variances are
  close. A generic Weyl, Temple or conjugate-variance bound cannot improve an
  already known exact eigenvalue of the same readout subspace.
- Full covariance reconstruction costs a basis of adjoints, not one scalar
  adjoint contraction. Matrix-free eigenvalue methods may be cheaper.
- A linearized optimum over unrestricted filters need not be a measurable
  counting value: it may transmit a negligible coherent photon number.
  Report brightness and the quadratic Gaussian count correction, or impose
  a stated minimum brightness. Noise propagation also needs a step-size
  convergence check beyond convergence of the classical pulse.

## Literature

See the proof note for searches, identifiers and access levels. This lane
covers general Gaussian readouts and binary optimization, not the three
propagation-regime literature reviews.
