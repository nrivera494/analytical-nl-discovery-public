---
agent: claude-interactive.13
model: claude-opus-5-5
family: claude
claim: C-20261019-pi-chatgpt-02
task: T-20261019-claude-interactive-03
date: 2026-10-19
status: complete
verdict: pass
---

# Cross-family verification of C-20261019-pi-chatgpt-02 (similariton matched LO: phase growth, short-gain squeezing, large-gain floor)

**Status of this file.** Parts 1 and 2 were written and committed before any of the proposer's material was opened. Read before that commit: the claim card, C-20261008-claude-a-01, C-20261008-claude-a-02 (model and notation), P-001, AGENTS.md, `docs/AUDIT_PROTOCOL.md`, `runs/README.md` and `scripts/validate.py`. Not read before that commit: run `2026-10-18-pi-chatgpt-independent-verification` (report, `archive/similariton/`), `docs/review-2026-10-18-pi-chatgpt-*`, run `2026-10-19-claude-interactive-gpt6pro-quick-repro`, `claims/notes/C-20261008-claude-a-derivation.md`, and every log entry. All numbers are from run [`2026-10-19-claude-interactive.13-similariton-lo-verification`](../../runs/2026-10-19-claude-interactive.13-similariton-lo-verification/) (`summary.json`), computed with two codes I wrote for this run. No repository solver was used.

## Verdict

**Pass.** (i), (ii) and (iii) hold as stated in the stated regime. No blocker. One boundary correction to the wording of (ii) and two scope notes follow.

| Part | Prediction | Measured (this run) |
|---|---|---|
| (i) source | power of $\varepsilon_0^2C_{PP}$ over $12\le\tau\le26$, $\Gamma=\sqrt{18}$, asymptotic seed, $n_{sp}=1$: 2.3335 (7/3) | 2.33350 (least squares); 2.333333 over 26–40; equal-phase pairs over 40–80: 2.3333333–2.3333334 |
| (i) held out | $\Gamma=1$: ratio $C_{PP}/[(32n_{sp}/9)G\Phi_{NL}^2]\to1$, power $\to7/3$ | ratio in [0.99981, 1.00130] over 12–26 and in $1\pm3\times10^{-7}$ over 40–80; power 2.33175 (12–26), 2.333314 (26–40), 2.3333331–2.3333334 (equal phase, 40–80) |
| (ii) source | $\lambda_{\rm LO}=0.8964864655$ (smoothed parabola, $\varepsilon_0=0.05$, $\Gamma=\sqrt{18}$, $n_{sp}=1$, $\tau=0.02$) | 0.8965069620 with my smoothing and the asymptotic chirp; 0.8960636575 unchirped. On the source's launch (read in Part 3): 0.8964864646–0.8964864653, i.e. reproduced to $10^{-9}$ |
| (ii) held out | $n_{sp}=2$: sign change at $\gamma P_0/g=5/2$ (parabola), $2\sqrt2$ (Gaussian) | Gaussian 2.828427; smoothed parabola $2/\kappa_\delta$ = 2.50699 ($\delta=0.05$), 2.50030 ($\delta=0.01$), 2.500076 ($\delta=0.005$), converging to 5/2 as $\delta^{1.98}$. Root of the measured slope within $3.3\times10^{-9}$ of $R=1$ in all six shape/chirp/$n_{sp}$ cases |
| (iii) source | $\lambda_{\rm LO}\simeq3.159$ at $\tau=4$, $\varepsilon_0=0.05$ (full field) | 3.16133 ($\delta=0.05$), 3.16303 ($\delta=0.02$), converged to $10^{-6}$; on the source's launch 3.1592357 (source 3.1592358) |
| (iii) held out | $G^{-1/3}\lambda_{\min}(C_{\rm LO})$ bounded above and away from 0 over 12–26 | [0.338, 0.633] ($\Gamma=\sqrt{18}$ asymptotic, $n_{sp}=1$); [0.935, 1.534] ($n_{sp}=2$); [0.247, 0.797] ($\Gamma=1$ unchirped); same bounds over 26–80 |

**Correction to (ii), not a blocker.** The first-order slope is exactly as claimed, so "squeezed at short length if $R>1$, not if $R<1$" holds, with $R=\gamma\int P^2/(n_{sp}g\int P)$. At $R=1$ the slope vanishes and the $(gz)^2$ term decides. For a frequency-flat amplifier and negligible dispersion that term is $2\,\mathrm{Var}_P(\gamma P/g)-n_{sp}$. It is negative for both shapes at $n_{sp}=1,2$, measured in the full field: $-0.852$, $-1.407$ (parabola), $-0.691$, $-0.762$ (Gaussian), equal to the formula to four digits. So the matched mode is squeezed at $R=1$ too, and the literal "only if $R>1$" fails on the boundary. Suggested wording: "squeezed at short length if $R>1$; not squeezed at short length if $R<1$."

**Scope notes.**
1. *(i) converges slowly.* The ratio $C_{PP}/[(32n_{sp}/9)G\Phi_{NL}^2]$ approaches 1 as $1+O(G^{-1/3})$, oscillating in $\ln G$. The measured exponent of the error envelope is $-0.334$ ($\Gamma=\sqrt{18}$) and $-0.332$ ($\Gamma=1$), against $-1/3$ from my derivation (the $p_0$–$p_2$ cross-covariance below). At $\tau\le8$ (gain up to 35 dB) the ratio is 0.86–1.11 and the local power 2.19–2.90, so the $G^{7/3}$ law is an asymptotic statement. The card's "prefactors oscillate in $\ln G$" covers this. I would add the rate.
2. *Bright field.* The large-gain window is outside the linearized regime for any realistic seed. At $\varepsilon_0=0.05$ ($\Gamma=\sqrt{18}$, asymptotic seed), $\Phi_{NL}^2=8.97\times10^3$, $4.44\times10^8$ and $5.68\times10^{16}$ at $\tau=4$, 12 and 26. For the energetic seed of C-20261008-claude-a-01 ($N_0=2.6\times10^9$), $\Phi_{NL}^2/N_0=3.4\times10^{-6}$, 0.17 and $2\times10^7$. The card states this restriction. (i) and (iii) are properties of the linearized model above $\tau\approx12$. The short-gain squeezing of (ii) is deep in the bright-field regime: $\Phi_{NL}^2=0.009$ at $\tau=0.02$.

3. *Linearization of (ii).* A truncated-Wigner simulation (nonlinear, stochastic) reproduces the linearized $\lambda_{\rm LO}$ within $1\sigma$ at $N_0=10^6$ ($\tau=0.3$, $-3.3$ dB with full ASE). At $N_0\le10^4$ it shows less squeezing, scaling as $1/N_0$, which I have not separated from the method's own validity limit (2e). The card's $\Phi_{NL}^2/N_0\ll1$ may not be sufficient for strongly squeezed variances.
4. *Beyond the claim.* The matched mode is squeezed at some finite length already for $R>R_{\min}<1$: 0.78 (parabola) and 0.90 (Gaussian) at $n_{sp}=1$, from a closed-form dispersionless model checked against the full field (Part 4, 2f).

5. *Lab relevance of (ii)* (my arithmetic, with the parameters of C-20261008-claude-a-01: $\beta_2=25$ ps²/km, $\gamma=5$ W⁻¹km⁻¹).
   - Its energetic parabolic seed (3 ps, 500 pJ, $P_0=125$ W, $g=0.2$ m⁻¹, $N_0=2.6\times10^9$) has $\gamma P_0/g=3.1$, so $R=2.5/n_{sp}$. Its matched mode is squeezed at short length for any $n_{sp}<2.5$, deep in the bright-field regime.
   - Its typical short seed (0.2 ps, 10 pJ, $g=1.9$ m⁻¹) has $\gamma P_0/g=0.10$, far below even the finite-length threshold, so no squeezing is predicted.
   - Detection loss and LO mode mismatch are not included.

**Regime I sign off on.**
- (i), (iii): the reduced leading-order hydrodynamic model with intensity-quadrature noise, $0.5\le\Gamma\le10$ (tested at 0.5, 1, 2, $\sqrt{18}$, 10), parabolic seeds with $a(0)=1$ and $a'(0)\in\{0,\Gamma/3\}$, $n_{sp}\in\{1,2\}$, $\tau\ge12$ for the 1% level, tested to $\tau=80$. In the full field the reduced model is reached as $\varepsilon_0\to0$ at fixed $\tau\le4$ (Part 2c). Linearization requires $\Phi_{NL}^2/N_0\ll1$.
- (ii): any smooth coherent mean, frequency-flat gain, any dispersion, as $z\to0^+$, with the boundary wording above. Tested on smoothed parabolas (four smoothings, two chirps) and a Gaussian, $n_{sp}=1,2$, $R\in[0.5,2]$.

## Part 1. Independent derivation

### Restatement and assumptions

Normalized model of C-20261008-claude-a-01: $x=T/T_0$, $\zeta=z/\sqrt{L_DL_{NL}}$, $\varepsilon_0=\sqrt{L_{NL}/L_D}$, $\Gamma=g\sqrt{L_DL_{NL}}$, so
$$\partial_\zeta\psi=-\tfrac{i\varepsilon_0}{2}\psi_{xx}+\tfrac{i}{\varepsilon_0}|\psi|^2\psi+\tfrac\Gamma2\psi,\qquad \tau=\Gamma\zeta=gz=\ln G,\qquad \gamma P_0/g=1/(\varepsilon_0\Gamma).$$
Quadratures have vacuum covariance $I$; $X_A=2\langle u,b\rangle$ and $P_{\rm LO}=2\langle iu,b\rangle$ with $u=\bar\psi(z)/\|\bar\psi(z)\|$ and $\langle w,b\rangle={\rm Re}\sum w^*b$.

Assumptions as listed on the card, plus three that the card does not list:
- (i)/(iii) use only intensity-quadrature noise at leading order. Input-vacuum and ASE phase-quadrature noise is dropped, as in C-20261008-claude-a-02 assumption 5. For the sharp parabola its Legendre projections are log-divergent at the edges.
- (ii) needs the gain to be phase-insensitive and frequency-flat at $z=0$; dispersion may be anything.
- (ii) is a first-order statement. The boundary $R=1$ needs the second-order term (above).

### (ii): the initial slope

At $z=0$ the state is coherent, $C(0)=I$ in every mode. For linear dynamics $\dot y=Sy+\dot\nu$ with symmetric diffusion $D$, $\dot C(0)=S+S^T+D$.
- Dispersion, $-\tfrac{i\beta_2}{2}\partial_t^2$, is anti-Hermitian, hence antisymmetric as a real operator. It contributes 0.
- Kerr: $\delta\dot A=i\gamma(2|\bar A|^2\delta A+\bar A^2\delta A^*)$. The first term is a local rotation (antisymmetric). In the frame of the local mean phase the second is $\dot x=\gamma Pp$, $\dot p=\gamma Px$, which contributes $2\gamma P(t)\sigma_x$.
- Gain drift plus ASE contribute $gI+g(2n_{sp}-1)I=2n_{sp}gI$.

The LO basis $E(z)=[e_X,e_P]$ moves with the mean field, but $E^TE=I$ and $C(0)=I$ give $\tfrac{d}{dz}(E^TCE)|_0=E^T\dot C(0)E$. In the local frame $e_X=(|u|,0)$ and $e_P=(0,|u|)$, so
$$\dot C_{\rm LO}(0)=\begin{pmatrix}2n_{sp}g&2\gamma\kappa\\2\gamma\kappa&2n_{sp}g\end{pmatrix},\qquad \kappa=\int|u|^2P=\frac{\int P^2}{\int P},$$
and $\lambda_{\rm LO}=1+z(2n_{sp}g-2\gamma\kappa)+O(z^2)$. This is the claimed formula. The C(0) eigenvalue is double, but the $2\times2$ perturbation splits it at first order ($\pm2\gamma\kappa$), so $\lambda_{\min}$ is analytic for $z>0$. For the parabola $\kappa=\tfrac45P_0$; for $P_0e^{-t^2/T_0^2}$, $\kappa=P_0/\sqrt2$.

**Second order at $R=1$** (dispersionless, unchirped; each time slot independent). In a slot, $\dot C_t=A_tC_t+C_tA_t^T+(2n_{sp}-1)g$ with $A_t=\tfrac g2+K_t$ and $K_t=\begin{pmatrix}0&0\\2\gamma P_te^{gz}&0\end{pmatrix}$, and $C_{\rm LO}=\int|u|^2C_t$. The Kerr rate grows with the amplified power. Expanding to $(gz)^2$ along the soft eigenvector $(1,-1)/\sqrt2$, with $k=\gamma P/g$ and $\bar k=n_{sp}$:
$$\lambda_{\rm LO}=1+\big[2\,\mathrm{Var}_P(k)-n_{sp}\big](gz)^2+O(z^3).$$
The $-n_{sp}$ is the growth term. With a constant Kerr rate it cancels and the coefficient is $+2\mathrm{Var}_P(k)$. I checked that against an exact single-mode solution, and it was my first, wrong, expectation for the full field. The full field confirms the growth term.

### (i) and (iii): reduced model

Madelung ($\psi=\sqrt\rho e^{iS/\varepsilon_0}$, $v=-S_x$) gives $\rho_\zeta+(\rho v)_x=\Gamma\rho$ and $v_\zeta+vv_x=-\rho_x+O(\varepsilon_0^2)$. The parabola $\rho=\rho_0(1-x^2/a^2)$, $v=(a'/a)x$, has $\rho_0=e^{\Gamma\zeta}/a$ and $a''=2e^{\Gamma\zeta}/a^2$. Linearizing with $\delta\rho=\rho_0n(\xi)$, $\delta S=\varepsilon_0p(\xi)$ and $\xi=x/a$ separates in Legendre polynomials: $p_l'=\rho_0q_l$, $q_l'=-l(l+1)p_l/a^2$, with $q_l=n_l/\varepsilon_0$. This rederives C-20261008-claude-a-02 (a).

Noise enters through the intensity quadrature, $\delta\rho=\sqrt\rho\,x_q$. Per unit $\tau$ it adds
$$\frac{d}{d\tau}\big[N_0\varepsilon_0^2\,\mathrm{Cov}(q_l,q_m)\big]=\tfrac13(2l+1)(2m+1)B_{lm}(2n_{sp}-1)e^{-\tau},\qquad B_{lm}=\int_{-1}^1(1-\xi^2)P_lP_m,$$
with the same matrix (factor 1) at $\tau=0$ from the input vacuum.

The matched LO needs only $l=0,2$:
- $X_A=\tfrac32\varepsilon_0\sqrt N q_0$ and $P_{\rm LO}=2\sqrt N\bar p$, with $\bar p=p_0-p_2/5$ (the intensity weights of $P_0,P_2$ are $1,-1/5$);
- so $C_{AA}=\tfrac94G\tilde S_{q_0q_0}$, $\varepsilon_0C_{AP}=3G\tilde S_{q_0\bar p}$ and $\varepsilon_0^2C_{PP}=4G\tilde S_{\bar p\bar p}$, where $\tilde S=N_0\varepsilon_0^2\,\mathrm{Cov}$;
- $C_{AA}$ comes out as $2n_{sp}G-(2n_{sp}-1)$ exactly.

Writing $p_0=\theta q_0+r_0$ with $dr_0=-\theta\,dW_0$ (where $\theta=\varepsilon_0\Phi_{NL}$) carries the energy-locked part exactly.

*(i).* $\tilde S_{p_0p_0}\to\tfrac89n_{sp}\theta^2$, so $C_{PP}\to\tfrac{32n_{sp}}9G\Phi_{NL}^2$. Two corrections:
- $\mathrm{Cov}(p_0,p_2)$ is nonzero because $B_{02}=-\tfrac4{15}$. The $l=2$ response to an early kick is $\propto e^{\tau/3}\sin(\tfrac{\sqrt2}3(\tau-\tau'))$, so the cross term is $\Theta(G)$ against $\Theta(G^{4/3})$: a relative $O(G^{-1/3})$ correction with log-gain period $2\pi/(\sqrt2/3)=13.33$.
- $\mathrm{Var}(p_2)$ is $O(G^{2/3})$, a relative $O(G^{-2/3})$ correction.

*(iii).* $\lambda_{\min}=\det C_{\rm LO}/\lambda_{\max}\to C_{AA}\,\mathrm{Var}(\bar p\,|\,q_0)/\mathrm{Var}(\bar p)$. Here $\mathrm{Var}(\bar p|q_0)\simeq\mathrm{Var}(p_2|\cdot)/25=\Theta(G^{2/3})$, a positive-definite quadratic form in $(\cos,\sin)$ of $\tfrac{\sqrt2}3\tau$. The residual $\int\theta\,dW_0$ is $O(G^{1/3})$. So $\lambda_{\min}=\Theta(G\cdot G^{2/3}/G^{4/3})=\Theta(G^{1/3})$, independent of $\varepsilon_0$ at leading order.

## Part 2. Independent numerics

### 2a. Reduced model (`reduced.py`, `reduced_analysis.py`)

- ODEs in $\tau$ for $a$, $\theta$ and the $4\times4$ covariance of $(q_0,r_0,p_2,q_2)$. Input and ASE parts are separate. DOP853, rtol $10^{-12}$, output every 0.005 to $\tau=80$.
- Changing rtol from $10^{-9}$ to $10^{-13}$ changes the fitted power by $10^{-14}$ and $G^{-1/3}\lambda_{\min}$ by $2\times10^{-10}$. $C_{AA}$ matches its exact formula to $7\times10^{-15}$.
- **Check against the parent card.** At $\Gamma=\sqrt{18}$, unchirped, $\tau=2,4,6$, the code gives $\varepsilon_0^2C_{PP}/G$ = (3.80927, 2.25792), (61.8132, 55.3166), (700.903, 685.280) and $1-r^2$ = 0.0743628, 0.0125054, 0.00435594. Those are C-20261008-claude-a-02 P4 to every quoted digit, and $a_L$, $\theta_L$ match its P1. The parent card's own table grows like $G^{4/3}$, not $G^0$, in $\varepsilon_0^2C_{PP}/G$, as the claim says.
- **(i), power and prefactor.**

| case ($n_{sp}=1$) | LS power 12–26 | LS power 26–40 | equal-phase power, pairs 13.33 apart in 40–80 | ratio range 12–26 | error-envelope exponent |
|---|---|---|---|---|---|
| $\Gamma=\sqrt{18}$, asymptotic | 2.33350 | 2.333333 | 2.3333333–2.3333334 | [0.9904, 1.0023] | −0.334 |
| $\Gamma=\sqrt{18}$, unchirped | 2.33355 | 2.333331 | 2.3333333–2.3333334 | [0.99955, 1.0039] | −0.333 |
| $\Gamma=1$, unchirped (held out) | 2.33175 | 2.333314 | 2.3333331–2.3333334 | [0.99981, 1.0013] | −0.332 |
| $\Gamma=1$, chirp $\Gamma/3$ | 2.33182 | 2.333315 | 2.3333331–2.3333334 | [0.99896, 1.0011] | −0.332 |

At $n_{sp}=2$ the powers are 2.33360, 2.33362, 2.33190 and 2.33199 over 12–26, converging the same way. Equal-phase pairs inside 12–26 give 2.33379–2.33410 ($\Gamma=\sqrt{18}$ asymptotic). They are worse than the least-squares fit because they use the early end of the window, where the $G^{-1/3}$ term is largest. The local power over 12–26 ranges over [2.3327, 2.3401] ($\Gamma=\sqrt{18}$) and [2.3272, 2.3550] ($\Gamma=1$).
- **(iii).** $G^{-1/3}\lambda_{\min}$ ranges, $n_{sp}=1$ and 2, are in the verdict table. They are unchanged at $\varepsilon_0=0.05$ (exact $2\times2$ eigenvalue) and over $26\le\tau\le80$. The fitted power of $1-r^2$ over 12–26 is $-0.653$ ($\Gamma=\sqrt{18}$ asymptotic; C-20261008-claude-a-02 reports $-0.648$) and $-0.700$ ($\Gamma=1$), against $-2/3$ modulated by the $l=2$ oscillation.

- **Other $\Gamma$ (`reduced_gamma_scan.py`).** At $\Gamma=0.5$, 2 and 10, each with an unchirped and a $\Gamma/3$-chirped unit seed ($n_{sp}=1$):
  - power over 12–26 between 2.3309 and 2.3348, over 40–60 equal to 2.33333;
  - the ratio within $[0.978,1.005]$ over 12–26 and 1 to $10^{-5}$ over 40–60;
  - $G^{-1/3}\lambda_{\min}$ within $[0.170, 2.481]$ over 12–60. The range depends on $\Gamma$ and the seed, and is bounded above and away from zero in every case.

### 2b. Full field (`fullfield.py`, `ff_tests.py`, `slopes.py`, `explicit.py`)

- Linearized NLSE on a periodic grid, one discrete mode per point, both quadratures. Strang step: dispersion $\tfrac h2$, linear amplifier $\tfrac h2$, Kerr $h$, amplifier $\tfrac h2$, dispersion $\tfrac h2$. The Kerr tangent is the exact derivative of the exact Kerr substep, so it is symplectic.
- Each amplifier substep of power gain $G_h$ injects symmetric variance $(2n_{sp}-1)(G_h-1)$ and commutator $-(G_h-1)$: the complete reservoir.
- The $2\times2$ LO covariance and the commutator $[X_A,P_{\rm LO}]/2i$ come from an exact discrete adjoint of the two output functionals, with checkpointing.

Tests:
- **Kerr off.** $C_{\rm LO}=[2n_{sp}G-(2n_{sp}-1)]I$ to $8\times10^{-13}$ ($n_{sp}=1,2$, chirped smoothed parabola, $\tau=1$).
- **Passive, nearly dispersionless.** Gaussian, $\varepsilon_0=10^{-4}$: the slot-by-slot Kerr shear $C=[[1,\overline s],[\overline s,1+\overline{s^2}]]$ to $3\times10^{-6}$ relative.
- **Commutator.** Restored to $\le2\times10^{-14}$ in all slope runs and $\le4\times10^{-13}$ in the explicit case. Over every full-field run, the largest error is $1.6\times10^{-10}$ ($\tau=4$, 40000 steps). Without the reservoir term it equals $G$: 1.020201 at $\tau=0.02$, 2.718282 at $\tau=1$. So the reservoir restores it.
- **Uncertainty.** $\det C_{\rm LO}\ge1.084$ in every curve run.

Results:
- **Slopes (prediction 4).** $\lambda_{\rm LO}$ at $\tau=(0.5,1,2,3,4)\times10^{-3}$, fitting $(\lambda-1)/\tau=s+c\tau+d\tau^2$. Cases: smoothed parabola ($\delta=0.05$) unchirped and with the asymptotic chirp, and the Gaussian; $n_{sp}=1,2$; seven $R$ values each in $[0.5,2]$, with $\Gamma=\kappa/(n_{sp}\varepsilon_0R)$ at $\varepsilon_0=0.05$.
  - $\max|s-2n_{sp}(1-R)|\le7.1\times10^{-7}$; the root in $R$ is within $3.3\times10^{-9}$ of 1.
  - The slope does not move with $N$ (2048→4096), $L$ (8→12) or steps (60→240): 0.4000000011–0.4000000012 against 0.4.
  - At $\delta=0.01$ and $n_{sp}=2$ the slope changes sign between $\gamma P_0/g=2.50$ ($+4.84\times10^{-4}$) and 2.52 ($-3.15\times10^{-2}$). These match $4(1-R)$ to $10^{-8}$; the threshold there is 2.50030.
- **Explicit squeezed case with full ASE (prediction 3).** Smoothed parabola $\delta=0.05$, $\varepsilon_0=0.05$, $\Gamma=\sqrt{18}$, $n_{sp}=1$, $\tau=0.02$: $\lambda_{\rm LO}=0.8965069620$ (asymptotic chirp) and 0.8960636575 (unchirped). They are stable to $10^{-9}$ over $N=2048$–8192, $L=8$–12 and 200–800 steps, with $\det C=1.0844$. Gaussian with $n_{sp}=2$ at the same $\varepsilon_0$, $\Gamma$, $\tau$ ($R=1.667$): $\lambda_{\rm LO}=0.94978$.
- **Squeezing persists well beyond $z\to0^+$.** Same seed, $\Gamma=\sqrt{18}$, $n_{sp}=1$:
  - $\varepsilon_0=0.05$: $\lambda_{\rm LO}=0.384$ at $\tau=0.3$ ($-4.2$ dB), back to 1 near $\tau\approx1.6$;
  - $\varepsilon_0=0.025$: 0.258 at $\tau=0.2$ ($-5.9$ dB), back to 1 near $\tau\approx1.6$.

### 2c. Full field against the reduced model (`curve.py`, `eps_delta.py`); relaxed assumption for (i)/(iii)

The full field relaxes the hydrodynamic leading order, the sharp edge and the dropped phase-quadrature noise. Asymptotically chirped seed, $\Gamma=\sqrt{18}$, $n_{sp}=1$:

| $\tau$ | quantity | reduced ($\varepsilon_0\to0$) | $\varepsilon_0=0.05$, $\delta=0.05$ | $0.05$, $0.02$ | $0.025$, $0.05$ | $0.025$, $0.02$ |
|---|---|---|---|---|---|---|
| 2 | $\lambda_{\min}$ | 1.29617 | 1.33676 | 1.32571 | 1.31837 | 1.30650 |
| 2 | $\varepsilon_0^2C_{PP}/G$ | 3.80707 | 3.80565 | 3.81340 | 3.80126 | 3.80766 |
| 4 | $\lambda_{\min}$ | 3.03422 | 3.16133 | 3.16303 | 3.09248 | 3.07306 |
| 4 | $\varepsilon_0^2C_{PP}/G$ | 88.137 | 88.283 | 88.136 | 88.309 | 88.159 |

- The full-field $C_{AA}$ equals $2G-1$ to $10^{-11}$ relative.
- $\varepsilon_0^2C_{PP}/G$ agrees with the reduced model to 0.2% at every point, and to 0.03% at $\tau=4$ with $\delta=0.02$.
- $\lambda_{\min}$ approaches the reduced value as $\varepsilon_0$ and $\delta$ shrink, from 4.2% above to 1.3% above at $\tau=4$.
- The rate is not established. The two $\varepsilon_0$ values give apparent exponents from 0.9 to 1.7 depending on $\delta$ and $\tau$.
- At $\tau=4$, steps 2000→4000, $N$ 4096→8192 and $L$ 16→24 change $\lambda$ by $8\times10^{-7}$, $10^{-11}$ and $10^{-11}$.

### 2d. Attacks that did not break the claim

- Units and limits: $\gamma P/g$ is the only group in (ii). With Kerr off the matched mode is never squeezed (tested). At $g=0$, (ii) reduces to Kerr squeezing.
- Shape: two smoothings of the parabola edge, two chirps, a Gaussian. The criterion depends on the profile only through $\int P^2/\int P$, as claimed.
- Seed of (i)/(iii): two launch chirps at each $\Gamma$; the held-out $\Gamma=1$ approaches the asymptote from far away.
- Not done here: Raman, gain saturation, gain bandwidth (all excluded by the card), and an exact non-Gaussian quantum calculation (positive-P or few-mode exact). The truncated-Wigner check is 2e.

### 2e. Relaxing the linearization: truncated Wigner (`twa.py`; written before Part 3, results after)

- Nonlinear stochastic propagation of Wigner samples on the same grid and Strang scheme as `fullfield.py`, so splitting error cancels in the comparison:
  - Kerr in Wigner form $\psi	o\psi\exp[ih(|\psi|^2-\hbar/dx)/arepsilon_0]$;
  - exact amplifier substeps with Gaussian noise of variance $(2n_{sp}-1)(G_h-1)/4$ per quadrature;
  - coherent input with vacuum variance $1/4$ per quadrature.
- Setup: Gaussian seed, $arepsilon_0=0.05$, $\Gamma=\sqrt{18}$, $	au=0.3$, 256 grid modes, 100 steps, numpy seed 20261019. Errors are bootstrap standard deviations.

| $n_{sp}$ | $N_0$ | grid modes | trajectories | TWA $\lambda_{
m LO}$ | linearized |
|---|---|---|---|---|---|
| 1 | $10^6$ | 256 | $2	imes10^5$ | $0.4729\pm0.0013$ | 0.4729 |
| 2 | $10^6$ | 256 | $2	imes10^5$ | $0.7999\pm0.0024$ | 0.7978 |
| 1 | $10^4$ | 64 / 128 | $10^5$ | $0.4877\pm0.0024$ / $0.4915\pm0.0022$ | 0.4729 |
| 1 | $10^3$ | 64 / 128 / 256 | $10^5$ / $10^5$ / $2	imes10^5$ | 0.633 / 0.669 / $0.687\pm0.002$ | 0.4729 |

- At $N_0=10^6$ the nonlinear stochastic simulation reproduces the linearized squeezing within $1\sigma$. The sample covariance entries agree within 0.2–0.4% (about $1\sigma$).
- So the short-gain squeezing with full ASE of (ii) is not an artefact of linearization for bright pulses. Here $\Phi_{NL}pprox1.65$ rad and $\Phi_{NL}^2/N_0=2.7	imes10^{-6}$.
- At $N_0\le10^4$ TWA gives less squeezing: by 0.015–0.019 at $10^4$ and 0.16–0.21 at $10^3$, scaling as $1/N_0$ and growing with the number of grid modes. This is outside the claim's bright-field regime. It is also where truncated Wigner itself is unreliable (photon number not $\gg$ number of modes).
- I did not separate the physical non-Gaussian correction from the TWA artefact. Note that $\Phi_{NL}^2/N_0$ is only $2.7	imes10^{-4}$ at $N_0=10^4$. If even part of the shift is physical, the card's condition $\Phi_{NL}^2/N_0\ll1$ is not sufficient for percent accuracy of a strongly squeezed variance.

**Source launch at $	au=4$ (`source_seed.py`, after Part 3).** On the proposer's launch my code gives $\lambda_{
m LO}$ = 3.1592357140 ($arepsilon_0=0.05$; identical at $N=4096$ and 8192), 3.4107522440 ($arepsilon_0=0.1$) and 3.0741497740 ($arepsilon_0=0.025$). The source reports 3.159235825, 3.410751835 and 3.074149802: agreement to $1.2	imes10^{-7}$ relative. Prediction 5 is reproduced. Against the reduced value 3.03422 these are 4.1%, 12.4% and 1.3% high: with $\delta\proptoarepsilon_0^{2/3}$ the excess falls with an apparent exponent of about 1.6 in $arepsilon_0$. That is consistent with, but does not establish, $O(arepsilon_0^2\ln(1/arepsilon_0))$ (task T-20261019-claude-interactive.13-02).

### 2f. Finite-length squeezing below $R=1$, full field (`finite_length.py`; see Part 4)

$arepsilon_0=0.05$, $n_{sp}=1$, unchirped seeds, $	au\le2$; values are minima over the $	au$ grid.

| $R$ | 0.5 | 0.7 | 0.75 | 0.8 | 0.85 | 0.9 | 0.95 | 1.0 |
|---|---|---|---|---|---|---|---|---|
| parabola ($\delta=0.05$) | 1.049 | 1.028 | 1.023 | **0.992** ($	au=0.8$) | **0.948** | **0.910** ($	au=0.8$) | | |
| Gaussian | 1.049 | | | | 1.013 | 1.001 | **0.969** ($	au=0.5$) | **0.940** ($	au=0.5$) |

The thresholds lie in [0.75, 0.8] (parabola) and [0.90, 0.95] (Gaussian). The dispersionless slot model of Part 4 gives 0.781 and 0.902. Its minima at $R=0.9$ (parabola: 0.904 at $	au=0.84$) and $R=1$ (Gaussian: 0.939 at $	au=0.52$) match the full field (0.910, 0.940).

## Part 3. Proposer's material (read after the commit of Parts 1–2)

Read after commit 4ff455f: `archive/similariton/TECHNICAL_NOTES.md` (all), report sections 4.1–4.4 (`independent_verification_report.tex`, lines 285–391), `archive/similariton/analysis_summary.json`, and the run's `meta.yaml`. `twa.py` (2e) was written and started before this reading; `source_seed.py` was written after it.

**Derivations.**
- *(ii)* Report §4.3 and notes §5 give the same first-order argument as Part 1: zero symmetric dispersive part at vacuum, $2n_{sp}gI$ from gain plus ASE, and the Kerr shear weighted by $\int P^2/\int P$. It is correct. The source proves only the "if" direction ("a short positive-distance interval squeezes"); the card's "if and only if" is the filer's wording. Neither treats $R=1$. The second-order result in Part 1 is new relative to the source.
- *(i)* Notes §4 and report §4.2 match Part 1. The source names "oscillatory prefactors" but does not give the $O(G^{-1/3})$ correction from $\mathrm{Cov}(p_0,p_2)$; my measured exponent ($-0.334$) adds that.
- *(iii)* Same Schur-complement argument. Its regression residual $\mathrm{Var}R_0=O(G^{1/3}/\epsilon^2)$ agrees with mine.
- I found no error in these sections.

**Numbers: two independent codes.**
- *Reduced model.* Their finite-volume code and my Legendre code agree to a few parts in $10^6$:
  - fitted power of $\varepsilon_0^2C_{PP}$ over 12–26: 2.3335053 against 2.3334999;
  - $\varepsilon_0^2C_{PP}$ at $\tau=18$: $7.74098\times10^{17}$ against $7.74095\times10^{17}$;
  - $\theta(18)$ identical to 14 digits;
  - $1-r^2$ at $\tau=4,6,12,15,18,24$ (asymptotic launch) and $\tau=4,6$ ($\Gamma=1$ unchirped): agreement to 1.5–5$\times10^{-6}$ relative, within their 1024-cell discretization error.
- *Full field, source seed.* The notes (§7) specify the launch $|U|^2=c\,\delta\log[1+e^{(1-\xi^2)/\delta}]$, $\delta=0.25\varepsilon_0^{2/3}$, $c$ fixing energy $4/3$, with the asymptotic chirp. My full-field code on that launch (`source_seed.py`) gives $\lambda_{\rm LO}(\tau=0.02)$ = 0.8964864653, 0.8964864646 and 0.8964864644 on three grids. The source reports 0.8964864655. My $C_{\rm LO}$ = [[1.0404026801, 0.1560393898], [·, 1.065670259]] and det 1.0843779023 match theirs to $3\times10^{-10}$. So prediction 3 is reproduced, by a lab-frame code against their lens-coordinate code. The 2e-5 difference in Part 2 came entirely from the different smoothing.
- *Full field at $\tau=4$, source seed.* 3.1592357140 against 3.159235825 (prediction 5), and the source's $\varepsilon_0=0.1$, 0.025 values to $1.2\times10^{-7}$ (2e).

**Nothing in the proposer's material changes the verdict.** The $R=1$ boundary note and the $G^{-1/3}$ rate are additions; the source's counterexample also survives a nonlinear (truncated-Wigner) simulation at $N_0=10^6$ (2e).

## Part 4. Beyond the claim: squeezing at finite length below the short-length threshold

(ii) is a statement at $z\to0^+$. Because gain raises $\gamma\int P^2/\int P$ as $G$, $R<1$ does not rule out squeezing at a finite length. In the dispersionless slot model (Part 1, with the Kerr rate growing as $e^{gz}$) the matched-LO covariance has a closed form. Write $k=\gamma P/g$, $\bar k=\langle k\rangle_P=n_{sp}R$, $\overline{k^2}=\langle k^2\rangle_P$, $n=n_{sp}$ and $\ell=\ln G$:
$$C_{AA}=2nG-(2n-1),\qquad C_{AP}=2\bar kG\big[(G-1)+(2n-1)(G-1-\ell)\big],$$
$$C_{PP}=G+4\overline{k^2}G(G-1)^2+(2n-1)\big[(G-1)+4\overline{k^2}G(G^2-2G\ell-1)\big].$$
- It depends on the profile only through $v=\mathrm{Var}_P(P)/\langle P\rangle_P^2$: 0.1547 for a Gaussian, 0.0714 for a parabola.
- At $\varepsilon_0=0.005$ the full-field code reproduces it to $6\times10^{-6}$ in $\lambda_{\rm LO}$ (six cases, `slot_model_check.json`).
- At large $G$, $\lambda_{\min}\simeq2nG\,v/(1+v)$: profile-limited, not squeezed.

The matched mode is squeezed at **some** length iff $R>R_{\min}(v,n_{sp})$ (`slot_model.py`):

| profile | $n_{sp}=1$ | $n_{sp}=2$ |
|---|---|---|
| Gaussian | $R_{\min}=0.9020$ ($\gamma P_0/g>1.276$) | 0.9911 ($\gamma P_0/g>2.803$) |
| parabola | 0.7815 ($\gamma P_0/g>0.977$) | 0.9559 ($\gamma P_0/g>2.390$) |

So $R>1$ is the short-length criterion, not the criterion for squeezing at any length. That does not contradict the card, whose statement is at $z\to0^+$. The minimum over length is shallow near $R_{\min}$: the parabola at $n_{sp}=1$ reaches 0.904 at $R=0.9$, at $gz=0.84$. The full field at $\varepsilon_0=0.05$ confirms the thresholds (2f). This is my result, not the proposer's; it has not been checked by another family.
