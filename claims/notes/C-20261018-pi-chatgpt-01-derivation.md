> **Provenance.** The PI supplied this README on 2026-10-18, from their ChatGPT session with **GPT 6 Pro** (family gpt). It accompanies the shared conversation https://chatgpt.com/s/t_6ad4b5574cc48191946a991871e10790. The orchestrator claude-interactive committed it as the derivation note for claim C-20261018-pi-chatgpt-01. Two changes were made: LaTeX delimiters were converted from `\[…\]`/`\(…\)` to `$$…$$`/`$…$`, so that the file renders on GitHub, and this note was added. The text is otherwise unchanged. The reproduction scripts it names (`compute_bounds.py`, `explore.py`, `requirements.txt`) were not supplied and are not in this repository.

# Bounds on the energy fraction in the leading soliton

**Date:** 18 October 2026. **Status:** analytical derivation supplied for independent review. The proof below does not depend on numerical optimization. Numerical baselines are convergence checked, not interval-certified. Priority for the sharp single-eigenvalue inequality has not been established. No repository files were modified.

## 1. Setting and main bound

Use the focusing NLSE and decaying-line Zakharov–Shabat problem

$$
iq_z+\tfrac12q_{tt}+|q|^2q=0,\qquad
v'=\begin{pmatrix}-i\zeta&q\\-\bar q&i\zeta\end{pmatrix}v.
$$

A discrete eigenvalue $\zeta=\xi+i\eta$, $\eta>0$, carries scattering-component energy $4\eta$. “Leading” means the largest imaginary part, not necessarily the reddest component. An integrable bound state need not separate into individual pulses.

Let $S(k)\ge0$ be the upstream laser spectral amplitude, with Fourier convention
$Q(k)=\int q(t)e^{-ikt}dt$. Put

$$
q_0=\mathcal F^{-1}S,\quad q_m=\mathcal F^{-1}(mS),\quad |m(k)|\le1,
\quad M_0=\int|q_0|^2dt.
$$

The denominator is **upstream laser energy**, before any mask attenuation. Assume the usual decaying-potential ZS setting and enough regularity for the expressions below; smooth rapidly decaying pulses are sufficient. The argument is not restricted to a finite mask basis, real fields, symmetric spectra, or unimodal spectra.

Define

$$
J_p=\int_{\mathbb R}\operatorname{sech}^{p}t\,dt
=\frac{\sqrt\pi\,\Gamma(p/2)}{\Gamma((p+1)/2)},
$$
$$
C_p=\frac{p^p}{(p-1)^{p-1}}\frac{J_p}{2},\qquad p>1.
$$

For every positive integer $n$, every eigenvalue of every admissible passive mask satisfies

$$
\boxed{\quad
\eta\le U_{2n}[S]:=
\left[\frac{\int |q_0(t)|^{2n}dt}{C_{2n}}\right]^{1/(2n-1)}.
\quad}
$$

Consequently,

$$
\boxed{\quad
f_{1,\mathrm{opt}}[S]
:=\sup_{|m|\le1}\frac{4\eta_{\max}(q_m)}{M_0}
\le\frac4{M_0}\inf_{n\ge1}U_{2n}[S].
\quad}
$$

At $n=1$, $C_2=4$ and the bound is $f_1\le1$. As $n\to\infty$, the bound on $\eta$ tends to $\|q_0\|_\infty$. Thus the hierarchy includes the earlier energy and peak bounds while supplying intermediate, often much sharper bounds.

A finite choice of n always gives a valid bound. Computing a global minimum over n is not necessary to validate a particular ceiling.

## 2. Sharp single-eigenvalue inequality

The key ingredient, derived here, is

$$
\boxed{\int |q(t)|^pdt\ge C_p\eta^{p-1},\qquad p>1.}
$$

This concerns each eigenvalue separately; it is not asserted to be a Lieb–Thirring inequality for a sum of powers of eigenvalues.

### Proof

For a bound-state spinor write

$$
a(t)=|v_1(t)|,\quad b(t)=|v_2(t)|,\quad
\theta(t)=\arctan\frac{b(t)}{a(t)}\in[0,\pi/2].
$$

Use the continuous atan2 definition at zeros of a component. Both components cannot vanish simultaneously. The left and right decaying asymptotic subspaces imply

$$
\theta(-\infty)=0,\qquad\theta(+\infty)=\pi/2.
$$

Away from component zeros, differentiating the moduli gives

$$
a'=\eta a+\frac{\Re(qv_2\bar v_1)}a,\qquad
b'=-\eta b-\frac{\Re(qv_2\bar v_1)}b,
$$

and hence, almost everywhere,

$$
\theta'=\nu-\eta\sin2\theta,\qquad\nu:=-\frac{\Re(qv_2\bar v_1)}{ab}\le |q|.
$$

Thus

$$
\theta'\le r-\eta\sin2\theta,\qquad r=|q|.
$$

For $r,s\ge0$, elementary convexity gives the sharp pointwise inequality

$$
r^p\ge K_p s^{p-1}(r-s),\qquad
K_p=\frac{p^p}{(p-1)^{p-1}}.
$$

For $s>0$, set $x=r/s$; the minimum of $x^p-K_p(x-1)$ is zero at $x=p/(p-1)$. For $s=0$, the inequality is immediate.

Set $s=\eta\sin2\theta$. Since its coefficient is nonnegative,

$$
|q|^p\ge K_p\eta^{p-1}\sin^{p-1}(2\theta)\,\theta'.
$$

Integrating uses an antiderivative in $\theta$, not a change of variables that assumes monotonicity. Even if $\theta(t)$ turns around,

$$
\int\sin^{p-1}(2\theta)\theta' dt
=\int_0^{\pi/2}\sin^{p-1}(2x)dx=\frac{J_p}{2}.
$$

This proves the inequality. Zeros of individual spinor components do not affect the almost-everywhere argument; the weighting vanishes there, and the integrated antiderivative is continuously differentiable for p>1.

### Sharpness

Equality is attained by

$$
q_*(t)=\frac{p\eta}{p-1}
\operatorname{sech}\!\left(\frac{2\eta(t-t_0)}{p-1}\right),
$$

up to a constant phase and carrier modulation. To verify the bound state directly, put

$$
b_*:=\frac{2\eta}{p-1},\qquad
\theta=\arctan e^{b_*(t-t_0)},\qquad
R=\operatorname{sech}^{(p-1)/2}(b_*(t-t_0)),
$$

and use $v=R(\cos\theta,-\sin\theta)^T$ at $\zeta=i\eta$. It solves the ZS equation and decays at both ends. Its potential has soliton order p/2; reflectionlessness is not needed for sharpness.

Checks: p=2 recovers $\eta\le\|q\|_2^2/4$; p tending to infinity recovers the peak bound; p tending down to 1 recovers the necessary area condition $\|q\|_1\ge\pi/2$ under the relevant integrability assumptions.

## 3. From a pulse inequality to a fixed-source bound

For an even exponent p=2n, Plancherel and the convolution formula give

$$
\int|q_m|^{2n}=\|q_m^n\|_2^2
\le \|q_0^n\|_2^2=\int|q_0|^{2n},
$$

because

$$
|(mS)*\cdots*(mS)|\le S*\cdots*S.
$$

All Fourier normalization constants are identical on the two sides. Combining this majorant inequality with Section 2 proves the main bound.

The even-exponent Fourier majorant property is classical; see Lenzmann–Sok, Lemma 5.1. For a general spectrum it must NOT be extended to arbitrary real p. That extension is false in general. The Gaussian exception below follows from a different, sharp Fourier inequality.

## 4. Exact result for integer-order sech sources

Take $q_0(t)=N\operatorname{sech}t$, with integer $N\ge1$. Choose p=2N. The common factor J_p cancels, giving

$$
U_{2N}=N-\tfrac12.
$$

The TL pulse attains this value: its leading eigenvalue is $i(N-1/2)$. Therefore

$$
\boxed{\sup_{|m|\le1}\eta_{\max}(q_m)=N-\tfrac12,
\qquad f_{1,\mathrm{opt}}=\frac{2N-1}{N^2}.}
$$

This is a global result for the admissible passive-mask class, not a local search result. In particular, for N=4 the maximal upstream-normalized leading fraction is exactly 7/16=43.75%, improving the earlier peak-only ceiling of 50%.

For noninteger $N>1/2$, every integer n gives

$$
U_{2n}=\frac{2n-1}{2n}N\left(\frac{N}{n}\right)^{1/(2n-1)}.
$$

This bounds the headroom relative to the exact TL eigenvalue N-1/2. Examples: at N=2.5, 3.5 and 5.5 the ceilings on relative improvement are about 0.43672%, 0.15446% and 0.03888%, respectively. Exact noninteger-sech optimality is not asserted.

For n close to N,

$$
\log\frac{U_{2n}(N)}{N-1/2}
=\int_n^N\frac{x-n}{(2n-1)x(x-1/2)}\,dx.
$$

This supplies an explicit quadratic bound in the distance from the nearest integer and O(N^-3) relative headroom for a bounded offset at large N.

## 5. Gaussian sources: continuous-exponent refinement

Take $q_0(t)=N e^{-t^2/2}$. The Fourier spectrum is Gaussian. The sharp Hausdorff–Young inequality, attained by Gaussians, implies

$$
\|q_m\|_p\le\|q_0\|_p\quad\text{for every real }p\ge2.
$$

Indeed, with p'=p/(p-1),

$$
\|q_m\|_p\le
(2\pi)^{-1/p'}\left(\frac{p'^{1/p'}}{p^{1/p}}\right)^{1/2}
\|mS\|_{p'}\le
(2\pi)^{-1/p'}\left(\frac{p'^{1/p'}}{p^{1/p}}\right)^{1/2}
\|S\|_{p'}=\|q_0\|_p.
$$

Consequently,

$$
\boxed{\eta_{\max}(q_m)\le
\inf_{p\ge2}\left[\frac{N^p\sqrt{2\pi/p}}{C_p}\right]^{1/(p-1)},}
$$
$$
\boxed{f_{1,\mathrm{opt}}\le
\frac{4}{\sqrt\pi N^2}\inf_{p\ge2}
\left[\frac{N^p\sqrt{2\pi/p}}{C_p}\right]^{1/(p-1)}.}
$$

This is a one-dimensional minimization of elementary/gamma functions, with no ZS solve or mask search needed to obtain an upper bound. In the evaluator, p is rounded to a finite decimal and the expression is evaluated at that p with 70 decimal digits. Thus validity of the bound does not depend on certification that the p-optimizer located the exact infimum.

Selected numerical results (fractions, not percentages):

| N | TL fraction, numerical | Upper fraction from the theorem | Relative headroom, percent |
|---|---|---|---|
| 1 | 0.9494933953 | 1 | 5.31932 |
| 1.5 | 0.9519259914 | 0.9546240545 | 0.28343 |
| 2 | 0.8254688397 | 0.8265045803 | 0.12547 |
| 3 | 0.6209924762 | 0.6212206123 | 0.03674 |
| 4 | 0.4912507580 | 0.4913243554 | 0.01498 |
| 6 | 0.3440877734 | 0.3441022586 | 0.004210 |
| 10 | 0.2142456148 | 0.2142474594 | 0.0008610 |

The upper-bound formulas are analytical. The displayed decimals and gaps are numerical evaluations. TL baselines were checked by normalized RK4 shooting at successively halved steps, an enlarged time window, and a separate DOP853 integration of the angle equation. The largest baseline spread in the table is about 1.3e-10 in eta, at N=10. These comparisons are not interval certificates or rigorous error bars.

### A direct spectral-norm bound for any source

Sharp Hausdorff–Young is also useful without Gaussian saturation. For any S and p>=2 it gives the independent bound

$$
\eta\le
\frac{\sqrt{p'}}{2\pi}
\left(\frac1{\sqrt p\,C_p}\right)^{1/(p-1)}
\int S(k)^{p'}dk.
$$

One may minimize this over real p and take its minimum with the even-moment hierarchy. For non-Gaussian sources the two constructions need not be equally tight.

## 6. Physical units

For a scalar anomalously dispersive Kerr fiber with constant beta2 and gamma, let $P_0(T)=|A_{\rm TL}(T)|^2$, $E_L=\int P_0(T)dT$, and $D=|\beta_2|/\gamma$. The dimensionless scaling gives

$$
\boxed{
\frac{E_1}{E_L}\le\frac4{E_L}\inf_{n\ge1}
\left[\frac{D^{n-1}}{C_{2n}}\int P_0(T)^n dT\right]^{1/(2n-1)}.
}
$$

The arbitrary normalization time cancels. For a Gaussian, replace 2n by real p>=2 and D^(n-1) by D^(p/2-1).

For the sech source, $N^2=\gamma P_{\rm peak}T_0^2/|\beta_2|$, $E_L=2N^2D/T_0$, and at integer N,

$$
E_{1,\max}=\frac{2(2N-1)D}{T_0}.
$$

## 7. Scope and limitations

- The general inequality does not assume TL optimality and is consistent with the earlier asymmetric counterexample.
- It is NOT uniformly tight. For the earlier source $S=\pi\cos(1)e^k\operatorname{sech}(\pi k/2)$, the even-moment checks n=1,...,20 give only the trivial fraction ceiling 1. No percent-level optimality claim for that asymmetric source follows.
- The fractional gaps in the Gaussian table are relative to the TL leading fraction, not percentage points of total laser energy.
- The bounds concern the initial scattering data and its isospectral integrable evolution. They do not bound the tallest transient intensity peak or the energy in an arbitrary time gate.
- Raman, higher-order dispersion, loss, and self-steepening break the inference from initial eigenvalues to final soliton energy. Interpulse Raman energy transfer is established in the literature. A final nonintegrable efficiency bound needs a separate, controlled transfer estimate.
- The underlying Fourier inequalities, the trace normalization, and the sech scattering eigenvalues are established. The sharp angle inequality is derived here from elementary steps; an exhaustive priority search has not been performed. These are not claims of first publication.

## Reproduction

```
python -m pip install -r requirements.txt
python compute_bounds.py
```

This writes `results.json`. The file `explore.py` is the preliminary evaluator; `compute_bounds.py` is the documented reproduction entry point.

## References

1. E. Lenzmann and J. Sok, *A sharp rearrangement principle in Fourier space and symmetry results for PDEs with arbitrary order*, arXiv:1805.06294v4, Lemmas 5.1–5.2. https://arxiv.org/html/1805.06294v4
2. W. Beckner, *Inequalities in Fourier Analysis*, Annals of Mathematics 102 (1975), 159–182; DOI 10.2307/1970980. The short announcement is *Inequalities in Fourier analysis on Rn*, PNAS 72 (1975), 638–641, DOI 10.1073/pnas.72.2.638.
3. M. I. Yousefi and F. R. Kschischang, *Information Transmission using the Nonlinear Fourier Transform, Part II: Numerical Methods*, arXiv:1204.0830v2, trace identities and Satsuma–Yajima section. https://arxiv.org/html/1204.0830v2
4. M. Klaus and J. K. Shaw, *On the Eigenvalues of Zakharov–Shabat Systems*, SIAM J. Math. Anal. 34 (2003), 759–773; DOI 10.1137/S0036141002403067. The sharp area threshold is a consistency check on the p-to-1 limit.

5. R. Kormokar, M. H. M. Shamim, and M. Rochette, *Energy conversion efficiency from a high order soliton to fundamental solitons in presence of Raman scattering*, arXiv:2301.02945 (2023). https://arxiv.org/abs/2301.02945
