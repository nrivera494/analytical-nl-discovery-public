---
agent: gpt-d
model: gpt-6-astra
family: gpt
date: 2026-10-16
claim: C-20261016-claude-interactive.6-01
task: T-20261016-claude-interactive.6-01
verdict: fail
status: independent-audit-complete
---

# Audit of the loss-edge soliton budget

**Verdict: fail as stated.** The fourth-power first integral is correct for the specified Gordon ODE. The closed-form optimal length fails at the stated crossing-parameter boundary, even while the other dimensionless bounds hold. The terminal expression also drops a finite-launch normalization without stating the corresponding far-from-edge condition. These findings do not negate the usefulness of a numerically integrated, full-response soliton model.

The first independent report was committed before consulting any proposer implementation, derivation notes, logs, PR description or branch history. Only the permitted cards, evaluator, solver documentation and cited run metadata/summaries were used. Setup printed commit subjects and merge file names incidentally. All implementations and runs below are the auditor's. Subsequent permitted reading is disclosed below.

## Restatement and assumptions

The claim eliminates distance from a single soliton's Raman drift and absorption equations to predict the photons remaining at a specified frequency. It then approximates extinction at a loss edge and maximizes the photon tail beyond a cutoff over fibre length. This is a conditional result for a soliton, not an upper bound over all shaped laser inputs.

Besides the explicit assumptions on polarization, spatial mode, Raman response and mode area, the reduction requires a pulse close to a local fundamental sech, sufficiently narrow relative to its carrier, no appreciable photon exchange with radiation or another pulse, and material coefficients that depend on frequency rather than independently on distance. The Gordon first integral additionally neglects the absorption-induced centroid blueshift. The cutoff formula needs the loss-per-frequency and spectral width to vary little throughout the crossing interval; its stated bound on the crossing parameter alone does not guarantee this.

## Decisive attack: optimal length

The independently chosen silica case uses a fundamental pulse at the edge of the allowed crossing regime. Parameters and both predictions were frozen in `runs/2026-10-16-gpt-d-loss-edge-audit/cutoff_long_predictions.json` before propagation (commit `2759a43`). The constant quadratic dispersion isolates the claimed mechanism.

| Quantity | Result | Run |
|---|---|---|
| Input duration and cutoff | $T_0=200$ fs, launch $2$ µm, cutoff $2.001$ µm | `2026-10-16-gpt-d-cutoff-edge200` |
| Crossing parameter | $\varepsilon/(2a)=0.1$ | `2026-10-16-gpt-d-loss-edge-audit` |
| Claimed closed-form length | $281.246$ m | `2026-10-16-gpt-d-loss-edge-audit` |
| Direct Gordon-ODE optimum | $101.12$ m | `2026-10-16-gpt-d-loss-edge-audit` |
| Independent GNLSE optimum | $98$ m | `2026-10-16-gpt-d-cutoff-edge200` |
| Adiabaticity near the predicted length | $\alpha z_0=0.00796$ | `2026-10-16-gpt-d-cutoff-edge200` |
| Other conditions there | $(wT_s)^{-2}=0.00391$, $T_s/\tau_1=33.4$ | `2026-10-16-gpt-d-cutoff-edge200` |
| Step, time-grid and window checks | All retain the $98$ m optimum | `2026-10-16-gpt-d-cutoff-edge200-step`, `2026-10-16-gpt-d-cutoff-edge200-grid`, `2026-10-16-gpt-d-cutoff-edge200-window` |

The photon-fraction approximation is much less affected: the closed form gives $0.65091$, the exact reduced optimization $0.66596$, and the doubled-window GNLSE $0.66768$ (same runs). The discrete cutoff-bin integration changes the GNLSE fraction by about $0.0052$ on window doubling; it does not move the length maximum. A second long-pulse case predicts $887.13$ m and peaks near $350.95$ m while remaining adiabatic at both lengths (`2026-10-16-gpt-d-cutoff-edge300`). The earlier, shorter-pulse attack is retained as a pilot; its predicted length leaves the regime and is not the decisive counterexample (`2026-10-16-gpt-d-cutoff-edge`).

The failure also occurs strictly inside the crossing bound. At crossing parameter $0.03$, the frozen closed length is $201.70$ m, the direct ODE maximum is $152.35$ m, and the GNLSE maximum is $151$ m. Adiabaticity stays below $0.001$ throughout that run (`2026-10-16-gpt-d-cutoff-q03`; prediction frozen in commit `ce9d7dc`). Beyond the stated domain, at crossing parameter $0.2$, the proposed crossing frequency is beyond the available photon budget and gives no finite admissible length; the GNLSE nevertheless has an interior maximum at $59$ m (`2026-10-16-gpt-d-cutoff-q20`). The latter is an extrapolation check, not an in-domain refutation. These near-launch cutoffs are explicitly permitted by the card's stated regime; they test the uniformity of the claimed formula rather than reproduce the main fluoride geometry.

The derivative explains the failure. Put $\delta=\omega_c-\omega$ and allow $a=a(\omega)$. Exact stationarity of the proposed sech-tail objective requires

$$\varepsilon(\omega)=[a(\omega)-\delta a'(\omega)]\{1-\tanh[a(\omega)\delta]\}.$$

The card omits $a'$ and evaluates $\varepsilon$ at the cutoff. As photons are lost the pulse broadens and its Raman rate drops strongly, so neither replacement is uniform near extinction. This discrepancy already occurs within the claim's own ODE, independently of any GNLSE implementation.

## Cheap checks and terminal limit

Units, signs, the lossless limit, and the constant-loss effective-length limit of part (a) pass. Equal $N_0^4-N^4$ does **not** mean equal lost photon counts $N_0-N$: two exact constant-coefficient trajectories demonstrate the distinction in `2026-10-16-gpt-d-loss-edge-audit/algebra_summary.json`.

For genuinely exponential $\alpha/K$, the finite-launch answer is

$$\left(\frac{N}{N_0}\right)^4=
\frac{1-\exp[-(\omega-\omega_\infty)/w_{\rm eff}]}{1-\exp[-(\omega_0-\omega_\infty)/w_{\rm eff}]}.$$

The omitted denominator matters unless $(\omega_0-\omega_\infty)/w_{\rm eff}\gg1$. For example, at an initial detuning of one effective edge width the card gives an initial photon fraction $0.89166$ instead of unity (`2026-10-16-gpt-d-loss-edge-audit`). The corresponding terminal condition needs the same finite-initial-frequency correction. Also, the distance diverges logarithmically in the inverse remaining detuning; the detuning approaches its terminal value exponentially in distance, not logarithmically.

The quarter-power exponent is correct for the exact reduced ODE. The independent fit gives $0.24929$ against $0.25$ (`2026-10-16-gpt-d-loss-edge-audit`). It is not a uniform GNLSE terminal law. At a nonzero absorption edge, $T_s\propto1/N$ makes $\alpha z_0$ diverge as photons vanish. Absorption's centroid blueshift also eventually competes with the Raman drift.

The silica terminal prediction was frozen at $\lambda_\infty=2.090339$ µm before propagation. A long run reaches photon fraction $0.04028$ and wavelength $2.089750$ µm, then has a positive centroid drift because filtering dominates (`2026-10-16-gpt-d-silica-terminal`). The fixed-prediction quarter-region fit, restricted to the stated adiabatic bound, gives exponent $0.300$ over the available interval, versus $0.25$; a terminal asymptote within the adiabatic domain was not established. Late-time values use the full photon norm: a fixed temporal isolation gate ceases to contain the broadened pulse. The late regime is outside the claim's adiabatic assumption and is not presented as an in-domain refutation.

## Independent reproduction, path tests and scaling

The fluoride runs use independently reconstructed LP01 properties. In the doubled-window main run, the soliton photon fractions at the four frozen planes are $(0.98256,0.96647,0.93595,0.89344)$ and wavelengths are $(3.55428,3.69614,3.77086,3.81742)$ µm. The first wavelength misses the frozen tolerance; the other listed quantities pass (`2026-10-16-gpt-d-z75-window`). The main launch is not already in the long-pulse asymptotic regime, so this mismatch is distinct from the decisive in-regime length counterexample.

| Case and cutoff | Frozen $(\eta^*,L^*/\mathrm m)$ | Independent GNLSE | Run |
|---|---|---|---|
| Main, $3.5$ µm | $(0.986,2.83)$ | $(0.97092,3.25)$ | `2026-10-16-gpt-d-z75-window` |
| Main, $3.6$ µm | $(0.967,4.12)$ | $(0.95130,4.60)$ | same run |
| Main, $3.7$ µm | $(0.921,6.19)$ | $(0.90483,6.75)$ | same run |
| Proposer held-out, $3.3$ µm | $(0.994,5.32)$ | $(0.98735,5.80)$ | `2026-10-16-gpt-d-z75-heldout` |
| Proposer held-out, $3.4$ µm | $(0.985,7.94)$ | $(0.97848,8.425)$ | same run, extended beyond the original endpoint |
| Auditor held-out, $T_0=40$ fs, $3.3$ µm | $(0.98904,14.875)$ | $(0.98558,15.35)$ | `2026-10-16-gpt-d-z75-ownheldout-extended` |
| Photon-conserving variable area, $3.5$ µm | $(0.973,6.81)$ | $(0.95828,7.325)$ | `2026-10-16-gpt-d-z75-variablearea` |

The auditor's case and extension were committed before their respective runs. Its cutoff maximum is interior, and the dimensionless bounds hold there. These local prediction successes do not establish the closed form uniformly over the whole claimed regime. Prediction files and detailed comparisons are in `2026-10-16-gpt-d-loss-edge-audit`.

Direct common-wavelength tests use two different launch energies in each fibre, without resetting the photon budget after propagation. At $3.65$ µm the two fluoride fourth-power losses are $0.21026$ and $0.21639$ in units of $10^{44}$ photons$^4$, versus a common Gordon integral $0.23416$ (`2026-10-16-gpt-d-z75-path100`, `2026-10-16-gpt-d-z75-path120`). At $2.02$ µm in silica they are $1.14393$ and $1.16037$ in units of $10^{40}$ photons$^4$, versus $1.17297$ (`2026-10-16-gpt-d-s28-path100`, `2026-10-16-gpt-d-s28-path120`). All quoted crossings satisfy the stated bounds. The residual contains finite-response and spectral-filtering corrections. The universal fourth-power subtraction is therefore an approximate physical model; replacing it by a general two-variable ODE does not retain an energy-independent function $\Lambda$.

At a fixed small fraction of the dispersion length, independent GNLSE shift errors scale with exponent $1.9456$ over the specified pulse-width range, approaching $2.0009$ in the longer-pulse subset, against the predicted exponent $2$ (`2026-10-16-gpt-d-rate50`, `2026-10-16-gpt-d-rate80`, `2026-10-16-gpt-d-rate120`, `2026-10-16-gpt-d-rate200`, `2026-10-16-gpt-d-rate300`, `2026-10-16-gpt-d-rate500`; fit in `2026-10-16-gpt-d-loss-edge-audit`). This supports the rate asymptotics, while not establishing uniform accuracy of a terminal-frequency prediction.

## Literature, physical realization and remaining checks

The independent full-text comparisons are recorded with access levels in `runs/2026-10-16-gpt-d-loss-edge-audit/novelty.md`. Kormokar 2021 (DOI 10.1364/JOSAB.409240, full text) and Kormokar 2023 (DOI 10.1364/JOSAB.478975, arXiv:2301.02945, full text) already contain the constant-loss drift/effective-length law. Petersen 2017 (DOI 10.1364/OE.25.015336, full text) establishes loss-driven length optimization numerically and experimentally. I did not find the frequency-dependent photon invariant or the stated analytic cutoff optimum in those three texts. This is a restricted negative search, not a proof of novelty. The invariant is an elementary elimination of distance from known drift equations.

Xia 2006 (DOI 10.1364/OL.31.002553, full text) supplies measured ZBLAN absorption-edge points. Their independent fit gives an edge slope $86.15$ µm and attenuation $0.603$ dB/m at the claim's reference wavelength, replacing assumed $92$ µm and $1$ dB/m (`2026-10-16-gpt-d-loss-edge-audit`). These measurements are from a different fibre and are a material sensitivity, not a Z75 calibration. Primary nonlinear-index measurements were located in Yan 2012 (DOI 10.1364/JOSAB.29.000238, abstract/table/preview only) and Adair 1987 (DOI 10.1364/JOSAB.4.000875, abstract/tables only); a defensible measured replacement for the specified Z75 fibre was not established.

No fine-tuned unphysical parameter identity is needed for the isolated-soliton ODE. A manufactured fibre nevertheless needs its own loss, nonlinear-index and Raman calibration. A mode-selected launch is also an assumption, rather than a consequence of the specified fluoride geometry (Boilard et al., arXiv:2109.13366, full text).

The source-edge rerun changes the fluoride optima at the three main cutoffs to $(0.97387,3.375\,\mathrm m)$, $(0.95872,4.725\,\mathrm m)$ and $(0.92403,6.90\,\mathrm m)$ (`2026-10-16-gpt-d-z75-sourced`). This is a noticeable photon-budget sensitivity at the longest cutoff. Keeping only $\beta_2$ and $\beta_3$ gives lengths $(2.075,2.625,3.275)$ m instead; a local cubic expansion is not interchangeable with the full curve over this shift (`2026-10-16-gpt-d-z75-cubic`, `2026-10-16-gpt-d-z75-window`).

At fixed launched photon number, changing the assumed $n_2$ by $-10\%$ or $+10\%$ moves the Gordon terminal prediction from $3.9113$ µm to $3.8728$ or $3.9466$ µm. Maintaining a fundamental pulse at fixed photon number requires retuning its width. If instead the width is fixed and the fundamental energy is retuned inversely with $n_2$, the normalized trajectory is unchanged. These are different experimental comparisons, not evidence that a fixed laser input is insensitive to $n_2$ (`2026-10-16-gpt-d-loss-edge-audit/followup_predictions.json`). The larger alternative nonlinear-index value discussed in Agger et al. (DOI 10.1364/JOSAB.29.000635, full text) is retained only as a sensitivity scenario, not adopted as a measured calibration of this fibre.

## Fission and numerical artefacts

The independent fission protocol selects a separated, approximately sech daughter before freezing its conditional trajectory. The selected formation plane is $0.0625$ m, with photon fraction $0.84491$, fitted width $24.01$ fs and nearest-pulse separation $12.75$ fitted widths (`2026-10-16-gpt-d-z75-fission-prefix`; frozen continuation in `2026-10-16-gpt-d-loss-edge-audit`). The whole-field long run suffers periodic-window overlap and inconsistent pulse identification. It is retained as an inconclusive run, not scored as a physical failure (`2026-10-16-gpt-d-z75-fission`).

A disclosed post-pilot check isolates the actual daughter field at $0.5$ m and continues its amplitude and phase, without replacing it by a sech. It retains the original frozen formation-plane prediction and scores every requested plane, including the earliest one. The photon-ratio errors are $(0.00829,0.01463,0.01393,0.01159)$ and wavelength errors $(-0.01632,-0.00528,-0.00239,-0.00155)$ µm, all inside the stated tolerances. The later two planes exceed the stated adiabaticity bound, despite agreeing numerically (`2026-10-16-gpt-d-fission-daughter`; comparison in `2026-10-16-gpt-d-loss-edge-audit/supplement_summary.json`). This supports the isolated-daughter reduction but does not certify the whole fission field. Task `T-20261016-gpt-d-03` retains that loose end.

The independent unperturbed NLSE soliton check has relative field error $1.85\times10^{-13}$ after removing its known global phase (`2026-10-16-gpt-d-nlse-limit`). The lossless photon-conserving fluoride run has total-photon drift $-3.41\times10^{-8}$; energy is not the conserved norm with Raman (`2026-10-16-gpt-d-z75-lossless`). Global phase and time translation leave the equations and photon observables invariant; frequency translation is not a symmetry of frequency-dependent dispersion and absorption.

Step halving, grid refinement, and window doubling are recorded separately. For the main case, step halving changes the maximum cutoff fraction by at most $1.60\times10^{-6}$. Window doubling changes it by less than $1.8\times10^{-4}$, although a temporal isolation gate is more sensitive to weak radiation. Analytic and sampled causal Raman kernels were compared at a $3$ fs spacing (`2026-10-16-gpt-d-z75-step`, `2026-10-16-gpt-d-z75-grid`, `2026-10-16-gpt-d-z75-window`, `2026-10-16-gpt-d-z75-wide`, `2026-10-16-gpt-d-z75-sampled`).

The decisive long-pulse case remains a local fundamental soliton: at the measured and predicted optima, the intensity-fit residuals are $0.00257$ and $0.00169$, and measured-to-fundamental width ratios are $1.00027$ and $0.99675$ (`2026-10-16-gpt-d-cutoff-edge200-shape`). The Julia solver independently peaks at the same $98$ m with cutoff fraction $0.66718$, versus Python $0.66765$ on the matched grid (`2026-10-16-gpt-d-julia-cutoff200`, `2026-10-16-gpt-d-cutoff-edge200-shape`). Its final photon fraction differs by $7.57\times10^{-5}$. A separate fluoride comparison at the first scoring plane agrees in total photons to $7.73\times10^{-6}$ (`2026-10-16-gpt-d-julia-z75-window`).

A black-box four-wave-mixing probe confirms that the Julia implementation suppresses nonlinear generation near the blue grid edge: the prefactor is $0.993$ at $0.85$ Nyquist and $0.581$ at $0.95$ Nyquist, while the tested red-edge point is unaffected (`2026-10-16-gpt-d-window-probe`). This is a numerical modification, not physical absorption. The decisive silica spectrum has negligible edge occupancy, and both independent window refinement and the second solver preserve its optimum. The probe did not inspect implementation source.

The requested spectral-mask attack used nine phase/attenuation coefficients, passive amplitude masks, L-BFGS, and seeds $(101,203,307)$. The forward and explicitly selected `adjoint_mode=:discrete_rk4ip` both used fixed-step Float64 RK4IP with the same step. A mixed directional finite-difference check has relative error $7.49\times10^{-9}$, and changing checkpoint stride leaves the gradient unchanged. Each start reached its iteration limit without satisfying the convergence criterion. The best coarse-grid fraction is $0.664555$ against baseline $0.664367$ (`2026-10-16-gpt-d-adjoint-cutoff200-complete`). This is a search over a relaxed launch family: a nontrivial mask need not preserve the initially fundamental-soliton assumption, so it is not used to refute the conditional invariant.

Independent propagation of that mask, step halving, grid refinement, two successive window doublings, and continuous cutoff integration show that the tiny gain is not converged in the propagation window. It changes sign across the tested windows even after resolving the cutoff integral. No robust extra headroom or global optimum is certified (`2026-10-16-gpt-d-mask-validation`, `2026-10-16-gpt-d-mask-validation-wide`; continuous quadrature in `2026-10-16-gpt-d-loss-edge-audit/mask_continuous_summary.json`). The failed first launch is retained under `2026-10-16-gpt-d-adjoint-cutoff200`; its termination cause was not established. A diagnostic restart exposed an unavailable optimizer convenience API and is retained under `2026-10-16-gpt-d-adjoint-cutoff200-retry`. The successful run uses the public objective/gradient interface with the original starts and numerical protocol.

Explicit boundary probes were frozen before propagation. At initial loss-width parameters $0.25$ and $0.5$, the measured spectral-to-centre loss factors are $1.04295$ and $1.08862$, consistent with the finite-bandwidth correction and its growth outside the stated range (`2026-10-16-gpt-d-width-bound`, `2026-10-16-gpt-d-width-beyond`). Separate runs start at adiabaticity $0.01$ and $0.03$ and follow its increase; the latter is an intentional out-of-regime probe, not a certified extension (`2026-10-16-gpt-d-adiab-bound`, `2026-10-16-gpt-d-adiab-beyond`). The pulse-width rate sweep includes the stated lower boundary and shorter pulses. Thus the crossing, loss-width, adiabaticity and Raman-duration boundaries have all been probed explicitly.

The first independent mask replay emitted BLAS floating-point flags. Elementwise reconstruction of every stored masked input is finite, passive and agrees to relative error about $10^{-15}$; the wider-window rerun uses that contraction directly (`2026-10-16-gpt-d-loss-edge-audit/mask_reconstruction_summary.json`). Those warnings are not treated as evidence for or against the claim.

## Post-commit shaping comparison

After the first independent report was committed (`08a7320`), I read only the proposer's shaping-run metadata and summary, not its code, derivation notes, logs or PR description. This did not change the loss-edge verdict. The shaping case was a lossless silica model with a roughly $100$ fs intensity FWHM pulse, soliton order $3$ (plus an order-$2$ extension), and a fixed fibre endpoint. Those parameter values and access disclosure are recorded in `2026-10-16-gpt-d-literature`.

Rosenberg et al. (DOI 10.1364/OE.383014, full text through an indexed author upload) instead study few-cycle input, fission and passage through an absorption band. Their negative-prechirp benefit changes the energy partition into the leading daughter and is strongest at higher soliton order; their fundamental case favours near-zero chirp. Thus their result does not conflict with a small local gain in the proposer's longer-pulse, lossless case. Neither experiment nor the proposer's limited searches establishes a universal shaping ceiling. An independent fine-GDD scan finds a small gain at $+150$ fs²: the refined-grid cutoff fraction increases from $0.304646$ to $0.305139$, or about $0.162\%$. Window doubling gives the same relative gain. This is enough to reject the categorical phrase “GDD never helps,” but is a small local improvement, not a practically large shaping headroom (`2026-10-16-gpt-d-chirp-silica`, `2026-10-16-gpt-d-chirp-convergence`).

## Regime I would sign off on

I sign off on part (a) as an exact first integral **of its stated autonomous ODE**, with positive $K$, nonnegative absorption, and positive remaining $N_0^4-\Lambda$. The full collection of statements has no certified physical regime under the card's present bounds. Any repaired cutoff approximation must additionally control $|\delta\partial_\omega\log a|$ and $|\delta\partial_\omega\log\varepsilon|$ throughout the crossing. Any physical quarter-power test must control the terminal-frequency prediction error relative to the remaining detuning, the filtering-to-Raman drift ratio, and adiabaticity simultaneously. No numerical bounds for a repaired joint regime are certified here. Repair and full-text novelty follow-up are tracked by `T-20261016-gpt-d-01`, material calibration by `T-20261016-gpt-d-02`, whole-field fission by `T-20261016-gpt-d-03`, and a calibrated chirp comparison by `T-20261016-gpt-d-04`. The original claim regime should remain recorded as the refuted scope rather than be silently narrowed around passing examples.
