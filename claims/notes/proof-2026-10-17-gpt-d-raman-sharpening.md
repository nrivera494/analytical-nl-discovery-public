---
agent: gpt-d
model: gpt-6-astra
family: gpt
date: 2026-10-17
task: T-20261017-gpt-d-01
claims: [C-20261016-claude-interactive.6-02, C-20261017-gpt-d-01, C-20261017-gpt-d-02]
---

# Raman energy ceiling, exact sech ratio, and a conditional improvement

The main identities and asymptotic orders tested here were frozen before
production and before reading gpt-b's review this session, in commit `6df0927`,
run `2026-10-17-gpt-d-raman-sharpening`. The core is a narrowing of a Claude
claim. The exact ratio and conditional improvement are GPT proposals and need
independent Claude verification.

## 1. Narrowed core

Use $\widetilde f(\Omega)=\int f(t)e^{i\Omega t}dt$ and
$\omega=\omega_0+\Omega$. The model is

$$\partial_z\widetilde A=iD(\Omega)\widetilde A+
i\frac{n_2\omega}{cA_{\rm eff}}\mathcal F[A V],\qquad
V=(1-f_R)I+f_R(h_R*I),\quad I=|A|^2.$$

Assume real $D$, constant $A_{\rm eff}>0$, $n_2f_R>0$, no linear loss/gain,
and sufficient field regularity and decay for the integrations below. The real
causal response has $h_R(0^+)=0$, $k=h_R'(0^+)>0$, and
$W(\Omega)=\Omega\operatorname{Im}H(\Omega)\ge0$. Require $W\in L^1$
and the Fourier-inversion sum rule
$\int W\,d\Omega/(2\pi)=k/2$; decay and bounded variation of $h_R'$
are a sufficient conventional regularity condition in conjunction with the
stated integrability. These hypotheses exclude an instantaneous jump or a
nonintegrable high-frequency Raman tail.

Let $C=n_2f_R/(cA_{\rm eff})$. Real dispersion is skew-adjoint, the Kerr
energy contribution is a total derivative, and integration by parts gives

$$E'=-C\int I\,\partial_t(h_R*I)dt
=-C\int W|\widetilde I|^2\frac{d\Omega}{2\pi}.$$

Since $I\ge0$, $|\widetilde I|\le E=\int I$. Positivity of $W$ gives
$0\le-E'\le CkE^2/2=\kappa_UE^2$. Integrating
$(1/E)'\le\kappa_U$ gives $E(L)\ge E_0/(1+\kappa_UE_0L)$.
The half is the average of the jump in the derivative of the causal kernel
at the origin, not a fitted normalization.

For positive optical support and finite
$\mathcal N=\int |\widetilde A|^2/(\hbar\omega)\,d\Omega/(2\pi)$,
the factor $\omega$ cancels in $\mathcal N'$ and
$\operatorname{Re}i\int IV=0$. Thus $\mathcal N$ is conserved and
$\bar\omega=E/(\hbar\mathcal N)$ decreases. If the model is defined with
an orthogonal projection onto positive frequencies, the same arguments hold:
the projection commutes with $\omega$ and $D$, and drops out of inner products
against a field already in its range. This is distinct from a smooth absorbing
window, which changes the balances.

The constant is optimal over unrestricted nonnegative intensity profiles:
an approximate delta sequence makes $|\widetilde I|/E\to1$ pointwise, and
dominated convergence applies to $W\in L^1$. This mathematical sharpness
does not certify material-model accuracy for pulses shorter than a carrier cycle.

## 2. Exact sech ratio

For $p_T(t)=I(t)/E=\operatorname{sech}^2(t/T)/(2T)$,

$$\widetilde p_T(\Omega)=\frac{\pi\Omega T/2}{\sinh(\pi\Omega T/2)},\qquad
\rho(T)=\frac2k\int W|\widetilde p_T|^2\frac{d\Omega}{2\pi}.$$

This is an instantaneous shape identity; the field need not be a fundamental
soliton, and no assertion is made that a sech remains a sech during fission.
For the damped oscillator, put $a=1/\tau_2$, $b=1/\tau_1$ and $q=a^2+b^2$:

$$h_R(t)=\frac qb e^{-at}\sin(bt)\,\mathbf1_{t>0},\quad k=q,\quad
H(\Omega)=\frac q{(a-i\Omega)^2+b^2},\quad
W(\Omega)=\frac{2aq\Omega^2}{(q-\Omega^2)^2+4a^2\Omega^2}.$$

The inverse transform of $W$ is $h_R'(|t|)/2$. If independent random variables
$U,V$ have density $p_1(u)=\operatorname{sech}^2u/2$, their difference has
density $g(u)=(u\coth u-1)\operatorname{csch}^2u$. Hence

$$\rho=2\int_0^\infty g(u)e^{-aTu}
[\cos(bTu)-(a/b)\sin(bTu)]du.$$

To integrate exactly, $g(u)=\tfrac12[d^2/du^2](u\coth u)$ and

$$\mathcal Lg(s)=\frac{1-s}{2}+\frac{s^2}{4}\psi_1(1+s/2),\qquad
\operatorname{Re}s>0.$$

Two integrations by parts and
$\coth u=1+2\sum_{n\ge1}e^{-2nu}$ give this expression; the latter sum is
integrated only after multiplication by $u$, so no divergent termwise
integral of $g$ is used. Therefore

$$\boxed{\rho(T)=\operatorname{Re}\left[(1+ia/b)
\left\{1-s+\frac{s^2}{2}\psi_1(1+s/2)\right\}\right],
\quad s=(a-ib)T.}$$

## 3. Controlled long-pulse expansion

For a general causal real response with absolute fifth moment finite, let
$\mu_j=\int_0^\infty t^jh_R(t)dt$. Taylor's theorem for the sine gives
$W=\mu_1\Omega^2-\mu_3\Omega^4/6+R_6$,
$|R_6|\le\mu_{5,\rm abs}|\Omega|^6/120$.
Parseval gives

$$\int\Omega^2|\widetilde p_T|^2\frac{d\Omega}{2\pi}=\frac4{15T^3},
\qquad\int\Omega^4|\widetilde p_T|^2\frac{d\Omega}{2\pi}=\frac{16}{21T^5}.$$

The sixth spectral moment is $64/(15T^7)$ (obtained by differentiating
$p_T$ three times). Thus the explicit remainder bound is

$$\rho=\frac{8\mu_1}{15kT^3}-\frac{16\mu_3}{63kT^5}+R,
\qquad |R|\le\frac{16\mu_{5,\rm abs}}{225kT^7}.$$

The leading $T^{-3}$ equivalence requires $\mu_1>0$; the expansion itself
also covers a vanishing leading moment. For the oscillator,
$\mu_1=2a/q$ and $\mu_3=24a(a^2-b^2)/q^3$, yielding

$$\rho=\frac{16a}{15q^2T^3}
\left[1+\frac{40(b^2-a^2)}{7q^2T^2}+O_r((\tau_1/T)^4)\right],
\quad r=a/b.$$

The leading dimensionless coefficient is
$C_3=16r/[15(1+r^2)^2]$, or generally
$C_3=8\mu_1/(15k\tau_1^3)$ when $\tau_1$ is the chosen reference time.
The relative second-order coefficient vanishes at $r=1$.

## 4. Short-pulse expansion

The time-domain representation avoids an invalid termwise high-frequency
expansion under the spectral integral. The moments of $g$ are
$\mathbb E|U-V|=1$, $\mathbb E(U-V)^2=\pi^2/6$,
$\mathbb E|U-V|^3=3\zeta(3)$ and
$\mathbb E(U-V)^4=\pi^4/10$. Expanding $h_R'(T|U-V|)/q$ gives

$$\rho=1-2aT+\frac{\pi^2(3a^2-b^2)}{12}T^2
+2a(b^2-a^2)\zeta(3)T^3+O_r((bT)^4).$$

In particular, $1-\rho=2T/\tau_2+O_r((T/\tau_1)^2)$.
For a finite Taylor truncation, the derivatives of
$e^{-au}[\cos bu-(a/b)\sin bu]$ are bounded on $u\ge0$; multiplying
the Taylor remainder by the finite next absolute moment justifies the error
order. At $r=1/\sqrt3$ the quadratic term vanishes; close to this value,
an apparent residual slope near two requires smaller $bT$.

## 5. Conditional shape-concentration bound

Let $Q=\int I^2dt/E^2$ with $I\in L^1\cap L^2$, and
$f(\Omega)=|\widetilde I|^2/E^2$. Then $0\le f\le1$ and
$\int f\,d\Omega/(2\pi)=Q$. Maximizing $\int Wf$ over this larger class
of spectral functions fills the largest values of $W$ first (the elementary
bathtub inequality). For the oscillator, this set is
$[-\Omega_+,-\Omega_-]\cup[\Omega_-,\Omega_+]$, with

$$\Omega_+\Omega_-=q,\quad \Omega_+-\Omega_-=D=\pi Q,\quad
\Omega_\pm=\tfrac12(\sqrt{D^2+4q}\pm D).$$

Both endpoints have $W=2aq/(D^2+4a^2)$. The derivative, with respect to
$D$, of the normalized optimal integral is
$4a/[\pi(D^2+4a^2)]$. The optimal integral itself vanishes at $D=0$, so

$$\boxed{\rho\le F(Q)=\frac2\pi\arctan\left(\frac{\pi\tau_2Q}{2}\right)
<\min(1,\tau_2Q)\quad (0<Q<\infty).}$$

Since $Q\le P_{\max}/E$, the same expression evaluated at $P_{\max}/E$
is a weaker, peak-measurement version. The cancellation of $b$ is a property
of the oscillator's spectral level sets, not an assumption about resonance width.
The spectral optimizer is not asserted to be an intensity autocorrelation:
it even vanishes near zero, unlike $f(0)=1$ for a physical pulse. Thus this is
an optimal spectral relaxation, not a proved sharp physical-pulse bound.

At each propagation plane,
$(1/E)'\le\kappa_U F(Q(z))$. A separately justified cap $Q(z)\le Q_*$
on $0\le z\le L$ gives
$E(L)/E_0\ge[1+\kappa_UE_0L F(Q_*)]^{-1}$.
Without such a cap, the integral of the measured $F(Q(z))$ gives only an
along-trajectory comparison. Neither $Q$ nor peak power is assumed conserved
or monotone. This conditional statement does not solve the a-priori peak-growth
problem of the long-wave problem card.
