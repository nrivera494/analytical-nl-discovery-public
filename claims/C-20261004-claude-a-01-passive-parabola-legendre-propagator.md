---
id: C-20261004-claude-a-01
problem: P-001
title: "Passive parabolic pulse: Legendre–Pöschl–Teller linear propagator, and matched-LO squeezing whose profile limit vanishes at zeta* = 4.737"
type: noise-formula
status: cheap-checks-passed
proposed_by: claude-a
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-04
updated: 2026-10-04
solver_commit: null
result: null
supersedes: C-0001
---

## Statement

**System.** A parabolic pulse is launched into passive, lossless, normal-dispersion single-mode fibre:
$$A(0,T)=\sqrt{P_0}\,(1-T^2/T_0^2)^{1/2}\,e^{iCT^2/2T_0^2}\ \text{ for }|T|<T_0,\qquad A=0\ \text{ outside}.$$
The model is $\partial_zA=-\tfrac{i}{2}\beta_2\partial_T^2A+i\gamma|A|^2A$ with $\beta_2>0$.

Dimensionless groups:
- $\varepsilon=1/N=\sqrt{\beta_2/(\gamma P_0T_0^2)}$;
- $\zeta=z/\sqrt{L_DL_{NL}}=z\sqrt{\gamma P_0\beta_2}/T_0$;
- $\xi=T/(T_0\,a(\zeta))$, the comoving time coordinate.

For the unchirped launch ($C=0$) the background obeys
$$a=\cosh^2\theta,\qquad \zeta=\tfrac{\theta}{2}+\tfrac14\sinh2\theta,\qquad \theta=\varepsilon\Phi_{NL},\qquad \mu\equiv\tanh\theta .$$
Here $\Phi_{NL}$ is the accumulated peak nonlinear phase, and $\mu$ is the fraction of the final spectral width already generated.

**(a) Linear propagator.** Take the leading order as $\varepsilon\to0$. Write a small perturbation at any $\zeta$ as $\delta A=\bar A(\nu/2+ip)$, where $\nu$ is the relative intensity and $p$ the phase in rad. Expand in Legendre polynomials:
$$n\equiv(1-\xi^2)\nu=\sum n_lP_l(\xi),\qquad p=\sum p_lP_l(\xi).$$
Then the linearized dynamics is exactly block-diagonal in $l$:
$$\begin{pmatrix}p_l\\ n_l/\varepsilon\end{pmatrix}(\mu)=M_l(\mu,\mu_0)\begin{pmatrix}p_l\\ n_l/\varepsilon\end{pmatrix}(\mu_0),$$
$$M_l=\Phi_l(\mu)\Phi_l(\mu_0)^{-1},\qquad \Phi_l=\begin{pmatrix}P_l&Q_l\\(1-\mu^2)P_l'&(1-\mu^2)Q_l'\end{pmatrix},$$
with $P_l,Q_l$ the Ferrers (Legendre) functions. Equivalently, $p_l''(\theta)+l(l+1)\,\mathrm{sech}^2\theta\,p_l=0$.

What the blocks contain:
- $l=0$: energy is conserved, and the Kerr phase is $p_0\mathrel{+}=\theta\,n_0/\varepsilon$.
- $l=1$: timing and frequency. The mean frequency is conserved and the walk-off is ballistic.
- $l=2$: width, chirp and mean phase. For $\mu_0=0$,
$$M_2=\begin{pmatrix}1-3\mu^2&-\tfrac12Q_2(\mu)\\-6\mu(1-\mu^2)&-\tfrac12(1-\mu^2)Q_2'(\mu)\end{pmatrix}.$$
- $l\ge3$: shape modes, given by the same formula.

**(b) Matched-LO noise.** The input is a coherent state, and the homodyne local oscillator is the output mean field $\bar A_{\rm out}$ at phase $\vartheta$, with shot noise equal to 1. The covariance of the amplitude and phase quadratures is
$$C_{AA}=1,\qquad C_{AP}=\langle G\rangle,\qquad C_{PP}=\langle G^2\rangle+K,$$
$$G(\xi)=\frac{4}{3\varepsilon}\Big[\theta+\tfrac12Q_2(\mu)P_2(\xi)\Big],\qquad \langle f\rangle=\tfrac34\int_{-1}^{1}(1-\xi^2)f\,d\xi .$$
Here $K\ge1$ is the edge term in (c).

As $\varepsilon\to0$ at fixed $\zeta$, the minimum variance over $\vartheta$ tends to
$$V_{\min}\to R_\infty(\mu)=\frac{\tfrac{18}{175}Q_2^2}{4\theta^2-\tfrac45\theta Q_2+\tfrac17Q_2^2}.$$
Along the fibre:
- $R_\infty=1/15$ as $\zeta\to0$ (pure SPM);
- $R_\infty=0$ at $\zeta^*=4.737126$, where $Q_2(\mu^*)=0$, $\mu^*=0.937612$ and $a^*=8.2724$;
- $R_\infty\to2/65$, logarithmically slowly, as $\zeta\to\infty$.

At $\zeta^*$ the $l=2$ density-to-phase transfer $M_{2,12}$ changes sign. The matched mode then acts as a single-mode Kerr medium.

$\zeta^*$ has a classical meaning. At fixed fibre length $L$ and fixed $T_0$, the output chirp rate $\partial_T\delta\omega$ at the pulse centre is $(\zeta\dot a/a)/(\beta_2L)$. It is stationary with respect to the launched peak power exactly where $Q_2=0$, with maximum value $1.0738/(\beta_2L)$ at $\zeta=\zeta^*$. There, a first-order power fluctuation shifts the core phase uniformly and leaves the chirp unchanged.

Sign convention: $X_P$ is the quadrature whose local oscillator is $e^{i\pi/2}\bar A_{\rm out}$. It increases with $\arg A$ in Agrawal's convention, so $C_{AP}>0$ (more power, more phase).

**(c) Leading edge correction (noise).** The edge term is
$$K=1+\tfrac13(1-M_{2,11})^2J_\delta,\qquad J_\delta=\ln\tfrac{2-\delta}{\delta}-3+O(\delta),\qquad \delta=c\,\varepsilon^{2/3}.$$
The constant $c=O(1)$ is not predicted. For $\mu_0=0$, $K=1+2\mu^4\ln(1/\varepsilon)+O(1)$.

At $\zeta^*$, where $\mathrm{Var}(G)=0$, this gives $\det C\simeq K$ and $V_{\min}\simeq9\varepsilon^2K/(16\theta^{*2})$. The asymptotic slope of $\det C$ against $\ln(1/\varepsilon)$ is $2\mu^{*4}=1.546$.

## Regime

- **Semiclassical parameter.** $\varepsilon\le0.1$ ($N\ge10$). Statements (a) and (b) are $\varepsilon\to0$ limits at fixed $\zeta$. Their errors are asserted to fall at least as fast as $\varepsilon^{4/3}$, the edge-layer volume bound. It is not determined whether the $\varepsilon^{4/3}$ terms cancel in this dynamic problem. They do cancel in the 3D trapped-condensate literature, and for the static 1D Thomas–Fermi edge by a Hastings–McLeod identity (derivation note §6). Cancellation would leave $\varepsilon^2\ln(1/\varepsilon)$ (task T-20261004-claude-a-01). Statement (c) is asymptotic in $\varepsilon^{2/3}\ll1$.
- **Distance.** $0\le\zeta\le10$ for the unchirped launch, and $0\le\zeta\le8$ for the held-out pre-chirped launch ($\mu_0=-1/2$). There is no wave breaking at leading order, and the effective $\varepsilon/\sqrt a$ falls as the pulse expands.
- **Mode index.** $l\le4$ and $l\,\varepsilon\le0.2$.
- **Third-order dispersion.** $\delta_3\equiv2N\beta_3/(3\beta_2T_0)\le0.02$.
- **Raman.** $\tau_R\zeta\le0.01$ with $\tau_R=T_R/T_0$.
- **Self-steepening.** $2N/(\omega_0T_0)\le0.02$.
- **Quantum part.** $n_0=P_0T_0/\hbar\omega_0\ge10^6$ and $\Phi_{NL}^2\ll n_0$ (Gaussian linearization). Loss and detection inefficiency must satisfy $1-\eta\ll V_{\min}$, since $V\to\eta V+1-\eta$.

**Example system** (run `2026-10-04-claude-a-c01-cheap-checks`, `example_system`). Standard fibre near 1.06 µm with $T_0=2$ ps, $P_0=500$ W, $\beta_2=20$ ps²/km and $\gamma=5$ W⁻¹km⁻¹:
- $N=22.4$ ($\varepsilon=0.045$), $\sqrt{L_DL_{NL}}=8.94$ m, and $\zeta^*$ corresponds to $L^*=42.4$ m;
- $\delta_3=0.015$ for $\beta_3=0.04$ ps³/km, $\tau_R\zeta^*=0.007$, self-steepening group 0.013, $n_0=5\times10^9$;
- every bound is met;
- 1 dB/km loss alone limits measurable squeezing at $L^*$ to about −20 dB, so the deep minimum near $\zeta^*$ is a model prediction, not a lab target;
- the chirp-rate maximum (P3) and $R_\infty$ at $\zeta\lesssim2$ are within reach.

## Assumptions

1. Scalar 1D NLSE, one polarization and one spatial mode (inherited from the model).
2. Instantaneous Kerr response. No Raman, neither classical nor spontaneous, and no self-steepening or GAWBS.
3. Second-order dispersion only.
4. Passive and lossless: no gain and no distributed noise.
5. The launch is an exact parabola with sharp edges. The effects of its corner (grid-dependent dispersive energy, radiated as fast waves) are assumed to be subleading.
6. Linearization about the mean field, a coherent input, and large photon number.
7. Hydrodynamic (dispersionless) leading order in the pulse core. The edges enter only through regularity (bounded flux) at $\xi=\pm1$, which selects $P_l$, and through the noise cut-off $\delta\propto\varepsilon^{2/3}$. The cut-off is an assumption of (c).
8. The local oscillator equals the output mean field, including its chirp. Mode matching and detection are perfect.

## Predictions

Frozen 2026-10-04. Every number below is from run `2026-10-04-claude-a-c01-cheap-checks` (`summary.json`), which evaluates the closed forms above. No NLSE simulation was used to build any of them.

**Readouts (definitions for the verifier).** All are integral moments of the output perturbation, in normalized units $x=T/T_0$, $\rho=|A|^2/P_0$ and $\xi=x/a$. Use the background values of $a$ and $\dot a=da/d\zeta$ from the formulas: $\dot a=2\mu$ for the unchirped launch, and $a=a_m\cosh^2\theta$, $\dot a=2\mu/\sqrt{a_m}$ for the held-out launch.
- $n_0=\tfrac12\int\delta\rho\,dx$;
- $n_2=\tfrac{15}{4}[a^{-2}\!\int x^2\delta\rho\,dx-\tfrac23n_0]$;
- $p_2=-\tfrac{5}{4\varepsilon}[\delta\!\int x\rho v\,dx-\dot a\,a^{-1}\!\int x^2\delta\rho\,dx]$, with $\rho v=-\varepsilon\,\mathrm{Im}(\psi^*\psi_x)$;
- $p_0=\tfrac34[\int\mathrm{Im}(\bar\psi^*\delta\psi)\,dx+\tfrac4{15}p_2]$.

Odd blocks:
- $n_1=\tfrac32a^{-1}\!\int x\delta\rho\,dx$;
- $n_3=\tfrac{35}{4}[a^{-3}\!\int x^3\delta\rho\,dx-\tfrac25n_1]$;
- $p_1=-\tfrac{3a}{4\varepsilon}[\delta\!\int\rho v\,dx-\tfrac{\dot a}{a}\!\int x\delta\rho\,dx]$;
- $p_3=-\tfrac{35}{16}\big[(\varepsilon a)^{-1}(\delta\!\int x^2\rho v\,dx-\tfrac{\dot a}{a}\!\int x^3\delta\rho\,dx)+\tfrac4{15}p_1\big]$.

Moments up to order $k$ see only $l\le k$, so these readouts are exact projections and never use the phase where the field vanishes.

Input perturbations are $\delta A_{\rm in}=\bar A_{\rm in}(\nu/2+ip)$ with polynomial $\nu$ and $p$. Examples:
- $\nu=1$ (peak power) gives $n_0=-n_2=2/3$;
- $p=\xi^2$ (chirp) gives $p_0=1/3$ and $p_2=2/3$.

**P1. Blocks, unchirped launch ($\mu_0=0$).** Matrices act on $(p_l,n_l/\varepsilon)$.

$\varepsilon\Phi_{\rm eff}$ is the matched-LO phase response to a uniform relative power change, $\bar p=\Phi_{\rm eff}\nu$, scaled by $\varepsilon$:
$$\varepsilon\Phi_{\rm eff}=\tfrac23\theta-\tfrac1{15}Q_2 .$$

| $\zeta$ | $\mu$ | $a$ | $\theta=\varepsilon\Phi_{NL}$ | $\varepsilon\Phi_{\rm eff}$ | $M_2$ | $M_3$ | $R_\infty$ | $R_\infty$ (dB) |
|---|---|---|---|---|---|---|---|---|
| 0.25 | 0.2402 | 1.0613 | 0.2450 | 0.1941 | [[0.8268, 0.2308],[-1.3583, 0.8302]] | [[0.6638, 0.2171],[-2.5560, 0.6703]] | 0.06071 | -12.17 |
| 0.5 | 0.4342 | 1.2323 | 0.4650 | 0.3602 | [[0.4345, 0.3761],[-2.1139, 0.4715]] | [[-0.0184, 0.2978],[-3.3612, 0.0467]] | 0.04749 | -13.23 |
| 1 | 0.6659 | 1.7969 | 0.8034 | 0.5933 | [[-0.3304, 0.4331],[-2.2237, -0.1118]] | [[-0.9771, 0.1737],[-1.9458, -0.6775]] | 0.02378 | -16.24 |
| 2 | 0.8367 | 3.3343 | 1.2101 | 0.8460 | [[-1.1003, 0.2947],[-1.5056, -0.5056]] | [[-1.2453, -0.1396],[0.4738, -0.7499]] | 0.005515 | -22.58 |
| 3 | 0.8961 | 5.0754 | 1.4520 | 0.9894 | [[-1.4089, 0.1606],[-1.0593, -0.5890]] | [[-1.0208, -0.3031],[1.2985, -0.5940]] | 0.001203 | -29.20 |
| 4.737 | 0.9376 | 8.2724 | 1.7179 | 1.1453 | [[-1.6373, 0.0000],[-0.6801, -0.6107]] | [[-0.6107, -0.4362],[1.7179, -0.4105]] | 0 | — |
| 6 | 0.9519 | 10.6602 | 1.8521 | 1.2238 | [[-1.7186, -0.0818],[-0.5358, -0.6074]] | [[-0.3738, -0.4858],[1.8036, -0.3312]] | 2.04e-4 | -36.90 |
| 8 | 0.9649 | 14.4965 | 2.0124 | 1.3178 | [[-1.7931, -0.1784],[-0.3994, -0.5974]] | [[-0.0810, -0.5323],[1.8402, -0.2521]] | 8.37e-4 | -30.77 |
| 10 | 0.9724 | 18.3723 | 2.1347 | 1.3897 | [[-1.8367, -0.2509],[-0.3176, -0.5878]] | [[0.1441, -0.5601],[1.8377, -0.2029]] | 1.49e-3 | -28.27 |

The $M_0$ and $M_4$ blocks are in `summary.json`. Energy, mean frequency and the linearized Hamiltonian are conserved, and the timing walk-off is ballistic. These hold at every $\varepsilon$, so they test the numerics, not the claim.

**P2. Matched-LO covariance, unchirped launch.** As $\varepsilon\to0$:
- $\varepsilon\,C_{AP}\to\tfrac23(2\theta-\tfrac15Q_2)$;
- $\varepsilon^2C_{PP}\to\tfrac49(4\theta^2-\tfrac45\theta Q_2+\tfrac17Q_2^2)$;
- $C_{AA}=1$;
- $V_{\min}\to R_\infty$, the table column.

At fixed $\zeta\ne\zeta^*$, $V_{\min}-R_\infty=O(\varepsilon^2\ln1/\varepsilon)$. For reference, the hydrodynamic finite-$\varepsilon$ values with the edge term dropped ($K=1$) are:

| $\varepsilon$ | $\zeta=1$ | $\zeta=2$ | $\zeta=8$ |
|---|---|---|---|
| 0.1 | 0.0303 | 0.00893 | 0.00227 |
| 0.05 | 0.0254 | 0.00637 | 0.00120 |
| 0.025 | 0.0242 | 0.00573 | 0.00093 |
| 0.0125 | 0.0239 | 0.00557 | 0.00086 |

**P3. Sign change.** The classical transfer $M_{2,12}$ (input $l=2$ amplitude to output $l=2$ phase) changes sign at $\zeta^*=4.737$ in the limit $\varepsilon\to0$. At fixed $\varepsilon$, the minimum over $\zeta$ of $\det C$ lies near $\zeta^*$.

Classical equivalent, testable with two noise-free runs at $P_0(1\pm\eta)$, or in the lab with FROG:
- at fixed $L$, the output chirp rate, normalized as $(\partial_T\delta\omega)\,\beta_2L$, follows $\zeta\dot a/a$;
- values: 0.7412 at $\zeta=1$, 1.0038 at 2, maximum 1.0738 at $\zeta^*$, 1.0650 at 8, 1.0387 at 20, and $\to1$ as $\zeta\to\infty$ (run `2026-10-04-claude-a-c01-cheap-checks`, B6);
- so the maximum sits at $P_0^*=(4.737)^2T_0^2/(\gamma\beta_2L^2)$.

**P4. Edge term.** Over $\zeta\in[3.5,6.5]$, $\min_\zeta\det C(\zeta;\varepsilon)$ grows without bound as $\varepsilon\to0$, following $1+3\mu^{*4}J_{c\varepsilon^{q}}$ with $q=2/3$. This tends to $1+1.546\ln(1/\varepsilon)+\text{const}$.
- How to test: fit $c$ and $q$ to at least four values of $\varepsilon$.
- Prediction: $q$ between 0.5 and 0.9, with residuals within the numerical error.
- A $\det C$ that does not grow as $\varepsilon$ decreases refutes (c).
- A fitted $q$ near 1 indicates a cut-off $\propto\varepsilon$ instead of $\varepsilon^{2/3}$ (asymptotic slope $3\mu^{*4}=2.32$).
- Why both are fitted: the local slope approaches 1.546 only slowly, because it carries the factor $2P_2(1-\delta)^2/(2-\delta)$. For example, with $c=1$ the local slope at $\varepsilon=0.0125$ is about 1.13, and with $c=4$ about 0.31 (`edge_local_slope_at_mu_star` in the run summary).

**P5. Held-out case (not used to build anything above).** Pre-chirped launch with $C=2N/\sqrt3$, i.e. $\mu_0=-1/2$:
- the pulse first compresses, to $a_m=0.75$ at $\zeta=0.3949$;
- $M_{2,12}$ changes sign at $\zeta_z=1.0115$ ($\mu_z=0.64964$), where $R_\infty=0$.

Matrices are in the input-pulse variables $(p,n/\varepsilon)$ with $\varepsilon=1/N$ of the launched pulse:

| $\zeta$ | $\mu$ | $a$ | $\varepsilon\Phi_{NL}$ | $\varepsilon\Phi_{\rm eff}$ | $M_2$ | $R_\infty$ | $R_\infty$ (dB) |
|---|---|---|---|---|---|---|---|
| 0.25 | -0.2161 | 0.7867 | 0.2856 | 0.2250 | [[0.7426, 0.2595],[-1.7889, 0.7214]] | 0.05734 | -12.42 |
| 0.5 | 0.1591 | 0.7695 | 0.6146 | 0.4580 | [[-0.0598, 0.3614],[-2.7420, -0.1496]] | 0.02769 | -15.58 |
| 1 | 0.6436 | 1.2805 | 1.1377 | 0.7596 | [[-1.0585, 0.0084],[-0.6860, -0.9393]] | 5.6e-6 | -52.5 |
| 2 | 0.8709 | 3.1051 | 1.6334 | 1.0352 | [[-0.9137, -0.4030],[0.9930, -0.6565]] | 0.00688 | -21.62 |
| 4 | 0.9476 | 7.3546 | 2.0416 | 1.2794 | [[-0.4115, -0.6125],[1.3710, -0.3896]] | 0.01037 | -19.84 |
| 8 | 0.9767 | 16.2775 | 2.3984 | 1.5023 | [[0.0885, -0.7251],[1.4103, -0.2557]] | 0.01054 | -19.77 |

**P6. Error scaling.** For the entries of $M_0$, $M_2$ and $M_3$, and for $V_{\min}$ at $\zeta\in\{1,2,8\}$, the deviation from the $\varepsilon\to0$ values falls as $\varepsilon^p$:
- asserted: $p\ge4/3$;
- $p\approx2$ with a logarithm if the edge-layer $\varepsilon^{4/3}$ terms cancel; this is not derived;
- for $V_{\min}$ at fixed $\zeta\ne\zeta^*$, the finite-shear part alone already gives $V_{\min}-R_\infty\propto\varepsilon^2$ (P2 table);
- a measured $p<1$ over $\varepsilon\in[0.0125,0.1]$ refutes (a) and (b) as stated.

## Derivation

Full derivation: `claims/notes/C-20261004-claude-a-01-derivation.md`. Machine checks: `runs/2026-10-04-claude-a-c01-cheap-checks/check.py`.

The derivation proceeds in five steps:
1. In Madelung variables, the dispersionless limit has the exact expanding-parabola solution.
2. Linearizing in the comoving coordinate $\xi$ gives $n_\zeta=-a^{-2}\partial_\xi[(1-\xi^2)\partial_\xi\phi]$ and $\phi_\zeta=-n/a$. The spatial operator is the Legendre operator, so every $P_l$ is an exact block.
3. In $\theta=\int d\zeta/a$ each block is a zero-energy reflectionless Pöschl–Teller equation, solved by $P_l(\tanh\theta)$ and $Q_l(\tanh\theta)$. The full perturbation equation is $\mathcal L_\mu\phi=\mathcal L_\xi\phi$.
4. The matched local oscillator reads only $l=0$ and $l=2$. Pulling it back to the coherent input gives (b).
5. The pulled-back phase weight is nonzero at the pulse edges, where vacuum phase noise diverges like $1/(1-\xi^2)$. This gives the logarithm in (c), cut off at the edge layer $1-|\xi|\sim\varepsilon^{2/3}$.

The separation in step 2 is a special case of Fedichev & Fischer (2004), Eqs. (22)–(25) (see Novelty search). The edge estimate for the classical blocks is a power-counting argument, not a proof.

Kept apart, as P-001 requires:
- The Legendre modes are both the instantaneous (frozen) eigenmodes and the basis in which the finite-distance propagator is block-diagonal.
- They are not the singular vectors of the propagator in the field (vacuum) metric, and not the covariance eigenmodes. Both of those mix blocks, because the vacuum covariance of the phase is $\propto1/(1-\xi^2)$.
- C-0001's singular-vector prediction is therefore not supported.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | All groups dimensionless (A6) | claude | 2026-10-04-claude-a-c01-cheap-checks | 2026-10-04 |
| Known limits | Zero length: $M_l(\mu_0,\mu_0)=I$ to $10^{-33}$ (B1). Low power ($P_0\to0$ at fixed fibre): $C\to I$, deviation $O(\Phi_{NL})$ (B4d). Pure SPM ($\zeta\to0$): $R_\infty\to1/15=1-(\int I^2)^2/\int I\!\int I^3$ (B4e). | claude | 2026-10-04-claude-a-c01-cheap-checks | 2026-10-04 |
| Symmetries | Translation $=P_1$, boost $=Q_1$, $\zeta$-shift $=P_2$, power scaling solves the $l=2$ block (A4). Linearized energy, momentum and Hamiltonian conserved (A5). The peak-power-scaling solution reproduces $\zeta^*$ as the stationary point of the output chirp rate at fixed $L$ (B6). | claude | 2026-10-04-claude-a-c01-cheap-checks | 2026-10-04 |
| Symbolic residual | Background (A1), Legendre separation for $l\le6$ (A2), Pöschl–Teller solutions (A3) all residual 0. Legendre propagator agrees with direct ODE integration in $\zeta$ to $6\times10^{-12}$ (B3); pre-chirped mapping agrees to $4\times10^{-12}$ (B5). The moment readouts recover $n_0..n_3$ and $p_0..p_3$ exactly (B7). The Hastings–McLeod edge-mass identity used in the error argument holds to $4\times10^{-6}$ (B8). | claude | 2026-10-04-claude-a-c01-cheap-checks | 2026-10-04 |
| Commutator / uncertainty | $\det M_l=1$ (B2). $[X_A,X_P]=2i$ preserved (B4a). Commutators of 20 random polynomial local oscillators preserved (B4c). $\det C\ge1$ on the grid, minimum 1.046 (B4b). | claude | 2026-10-04-claude-a-c01-cheap-checks | 2026-10-04 |
| Simulation, core regime | | | | |
| Error-scaling exponent | | | | |
| Held-out region | | | | |
| Convergence and artefacts | | | | |
| Second solver or relaxed assumption | | | | |
| Adversarial audit | | | | |
| Novelty search | See below | claude (claude-a, claude-a.1) | | 2026-10-04 |

**Novelty search (2026-10-04).** Access levels: `full text` means the named sections were read.

- **Fedichev & Fischer**, PRA 69, 033602 (2004), [arXiv:cond-mat/0303063](https://arxiv.org/abs/cond-mat/0303063). Full text, Secs. II–IV. Read by claude-a.1; Eqs. (8)–(14) and (22)–(27) re-read by claude-a.
  - It linearizes superfluid hydrodynamics about the scaling solution in a time-dependent trap. The phase fluctuation separates into static Thomas–Fermi modes times $\chi_n''+F(\tau_s)\epsilon_n^2\chi_n=0$, which it solves by WKB.
  - Our separation (step 2) is a special case. The 1D, $\gamma=2$ free-release specialization to $\mathrm{sech}^2$ is ours. The closed form $P_l,Q_l(\tanh\theta)$ was not found there.
- **Gallo & Pelinovsky**, [arXiv:0806.3516](https://arxiv.org/abs/0806.3516). Full text, Sec. 1 (from the P-001 audit). This is the frozen model problem, and the [BT] private communication cited there is unobtainable. The residual risk that [BT] contained a Gegenbauer projection of similariton perturbations stands.
- **Anderson et al.**, [DOI:10.1364/JOSAB.10.001185](https://doi.org/10.1364/JOSAB.10.001185). Abstract only. Source of the background solution.
- **Pulsed Kerr squeezing with a local oscillator matched to the pulse.**
  - Shirasaki & Haus (1990), [DOI:10.1364/JOSAB.7.000030](https://doi.org/10.1364/JOSAB.7.000030). Abstract only.
  - Bergman & Haus (1991), [DOI:10.1364/OL.16.000663](https://doi.org/10.1364/OL.16.000663). Abstract only.
  - Doerr, Shirasaki & Khatri (1994), [DOI:10.1364/JOSAB.11.000143](https://doi.org/10.1364/JOSAB.11.000143). Abstract only. Linearized numerics with dispersion report that squeezing "can even be enhanced"; this is the closest prior art for (b).
  - The profile-limited value $1-(\int I^2)^2/(\int I\int I^3)$ is probably published for Gaussian and sech pulses. It has not been confirmed, because those full texts were not read.
- **Beyond-Thomas–Fermi corrections.**
  - Fetter & Feder, [DOI:10.1103/PhysRevA.58.3185](https://doi.org/10.1103/PhysRevA.58.3185). Abstract only.
  - Zambelli & Stringari, [arXiv:cond-mat/0107464](https://arxiv.org/abs/cond-mat/0107464). Full text, Secs. I–III (claude-a.1). In 3D the correction is $\varepsilon^2$ or $\varepsilon^2\ln\varepsilon$, and the two papers disagree about the logarithm. No 1D result was found.
- Searched and not found: the closed-form propagator for 1D free expansion; any noise, squeezing or linear-response theory of parabolic pulses in passive fibre; Pöschl–Teller time dependence for expanding condensates. Exact search strings are in `log/2026-10-04_claude-a_T-20261004-claude-interactive-05.md`.

## Outcome
