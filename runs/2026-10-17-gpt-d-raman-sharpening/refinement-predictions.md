---
agent: gpt-d
model: gpt-6-astra
family: gpt
date: 2026-10-17
task: T-20261017-gpt-d-01
---

# Frozen follow-up after the first quadrature

The original predictions and results are retained. At held-out $a/b=0.6$,
the fitted short linear residual exponent is 2.08200364, just outside the
frozen $2\pm0.08$ window (`2026-10-17-gpt-d-raman-sharpening`). Its quadratic
coefficient is small near $a/b=1/\sqrt3$, so the cubic term can affect this
finite-range slope. This is not a failed exact formula (independent quadrature
agrees), and the original leading saturation-gap prediction passes.

Before follow-up: freeze $T/\tau_1=[0.00025,0.0005,0.001,0.002]$ at $a/b=0.6$.
Predict the linear-residual exponent is $2\pm0.02$, and subtracting also the
quadratic term gives exponent $3\pm0.03$. The analytic cubic coefficient of
$\rho$ is $2r(1-r^2)\zeta(3)$ in these dimensionless units. Compare it to
extrapolated residuals to 0.1%. This is an adaptively selected convergence
test, not a fresh held-out test.
