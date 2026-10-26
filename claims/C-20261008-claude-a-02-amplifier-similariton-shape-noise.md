---
id: C-20261008-claude-a-02
problem: P-001
title: "Amplifier similariton: shape fluctuations are amplified phase-sensitively (G^(1/3) intensity, G^(5/3) phase), so single-shot spectral noise tends to rank one and the matched-LO phase noise becomes energy-locked as G^(-2/3)"
type: noise-formula
status: promoted
proposed_by: claude-a
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: pi-chatgpt
verifier_family: gpt
verifier_model: gpt-6-pro
audited_by: gpt-e
auditor_family: gpt
created: 2026-10-08
updated: 2026-10-19
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: R-0011
---

## Statement

> **Clean-context adversarial audit (gpt-e, gpt-6-astra, family gpt, 2026-10-19): pass-reduced-regime.** [Report](notes/audit-2026-10-19-gpt-e-C-20261008-claude-a-02.md), run `2026-10-19-gpt-e-similariton`.
> - The leading hydrodynamic fixed-order variance **envelopes**, the stated orthonormal five-component spectral ratio, and the reduced phase–energy deficit survive independent covariance integration with ASE. Log-gain oscillations prevent treating finite-window slopes as universal exponents or assuming constant asymptotic prefactors.
> - Modest-gain full-field checks support matched phase/energy readouts. Sharp-edge raw shape moments remain sensitive to Fourier resolution and periodic-window wraparound; smoothing the edge restores convergence in the tested case. The generic P6 full-moment accuracy promise and any uniform sharp-edge remainder are **outside the audited scope**.
> - Reduced probes beyond the stated physical gain bound test mathematical envelopes only. The stationary-phase and brightness conditions remain necessary. Phase-quadrature edge regularization, high-gain full-field spectral eigenvalues and material-specific gain/Raman corrections remain open.

> **As verified (GPT 6 Pro, family gpt, 2026-10-18; filed 2026-10-19 by claude-interactive).** Run `2026-10-18-pi-chatgpt-independent-verification`, [review](../docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md).
> - **Verified, narrowed:**
>   - (a) holds in leading parabolic hydrodynamics as variance **envelopes** of photon-normalized fixed low-order shape variables: $G^{1/3}$ (intensity) and $G^{5/3}$ (phase), rms $G^{1/6}$ and $G^{5/6}$. The prefactors oscillate in $\ln G$, so $G^{-q}{\rm Var}$ need not converge.
>   - (b) The spectral ratio $\mu_2/\mu_1=\Theta(G^{-2/3})$ holds for the stated five-component orthonormal projection only; it is not a full-field or rank-one-quantum-state statement.
>   - (c) $1-r^2=\Theta(G^{-2/3})$ holds in the reduced model.
> - **Superseded:**
>   - $C_{PP}\propto G/\varepsilon_0^2$ is wrong. It is $C_{PP}\sim(32n_{sp}/9)G\Phi_{NL}^2\propto G^{7/3}/\varepsilon_0^2$, consistent with this card's own table P4.
>   - "With ASE there is no squeezing" is wrong as an unconditional statement. A matched mode is squeezed at short gain when $\gamma P_0>5n_{sp}g/4$: the counterexample gives $\lambda_{\rm LO}=0.8965$ with full ASE. Only the restricted statement survives: at large gain the matched mode's minimum variance grows as $\Theta(G^{1/3})$ (reduced model).
>   - These two corrections are claim C-20261019-pi-chatgpt-02.
> - **Not verified:**
>   - the uniform edge remainder $O(\varepsilon_0^2\ln(1/\varepsilon_0))$: for the sharp seed, raw phase projections are log-divergent;
>   - any all-mode quantum covariance limit.
> - **Regime correction:** $N_0\ge10^4$ is not sufficient at high gain. The linearization needs $\Phi_{NL}^2/N_0\ll1$.

**System.** The same amplifier as C-20261008-claude-a-01: normal-dispersion fibre, frequency-flat gain $g$, ASE with factor $n_{sp}$, and a coherent parabolic seed of $N_0$ photons.

**Units.** $x=T/T_0$, $\zeta=z/\sqrt{L_DL_{NL}}$, $\varepsilon_0=\sqrt{L_{NL}/L_D}$, $\Gamma=g\sqrt{L_DL_{NL}}$, and $\xi=T/T_p(z)$ the comoving time. The parabolic background has half-width $a(\zeta)=T_p/T_0$ with $a''=2e^{\Gamma\zeta}/a^2$.

**(a) Blocks with gain (dispersionless leading order).** Write a perturbation as
- $\delta|A|^2=\rho_0(z)\,n(\xi)$, with $\rho_0$ the current peak power;
- $\delta\arg A=p(\xi)$.

Each Legendre component ($n=\sum n_lP_l$, $p=\sum p_lP_l$) then evolves on its own, for any parabolic background, transient or asymptotic:
$$\frac{dp_l}{d\zeta}=\frac{e^{\Gamma\zeta}}{a}\frac{n_l}{\varepsilon_0},\qquad \frac{d}{d\zeta}\frac{n_l}{\varepsilon_0}=-\frac{l(l+1)}{a^2}p_l .$$
- The block map $M_l$ has determinant 1.
- At $g=0$ it is the passive Legendre–Pöschl–Teller propagator of C-20261004-claude-a-01.
- On the asymptote, $n_l\propto e^{\lambda z}$ with $\lambda=\tfrac g3[-1\pm\sqrt{1-l(l+1)/2}]$. For $l\ge2$: decay at $g/3$, oscillation at $\tfrac g3\sqrt{l(l+1)/2-1}$.

**Photon-normalized quadratures.** These are $\sqrt E\,n$ (intensity shape) and $\sqrt E\,p$ (phase shape). For $l\ge2$ their power gains have envelopes $G^{1/3}$ and $G^{5/3}$, against $G$ for both quadratures of a linear amplifier.

The attraction therefore acts as a phase-sensitive amplifier on every shape mode. It de-amplifies intensity-shape noise by $G^{-2/3}$ relative to linear amplification, and amplifies phase-shape noise by $G^{2/3}$.

**(b) Single-shot spectral covariance (dispersive Fourier transform).**

*Definitions.*
- The output is strongly chirped, so $\omega\simeq\kappa T$ with $\kappa=\dot T_p/(\beta_2T_p)$.
- $s=\delta S(\omega)/S_0$, where $S_0$ is the peak of the mean spectrum, with Legendre components $s_l$ in $\xi_\omega=\omega/\omega_{\rm edge}$.
- At leading order $s_l=n_l-l(l+1)\varepsilon_0p_l/(aa')$, where $a'=da/d\zeta$.

*Content of the low-order components.*
- $s_0$ is the energy: the similariton's energy mode is a uniform $\delta S$ over the core, because a stronger pulse is both taller and wider.
- $s_1$ is the centroid frequency.
- $s_{l\ge2}$ are the shape modes.

*Prediction.* On the asymptote every $\mathrm{Var}(s_{l\ge1})/\mathrm{Var}(s_0)$ decays as $G^{-2/3}$. The covariance of $\delta S$ restricted to Legendre modes $l\le4$, in $L^2$ over the spectral core, tends to rank one: its second-to-first eigenvalue ratio falls as $G^{-2/3}$.

**(c) Matched local oscillator (LO = output mean field).**
- $C_{AA}=G+(2n_{sp}-1)(G-1)$ in output shot-noise units (exact).
- The phase quadrature $\propto\bar p=p_0-p_2/5$ has $C_{PP}\propto G/\varepsilon_0^2$ (Kerr conversion of energy noise). *[Superseded 2026-10-19: $\propto G^{7/3}/\varepsilon_0^2$, run `2026-10-18-pi-chatgpt-independent-verification`; see the verified block above.]*
- Let $r$ be the correlation between $\bar p$ and the photon number. On the asymptote, $1-r^2$ (the share of phase-quadrature noise not linear in the energy noise) falls as $G^{-2/3}$.
- This is the gain counterpart of the passive profile-limited squeezing in C-20261004-claude-a-01. With ASE there is no squeezing. *[Superseded 2026-10-19: false as an unconditional statement (short-gain counterexample $\lambda_{\rm LO}=0.8965$, run `2026-10-18-pi-chatgpt-independent-verification`); at large gain the matched mode is not squeezed.]*
- The uniform ($l=0$) part of the Kerr phase noise has a closed form for any background (C11 checks it on the asymptote):
$$\varepsilon_0^2N_0\mathrm{Var}(p_0)=\tfrac49\Big[\theta_L^2+(2n_{sp}-1)\Gamma\!\int_0^{\zeta_L}\!e^{-\Gamma\zeta}(\theta_L-\theta)^2d\zeta\Big],\qquad \theta=\varepsilon_0\Phi_{NL}(\zeta).$$
  For large $G$ this tends to $\Phi_{NL,L}^2\cdot\tfrac49\cdot2n_{sp}/N_0$: the peak nonlinear phase times the relative energy noise, which is mostly injected early.

## Regime

- $\varepsilon_0\le0.1$, with $\varepsilon_{\rm eff}=\varepsilon_0/\sqrt{a\,e^{\Gamma\zeta}}$ decreasing along the amplifier. The relative error is $O(\varepsilon_0^2\ln(1/\varepsilon_0))$ for (b) and (c) *[not verified, 2026-10-19]*; for the block matrices in (a) it falls at least as fast as $\varepsilon_0^{4/3}$ (C-20261004-claude-a-01's bound).
- $l\le4$ and $l\,\varepsilon_{\rm eff}\le0.2$.
- $0.5\le\Gamma\le10$ and $gL\le12$. Exponents are fitted at $gL=12$–18.
- The stationary-phase map needs $aa'/\varepsilon_0\ge20$, i.e. a strongly chirped output.
- $N_0\ge10^4$. *[Insufficient at high gain (GPT 6 Pro, 2026-10-18): the linearized phase needs $\Phi_{NL}^2/N_0\ll1$; at $\varepsilon_0=0.05$, $gL=12$, $N_0=10^4$ gives about 199 rad rms phase.]*
- Gain flatness ($gL(\omega_{\rm edge}/\Omega_g)^2\le0.05$), Raman, third-order dispersion and self-steepening bounds as in C-20261008-claude-a-01. That claim's example systems show that a realistic short-seed amplifier is outside this regime at launch.

## Assumptions

1. Scalar 1D NLSE (inherited); instantaneous Kerr; second-order dispersion only.
2. Frequency-flat, unsaturated gain; white ASE with factor $n_{sp}$, symmetric ordering; ASE–ASE beat neglected.
3. Linearization in the noise.
4. Dispersionless (hydrodynamic) leading order for the blocks. Regular, bounded-flux edges select $P_l$.
5. Only the intensity quadrature of the noise is kept at leading order. The phase quadrature (vacuum and ASE) is edge-singular, $\propto1/(1-\xi^2)$, and enters (b) and (c) at relative order $\varepsilon_{\rm eff}^2\ln(1/\varepsilon_{\rm eff})$. Its cut-off is $\delta\propto\varepsilon_{\rm eff}^{2/3}\propto e^{-4gz/9}$.
6. The time–frequency map uses the mean chirp. Corrections are $O(\varepsilon_{\rm eff})$.
7. The parabolic seed has sharp edges. Non-parabolic seeds are outside this claim.

## Predictions

Frozen 2026-10-08, from run `2026-10-08-claude-a-amp-sim-checks` (`numeric.json`). Each entry is ($I_{\rm in}$, $I_{\rm ase}$); the variance is $I_{\rm in}+(2n_{sp}-1)I_{\rm ase}$.

**Readouts with gain.** These are exact projections; C10 checks them. With $E(\zeta)$ the mean energy and $\rho v=-\varepsilon_0\mathrm{Im}(\psi^*\psi_x)$ in normalized units:
- $n_0=\tfrac23\delta E/E$;
- $n_2=\tfrac{15}4[\tfrac43\int x^2\delta\rho\,dx/(a^2E)-\tfrac23n_0]$;
- $p_2=-\tfrac5{3\varepsilon_0E}[\delta\int x\rho v\,dx-\tfrac{a'}a\int x^2\delta\rho\,dx]$;
- $p_0=\int\mathrm{Im}(\bar\psi^*\delta\psi)dx/E+p_2/5$;
- $n_1=2\int x\delta\rho\,dx/(aE)$;
- $p_1=-\tfrac a{\varepsilon_0E}[\delta\int\rho v\,dx-\tfrac{a'}a\int x\delta\rho\,dx]$;
- $n_3=\tfrac{35}4[\tfrac43\int x^3\delta\rho\,dx/(a^3E)-\tfrac25n_1]$;
- $p_3=-\tfrac{35}{16}[\tfrac4{3\varepsilon_0Ea}(\delta\int x^2\rho v\,dx-\tfrac{a'}a\int x^3\delta\rho\,dx)+\tfrac4{15}p_1]$.

**P1. Block matrices** at the output, acting on $(p_l,n_l/\varepsilon_0)$.

Main case, $\Gamma=\sqrt{18}$, unchirped seed:

| $gL$ | $\theta_L=\varepsilon_0\Phi_{NL}$ | $M_0$ | $M_2$ | $M_3$ |
|---|---|---|---|---|
| 2 | 1.2825 | [[1, 1.2825],[0, 1]] | [[-0.5929, 0.7947],[-1.4327, 0.2337]] | [[-1.4540, 0.4284],[-1.5309, -0.2367]] |
| 4 | 5.8878 | [[1, 5.8878],[0, 1]] | [[-3.6111, 0.0441],[-0.1567, -0.2750]] | [[0.1955, -1.1041],[0.9355, -0.1679]] |
| 6 | 20.4518 | [[1, 20.4518],[0, 1]] | [[-1.3858, -3.1045],[0.2516, -0.1579]] | [[7.7269, -0.4042],[0.1727, 0.1204]] |

**P2. Phase-sensitive exponents (asymptotic seed, $l=2$).** The photon-normalized quadrature power-gain exponents at $gL=12$, 18 and 24 are (1.705, 0.295), (1.690, 0.310) and (1.674, 0.326). They converge to 5/3 and 1/3 (C8).

**P3. Spectral covariance, main case.** $N_0\mathrm{Var}(s_l)$ for $l=0$–4, and the eigenvalue ratio $\lambda_2/\lambda_1$ in the $l\le4$ subspace ($n_{sp}=1$):

| $gL$ | $s_0$ | $s_1$ | $s_2$ | $s_3$ | $s_4$ | $\lambda_2/\lambda_1$ |
|---|---|---|---|---|---|---|
| 2 | (0.4444, 0.3843) | (0, 0.08407) | (2.645, 1.486) | (8.067, 7.783) | (3.658, 14.36) | 0.9868 |
| 4 | (0.4444, 0.4363) | (0, 0.04278) | (0.1312, 0.2949) | (0.481, 0.5688) | (0.8996, 2.013) | 0.3735 |
| 6 | (0.4444, 0.4433) | (0, 0.01835) | (0.004664, 0.04164) | (0.07037, 0.242) | (0.4, 0.4685) | 0.1095 |

On the asymptotic seed, $\lambda_2/\lambda_1$ is $3.03\times10^{-3}$, $4.14\times10^{-4}$ and $6.07\times10^{-5}$ at $gL=12$, 15 and 18. The fitted slope is $d\ln/d(gL)=-0.652$; the prediction is $-2/3$ (C9).

**P4. Matched LO, main case.** $\varepsilon_0^2C_{PP}/G$ (in, ase) and $1-r^2$ ($n_{sp}=1$):

| $gL$ | $\varepsilon_0^2C_{PP}/G$ | $1-r^2$ |
|---|---|---|
| 2 | (3.809, 2.258) | 0.07436 |
| 4 | (61.81, 55.32) | 0.01251 |
| 6 | (700.9, 685.3) | 0.004356 |

On the asymptotic seed, $1-r^2$ is $8.96\times10^{-5}$, $9.59\times10^{-6}$ and $1.84\times10^{-6}$ at $gL=12$, 15 and 18. The fitted slope is $-0.648$; the prediction is $-2/3$, modulated by the shape-mode oscillation.

**P5. Held-out case (not used to build anything above).** $\Gamma=1$, unchirped seed.

| $gL$ | $M_2$ | $s_0$ | $s_2$ | $\lambda_2/\lambda_1$ | $1-r^2$ |
|---|---|---|---|---|---|
| 2 | [[-2.4011, -0.0459],[-0.4942, -0.4259]] | (0.4444, 0.3843) | (0.2596, 0.265) | 0.4257 | 0.06191 |
| 4 | [[-2.5017, -1.9674],[0.1628, -0.2717]] | (0.4444, 0.4363) | (0.001834, 0.07332) | 0.1256 | 0.0211 |
| 6 | [[1.8798, -5.3885],[0.2263, -0.1166]] | (0.4444, 0.4433) | (0.01736, 0.03703) | 0.0757 | 0.007757 |

The other entries are in `numeric.json` under `heldout`.

**P6. Convergence.**
**Not verified; outside the audited claim (gpt-e, 2026-10-19).** The original generic accuracy promise below is retained as superseded scope. Sharp-edge full moments are not uniformly converged in run `2026-10-19-gpt-e-similariton`; no error exponent or blanket ten-percent guarantee is signed off on. The narrowed reduced-model statements above do not depend on P6.
- Entries of P1, P3 and P4 approach the tables as $\varepsilon_0\to0$ at fixed ($\Gamma$, $gL$). The expected relative error is $\le10\%$ at $\varepsilon_0=0.05$.
- A deviation that does not shrink with $\varepsilon_0$ refutes the corresponding part.
- Measured exponents below 1 refute the error statement.

## Derivation

Full derivation: `claims/notes/C-20261008-claude-a-derivation.md`, Secs. 4, 5, 7 and 8. Checks: run `2026-10-08-claude-a-amp-sim-checks`.

1. Linearizing the gain hydrodynamics about any parabolic background separates exactly in Legendre polynomials (G3). The gain term cancels against the background growth.
2. Eliminating $p_l$ gives the orchestrator's second-order equation and asymptotic rates (G4). Its phase-sensitive statement is confirmed numerically (C8).
3. ASE projects onto the intensity components with the non-diagonal metric $B_{lm}=\int(1-\xi^2)P_lP_m$, which is kept. The edge-singular phase part is subleading.
4. Spectral components follow from stationary phase.
5. The matched local oscillator reads $p_0$ and $p_2$.

Prior art for the hydrodynamic modes:
- 1D trapped-condensate modes $\omega^2=\omega_z^2k(k+1)/2$ (Menotti & Stringari 2002, arXiv:cond-mat/0201158). Full text, read by claude-a.2.
- The expanding-condensate separation (Fedichev & Fischer 2004; see P-001).
- The attraction of amplifier similaritons is established (Kruglov et al. 2002; Finot, Millot & Dudley, Opt. Lett. 29, 2533 (2004), DOI 10.1364/OL.29.002533, abstract only).
- An analytic attraction model: Wabnitz, IEEE PTL 19, 507 (2007), DOI 10.1109/LPT.2007.893823. Abstract only; its rates are not checked against $g/3$.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Dimensionless groups only (config.yaml) | claude | 2026-10-08-claude-a-amp-sim-checks | 2026-10-08 |
| Known limits | $g\to0$ equals the passive blocks to $5\times10^{-9}$ (C2). The energy block reproduces the exact energy noise (C7). | claude | 2026-10-08-claude-a-amp-sim-checks | 2026-10-08 |
| Symbolic residual | Separation with gain for $l\le6$ (G3); block ODE and rates (G4) | claude | 2026-10-08-claude-a-amp-sim-checks | 2026-10-08 |
| Zero-length identity and determinant | $M_l(0)=I$; $\lvert\det M_l-1\rvert\le7\times10^{-12}$ (C1) | claude | 2026-10-08-claude-a-amp-sim-checks | 2026-10-08 |
| Commutator / uncertainty | Only $\det M_l=1$ is checked (C1). The uncertainty relation is not checked at this order: the leading-order covariance drops the phase-quadrature noise, so a single block's ($p$, $q$) covariance is not a complete quantum state. The complete centroid pair is checked in C-20261008-claude-a-01 (C6). | claude | 2026-10-08-claude-a-amp-sim-checks | 2026-10-08 |
| Readouts | Moment readouts with gain recover $n_0..n_3$ and $p_0..p_3$ (C10) | claude | 2026-10-08-claude-a-amp-sim-checks | 2026-10-08 |
| Simulation, core regime | | | | |
| Error-scaling exponent | | | | |
| Held-out region | | | | |
| Convergence and artefacts | | | | |
| Second solver or relaxed assumption | | | | |
| Adversarial audit | **Pass-reduced-regime**, [report](notes/audit-2026-10-19-gpt-e-C-20261008-claude-a-02.md). Independent finite-volume ASE covariance, orthonormal spectral projection, chirped/unchirped full-field readouts and unchanged-solver adjoint check. Sharp-edge moments fail resolution robustness; smoothed launch converges. Uniform P6/edge and all-mode claims excluded | gpt-e (gpt; gpt-6-astra) | `2026-10-19-gpt-e-similariton` | 2026-10-19 |
| Novelty search | No published linear spectrum, $g/3$ rate, shape-mode phase-sensitive amplification or DFT covariance for amplifier similaritons was found. Attraction itself is established; see log. | claude (claude-a.2) | | 2026-10-08 |
| Independent verification, core regime | Exponents reproduced with independent finite-volume covariance code (8 orthonormal numerical modes, 32–1024 cells, $\Gamma=\sqrt{18}$, $n_{sp}=1$): fitted over $12\le\tau\le26$, density 0.32461 (1/3), phase 1.69203 (5/3), spectral ratio $-0.66551$ ($-2/3$), phase–energy deficit $-0.65351$ ($-2/3$); equal-phase fits over two covariance periods, 0.333488 and 1.666759. The card's unchirped-seed values are reproduced ($\mu_2/\mu_1=0.3735559$, $1-r^2=0.01250545$ at $\tau=4$) | pi-chatgpt (gpt) | `2026-10-18-pi-chatgpt-independent-verification` | 2026-10-18 |
| Second solver or relaxed assumption | Full lens-coordinate NLSE with all second derivatives, exact tangent and adjoint, both vacuum and both ASE quadratures, smoothed asymptotically chirped launch: the $l=2$ response decays at rate 0.333825 with log-gain frequency 0.470401 (predictions $1/3$, $\sqrt2/3=0.471405$); grid and step doubling change the decay by $2\times10^{-10}$ | pi-chatgpt (gpt) | `2026-10-18-pi-chatgpt-independent-verification` | 2026-10-18 |
| Error-scaling exponent | Matched-LO phase variance fitted power 2.33351 against the card's implied 1 and the corrected $7/3$ | pi-chatgpt (gpt) | `2026-10-18-pi-chatgpt-independent-verification` | 2026-10-18 |
| Counterexample | Complete-ASE short amplifier ($\varepsilon_0=0.05$, $\Gamma=\sqrt{18}$, $n_{sp}=1$, $\tau=0.02$): matched-LO minimum 0.8964864655 below vacuum; commutator restored to $7\times10^{-14}$. Refutes "with ASE there is no squeezing" as unconditional | pi-chatgpt (gpt) | `2026-10-18-pi-chatgpt-independent-verification` | 2026-10-18 |
| Reproduction before filing | Archive checksums verified; quick suite rerun on a second platform gives 0.8964864655 (same digits) | claude-interactive (claude) | `2026-10-19-claude-interactive-gpt6pro-quick-repro` | 2026-10-19 |
| Novelty search | Background similariton, attraction and reservoir physics are prior art; the $g/3$ breathing rate follows from linearizing the known width equation, so a broad first-ever attraction-rate claim is unsafe. No antecedent was located for the projected-noise exponents (provisional). Lead not accessed: Wang et al., Proc. SPIE 9893, 98930J (2016), DOI 10.1117/12.2227743 | pi-chatgpt (gpt) | — | 2026-10-18 |
| Novelty search | The lead above, read at abstract level (no open full text found): Wang, Liu, Song & Hu, Proc. SPIE 9893, 98930J (2016), DOI 10.1117/12.2227743, and its journal version, Opt. Lett. 41, 5286 (2016), DOI 10.1364/OL.41.005286. They report classical total-power RIN of a spectral-breathing similariton amplifier against launch chirp and input energy. The SPIE abstract credits the attraction, among other causes, with lower ASE-driven RIN. The exponents in (a), and (b) and (c), are not anticipated. Only the interpretive sentence of (a) is partly anticipated, qualitatively and for a different observable: total energy, which this card's flat-gain model leaves at the linear-amplifier value. No closer antecedent in either reference list or in the one citing paper (Haviv et al., Opt. Lett. 51, 1812 (2026), DOI 10.1364/OL.591606, gain-managed amplifier, spectrally sliced RIN; nearest experimental neighbour for (b)). [Review](../docs/review-2026-10-19-claude-interactive.14-spie2016-similariton-noise.md) | claude-interactive.14 (claude) | — | 2026-10-19 |
| Novelty search | Full-text check (PI download, 2026-10-19) of Wang et al., Proc. SPIE 9893, 98930J (2016) and Opt. Lett. 41, 5286 (2016). Classical total-power RIN at a single gain; no shape modes, spectral covariance or phase noise; (a)–(c) not anticipated, the attraction credited only qualitatively for total-energy noise. Verdicts of the abstract-level check confirmed: [review](../docs/review-2026-10-19-claude-interactive-spie2016-fulltext.md) | claude-interactive (claude) | — | 2026-10-19 |
| Novelty search | Full text of Wabnitz, IEEE PTL 19, 507 (2007) (PI download, 2026-10-19): dispersionless parabolic ODEs with gain and a spiral attractor (Fig. 3). No noise, no shape modes beyond the parabola's own, and no stated relaxation rate, so the $l=2$ relaxation is anticipated only qualitatively and (a)–(c) are not anticipated. [Review](../docs/review-2026-10-19-claude-interactive-wabnitz2007-fulltext.md) | claude-interactive (claude) | — | 2026-10-19 |

## Outcome

**Audited, narrowed (2026-10-19).** GPT 6 Pro's earlier cross-family verification is followed by gpt-e's separately committed clean-context audit in task T-20261019-claude-interactive-04. The reduced envelopes and projected readouts pass in the scope above. The old $C_{PP}$ power and unconditional no-squeezing sentence remain superseded; the uniform edge remainder and generic P6 full-field accuracy promise remain unverified. Brightness must satisfy the corrected gain-dependent condition.

**Promoted (2026-10-19).** The narrowed statement above is promising result [R-0011](../results/promising/R-0011-similariton-shape-noise-exponents/RESULT.md), on the PI's decision to promote every cross-family verified claim. G5 is open: when the clean-context audit reports, it fills `audited_by` without changing the status. The corrections in C-20261019-pi-chatgpt-02 are not part of R-0011.

**Audit recorded on the result (2026-10-19).** gpt-e's clean-context audit (pass with reduced regime) closes gate G5 of R-0011, whose Adversarial audit section gives the signed-off scope.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-19 | gpt-e (gpt; gpt-6-astra) | Clean-context pass-reduced-regime; sim-verified → audited. Reduced ASE envelopes and fixed spectral projection signed off; sharp-edge full-moment and P6 accuracy scope explicitly excluded | [Audit](notes/audit-2026-10-19-gpt-e-C-20261008-claude-a-02.md); run `2026-10-19-gpt-e-similariton` |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Filed GPT 6 Pro's independent verification. Status cheap-checks-passed → sim-verified (narrowed); verified_by pi-chatgpt (gpt). Superseded statements marked inline; Checks rows added | Runs `2026-10-18-pi-chatgpt-independent-verification`, `2026-10-19-claude-interactive-gpt6pro-quick-repro`; [review](../docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md) |
| 2026-10-19 | claude-interactive.14 (claude; claude-opus-5-5) | Novelty check of the SPIE 2016 lead (task T-20261019-claude-interactive-05); Novelty search row added; status unchanged. Also restored six control characters in the verified block (the backslashes of `\varepsilon` and `\rm` had become VT and CR bytes); text otherwise unchanged | [Review](../docs/review-2026-10-19-claude-interactive.14-spie2016-similariton-noise.md) |
| 2026-10-19 | claude-interactive.17 (claude; claude-opus-5-5), task T-20261019-claude-interactive-10, on the PI's promotion decision | Status sim-verified → promoted; result R-0011 (promising tier). Statement unchanged; G5 (clean-context audit, T-20261019-claude-interactive-04) still open | [R-0011](../results/promising/R-0011-similariton-shape-noise-exponents/RESULT.md); PI decision of 2026-10-19 recorded in T-20261019-claude-interactive-07 |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5) | Merged gpt-e's audit (PR #76) with the promotion to R-0011: status stays promoted, audited_by gpt-e; G5 of R-0011 set to met | PR #76; claims/notes/audit-2026-10-19-gpt-e-C-20261008-claude-a-02.md |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5) | Full-text novelty check of the Wang et al. (2016) papers; verdicts unchanged; R-0011 Novelty updated | [review](../docs/review-2026-10-19-claude-interactive-spie2016-fulltext.md); task T-20261019-claude-interactive.14-02 |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5) | Full-text check of Wabnitz (2007); R-0011 G6 set to met | [review](../docs/review-2026-10-19-claude-interactive-wabnitz2007-fulltext.md); task T-20261008-claude-a-05 |
