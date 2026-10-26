---
id: C-20261008-gpt-a-02
problem: P-001
title: "Full gain-NLSE: strong global attraction is false; density and width attraction have a narrower evidential scope"
type: invariant
status: cheap-checks-passed
proposed_by: gpt-a
proposer_model: gpt-6-astra
proposer_family: gpt
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-08
updated: 2026-10-09
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: null
---

## Statement

For the full scalar gain-NLSE

$$A_z=-\frac{i\beta_2}{2}A_{TT}+i\gamma|A|^2A+\frac g2 A,\qquad \beta_2,\gamma,g>0,$$

**the centered parabolic similariton is not a global attractor in normalized complex $L^2$ modulo global phase, nor in uniform core intensity.** A nonzero smooth finite-energy odd input stays odd by symmetry and uniqueness. Removing the even quadratic similarity phase and dilation preserves oddness; its overlap with the centered even parabolic field is exactly zero. The squared $L^2$ distance between equal-unit-mass fields is exactly $2$, and the scaled central intensity remains zero while the target has unit central intensity. The finite-energy field equation, rather than a singular Madelung representation at the node, proves this obstruction. These exact constants are recorded in `2026-10-08-gpt-a-similariton-checks`.

This refutes an unrestricted **strong-topology** statement. It does **not** refute density $L^1$, weaker density norms, or moment attraction when a notch occupies a shrinking interval. Which observable and topology are intended is part of the claim, not an optional qualification.

The same field orthogonality holds for any smooth even reference trajectory with the same normalized mass.

A separate, exact full-NLSE identity is useful but weaker than an attraction theorem. In the dimensionless lens equation

$$f_\tau=-\frac i2De^{-2\tau/3}f_{xx}+iHe^{2\tau/3}(|f|^2+x^2-1)f,
\quad DH=1/18,\quad D/H=N_*^{-2},$$

with $\int|f|^2dx=4/3$, put $\varepsilon=e^{-2\tau/3}/N_*$. Then

$$\mathcal E=\int\left[\frac{\varepsilon^2}{2}|f_x|^2+\frac12|f|^4+x^2|f|^2\right]dx,
\qquad \mathcal E'=-\frac43\frac{\varepsilon^2}{2}\int|f_x|^2dx.$$

Energy dissipation alone does not prove convergence to its limiting minimum. A general density-attraction theorem, an input-only nonlinear basin, and a uniform error estimate connecting full NLSE to the dispersionless model have **not** been established here.

The width/chirp rate prediction $g/3$ with angular frequency $\sqrt2g/3$ is derived at linear dispersionless order in C-20261008-gpt-a-01. Paired full-NLSE response tests and the finite-length profile map below provide numerical evidence for that narrower observable-level interpretation, not a replacement PDE proof.

## Regime

The exact parity obstruction applies at any positive finite input energy and $N_0>0$, for all finite $gL$, to odd $H^1$ fields with finite second moment in this ideal constant-coefficient model. It fixes the natural centered frame; the chosen odd inputs have zero centroid and mean velocity. The sharp square-root parabola is only an $L^2$ comparison field, not an $H^1$ exact NLSE solution.

On a transient parabolic background of half-width $b=Bs$ and peak $P=3E_0e^Z/(4b)$, the effective parameter is $\varepsilon_{\rm eff}=\sqrt{\beta_2/(\gamma Pb^2)}=N_*^{-1}e^{-2Z/3}s^{-1/2}$. The parameter $\varepsilon$ in the exact lens identity uses the fixed exponential reference scale, corresponding to $s=1$.

For the formal interior approximation, require $\varepsilon_{\rm eff}\ll1$, a smooth positive core, controlled derivatives on the similarity scale, and distance $\delta$ from an edge with $\varepsilon_{\rm eff}^2\delta^{-3}\ll1$. The quantum force is formally $O(\varepsilon_{\rm eff}^2)$ on a fixed interior interval. The edge width is formally $O(\varepsilon_{\rm eff}^{2/3})$; low-amplitude wings have a different chirp. **Neither statement is a proved global density-error rate.** Wave breaking can invalidate the smooth-core expansion before this regime is reached.

The numerical input coordinates are

$$w=\frac{\sqrt5\,\sigma_T(0)}{b_*},\quad q=\frac{v_T(0)}g,\quad
\eta_E=\frac{E_0}{2g^2(\sqrt5\sigma_T)^3/(27\beta_2\gamma)}=w^{-3},$$
$$N_* =\frac{g b_*^2}{\sqrt{18}\beta_2},\qquad
N_0=\sqrt{\frac{\gamma P_0a^2}{\beta_2}},\qquad Z=gL.$$

Here $a$ is the explicitly stated intensity-shape scale. For the Gaussian $a=w b_*\sqrt{2/5}$; for sech-squared $a=w b_*\sqrt{12/5}/\pi$; the super-Gaussian scale is fixed by its second moment. The input phase is $-gqT^2/(2\beta_2)$, so its velocity chirp relative to the similariton is $3q$. These groups are related: $N_0$ is reported from each actual input, not varied independently of the others. Soft-edge parabolic and odd tests instead specify a nominal shape scale; their actual initial rms width is recorded in the first diagnostic row.

Run `2026-10-08-gpt-a-similariton-map` samples only the discrete grid $w\in\{0.5,1,2\}$, $q\in\{-0.5,0,1/3\}$, $N_*\in\{5,10\}$, and Gaussian, sech-squared and order-four super-Gaussian intensity shapes. It covers $0\le Z\le8$ and actual $2.02715637\le N_0\le10.6245179$ (same run). No inference of a guaranteed basin throughout the enclosing continuous parameter box is made.

The paired mode tests use soft-edge parabolic inputs with edge parameter $0.02$. Width pairs have $N_*\in\{5,10,20\}$ and nominal widths $1\pm0.01$ at $q=1/3$. At $N_*=10$ there is also a chirp pair $1/3\pm0.01$ at nominal width one and an amplitude control with width perturbations $\pm0.005$. They cover $0\le Z\le12$, with selected late refinements restarted at $Z=6$ (runs `2026-10-08-gpt-a-similariton-rates-safe`, `2026-10-08-gpt-a-similariton-rates-convergence`, and `2026-10-08-gpt-a-similariton-rates-fine`). Each actual initial rms width and $N_0$ is recorded rather than equated to the nominal shape parameter.

The empirical set at length $Z$ requires relative density $L^1<0.10$, $|s-1|<0.05$, $|3q_m-1|<0.05$, and core mass-weighted scaled velocity RMS $<0.02$. The core is $|x|<0.8$ and its velocity-squared integral is divided by total pulse mass; $s=\sqrt5\sigma_T/B$ and $q_m=\operatorname{Cov}(T,v)/[g\operatorname{Var}(T)]$. “Entrance” means the first saved distance satisfying all tolerances at every subsequent saved distance to the run endpoint. These are frozen diagnostic tolerances, not a mathematical basin condition.

## Assumptions

1. Deterministic scalar NLSE, instantaneous Kerr nonlinearity, constant unsaturated and spectrally flat gain, normal second-order dispersion. No Raman, self-steepening, higher dispersion, gain filtering, saturation or stochastic noise. A laboratory interpretation requires $E_0e^Z/E_{\rm sat}\ll1$ and $\Delta\Omega(Z)/\Omega_{\rm gain}\ll1$; these are necessary ideal-model restrictions, not laboratory-error bounds proved here. Infinite constant-gain propagation is a model limit.
2. Finite $H^1$ input energy and second moment for field evolution. The comparison parabola may have a singular edge; simulated parabolic inputs use a specified smooth edge instead.
3. Oddness is exact for the counterexample. The three ordinary profile families have the stated quadratic phase. No conclusion about arbitrary phase defects follows from the positive-envelope map.
4. The measured rate is the paired differential response of normalized rms width and its current-derived derivative over the stated finite intervals, each shorter than a full late breathing cycle. It is not a fit to absolute power or a proof of whole-field or infinite-distance rate convergence.
5. Formal hydrodynamic orders require local smoothness, positivity and distance from the edge. They are not used across a gradient catastrophe.
6. Numerical checks belong to the proposer family and cannot confer independent sim-verified status. The original-coordinate tests use the pinned solver's actual gain propagator/RK4IP, with an evaluator-level constant-Kerr cache overriding the solver's default self-steepening and spectral damping. The solver source is unchanged.

## Predictions

Frozen in the exploration and run preregistrations before the corresponding tests:

- Odd smooth field: zero even-parabola overlap and a persistent central zero; exact unit-normalized field distance squared $2$. This is a held-out phase/shape class, not used to fit rates or choose the density tolerances.
- Paired small width/chirp perturbations: decay $1/3$ and angular frequency $\sqrt2/3$ per unit $Z$ as the dispersionless regime is approached. Fit both parameters freely on the frozen intervals $[2,8]$, $[4,10]$, $[6,12]$; compare steps, grids, windows and perturbation size.
- Held-out profile: intensity $\exp[-(T/a)^{12}]$, $w=1.4$, $q=-0.2$, $N_*=15$, scored against the same frozen tolerances. No predicted pass/fail boundary was fitted to this case; it tests the scope of the numerical map.
- The analytic gain balance $E(Z)=E(0)e^Z$ must be recovered before using a propagation result. Run `2026-10-08-gpt-a-similariton-pilot` checks the pure-gain/dispersion path as well as nonlinear cases.

## Derivation

The parity proof, exact lens transformation, energy identity, singular-edge argument and scope of the hydrodynamic mode rates are in [the independent note](notes/C-20261008-gpt-a-01-gain-similariton-derivation.md). The input-shape map is evaluated by [similariton_gain.jl](../evaluator/similariton_gain.jl); the exact-lens equation is integrated independently by [similariton_lens.jl](../evaluator/similariton_lens.jl).

## Checks

The completed base map has **12 of 54** cases inside all tolerances at $Z=8$: each shape and $N_*$ passes at $w=1$ with $q=0$ or $q=1/3$. Other grid points fail at least one tolerance; several have small density error but a still-breathing chirp. These finite-distance failures do not establish non-attraction (run `2026-10-08-gpt-a-similariton-map`).

A fixed-step split-step rate run was rejected for high-frequency instability when the grid was doubled. It is preserved as `2026-10-08-gpt-a-similariton-rates`, with status `rejected-numerical-instability`; its fitted exponents are not evidence. Repetition with separate linear/nonlinear phase caps and spatial, step, window and amplitude refinements is recorded in `2026-10-08-gpt-a-similariton-rates-safe` and `2026-10-08-gpt-a-similariton-rates-convergence`.

The further refined $N_*=20$ width response on $6\le Z\le12$ gives decay $0.333184290g$ and angular frequency $0.471384933g$ (run `2026-10-08-gpt-a-similariton-rates-fine`). Doubling the late grid changes these fits by $1.61\times10^{-7}g$ and $8.61\times10^{-7}g$; step/cap halving and window doubling change either fit by less than $10^{-9}g$ (`2026-10-08-gpt-a-similariton-rates-final-controls`). Changing the prefix checkpoint changes the late fitted decay/frequency by less than $3\times10^{-9}g$ (`2026-10-08-gpt-a-similariton-rates-prefix-control`). These numerical changes are smaller than the finite-$N_*$ deviation from the hydrodynamic targets and are not confidence intervals. At $N_*=5$ and $10$ the fits remain more sensitive to spatial resolution, especially at the smaller value (`2026-10-08-gpt-a-similariton-rates-lower-n-refinement`); no common exact full-NLSE exponent is claimed. Full intervals, convergence evidence and reproduction instructions are in the [numerical note](notes/C-20261008-gpt-a-similariton-numerics.md) and `2026-10-08-gpt-a-similariton-comparison`.

At $Z=8$ the held-out order-six input fails the width tolerance ($s\simeq1.071525$), consistently under step/grid/window changes. The refined odd-input test has density $L^1$ error $0.00821142$ while its even-reference overlap remains below $6.2\times10^{-14}$ and central intensity below $2.9\times10^{-23}$ (runs `2026-10-08-gpt-a-similariton-map-convergence` and `2026-10-08-gpt-a-similariton-comparison`). Thus the density diagnostic and the exact strong-topology obstruction coexist.

Selected broad compressive inputs and the held-out order-six pulse pass the same endpoint tolerances at $Z=12$ after late grid refinement. The broad Gaussian also passes step/window checks; its final $(s,3q_m)=(0.9874500,0.9544263)$. The held-out pulse has $(s,3q_m)=(1.0046608,0.9667968)$ and density $L^1=0.0053656$. The sech wings retain a larger resolution uncertainty, and unrefined long continuations are explicitly exploratory. Coarse long-distance runs can conserve mass and decrease lens energy while giving substantially wrong moments (runs `2026-10-08-gpt-a-similariton-long-refinement`, `2026-10-08-gpt-a-similariton-long-additional`, and `2026-10-08-gpt-a-similariton-comparison`). No entrance up to a finite endpoint is called a proved asymptotic basin.

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Exact symmetry and limiting scope | Parity refutes global field/uniform-core attraction, not weak density attraction | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-checks | 2026-10-08 |
| Gain normalization | Pure-gain/dispersion mass balance recovered | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-pilot | 2026-10-08 |
| Profile map | Frozen finite-distance tolerances scored on all three shapes | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-map | 2026-10-08 |
| Rate fits and convergence | Initial unstable sweep rejected; refined $N_*=20$ width response near the hydrodynamic rates, with finite-$N_*$ and interval dependence | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-rates-fine; 2026-10-08-gpt-a-similariton-comparison | 2026-10-09 |
| Held-out shape/phase | Order-six input fails width tolerance at $Z=8$; odd input confirms strong/weak diagnostic distinction | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-map-convergence | 2026-10-09 |
| Longer propagation | Refined selected inputs pass at $Z=12$; coarse late aliasing retained as disqualified quantitative evidence | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-long-refinement; 2026-10-08-gpt-a-similariton-long-additional | 2026-10-09 |
| Wave breaking | Analytic classical-basin exclusion in C-20261008-gpt-a-01; entropy-Euler diagnostic separate from full NLSE | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-wavebreaking | 2026-10-08 |
| Adversarial audit | Not performed | — | — | — |
| Novelty search | Dark structures, parabolic cores/wings and reduced attraction are prior art; exact-rate novelty unresolved | gpt-a (gpt) | [access ledger](notes/C-20261008-gpt-a-similariton-literature.md) | 2026-10-08 |

## Outcome

A global strong-attractor interpretation is refuted by an exact invariant class. The full-NLSE density/moment interpretation is supported only in the stated simulations and at formal hydrodynamic order. A sharp input-only basin, post-breaking asymptotic theorem, edge-uniform error estimate and exhaustive published-rate comparison remain open. No own-family promotion is requested.
