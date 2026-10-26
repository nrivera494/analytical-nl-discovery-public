# Fission-burst dispersive-wave yield and the complex-time singularity of the compressed pulse

claude-b (claude-opus-5-5), T-20261016-claude-interactive-03, 2026-10-16. Derivation note for claim C-20261016-claude-b-01. The hypotheses were frozen in `explorations/2026-10-16-claude-b-dw-yield-hypotheses.md` (commits d1b7f71, 85637bb, b9067fa, f736bd3, 3a852dc). The runs are in `runs/2026-10-16-claude-b-dw-oracle/`.

## Setting

Model M0 (Roy, Bhadra and Agrawal 2009, Eqs. 1–2):
$$iu_\xi+\tfrac12u_{\tau\tau}+N^2|u|^2u=i\delta_3u_{\tau\tau\tau},\qquad\delta_3=\beta_3/(6|\beta_2|T_0).$$
- Fourier convention: $u=\frac1{2\pi}\int\hat u\,e^{-iw\tau}dw$. The linear phase is $D(w)=\delta_3w^3-w^2/2$.
- The ZDW is at $w_z=1/(6\delta_3)$ and the linear resonance near $w_{\rm DW}=1/(2\delta_3)$.

Let $u_0(\xi,\tau)$ be the $\delta_3=0$ solution from the same launch.
- For $\xi>0$ it is analytic in a strip $|\mathrm{Im}\,\tau|<d(\xi)$, with its nearest singularities on the boundary. A Gaussian launch is entire at $\xi=0$, so its singularities come in from infinity.
- Then $|\hat u_0(\xi,w)|=A(\xi)\,w^{\alpha}e^{-d(\xi)|w|}(1+o(1))$ as $|w|\to\infty$.
- Define $d_*=\min_{0\le\xi\le\xi_f}d(\xi)$, attained at $\xi_*$.

## Leading-order argument

1. **First order in $\delta_3$.** Write $u=u_0+v$. The radiation $v$ at frequencies $w\gg$ (the spectral width of $u_0$) obeys
$$\hat v_\xi\simeq iD(w)\hat v+i\delta_3w^3\hat u_0(\xi,w).$$
   Cross-phase modulation by $u_0$ adds an $O(1)$ phase only. Hence
$$\hat v(\xi_f,w)\simeq i\delta_3w^3e^{iD\xi_f}\int_0^{\xi_f}\hat u_0(\xi,w)\,e^{-iD(w)\xi}d\xi.$$
2. **Laplace's method in $\xi$.** For large $w$ the integrand is $\propto e^{-w\,d(\xi)}$ times a phase $e^{i(k(\xi)-D(w))\xi}$, where $k$ is the local rotation rate of the tail. The integral is dominated by a window of width $(w\,d''(\xi_*))^{-1/2}$ around $\xi_*$.
   - At the resonance, $D(w)=k(\xi_*)=O(1)$, and the contribution is $\propto e^{-w d_*}\times$(a power of $w$).
   - Away from the resonance, the phase mismatch $|D(w)-k|$ grows as $\delta_3^{-2}$ across the band. It suppresses the integral by $\exp[-(D-k)^2/(2wd'')]=\exp[-O(\delta_3^{-3})]$, which beats the $e^{O(\delta_3^{-1})}$ gain of the $e^{-wd_*}$ factor toward lower $w$.
   - So the emission is pinned to $w=w_{\rm DW}+O(\delta_3^{1/2})$.
3. **Photon number.** $\int_{w\ge w_z}|\hat v|^2dw\propto e^{-2d_*w_{\rm DW}}\times$(powers of $\delta_3$). Since $w_{\rm DW}=1/(2\delta_3)+O(\delta_3)$,
$$\ln\eta_{\rm DW}=-\frac{d_*}{\delta_3}+p\ln\delta_3+c+o(1).$$
   The local slope is $s(\delta_3)=-d\ln\eta/d(1/\delta_3)=d_*+p\,\delta_3+\dots$, so its error vanishes linearly in $\delta_3$.

This is a heuristic leading-order argument, not a proof. Points not controlled:
- the validity of first-order perturbation inside the compression event, where the field is large;
- the XPM phase;
- the possibility that fission induced by TOD before $\xi_*$ changes $d_*$ by $O(\delta_3)$. That would change only the prefactor.

The prefactor exponent $p$ is not derived; it is measured.

## Relation to the Akhmediev–Karlsson / Roy law

*What Eq. 6 is.* Roy, Bhadra and Agrawal's Eq. 6 (PRA 79, 023824, 2009; full text) estimates the NSR **spectral-peak level** $p_d=P_d/P_0$. It applies the Akhmediev–Karlsson single-soliton result to the shortest ejected soliton, of amplitude $\eta=2N-1$.
- Its exponent $\pi/(2(2N-1)\delta_3)$ equals $2\,(\pi/2\eta)\,w_{\rm DW}$. Here $\pi/(2\eta)$ is the strip width of $\eta\,\mathrm{sech}(\eta\tau)$, so Eq. 6 is the same pole mechanism evaluated on the stationary ejected soliton.
- Its stated validity is $(2N-1)\delta_3\ll1$, and it becomes doubtful near −15 dB.

*How Roy et al. validated it.* Against their full model: Raman with $f_R=0.245$ and a two-component response, self-steepening, sech launch, $T_0=50$ fs, $\xi=4$.
- In their Fig. 3(b) the Eq. 6 line falls close to the full-model data.
- Fig. 4(b) shows good agreement at $\delta_3=0.02$ and reasonable agreement at 0.03 up to $N=3$; it breaks down for $(2N-1)\delta_3\gtrsim0.15$.
- They also report that Eq. 6 deviates considerably from their TOD-only data, and that Raman lowers the NSR peak by more than 25 dB at $\delta_3=0.02$.

*The TOD-only gap.* Without Raman the compression transient has a narrower strip, $d_*<\pi/(2(2N-1))$, and dominates.
- The law gives the $\delta_3\to0$ exponent of that known gap, $[\pi/(2(2N-1))-d_*]/\delta_3$.
- At finite $\delta_3$ the gap is much smaller. At $N=2$ the TOD-only NSR peak exceeds Eq. 6 by 39.5, 12.8 and −0.4 dB at $\delta_3=0.02$, 0.03 and 0.04 (run 2026-10-16-claude-b-dw-oracle).

*Caveats.*
- The asymptotic tests ($d_*/\delta_3\gtrsim30$) lie at DW peak levels at or below the −80 dB visibility floor Roy et al. adopt.
- With Raman, the law holds with $d_*$ computed in the Raman model, but only for the single-oscillator response with $f_R=0.18$. A comparison with Roy's full model was **not** done.

*Prior work* (from gpt-b's novelty review, PR #49):
- compression-localised emission is published: Austin et al. 2006; Demircan et al. 2007; Driben, Yulin & Efimov 2015;
- pole-controlled radiation of fundamental cores is published: Wai, Chen & Lee 1990; Karpman 1993; Akhmediev & Karlsson 1995;
- the minimum-strip exponent for an evolving breather was not found there.

Identifiers and access levels are in claim C-20261016-claude-b-01.

## Exact anchor: the $N=2$ breather

For $iv_\xi+\frac12v_{\tau\tau}+|v|^2v=0$, $v(0)=2\,\mathrm{sech}\,\tau$ (Satsuma–Yajima),
$$v=\frac{4[\cosh3\tau+3e^{4i\xi}\cosh\tau]e^{i\xi/2}}{\cosh4\tau+4\cosh2\tau+3\cos4\xi}.$$
- Put $c=\cosh2\tau$. The denominator vanishes where $2c^2+4c+3\cos4\xi-1=0$, i.e. $c=-1\pm\sqrt3|\sin2\xi|$.
- The root with $|c|<1$ gives purely imaginary poles, $\tau=\pm\frac i2\arccos(\sqrt3|\sin2\xi|-1)$.
- Hence $d(\xi)=\tfrac12\arccos(\sqrt3|\sin2\xi|-1)$. It equals $\pi/2$ at $\xi=0$, as for $2\,\mathrm{sech}$, and has its minimum
$$d_*=\tfrac12\arccos(\sqrt3-1)=0.374664\quad\text{at }\xi=\pi/4.$$
- The numerical strip-width fit (`singularity.py`) reproduces $d(\xi)$ to $10^{-4}$ (run 2026-10-16-claude-b-dw-oracle, `singularity_validation.json`).

## Numerical results

Run 2026-10-16-claude-b-dw-oracle. The fit is $\ln\eta_{\rm DW}=c+p\ln\delta_3-d/\delta_3$ over the four smallest $\delta_3$.

| Launch | $\xi_f$ | $d_*$ ($\delta_3=0$) | Fitted $d$ | Deviation | $p$ | Ejected-soliton strip $\pi/(2(2N-1))$ (the exponent of Roy Eq. 6) |
|---|---|---|---|---|---|---|
| sech $N=2$ (construction set) | 4 | 0.37466 (exact) | 0.3788 | +1.1% | −3.43 | 0.5236 |
| sech $N=3$ (held out) | 2 | 0.1997 | 0.2008 | +0.6% | −3.20 | 0.3142 |
| Gaussian $N=4$ (held out) | 1 | 0.1317–0.1322 | 0.1323 | +0.1% | −3.02 | — |
| Gaussian $N=3$ | 2 | 0.1923 (global minimum, second compression at $\xi=1.103$) | 0.1929 | +0.3% | −2.88 | — |

The Gaussian $N=3$ row compares with the global minimum. Against the first-compression value 0.2015 used in amendment A1 the deviation is −4.3%; see A3.

Other checks:
- The local slopes approach $d_*$ from below. Their deviation shrinks as $\delta_3^{1.2}$ (sech $N=2$), $\delta_3^{1.9}$ (sech $N=3$) and $\delta_3^{1.1}$ (Gaussian $N=4$).
- The tails at $\xi_*$ are pure exponentials (fit residual rms $10^{-4}$), so the singularities lie on the imaginary axis.
- Gate independence: widening the gate by 5 changes $\eta_{\rm DW}$ by less than $10^{-4}$ relative for $\delta_3\le0.016$.
- Step convergence: halving the step changes $\eta_{\rm DW}$ by at most 13% at the smallest yields ($\approx10^{-13}$), and by less than 1% for $\eta_{\rm DW}>10^{-9}$. The scheme is fourth order.
- A second integrator (RK4IP) agrees on yields to between $2\times10^{-7}$ and $3\times10^{-4}$ (`m0_two_integrators.json`).
