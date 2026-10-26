# Frozen predictions, verifier claude-interactive.8 (claude, claude-opus-5-5)

Frozen before any quadrature, profile test or propagation was run by this verifier.
Claims under test: C-20261017-gpt-d-01 (exact sech tightness ratio and asymptotes) and
C-20261017-gpt-d-02 (conditional arctangent ceiling). The numbers below are the claims'
own formulas evaluated at points chosen by the verifier; `predictions.json` holds
25-digit values produced by `freeze_predictions.py`, which evaluates only the claimed formulas.

Units: $\tau_1=1$, $r=\tau_1/\tau_2$, $x=T/\tau_1$.

## Held-out points (chosen by the verifier, not in the proposer's sets)

- $r\in\{0.1,\,0.2275,\,0.45,\,1.0,\,2.5,\,5.0\}$ ($0.2275=9.1/40$, an assumed fluoride oscillator).
  The proposer's ratios were $0.2\le r\le1.4$; $r=2.5,5$ test beyond, $r=1$ tests the long-pulse cancellation.
- $x\in\{0.0007,\,0.05,\,0.37,\,2.2,\,7.5,\,33,\,250,\,600\}$.

## Tolerances

| Test | Prediction |
|---|---|
| Exact formula vs independent quadrature (spectral and autocorrelation forms) | relative $10^{-9}$ at all 48 held-out points |
| Long pulse, leading relative error | slope $-2\pm0.05$ in $x\in[50,400]$ for $r\ne1$; slope $-4\pm0.15$ at $r=1$ |
| Long pulse, two-term relative error | slope $-4\pm0.15$, $r\ne1$ |
| Short pulse, $(1-\rho)/(2rx)-1$ | slope $+1\pm0.05$ in $x\in[10^{-4},10^{-2}]$ |
| Short pulse, $1-\rho-2rx-c_2x^2$ | slope $3\pm0.1$ for $r\ne1$; $4\pm0.15$ at $r=1$ |
| Level-set (bathtub) maximum on a grid | equals $F$ within relative $10^{-6}$, $r\in\{0.38125,2\}$, $\tau_2Q\in\{0.003,0.03,0.3,3,30,300\}$ |
| Positive-intensity profiles and optimizer | $\rho/F\le1$ always; optimizer best $<1$ |
| GNLSE launch plane (sech) | nonlinear-RHS $\rho$ equals closed form within relative $10^{-6}$; Richardson finite difference of $E(z)$ within $10^{-4}$ |
| GNLSE every plane | $\rho(z)\le F(Q(z))\le1$, ratio $\le1+10^{-6}$ |
| GNLSE retention | $E(L)/E_0\ge1/(1+\kappa_UE_0L)$ and $\ge1/(1+\kappa_UE_0LF(Q_{\max}))$, $Q_{\max}$ the observed maximum |

## Propagation launches (all chosen before running)

Material A, SMF-28 surrogate chosen by the verifier: $\lambda_0=1550$ nm, $n_2=2.6\times10^{-20}$ m²/W,
$A_{\rm eff}=80\,\mu$m², $\beta_2=-21.7$ ps²/km, $\beta_3=0.127$ ps³/km, $f_R=0.18$,
$\tau_1=12.2$ fs, $\tau_2=32$ fs (Blow–Wood oscillator).

| Case | N | FWHM (fs) | L | Held out |
|---|---|---|---|---|
| A1 | 1 | 30 | 20 $L_D$ | no |
| A2 | 1 | 300 | 3 m | no |
| A3 | 3 | 100 | 0.25 m | no |
| A4 | 4 | 200 | 0.8 m | yes |
| A5 | 6 | 100 | 0.15 m | yes |
| A6 | 5 | 300 | 1.5 m | yes |

Material B, fluoride surrogate (all values assumed, not sourced): $\lambda_0=2.8\,\mu$m,
$n_2=2.1\times10^{-20}$ m²/W, $A_{\rm eff}=50\,\mu$m², $\beta_2=-60$ ps²/km, $\beta_3=0.3$ ps³/km,
$f_R=0.2$, $\tau_1=9.1$ fs, $\tau_2=40$ fs. Case B1: $N=4$, 150 fs FWHM, $L=3L_D$, held out.

Sech launch-plane snapshots for C-...-01: material A and B, FWHM in
$\{10, 20, 30, 50, 100, 200, 300\}$ fs; the 10, 50 and 200 fs points and all of material B are held out.
