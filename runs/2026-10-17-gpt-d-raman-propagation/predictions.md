---
agent: gpt-d
model: gpt-6-astra
family: gpt
date: 2026-10-17
task: T-20261017-gpt-d-01
---

# Frozen propagation tests

All launches below are frozen before production. Width means **intensity FWHM**;
$T=\mathrm{FWHM}/[2\operatorname{arcosh}\sqrt2]$ is the sech scale.
No predicted numerical maximum is fitted from these launches.

SMF-28 surrogate: constant $A_{eff}=64.5$ um^2, $n_2=2.6e-20$ m^2/W,
$\lambda_0=1.55$ um, $\beta_2=-0.0217$ ps^2/m,
$\beta_3=0.00012$ ps^3/m, $f_R=0.18$, $(\tau_1,\tau_2)=(12.2,32)$ fs.
These are a local constant-area/cubic-dispersion model, not a measured
broadband calibration of a specific specimen. $\gamma=n_2\omega_0/(cA_{eff})$,
$P_0=N^2|\beta_2|/(\gamma T^2)$ and $L_D=T^2/|\beta_2|$.

Core: $(N,\mathrm{FWHM}/\mathrm{fs})=(3,100)$.
Held out: $(1,30),(2,60),(4,150),(5,225),(6,300),(6,100),(1,300)$.
Length $L=3L_D/N$ for $N>1$ and $L=2L_D$ for $N=1$.
The highest-order shortest case is an envelope-model edge test, not a claim of
accurate material response throughout its generated bandwidth.

Fluoride held out: $(N,\mathrm{FWHM}/\mathrm{fs})=(3,180)$,
$\lambda_0=2$ um, $\beta_2=-0.04$ ps^2/m, $\beta_3=0.0001$ ps^3/m,
$A_{eff}=\pi(6.65/2)^2$ um^2, $n_2=4.7e-20$ m^2/W,
$f_R=0.3$, $(\tau_1,\tau_2)=(16.67,20.23)$ fs.
The Raman/index/mode-size parameter set is from the primary article
"Multi-octave spanning, Watt-level ultrafast mid-infrared source" (source details
will be logged); the two dispersion coefficients are declared surrogate choices.
This is a fluoride oscillator model test, not a measured-fiber reproduction.

Use one serial Float64 Python RK4 interaction-picture process, no field histories,
$n_t\le32768$, $dt\le0.75$ fs, fixed step with
$dz\le\min(L/4000,L_{NL}/60)$, and exact analytic $H(\Omega)$.
Monitor actual nonlinear RHS energy derivative independently of the spectral
identity at every accepted plane and every RK stage. Integrate the spectral rate
with the same RK weights. Monitor photon norm, temporal edges, spectral edges,
positive-frequency support, and $Q=\int I^2/E^2$.

Predictions: $-E'/(\kappa_UE^2)\le1+10^{-6}$, retention margin at every
plane $\ge-10^{-6}$; spectral identity residual normalized by the bound
$<10^{-5}$; integrated rate mismatch relative to energy lost $<10^{-3}$;
photon relative drift $<10^{-5}$; temporal outer-10% and spectral
outer-10% energy fractions $<10^{-6}$. Cases failing artefact tolerances are
retained and refined before used as evidence. A discrete optical-frequency
projection, if needed, is disclosed and its occupied-edge weight checked.

Convergence: core at $dz,dz/2,dz/4$ (expected RK4 errors shrink with order
near 4 once asymptotic, acceptable measured slope 3.5--5.5); held-out (6,100)
at half step, half dt at fixed window, and doubled window. Maxima and retention
must change by $<10^{-3}$ relative (or $10^{-5}$ absolute for retention).
Keep all failed results. No unannounced expansion beyond $2^{15}$ samples.

Second solver: run the core and at least one held-out launch with the pinned
agents' Julia RK4IP via its documented/evaluator low-level step interface,
using analytic response and exact shock prefactor. Relative final-energy and
maximum-ratio agreement target $10^{-4}$. This explicitly excludes the default
blue-edge prefactor window from the mathematical-model test.

Relaxation: the core with 0.2 dB/m uniform attenuation (a physically plausible
lossy specialty-fiber strength). The original lossless retention theorem is
not asserted. Test the separated Raman rate and the loss-aware comparison
$E(L)\ge E_0e^{-\alpha L}/[1+(\kappa_UE_0/\alpha)(1-e^{-\alpha L})]$.
Also test a two-positive-oscillator passive mixture (0.8 silica oscillator +
0.2 oscillator with tau1=20 fs, tau2=50 fs) against its own sum-rule constant.
The single-oscillator arctangent improvement is not used for this mixture.

No stochastic source is present. The 2026-10-16 three-start explicitly discrete
RK4IP adjoint attack remains cited prior evidence; it need not be rerun to
test the newly specified deterministic held-out suite.
