---
agent: claude-b
model: claude-opus-5-5
family: claude
date: 2026-10-08
task: T-20261008-claude-b-01
problem: P-20261004-root-03
claim: C-20261008-claude-b-01
runs:
  - 2026-10-08-claude-b-grin-manakov-lib
  - 2026-10-08-claude-b-exponents
  - 2026-10-08-claude-b-kw-map
  - 2026-10-08-claude-b-optimum
  - 2026-10-08-claude-b-heldout
  - 2026-10-08-claude-b-thirdorder
  - 2026-10-08-claude-b-normalization
  - 2026-10-08-claude-b-gif625-fwm-mismatch
  - 2026-10-08-claude-b.5-solver-twomode-check
---

# Manakov (LP01) against GRIN filtered soliton noise: derivation

This note is the derivation behind claim C-20261008-claude-b-01. Auditors should not read it before committing their report.

## 1. Setting

**Model.** Cross-phase-only $M$-mode NLS in soliton units, $\tau=T/T_0$, $\zeta=z/L_D$:
$$i\partial_\zeta a_m+i\delta_m\partial_\tau a_m+\tfrac12\partial_\tau^2a_m+\Big(\sum_nC_{mn}|a_n|^2\Big)a_m=0 .$$
- Equal $\beta_2$ in all modes; no $\beta_3$; no Raman; no self-steepening.
- No intermodal four-wave mixing: the coherent terms are averaged out by the propagation-constant differences.
- $C$ is real and symmetric, written $C=J+\Delta$ with $J$ the all-ones matrix. $\Delta=0$ is the Manakov case.
- $\delta_m$ is the walk-off of mode $m$ against LP01 ($\delta_1=0$).
- For ideal parabolic-profile GRIN modes, $C=\begin{pmatrix}1&1\\1&1-\varepsilon\end{pmatrix}$ with $\varepsilon=1/2$ for LP01/LP02 and $1/4$ for LP01/LP11a.

**Launch (γ_eff energy, the card's).** $a_m(0)=c_m\,\mathrm{sech}\,\tau/\sqrt\Sigma$, with:
- $c_m=\sqrt{p_m}$ and $\sum_mp_m=1$, so $p_m$ is the photon fraction;
- $\Sigma=p^TCp$.

At $\Sigma\ne1$ this is an evolving near-soliton launch, not a stationary vector soliton (card, mean-field qualification). The analysis below includes all radiation, because the numerics solve the full PDE.

**Readout.** A passive spectral filter with transmission $T(\omega)\in[0,1]$, applied identically to every mode, followed by counting all modes: $N_T=\sum_m\langle a_m,\hat T a_m\rangle$, with the vacuum of the filter's loss port. The comparison quantity is the linearized Fano factor $F=\mathrm{Var}(N_T)/\langle N_T\rangle$ for coherent input; it does not depend on photon number. $F_s(\zeta;T)$ denotes the scalar LP01 soliton ($p_1=1$).

**Comparison.** The two launches are compared at equal $\zeta$, each at its own soliton energy. This is the experimentally natural comparison: the same fiber, the same $T_0$ and the same $L$, with the power set for a fundamental soliton. With equal photon number instead, the mixed launch is not at its soliton order, and $F$ already changes at first order in $\Delta$ through the $N$-dependence of the scalar $F$. The first-order null below is specific to the γ_eff normalization.

## 2. Rotated basis

Take an orthonormal basis of mode space with $e_0=c$ and $e_j\perp c$. Define $u=c^Ta$ (soliton direction) and $v_j=e_j^Ta$ (dark directions). The change of basis is orthogonal, so:
- the readout is invariant: $N_T=\langle u,\hat Tu\rangle+\sum_j\langle v_j,\hat Tv_j\rangle$;
- the vacuum is invariant.

The quartic potential splits as $-\tfrac12\big(\sum_m|a_m|^2\big)^2-\tfrac12\sum_{mn}\Delta_{mn}|a_m|^2|a_n|^2$. The first part is $U(M)$-invariant.

## 3. Exact statements

**(E1) Manakov equivalence.** For $\Delta=0$ and $\delta=0$, $F(T)=F_s(T)$ for every $T$ and every $p$.
- The equations, the launch $c\,\mathrm{sech}\,\tau=U(\mathrm{sech}\,\tau,0,\dots)$, the vacuum and $N_T$ are all covariant under $U(M)$, so every moment of $N_T$ equals its scalar value.
- In the Kerr-only model this holds beyond linearization, because the normal-ordered quartic $\big(\sum_ma_m^\dagger a_m\big)^2$ is $U(M)$-invariant.
- Numerical check (run `2026-10-08-claude-b-grin-manakov-lib`): the per-bin all-mode covariance equals the scalar one to $4\times10^{-9}$ relative.

**(E2) Parity.** $F(\delta;T(\omega))=F(-\delta;T(-\omega))$. Reflecting $\tau\to-\tau$ maps $\delta_m\to-\delta_m$ and leaves the sech launch and the vacuum invariant. For symmetric filters, $F$ is therefore even in $\delta$.

**(E3) First-order null.** At $\delta=0$, linearized and with the γ_eff launch, $\partial F/\partial\Delta=0$ at $\Delta=0$, for every $p$, $\zeta$ and $T$.

*Mean field.* Restricted to $v=0$, the quartic term is $-\tfrac12(p^TCp)|u|^4=-\tfrac12\Sigma|u|^4$. So $u$ obeys the scalar NLS with nonlinear coefficient $\Sigma$, and the launch $\mathrm{sech}/\sqrt\Sigma$ is its exact soliton. The dark directions are driven by
$$\partial V/\partial v_j^*|_{v=0}=-q_j|u|^2u,\qquad q_j=e_j^T\mathrm{diag}(c)\,\Delta\,p ,$$
because $e_j^T\mathrm{diag}(c)Jp=e_j^Tc=0$. Hence $\bar v_j=O(q)$, and $\bar u$ is the exact scalar soliton (times $\Sigma^{-1/2}$) up to $O(q^2)$.

*Linearized propagator $\mathcal J$* (input quadratures to output fields):
- At $O(\Delta^0)$ it is block-diagonal. The $uu$ block is the scalar soliton's. Each $v_jv_j$ block is the passive operator $i\partial_\zeta+\tfrac12\partial_\tau^2+|\bar u|^2$, identical for all $j$.
- At $O(\Delta)$ the $uu$ block is unchanged. The $\Sigma$-rescaled amplitude exactly compensates the change of the $u$ self-phase.
- The $uv$ and $vu$ blocks are $O(q)$: they come from the $\Delta$ terms, whose coupling vector is again $q$, and from the Manakov cross-phase with $\bar v=O(q)$.
- The $vv$ blocks change by $O(\Delta)$.

*Readout gradient.* $g=(2\hat T\bar u,\,2\hat T\bar v_j)$, with $g_v=O(q)$.

*Variance.* $\mathrm{Var}=\tfrac14\|\mathcal J^Tg\|^2$.
- The $u$-input component is $\mathcal J_{uu}^Tg_u+\mathcal J_{vu}^Tg_v=\mathcal J_s^Tg_s+O(q^2)$.
- The $v$-input component is $O(q)$.

So $\mathrm{Var}=\mathrm{Var}_s/\Sigma+O(q^2)$ and $\langle N\rangle=\langle N\rangle_s/\Sigma+O(q^2)$, which gives $F=F_s+O(q^2)$. ∎

**(S2) Second-order form** (derived at this order; coefficients numerical). With $r_j=e_j^T\mathrm{diag}(\delta)\,c$:
$$F(T)-F_s(T)=K(\zeta;T)\,\|q\|^2+W(\zeta;T)\,\|r\|^2+X(\zeta;T)\,q\cdot r+O(3),$$
$$q=P_\perp\,\mathrm{diag}(\sqrt p)\,\Delta\,p,\qquad r=P_\perp\,\mathrm{diag}(\delta)\,\sqrt p,\qquad P_\perp=1-\sqrt p\sqrt p^{\,T}.$$
- Every first-order coupling to the dark subspace is linear in $(q,r)$.
  - The walk-off term splits into a common drift $\bar\delta=p\cdot\delta$ of $u$, which is a pure time translation and leaves every spectral readout unchanged, and the couplings $r_j$.
  - The relative drifts of the dark modes are $O(\delta)$ corrections to their propagators, which enter only at third order.
- The zeroth-order dark propagators are identical and decoupled. So the second-order form is isotropic in the dark subspace, and $K$, $W$, $X$ depend only on $\zeta$ and $T$: not on $M$, on $p$, or on which overlaps differ from 1.
- The $q$ source ($|u|^2u$) is even in $\tau$ and the $r$ source ($u_\tau$) is odd, so $X=0$ for symmetric filters.
- For two modes:
  - $\|q\|^2=p_1p_2\,[(C_{12}-1)(p_1-p_2)+(C_{22}-1)p_2-(C_{11}-1)p_1]^2$, which reduces to $\varepsilon^2p_1p_2^3$ for the GRIN matrix;
  - $\|r\|^2=\delta^2p_1p_2$.
- The third-order terms are $O(\|q\|^2\,|\Delta|)$, $O(\|r\|^2\,|\Delta|)$ and $O(\|r\|^2\delta^2)$. For GRIN LP02: $\varepsilon^3p_1^2p_2^4$, $\varepsilon\delta^2p_1^2p_2^2$ and $\delta^4p_1p_2$.

**(S3) Optimized filter: envelope argument.** Let $T^*$ minimize $F_s$ over a filter class $\mathcal T$, with a nondegenerate minimum (quadratic, or a discrete minimum separated by a gap larger than the perturbation). Then
$$\min_{\mathcal T}F_{\rm GRIN}-\min_{\mathcal T}F_s=K(\zeta;T^*)\|q\|^2+W(\zeta;T^*)\|r\|^2+O(3),$$
because the shift of the optimal filter changes $F$ only at $O(\|q\|^4)$.

Whether a GRIN launch can beat LP01 at the optimum is therefore decided, at leading order, by the signs of $K^*=K(\zeta;T^*)$ and $W^*=W(\zeta;T^*)$.
- If $W^*>0>K^*$, it beats LP01 exactly when $\delta<\delta_c$, with $\delta_c$ given by $\|r\|^2/\|q\|^2=-K^*/W^*$; for GRIN LP02, $\delta_c=\varepsilon p_2\sqrt{-K^*/W^*}$.
- At a fixed filter (inequality (I2)) the same holds with $T$ in place of $T^*$.

## 4. Physical regime of the two-mode model in GIF625 (ideal profile, 1550 nm)

Computed with the analytic GRIN propagation constant of run `2026-10-04-claude-b-gif625-walkoff` (same functions):
- The l = 0 mixing 02+02 → 01+03 has phase mismatch $\Delta\beta=-25.6\ \mathrm{m}^{-1}$, so $|\Delta\beta|L_D=912\,T_0^2$ ($T_0$ in ps).
- $\delta_{\rm LP02}=5.37\,T_0$ and $\delta_{\rm LP11}=2.59\,T_0$.
- Hence $\delta_{\rm LP02}=0.178\sqrt{|\Delta\beta|L_D}$. The two-mode cross-phase model needs $|\Delta\beta|L_D\gtrsim10$, i.e. $\delta_{\rm LP02}\gtrsim0.56$. **For LP01+LP02 in this fiber, $\delta\approx0$ and the two-mode model cannot both hold.**

Degenerate-group mixing (02+02 ↔ 21+21) is phase-matched. For an axisymmetric launch, though, the $l=\pm2$ fluctuations decouple from the $l=0$ sector in the linearized equations (angular momentum), so they do not enter $F$ at this order.

Run `2026-10-08-claude-b-gif625-fwm-mismatch` registers these numbers. It also gives the LP11 case: 11+11 → 01+21 has $|\Delta\beta|L_D=227\,T_0^2$ and $\delta_{\rm LP11}=2.59\,T_0$, so $\delta_{\rm LP11}\gtrsim0.54$.

## 5. Numerics (pure Kerr, two and three modes; same-family numpy code)

### Method

**Code** (run `2026-10-08-claude-b-grin-manakov-lib`):
- one central-difference Jacobian per case gives the covariance of the photon counts in every spectral bin and mode;
- every common filter is then a quadratic form, so filter optimization is cheap.

**Validation** (same run):
- the Manakov per-bin covariance equals the scalar one to $4\times10^{-9}$;
- one propagation step gives $F=1-3\times10^{-7}$;
- round-1 numbers are reproduced to $1.8\times10^{-10}$;
- the $M$-mode code equals the two-mode code exactly at $M=2$.

**Filter classes:**
- A: hard symmetric band;
- A': fractional edge bin (a continuous edge);
- B: any hard interval, searched exhaustively;
- C: any transmission in [0, 1], local optimizer.

### Results

**First-order null** (run `2026-10-08-claude-b-exponents`, $p_2=0.2$, $C_{22}=1\mp e$):
- At $\zeta=2$, LP01-optimal band $k_{\max}=5$: the even part of $\Delta F$ scales as $e^{1.998}$ and $e^{1.992}$, and the odd part as $e^{3.000}$ and $e^{2.998}$.
- At $\zeta=5$, $k_{\max}=4$: even $e^{1.997}$, odd $e^{2.994}$.
- There is no linear term.

**$p_2^3$ law (GRIN).**
- $K_{\rm eff}=\Delta F/(\varepsilon^2p_1p_2^3)$ at $\zeta=2$: $-0.383,-0.389,-0.401,-0.423,-0.458$ for $p_2=0.025,0.05,0.1,0.2,0.4$.
- At $\zeta=5$: $3.325,3.315,3.307,3.354,3.804$.

**$\delta^2p_1p_2$ law (Manakov overlaps).**
- At $\zeta=2$, $W_{\rm eff}=0.4243,0.4245,0.4252,0.4270$ for $\delta=0.05$–0.4, and $0.4277,0.4258,0.4252$ for $p_2=0.1,0.3,0.5$.
- At $\zeta=5$, $W_{\rm eff}=0.339,0.356,0.428,0.772$ for $\delta=0.05$–0.4, i.e. $W\approx0.33+2.3\delta^2$. The $\delta$ expansion is short-ranged at long $\zeta$.

**$K^*$ and $W^*$ against $\zeta$** (run `2026-10-08-claude-b-kw-map`; hard-band class; the other classes agree in sign everywhere):

| $\zeta$ | 0.5 | 1 | 1.5 | 2 | 2.5 | 3 | 4 | 5 | 6 | 8 |
|---|---|---|---|---|---|---|---|---|---|---|
| $F_s^*$ | 0.971 | 0.890 | 0.771 | 0.635 | 0.504 | 0.396 | 0.261 | 0.227 | 0.278 | 0.494 |
| $K^*$ | −0.056 | −0.207 | −0.363 | −0.380 | −0.144 | +0.366 | +1.94 | +3.26 | +4.27 | +1.58 |
| $W^*$ | +0.005 | +0.060 | +0.209 | +0.424 | +0.622 | +0.708 | +1.06 | +0.331 | +0.014 | +4.05 |

- **Fixed bands.** $K(\zeta;T)<0$ for at least one band at every $\zeta$, so (I2) fails everywhere. At $\zeta\le2$ every band from $k_{\max}=3$ to 10 has $K<0$.
**All hard intervals** (`all_intervals.py` in run `2026-10-08-claude-b-kw-map`; 19,197 intervals holding at least 0.5% of the photons):
- $K_0<0$ for 87.5% of intervals at $\zeta\le2$, 89–90% at $\zeta=2.5$–3, and 62% at $\zeta=8$.
- The largest $K_0$ is $+0.12$ at $\zeta=0.5$ and $+1.4$ at $\zeta=2$.
- So no filter-independent sign holds even at short lengths. Every symmetric band has $K<0$ for $\zeta\le1.5$.
- Some asymmetric intervals that hold little light reach $K_0=-12$ ($\zeta=5$) and $-16$ ($\zeta=6$). Fixed-filter differences can therefore be much larger than at the optimum, in regions where $F_s$ itself is far from its minimum.

- **Walk-off at long $\zeta$.** $W$ is negative for several bands at $\zeta=6$ and 8, e.g. $-3.07$ at $\zeta=8$, $k_{\max}=6$. These values come from $\delta\zeta\ge0.6$, where the extrapolation is unreliable.

**Independent code** (run `2026-10-08-claude-b.5-solver-twomode-check`, subagent claude-b.5, same family). The solver, FastDifferentiableMMNLO with RK4IP and the discrete adjoint, ran the same model. It was blind to these numbers until its summary was hashed.
- $\Delta F$ agrees to $\le1.5\times10^{-8}$ at $\zeta=2$ and $\le6.3\times10^{-8}$ at $\zeta=5$.
- The Manakov identity holds to $3.5\times10^{-14}$.
- The full coherent Kerr tensor converges to the cross-phase model as $0.095/\kappa$, with $\kappa=\Delta\beta_0L_D$.
- RK4IP in the numpy code also reproduces the $\zeta=2$ counterexample to $10^{-6}$.

**Envelope check.** At every $\zeta$ the separately optimized difference $\min F_{\rm GRIN}-\min F_s$ at $p_2=0.2$ equals $K(T^*)\|q\|^2$ to three digits.

**Counterexample to (I1)** (run `2026-10-08-claude-b-optimum`, $\zeta=2$, $\delta=0$, $C_{22}=1/2$):

| $p_2$ | 0.3 | 0.5 | 0.75 | 0.9 |
|---|---|---|---|---|
| $\min F_{\rm GRIN}-\min F_s$ | $-2.09\times10^{-3}$ | $-7.33\times10^{-3}$ | $-1.054\times10^{-2}$ | $-7.0\times10^{-4}$ |

- These are the same in all four classes.
- At $p_2=0.75$: halving the step or the sample spacing gives $-1.054\times10^{-2}$ again, and a doubled window gives $-1.040$ to $-1.047\times10^{-2}$.
- The second-order prediction $K^*\|q\|^2$ is within 5% at $p_2=0.75$, 23% at 0.5 and 16% at 0.3.

### Mode-resolved weighted detection (beyond the common-filter class)

Run `2026-10-08-claude-b-optimum`, `mode_resolved.py` and `mode_resolved_scaling.py`. The readout is $X=w_aN_a(T_a)+w_bN_b(T_b)$ with a hard band per mode, scored by $R=\mathrm{Var}X/\sum_mw_m^2\langle N_m\rangle$.
- **Manakov control** ($p_2=0.3$). The optimum is equal weights and bands, with $R$ equal to the scalar optimum. A Manakov launch is unitarily a scalar soliton plus vacuum, so mode-specific bands act like a soft common filter and cannot help.
- **GRIN, $\zeta=2$.** $R=0.62742$ ($p_2=0.3$) and $0.56554$ ($p_2=0.75$) against LP01's 0.63475. At $p_2=0.75$ that is $-0.50$ dB, about 7 times the common-filter advantage.
- **Order.** The gain is quadratic in $\varepsilon$ (exponents 1.93–1.96 at $p_2=0.2$), with the optimal LP02 weight $\approx1-0.33\varepsilon$. The readout is not mode-symmetric, so its optimal weights move at first order; by the envelope argument the gain is still second order, with a larger coefficient.
- **$\zeta=5$.** No advantage over LP01: $+2.3\times10^{-3}$ and $+0.017$ at $p_2=0.2$ and 0.4.
- **With walk-off** (`mode_resolved_walkoff.py`), relative to LP01:
  - LP02, $\delta=0.3$, $\zeta=2$: $-0.0006$;
  - LP11, $\delta=0.59$ (GIF625 at 0.227 ps), $\zeta=2$: $+0.027$, i.e. $+0.18$ dB;
  - at $\zeta=5$: $+0.24$ and $+0.78$ dB.
  At the lab pulse width, mode-resolved detection does not rescue the GRIN launch.

## 6. What Raman would change (not derived, not computed)

- **Mean field.** If the Raman (delayed) part of the overlap tensor has the Manakov form, both the direct term $a_m\,h*(\sum_n|a_n|^2)$ and the exchange term $\sum_na_n\,h*(a_ma_n^*)$ are $U(M)$-covariant. The covariance argument (E1) then extends to the Raman mean dynamics.
- **Ideal GRIN overlaps.** The Raman overlaps equal the Kerr ones, so the γ_eff rescaling also compensates the Raman self-term in the soliton direction. The first-order null of the mean dynamics should then persist.
- **Raman noise.** Whether the Raman Langevin reservoir is $U(M)$-covariant depends on the multimode Langevin model, and was not checked. In particular, does the dark direction receive Raman noise at zeroth order only through $\bar v=O(q)$?
- **Expectation.** If it is covariant, the Raman noise enters $\Delta F$ at second order too, with a new $\zeta$-, $T$- and temperature-dependent coefficient that adds to $K$.
- **Solver caveat.** Any numerical test must use the coth Raman spectrum, not the solver default (docs/solver-upstream).

Loose end: T-20261008-claude-b-03.

## 7. Held-out tests and third-order terms

**Held-out.** Predictions were frozen in commits 8888748 and fb713de before the cases ran; results are in run `2026-10-08-claude-b-heldout`. The claim card records the scores. Summary:
- The sign and order of magnitude of every held-out $\Delta F$ are right.
- At finite defects, the third-order corrections were larger than the frozen tolerances allowed. They are about $|\Delta|$ relative to the second-order term, and the $\varepsilon\delta^2$ cross term is sizeable at $\zeta=2$.

**Post-hoc scaling** (run `2026-10-08-claude-b-thirdorder`, not frozen) measures how these corrections shrink with the defect size:
- **Off-diagonal defect $C_{12}=1-x$:** $\Delta F/(K_0\|q\|^2)$ is 1.018, 1.048, 1.112, 1.252, 1.463 for $x=0.025,0.05,0.1,0.2,1/3$ ($\zeta=2$, $p_2=0.2$; nearly the same at $p_2=0.3$). Ratio − 1 shrinks with exponent 1.2–1.5 and extrapolates to within about 1% of 1.
- **Diagonal defect:** ratio 1.011, 1.034, 1.078 for $\varepsilon=1/16,1/8,1/4$ ($p_2=0.3$).
- **At $\zeta=5$** the ratios approach about 1.02. That matches a 2% bias of $K_0$, which was extrapolated from $p_2=0.1,0.2$: the small-$p_2$ value is 3.325, against the extrapolated 3.260.
- **Cross term** at $\zeta=2$, $\delta=0.3$, $p_2=0.3$: $\Delta F(\varepsilon,\delta)-\Delta F(\varepsilon,0)-\Delta F(0,\delta)=-5.5,-11.2,-22.9\times10^{-4}$ for $\varepsilon=1/8,1/4,1/2$. That is linear in $\varepsilon$ (exponent 1.02), about $-1.15\,\varepsilon\delta^2p_1^2p_2^2$.

So the universal second-order form holds asymptotically, and the misses come from third-order terms of relative size about $|\Delta|$.

**Zero crossing of $K^*$** (`crossing.py` in run `2026-10-08-claude-b-kw-map`, $\zeta=2.5$–3 in steps of 0.1):
- $K^*=-0.144,-0.063,+0.029,+0.132,+0.245,+0.366$.
- The crossing is at $\zeta_c=2.67$ (hard band and interval) and 2.66 (fractional edge).

## 8. Answer to the PI's question, within the stated model

- **"GRIN can never beat LP01-only" is false**, both at a fixed filter and at the optimal filter, in the pure-Kerr cross-phase model.
  - **Fixed filter.** It fails at every length studied.
  - **Optimal filter.** It fails at $\delta=0$ for $\zeta<\zeta_c\approx2.67$. The converged counterexample is $\zeta=2$, $p_2=0.75$: $-1.05\times10^{-2}$ in $F$.
- **Why it can fail.** The Manakov point is a stationary point of $F$ in overlap space (first-order null). So the GRIN–LP01 difference is a second-order quantity with a sign set by the universal coefficient $K^*(\zeta)$, which changes sign at $\zeta_c$.
- **Narrowed inequality.** For two-mode GRIN LP02 the advantage is at most about $|K^*_-|\varepsilon^2\max(p_1p_2^3)\approx10^{-2}$ in $F$ (about 0.07 dB). Walk-off removes it for $\delta>\delta_c=\varepsilon p_2\sqrt{-K^*/W^*}$.
- **In GIF625 at 1550 nm**, where the two-mode model holds ($\delta\gtrsim0.56$ for LP02), the remaining advantage is at most about 0.3% in $F$, which is not measurable. Walk-off dominates and makes the GRIN launch worse: about +0.2 dB for a 70/30 LP11 launch at the lab's 0.227 ps pulse.
