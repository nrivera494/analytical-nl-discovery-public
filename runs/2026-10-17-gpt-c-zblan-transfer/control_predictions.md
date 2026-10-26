# Additional numerical oracle, frozen before execution

gpt-c / gpt-6-astra / gpt, 2026-10-17. This supplements the original
convergence design without changing any material prediction or tolerance.

For the reference ZBLAN N=4 case at the originally predicted duration,
zN=2, compare RK4IP with a Strang split-step forward. The reference
nonlinear subflow is exact: intensity is invariant within that substep,
so multiply by exp(i*h*((1-fR)*I+fR*(hR*I))). Use steps 4e-4,2e-4,1e-4
in z/LD. Expect successive field differences of order two (1.8..2.2),
and relative field disagreement below 1e-3 with the finest frozen RK4IP
forward. This tests integration using the same PDE/kernel and FFT
convention; it is not an independently sourced response implementation.

Original fixed-step RK4IP, time-domain kernel and local-ZS mesh controls
retain their predictions. For the latter two the two finest successive
orders should lie in 1.8..2.2. Run all controls serially with the same
memory and grid limits. Record failures as failures.

An additional matched forward uses the pinned agents' solver b9fa957,
with a run-local measured-ZBLAN response subtype (no solver edits).
Physical N=4, T0=200fs, zN=2, n8192, width96, fixed step1e-4 in z/LD;
match the normalized sampled kernel, built-in shock and frequency filter,
TOD and loss in Python. Predict direct complex-field relative agreement
below1e-6. This is a separate implementation check, not a fitted material
prediction. No adjoint or noise is used.
