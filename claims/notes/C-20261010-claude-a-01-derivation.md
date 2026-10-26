# Derivation note for C-20261010-claude-a-01: exact dispersionless theory of filtered Fano bounds

- Author: claude-a (claude-opus-5-5), 2026-10-10.
- Task: T-20261010-claude-interactive-04, problem P-20261010-claude-interactive-01.
- Code and runs: `runs/2026-10-10-claude-a-dispersionless-fano/`.
  - `dlfano.py` holds the exact covariance, spectral kernels, bounds and the binary search.
  - `lin_ssfm.py` is an independent linearized split-step propagator, used for dispersion and self-steepening.
  - `polarization.py` is the two-polarization model.

## 1. Exact linearized solution

**Model.** $\partial_zA=i\gamma A\,(R*|A|^2)+iA\,\Gamma_R$ with $R(t)=(1-f_R)\delta(t)+f_Rh_R(t)$, where $h_R$ is causal and real with $\int h_R=1$. There is no dispersion and no self-steepening.

**The intensity is conserved.** $\partial_z|A|^2=2\,\mathrm{Re}(A^*\partial_zA)=0$, because $R*|A|^2$ and $\Gamma_R$ are real. So
$$A(z,t)=A_0(t)\,e^{i\gamma z(R*P)(t)+i\int_0^z\Gamma_R}$$
exactly, for the full nonlinear classical field.

**Linearization.** Take shot-noise-normalized quadratures in the frame of the mean phase, $[X(t),Y(t')]=2i\delta(t-t')$, with $p=P/P_0$, $\Phi=\gamma P_0L$ and $\delta P=\sqrt P\,X$. Then:
$$X_{\rm out}=X_{\rm in},\qquad Y_{\rm out}=Y_{\rm in}+KX_{\rm in}+N_R,$$
$$K=2\Phi\sqrt p\,\hat R\sqrt p,\qquad N_R=2\sqrt p\,\xi,\quad \xi=\int_0^L\Gamma_R\,dz.$$
This confirms the task's starting observation: the map is a nonlocal Kerr–Raman shear plus pure phase noise.

**Reservoir.** Unitarity fixes the commutator of $\xi$. Requiring $[Y_{\rm out}(t),Y_{\rm out}(t')]=0$ gives
$$[N_R(t),N_R(t')]=-2i\,[K(t,t')-K(t',t)].$$
The commutator is therefore set by the antisymmetric part of the causal kernel, $\propto\mathrm{Im}\,\tilde h_R(\omega)$. Thermal equilibrium then gives the symmetrized spectrum:
$$\langle N_R N_R\rangle_{\rm sym}=2\Phi f_R\sqrt p\,\hat H\sqrt p,\qquad \tilde H(\omega)=2|\mathrm{Im}\,\tilde h_R(\omega)|\coth\frac{\hbar|\omega|}{2k_BT}.$$

**Output covariance** (exact within the model):
$$V=\begin{pmatrix}I&K^{\mathsf T}\\K&I+KK^{\mathsf T}+N\end{pmatrix},\qquad N=2\Phi f_R\sqrt p\,\hat H\sqrt p .$$

Numerical checks of this covariance:
- $V+i\Omega\succeq0$ on every grid, minimum eigenvalue $\ge-10^{-12}$ (`symplectic_min`). This checks the reservoir normalization.
- The independent split-step propagator reproduces $V$, $\lambda_{\rm gen}$ and the binary optimum to $10^{-13}$ at $\beta_2=0$.
- $P\to0$ gives $V=I$ and $F=1$.

## 2. $\lambda_{\min}(V)$

**Without the reservoir.** $V_0=SS^{\mathsf T}$ with $S=\begin{pmatrix}I&0\\K&I\end{pmatrix}$. The singular-value decomposition of $K$ splits $V_0$ into $2\times2$ blocks $\begin{pmatrix}1&\sigma\\\sigma&1+\sigma^2\end{pmatrix}$, so
$$\lambda_{\min}(V_0)=V_{\min}(\sigma_{\max}/2),\qquad V_{\min}(\Phi)=1+2\Phi^2-2\Phi\sqrt{1+\Phi^2}.$$
- Kerr ($R=\delta$): $\sigma_{\max}=2\Phi$, which is the anchor.
- Short pulses ($T_0\lesssim100$ fs), where the delayed part averages out of the peak shear: $\sigma_{\max}\simeq2(1-f_R)\Phi$.

**With the reservoir, at large $\sigma$.** The Schur form $v^{\mathsf T}Vv=|a+K^{\mathsf T}b|^2+|b|^2+b^{\mathsf T}Nb$ gives
$$\lambda_{\min}(V)\simeq\min_b\frac{b^{\mathsf T}(I+N)b}{b^{\mathsf T}KK^{\mathsf T}b},$$
a generalized singular value.

**Long pulses** ($T_0\gg$ Raman times). $\hat H$ is white with weight $\tilde H(0)=4k_BT|\partial_\omega\mathrm{Im}\,\tilde h_R(0)|/\hbar$. For Blow–Wood, $\partial_\omega\mathrm{Im}\,\tilde h_R(0)=2\tau_2^{-1}/(\tau_1^{-2}+\tau_2^{-2})=8.12$ fs, so $\tilde H(0)=1.276$ at 300 K. The slice at the peak gives
$$\lambda_{\min}\simeq\lambda_{\min}\begin{pmatrix}1&2\Phi\\2\Phi&1+4\Phi^2+2\Phi f_R\tilde H(0)\end{pmatrix}\approx\frac1{4\Phi^2}+\frac{f_R\tilde H(0)}{2\Phi}.$$
So the reservoir leaves no floor. It changes the large-$\Phi$ law from $\Phi^{-2}$ to $\Phi^{-1}$, with coefficient $f_R\tilde H(0)/2=0.115$ at 300 K. That coefficient is linear in $T$ at low frequency, and vanishes at 0 K apart from zero-point terms.

Two caveats (added in the afternoon):
- The slice value is reached for modes restricted to a band $\Omega_b$ only when $\Omega_bT_0\gtrsim30$. A narrower band costs about $(\Omega_bT_0)^{-1.7}$, independent of $T_0$ (`band_cost_check.json`).
- Over all modes, $\lambda_{\min}\le V_{\min}((1-f_R)\Phi)$, through far-detuned modes. For long pulses at 0 K, slow modes at the peak do better.

## 3. $\lambda_{\rm gen}$: the spectral-centroid (momentum) mode

**Bin quadratures.** The binary filter acts on $\tilde A(\omega)$. A bin's amplitude quadrature is $x_\omega=\int[c_\omega X-s_\omega Y]\,dt$, with $c_\omega+is_\omega=e^{-i\psi(\omega)}e^{i\omega t+i\bar\phi(t)}$. So $V^{\rm amp}=BVB^{\mathsf T}$ is an explicit double time integral, and no noise propagation is needed.

**Momentum weights.** Take real weights $g(\omega)=\omega$, i.e. measure the photon-number-weighted spectral centroid. Its noise is
$$\delta P_{\rm mom}=\int(\sqrt p)'\,Y_{\rm in}+\Phi\!\int\sqrt p\,[(\hat R^{\mathsf T}-\hat R)p']\,X_{\rm in}+\int p'\xi .$$
- For Kerr the $X$ term cancels exactly, because $K^{\mathsf T}(\sqrt p)'=\Phi\sqrt p\,p'=\bar\phi'\sqrt p$. Momentum is conserved.
- The reference is the shot noise of the weighted count, $\sum\omega^2\bar n$, the output rms bandwidth.

Hence
$$\lambda_{\rm gen}\le\lambda_{P,R}=\frac{I_1+\Phi^2D_R+\tfrac\Phi2f_RS_R}{I_1+\Phi^2I_{2,R}}$$
with the 1D integrals
- $I_1=\int(\sqrt p)'^2$;
- $I_{2,R}=\int p\,(\hat Rp')^2$;
- $D_R=\int p\,[(\hat R^{\mathsf T}-\hat R)p']^2$;
- $S_R=\int\frac{d\omega}{2\pi}\tilde H|\widetilde{p'}|^2$.

This is exact as an upper bound on $\lambda_{\rm gen}$, given resolved bins. Numerically $\lambda_{P,R}$ equals the momentum-weight value on the grid ($0.07036$ at $T_0=50$ fs, 300 K, $\Phi=10$).

**Kerr closed form.** $\lambda_P=I_1/(I_1+\Phi^2I_2)$:
- Gaussian: $\lambda_P=1/(1+4\Phi^2/3\sqrt3)\to1.299/\Phi^2$;
- sech: $\lambda_P=1/(1+0.9143\Phi^2)$.

The bound holds for any $\beta_2$, $\beta_3$, because dispersion and Kerr conserve $N$ and momentum and the output bandwidth is a mean-field quantity. Only Raman and self-steepening break it.

**Stationary phase: why $\lambda_{\rm gen}\to\lambda_P$.** For a smooth weight $g$, the measured local-oscillator mode is $u=g(\hat\omega)\bar A$. At large $\Phi$ each frequency comes from instants with $\omega=\omega_{\rm inst}(t)$, and to leading order
$$u\simeq\big[g(\omega_{\rm inst})+i\,g'(\omega_{\rm inst})(\sqrt p)'/\sqrt p\big]\bar A .$$
The $O(\Phi)$ anti-squeezed part of $Y_{\rm out}$ cancels away from $\omega=0$ only if $g-\omega g'=0$. That allows a different slope on each side of $\omega=0$.

**Correction (2026-10-10, 12:00).** An earlier version said that every such $g$, with independent slopes on the two sides, gives $\lambda=I_1/(I_1+\Phi^2I_2)$ at leading order. That is false, and is refuted by run `dither_ramp.json`. At $\Phi=10$ the weight $g=|\omega|$ gives $F=13.8$ and the one-sided ramp $\omega\Theta(\omega)$ gives $F=6.9$.

The reason: the instant that produces $\omega=0$ is the pulse peak, which is the brightest instant and has the largest chirp rate. A kink in $g$ there acts over a Fresnel zone $|\bar\phi''|^{-1/2}$ and admits $O(\Phi)$ anti-squeezed noise. Only $g\propto\omega-c$, with a single slope, cancels at leading order. Its value is $\lambda_P=I_1/(I_1+\Phi^2I_2)$.

Each frequency in the SPM band is produced by two instants, an inner and an outer one, with different local Kerr shears. A weight that rotates one instant's local oscillator to its squeezing angle therefore anti-squeezes the other. That is why no single bin, and no narrow band, is squeezed. Every bin variance exceeds 1 and grows with $\Phi$, and only a band-wide linear weight works.

Numerically, $\lambda_{\rm gen}/\lambda_P$ is 0.81–0.996 over $\Phi=1$–40 and 0.99 at $\Phi=50$, approaching 1 with an oscillating, shrinking deficit. The bin threshold must reach about $10^{-9}$ at large $\Phi$ (`grid_check2.json`, `open_prediction_phi50.json`). With Raman the true $\lambda_{\rm gen}$ is lower than $\lambda_{P,R}$, by up to 1.8× at $T_0=50$ fs. A four-term moment basis $\{1,\omega,\omega^2,\omega^3\}$, i.e. a 4×4 generalized eigenproblem, recovers $\lambda_{\rm gen}$ within 7%.

**Raman, long pulses.** With $T_0\gg\tau_{1,2}$ and $\Phi\hbar/k_BT\ll T_0$, $\hat H$ is white with weight $\tilde H(0)$ and the delay terms vanish:
$$\lambda_{P,R}\to\frac{I_1+\tfrac\Phi2f_R\tilde H(0)\int p'^2}{I_1+\Phi^2I_2}\to\frac{0.211}{\Phi}\quad(\text{Gaussian, 300 K}).$$
It is within 7% of $\lambda_{\rm gen}$ for $T_0\ge200$ fs (`raman_momentum_compare.json`).

**Wasted squeezing.**
- Kerr: $\lambda_{\rm gen}/\lambda_{\min}(V)\to4I_1/I_2$, which is $3\sqrt3=5.20$ (7.2 dB) for a Gaussian and 4.375 (6.4 dB) for a sech.
- Raman, short pulses: $\lambda_{\rm gen}\propto\Phi^{-1}$ while $\lambda_{\min}\propto\Phi^{-2}$, so the waste grows linearly in $\Phi$.

## 4. Binary filters

There is no closed form. Section 4a gives the newer results (12:00 onward); the older tabu-search findings follow.

### 4a. Dithering, box relaxation, parity

**Dithering formula** (run `dither_ramp.json`). A binary filter can realize a weight density $d(\omega)\in[0,1]$ by error-diffusion dithering over the fine bins. The dither error is high-pass in $\omega$, so it maps to large delays where the field is dark, and it adds vacuum noise $d(1-d)$ per photon. Then
$$F_{\rm bin}\simeq1-(1-F_d)\,\frac{\langle d^2\rangle}{\langle d\rangle},$$
where $F_d$ is the smooth-weight Fano factor of $d$. This holds to about 1% over 22 shapes at $\Phi=10$.

**Box relaxation as a search** (run `binary_relax_*.json`). For binary $T$, $F[T]=1+T^{\mathsf T}(\Sigma-D)T/\bar n^{\mathsf T}T$ with $D=\mathrm{diag}\,\bar n$, using $T_i^2=T_i$. Its box extension $J(d)$ is realized by dithering. So local minima of $J$ (L-BFGS-B), dithered and then tabu-polished, give binary filters.
- These beat the nested tabu search: $\Phi=10$, 0.471 against 0.509; $\Phi=20$, 0.401 against 0.519.
- They take seconds instead of minutes.
- This is a search method, not a certificate.

**Parity bound** (claim C-20261010-claude-a-03). For non-negative weights on a parity-symmetric problem, $F\ge(\lambda_{\rm odd}+\lambda_{\rm even})/2$. In the dispersionless Kerr case $\lambda_{\rm even}$ is 0.12–0.30 for $\Phi=7$–40 and decays slowly: about $\Phi^{-1/2}$ in window averages to $\Phi=60$, then steeper, reaching 0.055 at $\Phi=100$. So this bound weakens far more slowly than $\lambda_{\rm gen}$.

### 4b. Earlier findings (nested tabu search)

These are numerical findings from the nested tabu search described in `dlfano.py` (`binary_search4`).
- No contiguous band beats $F=1$ in the dispersionless limit (exhaustive band scan).
- A sharp filter edge at frequency $\omega_c$ acts in time at the instants with $\omega_{\rm inst}=\omega_c$. Over a Fresnel width $|\bar\phi''|^{-1/2}$ it rotates the local oscillator by $O(1)$, which picks up the anti-squeezed phase noise $4\Phi^2p^2$. The half-spectrum filter has $F=11.6$ at $\Phi=10$.
- The best filters found are one-sided combs that avoid edges on bright instants. They reach $F\approx0.46$–0.56 for $\Phi=7$–30, and appear not to improve with $\Phi$. Superseded by 4a: the better search finds about $0.47(\Phi/10)^{-0.21}$.
- Their noise budget at $\Phi=10$: anti-squeezed modes 0.05, vacuum-like 0.34, squeezed 0.12. Their overlap with the momentum mode is 0.28. A non-negative filter can project at most about half of the odd momentum mode, which is the Cauchy–Schwarz argument. Values below 1/2 use additional moderately squeezed even modes.
- This apparent saturation was a search artefact (see 4a). Binary-specific bounds are the job of T-20261010-claude-interactive-03.

## 5. Self-steepening, dispersion, polarization

**Self-steepening.** The canonical variables are photon-flux amplitudes $b(\omega)=\tilde A(\omega)/\sqrt{1+s\omega}$, which is an $\omega$-dependent normalization. With them the linearized map is symplectic to $7\times10^{-9}$; with the naive normalization it is not.
- Time reversal ($t\to-t$, $s\to-s$) makes every filter quantity even in $s$ for a symmetric pulse, so there is no first-order term.
- At $\Phi=10$: $\Delta\lambda_{\rm gen}/\lambda_{\rm gen}=-0.02\%$ at $\Phi s=0.05$ and $+2.3\%$ at $\Phi s=0.1$.
- $\lambda_{\min}(V)$ with self-steepening and no dispersion is dominated by dark modes near the grid cut-off and depends on the grid. It is not reported.

**Dispersion** (independent split-step propagator, both signs of $\beta_2$). Let $x=\Phi^2L/L_D$.
- $\lambda_{\rm gen}$ changes by $\le2\%$ for $x\le0.1$, and by about 5–14% at $x=0.3$–1.
- The best binary responds at first order in $\beta_2$ (normal lowers it, anomalous raises it). At $x=0.1$ the change is about $\pm1.7\%$ for $\Phi=10$ and $-9\%$/$+11\%$ for $\Phi=20$ (`binary_vs_dispersion.json`).
- Normal dispersion: $\lambda_{\min}(V)/V_{\min}(\Phi)-1=\frac{\Phi^{3/2}}{\sqrt{1+\Phi^2}}\sqrt{\tfrac13|p''(0)|\beta_2L}\,[1+c_2\sqrt y]$, with $y=\Phi L/L_D$ and $c_2\simeq1.0$. This is the harmonic-oscillator balance derived in claim C-20261010-claude-a-01. Runs `lam_min_dispersion.json` and `lam_min_dispersion_sech.json` measure an exponent of 0.502 at $\Phi=2$–20.
- The momentum bound with dispersion uses the actual output bandwidth: $\lambda_{\rm gen}\le\langle\omega^2\rangle_{\rm in}/\langle\omega^2\rangle_{\rm out}(\beta_2)$. It holds at every converged point and is 0.85–0.96 tight (`momentum_dispersion.json`).
- Anomalous dispersion: $\lambda_{\min}(V)$ collapses for any $\beta_2<0$. Modulation instability amplifies dark vacuum sidebands, and the collapse depends on the grid bandwidth. The dispersionless $\lambda_{\min}(V)$ is the $\beta_2\to0^+$ limit.

**Polarization, isotropic fibre (Kerr).** In the circular basis $|A_\pm|^2$ are $z$-invariant. $K$ is the $2\times2$ matrix $\tfrac{4\Phi p}{3}\begin{pmatrix}c_+&2\sqrt{c_+c_-}\\2\sqrt{c_+c_-}&c_-\end{pmatrix}$, with $c_\pm=(1\pm\sin2\chi)/2$. Hence
$$\lambda_{\min}(V)=V_{\min}(\Phi_{\rm eff}),\qquad \Phi_{\rm eff}=\tfrac\Phi3\big(1+\sqrt{1+3\cos^22\chi}\big),$$
which is $\Phi$ for linear input and $2\Phi/3$ for circular input.

**Polarization, strong linear birefringence** (no walk-off): $\Phi_{\rm eff}=\tfrac\Phi2\big(1+\sqrt{1-\tfrac{20}9c_xc_y}\big)$, which is $5\Phi/6$ at 45°.

Linear or circular input leaves the orthogonal channel dark, so filtered counting reduces to the scalar case with $\Phi_{\rm eff}$. Elliptical input needs the two-channel computation (run).

## 6. Additions (2026-10-10, afternoon)

### Weak normal dispersion: the general ground-state form

Write the peak intensity as $1-p\simeq\kappa|t|^{2m}$, where $m=1$ for Gaussian and sech and $m=2$ for $e^{-t^4}$.

**The functional.** The best mode minimizes
$$\big\langle b\Omega^2+A\kappa|t|^{2m}\big\rangle,\qquad b=\tfrac13\tfrac{\Phi^2}{\sqrt{1+\Phi^2}}\beta_2L,\quad A=\tfrac{2\Phi}{\sqrt{1+\Phi^2}} .$$
- $b$ comes from the CW sideband generator $\begin{pmatrix}0&-a\\a+2g&0\end{pmatrix}$: to first order in $a=\beta_2\Omega^2/2$, $\mathrm{tr}\,MM^{\mathsf T}=2+4\Phi^2-\tfrac83aL\Phi^3$.
- $A$ comes from $d\ln V_{\min}/d\Phi=-2/\sqrt{1+\Phi^2}$.

**Result.** Scaling gives
$$\frac{\lambda_{\min}}{V_{\min}(\Phi)}-1=e_{2m}\,b^{m/(m+1)}(A\kappa)^{1/(m+1)},$$
with $e_2=1$ (harmonic) and $e_4=1.0603620905$ (quartic).
- $m=1$: exponent 1/2 in $y$.
- $m=2$: exponent 2/3, with prefactor $0.64226\,\Phi/\sqrt{1+\Phi^2}$.

**Status.** The $m=2$ prediction was frozen before computing (`HELDOUT.md`, commit 326c335) and tested in `lam_min_dispersion_flattop.json`.

**Next order ($c_2\simeq1.0$).**
- Two pieces of the same order:
  - the local-symbol corrections: the CW sideband formula beyond first order in $a$, and the non-quadratic part of $V_{\min}(\Phi p(t))/V_{\min}(\Phi)=p^{-2}+\dots$. A numerical ground state of $H=S(1+K)S-1$ gives about 0.47;
  - dispersive reshaping of the mean field. Near the peak, $\partial_z|A|^2=\beta_2\,\mathrm{Im}(A^*\partial_t^2A)=-2\beta_2\Phi z\,p$, so the $z$-averaged peak intensity is $1-y/3$ and the peak shear is $\Phi(1-y/3)$.
- Combined, these reproduce the propagated $\lambda_{\min}$ to $3\times10^{-5}$ to $3\times10^{-3}$ relative (`c2_symbol_model.json`, `c2_reshaping_check.json`). They over-correct slightly, so $c_2$ is not derived in closed form.

### Birefringence of arbitrary strength (Kerr, 45° linear input)

Each time slice obeys the two-component ODE with the coherent term $\tfrac13A_x^*A_y^2$ and phase mismatch $\Delta\beta$. With $b=\Delta\beta/\gamma P_0$, it interpolates between the isotropic case ($b=0$, $\Phi_{\rm eff}=\Phi$) and strong birefringence ($b\to\infty$, $\Phi_{\rm eff}=5\Phi/6$).

Numerically, $\Phi_{\rm eff}(b)/\Phi$ collapses in $b$ for $\Phi=5$, 10 and 20 to within about 1%. The crossover lies at $0.03\lesssim b\lesssim5$. There is no closed form.

### Bin-set dependence

$\lambda_{\rm gen}$ and $\lambda_{\rm even}$ are minima over readouts on a bin set $B$. Admitting darker bins can only lower them.
- $\lambda_{\rm gen}$ moves by 0.4–3% between thresholds $10^{-6}$ and $10^{-12}$ for $\Phi\le40$.
- $\lambda_{\rm even}$ moves by up to 2.5×.

Linearization needs $\bar n_i\gg1$ in every bin used, so the physical bin set depends on the pulse energy. Quote both quantities with their $B$.

### Anisotropic Raman: exact reduction for linear and circular input (derived, not run)

**Model.** Write the delayed response in Hellwarth form, $P_i\propto E_i\!\int a\,E_jE_j+E_j\!\int b\,E_iE_j$, with $a$ the isotropic and $b$ the anisotropic kernel, and $\int(a+b)=1$ for the parallel response.

**Three channels.** For transverse envelopes this splits into three independent channels. Each couples to one bilinear and has its own thermal bath, by fluctuation–dissipation per channel:
- $M_0=|A_x|^2+|A_y|^2$, kernel $a+b/2$;
- $M_1=|A_x|^2-|A_y|^2$, kernel $b/2$;
- $M_2=2\,\mathrm{Re}\,A_xA_y^*$, kernel $b/2$.

The $M_0$ kernel collects $a$, the 3D-trace part of the $b$ bath ($b/3$), and one traceless component ($b/6$). Each envelope equation reads
$$\partial_zA_i\ni i\gamma f_R\sum_k\frac{\partial M_k}{\partial A_i^*}\big[(r_k*M_k)+\xi_k\big].$$
In the circular basis, $M_1+iM_2=2A_-A_+^*$.

**Linear input.** $A_y=0$ at mean field. The $x$ channel sees $r_0+r_1=a+b$, the parallel kernel, with noise from both channels. The $y$ channel is dark at linear order. So C-20261010-claude-a-01 and -02 apply with $h_R\to a+b$.

**Circular input.** $A_-=0$. Then $\partial M_{1,2}/\partial A_+^*\propto A_-=0$, so $A_+$ is an exact scalar shear with kernel
$$\tfrac23(1-f_R)\delta+f_R\,(a+b/2),$$
and a reservoir from the $M_0$ channel only. $A_-$ is dark at linear order and invisible to counting.
- Long-pulse peak phase: $\Phi_{\rm eff}=[\tfrac23(1-f_R)+f_R(1-\rho/2)]\Phi$, with depolarization weight $\rho=\int b$.
- Without Raman this is $2\Phi/3$.
- With $f_R=0.245$ and $\rho$ between 0.21 and 0.25, it is 0.718–0.723$\,\Phi$. These parameter values are from the gnlse-python implementation of the Lin–Agrawal response (source code read; the paper, OL 31, 3086 (2006), was not accessed). That source gives only the parallel combination $(f_a+f_c)h_a+f_bh_b$, so $\rho$ is uncertain within that range.

**Elliptical input.** The anisotropic channels act on $2A_-A_+^*$, whose phase rotates with the nonlinear ellipse rotation. With a delayed response this exchanges power between $\sigma_\pm$, so neither $|A_\pm|^2$ is conserved and there is no exact shear.

**Propagation (`vector_raman_prop.py`).** The three channels and their reservoirs are integrated in $z$ through the Lyapunov equation $dV/dz=JV+(JV)^{\mathsf T}+D$ (RK4, $n_z=400$).
- **Validation.** It reproduces the exact circular and linear reductions to 6 digits ($\lambda_{\min}$, $\lambda_{\rm gen}$, binary) and the Kerr-only elliptical run. $V+i\Omega\succeq0$ to $-6\times10^{-6}$.
- **Results** at $\chi=\pi/8$, $T_0=200$ fs, $\Phi=10$, Lin–Agrawal-type kernels, polarization-insensitive bins:
  - $\lambda_{\rm gen}=0.0277$ (0 K) and 0.091–0.093 (300 K, the two splits); best binary 0.656 and 0.684.
  - Linear input: 0.0170 / 0.0611, binary 0.510 / 0.535. Circular: 0.028 / 0.085–0.087, binary 0.53–0.55 / 0.57.
  - At 300 K, elliptical input is noisier than both limits, and it is the worst case for binary filters.
  - The $\sigma_+$ fraction at the peak drifts from 0.854 to 0.834 over the fibre.

