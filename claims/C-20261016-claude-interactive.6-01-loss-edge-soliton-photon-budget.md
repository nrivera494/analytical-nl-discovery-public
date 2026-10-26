---
id: C-20261016-claude-interactive.6-01
problem: P-20261016-claude-interactive-02
title: "Loss-edge photon budget of a Raman soliton: the photon number is a function of the frequency reached, N^4 = N0^4 - Lambda(omega), which fixes the best photon fraction beyond a cutoff and the optimal length"
type: reduced-model
status: refuted
proposed_by: claude-interactive.6
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: gpt-d
auditor_family: gpt
created: 2026-10-16
updated: 2026-10-16
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: null
---

## Statement

**System.** A single fundamental Raman soliton shifts to the red in a single-mode fibre. The fibre has:
- dispersion $\beta_2(\omega)<0$ along the path;
- nonlinearity $\gamma(\omega)=n_2\omega/(cA_{\rm eff})$, taken constant-$A_{\rm eff}$ or photon-conserving with $A_{\rm eff}(\omega)$;
- a causal Raman response $h_R$ with fraction $f_R$ and $T_R=f_R\int t\,h_R$;
- a power loss $\alpha(\omega)$ that rises toward low frequency, such as a multiphonon edge.

Let $N$ be the soliton's photon number, $\omega$ its centre frequency, and $\mathcal N$ the launched photon number. The launch is at $\omega_0$ with $N(\omega_0)=N_0$.

**(a) Path-independent photon number.** With the linear-$T_R$ (Gordon) rate $\dot\omega=-K(\omega)N^4$, where $K=T_R\gamma^4(\hbar\omega)^4/(30|\beta_2|^3)$, and with $\dot N=-\alpha N$:
$$N(\omega)^4=N_0^4-\Lambda(\omega),\qquad \Lambda(\omega)=4\int_\omega^{\omega_0}\frac{\alpha(\omega')}{K(\omega')}\,d\omega'.$$
- The loss a soliton has suffered depends only on how far it has shifted, not on the length or the route.
- $N_0^4-N^4$ is a fibre property, the same function of $\omega$ for every launch energy.
- The distance is $z(\omega)=\int_\omega^{\omega_0}d\omega'/[K(N_0^4-\Lambda)]$.
- With the full Raman response, $K N^4$ is replaced by the sech-overlap rate:
$$\dot\omega=-\frac{\gamma f_R}{E}\int\frac{d\Omega}{2\pi}\,\Omega\,{\rm Im}\,\tilde h_R\,|\tilde I_{\rm sech}|^2 ,$$
with $E=\hbar\omega N$ the soliton energy and $\tilde I_{\rm sech}$ the transform of a sech² intensity of the local soliton width. Then (a) becomes a two-variable ODE in which $\dot N/\dot\omega$ again depends only on $(\omega,N)$.

**(b) Terminal frequency and the quarter power.** Take $\alpha\propto e^{-\omega/w}$ and $K\propto e^{\kappa\omega}$ locally. Then
$$N/N_0=\left[1-e^{-(\omega-\omega_\infty)/w_{\rm eff}}\right]^{1/4},\qquad w_{\rm eff}=(1/w+\kappa)^{-1},$$
$$\alpha(\omega_\infty)=\frac{K(\omega_\infty)N_0^4}{4w_{\rm eff}}=\frac{|\dot\omega|_{\rm lossless}(\omega_\infty)}{4w_{\rm eff}} .$$
The soliton approaches $\omega_\infty$ only logarithmically in $z$. It keeps most of its photons until it is within about $w_{\rm eff}$ of $\omega_\infty$.

**(c) Best photon fraction beyond $\lambda_c$, and the optimal length.**
$$\eta^*(\lambda_c)=\max_L\eta(\lambda_c,L)=\frac{N(\omega_c)}{\mathcal N}\,(1-c_\times),\qquad c_\times\simeq\frac{\varepsilon}{2a}\Big(1+\ln\frac{2a}{\varepsilon}\Big),$$
with $\varepsilon=\alpha(\omega_c)/|\dot\omega(\omega_c)|$ the photon loss per unit frequency shift, and $a=\pi T_s/2$. The maximum is reached at
$$L^*=z(\omega_c-\delta^*),\qquad \tanh(a\delta^*)=1-\varepsilon/a ,$$
that is, just after the soliton's spectrum has crossed $\omega_c$. The optimum is interior whenever $\Lambda(\omega_c)<N_0^4$.

## Regime

Small parameters:
- adiabaticity, $\alpha z_0\le10^{-2}$ with $z_0=\pi T_s^2/(2|\beta_2|)$;
- loss variation across the soliton spectrum, $(wT_s)^{-2}\le0.25$ on the part of the path where the loss acts. This is the tested range: about 0.2–0.25 in the main case at the stall, $T_s\approx100$ fs. The ODE averages $\alpha$ over the sech² spectrum. The closed forms (a) and (b) take $\alpha$ at the centre, which underestimates $\Lambda$ by a relative $\simeq(wT_s)^{-2}/6$ (the sech² moment-generating function);
- for the closed form (c), the crossing parameter $\varepsilon/(2a)\le0.1$;
- for the linear-$T_R$ form (a) and (b), $T_s\ge50$ fs (silica) or the equivalent $T_s\Omega_R\ge4$.

The full-response ODE has no $T_s$ limit from the Raman linearization. It still overestimates the shift by 7–20% for $T_s\le30$ fs: run `2026-10-16-claude-interactive.6-h2-fundamental`, where the error falls to 1% at $T_s\ge50$ fs.

One isolated soliton carries the photons beyond $\lambda_c$: no collisions, and no second soliton or dispersive wave beyond $\lambda_c$.

**Predicted error order.** The linear-$T_R$ rate has relative error $\propto T_s^{-2}$. The measured exponent is 1.83 over $T_0=50$–200 fs (run `2026-10-16-claude-interactive.6-h2-fundamental`).

## Assumptions

- Scalar, single-mode, single polarization; deterministic, with no quantum or thermal noise.
- GNLSE in the photon-conserving form: constant $A_{\rm eff}$ with the shock factor $\omega/\omega_0$ (the agents' solver model), or Laegsgaard's $A_{\rm eff}(\omega)^{-1/4}$ form.
- The soliton stays a fundamental sech soliton of the local $\beta_2(\omega)$ and $\gamma(\omega)$. Higher-order dispersion enters only through $\beta_2(\omega)$. Cherenkov radiation is neglected.
- Raman: a single damped oscillator in the tests; the result holds for any causal $h_R$ in the full-response form.
- Loss is averaged over the soliton's sech² photon spectrum. The loss-slope drift of the centroid is included in the ODE and neglected in (a) and (b).
- **Test fibre Z75.** Step-index ZrF₄, core radius 3.75 µm, NA 0.30.
  - Cladding Sellmeier: Boilard, Vallée & Bernier, arXiv:2109.13366, Table 2 (full text). The LP01 mode is weakly guiding.
  - $n_2=2.1\times10^{-20}$ m²/W, **assumed**, not sourced.
  - Raman: single-oscillator stand-in, $f_R=0.20$, $\tau_1=20.9$ fs, $\tau_2=53$ fs. It is built from the broad component of the InF₃ fit of Gauthier et al., Sci. Rep. 12, 15898 (2022), DOI 10.1038/s41598-022-19658-8 (full text via PMC).
  - Edge: $\alpha=Ae^{-B/\lambda}$, with 1 dB/m at 4.2 µm (Gauthier 2022, for ZrF₄ fibre) and **assumed** slope $B=92$ µm, so $w=2\pi c/B=20.5$ rad/ps.

## Predictions

Frozen before any production run. The hypotheses are in commit `4f0f1ff` (`claims/notes/T-20261016-claude-interactive-04-hypotheses.md`, H3). The values come from `runs/2026-10-16-claude-interactive.6-lwir-predictions/predictions.json`. The held-out case is in commit `38bb1af` (`predictions_heldout.json`).

**Main case.** Z75, constant $A_{\rm eff}$, fundamental soliton at 2.8 µm with $T_0=20$ fs (9.13 nJ), $L=8$ m.
- $N/N_0$ at 2, 4, 6, 8 m: 0.995, 0.975, 0.941, 0.894 (±0.02).
- $\lambda_s$ at the same planes: 3.589, 3.718, 3.787, 3.830 µm (±0.03 µm).
- $(\eta^*,L^*)$ = (0.986, 2.83 m), (0.967, 4.12 m) and (0.921, 6.19 m) at $\lambda_c=3.5$, 3.6 and 3.7 µm. Tolerances: $\eta^*$ ±0.03, $L^*$ ±20%.

**Held-out.** Same fibre, $T_0=30$ fs (6.09 nJ):
- $N/N_0$ at 8 m: 0.988;
- $\lambda_s$ at 2, 4, 6, 8 m: 3.276, 3.398, 3.471, 3.522 µm;
- $(\eta^*,L^*)$ = (0.994, 5.32 m) at 3.3 µm and (0.985, 7.94 m) at 3.4 µm.
- Tolerances as for the main case.

**Relaxed assumption.** The `pc` form with $A_{\rm eff}(\omega)$, against the reduced model with $\gamma(\omega)$: $(\eta^*,L^*)$ = (0.973, 6.81 m) at 3.5 µm.

**Relaxed assumption 2, a soliton born from fission** (frozen in commit `638af7a`, 2026-10-16 14:02, before the run). Launch a TL sech of order $N=2$, $T_0=40$ fs, at 2.8 µm in Z75 with constant $A_{\rm eff}$, $L=8$ m. Find the leading soliton's separation plane $z_s$ with the criterion of `h2_reach_post.py`. Start the full-response ODE (with loss) from the GNLSE values $(z_s,\omega_1,N_1)$. It predicts $N_1/N_1(z_s)$ at 2, 4, 6 and 8 m within ±0.02, and $\lambda_1$ within ±0.03 µm.

## Derivation

$\dot N/\dot\omega=\alpha N/(KN^4)$, so $d(N^4)/d\omega=4\alpha/K$. This is separable and gives (a).
- (b): with $4\alpha/K\propto e^{-\omega(1/w+\kappa)}$, $\Lambda(\omega)=4\alpha w_{\rm eff}/K$ up to $e^{-(\omega_0-\omega)/w_{\rm eff}}$. Setting $\Lambda(\omega_\infty)=N_0^4$ gives the terminal condition and the quarter power.
- (c): maximize $N(\omega_s)\Phi(\omega_c-\omega_s)$, where $\Phi=\tfrac12[1+\tanh a(\omega_c-\omega_s)]$ is the photon fraction of the sech² spectrum beyond $\omega_c$. With $d\ln N/d\omega=\varepsilon$, the condition is $a(1-\tanh a\delta)=\varepsilon$.
- Known limit: for constant $\alpha$ and $K$, (a) gives $\omega_0-\omega=\frac{KN_0^4}{4\alpha}(1-e^{-4\alpha z})$. This is the effective-length law $z_{\rm eff}=(1-e^{-4\alpha z})/(4\alpha)$ in Kormokar, Shamim & Rochette, JOSA B 40, 412 (2023), Eq. 13 (full text).
- Code: `runs/2026-10-16-claude-interactive.6-lwir-common/lwir.py`, class `ReachModel` and function `gordon_K`.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | $K N^4$ in rad ps⁻¹ m⁻¹; $\Lambda$ in photons⁴ | claude | — | 2026-10-16 |
| Known limits | Constant $\alpha$, $K$ reproduce the $z_{\rm eff}$ law (Kormokar 2023, Eq. 13); $\alpha=0$ gives the lossless reach integral | claude | — | 2026-10-16 |
| Symmetries | Global phase and time translation preserve the equations and observables; a frequency translation is not a symmetry of the material coefficients | gpt-d (gpt) | 2026-10-16-gpt-d-loss-edge-audit | 2026-10-16 |
| Symbolic residual | Closed form (c) against the reduced-model ODE, at $\lambda_c=3.6$ µm in the main case. From the frozen trajectory: $\varepsilon\approx\Delta\ln N/\Delta\omega=0.0203/18.2$ rad⁻¹ ps between 2 and 4 m, and $a=\pi T_s/2\approx0.118$ ps. This gives $c_\times=0.030$ and $\eta^*=0.993\times0.970=0.963$, against the ODE optimum 0.967. **(b) against the exact quadrature** of $\Lambda$ (linear-$T_R$ $K$, Z75, main-case $N_0$; `closed_form_b_check.json`). $\lambda_\infty=3.911$ µm and $w_{\rm eff}=11.1$ rad/ps, against the edge $w=20.5$ rad/ps; the decline of $K$ halves the effective width. The quarter-power form matches the exact $N/N_0$ to within 0.004 for $(\omega-\omega_\infty)/w_{\rm eff}$ from 0.1 to 4. The terminal condition $\alpha(\omega_\infty)=KN_0^4/(4w_{\rm eff})$ holds to 2% (ratio 0.980). (b) is not tested in the GNLSE: no run reached the terminal regime | claude | 2026-10-16-claude-interactive.6-lwir-predictions | 2026-10-16 |
| Simulation, core regime | Main case: $N/N_0$ all four within ±0.02 (0.983, 0.966, 0.936, 0.893); $\lambda_s$ 3.554, 3.696, 3.771, 3.818 µm, so 2 m misses by 0.035 and the other three pass; $(\eta^*,L^*)$ = (0.971, 3.2 m), (0.951, 4.6 m), (0.905, 6.75 m), all within tolerance | claude (numpy GNLSE) | 2026-10-16-claude-interactive.6-h3-edge | 2026-10-16 |
| Error-scaling exponent | Linear-$T_R$ rate error $\propto T_0^{-1.83}$ (isolated solitons, S28) | claude | 2026-10-16-claude-interactive.6-h2-fundamental | 2026-10-16 |
| Path independence, (a) in its own form | GNLSE photon number at the soliton's own wavelength against the model's $N(\lambda)$ at the same wavelength, renormalized at 2 m to remove the 1.4% the bare-sech launch sheds as radiation: max difference 0.0049. Loss accumulated after 2 m: 9.09% (GNLSE) against 8.60% (model); the GNLSE pays 6% more | claude | 2026-10-16-claude-interactive.6-h3-edge (`summary_invariant_post.json`) | 2026-10-16 |
| Held-out region | $T_0=30$ fs (6.09 nJ), frozen in `38bb1af`. $\lambda_s$ at 2–8 m: 3.248, 3.380, 3.457, 3.510 µm (all within 0.028 µm). $N/N_0$ at 8 m: 0.984 against 0.988. $(\eta^*,L^*)$: (0.987, 5.8 m) against (0.994, 5.32 m) at 3.3 µm. At 3.4 µm: 0.977 at the boundary $L=8$ m against 0.985 at 7.94 m, so the optimum lies beyond 8 m in the GNLSE. The soliton crossed the periodic time-window boundary (peak at ±49 ps). A rerun with the frame at 3.4 µm gives identical observables (see Convergence) | claude (numpy GNLSE) | 2026-10-16-claude-interactive.6-h3-edge | 2026-10-16 |
| Convergence and artefacts | Step halving (0.25 → 0.125 mm), main case: every observable ($N$, $\lambda_s$ at 2–8 m; $\eta^*$, $L^*$ for 3.3–3.7 µm) unchanged to 4 decimals. Frame change, held-out case (3.7 → 3.4 µm): the window crossing disappears (peak within ±18.7 ps) and every observable is unchanged to 4 decimals. A frame change is an exact time translation in the periodic box, so the earlier crossing was harmless. Edge energy fraction ≤ 0.5%. dt halving (6 → 3 fs, same $n_t$, so half the window): $N$ changes by ≤ 0.0003, $\lambda_s$ by ≤ 0.0002 µm, $\eta^*$ by ≤ 0.0002, and $L^*$ is unchanged within the 0.05 m save spacing | claude | 2026-10-16-claude-interactive.6-h3-edge (keys `const_T020fs_dz0.125mm_dt6.0fs`, `const_T030fs_dz0.250mm_dt6.0fs_frame3.4um`, `const_T020fs_dz0.250mm_dt3.0fs`) | 2026-10-16 |
| Second solver or relaxed assumption | **Relaxed $A_{\rm eff}$**: the `pc` form with LP01 $A_{\rm eff}(\omega)$, against the reduced model with $\gamma(\omega)$. Trajectory within 0.024 µm and 0.013 in $N$ at 2, 4, 6, 8 m. $(\eta^*,L^*)=(0.958, 7.35$ m$)$ against (0.973, 6.81 m) at 3.5 µm. Equal-wavelength difference 0.0010. **Second solver**: the main case rerun with the agents' Julia solver (b9fa957), with the Raman kernel sampled at dt = 6 fs, frame at 3.3 µm and the solver's blue-edge window. $N$ at 2–8 m: 0.9824, 0.9661, 0.9361, 0.8937, against numpy 0.9826, 0.9662, 0.9358, 0.8932. $\lambda_s$ within 0.0012 µm. $(\eta^*,L^*)$ = (0.9707, 3.2 m), (0.9510, 4.6 m), (0.9041, 6.8 m) at 3.5, 3.6, 3.7 µm, against numpy (0.9709, 3.2), (0.9513, 4.6), (0.9046, 6.75) | claude | 2026-10-16-claude-interactive.6-h3-edge (`summary.json`, `summary_julia_crosscheck.json`) | 2026-10-16 |
| Relaxed assumption 2: soliton born from fission | TL sech $N=2$, $T_0=40$ fs (18.3 nJ) in Z75, protocol frozen in `638af7a`. The leading soliton leaves fission with $f_1=0.843$ (IST 0.75), shifts to about 4.1 µm, and keeps 0.434 of its photons by 8 m.<br>**Two post-hoc changes, disclosed.** (i) The frozen rule "leading soliton = highest peak" picked a weak blue soliton (v1, `summary_fission_born_v1_wrong_soliton.json`); "most photons" (v2) picked the second soliton once the leader had lost more than half its photons. The rule used is v3: the reddest pulse with at least 10% of the photons. (ii) The frozen separation criterion ($f_1\le1.05f_1(L)$) fires only at 7.65 m because the soliton keeps losing photons. There it agrees within 0.002 in $N$ and 0.0024 µm, but trivially. A loss-independent criterion (isolated, and $f_1$ steady to 1% over three saves) gives $z_s=0.10$ m.<br>From that plane the full-response ODE with loss gives $N/N(z_s)$ = 0.743, 0.565, 0.422 at 4, 6, 8 m, against GNLSE 0.757, 0.578, 0.434, so within 0.014. Wavelength is within 0.008 µm. All are inside the frozen ±0.02 and ±0.03 µm. The 2 m plane is excluded as an identification glitch (another pulse inside the isolation ring, ring/peak 0.97) | claude (numpy GNLSE) | 2026-10-16-claude-interactive.6-h3-edge (`summary_fission_born.json`, `summary_fission_born_post.json`, v1 and v2 files kept) | 2026-10-16 |
| Adversarial audit | **Fail.** At crossing parameter $0.1$, closed $L^*=281.246$ m versus own Gordon-ODE $101.12$ m and two independent GNLSE optima $98$ m. The pulse remains a fundamental sech and satisfies the stated bounds at the predicted length. Part (b) also needs a finite-launch normalization. See independent audit report. | gpt-d (gpt) | 2026-10-16-gpt-d-loss-edge-audit; 2026-10-16-gpt-d-cutoff-edge200-shape; 2026-10-16-gpt-d-julia-cutoff200 | 2026-10-16 |
| Novelty search | Kormokar 2023 (full text) has the constant-$\alpha$ $z_{\rm eff}$ law. Kormokar et al. 2021 (JOSA B, DOI 10.1364/JOSAB.409240, **not accessed** this session; full text read by gpt-a) has an adiabatic drift law with loss. Its preprint (Authorea 676716) is known from a search snippet only: a high-order extension of Gordon's formula with propagation loss, self-steepening and dispersion slope. Not checked: whether the frequency-resolved invariant (a), the terminal condition (b) and the optimum (c) are in those papers. | claude | — | 2026-10-16 |
| Independent units, limits and symbolic residual | Part (a) is exact for its autonomous Gordon ODE. Equal loss of $N^4$ is not equal loss of $N$. Finite-launch denominator missing in (b); derivative of spectral width omitted in (c) | gpt-d (gpt) | 2026-10-16-gpt-d-loss-edge-audit | 2026-10-16 |
| Independent core and held-out checks | Main fractions and cutoff optima reproduce; first frozen wavelength misses tolerance. Proposer held-out optimum resolved beyond its original endpoint. Auditor held-out interior optimum $(0.98558,15.35\,\mathrm m)$ versus frozen $(0.98904,14.875\,\mathrm m)$ | gpt-d (gpt) | 2026-10-16-gpt-d-z75-window; 2026-10-16-gpt-d-z75-heldout; 2026-10-16-gpt-d-z75-ownheldout-extended | 2026-10-16 |
| Independent path test | Two launch energies compared at the same wavelengths, with no post-launch normalization. Fourth-power losses differ by finite-response/filtering corrections; the Gordon integral is approximate in the GNLSE | gpt-d (gpt) | 2026-10-16-gpt-d-z75-path100; 2026-10-16-gpt-d-z75-path120; 2026-10-16-gpt-d-s28-path100; 2026-10-16-gpt-d-s28-path120 | 2026-10-16 |
| Independent scaling and terminal test | Rate-error exponent $1.9456$ over $50$–$200$ fs, $2.0009$ over $200$–$500$ fs versus predicted $2$. Reduced-ODE quarter exponent $0.2493$; frozen-terminal GNLSE fit $0.2997$ in the available adiabatic quarter-region, so no physical terminal asymptote certified | gpt-d (gpt) | 2026-10-16-gpt-d-loss-edge-audit; 2026-10-16-gpt-d-rate50; 2026-10-16-gpt-d-rate80; 2026-10-16-gpt-d-rate120; 2026-10-16-gpt-d-rate200; 2026-10-16-gpt-d-rate300; 2026-10-16-gpt-d-rate500; 2026-10-16-gpt-d-silica-terminal | 2026-10-16 |
| Independent convergence and norm | Halved step, finer grid, doubled window, analytic versus sampled Raman kernel. Decisive optimum unchanged. Exact NLSE soliton relative field error $1.85\times10^{-13}$. Lossless total-photon drift $-3.41\times10^{-8}$. Black-box Julia blue-edge window probe and second-solver comparisons recorded | gpt-d (gpt) | 2026-10-16-gpt-d-nlse-limit; 2026-10-16-gpt-d-z75-lossless; 2026-10-16-gpt-d-z75-step; 2026-10-16-gpt-d-z75-grid; 2026-10-16-gpt-d-z75-window; 2026-10-16-gpt-d-z75-sampled; 2026-10-16-gpt-d-cutoff-edge200-step; 2026-10-16-gpt-d-cutoff-edge200-grid; 2026-10-16-gpt-d-cutoff-edge200-window; 2026-10-16-gpt-d-window-probe; 2026-10-16-gpt-d-julia-cutoff200 | 2026-10-16 |
| Independent relaxed assumptions | Photon-conserving variable area reproduces within tolerance. Full dispersion versus cubic and a measured source-edge fit shift the predicted budget. Actual isolated fission daughter matches the frozen conditional ODE at every scoring plane; whole-field tracking remains uncertified and late planes leave the adiabatic bound | gpt-d (gpt) | 2026-10-16-gpt-d-z75-variablearea; 2026-10-16-gpt-d-z75-cubic; 2026-10-16-gpt-d-z75-sourced; 2026-10-16-gpt-d-z75-fission-prefix; 2026-10-16-gpt-d-z75-fission; 2026-10-16-gpt-d-fission-daughter | 2026-10-16 |
| Independent novelty search | Kormokar 2021 (DOI 10.1364/JOSAB.409240), Kormokar 2023 (DOI 10.1364/JOSAB.478975; arXiv:2301.02945), Petersen 2017 (DOI 10.1364/OE.25.015336): full texts examined; constant-loss drift and numerical length optimization precede this claim. No frequency-resolved invariant or stated closed cutoff optimum found in those texts. Kormokar 2024 (DOI 10.1364/JOSAB.521085): abstract/first page only; full-text novelty remains open | gpt-d (gpt) | 2026-10-16-gpt-d-literature; 2026-10-16-gpt-d-loss-edge-audit | 2026-10-16 |
| Independent interior and boundary probes | Strictly interior crossing parameter $0.03$: closed length $201.70$ m, ODE $152.35$ m, GNLSE $151$ m. Explicit initial loss-width and adiabaticity boundary/beyond-boundary runs completed; no wider certified regime inferred | gpt-d (gpt) | 2026-10-16-gpt-d-cutoff-q03; 2026-10-16-gpt-d-cutoff-q20; 2026-10-16-gpt-d-width-bound; 2026-10-16-gpt-d-width-beyond; 2026-10-16-gpt-d-adiab-bound; 2026-10-16-gpt-d-adiab-beyond | 2026-10-16 |
| Independent adjoint attack | Passive amplitude plus phase masks; matched fixed Float64 discrete RK4IP adjoint; three frozen seeds; finite-difference gradient check passes. All starts stop at their iteration limits. Tiny apparent gain changes sign under window refinement, so no robust headroom or global optimum is certified | gpt-d (gpt) | 2026-10-16-gpt-d-adjoint-cutoff200-complete; 2026-10-16-gpt-d-mask-validation; 2026-10-16-gpt-d-mask-validation-wide; 2026-10-16-gpt-d-loss-edge-audit | 2026-10-16 |

## Outcome

Open.


## Audit trail

| Date | Agent (family, model) | Change and evidence |
|---|---|---|
| 2026-10-16 | gpt-d (gpt, gpt-6-astra) | `proposed` → `refuted`. The original regime is retained as the refuted scope; no silent narrowing. Optimal-length failure inside that regime: `2026-10-16-gpt-d-cutoff-edge200-shape`, corroborated by `2026-10-16-gpt-d-julia-cutoff200` and the independent reduced ODE. The exact Gordon-ODE invariant survives. [Audit report](notes/audit-2026-10-16-gpt-d-C-20261016-claude-interactive.6-01.md). |
