# Independent verification of amplifier-similariton fluctuations

**Scope.** P-001, particularly C-20261008-claude-a-02, in
[analytical-nl-discovery](https://github.com/nrivera494/analytical-nl-discovery),
commit 970bfe756b131094872de351ff91ab46a537d9b2. Analysis date: 2026-10-18.
The accompanying programs were independently implemented and do not import
or execute repository code.

## 1. Conclusions

The strongest result survives with a precise qualification: **in the
linearized, dispersionless parabolic core, each fixed shape mode of degree
at least two has photon-number-weighted density and phase variances with
gain exponents \(1/3\) and \(5/3\)**. These are variance exponents, not
field-amplitude exponents. The prefactors generally oscillate in \(\log G\);
envelopes or two-sided asymptotic bounds are appropriate.

The spectral covariance ratio and phase–energy correlation deficit have
exponent \(-2/3\) for a correctly normalized fixed finite-mode projection
with nondegenerate input and reservoir noise. An independent real-space
finite-volume covariance calculation reproduces the reduced-model numbers.
An independent full gain-NLSE tangent/adjoint calculation supports the
leading low-mode dynamics and provides complete-noise representative
covariances. It does not certify the claimed uniform boundary-layer error
estimates or a full-field infinite-gain quantum theorem.

Two assertions require correction. The dominant matched-LO phase covariance
scales as \(G^{7/3}/\epsilon^2\), not \(G/\epsilon^2\), at fixed dimensionless
gain. A literal statement that amplifier-added noise prevents all squeezing
is false: a short-distance analytical counterexample survives complete
quantum-limited ASE and is reproduced by the full NLSE. The restricted
large-gain matched-LO excess-noise statement does survive.

These are results for an instantaneous Kerr response, second-order normal
dispersion, unsaturated uniform gain, and a specified Markov bath.
Finite bandwidth, finite detection aperture, edge regularization and a
joint bright limit are material conditions, not optional refinements.

## 2. Model and independent mode derivation

### Definitions and mean field

Use the power-normalized envelope \(|A|^2=P\):

\[
\partial_z A=-\frac{i\beta_2}{2}A_{TT}
+i\gamma|A|^2A+\frac g2A+F,\qquad \beta_2>0,\qquad
[A(T),A^\dagger(T')]=\hbar\omega_0\delta(T-T').
\]

The photon-flux field is \(A/\sqrt{\hbar\omega_0}\), with unit commutator.
One should not call \(A\) photon normalized while keeping the power-field
commutator without this conversion.

The gain \(G=e^{gL}\) is **power or coherent-signal energy gain**; field
gain is \(\sqrt G\). Define

\[
L_D=T_0^2/\beta_2,\quad L_{\rm NL}=1/(\gamma P_0),\quad
Z_0=\sqrt{L_DL_{\rm NL}},\quad
\epsilon=\sqrt{L_{\rm NL}/L_D},\quad
\Gamma=gZ_0,\quad \zeta=z/Z_0,\quad \tau=\Gamma\zeta=gz.
\]

The semiclassical parameter \(1/\epsilon\) is distinct from the input
photon number \(N_0=4P_0T_0/(3\hbar\omega_0)\) of a parabola.
In the bright-signal approximation \(N_{\rm out}=GN_0\).
Also \(\gamma P_0/g=1/(\Gamma\epsilon)\).

Writing \(A/\sqrt{P_0}=\sqrt\rho e^{i\phi}\), \(x=T/T_0\),
\(v=-\epsilon\phi_x\), gives

\[
\rho_\zeta+(\rho v)_x=\Gamma\rho,\qquad
v_\zeta+vv_x=-\rho_x+
\frac{\epsilon^2}{2}\partial_x
\left[\frac{(\sqrt\rho)_{xx}}{\sqrt\rho}\right].
\]

Dropping the last, dispersive-pressure term produces the hydrodynamic
core. This approximation is logically separate from whether noise is
classical or quantum. The parabolic family is

\[
\rho_b=\frac{e^{\Gamma\zeta}}a(1-\xi^2),\quad
\xi=x/a,\quad |\xi|<1,\quad v_b=(a'/a)x,\quad
a''=2e^{\Gamma\zeta}/a^2.
\]

Primes here denote \(\zeta\). The exact exponentially expanding member is
\(a=A_*e^{\tau/3}\), \(A_*^3=18/\Gamma^2\). At \(\Gamma=\sqrt{18}\),
\(A_*=1\), and an asymptotic launch has \(a(0)=1,a'(0)=\Gamma/3\).
The principal repository table instead uses \(a'(0)=0\).

Within this parabolic width ODE, attraction can be proved. For
\(s=a/(A_*e^{\tau/3})\),

\[
s_{\tau\tau}+\tfrac23s_\tau+s/9=1/(9s^2),\qquad
\mathcal V=\tfrac12s_\tau^2+s^2/18+1/(9s),\qquad
\mathcal V_\tau=-\tfrac23s_\tau^2.
\]

Positive-width sublevel sets are bounded and bounded away from zero;
the only invariant set with zero dissipation is \(s=1,s_\tau=0\).
This proves convergence within the width ODE, not an arbitrary-initial-data
full-NLSE fluctuation theorem.

### Shape modes

Define \(\delta\rho=\rho_{\rm peak}n(\xi,\zeta)\) and
\(\delta\phi=p(\xi,\zeta)\), with \(\rho_{\rm peak}=e^{\Gamma\zeta}/a\).
Thus \(n\) is relative to the peak; the local relative intensity is
\(n/(1-\xi^2)\), a different, edge-singular observable.
Independent linearization in the comoving coordinate yields

\[
p_\zeta=\frac{e^{\Gamma\zeta}}{a\epsilon}n,\qquad
n_\zeta=\frac{\epsilon}{a^2}\mathcal Dp,\qquad
\mathcal D=\partial_\xi[(1-\xi^2)\partial_\xi].
\]

Regular no-flux core eigenfunctions are \(P_l\), with
\(\mathcal DP_l=-l(l+1)P_l\). For \(n=\sum n_lP_l,\ p=\sum p_lP_l\),

\[
\frac d{d\zeta}\begin{pmatrix}p_l\\n_l/\epsilon\end{pmatrix}
=
\begin{pmatrix}0&e^{\Gamma\zeta}/a\\-l(l+1)/a^2&0\end{pmatrix}
\begin{pmatrix}p_l\\n_l/\epsilon\end{pmatrix}.
\]

For \(l\ge1\), elimination gives

\[
n_l''+2(a'/a)n_l'+l(l+1)e^{\Gamma\zeta}a^{-3}n_l=0.
\]

On the exponential member:

\[
n_{l,\tau\tau}+\tfrac23n_{l,\tau}
+\frac{l(l+1)}{18}n_l=0.
\]

For \(l\ge2\),

\[
n_l=e^{-\tau/3}[A_l\cos(\nu_l\tau)+B_l\sin(\nu_l\tau)],
\qquad \nu_l=\tfrac13\sqrt{l(l+1)/2-1}.
\]

Phase has envelope \(G^{1/3}/\epsilon\) for a density seed. The physical
distance frequency is \(g\nu_l\). The \(l=0\) first-order equation has
constant \(n_0\); applying the eliminated equation there introduces a
spurious decaying solution. The \(l=1\) repeated root gives
\((A+B\tau)e^{-\tau/3}\), a collective displacement/frequency mode.

For a nondegenerate stochastic ensemble and fixed \(l\ge2\),

\[
\boxed{N_{\rm out}\operatorname{Var}n_l=\Theta(G^{1/3}),\qquad
N_{\rm out}\operatorname{Var}p_l=\Theta(G^{5/3}/\epsilon^2).}
\]

The explicit \(\epsilon^{-2}\) disappears when the phase coordinate is
\(\epsilon p_l\). Standard-deviation exponents of the photon-weighted
coordinates are \(1/6\) and \(5/6\). Raw density and phase amplitude
envelopes are \(G^{-1/3}\) and \(G^{1/3}\). Orthonormalizing the Legendre
basis changes constants, not these exponents.

### Distributed noise and a finite-mode proof of the exponents

Put \(u_l=e^{\tau/3}n_l,\ w_l=\epsilon e^{-\tau/3}p_l\). The asymptotic
drift is constant:

\[
B_l=\begin{pmatrix}
1/3&-l(l+1)/(\Gamma A_*^2)\\
1/(\Gamma A_*)&-1/3
\end{pmatrix},\qquad B_l^2=-\nu_l^2I.
\]

Its propagator \(\cos(\nu_l\tau)I+\sin(\nu_l\tau)B_l/\nu_l\) and inverse
are uniformly bounded. Intensity diffusion in these coordinates is
proportional to \(e^{-\tau/3}\); regulated phase diffusion is proportional
to \(\epsilon^2e^{-5\tau/3}\). Their interaction-picture time integrals
converge. Density diffusion plus the nonzero drift coupling makes each
shape block controllable, yielding a positive definite limiting
interaction-picture covariance for a physical inverted bath.
This proves the two-sided powers for a fixed finite truncation and fixed
edge regulator. Oscillatory prefactors remain, so a constant-prefactor
equivalence \(cG^\alpha[1+o(1)]\) is generally too strong. A deterministic
single-quadrature seed can have zeros; the nondegenerate covariance avoids
that lower-bound failure.

## 3. Quantum accounting and the edge domain

A consistent phase-insensitive amplifier reservoir satisfies

\[
\langle F^\dagger F\rangle=gn_{\rm sp}\hbar\omega_0\delta\delta,\qquad
\langle FF^\dagger\rangle=g(n_{\rm sp}-1)\hbar\omega_0\delta\delta,
\quad n_{\rm sp}\ge1.
\]

Hence \([F,F^\dagger]=-g\hbar\omega_0\delta\delta\) and symmetric noise is
\(g(n_{\rm sp}-1/2)\hbar\omega_0\delta\delta\).
Quantum-limited inversion is \(n_{\rm sp}=1\). Both field quadratures and
the coherent input vacuum are required; see [Caves 1982](https://doi.org/10.1103/PhysRevD.26.1817)
and [Drummond–Corney 2001](https://arxiv.org/abs/quant-ph/9912095).

The relative variables obey

\[
[n(\xi),p(\eta)]=\frac{4i}{3N_{\rm out}}\delta(\xi-\eta),\qquad
[n_l,p_m]=\frac{2i(2l+1)}{3N_{\rm out}}\delta_{lm}.
\]

Unit determinant of a relative-coordinate classical block is therefore
not a physical gain-channel commutator check. Gain expands photon-normalized
phase-space area; the inverted reservoir restores the canonical
commutator. For \([R_j,R_k]=2i\Omega_{jk}\), a Gaussian channel
\(V\mapsto XVX^T+Y\) requires
\(Y+i\Omega-iX\Omega X^T\succeq0\).

At the sharp edge, \(f=1-\xi^2\),

\[
\delta A=\sqrt{P_{\rm peak}}e^{i\phi_b}
\left[\frac{n}{2\sqrt f}+i\sqrt f\,p\right].
\]

A pure density Legendre coefficient gives a field proportional to
\(P_l/\sqrt f\), which is not square integrable. For
\(c_l=(2l+1)/2\), coherent input satisfies

\[
N_0\operatorname{Cov}(n_l,n_m)=\tfrac43c_lc_m\int fP_lP_m\,d\xi,
\]
\[
N_0\operatorname{Cov}(p_l,p_m)=\tfrac13c_lc_m\int P_lP_m/f\,d\xi.
\]

The latter diverges logarithmically. Thus a sharp-edge Legendre block is
not itself a normalized optical mode with vacuum covariance \(I\).
Smooth edges, resolution cutoffs, or suitable weighted observables are
needed. Omitting phase noise is a leading semiclassical core
approximation, not complete quantum accounting.

The edge balance suggests a fractional width
\(\delta_\xi\sim\epsilon_{\rm eff}^{2/3}\), with
\(\epsilon_{\rm eff}=\epsilon/\sqrt{aG}\). That balance does not prove
the claimed \(O(\epsilon^2|\log\epsilon|)\) observable errors or a uniform
covariance-operator estimate. Input and early ASE phase noise retain
launch-dependent coefficients; one cannot automatically replace the
launch \(\epsilon\) by the much smaller final \(\epsilon_{\rm eff}\)
in every accumulated error.

## 4. Covariance and correlation laws

### Spectral covariance

For a strongly chirped core, let \(S_0\) denote the peak mean spectrum,
\(s=\delta S/S_0\), and normalize frequency to the reference chirp edge.
This is not the locally divided spectrum \(\delta S/S(\omega)\).
Stationary phase gives

\[
s=n+\frac{\epsilon}{aa'}\mathcal Dp,\qquad
s_l=n_l-\frac{l(l+1)\epsilon}{aa'}p_l.
\]

On the exponential member \(s_l=n_l+3n_{l,\tau}\), which cancels the
\(l=1\) Jordan factor. Also \(s_0=n_0=(2/3)\delta N/N\).
For covariance eigenvalues in orthonormal \(L^2[-1,1]\), raw-coefficient
covariance must be transformed as

\[
C^{L^2}_{lm}=
\sqrt{\frac2{2l+1}}\operatorname{Cov}(s_l,s_m)
\sqrt{\frac2{2m+1}}.
\]

The reported independent ratios use degrees zero through four in this
metric. Unweighted raw Legendre coefficients give a different covariance,
and a spectral-intensity covariance is not a field quadrature covariance.

For a fixed finite projection the asymptotic structure is

\[
C_s=\begin{pmatrix}
a+o(1)&G^{-1/3}b(\tau)^T\\
G^{-1/3}b(\tau)&G^{-2/3}D(\tau)
\end{pmatrix}.
\]

If \(a>0\) and the conditional shape matrix \(D-bb^T/a\) is
uniformly positive and bounded, the Schur complement proves
\(\lambda_2/\lambda_1=\Theta(G^{-2/3})\).
The covariance's norm difference from a fixed rank-one matrix can still
be \(O(G^{-1/3})\) because of the cross block. No estimate uniform in
mode cutoff, bandwidth or edge regulator has been established.

### Matched-LO phase and energy

Define physical quadratures
\(Q_A=\delta N/\sqrt{N_{\rm out}}\),
\(Q_P=2\sqrt{N_{\rm out}}\bar p\), with shot noise one, and
\[
\bar p=\frac{\int fp\,d\xi}{\int f\,d\xi}=p_0-p_2/5.
\]
The bright-signal energy covariance is
\[
C_{AA}=G+(2n_{\rm sp}-1)(G-1).
\]
On the exponential member,
\[
\Phi_{\rm NL}=\frac{3}{2\Gamma A_*\epsilon}(G^{2/3}-1),
\qquad \theta=\epsilon\Phi_{\rm NL}.
\]
The intensity-sourced uniform phase obeys
\[
\epsilon^2N_0\operatorname{Var}p_0=
\frac49\left[\theta(\tau)^2+
(2n_{\rm sp}-1)\int_0^\tau
e^{-s}\{\theta(\tau)-\theta(s)\}^2ds\right].
\]
Consequently
\[
\operatorname{Var}p_0\sim\frac{8n_{\rm sp}}{9N_0}\Phi_{\rm NL}^2,\qquad
\boxed{C_{PP}\sim
\frac{8n_{\rm sp}}{\Gamma^2A_*^2\epsilon^2}G^{7/3}.}
\]
The printed \(G/\epsilon^2\) scaling is wrong at fixed \(\Gamma\);
the repository's numerical expression retains \(\theta^2\) and exhibits
the correct \(G^{7/3}\) behavior.

For regression on energy, integration by parts gives
\[
p_0(\tau)=\Phi_{\rm NL}(\tau)n_0(\tau)+R_0(\tau),\qquad
\operatorname{Var}R_0=O(G^{1/3}/\epsilon^2).
\]
The reservoir term in \(R_0\) is
\(-\int_0^\tau\Phi_{\rm NL}(s)dn_0(s)\); its variance grows like
\(\int e^{-s}\Phi_{\rm NL}(s)^2ds\).
The conditional \(p_2\) variance, of order \(G^{2/3}/\epsilon^2\),
dominates this regression residual, while the total phase variance is
of order \(G^{4/3}/\epsilon^2\). Thus
\[
\boxed{1-r^2=
\frac{\operatorname{Var}(\bar p\mid\delta N)}
{\operatorname{Var}\bar p}=\Theta(G^{-2/3}).}
\]
This is a finite-mode result with nondegenerate conditional noise and
generally oscillatory prefactors.

Strong correlation does not imply squeezing. In this asymptotic
matched-LO setting,
\(\lambda_{\min}(C_{\rm LO})\sim C_{AA}(1-r^2)=\Theta(G^{1/3})\).
It eventually exceeds shot noise. This does not bound every possible LO
and does not exclude finite-gain squeezing.

## 5. Explicit complete-noise squeezing counterexample

For a coherent bright input, matched initial LO, and smooth pulse, direct
first-order covariance expansion gives
\[
\left.\frac{d\lambda_{\min}}{dz}\right|_0
=2n_{\rm sp}g-
2\gamma\frac{\int\rho^2(T)dT}{\int\rho(T)dT}.
\]
The first term includes input-vacuum amplification and ASE. The second
is the smaller eigenvalue of the symmetric Kerr shear. Passive normal GVD
preserves vacuum covariance at first order. For the parabolic limit
\(\int\rho^2/\int\rho=4P_0/5\), hence
\[
\left.\lambda_{\min}'\right|_0=2n_{\rm sp}g-\frac85\gamma P_0.
\]
If \(\gamma P_0>5n_{\rm sp}g/4\), a short positive-distance interval
squeezes. The strict negative inequality is open under smooth
approximations to the parabola. The sharp square-root parabola is not in
the classical \(H^2\) generator domain of the full NLSE, so this derivative
should be formulated for a smooth regulator and its limit, rather than
silently differentiating a singular field in that domain.

At \(\epsilon=.05,\Gamma=\sqrt{18},n_{\rm sp}=1\), the limiting derivative
per \(\tau=gz\) is \(-5.54247233266\). The independent full NLSE for the
smooth launch in Section 7, at \(\tau=.02\), gives
\[
C_{\rm LO}=\begin{pmatrix}
1.040402680054&.156039389617\\
.156039389617&1.065670258932
\end{pmatrix},
\qquad \lambda_{\min}=.896486465508.
\]
This is approximately \(-.475\) dB. The determinant is 1.0843779023.
Refining 512 to 1024 grid points and halving the step changes the minimum
by \(3.5\times10^{-9}\). Complete-noise commutator and tangent-adjoint
pairing residuals are \(6.7\times10^{-14}\) and \(2.8\times10^{-14}\).
This refutes an unrestricted no-squeezing claim in the bright linearized
quantum model. It is not a result about arbitrary-power non-Gaussian
quantum evolution.

## 6. Order of limits and physical restrictions

**Brightness.** \(N_0\ge10^4\) is not sufficient at arbitrary gain.
The large uniform phase requires \(\Phi_{\rm NL}^2/N_0\ll1\) for
field linearization around a fixed mean. For
\(\epsilon=.05,\Gamma=\sqrt{18},n_{\rm sp}=1\):

| \(\tau\) | \(\Phi_{\rm NL}\) | Leading \(N_0\operatorname{Var}p_0\) | Phase RMS at \(N_0=10^4\) |
|---:|---:|---:|---:|
| 6 | 378.996 | \(1.2768\times10^5\) | 3.57 rad |
| 12 | 21071.485 | \(3.9467\times10^8\) | 198.7 rad |
| 18 | \(1.1508\times10^6\) | \(1.1773\times10^{12}\) | \(1.0850\times10^4\) rad |

Thus a formal high-gain quantum interpretation requires a joint bright
limit \(N_0\gg G^{4/3}/\epsilon^2\), or a separate phase-conditioned
nonlinear measurement theory. Small relative density noise does not
repair large random phase.

**Bandwidth.** The spectral edge scales as \(G^{1/3}\), so at fixed
gain bandwidth \(\Omega_g\) the flat-gain asymptotic window ultimately
ends. For an asymptotic edge the accumulated squared bandwidth ratio is
\[
\int_0^{\tau_L}\left(\frac{\Omega_{\rm edge}(s)}{\Omega_g}\right)^2ds
=\frac32\left(\frac{\Omega_{\rm edge,L}}{\Omega_g}\right)^2
(1-G^{-2/3}).
\]
A finite-bandwidth model also requires colored amplifier noise.
If both gain and absorption are present, their difference gives drift
and their sum gives symmetric diffusion; negative net gain is not
negative diffusion.

**Total ASE.** White ASE over infinite time and bandwidth has infinite
total photon number. Finite modal observables may remain finite, but
total counts require an aperture. For \(M\) modes, flat ideal gain,
coherent seed \(N_0\), and number-conserving Kerr/dispersion between
infinitesimal gain steps, exact total-number moments are
\[
\langle N\rangle=GN_0+Mn_{\rm sp}(G-1),
\]
\[
\operatorname{Var}N=GN_0[1+2n_{\rm sp}(G-1)]
+Mn_{\rm sp}(G-1)[1+n_{\rm sp}(G-1)].
\]
The bright-signal \(C_{AA}\) formula retains the first variance term.
Neglect of ASE–ASE counting noise needs a condition such as
\(N_0\gg n_{\rm sp}M\); it is not an exact unrestricted full-field claim.

**Launch.** Parabolic width attraction does not make all noise histories
equal. Early profile, chirp, edge and reservoir contributions affect
covariance constants. The complete NLSE tests below use a rounded
asymptotic seed and are distinct from the sharp unchirped reduced tables.

## 7. Independent numerical evidence

### Real-space finite volumes and Lyapunov propagation

The program **fv_covariance.py** builds \(\mathcal D\) from conservative
midpoint cells on \([-1,1]\), with face flux
\((1-\xi_{\rm face}^2)\Delta p/h\) and natural zero endpoint flux.
It numerically diagonalizes the symmetric tridiagonal spatial matrix and
propagates a differential covariance Lyapunov equation in \((u,w)\).
The width and accumulated nonlinear phase are integrated simultaneously
using DOP853, relative tolerance \(2\times10^{-12}\).

This is independent of the repository's analytic Legendre blocks and
fundamental-matrix noise quadrature. Legendre functions only fix the
signs of the numerical eigenvectors. Readout uses the same orthonormal
discrete eigenbasis as propagation, so its covariance metric is consistent.
Eight numerical modes are retained; spectral readout uses degrees zero
through four. Grids 32, 64, 128, 256, 512 and 1024 check convergence.
The leading runs, labelled eps=0, omit
the subleading phase source; supplementary eps=.05 runs include it at
the finite grid cutoff and expose its logarithmic edge dependence.
The exact energy covariance is reproduced with error below
\(2\times10^{-11}\).

For the exact-asymptotic launch, \(\Gamma=\sqrt{18},n_{\rm sp}=1\),
the 1024-cell leading-source results are:

| \(\tau\) | \(\lambda_2/\lambda_1\) | \(1-r^2\) |
|---:|---:|---:|
| 4 | .2779052513 | .02804376504 |
| 6 | .1304134133 | .004326973007 |
| 12 | .003031086958 | \(8.963256748\times10^{-5}\) |
| 15 | .0004141246858 | \(9.586716069\times10^{-6}\) |
| 18 | \(6.071350795\times10^{-5}\) | \(1.836600756\times10^{-6}\) |
| 24 | \(1.116748543\times10^{-6}\) | \(3.515894598\times10^{-8}\) |

For unchirped \(\Gamma=\sqrt{18}\), the pairs are
\((.3735559048,.01250544736)\) at \(\tau=4\), and
\((.1095324742,.004355962569)\) at \(\tau=6\).
For the held unchirped \(\Gamma=1\) case they are
\((.1255567758,.02110411002)\) and
\((.07570995040,.007756816177)\).
These independently reproduce the representative reduced-model numbers.

Log-linear fits of the 512-cell dense output over \(12\le\tau\le26\):

| Quantity | Fitted exponent | Derived exponent |
|---|---:|---:|
| \(N_{\rm out}\operatorname{Var}n_2\) | .32461 | \(1/3\) |
| \(\epsilon^2N_{\rm out}\operatorname{Var}p_2\) | 1.69203 | \(5/3\) |
| \(\epsilon^2 C_{PP}\) | 2.33351 | \(7/3\) |
| Spectral ratio | -.66551 | \(-2/3\) |
| Correlation deficit | -.65351 | \(-2/3\) |

Finite-window differences from exact powers reflect oscillatory
prefactors. Comparing equal oscillatory phases over two covariance
periods, from \(\tau=18\) to \(18+2\pi/\nu_2=31.32864881\),
gives density and phase exponents **.33348834 and 1.66675915**.
The residual difference comes from the still-decaying noise-injection
tail. The exact comparison times and raw readouts are stored in the JSON.

A final visual check uncovered and corrected a numerical readout defect:
midpoint quadrature against the continuous \(P_2\), instead of the native
orthonormal discrete eigenvector, leaked \(O(h^2)\) of the nondecaying
energy mode into the decaying shape readout. Its relative effect was
nonuniform at high gain. The original data are retained only as
**results_fv_midpoint_readout.json**, a diagnostic of that defect.
All tables and figures here use the corrected native-basis readout.
For example at \(\tau=26\), corrected compensated density variances for
256, 512 and 1024 cells are 1.29785754, 1.29774467 and 1.29771646;
the compensated phase values are .27477166, .27474777 and .27474180.
The 512-to-1024 changes are about \(2.2\times10^{-5}\) relative.
The fixed-grid shape slopes are unchanged to about \(10^{-12}\) between
128 and 512 cells after this correction. The known constant null mode of
the conservative operator is assigned eigenvalue zero to remove
eigensolver roundoff. This is a reduced hydrodynamic calculation, not
an NLSE edge-error certification.

### Full gain-NLSE, tangent and real adjoint

The program **lens_nlse.py** uses the exact lens coordinate
\[
\psi=\sqrt{G/a}\,U(\xi,\tau)
\exp[i\Phi-iaa'\xi^2/(2\epsilon)].
\]
Choosing \(a\) from the width ODE yields the exact deterministic equation
\[
U_\tau=-\frac{i\epsilon}{2\Gamma a^2}U_{\xi\xi}
+\frac{iG}{\Gamma\epsilon a}(|U|^2+\xi^2-1)U.
\]
Here \(a\) is a coordinate choice; \(U\) need not stay parabolic.
All spatial second derivatives and quantum pressure are retained.
Symmetric Fourier split steps use midpoint coefficients, exact cubic
tangent maps, and their exact backward real adjoint.

Initial density is
\[
|U(\xi,0)|^2=c\,\delta\log[1+\exp((1-\xi^2)/\delta)],
\qquad \delta=.25\epsilon^{2/3},
\]
where \(c\) sets energy \(4/3\), with asymptotic initial chirp.
This rounded launch is explicitly different from the main sharp,
unchirped repository seed.
Finite-energy tangent seeds are \(dU=iUP_l/\epsilon\), \(l=2,3,4\);
thus \(\epsilon p_l(0)=1,\ n_l(0)=0\). The core prediction at \(A_*=1\) is
\[
n_l(\tau)=-\frac{l(l+1)}{\Gamma\nu_l}
e^{-\tau/3}\sin(\nu_l\tau).
\]
Fits over \(1\le\tau\le6\), \(\epsilon=.05\), give:

| Degree | Grid, step | Fitted decay | Fitted frequency | Predicted frequency | Relative trajectory error |
|---:|---|---:|---:|---:|---:|
| 2 | 2048, .002 | .3338248773 | .4704012993 | .4714045208 | .0063308 |
| 2 | 4096, .001 | .3338248775 | .4704012304 | .4714045208 | .0063310 |
| 3 | 4096, .001 | .3393769333 | .7390941499 | .7453559925 | .0262212 |
| 4 | 4096, .001 | .3689066408 | .9890894090 | 1 | .0730266 |

The predicted decay is \(1/3\) throughout. The low-mode agreement is
stable under refinement. Higher modes show stronger edge/launch
transients. These are finite-distance full-field response fits, not
infinite-gain stochastic-variance fits.

For adjoints \(h_j(s)\) of physical output observables, the covariance
at \(n_{\rm sp}=1\) is
\[
C_{\rm LO}=G\left[
\operatorname{Re}\langle h_i(0),h_j(0)\rangle+
\int_0^\tau e^{-s}
\operatorname{Re}\langle h_i(s),h_j(s)\rangle ds\right].
\]
The first term includes both input quadratures; the second includes
both ASE quadratures. Its general coefficient is \(2n_{\rm sp}-1\).
The commutator uses the imaginary Gram matrix and a minus sign for the
inverted bath. Weighted trapezoids integrate the exponential weight
exactly and give the energy-mode normalization benchmark.

Spectral projections use the actual Fourier transform of the chirped
output, with an orthonormal Legendre filter inside the reference core
spectral edge; they do not insert the stationary-phase formula.
Representative results at \(\tau=4,\Gamma=\sqrt{18}\):

| \(\epsilon\) | Grid | Step | Box half-width | Spectral ratio | \(1-r^2\) | Matched-LO minimum |
|---:|---:|---:|---:|---:|---:|---:|
| .10 | 2048 | .001 | 2 | .3317394223 | .03153063336 | 3.410751835 |
| .05 | 8192 | .0005 | 4 | .3124872157 | .02920070724 | 3.159235825 |
| .025 | 8192 | .00025 | 2 | .2954726785 | .02841309541 | 3.074149802 |
| Leading sharp core | 1024 FV cells | adaptive | 1 | .2779052513 | .02804376504 | — |

These trend toward the core while retaining significant finite-edge and
launch coefficients. They do not isolate a rigorous error power in
\(\epsilon\). For \(\epsilon=.05\), box 4 and step .001, refinement
4096 to 8192 changes the spectral ratio .3125074364 to .3125001066;
halving the step gives .3124872157. Box 8, 8192 points and step .001
gives .3126869498, a residual sharp-filter/box effect of about .06%.
The LO deficit is much less box-sensitive.
The coarse .025, 4096-point, .001-step spectral value was not converged;
the table uses the refined result.

The two finest \(\tau=4\) certification cases have energy-noise error
below \(1.3\times10^{-11}\), commutator residual below
\(6.3\times10^{-11}\), and tangent-adjoint pairing discrepancy below
\(6.3\times10^{-8}\). These verify discrete normalization and noise
accounting, not continuum error bounds. A discrepancy for a rounded
asymptotic seed cannot itself refute an error estimate stated for a
different sharp unchirped seed.

## 8. Primary literature and novelty

Access scope matters. The following sources were independently examined;
selected full-text passages means the relevant equations or sections
were read, not that every line of the article was audited.

1. **Fermann et al., PRL 84, 6010 (2000)**,
   [DOI 10.1103/PhysRevLett.84.6010](https://doi.org/10.1103/PhysRevLett.84.6010),
   [institutional PDF](https://discovery.ucl.ac.uk/97897/1/97897.pdf).
   Full primary model, mean asymptotic solution and numerical-validation
   passages accessed. Establishes the mean amplifier similariton, not
   the four quantum covariance exponents.

2. **Kruglov et al., JOSA B 19, 461 (2002)**,
   [DOI 10.1364/JOSAB.19.000461](https://doi.org/10.1364/JOSAB.19.000461).
   Relevant primary article derivation accessed in a
   [public article transcription](https://www.scribd.com/document/1034463404/2-Self-similar-Propagation-of-Parabolic-Pulses-in-Normal-dispersion-Fiber-Amplifiers-figure1-3);
   publisher PDF not obtained. Establishes the quadratic-phase
   ansatz and asymptotically dropped amplitude-curvature term.

3. **Wabnitz, “Analytical Dynamics of Optical Similaritons,” QELS (2007)**,
   [DOI 10.1109/QELS.2007.4431461](https://doi.org/10.1109/QELS.2007.4431461),
   [author-accessible two-page text](https://www.researchgate.net/publication/238087766_Analytical_Dynamics_of_Optical_Similaritons).
   Full conference text accessed: parabolic hydrodynamic parameter
   dynamics and spiraling width/chirp attraction precede this work.
   The related PTL 19, 507–509 paper,
   [DOI 10.1109/LPT.2007.893823](https://doi.org/10.1109/LPT.2007.893823),
   was accessible only as an
   [institutional abstract](https://iris.uniroma1.it/handle/11573/1214370).
   Its PDF is restricted. Exact-rate priority cannot be excluded from
   an unread journal paper.

4. **Finot, Millot and Dudley, OL 29, 2533 (2004)**,
   [DOI 10.1364/OL.29.002533](https://doi.org/10.1364/OL.29.002533),
   [author-accessible primary text](https://www.researchgate.net/publication/8144220_Asymptotic_characteristics_of_parabolic_similariton_pulses_in_optical_fiber_amplifiers).
   Relevant model, input-profile/duration comparisons and experimental
   discussion accessed. Establishes mean asymptotic behavior, not
   launch-independent quantum fluctuation coefficients.

5. **Menotti and Stringari (2002), “Collective oscillations of a
   one-dimensional trapped Bose-Einstein gas,”**
   [primary preprint](https://arxiv.org/pdf/cond-mat/0201158).
   Hydrodynamic equations and Eq. (11) accessed. The mean-field
   polynomial spectrum \(l(l+1)/2\) is a close mathematical antecedent
   to the frozen parabolic-core modes, without optical gain or ASE.

6. **Fedichev and Fischer, PRA 69, 033602 (2004)**,
   [primary preprint](https://arxiv.org/pdf/cond-mat/0303063).
   Scaling, fluctuation-mode separation and quantum normalization
   passages accessed. Expansion-induced separation into static
   spatial modes and time-dependent oscillators is established
   methodology; the optical inverted reservoir differs.

7. **Drummond and Corney, “Quantum noise in optical fibers. I.
   Stochastic equations,” JOSA B 18, 139 (2001)**,
   [DOI 10.1364/JOSAB.18.000139](https://doi.org/10.1364/JOSAB.18.000139),
   [primary preprint](https://arxiv.org/pdf/quant-ph/9912095).
   Coherent input vacuum, Wigner gain/loss noise and finite-mode
   ordering corrections accessed. Full input-plus-reservoir noise
   treatment is established quantum-fiber methodology.

8. **Caves, Phys. Rev. D 26, 1817 (1982)**,
   [publisher DOI](https://doi.org/10.1103/PhysRevD.26.1817).
   Publisher abstract only was readable in this session. The
   phase-insensitive amplifier bound does not exclude Kerr-generated
   phase-sensitive squeezing.

9. **Boscolo et al. (2002), matched-asymptotic parabolic-pulse analysis**,
   [primary journal abstract](https://www.mathnet.ru/eng/tmf405),
   [Russian DOI](https://doi.org/10.4213/tmf405),
   [English DOI](https://doi.org/10.1023/A:1021402024334).
   Abstract only accessed: core, transition-layer and tail matching.
   No quantum covariance error theorem was verified from this source.

10. **Soh, Nilsson and Grudinin, JOSA B 23, 10–19 (2006)**,
    [DOI 10.1364/JOSAB.23.000010](https://doi.org/10.1364/JOSAB.23.000010),
    [publisher abstract](https://opg.optica.org/josab/abstract.cfm?uri=josab-23-1-10).
    Abstract only accessed: finite Lorentzian gain bandwidth modifies
    chirp, spectrum and compression.

An additional lead is **Wang, Liu, Song and Hu (2016), “Intensity noise
reduction of a high-power nonlinear femtosecond fiber amplifier based on
spectral-breathing self-similar parabolic pulse evolution,” Proc. SPIE
9893, 98930J, [DOI 10.1117/12.2227743](https://doi.org/10.1117/12.2227743)**.
Its abstract was located in author-profile/secondary mirrors and its
DOI in a bibliography; primary full text was not accessed. It makes a
categorical absence-of-amplifier-similariton-noise-literature claim unsafe.
Whether it anticipates any precise quantum exponent remains unverified.

The mean attractor, hydrodynamic polynomial modes, expansion-mode
separation and generic quantum noise propagation are established.
The particular single-pass gain-weighted variance exponents and the
finite-core rank-one/correlation laws were not located in the primary
passages inspected. They may constitute a useful specific synthesis,
but novelty should be claimed modestly. Restricted access to the 2007
journal article and the 2016 noise paper prevents a definitive priority
statement. Classical contraction alone is not observable quantum squeezing.

## 9. Classification

| Assertion | Assessment | Strongest supported formulation |
|---|---|---|
| Parabolic amplifier mean | Established prior result | Ideal gain-NLSE asymptotic mean and dispersionless core |
| Shape powers \(1/3,5/3\) | Independently derived and reproduced | Photon-weighted variance envelopes of each fixed \(l\ge2\) |
| Low-mode full-NLSE response | Reliable representative numerical evidence | \(l=2\) decay/frequency agree closely through \(\tau=6\), with refinement |
| Spectral ratio \(G^{-2/3}\) | Conditional reduced theorem | Fixed, correctly normalized finite projection and nondegenerate conditional noise |
| Correlation deficit \(G^{-2/3}\) | Conditional reduced theorem | Matched LO in a joint bright, broadband, regulated regime |
| \(C_{PP}\propto G/\epsilon^2\) | Incorrect | \(G^{7/3}/\epsilon^2\) at fixed \(\Gamma\) |
| ASE forbids squeezing | Incorrect without qualification | Large-gain matched-LO excess noise; finite-gain squeezing can occur |
| Sharp block is an optical vacuum mode | Incorrect without regulation and metric | Use finite-energy field modes and full physical commutators/noise |
| Uniform boundary/error rates | Unverified | Edge balance motivates a regulator, not a covariance error theorem |
| Fixed \(N_0\ge10^4\) at arbitrary gain | Incorrect | Joint bright limit, roughly \(N_0\gg\Phi_{\rm NL}^2\), plus ASE aperture control |
| Universal fluctuation launch independence | Unverified | Width attraction does not erase accumulated covariance history |
| Novel quantum phenomenon | Partly open | Potentially new specific reduced covariance synthesis, not new quantum-noise machinery |

The independent work establishes the reduced mathematics and gives a
complete-noise full-model counterexample to a stronger physical claim.
The continuum, bandwidth-limited, high-gain quantum error theorem remains
open and should not be described as already proved.
