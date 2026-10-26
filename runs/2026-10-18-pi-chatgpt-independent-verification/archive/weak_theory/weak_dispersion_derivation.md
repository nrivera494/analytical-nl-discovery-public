# Independent verification of the weak normal-dispersion squeezing law

Prepared 2026-10-18. Repository snapshot: `970bfe756b131094872de351ff91ab46a537d9b2`.
Target: C-20261010-claude-a-01, principally item 5.

This note derives the asymptotic coefficients from the full mean-field and
Bogoliubov equations. It does not import the repository's implementation. The
independent full-NLSE numerical tests are in the sibling `weak/` directory.
The algebraic scripts in this directory implement the derivations below.

## 1. Conclusions and status

1. The Gaussian leading coefficient and the localization scale survive the
   independent calculation. With fixed nonlinear phase `Phi > 0`, an isolated
   nondegenerate intensity maximum, positive second-order dispersion and an
   unrestricted local-oscillator mode,

   \[
   \lambda/\lambda_0-1\sim
   \sqrt{2/3}\,\frac{\Phi}{\sqrt{1+\Phi^2}}\sqrt y,
   \qquad
   \sigma_t/T_0\sim(y/24)^{1/4}.
   \]

   The width formula is valid at every fixed positive `Phi`; it does not require
   the further large-`Phi` limit stated alongside the repository's formula.

2. The quantity is the unrestricted quadrature-covariance spectral infimum,
   achievable with an appropriate independent homodyne local oscillator. It is
   a lower bound on binary-filter photon-counting Fano factors. It is not, by
   itself, the optimal filtered Fano factor.

3. The peak-shape generalization is correct for a first nonzero peak term of
   order `2m`: the excess scales as `y^(m/(m+1))`, with localization width
   `y^(1/(2m+2))`. A statement covering *every* even smooth pulse with exponent
   `1/2` is false; the claim's own quartic example is a counterexample.

4. The effective oscillator has an exact variational proof. The full optical
   propagator has the displayed controlled expansion on localized smooth trial
   functions; this supplies quasimodes and upper bounds. Turning this into a
   completely rigorous theorem for the global, unbounded-bandwidth spectral
   infimum needs a uniform spectral-localization/high-frequency estimate. The
   frozen principal symbol strongly supports that estimate, and the independent
   full-NLSE calculations support the predicted global minimum. This note does
   not pretend that the missing uniform estimate follows just by naming the
   harmonic oscillator.

5. A new formal second-order calculation refines the empirical `c2 ≈ 1`:

   \[
   \frac{\lambda}{\lambda_0}-1
   =A(\Phi)\sqrt y+B(\Phi)y+O(y^{3/2}),
   \qquad A(\Phi)=\sqrt{\frac23}\frac{\Phi}{S},\quad S=\sqrt{1+\Phi^2},
   \]
   \[
   B(\Phi)=\frac{45+81\Phi^2+56\Phi^4+40\Phi^3S}{120\Phi S^3},
   \]
   \[
   c_2(\Phi)=\frac{B}{A}
   =\frac{\sqrt6\,[45+81\Phi^2+56\Phi^4+40\Phi^3S]}
           {240\Phi^2(1+\Phi^2)}.
   \]

   This is an independently derived local asymptotic refinement, checked
   symbolically and against independent full-NLSE numerical data. A global
   uniform `O(y^(3/2))` theorem has not been established here.

6. A fixed detector bandwidth, a fixed time grid, a finite electronic response
   time, or fixed finite pump photon number cannot be carried unchanged through
   the mathematical `y -> 0` all-mode limit. These are relevant orders of limits,
   not defects in the leading idealized oscillator calculation.

## 2. Model, normalizations and the observable

Set

\[
s=z/L,\quad x=t/T_0,\quad \delta=\beta_2 L/T_0^2=L/L_D>0,
\quad\Phi=\gamma P_0L,\quad y=\Phi\delta.
\]

Here `T0` is defined by the **intensity** profile
`p(x)=exp(-x^2)`, so the mean field at input is `u(0,x)=exp(-x^2/2)`.
The sign convention is

\[
\partial_su=-\frac{i\delta}{2}\partial_x^2u+i\Phi|u|^2u.
\tag{1}
\]

The field perturbation obeys the Fréchet derivative of exactly the same flow:

\[
\partial_sv=-\frac{i\delta}{2}\partial_x^2v
       +i\Phi(2|u|^2v+u^2v^*).
\tag{2}
\]

Normalize the quantum field in photon-flux units with
`[a(x), a†(x')]=delta(x-x')`. In the mean-phase frame write

\[
X=a+a^\dagger,\qquad Y=(a-a^\dagger)/i,
\qquad [X(x),Y(x')]=2i\delta(x-x').
\]

The coherent-input symmetrized covariance is the identity kernel. For the real
Bogoliubov transfer `M`,

\[
V=MM^*,\qquad MJM^*=J,
\quad J=\begin{pmatrix}0&I\\-I&0\end{pmatrix}.
\tag{3}
\]

The adjoint includes integration over time. Uniform orthogonal phase rotations
and the local mean-phase rotation preserve covariance eigenvalues. The
Hamiltonian model has no amplifier, absorption or Raman reservoir, so it
requires no added Langevin source. Its coherent-input covariance is pure:
`VJV=J`, and the finite-dimensional eigenvalues occur in reciprocal pairs.
Neither a classical-noise-only covariance nor an anti-alias operation that
removes vacuum without restoring its channel can be substituted for (3).

For any normalized complex local oscillator `l(x)`, its homodyne quadrature is

\[
Q_l=\int\{\Re l\,X+\Im l\,Y\}\,dx,
\qquad \int |l|^2dx=1.
\]

Therefore

\[
\lambda_{\min}=\inf_{\|f\|=1}\langle f,Vf\rangle
\tag{4}
\]

is a directly meaningful homodyne squeezing optimization. Photon counting after
a binary spectral mask has its local-oscillator direction fixed by the
filtered mean field. It searches a smaller set of directions. Thus
`F_binary,opt >= lambda_min`, generally with a gap. Opatrný, Korolkova and
Leuchs (2002), Sections IV–V, already establish this covariance-eigenvalue
bound and the distinction from filtering; their vacuum convention is `1/2`
rather than `1`.

## 3. Dispersionless anchor: exact algebra, but an infimum

At `delta=0`, `u(s,x)=sqrt(p(x))*exp(i Phi s p(x))`. After removal of this mean
phase the real transfer acts pointwise:

\[
M_0(x)=\begin{pmatrix}1&0\\2\Phi p(x)&1\end{pmatrix},
\qquad
V_0(x)=\begin{pmatrix}1&2\Phi p\\2\Phi p&1+4\Phi^2p^2\end{pmatrix}.
\]

The lower local covariance eigenvalue is

\[
v_-(g)=(\sqrt{1+g^2}-g)^2=e^{-2\operatorname{asinh}g},
\qquad g=\Phi p(x).
\]

For `0<=p<=1` with a unique maximum at zero,

\[
\lambda_0=v_-(\Phi),\qquad
\frac{d\log v_-}{dg}=-\frac2{\sqrt{1+g^2}}.
\tag{5}
\]

This is the continuum **spectral infimum**. At an isolated maximum it has no
normalizable temporal eigenfunction. Any normalized mode has nonzero weight
where `p<1`, and hence a strictly larger Rayleigh quotient. A sequence
concentrating at the maximum approaches (5). A time-grid calculation with a
sample exactly at `x=0` converts this unattained infimum into an attained
discrete eigenvalue. That conversion matters when taking dispersion to zero.

## 4. Exact continuous-wave calculation

Freeze the local pulse power at `p` and take a Fourier component of frequency
`k` conjugate to `x`. Let

\[
g=\Phi p,\qquad a=\delta k^2/2,\qquad
w=\sqrt{a(a+2g)}.
\]

The generator and transfer over `0<=s<=1` are

\[
G=\begin{pmatrix}0&-a\\a+2g&0\end{pmatrix},\qquad
M=\cos w\,I+\frac{\sin w}{w}G.
\tag{6}
\]

Since `det(M)=1`, the trace determines its covariance eigenvalues:

\[
\operatorname{tr}(MM^T)=2+4g^2\operatorname{sinc}^2w,
\]
\[
\lambda_{\rm CW}(p,a)=v_-\big(g|\operatorname{sinc}w|\big).
\tag{7}
\]

For normal dispersion `a>=0`, `|sinc w|<=1`; hence this principal symbol is
never below `v_-(Phi)`. Its unique global minimum, for an isolated pulse peak,
is `(x,k)=(0,0)`. The high-frequency limit is vacuum, since the nonlinear
Bogoliubov coefficient tends to zero. These are crucial facts when seeking a
global lower bound; a localized trial mode alone would not prove it.

At `p=1`, expansion of the exact formula gives

\[
\log\frac{\lambda_{\rm CW}}{\lambda_0}
=\frac{2\Phi^2}{3S}a+O(a^2),\qquad S=\sqrt{1+\Phi^2}.
\tag{8}
\]

Peak-power variation gives

\[
\log\frac{v_-(\Phi p(x))}{\lambda_0}
=\frac{2\Phi}{S}[1-p(x)]+O([1-p(x)]^2).
\tag{9}
\]

Combining (8) and (9) suggests the effective operator; the following section
derives it directly from (1)–(2), including why mean reshaping does not change
the leading coefficient.

## 5. Direct rescaled Bogoliubov derivation

### 5.1 Exact generator in the mean-phase frame

Let `u=R exp(i theta)`, with `rho=R^2`. The mean-field equations are

\[
\rho_s=\delta(\rho\theta_x)_x,
\quad
\theta_s=\Phi\rho-\frac\delta2\frac{R_{xx}}R
                       +\frac\delta2\theta_x^2.
\tag{10}
\]

Remove `theta` from the perturbation and use its real quadratures. Their exact
generator is

\[
\partial_s\begin{pmatrix}X\\Y\end{pmatrix}
=\begin{pmatrix}T&-K\\K+2\Phi\rho&T\end{pmatrix}
\begin{pmatrix}X\\Y\end{pmatrix},
\tag{11}
\]
\[
T=\delta\theta_x\partial_x+\tfrac\delta2\theta_{xx},
\qquad K=\tfrac\delta2[-\partial_x^2+R_{xx}/R].
\]

`T` is anti-self-adjoint and `K` is self-adjoint, so (11) preserves the
canonical commutators. Where `R>0`, its kinetic operator also factors as
`-d^2/dx^2+R_xx/R=(d/dx-R_x/R)^*(d/dx-R_x/R)` on its natural domain.
The term `R_xx/R` is needed for the consistent second-order calculation.

### 5.2 Leading expansion at a quadratic peak

Suppose `p(x)=1-kappa*x^2+O(x^4)`, `kappa>0`. Set

\[
\epsilon=\sqrt y,\qquad x=\sqrt\epsilon\,q,\qquad D=-\partial_q^2.
\]

On every fixed smooth localized mode in `q`, the initial intensity varies by
`O(epsilon)`, whereas dispersive reshaping of that intensity is `O(epsilon^2)`.
The rescaled generator becomes

\[
G_\epsilon=G_0+\epsilon G_1+O(\epsilon^2),
\qquad G_0=\begin{pmatrix}0&0\\2\Phi&0\end{pmatrix},
\]
\[
G_1=
\begin{pmatrix}
0&-D/(2\Phi)\\
D/(2\Phi)-2\Phi\kappa q^2&0
\end{pmatrix}.
\tag{12}
\]

The output transfer has the Duhamel expansion

\[
M_\epsilon=M_0+\epsilon M_1+O(\epsilon^2),\qquad
M_1=\int_0^1 M_0(1-s)G_1M_0(s)\,ds,
\]
\[
M_0(s)=\begin{pmatrix}1&0\\2\Phi s&1\end{pmatrix},
\]
\[
M_1=\begin{pmatrix}
-D/2&-D/(2\Phi)\\
(1/(2\Phi)-\Phi/3)D-2\Phi\kappa q^2&-D/2
\end{pmatrix}.
\tag{13}
\]

Consequently `V_epsilon=V_0+epsilon V_1+O(epsilon^2)`, with

\[
V_1=
D\begin{pmatrix}-1&-4\Phi/3\\-4\Phi/3&1-4\Phi^2/3\end{pmatrix}
\;+
\kappa q^2\begin{pmatrix}0&-2\Phi\\-2\Phi&-8\Phi^2\end{pmatrix}.
\tag{14}
\]

Let `r=S-Phi`, so `lambda0=r^2`, and let

\[
e_-=(1,-r)^T/\sqrt{1+r^2},\qquad
e_+=(r,1)^T/\sqrt{1+r^2}.
\]

These are the two constant quadrature eigenvectors of `V_0`. Direct projection
of (14) gives the exact first-order operator identity

\[
\lambda_0^{-1}e_-^T V_1e_-
=\frac{\Phi}{S}\left(\frac D3+2\kappa q^2\right).
\tag{15}
\]

The other quadrature branch lies a fixed positive distance away for fixed
`Phi>0`. Mixing with it first changes the eigenvalue at second order in
`epsilon`. Equation (15) is the desired oscillator reduction; it was obtained
from the full field and fluctuation equations rather than assuming that a
local CW symbol can simply be minimized as a scalar function.

### 5.3 Exact oscillator minimum and mode width

For normalized `f` in the quadratic-form domain,

\[
q_0\|f'\|^2+\alpha\|xf\|^2\ge\sqrt{q_0\alpha},
\]

because

\[
\|\sqrt{q_0}f'+\sqrt\alpha\,xf\|^2
=q_0\|f'\|^2+\alpha\|xf\|^2-\sqrt{q_0\alpha}.
\tag{16}
\]

Equality holds exactly for the normalized Gaussian
`f ∝ exp[-sqrt(alpha/q0)*x^2/2]`. In original dimensionless time the operator is

\[
H_{\rm eff}=-q_0\partial_x^2+\alpha x^2,
\quad q_0=\frac{\delta\Phi^2}{3S},\quad
\alpha=\frac{2\Phi\kappa}{S}.
\]

Thus its ground energy is

\[
\sqrt{q_0\alpha}
=\sqrt{\frac{2\kappa}3}\frac{\Phi}{S}\sqrt y.
\tag{17}
\]

For the Gaussian, `kappa=1`. Its intensity-weighted rms width is

\[
\frac{\sigma_t}{T_0}
=\frac1{\sqrt2}\left(\frac{y}{6\kappa}\right)^{1/4}
=\left(\frac{y}{24\kappa}\right)^{1/4}.
\tag{18}
\]

The distinction between the Gaussian amplitude scale and its intensity rms
width explains the otherwise easily missed factor `sqrt(2)`.

### 5.4 What is rigorous here, and what is not

Equation (16) is an exact theorem for the effective operator. Equations
(12)–(15) can be made into finite-order norm estimates on Schwartz trial modes,
or on smooth cutoff oscillator modes. Taylor's theorem and Duhamel's formula
control the local remainder; one obtains an optical-covariance quasimode and
an upper bound

\[
\inf\sigma(V_\delta)\le\lambda_0
\{1+\sqrt{2\kappa/3}(\Phi/S)\sqrt y+O(y)\}.
\tag{19}
\]

A quasimode also puts an actual spectral point nearby, but does not exclude
lower modes elsewhere in phase space. The frozen symbol (7) has exactly the
right unique-well property to support a matching lower bound. One can formulate
a conditional completion as follows:

*Assume* that the rescaled covariance admits a microlocal expansion with this
principal symbol, that its low spectral states localize near `(x,k)=(0,0)`,
that its subprincipal value at the minimum vanishes, and that the covariance
on the complementary temporal/frequency region has a uniform gap above
`lambda0+O(sqrt(delta))`. The matrix branch can then be reduced to the scalar
well and the harmonic approximation gives equality in (19) to leading order.

The first subprincipal value vanishes at the minimum because derivatives of
the mean power and the frozen frequency term both vanish there. However,
proving uniform high-frequency estimates for the full finite-time Bogoliubov
propagator is an additional argument. Its free-dispersion factor has rapid
oscillations as frequency grows, so a formal bounded-symbol statement over an
arbitrary compact frequency set is not automatically a statement over all
frequencies. The independent simulations check precisely that no lower branch
appears over successively enlarged resolved grids, but are not an interval
certificate covering infinite frequency.

Simon's 1983 harmonic-approximation theorem is a rigorous antecedent for the
scalar Schrödinger step. It does not directly discharge these optical
propagator and matrix-symbol hypotheses. The repository's derivation note
does not discharge them either. This is the honest boundary between a strong
asymptotic result and a completed global functional-analytic proof.

## 6. Locally flatter maxima

Let

\[
p(x)=1-\kappa x^{2m}+o(x^{2m}),\qquad \kappa>0,
\]

with no other equal or higher peak. Rescale

\[
x=y^{1/(2m+2)}q,\qquad \eta=y^{m/(m+1)}.
\]

Both the kinetic term and the leading departure of `p` from one are now of
order `eta`. The same calculation as (12)–(15) gives

\[
\lambda_0^{-1}e_-^T V_1e_-
=\frac{\Phi}{S}\left(\frac{-\partial_q^2}{3}+2\kappa q^{2m}\right).
\]

If `e_(2m)` denotes the ground energy of `-d^2/dq^2+q^(2m)`, then

\[
\frac\lambda{\lambda_0}-1
\sim e_{2m}\left(\frac{2\kappa}{3^m}\right)^{1/(m+1)}
        \frac\Phi S y^{m/(m+1)}.
\tag{20}
\]

The temporal scale is

\[
w/T_0=(y/(6\kappa))^{1/(2m+2)},
\]

multiplied by the rms width of the ground state of
`-d^2/dq^2+q^(2m)`. For `kappa=1`, an independent one-dimensional
Schrödinger discretization and Richardson extrapolation give:

| `m` | `e_(2m)` | Excess prefactor before `(Phi/S) y^(m/(m+1))` | RMS prefactor before `T0 y^(1/(2m+2))` |
|---:|---:|---:|---:|
| 1 | 1 exactly | 0.81649658093 | 0.45180100180 |
| 2 | 1.06036209028 | 0.64226859670 | 0.44635046932 |
| 3 | 1.14480245368 | 0.59723755583 | 0.44355783696 |

The quartic coefficient quoted as `0.64226` is therefore correct to its stated
precision. The sextic example is a useful genuinely new held-out test of the
mechanism. These constants are reproduced by `effective_oscillator.py` and
stored with grid convergence data in `oscillator_constants.json`.

A perfectly flat interval of maxima, infinitely flat peaks, multiple equal
peaks, nonsmooth cusps, and a peak on a boundary require other local models.
For multiple equal peaks, the asymptotically most favorable well wins; for
two identical nondegenerate wells, the two lowest modes can have a much smaller
tunneling splitting than their common `sqrt(y)` shift. Smoothness and evenness
alone do not force `m=1`.

## 7. New second-order Gaussian calculation

### 7.1 Mean reshaping to the required order

For `p=exp(-x^2)`, using `epsilon=sqrt(y)` and `x=sqrt(epsilon) q`, solving
(10) order by order gives

\[
\rho(s,q)=1-\epsilon q^2+\epsilon^2(q^4/2-s^2)+O(\epsilon^3),
\tag{21}
\]
\[
\theta(s,q)=\Phi s-\epsilon\Phi s q^2
 +\epsilon^2(\Phi s q^4/2-\Phi s^3/3+s/(2\Phi))
 +O(\epsilon^3).
\tag{22}
\]

In particular, the peak intensity is `1-y s^2`, and its average along the
fiber is `1-y/3`. The leading square-root term is larger than this reshaping
effect; reshaping contributes at order `y` and must be kept in `c2`.

### 7.2 The full second-order generator

In (11), expansion yields

\[
G_\epsilon=G_0+\epsilon G_1+\epsilon^2G_2(s)+O(\epsilon^3),
\]
\[
G_2(s)=\begin{pmatrix}
-s(2q\partial_q+1)&1/(2\Phi)\\
\Phi q^4-2\Phi s^2-1/(2\Phi)&-s(2q\partial_q+1)
\end{pmatrix}.
\tag{23}
\]

The diagonal dilation term is anti-self-adjoint. The constants `±1/(2 Phi)`
come from `R_qq/R`; omitting them is inconsistent. The `-2 Phi s^2` term is
mean reshaping. In addition to (23), time ordering of two copies of `G1`
retains the noncommutativity of `D` and `q^2`:

\[
M_2=\int_0^1M_0(1-s)G_2(s)M_0(s)ds
\]
\[
\quad+\int_0^1\int_0^s
M_0(1-s)G_1M_0(s-t)G_1M_0(t)\,dt\,ds.
\tag{24}
\]

Then

\[
V_2=M_2M_0^*+M_0M_2^*+M_1M_1^*.
\]

Let the normalized oscillator ground state be
`g(q)=(sqrt(6)/pi)^(1/4) exp(-sqrt(6) q^2/2)`. The second-order eigenvalue
coefficient is

\[
\lambda^{(2)}=
\langle e_-g,V_2e_-g\rangle
 -\frac{\|e_+^TV_1e_-g\|^2}{\lambda_0^{-1}-\lambda_0}.
\tag{25}
\]

There is no first-order coupling from this ground state to a different spatial
eigenstate within the squeezed quadrature branch, because `g` is already the
ground eigenfunction of (15). The second term in (25) is the correction from
the other quadrature branch. This term is essential and is not obtained by
using a scalar local-symbol energy alone.

The exact polynomial action `d/dq -> d/dq-sqrt(6)q` on `g`, Gaussian moments,
and the integrals in (24) produce

\[
\frac{\lambda^{(2)}}{\lambda_0}
=\frac{45+81\Phi^2+56\Phi^4+40\Phi^3\sqrt{1+\Phi^2}}
       {120\Phi(1+\Phi^2)^{3/2}}.
\tag{26}
\]

`second_order_symbolic.py` carries out precisely these operations in SymPy.
It uses no formula for `c2` as an input. Its intermediate output in terms of
`r=sqrt(1+Phi^2)-Phi` is

\[
\lambda^{(2)}=
\frac{r^2(4r^8+45r^6+102r^4+5r^2+24)}
     {30(1-r^2)(1+r^2)^3}.
\]

Simplifying with `Phi=(1-r^2)/(2r)` yields (26).

| `Phi` | Predicted `c2(Phi)` |
|---:|---:|
| 2 | 1.01069098097 |
| 3 | 0.98946456305 |
| 5 | 0.98238823557 |
| 10 | 0.98034160063 |
| 20 | 0.97992570214 |
| 40 | 0.97982793097 |
| infinity | `2 sqrt(6)/5 = 0.97979589711` |

This explains why a roughly `Phi`-independent numerical value near one was
seen for `Phi>=2`. The coefficient is not exactly one and is not universal
under pulse-shape changes. The independent full-NLSE `Phi=10`, `y=1e-6`
calculation at stringent tolerance gave effective `c2=0.9799761`, within the
expected remaining `O(sqrt(y))` deviation. Numerical results and additional
refinements are recorded by the main numerical verification script.

## 8. Orders of limits and physical applicability

### Fixed phase versus simultaneous weak nonlinearity

The theorem being sought is a one-sided limit at fixed `Phi>0`. Its error
constants are not uniform as `Phi->0`; (26) already shows that
`c2 ~ 3 sqrt(6)/(16 Phi^2)`. A sufficient asymptotic separation for the same
hierarchy at small `Phi` is `sqrt(y) << Phi^2`, or `delta << Phi^3`.

This can also be seen from the exact CW formula. At very small `Phi`, the
phase-mismatch term `a^2` in `w^2=a(a+2 Phi)` competes with `2 Phi a`.
When it dominates, the effective dispersion penalty is proportional to
`Phi delta^2 k^4`, not `delta Phi^2 k^2`. Balancing it against the quadratic
peak penalty leads to a different quartic-kinetic crossover. The fixed-`Phi`
claim should not be presented as a uniform joint limit over all powers.

### Bandwidth and time-grid order

The optimal Gaussian has

\[
\sigma_\Omega T_0=(3/(2y))^{1/4}.
\]

To capture it, an optical local-oscillator/detection band must grow compared
with this scale: `Omega_b T0 y^(1/4) >> 1`. A mesh must have
`dt/T0 << y^(1/4)`. Keeping a finite bandwidth or fixed discretization while
taking `delta->0` produces a different problem, with a restricted anchor
strictly above `lambda0`. A fixed finite Hamiltonian discretization has an
analytic covariance family and ordinary analytic eigenvalue branches; the
square-root excess from continuum mode localization cannot persist
arbitrarily far below its resolution scale. A finite-band continuum statement
also requires the usual smoothness estimates when exchanging projection and
the small-dispersion limit; analyticity of that full continuum propagator is
not needed for the counterexample below.

There is a simple explicit bandwidth lower bound at zero dispersion. Write
`B=Omega_b T0`, and let the normalized complex LO be supported in the Fourier
band `[-B,B]`. Cauchy--Schwarz gives `|l(x)|^2 <= B/pi`. With
`a=pi/(4B)`, no more than half its mass can be inside `[-a,a]`. The Gaussian
pulse has `p(x)<=exp(-a^2)` outside, so pointwise covariance positivity gives

\[
\lambda_{B,0}\ge\lambda_0+
\tfrac12\{v_-(\Phi e^{-a^2})-\lambda_0\}>\lambda_0.
\tag{29}
\]

Mean-phase rotations do not change `|l(x)|`, so they do not evade this bound.
At large `B`, the displayed gap divided by `lambda0` is asymptotic to
`pi^2 Phi/(16 S B^2)`. Thus the unrestricted anchor is already wrong for a
fixed optical band. An even simpler explicit restriction is to admit only
one prescribed temporal mode: its dispersionless variance is a weighted
average over `p<1` and strictly exceeds `lambda0` for every finite-width
mode. These examples refute applying the unrestricted law to arbitrary fixed
detectors.

The relevant bandwidth is the optical mode bandwidth, not automatically an
RF photocurrent analysis window. Balanced detection with a shaped pulsed LO
can probe a very broad optical supermode at low RF frequency.

### Finite photon number and the ultraviolet limit

At zero dispersion, the instantaneous Kerr Bogoliubov creation kernel is
proportional to `p(x) delta(x-x')`. As an operator on `L2(R)` it is not
Hilbert-Schmidt, so the formal transformation has infinite spontaneous
occupation on continuum vacuum. It is not a globally implementable finite-
energy Gaussian transformation on the original vacuum Fock space without an
ultraviolet regularization. A finite material response time or bandwidth
removes this problem. This issue is part of the rationale for the finite Kerr
time in Joneckis and Shapiro's 1993 quantum propagation theory.

For the ideal nonzero-dispersion model, the frozen symbol gives the following
semiclassical estimate for the total spontaneous photon number:

\[
N_{\rm ex}\sim\frac1{2\pi\sqrt\delta}
\int dx\int d\xi\;(\Phi p(x))^2
\operatorname{sinc}^2
\left(\sqrt{\frac{\xi^2}{2}
                 \left(\frac{\xi^2}{2}+2\Phi p(x)\right)}\right).
\tag{27}
\]

Thus it grows as `delta^(-1/2)` at fixed phase. In the further large-`Phi`
limit, scaling `eta=sqrt(Phi p) xi` and using
`integral sinc^2(eta) deta=pi` gives

\[
N_{\rm ex}\sim\frac{\Phi^2}{2\sqrt y}\int p^{3/2}dx.
\tag{28}
\]

For a Gaussian the prefactor is `sqrt(2 pi/3)/2 = 0.723601...`.
Consequently a necessary undepleted-pump check in this ideal all-mode limit is
`N_ex << N_ph`; the often quoted `Phi^2 << N_ph` alone is not uniform as
`y->0`. Equation (27) is a semiclassical estimate, not an exact trace identity
for a finite pulse. It identifies the divergent scaling and the omitted
dimensionless condition.

The mean photons overlapping the optimal localized mode also shrink as
`N_ph y^(1/4)`. Requiring this local brightness to dominate the large
antisqueezed fluctuations is a useful additional sufficient linearization
check. This should not be confused with requiring a bright coherent mean in
every detected mode: homodyne detection can validly measure squeezed vacuum
modes with zero coherent amplitude.

Real material dispersion, frequency-dependent nonlinearity, self-steepening,
electronic response, Raman noise, loss and mode shaping constraints can
intervene before the formal asymptotic limit. Their presence does not change
the calculation inside its explicitly idealized Hamiltonian model; it changes
which asymptotic regime an experiment can access.

### A correction to the card's anomalous-dispersion wording

For the ideal CW Kerr model with anomalous dispersion, choose `a=-Phi`. Then

\[
M=\begin{pmatrix}\cosh\Phi&\sinh\Phi\\\sinh\Phi&\cosh\Phi\end{pmatrix},
\qquad \lambda_{\min}=e^{-2\Phi},
\]

at the finite detuning
`Omega=sqrt(2 gamma P0/abs(beta2))`. Once this instability maximum is resolved,
the result is independent of a further increase in the cutoff. Therefore
anomalous squeezing is not intrinsically or perpetually set by the grid
bandwidth in the pure `beta2+Kerr` model. As `beta2->0-`, the optimum moves to
infinite detuning, and a fixed-band limit differs from the unrestricted limit.
The appropriate warning is failure of continuity to the Kerr shear anchor and
noncommuting limits. This exact CW counterexample does not by itself establish
a theorem for the corresponding finite-pulse one-sided limit.

## 9. Literature and novelty assessment

The following are primary sources inspected during this verification. Access
levels are stated to avoid converting an abstract search into a claim to have
ruled out results in the full paper.

| Source | Access and specific antecedent |
|---|---|
| M. J. Potasek and B. Yurke, *Squeezed-light generation in a medium governed by the nonlinear Schrödinger equation*, Phys. Rev. A **35**, 3974 (1987), DOI [10.1103/PhysRevA.35.3974](https://doi.org/10.1103/PhysRevA.35.3974) | Publisher abstract read. Squeezing in normal and anomalous dispersion, including a fourth-order-dispersion treatment near zero dispersion. Antecedent to the CW phase-mismatch ingredient, not evidence for the pulsed singular localization coefficient. |
| P. D. Drummond and S. J. Carter, *Quantum-field theory of squeezing in solitons*, JOSA B **4**, 1565 (1987), DOI [10.1364/JOSAB.4.001565](https://doi.org/10.1364/JOSAB.4.001565) | Publisher abstract read. Quantum stochastic NLSE; CW squeezing bandwidth shrinks in normal dispersion. Broad physical mechanism is established. |
| L. G. Joneckis and J. H. Shapiro, *Quantum propagation in a Kerr medium: lossless, dispersionless fiber*, JOSA B **10**, 1102 (1993), DOI [10.1364/JOSAB.10.001102](https://doi.org/10.1364/JOSAB.10.001102), with 1994 erratum | Publisher abstract read. Multitemporal quantum Kerr propagation and explicit Gaussian moments, with a material response time to control broadband vacuum effects. The dispersionless Gaussian framework and ultraviolet concern are established. |
| C. R. Doerr, M. Shirasaki and F. I. Khatri, *Simulation of pulsed squeezing in optical fiber with chromatic dispersion*, JOSA B **11**, 143 (1994), DOI [10.1364/JOSAB.11.000143](https://doi.org/10.1364/JOSAB.11.000143) | Publisher abstract read. Arbitrary complex input pulses, linearized propagation with dispersion, and squeezing that can improve despite mean-pulse distortion. The numerical propagation framework is established. |
| T. Opatrný, N. Korolkova and G. Leuchs, *Mode structure and photon number correlations in squeezed quantum pulses*, Phys. Rev. A **66**, 053813 (2002), [arXiv:quant-ph/0204131](https://arxiv.org/pdf/quant-ph/0204131) | Full text, particularly §§IV–VI and Eqs. (52)–(64), read. Explicit optimum-covariance-eigenvalue squeezing, optimal LO, proof that spectral filtering cannot outperform it, and vacuum entering attenuating filters. This directly anticipates the general eigenvalue/readout-bound interpretation. |
| B. Simon, *Semiclassical analysis of low lying eigenvalues. I. Non-degenerate minima: asymptotic expansions*, Ann. IHP A **38**, 295 (1983), [full text](https://www.numdam.org/item/AIHPA_1983__38_3_295_0.pdf) | Full text §§1–4 read. Rigorous scalar Schrödinger harmonic approximation, separate upper and lower bounds, and the localization argument needed for the latter. The mathematical exponent mechanism is established; application to this optical covariance is a new reduction. |
| H. Liu et al., *Towards arbitrary time-frequency mode squeezing with self-conjugated mode squeezing in fiber*, Nat. Commun. **16**, 6524 (2025), DOI [10.1038/s41467-025-61225-y](https://doi.org/10.1038/s41467-025-61225-y) | Full publisher text, targeted theory read. Flexible squeezed optical modes in a CW/broad-phase-matching regime. This is adjacent modern mode-engineering work, with a different limit and no identified weak-normal-dispersion Gaussian coefficient. |

The 2025 conference presentation *Quantum mode structure of pulsed Kerr
squeezing in media with normal, near-zero and anomalous group velocity
dispersion* by A. V. Andrianov was also located on the Math-Net conference
site. Its title and indexed abstract are closely related to modal dispersion
questions, but the video/slides were not inspected and no inference about
its detailed asymptotics is made.

Searches using the exact weak-dispersion, square-root, Gaussian peak,
harmonic-oscillator and localized-optimum concepts, as well as the surrounding
Kerr/normal-dispersion literature, found no prior primary source displaying
the coefficient `sqrt(2/3) Phi/sqrt(1+Phi^2)` or the shape family (20).
That is positive evidence for a potentially new explicit asymptotic result,
not an exhaustive priority proof. Several closest older fiber papers were
accessible only at the abstract level. The defensible novelty claim is the
specific singular asymptotic and its coefficients, not Kerr squeezing, the
Bogoliubov method, covariance eigenmodes, or the lower bound on filtering.

## 10. Reproduction

The mathematical supporting calculations require Python 3, NumPy, SciPy and
SymPy. In a normal environment:

```bash
python -m pip install numpy scipy sympy
python effective_oscillator.py
python second_order_symbolic.py
```

`effective_oscillator.py` writes `oscillator_constants.json`, including its
grid convergence. `second_order_symbolic.py` prints the exact rational result
in `r`, and the table of `c2(Phi)`. Neither file reads repository scripts or
stored claim results. The main independent propagation results, convergence
checks and representative modes are generated by `../weak/verify_weak.py`
and its suite; consult that suite for the physical-NLSE numerical reproduction.
