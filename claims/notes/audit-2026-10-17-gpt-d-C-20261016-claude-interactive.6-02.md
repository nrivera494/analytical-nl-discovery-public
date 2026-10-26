---
agent: gpt-d
model: gpt-6-astra
family: gpt
date: 2026-10-17
task: T-20261017-gpt-d-01
claim: C-20261016-claude-interactive.6-02
verdict: pass-reduced-regime
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
---

# Independent sharpening and verification of the Raman energy ceiling

**Verdict: pass with narrowed content and explicit regularity hypotheses.**
The identity, energy-squared ceiling and retention theorem survive. The original
inverse-square sech tightness assertion remains refuted. It is excluded from the
scope receiving audited status, not silently corrected in the original statement.
The corrected sech law and a conditional concentration bound are new GPT claims,
C-20261017-gpt-d-01 and C-20261017-gpt-d-02; the numerical work here is only
proposer checking for those claims.

## Independence and frozen tests

Before this report's initial commit I read the claim and problem cards, allowed
evaluator/solver documentation, the specifically authorized 2026-10-16 gpt-d
audit, and permitted run configurations and summaries. I did not read the
proposer's explorations, logs, PR descriptions or run implementation. Both the
Python forward implementation and the analytic calculations were written afresh.
The Julia cross-check uses the low-level RK4IP interface demonstrated in
evaluator/soliton_noise_baselines.jl, on the pinned agents' solver copy.
No original-solver repository was modified.

The initial mathematical and propagation predictions were committed in
6df0927ef31369add037f36db21643b14d68bf51 before production. A cancellation
follow-up was frozen in 3259dd5be15c597202b52436ff7d5d1918c702dc. Additional
direct-RHS and sampled-kernel checks were frozen in
ca03c40b69e09530f57de96863bab3d048df06ea. Their prediction files remain unchanged.
The latter tests are explicitly adaptive checks, not relabeled held-out cases.
The requested gpt-b literature-review comparison is deferred until this report
has been committed.

Run abbreviations in this report:

| Label | Run id |
|---|---|
| M | 2026-10-17-gpt-d-raman-sharpening |
| P | 2026-10-17-gpt-d-raman-propagation |
| Q | 2026-10-17-gpt-d-raman-conditional (derived from M and P) |
| L | 2026-10-17-gpt-d-raman-literature |

## Statement I would sign off on

Use $\widetilde f(\Omega)=\int f(t)e^{i\Omega t}dt$,
$I=|A|^2$, $E=\int I\,dt$, $\omega=\omega_0+\Omega$ and
$W(\Omega)=\Omega\operatorname{Im}H_R(\Omega)$. The deterministic scalar model is

$$\partial_z\widetilde A=iD(\Omega)\widetilde A+
i\frac{n_2\omega}{cA_{\rm eff}}\mathcal F\{A[(1-f_R)I+f_Rh_R*I]\}.$$

Assume real $D$; constant $A_{\rm eff}>0$ and $n_2f_R>0$; no gain or
linear loss; and sufficient field regularity and decay for integration by parts.
Require real causal normalized $h_R$, $h_R(0^+)=0$, finite positive
$k=h_R'(0^+)$, passive integrable $W\ge0$, and the Fourier inversion sum rule
$\int W\,d\Omega/(2\pi)=k/2$. Decay and bounded variation of $h_R'$ together
with the stated integrability suffice. A finite right derivative alone is
not substituted for these assumptions.

Then, exactly within this model,

$$\boxed{
0\le-\frac{dE}{dz}
=\frac{n_2f_R}{cA_{\rm eff}}\int W|\widetilde I|^2\frac{d\Omega}{2\pi}
\le\kappa_UE^2,\quad
\kappa_U=\frac{n_2f_Rk}{2cA_{\rm eff}},\quad
\frac{E(L)}{E_0}\ge\frac1{1+\kappa_UE_0L}.}$$

The dimensionless domain is $E/E_0>0$, $0\le\kappa_UE_0L<\infty$;
there is no restriction on soliton order, dispersion sign, or pulse duration.
Positive optical support and finite
$\mathcal N=\int|\widetilde A|^2/(\hbar\omega)\,d\Omega/(2\pi)$
give $\mathcal N'=0$ and the equivalent decreasing mean frequency.
An orthogonal frequency projection preserving the field's support is allowed.
A smooth absorbing blue-edge window changes the model and is not allowed in
this exact conservation assertion.

**Proof and attacks.** Real dispersion is skew-adjoint. Kerr gives a total
derivative. The Raman term integrates to the spectral identity. Nonnegative
intensity gives $|\widetilde I|\le E$; passivity and the sum rule give the
factor one-half and the ceiling. Integrate $(1/E)'\le\kappa_U$ for retention.
Units are $[\kappa_U]={\rm J}^{-1}{\rm m}^{-1}$. The zero-Raman limit,
phase/time translations, arbitrary real dispersion, and both oscillator
passivity signs check. An approximate delta intensity makes the constant sharp
by dominated convergence; this is a mathematical envelope-model limit, not
a subcycle material prediction. The full independent proof is in
[the proof note](proof-2026-10-17-gpt-d-raman-sharpening.md).

## Propagation evidence and errors

P contains a core, eight frozen held-out launches, five refinements and two
assumption relaxations. SMF-28 parameters denote a local constant-area,
cubic-dispersion surrogate, not a measured broadband specimen. The fluoride
Raman/index/mode-size parameters are from Butler et al., DOI
10.1088/2515-7647/ab4976 (full text, relevant ZBLAN section and table read);
its dispersion here is explicitly a surrogate. Width below means intensity
FWHM; the sech scale is $T={\rm FWHM}/(2\operatorname{arcosh}\sqrt2)$.

| Material, launch | Held out | Length (definition) | Largest accepted-plane $\rho$ | $E(L)/E_0$ | Retention lower bound |
|---|---|---|---:|---:|---:|
| Silica, $N=3$, 100 fs | no | $L_D$ | 0.22966842 | 0.95296272 | 0.63213680 |
| Silica, $N=1$, 30 fs | yes | $2L_D$ | 0.15296830 | 0.99482544 | 0.96265316 |
| Silica, $N=2$, 60 fs | yes | $3L_D/2$ | **0.31037732** | 0.96940123 | 0.81117841 |
| Silica, $N=4$, 150 fs | yes | $3L_D/4$ | 0.16068382 | 0.94098076 | 0.46213452 |
| Silica, $N=5$, 225 fs | yes | $3L_D/5$ | 0.11316019 | 0.92944389 | 0.31424206 |
| Silica, $N=6$, 300 fs | yes | $L_D/2$ | 0.08380161 | 0.91982103 | 0.22263700 |
| Silica, $N=6$, 100 fs | yes | $L_D/2$ | 0.08513644 | 0.94479627 | 0.46213452 |
| Silica, $N=1$, 300 fs | yes | $2L_D$ | 0.00011670 | 0.99995478 | 0.72048322 |
| ZBLAN, $N=3$, 180 fs | yes | $L_D$ | 0.10255044 | 0.93582636 | 0.36117774 |

All table numbers trace to P/config.yaml and P/summary.json; $L_D=T^2/|\beta_2|$.
The primary suite covers $1\le N\le6$, $1.395\le T/\tau_1\le13.950$,
$20.68\le\omega_0T\le206.83$ and zero linear loss. This is the tested subset,
not an extra mathematical theorem restriction. Nonlinear evolution includes
compression and breakup: the final $N=6$, 100 fs profile has five prominent
intensity lobes under the recorded diagnostic, not a claimed eigenvalue count.

The identity was checked against the **actual nonlinear RHS**, independently
of its spectral formula, at every accepted plane and internal RK stage:
36,011 primary accepted planes and 144,017 primary RHS evaluations. The
largest primary accepted-plane ratio is 0.3103773218; including internal
stages it is 0.3103787029. No negative Raman rate, energy increase on an
accepted plane, rate-bound violation or retention violation was found (P).
The largest direct identity residual divided by the bound is $5.59\,10^{-14}$;
largest integrated-identity relative mismatch is $1.36\,10^{-6}$ (P).

The constant from the declared silica material parameters is
$\kappa_U=9.31224924\,10^{-4}\ {\rm pJ}^{-1}{\rm m}^{-1}$ (P), agreeing with
the original rounded $9.31\,10^{-4}$. The prior audit used a different
carrier/material configuration and quoted $9.31031320\,10^{-4}$; its precise
value is not reused as though the two configurations were identical.

Convergence and artifact checks (P, and M/followup_summary.json):

- Core step, half-step and quarter-step runs give measured integrated-balance
  error order 4.972 and accepted-plane photon-drift order 4.465, within the
  frozen 3.5--5.5 interval. The bound is exact, so these are integrator-error
  exponents, not a physical asymptotic correction to the inequality.
- Held-out $N=6$, 100 fs: halving step changes maximum $\rho$ by
  $1.94\,10^{-6}$ relative and retention by $8.29\,10^{-8}$ absolute.
  Halving time spacing and doubling the time window change retention by at
  most $1.30\,10^{-12}$ absolute and maximum $\rho$ by $2.42\,10^{-14}$
  relative. Temporal outer-10% energy stays below $5.87\,10^{-9}$ in the
  primary suite; spectral outer-10% weight stays below $1.84\,10^{-18}$.
- Production uses the exact transfer function on $dt\le0.75$ fs grids.
  A separate sampled-kernel test at $dt=3,1.5,0.75,0.375$ fs gives
  normalization-error exponent 2.00026 and Raman-rate-error exponent 4.00215.
  It exposes the finite-grid normalization error rather than hiding it by
  renormalization. The analytic transfer's continuum tail is not renormalized.
- The orthogonal cutoff is $\omega>0.02\omega_0$. Occupied energy below
  $0.1\omega_0$ never exceeds $9.02\,10^{-11}$ (P). This and the direct
  identity/grid checks make the support cutoff negligible for these launches.
- Pinned Julia RK4IP core/held-out final energy fractions agree with Python
  within $1.04\,10^{-10}$ absolute, and maximum ratios within $2.84\,10^{-6}$
  relative. Julia maxima evaluate the spectral identity on Julia fields;
  the separate direct-RHS identity test is the Python check. Julia used
  4,000 steps versus 4,001 in these Python cases, explaining small differences
  in the sampling of maxima. Both Julia numerical runs finished and wrote
  results; the surrounding macOS time utility exited nonzero because its
  memory-statistics sysctl was denied. No measured peak RSS is claimed.

**Retained diagnostic failure.** The first core summary classified photon
drift using intermediate RK stages and exceeded the invariant tolerance.
Stages are not accepted solutions. The raw failed summary is retained.
The separately frozen reanalysis extracts accepted-plane drift from the
already saved scalar trajectory: $3.57\,10^{-10}$ for the core and at most
$5.42\,10^{-8}$ in the primary suite (P). The aggregate contains both the
original flag and the correctly identified accepted-plane diagnostics.

**Relaxed assumptions.** A core run with 0.2 dB/m uniform attenuation obeys
the separately derived comparison
$E(L)/E_0\ge e^{-\alpha L}/[1+\kappa_UE_0(1-e^{-\alpha L})/\alpha]$,
and its Raman-only rate still obeys the ceiling. This is not an assertion
of the lossless theorem in a lossy fiber. A two-positive-oscillator response
also obeys the core bound using its own $k$; its maximum accepted $\rho$ is
0.23865675 (P). The arctangent claim is not applied to this mixture.
The earlier frequency-dependent-area audit remains relevant: an appropriate
transformed norm is needed, and the unweighted energy-squared extension is
not asserted (2026-10-16-gpt-d-c02-area).

**Optimization attack.** The permitted prior audit contains a three-start
phase-mask search using the explicitly selected discrete-RK4IP adjoint,
Float64 fixed-step forward, and a finite-difference gradient check. It found
no violation and reached integrated objective 0.865773
(2026-10-16-gpt-d-c02-adjoint and 2026-10-16-gpt-d-c02-mask-fine-shaped).
This is cited prior evidence, not a new adjoint run. No noise source was used.

## New content: sech ratio, with retained finite-range failure

For $a=1/\tau_2$, $b=1/\tau_1$, $s=(a-ib)T$ and the normalized oscillator,
the proposed exact result is

$$\rho=\operatorname{Re}\!\left[(1+ia/b)
\left(1-s+\frac{s^2}{2}\psi_1(1+s/2)\right)\right].$$

For a general response with $\mu_j=\int t^jh_R(t)dt$, finite absolute fifth
moment, and $k=h_R'(0^+)$,

$$\rho=\frac{8\mu_1}{15kT^3}-\frac{16\mu_3}{63kT^5}+R,\qquad
|R|\le\frac{16\mu_{5,\rm abs}}{225kT^7}.$$

For the oscillator, $r=\tau_1/\tau_2$, $x=T/\tau_1$:

$$\rho=\frac{16r}{15(1+r^2)^2}x^{-3}
\left[1+\frac{40(1-r^2)}{7(1+r^2)^2}x^{-2}+O_r(x^{-4})\right],
\qquad 1-\rho=2rx+O_r(x^2).$$

The closed form, spectral quadrature and direct GNLSE RHS agree. Maximum
quadrature relative difference is $7.84\,10^{-16}$ on five response ratios,
including three frozen held-out ratios (M). Direct RHS error is below
$9.06\,10^{-12}$ on the frozen snapshot suite with $\omega_0T=50$.
These snapshots vary the carrier to stay in a formal positive-frequency
envelope regime; their near-saturation $\rho=0.96880762$ is not a physical
fixed-wavelength propagation maximum (M).

For silica, the long decay exponent is 3.00158, the leading relative-error
exponent 2.00170, and the corrected relative-error exponent 4.00091. The
extrapolated dimensionless coefficient is $0.30999923$, with fit-window
sensitivity $2.13\,10^{-7}$, versus exact $0.30999947$. This sensitivity is
not a statistical confidence interval. The short-gap exponent is 1.00390;
its extrapolated coefficient is 0.762500043 with fit-window sensitivity
$3.38\,10^{-8}$, versus exact 0.7625 (M).

One original held-out tolerance failed: at $r=0.6$ the residual from the
linear short approximation has slope 2.08200, outside $2\pm0.08$. Its
quadratic coefficient is small near $r=1/\sqrt3$. The subsequent frozen
smaller-$x$ test gives 2.01144, and after subtracting the quadratic term the
slope is 2.99929; the predicted cubic coefficient agrees to
$6.09\,10^{-8}$ relative. The original failure remains in the record
(M/followup_summary.json). No universal finite-window exponent is claimed
near coefficient cancellations.

## New content: conditional concentration ceiling

For the single oscillator and $Q=\int I^2dt/E^2$,

$$\rho\le F(Q)=\frac2\pi\arctan\!\left(\frac{\pi\tau_2Q}{2}\right)
<\min(1,\tau_2Q),\qquad 0<Q<\infty.$$

The proof maximizes the Raman spectral overlap subject to
$0\le|\widetilde I|^2/E^2\le1$ and its fixed integral $Q$. It is a
sharp bound in that relaxed spectral problem, not a proven attainable
physical-intensity bound. A separately justified cap $Q(z)\le Q_*$ gives
retention $[1+\kappa_UE_0LF(Q_*)]^{-1}$. Neither $Q$ nor peak power is
assumed conserved or monotone; this is not a launch-only fission theorem.

Level-set quadrature agrees to $1.34\,10^{-13}$ relative. All 82 frozen
profile checks pass, with largest $\rho/F=0.98012330$. All primary
propagation planes pass, with maximum $\rho/F=0.50200193$ (Q, derived from
M and P). On the core trajectory, the original retention bound 0.632137
becomes 0.755777 using the observed concentration maximum, or 0.840231
using its path integral; actual retention is 0.952963. These postcomputed
comparisons are not certified a priori caps between all continuum planes.

## Prior work, blockers and limitations

The source ledger and search strings are in L. Bonetti et al.,
DOI 10.1364/JOSAB.377891 (full text read, equations visually checked),
already derive the photon-conserving model and describe energy decrease.
The general spectral identity and energy-squared/retention inequalities
were not explicitly found in their displayed equations; the core here
is an elementary corollary of that model.

Huang et al., arXiv:2607.05244 (full text, relevant energy/bright-soliton
sections read), equation (18) explicitly gives the long-pulse
$E^2/T^3$ energy-loss law. The corrected exponent is therefore published
physics. Nordebo and Stumpf, arXiv:2402.04806 (full text, passive-system
representation and sum-rule sections read), establish the standard
positive-measure/sum-rule method behind such response bounds.

Hollenbeck and Cantrell, DOI 10.1364/JOSAB.19.002886 (full text, response
and gain sections read), and Lin and Agrawal, DOI 10.1364/OL.31.003086
(abstract only), show why a single oscillator is an approximation for
silica. Nie et al., arXiv:2511.04013 (full text, main theory and
supplementary I.1--I.3 read), address related nonadiabatic short-pulse
SSFS, but the reviewed derivation does not supply the exact trigamma
ratio or the concentration inequality. Gordon,
DOI 10.1364/OL.11.000662 (abstract only), remains a full-text comparison
gap. Thus **novelty is unestablished**, not inferred from absent search hits.

There is no remaining blocker to auditing the explicitly narrowed core.
The two new claims still need independent Claude-family verification.
No assertion is made of calibrated subcycle silica physics, a measured
broadband SMF-28 or fluoride prediction, a universal multimode/variable-area
extension, or a launch-only concentration cap. No result is promoted.
The PI's explicit sharpening assignment was followed despite the problem
card still being candidate; proposed card updates belong in the log.

## Post-commit comparison with gpt-b's review

The independent report above was committed and pushed as
bcecbc639d49b69ddfee93d8e4c4ff45c1bc8768aa before reading the requested
[gpt-b review](../../docs/review-2026-10-16-gpt-b-supercontinuum-literature.md),
specifically its long-wave/IR section. It already gives the same exact spectral
energy identity and the conditional peak/supremum-weight inequality
$-E'\le C\,(\sup W)P_{\max}E$, where $C=n_2f_R/(cA_{\rm eff})$.
For the oscillator, $\sup W=k\tau_2/2$, so its normalized form is
$\rho\le\tau_2P_{\max}/E$. The proposed arctangent peak version is strictly
smaller, but still needs a propagated-peak or concentration cap for an a priori
finite-length improvement. Thus it does not resolve the review's stated
dynamical-closure gap. The review also agrees that passivity is stronger than
causality, frequency-dependent area needs a different model, and surviving
photon means under selective loss need a covariance term.

This comparison changes neither the independent verdict nor the two new
claims' unverified status. Follow-ups: T-20261017-gpt-d-02 (sech law,
Claude verification), T-20261017-gpt-d-03 (concentration inequality,
Claude verification), T-20261017-gpt-d-04 (original-text prior art), and
T-20261017-gpt-d-05 (realistic response/area and dynamical closure).

A final targeted search also located Herrmann and Nazarkin,
DOI 10.1364/OL.19.002065 (publisher abstract only): their short-pulse
soliton frequency-shift rate is inverse in duration. This is direct prior
work on the crossover, not evidence that this physical regime is new.
Full text could not be retrieved, so equivalence of its exact coefficients
to the normalized expression here remains part of T-20261017-gpt-d-04.
