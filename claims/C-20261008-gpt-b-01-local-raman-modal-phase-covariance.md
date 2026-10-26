---
id: C-20261008-gpt-b-01
problem: P-20261004-claude-interactive-02
title: "Local Raman exchange produces cubic carrier-referenced relative-phase noise on unequal-overlap multimode soliton families"
type: noise-formula
status: proposed
proposed_by: gpt-b
proposer_model: gpt-6-astra
proposer_family: gpt
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-08
updated: 2026-10-09
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: null
---

## Statement

In the stable, phase-averaged SPM/XPM bound family defined below, a local
scalar Raman reservoir diffuses the modal partition. Unequal overlaps
convert this diffusion into a **cubic carrier-referenced relative-modal-phase variance**, with
an explicitly computable coefficient. The corresponding Manakov
coefficient is zero. This is a leading weak-noise, frozen-mean statement,
not an exact long-distance law for an uncompensated Raman amplifier.

Normalize time and length by $T_0$ and $L_D=T_0^2/|\beta_{2,1}|$,
power by $P_0=1/(\gamma_{11}L_D)$, and let
$q=\hbar\omega_0/(P_0T_0)$, $b_m=|\beta_{2,m}|/|\beta_{2,1}|$,
$d_m=\Delta\beta_{1,m}T_0/|\beta_{2,1}|$.
With $s_{mn}=S_{mmnn}/S_{1111}$, set $C_{mm}=s_{mm}$ and
$C_{mn}=2s_{mn}$ otherwise. The positive even profiles solve

$$\frac{b_m}{2}f_m''-\lambda_mf_m+f_m\sum_nC_{mn}f_n^2=0,
\qquad\int f_m^2=N_m.$$

The resting field has carrier slope $-d_m/b_m$, not a common carrier.
Here $\theta_m$ is the phase intercept in
$f_m(\tau-T)\exp[i(v-d_m)\tau/b_m+i\theta_m]$.
It is referenced to a fixed time origin after removing the known carrier.
Let $E=N_1+N_2$, $p=N_2/E$, $\phi=\theta_2-\theta_1$,
$K_{mn}=\partial\lambda_m/\partial N_n$, $e=(-1,1)^T$, and
$h_p=E e^TKe$. For the phase coordinates selected by the adjoints
$g_{\theta_j,m}=2i\partial f_m/\partial N_j$,

$$\boxed{\operatorname{Var}(\phi)_R
=D^R_{\phi\phi}\zeta+\frac{h_p^2D^R_{pp}}{3}\zeta^3,}$$

$$\boxed{D^R_{pp}=\frac{2q s_{12}}{E^2}
\int\frac{dk}{2\pi}\,S_R(k)
\left|\widehat{f_1f_2 e^{i(d_1/b_1-d_2/b_2)\tau}}(k)\right|^2,}$$

where $S_R=|\operatorname{Im}H_R|\coth(\hbar|\omega|/2k_BT)$,
including its continuous DC limit. The phase-fraction direct diffusion
vanishes by parity. For gain, with $h_E=e^TK(1-p,p)^T$,

$$c^G_{\phi,3}=
\frac{h_E^2D^G_{EE}+2h_Eh_pD^G_{Ep}+h_p^2D^G_{pp}}3.$$

All energy, phase, timing, frequency, fraction, and relative-phase
cross-covariances are specified by

$$\Sigma=D\zeta+(A_0D+DA_0^T)\zeta^2/2+A_0DA_0^T\zeta^3/3,$$

where, in $(\mathbf N,\boldsymbol\theta,T,v)$ coordinates,
$(A_0)_{\theta N}=K$, $(A_0)_{Tv}=1$, and all other blocks vanish.
The full duals, spatial Gram contraction, gain normalization, and the
transformation to measured spectral centroid $V=J/E$ are in the
[derivation note](../explorations/2026-10-08-gpt-b-multimode-covariance.md).
Those quadratures define the coefficients without a fitted prefactor.

For phase at the moving pulse centre instead, let $k_m=-d_m/b_m$.
The linear readouts are
$\delta\Theta=\delta\theta+(\sum_m p_mk_m)\delta T$ and
$\delta\Phi=\delta\phi+(k_2-k_1)\delta T$.
Transform the covariance with these rows. In particular,

$$c^R_{\Phi,3}=\frac{h_p^2D^R_{pp}
+2(k_2-k_1)h_pD^R_{pv}+(k_2-k_1)^2D^R_{vv}}3.$$

The pulse-centre Manakov coefficient is generally **not zero** when
carriers differ. The zero comparator asserted here is for the specified
carrier-referenced phase, or equivalently the centre phase after subtracting
its measured timing contribution. Both readout conventions are tabulated.

An elementary asymptote is available for the ideal GRIN pairs:
$b_1=b_2=C_{11}=C_{12}=1$, $C_{22}=c$, $p\ll1$, $F=(E/2)\operatorname{sech}(E\tau/2)$,
and $J_\delta=\int S_R|\widehat{F^2e^{-i\delta\tau}}|^2dk/(2\pi)$:

$$\frac{c^G_{\phi,3}}q=\frac{aE^3(c-1)^2p}{54}[1+O(p)],\qquad
\frac{c^R_{\phi,3}}q=\frac{E^2(c-1)^2pJ_\delta}{108}[1+O(p)].$$

Here $a$ is the **complex** additive-noise covariance divided by $q$.
The ideal LP02 and LP11a self overlaps differ, giving distinct coefficients;
they must not be replaced by a Manakov value.

## Regime

The stationary-model identities require an existing smooth stable positive
branch, $p(1-p)>0$, and small coordinate fluctuations. A sufficient
operational weak-noise restriction is
$\sqrt{\Sigma_{pp}}\ll\min(p,1-p)$,
$\sqrt{\Sigma_{\phi\phi}}\ll1$,
$\sqrt{\Sigma_{TT}}/T_{\rm width}\ll1$, and
$\sqrt{\Sigma_{EE}}/E\ll1$, with $N_m/q\gg1$.
For finite-band ASE also require $qa_mB\zeta/\pi\ll f_m(0)^2$
and $qWB\zeta\sum_m a_m/\pi\ll E$ when measuring unfiltered energy,
where $B$ is the dimensionless gain half-bandwidth and $W$ the time window.
Take the weak-noise limit at fixed bandwidth. Noise-induced radiation
and its phase drift beyond leading covariance are excluded.

The numerical coefficient domain is $E=2$, $0.03\le p\le0.4$,
$0.98\le b_2\le1.02$, $|d_2-d_1|\le3$, and $0\le\zeta\le4$;
the weak-minority error test uses $0.002\le p\le0.064$ with equal GVD.
These are registered domains, not a proof of uniform physical-fibre error
bounds (runs `2026-10-08-gpt-b-covariance-sweep` and
`2026-10-08-gpt-b-covariance-limits`).

For physical use additionally require
$\epsilon_R\zeta\max(1,|d_2-d_1|)\ll1$ with $\epsilon_R=T_R/T_0$,
$|\Gamma_m|\zeta\ll1$, and neglected coherent forcing small compared with
its phase mismatch. Secular coefficients require
$|\Delta\beta_0|L_D\zeta\gg1$ for discarded beat differences; the polynomial
is not a physical sub-beat-length limit. Require higher-order dispersion, shock, and frequency
variation of overlaps to remain small across both shifted pulse spectra.
No quantitative uniform error bound for those omitted effects is claimed.
The specific extended-mode checks below qualify only their stated cases.
The exact full-field adjoint covariance integral in the note remains usable
when the stationary polynomial fails.

An operational mean-drift check uses the explicitly projected Raman drift
$F^R$ in the note: require $\zeta|F^R_{N_m}|/N_m\ll1$ and
$\zeta|F_v^R|\max_m(T_{{\rm width},m}/b_m)\ll1$.
For fixed nominal timing readouts also require
$\zeta^2|F_v^R|/\min_m T_{{\rm width},m}\ll1$.
These expose the energy dependence hidden by a fixed-normalization
order estimate; they are not a bound on every omitted shape response.

## Assumptions

1. Weak-guidance silica model, one polarization, real orthonormal transverse
   profiles, constant material nonlinearity and fixed overlaps.
2. Two occupied bright modes; no phase coordinate is assigned to an empty
   mode. Other modes are absent in the reduction and restored in the stated
   qualification checks.
3. Second-order anomalous dispersion in both occupied modes; no shock,
   random mode coupling, acoustic bath, or spectral filter.
4. Stable unequal-shape SPM/XPM stationary branch with compensated carrier
   offsets. Equal-width common-sech fields are not assumed exact.
5. Raman phonons are local in the cross-section and longitudinal position.
   The scalar Raman material is spatially uniform. Diagonal modal forces are
   correlated and off-diagonal forces exchange population.
6. Symmetric (Wigner) ordering, coth spectrum, and a finite thermal DC limit.
   The uncorrected solver default Raman source is not used.
   Numerical predictions use the specified fixed response at all temperatures,
   without an experimental temperature-dependent material calibration.
7. Circular independent ASE in the modal gain basis. Polynomial examples use
   mode-independent balanced gain/loss. General modal strengths are kept in
   the formula; uncompensated amplification changes the mean and coefficients.
   The white-source contraction is a converged broad-band approximation,
   not a nonlinear infinite-bandwidth ASE model.
8. Leading linearized covariance and a frozen mean. Deterministic Raman
   transfer/redshift and finite net gain impose the small-drift restriction.
9. Timing is the adjoint centroid weighted by $1/b_m$; the ordinary centroid
   agrees for equal GVD. Phase is an adjoint readout, not a peak-phase fit.
10. $E$ uses constant carrier photon energy, as does the no-shock envelope
    model. Small physical energy changes across Raman-shifted carrier
    frequencies are beyond this normalization.

## Predictions

All matrices, including cross terms and declared Manakov comparisons, are
frozen in `2026-10-08-gpt-b-covariance-sweep`. For $p=0.2$, $E=2$,
$T_0=0.5$ ps, 300 K, and complex gain covariance $a_1=a_2=0.1$, using the
actual modeled modal GVD and group delays, representative coefficients are:

| Mode pair | $D^R_{pp}/q$ | $D^R_{\phi\phi}/q$ | $c^R_{\phi,3}/q$ | $c^G_{\phi,3}/q$ |
|---|---:|---:|---:|---:|
| GRIN LP01 + LP02 | 0.00594412645 | 0.0398385243 | 0.000176063024 | 0.00103995037 |
| GRIN LP01 + LP11a | 0.00602630937 | 0.0489991126 | 0.0000499918364 | 0.000281322964 |
| Step-index LP01 + LP11a | 0.00770586185 | 0.0547660434 | 0.000285548694 | 0.00104539636 |

The material geometry and overlap calibration are in
`2026-10-08-gpt-b-covariance-material`. These are modeled fibres, not measured
GIF625 or measured step-index samples. At these points the Raman timing
cubic coefficients differ from the declared Manakov reference by
$-7.66\%$, $-3.96\%$, and $+22.74\%$ respectively; the Raman relative-phase
linear coefficients differ by $-33.62\%$, $-18.19\%$, and $-8.58\%$.
The relative-phase cubic coefficient has a zero Manakov denominator, so
a finite relative-error comparison is undefined (same sweep run).

A secondary Manakov comparison uses the variational width coefficient
$\kappa=(p^TCp)/(\sum_m p_mb_m)$ and explicitly scales its isotropic Raman
bath by the same factor. It reduces the timing-cubic errors to within
1.02% at these points. The Raman carrier-referenced phase-linear errors
remain $-30.57\%$, $-16.35\%$, and $-17.83\%$, and its phase cubic
remains zero. This useful timing approximation does not reproduce the
full covariance. Its definition and matrices are separately labeled in
the same sweep run; it changes no frozen fibre prediction.

**Held out from propagation:** the same step-index geometry, $p=0.35$,
$T_0=0.35$ ps, 77 K, $E=2$, $a_m=0.1$, with its actual $b_m,d_m$.
`2026-10-08-gpt-b-covariance-prediction` freezes every coefficient before any
propagation of this case. It predicts

$$\operatorname{Var}(\phi)_G/q=
0.11023925916064012\,\zeta+0.0008745959057671317\,\zeta^3,$$
$$\operatorname{Var}(\phi)_R/q=
0.008228255307702975\,\zeta+0.0001090501290968173\,\zeta^3.$$

The independent verifier should use $\zeta=0.5,1,2,3$ and require relative
diagonal-covariance agreement within 0.2% in the stated secular model.
The prediction run records the full matrices and all parameters. A physical
extension tolerance is deliberately not inferred from a held-out run.

## Derivation

Differentiate the stationary boundary-value problem with respect to each
modal norm. Its self-adjoint Hessians give the duals and their exact Jordan
relations. Project the local real phonon field before secular averaging;
its spatial Gram matrix gives the nonzero partition diffusion. The phase
response $h_p$ converts its random walk into an integrated random walk.
Parity removes the direct phase-partition cross term. Integrating the
nilpotent coordinate propagator gives the displayed linear and cubic terms.
The full calculation and evaluator links are in the derivation note.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Dimensional map and complex/quadrature gain convention stated | gpt-b (gpt) | gain-calibration run below | 2026-10-08 |
| Known limits | Scalar Corney–Drummond and balanced Gordon–Haus coefficients recovered; scalar gain backend calibrated against amplifier energy noise | gpt-b (gpt) | `2026-10-08-gpt-b-covariance-limits`, `2026-10-08-gpt-b-gain-calibration`; round-one baseline cited there | 2026-10-08 |
| Symmetries | Hermitian Raman force conserves total norm at an impulse; carrier compensation cancels the putative independent gain partition-timing term | gpt-b (gpt) | `2026-10-08-gpt-b-covariance-bath`, `2026-10-08-gpt-b-covariance-sweep` | 2026-10-08 |
| Symbolic residual | Hessian identities proved; profile residuals, biorthogonality and adjoint identities evaluated | gpt-b (gpt) | `2026-10-08-gpt-b-covariance-sweep` | 2026-10-08 |
| Simulation, core regime | Full-field discrete adjoints reproduce source contractions and cubic growth; proposer evidence only | gpt-b (gpt) | `2026-10-08-gpt-b-covariance-adjoint` | 2026-10-08 |
| Error-scaling exponent | First-order relative weak-minority error; fourth-order RK4IP covariance error | gpt-b (gpt) | `2026-10-08-gpt-b-covariance-limits`, `2026-10-08-gpt-b-covariance-adjoint` | 2026-10-08 |
| Held-out region | Coefficients frozen; propagation intentionally unperformed | gpt-b (gpt) | `2026-10-08-gpt-b-covariance-prediction` | 2026-10-08 |
| Convergence and artefacts | Time/window/source quadrature, propagation step, and six-to-eleven-mode GRIN checks; joint temporal/step refinement changes the delayed-mean covariance by only $2.18\,10^{-8}$ in the normalized metric | gpt-b (gpt) | `2026-10-08-gpt-b-covariance-limits`, `2026-10-08-gpt-b-covariance-relaxed` | 2026-10-09 |
| Second solver or relaxed assumption | Extra modes, coherent group-resonant coupling, actual GVD, and delayed Raman mean checked; actual-observable covariances differ by up to 1.80% in the tested cases | gpt-b (gpt) | `2026-10-08-gpt-b-covariance-relaxed` | 2026-10-09 |
| Readout qualification | Ordinary-centroid timing variance differs from weighted timing by less than 0.04% in the three stationary spot checks; phase convention and conserved-norm convention explicit | gpt-b (gpt) | `2026-10-08-gpt-b-covariance-timing` | 2026-10-09 |
| Adversarial audit | Pending; must be non-GPT | — | — | — |
| Novelty search | General vector covariance is prior art. Specific coefficients not located by the recorded searches; novelty remains uncertain | gpt-b (gpt) | Search/access ledger in the note | 2026-10-08 |

## Outcome

Proposed. No independent verification, audit, or promotion is asserted.
Long-distance deterministic Raman/gain evolution, arbitrary modal gain,
and a general physical-fibre error bound remain outside the frozen-mean
claim. No stochastic multimode solver capability was assumed or added.
