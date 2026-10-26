# Configuration

agent: gpt-b; model: gpt-6-astra; family: gpt.

Frozen fundamental Kerr soliton with a symmetrized scalar Raman reservoir.
Material: $f_R=0.18$, $\tau_1=12.2$ fs, $\tau_2=32$ fs. The analytic spectrum
in `scripts/soliton_frozen_raman.py` is used for theory only; the physical
solver run uses the unchanged fetched Julia coth helper.

Commands use the Python environment and thread limits in the Kerr run.

- `soliton_frozen_raman.py --n 256 --window 40 --T0 .125 .25 .5 1 2 --temperature 0 77 300 --raw <raw>/pilot`
- `soliton_frozen_raman.py --white --T0 1 --temperature 0 77 300 --raw <raw>/white_reference`
- `soliton_continuum_sweep.py --n 512 --window 80 --dz .25 --max-z 8 --raw <raw>/distance`
- `soliton_thermal_optimum.py <raw>/edge_optimum.json`

The distance sweep's temperature-zero white-source curve is the infinite-pulse
Kerr limit, not a finite-pulse zero-temperature Raman calculation. The pilot
includes the actual finite-pulse zero-point source. Optimized centered
passbands are achievable upper bounds on arbitrary binary optima.

Additional independent checks:

- `soliton_material_lower_bound.py --T0 <width> --temperature <K> --z <zeta>
  --n <n> --window <window> --output <raw>/material_<case>_n<n>_w<window>.json`
  evaluates the cutoff-white, cutoff-linear-coth, and complete oscillator
  sources. The pilot and both held-out points use (n,window)=(256,40),
  (512,40), and (512,80).
- `soliton_material_jost_check.py --output <raw>/material_jost.json` computes
  independent continuum-cell covariances with widths .2, .1 and .05.
  Refinements use `--widths .025 --order 12` and `--widths .05 --order 24`.
- `soliton_thermal_asymptote.py --reference <raw>/pilot/summary.json
  --output <raw>/thermal_asymptote.json` predicts the next eigenvalue
  coefficients by perturbing the covariance operator, without a fit.
- `soliton_union_filters.py` optimizes symmetric disconnected interval
  edges, then checks quadrature at orders 48, 96 and 192. The output's
  edge lists and method settings fully describe the achieved filters.

Material/Jost and asymptotic checks use one BLAS thread. Every numerical
eigenvalue remains an approximation in the declared basis, not a certified
infinite-dimensional lower enclosure.

`log_tail_prediction.json` was committed before checking the large-distance
source integral. `log_tail.json` evaluates `bandpass(z,.7368,order=n,cutoff=8,
include_checks=True)` for the recorded distances and orders, retaining only
the bath coefficient per unit rho. It tests a fixed-mask frozen-model
asymptote, not a physical long-distance fibre prediction.

`soliton_log_growth.py --z 1024 2048 --orders 16384 32768 --output <raw>/log_growth_fine.json`
checks the large-distance period-averaged source derivative. It includes
the separately derived continuum-threshold and sharp-edge asymptotes.
`colored_log_coefficient.json` evaluates the stated one-dimensional
source moment at the widths and temperatures stored in that summary.

`soliton_manakov_readout.py --input <raw>/pilot/T0.25_K300_z4.712389.npz
--reference <raw>/pilot/summary.json --output <raw>/manakov_readout.json`
checks a conditional common-reservoir Manakov covariance identity, including
mode-dependent masks and their fractional-transmission/loss-vacuum reduction.
It constructs the bright/dark covariance algebraically; it is not a physical
GRIN simulation or an independent verification of the older multimode claim.

`soliton_short_distance.py --output <raw>/short_distance.json` checks the
unfitted even-mask Kerr quadratic and Raman cubic distance coefficients,
including their fourth- and fifth-order residuals.
`soliton_dc_check.py --input <raw>/pilot/T0.25_K300_z4.712389.npz
--output <raw>/dc_shared_limit.json` checks the uniform-phase-noise null
on counting readouts. Removing DC is a diagnostic only.

`soliton_quadratic_source.py --T0 <width> --temperature <K> --z <zeta>
--output <raw>/quadratic_<case>.json` evaluates the sharper polynomial-coth
minorant and the full oscillator. `quadratic_asymptote.json` compares their
amplitude eigenvalues at widths .25, .5, 1 and 2 ps, at zero and 300 K.
The third physical held-out prediction is separately frozen in commit
`55d2da6`; earlier physical points were already known when this refinement
was derived, so only the third point tests its predictive accuracy.
