---
agent: claude-b
model: claude-opus-5-5
family: claude
date: 2026-10-10
task: T-20261010-claude-interactive-05
problem: P-20261010-claude-interactive-01
runs:
  - 2026-10-10-claude-b-nd-oracle
  - 2026-10-10-claude-b-nd-meanfield
  - 2026-10-10-claude-b-nd-semiclassical
  - 2026-10-10-claude-b-nd-heldout
---

# Semiclassical theory of filtered Fano bounds in normal dispersion (Gaussian, $N\gg1$)

Derivation and numerics behind claim C-20261010-claude-b-01. Auditors should not read this before committing their report.

## 1. Scaling

**Normalized equation.** In normal dispersion, with $\tau=T/T_0$, $\xi=z/L_D$, $u=A/\sqrt{P_0}$ and $N^2=\gamma P_0T_0^2/\beta_2$:
$$iu_\xi-\tfrac12u_{\tau\tau}+N^2|u|^2u=0,\qquad u(0)=e^{-\tau^2/2}.$$

**Semiclassical form.** With $\varepsilon=1/N$ and the semiclassical distance $Z=N\xi=z/\sqrt{L_DL_{NL}}$ this becomes
$$i\varepsilon u_Z-\tfrac{\varepsilon^2}{2}u_{\tau\tau}+|u|^2u=0,$$
the defocusing NLSE with $\hbar\to\varepsilon$. The peak nonlinear phase is $\Phi_{\rm peak}=N^2\xi=NZ$.

**Hydrodynamic limit.** Write $u=\sqrt\rho\,e^{i\theta/\varepsilon}$ and $v=\theta_\tau$ (signs chosen for the conjugate field, which obeys the standard defocusing form). The mean field obeys, up to $O(\varepsilon^2)$:
- the shallow-water equations $\rho_Z+(\rho v)_\tau=0$ and $\theta_Z+\tfrac12v^2+\rho=0$;
- equivalently, Riemann invariants $r_\pm=v\pm2\sqrt\rho$ with speeds $v\pm\sqrt\rho$.

**Time–frequency map.** The instantaneous angular frequency is $\omega=\mp Nv(\tau)$, depending on the sign convention. Before breaking, $v(\tau)$ is single-valued but not monotone: it peaks near the pulse shoulders. So every frequency below the maximum appears at two instants, an inner and an outer branch, and the spectrum shows fringes.

## 2. Mean field and wave breaking (run `2026-10-10-claude-b-nd-meanfield`)

**Onset of oscillations.** The first extra intensity maximum (threshold $10^{-6}$ of the peak) appears at $Z=1.21$, 1.23, 1.2375 and 1.244 for $N$ = 10, 20, 40 and 80. So the hydrodynamic breaking distance of the Gaussian is $Z_b\approx1.25$.

**Dispersionless gradient catastrophe.** Integrating the $\varepsilon=0$ equations directly (pseudo-spectral; `gradient_catastrophe.py`), $\max|v_\tau|$ diverges at $Z_b\approx1.27\pm0.02$. A linear fit of $1/\max|v_\tau|$ gives 1.286 on 4096 points and 1.268 on 8192; the filtered method blurs the singularity. This is consistent with the NLSE onset extrapolated to $N\to\infty$.

**Comparison with the quoted formula.** The often-quoted $z_{\rm wb}=L_D/\sqrt{4N^2e^{-3/2}-1}$ gives $Z\to1.0585$.
- It is attributed to Anderson et al. 1992 through Finot et al. 2008. I could read neither (see the log for access).
- It is used here only as the reference scale for $z/z_{\rm wb}$.
- So $z/z_{\rm wb}=1$ ($Z=1.06$) lies before the onset, and $z/z_{\rm wb}=1.5$ ($Z=1.59$) after it.

## 3. Fluctuations: block structure and the leading order of $\lambda_{\min}(V)$

**Quadratures.** Take quadratures relative to the local mean phase:
- amplitude $X=\delta\rho/(2\sqrt\rho)$;
- phase $Y=\sqrt\rho\,\delta\theta/\varepsilon$.

These are in photon units, so input vacuum has covariance $\mathbb 1$, normalized to shot noise. In terms of $\delta\rho$ and $\delta\theta$, the linearized Madelung equations are $\varepsilon$-independent at leading order (the quantum pressure is $O(\varepsilon^2)$).

**Block form.** Hence, in $(X,\tilde Y)$ with $\tilde Y=\varepsilon Y$, the input–output map $M_h=\begin{pmatrix}A&B\\C&D\end{pmatrix}$ is $\varepsilon$-independent. In $(X,Y)$ it is
$$M=\begin{pmatrix}A&\varepsilon B\\ C/\varepsilon&D\end{pmatrix}.$$
- $C$ is the shear of the scaled phase driven by input amplitude noise. With no dispersion, $\tilde Y=-2Z\rho_0X_0$, i.e. $C=-2Z\rho_0$.
- $M_h$ is symplectic, so $A^{\mathsf T}D-C^{\mathsf T}B=\mathbb 1$ and $B-AC^{-1}D=-C^{-\mathsf T}$.

**Smallest eigenvalue.** $V=MM^{\mathsf T}$, and for an output vector $(x,y)$, $\|M^{\mathsf T}(x,y)\|^2=\|A^{\mathsf T}x+C^{\mathsf T}y/\varepsilon\|^2+\|\varepsilon B^{\mathsf T}x+D^{\mathsf T}y\|^2$. A variance of order $\varepsilon^2$ needs $y=\varepsilon\hat y$ with $A^{\mathsf T}x+C^{\mathsf T}\hat y=0$, and then the variance is $\varepsilon^2\|C^{-1}x\|^2$. Therefore
$$\lambda_{\min}(V)=\frac{\varepsilon^2}{\sigma_{\max}(C_Z)^2}+o(\varepsilon^2)=\frac{\Lambda(Z)}{N^2}+o(N^{-2}),\qquad\Lambda(Z)=\sigma_{\max}(C_Z)^{-2}.$$
- **Universality.** $\Lambda$ depends only on $Z$ (and on the pulse shape).
- **Dispersionless check.** It gives $\Lambda=1/(4Z^2)$, i.e. $\lambda_{\min}=1/(4\Phi_{\rm peak}^2)$: the large-$\Phi$ Kerr anchor on the card, and the short-length limit of task -04.
- **Status.** This is a leading-order statement. The truncation (infinitely many modes, unbounded $C^{-1}$) is handled numerically below, not proved.

**Small-$Z$ expansion.** Near the peak, $\rho_0\approx1-\tau^2$, and expanding the linearized hydrodynamics to $O(Z^3)$ gives
$$\delta\theta=-Z\delta\rho_0-\tfrac{Z^3}{3}\rho_0'\delta\rho_0'-\tfrac{Z^3}{6}(\rho_0\delta\rho_0)'' .$$
- The operator $C/(-2Z)$ is then $1-\tau^2+\tfrac{Z^2}{6}\partial_\tau^2+O(Z^2)$: a harmonic oscillator, whose largest eigenvalue is $1-Z/\sqrt6+O(Z^2)$.
- Hence $\sigma_{\max}=2Z(1-Z/\sqrt6+O(Z^2))$ and
$$\Lambda(Z)=\frac{1+(2/\sqrt6)Z+O(Z^2)}{4Z^2},\qquad 2/\sqrt6=0.8165 .$$
- Only the $O(Z)$ coefficient is claimed: at $O(Z^2)$ the first-derivative term and the curvature of $\rho_0$ beyond $\tau^2$ also contribute.
- Physically, the most squeezed mode is the oscillator ground state, of width $\sim\sqrt Z$ about the peak. Dispersion makes a narrower mode pay in acoustic spreading, and a wider one samples lower intensity.

**Reduced computation of $\Lambda(Z)$** (run `2026-10-10-claude-b-nd-semiclassical`).
- $C$ is computed on the span of the first $M$ Hermite functions, from $2M$ propagations instead of $4N_t$.
- At $Z=0.742$: $\Lambda_{\rm red}=0.87542$ ($N=10$) and $0.87576$ ($N=20$), the same for $M$ = 20, 40 and 60. So $C$ is $N$-independent to $4\times10^{-4}$, as the scaling predicts.
- The full oracle gives $N^2\lambda_{\min}=0.8571$ ($N=10$) and $0.8724$ ($N=20$), i.e. $-2.1\%$ and $-0.4\%$ from $\Lambda_{\rm red}$.
- Table against $Z$: see section 5.

## 3b. Characteristics and Riemann invariants (how $C_Z$ is built)

**Linearized system.** In the standard defocusing form, $\rho_Z+(\rho v)_\tau=0$ and $v_Z+vv_\tau+\rho_\tau=0$. The Riemann invariants $r_\pm=v\pm2\sqrt\rho$ obey $\partial_Zr_\pm+c_\pm\partial_\tau r_\pm=0$ with $c_\pm=v\pm\sqrt\rho$. Linearizing about the mean field gives
$$\partial_Z\delta r_\pm+c_\pm\partial_\tau\delta r_\pm=-(\partial_\tau r_\pm)\,\delta c_\pm,\qquad \delta c_\pm=\tfrac{3\delta r_\pm+\delta r_\mp}{4}.$$
So each perturbation is carried along its own characteristic and is fed by the other one through the mean-field gradients. The phase follows from $\delta\theta_Z=-(v\,\delta v+\delta\rho)$ with $\delta v=(\delta r_++\delta r_-)/2$ and $\delta\rho=\sqrt\rho\,(\delta r_+-\delta r_-)/2$.

**What this means for the map.**
- **Input.** An input amplitude perturbation enters as $\delta r_\pm=\pm\delta\rho_0/\sqrt{\rho_0}$, equal and opposite on the two families.
- **$C_Z$.** $C_Z$ is the map from it to $\sqrt\rho\,\delta\theta$ after the two families have separated and sheared. At small $Z$ they have not separated, and $C_Z\to-2Z\rho_0$, the local Kerr shear. As $Z$ grows, the two families move apart at relative speed $2\sqrt\rho$, so the shear seen by a narrow input mode is diluted. That dilution is the origin of the $Z^2\partial_\tau^2/6$ term of the oscillator in section 3.
- **Computation.** For the Gaussian these equations have no closed-form solution. `hydro_direct.py` integrates the equivalent $(\rho,v,\theta)$ form directly; its $\Lambda$ and $\Pi$ match the NLSE-based values to $\le10^{-4}$ (section 5.2).
- **Breaking.** At the gradient catastrophe ($Z_b\approx1.27$) $\partial_\tau r_\pm$ diverges in the tails, and the linearized transport is singular there. The squeezed modes sit in the centre, where the mean field stays smooth (rarefaction). That is why $\Lambda$ continues smoothly through breaking.

## 3c. A single band as a time gate plus edges

**Count of a band.** On a monotone part of the chirp, a band $[\omega_1,\omega_2]$ selects the instants $\tau_1,\tau_2$ where $Nv=\omega_{1,2}$. Its count fluctuation is
$$\delta N=\bar n\Big[\int_{\tau_1}^{\tau_2}\delta\rho\,d\tau+\rho(\tau_2)\delta\tau_2-\rho(\tau_1)\delta\tau_1\Big],\qquad \delta\tau_e=-\frac{\varepsilon\,\partial_\tau\delta\phi}{v_\tau}\Big|_{\tau_e},$$
with $\delta\phi$ the phase fluctuation in radians.

**Size of the edge term.**
- In shot-noise units the phase noise is of order $Y/\sqrt{\rho}$, with $Y=\tilde Y/\varepsilon$ and $\tilde Y=O(1)$.
- So the edge term involves $\partial_\tau\tilde Y$ at a point. This is the derivative of a nearly white field, regularized only over the Fresnel width $w\sim\sqrt{\varepsilon/|v_\tau|}$ of a sharp spectral edge.
- Its contribution to $F$ therefore scales as $\rho_e^3\,Z^2/(w^3v_\tau^2\int_{\rm gate}\rho)\propto\rho_e^3\,\varepsilon^{-3/2}$.

**What the data show instead** (`runs/2026-10-10-claude-b-nd-oracle/interval_edges.json`). The estimate above suggests pushing the edges into the dark wings. The optimal intervals do not do that.
- **Large $N$.** For $N\ge14$ at $z/z_{\rm wb}=0.7$ and $N\ge28$ at 1.0, the best band is symmetric, with edges at $|v|$ = 0.60–0.62 and 0.74 respectively.
  - These are near the outer spectral maxima, the "ears" of the SPM spectrum, where $\bar n_e/\bar n_{\max}$ = 0.14–0.23. The band removes only 1.7–4% of the photons.
  - The edges are therefore near the turning point of the chirp, $v_\tau\to0$. That point is a caustic of the time–frequency map, where the Fresnel-width estimate above does not apply.
- **Small $N$.** At smaller $N$ the best interval is asymmetric: one edge near line centre (at $\bar n_e/\bar n_{\max}\approx0.8$–0.98) and the other in the far wing.
- **Open.** The saturation of the best-interval $F$ near 0.8 ($z/z_{\rm wb}=0.7$) and 0.73 (1.0) is not explained, and the edge argument above is incomplete.

## 4. Spectral readouts

**Single-branch weighted counting.** On a single monotone branch, stationary phase maps a spectral weight $w(\omega)$ to a time-domain functional:
$$\delta N_w=\int\big[w(v)\,\delta\rho+w'(v)\,\rho\,\delta v\big]\,d\tau,\qquad\delta v=\partial_\tau(\tilde Y/\sqrt\rho).$$
- Both terms are $O(1)$ in the hydrodynamic scaling.
- $\lambda_{\rm gen}=O(\varepsilon^2)$ needs the $O(1)$ part, $A^{\mathsf T}g_w+C^{\mathsf T}h_w$, to cancel, with $g_w=2\sqrt\rho\,w(v)$ and $h_w=-\partial_\tau(w'(v)\rho)/\sqrt\rho$. The numerics show this is reachable: $N^2\lambda_{\rm gen}$ tends to a constant.

**Binary filters.**
- $w\in\{0,1\}$ makes $w'$ a sum of delta functions at the edges, so with finitely many edges the $O(1)$ part cannot cancel. A band gives the gate-plus-edges count $\delta N=\int_{\rm gate}\delta\rho\,d\tau+\sum_{\rm edges}\pm\rho\,\delta v/|v_\tau|$.
- The edge terms involve $\delta v$ at a point, which is a derivative of white noise. This is regularized only by the time–frequency resolution of the map, which narrows as $N$ grows.
- My first expectation, never derived, was that the best single band approaches $F=1$ as $N\to\infty$. The data contradict it. The best band saturates near 0.8 ($z/z_{\rm wb}=0.7$) and 0.73 (1.0), with symmetric edges near the spectral ears (section 3c).
- Filters that resolve the two-branch fringes see the relative phase of the branches, which is amplified as $1/\varepsilon$. That is a self-homodyne channel, and it lets structured binary filters improve with $N$.

**The spectral centroid is an exact $O(\varepsilon^2)$ member of the smooth family (claim C-20261010-claude-b-02).**
- **The weight.** Take $w(v)=v$, i.e. weight $\omega-\bar\omega$.
- **Pull-back.** Its counting functional is the field momentum $\int\mathrm{Im}(u^*u_\tau)\,d\tau$, which the NLSE conserves. So the pulled-back functional is the input momentum, $2\int u_0'\,\delta u_{\rm imag}\,d\tau$ for real $u_0$: a pure input-phase functional with no $X_0$ part.
- **Size.** In the hydrodynamic scaling it is $O(\varepsilon)$, so its variance is $O(\varepsilon^2)$ relative to the output shot noise $\sum\omega^2\bar n_{\rm out}=N^2\langle v^2\rangle_\rho$.
- **Exact value.** $F_{\rm cen}=\langle\Delta\omega^2\rangle_{\rm in}/\langle\Delta\omega^2\rangle_{\rm out}$. The Hamiltonian $\int(\tfrac12|u_\tau|^2+\tfrac{N^2}{2}|u|^4)$ gives $\langle\Delta\omega^2\rangle_{\rm out}=\tfrac12+N^2K$, with $K=(\int\rho_0^2-\int\rho^2)/\int\rho_0$.
- **Consequence.** Hence $N^2\lambda_{\rm gen}\le1/(2K(Z))$ as $N\to\infty$.
- **What the data show.** The real-weight optimum turns out to be only 0.03–0.9 dB below the centroid. That is, the minimizer of $\lambda_{\rm gen}$ is close to the momentum weight.

**Why sign matters for filters.**
- **Smooth non-negative weights.** Consider weights $w\ge0$ that are smooth on the fringe scale. At small $Z$ (dispersionless kinematics $v=-Z\rho_\tau$), the cancellation condition becomes $w(v)-vw'(v)-Z^2\rho\rho_{\tau\tau}w''(v)=0$ on both branches. Its only solutions are $w\propto v$. So a smooth $w\ge0$ cannot cancel the $O(1)$ part, and its $F$ stays $O(1)$ at small $Z$.
- **What still lowers $F$.** Anything below $O(1)$ must come from fringe-resolving structure, i.e. interference between branches.
- **The filters found.** The best binary filters found are of this type: one broad band on one side of the spectrum, plus a set of narrow bands near the centre on the scale of the interference fringes there. In $v$ the spacings are 0.05–0.35, against fringe spacings of 0.08–0.36 for $N$ = 10–40. The fringes come from the centre of the pulse interfering with its weakly chirped far tails, which emit at the same small $|v|$.
- **Anatomy** (`runs/2026-10-10-claude-b-nd-oracle/comb_diagnostic.json`, $z/z_{\rm wb}=0.7$, $N$ = 10–40).
  - Each part alone is strongly super-Poissonian: the band (|v| ≥ 0.3) has $F$ = 2.0–4.5 and the central bands have $F$ = 3.7–10.
  - Their counts are anticorrelated with coefficient −0.88, −0.90, −0.90, −0.89, −0.96 for $N$ = 10, 14, 20, 28, 40.
  - So the filter is a self-homodyne pair: two spectral regions carry opposite-sign copies of the large, $\Phi$-amplified phase-quadrature noise, which cancel in the sum. The residual sets $F$, and the cancellation improves with $N$.
- **Status.** This mechanism is a hypothesis; no theory of the comb's asymptotics is given.

**Parity bound** (C-20261010-claude-a-03 by claude-a, unverified; evaluated here in `parity_bound.json`).
- The problem is parity-symmetric. The optimal weighted mode, which is centroid-like, is odd: $\lambda_{\rm odd}=\lambda_{\rm gen}$ at all 33 points.
- A non-negative filter has $|y_{\rm even}|\ge|y_{\rm odd}|$, so $F\ge(\lambda_{\rm odd}+\lambda_{\rm even})/2\approx\lambda_{\rm even}/2$.
- $\lambda_{\rm even}$ decays only as about $N^{-0.5}$ (0.30 → 0.15 for $N$ = 10 → 40 at $z/z_{\rm wb}=0.7$).
- This certifies 7–16 dB of the binary gap, and leaves 2–6 dB between the bound and the best binary filters found.
- This is the rigorous form of "sign matters".

## 5. Numerics

### 5.1 Oracle (run `2026-10-10-claude-b-nd-oracle`)

**Method.**
- Full linearized covariance by central differences of the split-step map, in all $2N_t$ input directions.
- Grid: $N_t$ = 512 or 1024 over 40 $T_0$; 1024 over 60 $T_0$ at $z/z_{\rm wb}$ = 2 and 3.
- Step: peak nonlinear phase step 0.02.
- Spectral bins of width $2\pi/40$, keeping the bins that hold $1-10^{-9}$ of the photons.

**Validation.**
- **Linear map.** $V=1$ to $1.5\times10^{-9}$.
- **Small-$N$ chain.** At $N=0.3$ the chain is ordered.
- **$\lambda_{\rm pass}$ by two methods.** The penalty method and an exact projection agree to $10^{-14}$.
- **Momentum identity.** It holds to $\le1.1\times10^{-5}$ on 33 points. It fails on three under-resolved grids (N14 and N28 at $z/z_{\rm wb}=1.5$; N20 at $z/z_{\rm wb}=2$, by 19%). Those points are flagged and excluded from the fits.
- **Independent solver.** FastDifferentiableMMNLO (run `2026-10-10-claude-b.6-solver-nd-check`, subagent claude-b.6, blind and frozen before comparison) reproduces the oracle's filtered $F$ for two binary filters and two intervals to $\le1.4\times10^{-6}$.

**Results.** All numbers in `runs/2026-10-10-claude-b-nd-oracle/summary.json`. Selected rows:

| point | $\Phi$ | $N^2\lambda_{\min}$ | $\Lambda(Z)$ | err | $N^2\lambda_{\rm pass}$ | $\Pi(Z)$ | $N^2\lambda_{\rm gen}$ | $N^2F_{\rm cen}$ | best binary (photon fraction) |
|---|---|---|---|---|---|---|---|---|---|
| N10, 0.7 | 7.5 | 0.8571 | 0.8707 | −1.56% | 2.114 | 2.191 | 3.339 | 3.520 | 0.4513 (0.43) |
| N20, 0.7 | 14.8 | 0.8724 | 0.8759 | −0.40% | 2.178 | 2.198 | 3.452 | 3.659 | 0.3403 (0.43) |
| N40, 0.7 (held out) | 29.6 | 0.8763 | 0.8772 | −0.10% | 2.195 | 2.200 | 3.534 | 3.696 | 0.2434 (0.39) |
| N40, 1.0 (held out) | 42.4 | 0.5464 | 0.5467 | −0.06% | 1.722 | 1.725 | 2.343 | 2.397 | 0.2440 (0.45) |
| N20, 1.5 | 31.8 | 0.3395 | 0.3400 | −0.15% | 1.378 | 1.398 | 1.568 | 1.600 | 0.4212 (0.54) |
| N10, 2.0 | 21.3 | 0.2512 | 0.2519 | −0.27% | 1.163 | 1.196 | 1.235 | 1.245 | 0.4680 (0.61) |
| N10, 3.0 | 31.9 | 0.1753 | 0.1754 | −0.06% | 0.968 | 0.985 | 0.991 | 0.998 | 0.4294 (0.56) |
| N10, 5.0 | 53.2 | 0.1201 | 0.1200 | +0.04% | 0.815 | 0.824 | 0.829 | 0.851 | 0.3766 (stage 1 only) |
| N10, 9.0 | 95.8 | 0.0841 | 0.0840 | +0.13% | 0.718 | 0.725 | 0.727 | 0.774 | 0.3242 (stage 1 only) |

$\Lambda$ and $\Pi$ are from the $N=200$ reduced curve, and from the $N=50$ long curve for $Z>3.3$.

**Error exponents** of $\lambda_{\min}$ against $\Lambda(Z)/N^2$, resolved $N\ge10$:

| $z/z_{\rm wb}$ | 0.3 | 0.7 | 1.0 | 1.5 |
|---|---|---|---|---|
| exponent | −1.93 | −1.98 | −1.98 | −1.78 (two points) |
| fit points ($N$) | 10–28 | 10–40 | 10–40 | 10, 20 |

- **Size of the correction.** The error coefficient $c=(1-N^2\lambda_{\min}/\Lambda)\Phi^2$ is constant in $N$ before breaking: 0.47–0.52 at $Z=0.106$ (the dispersionless value is $1/2$), 0.59–0.63 at 0.32, 0.83–0.88 at 0.74, 1.04–1.09 at 1.06. After breaking it drifts with $N$ (1.30 → 1.52 at $Z=1.59$ from $N=5$ to 20).
- **$\lambda_{\rm pass}$** converges to $\Pi(Z)/N^2$ at the same rate before breaking (exponents −1.91, −1.97, −1.94). After breaking it is slower (−1.42 at 1.5): −2.7% at N10, $z/z_{\rm wb}=2$.

**Binary filters** (three search stages: `run_points.py`, `refine_binary.py`, `transfer_binary.py`).
- **Scaling.** The best filter found decreases as $N^{-0.47}$, $N^{-0.44}$, $N^{-0.36}$ at $z/z_{\rm wb}$ = 0.3, 0.7, 1.0.
- **Best single interval.** It increases with $N$ toward about 0.7–0.8 at $z/z_{\rm wb}$ = 0.7–1, and toward 1 at 0.3. The held-out extrapolation of the interval failed at $N=40$, $z/z_{\rm wb}=1$, so this trend is not understood.
- **Non-negative weights.** Projected gradient from 28 starts ends 0.3–4.7 dB below the best binary filter and 6–17.5 dB above $\lambda_{\rm gen}$.
- **Search outlier.** N14 at $z/z_{\rm wb}=0.3$ (0.714) did not improve in any stage. It is either a search failure or a real non-monotonicity in $N$.

**Few-detector signed readouts** (`few_detectors.json`).
- The centroid weight, quantized to $K$ = 4, 8, 16 equal-photon bands, gives $-7.7$, $-11.8$, $-15.7$ dB at N20, $z/z_{\rm wb}=0.7$, against $-4.7$ dB for the best binary filter and $-20.6$ dB for $\lambda_{\rm gen}$.
- At N40, $z/z_{\rm wb}=1$ the same readouts give $-2.4$, $-13.6$, $-16.9$ dB.
- A split detector ($K=2$) is above shot noise at five of six points.
- So the gap between binary filters and $\lambda_{\rm gen}$ is mostly recoverable with a modest number of signed detectors, but $K$ must grow with $N$.

### 5.1b Large-$N$ readouts (2026-10-11; run `2026-10-11-claude-b-nd-binary-theory`)

**Tool.** A discrete adjoint of the split-step map gives the spectral count covariance from one batched backward pass over the kept bins.
- It matches the finite-difference oracle to $2\times10^{-9}$ and is 15 times faster.
- It reaches $N=112$ ($N_t=4096$) in 7 minutes.

**Three tiers of readout** (`fig_scaling.png`, `summary.json`), at $z/z_{\rm wb}=0.7$ over $N$ = 20–112:

| readout | slope in $N$ | value at $N=112$ |
|---|---|---|
| signed weights ($\lambda_{\rm gen}$, the odd centroid mode) | $-1.97$ | $N^2\lambda_{\rm gen}=3.64$, converging toward $1/(2K)=3.70$ |
| non-negative weights (heuristic) | $-0.70$, last local $-1.29$ | 0.045 |
| $\lambda_{\rm even}$ and the parity bound | $-0.70$, last local $-1.34$ | 0.060 and 0.030 |
| best binary filter found | $-0.43$ ($F\approx1.24N^{-0.43}$) | 0.160 |

At $z/z_{\rm wb}=1.0$ ($N\le80$) the slopes are $-1.96$, $-1.08$, $-0.92$ and $-0.62$ for the same four tiers.

**Consequence.**
- The parity bracket for binary filters widens with $N$: 5.1 dB at $N=40$, 7.2 dB at $N=112$.
- At large $N$ the binary constraint itself separates binary filters from graded non-negative readouts: 5.5 dB at $N=112$.

**The even mode** (`fig_modes.png`).
- **Shape.** A broad positive weight with strong modulation locked to the central interference fringes.
- **Resolution.** Making the weights piecewise constant over a third of a fringe raises $\lambda_{\rm even}$ by about 1.6 times (`coarse_grain.json`).
- **Sign structure.** It is 92–99% non-negative by weight, yet clipping its small negative parts destroys the squeezing ($F$ 0.23–1.75). The cancellation is delicate.
- **Leading-order picture fails.** A leading-order picture with an $O(\varepsilon)$ fringe admixture is not borne out: the fringe-locked (rough) part carries 18–34% of the mode at every $N$.
- **Status.** No theory of the even sector or of the binary law is given here (tasks T-20261010-claude-b-04, -05).

### 5.2 Reduced curve (run `2026-10-10-claude-b-nd-semiclassical`)

**Method.** `lambda_curve.py` propagates $u_0\pm\eta H_m$ ($m<80$) once and reads $C_Z$ at every recorded $Z$.

**Convergence.**

| change | effect on $\Lambda$ | effect on $\Pi$ |
|---|---|---|
| step halved ($N=50$) | $\le5\times10^{-7}$ | $\le1.4\times10^{-6}$ |
| $N$ = 50 → 100, $Z=0.1$ | $1.5\times10^{-3}$ | $4.8\times10^{-3}$ |
| $N$ = 100 → 200, $Z=0.1$ | $3.8\times10^{-4}$ | $1.2\times10^{-3}$ |
| $N$ = 50 → 100, $Z\ge0.3$ | $\le4\times10^{-4}$ | $\le2\times10^{-3}$ |
| $N$ = 100 → 200, $Z\ge0.3$ | $\le1\times10^{-4}$ | $\le3\times10^{-4}$ |
| basis $M$ = 80 → 120, $Z=0.1$ | $1.2\times10^{-4}$ | — |

**Direct $\varepsilon=0$ check** (`hydro_direct.py`, `hydro_direct.json`).
- **Method.** Integrate the dispersionless Madelung equations ($\rho_Z+(\rho v)_\tau=0$, $v_Z+vv_\tau+\rho_\tau=0$, $\theta_Z+v^2/2+\rho=0$; pseudo-spectral, RK4) for the 80 Hermite amplitude perturbations. No NLSE is involved. Then take $\sigma_{1,2}$ of the map to $\sqrt\rho\,\delta\theta$.
- **Result.** $\Lambda$ = 27.2373, 7.45546, 3.63509, 1.570244, 0.862842, 0.587701 and $\Pi$ = 32.0327, 10.1862, 5.70723, 3.13171, 2.18007, 1.78620 at $Z$ = 0.1, 0.2, 0.3, 0.5, 0.75, 1.0. These are grid-converged to $10^{-9}$.
- **Comparison.** They differ from the $N=200$ NLSE curve by $+1.3\times10^{-4}$ at $Z=0.1$, falling to $\le10^{-5}$ for $Z\ge0.5$. That equals the $N\to\infty$ Richardson extrapolation of the $N$ = 100, 200 curves.
- **Conclusion.** The leading-order structure is confirmed: $\Lambda$ is the linearized dispersionless hydrodynamics. The method is limited to $Z\le1$, before the gradient catastrophe.

**Small-$Z$ coefficients.** Extrapolating $(4Z^2\Lambda-1)/Z$ to $Z=0$ on the $N=200$ curve (degree 2–3, $0.1\le Z\le0.3$–0.4) gives 0.8159, against the derived $2/\sqrt6=0.8165$. The same for $\Pi$ gives 2.44–2.50, against $\sqrt6=2.449$, the first excited oscillator level.

**After breaking.** The amplitude block grows with $N$ ($\sigma_1(A)$ = 2.5 → 3.0 from $N$ = 50 to 100 at $Z\ge2$; 3.5 → 6.2 at $Z=1.6$), while $\Lambda$ and $\Pi$ do not.

**Reading.** The dispersive shock waves carry large amplitude responses, but the squeezed modes live in the smooth centre. So no Whitham-modulation treatment is needed for $\lambda_{\min}$ or $\lambda_{\rm pass}$ up to $Z=3.3$ ($z/z_{\rm wb}\approx3.1$). Within this range the leading order has not been seen to fail.

### 5.2a Far after breaking, and convergence

**Long reduced curve** (`curve_N50_long.json`: $N=50$, 80 $T_0$ window, $Z\le10$).
- It agrees with the 40 $T_0$ curve to $10^{-9}$ where they overlap.
- $\Lambda$ falls smoothly to 0.1252 at $Z=5$ and 0.0821 at $Z=10$.
- At $Z=10$, $4Z^2\Lambda=32.8$: dispersion has raised the best quadrature variance 33-fold above the dispersionless $1/(4\Phi^2)$.
- $\Pi$ and $1/(2K)$ approach each other at large $Z$ (0.720 and 0.777 at $Z=10$). So the passive limit, the weighted-counting limit and the centroid readout merge far after breaking, while $\lambda_{\min}$ stays 9.4 dB below them.

**Oracle far after breaking** (N10 at $z/z_{\rm wb}=5$, $Z=5.32$, $N_t=1024$ over 100 $T_0$).
- At $z/z_{\rm wb}=5$ ($Z=5.32$, $\Phi=53$): $N^2\lambda_{\min}=0.1201$ against $\Lambda=0.1200$, an error of $+0.04\%$.
- At $z/z_{\rm wb}=9$ ($Z=9.58$, $\Phi=96$, run time 21 min): $N^2\lambda_{\min}=0.0841$ against $0.0840$, an error of $+0.13\%$.
- Both points pass the momentum check. Within $Z\le9.6$, i.e. up to 9 $z_{\rm wb}$, I found no place where the leading order fails.
- At these points the best binary filter found is 0.377 and 0.324, and $\lambda_{\rm gen}$ is 16.5 dB below it.

**Convergence** (run `2026-10-10-claude-b-nd-convergence`).

| change at N10, $z/z_{\rm wb}=0.7$ | effect on the $\lambda$'s | effect on the best binary |
|---|---|---|
| $N_t$ doubled at fixed window | $\le5\times10^{-9}$ | none |
| window doubled (bins halved) | $\le6\times10^{-9}$ | $-0.17\%$ |
| step halved | 1–2$\times10^{-6}$ | — |

- At N20 with $N_t=2048$ over 80 $T_0$, the $\lambda$'s change by $\le1.2\times10^{-8}$ and the best binary by $-0.55\%$.
- $\lambda_{\rm pass}=\lambda_2$ to $\le10^{-12}$ at all four points.

### 5.2b Cross-check on the passive parabola (run `2026-10-10-claude-b-nd-parabola`)

**Closed form from claude-a's propagator.** From statement (a) of C-20261004-claude-a-01, the amplitude-to-phase element of Legendre block $l$ is $m_l(\mu)=P_l(0)Q_l(\mu)-Q_l(0)P_l(\mu)$. This uses the Ferrers functions, whose Wronskian at 0 is 1.
- Check: $m_0=\theta$ (Kerr), $m_2=-Q_2/2$, $|m_1|=\mu$.
- In the quadrature norms, $n=2\sqrt{1-\xi^2}X_0$ and $\|\tilde Y\|^2=\int(1-\xi^2)p^2$.
- So $\sigma_k(C)^2$ are the eigenvalues of $K^{\mathsf T}DGDK$, with $D=\mathrm{diag}(m_l)$, $G_{lk}=\int(1-\xi^2)P_lP_k$ and $K_{lj}=(2l+1)\int\sqrt{1-\xi^2}\phi_jP_l$.
- This gives $4\zeta^2\Lambda_{\rm par}$ = 1.091, 1.263, 1.640, 2.674, 5.523 and 17.11 at $\zeta$ = 0.1, 0.25, 0.5, 1, 2 and 4.737. The top singular vector is even and the second is odd at every $\zeta$.

**Comparison with the reduced numerics on $u_0=\sqrt{\max(1-\tau^2,0)}$.**
- **$\Lambda$.** Agreement to $\le0.11\%$ for $\zeta\le2$ at $N=100$. The small-$\zeta$ deviation shrinks from $N=50$ to 100.
- **$\Pi$.** Agreement to 0.06% for $\zeta\le0.5$. The excess is 0.54% at $\zeta=1$ and 1.9% at $\zeta=2$ with $M=80$; with $M=240$ it is 0.32% and 0.88%.
- **Reading.** The remaining differences are slow Hermite-basis convergence at the square-root edge.

### 5.2c Root-01 anchors (run `2026-10-10-claude-b-nd-anchor-map`)

| anchor | Gaussian bandpass | registered $F$ | best binary | $\lambda_{\rm gen}$ |
|---|---|---|---|---|
| 0.25 m ($N=4.26$, $\Phi=1.36$) | 0.864 | 0.925 | 0.790 | 0.377 |
| 1 m ($N=3.15$, $\Phi=2.97$) | 0.721 | 0.834 | 0.639 | 0.202 |

Both points are below this note's regime, and the anchors use a measured non-Gaussian spectrum with Raman.

### 5.3 Self-steepening and Raman

**Self-steepening, oracle.** At $s$ = 0.0082 and 0.0164 ($sN$ = 0.082, 0.164) at N10, $z/z_{\rm wb}=0.7$:

| quantity | change at $sN=0.082$ | change at $sN=0.164$ |
|---|---|---|
| $N^2\lambda_{\min}$ | +0.06% | +0.39% |
| $\lambda_{\rm gen}$ | +0.1% | +0.5% |

- **Binary filter found.** It moves by at most 0.013 (search noise is of the same size).
- **Parity.** $(\tau,s)\to(-\tau,-s)$ is a symmetry, so the eigenvalues are even in $s$. The two points are consistent with a small even dependence but do not isolate the $s^2$ law.

**Solver, physical fibre** ($T_0=100$ fs, 1550 nm, $N=10$, $z=0.7z_{\rm wb}$, run `2026-10-10-claude-b.6-solver-nd-check`). All values are for the oracle's filter orientation (the "mirror" column there).

| filter | Kerr only | self-steepening | + deterministic Raman | + Raman reservoir, 300 K |
|---|---|---|---|---|
| binary | 0.451 | 0.461 | 0.466 | 0.504 |
| interval | 0.727 | 0.755 | 0.794 | 0.905 |

- **Units.** Photon-energy weighting alone moves $F$ by up to 0.018.
- **Raman model.** Agarwal–Raman with $f_R=0.18$; symmetrized coth reservoir spectrum, $\mathrm{d}t\to0$ extrapolated.
- **Reservoir size.** The Raman reservoir adds 0.038 to the binary filter's $F$ and 0.11 to the interval's.

**Weighted readouts with Raman, solver** (run `2026-10-10-claude-b.6-solver-weighted-raman`).
- **Kerr only.** The centroid identity holds to $2\times10^{-12}$.
- **Raman, N10 at $z/z_{\rm wb}=0.7$, $T_0=100$ fs, 300 K:**

| readout | Kerr only | with Raman |
|---|---|---|
| centroid | 0.0352 | 0.0733 |
| $\lambda_{\rm gen}$ eigenvector | 0.0334 | 0.0719 |
| best binary | 0.451 | 0.491 |

- **Split of the centroid's increase.** Deterministic Raman contributes $+0.0023$ (it breaks momentum conservation); the reservoir contributes $+0.0358$.
- **Reading.** At this pulse width the Raman reservoir already sets a floor comparable to the Kerr value of weighted counting. It matters much less for binary filters, whose $F$ is an order of magnitude higher.

**Raman reservoir on the bounds** (run `2026-10-10-claude-b-nd-raman`).
- **Method.** The numpy oracle with the reservoir added as phase noise. In shot-noise units the noise added over $d\xi$ is $4N^2ERE^{\mathsf T}d\xi$, where $E$ holds the local phase directions times $|u|$ and $R$ is the circulant of $\hat c(\Omega)=|\mathrm{Im}\,h_R(\Omega/T_0)|\coth(\hbar\Omega/2k_BTT_0)$. Then $V=J(I+W)J^{\mathsf T}$. $\hbar$ and the photon number drop out, so only $N$, $Z$, $T_0$ and the temperature enter.
- **Validation.** Against the solver, the reservoir part of the centroid and $\lambda_{\rm gen}$-eigenvector readouts agrees to 0.4% (N10) and 0.3–1.6% (N20).
- **Result.** $\lambda_{\min}$ rises 2.1–5.8 times at seven points ($N$ = 5–20, $z/z_{\rm wb}$ = 0.3–1.5). The excess is $\Delta\lambda_{\min}\approx\rho(Z)\hat c(0)/\Phi$, with $\hat c(0)=4af_Rk_BT/[\hbar(a^2+b^2)]=0.114$ at 300 K.
- **The factor $\rho$.** It is about 1.1 at $Z=0.32$, 1.3 at 0.75 and 1.9 at 1.6; at fixed $Z$ it is nearly independent of $N$.
- **Estimate behind it.** The dispersionless estimate (squeezed-quadrature phase weight $1/(2\Phi)$ times the accumulated phase noise $4\Phi\hat c$) gives $\hat c/\Phi$, i.e. $\rho=1$. The growth of $\rho$ with $Z$ is not derived; possible sources are the dispersive mixing of injected phase noise into amplitude, and $\hat c(\Omega)$ rising toward the Raman peak.
- **Crossover.** The Raman term beats the Kerr term $\Lambda/N^2$ once $\Phi\gtrsim4Z^2\Lambda/(5\hat c(0))\approx3$ at $Z=0.74$.
- **Other bounds.** $N^2\Delta\lambda/\Phi$ is $N$-independent at fixed $Z$: 0.27, 0.38, 0.46 and 0.46 for $\lambda_{\min}$, $\lambda_{\rm pass}$, $\lambda_{\rm gen}$ and the centroid at $Z=0.74$ ($T_0=1$ ps).

**Conjecture (not tested beyond these points).**
- $\rho(Z)\approx\sqrt{4Z^2\Lambda(Z)}$. The comparison is 0.99 (N10) to 1.17 (N20, 100 fs) against 1.15 at $Z=0.32$; 1.18 → 1.32 ($N$ = 5 → 20, 1 ps), rising with $N$, against 1.39 at $Z=0.75$; and 1.85 against 1.86 at $Z=1.6$.
- If it holds, $\lambda_{\min}\approx\Lambda/N^2+2\hat c(0)\sqrt\Lambda/N=(\sqrt\Lambda/N)(\sqrt\Lambda/N+2\hat c(0))$.

**Raman scaling (estimate, superseded by the numbers above).**
- The reservoir injects phase noise along the fibre. In the hydrodynamic scaling the squeezed functional has phase weight $O(\varepsilon)$, so a phase-noise variance $\sigma_R^2$ (photon units) adds $O(\varepsilon^2\sigma_R^2)$ to $\lambda_{\min}$.
- $\sigma_R^2$ accumulated over the fibre grows like $\Phi\,f_R\,(\bar n_{\rm th}+\tfrac12)\,g(T_0)$, with $g$ the overlap of the pulse spectrum with the Raman gain.
- So the Raman floor in $N^2\lambda_{\min}$ grows like $\Phi$, and it overtakes $\Lambda(Z)$ once $\Phi f_R(\bar n_{\rm th}+\tfrac12)g\gtrsim\Lambda(Z)$.
- No run computes $\lambda_{\min}$ with the reservoir yet; that is a loose end.
