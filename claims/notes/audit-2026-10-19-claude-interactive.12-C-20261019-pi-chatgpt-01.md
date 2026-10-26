---
agent: claude-interactive.12
model: claude-opus-5-5
family: claude
claim: C-20261019-pi-chatgpt-01
task: T-20261019-claude-interactive-02
date: 2026-10-19
status: complete
verdict: pass
---

# Independent verification: closed-form $c_2(\Phi)$ for weak normal dispersion, Gaussian pulse

**Verdict: pass.** I derived $c_2(\Phi)$ again by a different route and obtained exactly the claimed closed form (symbolic residual 0). My own full mean-plus-tangent propagation extrapolates to it within $1.1\times10^{-6}$ at the source value $\Phi=3$ and at the three frozen held-out values $\Phi=1$, 1.5 and 7. The approach is linear in $\sqrt y$, and the remainder after the $c_2$ term scales as $y^{1.00}$, as claimed. No blocker. The stated regime does not need narrowing; I add the region I checked.

All numbers are from run `2026-10-19-claude-interactive.12-c2-weak-dispersion-verification` (`summary.json`, `derive_c2*.json`).

## Clean context

Before committing my own work I read only: the claim card, the parent card C-20261010-claude-a-01 (item 5), the problem card P-20261010-claude-interactive-01, `AGENTS.md`, `docs/AUDIT_PROTOCOL.md`, `runs/README.md`, `scripts/validate.py` and `docs/SOLVER.md`. The parent card quotes the source's $\lambda_{\min}=0.0265400309069$ at $\Phi=3$, $y=10^{-4}$; I saw that number there, and my code computed its own value.

My independent work was committed and pushed before I opened any of the proposer's files:
- symbolic derivation, commit 23111dd (07:17 EDT);
- propagation code, commit eeb688e;
- results, sech test, fits and figure, commit e136364 (07:52 EDT).

I then read `archive/weak_theory/weak_dispersion_derivation.md` (sections 5 and 7), `second_order_symbolic.py` and its JSON output, and report sections 5.5 and 6.1 of run `2026-10-18-pi-chatgpt-independent-verification`. I did not open the review document, the quick-reproduction run, or claude-a's code at any point.

## Restatement and assumptions

Scalar lossless NLSE, $u_\zeta=-i\tfrac{\varepsilon}{2}u_{xx}+i\Phi|u|^2u$ with $\varepsilon=L/L_D$, $y=\Phi\varepsilon$, and input $u(0,x)=e^{-x^2/2}$. Linearized noise with vacuum covariance $I$; $\lambda_{\min}$ is the smallest eigenvalue of $MM^{\mathsf T}$ over all modes, where $M$ is the real tangent map. At fixed $\Phi$, as $y\to0$:
$$\lambda_{\min}/\lambda_0-1=A\sqrt y\,[1+c_2\sqrt y+O(y)],$$
with $A$ and $c_2$ as on the card.

The card's assumptions 1–4 are complete for this statement. Two are implicit, and both hold for the stated input:
- **Even, unchirped input.** The mean is even and unchirped, so the generator commutes with parity and the optimum lies in the even sector.
- **Local normalization.** The Gaussian's local expansion is normalized to unit curvature, $p=1-x^2+\tfrac12x^4+\dots$. The quartic coefficient $\tfrac12$ enters $c_2$ (see the sech test below).

## A. Independent derivation (before reading)

`derive_c2.py` (SymPy) works as follows.
- **Scaling.** Local variables $x=h^{1/2}q$ with $h=\sqrt y$, so $\varepsilon\partial_x^2=(h/\Phi)\partial_q^2$ and $|u(0)|^2=e^{-hq^2}$.
- **Mean field.** Solved order by order in $h$ in a frame rotating at the constant rate $\Phi$, not the local mean phase. The residual is checked to vanish through $h^2$. The peak intensity is $1-y\zeta^2$.
- **Tangent generator.** $a_\zeta=-\Phi I a+[\Phi(1-2\rho+R)+\tfrac{h}{2\Phi}\partial_q^2]b$ and $b_\zeta=[\Phi(2\rho+R-1)-\tfrac{h}{2\Phi}\partial_q^2]a+\Phi I b$, where $U^2=R+iI$. It is expanded to $L_0+hL_1+h^2L_2$.
- **Duhamel to second order.** Includes the time-ordered $L_1L_1$ term.
- **Eigenvalue problem.** Quasi-degenerate perturbation theory on the input-side operator $W=M^{\mathsf T}M$, whose zeroth order has eigenvalue $\lambda_0$ infinitely degenerate:
  - $K_1=PW_1P$ is a harmonic oscillator in $q$ with ground state $e^{-\kappa q^2/2}$, $\kappa=\sqrt6$, i.e. rms width $(y/24)^{1/4}$;
  - $E_2=\langle W_2\rangle-\|P_+W_1\Psi_0\|^2/(\lambda_+-\lambda_0)$.
- **Exactness.** Operators act exactly on polynomial times Gaussian, and inner products use Gaussian moments. The parametrization $r=S-\Phi$ makes everything rational in $r$.

Results:
- $A=\sqrt{2/3}\,\Phi/S$, and
  $$c_2=\frac{\sqrt6\,(4r^8+45r^6+102r^4+5r^2+24)}{60(1-r^2)^2(1+r^2)^2}.$$
  Its difference from the card's closed form simplifies to **exactly 0**. Numerically it agrees to all 15 printed digits at $\Phi=0.25$, 0.5, 1, 1.5, 2, 3, 7, 10 and 40, and $c_2\to2\sqrt6/5$.
- **Size of the pieces.** In units of the first-order energy, at $\Phi=3$, the terms of $E_2$ are:

  | Piece | Value |
  |---|---|
  | $L_2$ Duhamel term | +6.13 |
  | time-ordered $L_1L_1$ term | −19.12 |
  | $M_1^{\mathsf T}M_1$ | +55.83 |
  | branch mixing | −41.86 |
  | **sum** | **0.98946** |

  $\langle W_2\rangle$ and the branch-mixing term are each about $4\Phi^2$ times $c_2$ and cancel (at $\Phi=40$: $+6213$ against $-6212$). So omitting branch mixing, or any $O(1)$ error in either term, changes $c_2$ grossly, as card assumption 4 says. The split among the first three pieces depends on the frame; $\langle W_2\rangle$ and the branch-mixing term do not, because the frames differ only by an orthogonal map on the output side.
- **Mean reshaping ablation.** Removing dispersion from the mean-field equation, while keeping it in the tangent equation, lowers $c_2$ by exactly $1/\sqrt6=0.408$ at every $\Phi$ (`derive_c2_ablation_no_mean_reshaping.json`).
- **Shape specificity.** The same script with input $\mathrm{sech}\,x$, whose intensity $\mathrm{sech}^2x=1-x^2+\tfrac23x^4$ has the same curvature as the Gaussian, gives
  $$c_2^{\rm sech}=\frac{\sqrt6\,(11r^8+180r^6+418r^4+20r^2+91)}{240(1-r^2)^2(1+r^2)^2}=c_2-\frac{1}{8\sqrt6}.$$
  This is a constant shift of −0.0510, with $c_2^{\rm sech}(\infty)=91\sqrt6/240=0.92876$ (`derive_c2_sech.json`). I wrote this prediction down before computing the sech numerics.

## B. Independent full propagation (before reading)

`lam_min.py` propagates the mean and the tangent columns together:
- **Discretization.** Periodic Fourier grid on $|x|<10$, with dispersion exact in the interaction picture.
- **Integration.** Kerr terms by DOP853 (scipy) at rtol $10^{-13}$; points with $y\le10^{-6}$ were rerun at $3\times10^{-14}$, which is the tolerance used.
- **Input.** Restricted to even grid functions with $|x|\le10\sigma$, $\sigma=(y/24)^{1/4}$, both quadratures; all output rows are kept.
- **Grid.** $dx\le\sigma/3$, so $N=2048$ to 16384.
- **Readout.** $\lambda_{\min}=\sigma_{\min}^2$ of the restricted map, an upper estimate.

**Validation at $y=0$.** It returns $\lambda_0$ to $2\times10^{-14}$ ($\Phi=1$) and $4.5\times10^{-13}$ ($\Phi=7$). At $\Phi=3$, $y=10^{-4}$ it gives 0.0265400309068293. That matches the source's separate Fourier solver (0.02654003090684555) to $6\times10^{-14}$ relative; I saw that value only after my run.

Effective coefficient $c_{\rm eff}=[(\lambda_{\min}/\lambda_0-1)/(A\sqrt y)-1]/\sqrt y$ (held-out $\Phi$ marked *):

| $\Phi$ | $y=10^{-4}$ | $10^{-5}$ | $10^{-6}$ | $10^{-7}$ | extrapolated $c_2$ | claimed $c_2$ | difference | slope $d$ | remainder exponent |
|---|---|---|---|---|---|---|---|---|---|
| 1* | 1.201924 | 1.212507 | 1.215877 | 1.216945 | 1.2174395 | 1.2174400 | $-4.8\times10^{-7}$ | −1.563 | 0.9989 |
| 1.5* | 1.044623 | 1.050047 | 1.051757 | 1.052297 | 1.0525472 | 1.0525474 | $-2.5\times10^{-7}$ | −0.790 | 1.0002 |
| 3 | 0.985049 | 0.988076 | 0.989026 | 0.989325 | 0.9894640 | 0.9894646 | $-5.7\times10^{-7}$ | −0.438 | 1.0003 |
| 7* | 0.977447 | 0.979872 | 0.980632 | 0.980870 | 0.9809822 | 0.9809834 | $-1.1\times10^{-6}$ | −0.350 | 0.9994 |

How the table was built:
- **Data.** Ten values of $y$ from $10^{-4}$ to $10^{-7}$ per $\Phi$.
- **Extrapolated $c_2$.** Fit $c+d\sqrt y+ey$ over $10^{-7}\le y\le10^{-4}$. Two other fits, linear over $10^{-7}$–$10^{-5}$ and quadratic over $2\times10^{-7}$–$2\times10^{-5}$, agree to within $2.4\times10^{-6}$ ($\Phi=1$) and $\le6\times10^{-7}$ (others).
- **Remainder exponent.** The exponent of $|(c_{\rm eff}-c_2)\sqrt y|$ against $y$, i.e. the $O(y)$ remainder of the bracket; the claim predicts 1.
- **Leading exponent.** The fitted exponent of the excess itself is 0.5012–0.5015, i.e. ½ plus the $c_2\sqrt y$ correction.
- **Mode width.** The fitted mode rms width matches $(y/24)^{1/4}$ to 0.5% ($\Phi=1$) or better at $y=10^{-4}$, and to 0.1% at $y\le10^{-6}$.
- **Below $10^{-7}$.** At $\Phi=3$ and 7 I also ran $y=5\times10^{-8}$ and $2\times10^{-8}$. They give 0.989390 and 0.980905 at $y=2\times10^{-8}$, which is $1.2\times10^{-5}$ and $2.8\times10^{-5}$ below the fitted line. That is consistent with the rtol $10^{-13}$ bias, which already lowers $c_{\rm eff}$ by $1.5\times10^{-6}$ and $4\times10^{-6}$ at $y=10^{-7}$ and grows as $1/y$. These points are not used in the fits.

**Held out.** All three frozen values pass: $c_2(1)$, $c_2(1.5)$ and $c_2(7)$ are reproduced to $5\times10^{-7}$, $3\times10^{-7}$ and $1.2\times10^{-6}$. The measured approach is $O(\sqrt y)$ with slopes $d(\Phi)$ as tabulated.

## C. Convergence and artefacts

At $\Phi=1$, 3 and 7, for $y=10^{-4}$ and $10^{-7}$:

| Check | Change in $\lambda$ (relative) | Change in $c_{\rm eff}$ |
|---|---|---|
| $N$ doubled | $\le1.7\times10^{-13}$ | $\le9\times10^{-7}$ |
| window $\lvert x\rvert <8$ or $<14$ | $\le7\times10^{-14}$ | $\le5\times10^{-7}$ |
| input support $7\sigma$ or $14\sigma$ | $\le4\times10^{-13}$ | $\le5\times10^{-7}$ |
| rtol $10^{-12}$ or $3\times10^{-14}$ instead of $10^{-13}$ | — | up to $1.6\times10^{-6}$ ($\Phi=1$), $1.8\times10^{-5}$ ($\Phi=3$), $5.2\times10^{-5}$ ($\Phi=7$) at $y=10^{-7}$; hence the rtol $3\times10^{-14}$ reruns |
| even and odd inputs ($y=10^{-6}$) | $\le5\times10^{-15}$ | — |

- **Containment.** The input singular vector's amplitude at the support edge is $\le10^{-11}$ of its peak in every run.
- **No remote competitor.** I computed the fully unrestricted map once, with all 1024 grid points of $|x|<10$ as inputs in both quadratures, at $y=10^{-4}$. It gives the same $\lambda_{\min}$ as the restricted support to $1.1\times10^{-12}$ ($\Phi=3$) and $1.2\times10^{-13}$ ($\Phi=1$).
- **Second integrator.** Fixed-step RK4IP at 1000 and 2000 steps with Richardson extrapolation agrees with DOP853 to $3\times10^{-14}$, $1.2\times10^{-13}$ and $1.1\times10^{-13}$ relative ($\Phi=1$, 3, 7 at $y=10^{-4}$), and to $9\times10^{-14}$ at $\Phi=3$, $y=10^{-6}$.

## D. Non-uniformity as $\Phi\to0$

- **$\Phi=1$.** At $\sqrt y\le10^{-2}\ll\Phi^2=1$ the expansion is usable. The $O(y)$ term $d\,y$ is 1.3% of the $c_2\sqrt y$ term at $y=10^{-4}$.
- **Smaller $\Phi$ (rtol $3\times10^{-14}$).** The slope grows quickly as $\Phi$ falls, roughly as $\Phi^{-3.6}$ between 0.5 and 0.25. That supports the card's hierarchy $\sqrt y\ll\Phi^2$.

  | $\Phi$ | slope $d$ | extrapolated $c_2$ | claimed $c_2$ | difference |
  |---|---|---|---|---|
  | 0.5 | −10.8 | 2.42791 | 2.42794 | $3\times10^{-5}$ |
  | 0.25 | −130 | 7.8227 | 7.8269 | 0.05% |

  At $\Phi=0.25$ the extrapolation is limited by curvature: $\sqrt y/\Phi^2$ reaches 0.16 at $y=10^{-4}$.

## E. Relaxed assumptions

1. **Formal local expansion (card assumption 3).** The propagation does not expand locally. It solves the full nonlinear mean and the full tangent map over the whole pulse, and the unrestricted-input run excludes remote or mixed competitors on the grid at $y=10^{-4}$. It does not prove the global continuum bound or a uniform remainder. Both derivations are formal and share that limitation.
2. **Pulse shape.** For sech input, $c_{\rm eff}$ extrapolates to my prior prediction:

   | $\Phi$ | extrapolated | predicted | slope | Gaussian $c_2$ |
   |---|---|---|---|---|
   | 1 | 1.1664086 | 1.1664090 | −1.77 | 1.21744 |
   | 3 | 0.9384332 | 0.9384335 | −0.59 | 0.98946 |

   Window $|x|<25$, $10^{-6}\le y\le10^{-4}$, remainder exponents 0.998 and 1.000. So $c_2(\Phi)$ is specific to the Gaussian; the sech value is lower by $1/(8\sqrt6)$. That test exercises the quartic-potential and mean-reshaping terms of the derivation on a case the source did not compute. *Addendum, after this report was first committed:* $E_2$ is linear in the second-order generator, and the peak's quartic coefficient $\kappa_4$ enters only there, so $c_2$ is affine in $\kappa_4$. From the Gaussian and sech values this gives $c_2(\Phi,\kappa_4)=c_2(\Phi)-\tfrac{\sqrt6}{8}(\kappa_4-\tfrac12)$. I froze the prediction for a third shape, intensity $e^{-x^2-x^4/2}$ with $\kappa_4=0$, before computing it (`HELDOUT_kappa4.md`, commit 76856b7). The symbolic result is exactly $c_2+\sqrt6/16$. Propagation extrapolates to 1.370533 and 1.142558 at $\Phi=1$ and 3, against the frozen 1.370533 and 1.142558 (differences $\le4\times10^{-7}$). This is filed as the separate claim C-20261019-claude-interactive.12-01, which needs verification by another family (task T-20261019-claude-interactive.12-05).
3. **Not relaxed: physics.** I did not test Raman, $\beta_3$, self-steepening, loss or finite detection bandwidth. The parent card already shows that self-steepening and a fixed bandwidth change what $\lambda_{\min}$ measures. The PI's Julia solver was not used: the parent card records that its anti-alias window corrupts the full-$V$ $\lambda_{\min}$. My two integrators and one independent cross-solver point (the source's Fourier solver) stand in for a second solver.

## F. Comparison with the proposer's derivation (after reading)

The two derivations are independent routes to the same coefficient.
- **Frame.** The source works in the local mean-phase frame, equation (11) of the derivation note. Its $G_2$ has a dilation $-s(2q\partial_q+1)$, the constants $\pm1/(2\Phi)$ from $R_{qq}/R$, and the potential $\Phi q^4-2\Phi s^2$. I work in a frame at the constant rate $\Phi$, where the same effects enter through $I=\mathrm{Im}\,U^2$ and the $q$-dependent mean phase.
- **Side.** The source applies perturbation theory to the output covariance $V=MM^{\mathsf T}$ along $e_-=(1,-r)$. I apply it to $M^{\mathsf T}M$ on the input side along $v_-=(r,-1)/\sqrt{1+r^2}$.

I checked their equations (21)–(25) against my expansion line by line:
- **Mean reshaping.** Their $\rho=1-\epsilon q^2+\epsilon^2(q^4/2-s^2)$ equals my $\rho_2$. Their phase term $\epsilon^2s/(2\Phi)$ agrees with my $-\tfrac{h}{2\Phi}\mathrm{Re}(U_{qq}/U)$ term at this order.
- **$G_2$.** Their dilation follows from conjugating $\partial_q^2$ by the chirp $\theta_q=-2\Phi s\epsilon q$. Their $\pm1/(2\Phi)$ is the $R_{qq}/R=-\epsilon$ term. Both are correct.
- **Time ordering.** Their nested integral (24) is my $L_1f_1$ term.
- **Noncommutation of $D$ and $q^2$.** Both calculations apply the operators in sequence to explicit functions, so it is included automatically.
- **Branch mixing.** Their $-\|e_+^{\mathsf T}V_1e_-g\|^2/(\lambda_0^{-1}-\lambda_0)$ has the same structure as mine on the other side.
- **Same intermediates.** The oscillator ground state $e^{-\sqrt6q^2/2}$ is the same in both. Their intermediate $r$-form of $c_2$ (`second_order_symbolic.json`) is character for character the expression I obtained.

I found no error. Their hand-written $S_1^\dagger e$ and $V_1$ were not checked separately; my calculation does not use them, and the final coefficients agree exactly.

**The source's single-point numbers.** The card's prediction 3 quotes 0.98943 at $\Phi=3$, $y=10^{-7}$ and 0.97998 at $\Phi=10$, $y=10^{-6}$. I get 0.989325 and 0.980000. Mine lie on the smooth $\sqrt y$ approach to the closed form; the slope at $\Phi=3$ predicts 0.989326. The differences, $+1.05\times10^{-4}$ and $-2.4\times10^{-5}$, correspond to relative errors in $\lambda$ of $8\times10^{-12}$ and $2\times10^{-11}$. That is the scale of the source's eighth-order finite-difference grid error: its $\Phi=3$, $y=10^{-6}$ value 0.0263544574334 differs from my spectrally converged 0.0263544574230 by $4\times10^{-10}$ relative, and the source itself reports a $4\times10^{-12}$ absolute change from 2048 to 3072 points. This does not affect the claim; prediction 3 says only that the approach is $O(\sqrt y)$.

## Blockers

None.

## Non-blocking concerns

1. **Formal result.** Neither derivation bounds the remainder uniformly or proves the global spectral-localization lower bound (card assumption 3). The numerics cover $0.25\le\Phi\le7$ and $10^{-7}\le y\le10^{-4}$, with unrestricted input checked at $y=10^{-4}$ only. Task T-20261019-claude-interactive.12-01.
2. **Source values.** The source's quoted $c_{\rm eff}$ values carry numerical errors of up to $10^{-4}$ (section F). My values are recorded on the card next to them.
3. **No physical relaxation.** None was tested (section E3). Task T-20261019-claude-interactive.12-02.
4. **Status.** This was a clean-context derivation and simulation check, not an adversarial audit by a separate auditor. The claim can be `sim-verified`; `audited` needs a separate non-gpt audit. Task T-20261019-claude-interactive.12-03.

## Regime I sign off on

The card's statement holds, within linearized, scalar, lossless Kerr theory with $\beta_2>0$ only and unrestricted detection, for a Gaussian input.
- **Coefficient values.** $c_2(\Phi)$ as stated, checked for $\Phi\in\{0.25,0.5,1,1.5,3,7\}$ over $10^{-7}\le y\le10^{-4}$, with single points at $\Phi=2$ and 10.
- **Extrapolation agreement.**
  - $\Phi\ge1$: within $1.1\times10^{-6}$;
  - $\Phi=0.5$: within $3\times10^{-5}$;
  - $\Phi=0.25$: within 0.05%.
- **Accuracy at finite $y$.** $|c_{\rm eff}-c_2|\approx|d|\sqrt y$, with $d=-1.56$, −0.79, −0.44 and −0.35 at $\Phi=1$, 1.5, 3 and 7. That is below $2\times10^{-3}$ for $\Phi\ge1.5$ at $y\le10^{-5}$.
- **Small $\Phi$.** The hierarchy $\sqrt y\ll\Phi^2$ is the controlling condition.
