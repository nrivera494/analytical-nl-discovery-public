---
agent: gpt-d
model: gpt-6-astra
family: gpt
created: 2026-10-16
claim: C-20261016-claude-interactive.6-01
---

# Independent protocol, frozen before propagation

The claim is an exact first integral of a particular two-coordinate ODE, followed by approximations to a terminal frequency and a cutoff optimum. Its physical interpretation additionally requires a single adiabatic sech pulse, negligible spectral filtering drift, a narrow spectrum relative to the carrier and loss slope, and a sufficiently long pulse for the Gordon approximation. Equal launch-to-output differences in N^4, rather than in N, are the proposed invariant.

No proposer code, derivation notes, logs, PR descriptions or branch history have been read. Claim cards, the problem card, allowed run metadata/summary and solver documentation have been read. Setup commands printed commit subjects and merge file names incidentally; they were not used as evidence.

## Frozen checks

1. Independently build LP01 dispersion from the claim's geometry and Boilard et al., arXiv:2109.13366, Table 2; derive effective area by radial quadrature. Reproduce the Z75 main and held-out launches, their recorded planes and cutoff maxima. Use the claim tolerances without refitting parameters. Also run the photon-conserving variable-area equation.
2. Independent held-out case: Z75, fundamental T0 = 40 fs at 2.8 um, full dispersion, constant launch-frequency area, the same loss edge, length 12 m. Freeze the independent full-response ODE predictions in predictions.json before launching its GNLSE. Apply the claim's wavelength/photon/optimal-length tolerances.
3. Direct path test: at a common launch frequency and common output frequency compare N0^4 - N^4 for two fundamental launch widths. Evaluate the analytic Gordon integral without post-hoc renormalization. Separately show the effect of post-formation initialization, and disclose every such change. Choose widths at or above the stated long-pulse bound for the genuine linear-TR test; report if the loss is too small to resolve.
4. Terminal test: start with a fundamental, long-pulse soliton near the exponential absorption edge, choosing loss strength so alpha*z0 starts below 0.01. Freeze the predicted terminal frequency, distances and photon fractions from the Gordon quadrature. Fit log N against log(omega-omega_infinity) only with the frozen terminal frequency. The expected exponent is 1/4. Track alpha*z0 throughout; an asymptote outside the adiabatic domain is not an in-domain validation. A silica case with constant beta2 provides a controlled terminal test; full-dispersion silica is the physical relaxation.
5. Rate asymptotics: silica fundamentals T0 = 50, 80, 120, 200 fs (plus shorter and longer edge cases), compare the measured shift with Gordon at fixed fractions of the dispersion length. Predicted relative-error exponent is 2 in 1/T0. Also measure the exact instantaneous sech-overlap expansion, to separate rate linearization from shape evolution.
6. Fission: Z75 order 2, T0 = 40 fs at 2.8 um. Identify the reddest localized pulse by continuity and frequency, never by the largest peak alone. Choose a separation plane from a loss-independent isolation test. Record any failure of identification instead of silently changing the rule.
7. Artefacts: halve dz, double the temporal window, and halve dt for a decisive case. dt <= 3 fs normally. Track photons, spectral/window-edge occupation, and the difference between total-field and isolated-pulse observables. Run a lossless conservation check. Use analytic Raman transforms and compare the sampled-kernel implementation explicitly.
8. Test the algebra of the optimum including the changing sech width and the exact initial-condition term in the exponential-edge integral. Examine the low-loss and constant-loss limits.
9. Source search: Kormokar 2021 and 2023, Petersen 2017, primary ZrF4 nonlinear-index and multiphonon-edge data. Record access levels and uncertainty. No absence-of-prior-work claim from abstracts alone.
10. If computation permits, use the agents' solver's explicit discrete RK4IP adjoint, fixed Float64 steps, matched backward steps, and several seeded spectral-mask starts. A search not performed is a blocker for an audited optimality claim.

All production cases are sequential, under the shared-machine memory policy. Raw arrays go outside git. Exact chosen parameters and predictions will be committed before each newly chosen propagation family.

Pre-terminal-run amendment: truncate the planned silica propagation at 500 m (frozen ODE has N/N0 about 0.04 there), before temporal width can consume the available window. Use 16384 points at 3 fs and dz=0.02 m. The original 1800 m ODE remains recorded, explicitly outside the adiabatic and numerical-window regime. The terminal frequency and all earlier predictions are unchanged. This amendment is made before any silica GNLSE.

Additional frozen cases (`extra_predictions.json`): two long-pulse, full-dispersion paths in each material; and a quadratic-dispersion silica cutoff case chosen to have epsilon/(2a)=0.1 at the cutoff. The latter deliberately tests the stated boundary of the crossing approximation. Its closed-form length and the directly integrated Gordon-ODE optimum are both recorded before GNLSE propagation. This distinguishes algebraic approximation error from failure of the GNLSE reduction.

Pre-run additions: repeat the fluoride main case with the measured Xia 2006 edge fit, and with cubic dispersion; compare analytic and sampled Raman kernels; run lossless conservation and silica rate-scaling cases at 0.1 dispersion lengths. Rate shifts are measured from the full-field photon centroid and the exact initial derivative, so no isolation threshold is fitted. Fission uses the reddest time-localized candidate with at least 10 percent of launch photons; a formation plane is accepted only if separated from every other candidate by at least eight fitted widths and its sech-intensity residual is below 10 percent at consecutive output planes. Failure to satisfy this rule is reported, not repaired post hoc.

Before inspecting any fission output, require at least two resolved temporal peaks and less than 95 percent of launch photons in the candidate; otherwise the initial unfissioned sech would vacuously satisfy the isolation rule. The prefix run in the currently running batch imported the earlier tracker before this clarification; its raw fields and numbers will be retained, but any accepted formation plane must satisfy these additional conditions. Freeze the conditional continuation ODE from the short prefix before running the full fission trajectory.

Post-pilot numerical amendment: the whole-field fission run's progress at 2 m indicates overlapping pulses in the periodic time window. Preserve that run and its tracker output. In a separate run, take the actual daughter field at the already completed prefix's final plane, 0.5 m, retain a temporal window of halfwidth 1.5 ps around it, and propagate that field without replacing it by a sech. At that plane the other pulse is already much farther away. This checks an isolated fission-born daughter without allowing a distant pulse to wrap around and collide artificially. The original frozen ODE from 0.0625 m is unchanged, and the 2 m scoring plane is retained. This is not certification of the whole-field fission calculation; the removed pulse and radiation are explicitly excluded from the continuation.

### Adjoint restart disclosure
The first adjoint launch disappeared without a completion file after its directional-gradient check. Its cause was not established. The incomplete run and available field are retained. The identical frozen search is restarted under `2026-10-16-gpt-d-adjoint-cutoff200-retry`, with explicit garbage collection and persisted progress to limit allocation accumulation and improve diagnostics. No numerical objective or start is changed.

The persisted restart identifies an auditor API error: `Optim.only_fg!` is unavailable. The public objective/gradient interface replaces it, with a shared cache. The failed run is retained, and the unchanged starts/objective are rerun as `2026-10-16-gpt-d-adjoint-cutoff200-complete`.
