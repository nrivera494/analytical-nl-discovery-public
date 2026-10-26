---
agent: gpt-b
model: gpt-6-astra
family: gpt
claim: C-20261018-claude-interactive.7-01
task: T-20261018-claude-interactive.7-02
date: 2026-10-18
report_status: complete
verdict: pass-reduced-regime
---

The quadrature curvature scale and its $1/n$ correction have a defensible, independently tested core. The tangent map is a leading fluctuation approximation, not the exact quantum state until coherence collapse. Its photon-counting prediction needs its own nonlinear test: phase invariance of photon counts proves robustness under a pure phase-only Kerr map, not under a multimode map that exchanges intensity. Some preliminary counting discrepancies are highly step-sensitive and are retained as failed numerical attacks rather than accepted continuum counterexamples.

Numerical values below refer to `2026-10-18-gpt-b-grin-squeezing` unless the exact-Kerr or condensate run is named. The initial specification was committed at `9db4bb6a67b640d79365810a984c3af5c6a9da92`; counting confirmations at `7e0e9b97c51782bb0fa74fc2a04f8a3d19fc904a` and `368fd6b`; subsequent resolution criteria at `6601282`. The chronological prediction files preserve which results were already known when an extension was frozen. No proposer scripts, notes, logs or PR descriptions were read.

## Definitions and independent model

Use vacuum quadrature variance one. A real symplectic tangent map $S$ about a classical coherent trajectory gives $V_{\rm lin}=SS^T$. If $P_a$ selects amplitude quadratures at the local classical mean phases, the leading counting formula is
$$\lambda_{\rm count,lin}=\lambda_{\min}(P_aV_{\rm lin}P_a^T),\qquad
\lambda_{\rm quad,lin}=\sigma_{\max}(S)^{-2}.$$
These are exact properties of the linearized model, not identities for the nonlinear quantum state.

The independent Hamiltonian uses the exact normalized Hermite–Gauss Kerr tensor, resonant mask $q_p+q_q=q_r+q_s$, and $K=5$ groups/15 modes. The sign convention is $da_p/dz=-i\sum S_{pqrs}a_q^*a_ra_s$; reversing the Hamiltonian sign reverses optimal phase angles but not the relevant single-mode variance limits. Our launch has equal energy in groups 1 and 2 and phases from seeds 4201–4213. The proposer config says equal power in those groups. This population difference and the independent random paths prevent interpreting a new realization as a bitwise reproduction of the proposer's sole reference launch. They do test whether $N,E'$ and the displayed regime suffice.

Brownian disorder is full Hermitian noise within each spatial group, covariance $dz/d$ per matrix component, with $L_d/L_{\rm NL}=\sigma^{-2}$. The same quenched noise path acts on the base trajectory, tangent vectors, and every Wigner trajectory in a quantum ensemble. It is not an ensemble of independently fluctuating fibres mixed into one quantum covariance. Tests include the original $\sigma=0.3$, stronger $\sigma=3$, no disorder, and $K=4$ as a mode-truncation stress test. This spatial noise is not identified with a measured polarization-disorder tensor.

## Exact single-mode attack and the curvature scale

The independent exact Kerr moments and Fock oracle are in `2026-10-18-gpt-b-kerr-exact`. For a coherent mode with displacement occupation $n_0$, shear $s=\chi n_0z$, and $1\ll s$ in the small phase-spread regime,
$$\lambda_{\rm lin}\simeq\frac1{4s^2},\qquad
\Delta V_{\rm fixed}\simeq\frac{2s^4}{n_0},\qquad
\frac{\Delta V_{\rm fixed}}{\lambda_{\rm lin}}
\simeq\frac{\sigma_{\max}^6}{8n_0}.$$
The correction is measured along the tangent squeezed direction, chosen before evolution. Balancing it against the linear variance gives the known coherent Kerr optimum $0.94494n_0^{-1/3}$. Exact evolution therefore leaves the Gaussian squeezing approximation long before first-order coherence collapses. A coherence-based $z_E$ is not a Gaussian-validity theorem.

The constant 0.8 corresponds asymptotically to a 10% variance correction, not an exact sharp boundary. At $\sigma_{\max}^6/n_0=0.8$, the exact relative excess is 0.11060 at $n_0=10^4$ and 0.10015 at $10^{10}$; the finite-shear correction is visible. The fixed-shear occupation scans and their error powers are retained in the exact-Kerr summary. TWA is separately compared with exact moments and Fock evolution before it is used as a multimode curvature reference.

## Multimode curvature and frozen held-out tests

At fixed $E'=0.6$, $\sigma=0.3$, launch 4201/disorder 7601 and $z=10L_{\rm NL}$, the independent nonlinear ensemble gives
$$
\frac{V_{\rm fixed}}{V_{\rm lin}}-1
\simeq (0.0920\pm0.0039)\frac{\sigma_{\max}^6}{n_0}.
$$
The coefficient uncertainty is between four scrambled vacuum ensembles. Over the frozen $n=3\times10^5,10^6,3\times10^6$ fit points, the measured occupation exponent is $-0.9947\pm0.0103$. The coefficient is a trajectory/direction-specific calibration, not a universal function of the largest singular value. The separate antithetic test in `2026-10-18-gpt-b-condensate-squeezing` verifies the $1/n$ curvature residual on new frozen occupations with much smaller sampling contamination.

The original held-out $E'=0.9,n=10^{10}$ and $E'=0.3,n=10^8$ quadrature predictions pass. For the latter, the fixed-direction excess is 0.299 dB at $z=10$, 6.743 dB at 20, and 28.648 dB at 50. For the former it is 0.081 dB at 20 and 7.127 dB at 50. The early high-occupation predictions around −30 dB are therefore consistent with the independent TWA calculation in this ideal model, with a phase-locked, mode-shaped quadrature detector. The exact single-mode results justify the mechanism; the multimode coefficient and error envelope are numerical.

Matching $E'$ does not ensure the same instantaneous condensate fraction. Our $E'=0.9$ launch has $f_0=0.415$–0.501 at those early checkpoints, below the card's $f_0\ge0.55$ bound. Those held-out energy tests therefore also relax that bound. The $E'=0.3,z=20$ reference is just above 0.87. The signed-off interior envelope separately enforces $0.55\le f_0\le0.87$ in `summary.json`; successful edge tests are not silently included in the original rectangular domain.

The frozen conjecture that the optimized full quadrature stays above −35 dB at $n=10^{10}$ passes the 25 sampled checkpoints: the lowest optimized value is −31.487 dB, or −31.450 dB with cross-fitted directions (`summary.json`). Passing finitely many cases is not a proof for every distance or a universal multimode Kerr ceiling. The largest singular value alone does not determine the projected nonlinear Hessian or the occupation distribution of all modes. No new universal multimode bound is claimed or filed.

## Photon counts and ordering

For fields normalized to total classical power one, the exact Wigner symbols give
$$
\langle N_p\rangle=n\langle|a_p|^2\rangle_W-\tfrac12,\qquad
\operatorname{Cov}(N_p,N_q)=n^2\operatorname{Cov}_W(|a_p|^2,|a_q|^2)-\tfrac14\delta_{pq}.
$$
The symbol identity is exact; replacing the quantum Wigner evolution with classical Weyl flow is TWA. Variances are computed from centered powers before multiplying by $n^2$, avoiding subtraction of $O(n^2)$ means. The scalar weighted-count variance is also evaluated directly.

There are three distinct tests: weights physically frozen at the classical tangent prediction; the tangent eigenvector with whitening updated to measured mean populations; and weights reoptimized on independent training batches then evaluated on held-out batches. The original JSON key `count_fixed` denotes the second. `count_frozen_weights` denotes the first; no old number is relabelled. Cross-fitting exposes the bias from choosing an eigenvector on the same finite sample used to estimate its variance.

For one mode, Kerr conserves its number distribution exactly. For an exchange Hamiltonian, the output intensity is a nonlinear function of input amplitude and phase, so its second and higher derivatives contribute to counting variance. The argument “a phase rotation leaves $|a|^2$ unchanged” does not remove those contributions. Even a small absolute correction can be large relative to a very small optimized variance.

The first $n=10^6,z=100$ disorder-path attack gave a 9.40 dB discrepancy at step 0.02, but only 0.89 dB at 0.01. The condensate coherence in the latter calculation is 0.99096. The large coarse-grid discrepancy is **not** accepted as a converged physical counterexample. Both calculations are preserved; finer same-Wiener-path and deterministic no-disorder tests were frozen before running them. The analogous long-distance $n=10^{10},z=300$ attack is also subjected to step and trajectory-count checks. The final accepted/unresolved classifications are tabulated in `summary.json`; a failed resolution check cannot be repaired by increasing trajectory count alone.

The final $h=0.005\to 0.0025$ comparison at $n=10^6,z=100$ is:

| Launch/disorder | Observable | Finest error, dB ± sampling SE | Change in error, dB | Frozen convergence gate |
|---|---|---:|---:|---|
| 4201/7601 | Frozen physical weights | 0.803±0.078 | −0.307 | Fails narrowly |
| 4201/7601 | Reoptimized covariance | 0.654±0.088 | −0.212 | Passes, but excess above 0.5 dB is not resolved at 3 SE |
| 4203/7603 | Frozen physical weights | 2.421±0.059 | −11.247 | Fails |
| 4203/7603 | Reoptimized covariance | 0.402±0.115 | −2.188 | Fails |

The first row's paired SE for the change is 0.0653 dB, so the literal threshold is 0.3 dB; adding the marginal SEs in quadrature would incorrectly pass it. The fresh path's finest coherence is 0.99373 and its least populated mode still has 1771 photons. Its large coarse-grid discrepancy disappears for reoptimized weights, but the fine value cannot be declared converged. Cross-fitting gives the same unresolved classification. No continuum counting counterexample is accepted from these attacks.

Without disorder, deterministic refinement changes these discrepancies by less than $2\times10^{-6}$dB. Reoptimized errors for launches 4201,4203 and held-out4213 are0.085,0.418 and 0.110 dB; doubling trajectories on4201 changes its fixed-weight error from 0.109 to 0.121 dB. These are successful restricted counting checks, not a proof of curvature immunity under every exchange trajectory. At $n=10^{10},z=300$, the refined optimized and cross-fitted errors are about1.64 and 1.70 dB, but the step change remains too large: original prediction4 is unresolved in the continuum, with its finite-grid failure retained.

## Independent exact exchange benchmark and numerical artefacts

The three-mode Hermite–Gauss ladder $(00,10,20)$ retains real resonant exchange. Independent sparse-Fock evolution checks the full quadrature and counting covariance against Wigner trajectories at moderate total occupation, with a frozen held-out higher occupation. The total-photon cutoff is increased on one case. An initial pilot unintentionally used Float32 special functions on an int16 occupation array; it was rejected and retained in `initial-float32-factorial/`. Accepted exact references explicitly cast factorials and ladder coefficients to Float64. This precision correction is recorded, not hidden by deleting the failed pilot.

For accepted references, increasing the cutoff changes the quadrature/counting minima by at most $5.59\times10^{-11}$; the maximum norm and total-number Fano errors are $1.45\times10^{-11}$ and $2.35\times10^{-10}$. At $z=1$, the full-quadrature TWA error decreases from 0.673 dB at $n=8$ to 0.153 dB at held-out $n=64$. At $n=64$, the own-mode error is 0.0592 dB and the counting error is 0.000670 dB. At $z=10$ the latter becomes −0.113 dB. These observable-dependent errors are incompatible with treating agreement of coherence alone as a TWA accuracy certificate (`exact_exchange` in `summary.json`).

The second solver uses fixed-step Float64 RK4IP from the read-only pinned agents' solver, with the independently generated tensor. The first resonant-tensor comparison failed while the single-mode limit passed; the raw and summary results are retained. A one-step black-box index-convention probe found that the solver conjugates its fourth tensor slot, whereas the independent implementation conjugates its second. Exporting axes $(0,2,3,1)$ resolves the discrepancy: the largest Jacobian error is $3.48\times10^{-8}$, and the counting/quadrature differences are below $1.22\times10^{-7}$ dB (`solver_check.json`). Full, unaveraged Hermite–Gauss tensors are permutation-symmetric, whereas the resonant mask is not, so the old full-tensor check could not expose this convention issue. No solver source was changed or needed for the diagnosis.

The applicable checks are stochastic step, quantum trajectory count, Fock cutoff, mode truncation, symplectic reciprocity, exact total-number shot noise, and conservation of $N,E'$. The long-distance counting refinement is the explicitly recorded exception to the $2^{15}$ integration-step cap; it stores only the frozen snapshots. There is no temporal FFT window, spectral grid, Raman kernel or adjoint in the independent monochromatic model. The pinned-solver two-point constant temporal field is an interface check, not a pulse/Raman simulation. All production numerical children run serially after the required memory check.

Apple Accelerate emitted floating-point warnings on some finite small matrix products. An independent direct-contraction check agrees with the BLAS amplitude projection to $3.6\times10^{-15}$ relative error, with all inputs and outputs finite. Forming the counting Gram matrix directly changes its minimum by at most $2.1\times10^{-6}$dB. This numerical check rules out that cancellation/BLAS route as the explanation of the large step-sensitive counting discrepancies (`artifacts` in `summary.json`).

## Relaxed assumptions and literature

The companion condensate run tests stronger disorder, launch variation, quantum-limited distributed loss, and finite detection efficiency. The pure attenuation identity $\lambda_{\rm det}=1-\eta+\eta\lambda$ applies to quadrature covariance without assuming Gaussianity. The specified 90% transmission and 90% detector example limits arbitrarily deep ideal quadrature squeezing to −7.21 dB. The ideal −30 dB numbers are not a prediction for a fibre with unspecified loss and Raman noise.

Bajer et al., DOI **10.1023/A:1021867510898**, arXiv **quant-ph/0212158** (**full text**) and Najafabadi et al., DOI **10.1016/j.optcom.2023.129717** (**full text, relevant theory/conclusions**) supply coherent-Kerr prior art. Sloan et al., **arXiv:2509.03482** (**full text, main article**) overlaps with the multimode tangent-noise framework. Kitagawa and Yamamoto, DOI **10.1103/PhysRevA.34.3974** (**abstract only**) distinguish Kerr crescent evolution and interferometric number squeezing. None of these accesses proves the present 15-mode counting robustness statement. Search strings and access levels are recorded in the companion exact-Kerr run's `literature.md`.

## Scope of the verdict

The defensible core is an early high-occupation tangent quadrature prediction with a measured $1/n$ curvature correction and frozen held-out checks. Gaussianity until $z_E$ and curvature-free counting under arbitrary multimode exchange do not follow. A continuum numerical counting counterexample is accepted only after its own resolution gate; unresolved attacks are reported as such. Exact 15-mode quantum error control, a universal multimode curvature ceiling, and realistic temporal/polarization/Raman noise remain open.

The status changes from `cheap-checks-passed` to `sim-verified` **only for the sharpened early-quadrature statement**. Original predictions 1–3 pass. Prediction4 has unresolved propagation error. Prediction5 passes the sampled checkpoints and remains unproved between them or for arbitrary mode couplings. The original exact-Gaussian premise is refuted by exact Kerr evolution; the blanket counting claim remains unverified. T-20261018-gpt-b-01 retains these loose ends.
