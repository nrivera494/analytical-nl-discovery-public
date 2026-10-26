---
id: C-20261008-gpt-a-01
problem: P-001
title: "Gain similariton: global attraction on parabolas, conditional nonlinear attraction, and a compressive exclusion"
type: bound
status: cheap-checks-passed
proposed_by: gpt-a
proposer_model: gpt-6-astra
proposer_family: gpt
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-08
updated: 2026-10-09
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: null
---

## Statement

**Model-level theorem, conditional beyond the invariant family.** For the dispersionless limit of the scalar normal-dispersion constant-gain NLSE, put $k=\beta_2\gamma>0$, $\tau=gz$, $b_*^3=27kE_0/(2g^2)$, $B=b_*e^{\tau/3}$, $P_*=3E_0/(4b_*)$, $x=T/B$, $\rho=P_*e^{2\tau/3}R$ and $v=-\beta_2\phi_T=gB(x/3+u)$. The exact normalized equations are

$$R_\tau+(Ru)_x=0,\qquad u_\tau+uu_x+\frac23u+\frac{x}{9}+\frac{R_x}{18}=0,$$

with equilibrium $R_*=(1-x^2)_+$ and $u_*=0$.

The physical system is an unsaturated single-mode normal-dispersion fiber amplifier. The measurable reduced-model prediction is the damping and breathing of its energy-normalized duration and chirp; finite-dispersion qualifications belong to C-20261008-gpt-a-02.

For $r=R/18$ of mass $M=2/27$, let $X(m,\tau)$ and $X_*(m)$ denote the cumulative-mass inverse maps, and define

$$\mathcal F[X]=\int_0^M\left[\frac1{2X_m}+\frac{X^2}{18}\right]dm,\qquad
\mathcal H=\mathcal F[X]-\mathcal F[X_*]+\frac12\|X_\tau+(X-X_*)/3\|_{L^2(dm)}^2.$$

**Provided the classical monotone flow exists globally and has the boundary regularity below**, the direct convex-energy calculation proves

$$\mathcal H(\tau)\le\mathcal H(0)e^{-\tau/3},\qquad
\int_0^M|X-X_*|^2dm\le18\mathcal H(0)e^{-\tau/3},$$
$$\|r-r_*\|_{L^2(dx)}\le\sqrt{2\mathcal H(0)}e^{-\tau/6}.$$

These are nonlinear, nonsharp bounds; they do not prove global regularity. A weighted-Sobolev local nonlinear stability theorem for arbitrary small physical-vacuum perturbations is **not** claimed.

There is also an unconditional result **within the parabolic hydrodynamic family**. Its width $b=Bs$ satisfies

$$\ddot s+\tfrac23\dot s+s/9=1/(9s^2),\quad
\frac{d}{d\tau}\left(\dot s^2/2+s^2/18+1/(9s)\right)=-2\dot s^2/3.$$

Every $s(0)>0$, finite $\dot s(0)$ converges to $(s,\dot s)=(1,0)$. The linear width/chirp rates are $\lambda/g=(-1\pm i\sqrt2)/3$.

The linear dispersionless blocks about any parabolic background of peak density $P=3E_0e^{gz}/(4b)$ use $n=\delta\rho/P$ and $\delta v=\psi_x/b$ in $x=T/b$. For regular Legendre modes and $l\ge1$,

$$n_l'=\frac{l(l+1)}{b^2}\psi_l,\quad \psi_l'=-\beta_2\gamma Pn_l,\quad
n_l''+2\frac{b'}b n_l'+\frac{l(l+1)b''}{2b}n_l=0.$$

On the exponential asymptotic background the eigenvalues are $\lambda_l=(g/3)[-1\pm\sqrt{1-l(l+1)/2}]$. The first-order $l=0$ equation is $n_0'=0$; a second decaying density root obtained by extending the eliminated equation to that block is spurious. The $l=1$ repeated root has the generic factor $(c_1+c_2z)e^{-gz/3}$. These are peak-normalized density/displacement rates, not complex-field convergence rates.

An all-input **global classical** version is false: the sufficient compressive family below forms an interior gradient singularity before a finite upper time. This does not refute attraction of a separately defined entropy continuation.

## Regime

- $g>0$, $\beta_2\gamma>0$, $0<E_0<\infty$, and $\tau\ge0$. The equations here have $\varepsilon_{\rm eff}=0$ exactly. No finite-NLSE-error claim is attached to this theorem.
- Parabolic basin: $w=b(0)/b_*>0$, $q=v_T(0)/g\in\mathbb R$ finite. Then $\dot s(0)=w(q-1/3)$; no smallness restriction is needed. The input energy relative to a similariton of the same initial half-width is $w^{-3}$.
- The Legendre rates are first-order statements for fixed admissible mode index and small regular material displacement/velocity. In equilibrium labels $a\in[-1,1]$, one sufficient linearization scaling is $\|\eta-a\|_{C^2}+\|\eta_\tau\|_{C^1}=\delta\ll1$. No uniform nonlinear error bound or input-only global basin is inferred from this scaling.
- Beyond parabolas: fixed normalized mass, $\mathcal H(0)<\infty$, $X_m>0$ in the interior at every finite time, and a global solution in the regularity class below. This is an evolution-dependent sufficient basin, not a complete condition on initial energy, duration and chirp.
- A sufficient excluded set is specified in original hydrodynamic variables by $r_-=v-2c=-2c_0$, $r_+=v+2c=2c_0-(c_0/2)\tanh(T/\ell)$ on $|T|<R$, where $c=\sqrt{k\rho}$ and $0<\chi=g\ell/c_0<1/2$, with a finite-energy continuation satisfying $\sup_T\max(|r_+(0,T)|,|r_-(0,T)|)\le5c_0/2$. Define $G=c_0/(2\ell)$ and $z_b=4\sqrt{8/7}/[3(G-g)]$. If $R>(10c_0/g)(e^{gz_b/2}-1)$, a classical solution breaks by $z_b$ or loses regularity earlier. Such a continuation can have physical-vacuum endpoints or smooth positive decaying tails. This is sufficient, not a sharp basin boundary.

The excluded set depends on a shape derivative, which cannot be bounded using energy, rms duration and average chirp alone. Conversely, a parabolic pulse with compressive chirp stays smooth within its invariant family.

## Assumptions

1. Scalar deterministic gain-NLSE hydrodynamic limit; constant positive gain, positive normal dispersion and Kerr coefficient. No Raman, higher dispersion, self-steepening, filtering, gain bandwidth, saturation or noise.
2. Finite positive mass, second moment, internal energy and kinetic energy; centered coordinates for the displayed reference solution. Timing/boost components are allowed in the conditional estimate.
3. For the nonlinear theorem, a global classical flow with the regularity below and strict monotonicity of the mass map. This global-existence assumption does essential work.
4. A concrete sufficient compact-support class is $X(m(a),\tau)=\eta(a,\tau)$, $m_a=(1-a^2)/18$, with $\eta\in C^2([-1,1]\times[0,S])$ and $0<j_-(S)\le\eta_a\le j_+(S)<\infty$ for every finite $S$. It has a connected occupied interval, positive interior density, material endpoints and physical vacuum; the pressure boundary terms vanish. Alternatively allow smooth strictly positive tails when $r$ and its spatial derivatives through order two decay faster than every inverse power, while $u$ and its first space/time derivatives grow at most polynomially, uniformly on each finite time interval. These sufficient classes justify the displayed energy identities; they are not claimed to persist from arbitrary initial data.
5. No use of the mass-coordinate identity through a shock. No equivalence between the entropy Euler continuation and the post-breaking NLSE.
6. Linear Legendre modes require regular displacement/finite kinetic energy or zero boundary flux; merely bounded flux is insufficient. Fix mass to remove the neutral energy mode, and distinguish global phase from hydrodynamic variables.

## Predictions

Frozen first in the independent exploration and `similariton-checks` evaluator, before the numerical checks:

- Generic small width/chirp perturbations have decay $g/3$ and angular breathing frequency $\sqrt2g/3$. The joint nonlinear-ODE fit on $18\le gz\le36$ for the small-width case gives $0.333333389g$ and $0.471404851g$ (run `2026-10-08-gpt-a-similariton-checks`).
- Held-out inward launch $w=1.6$, $q=-0.6$ remains at positive width and returns. It reaches minimum normalized width $0.272252479$; the late fit gives decay $0.333343146g$ and frequency $0.471478112g$ on $24\le gz\le42$ (same run). This is ODE evidence, not a PDE existence test.
- Every admissible nonlinear mass map satisfies $\mathcal H'+\mathcal H/3\le-\|X_\tau\|_2^2/6$. Independent quadrature on nonparabolic maps checks the inequality but is not the proof (same run).
- The separately preregistered smooth physical-vacuum tests predict decay $1/3$ and frequencies $\sqrt5/3$ and $1$ for the small $l=3,4$ displacement modes. On $12\le gz\le20$, the degree-64 direct-contraction calculation measures $(0.3333333334,0.7453559926)$ and $(0.3333334570,0.9999992922)$, respectively. The held-out asymmetric nonparabolic flow keeps minimum material Jacobian $0.873614241$ through $gz=24$ and respects the conditional energy bound (run `2026-10-08-gpt-a-similariton-physical-vacuum-direct`). These are finite-time PDE checks, not a proof of the global-existence assumption.
- For the protected compression example $\chi=0.025$, $g=c_0=R=1$, the proved upper breaking gain length is $gz_b=0.0750206995$ and the required protected radius is $0.382227424<R$ (run `2026-10-08-gpt-a-similariton-checks`; exact construction in the derivation). These constants were computed independently of the finite-volume experiment.

## Derivation

See [independent derivation](notes/C-20261008-gpt-a-01-gain-similariton-derivation.md), especially its mass-coordinate strong-convexity proof and the source-corrected Riemann-gradient Riccati equation. The symbolic evaluator is [similariton_checks.py](../evaluator/similariton_checks.py). Auditors should freeze their report before reading the note.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units and sign | Explicit normalization reproduces pressure, damping and trap coefficients | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-checks | 2026-10-08 |
| Known limits | Width ODE, energy change and invariant parity identities checked | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-checks | 2026-10-08 |
| Symbolic residual | Continuity, parabolic momentum, width Lyapunov, Legendre identities and gain Riemann-gradient equation vanish | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-checks | 2026-10-08 |
| Nonlinear inequality | Direct proof; quadrature stress test on increasing nonparabolic maps | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-checks | 2026-10-08 |
| Physical-vacuum PDE | Smooth nonparabolic flows and higher Legendre modes tested with polynomial-degree refinement; direct-contraction repetition resolves backend warnings | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-physical-vacuum-direct; 2026-10-08-gpt-a-similariton-comparison | 2026-10-09 |
| Error-scaling exponent | ODE decay/frequency measured as above; not a general-PDE sharp rate | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-checks | 2026-10-08 |
| Held-out region | Strong inward parabolic launch returns with no zero width | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-checks | 2026-10-08 |
| Full-NLSE relaxed assumption | Separate claim distinguishes singular dispersion and topology | gpt-a (gpt) | gain map/rate runs in C-20261008-gpt-a-02 | 2026-10-08 |
| Cross-family check | Confirms the Claude-family formulas with the zero-block restriction, explicit density normalization, Jordan factor and boundary qualifications | gpt-a (gpt) | 2026-10-08-gpt-a-similariton-checks | 2026-10-08 |
| Adversarial audit | Not performed; proposer-family checks cannot confer audited or sim-verified status | — | — | — |
| Novelty search | Width-family attraction has prior reduced-system evidence; convex-energy method is established. Exact rate prior art unresolved without Kruglov–Harvey full text | gpt-a (gpt) | [literature note](notes/C-20261008-gpt-a-similariton-literature.md) | 2026-10-08 |
| Novelty search | Full text of Wabnitz, IEEE PTL 19, 507 (2007) (PI download, 2026-10-19): the global attraction within parabolas is shown numerically and graphically (Fig. 3, every tested input width at fixed energy), with no proof or Lyapunov function. Partly anticipated. [Review](../docs/review-2026-10-19-claude-interactive-wabnitz2007-fulltext.md) | claude-interactive (claude) | — | 2026-10-19 |

## Outcome

The unrestricted classical-attractor statement is narrowed, not accepted. The conditional nonlinear theorem and explicit compressive exclusion are proposed for independent audit. No result-folder promotion and no assertion of novelty of the width focus or Lyapunov method. A physical-vacuum global-existence theorem and a shock-admitting attraction theorem remain separate open work.
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5) | Full-text check of Wabnitz (2007); novelty row added; status unchanged | [review](../docs/review-2026-10-19-claude-interactive-wabnitz2007-fulltext.md); task T-20261008-claude-a-05 |
