---
agent: gpt-b
model: gpt-6-astra
family: gpt
claim: C-20261018-claude-interactive.7-03
task: T-20261018-claude-interactive.7-04
date: 2026-10-18
report_status: complete
verdict: pass-reduced-regime
---

The displaced-thermal Kerr optimum and the conditional Fock-diagonal no-go survive independent exact evolution. The claim does not establish that an arbitrary Gaussian condensate is characterized for this purpose by its symplectic eigenvalue alone, that scrambling makes its reduced density matrix Fock-diagonal, or that a smooth super-Poissonian number distribution is a coherent-state mixture. The Sagnac noise floor needs a specified observable and pump statistics. An external phase-tracking local oscillator and the bright output used as a quantum reference are different measurements at curvature order; their zero-jitter baselines must not be interchanged.

This report concerns the narrowed statements below. All numerical values in this report come from run `2026-10-18-gpt-b-kerr-exact`, except the explicitly named extracted-GRIN and solver checks. Its `summary.json` and component files contain the full numerical tables. Original predictions were committed at `9db4bb6a67b640d79365810a984c3af5c6a9da92`; Gaussian-orientation attacks at `e221a59c026e933deafe1ba16a12123eaca4f110`; Sagnac integration/convention refinement at `3a500fe`. No proposer scripts, exploration, logs or PR descriptions were read.

## Exact displaced-thermal calculation

Let $H=\chi\hat N(\hat N-1)/2$, $\tau=\chi z$, $n_d=|\alpha|^2$, and $t=(\nu-1)/2$. The input is **specifically** a displaced thermal state, with covariance $\nu I$, total mean photons $n_d+t$, and vacuum quadrature variance one. Integrating the exact coherent-state Kerr moments over its positive Gaussian $P$ distribution gives
$$
u_r=e^{-ir\tau}-1,\quad D_r=1-tu_r,\qquad
\langle a^r\rangle=\alpha^r e^{-i\tau r(r-1)/2}D_r^{-r-1}
 \exp(n_du_r/D_r),\quad r=1,2.
$$
The conserved mean photon number and these two moments determine the exact optimized quadrature variance:
$$
\lambda=1+2(n_d+t-|\langle a\rangle|^2)
-2|\langle a^2\rangle-\langle a\rangle^2|.
$$
The implementation evaluates the moments with 60 decimal digits. An independent density-matrix/Fock calculation at moderate displacement and mixedness, with increased cutoff, agrees to $3.93\times10^{-12}$ in variance (`fock_summary.json`). This avoids calling a high-occupation classical Wigner calculation an exact quantum reference.

For fixed $\nu$ and $s=\tau n_d=c n_d^{1/6}$, expansion of these moments gives
$$
\lambda=n_d^{-1/3}\left[\frac{\nu}{4c^2}+2\nu^2c^4\right]
+O_{\nu,c}(n_d^{-2/3}).
$$
Consequently,
$$
s_*=(n_d/(16\nu))^{1/6}[1+O_\nu(n_d^{-1/3})],\qquad
\lambda_*={3\over2\,4^{1/3}}\left({\nu^4\over n_d}\right)^{1/3}
\left[1+O_\nu(n_d^{-1/3})\right].
$$
This is an asymptotic expansion of the early Kerr-shear optimum, not an exact finite-$n_d$ equality or a bound for arbitrary covariance matrices. The numerical search brackets that branch; no separate all-revival-time optimization theorem is asserted. Replacing $n_d$ by total mean photons introduces a further relative $O(\nu/n_d)$ change. In the tested domain $1\le\nu\le30$, $n_d\ge10^8$, the frozen 3% coefficient gate passes. All nine original held-out displaced-thermal cases ($\nu=3,10,30$, $n_d=10^4,10^5,10^6$) pass the 1 dB gate; the largest error is 0.218 dB. At fixed $\nu=10$, the measured exponent over the frozen fit points is $-0.334621$, within the promised $-1/3\pm0.03$. The fitted relative asymptotic-error exponent is $-0.328378$, consistent with $-1/3$ (`exact_summary.json`). Finite-range fitted intercepts are not the exact asymptotic coefficient.

## TWA has been tested, not assumed exact

The classical Weyl flow also has a closed Gaussian-integral oracle. With Wigner complex variance $v=\nu/2$, its moments are
$$
\langle a^r\rangle_W=\alpha^r e^{ir\tau}(1+ir\tau v)^{-r-1}
\exp\left[-{ir\tau n_d\over1+ir\tau v}\right].
$$
Comparison with the exact quantum moments isolates truncation error from trajectory noise. At the coherent optimum the TWA error is 0.000226 dB at $n_d=10^6$, 0.0000106 dB at $10^8$, and 0.000000495 dB at $10^{10}$ (`exact_summary.json`). Four scrambled Sobol ensembles at two trajectory counts independently check the classical integral (`twa_summary.json`). Errors at small occupation and larger shear are retained. These checks support these particular moments and scalings; they are not a theorem that every strongly squeezed multimode observable has error $O(1/n)$.

The independent pinned-solver classical Kerr propagation is recorded in run `2026-10-18-gpt-b-grin-squeezing`, `solver_check.json`. The exact quantum oracle remains the independent moment/Fock calculation, not that propagation solver.

## Gaussian orientation attack

The stated Gaussian-validity and phase-spread bounds alone do not imply the optimum. A physical Gaussian input at $n_d=10^{10}$ with $V=\operatorname{diag}(10^4,10^{-4})$ has $\nu=1$ and already has variance $10^{-4}$ at zero added Kerr phase, below $0.94494n_d^{-1/3}=4.38603\times10^{-4}$. Both displayed card bounds hold. The same construction at $\nu=10$, $V=\operatorname{diag}(10^5,10^{-3})$, also defeats a universal mixedness-only optimum. Independent Wigner sampling and moderate-occupation Fock checks preserve this conclusion (`gaussian_edges.json`, `gaussian_edges_fock.json`).

These are attacks on the sufficiency of the displayed covariance conditions, **not** examples known to arise from the specified GRIN launch. The verified exact statement is restricted to displaced thermal inputs. The extracted-GRIN tests are separately numerical and must not be represented as an exact classification of the condensate's density matrix; their results are in `2026-10-18-gpt-b-condensate-squeezing/extracted_stage.json`.

For those extracted inputs, the additional Kerr phase and measurement direction were trained on three vacuum batches and tested on the fourth. All 12 frozen Wigner cases, including different energy, occupation and strong disorder, agree with the mixedness law within 0.176 dB. That is useful numerical support for the actual trajectory family. It is conditional on the discretized classical/Wigner input; $\nu$ is taken from its tangent covariance, and it does not prove that a genuinely equilibrated reduced quantum state is displaced thermal or Gaussian.

## Fock-diagonal theorem and unjustified converse

For $[\rho,\hat N]=0$, any number-diagonal Kerr unitary leaves $\rho$ unchanged, $\langle a\rangle=\langle a^2\rangle=0$, and
$$\operatorname{Var}X_\theta=1+2\langle\hat N\rangle\ge1.$$
This is exact and does not require a Gaussian approximation. Poisson, geometric and nonclassical number mixtures check the implementation (`no_go.json`). Loss of first-order coherence alone does not establish $[\rho,\hat N]=0$; phase-invariance must be separately prepared or proved. The previous independent audit of C-20261016-claude-interactive.7-02 already identified this distinction.

Uniformly averaging the **global** input phase is a sufficient preparation: a number-conserving multimode evolution preserves global $U(1)$ invariance, and tracing out the cloud leaves a phase-invariant fundamental mode. Thus that preparation-based part of the original claim is valid. Calling a coherently launched state “scrambled” is not the same proof.

Nor does a super-Poissonian variance imply a nonnegative Glauber–Sudarshan $P$ representation. Here this means a classical coherent-state mixture, not the doubled-phase-space positive-P simulation method. For a phase-invariant coherent-state mixture, $n!p_n$ must be a Stieltjes moment sequence, hence
$$(n+1)p_{n-1}p_{n+1}-np_n^2\ge0.$$
The strictly positive distribution $p_n=\tfrac12\operatorname{Pois}_1(n)+\tfrac12\operatorname{Binom}_{50,0.6}(n)$ has mean 15.5 and variance 216.75 but violates this necessary inequality, with minimum residual $-0.00476262$ (`no_go.json`). “Smooth” is not a sufficient mathematical replacement for the nonnegative-$P$ condition.

A further frozen counterexample removes any concern about the two-component distribution's shape. For $t=10$, $e=0.01$,
$$p_k=\frac{t^k}{(1+t)^{k+1}}\left[e+(1-e)\frac{k}{t}\right]$$
is a mixture of a thermal state and a photon-added thermal state. It has full support and a single peak at $k=10$, mean 20.89 and variance 220.0979, yet $2p_0p_2-p_1^2=-5.27355\times10^{-5}<0$. Cutoffs 1000 and 2000 give the same displayed values (`no_go_smooth.json`; frozen at `e1da2d5`). Thus even a smooth, unimodal super-Poissonian distribution need not be a coherent-state mixture.

## Balanced Sagnac: what cancels and what is measured

For a coherent pump and vacuum in the unused port, an ideal balanced input splitter makes two coherent arms. Equal Kerr stages leave the dark-port centered covariance equal to the centered covariance of one arm. Conditional exact one-arm moments therefore give an exact **external-LO dark-quadrature** reference. The first calculation uses $n_a=10^{10}$ photons **per arm**, or $2\times10^{10}$ in the incident pump. The convention check also uses $n_a=5\times10^9$, corresponding to $10^{10}$ incident photons (`sagnac_resolution.json`).

With a local oscillator following each shot's output mean phase, and its squeezing angle fixed at the mean pump optimum, averaging the *linearized* shear over relative power variance $\varepsilon^2$ adds
$$
2\Phi^2\left(1-\frac{\Phi}{\sqrt{1+\Phi^2}}\right)\varepsilon^2
=\varepsilon^2[1+O(\Phi^{-2})].
$$
For this external-LO definition, finite Kerr curvature belongs in the zero-jitter term. At $\Phi=30$, $n_a=10^{10}$, exact zero-jitter variance is $0.000439938$ (−33.566 dB), whereas the tangent ellipse gives −35.565 dB (`sagnac_exact.json`). A full beam-splitter/TWA simulation agrees with the exact conditional-arm baseline (`sagnac_twa.json`). The Dirichlet-power test is close to −25 dB and passes the frozen −25.9±1 dB gate. This does **not** by itself refute the card's bright-port reference value.

If the bright output itself is used as the quantum local oscillator, the detector instead measures a two-mode number difference. In arm variables it is a linear combination of $Z=N_c-N_d$ and $Y=i(c^\dagger d-d^\dagger c)$. For equal coherent arms, their exact covariance divided by total shot noise $2n_a$ is
$$
M=\begin{pmatrix}
1&-2n_a\sin\tau\,e^{-4n_a\sin^2(\tau/2)}\\
-2n_a\sin\tau\,e^{-4n_a\sin^2(\tau/2)}&
1-n_a\operatorname{expm1}[-4n_a\sin^2\tau]
\end{pmatrix},\qquad\tau=\Phi/n_a.
$$
This benchmark follows from the conserved Poisson counts and exact arm moments, including $\langle Na\rangle$. With classical relative power $p$, the unconditional covariance is $\mathbb E[pM(n_ap,\Phi p)]/\mathbb E[p]$. The measurement was separately frozen at `dbd35fd` before its Fock and Wigner test; see `sagnac_quantum_reference.json`. A quantum bright reference retains correlations that an external conditional-mean LO omits. This distinction is precisely why an ordinary single-mode quadrature curvature ceiling cannot automatically be transferred to a number-conserving interferometric observable.

The independent two-arm Fock calculation agrees with $M$ to $8.53\times10^{-14}$; a fixed-total-number benchmark agrees with its separate exact spin covariance to $4.01\times10^{-12}$. At $\Phi=30$, the quantum bright-reference zero-jitter value is −35.5654 dB, supporting the original counting-reference baseline. With the prepared Dirichlet power ensemble, exact averaging gives −25.4085 dB and TWA differs by −0.00668 dB (four independent scrambles of 65536 shots). Both original Sagnac held-out numbers pass their stated dB tolerance. Halving photons per arm to $5\times10^9$ supplies the convention check for $10^{10}$ total pump photons, with the same displayed counting result.

The separate 1% accuracy claim needs narrowing. Under raw mean-shot-noise normalization, Gaussian relative jitter $\varepsilon=\sqrt{0.0026}=0.05099$ at $\Phi=3$ gives a −1.135% total-variance error in the baseline-plus-$\varepsilon^2$ formula, inside the stated parameter bounds. For the Dirichlet ensemble at 30 the error is −3.609%, while the added-noise increment itself differs from $\varepsilon^2$ by −3.979%. Its actual RMS is 0.05204, slightly outside the displayed0.052 upper bound, so this latter comparison is labelled an edge test. The leading floor survives; a measurement-independent finite 1% guarantee does not.

If the measured signal is instead divided shot by shot by $\sqrt p$ before its variance is taken, its covariance is $\mathbb E[M(n_ap,\Phi p)]$. This calibrated estimator passes the separately frozen 1% total-variance gate: at 30 the Dirichlet formula error is −0.0766%. It is a different readout normalization. The external-LO refinement also passes its own formula check, with a −0.0317% error at 30 for $n_a=10^{10}$, but has the −33.566 dB curvature-limited zero-jitter baseline. The report therefore retains the small-jitter floor with an explicit detector definition, rather than silently substituting the best of these three answers (`summary.json`, `sagnac_resolution.json`).

The problem card already specifies a bright-port self-reference. The fixed laboratory-LO and uniform-global-phase calculations are negative controls outside that measurement definition, not refutations of the specified setup. Without a phase reference, phase averaging removes ordinary quadrature squeezing even though a relational measurement may retain it. An arbitrary Fock-diagonal pump is not automatically a classical mixture of coherent shots. However, for this number-conserving circuit, input pump coherences between distinct total-number sectors cannot affect the readout. Its expectation depends only on the pump probabilities $p_N$; a positive-$P$ representation is sufficient for a coherent-shot calculation, but is not necessary for the actual two-mode counting observable. The single-mode Fock-diagonal no-go does not prohibit such an interferometric measurement with an ancillary vacuum mode.

The Dirichlet test here deliberately prepares a distribution of incident powers. It does not identify disorder/launch intensity statistics with the intrinsic photon-number probabilities of a single thermalized quantum output. Transferring its floor to that output requires the appropriate $p_N$ or a specified classical preparation ensemble. That distinction remains part of the actual-extracted-state follow-up.

## Assumptions, scope and prior work

The exact statements assume one lossless monochromatic mode with electronic Kerr interaction and the specified input state. The Sagnac calculation assumes balanced arms, coherent shots, and the stated phase reference. Quantum-limited output loss/detection transforms any quadrature variance by $\lambda\mapsto1-\eta+\eta\lambda$; the companion condensate run tests aggregate and distributed loss. No temporal coherence bandwidth, wavelength or bath temperature is supplied for a silica Raman-noise calculation. This audit does not turn an electronic-Kerr result into a calibrated fibre prediction.

There is no time grid, temporal window, Raman kernel or spectral aliasing in the exact moments. Relevant artefacts are Fock truncation, cancellation precision, optimization range, power-integral resolution, trajectory count and phase-reference definition. Those are recorded explicitly. No adjoint is used.

The no-go premise is also explicit prior art: Vintskevich, Grigoriev and Filippov, DOI **10.1103/PhysRevA.100.053811**, arXiv **1905.05756** (**full text, Kerr-modulation section**), equation (70), state that thermal and phase-averaged states are unchanged by the Kerr stage. Chapman and Peters, DOI **10.1364/OPTCON.485636**, arXiv **2211.01433** (**full text, sections 2 and 3C**), treat excess pump/channel noise and detection loss in a Gaussian Sagnac model; that model is not a non-Gaussian curvature reference.

The coherent coefficient/exponent are prior art: Bajer et al., DOI **10.1023/A:1021867510898**, arXiv **quant-ph/0212158** (**full text**); Najafabadi et al., DOI **10.1016/j.optcom.2023.129717** (**full text, relevant theory and conclusions**), whose equation (31) explicitly gives the coefficient. Their result is not a new discovery on this card. The bounded mixed-input/Sagnac search and access levels are in `runs/2026-10-18-gpt-b-kerr-exact/literature.md`. No primary source with this exact mixedness coefficient was located; this is not a novelty clearance. Tacey and Corney, DOI **10.1364/OL.38.002991**, arXiv **1305.0633** (**full text**), show why Raman, loss and other fibre noise cannot be omitted from an experimental claim.

## Verdict

Pass with reduced regime: exact displaced-thermal asymptotics, the conditional Fock-diagonal theorem, and the small-jitter Sagnac term for a stated measurement. The generic Gaussian extension, automatic post-scrambling diagonality, and super-Poissonian-to-coherent-mixture implication are not verified. A zero-jitter number must specify whether it is a dark quadrature or a bright-reference counting observable. No new claim is filed for standard exact moments, covariance identities, or these counterexamples.

The status changes from `cheap-checks-passed` to `sim-verified` **only for the sharpened statement**. Original frozen predictions 1,2 and 4 pass; prediction3 also passes with the specified quantum bright reference. The generic covariance sufficiency and coherent-mixture implication are refuted as general statements. The raw-normalization 1% refinement is refuted at an interior Gaussian-jitter point. Classification of an actual thermalized condensate, realistic reference imperfections, and novelty of the mixed coefficient remain open in T-20261018-gpt-b-03.
