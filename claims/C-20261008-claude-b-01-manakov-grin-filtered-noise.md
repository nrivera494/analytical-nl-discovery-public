---
id: C-20261008-claude-b-01
problem: P-20261004-root-03
title: "Filtered soliton noise of a GRIN multimode launch differs from LP01 only at second order, through two universal coefficients; 'GRIN never beats LP01' is false but violated by at most about 1.7% in F"
type: noise-formula
status: proposed
proposed_by: claude-b
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-08
updated: 2026-10-08
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: null
---

## Statement

**Model ($\mathcal M$).** $M$ modes with fields $a_m(\zeta,\tau)$ in soliton units ($\tau=T/T_0$, $\zeta=z/L_D$), obeying the cross-phase-only NLS
$$i\partial_\zeta a_m+i\delta_m\partial_\tau a_m+\tfrac12\partial_\tau^2a_m+\Big(\sum_nC_{mn}|a_n|^2\Big)a_m=0,\qquad C=J+\Delta .$$
- $J$ is the all-ones matrix (the Manakov case), $\Delta$ is real symmetric, and $\delta_m=\Delta\beta_{1,m}T_0/|\beta_2|$ is the walk-off against LP01.
- Ideal parabolic-GRIN overlaps:
  - LP01/LP02: $\Delta=\mathrm{diag}(0,-\tfrac12)$;
  - LP01/LP11a: $\Delta=\mathrm{diag}(0,-\tfrac14)$;
  - LP01/LP02/LP11a: $C=\begin{pmatrix}1&1&1\\1&1/2&1/2\\1&1/2&3/4\end{pmatrix}$ (exact Laguerre–Gauss integrals).

**Launch.** Common sech at the $\gamma_{\rm eff}$ energy: $a_m(0)=\sqrt{p_m}\,\mathrm{sech}\,\tau/\sqrt{p^TCp}$, with photon fractions $p_m$ and $\sum p_m=1$. This is an evolving near-soliton; radiation is included.

**Readout.** Any spectral transmission $T(\omega)\in[0,1]$, the same for every mode, followed by counting all modes, with the filter's loss-port vacuum included.
- $F(T)$ is the linearized Fano factor for coherent input; $F_s(T)$ is the LP01-only soliton at the same $\zeta$.
- The comparison is at equal $\zeta$, each launch at its own soliton energy.
- With equal photon numbers instead, the soliton direction has order $N^2=\Sigma<1$, and $F$ follows the scalar at that order.
  - Run `2026-10-08-claude-b-normalization`, $\zeta=2$, best band: $p_2=0.3$ gives $0.6850$ against the scalar at $N^2=\Sigma$, $0.6874$, and LP01 at $N=1$, $0.6347$.
  - $p_2=0.75$ gives $0.9002$ against $0.9173$ and $0.6347$.
  - That comparison measures the energy mismatch rather than the mode physics, which is why the $\gamma_{\rm eff}$ energy is used.

**Invariants.** With $c=\sqrt p$ and $P_\perp=1-cc^T$: $q=P_\perp\,\mathrm{diag}(c)\,\Delta\,p$ and $r=P_\perp\,\mathrm{diag}(\delta)\,c$.
- Two modes: $\|q\|^2=p_1p_2[\Delta_{12}(p_1-p_2)+\Delta_{22}p_2-\Delta_{11}p_1]^2$ and $\|r\|^2=\delta^2p_1p_2$.
- GRIN LP01/LP02: $\|q\|^2=\varepsilon^2p_1p_2^3$ with $\varepsilon=\tfrac12$.

**Claim.**

1. **Exact.**
   - $\Delta=0$ and $\delta=0$ give $F(T)=F_s(T)$ for every $T$ and $p$. This follows from $U(M)$ covariance and holds beyond linearization in the Kerr model.
   - $F(\delta;T(\omega))=F(-\delta;T(-\omega))$ (parity).
2. **Exact, linearized: first-order null.** At $\delta=0$, $F(T)-F_s(T)$ has no term linear in $\Delta$, for any $M$, $p$, $\zeta$ and $T$. The same argument covers interference with a coherent copy of the input, whose readout gradient lies in the soliton direction; this case was argued but not computed.
3. **Second order.** For symmetric $T$,
   $$F(T)-F_s(T)=K(\zeta;T)\,\|q\|^2+W(\zeta;T)\,\|r\|^2+O(3).$$
   $K$ and $W$ depend only on $\zeta$ and $T$, not on $M$, $p$, or which entries of $\Delta$ are nonzero. For a filter class $\mathcal T$ with LP01 optimum $T^*$,
   $$\min_{\mathcal T}F-\min_{\mathcal T}F_s=K^*\|q\|^2+W^*\|r\|^2+O(3),\qquad K^*=K(\zeta;T^*),\ W^*=W(\zeta;T^*).$$
4. **Numerical: sign structure** (run `2026-10-08-claude-b-kw-map`; classes: hard symmetric band, fractional edge, any interval, any transmission).
   - $K^*<0$ for $\zeta<\zeta_c$ and $K^*>0$ for $\zeta_c<\zeta\le8$, with $\zeta_c=2.67$ (2.66 for the fractional-edge class).
   - Hard-band values of $K^*$:

     | $\zeta$ | 0.5 | 1 | 1.5 | 2 | 2.5 | 2.6 | 2.7 | 3 | 4 | 5 | 6 | 8 |
     |---|---|---|---|---|---|---|---|---|---|---|---|---|
     | $K^*$ | −0.056 | −0.207 | −0.363 | −0.380 | −0.144 | −0.063 | +0.029 | +0.37 | +1.9 | +3.3 | +4.3 | +1.6 |

   - All classes agree in sign at every $\zeta$. For $\zeta\le2.5$ they share the same LP01 optimum.
   - $W^*>0$ for $\zeta\le5$ (from $+0.005$ at $\zeta=0.5$ to $+1.06$ at $\zeta=4$) in the classes whose LP01 optimum is symmetric: hard band and fractional edge at every $\zeta$, interval at every $\zeta$ except 4 and 8. At $\zeta=6$, $|W^*|\le0.03$ and its sign is not established.
   - Where the optimum is asymmetric (interval class at $\zeta=4,8$, and the free-transmission class), $F$ has a term linear in $\delta$ and the even-in-$\delta$ coefficient $W^*$ is not the right description. Those $W$ values in run `2026-10-08-claude-b-kw-map` should not be used.
5. **Consequences.**
   - **(I2) is false at every $\zeta$ studied (0.5–8).** (I2) is $F_{\rm GRIN}(T)\ge F_s(T)$ at a fixed filter. Some hard band has $K(\zeta;T)<0$ at each $\zeta$.
     - Example away from the $\zeta<\zeta_c$ window: $\zeta=5$, band $|k|\le2$, GRIN LP01/LP02 with $p_2=0.1,0.2,0.4$ gives $F_{\rm GRIN}-F_s=-1.2\times10^{-4},-6.9\times10^{-4},-3.0\times10^{-3}$ (run `2026-10-08-claude-b-exponents`).
   - **(I1) at $\delta=0$ is false for $\zeta<\zeta_c=2.67$.** (I1) is $\min_TF_{\rm GRIN}\ge\min_TF_s$.
     - Converged counterexample (run `2026-10-08-claude-b-optimum`): $\zeta=2$, GRIN LP01/LP02, $p_2=0.75$, $\delta=0$ gives $\min F_{\rm GRIN}=0.62420$ against $\min F_s=0.63475$.
     - The difference is $-1.05\times10^{-2}$ ($-0.073$ dB), identical in all four classes.
   - **(I1) holds at second order for $\zeta_c<\zeta\le8$.**
   - **Narrowed inequality** (two-mode GRIN LP02, on the sampled $\zeta\le8$):
     $$\min_TF_{\rm GRIN}\ge\min_TF_s-|K^*_-|\,\varepsilon^2p_1p_2^3+O(3),\qquad K^*_-=\min(K^*,0)\ge-0.38 .$$
     - Since $\varepsilon^2p_1p_2^3\le0.0264$, the GRIN advantage at the optimum is at most about $10^{-2}$ in $F$.
     - The direct maximum found is $1.05\times10^{-2}$ (1.7%, 0.073 dB) at $\zeta=2$, $p_2=0.75$.
   - **Walk-off:** for $\zeta<\zeta_c$ the advantage survives only for $\delta<\delta_c=\varepsilon p_2\sqrt{-K^*/W^*}$, which is $1.86,\ 1.32,\ 0.95,\ 0.48$ times $\varepsilon p_2$ at $\zeta=1,1.5,2,2.5$. There all classes share the symmetric hard-band optimum.

6. **Numerical, beyond the common-filter readout: mode-resolved weighted detection.** The readout is $X=w_aN_a(T_a)+w_bN_b(T_b)$ with a hard band per mode, scored by $R=\mathrm{Var}X/\sum_mw_m^2\langle N_m\rangle$ (run `2026-10-08-claude-b-optimum`, `mode_resolved.py` and `mode_resolved_scaling.py`).
   - *Manakov control.* At $p_2=0.3$ the best choice is equal weights and equal bands, giving exactly the scalar optimum (0.634746).
   - *GRIN, $\zeta=2$, $\delta=0$.* Best $R=0.62742$ ($p_2=0.3$) and $0.56554$ ($p_2=0.75$; bands $k_{\max}=4,6$, LP02 weight 0.49), against LP01's 0.63475. That is $-0.069$ in $R$ ($-0.50$ dB), about 7 times the common-filter advantage.
   - *Order.* The gain is still second order in the overlap defect: $\propto\varepsilon^{1.93\text{–}1.96}$ at $p_2=0.2$, with optimal weights shifting linearly in $\varepsilon$.
   - *$\zeta=5$.* Mode resolution reduces the GRIN penalty but does not beat LP01: $+2.3\times10^{-3}$ at $p_2=0.2$ and $+0.017$ at $p_2=0.4$.
   - *Walk-off* (`mode_resolved_walkoff.py`, stored covariances of H4 and H5; bands centred on the launch carrier): the advantage is gone.
     - LP02, $\delta=0.3$, $\zeta=2$: $-0.0006$ ($-0.004$ dB).
     - LP11 at the lab pulse ($\delta=0.59$), $\zeta=2$: $+0.027$ ($+0.18$ dB).
     - Both at $\zeta=5$: $+0.24$ and $+0.78$ dB.
   - *Not covered:* optimized per-mode filters, including carrier-following ones (T-20261008-claude-b-05).

## Regime

- **Small parameters:** $\|q\|$ and $\|r\|$. Third-order terms are $O(\|q\|^2|\Delta|)$, $O(\|r\|^2|\Delta|)$ and $O(\|r\|^2\delta^2)$.
- **Measured third-order corrections** (runs `2026-10-08-claude-b-exponents`, `-kw-map`, `-thirdorder`). The ratio $\Delta F/(K_0\|q\|^2)$ tends to 1 as the defect goes to 0, and the deviation shrinks roughly linearly with the defect.
  - *Off-diagonal defect $\Delta_{12}=-x$:* ratio $1+1.2x$ at $\zeta=2$, i.e. 1.018, 1.048, 1.11, 1.25, 1.46 for $x=0.025$–1/3 ($p_2=0.2$). At $\zeta=5$ it is about $1.02+0.9x$; the 0.02 offset is the bias of the $K_0$ extrapolation there.
  - *Diagonal defect:* the ratio is 1.011, 1.034, 1.078 for $\varepsilon=1/16,1/8,1/4$ ($p_2=0.3$, $\zeta=2$). For GRIN, $K_{\rm eff}$ is $-0.383,-0.401,-0.423,-0.458$ at $p_2=0.025,0.1,0.2,0.4$.
  - *Cross term:* $\Delta F(\varepsilon,\delta)-\Delta F(\varepsilon,0)-\Delta F(0,\delta)\approx-1.15\,\varepsilon\delta^2p_1^2p_2^2$ at $\zeta=2$; measured exponent in $\varepsilon$: 1.02.
  - *Walk-off:* $W_{\rm eff}$ changes by less than 1% for $\delta\le0.4$ at $\zeta=2$. At $\zeta=5$, $W\approx0.33+2.3\delta^2$.
- **Asserted domain for 10% accuracy of the second-order form:** $0.5\le\zeta\le5$; off-diagonal $|\Delta|\lesssim0.08$; diagonal $\varepsilon p_2\lesssim0.1$; $\delta\lesssim0.4$ for $\zeta\le2.5$ and $\delta\lesssim0.12$ at $\zeta=5$.
- The sign statements in item 4 and the counterexample do not need this accuracy. The sign statements also cover $\zeta=6,8$, where the coefficient values are less accurate ($K$ extrapolation spread up to 25%).
- **Physical domain of $\mathcal M$ in ideal GIF625 at 1550 nm** (run `2026-10-08-claude-b-gif625-fwm-mismatch`):
  - LP01+LP02: the l = 0 mixing 02+02 → 01+03 has $|\Delta\beta|L_D=912\,T_0^2$ ($T_0$ in ps), and $\delta_{\rm LP02}=5.37\,T_0$. $\mathcal M$ needs $|\Delta\beta|L_D\gtrsim10$, i.e. $\delta_{\rm LP02}\gtrsim0.56$.
  - LP01+LP11a: 11+11 → 01+21 has $227\,T_0^2$, and $\delta_{\rm LP11}=2.59\,T_0$, i.e. $\delta_{\rm LP11}\gtrsim0.54$.
  - Inside these domains, the second-order formula gives a largest GRIN advantage at the optimum of $2.4\times10^{-3}$ in $F$ (0.26%, LP02 at $\zeta=1$, $p_2\approx0.84$, $\delta=0.56$) and $1.4\times10^{-4}$ for LP11 (`domain_bound.py` in run `2026-10-08-claude-b-kw-map`).
  - The LP02 point has $\varepsilon p_2=0.42$, outside the asserted domain, so read it as "about 0.3%". It is not a measurable advantage.

## Assumptions

1. Cross-phase-only coupling: every intermodal four-wave-mixing term is phase-mismatched and averaged out (see Regime for GIF625).
   - The model is the $\kappa=\Delta\beta_0L_D\to\infty$ limit of the full Kerr tensor. The solver run `2026-10-08-claude-b.5-solver-twomode-check` measures the residual of the averaged coherent terms as $\approx0.095/\kappa$ in $F$ ($\zeta=2$, $p_2=0.3$, $k_{\max}=5$; local exponent $-1.000$).
   - In ideal GIF625 at $T_0=0.227$ ps, $\kappa=2.2\times10^4$ (LP02) and $1.1\times10^4$ (LP11) (run `2026-10-08-claude-b-gif625-fwm-mismatch`). That gives $\lesssim10^{-5}$ in $F$.
   - Degenerate-group mixing (02+02 ↔ 21+21) is phase-matched, but for an axisymmetric launch it decouples from the $l=0$ fluctuations at linear order.
2. Equal $\beta_2$ in all modes; no $\beta_3$; no self-steepening. In the solver run, self-steepening changes $F$ by $\approx0.8/(\omega_0T_0)^2$, i.e. $5\times10^{-7}$ at $T_0=1$ ps and about $10^{-5}$ at $T_0=0.227$ ps (1550 nm).
3. No Raman: neither the delayed response nor its reservoir. What Raman changes is discussed in the note, but not derived.
4. Linearized (Gaussian) quantum fluctuations with coherent-state input.
5. Common sech launch at the $\gamma_{\rm eff}$ energy, not a stationary vector soliton.
6. Ideal parabolic-profile overlaps for the GRIN cases. No random mode coupling.
7. One passive spectral filter applied to all modes, then counting all modes.
8. Numerical: a $40\,T_0$ window with 256 points.
   - Halving the step or the sample spacing changes the optimum difference by less than $10^{-6}$.
   - Doubling the window changes the absolute optimum $F$ by 0.17% for both launches and their difference by 1.3% (run `2026-10-08-claude-b-optimum`).

## Predictions

Frozen before the held-out cases were computed: H1–H5 in commit 8888748 (`runs/2026-10-08-claude-b-heldout/predictions.json`) and H6–H7 in commit fb713de (`predictions_m3.json`).
- **Method.** $\Delta F(T)=K_0(\zeta;T)\|q\|^2+W_0(\zeta;T)\|r\|^2$ at $\zeta=2$ and 5, for the hard bands $k_{\max}=3..7$ and the LP01 class optima. $K_0$ and $W_0$ come only from the GRIN-$C_{22}$ and Manakov-walk-off runs of `2026-10-08-claude-b-kw-map`.
- **Pass criterion.** $|\text{actual}-\text{predicted}|\le\text{tol}\cdot|\text{predicted}|$ for every filter.

| Case | Structure (not used to build $K$, $W$) | $p$ | $\delta$ | tol |
|---|---|---|---|---|
| H1 | $C_{12}=0.9$ (off-diagonal defect, $\|q\|^2\propto p_1p_2(p_1-p_2)^2$) | $p_2=0.3$ | 0 | 15% |
| H2 | $C_{12}=2/3$ (polarization pair in a PM fiber, cross-phase only) | $p_2=0.2$ | 0 | 25% |
| H3 | LP11a, $C_{22}=3/4$ | $p_2=0.3$ | 0 | 15% |
| H4 | GRIN LP02 with walk-off (additivity, no cross term) | $p_2=0.3$ | 0.3 | 20% |
| H5 | GIF625 LP01+LP11a at $T_0=0.227$ ps (1550 nm) | $p_2=0.3$ | 0.588 | 20% |
| H6 | three modes LP01/LP02/LP11a | (0.6, 0.2, 0.2) | 0 | 25% |
| H7 | three modes LP01/LP02/LP11a | (0.4, 0.3, 0.3) | 0 | 25% |

Sample frozen values at $\zeta=2$, LP01-optimal band $k_{\max}=5$, in units of $10^{-3}$:
- H1: $-0.128$; H2: $-2.43$; H3: $-0.449$;
- H4: $+6.22$; H5: $+30.4$;
- H6: $-2.89$; H7: $-6.60$.

**Lab-facing prediction (H5).** In GIF625 at 1550 nm ($T_0=0.227$ ps, $L=2L_D=3.67$ m), a 70/30 LP01/LP11a launch raises the minimum all-mode bandpass Fano factor above the LP01-only value by $\approx0.030$, i.e. about +0.2 dB at $F_s=0.635$, within model $\mathcal M$.

**Scores** (runs `2026-10-08-claude-b-heldout`, `summary.json` and `summary_m3.json`). Ratio actual/predicted at the LP01-optimal hard band, then the worst relative error over all listed filters against the frozen tolerance:

| Case | $\zeta=2$ | $\zeta=5$ | worst rel. error | frozen verdict |
|---|---|---|---|---|
| H1 | 1.10 | 1.12 | 0.195 (tol 0.15) | **fail** (edge bands $k_{\max}=3$ at $\zeta=2$, $6,7$ at $\zeta=5$) |
| H2 | 1.46 | 1.30 | 0.52 (tol 0.25) | **fail** |
| H3 | 1.08 | 1.05 | 0.25 (tol 0.15) | **fail** ($k_{\max}=3$ at $\zeta=2$) |
| H4 | 0.60 | 0.96 | 0.85 (tol 0.20) | **fail** at $\zeta=2$, pass at $\zeta=5$ |
| H5 | 0.89 | 2.63 | 1.68 (tol 0.20) | **pass** at $\zeta=2$; **fail** at $\zeta=5$ ($\delta\zeta=2.9$) |
| H6 | 1.19 | 1.14 | 0.58 (tol 0.25) | **fail** (edge bands) |
| H7 | 1.25 | 1.43 | 0.78 (tol 0.25) | **fail** |

- **What held.** The sign of $\Delta F$ was right in every case and filter, except H5 at $\zeta=5$, $k_{\max}=6$. The magnitudes were within a factor 1.8.
- **What failed.** The frozen tolerances assumed small third-order terms. In fact:
  - the off-diagonal correction is $\approx+1.2|\Delta|$ (H1, H2, H6, H7);
  - the $\varepsilon\delta^2$ cross term is $\approx-1.15\,\varepsilon\delta^2p_1^2p_2^2$ (H4 at $\zeta=2$);
  - the $\delta^4$ term is large at $\zeta=5$ (H5).
- **Not a refutation of the second-order form.** That form is asymptotic, and the post-hoc run `2026-10-08-claude-b-thirdorder` shows the ratio tends to 1 as the defects shrink. But the quantitative predictions at these finite defects failed as frozen.

## Derivation

See `explorations/2026-10-08-claude-b-manakov-grin-inequality.md` (U(M) covariance; rotated soliton/dark basis; block structure of the linearized propagator; isotropy of the dark subspace; envelope argument).

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Dimensionless soliton units; $F$ is independent of photon number in linearized theory | claude-b (claude) | — | 2026-10-08 |
| Known limits | Manakov identity: per-bin covariance equals the scalar one to $4\times10^{-9}$ ($M=2,3$). Shot noise at $\zeta\to0$. Round-1 values reproduced to $1.8\times10^{-10}$ | claude-b (claude) | 2026-10-08-claude-b-grin-manakov-lib | 2026-10-08 |
| Symmetries | Odd part of $\Delta F$ in $\varepsilon$ scales as $\varepsilon^{3.00}$ (no linear term); even part as $\varepsilon^{1.99}$. Parity $F(\delta;T(\omega))=F(-\delta;T(-\omega))$ holds to $2.7\times10^{-9}$ (symmetric and asymmetric bands). $W$ independent of $p$ within 0.6% at $\zeta=2$ | claude-b (claude) | 2026-10-08-claude-b-exponents | 2026-10-08 |
| Symbolic residual | Not done | | | |
| Simulation, core regime | $K$, $W$ maps for $\zeta=0.5$–8; the envelope prediction matches the separately optimized difference to 3 digits | claude-b (claude) | 2026-10-08-claude-b-kw-map | 2026-10-08 |
| Error-scaling exponent | $\Delta F/p_1$ against $p_2$: exponent 2.99 → 3 at $\zeta=2$ ($K_{\rm eff}$ flat to 1.6% for $p_2\le0.05$). $\Delta F$ against $\delta$: 2.000 at $\zeta=2$. Post hoc: (ratio − 1) shrinks with the defect, exponent 1.2–1.5 (off-diagonal, $\zeta=2$); cross term linear in $\varepsilon$ (exponent 1.02) | claude-b (claude) | 2026-10-08-claude-b-exponents, 2026-10-08-claude-b-thirdorder | 2026-10-08 |
| Held-out region | **Failed as frozen** in H1, H2, H3, H4 ($\zeta=2$), H5 ($\zeta=5$), H6, H7; passed in H4 ($\zeta=5$) and H5 ($\zeta=2$, the GIF625 LP11 lab case). Signs right everywhere except one band in H5 at $\zeta=5$. Third-order terms were larger than the frozen tolerances (see Predictions) | claude-b (claude) | 2026-10-08-claude-b-heldout | 2026-10-08 |
| Convergence and artefacts | Counterexample stable under halved step and sample spacing ($<10^{-6}$) and doubled window (1.3%). An RK4IP integrator gives $-1.05441\times10^{-2}$ at $h=4\times10^{-3}$ and $2\times10^{-3}$, against split step $-1.0544\times10^{-2}$. FD Jacobian checked against the rotation formulas to $10^{-9}$ | claude-b (claude) | 2026-10-08-claude-b-optimum | 2026-10-08 |
| Second solver or relaxed assumption | Independent code: FastDifferentiableMMNLO with RK4IP and the discrete adjoint, by subagent claude-b.5 (same family, blind to the numpy numbers until its summary was hashed). Manakov identity to $3.5\times10^{-14}$. $\Delta F$ agrees with the numpy code to $\le1.5\times10^{-8}$ at $\zeta=2$ ($p_2=0.1,0.2,0.3$, five bands) and $\le6.3\times10^{-8}$ at $\zeta=5$. Its $F$ is converged to $\sim10^{-12}$ in step, $N_t$ and $\Delta\beta_0$. Relaxed assumption: the full coherent Kerr tensor converges to this model as $0.095/\kappa$ | claude-b.5 (claude) | 2026-10-08-claude-b.5-solver-twomode-check | 2026-10-08 |
| Adversarial audit | | | | |
| Novelty search | Bounded search; titles only, no full texts read. OpenAlex, 2026-10-08, first 10–15 titles of each: "squeezing vector soliton non-integrable cross-phase modulation Manakov perturbation", "quantum noise multimode soliton graded-index fiber squeezing", "photon-number squeezing spectral filtering vector soliton two-component", "quantum theory Manakov soliton noise cross-phase modulation coefficient birefringent fiber squeezing", "multimode soliton quantum noise Fano factor mode overlap". No work found that compares the filtered photon-number noise of an unequal-overlap (non-Manakov) launch with the Manakov/scalar value. The closest are already on the card: Rand, Steiglitz & Prucnal 2005 (Manakov homodyne, DOI 10.1103/PhysRevA.71.053805) and Konyukhov 2025 (arXiv:2412.09208). Absence is not proven | claude-b (claude) | — | 2026-10-08 |

## Outcome

Open, status `proposed`.
- **Needs a non-Claude verifier.** All work is by the Claude family, including the solver cross-check by subagent claude-b.5.
- **Held-out record.** The quantitative held-out predictions failed at their frozen tolerances (see Predictions). The exact statements (items 1–2), the sign structure (item 4) and the counterexample (item 5) do not depend on them.
- **Expected verifier focus:**
  - the counterexample at $\zeta=2$ with an independent code;
  - the sign change of $K^*$ near $\zeta_c=2.67$;
  - the first-order null (odd part $\propto\varepsilon^3$).
