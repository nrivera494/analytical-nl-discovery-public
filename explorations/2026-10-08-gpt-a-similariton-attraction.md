---
date: 2026-10-08
agent: gpt-a
model: gpt-6-astra
family: gpt
task: T-20261008-gpt-a-01
problem: P-001
status: completed
---

# Amplifier similariton: independent derivation and test plan

This is the first committed independent exploration. It was derived from the
gain NLSE and the PR #20 sketch, without reading claude-a's round-2 branch.
The passive claim and its already-merged derivation were read as requested.
This is not an audit of that passive claim or of claude-a's new noise claim.

## Current disposition

The material below preserves the first committed derivation and numerical plan.
The completed statements are [C-20261008-gpt-a-01](../claims/C-20261008-gpt-a-01-gain-similariton-conditional-attraction.md)
and [C-20261008-gpt-a-02](../claims/C-20261008-gpt-a-02-gain-nlse-attraction-scope.md),
with the final proof, literature access ledger and numerical report linked from
those cards. Both remain proposer-family cheap checks, awaiting independent
verification and audit. The outcome is global hydrodynamic attraction within
the parabolic family, conditional nonlinear attraction beyond that family,
an explicit sufficient compression exclusion from global classical flow,
and an exact odd-field obstruction to unrestricted strong full-NLSE attraction.
The full-NLSE density basin and an input-only physical-vacuum existence theorem
remain open. The initial uncapped rate run and underresolved long-distance
outputs are retained and explicitly disqualified where appropriate.

## Normalization and what attraction means

Write $k=\beta_2\gamma>0$, $\tau=gz$, and
$b_*^3=27kE_0/(2g^2)$, $P_*=3E_0/(4b_*)$.
Use $x=T/(b_*e^{\tau/3})$, $\rho=P_*e^{2\tau/3}R$ and
$v=gb_*e^{\tau/3}(x/3+u)$, where $v=-\beta_2\phi_T$.
Dropping quantum pressure gives exactly
$$R_\tau+(Ru)_x=0,\qquad
u_\tau+uu_x+\tfrac23u+\tfrac19x+\tfrac1{18}R_x=0.$$
The stationary mass-normalized profile is $R_*=(1-x^2)_+$, $u_*=0$.
Attraction below refers to this density/velocity normalization, not to absolute
power, absolute timing, or distance in the complex optical-field norm.

## Independent check of the orchestrator sketch

For $\rho=3E_0e^{gz}(1-T^2/b^2)/(4b)$ and $v=(b'/b)T$,
$$b''=\frac{3kE_0e^{gz}}{2b^2}.$$
Putting $b=b_*e^{\tau/3}s$ gives
$$s_{\tau\tau}+\tfrac23s_\tau+\tfrac19s=\frac1{9s^2},\quad
V=\tfrac12s_\tau^2+\tfrac1{18}s^2+\frac1{9s},\quad
V_\tau=-\tfrac23s_\tau^2.$$
Every finite-energy orbit with $s(0)>0$ remains in a compact subset of
$(0,\infty)\times\mathbb R$. The only invariant set with $V_\tau=0$ is
$(s,s_\tau)=(1,0)$. Thus convergence on this family is global, for every
finite initial chirp and nonzero positive energy. This does not imply global
classical solvability for general shapes.

For a general parabolic background define $n=\delta\rho/P(z)$ and
$\delta v=b^{-1}\psi_x$, with $P=3E_0e^{gz}/(4b)$.
The first-order Legendre blocks are
$$n_l'=\frac{l(l+1)}{b^2}\psi_l,\qquad \psi_l'=-kP n_l.$$
For $l\ge1$, eliminating $\psi_l$ gives
$$n_l''+2\frac{b'}b n_l'+\frac{l(l+1)b''}{2b}n_l=0.$$
This is the sketch's equation, with two qualifications: $n$ is the density
perturbation divided by the peak background density, NOT the pointwise relative
density $\delta\rho/\bar\rho$; and the $l=0$ density obeys $n_0'=0$.
Applying the second-order formula at $l=0$ would introduce an extraneous
$e^{-2gz/3}$ density solution; the sketch correctly calls the energy mode neutral.
The asymptotic roots for $l\ge1$ are
$$\lambda_l=\frac g3\left[-1\pm\sqrt{1-\frac{l(l+1)}2}\right].$$
The timing mode is a Jordan block, $(a+bz)e^{-gz/3}$, corresponding to ballistic
absolute timing and constant mean frequency. Width/chirp has decay $g/3$ and
angular frequency $\sqrt2g/3$. Optical phase is not a decaying coordinate.

The effective semiclassical parameter is
$$\varepsilon_{\rm eff}=\sqrt{\frac{\beta_2}{\gamma P b^2}}
=\varepsilon_* e^{-2\tau/3}s^{-1/2},\qquad
\varepsilon_*=\frac{\sqrt{18}\beta_2}{gb_*^2}.$$
The pure exponential is correct on the asymptote. No noise claim is checked here.

## A nonlinear result to establish carefully

Set $r=R/18$ and use the cumulative mass coordinate $m$, so that $x=X(m,\tau)$,
$r=1/X_m$. The equation is the damped gradient equation
$$X_{\tau\tau}+\tfrac23X_\tau+\nabla F[X]=0,\qquad
F[X]=\int\left(\frac1{2X_m}+\frac{X^2}{18}\right)dm.$$
On increasing maps, $F$ is $1/9$-strongly convex in $L^2(dm)$.
With $Y=X-X_*$, a candidate exact modulated energy is
$$\mathcal H=F[X]-F[X_*]+\tfrac12\|X_\tau+Y/3\|_{L^2(dm)}^2.$$
Direct differentiation and convexity give
$\mathcal H'\le-\mathcal H/3$ while the classical Lagrangian solution and
the integrations by parts exist. This implies a conditional, non-sharp
$W_2=O(e^{-\tau/6})$ estimate for every such global solution. It does not
prove global regularity, preserve a positive Jacobian, or justify extension
through shocks. The physical-vacuum boundary and all such qualifications must
remain in the final statement.

## Full NLSE obstruction and edge qualification

Odd complex initial fields stay odd by uniqueness and parity invariance.
After the even quadratic lens phase and dilation are removed, they remain
orthogonal to the even parabolic field. Thus universal attraction in normalized
complex $L^2$ modulo only global phase is false. A persistent central node also
rules out uniform intensity convergence on a core containing the origin. This
does not rule out convergence of mass-weighted density observables or a weaker
density norm with a shrinking notch.

Quantum pressure is singular at a physical-vacuum edge. The formal core
parameter is $\varepsilon_{\rm eff}^2$, but its edge layer has scaled thickness
$O(\varepsilon_{\rm eff}^{2/3})$. Neither bulk smallness nor the finite-family
Lyapunov function supplies a full-NLSE attraction theorem.

## Frozen numerical plan (before simulations)

All numerical outputs will receive run folders before being cited in claims.

1. Symbolic residuals for the background, transformed equations, Legendre
   blocks and Lyapunov identities; direct width-ODE rate fits over late gain
   lengths, including inward-chirped launches.
2. Full gain-NLSE maps for Gaussian, sech and super-Gaussian intensity inputs.
   Use fixed input energy, width ratio $w=\sqrt5\sigma_T/b_*$, normalized chirp
   $q=v_T/g$, and $\varepsilon_*$; report the corresponding input $N_0$ rather
   than treating it as independent of these choices. Cover both signs of chirp,
   narrower and wider launches, and several gain lengths. A finite-length map
   is not an infinite-time basin proof.
3. Readouts: mass error; width ratio; mass-weighted chirp slope; relative $L^1$
   intensity error to the energy-matched parabola; core chirp error; wing mass;
   edge-of-window and Nyquist energy. Success thresholds are descriptive and
   must be explicitly labeled as numerical tolerances.
4. Fit the paired small width/chirp response to a damped sinusoid with decay
   and frequency free. Predictions are $1/3$ and $\sqrt2/3$ per unit $gL$.
   Compare independent step, time-grid and window refinements, and an
   independent solver of the exactly transformed equation if practical.
5. Held-out tests: an inward-chirped parabolic width orbit with
   $s(0)=1.6$, $v_T/g=-0.6$; a super-Gaussian of different order from the map;
   and an odd smooth field to test the exact parity obstruction. These cases
   must not be used to tune a proposed basin boundary or fitted rates.

## Literature status at first commit

Full text read: Fermann et al. (2000), DOI:10.1103/PhysRevLett.84.6010
(UCL eprint 97897); Kruglov et al. (2002), DOI:10.1364/JOSAB.19.000461
(public HTML transcription of the nine-page article, equations partly garbled).
The latter constructs a similarity ansatz, gives numerical input-shape tests
and design criteria, and refers its stability assertion to reference 16,
an article listed as "to be submitted". Its existence as a published paper
has not yet been established. The other mandatory full-text searches remain
in progress. No novelty conclusion is frozen at this stage.
