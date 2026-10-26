---
date: 2026-10-16
agent: gpt-c
model: gpt-6-astra
family: gpt
task: T-20261016-claude-a-02
duration_min: 0
---

## Did

Independently audited C-20261016-claude-a-02 on the task branch stacked on
PR #48, which stacks on PR #44. Built a separate scalar Fourier RK4IP
implementation and a C two-sided ZS shooting measurement. Used a peak census,
local physical normalization and direct gated observables. The pinned agents'
solver was used for a matched fixed-step cross-check; its source and the
original solver repository were not modified.

The completed independent verdict was committed as
`143cc58cd167f32b4edc88b7f007d23ab2dd641c` before reading the delegated novelty
report in gpt-b's PR #52. The audit's post-commit section records that review,
the subsequent solver-window source inspection, and later controls. No
proposer run scripts, explorations or logs were used, and no conversations
from other projects were accessed.

One heavy propagation process ran at a time, with a memory-pressure check
before each launch/case. Raw fields were streamed to the designated data
directory. Larger grids were explicit aliasing or convergence tests; no
dense scattering matrices or full propagation histories were allocated.

## Found

All numerical findings below cite run `2026-10-16-gpt-c-raman-audit` and its
case-linked summary and audit report.

The verdict is **fail as written**. At fixed N, launch energy is proportional
to 1/T0. At a positive differentiable interior share maximum, the derivative
of leading-soliton energy is negative, not zero. In the published-dispersion,
HC-Raman model, N=3 at the same 1.3-m physical fibre length gives about
2.23 nJ for T0=80 fs, 1.88 nJ for 100 fs and 1.395 nJ for 140 fs. The 80-fs
case passes grid, window and integration controls and retains more than
99.999% of global spectral energy in the dispersion comparison band. The
earlier 50-fs counterexample and its radiation-support limitation also remain
in the report; neither was hidden by the cleaner follow-up.

The approximate reference peak-share and duration laws survive the sampled
checks, including the preregistered N=4.5 point, central N=12 and 16 predictions,
and multi-peak HC response. This does not establish global maxima. At the
physical efficient points, the tested model gives roughly 1.44-1.46 nJ for
N=3,4,6, rather than preserving the proposed numerical energy scale.

The N=2 weak-Raman excess exponent is about 1.007 against predicted 1;
the strictly clean alternative fit and weak late radiation flags are retained.
The extended N=4 exponent is about 1.156 against predicted 1, and its lower
last coefficient survives grid, window, integration and saturation checks.
This finite-range result does not establish or disprove an infinite-limit
expansion. Full details are in the audit, with later controls separated from
the independent verdict.

High-N aliasing can corrupt the identified soliton while norm drift remains
small. Grid, window, integration and extraction checks are recorded without
discarding failed runs. With shock, the unscaled ZS proxy and locally normalized
energy/photon measurements must be distinguished; the narrower proxy tolerance
does not certify the physical photon fraction.

## Changed

C-20261016-claude-a-02 changes from `proposed` to `refuted`. Updated only its
verification/audit metadata, Regime, Checks and Audit trail. Preserved the
submitted Statement, Derivation, title and superseded regime. Added one audit
report, the independent run and two follow-up tasks. No problem cards or
generated files were edited by this audit, and nothing was promoted to results.

## Not verified

C-20261016-claude-a-01, C-20261016-claude-a-04 and the soundness of the earlier
C-20261016-claude-a-03 refutation were not audited in this session. Their statuses
remain unchanged; their verify tasks were not claimed. The PI's priority order
and preference for a complete audit of fewer claims determined this allocation.

No phase-mask adjoint optimizer, jitter/noise calculation, Gaussian-launch
universality test or proof of a global high-N optimum was performed. The
fixed-N duration attack already refutes the proposed energy maximum inside
its TL-sech class. Any shaping conclusions require the separately assigned
mask audits. The physical model does not include wavelength-dependent mode
area or a measured PI fibre sample.

## Loose ends

- T-20261016-gpt-c-01: resolve numerical weak-Raman coefficient convergence and
  breather-phase dependence, complementary to the uniform-limit derivation
  T-20261016-gpt-b-01 in PR #52.
- T-20261016-gpt-c-02: calibrated physical efficient-point energy, including
  mode area, attenuation, output length and the optional long fixed-length
  doubled-window control.
- T-20261016-gpt-b-02 in PR #52: derive or replace the compression/response-width
  mechanism. The post-commit numerical premise check is supporting evidence,
  not a completed derivation.
- T-20261016-gpt-b-03 in PR #52: remaining bracketed high-N/global-maximum,
  response-shape and experimental-observable tests. The execution inventory
  explicitly lists registered configurations that were not run.
- Existing T-20261016-claude-a-01 and T-20261016-claude-a-03 retain the other
  assigned claim audits and adjoint mask searches; T-20261016-claude-a-04
  retains the jitter work. They were not marked done by this session.

## Proposed card changes

No problem card was edited. For P-20261016-claude-interactive-03, separate
maximum conversion share, energy at a share-optimal point, maximum absolute
energy at a specified input constraint, and the corresponding photon fractions.
State output length and spectral support with each physical prediction. Split
the surviving empirical peak laws from the refuted energy-ceiling interpretation
and the unproved pointwise asymptotic remainder. Retain the empirical law only
on independently tested points until the follow-up tasks establish a wider
regime. The precise SMF-28 energy scale needs fibre calibration.

## Session closure

Final execution inventory, validation results, duration and PR are recorded
when the remaining controls stop. This entry is provisional until that update.
