---
agent: gpt-d
model: gpt-6-astra
family: gpt
date: 2026-10-16
claim: C-20261016-claude-interactive.6-02
task: T-20261016-claude-interactive.6-02
verdict: fail
status: independent-audit-complete
---

# Audit of the universal Raman rate bound

**Verdict: fail as written, because the stated long-pulse tightness law is false. The central inequality and energy-retention theorem pass the independent mathematical and numerical checks. No violation of either bound was found.** The card says that rate divided by bound decreases as $T^{-2}$ for long sech pulses. It decreases as $T^{-3}$. This distinction is not a reduced validity domain for the theorem: the theorem holds throughout the stated ideal model. The card should separate its correct theorem from its incorrect tightness assertion before promotion.

This report was prepared without reading the proposer's scripts, derivation notes, logs, PR description or branch history, or gpt-b's PR #46 review. The allowed claim card and cited run metadata/summaries were consulted. All calculations and scripts here are independent. The ambiguous held-out label “100 fs” was resolved from metadata as intensity FWHM, rather than sech width. Subsequent permitted reading, if any, is identified below.

![Independent tightness scaling and retained-energy checks](../../runs/2026-10-16-gpt-d-raman-bound-audit/audit_summary.png)

Figure data: `2026-10-16-gpt-d-raman-bound-audit`, with individual propagation run ids listed below.

## Restatement and assumptions

For a scalar, deterministic, lossless field with constant positive nonlinear index and mode area, the exact optical shock factor makes photon number invariant. A passive delayed response removes optical energy. The total Raman spectral weight then bounds the instantaneous energy-loss rate by a constant times energy squared. Integrating that differential inequality gives a lower bound on retained energy, regardless of pulse shape or real dispersion.

The argument also needs a finite positive photon norm, adequate field regularity for Parseval and integration by parts, vanishing temporal boundary terms, a finite right derivative of the causal response, and nonnegative $n_2 f_R$. The physical interpretation of the photon mean requires positive optical frequencies. No narrowband, fundamental-soliton, or long-pulse assumption is needed for the mathematical energy inequality. Numerical projections, absorbing frequency boundaries and the solver's blue prefactor window are extra model modifications and must be checked separately.

## Independent derivation and cheap attacks

Let $C=n_2f_R/(cA_{\rm eff})$, $I=|A|^2$, and $W(\Omega)=\Omega\operatorname{Im}H(\Omega)$. Directly differentiating the energy and integrating the shock derivative by parts yields

$$E'=-C\int I\,\partial_t(h_R*I)\,dt
     =-C\int W(\Omega)|\widetilde I(\Omega)|^2\frac{d\Omega}{2\pi}.$$

Real dispersion contributes zero. The instantaneous Kerr contribution is a total derivative. Dividing the spectral field equation by optical frequency before taking its quadratic norm gives $\mathcal N'=0$. These are distinct conservation statements: Raman preserves photons and decreases optical energy.

For passive $W$, $|\widetilde I|\le E$ gives $-E'\le CE^2\int W/(2\pi)$. The one-sided derivative jump at the causal origin supplies $\int W/(2\pi)=h'_R(0^+)/2$. The half is essential. Consequently $(1/E)'\le\kappa_U$, and both the stated retention inequality and photon-harmonic-mean wavelength inequality follow. Units, the zero-Raman limit, constant global phase, time translation and amplitude scaling all agree. Frequency translation leaves this instantaneous energy functional unchanged when the translated field retains positive-frequency support; it is not a symmetry of propagation through a fixed arbitrary dispersion curve.

For $a=1/\tau_2$, $b=1/\tau_1$, the independently obtained oscillator weight is

$$W(\Omega)=\frac{2a(a^2+b^2)\Omega^2}{(a^2+b^2-\Omega^2)^2+4a^2\Omega^2}\ge0.$$

This proves passivity for both oscillator responses actually used, rather than just sampling it. Independent quadrature of the sum rule has relative error $2.22\times10^{-16}$. The silica coefficient is $9.3103132\times10^{-4}$ pJ$^{-1}$m$^{-1}$, agreeing with the card; the fluoride stand-in gives $3.7603908\times10^{-4}$ in the same units (`2026-10-16-gpt-d-raman-bound-audit`, `math_summary.json`). A positive sum of such oscillators also remains passive. This does not establish passivity or the same coefficient for every measured multi-band response.

Direct FFT functional checks reproduce the phase/time/frequency-translation invariances and the quartic field-amplitude dependence. The Kerr-only derivative is at floating-point roundoff (`2026-10-16-gpt-d-raman-bound-audit`, `symmetry_summary.json`).

## Decisive failed check: tightness exponent

For $I=E\operatorname{sech}^2(t/T)/(2T)$, $\widetilde I/E=(\pi\Omega T/2)/\sinh(\pi\Omega T/2)$. Expanding the passive oscillator at low frequency and integrating this intensity spectrum gives

$$\rho(T)\equiv\frac{-E'}{\kappa_U E^2}
\sim\frac{16a}{15(a^2+b^2)^2T^3}\quad(T/\tau_1\to\infty).$$

The missing inverse power in the card comes from the shrinking integration bandwidth. This prediction, including its coefficient, was committed before numerical quadrature and propagation (`42e3eac`, `2026-10-16-gpt-d-raman-bound-audit/protocol.md`). Quadrature gives decay exponent $3.0172$ on $10\le T/\tau_1\le80$ and $3.00158$ on $40\le T/\tau_1\le160$, versus the card's $2$. The independent GNLSE's actual RHS energy derivative gives the same exponents, including $3.00158$ in the farther asymptotic subset (`2026-10-16-gpt-d-c02-rate10`, `2026-10-16-gpt-d-c02-rate20`, `2026-10-16-gpt-d-c02-rate40`, `2026-10-16-gpt-d-c02-rate80`, `2026-10-16-gpt-d-c02-rate160`; full run ids carry the same `2026-10-16-gpt-d-c02` prefix). The corresponding fluoride quadrature exponent is $3.00153$ (`2026-10-16-gpt-d-raman-bound-audit`).

For the short-pulse limit, the independently frozen prediction is $1-\rho\sim2T/\tau_2$. Its measured exponent is $1.00198$ in silica and $1.00181$ in the fluoride oscillator, against predicted $1$ (`2026-10-16-gpt-d-raman-bound-audit`). These are asymptotic quadrature tests; they do not claim that an envelope model is a calibrated physical description at arbitrarily small duration.

## Core and held-out propagation

The independent Python implementation calculates the energy rate directly from the nonlinear RHS, separately calculates the spectral identity, and integrates both at every RK stage. It does not enforce the identity by definition or estimate its integral from sparse saved output.

| Case | Retained energy | Retention lower bound | Maximum rate/bound | Run |
|---|---:|---:|---:|---|
| Core, soliton order 3 | 0.885179 | 0.201725 | 0.231692 | `2026-10-16-gpt-d-c02-core` |
| Held out, order 4, short pulse | 0.903725 | 0.321489 | 0.175075 | `2026-10-16-gpt-d-c02-heldout4` |
| Held out, order 6, short pulse | 0.882487 | 0.173953 | 0.0892784 | `2026-10-16-gpt-d-c02-heldout6-fine` |
| Held out, order 6, long pulse | 0.893168 | 0.112236 | 0.0824761 | `2026-10-16-gpt-d-c02-heldout6long` |
| Auditor's chirped coherent pulse pair | 0.998724 | 0.992607 | 0.230830 | `2026-10-16-gpt-d-c02-own` |

The core and all prescribed held-out retention inequalities pass at every saved plane. The held-out rate maxima remain below the frozen ceiling and occur near the first compression. The core's original stricter slack prediction fails, as the proposer already disclosed; it is not required by the exact theorem. The auditor's arbitrary-field case was frozen before execution and tests an interfering, spectrally chirped pair rather than another sech ansatz.

The core's integrated identity mismatch is $2.77\times10^{-6}$, decreasing to $1.39\times10^{-7}$ on step halving, below the frozen tolerance (`2026-10-16-gpt-d-c02-core`, `2026-10-16-gpt-d-c02-core-step`). The arbitrary pair gives $2.78\times10^{-11}$ (`2026-10-16-gpt-d-c02-own`). Energy decreases at every saved plane, and photon drift decreases under refinement. The theorem itself has no perturbative error exponent; the measured exponent above tests the card's separate asymptotic tightness statement.

## Approaching and optimizing against the bound

Formal, constant-area, zero-dispersion tests with positive-frequency input support attain maximum ratios $0.86585$, $0.93378$ and $0.95566$ as the sech width decreases from $2$ fs to $1$ fs and $0.5$ fs. Window doubling gives $0.95564$ in the shortest case (`2026-10-16-gpt-d-c02-short2p0`, `2026-10-16-gpt-d-c02-short1p0`, `2026-10-16-gpt-d-c02-short0p5`, `2026-10-16-gpt-d-c02-short0p5-wide`). Thus the constant is not merely a very loose algebraic ceiling over unrestricted model fields. These tests are explicitly not calibrated predictions for subcycle pulses in a real fibre; finite positive-frequency projection also prevents identifying them with the mathematical delta-pulse limit.

The requested adjoint attack optimized five spectral phase coefficients, with $|m|=1$, using L-BFGS and seeds $(101,305,707)$. The forward was fixed-step Float64 RK4IP and the backward used `adjoint_mode=:discrete_rk4ip` with exactly the forward step. The mixed directional derivative agrees with finite differences to relative error $1.58\times10^{-7}$; changing checkpoint stride leaves it unchanged. The objective was $(E_0-E_L)/(\kappa_U E_0^2L)$, whose allowed ceiling follows from the retention bound. The baseline objective is $0.86577168$ and the best is $0.86577286$. One start converged; the other two reached their iteration limits with almost identical values (`2026-10-16-gpt-d-c02-adjoint`). No violation was found.

Independent replays with an analytic Raman kernel give $0.86577175$ and $0.86577293$ for baseline and optimized phase. Halving the propagation step, refining the temporal grid and doubling the window preserve these values (`2026-10-16-gpt-d-c02-mask-base-tl`, `2026-10-16-gpt-d-c02-mask-base-shaped`, `2026-10-16-gpt-d-c02-mask-step-tl`, `2026-10-16-gpt-d-c02-mask-step-shaped`, `2026-10-16-gpt-d-c02-mask-fine-tl`, `2026-10-16-gpt-d-c02-mask-fine-shaped`, `2026-10-16-gpt-d-c02-mask-wide-tl`, `2026-10-16-gpt-d-c02-mask-wide-shaped`). This confirms the small finite-distance phase adjustment, not a global optimum over all inputs. At a fixed spectral amplitude, flat or linear spectral phase maximizes the instantaneous Raman energy-loss functional by the autocorrelation triangle inequality; a finite-distance optimum can compensate subsequent evolution.

## Artefacts and relaxed assumptions

The compressed short-pulse held-out case was repeated with half step, finer time spacing at fixed window, and doubled window. The fine grid removes the instantaneous identity residual due to aliased nonlinear products, from $5.37\times10^{-5}$ of the bound to $3.74\times10^{-15}$. Its maximum ratio changes from $0.0892803$ to $0.0892784$; the retention changes by $5.35\times10^{-6}$. Window doubling changes retention by $6.56\times10^{-9}$ (`2026-10-16-gpt-d-c02-heldout6`, `2026-10-16-gpt-d-c02-heldout6-step`, `2026-10-16-gpt-d-c02-heldout6-fine`, `2026-10-16-gpt-d-c02-heldout6-wide`). The larger grids are disclosed convergence exceptions, with no dense matrices or full field histories.

The observed two-step photon-drift slope is $4.24$ in the core and $4.92$ in the high-order case; the stage-integrated RHS mismatch slopes are $4.32$ and $4.87$. These are finite-resolution two-point slopes, not a claimed universal convergence order. They do not reproduce the proposer's asserted third-order drift. The checks relevant to the bound already pass; an additional solver-order claim would require a dedicated asymptotic sequence (`2026-10-16-gpt-d-raman-bound-audit`, `summary.json`).

The actual agents' Julia solver gives core energy retention $0.88517745$, versus Python $0.88517859$, and photon drift $3.61\times10^{-7}$ at the resolved grid (`2026-10-16-gpt-d-c02-julia-core`, `2026-10-16-gpt-d-c02-core`). Its saved rate diagnostic evaluates the ideal identity on the Julia fields; it is not mislabeled as Julia's exact RHS. The solver's fixed blue prefactor window remains a documented numerical modification. Independent black-box probing was performed during claim 01 (`2026-10-16-gpt-d-window-probe`); here temporal refinement moves occupied bands away from that edge and the second-solver agreement is correspondingly close. No solver implementation source was inspected.

With frequency-dependent mode area in the photon-conserving form, use $B=\mathcal F^{-1}[(A_0/A(\omega))^{1/4}\widetilde A]$. The exact identity has $|B|^2$ in place of $I$, and the bound becomes $-E'\le\kappa_U E_B^2$, where $E_B=\int|B|^2dt$. The unweighted $E^2$ theorem is not automatically transferable. The relaxed-area run retains $0.900050$ of its energy, has maximum weighted ratio $0.226060$, integrated-identity mismatch $1.72\times10^{-6}$ and photon drift $3.41\times10^{-7}$ (`2026-10-16-gpt-d-c02-area`). This supports the card's caveat rather than extending its unweighted bound without proof.

## Prior work, usefulness and sign-off

Bonetti et al., DOI **10.1364/JOSAB.377891**, **full text**, introduce the photon-conserving generalization, show its reduction to the usual positive shock coefficient, and demonstrate energy loss and photon conservation. Their numbered equations do not explicitly give the general spectral energy identity or the $E^2$ retention bound. The identity is a direct corollary of their model; its physical content is prior work. Linale et al., DOI **10.1364/OL.401096**, **full text**, treat self-steepening and photon conservation primarily without Raman; the claimed universal Raman bound was not found there. Huang et al., **arXiv:2607.05244**, **full text accessed, energy and bright-soliton sections read**, give the long-pulse sech energy-loss law with the inverse-cube width dependence, consistent with the independent correction here. These sources and the exact search strings are recorded in `2026-10-16-gpt-d-c02-literature`.

The extra inequality is a short positivity/triangle-inequality argument followed by a differential-inequality integration. I did not find its exact constant and retention form in the searched sources. That restricted negative search does not establish novelty or publication interest. It is a useful model consistency check and a sharp instantaneous ceiling in the unrestricted model, but a weak practical lower bound for the tested high-energy fission fields. Near-saturation requires temporal scales at which a calibrated material response and a suitable carrier-resolved propagation model matter.

I would sign off on the central theorem for $E>0$, $\mathcal N>0$, nonnegative passive weight, $h_R(0^+)=0$, finite $h'_R(0^+)$, constant positive area/index, no linear loss or gain, and real dispersion. There is no small-parameter restriction: $T/\tau_1>0$ and $\kappa_U E_0L\ge0$. The practical usefulness condition $\kappa_U E_0L\lesssim1$ is not a validity condition. No special relation between independently adjustable material parameters is required.

The blocker for the card as written is the false inverse-square tightness statement. Core inequalities, the constant, passivity of the used responses, and the specified held-out predictions pass. Remaining concerns are material calibration of the formal near-saturation regime and completeness of the novelty search. The original regime is retained as the refuted scope; it is not silently narrowed or rewritten to hide the failed scaling check.

## Post-commit comparison

After independent report commit `4f82776`, I read the energy-identity section of gpt-b's review in PR #46 (`docs/review-2026-10-16-gpt-b-supercontinuum-literature.md`). It independently gives exactly the same spectral energy identity, photon cancellation and passivity qualification. Its subsequent bound uses peak power and the supremum of the Raman weight, whereas this claim uses energy squared and the integrated weight. This confirms that the identity is already established within the project; it does not change the mathematical verdict or rescue the failed tightness exponent. No proposer implementation was opened for this claim.

A subsequent institutional-repository search located Linale, Fierens and Grosz, DOI **10.1109/JQE.2020.3047691**, **full text**, published in the 2021 journal volume after online publication in 2020. Sections II–IV and Appendix A analyze Raman/steepening dynamics and higher-order nonlinearity, including the distinction between the conventional and photon-conserving models. I did not find the general spectral energy identity, the energy-squared coefficient, or the integrated retention inequality explicitly stated there. This closes the specific Linale access gap, but does not establish novelty over the entire literature (`2026-10-16-gpt-d-c02-literature`).
