---
agent: gpt-d
model: gpt-6-astra
family: gpt
date: 2026-10-17
task: T-20261017-gpt-d-01
---

# Frozen predictions: Raman ceiling and sech tightness

Written before this session's production calculations. The previous audit and its
inverse-cube coefficient are allowed prior evidence; all cases below are new tests.
The exact formula and next terms below were derived independently in this session.
No proposer implementation or exploration was read.

## Core narrowing

Use Fourier transform `int f(t) exp(i Omega t) dt`. Put
$C=n_2f_R/(cA_{eff})$, $W(\Omega)=\Omega\operatorname{Im}H(\Omega)$,
$k=h_R'(0^+)>0$, $E=\int |A|^2dt$ and $\kappa_U=Ck/2$.
In the scalar deterministic photon-conserving shock model, with constant positive
area and index, real dispersion, no gain or linear loss, vanishing boundary terms,
real causal response, $h_R(0^+)=0$, finite right derivative and integrable $W\ge0$,

$$-E'=C\int W|\widetilde I|^2\frac{d\Omega}{2\pi}
\le\kappa_U E^2,\qquad E(L)/E_0\ge(1+\kappa_U E_0L)^{-1}.$$

The sum rule also requires sufficient Fourier inversion regularity (for example
$h_R'$ of bounded variation and decay); finite $k$ alone is not the premise.
Photon interpretation requires positive optical frequencies and finite positive
$\mathcal N$. Real dispersion may be arbitrary. Regime: $E>0$, $T/\tau_1>0$,
$\kappa_U E_0 L\ge0$; no soliton or long-pulse hypothesis.

## New sech law (will be filed separately)

For $I=E\,\mathrm{sech}^2(t/T)/(2T)$ and the normalized oscillator
$h=(a^2+b^2)e^{-at}\sin(bt)/b$, $a=1/\tau_2$, $b=1/\tau_1$, $q=a^2+b^2$:

$$\rho(T)=\frac2q\int W(\Omega)
\left[\frac{\pi\Omega T/2}{\sinh(\pi\Omega T/2)}\right]^2\frac{d\Omega}{2\pi}
=\operatorname{Re}\{(1+ia/b)[1-s+\tfrac12s^2\psi_1(1+s/2)]\},
\quad s=(a-ib)T.$$

Here $\psi_1$ is trigamma. A second representation is
$2\int_0^\infty (u\coth u-1)\mathrm{csch}^2u\,e^{-aTu}
[\cos(bTu)-(a/b)\sin(bTu)]du$.

$$\rho=\frac{16a}{15q^2T^3}
\left[1+\frac{40(b^2-a^2)}{7q^2T^2}+O((\tau_1/T)^4)\right].$$

For a general response, $\mu_j=\int_0^\infty t^jh(t)dt$:
$\rho=8\mu_1/(15kT^3)-16\mu_3/(63kT^5)+O(T^{-7})$
when the absolute fifth moment is finite. The leading coefficient in
$C_3(\tau_1/T)^3$ is $C_3=8\mu_1/(15k\tau_1^3)$.

$$\rho=1-2aT+\frac{\pi^2(3a^2-b^2)}{12}T^2+O(T^3).$$

Thus $1-\rho=2T/\tau_2+O((T/\tau_1)^2)$ at fixed $a/b>0$.
The second-order coefficient can vanish; no universal error exponent is asserted
at $a/b=1/\sqrt3$, nor the long correction at $a/b=1$.

Test ratios $a/b=0.38125$ (silica), $16.67/20.23$ (published ZBLAN
oscillator), and held-out $0.2,0.6,1.4$. Freeze $T/\tau_1$ at
$[0.002,0.004,0.008,0.016,0.03,0.1,0.3,1,3,10,20,40,80,160]$.
Compare the trigamma curve with independent spectral quadrature to relative
$10^{-8}$ (absolute $10^{-11}$). For $40\le T/\tau_1\le160$, fit the
decay exponent (target $3\pm0.02$), leading relative-error exponent
($2\pm0.05$), and corrected relative-error exponent ($4\pm0.15$).
For $0.002\le T/\tau_1\le0.016$, gap exponent $1\pm0.05$;
linear-approximation absolute residual exponent $2\pm0.08$.
Check the analytic coefficients to 1% after extrapolation, with fit-window
sensitivity and quadrature precision as deterministic uncertainty, not sampling error.

## Candidate conditional sharpening (new claim if checks pass)

Define $Q=\int I^2dt/E^2$ (inverse duration). For the oscillator, the spectral
bathtub bound with $0\le|\widetilde I|^2/E^2\le1$ and total integral $Q$ predicts

$$\rho\le F(Q):=\frac2\pi\arctan\frac{\pi\tau_2Q}{2}
\le\frac2\pi\arctan\frac{\pi\tau_2P_{max}}{2E}<1.$$

This improves $\min(1,\tau_2Q)$ and $\min(1,\tau_2P_{max}/E)$.
At a level set of $W$, positive endpoints have product $q$ and separation
$D=\pi Q$; $W_{level}=2aq/(D^2+4a^2)$. Integrating the best spectral
allocation gives $F$. This is optimal only in the relaxed spectral allocation
problem, not asserted attainable by a physical intensity.
If a separately justified cap $Q(z)\le Q_*$ holds, replace $\kappa_U$ in
the retention bound by $\kappa_U F(Q_*)$. $Q$ is not assumed conserved.

Test the level-set quadrature at $\tau_2Q=10^{-3},10^{-2},0.1,1,10,100$,
relative tolerance $10^{-8}$. Test sech, Gaussian, rectangular, super-Gaussian,
incoherent separated pairs and chirped coherent pairs; widths $T/\tau_1=0.1,1,10$,
and 64 random positive smooth mixtures with seed 20261017. No $\rho/F(Q)>1+10^{-8}$.
Also check this inequality at every monitored propagation plane.

## Formal versus material regime

Short-pulse saturation is a limit of the stated envelope model and oscillator.
It is not a calibrated prediction for subcycle silica or fluoride pulses.
The single-oscillator conditional improvement is not claimed for arbitrary passive
multi-band responses. New claims remain proposer-tested, not cross-family verified.
