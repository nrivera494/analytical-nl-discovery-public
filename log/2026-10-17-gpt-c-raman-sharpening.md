---
date: 2026-10-17
agent: gpt-c
model: gpt-6-astra
family: gpt
task: T-20261017-gpt-c-01
duration_min: 232
---

## Did

Started at 16:42:28 EDT with the PI's 240-minute budget. Inspected all 25
interrupted files with git status and diff before stashing, synchronized main
and the agents' solver, then created and claimed the assigned task. Restored
the interrupted work on the new task branch in separate commit d30913a,
labelled "complete post-audit controls from 2026-10-16 (uncommitted at the
usage limit)". The single card conflict kept both gpt-b's merged novelty row
and the stronger recovered physical counterexample. Nothing was discarded;
the stash and orchestrator backup remain.

Read the permitted cards, prior independent audit, authorized gpt-b literature
review and repository/solver protocols. No proposer scripts, explorations,
logs or PR descriptions were read, and no other clone or project conversation
history was accessed. No solver modification, adjoint or stochastic Raman
calculation was needed. The pinned agents' solver remains clean.

Ran serial independent propagation and a matched Julia forward. Initial
predictions were committed in 7390e2c, fitted BW coefficients/holdouts in
abe44ab, and physical resolution controls in 73562db, before their runs.
No frozen coefficient was refitted using heldout observations. Case-boundary
handoffs prioritized physical quantities, response controls and finally the
eight frozen BW midpoint refinements. No in-flight propagation was killed.
The last forward completed before the 20:27:28 EDT finalization reserve.

All propagation launches checked memory pressure; the lowest recorded free
percentage was 52%, and the largest recorded process RSS was 1.416 GB.
Only one propagation process ran at a time. Larger-than-32768 grids were
identified convergence controls, and raw checkpoints remain outside git.

## Found

Run `2026-10-17-gpt-c-raman-sharpening` supports the original finite BW/sech
peak approximations after narrowing. For integer orders 3–10 the numerical
scaled-share envelopes are within 2.1% of 1.29. The scaled share rises to
about 1.295 near N=5 and falls to 1.222 at N=16. The final duration exponent
is 1.62232, with a residual-based 95% interval 1.61459–1.63005 and much wider
full-bracket sensitivity 1.48516–1.75714. No constant scaled inverse duration
fits every bracket; no infinite-order limit follows.

All four new BW heldout orders pass both their scaled-share resolution
envelopes and full 5% duration-bracket tests. All response/shape holdout scans
completed. HC shares are about 0.9–2.3% below BW and the As-like response
about 3.5–6.4% below it. Equal peak-based order does not mean equal launch
energy; Gaussian fractions and normalized leading energies are separated.

The exit-width/overlap-maximum hypothesis fails at the tested turnover peaks,
including controlled counterexamples. No new claim was filed at the phase-1
close; the later material extrapolation is C-20261017-gpt-c-01. The exact
energy derivative at a fixed-N share maximum remains negative. The specified
realistic SMF-28 model gives local-ZS efficient-point energies about
1.44–1.46 nJ, with full numerical energy brackets inside the frozen
1.35–1.55 nJ interval. Directly gated energy and integrated photon fractions
are separate observables. A fixed 3 nJ, 10 kW, 2 m scan gives a best resolved
sample of 1.811 nJ gated output; it is not a certified continuous maximum.

All numbers above trace to the new run. The recovered weak-Raman controls
retain run id `2026-10-16-gpt-c-raman-audit`; their N=4 coefficient drop and
clean physical counterexample remain valid.

## Changed

Added the dated audit, one-page PI summary, single-panel verification plot,
independent scripts, freeze/source ledgers, detailed tables and run summaries.
Added the required cross-family sharpening section and current Checks/Outcome
rows to the original card; status remains refuted. Hash checks confirm that
the submitted Statement and Derivation are unchanged. Earlier regime text is
explicitly dated; the new sharpening governs the current scope.

Corrected summary bookkeeping that had treated a missing previous valid
checkpoint as zero plateau drift. Frozen BW calibration values were unchanged;
the As-like N=4 extension now passes the stricter criterion. Fixed the initial
HC kernel diagnostic's integer-array error and retained its failed log.
Independent quadrature showed that a small HC first-moment difference was
sampled-kernel discretization, not Fourier cancellation. These corrections
changed no forward propagation or frozen prediction. Coarse brackets were
superseded by retained midpoint data, not silently removed.

The final inventory has 221 completed cases, three retained edge-terminated
cases and 58 unrun designs. All primary heldouts and physical scans completed;
the unresolved 500 fs constrained extraction remains excluded. The unrun
set includes supplemental damping, matched-resource shapes and additional
refinements/repeated controls. T-20261017-gpt-c-01 is done; follow-ups remain open.

Final validation passed: `scripts/validate.py`,
`scripts/check_generated.py origin/main` after refreshing main, and
`git diff --check`. The final consistency check confirms the original-section
hashes, unchanged frozen training file and forward implementation, all four
full-bracket heldout passes, physical energy intervals, and the 720-by-540
pixel, 64,568-byte authored figure. No generated index or result folder changed.

## Not verified

A controlled physical asymptotic remainder for the peak laws; an infinite-N
limit; global duration unimodality; an output-length-independent limiting
partition; uniform long-pulse coefficients for N>=3; and a continuous
constrained-energy maximum. Physical parameter intervals are conditional on
the stated dispersion fit, constant mode area and uniform loss, and are not
spool-to-spool uncertainty estimates. Equal-energy/FWHM/length shape
universality and the supplemental tau2-halved fission scans remain untested.
The overlap maximum itself was computed for that response.

The finite drift curve is a plotting interpolation, not a new physical law.
Numerical fourth-order propagation, second-order shooting/kernel convergence,
and the isolated-profile cubic overlap remainder do not prove a fission-law
error order. Source access and the published antecedents are in SOURCES.md;
no new literature-novelty claim is asserted.

## Loose ends

- T-20261017-gpt-c-02: finite-order drift, large-N limit, global peak/length
  questions and a controlled physical derivation.
- T-20261017-gpt-c-03: continuous constrained optimization, wavelength-dependent
  mode area/loss and spool calibration.
- T-20261017-gpt-c-04: remaining frozen numerical controls and tighter duration
  brackets, using a new run under the executing agent's identity.
- Existing T-20261016-gpt-c-01 and T-20261016-gpt-b-08: long-pulse coefficients.
- Existing T-20261016-gpt-b-09: transient response overlap/compression mechanism.
- Existing T-20261016-gpt-b-10: matched-resource launch shapes, coordinated with
  the deferred cases in the new inventory.

## Proposed card changes

For P-20261016-claude-interactive-03, separate share-optimal operation from
energy maximization under a specified launch constraint. Keep finite numerical
peak fits distinct from asymptotic laws and from the published silica overlap
maximum. Do not present the failed exit-width equality as a selection rule.
Require the energy observable, output length and spectral support whenever
stating a physical operating point. No problem card was edited.
