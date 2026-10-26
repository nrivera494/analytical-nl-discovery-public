# Gain similariton: independent derivation and limits of attraction

- agent: gpt-a
- model: gpt-6-astra
- family: gpt
- task: T-20261008-gpt-a-01
- status: independent derivation; no independent audit yet

This note was derived independently of the Claude-family orchestrator sketch. The first exploration and predictions were committed before any inspection of the current claude-a branch (which has not been inspected). Numerical identities and reduced-model constants refer to run `2026-10-08-gpt-a-similariton-checks`. Literature access and novelty qualifications are recorded separately in the literature note.

## Verdict on the orchestrator sketch

| Item | Independent verdict |
|---|---|
| Parabolic invariant family and width ODE | Correct in the dispersionless model; not an exact finite-energy NLSE family. |
| Width Lyapunov identity | Correct. Coercivity and LaSalle upgrade the suggested convergence to a global theorem within this family. |
| Legendre-block second-order equation | Correct for $l≥1$ when density is normalized by the peak. “Relative density” must not mean division by the local parabola. Extending the second-order equation to $l=0$ is invalid. |
| Asymptotic rates | Correct for admissible $l≥1$ modes. The sketch correctly identifies neutral energy; the double $l=1$ root also needs its Jordan factor. Neither statement implies complex-field attraction. |
| Effective semiclassical parameter | Correct asymptotically; the exact expression on a transient parabola also contains $s^{-1/2}$. |
| General-input or noise implications | Not established by the sketch. Noise is outside this task's check. |

The sketch's main hydrodynamic formulas are confirmed; the qualifications prevent extending them beyond their actual scope.

## 1. Sign convention and normalization

Assume constant $g>0$, $\beta_2>0$, $\gamma>0$, scalar field, instantaneous Kerr response, no Raman, higher dispersion, self-steepening, filtering, gain saturation or noise. Write $A=\sqrt\rho e^{i\phi}$, $v=-\beta_2\phi_T$ and $k=\beta_2\gamma$. Wherever $\rho>0$ the exact Madelung equations are

$$\rho_z+(\rho v)_T=g\rho,$$
$$v_z+vv_T=-k\rho_T+\frac{\beta_2^2}{2}\partial_T\frac{(\sqrt\rho)_{TT}}{\sqrt\rho}.$$

Deleting the last term defines the dispersionless model; it does not turn its solutions into exact NLSE solutions. Let $E_0=\int\rho(0,T)dT>0$ and

$$b_*^3=\frac{27kE_0}{2g^2},\quad P_*=\frac{3E_0}{4b_*},\quad \tau=gz,\quad B=b_*e^{\tau/3},\quad x=T/B,$$
$$\rho=P_*e^{2\tau/3}R,\qquad v=gB(x/3+u).$$

Then the dispersionless equations become exactly

$$R_\tau+(Ru)_x=0,\qquad u_\tau+uu_x+\frac23u+\frac{x}{9}+\frac{R_x}{18}=0. \tag{1}$$

The steady solution with $\int Rdx=4/3$ is $R_*=(1-x^2)_+$, $u_*=0$. Equivalently $r=R/18$ has mass $M=2/27$, pressure $p(r)=r^2/2$, confining potential $x^2/18$, and damping $2/3$. Translations and boosts in physical time become decaying/Jordan modes in these coordinates; constant optical phase is not a hydrodynamic variable.

## 2. The entire parabolic family is an invariant family of the dispersionless equations

For any $b(z)>0$,

$$\rho=\frac{3E_0e^{gz}}{4b}\left(1-\frac{T^2}{b^2}\right)_+,\qquad v=\frac{b'}bT$$

satisfies continuity. Momentum on the occupied interval is equivalent to

$$b''=\frac{3kE_0e^{gz}}{2b^2}. \tag{2}$$

The vacuum edges move with $v(\pm b)=\pm b'$. The squared sound speed vanishes linearly at these edges, so this is a physical-vacuum flow. Setting $b=Bs$ gives, with dots denoting $\tau$ derivatives,

$$\ddot s+\frac23\dot s+\frac{s}{9}=\frac1{9s^2},\qquad
V(s,\dot s)=\frac{\dot s^2}{2}+\frac{s^2}{18}+\frac1{9s},\qquad
\dot V=-\frac23\dot s^2. \tag{3}$$

For every $s(0)>0$ and finite $\dot s(0)$, a sublevel set of $V$ is compact and bounded away from $s=0$. The ODE therefore exists globally. Its only invariant subset in $\dot V=0$ is $(s,\dot s)=(1,0)$, giving global attraction within this family by LaSalle's argument. This includes arbitrarily compressive finite initial chirp: compression alone does not imply wave breaking for a parabola. Linearizing yields

$$\ddot\eta+\frac23\dot\eta+\frac13\eta=0,\qquad
\lambda_{\pm}/g=(-1\pm i\sqrt2)/3. \tag{4}$$

For a generic nonzero small perturbation the width/chirp envelope therefore decays at $g/3$ and breathes with angular frequency $\sqrt2g/3$. This is a reduced-model statement, already closely related to published stable-focus arguments; novelty is not asserted.

## 3. Legendre blocks about any parabolic background

Let $P(z)=3E_0e^{gz}/(4b)$ and use the moving coordinate $x=T/b(z)$. Define the **peak-normalized density perturbation** $n=\delta\rho/P$ and a velocity potential $\delta v=b^{-1}\psi_x$. The linearized equations, after choosing the irrelevant potential gauge, are

$$n_z=-b^{-2}\partial_x[(1-x^2)\psi_x],\qquad \psi_z=-kP n. \tag{5}$$

Expand in regular Legendre polynomials $P_l(x)$. For $l\ge1$,

$$n_l'=\frac{l(l+1)}{b^2}\psi_l,\qquad \psi_l'=-kPn_l,$$
$$n_l''+2\frac{b'}b n_l'+\frac{l(l+1)b''}{2b}n_l=0. \tag{6}$$

On the asymptotic exponential background this gives

$$\lambda_l=\frac g3\left[-1\pm\sqrt{1-\frac{l(l+1)}2}\right]. \tag{7}$$

Qualifications essential to the sketch:

- $n$ is not $\delta\rho/\bar\rho$. The latter is $n/(1-x^2)$ and generally diverges at an edge whose location is displaced. That divergence does not itself mean a singular material displacement.
- For $l=0$, (5) gives $n_0'=0$. Eliminating the first-order system as if $l(l+1)\ne0$ invents a second density solution. The apparent root $-2g/3$ is spurious in this block. The constant mode changes total energy; global phase is independently neutral.
- $l=1$ has a repeated root and the generic solution $(c_1+c_2z)e^{-gz/3}$, corresponding to physical timing/boost symmetry. It is not two distinct exponential modes.
- For $l\ge2$, (7) gives damping $g/3$ and frequency $(g/3)\sqrt{[l(l+1)-2]/2}$ in this linear dispersionless calculation. A complete nonlinear PDE rate theorem does not follow from the blocks.
- Regular material displacement, finite kinetic energy, or zero boundary flux excludes singular Legendre $Q_l$ solutions. **Bounded flux alone does not**: $(1-x^2)Q_l'$ can have a nonzero finite limit. This is a boundary-condition correction to a casual modal argument.
- The potential $\psi_l$ can grow like $e^{gz/3}$ while normalized density and relative chirp decay. Neither (6) nor (7) proves convergence of the complex optical field after removal of only the leading quadratic phase.

These are regularity-restricted interior/free-boundary linearizations, not a spectral theorem for unrestricted NLSE perturbations.

## 4. A nonlinear attraction theorem conditional on global regularity

Suppose (1) has a global classical flow with fixed mass, nonnegative density, finite internal energy and second moment, and finite kinetic energy. A concrete sufficient compact-pulse regularity class uses equilibrium mass labels $m_a=(1-a^2)/18$, $a\in[-1,1]$, and $X(m(a),\tau)=\eta(a,\tau)$: require $\eta\in C^2([-1,1]\times[0,S])$ and $0<j_-(S)\le\eta_a\le j_+(S)<\infty$ for each finite $S$. Then $r(\eta)=r_*(a)/\eta_a$ has a connected material support, positive interior density, and physical-vacuum edges with finite nonzero density slope. All energy derivatives below are integrable and the pressure boundary terms vanish. A sufficient noncompact alternative is a smooth strictly positive density with spatial derivatives through order two uniformly rapidly decaying on each finite time interval, and velocity with first space/time derivatives of at most polynomial growth. This also gives the needed integrability and zero boundary terms. These are hypotheses on the entire evolution, not a proved condition on arbitrary initial data.

Let $X(\tau,m)$ be the inverse cumulative mass map of $r=R/18$, $m\in(0,M)$. Then $X_m=1/r>0$, $X_\tau=u(\tau,X)$, and

$$X_{\tau\tau}+\frac23X_\tau+\nabla\mathcal F[X]=0,$$
$$\mathcal F[X]=\int_0^M\left(\frac1{2X_m}+\frac{X^2}{18}\right)dm,
\quad \nabla\mathcal F=\frac X9+\partial_m\frac1{2X_m^2}. \tag{8}$$

At a physical vacuum $X_m\to\infty$ and the pressure boundary term vanishes for finite edge displacements. This justifies, rather than ignores, the moving boundary. The admissible increasing maps form a convex set; $1/(2q)$ is convex for $q>0$, and the last term makes $\mathcal F$ $1/9$-strongly convex in $L^2(dm)$. Its unique minimizer is the quantile $X_*$ of $r_*=(1-x^2)_+/18$.

Put $Y=X-X_*$, $V=X_\tau$, $W=V+Y/3$ and

$$\mathcal H=\mathcal F[X]-\mathcal F[X_*]+\frac12\|W\|_2^2. \tag{9}$$

Since $W_\tau=-V/3-\nabla\mathcal F$,

$$\mathcal H'=-\frac13\|V\|_2^2-\frac19\langle Y,V\rangle-\frac13\langle Y,\nabla\mathcal F\rangle.$$

Strong convexity gives $\langle Y,\nabla\mathcal F\rangle\ge\mathcal F-\mathcal F_*+\|Y\|_2^2/18$, hence

$$\boxed{\mathcal H'+\frac13\mathcal H\le-\frac16\|V\|_2^2,\qquad
\mathcal H(\tau)\le\mathcal H(0)e^{-\tau/3}.} \tag{10}$$

Consequently the **unnormalized mass transport cost** obeys

$$D_2^2:=\int_0^M|X-X_*|^2dm\le18\mathcal H(0)e^{-\tau/3}. \tag{11}$$

The probability-normalized Wasserstein distance is $D_2/\sqrt M$. In Eulerian form, using equal masses,

$$\mathcal F[r]-\mathcal F[r_*]=\frac12\|r-r_*\|_{L^2(dx)}^2+
\int_{|x|>1}\frac{x^2-1}{18}r\,dx.$$

Thus $\|r-r_*\|_2\le\sqrt{2\mathcal H(0)}e^{-\tau/6}$ and $\|V\|_{L^2(dm)}\le2\sqrt{2\mathcal H(0)}e^{-\tau/6}$. The norm exponent $1/6$ is a nonsharp energy estimate, distinct from the linear mode exponent $1/3$.

This is a direct proof of **conditional nonlinear global attraction**. It neither constructs a global flow nor controls the high derivatives needed to keep it classical at physical vacuum. It is not a local weighted-Sobolev nonlinear stability theorem, and it does not authorize continuing (8) through shocks. The method belongs to the convex-energy/damped-Euler literature, especially Carrillo–Choi–Tse (arXiv:1712.05923, DOI:10.1007/s00220-018-3276-8); the explicit specialization here avoids importing a different gravity/Barenblatt theorem.

There is a more precise connection to the time-dependent-damping literature. In the original hydrodynamic variables set $t=e^{gz/2}-1$, $\widetilde\rho=e^{-gz}\rho$, and $\widetilde v=2v/[g(1+t)]$. Direct substitution gives

$$\widetilde\rho_t+(\widetilde\rho\widetilde v)_T=0,\qquad
\widetilde v_t+\widetilde v\widetilde v_T+\frac{\widetilde v}{1+t}
=-\frac{4k}{g^2}\widetilde\rho_T.$$

After a constant density scaling this is the polytropic-exponent-two Euler problem with damping parameters $\lambda=1$, $\mu=1$. Pan's Theorems 2.2–2.3 (arXiv:2007.14802, DOI:10.1007/s00526-020-01866-7; full text accessed, introduction and theorem statements read) require $\mu>2$ when $\lambda=1$. They therefore do not supply the missing global-existence hypothesis here. Pan's conjecture about smaller damping is not a theorem and is not used as a refutation of local stability around our exact affine flow. The new time variable also makes clear why a constant-damping Barenblatt theorem cannot simply be imported.

## 5. A sufficient wave-breaking exclusion from the classical basin

One can refute global classical attraction of all smooth inputs without relying on a damped-Euler theorem for a different force. Return to the original dispersionless equations and let $c=\sqrt{k\rho}$, $r_\pm=v\pm2c$, $D_\pm=\partial_z+(v\pm c)\partial_T$. Then

$$D_\pm r_\pm=\pm gc.$$

Writing $\alpha=\partial_T r_+$ and $\beta=\partial_T r_-$ gives

$$D_+\alpha=-\frac14(3\alpha+\beta)\alpha+\frac g4(\alpha-\beta),\quad
D_+c=\frac g2c-\frac12c\beta.$$

The exact Riccati variable $Q_+=(\alpha+g)/\sqrt c$ obeys

$$D_+Q_+=-\frac34\sqrt c\,Q_+^2+\frac{3g}{2}Q_+-\frac{g^2}{\sqrt c}; \tag{12}$$

the minus family has the same equation with $\beta$. If $Q_+(0)<0$ and $c\ge c_{\min}>0$ throughout the relevant characteristic domain, then $Q_+$ cannot turn positive and blows down no later than

$$z_b=\frac{4\sqrt{c(0)}}{3\sqrt{c_{\min}}[-\alpha(0)-g]}. \tag{13}$$

An explicit finite-domain construction makes the lower-bound assumption checkable. On $|T|<R$ prescribe

$$r_-=-2c_0,\quad r_+=2c_0-\frac{c_0}{2}\tanh(T/\ell). \tag{14}$$

Choose a finite-energy extension with $\sup_T\max(|r_+(0,T)|,|r_-(0,T)|)\le5c_0/2$; both physical-vacuum and smooth positive-tail extensions can satisfy this bound. Inside the protected interval, $r_+\ge3c_0/2$ and $r_-\le-2c_0$ initially, and the signs of their source terms preserve those bounds along the respective characteristics as long as their domain of dependence lies there. Thus $c\ge7c_0/8$ in that domain. At the center $c=c_0$, $\alpha=-c_0/(2\ell)=:-G$. The global initial invariant bound and $|gc|\le(g/2)\max(|r_+|,|r_-|)$ give $|r_\pm|\le K(z)=(5c_0/2)e^{gz/2}$ by Gronwall. Both characteristic speeds are at most $K(z)$ in magnitude. Therefore, if

$$G>g,\quad z_b=\frac{4}{3(G-g)}\sqrt{\frac87},\quad
R>\frac{10c_0}{g}(e^{gz_b/2}-1), \tag{15}$$

the characteristic from the center and its domain of dependence remain inside this prescribed interval until the upper blow-up time: the displayed radius exceeds $2\int_0^{z_b}K(s)ds$. A classical solution must lose interior gradient regularity by then, or cease being classical even earlier. The density there stays strictly positive: this is not the degeneracy at a vacuum edge. Smoothly attach (14) to positive density with physical-vacuum endpoints outside the protected interval, respecting the initial invariant bound; finite propagation then makes the attachment irrelevant to the argument. Alternatively attach smooth strictly positive rapidly decaying tails with the same bound. Thus the counterexample does not depend on requiring a compact vacuum boundary. In the compact case, classical physical-vacuum regularity refers to the occupied interval and its material endpoints, not to a prescribed velocity in empty space.

In dimensionless form the excluded family is specified by $\chi=g\ell/c_0<1/2$ and a sufficiently large $R/\ell$ satisfying (15). This is a sufficient excluded region, not a sharp threshold. Finite energy, rms duration, average chirp and soliton number do not bound the compressive derivatives in (12). A basin advertised only by those low moments omits necessary shape/regularity information.

To relate this derivative condition to optical input groups, choose an intensity scale $a$, peak $P_0$, central density $\rho_c=c_0^2/k$, $G_D=ga^2/\beta_2$ and $N_0^2=\gamma P_0a^2/\beta_2$. Then

$$\chi=\frac{\ell}{a}\frac{G_D}{N_0}\sqrt{\frac{P_0}{\rho_c}}.$$

The local semiclassical number on the compression scale is $N_\ell=N_0(\ell/a)\sqrt{\rho_c/P_0}$. Making $\ell/a$ small at fixed $N_0$ can violate a hydrodynamic approximation even though it satisfies the Euler compression criterion. Thus (15) excludes global classical Euler flow; it is not a claim of a singularity in the finite-$N_0$ field equation. The independently published unchirped-Gaussian onset estimate, written in $G_D,N_0$ in the literature ledger, has the same need for an SPM-dominated regime and does not supply a full-NLSE basin exclusion.

## 6. Dispersion is a decreasing singular perturbation, not a uniform error bound

On the parabolic family,

$$\varepsilon_{\rm eff}=\sqrt{\frac{\beta_2}{\gamma P b^2}}
=\varepsilon_*e^{-2\tau/3}s^{-1/2},\qquad
\varepsilon_*=\frac{\sqrt{18}\beta_2}{g b_*^2}. \tag{16}$$

Thus the orchestrator's exponential scaling is correct on the asymptotic family (with the transient $s$ factor). In a smooth interior region the omitted force is of formal order $\varepsilon_{\rm eff}^2$ relative to the pressure force, provided derivatives remain bounded on the similarity scale. For $R_*\sim1-|x|$, the amplitude curvature diverges at an edge. Balancing the dispersive and linear turning-point terms gives a formal layer width $|1-|x||=O(\varepsilon_{\rm eff}^{2/3})$. Boscolo et al. (DOI:10.4213/tmf405; English DOI:10.1023/A:1021402024334) explicitly derive a Painleve-II matching problem. Kruglov et al. (DOI:10.1364/JOSAB.19.000461) retain low-amplitude wings with a different chirp. These layers/wings cannot be deleted when asserting a global norm estimate.

The sharp square-root parabolic amplitude is not in $H^1$: its derivative has a logarithmically divergent squared integral at the edge. It is therefore not an exact finite-energy NLSE initial condition. The power count above is not a proved global $L^p$ error, and exponential smallness of a coefficient alone does not justify exchanging large-distance and semiclassical limits after wave breaking.

## 7. Exact full-NLSE statements

Finite-distance field existence is not the obstruction here. In one spatial dimension the cubic nonlinearity is locally Lipschitz on $H^1$, so the unitary Schrödinger group gives the local mild solution and its norm-continuation criterion. Write $K_A=(\beta_2/2)\int|A_T|^2$ and $U_A=(\gamma/2)\int|A|^4$. The positive Hamiltonian obeys

$$\frac{d}{dz}(K_A+U_A)=gK_A+2gU_A\le2g(K_A+U_A),\qquad E(z)=E_0e^{gz}.$$

These identities, first for smooth data and then by approximation, bound the $H^1$ norm on every finite interval and give global finite-distance continuation and uniqueness. A finite second moment also stays finite on each such interval, by differentiating it and applying Cauchy–Schwarz to the current. Thus the parity argument below concerns an actual global field evolution, even when its Madelung variables are undefined at a node.

Use the dimensionless realization $g=b_*=P_*=1$, $E_0=4/3$, $D=\beta_2=1/(\sqrt{18}N_*)$, $H=\gamma=N_*/\sqrt{18}$. The lens transformation, with an additional spatially constant phase to remove the chemical potential, yields

$$A(\tau,T)=e^{\tau/3}e^{-iT^2/(6D)}f(\tau,Te^{-\tau/3})\times e^{i\theta(\tau)},$$
$$f_\tau=-\frac{i}{2}De^{-2\tau/3}f_{xx}+iHe^{2\tau/3}(|f|^2+x^2-1)f. \tag{17}$$

Here $\theta'=He^{2\tau/3}$, or $\theta=3H(e^{2\tau/3}-1)/2$ with zero initial gauge phase. It restores the removed spatial constant and has no effect on any intensity/current diagnostic. With $\varepsilon=e^{-2\tau/3}/N_*$,

$$\mathcal E=\int\left[\frac{\varepsilon^2}{2}|f_x|^2+\frac12|f|^4+x^2|f|^2\right]dx,
\quad K=\frac{\varepsilon^2}{2}\int|f_x|^2dx,$$
$$\mathcal E'=-\frac43 K. \tag{18}$$

This follows from the Hamiltonian variational derivative and the explicit derivative of $\varepsilon^2$; the removed mass term has no effect because mass is conserved. It holds for sufficiently regular finite-energy fields, including fields with nodes. It bounds energy and time-integrated kinetic energy. It does **not**, by itself, identify the limiting energy with the minimum or prove attraction in density.

There is an exact obstruction to an unrestricted stronger claim. Any nonzero smooth odd input remains odd by reflection symmetry and uniqueness. Dilation, the even quadratic phase, and a constant phase preserve oddness. Its overlap with the centered even square-root parabola is zero at every distance. At equal normalized mass, the squared distance between normalized fields is exactly $2$, minimized over global phase as well. Also $|f(\tau,0)|^2=0$, so the core intensity cannot converge uniformly to $R_*(0)=1$. This counterexample does not rule out $L^p$ density convergence or moment convergence with a shrinking dark notch. Finot–Wu (DOI:10.1142/S0218863509004944) already found persistent dark/grey structures from phase steps numerically; no novelty is claimed for that physical warning.

## 8. What the word basin can mean here

A proved, explicit classical basin exists **inside the parabolic invariant family**: any positive width, finite chirp and positive finite energy. Beyond it the proved statement has the conditional basin of global regular monotone finite-energy flows, with the nonsharp transport/density rate (10)–(11). The sufficient excluded set (15) shows why the global-regularity hypothesis cannot be omitted. Neither a complete input-only physical-vacuum basin nor a shock-admitting entropy attraction theorem has been established in this work.

For the full NLSE, the reported Gaussian/sech/super-Gaussian map is a finite-length set satisfying explicitly frozen density, width, chirp and current tolerances. It is **not** a mathematical basin. Passing through a dispersive wave-breaking transient is not necessarily outside that empirical set. Odd/phase-defect inputs are excluded if the desired topology is uniform intensity or complex-field convergence. The broad positive smooth-input density-attraction claim remains a conjecture unless accompanied by a proof controlling the edge, wings and any post-breaking oscillations.
