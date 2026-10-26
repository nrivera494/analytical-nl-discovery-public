# Width and chirp rates

agent: gpt-a; model: gpt-6-astra; family: gpt; task: T-20261008-gpt-a-01.

Frozen before these tests. Paired +/-0.01 width and chirp perturbations about a smooth-edged parabola at fixed energy. Predictions: decay 1/3 and angular frequency sqrt(2)/3 per gain length. The directly measured derivative of the width ratio s is s*(chirp_ratio-1)/3. Jointly fit paired differences of s and this derivative to a damped sinusoid, with both decay and frequency free, on [2,8], [4,10] and [6,12]. No fitting to the ODE-derived constants. Initial soft-edge scale is 0.02; this is an H1 input, not an exact hydrodynamic parabola. Report dependence on Nstar, fit interval and perturbation size.

The independent exact-lens integrator is used to reach 12 gain lengths; original-coordinate solver gain/RK4IP counterparts through eight gain lengths are required. Refine step, grid and window independently. Treat unresolved late times as failed rather than as rate evidence.
