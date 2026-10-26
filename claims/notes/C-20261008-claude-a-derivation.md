# Derivation for C-20261008-claude-a-01 and C-20261008-claude-a-02 (amplifier similariton noise)

- Author: claude-a (claude-opus-5-5), 2026-10-08, task T-20261008-claude-a-01.
- Builds on the passive derivation `claims/notes/C-20261004-claude-a-01-derivation.md`, and on the orchestrator's sketch in P-001, which is re-derived here, not adopted.
- Machine checks are in run `2026-10-08-claude-a-amp-sim-checks`: `symbolic.py` (G1–G5) and `numeric.py` (C1–C9). Their outputs are `symbolic.json` and `numeric.json`.

## 1. Model, units, noise convention

$\partial_zA=-\tfrac i2\beta_2\partial_T^2A+i\gamma|A|^2A+\tfrac g2A+F(z,T)$, with $\beta_2>0$ and $g$ the frequency-flat power gain.

The field is normalized to photon flux, $[A(z,T),A^\dagger(z,T')]=\hbar\omega_0\delta(T-T')$. The amplifier Langevin force has
- $\langle F^\dagger F\rangle=g\,n_{sp}\hbar\omega_0\,\delta\delta$ (spontaneous-emission photons);
- $\langle FF^\dagger\rangle=g(n_{sp}-1)\hbar\omega_0\,\delta\delta$;
- so $[F,F^\dagger]=-g\hbar\omega_0\delta\delta$, as an amplifier requires.

All covariances below are **symmetric-ordered (Wigner)**. The symmetric noise strength is $D=g(n_{sp}-\tfrac12)\hbar\omega_0$, and a coherent input has $\langle\delta A\,\delta A^*\rangle_{\rm sym}=\tfrac12\hbar\omega_0\delta$.

Every variance therefore has the form $I_{\rm in}+(2n_{sp}-1)I_{\rm ase}$.

Photon-counting statistics differ from Wigner moments only by ordering terms that do not enter the signal–ASE beat quantities used here; the energy check C5 confirms this.

**Dimensionless units.** Launch half-width $T_0$, peak power $P_0$, $Z_0=\sqrt{L_DL_{NL}}$, $x=T/T_0$, $\zeta=z/Z_0$.
- $\varepsilon_0=\sqrt{L_{NL}/L_D}=1/N$, the launch semiclassical parameter.
- $\Gamma=gZ_0$, the gain per nonlinear-dispersive length.
- $n_0=P_0T_0/\hbar\omega_0$, and the photon number of the parabolic launch is $N_0=\tfrac43n_0$.

In these units the NLSE reads $\psi_\zeta=-\tfrac i2\varepsilon_0\psi_{xx}+\tfrac i{\varepsilon_0}|\psi|^2\psi+\tfrac\Gamma2\psi+f$, with $\langle ff^*\rangle_{\rm sym}=\Gamma(n_{sp}-\tfrac12)/n_0\,\delta(\zeta-\zeta')\delta(x-x')$.

## 2. Exact moment equations (any pulse, any $N$)

With frequency-flat gain, Kerr and $\beta_2$, the following hold (✓G5: flux forms, and an Euler-operator test for momentum):
- $\rho_\zeta+\partial_xJ=\Gamma\rho$;
- the momentum density $K=-\mathrm{Im}(\psi^*\psi_x)$ obeys $K_\zeta=\Gamma K+\partial_x(\cdot)$;
- $\tfrac{d}{d\zeta}\int x\rho=\Gamma\int x\rho+\varepsilon_0\int K$.

So, with $E=\int\rho$, $\Omega_c=\int K/E$ and $T_c=\int x\rho/E$, the noise-free motion is:
$$E=E_0e^{\Gamma\zeta},\qquad \Omega_c'=0,\qquad T_c'=\varepsilon_0\Omega_c$$
(physical units: $dT_c/dz=\beta_2\Omega_c$). These hold for every pulse shape, with no hydrodynamic approximation.

Noise enters linearly. A white field increment $\delta\psi$ moves a functional $\int 2\mathrm{Re}(u^*\delta\psi)$. Two such functionals have covariance $2D\,\mathrm{Re}\!\int u^*w$. Hence:
- **Energy:** $d\mathrm{Var}(E)=2\Gamma\mathrm{Var}(E)\,d\zeta+2\Gamma(n_{sp}-\tfrac12)E/n_0\,d\zeta$. This gives $N_0\mathrm{Var}(N)/\langle N\rangle^2=1+(2n_{sp}-1)(1-1/G)$, i.e. $\mathrm{Var}(N)=GN_0[1+2n_{sp}(G-1)]$: exactly the linear-amplifier result for any nonlinear pulse (✓C5, C7).
- **Centroids:** $(T_c,\Omega_c)$ is a linear Gaussian process. It has drift $T_c'=\varepsilon_0\Omega_c$ and increment covariance $\tfrac{2D_{\rm dl}}{E}W(\zeta)\,d\zeta$. Here $W=\begin{pmatrix}\sigma_x^2&C\\C&\sigma_k^2\end{pmatrix}$ is the pulse's own time–frequency covariance: $C=\langle(x-T_c)(k_{\rm inst}-\Omega_c)\rangle_\rho$, and $\sigma_k^2$ includes the transform-limited part $\int(\sqrt\rho)_x^2/E$.
- **Input vacuum:** contributes $W(0)/N_0$.
- **Compressed pulse:** a linear compressor of group-delay dispersion $D_c$ gives $T_{\rm comp}=T_c+D_c\Omega_c$, exactly. We use the rms-optimal $D_c=-C_L/\sigma_{kL}^2$.

So the collective-coordinate channel is fixed by the deterministic $W(\zeta)$ alone. The attraction enters only through how $W$ evolves.

## 3. Parabolic background with gain

Dispersionless form, with $\rho=|A|^2$ and $v=-\beta_2\partial_T\phi$: $\rho_z+(\rho v)_T=g\rho$, $v_z+vv_T=-\gamma\beta_2\rho_T$.

Parabolic intensity with linear chirp is an invariant family for any $T_p(z)$ obeying $\ddot T_p=\tfrac32\gamma\beta_2E_0e^{gz}/T_p^2$ (✓G1). In units: $a''=2e^{\Gamma\zeta}/a^2$, with $a=T_p/T_0$.

Rescale with $T_p=ce^{gz/3}s(\tau)$, $\tau=gz$, $c^3=27\gamma\beta_2E_0/2g^2$, so that $c$ is the asymptotic width constant. Then:
- $s''+\tfrac23s'+\tfrac s9=\tfrac1{9s^2}$;
- $V=\tfrac12s'^2+\tfrac{s^2}{18}+\tfrac1{9s}$ obeys $V'=-\tfrac23s'^2$, and $V(s)$ has a single critical point, at $s=1$ (✓G2).

Every launch in the parabolic family (any width, chirp or energy) therefore converges to $s=1$ by LaSalle. Numerically $V\to1/6$ for six launches (✓C3). This confirms the sketch's Lyapunov statement *within the dispersionless parabolic family only*. Whether non-parabolic inputs and the full NLSE also converge is gpt-a's task, not checked here.

In dimensionless units the asymptote is $a\to Ae^{\Gamma\zeta/3}$ with $A^3=18/\Gamma^2$. So $\Gamma=\sqrt{18}$ means the launch width equals the asymptotic width constant.

## 4. Linear blocks with gain

Linearize about any parabolic background and use comoving $\xi=T/T_p$.
- Define $n=\delta\rho/\rho_0$ (relative to the current peak) and $\psi=-\beta_2p$, with $p$ the phase perturbation.
- The gain term cancels exactly against the growth of $\rho_0$.
- Each Legendre component closes (✓G3): $n_l'=-\tfrac{\beta_2l(l+1)}{T_p^2}p_l$, $p_l'=\gamma\rho_0n_l$.

Dimensionless, with $q_l=n_l/\varepsilon_0$:
$$p_l'=\frac{e^{\Gamma\zeta}}{a}q_l,\qquad q_l'=-\frac{l(l+1)}{a^2}p_l .$$
- The generator is traceless, so $\det M_l=1$ along the amplifier (✓C1).
- $\Gamma\to0$ gives the passive Legendre-function blocks of C-20261004-claude-a-01 (✓C2).
- The time variable $\theta$, with $\theta'=e^{\Gamma\zeta}/a$, is still $\varepsilon_0\Phi_{NL}$.

Eliminating $p_l$ gives the sketch's equation: $n_l''+2(\dot T_p/T_p)n_l'+l(l+1)(\ddot T_p/2T_p)n_l=0$.

On the asymptote the rates are $\lambda_l=\tfrac g3[-1\pm\sqrt{1-l(l+1)/2}]$ (✓G4):
- $l=0$: $n_0$ is constant (energy).
- $l=1$: double root at $-g/3$, i.e. the timing and frequency shifts, neutral in absolute terms.
- $l\ge2$: $n_l$ decays as $e^{-gz/3}$ while oscillating at $\tfrac g3\sqrt{l(l+1)/2-1}$, and $p_l$ grows as $e^{gz/3}$.

**Photon-normalized quadratures.** These are $\sqrt E\,\varepsilon_0q$ for the intensity shape and $\sqrt E\,p$ for the phase shape. For $l\ge2$ their power gains scale as $G^{1/3}$ and $G^{5/3}$, with product $G^2$, the same as a phase-insensitive amplifier. Numerically the $l=2$ exponents at $gL=12,18,24$ are (1.705, 0.295), (1.690, 0.310), (1.674, 0.326), converging to 5/3 and 1/3 (✓C8).

The sketch's phase-sensitive statement is therefore confirmed, as an envelope statement on the asymptote, modulated by the $l$-dependent oscillation.

## 5. Noise in the blocks

The ASE and the input vacuum project onto $(n,p)$ as follows:
- intensity part: $\langle S_nS_n\rangle=2D_{\rm dl}(1-\xi^2)\delta(\xi-\xi')/(\rho_0a)$;
- phase part: $\langle S_pS_p\rangle=D_{\rm dl}\delta/[2\rho_0a(1-\xi^2)]$.

The intensity part couples $l$ to $l\pm2$ through $B_{lm}=\int(1-\xi^2)P_lP_m$ (the vacuum-metric issue). This coupling is kept exactly: block $l$'s output covariance with block $m$ uses $B_{lm}$.

The phase part is edge-singular, $\propto1/(1-\xi^2)$. Its effect on every readout used here is subleading:
- In timing, frequency and spectral readouts it appears through the transform-limited bandwidth term or through $\varepsilon_0p$. That is relative order $\varepsilon_{\rm eff}^2\ln(1/\varepsilon_{\rm eff})$.
- In the matched-LO phase it competes with the Kerr-converted part, which is $O(\varepsilon_0^{-2})$ larger.

The edge cut-off shrinks along the amplifier. With $\varepsilon_{\rm eff}=\varepsilon_0/\sqrt{a\,e^{\Gamma\zeta}}\propto e^{-2gz/3}$ on the asymptote, $\delta\propto\varepsilon_{\rm eff}^{2/3}\propto e^{-4gz/9}$. Its logarithm therefore grows only linearly in $gz$, multiplied by $\varepsilon_{\rm eff}^2$, which decays.

**Leading order.** Keep only intensity sources, $\langle S_{q,l}S_{q,m}\rangle=\varepsilon_0^{-2}c_lc_mB_{lm}\cdot2\Gamma(n_{sp}-\tfrac12)e^{-\Gamma\zeta}/n_0$ with $c_l=(2l+1)/2$, and the input $\langle q_lq_m\rangle=\varepsilon_0^{-2}c_lc_mB_{lm}/n_0$. Propagate with $M_l$. The block machinery reproduces the exact energy result (✓C7).

## 6. Collective coordinates at leading order

The chirp dominates the bandwidth: $\kappa=a'/(\varepsilon_0a)$ and $W=\tfrac{a^2}5\begin{pmatrix}1&\kappa\\\kappa&\kappa^2\end{pmatrix}$, which is rank one. The transform-limited part is $O(\varepsilon_0^2\ln)$ relative and is dropped.

With $X(\zeta)=a+a'(\zeta_L-\zeta)$, the width extrapolated to the output, and $h=X-a'a_L/a_L'$:
$$N_0\mathrm{Var}(T_c)=\tfrac15\Big[X(0)^2+(2n_{sp}-1)\Gamma\!\int_0^{\zeta_L}\!e^{-\Gamma\zeta}X^2d\zeta\Big],$$
$$N_0\mathrm{Var}(T_{\rm comp})=\tfrac15\Big[h(0)^2+(2n_{sp}-1)\Gamma\!\int e^{-\Gamma\zeta}h^2\Big],$$
$$N_0\varepsilon_0^2\mathrm{Var}(\Omega_c)=\tfrac15\Big[a'(0)^2+(2n_{sp}-1)\Gamma\!\int e^{-\Gamma\zeta}a'^2\Big].$$
All are in units of $T_0$.

**Closed forms for a launch on the asymptote** (✓C4). Here $\sigma_{T0}$ and $\sigma_{\omega0}=\tfrac g{3\beta_2}\sigma_{T0}$ are the launched rms width and bandwidth, and $U=gL$:
- $N_0\mathrm{Var}(\Omega_c)/\sigma_{\omega0}^2=1+3(2n_{sp}-1)(1-G^{-1/3})$. A linear amplifier gives $1+(2n_{sp}-1)(1-G^{-1})$.
- $N_0\mathrm{Var}(T_c)/\sigma_{T0}^2=(1+U/3)^2+(2n_{sp}-1)(3+U^2/3-3G^{-1/3})$.
- $N_0\mathrm{Var}(T_{\rm comp})/\sigma_{T0}^2=U^2/9+(2n_{sp}-1)(U^2/3-2U+6(1-G^{-1/3}))$. A linear amplifier with ideal dispersion compensation gives $1+(2n_{sp}-1)(1-1/G)$.

**Mechanism for the compressed timing.** An ASE kick at $z'$ moves time and frequency together along the local chirp. The fibre's $\beta_2$ maps the frequency part into timing over the remaining length $L-z'$, and the compressor removes only the output chirp. The residual is $\delta T\cdot\tfrac g3(L-z')$ on the asymptote.

## 7. Spectral intensity covariance (dispersive Fourier transform)

By stationary phase, the chirped output maps time to frequency, $\omega=\kappa T$, with corrections of order $\varepsilon_{\rm eff}$. Define $s(\xi_\omega)=\delta S/S_0$, where $S_0$ is the peak of the mean spectrum and $\xi_\omega=\omega/\omega_{\rm edge}$. Then $s=n+\mathcal Lp/(\kappa T_p^2)$, so $s_l=n_l-l(l+1)\varepsilon_0p_l/(aa')$.

- $l=0$ is the energy.
- $l=1$ is the centroid frequency.
- On the asymptote all $s_{l\ge1}$ decay as $e^{-gz/3}$ relative to $s_0$.

The covariance operator of $\delta S$ (in $L^2$ over the spectral core, Legendre modes $l\le4$) therefore tends to rank one, with the energy mode $\delta S\propto\mathbf 1_{|\xi|<1}$. Its second-to-first eigenvalue ratio falls as $G^{-2/3}$: the fitted slope is −0.652 at $gL=12$–18 (✓C9).

Note that the energy mode of the similariton spectrum is uniform in $\xi$, not $\propto\bar S$, because a higher-energy similariton is both taller and wider.

## 8. Matched local oscillator with gain

- $C_{AA}=G+(2n_{sp}-1)(G-1)$ in output shot-noise units. This is exact.
- At leading order the phase quadrature reads $\bar p=p_0-p_2/5$, so $\varepsilon_0^2C_{PP}/G=4\varepsilon_0^2N_0\mathrm{Var}(\bar p)$.
- Let $r$ be its correlation with the photon number. Then $1-r^2$ is the fraction of phase-quadrature noise that is not linear in the energy noise. It falls as $\approx G^{-2/3}$ on the asymptote (slope −0.648, ✓C9): shape-mode attraction makes the Kerr phase noise uniform across the pulse.
- Passive analogue: the profile-limited squeezing of C-20261004-claude-a-01. With ASE there is no squeezing; $1-r^2$ is the energy-feedforward residual.

## 9. What is not derived

- The $O(\varepsilon_0^2)$ corrections, the edge-layer terms, and the dynamics outside the parabolic family (non-parabolic launch). The predictions below fix the leading order and give the expected error order.
- Gain bandwidth, gain saturation, Raman (classical shift and spontaneous noise), third-order dispersion, self-steepening, ASE–ASE beat noise. All are excluded by assumption, and their dimensionless groups are bounded in the claims.
