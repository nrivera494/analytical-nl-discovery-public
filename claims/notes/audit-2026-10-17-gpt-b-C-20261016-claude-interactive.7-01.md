---
agent: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-17
claim: C-20261016-claude-interactive.7-01
task: T-20261016-claude-interactive.7-07
verdict: pass-reduced-regime
status: completed
---

# Independent audit of the condensed Dirichlet law

The scalar, classical **ensemble identity is correct**. The independent
resonant-HG simulations support it in the tested disorder regimes, with much
larger finite-length uncertainty under strong disorder. They do not verify
the card's quantum reduced-state interpretation, vector/polarization
corollaries, or a universal physical-fibre equilibration length.

Clean context was maintained: the cards, problem card, permitted run metadata,
evaluator and protocol/solver documentation were read. No proposer exploration,
log, PR description or run script was read. Predictions were committed at
`dc4c5e2bdb18c7255788b04f49e7bde833fed4cd` before production. Numerical evidence
in this report is from **run `2026-10-17-gpt-b-dirichlet`**, except the explicitly
identified GGE counterchecks. Raw arrays are outside git at the location in
that run's metadata. This report records gpt-b's derivation and code.

## Exact statement and proof

Let $A_j=\sqrt{I_j}e^{i\phi_j}$ be canonical complex amplitudes, with one ground
mode of energy zero, $D=M-1$ excited gaps $e_j>0$, fixed total power $N>0$ and
fixed excitation energy $E'>0$. Assume flat complex Liouville measure
conditioned on $(N,E')$. If $\rho=E'/(N\min_j e_j)\le1$, then

$$x_j=e_j I_j/E'\sim\operatorname{Dirichlet}(1^D),\qquad
I_0=N-E'\sum_jx_j/e_j.$$

Indeed $d^2A_j=\tfrac12dI_jd\phi_j$. Integrating the power delta function over
$I_0$ leaves a constant intensity measure with $I_j\ge0$, $\sum e_jI_j=E'$,
and $\sum I_j\le N$. The last inequality follows from $\rho\le1$ and imposes
no further cut. The change to $x_j$ has constant Jacobian on $\sum x_j=1$.
This proves the distribution, without a large-$M$ or small-depletion expansion.
At $E'=0$ the excited intensities vanish and their normalized $g^{(2)}$ is
undefined; this degenerate case must not be included in that observable.

Writing $S_r=\sum_{j=1}^{D}e_j^{-r}$ gives

$$\langle I_j\rangle=\frac{E'}{D e_j},\quad
g^{(2)}_j=\frac{2D}{D+1}=2-\frac2M,\quad
g^{(2)}_{jk}=\frac{D}{D+1}\quad(j\ne k),$$
$$\operatorname{Var}I_0=\frac{E'^2(DS_2-S_1^2)}{D^2(D+1)},\qquad
\operatorname{Cov}(I_0,I_j)=-\frac{E'^2(D/e_j-S_1)}{e_jD^2(D+1)}.$$

The covariance changes sign at $e_j=D/S_1$. Cauchy–Schwarz ensures the
condensate variance is nonnegative; equal excited gaps give zero condensate
variance, despite fluctuating individual modes. $D=1$ gives a fixed excited
power and $g^{(2)}=1$. The RJ parameter $T=E'/D$ here describes the modal
means; its identification with a thermodynamic temperature depends on the
entropy convention at finite $D$.

For fluctuating $(N,E')$, use total covariance. The card's added
$\operatorname{Var}N$ is valid when $E'$ is fixed and every sampled $N$ satisfies
the condensed bound. It is not a general formula for a coherent ensemble
whose energy also fluctuates. No refutation of the explicitly sharp-energy
special case is intended.

## Independent model and what it tests

The implementation is `evaluator/thermalized_light.py` and
`evaluator/thermalized_light_core.c`. Modes are Cartesian Hermite–Gauss
functions with $q=n_x+n_y<K$, including complete degenerate groups. Their
four-function overlap is evaluated by exact-degree Gauss–Hermite quadrature,
normalized to $S_{0000}=1$, and restricted to $q_p+q_q=q_r+q_s$. The equation
is $i\partial_s a_p=\sum S_{pqrs}a_q^*a_ra_s$, with $N=1$ and $s=z/L_{\rm NL}$.
This Hamiltonian sign is used consistently for the independent full-tensor
reference; conjugation relates the opposite optical sign convention but
requires conjugating a fixed phase launch too.

The disorder is a full Hermitian Brownian matrix within each spatial group,
with $\mathbb E[dB_{ij}dB_{kl}]=\delta_{il}\delta_{jk}ds/(q+1)$ and amplitude
$\sigma$. Thus our definition is $L_d/L_{\rm NL}=\sigma^{-2}$. Each generator
flow preserves $N$ and $E'$. This normalization and full spatial-group noise
need not coincide with the proposer's realization or the polarization disorder
in Fusaro et al. The strong case is physically motivated by disorder faster
than Kerr, but is not a calibrated model of a specific measured fibre.

The flat $(N,E')$ measure is stationary under each Hamiltonian and unitary
noise flow. Its selection by an individual launch still requires mixing.
No theorem of ergodicity or spectral-gap estimate is claimed.

## Frozen tests and numerical findings

- Direct simplex sampling uses independent batches at $M=6,10,15,21,28,36$.
  The measured finite-size exponent of $2-g^{(2)}$ versus $1/M$ is
  $1.00166\pm0.00214$ (fit SE), with fitted coefficient $2.00778\pm0.01227$ against exact
  coefficient two. All means, covariances and excited-mode correlations pass
  the frozen five-batch-SE direct-sampling test. The $M=21,36$ sampling cases were held out.
- Six independent launch/disorder pairs per case test $K=5$ at
  $\rho=0.3,0.6,0.9$ and $\sigma=0.3,3$. At $\sigma=0.3$, pooled excited-mode
  $g^{(2)}$ is 1.8701, 1.8591, 1.8647, respectively, against $28/15$.
  Condensate variance divided by its exact prediction is
  $1.034\pm0.020$, $0.988\pm0.040$, $1.036\pm0.025$ (one cluster SE).
- Held-out dynamical cases $K=4,\rho=0.45$ and $K=6,\rho=0.75$ give
  $g^{(2)}=1.7862,1.9072$, against 1.8 and $40/21$. Their variance ratios are
  $0.949\pm0.039$ and $1.032\pm0.047$. All frozen moment and resolved
  covariance-sign checks pass in the $[2000,8000]$ window.
- At $\sigma=3$, the initial $[2000,8000]$ window fails a frozen moment test
  for $\rho=0.3$. This failure is retained. In the preregistered extended
  $[8000,24000]$ window all tests pass their tolerances, but the variance
  ratios are only $0.885\pm0.169$, $0.986\pm0.159$, $0.867\pm0.123$.
  Compatibility at this precision is not evidence of exact equilibration
  in every realization or of a universal short relaxation length.
- A separate held-out fixed-length ensemble has 200 independent input-phase
  draws, grouped under four quenched disorder realizations, at
  $K=6,\rho=0.75,\sigma=0.3,s=2000$. It gives mean excited $g^{(2)}$
  $1.9161\pm0.0210$ and excited cross-correlation $0.95198\pm0.00109$,
  against $40/21$ and $20/21$. However, three individual excited-mode
  correlations fail the frozen tolerance. The entire 200-draw test is therefore
  a failure despite its passing aggregate moments and covariance signs. The
larger ensemble and independently frozen new-energy holdout are reported below.
- For $K=5$ the covariance threshold lies between groups two and three.
  Every resolved group sign passes. Quantitative covariance errors can be
  relatively large near this zero: at $\rho=0.9$ the group-two covariance
  is about 30% less negative than the exact value. The numerical check of
  signs should not be represented as high-precision validation of every
  small covariance.

Uncertainties cluster by independent disorder realization; time samples are
not counted as independent realizations. The plot uses two cluster SE.
Finite-window RMS errors at durations 500–4000 have fitted exponents
$-0.643$ (mean condensate), $-0.365$ (mean excited $g^{(2)}$), and $-0.482$
(condensate variance). Cluster bootstrap intervals are broad and stored in
`summary.json`; these are sampling diagnostics, not a universal relaxation
law or an additional claimed exponent.

### Fixed-length phase follow-up

The follow-up was frozen at `b14f2de`, after the original 200-draw failure.
The enlarged 800-draw ensemble, over eight disorder realizations at the same
$K=6,\rho=0.75,s=2000$, passes every original moment and resolved-sign gate.
Its mean excited $g^{(2)}$ is $1.91561\pm0.01032$, cross-correlation
$0.95185\pm0.00056$, and condensate-variance ratio $1.05276\pm0.05092$.
All 200 original final fields are reproduced exactly by the batched
implementation; the improvement comes from added draws, not changed paths.
This enlarged sample is a post-failure diagnostic, not a new blind test.

The independently frozen fresh holdout uses $K=6,\rho=0.5,s=8000$,
400 phase draws and eight new disorder seeds. Every moment and resolved-sign
gate passes. Its mean excited $g^{(2)}$ is $1.88248\pm0.01331$, cross-correlation
$0.95360\pm0.00069$, condensate mean $0.81869\pm0.00117$, and variance ratio
$0.93441\pm0.09743$. The maximum final power and energy drifts are
$9.02\times10^{-8}$ and $3.68\times10^{-8}$. These uncertainties are one
disorder-cluster jackknife SE. The failed original sample remains in
`summary.json`; both follow-ups are in `phase_batch_summary.json`.

## Attacks, convergence and limitations

Step changes 0.04→0.02→0.01 preserve the statistical conclusion for the
central weak- and strong-disorder cases. These are ensemble tests using
separately discretized disorder paths, not pathwise convergence. Deterministic
RK4 errors against DOP853 decrease at fourth order; doubling the tensor
quadrature changes entries by less than $10^{-15}$ (pilot checks in the run).
The largest $N,E$ drifts in the original and extended disorder scans are
$3.56\times10^{-7}$ and $1.26\times10^{-7}$. No trajectory projection or
renormalization masks invariant drift.

A second implementation using the pinned agents solver commit
`b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa` agrees with the independent full-HG
DOP853 field at $s=4$: the largest field-norm difference is $7.23\times10^{-8}$
at solver step 0.002, falling to $4.90\times10^{-9}$ at 0.001. The solver uses
Float64 fixed-step RK4IP with a constant two-point temporal field and no Raman
or adjoint. This is a genuine shared-tensor implementation check, not a
long stochastic propagation by the pinned solver.

Relaxing beat averaging with the full HG tensor at
$\epsilon=(\kappa L_{\rm NL})^{-1}=0.1,0.05,0.025,0.0125$, over $s\le4$,
gives field-error powers 0.9883, 0.9880 and 0.9826 for three launches.
This supports a short-length $O(\epsilon)$ normal form. It does not control
$O(10^4)$ nonlinear lengths or the physical-fibre stationary measure.
The host BLAS emitted floating-point warnings for a matrix product; an
independent scalar contraction agreed exactly and all saved data were finite.
The warnings were investigated, not interpreted as physical singularities.

At $\rho=1.2,K=3$, cutting the simplex at $I_0\ge0$ gives excited $g^{(2)}$
about 1.60–1.62 instead of $5/3$. For two unconstrained ground components,
the measure is tilted by $I_0$: the scalar formula fails increasingly with
excited power. These attacks confirm why the condensed bound and scalar
single-ground-mode assumptions matter. They do not verify the card's
spin-constrained vector extension.

The model is monochromatic and modal: there is no temporal window, time grid,
Raman kernel, or temporal aliasing to converge. A ≤3 fs Raman-grid check is
therefore inapplicable. Spatial tensor quadrature, mode cutoff and propagation
step are the applicable checks. Raman, polarization, walk-off, gain/loss,
inter-group disorder and exact quantum dynamics remain outside the verified
statement. No adjoint or optimized physical-fibre counterexample search was
performed; this is simulation verification, not a completed promotion audit.

## Prior art and signed-off scope

Vardi, Ramos and Kottos, DOI
[10.1103/PhysRevResearch.6.043282](https://doi.org/10.1103/PhysRevResearch.6.043282),
arXiv:2409.01422 (**full text**, microcanonical and numerical sections), already
show finite-mode microcanonical departures from RJ in a different model.
The uniform-simplex oscillator law is standard; the exact mapping and the
specified covariance are the content verified here. This audit does not
certify novelty. The bounded searches and other primary sources are recorded
in `runs/2026-10-17-gpt-b-gge/literature.md`.

I sign off on the exact scalar classical measure and the tested resonant-HG
statistics at $0<\rho\le1$ under that measure, with dynamical evidence only at
the listed $(K,\rho,\sigma,s)$ values. The quantum interpretation, automatic
equilibration, and a uniform long-distance full-fibre error bound are excluded.
The dynamical checks test the listed moments, not convergence of the entire
joint phase-space density. **Status: cheap-checks-passed → sim-verified for
this narrowed statement.** This is not an `audited` promotion: a calibrated
physical-fibre adversarial search remains open in T-20261017-gpt-b-01.
