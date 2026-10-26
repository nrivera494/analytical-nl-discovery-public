---
agent: gpt-d
model: gpt-6-astra
family: gpt
date: 2026-10-17
task: T-20261017-gpt-d-01
---

# Additional frozen RHS and Raman-grid checks

These tests are specified after the first quadratures, but before their own
execution. They do not replace the original held-out suite.

1. Evaluate the full photon-conserving GNLSE nonlinear RHS at sech inputs
   $T/\tau_1=[0.04,0.1,0.25,0.5,1,2,4,8,40,80,160]$ using silica response.
   Use $n=32768$ and window $\max(40T,40\tau_2)$; this keeps $dt<3$ fs.
   Set $\omega_0T=50$ to make the formal narrow-packet/positive-frequency
   condition uniform. These are mathematical snapshot checks, not a single
   wavelength material sweep. Predict agreement of the direct RHS derivative
   with the exact trigamma ratio within $10^{-7}$ relative; predict the fitted
   long-pulse decay exponent on $40,80,160$ is $3\pm0.02$.
2. Sample the unnormalized causal oscillator on a 1.536 ps window at
   $dt=[3,1.5,0.75,0.375]$ fs. Euler--Maclaurin predicts
   $1-dt\sum h_R=qdt^2/12+O(dt^4)$, hence exponent $2\pm0.02$.
   For a sech of width 56.7 fs, compare the energy-rate functional using this
   sampled kernel with the analytic transfer function. The leading sampling
   error in $H$ is real, so the Raman energy-rate error is $O(dt^4)$,
   with measured exponent $4\pm0.1$. Both checks are separate from production,
   which uses the exact analytic transfer function.

The original core summary's `max_photon_drift` included internal RK stages and
crossed the invariant tolerance. Accepted-plane photon drift will be extracted
from its already saved scalar trajectory; the original raw summary is retained.
Subsequent runs explicitly record both stage and accepted-plane diagnostics.
