# Finite-length entrance map

agent: gpt-a; model: gpt-6-astra; family: gpt; task: T-20261008-gpt-a-01.

Frozen before the sweep. Config enumerates 54 cases. Shapes: intensity exp(-y^2), sech(y)^2 and exp(-y^8). All input masses are 4/3; b*=P*=g=1 in the dimensionless realization. Width w=sqrt(5)*rms(T)/b*. Chirp q=v_T/g. E, beta2, gamma determine b* and epsilon*=1/Nstar; report each actual N0 from peak and analytic shape scale.

Define numerical entrance at a saved distance by relative density L1 < 0.10, abs(width_ratio-1)<0.05, abs(chirp_ratio-1)<0.05 and core scaled velocity RMS <0.02. Report whether this remains true at all subsequent sampled distances through gL=8, rather than a single favorable crossing. This is a finite-length tolerance set, not a proven basin.

Independent convergence cases are selected across all three shapes, both chirp signs represented by negative and the positive 1/3, both ends of the width and Nstar ranges, and the most severe observed resolution indicators. Change step, window and grid independently. The held-out super-Gaussian has order six (intensity exp(-y^12)), w=1.4, q=-0.2, Nstar=15; do not use it to choose this rule.
