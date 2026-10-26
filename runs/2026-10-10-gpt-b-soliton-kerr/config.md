# Configuration

agent: gpt-b; model: gpt-6-astra; family: gpt.

Ideal coherent fundamental soliton of the scalar focusing NLSE. Vacuum
quadrature covariance is one, $x=t/T_0$, $\zeta=z|\beta_2|/T_0^2$.
The numerical matrix generator is defined in `scripts/soliton_fano_theory.py`;
the independent exact continuum formulas are in `scripts/soliton_jost_filter.py`.
There is no nonlinear propagation or Raman noise in the Kerr runs.

Use `~/agent-work/venv/bin/python`, with `OPENBLAS_NUM_THREADS=2`,
`VECLIB_MAXIMUM_THREADS=2`, and `OMP_NUM_THREADS=2`.

- `soliton_fano_theory.py --n 256 --window 40 --z 0 1 2 3 4 4.71238898038469 6 8 --raw <raw>/pilot`
- `soliton_fano_theory.py --n 512 --window 80 --z 1 2 3 4 4.71238898038469 5.5 6 8 12 --raw <raw>/refine`
- `soliton_symbolic_checks.py <raw>/symbolic.json`
- `soliton_jost_covariance_check.py --raw <raw>/jost_cells`

Binary search exhausts all contiguous intervals, uses 64 starts (the interval,
all-pass, both signs of eigenvector thresholds, and seeded random masks),
one-bit descent, and four annealing sweeps of 10,000 flips. The seed is
20261010. This finds an achievable mask and does not certify global optimality.
Finite-basis eigenvalues are Ritz approximations, not numerical certificates
for the continuum lower bound. Frequency-cell and time-window discretizations
are reported separately. `jost_pilot.json` predates the exact-completeness
subtraction; it is retained as an intermediate diagnostic, not a final score.
