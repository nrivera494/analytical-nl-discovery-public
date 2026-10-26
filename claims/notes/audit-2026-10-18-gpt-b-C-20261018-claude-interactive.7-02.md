---
agent: gpt-b
model: gpt-6-astra
family: gpt
claim: C-20261018-claude-interactive.7-02
task: T-20261018-claude-interactive.7-03
date: 2026-10-18
report_status: complete
verdict: pass-reduced-regime
---

The covariance approximation survives, and an independent weak-disorder ensemble shows condensate squeezing of the claimed order. Its algebra does not establish Gaussianity or uniquely attribute the conditional phase noise to the cloud. The numerical band and realization spread require a specified launch, disorder ensemble and length. The strong-disorder spread and late-distance paths do not pass the frozen resolution gates; they are not promoted as continuum predictions.

Unless another run is named, numerical values below refer to `2026-10-18-gpt-b-condensate-squeezing`, with nonlinear propagation shared explicitly from `2026-10-18-gpt-b-grin-squeezing`. The initial predictions were committed at `9db4bb6a67b640d79365810a984c3af5c6a9da92`; refined disorder paths at `e221a59c026e933deafe1ba16a12123eaca4f110`; the antithetic scaling test at `f380d72`; the fresh nonlinear ensemble at `de19ac5`. No proposer scripts, exploration note, logs or PR descriptions were read.

## What is exact

Write the fundamental-mode covariance in its mean-field frame as
$$V=\begin{pmatrix}V_X&C\\C&V_P\end{pmatrix},\qquad
D=\det V=V_XV_P-C^2,\quad \lambda_-\le\lambda_+.$$
For any physical covariance, Gaussian or otherwise,
$$
\lambda_-={D\over\lambda_+},\qquad
{D/V_P\over\lambda_-}-1
={V_X-\lambda_-\over V_P},\qquad
0\le{D/V_P\over\lambda_-}-1\le {V_X\over V_P}.
$$
Thus the proposed formula is an elongated-ellipse approximation with a directly computable relative error. It is not a dynamical law for $V$, and $\nu=\sqrt D$ is a Gaussian-state purity parameter only when the reduced state is actually Gaussian. The independent tangent ensembles satisfy the card's 0.3 dB algebraic gate; the exact identity and its floating-point residual are tabulated in `summary.json`.

$V_{P|X}=V_P-C^2/V_X$ is the Schur complement, or the variance remaining after the best linear regression on $X$. It is not the phase variance after a projective measurement of the noncommuting amplitude quadrature. Across the tested covariances the approximation error is at most 0.0618 dB, and the identity residual is below $2.2\times10^{-13}$.

## Independent physical and numerical model

The scalar resonant Hamiltonian uses exact two-dimensional Hermite–Gauss overlaps, normalized by $S_{0000}=1$, with groups $q=n_x+n_y<K=5$ and 15 modes. $N=\sum|a_p|^2=1$ and $E'=\sum q_p|a_p|^2$. The launch places equal **energy** in groups 1 and 2, with uniform power within each group and ground fraction $1-3E'/4$. Random phases use the frozen independent seeds. The cited proposer config describes equal **power** in groups 1 and 2; these are different launch populations at fixed $N,E'$. The present ensemble is an independent robustness test, not a literal replay of that input or its random-number stream.

Full spatial-group Hermitian Brownian increments have covariance $\mathbb E[dB_{ij}dB_{kl}]=\delta_{il}\delta_{jk}dz/d$ in a group of dimension $d$, multiplied by $\sigma$. Our convention is $L_d/L_{\rm NL}=\sigma^{-2}$. Each quenched disorder path is shared by its quantum/Wigner trajectories. Reported realization SDs describe separately calibrated fibres or launches; pooling their fields before taking a covariance would add classical noise and is a different experiment. Homodyne phase is referenced to the fundamental's mean for that realization.

RK4 nonlinear evolution is split with unitary intragroup noise rotations. Analytic tangent propagation and full nonlinear Wigner trajectories share the same noise. A nested Brownian bridge preserves coarse increments for step refinement. We reuse only gpt-b's independent previous model; no proposer implementation was consulted. A second pinned solver is checked in the companion GRIN run. The moment/Fock checks are independent quantum implementations.

## Ensemble values and resolution

The finest tangent grid ($h=0.0025L_{\rm NL}$) gives, over 12 weak-disorder paths at $E'=0.3$, $\sigma=0.3$:

| $z/L_{\rm NL}$ | Mean squeezing, dB | Realization SD, dB | Mean $f_0$ |
|---|---:|---:|---:|
| 10 | −9.487 | 1.651 | 0.8295 |
| 20 | −9.547 | 2.906 | 0.8415 |
| 50 | −8.850 | 4.298 | 0.8636 |

These are means of dB values, not dB of an ensemble-averaged covariance. Confidence intervals and the separately randomized launch ensemble are in `summary.json`. Between the two finest steps, the maximum per-path difference is 0.042 dB at 10 and 0.140 dB at 20. At 50 it is 1.288 dB, failing the frozen 1 dB individual-path gate, although the paired mean changes by 0.147 dB. The signed-off dynamical band therefore stops at $20L_{\rm NL}$; later statistics are reported as estimates with an unresolved path error.

There is a separate domain restriction: all 12 paths at $z=10$ satisfy the original $f_0\le0.87$ bound, but four at $z=20$ exceed it (largest $f_0=0.8782$). The eight in-range paths at 20 have mean −7.952 dB and SD 1.978 dB. This postselected subset is reported for domain bookkeeping, not as an unbiased replacement population. The full-ensemble −9.547 dB at 20 is therefore a near-edge stress result, not a numerical assertion wholly inside the original rectangular regime. The covariance approximation survives on both sides; no universal −8 to −10 dB band is signed off.

The original held-out $E'=0.45$ weak-disorder ensemble passes its mean/spread gates. The strong-disorder result is less robust. At $\sigma=2$, the first six $h=0.0025$ paths have SD 1.616 dB at $z=50$, compared with the predicted maximum 1.5 dB; the coarse value was 2.625 dB. This is a failed literal sample prediction, not a statistically established lower bound on the population SD. Step dependence also prevents accepting it as a continuum refutation of that population statement. At $\sigma=3$, the initial $h=0.0025$ refinement gives a 12-path mean at $z=20$ of −6.867 dB with SD 1.258 dB, but the largest paired change from $h=0.005$ is 2.634 dB. At $z=50$, the mean shift is −0.565 dB and the largest path change 6.192 dB. The claim's universal three-to-sixfold spread reduction is not verified (`refinement_summary.json`).

Strong disorder also leaves the measured ground fraction close to its launch value at these lengths (about 0.775 for this launch), rather than the nominal 0.85. Calling all of these states “the equilibrated condensate” would hide a change of regime. All statistics retain the actual $f_0$.

## Curvature, Gaussianity and TWA

The physical covariance can depart from its tangent prediction while the mean remains coherent. For the frozen weak-disorder reference, nonlinear Wigner propagation at $n=10^{10}$ agrees closely with the own-mode tangent variance through the tested early range. At $n=10^8$, the deviations are −0.024 dB at $z=10$, +0.149 dB at 20, and +1.455 dB at 50. At $n=10^6$, they are +6.810 dB at 20 and +16.606 dB at 50. Thus the original lower-$n$ held-out predictions pass (companion GRIN run).

The fixed tangent squeezed direction is chosen before drawing Wigner noise. Antithetic vacuum pairs remove the odd finite-sample term; a paired tangent control removes sampling error in the linear covariance. Fitting only the frozen training occupations gives
$$\Delta V_{\rm own}(z,n)=A(z)/n+o(n^{-1})$$
for this trajectory, numerically. At $z=10$, $A=14826\pm612$ and the measured exponent is $-0.999928\pm0.000004$; the uncertainty is between-scramble SE, not a bound on physical/model error. The held-out occupations agree with the fitted law within 0.059%. At $z=5,20$, the measured exponents are −0.999986 and −0.999713, with all held-out coefficient errors below 0.226%. The measured leading coefficient is about 0.91–0.98 of the sagitta estimate $V_P^2/(8f_0)$ across these three distances (`scaling_summary.json`). This is a tested **TWA curvature** scaling, not the quantum error of TWA itself.

The useful dimensionless check is $r=V_P^2/(8n f_0\lambda_-)\ll1$. The narrower numerical sign-off uses $r\le0.1$, high occupation and the weak-disorder early range. Small $r$ constrains this variance error; it does not prove that the entire density matrix is Gaussian. Exact one-mode moments/Fock checks and the three-mode exchange benchmark in the companion runs calibrate TWA observable by observable. They do not prove a uniform error bound at arbitrary distance for all 15 modes.

## SPM and the cloud

An independent integration of the classical self phase gives the reference ratio $(1+4\Phi_{\rm self}^2)/V_P$. Over the weak-disorder ensemble its mean is 0.822 at $z=10$, 0.863 at 20, and 0.889 at 50; individual values span a wider range than 84–91%. At strong disorder the reference is around 0.80 for this launch (`spm_reference.json`). The finer integration sample confirms the scalar phase integral, and its field path agrees with the tangent base path.

The SPM-only reference also needs its own curvature limit. Evaluating the exact coherent one-mode oracle at each path's measured $n_0$ and integrated self phase gives a weak-ensemble mean of −30.64 dB at $z=50$, while its tangent reference says −38.49 dB (`SPM_exact_reference_diagnostic` in `summary.json`, using the companion exact-Kerr oracle). This is a diagnostic reference, not an independently propagated SPM-only fibre. It nevertheless prevents treating the entire quoted SPM reference range as physical Gaussian squeezing at $n=10^{10}$.

That ratio is not an additive causal percentage: phase responses can be correlated, and switching off terms changes the trajectory. A controlled, number-diagonal SPM/XPM model, with exchange removed, admits exact coherent-state moments and an independent classical Wigner integral (`diagonal_mechanism.json`). Its conditional phase variance includes the intrinsic vacuum term even with no cloud, as well as cloud XPM. In the full exchange model $V_{P|X}$ can include unobserved correlations and mode transport. The audit therefore drops the identification of the entire conditional residual with a unique cloud-noise contribution while retaining the covariance approximation.

## Frozen nonlinear ensemble confirmation

The extension frozen at `de19ac5` uses six disorder paths for each of three ensembles, with $n=10^{10}$ and four independent vacuum scrambles per path. The weak core ($E'=0.3,\sigma=0.3$), strong stress case ($E'=0.3,\sigma=3$), and fresh held-out launch ($E'=0.45,\sigma=0.3$, launch 4213/disorder 7701–7706) all pass the frozen mean-error and individual-path gates through $20L_{\rm NL}$. The largest nonlinear-versus-tangent difference is 0.1754 dB. Doubling vacuum trajectories on the selected weak and strong paths changes the own-mode variance by at most 0.114 dB (`nonlinear_ensemble.json`, `summary.json`).

At $z=20$, the nonlinear means and realization SDs are −11.036±2.375 dB, −6.970±0.880 dB, and −6.535±1.675 dB, respectively. These six-path samples are different from the twelve-path tangent ensemble above. Three weak-core paths at 20 have $f_0>0.87$; the fresh held-out paths stay inside the original bounds. The plot deliberately retains the full frozen samples and identifies these edge cases in its caption. The spread of these means also shows why a universal −8 to −10 dB band is not retained.

Same-grid tangent/TWA agreement does not establish a continuum strong-disorder value: the selected strong path changes by −0.970 dB from $h=0.005$ to 0.0025 at 20 even though the two methods agree closely on each grid. The additional frozen finer-grid results are recorded separately below and in `summary.json`.

The final tangent refinement reaches $h=0.000625L_{\rm NL}$, with 32000 steps through 20. Comparing the last two grids gives:

| Disorder $\sigma$ | $z/L_{\rm NL}$ | Finest mean ± realization SD, dB | Paired mean change, dB | Largest path change, dB |
|---:|---:|---:|---:|---:|
| 2 | 10 | −7.340±1.016 | −0.076 | 0.572 |
| 2 | 20 | −7.320±0.978 | 0.123 | 1.325 |
| 3 | 10 | −7.077±0.658 | −0.062 | 0.449 |
| 3 | 20 | −6.794±0.861 | 0.378 | 1.147 |

All rows use twelve independently specified disorder paths. Both strengths pass the frozen 0.3 dB mean/1 dB individual gates at 10. At 20 the $\sigma=2$ individual gate fails, and both gates fail for $\sigma=3$. Thus the extra refinement does not justify signing off the strong-disorder statistics through 20 or 50 (`final_resolution.json`).

The last frozen nonlinear case was completed under a hard production deadline. At $h=0.000625$, its own-mode TWA-versus-tangent errors are 0.0110 dB at $z=10$, 0.0178 dB at $z=20$. This confirms the high-occupation approximation on that finite grid; it does not repair the failed stochastic step gates. The conservative scheduler checkpoint is retained in `budget_checkpoint.json`, and the successful bounded retry is recorded in the external resource log.

## Relaxed assumptions and remaining limits

At a specified output transmission $\eta_{\rm out}=0.9$ and detection efficiency $\eta_{\rm det}=0.9$, quantum-limited attenuation gives exactly
$$\lambda_{\rm det}=0.19+0.81\lambda_{\rm in}.$$
The companion nonlinear runs also include distributed quantum-limited loss $\alpha=-\ln(0.9)/(50L_{\rm NL})$, with independent vacuum Langevin noise and then 90% detection. Their measured noise and step checks are in `summary.json`. This is an order-of-magnitude loss/detection stress test, not a calibration of an identified fibre.

At $\sigma=3$, the four-path detected means are −5.354±0.539, −5.572±0.279, and −5.474±0.419 dB at $z=10,20,50$ (± realization SD). Halving the step on the first path changes these by +0.090, −0.278 and −0.431 dB. These are loss-stress estimates; the late value is not fully converged. They show why the ideal intrinsic squeezing and the detected squeezing must be reported separately.

The strong spatial-GUE noise test is also a dimensionless stress test. Garnier et al., DOI **10.1103/PhysRevA.100.053835**, arXiv **2011.03918** (**full text, disorder model and discussion**) use polarization matrix disorder; a numerical equality of the symbol $\sigma$ does not establish equality to our full spatial-group process. A physical disorder tensor and coherence-cell specification are still needed.

All three cards exclude Raman, dispersion and neighbouring temporal cells. Hence a Raman kernel at 3 fs, temporal-window doubling and spectral aliasing checks are inapplicable to this monochromatic electronic-Kerr model. A silica Raman calculation would require a temporal mode/bandwidth, wavelength and bath temperature. The audit does not invent these inputs. Fock cutoff, occupation, mode truncation, stochastic step, trajectory count, ordering corrections and conserved quantities are the applicable checks. No adjoint is used.

For context, Sloan et al., **arXiv:2509.03482** (**full text, main article**) already discuss multimode sensitivity-based quantum noise and SPM/XPM mechanisms. Tacey and Corney, DOI **10.1364/OL.38.002991**, arXiv **1305.0633** (**full text**) include loss and Raman in a different fibre Sagnac geometry. See the companion exact-Kerr run's `literature.md` for the bounded search and access ledger.

## Verdict

Pass with reduced regime for the covariance identity/approximation and the independently tested early, weak-disorder squeezing band. The original broad wording about Gaussianity, unique cloud-noise attribution, and a universal strong-disorder spread reduction is not signed off. A full quantum 15-mode result, converged late strong-disorder statistics, and a calibrated silica-fibre prediction remain open.

The status changes from `cheap-checks-passed` to `sim-verified` **only for the sharpened covariance and early weak-disorder statement**. Original predictions 1,3 and 4 pass; prediction2 passes at 20 on the finest six-path sample but fails its literal spread gate at 50, where continuum convergence remains unresolved. The Schur-complement identification as uniquely cloud noise is not established, and no universal mean/spread or realistic-fibre calibration is signed off. T-20261018-gpt-b-02 retains these loose ends.
