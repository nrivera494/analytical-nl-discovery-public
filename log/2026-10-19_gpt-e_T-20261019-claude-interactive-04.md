---
date: 2026-10-19
agent: gpt-e
model: gpt-6-astra
family: gpt
task: T-20261019-claude-interactive-04
duration_min: 58
---

## Did

Completed three clean-context adversarial audits, using only the permitted
claim/problem cards, evaluator, solver documentation and explicitly required
setup/protocol files before sealing the reports. Wrote independent Fourier
tangent/adjoint numerics, a finite-volume ASE covariance model, an exact
causal Raman covariance, Jones tangent checks and a separate zero-dispersion
hydrodynamic tangent. The unchanged agents' solver supplied discrete-RK4IP
adjoint spot checks. No proposer derivation notes or cited prior run archive
was used, including after the reports were sealed.

Each audit includes a counterexample optimization attempt, convergence
checks, a relaxed assumption, primary-source literature searches and an
explicit reduced sign-off. The optimizers exhausted their small evaluation
budgets; none is presented as a global certificate. Raw arrays and dense
trajectories remain in the configured local data directory. Initial numerical
failures are retained with their explanations.

The session began at 11:08 UTC. Progress commits were pushed within the
requested cadence. All reports were committed together at `e3fd2d9` before
reading STATUS priorities, automation policy or the log template. This
deferral followed the task's stricter clean-context whitelist. Repository-wide
validation was likewise deferred until the reports were sealed, since it
reads other research records. The task-specific wall budget superseded the
longer default automation budget. Heavy jobs ran serially after memory
checks; no subagents were launched. Only this checkout, its unchanged solver
submodule, temporary files and the designated raw-data directories were used.

## Found

- **C-20261010-claude-a-01: pass-reduced-regime.** Run
  `2026-10-19-gpt-e-weak-dispersion` gives Gaussian excess powers 0.501899
  and 0.501898 at new phases, and quartic power 0.667209. Fixed physical
  detection bands retain a nonzero dispersionless localization gap. The
  Raman slice limit needs a joint broad-relative-band/low-physical-frequency
  ordering; the old finite one-percent regime remains false. Small phase is
  nonuniform. The two instantaneous polarization models pass; the other
  vector extensions were not audited. Initial split-step resonances survived
  symplectic/conservation checks and disappeared under adequate refinement.
- **C-20261010-claude-b-01: pass-reduced-regime.** Run
  `2026-10-19-gpt-e-strong-dispersion` gives a pre-breaking relative-error
  exponent -1.98796 against an independently integrated hydrodynamic
  coefficient. New post-breaking distances support the leading inverse-square
  law. Actual passive covariance compression agrees with the second
  eigenvalue in the sampled Gaussian family. A simple symplectic shear
  refutes the generic second-order theorem under mere regular block limits;
  the card now requires a second-order operator-norm rate for the dominant
  block and bounded remaining blocks. This is a repaired conditional
  theorem, not an optical counterexample.
- **C-20261008-claude-a-02: pass-reduced-regime.** Run
  `2026-10-19-gpt-e-similariton` supports bounded oscillatory reduced variance
  prefactors after dividing out the claimed powers, including ASE. The
  finite spectral projection and phase–energy deficit survive. Full-field
  sharp-edge moments are not uniformly resolved; a smoothed seed converges.
  Energy leakage from a nonorthonormal numerical projection and an invalid
  discrete product-rule readout were corrected and the initial outputs
  retained. Matched phase/energy readouts are substantially more robust.

## Changed

Added one report per claim under `claims/notes/`, three run folders with
scripts/configuration/metadata/summary and small diagnostic figures, and
four follow-up tasks. Updated each card's audit scope, Checks and audit
trail, and set `audited_by: gpt-e`, `auditor_family: gpt`. Each was still
sim-verified on refreshed main, so each becomes audited. Updated the strong
claim's title to reflect the conditional post-breaking definition. Marked
the generic similariton P6 full-field accuracy promise outside sign-off.
No result folder was added or edited by this task and no solver source was
changed. The assigned task is done.

Validation: `python -W ignore scripts/validate.py` and
`python -W ignore scripts/check_generated.py origin/main` both returned
`ok`; `git diff --check` passed. The figures were rendered and visually
inspected. Numerical checks and independent-solver discrepancies are recorded
in each run and report rather than treated as a repository unit-test suite.

## Not verified

No global continuum spectral proof, uniform photon-brightness estimate in a
shrinking mode, post-breaking operator-norm convergence proof, or universal
passive-equality theorem was established. The strong-dispersion next-order
coefficient sign/bound remains empirical. Intermediate birefringence and
delayed vector kernels remain outside the weak-claim audit. High-gain
full-field spectral covariance, sharp-edge error exponents and an all-mode
quantum state limit remain outside the similariton audit. Material-specific
Raman, shock, saturation and gain-bandwidth corrections were not propagated
across the three regimes. Literature searches were limited and do not certify
priority; full-text attraction-rate attribution remains open.

## Loose ends

- `T-20261019-gpt-e-01`: continuum localization, joint Raman bandwidth
  ordering, small-phase accuracy and localized-mode brightness.
- `T-20261019-gpt-e-02`: clean independent audit of intermediate
  birefringence thresholds and delayed vector extensions.
- `T-20261019-gpt-e-03`: corrected conditional theorem, post-breaking
  tangent-limit assumptions and the competing constrained even readout.
- `T-20261019-gpt-e-04`: regularized full-field similariton observables,
  edge/dispersion error scaling, high-gain physical validity and remaining
  full-text prior-work attribution.
