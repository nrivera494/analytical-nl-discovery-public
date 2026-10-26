---
date: 2026-10-17
agent: gpt-c
model: gpt-6-astra
family: gpt
task: T-20261017-gpt-c-01
duration_min: 71
---

## Did

Continued the PI's phase-2 assignment from about 20:38 EDT on the same task
branch and PR #59, with an additional 120-minute budget and a 22:20 EDT
production cutoff. The phase-1 record remains in
`log/2026-10-17-gpt-c-raman-sharpening.md`. Reopened the parent task while
executing this extension. No user input was requested.

Chose ZBLAN because a published measured eight-mode Raman response is
available, rather than using a single-oscillator stand-in. Source-only
overlap/gain calculations preceded the material GNLSE. Frozen predictions,
source table, fibre model and scripts were committed and pushed in
b042d48 before any ZBLAN propagation. All material points are held out;
the gain-peak substitution was explicitly a risky new extrapolation, not
an established selection rule. No prediction was refitted to material data.

Used serial single-threaded propagation with memory checks before every
launch and case. Raw fields and logs are outside git, with sparse output
checkpoints only. Three narrow-window reference N=6 endpoints were excluded;
the failed files remain. The new analyzer's final-checkpoint edge check was
corrected, while the phase-1 analyzer already had that check. The recovered
reference bracket uses a wider window. One fixed-dt doubled-window control
requires 65536 points; its explicit convergence justification is committed
in `artifact_followup.md`. Ordinary cases remain at most 32768 points.

Refinement/control case lists were committed before execution. The response
implementation and original predictions remain unchanged. The pinned
agents' solver is read only; a run-local Raman subtype supplied the completed
matched Julia forward without editing solver files. No adjoint or noise
calculation is used.

Extended gpt-b's authorized review with material-response, bandwidth-matching,
fission-duration, chalcogenide/tellurite/fluoride and thesis searches.
Read accessible primary text and recorded incomplete access. Source access
was not inferred from another agent's access. Search metadata's incorrect
author label for Al-kadry's thesis was corrected using its title page.
No login, subscription, download restriction or TLS check was bypassed.

## Found

Run `2026-10-17-gpt-c-zblan-transfer` has all eight local peaks bracketed.
The physical model's frozen duration predictions fail for N=3–6; its
scaled-share prediction passes for N=3,4 and fails for N=5,6. Energy at the
share optimum passes the deliberately broad 45% tolerance. Both fitted and
area widths reject the 22.056 fs overlap-width null in every physical case.
All 17 grid/window/step/kernel comparisons pass: maximum relative
share/gated-energy change 0.0001666 and width change 0.0003679.

All 40 prediction scores are resolved, including full numerical intervals.
The reference shares all pass, positions all fail, energies pass only at
N=3, and the area-width null passes only at N=3. RK4IP field error converges
at order 3.990–3.996; sampled kernel, shooting and independent Strang errors
approach order two. Matched Julia/Python relative field error is 2.46e-14;
the finest Strang/RK4IP difference is 9.44e-5. These are numerical error
orders, not a controlled physical fission-law remainder.

The material inventory has 149 completed Python cases, two edge-terminated
cases and no unrun planned cases. Three original narrow-window endpoints
are excluded; failed outputs are retained. Separate Strang and Julia
checks completed. Minimum checked free memory was 57%; maximum single
process RSS was 1,402,912,768 bytes. Physical peak brackets have photon
drift below 1.64e-8 and more than 99.9998% of leading gated energy between
1.5 and 3 µm. Full observables, intervals and source references are in the
run's summary and tables. Both final plots were visually checked.

Novelty verdicts: selection, peak share, peak position and efficient-point
energy are each partly published, with high confidence in the ingredients.
Exact fixed-N laws and the fission exit-width equality were not found in
the bounded search, with medium confidence. No novelty is inferred from
the failed prediction. DOI/arXiv identifiers and access levels are in the
new review and source ledger.

## Changed

Filed C-20261017-gpt-c-01 as new GPT proposer content, with Claude-family
verify task T-20261017-gpt-c-05, and changed it from proposed to refuted by
proposer tests. Verifier/auditor fields remain null. Added a same-fibre calibration follow-up,
T-20261017-gpt-c-06, because the simulation combines a measured bulk Raman
fit and a separate published fibre model. Updated the original claim's
novelty/current-outcome rows while preserving its submitted Statement and
Derivation. Added the new audit, run scripts, prediction/score/source
ledgers, scalar diagnostics and summary plots.

Completed parent task T-20261017-gpt-c-01 across both phases. The original
claim remains refuted. PR: https://github.com/nrivera494/analytical-nl-discovery/pull/59.
The final integrity record checks frozen predictions and primary forward
code against b042d48, the original claim's protected sections, all scores,
numerical controls and the unchanged solver pin. `scripts/validate.py`,
`scripts/check_generated.py origin/main` and `git diff --check` passed;
the closing validation record identifies the checked baseline.

## Not verified

Independent Claude verification of the new claim; same-spool Raman/dispersion,
mode-area/loss calibration and its uncertainty; a controlled physical
asymptotic remainder; global duration unimodality; infinite-order or
output-length-independent limits. The area-law energy is evaluated at a
specified share optimum, not an absolute maximum. Source-only response
quadrature precision is not material uncertainty. Yan's full article and
some newer fluoride texts were inaccessible; the negative novelty finding
is bounded, not exhaustive.

## Loose ends

- T-20261017-gpt-c-05: independent Claude verification of the material test,
  response convention, failed null and numerical exclusions.
- T-20261017-gpt-c-06: physical calibration and uncertainty using data from
  the same ZBLAN fibre.
- Phase-1 T-20261017-gpt-c-02, -03 and -04 remain open for theory/asymptotics,
  constrained continuous energy optimization and the deferred controls.

## Proposed card changes

For P-20261016-claude-interactive-03, preserve the finite numerical silica
core but distinguish a response-overlap maximum from an exiting fission
soliton's width. State the output-length convention and energy/photon
observable alongside every material prediction. A measured multimode
response is an essential test of a gain-peak time substitution; a published
bulk fit is not a calibration of every fibre of that material. No problem
card or generated file was edited, and nothing was promoted to results.
