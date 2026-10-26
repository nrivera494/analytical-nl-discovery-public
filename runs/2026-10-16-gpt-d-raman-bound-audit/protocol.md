---
agent: gpt-d
model: gpt-6-astra
family: gpt
claim: C-20261016-claude-interactive.6-02
---

# Independent protocol

No proposer code, notes, logs, PR descriptions or branch history will be read before the independent report is committed. Only the claim/problem cards, solver documentation and cited run metadata/summary have been consulted. The held-out metadata resolves the ambiguous “100 fs” label: it is an intensity FWHM; the sech widths are 56.7 fs and 170.2 fs.

## Predictions frozen before independent calculations

For the stated Fourier sign, integration by parts gives the claimed negative energy derivative. The real linear dispersion contributes zero. With positive spectral weight W = Omega Im H, the triangle inequality for the transform of nonnegative intensity gives the E-squared bound and its integrated retention inequality. A finite positive photon norm and real dispersion are understood; the coefficient requires nonnegative n2 fR.

For a damped oscillator, set a=1/tau2 and b=1/tau1. Then W = 2a(a²+b²)Omega²/[(a²+b²-Omega²)²+4a²Omega²] is nonnegative. Its integral divided by 2 pi is (a²+b²)/2. This independently predicts the half factor in kappa_U.

For a sech-squared intensity of arbitrary energy, the rate-to-bound ratio is predicted to approach 16a/[15(a²+b²)² T³] for long pulses. The card's T^-2 statement is therefore suspect: the integration bandwidth supplies an additional inverse power of T. Fit widths from 10 to 100 Raman times, then a farther asymptotic subset. At short widths, the predicted leading saturation gap is 2T/tau2, so its exponent should approach one. Freeze these predictions before numerical quadrature or pulse propagation.

Reproduce the specified fundamental-model constant, core N=3 launch and all three lossless held-out launches, using an independent RK4IP implementation. Accumulate the energy identity at every RK stage instead of inferring its integral from sparsely saved output. Record actual RHS energy rate separately, to detect aliasing rather than automatically enforcing the identity being checked.

The auditor's additional held-out field is a coherent pair of short Gaussian pulses with a spectral chirp, specified in its config. This is outside a sech/soliton ansatz but within the claimed arbitrary-field model. It must satisfy the bound and retention inequality at every saved plane.

Use analytic Raman transforms and grids no larger than 16384 initially. If high-order compression requires a larger grid to refine time spacing while retaining the time window, a single 32768-point convergence test is allowed and its necessity will be recorded. Store initial/final fields only. Keep every failed or aliased pilot. Gate every heavy launch at the required free-memory threshold.

Relax constant area with the photon-conserving transformed field. Check the correct identity with its weighted intensity and the corrected bound based on that field's norm. Use fixed Float64 RK4IP and explicitly matched discrete RK4IP adjoints for a three-start spectral phase search of the short-pulse energy-loss ratio. A local search cannot certify a global shaping ceiling.
