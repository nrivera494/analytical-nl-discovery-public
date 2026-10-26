---
agent: gpt-a
model: gpt-6-astra
family: gpt
task: T-20261010-claude-interactive-03
problem: P-20261010-claude-interactive-01
created: 2026-10-10
status: exploration
---

# Scalar covariance reference and binary-filter bounds

The covariance-dependent binary certificates can be much tighter than the
generalized amplitude eigenvalue. However, the unrestricted linearized
optimization also exposes a serious reference-table failure mode: a formal
optimum can select virtually dark, high-frequency bins, where counting is
not described by its leading bright-field term. Propagation steps sufficient
for the classical pulse can also be insufficient for these vacuum modes.
The tables preserve these values and identify the qualifications needed
before using them to score a physical approximation.

All numerical statements in this note cite run
[`2026-10-10-gpt-a-readout-reference`](../runs/2026-10-10-gpt-a-readout-reference/meta.yaml).
The [machine-readable summary](../runs/2026-10-10-gpt-a-readout-reference/summary.json)
contains configurations, masks' coherent brightness, certificate details,
convergence residuals and code hashes. The
[numerical tables](../runs/2026-10-10-gpt-a-readout-reference/tables.md)
give every completed point and all three requested gaps in dB. Raw
covariances, masks, dual matrices and logs stay in the registered data
directory. This is exploration, not an independently audited claim.

The [proof note](2026-10-10-gpt-a-readout-hierarchy.md) states the exact
finite-dimensional bounds, including passive-port brightness conditions,
multiple modes and polarizations, mixed Raman states, binary moment/RLT
and triangle constraints, eigenvector mismatch, and approximation-error
transfer. This lane does not derive propagation formulas for a particular
dispersion regime.

## Model and configurations

The input is $A(0,t)=\sqrt{P_0}\exp[-t^2/(2T_0^2)]$. The model is scalar,
single-mode, lossless, and has instantaneous Kerr plus the specified
delayed Raman response when enabled. There is no gain, polarization,
mode coupling or self-steepening in the reference sweep. Photon energy is
the constant carrier value, consistent with this envelope/no-shock model.
The public-notebook gate below deliberately uses the notebook's different
shock, taper and photon-weight conventions.

| Family | Wavelength (nm) | $T_0$ (fs) | $\beta_2$ (ps²/m) | $\beta_3$ (ps³/m) | $\gamma$ (W⁻¹m⁻¹) | Dimensionless sampling |
|---|---:|---:|---:|---:|---:|---|
| Anomalous, SMF-28-like | 1550 | 150 | −0.0206 | 0 | 0.0013 | $N=1,1.5,2$; $z/z_0=0.25,0.75$ |
| Normal | 1030 | 100 | 0.025 | 0 | 0.004 | $N=3,6,10$; $z/(L_D/N)=0.5,1,2$ |
| Dispersionless | 1550 | 100 | 0 | 0 | 0.0013 | $\Phi=1,3,10$ |
| Near-zero, held out | 1300 | 120 | 0.0002 | 0.00012 | 0.0018 | $\Phi=3$; $L\beta_2/T_0^2=0.02315$; $L\beta_3/T_0^3=0.11574$ |

Here $L_D=T_0^2/|\beta_2|$, $N^2=\gamma P_0L_D$, and
$z_0=\pi L_D/2$. For the Gaussian input, $z_0$ is a stated length
normalization, not a claim of exact soliton recurrence. Likewise $L_D/N$
is a nominal normal-dispersion wave-breaking scale; this study does not
derive the actual wave-breaking location. The dispersionless points have
$\Phi^2L/L_D=0$. All material constants and physical lengths are in the
frozen configuration, including the held-out near-zero case.

The main grid has 512 bins in a 1.536 ps periodic window, hence 3 fs
sampling. Each point is run with and without Raman. Raman uses 300 K,
the solver's sampled Agarwal response, and the symmetrized coth reservoir
fetched verbatim from private-solver commit
`d79f150c4dabac6f461f0302eb06b1ec7900bd4e`, file
`example_notebooks/raman_bath_spectrum.jl`. Its source hash is saved.
The sampled response integral at 3 fs is 0.9942253; it is not silently
renormalized. Grid refinements halve the temporal sampling interval.

The DC reservoir correction matters for the full-field minimum even when
it does not affect counting. In `DC-reservoir-check`, removing only that
rank-one global-phase contribution changes the anomalous $N=1$, $z/z_0=0.75$
field minimum from 0.24083011 to 0.23032385, while changing the passive
minimum by less than $2\times10^{-15}$ and the amplitude block by zero.
The corresponding normal $N=3$, $z/(L_D/N)=1$ field values are 0.10552164
and 0.09832036. The fetched helper estimates the thermal DC limit from
the first nonzero frequency bin, so window convergence also checks that
approximation.

The no-shock adapter is an explicit task-local response type with its own
solver-cache methods. It preserves the sampled response and replaces the
shock/taper prefactor by constant $i\gamma$. This is not represented as
an unmodified public-default model. The solver source and pin are unchanged;
the actual private solver commit is
`b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa`.

## Covariance construction and gates

`scripts/readout_covariance.jl` propagates a complete basis of terminal
amplitude and phase quadratures backward with the public
`adjoint_mode=:discrete_rk4ip` API. Every forward run is Float64, fixed-step
RK4IP, and the adjoint uses exactly the forward step. Canonical input
vacuum contractions give $V_{\rm vac}$; independently sampled reservoir
responses give a positive Gram matrix $Y$, so $V=V_{\rm vac}+Y$.
The amplitude block gives the bin-count covariance
$\Sigma=\operatorname{diag}(\sqrt n)V^{\rm amp}
\operatorname{diag}(\sqrt n)$.

The three implementation gates passed:

- Weak power: $F=1.0000000000235632$ in `gate_weak_power`.
- Dispersionless Kerr at peak phase one: the full covariance minimum is
  0.171572883394, against $(\sqrt2-1)^2=0.171572875254$; absolute error
  $8.14\times10^{-9}$ in `pilot_kerr_phi1`.
- The notebook's supplied filter, mapped to a 3 fs grid with its public
  conventions, gives $F=0.347417005438$ from one discrete adjoint and
  $0.347417005438$ from independently assembled grouped covariance rows;
  absolute difference $3.16\times10^{-13}$ in `notebook_discrete_gate`.

The notebook gate is an agreement test on that stated grid, not a new
converged prediction for the original experiment. Every main point also
has a separate fixed-filter scalar-adjoint contraction check.

`scripts/readout_matrixfree.jl` implements the exact tangent of the same
RK4IP update and pairs it with the public discrete adjoint. A covariance
product uses one backward adjoint, the corresponding vacuum input tangent,
and all reservoir kicks propagated forward. In the two pilot gates its
products agree with dense covariance products to relative errors below
$3\times10^{-15}$. It permits longer-window and smaller-step checks without
reconstructing every matrix entry. Its Lanczos residuals are reported.
Ritz values with small residuals are numerical evidence, not rigorous
global eigenvalue enclosures.

All Julia work is serial at the process level, with two Julia threads,
one BLAS thread and one FFTW thread. The initial covariance implementation
had a Julia closure-scope race, detected by the Kerr gate. Both failed
pilot outputs are retained under `failed-*` prefixes and excluded from
the reference. Explicit worker-local bindings fixed the duplication.

## Optimization and what is certified

The initial binary search combines all-pass and singleton seeds, spectral
intervals and complements, eigenvector-threshold masks, and 96 seeded
random starts. It uses sequential improving one-bin flips and two-bin
escapes. Ordinary flip candidates have relative coherent population above
$10^{-12}$; eigenvector seeds may include fainter bins. This is a search
for a good feasible mask, not an exhaustive global search. Its tightness
is assessed against independently reconstructed lower bounds on the full
grid, including all faint bins.

The best bound combines the generalized eigenvalue, the binary
eigenvector-overlap certificate, nonnegative-vector information, and a
projective moment/RLT dual. A small-core SDP supplies one candidate dual;
a smooth minimum-eigenvalue optimizer works on the full grid. Points whose
initial gap exceeds 0.02 dB receive triangle-cut refinements on 48 bright
bins. All accepted duals are checked on the entire covariance. Core-only
lower bounds in the matrix-free calculations are explicitly labeled and
are not used as full-grid certificates.

For example, at `normal_N6_s0.5_K`, triangle cuts reduce the gap from
0.31945 dB to 0.01377 dB. At `anom_N2_z0.25_R`, the refined gap is
0.0007754 dB. These improvements exploit the binary readout constraint;
they do not require a propagation asymptotic formula.

The bound formulas are rigorous within the stated finite-dimensional
model. Their computed values use floating-point matrix eigenvalues, an
explicit downward margin and a Cholesky check. They are not interval
proofs of an exact continuum covariance. Optimizer iteration limits affect
tightness, not validity of the reconstructed nonnegative dual combination.
Exhaustive synthetic tests check the bounds, the overlap sorting and the
nonnegativity of the dual inequalities. Separate mixed-Gaussian tests
check the passive network construction and weighted shot-noise denominator.

## Faint filters and finite counting

At `anom_N1_z0.75_R`, the formal best mask passes two bins near
$\pm564.5$ rad/ps. Its coherent photon number is
$1.7436\times10^{-9}$, and its linearized value is 0.80062767.
The Gaussian number-moment diagnostic gives approximately 1.9998 for
that same mask. A bright mask gives approximately 0.9047 in that diagnostic.
The completion of the numerical covariance described below contributes
most of the change from the bright mask's linearized value 0.90418284;
the bright mask's quadratic counting correction itself is only about
$2.2\times10^{-9}$.

For an explicitly constrained family with at least $10^6$ coherent photons,
the full-grid conditional certificate is 0.90418273. The feasible bright
mask gives 0.90418284. This is a bound on the stated restricted family,
not on the unrestricted linearized minimum.

The exact Gaussian count formula uses the linear covariance plus
$|N_{ij}|^2+|M_{ij}|^2+\delta_{ij}N_{ii}$. A sub-shot linearized binary
lower bound remains a lower bound for these Gaussian counts. A faint
linearized trial value, however, need not be a physical upper value.
This distinction also applies to a passive eigenvector with vanishing
coherent overlap. Several no-Raman passive minimizers are dark to
numerical precision; balanced weighted ports avoid the particular
one-port darkness constraint.

Some finite-step covariances have small negative eigenvalues of $V+iJ$.
`scripts/readout_gaussian_counting.py` records that defect and adds the
explicit isotropic completion needed to define a nearby physical Gaussian
state. Its values are diagnostics, not silently corrected fibre predictions.
The original $V$ and all original scores are preserved. The completion is
not a proven enclosure of propagation error. Finite-array checks and
explicit small-matrix contractions passed despite floating-point warnings
from the installed numerical stack; the warnings remain in the raw logs.

## Convergence and remaining scope

The registered convergence configuration tests step, temporal sampling,
reservoir quadrature and window size on selected anomalous, normal,
dispersionless and held-out near-zero points. A fixed-mask step audit
separates changes in the propagated covariance from changes in the mask
search. An independent Kerr-only Strang tangent/transpose implementation
is also queued as a second numerical method. Final outcomes are recorded
in the summary and must be read alongside the coarse table.

The current reference does not certify a continuum optimum or include
self-steepening, general measured fibre dispersion, polarization or
multiple spatial modes. Its readout bounds do apply to covariances from
those models. A formula in material and pulse parameters still needs a
controlled covariance approximation from a propagation lane, followed by
the error transfer in the proof note. The literature search, identifiers
and access levels for this lane are recorded there.

## Numerical-method literature

Searched for the original symmetric splitting and optical-fibre RK4IP
papers on 2026-10-10, using their titles and publisher domains.

- Strang, DOI:10.1137/0705041, [publisher PDF](https://epubs.siam.org/doi/pdf/10.1137/0705041).
  **Full text**, especially pp. 510–512 on the half-step composition and
  its nonlinear second-order construction. The independent check uses
  that symmetric composition with exact linear and instantaneous-Kerr
  substeps. Its tangent/transpose implementation is given in the evaluator.
- Hult, DOI:10.1109/JLT.2007.909373,
  [publisher abstract](https://opg.optica.org/jlt/abstract.cfm?uri=JLT-25-12-3770).
  **Abstract only**; a located university PDF was inaccessible. The abstract
  reports fourth-order global accuracy for the optical RK4IP method.
  That order does not by itself certify any particular coarse noise run.
