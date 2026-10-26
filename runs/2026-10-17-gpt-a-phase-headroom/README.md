---
agent: gpt-a
model: gpt-6-astra
family: gpt
run: 2026-10-17-gpt-a-phase-headroom
---

# Independent phase-headroom verification

`config.yaml`, `meta.yaml` and `predictions.md` define the model, identity,
freezes and prospective decisions. Raw fields, complete optimizer histories,
failed trials and stdout belong in the absolute `raw_location` in `meta.yaml`;
they are deliberately absent from git. Coefficients are small reproducible
inputs and are committed. The solver submodule is unchanged.

The principal final products are `summary.json` (all case records),
`verification.json` (paired energy/share/shift comparisons and frozen tests),
`readout_checks.json` (ZS resolution, gate sensitivity and peak census),
`stationarity.json` (gradients of the selected coefficients), and
`fig_summary.png`. These products are complete. `verification.json` retains the three failed
stationarity thresholds; a completed run is not a completed optimization.

## Reproduction

Use the Python environment recorded in `meta.yaml`. Run one heavy process at a
time, with one numerical-library thread, after checking that `memory_pressure`
reports at least 35% free. The wrapper enforces the memory check; call it with
`/bin/zsh launch.sh`, since executable file permission is not assumed. Julia
uses `--project=solver` from the repository root.

The stages are deliberately separate:

1. `independent.py core` propagates the three authorized published masks and
   their paired TL launches. `suite.py` supplies the original convergence,
   length, duration and material-model cases; see its command-line choices.
2. `serial_queue.py` runs the initial 30-coefficient direct-ZS searches.
   `training_budget.json` records the three deferred starts. `polish_queue.py`
   refines completed candidates; `final_training_pipeline.py` sequences this
   with training-only independent repropagation and TL duration-peak location.
3. `training_census.py` first checks the leading-pulse identity on training
   fields. `freeze_selection.py` then makes `selected_masks.json` and coefficient
   files from training output. Commit these before running `qualify.py final`. The final
   stage must never select or retune a mask from a held-out result.
4. `check_stationarity.py` remeasures the actual selected mask gradients at two
   resolutions. `qualify.py final` runs selected-mask held-outs and numerical
   attacks, including an unchanged N=5 mask transferred to N=6.
5. `postprocess.py` performs an independent gate/census/ZS-resolution analysis.
   `finalize_analysis.py` rebuilds the complete summaries and figure.

The stages keep completed case files on restart. A changed physical input or
method requires a distinct case label, so a cached result cannot be silently
reinterpreted. Optimization attempts stopped by an exception, resolution guard
or iteration/time limit remain part of the evidence.

## Conventions and limits

Standard FFT positive frequency is physical red shift here. The authorized B
coefficients are converted by reversing odd Legendre orders. New committed
coefficients already use the independent code's convention. Phase-only masks
preserve input energy; all main fractions use that input energy as denominator.
Output-energy shares and energy in nJ are recorded separately.

Duration robustness holds the physical spectral mask fixed. Fixed-energy tests
also hold physical fibre length fixed, hence change N. The cross-N transfer
instead holds the normalized-frequency mask fixed, as prospectively specified.
TL duration optimization holds N fixed and therefore does not hold laser energy
fixed between durations; each masked/TL pair nevertheless has identical energy.

Reported numerical discrepancies are systematic resolution estimates, not
statistical confidence intervals. A small coefficient gradient certifies only
the declared finite-dimensional discretized stationary point. A feasible mask
certifies a lower bound on headroom; none of these searches certifies a global
upper bound or an N-dependent law. The material Taylor model and local ZS
diagnostic have the limitations stated in the audit and `sources.md`.

## Final qualification limits

Only N=3 meets the two-grid gradient target. N=4/N=5 are feasible witnesses,
not resolved optima. N=5's fraction is stable over three windows, but its full
complex waveform is window-sensitive (`window_diagnostics.json`). The bounded
post-run test `window_extension.py` uses 65536 points only at width 640 T0 to
keep dt=2.734375 fs; its pre-launch exception is recorded in `predictions.md`
and `meta.yaml`. It does not retune a mask. `complete_census.py` fills the same
frozen census on length and TL controls when restarting an older readout run.

Use `verification.json` for accepted paired fractions. Original raw records
include a retained failed ZS root for the N3 fixed-energy 90%-duration case;
`readout_checks.json` and `detune_N3_ZS_root_diagnosis.json` document its repair
on the identical stored field. `summary.json` retains all original values and
fills only missing ancillary photon/energy metadata in the earliest records.
