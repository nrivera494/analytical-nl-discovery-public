---
agent: gpt-a
model: gpt-6-astra
family: gpt
task: T-20261010-claude-interactive-03
problem: P-20261010-claude-interactive-01
created: 2026-10-10
status: exploration
---

# Readout hierarchy and binary certificates

These are finite-dimensional statements in bright-field linearized theory.
They apply to any number of frequency bins, spatial modes and polarizations,
and to mixed Gaussian output states. No propagation approximation or purity
assumption enters the hierarchy. This note is a standard readout reduction
and a covariance-dependent certificate, not a formula in fibre parameters
that avoids computing the covariance. The problem's literature audit is
still pending; no novelty or promotion is asserted.

## Conventions and assumption ledger

Write $a_i=\alpha_i+\delta a_i$, with canonical orthonormal discrete modes,
$x_i=\delta a_i+\delta a_i^\dagger$ and
$p_i=(\delta a_i-\delta a_i^\dagger)/i$. Vacuum has covariance $V=I$.
The real vector representing a complex mode $q$ is
$q_R=(\mathop{\rm Re}q,\mathop{\rm Im}q)$, so
$X_q=q^\dagger\delta a+\delta a^\dagger q=q_R^T(x,p)$.
Set $n_i=|\alpha_i|^2$, $b_i=\sqrt{n_i}$ and $D=\operatorname{diag}n$.
Counting is linearized as
$\delta n_i=b_i X_{e_i e^{i\arg\alpha_i}}$; the mean is $n_i$ to this order.
The amplitude embedding $E$ has these orthonormal real columns, and
$A=V^{\rm amp}=E^TVE$, $\Sigma=D^{1/2}AD^{1/2}$.

Exactly dark bins are removed from $D^{-1/2}$ and from the counting
optimization. They remain in the full field covariance and in passive
networks. A limit of a weakly populated bin is distinct from an exactly
dark bin. Photon weights must define canonical modes consistently with
the propagation/no-shock convention. The numerical table uses constant
carrier photon energy except in the explicit public-notebook check.

The formulas assume ideal resolved detection, coherent means large enough
for the neglected quadratic fluctuation terms to be small, a fixed
covariance, and no extra coherent reference. For weighted counting, the
normalization is its coherent-state shot noise, $w^TDw$, not its signed
mean $w^Tn$. This normalized noise is generally not a photon-number Fano
factor. Spectral masks are unrestricted binary masks on the stated grid.
The continuum requires a separate discretization limit.

## Hierarchy and reachability

Real weighted bin counting measures $E D^{1/2}w$, whence

$$\inf_{w\ne0}\frac{w^T\Sigma w}{w^TDw}
=\lambda_{\min}(A)=\lambda_{\rm gen}.$$

For a nonempty binary mask, $T^TDT=T^Tn$ and
$u_T=b\odot T/\sqrt{n^TT}$ is a unit vector. Thus
$F[T]=u_T^TAu_T\ge\lambda_{\rm gen}$.

If one mask must be shared across modes or polarizations, collect disjoint
groups $G_j$ and set $n'_j=\sum_{i\in G_j}n_i$. The column of $M$ for a
group has entries $b_i/\sqrt{n'_j}$ within that group and zero elsewhere.
Then $M^TM=I$ and the grouped amplitude covariance is $A'=M^TAM$.
Consequently $\lambda_{\rm gen}\le\lambda_{\min}(A')$ and every binary
certificate below also applies with $(A',n')$. Resolving a mode or
polarization and forcing it to share a mask are different readout families.

Let $g=(i\alpha)_R/\|\alpha\|$ and
$\mathcal H=g^\perp$. Every amplitude column lies in $\mathcal H$.
If $Q$ is any orthonormal basis of $\mathcal H$, define
$\lambda_{\rm pass}=\lambda_{\min}(Q^TVQ)$. Inclusion of the Rayleigh
quotient domains proves

$$\boxed{\lambda_{\min}(V)\le\lambda_{\rm pass}
\le\lambda_{\rm gen}\le\min_{T\ne0}F[T].}$$

Interlacing gives $\lambda_1(V)\le\lambda_{\rm pass}\le\lambda_2(V)$.
It does not imply a small gap unless the lowest two eigenvalues are close.

Here a passive network means a photon-number-preserving Gaussian mode
unitary, and an ideal port can select an output mode or subspace. More
generally, a counted port represented by a projector $P$ measures the
linearized direction $h=P\alpha$, has coherent brightness
$\|h\|^2=\alpha^\dagger P\alpha$, and satisfies
$\operatorname{Im}(\alpha^\dagger h)=0$. Thus the same lower limit applies
to a port collecting several orthogonal modes. Rank-one mode selection
supplies the converse construction below; if additional modes enter the
port, their quadratic count noise must also pass the brightness check.

For one normalized output mode $u$ of a lossless passive network,
$a_{\rm out}=u^\dagger a$, $\beta=u^\dagger\alpha$. Its count fluctuation
is $|\beta|X_q$, where $q=u e^{i\arg\beta}$ obeys
$q^\dagger\alpha=|\beta|>0$. Hence $q_R\in\mathcal H$.
Conversely every unit $q\in\mathcal H$ with nonzero real mean overlap is
realizable (choose its sign to make $q^\dagger\alpha>0$, then complete
$q$ to a unitary). A direction with $q^\dagger\alpha=0$ is dark: one-port
counting cannot measure its linearized quadrature at fixed brightness.
It can be approached by $q_\epsilon\propto q+\epsilon\alpha/\|\alpha\|$,
whose output mean photon number is asymptotically
$\epsilon^2\|\alpha\|^2$. Thus $\lambda_{\rm pass}$ is an infimum of
formal one-port Rayleigh quotients, attained by counting only if a
minimizing direction satisfies the fluctuation-relative brightness condition
below. For a dark squeezed minimizer, a sufficient procedure is the joint
limit $\epsilon\to0$, $\epsilon^2\|\alpha\|^2\to\infty$ at fixed $V$.
It need not be reachable at fixed total pulse energy. A vacuum dark direction
is a special case: its fluctuation population vanishes, so an absolute
requirement of many photons at that port would be unnecessarily strong.

The brightness criterion can be explicit. For a displaced one-mode
Gaussian state let $n_f=\langle\delta b^\dagger\delta b\rangle$,
$m=\langle\delta b\delta b\rangle$ and $v=\operatorname{Var}X_q$.
Its exact Fano factor is

$$F_{\rm exact}=\frac{|\beta|^2v+n_f(n_f+1)+|m|^2}
{|\beta|^2+n_f}.$$

For relative linearized accuracy $\eta$, it suffices to require
$|\beta|^2\gg n_f$ and
$[n_f(n_f+1)+|m|^2]/|\beta|^2\ll\eta v$.
This is a readout condition in addition to the propagation linearization
condition such as $\Phi/\sqrt{N_{\rm ph}}\ll1$.
For a port collecting a subspace, replace $n_f$ and the quadratic variance
by its total spontaneous mean $\nu$ and the $Q$ defined below; use
$\|P\alpha\|^2\gg\nu$ and $Q/\|P\alpha\|^2\ll\eta v$.

A concrete finite-energy limit is a bright coherent mode containing $N$
photons and an independent dark squeezed-vacuum mode with variance
$s\in(0,1)$. Put $\nu=(s+s^{-1}-2)/4$, $m=(s-s^{-1})/4$,
$C=\nu(\nu+1)+m^2-s\nu$, and $\Delta=1-s$.
Mixing a coherent fraction $t$ into the counted mode gives the exact
formula above with $|\beta|^2=Nt$, $v=s+\Delta t$,
$n_f=(1-t)\nu$ and $m_f=(1-t)m$. Minimization yields

$$t_*\sim\sqrt{C/(N\Delta)},\qquad
F_{\rm port,min}=s+2\sqrt{\Delta C/N}+O_s(N^{-1}).$$

The regime is fixed $0<s<1$ and
$N\gg\max\{C/\Delta,\nu^2\Delta/C\}$.
The port grows bright as $N^{1/2}$ while its coherent fraction vanishes;
at finite $N$ it does not attain the dark squeezed variance. This is a
readout example, not a fibre propagation claim. The registered run
`2026-10-10-gpt-a-readout-reference`, `finite-port-check`, measures an
excess exponent $-0.499968$ against the predicted $-1/2$.

### Multi-port weighted counting

After a passive unitary $U$, real weighted counts measure the vector
$h=U^\dagger\operatorname{diag}(w)U\alpha=H\alpha$, with $H$ Hermitian.
The shot-noise denominator is $\|h\|^2$, and
$\mathop{\rm Im}(\alpha^\dagger h)=0$. Conversely, for any such $h$,

$$H=\frac{h\alpha^\dagger+\alpha h^\dagger}{\|\alpha\|^2}
-\frac{\alpha^\dagger h}{\|\alpha\|^4}\alpha\alpha^\dagger$$

is Hermitian and satisfies $H\alpha=h$. Diagonalizing this rank-at-most-two
matrix constructs the network and real electronic weights. Therefore
weighted passive multi-port counting has the same $\lambda_{\rm pass}$
limit, and can realize a direction dark to a single port using bright
difference channels. In particular, for $h\perp\alpha$, use the two
modes $(\hat\alpha\pm\hat h)/\sqrt2$ and opposite weights. Resolving
only the original bins instead yields $\lambda_{\rm gen}$.

For the coherent-plus-squeezed example, balanced difference counting
measures $a_1^\dagger a_2+a_2^\dagger a_1$. Its exact variance is
$Ns+\nu$, so normalization by the coherent shot noise $N$ gives
$s+\nu/N$. Both ports have coherent brightness $N/2$.
Thus this particular two-port construction approaches the same dark
quadrature with an $O(N^{-1})$ correction, faster than the optimized
one-port $O(N^{-1/2})$ approach above. Normalization by the actual total
mean count instead gives $(Ns+\nu)/(N+\nu)$; neither convention is a
Fano factor of the signed zero-mean difference itself.

These statements concern arbitrary lossless mode unitaries. A restricted
laboratory network, for example spectral phase followed by counting in
the same spectral bins, need not span the hyperplane. Such a spectral
phase alone leaves all bin counts unchanged. If vacuum ancillary modes
and attenuation are allowed, include them in $V$ and $\alpha$ before
defining the bound. Appending vacuum changes the one-port infimum to
$\min(1,\lambda_{\rm pass})$. Omitting those modes would make an
unqualified claim for *any* passive network false for an entirely noisy
thermal input.

There is a separate hardware qualification. A stationary frequency-preserving
network followed by resolved spectral counting has block-diagonal $H$.
Writing its frequency blocks as $\alpha_g,h_g$ imposes
$\operatorname{Im}(\alpha_g^\dagger h_g)=0$ for **each** populated block,
not just one global constraint. Conversely the Hermitian construction
works within every such block. Its optimum is the covariance compressed
to these blockwise hyperplanes, and lies between the unrestricted
$\lambda_{\rm pass}$ and $\lambda_{\rm gen}$. Empty blocks contribute no
linearized counting direction. With only one signal mode in each frequency
block, this restricted optimum is exactly $\lambda_{\rm gen}$ (before
adding vacuum attenuation). Arbitrary temporal-mode mixing or a different
detection basis is a stronger capability. The table's $\lambda_{\rm pass}$
is the ideal unrestricted mode-unitary limit, not a promise for a stationary
spectral phase device.

### Raman and mixed states

For linearized evolution with an independent reservoir,
$V=S V_{\rm in}S^T+Y$ with $Y\succeq0$. All arguments above use the
output covariance and mean only, so they survive tracing out phonons,
thermal occupations, multiple polarizations and multiple spatial modes.
Gaussianity is needed for the displayed exact finite-brightness correction,
not for the leading linearized hierarchy. The uncertainty certificates
below additionally require a physically normalized symmetrized covariance.

For phase-equivariant deterministic propagation, a spatially uniform scalar
phase kick at any distance becomes a global phase kick at the output.
Its reservoir covariance is proportional to $gg^T$, so it vanishes on
$\mathcal H$ and on the amplitude subspace. Thus the Raman DC phase-noise
bin must be normalized correctly for the full $V$, but it cannot change
any ideal passive-counting covariance in this scalar phase-kick model.
This statement does not remove nonuniform Raman noise or differential
phase reservoirs between modes and polarizations.

### Exact counting within the Gaussian output model

A useful qualification goes beyond the bright-count expansion without
changing the Gaussian propagation model. Let $N_{ij}=\langle\delta
a_i^\dagger\delta a_j\rangle$ and $M_{ij}=\langle\delta a_i\delta a_j\rangle$.
For a binary projector $P$, Wick's theorem gives a spontaneous mean
$\nu=\operatorname{tr}(PN)$ and an added quadratic-count variance

$$Q=\nu+\sum_{i,j\in P}(|N_{ij}|^2+|M_{ij}|^2)\ge\nu.$$

Odd Gaussian moments vanish, so
$F_{\rm exact}=(n_PF_{\rm lin}+Q)/(n_P+\nu)$.
Consequently any linearized binary lower bound $B\le1$ also bounds exact
binary photon counting in that same Gaussian state, even for a faint mask:
$F_{\rm exact}\ge B$. A bright trial mask is still needed to make a
linearized *upper* value experimentally meaningful; its explicit count
correction can be evaluated from $V$. This extension does not cover
arbitrary signed electronic weights or the non-Gaussian corrections to
the propagation model.

If a mask is exactly dark in its coherent mean, its Gaussian count Fano
factor is $Q/\nu\ge1$ whenever $\nu>0$; a port with zero total mean has
no defined Fano factor. Thus a sub-shot linearized lower bound also covers
the entirely dark masks omitted from the linearized denominator.

## A binary eigenvector certificate

Let $\lambda_1\le\lambda_2$ be the two smallest eigenvalues of $A$, and
let $v_1$ be a normalized lowest eigenvector. Define

$$\rho_b(v)=\max_{T\ne0}\frac{(\sum_i b_i v_i T_i)^2}
{\sum_i b_i^2T_i}.$$

The spectral decomposition gives the rigorous finite-grid certificate

$$\boxed{F[T]\ge B_{\rm eig}
=\lambda_2-(\lambda_2-\lambda_1)\rho_b(v_1)
\ge\lambda_{\rm gen}.}$$

The improvement is strict when $\lambda_2>\lambda_1$ and no binary mask
is parallel to $v_1$. For a degenerate lowest eigenvalue this particular
certificate reduces to $\lambda_1$; it does not fake a strict improvement.
It is exact as a lower bound within linearized finite-grid theory, with
no error order beyond the model and covariance discretization errors.

Computing $\rho_b$ does not require a combinatorial search. Write
$c_i=b_i v_i$, $d_i=b_i^2$. Since
$S^2/W=\max_s(2sS-s^2W)$, maximization over $T$ and $s$ commutes:

$$\rho_b(v)=\max_s\sum_i\max(0,2s c_i-s^2d_i).$$

For each sign of $s$, the included bins are a prefix after sorting the
positive values of $\pm v_i/b_i$ in descending order. Evaluate
$(\sum c_i)^2/\sum d_i$ for all such prefixes. This is exact in
$O(m\log m)$ after two eigenpairs. The best prefix also supplies a
binary trial mask. If its actual Fano factor is $F_r$, then
$F_r-B_{\rm eig}$ and $10\log_{10}(F_r/B_{\rm eig})$ are certified
absolute and dB gaps to this trial filter; they are not claims that the
trial filter is globally optimal. A general upper estimate is
$F_r-B_{\rm eig}\le(\lambda_{\max}(A)-\lambda_2)(1-\rho_b)$.

## Projective binary moment relaxation

For a binary filter define $Y=u_Tu_T^T$. Then

$$Y\succeq0,\quad \operatorname{tr}Y=1,\quad Y_{ij}\ge0,
\quad b_jY_{ii}-b_iY_{ij}\ge0\quad(i\ne j).$$

The last constraints use $T_i^2=T_i$ and $T_iT_j\le T_i$.
Minimizing $\operatorname{tr}(AY)$ over these necessary conditions is a
semidefinite lower bound, at least $\lambda_{\rm gen}$.
It is the homogeneous, shot-noise-normalized version of positive moment
and upper RLT constraints. A conventional Charnes–Cooper Shor formulation
uses $X=TT^T/(n^TT)$, $x=T/(n^TT)$, $\tau=1/(n^TT)$,
$\operatorname{diag}X=x$, $n^Tx=1$, and
$\begin{pmatrix}\tau&x^T\\x&X\end{pmatrix}\succeq0$, together with
$0\le X_{ij}\le x_i,x_j$ and $X_{ij}\ge x_i+x_j-\tau$.
The projective constraints avoid a poorly conditioned $\tau$ in faint bins.
They are not represented as the full Shor-plus-all-RLT relaxation.

Every nonnegative combination $K$ of the displayed inequality matrices
satisfies $u_T^TKu_T\ge0$. Thus

$$B_K=\lambda_{\min}(A-K)\le\min_TF[T].$$

This provides a simple independently checkable dual certificate: clip
computed multipliers to nonnegative values, reconstruct $K$, and compute
the full matrix's smallest eigenvalue. Subtract a stated numerical margin.
One may impose inequalities only within a bright core while retaining the
full covariance in this final eigenvalue. Merely deleting faint bins and
calling the reduced optimum a global lower bound is not valid.

The evaluator also optimizes these same nonnegative dual multipliers on the
full grid by minimizing
$\beta^{-1}\log\operatorname{tr}\exp[-\beta(A-K)]$ with bound-constrained
L-BFGS. Its gradient is obtained from the Gibbs-weighted eigenspaces.
This smooth function is an optimization device only. The reported
certificate is always the actual full-matrix $\lambda_{\min}(A-K)$,
minus its numerical margin, followed by an independent Cholesky check.
An iteration limit affects tightness, not validity of a nonnegative dual
combination. Floating-point margins and Cholesky checks are numerical
verification; they are not an interval-arithmetic proof of the simulation.

### Triangle cuts

Additional triangle cuts can be included in the same dual construction.
For distinct $i,j,k$, the binary polynomial
$T_i-T_iT_j-T_iT_k+T_jT_k$ is nonnegative. Dividing by $n^TT$ gives

$$\frac{Y_{ii}}{b_i^2}-\frac{Y_{ij}}{b_i b_j}
-\frac{Y_{ik}}{b_i b_k}+\frac{Y_{jk}}{b_j b_k}\ge0.$$

Its nonnegative dual multiplier contributes another valid term to $K$.
The implementation rescales each cut by a positive factor for conditioning,
adds all three orientations for triples in a selected bright core, and
still checks $A-K$ on the entire frequency grid. The core selection affects
tightness only. Exhaustive synthetic checks include these cuts. Triangle
refinements of reference points are additional certificates, never replacements
for the original saved outputs.

### Transferring an approximate covariance bound

If $\|A-\widetilde A\|_2\le\delta$ and the positive amplitude weights
satisfy $1-\epsilon\le b_i/\widetilde b_i\le1+\epsilon$, $\epsilon<1$,
then any certificate $\widetilde B$ for $(\widetilde A,\widetilde b)$ gives

$$\min_TF[T]\ge\widetilde B-\delta
-\epsilon[\lambda_{\max}(\widetilde A)-\lambda_{\min}(\widetilde A)].$$

For each mask, the bounded ratios give
$\cos^2\theta\ge4(1-\epsilon)(1+\epsilon)/[(1-\epsilon)+(1+\epsilon)]^2
=1-\epsilon^2$. The difference
of their rank-one projectors has trace norm twice that sine. Subtracting
the midpoint of the spectrum from $\widetilde A$ proves the stated error.
Thus an asymptotic covariance/mean approximation transfers its explicitly
bounded error orders to the binary lower bound. Uniform relative accuracy
in faint bins is a real requirement, not something inferred from a small
total field error. Successive numerical grids alone do not establish such
a rigorous continuum error enclosure.

For a brightness-constrained question there is a version that avoids
relative errors in faint bins. Work in fixed canonical coordinates with
the full covariance, let $\|\alpha-\widetilde\alpha\|\le
\epsilon_\alpha\|\alpha\|$, and require
$\|P_T\alpha\|^2\ge\eta\|\alpha\|^2$, where
$0<\epsilon_\alpha<\sqrt\eta\le1$. Projection cannot increase the mean
error, and the angle between $P_T\alpha$ and
$P_T\widetilde\alpha$ has sine at most
$\epsilon_\alpha/\sqrt\eta$. Consequently an unrestricted approximate
binary lower bound transfers to this restricted family as

$$F[T]\ge\widetilde B-\|V-\widetilde V\|_2
-\frac{\epsilon_\alpha}{\sqrt\eta}
[\lambda_{\max}(\widetilde V)-\lambda_{\min}(\widetilde V)].$$

The finite brightness condition is essential to this global-field-error
version. It is not asserted as a uniform approximation bound for arbitrary
near-dark filters.

### A stated minimum brightness

If the readout question imposes $n^TT\ge M>0$, then in addition to the
projective constraints $Y_{ii}\le n_i/M$. For any $\nu_i\ge0$ and any
valid nonnegative binary-inequality combination $K$,

$$\boxed{B_{K,\nu;M}=\lambda_{\min}(A-K+\operatorname{diag}\nu)
-\sum_i\nu_i n_i/M\le\min_{n^TT\ge M}F[T].}$$

This is a rigorous way to suppress dark directions in a conditional
certificate while retaining all bins. Simply cropping them is not. The
floor $M$ must be reported; this bound is not a bound on the unrestricted
linearized optimum. Nor does a universal fixed $M$ alone guarantee a
small Gaussian count correction: that correction still depends on the
fluctuation population and covariance.

## Local search and the absence of a universal interval theorem

Put $q=T^T\Sigma T$, $s=n^TT$ and $f=q/s$. Adding a currently blocked bin
improves $f$ exactly when
$2(\Sigma T)_i+\Sigma_{ii}-fn_i<0$. Removing a transmitted bin (with
nonempty remainder) improves it exactly when
$-2(\Sigma T)_i+\Sigma_{ii}+fn_i<0$. Equivalently, a one-flip optimum
obeys a self-consistent threshold on
$2\sum_{j\ne i}\Sigma_{ij}T_j+\Sigma_{ii}-fn_i$:
nonpositive for selected bins, nonnegative for blocked bins. Sequential
strictly improving flips terminate on the finite mask set; simultaneous
threshold updates can cycle. These conditions certify only local optimality.

No regime-agnostic fixed bound on the number of spectral intervals follows
from covariance positivity or Gaussianity. Choose equal $b_i$ and any
disconnected support $S$, let $v$ be its normalized indicator, and take
$A=aI-(a-c)vv^T$ with $0<c<a$. The unique optimal binary support is $S$.
The covariance $V=\operatorname{diag}(A,A^{-1})$ is a physical pure Gaussian
covariance. The number of intervals in $S$ is arbitrary. A fibre-specific
interval theorem would need additional structure on its propagator.

## What generic cheap certificates can and cannot do

There is a useful positivity-specific certificate in addition to the
eigenvector certificate above. Define $A^-_{ii}=A_{ii}$ and
$A^-_{ij}=\min(A_{ij},0)$ for $i\ne j$. Every binary counting vector is
nonnegative, so

$$F[T]\ge u_T^T A^-u_T\ge\lambda_{\min}(A^-).$$

Thus $\max\{\lambda_{\rm gen},\lambda_{\min}(A^-)\}$ is a rigorous
model-level bound. Unlike an ordinary Weyl split, this uses the sign
constraint on the readout. It can exceed $\lambda_{\rm gen}$ (for example,
a covariance with positive off-diagonal entries and unit diagonal), but
need not: dropping many positive correlations can make the new eigenvalue
negative. It does not use binary magnitudes and is weaker than the full
nonnegative-moment relaxation. The reference run reports it separately.

Weyl gives $\lambda_{\min}(V_{\rm vac})+\lambda_{\min}(Y)
\le\lambda_{\min}(V)$, so this full-field split can never improve an
already known exact $\lambda_{\min}(V)$. Applying the split on the
amplitude subspace may beat $\lambda_{\min}(V)$, but is at most
$\lambda_{\rm gen}$.

Temple's inequality for a trial Rayleigh quotient $\mu$ and residual $r$
requires an independently justified lower bound $\beta>\mu$ on the
second eigenvalue. It gives $\lambda_1\ge\mu-\|r\|^2/(\beta-\mu)$.
It estimates the unrestricted or amplitude eigenvalue, so it cannot beat
that eigenvalue as a filter bound. One trial filter alone does not supply
the missing spectral enclosure. The same distinction applies to
Lehmann–Goerisch eigenvalue enclosures.

The uncertainty relation gives
$\operatorname{Var}X_q\ge1/\operatorname{Var}X_{iq}$ for normalized $q$.
Bounding the conjugate variance by the largest eigenvalue of the conjugate
readout subspace gives a valid reciprocal bound, but it is no larger than
that readout subspace's actual minimum variance. Therefore the usual
amplitude-conjugate certificate cannot beat $\lambda_{\rm gen}$.
Binary-specific information about the conjugate domain could strengthen
it; the generic version does not exploit that information.

## Frozen checks before the reference sweep

The following predictions are fixed before running the main table:
the hierarchy holds to the covariance discretization error; the eigenvector
certificate and all repaired nonnegative dual certificates never exceed an
exhaustive binary minimum; the eigenvector certificate is strictly above
$\lambda_1$ whenever its measured eigenvalue gap and mismatch are nonzero;
the overlap sorting exactly matches enumeration on small masks; a diagonal
$A$ is bounded exactly by its smallest diagonal entry.
The near-zero-$\beta_2$, nonzero-$\beta_3$, Raman case is held out from
method construction. No expected numerical gap is fit to it.

## Literature and access

Searched live web/arXiv for “Gaussian quantum information covariance passive
transformations”, “quantum noise multipixel image processing”, and “binary
quadratic semidefinite relaxation RLT”, on 2026-10-10.

- Weedbrook et al., [arXiv:1110.3234](https://arxiv.org/html/1110.3234),
  DOI:10.1103/RevModPhys.84.621. **Full text**, covariance conventions,
  uncertainty relation and passive Gaussian transformations, sections II.1–II.3.
- Treps et al., [arXiv:quant-ph/0407246](https://arxiv.org/html/quant-ph/0407246),
  DOI:10.1103/PhysRevA.71.013820. **Full text**, especially sections II and III,
  including arbitrary real gains and their shot-noise normalization in Eq. (41).
- Luo et al., DOI:10.1109/MSP.2010.936019. **Abstract only**, located at the
  authors' university publication page; standard SDR background, not a novelty claim.
- Wang, Shen and van den Hengel, [arXiv:1304.0840](https://arxiv.org/abs/1304.0840).
  **Abstract only**. Located scalable binary-quadratic SDP work; not used as a
  source for an unproved approximation guarantee.

All new inequalities above are derived explicitly here. The search is not
an exhaustive novelty audit of fractional binary optimization.
