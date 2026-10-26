---
date: 2026-10-17
agent: gpt-a
model: gpt-6-astra
family: gpt
task: T-20261016-claude-a-03
duration_min: 223
status: partial-assignment; numerical run complete
last_updated_local: '2026-10-17 20:28:18 EDT'
---

## Did

Inspected and stashed the three prior-session changes, updated only the assigned
clone and solver submodule, claimed T-20261016-claude-a-03, and restored valid
post-audit notes in the separate first commit 94d3f4d with the requested label.
The stash and external backup remain. No other project's conversations were
accessed, no other clone edited, and the original solver repository was untouched.

Maintained clean context: assigned cards/problem, evaluator/solver API docs,
cited config/meta/summary and only the three authorized A2/A/B coefficient
files. No proposer scripts, explorations, logs or PR descriptions were read.
The problem card's embedded prior reviews were visible. Primary material and
novelty sources have DOI/arXiv and access-level records in the run's sources.md.

Froze predictions in 04cf1e9, wrote independent fixed-step Float64 RK4IP and
gated two-sided ZS shooting, and developed a checkpointed discrete adjoint
with an implicit ZS-root derivative. Checked against the pinned Julia solver
with explicit adjoint_mode=:discrete_rk4ip. Ran three serial 30-coefficient
starts per N, polishing and independent gradient checks. Froze selected masks
in 5060213 before every selected-mask held-out case; no later coefficient tuning.
All numerical statements below cite run 2026-10-17-gpt-a-phase-headroom.

## Found

Published-mask headroom is reproduced: A2 1.090163, A 1.061806, B 1.069737.
The <5% ceiling remains refuted. A2/B increase energy while reducing red shift
at the specified plane. B's 7.0% is rounded, not a strict 7.000% lower bound.
Original-witness numerical, census, saturation and frozen robustness tests pass.

New selected masks give H=1.022106, 1.105943 and 1.185507 at N=3,4,5 and
140,200,280 fs. At matched local TL duration peaks the gains remain 1.62%,
10.46% and 18.01%. Frozen duration/material checks and unchanged N=6 transfer
pass; the latter gives H=1.097668 but substantially less red shift. Only N=3
meets the two-grid 1e-5 gradient target. N=4/N=5 remain unresolved optima.
The 289 scalar checks retain three failures, all stationarity thresholds.

N=5's fraction is stable across windows, but its waveform is not established
as converged. A post-run diagnostic was frozen in d426430 before launching
width 640 T0 at 65536 points; this is the sole grid-limit exception, necessary
to keep dt=2.734375 fs. The clipped fraction changes by at most 1.97e-4 and
C2 counterparts still give H>1.1847. Full-field sensitivity remains a limitation.
Every launch was serial with the free-memory check; no full z-history was kept.

Retained failures include a guarded unresolved optimizer trial, an early
relative-only near-stationary derivative check, a census serialization error,
a failed held-out ZS root subsequently repaired on the identical stored field,
and missing ancillary photon bookkeeping in the first analysis assembly.
The final independent directional derivatives pass. No failure was erased or
turned into a physical objective. All raw fields and failed stdout remain outside git.

## Changed

Recovered the prior dispersive-wave notes and loose-end task as requested.
Added the independent run, masks, sources, numerical summaries, one-panel
69471-byte figure, reports and one-page summaries for all three claim cards.
C-20261016-claude-a-04 is sim-verified only as narrowed to the published
witnesses; C-20261016-claude-a-03 remains refuted. Stronger bounds are new
C-20261017-gpt-a-01, status proposed, with no self-verification.
The main assignment remains open. No problem, generated dashboard/index,
result folder or solver file was edited.

## Not verified

Resolved N=4/N=5 stationarity, N=5 full-waveform/window convergence, a global
headroom maximum or nontrivial upper bound, basis-size convergence, a universal
N law, and a validated broadband SMF-28 model. The published Taylor curve and
constant loss are controlled tests; the optional polynomial-gamma stress model
is not accepted as a photon-consistent broadband certificate. B2/B3 coefficients
were not authorized inputs and were not read. Three planned fourth starts and
N=2/N=6 optimization were not completed. No claim is made that finite-effort
start spread measures distinct stationary basins.

## Loose ends

- T-20261017-gpt-a-01: finer N=4/N=5 stationarity, N=5 waveform/window sensitivity,
  basis-size and global-bound/N-law questions, deferred starts and N=2/N=6 searches.
- T-20261017-gpt-a-02: sourced, photon-consistent broadband fibre validation.
- T-20261017-gpt-a-03: Claude-family verification of new C-20261017-gpt-a-01.
- T-20261016-claude-a-03 remains open because its full stationary/global-bound
  assignment is incomplete; the completed numerical audit is reviewable in PR #57.

## Proposed card changes

For the PI, keep achievable witnesses, finite-basis stationary points and global
upper bounds distinct. The phase-shaped gains persist on top of a local TL
fraction optimum, but fixed-N duration optimization is not fixed laser energy.
Track energy, output share, red shift and material-model validity separately.
The quoted TL peak law is a baseline, not a bound on shaped launches. No problem
card was edited. Any stronger universal statement needs its own claim and audit.

## Validation

The required scripts/validate.py and scripts/check_generated.py origin/main
both returned ok. The final figure was inspected and its legend spacing fixed.
Final validation after all records were saved also returned ok; git diff --check
is clean. JSON is standard, selected-mask hashes are unchanged, all recorded
roots/censuses pass, and the three stationarity failures remain explicit.
The solver submodule is clean at the recorded commit; origin/main is an ancestor
of this task branch. PR: https://github.com/nrivera494/analytical-nl-discovery/pull/57.
