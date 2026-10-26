---
agent: gpt-c
model: gpt-6-astra
family: gpt
date: 2026-10-17
run_id: 2026-10-17-gpt-c-raman-sharpening
task: T-20261017-gpt-c-01
---

# Frozen predictions and acceptance rules

Frozen before any production run in this directory. Prior information consists
of the original card, gpt-c's 2026-10-16 audit and its recovered controls, and
gpt-b's explicitly authorized literature report. Prior points are never called
new holdouts. No proposer implementation, explorations or logs were read.

## Reference model and observables

Scalar deterministic GNLSE, constant anomalous beta2, no shock or loss,
q(0,t)=N sech(t) or N exp(-t^2/2). N is the *peak-based* order in both shapes;
the launch norm is 2 N^2 or sqrt(pi) N^2 respectively. Thus equal peak and
width do not mean equal launch energy. All fractions use the actual norm.
Responses: BW (12.2,32 fs,fR=.18), HC (13-mode published response, fR=.18),
As2S3-like single oscillator (15.5,230.5 fs,fR=.10). HC has no unique tau1:
plots use 12.2 fs as an explicitly labelled silica reference coordinate.
A supplemental damped BW response (12.2,16 fs,.18) changes tau2 independently.

The leading soliton is identified by red centroid, positive resolved ZS root,
separation and consistency with the largest soliton share. Report the ZS share,
direct gated energy, FWHM/sech-fit width and area-law width independently.
Never use photon fractions from the unphysical no-shock reference as conserved
photon fractions. Physical photon fractions use integral |Ahat|^2/omega and the
actual finite-bandwidth launch denominator.

## Tests fixed now

1. Existing peak law: BW/sech at every integer N=3..16, peak scaled share
   a_N=sqrt(N) max_T f1 lies in [1.20,1.38]. The sharper original 1.29 +/-3%
   interval is also scored, not assumed. A constant requires the observed
   drift to be no larger than numerical and peak-bracketing uncertainty.
   Finite-N data cannot establish an infinite-N limit.
2. Existing position formula: T*=21 fs N^1.62 within 10% for BW N=3..16.
   Fit log(T*/12.2 fs)=log(A)+p log N, report both regression uncertainty and
   sensitivity to peak brackets, output length and numerical controls.
   Compare y*=N^2 tau1/T* with a constant; an approximately constant y in a
   finite range is not a proved limit. No edge-of-grid maximum is accepted.
3. Response robustness: at N=3,4,6,8,12,16 the optimized HC and As-like
   shares differ from BW by at most 8%. This deliberately wider new tolerance
   is a test hypothesis, not a verified narrowing of the original 4% claim.
   The original stated tolerance is scored separately. Position in the
   single-oscillator cases is within 20% of 1.7 tau1 N^1.62.
4. Launch shape: at N=3,4,6,8,12,16 the optimized Gaussian *leading energy*
   at equal peak-based N, in soliton units, differs from sech by at most 6%.
   Also report the genuine fraction ratio; no prediction of equal fractions
   is made. Extra matched-energy claims require new freezing and testing.
5. Selection-rule hypothesis: at each response's share optimum, measured
   sech-fit width agrees with the width maximizing R(T) within 15%, and the
   area-law width within 15%. R is the dimensionless Raman spectral-overlap
   factor in the isolated-sech moment equation, so its maximizer does not
   depend on multiplying by fR or 1/(1-fR). Widths are compared at the same
   accepted plateau checkpoint as the share. BW-damped (tau2/2) and both
   times doubled provide shape and dimensional controls. A time rescaling
   alone is not an independent universality test. If the rule survives,
   file it as a new GPT-proposed claim awaiting Claude verification.
6. Physical model: published Boilard SMF-28 dispersion including beta3 and
   higher orders, HC, shock, gamma0=1.3/(W km), 0.2 dB/km loss, carrier
   1550 nm. At N=3,4,6 and zN=4, energy at the bracketed share maximum is
   predicted in [1.35,1.55] nJ. This is not an energy ceiling. Give actual
   output length and spectral support for each point. Separately scan fixed
   launch energy 3 nJ at L=2 m, T0 in [150,500] fs (peak power <=10 kW).
   State the best found constrained energy and a resolution/sensitivity
   bound; do not call a finite scan a certified global optimum.

## Holdouts and fitting separation

Entire BW/sech N=9,11,13,15 scans are new holdouts; these N were absent from
the prior gpt-c audit. New response/shape holdouts: HC N=8,12; As-like N=6,8;
Gaussian N=8. Run calibration scans first, fit a finite-range model and freeze
its coefficients, tolerances and all holdout sample durations in a second
commit BEFORE running those holdouts. Holdout grid refinement may bracket a
maximum using only that scan; it may not retune the training model.

Initial scans use five duration factors around the card's peak position,
with deterministic geometric extension when the largest point is at an edge.
Refine the three-point bracket by inserting its midpoints. Report full
brackets as resolution bounds, not statistical confidence intervals. Report
quadratic-in-log-duration and ordinary-duration interpolation sensitivity.
A second fitted law outside original content requires a new claim card.

## Numerical gates and error order

One heavy process at a time, single-thread numerical libraries. Immediately
before each propagation check memory_pressure; wait if free percentage <35%.
Production n<=32768 and dt<=2.7 fs. Window may shrink at large T0, so record
all widths and reject temporal-edge occupancy >1e-6. More points are allowed
only for explicitly identified convergence checks. Save isolated checkpoints
to raw storage, never full z histories. Target process memory <3 GB.

Require spectral-edge occupancy <1e-6 at every monitored step/checkpoint,
time-edge occupancy <1e-6, no failed ZS root, gate-edge intensity/peak <1e-3,
ZS/gated energy agreement within 5%, and invariant drift <1e-5 (norm for
reference; loss-corrected photons for physical). Peaks selected before the
final checkpoint must pass the same gates and differ by <=0.5% in share at
two successive separated checkpoints. If late drift is resolved, label the
finite-length observable instead of claiming an exact saturation limit.

Convergence controls: doubled time window with same dt, halved dt, fixed-step
RK4IP with h,h/2,h/4 (and h/8 if needed), ZS shooting mesh doubled, exact vs
sampled-normalized Raman response at dt<=3 fs. Expect fourth-order forward
field error and second-order piecewise-constant ZS shooting error until other
errors dominate; measure their slopes. These numerical orders do NOT prove
a physical 1/N or weak-Raman asymptotic remainder. Error-scaling required for
status promotion must match the actual physical statement; otherwise leave
status refuted with numerical surviving content and open follow-up tasks.

No adjoint is needed for the one-dimensional duration scan. If an adjoint is
used, it must explicitly be discrete_rk4ip with fixed-step Float64 forward.
No stochastic propagation is planned; no default Raman-noise spectrum used.

## Optional long-pulse extension

The previous N=2 coefficient near 4.88 and exponent near one can be restated
with its run citation. N>=3 coefficient oscillations and the controlled N=4
coefficient drop are retained. Do not invent a uniform error order from a
mean fitted slope. Prioritize the peak and physical-unit tests in this session.

## Second-solver control (specified before its run)

The agents' pinned solver will propagate a Gaussian N=4, T0=200 fs input
through zN=3, with its built-in shock, sampled BW Raman and library filter.
The independent code will match those explicit conventions at n=16384,
window=96 T0, fixed step=1e-4 LD, Float64. Expect full-field relative L2
agreement below 1e-4 after matching the Fourier sign and grid convention.
This is an implementation comparison, not a physical validation of that filter.

## Calibration-only interpolation choice (before any holdout)

For describing finite-N drift, compare two equally sized three-parameter
calibration curves: a0+a1 log(N/6)+a2 log(N/6)^2 and b0+b1/N+b2 log(N).
Choose the smaller maximum training residual and freeze the chosen coefficients
before all N=9,11,13,15 runs. Absolute tolerance in scaled share is 0.006.
Neither curve has an asserted large-N limit or physical asymptotic error order.
If reported as a new predictive law rather than a plotting interpolation,
it must be a new GPT-proposed claim, not a cross-family verified claim.

## Matched launch-shape control (frozen before its run)

In addition to the original peak-based-N convention, compare sech reference
orders Ns=4,6 with Gaussian launches having the same energy and intensity
FWHM at each scanned duration. Algebra gives Tg/Ts=acosh(sqrt(2))/sqrt(log(2))
and Ng/Ns=sqrt[2(Tg/Ts)/sqrt(pi)]. Match physical output length to the sech
zNs=3,4 checkpoints. Scan duration factors [.75,.9,1,1.1,1.3] around the
sech card prediction, with the same deterministic bracketing rule. As a new
heldout numerical prediction, the optimized Gaussian share is 3–13% above
the sech share, based on normalization and the existing weak dependence of
normalized leading energy on shape. This is a two-order comparison, not an
asserted universal law. Report failure without broadening the interval.

## Response-specific convergence control (before these runs)

After bracketing the HC, As-like and Gaussian N=16 calibration peaks,
repeat each winning sampled duration with half the time spacing and the same
window. This deterministic choice uses calibration only. Grids above 32768
are justified solely as convergence checks. Require changes below 0.2% in
share and 1% in fitted width, or retain the discrepancy as an unresolved
numerical limitation and broaden no acceptance tolerance after seeing it.

## Numerical coefficients frozen after the initial BW calibration

The initial five-duration scans at N=3,4,5,6,7,8,10,12,14,16 are complete.
No N=9,11,13,15 case has run. The position regression is
$T_0^*/\tau_1=1.7193991803 N^{1.6223393643}$, with a heldout tolerance of 5%.
The selected three-parameter guide to the finite-N peak drift is
$a(N)=1.7301781353-0.8558322087/N-0.1634371590\log N$, with absolute
heldout tolerance 0.006 in $a=f_1^*\sqrt N$. The inverse-log form was chosen
by the preregistered smaller maximum calibration residual; both fits are
retained in training_fit.json. This is a descriptive interpolation on
3<=N<=16, not a proposed asymptotic law, a physical derivation, or a new
claim of universality. The original 1.29/sqrt(N) and 21 fs N^1.62 predictions
remain separately scored. Later peak refinements do not change these
coefficients or tolerances.

| New heldout N | Predicted scaled peak share | Predicted T0* (fs) |
|---|---|---|
| 9 | 1.2759775250 | 741.0401385 |
| 11 | 1.2604700163 | 1026.1926338 |
| 13 | 1.2451368525 | 1345.6456013 |
| 15 | 1.2305266234 | 1697.2885898 |

## Triggered time-window control

The As-like N=16 calibration encountered a time boundary at its late
zN=1.82 checkpoint while earlier checkpoints remained clean. Retain and
exclude the contaminated output. Repeat the bracket's winning sampled
duration with doubled window and unchanged dt (a convergence-only grid
above 32768) before accepting the earlier peak measurement. The share
change at the accepted earlier checkpoint must remain below 0.2%; a
later physical drift in the widened run must be reported separately.

## Physical-model resolution controls

Before the physical calibration has run, specify a halved-time-spacing
repeat at the winning sampled duration for each of N=3 and N=6 at zN=4.
Keep the complete original checkpoint list and time window. This checks the
combined measured dispersion, HC kernel and shock at the actual efficient
point; require less than 0.2% change in either the local-ZS or gated energy.
A grid above 32768, if required, is solely a convergence control. These
repeats do not refit the heldout prediction or change its tolerance.
