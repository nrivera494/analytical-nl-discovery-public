# Frozen targets for the amplifier-similariton validation (claude-interactive.2, T-20261010-claude-interactive.2-01)

Frozen 2026-10-10 before any production run. Only the two prototype runs in
`~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-scratch/` (solver-API and adjoint checks at one
point, $\varepsilon_0=0.05$, $\Gamma=\sqrt{18}$, $gL=6$) were made before this file. Sources of the predictions:
the orchestrator's statements R1-R10 (task prompt), and the frozen tables of C-20261008-claude-a-01 and
C-20261008-claude-a-02 on branch `origin/task/T-20261008-claude-a-01` (read: statements and prediction tables
only). The closed forms of R7 were re-derived here by direct integration of R6(b) on the asymptote (algebra in
the log); they agree with the claim.

## Model and units

$\partial_zA=-\tfrac i2\beta_2A_{TT}+i\gamma|A|^2A+\tfrac g2A+F$, $\beta_2>0$, flat unsaturated gain, white ASE with
$\langle FF^*\rangle=g(n_{sp}-\tfrac12)\hbar\omega_0\,\delta\delta$, symmetric vacuum $\tfrac12$ photon per mode at
the input. Normalized units: $T_0=1$ ps is the seed half-width, $\beta_2=1$ ps²/m, $P_0$ the seed peak power;
$\varepsilon_0=\sqrt{\beta_2/(\gamma P_0T_0^2)}$, $\Gamma=g\sqrt{L_DL_{NL}}$, $U=gL$, $G=e^U$.
Variances are written $I_{\rm in}+(2n_{sp}-1)I_{\rm ase}$ and both parts are reported.

Seeds: parabolic intensity $P_0(1-T^2/T_0^2)$ with soft edges (softplus of width $\delta=0.5\varepsilon_0^{2/3}$ in
$1-T^2/T_0^2$), phase $-qgT^2/(2\beta_2)$ (chirp $v=qgT$). Main case: $\Gamma=\sqrt{18}$, $q=0$. Held-out case:
$\Gamma=1$, $q=0$. Asymptotic seed: $\Gamma=\sqrt{18}$, $q=1/3$.

## Targets

| id | quantity | prediction | parameters |
|---|---|---|---|
| R1 | rms-width $s(\tau)=\sqrt{5}\sigma_T/(c e^{\tau/3})$ and chirp | follow $s''+\tfrac23s'+\tfrac s9=\tfrac1{9s^2}$ with matched initial conditions; $V$ non-increasing; $s\to1$ for all launches; error $\to0$ as $\varepsilon_0\to0$ | $c^3=27\gamma\beta_2E_0/(2g^2)$; launches $(\Gamma,q)$ with $w=(\Gamma^2/18)^{1/3}\in\{0.38,1,1.76\}$, $q\in\{-0.5,0,1/3,1\}$; $\varepsilon_0\in\{0.1,0.05,0.025\}$ |
| R2 | block maps of $(p_l,n_l/\varepsilon_0)$ on the asymptotic seed | $l\ge2$: $n_l\propto e^{-\tau/3}$, angular frequency $\tfrac g3\sqrt{l(l+1)/2-1}$ ($\sqrt2g/3,\sqrt5g/3,g$ for $l=2,3,4$); $l=0$ neutral; $l=1$ double root $-g/3$; no mixing between $l$ | reduced block ODE of C-...-02 (a), readouts below; $\varepsilon_0\in\{0.1,0.05,0.025\}$, $gL\le6$ |
| R3 | effective semiclassical parameter on the asymptote | $\varepsilon_{\rm eff}\propto e^{-2gz/3}$; transform-limited share of the bandwidth $\propto\varepsilon_{\rm eff}^2$ up to a log; edge-layer width$/T_p\propto\varepsilon_{\rm eff}^{2/3}$ | asymptotic seed |
| R4 | energy mapping at fixed $z$ | $d\ln T_p/d\ln E_0=1/3$, $d\ln P_{\rm pk}/d\ln E_0=2/3$, $d\ln\sigma_\omega/d\ln E_0=1/3$, chirp $g/(3\beta_2)$ independent of $E_0$ | paired runs $E_0(1\pm10^{-3})$ |
| R5 | photon-normalized shape quadratures, $l\ge2$ | power-gain envelopes $G^{1/3}$ and $G^{5/3}$, product $G^2$ (linear amplifier: $G$, $G$) | block maps from R2 runs; reduced-model exponents at $gL=12,18,24$: (1.705, 0.295), (1.690, 0.310), (1.674, 0.326) (C-...-02 P2) |
| R6a | energy | $N_0\mathrm{Var}(N)/\langle N\rangle^2=1+(2n_{sp}-1)(1-1/G)$, any seed, Kerr on or off | MC (solver stochastic backend) and adjoint |
| R6a' | solver mapping | `ShotNoise(0.5)` + `GainLangevin(n_s)` is a symmetric-ordered amplifier with $n_{sp}=2n_s^2+\tfrac12$ | MC, $n_s\in\{0.5,1\}$, Kerr on and off |
| R6b | centroid covariance | $(T_c,\Omega_c)$ Gaussian, drift $dT_c/dz=\beta_2\Omega_c$, increment covariance $\tfrac{2D}{E}W(z)dz$, input $W(0)/N_0$ | adjoint vs moment formula vs MC, any $\varepsilon_0$ |
| R6c | compressor | $T_{\rm comp}=T_c+D_c\Omega_c$, $D_c=-C_L/\sigma_{\omega L}^2$ | |
| R7a | centre frequency, asymptotic seed | $N_0\mathrm{Var}(\Omega_c)/\sigma_{\omega0}^2=1+3(2n_{sp}-1)(1-G^{-1/3})$ | $(I_{\rm in},I_{\rm ase})$ = (1, 1.4597), (1, 2.2092), (1, 2.5940), (1, 2.7916) at $U=2,4,6,8$ |
| R7b | timing | $(1+U/3)^2+(2n_{sp}-1)(3+U^2/3-3G^{-1/3})$ | (2.7778, 2.7931), (5.4444, 7.5425), (9, 14.5940), (13.4444, 24.1249) |
| R7c | compressed timing | $U^2/9+(2n_{sp}-1)(U^2/3-2U+6(1-G^{-1/3}))$ | (0.4444, 0.2528), (1.7778, 1.7518), (4, 5.1880), (7.1111, 10.9164) |
| R7d | C-...-01 P3 table | main case, $gL=2,4,6$: values as frozen in the claim (normalizers $a_L$, $a'_L$ from the table) | $\varepsilon_0\in\{0.1,0.05,0.025\}$; deviation $\le5\%$ at these $\varepsilon_0$ except $\Omega_c$ input parts, falling as $\varepsilon_0^2$ up to a log |
| R7e | C-...-01 P5 table (held out) | $\Gamma=1$, $gL=2,4,6$, as frozen | same |
| R7f | C-...-01 P8 table | realistic Gaussian seed (250 fs FWHM, 10 pJ, 1030 nm, $\beta_2=25$ ps²/km, $\gamma=5$ W⁻¹km⁻¹, $g=1.9$ m⁻¹, $L=3.2$ m): $N_0\mathrm{Var}(T_{\rm comp})$ = (0.038353, 0.041576) ps², $\gamma=0$: (0.011271, 0.011246); ratio at $n_{sp}=1$: 3.55; $D_c=-0.045058$ ps² | adjoint; self-steepening off (model) and on (relaxed assumption) |
| R8 | vacuum share on the asymptote | $1/(1+3(2n_{sp}-1))$ for $\Omega_c$, $T_{\rm comp}$ and shape-mode intensity; $1/(1+(2n_{sp}-1))$ for energy (as $G\to\infty$; finite-$G$ forms follow from R7) | adjoint split ($I_{\rm in}$ vs $I_{\rm ase}$) and MC with vacuum-only and ASE-only noise |
| R9 | spectral covariance, Legendre $l\le4$ over the core $\lvert\omega\rvert\le\omega_{\rm edge}=\sqrt5\sigma_\omega$ | tends to rank one, $\lambda_2/\lambda_1\propto G^{-2/3}$; C-...-02 P3 table (main case, $gL=2,4,6$): $\lambda_2/\lambda_1$ = 0.9868, 0.3735, 0.1095 and the $N_0\mathrm{Var}(s_l)$ entries as frozen | adjoint |
| R10 | matched LO | $C_{AA}=G+(2n_{sp}-1)(G-1)$ exactly; $1-r^2\propto G^{-2/3}$; C-...-02 P4 (main case): $1-r^2$ = 0.07436, 0.01251, 0.004356 at $gL=2,4,6$, and $\varepsilon_0^2C_{PP}/G$ as frozen | adjoint |

Readouts (exact linear functionals, hydrodynamic normalization $\rho_{\rm pk}T_p=\tfrac34E$, $T_p=\sqrt5\sigma_T$ and
$T_p'=\sqrt5\beta_2C_{T\omega}/\sigma_T$ of the unperturbed run, $j=\beta_2\mathrm{Re}(A^*\,i\partial_TA)$):
$n_l=\tfrac{2l+1}2\tfrac4{3E}\int P_l(T/T_p)\delta\rho\,dT$;
$p_l=\tfrac{2l+1}{2\beta_2l(l+1)}\tfrac{4T_p}{3E}\big[\tfrac{T_p'}{T_p}\int P_l'(T/T_p)T\delta\rho\,dT-\int P_l'(T/T_p)\delta j\,dT\big]$ ($l\ge1$);
$p_0=\int\mathrm{Im}(\bar A^*\delta A)dT/E+p_2/5$. These reduce to the C-...-02 readouts for $l\le3$.

Pass criteria (stated before the runs): a leading-order statement is confirmed if its deviation falls with
$\varepsilon_0$ at a measured exponent $>0.5$ and is below 5% at $\varepsilon_0=0.025$ (10% for shape-mode
quantities); an exact statement is confirmed if it holds to discretization accuracy or MC statistics (2 sigma).
