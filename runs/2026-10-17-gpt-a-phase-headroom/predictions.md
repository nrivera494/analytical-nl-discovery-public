---
agent: gpt-a
model: gpt-6-astra
family: gpt
created: 2026-10-17
task: T-20261016-claude-a-03
---

# Frozen independent verification and sharpening

No production propagation or optimization has run before this file's first commit.
Only the assigned claim cards, problem, cited run configuration/metadata/summary,
three authorized coefficient files, evaluator code and solver API documentation
were used. The recovered previous audit notes concern a different completed task.

## Model and observable

Use q=N u, tau=t/T0, xi=z/LD, LD=T0^2/|beta2|, u(0)=sech(tau),
and d_xi u=i u_tautau/2+i N^2 u[(1-fR)|u|^2+fR h*|u|^2].
Blow-Wood: fR=.18, tau1=12.2 fs, tau2=32 fs; exact Fourier transfer
function, no stochastic noise. Phase-only masks preserve the input energy.
Measure the tallest isolated peak, compare with a census of other peaks,
and use the most redshifted isolated soliton if it differs. Report gated
energy/input energy, largest local ZS mass/input mass, centroid redshift,
input and output energies separately. Independent ZS uses two-sided shooting;
local-dispersion rescaling is required with higher dispersion. Gate sensitivity
is a systematic error, not a statistical confidence interval.

## Predictions and decision thresholds

V1. At N=4, T0=100 fs, xi=1, mask A2 has ZS headroom >=1.085;
mask A has >=1.055. At T0=200 fs, mask B has >=1.065.
Reproduction tolerance against the cited values is .005 absolute in f1 and
.005 absolute in the headroom ratio. These conservative inequalities narrow
the original numerical lower bounds; they are not new laws or upper bounds.
A2 or B with H>1.05 refutes C-20261016-claude-a-03 independently.

V2. A2 and B are saturated: changing L from 4 to 6 LD/N changes f1
by <.005 absolute, provided window and aliasing diagnostics pass. Compare 8
LD/N where affordable. Gated energy and ZS fraction agree within .01 absolute.
A gate-width variation by +/-25% changes the ZS fraction by <.003.

V3. The phase-only input energy changes by <1e-12 relative. Without shock or
loss, propagation energy drift is <2e-4. Time-edge and outer-20%-frequency
energy are <1e-6; stricter values will be reported. Halving step, halving dt,
and doubling the window change accepted f1 by <.002. On a four-level RK4IP
step sequence, asymptotic field-error order is expected in [3.3,4.7]; saturation
or another order is reported as a failed prediction, never forced by a fit.
Raman time resolution checks include dt <=3 fs. Independent Python RK4IP and
pinned Julia solver agree within .002 in f1 and 1% relative redshift.

V4. Held out: A2 at 90 and 110 fs; B at 180 and 220 fs, each at the
reference laser energy and reference physical length. Thus N=Nref sqrt(T/Tref),
xi=(4/Nref)(Tref/T)^2. Keep the phase mask fixed in physical frequency.
Predict H>=1.02. These cases cannot be used to optimize or choose masks.

V5. Held out: A2/B with (a) physical self-steepening at 1550 nm;
(b) beta3=.12 ps^3/km, beta2=-21.7 ps^2/km; (c) .2 dB/km attenuation;
(d) a sourced SMF-28 dispersion curve with shock and loss. Predict positive
energy headroom for a,b,c; no numerical prediction for d, a domain attack.
Physical input E=2 N^2 |beta2|/(gamma T0), gamma=1.3 /(W km).
If material evidence is unavailable, label the dispersion model explicitly
as a representative approximation, not a measured SMF-28 sample.

## Optimization (training; not held-out evidence)

N=3,4,5 at T0=140,200,280 fs respectively. Use >=30 smooth coefficients,
seeds 2026101701, 2026101702, 2026101703, 2026101704. Start from TL,
small random and larger random phases, plus authorized mask B at N=4.
Use fixed-step Float64 RK4IP and explicit adjoint_mode=:discrete_rk4ip,
checkpointed replay, no full-z histories. Optimize a differentiable isolated-
soliton energy gate, independently remeasure its ZS content, and report the
objective distinction. Target ||gradient||_2 <=1e-5 in the declared basis,
verify directional derivatives by central differences (relative error <1e-4),
report per-start spread, evaluations and termination reason. A stationary
point is not a global optimum. Unconverged starts remain lower bounds.

Freeze additional held-out cases before evaluating any best new mask:
N unchanged and T0 at +/-5% of its training value; length 6 LD/N;
finer step/grid. Predict the new mask exceeds its paired TL by >=1%.
TL duration scans at .8,.9,1,1.1,1.2 times training T0 quantify how much
headroom remains above the best sampled TL duration. Such scans are training.
No N power law or nontrivial upper bound is claimed in advance. Any new law
requires a new proposer claim and a Claude-family verification task.

## Resource and time rules

One heavy process at a time, memory free >=35% before launch, target RSS
<=3 GB, maximum grid 32768. Serial scans, sparse output, raw data outside git.
Stop production with >=15 minutes reserved for records and validation.

## Pre-optimization refinement

After the published-mask replication, but before any optimization, prefer a
direct discrete-ZS objective if its implicit eigenvalue derivative passes the
same 1e-4 directional check. For each piecewise-constant ZS transfer matrix,
differentiate its exact 2x2 exponential, contract the forward/backward products,
and use d zeta = -d a/(d a/d zeta). This removes the gated-energy proxy from
the optimizer. The independent, refined shooting measurement stays the final
readout. If the direct derivative fails, retain the original gate objective and
report the failure. No optimized output has been inspected when freezing this.

## Material-model freeze, before robustness runs

In addition to the representative dispersion curve, use the published SMF-28
Taylor curve in Kormokar et al., arXiv:2301.02945, Table 1 (full text accessed):
beta2=-21.61 ps²/km, beta3=.125 ps³/km, beta4=-3.99e-4 ps⁴/km,
beta5=1.99e-6 ps⁵/km. Normalize the shape to the common carrier beta2=-21.7
so the reference N, laser energy and fibre length stay fixed across models.
Test this dispersion with physical shock and .2 dB/km loss. Also test the
published normalized gamma(omega) Taylor curve (gamma0=1.42, gamma1=.0029,
gamma2=-1.43e-6, gamma3=-1.11e-8 in the paper's ps, W, km units), replacing
the linear shock factor, not multiplying it a second time. These are domain
attacks with no claimed minimum gain. No robustness simulation has run yet.

## Optimization-resolution decision

The first core convergence sequence measures RK4IP field orders 3.93 and 3.97,
and doubling the original step changes the baseline fraction by less than 1e-6
(run summary). Use hfac=2 for search, with all selected masks repropagated at
hfac=1 and .5 before acceptance. This changes search resolution, not the frozen
physical targets or held-out thresholds. A stationary point is certified only
for its stated grid, step and 30-coefficient basis, and finer-grid gradients
are reported if feasible. The Python checkpointed discrete adjoint agrees with
finite differences to 2.5e-8 and with the Julia baseline forward field to 4e-12.
The independent implementation does not use the solver's continuous adjoint.

## Before the independent multistart search

Use a wider optimization-only ZS truncation (half-width max[2,12/max|q|])
and a two-sided Evans determinant with its exact discrete derivative. This
suppresses moving-boundary effects in the stationarity test. The independent
reported readout remains the original gate with its frozen width checks.
Finite-difference checks must pass before each N's first production search.
The preliminary Julia search used the original narrower truncation and remains
recorded separately. This change was made while the robustness suite was
running, before the Python multistart optimizations began.

## Further held-out qualification, frozen before selection and evaluation

After all multistart searches and any training-only polishing, select masks
using independent propagation at their training N,T0 only. Freeze the selected
coefficients and commit their manifest before held-out qualification.

For each selected mask, repeat the already specified +/-5% duration and
6 LD/N held-out checks. Also evaluate physical shock, beta3=.12 ps³/km,
.2 dB/km loss, and the published dispersion+shock+loss model, with paired TL
launches. Predict positive energy headroom for shock, beta3 and loss; the
full material case and +/-10% duration at fixed laser energy/physical length
are domain attacks without a promised minimum gain. Keep the mask fixed in
physical frequency in duration tests. These outputs cannot select the mask.

Add a cross-N held-out transfer: apply the selected N=5 mask, unchanged in
normalized frequency, to N=6,T0=380 fs at 4 LD/N. Predict H_ZS>=1.05 relative
to its paired TL launch. No N=6 output has been run or used for optimization;
no subsequent tuning to this point is allowed. This tests transfer of a mask,
not convergence of an N=6 optimizer or a universal N law.

Refine the training-only TL duration maximum by bounded scalar searches over
112–140, 180–220 and 252–308 fs for N=3,4,5 respectively, using the existing
coarse scan to bracket the maximum. This establishes a local peak over the
stated bracket, not a global maximum over all laser spectra or energies.

## Polishing resolution, before any polishing or selected-mask holdouts

Polishing may use Fourier interpolation inside the optimizer's ZS gate, with
the exact transpose of that interpolation in the terminal derivative. This
reduces the known midpoint-shooting O(dt²) bias without changing the physical
objective or phase class. Odd padded input/output lengths avoid a Nyquist-mode
transpose ambiguity. Require the same directional derivative check before
production use. Prefer hfac=1 and ZS interpolation factor 4 for the final
training-only polish; independently check selected-point gradients on a finer
forward grid and step if the time budget permits. Report the resolution of
every gradient, and do not identify coarse-grid stationarity with a global or
continuum maximum.

## Matched comparison at the TL duration peak, before selection or peak search

After the training-only TL duration search fixes its local maximum for each N,
evaluate the already selected mask at that duration, with N unchanged and the
mask fixed in physical frequency relative to its training duration. Compare
against the TL launch at that same duration and laser energy. Predict positive
gated-energy headroom, and report its ZS fraction and red shift. The masked
output at this adaptively located *TL-only* peak is held out from all mask
selection and tuning; a failure will be reported without retuning the mask.
This additional test distinguishes exceeding the TL peak in fraction across
durations from adding headroom to a laser already set at the TL duration peak.

## Smooth cutoff continuation, before evaluating any such case

The numerical basis uses a clipped frequency coordinate outside the populated
laser band. Test a C2 continuation with the same coefficients: for
a=|k|/kc, retain a below .95 and set it to 1 above 1.05; in between use
y=.95+.1 r-.1 r^3+.05 r^4, r=(a-.95)/.1, restoring the sign of k.
This matches value and first/second derivatives at the joins and leaves the
central spectral phase unchanged. Predict |f_ZS(smooth)-f_ZS(clipped)|<.002
for A2, B and all selected new masks. This is a held-out implementation attack,
not a new optimization. The stationary-gradient statement remains attached
to the explicitly declared original basis.

## Resolution guard after a failed random-start trial

The first N=5 random start left the resolved time window during a line-search
trial and subsequently failed its ZS root solve. Retain that failed attempt
and resume its best resolved mask. Enforce the already frozen 1e-6 edge-energy
criterion during search as well as final qualification; reject unresolved
window/root trials with a recorded guard penalty, never a physical objective.
This restricts what the finite computational window can assess, not what
smooth physical phase masks could achieve. A returned optimizer endpoint must
still pass an ordinary objective/gradient evaluation without the penalty wrapper.

For held-out qualification, prefer the largest independently repropagated
training fraction among candidates meeting the raw-gradient target. If no
candidate meets it, report the failure and the best unconverged lower bound.
Always retain any larger unconverged candidate separately. This choice uses
only training output and the requested stationarity criterion.

## Wall-clock allocation before the remaining starts and all selected holdouts

Cap the initial search at three starts per N (nine total), then polish the best
candidate. The fourth planned starts are explicitly deferred in
`training_budget.json` to preserve the user's final validation/closeout reserve.
Use hfac=1 for training repropagation, TL peak location and ordinary paired
duration/material holdouts. The selected ideal cases still receive the full
four-level hfac=2,1,.5,.25 sequence, refined grid/window checks, and finer
gradients; N=6 and the closest published-mask held-out margin retain hfac=.5.
If a positive-gain decision is within .002 of its threshold or invariant/edge
checks fail, run a finer paired check before accepting it. No held-out masked
output has been observed when making this resource allocation.

Before running the final census, screen all output peaks above 5e-5 of the
maximum intensity (prominence 1e-5, minimum separation .25 T0), with no cap on
their number. For each candidate, limit its gate by neighboring peaks above
.005 of its own height, and require a half-width of at least 4/|q_peak| to
call it isolated. Identify the reddest resolved soliton among ZS masses above
1% of laser input energy with gate/ZS disagreement below 10% relative. Record
all screened peaks and this detection floor; do not imply completeness for
arbitrarily weak solitons or classify unresolved radiation as a soliton.

## Final resource guard before selected-mask holdouts

At 19:06 local, reserve the remaining wall-clock allocation for qualification
and closeout by limiting subsequent polishing launches to 420, 600 and 1200 s
for N=3,4,5. The already running N=3 launch retains its original iteration
limit. A time-limited endpoint is not called stationary unless its measured
raw gradient passes. The directional derivative check near stationarity uses
absolute error <=1e-9 + 1e-4 times the derivative magnitude; a relative-only
check had stopped at an absolute discrepancy of 8.2e-11 for an 8.0e-7
directional derivative. That stopped attempt remains in its raw stdout.

Before inspecting final finer-gradient output, also check one independent
direction at each selected mask on the finer gradient grid: random seed
2026101705, unit direction, central difference epsilon 1e-5, absolute plus
relative tolerance 1e-9 + 1e-4 times derivative magnitude. These are training
stationarity checks; no held-out output selects or changes a coefficient.

At the first N=5 polishing time limit, the raw gradient remains above target.
Before selected-mask holdouts, allow one further training-only continuation
from its best resolved coefficients, with the same 30-parameter class,
hfac=1, ZS refinement 4, preconditioned BFGS, and a 720-second limit.
Retain the first stopped attempt and report both gradients. The continuation
does not relax any physical, convergence or held-out acceptance threshold.

Before freezing selected coefficients, apply the already declared output-peak
census to training fields. Within the stationary-first ranking, select the
highest-fraction candidate whose tallest peak is also the reddest resolved
soliton above the declared 1% input-energy floor. Record and retain any rejected
candidate. If none passes, do not describe a tallest-pulse optimization as
verified leading-soliton headroom. This uses training outputs only, before any
selected-mask held-out propagation or census.

## Post-run window diagnosis, before additional propagation

The completed selected-mask checks show N=5 fraction stability under doubling
the window (difference 1.5e-4), but a large full-field change (relative norm
1.12, still 0.59 after phase/time alignment). N=3,4 do not show that sensitivity.
This is a newly observed concern, not an additional pre-registered success.
Run N=5 at width 640 T0 with 65536 points, hfac=1, and the frozen clipped mask;
also run its frozen C2 continuation at widths 320 and 640 with 32768 and 65536
points. The 65536-point exception is solely a window-convergence test: keeping
dt=2.734375 fs while quadrupling the original window requires that grid, and
memory remains far below 3 GB. No mask coefficients change. Independently
remeasure the fraction and pulse census. Report any failure of the previously
declared .002 fraction tolerance, and enlarge the numerical discrepancy bar;
do not call these diagnostic outputs held-out prediction successes.
