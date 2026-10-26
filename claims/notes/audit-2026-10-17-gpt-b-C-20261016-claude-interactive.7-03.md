---
agent: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-17
claim: C-20261016-claude-interactive.7-03
task: T-20261016-claude-interactive.7-09
verdict: fail
status: completed-verification-failed
---

# Independent audit of the resonant GGE endpoint

The resonant invariants and phase memory are real. A stationary constrained
measure is also well defined. These facts alone do not establish the card's
long-distance endpoint law. The independent tests compare the claimed
three-constraint measure with an angular-momentum-conditioned measure and
explicitly track slow drift, cutoff-dependent invariants and symmetry sectors.

All numerical evidence here is from **run `2026-10-17-gpt-b-gge`**, with
short-time averaging and tensor checks from **run `2026-10-17-gpt-b-dirichlet`**.
No proposer scripts, exploration notes, logs or PR descriptions were read.
The protocol was frozen at `dc4c5e2bdb18c7255788b04f49e7bde833fed4cd`;
the numerical shell predictions were committed at
`925e15923f30798e64e263537490a59978157353` before any deterministic production
trajectory. Later length and symmetry diagnostics are explicitly marked as
selected after those initial data; their own predictions were frozen before
execution. Original failures are retained.

## What is proved

For the finite scalar resonant HG Hamiltonian

$$H=\frac12\sum_{q_p+q_q=q_r+q_s}S_{pqrs}a_p^*a_q^*a_ra_s,
\quad N=\sum_p|a_p|^2,\quad E=\sum_pq_p|a_p|^2,$$

global-phase invariance gives $\{H,N\}=0$, and invariance under
$a_p\mapsto e^{iq_p\theta}a_p$ gives $\{H,E\}=0$. The Hamiltonian itself is
conserved. Complete triangular HG cutoffs commute with rotations, so
$L=a^\dagger L_za$ is conserved too. In Cartesian oscillator notation
$L_z=i(b_y^\dagger b_x-b_x^\dagger b_y)$, up to orientation convention.
Different input phases at fixed modal powers change $H$ and generally $L$.

Liouville's theorem consequently makes

$$d\mu_{N,E,h,\ell}=Z^{-1}\delta(N(a)-N)\delta(E(a)-E)
\delta(H(a)-h)\delta(L(a)-\ell)\prod_pd^2a_p$$

stationary. Equality of a trajectory's long-time average with this measure
requires ergodicity on its **accessible connected sector**. Stationarity is
not attraction, and a positive Lyapunov exponent by itself is not ergodicity.
At finite mode count this microcanonical measure should not be silently
replaced by a canonical exponential with the same mean charges.

The untruncated resonant harmonic-trap system has further Kohn and breathing
bilinears. A hard complete-group cutoff preserves rotations, but its top
boundary breaks ladder-operator identities. In our finite model, direct
vector-field tests give zero angular-momentum derivative to floating-point
precision and nonzero Kohn/breathing derivatives for a populated cutoff.
They therefore must not be imposed as exact extra charges of this finite
simulation. Conversely, their absence here limits transfer to an untruncated
ideal-GRIN fibre.

The exactly aligned, equal-within-group launch is even under x↔y. Its exact
flow remains in that subspace. A full-space floating-point integration can
amplify roundoff into an odd component; the initial runs did so. A separate
Hamiltonian reduction to an orthonormal even basis and deliberately perturbed
full-space launches test this issue without projecting trajectories.

## Independent simulation and reference measure

The model, tensor normalization, sign convention and Brownian coupling are
specified in the Dirichlet audit and `evaluator/thermalized_light.py`.
Here $K=5$, $M=15$, $N=1$, and $s=z/L_{\rm NL}$. The code's $E=E'/\kappa$
is the physical excitation energy divided by the group gap, so
$E/N=E'/(\kappa N)$. Core inputs have $E=0.6$, with excitation energy
equally divided between groups one and two. Six
independent phase configurations and an all-real configuration share exactly
the same modal powers. Held-out inputs have $E=0.9$, energy in groups one and
four, four independent phases and an all-real configuration. All-real in this
Cartesian basis is not identified with the proposer's centre-focused launch.

The reference sampler first samples flat Dirichlet energy fractions and
uniform phases, then conditions on either $H$ or $(H,L)$. Direct shell
rejection is inadequate for rare high-H launches: the resulting low effective
sample sizes are recorded and not used as resolved predictions. Independent
reversible MCMC uses symmetric phase moves and energy-fraction exchanges,
with four chains initialized from both the launch and unrelated shell draws.
Gaussian conditioning widths shrink from 0.2 to 0.05 unconditioned standard
deviations. Chain-range, split-chain Rhat and bandwidth-shift gates were set
before propagation. Difficult cases were sampled longer and the final
predictions committed before dynamical testing. Finite bandwidth remains a
systematic error, explicitly reported beside chain uncertainty.

The unperturbed production window is $s\in[4000,24000]$, at step 0.04, with
selected step-0.02 repetitions. Follow-ups to 240000 use step 0.02 (selected
0.01 checks), only block moments and sparse checkpoints, and at most 24000
observation points. Those follow-ups were chosen after initial failures and
cannot be counted as newly blind tests.

## Initial results and disorder memory

The frozen shell predictions vary substantially with phase configuration.
For example, at E=0.6 the H-only and (H,L) predictions are respectively
0.74568 and 0.71647 for seed 4101; 0.74792 and 0.69367 for seed 4104; and
0.68484 and 0.63135 for seed 4105. RJ predicts 0.73929 independently of phase.
The initial dynamical means for the latter two launches are 0.69672 and
0.62680. Including angular momentum materially improves the comparison.
This demonstrates why the same mode powers do not specify a common shell.

Some initial trajectories have slow drift or substantial step-to-step changes
in long averages. The all-real full-space integration also leaves its exact
symmetry sector through roundoff. These observations block a blanket GGE
verification from the initial runs; matching a mean within a wide interval
is not sufficient.

For disorder, the same two phase launches share each of four independent
Brownian realizations. We define $L_d/L_{\rm NL}=1/\sigma^2$ using the full-GUE
normalization in the run. In the $[2000,8000]$ window the launch difference
at sigma=0.003 is $0.1642\pm0.0088$ (one paired-realization SE).
At sigma=0.1, 0.3 and 1, the full difference ±2 SE lies within ±0.02 and
both endpoints ±2 SE lie within 0.02 of RJ. The differences are respectively
$-0.00280\pm0.00058$, $-0.00160\pm0.00132$ and $0.00254\pm0.00206$.
Sigma=0.01 and 0.03 are not resolved as erased by this stronger equivalence
criterion. Sigma=3 is also unresolved in the initial window, with
$-0.0199\pm0.0092$; its extended paired-launch test is reported separately.
These are finite-model, finite-window observations, not a universal threshold
in $z/L_d$ or a calibrated metre-scale prediction.

Fusaro et al., DOI
[10.1103/PhysRevLett.122.123902](https://doi.org/10.1103/PhysRevLett.122.123902),
arXiv:2011.05111 (**full text**, theory and disorder discussion), provide the
relevant scale distinction: disorder weak compared with linear mode spacing
can be strong compared with Kerr. In their kinetic regime, increasing such
disorder slows the collision rate even though it can unlock thermalization
relative to the coherent ordered system. Suppressing mode-overlap and
occupation factors, their rate implies the parametric scaling
$L_{\rm kin}\propto L_{\rm NL}^2/L_d$ under the scale ordering
$L_{\rm lin}\ll L_d\ll L_{\rm NL}$. This scaling is a literature-based
interpretation, not a fitted law from our scan. Our observations are
consistent with that distinction. Their polarization-noise model and many-mode fibre do not fix
our spatial-GUE normalization or its relaxation coefficient.

## Long-time and controlled-sector results

The window $[80000,240000]$ gives the following examples, with uncertainty
estimated conservatively over block lengths through 40000:

| E, phase | Measured mean I0 | Frozen (H,L) mean | Interpretation |
|---|---|---|---|
| 0.6, 4101 | $0.71583\pm0.00350$ | $0.71647\pm0.00151$ | Consistent, small half-window drift |
| 0.6, 4104 | $0.69188\pm0.00253$ | $0.69367\pm0.00144$ | Consistent; H-only prediction 0.74792 fails |
| 0.9, 4201 | $0.57852\pm0.00481$ | $0.58366\pm0.00188$ | Held-out geometry, consistent |
| 0.9, 4204 | $0.53779\pm0.00659$ | $0.53104\pm0.00097$ | Held-out geometry, consistent |

The E=0.6 phase-4103 mean changes from $0.61507\pm0.01006$ at step 0.02
to $0.68280\pm0.01947$ at step 0.01. The latter's final-half shift is 0.03758.
Both wide intervals can overlap the shell prediction 0.64360; that is not a
resolved endpoint. Small charge drift does not establish finite-window
statistical convergence.

For exactly even reflection-sector dynamics, the E=0.9 result
$0.55405\pm0.00473$ agrees with the independently frozen nine-mode shell
prediction $0.55446\pm0.00134$. At E=0.6 the trajectory gives
$0.58662\pm0.01146$, against $0.61057\pm0.00134$, with a final-half shift
of -0.03554. Its stationarity gate fails. The reduced-vector-field identity
was checked independently to about $10^{-16}$; this is not a projected
fifteen-mode trajectory.

Controlled full-space aligned launches with a phase perturbation of $10^{-6}$
or $10^{-4}$ radians preserve all initial modal powers. At E=0.6 they give
$0.57124\pm0.00392$ and $0.57047\pm0.00324$, against the full-shell prediction
$0.58507\pm0.00155$. The larger perturbation fails the frozen endpoint gate.
However, the shell's finite-bandwidth shift is 0.00537, so this discrepancy
alone is not a conclusive infinite-time falsification. At E=0.9, the
$10^{-4}$ perturbation gives $0.53663\pm0.00572$, consistent with 0.53686.
The actual changes in H and L are in `reflection_summary.json`; they are
small compared with the conditioning widths. Exact-symmetry and explicitly
perturbed launches must not be conflated.

The first sigma=3 paired-launch extension was unresolved: over [8000,24000]
the phase-launch difference is $-0.01339\pm0.00552$, and neither that window
nor [18000,24000] establishes the prespecified ±0.02 equivalence bound.
This does not prove permanent memory at nonzero disorder. It sets a limit on
what these realization counts and finite lengths establish.

**Verification verdict: fail; endpoint law remains unverified.** Leave the
claim at `cheap-checks-passed`, with the failed cross-family verification
recorded. The three-charge model is inadequate for these GRIN launches;
the four-charge measure improves some comparisons but does not pass a
resolved, converged endpoint test across the frozen cases. It would be
incorrect to promote it. It would also be incorrect to call the conditional
Liouville/ergodic theorem mathematically refuted by unresolved dynamics.
The general finite-window prediction and the quantum extension are not
certified. No new claim is filed. Follow-up T-20261017-gpt-b-02 records the
remaining mixing, sampling and sector questions.

## Completed resolution follow-up

The bounded follow-up plan was frozen at
`551b4b651c7633fe5964e4f654250121e45221c4` after the first audit. The refined
numerical references were frozen at
`b0f3fd2ae9201955b020ac8d85668882fd03387b` before the new trajectories.
These are diagnostics selected after initial failures, not fresh blind tests.

Four new sampler chains use eight million moves per width, shrinking the
Gaussian conditioning widths from 0.05 through 0.025 to 0.0125 unconditioned
standard deviations. At E=0.6, phase 4103 gives $0.63386\pm0.00436$ at the
narrowest width, but its chain range 0.01939 fails the prespecified 0.01 gate.
The width shift is 0.00509. This reference is **unresolved**, regardless of
whether a trajectory mean agrees with it. The controlled aligned-plus-1e-4
reference gives $0.58127\pm0.00204$, width shift 0.00039, and passes its
sampler gates. Both original reference estimates are retained.

The phase-4103 extensions through $s=1200000$ give
$0.64077\pm0.01370$ at step 0.01 and $0.62675\pm0.01134$ at 0.005 over
$[400000,1200000]$. Their half-window shifts are +0.02422 and -0.02677.
The largest N/E/H drift falls from below $6.3\times10^{-7}$ to below
$2.0\times10^{-8}$. The means are compatible under the frozen statistical
step gate, but both fail the precision requirement, measured 2 SE <0.01.
Together with the unresolved reference sampler, this blocks certification
even though both means overlap the shell prediction.

The controlled aligned-plus-1e-4 launch at the same length gives
$0.58735\pm0.00995$ at step 0.01, with a half-window shift of -0.03422:
both its stationarity and precision gates fail. At step 0.005 it gives
$0.56881\pm0.00193$, half-window shift -0.00235, and maximum charge drift
below $2.3\times10^{-8}$. This finer run passes precision and stationarity,
but differs from the refined reference $0.58127\pm0.00204$ by 0.01246,
exceeding the frozen endpoint tolerance 0.01. The two step means are compatible
only because the coarser run has wide uncertainty. The refined reference's
bandwidth shift is 0.00039. Thus the longer follow-up retains a resolved
finite-window mismatch, not an infinite-time nonergodicity proof.
The exact reflection-sector extension gives $0.56201\pm0.00173$, half-window
shift +0.00222, against the frozen reduced-shell prediction
$0.61057\pm0.00134$ (bandwidth shift 0.00555). It passes the prescribed
precision, window-stability and charge-drift gates but fails the endpoint
comparison by 0.04856. Maximum N/E/H drift is below $7.3\times10^{-7}$.
This first long-sector result uses step 0.01. It demonstrates a failure of
the frozen finite-window endpoint comparison; it is not an infinite-time
counterexample.

The one additional sector step check was frozen at
`a97c5be66c77cee66d581c812f9d3e5846dc948c` after the large sector mismatch,
and completed before closing this report. At step 0.005 the sector mean is
$0.58359\pm0.00743$, half-window shift -0.01380, and maximum N/E/H drift
below $2.28\times10^{-8}$. Its difference from the reference is 0.02698,
larger than its frozen endpoint tolerance 0.02265; it also fails the precision
gate. The two step means differ by 0.02158 and meet the statistical step gate
only because the finer run has wider uncertainty (tolerance 0.02289).
Thus the extra check does not establish a converged counterexample or rescue
the endpoint verification. It is an explicitly post-data convergence
diagnostic with the same reference and unchanged endpoint/precision gates.
All six deterministic follow-up records fail at least one frozen verification
gate; the original passing comparisons are retained separately.

The longer sigma=3 paired-launch ensembles are complete. Both step sizes and
both frozen windows pass the ±0.02 equivalence gate, which requires the whole
paired difference ±2 SE inside that interval and each mean ±2 SE within 0.02
of RJ=0.7392857:

| Step | Window | Realizations | Mean I0, random / aligned | Paired difference ± one SE |
|---|---|---|---|---|
| 0.04 | [32000,96000] | 12 | 0.74034 / 0.73923 | $0.00111\pm0.00226$ |
| 0.04 | [72000,96000] | 12 | 0.73941 / 0.73851 | $0.00090\pm0.00521$ |
| 0.02 | [32000,96000] | 4 | 0.73558 / 0.74453 | $-0.00895\pm0.00299$ |
| 0.02 | [72000,96000] | 4 | 0.73305 / 0.74504 | $-0.01199\pm0.00119$ |

The last residual is significantly nonzero relative to its paired SE even
though it meets the prescribed equivalence tolerance. Thus this establishes
only tolerance-level erasure of the mean condensate-fraction difference, not
zero memory or equality of all distributions. The steps are analyzed
separately, and the finer ensemble has only four disorder realizations.
Maximum N/E drift is below $8.8\times10^{-7}$ at step 0.04 and
$2.75\times10^{-8}$ at 0.02. This extension changes both length and sample
count, so it gives a sufficient tested observation window, not a minimal
relaxation length or a universal scaling law. No claim status is promoted.

## Weak-nonlinearity scaling, artefacts and scope

Within the exact resonant model, changing the Kerr coefficient only rescales
$s$; dimensionless phase-memory endpoints therefore do not shrink just because
the nonlinearity is weak. The independent full-tensor comparison at
$\epsilon=(\kappa L_{\rm NL})^{-1}=0.1$ down to 0.0125 gives errors proportional
to approximately $\epsilon^{0.98}$ over $s\le4$ (Dirichlet run). This is a
short-length normal-form check, not a uniform approximation over the very
long trajectories used for endpoint statistics.

The applicable artefacts are propagation step, tensor quadrature, modal cutoff,
invariant drift and symmetry-sector leakage. There is no temporal grid,
Raman kernel or window in this monochromatic model; temporal aliasing and a
≤3 fs Raman-grid test are inapplicable. Strong intra-group disorder relaxes
the no-disorder assumption. No solver adjoint or optimized counterexample
search was used. Quantum reduced states, dispersion/walk-off, polarization,
finite spectral detuning and realistic finite correlation lengths are not
established by these runs.

## Prior-art verdict

The full-text primary-source review is in
`runs/2026-10-17-gpt-b-gge/literature.md`, including the search strings and access
levels. Resonant GRIN Hamiltonians and phase sensitivity are already explicit
in Podivilov et al., DOI 10.1103/PhysRevLett.122.103902. Germain, Hani and Thomann,
arXiv:1501.03760 and 1502.05643, establish resonant invariants and invariant
Gibbs measures, including finite-dimensional approximations. Wu et al., DOI
10.1103/PhysRevLett.128.123901, give optical generalized Gibbs ensembles with
angular momentum. Thus neither the existence of extra resonant charges nor
Gibbs stationarity nor optical GGE terminology is new by itself. This bounded
search did not locate a proven universal endpoint law for the particular
fifteen-mode quartic-energy-conditioned fibre model. The missing step is
its dynamical validity, not the formal construction of a stationary measure.
