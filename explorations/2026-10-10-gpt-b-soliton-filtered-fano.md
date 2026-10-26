---
agent: gpt-b
model: gpt-6-astra
family: gpt
task: T-20261010-claude-interactive-06
problem: P-20261010-claude-interactive-01
status: partial
---

# Soliton spectral filtering with a symmetrized Raman reservoir

Session start: 2026-10-10 10:32:55 EDT. Wall-clock deadline: 14:32:55 EDT;
reserve the final fifteen minutes for validation and delivery.

The PI explicitly assigned this derivation despite the shared problem card's
candidate/unaudited status. No problem card or other agent's task is edited.

## Current outcome

- [C-20261010-gpt-b-01](../claims/C-20261010-gpt-b-01-cutoff-raman-soliton-bound.md)
  proposes an exact cutoff-source bound in the frozen fundamental-soliton
  model. Explicit continuum kernels give its distance dependence and the
  thermal scale $2k_BT T_R/\hbar$. The physical one-sided remainder is open.
- [C-20261010-gpt-b-02](../claims/C-20261010-gpt-b-02-gaussian-coherent-width-substitution-refuted.md)
  records the failed Gaussian coherent-width substitution. Inherited
  scattering covariance is necessary; a complete Gaussian formula is open.
- Three physical held-out predictions pass their frozen accuracy targets.
  The [quartet and gap table](../runs/2026-10-10-gpt-b-soliton-solver/scored_cases.md)
  distinguishes physical propagation from frozen formulas and finite-cell
  estimates. The notebook's broader mask reaches about -9.14 to -9.17 dB;
  [its figure](../runs/2026-10-10-gpt-b-soliton-anchor/figures/anchor_binary_masks.png)
  shows the filter and vacuum/reservoir contributions.

No global binary optimum, physical continuum certificate or promotion is
claimed. The assigned task remains open, with explicit continuation tasks.

## Scope and frozen held-out cases

The study constructs the Kerr linearized map from neutral modes and the
continuum, compares it with discrete solver adjoints, and projects the
symmetrized Raman bath through the map. Physical checks retain Raman drift,
shock and third-order dispersion. Arbitrary binary-mask searches are
reported separately from contiguous or centered passbands.

The held-out case and acceptance targets are frozen in
`runs/2026-10-10-gpt-b-soliton-freeze/` before any propagation or covariance
evaluation of that case. The targets are tests, not established bounds.

## Literature access and search ledger

The initial search was kept inside the PI's forty-minute limit. Searches
used the three supplied filtering titles, the authors/year/page strings,
`"Raman noise and soliton squeezing" pdf`,
`"Perturbation theory of quantum solitons" "dB"`,
`Klaus Shaw Gaussian pulse number solitons area pi Zakharov Shabat single lobe`,
and the arXiv identifiers below. Publisher, PubMed, arXiv, author-hosted,
MIT OCW, and indexed ResearchGate copies were checked. No claim of a
complete novelty search is made. Raw PDFs/text and the failed-access
responses are under the literature run's raw directory.

| Source | Access in this session | What it establishes here |
|---|---|---|
| Levandovsky, Vasilyev & Kumar, DOI [10.1364/OL.24.000043](https://doi.org/10.1364/OL.24.000043) | **Abstract only** at publisher/PubMed; indexed partial full-text preview and figure captions also inspected, but the full PDF could not be fetched | Complete analytical amplitude-quadrature correlator including continuum and numerical filter optimization are prior art. Square filters are approximately optimal up to three soliton periods; disconnected passbands improve longer-distance filtering. The full numerical Kerr optimum and their complete formula were not read. |
| Mecozzi & Kumar, DOI [10.1364/OL.22.001232](https://doi.org/10.1364/OL.22.001232) | **Abstract only**, PubMed; publisher full text not accessed | Soliton-bandwidth/photon-number correlation and continuum-induced oscillations/finite filtering limit are prior art. A specific parabolic-filter closed form is attributed to this paper by Raginsky–Kumar; the primary formula itself was not accessed. |
| Werner & Friberg, [arXiv:quant-ph/9904104](https://arxiv.org/abs/quant-ph/9904104) | **Full text**, including the filter convention and Fig. 4 | A symmetric passband for a sech input is optimized in cutoff and distance. For $T_0=1$ ps and 300 K the paper reports 4.8 dB, cutoff $125\pm12.5$ GHz, and $3\pm0.2$ soliton periods. In the angular-frequency convention here the central cutoff is $a=\pi/4$, not 0.125. This is not a global optimum over arbitrary binary masks. Source-reported numbers are transcribed in the literature run. |
| Kärtner, Dougherty, Haus & Ippen, DOI [10.1364/JOSAB.11.001267](https://doi.org/10.1364/JOSAB.11.001267) | **Abstract only**; publisher marks full text unavailable | Quantized Raman phonons, thermal/quantum excess noise, and limits for subpicosecond soliton squeezing are prior art. No particular numerical floor or analytic coefficient is attributed to the unread full text. |
| Drummond & Corney, [arXiv:quant-ph/9912095](https://arxiv.org/abs/quant-ph/9912095), DOI 10.1364/JOSAB.18.000139 | **Full text available**, sections on Raman coupling and symmetric/Wigner noise read closely | Scalar Raman noise is proportional to $(n_{\rm th}+1/2)\alpha_R=|\operatorname{Im}h|\coth$, including zero-point noise. A measured multi-Lorentzian response is distinguished from the single oscillator. A numerical discrepancy with Werner's material model cannot be interpreted as a theory discrepancy without matching the response. |
| Corney & Drummond, [arXiv:quant-ph/9912096](https://arxiv.org/abs/quant-ph/9912096) | **Full text available**, bright-soliton perturbation and source projections read closely; equations visually checked | Projection of multiplicative Raman noise and integrated frequency-to-timing diffusion are established. The paper treats deterministic redshift as a small correction in its analytic reduction and retains it in numerical checks. This does not establish a spectral-filter noise floor from neutral modes alone. |
| Raginsky & Kumar, [arXiv:quant-ph/0104120](https://arxiv.org/abs/quant-ph/0104120) | **Full text** | Confirms the soliton-plus-continuum/filtering conventions and prior analytical correlator. Its parabolic attenuation and cascaded stages are different readouts from one binary mask. |
| Kärtner, MIT 6.977 lecture notes, chapter 3, [official course PDF](https://ocw.mit.edu/courses/6-977-ultrafast-optics-spring-2005/c439bcfab7826300aec0017e7de1f2fd_chapter3.pdf) | **Full text available**, soliton perturbation section read | Source for continuum/discrete-mode completeness and adjoint conventions; educational source, no DOI/arXiv identifier. The primary filtering papers above carry the priority attribution. |
| Klaus & Shaw, DOI [10.1103/PhysRevE.65.036607](https://doi.org/10.1103/PhysRevE.65.036607) | **Abstract only** | Real single-hump Zakharov–Shabat potentials have imaginary discrete eigenvalues. Used only to motivate a separate Gaussian soliton-content check. |
| Uddin et al., DOI [10.1038/s41566-025-01677-2](https://doi.org/10.1038/s41566-025-01677-2), [arXiv:2311.05535](https://arxiv.org/abs/2311.05535) | **Full main text** from the latest arXiv PDF; supplement not accessed | Programmable spectral filtering of a Raman-shifted soliton and pump, including disconnected filters and noisy inputs, is already demonstrated. The displayed launch is a sech pulse. This session's Gaussian tests are related regime tests, not a reproduction of that experiment. |
| Uddin et al., [arXiv:2503.12646](https://arxiv.org/abs/2503.12646) | **Full text**; model and noise-source sections read closely | Power-dependent Raman-soliton and pump correlations are calculated from input-to-output sensitivities. The authors explicitly omit the phonon Langevin contribution after estimating it to be small in their setting. That omission does not establish a symmetrized-reservoir floor for the present readout. |
| Werner, DOI [10.1103/PhysRevA.60.R781](https://doi.org/10.1103/PhysRevA.60.R781) | **Abstract only** | The connection between long-fibre edge-filtered squeezing and Raman self-frequency shift is prior art. A fixed-mask frozen-mean distance asymptote must not be substituted for the moving Raman-soliton calculation in that work. |

The outcome is a **narrowing of novelty**, not a declaration of a new
soliton-filtering mechanism. The explicit interval implementation, its
readout-restricted lower bound, and the material/temperature asymptote
need independent comparison with the unavailable load-bearing full texts.
The prior scalar projection in C-20261008-gpt-b-01 is proposed and has not
been independently verified.

## Derivation

### Exact Kerr map, including the continuum

Set $x=t/T_0$, $\zeta=z/L_D$, $L_D=T_0^2/|\beta_2|$,
$P_0=|\beta_2|/(\gamma T_0^2)$, and $q=\operatorname{sech}x$.
The convention in this section is $u_\zeta=i u_{xx}/2+i|u|^2u$.
Remove the mean phase $e^{i\zeta/2}$ and write the perturbation $r+ij$.
Its real generator is

$$A_0=\begin{pmatrix}0&L_-\\-L_+&0\end{pmatrix},\qquad
L_-=-\tfrac12\partial_x^2+\tfrac12-q^2,\quad
L_+=-\tfrac12\partial_x^2+\tfrac12-3q^2.$$

Let $f=q+xq'$. The neutral coordinates, with the real $L^2$ pairing, are
$a=\int qr$, $X=\int xqr$, $\theta=\int fj$, and
$v=-\int q'j$. They reconstruct

$$\delta u_{\rm d}(\zeta)=f a-q'(X+\zeta v)
+i q(\theta+\zeta a)+i xqv.$$

The squared-Jost continuum and its frequency are

$$U_k(x)=\frac{(k+i\tanh x)^2}{1+k^2}e^{ikx},\qquad
W_k(x)=\frac{q^2}{1+k^2}e^{ikx},\qquad E_k=\frac{1+k^2}{2},$$

$$b_k=\int[U_k^*\delta u(0)-W_k^*\delta u(0)^*]dx,$$
$$\delta u_{\rm c}(\zeta)=\int\frac{dk}{2\pi}
[U_kb_ke^{-iE_k\zeta}+W_k^*b_k^*e^{iE_k\zeta}].$$

Together these give $M_\zeta=e^{A_0\zeta}$ without numerical propagation.
They are the standard soliton linearization, not a new exact solution.
The discrete collocation evaluator independently evaluates $e^{A_0\zeta}$;
the Jost evaluator instead contracts the explicit continuum Gram kernels.

For any real spectral weight $T(k)$, put
$g_T=\mathcal F^{-1}[T(k)\widehat q(k)]$,
$\widehat q(k)=\pi\operatorname{sech}(\pi k/2)$.
With coherent-input covariance equal to the identity,

$$F[T]=\frac{\|M_\zeta^*g_T\|^2}{\|g_T\|^2}$$

for a binary mask. The neutral phase and timing readouts vanish for **every**
spectral intensity weight, so their secular shear does not appear in this
restricted readout. Omitting the continuum is therefore especially harmful:
it omits the distance dependence that filtering measures.

### Explicit centered-passband formula

For $T(k)=1_{|k|<a}$, write $c=\pi/2$,
$n_a=2\tanh(ca)$, $A_a=\tanh(ca)-ca\operatorname{sech}^2(ca)$.
Define real even $b_a(k)$ by

$$b_a(k)=\frac{\widehat q(k)}{1+k^2}
\left[(k^2-1)1_{|k|<a}-J_1(a)-J_2(k,a)\right],$$
$$J_1(a)=\int_{-a}^{a}p\tanh(cp)\,dp,\qquad
J_2(k,a)=\operatorname{PV}\int_{-a}^{a}p\coth[c(k-p)]\,dp.$$

These primitives are logarithms and dilogarithms; their explicit real
implementation is in `scripts/soliton_jost_filter.py`. They have integrable
logarithmic singularities at the filter edges, which the quadrature splits.
Let $H(p)=\pi p/\sinh(\pi p/2)$, with $H(0)=2$, and

$$D(k,l)=\frac{2(1-kl)H(k-l)}{(1+k^2)(1+l^2)},\qquad
S(k,l)=\frac{2(1+k^2+l^2+kl)H(k-l)}{3(1+k^2)(1+l^2)}.$$

The full amplitude-quadrature answer is

$$\begin{split}
n_aF_a(\zeta)={}&2A_a^2
-2A_a\int\frac{dk}{2\pi}b_a(k)\widehat q(k)\cos(E_k\zeta)
+\int\frac{dk}{2\pi}b_a(k)^2\\
&+\iint\frac{dk\,dl}{(2\pi)^2}b_a(k)b_a(l)
\{D(k,l)\cos(E_k\zeta)\cos(E_l\zeta)
+S(k,l)\sin(E_k\zeta)\sin(E_l\zeta)\}.
\end{split}$$

Completeness gives $F_a(0)=1$. Evaluating $F_a(\zeta)-F_a(0)$ cancels the
distance-independent logarithmic-square integral and improves quadrature.
The best centered edge solves $\partial_a F_a=0$, with endpoints checked.
It is an **achievable upper bound** on the unrestricted binary optimum,
not a lower bound. No elementary closed form for its minimizing root is
asserted. Linear combinations of interval coefficients give the covariance
for disconnected even masks; the evaluator also contains the odd sector.

### Lower bound from the soliton continuum operator

Let $\mathcal R_q$ map a real unit spectral-amplitude quadrature to its
time-domain quadrature with the local phase of $\widehat q$. Then

$$B_K(\zeta)=\inf\operatorname{spec}
[\mathcal R_q^*M_\zeta M_\zeta^*\mathcal R_q]
=\lambda_{\rm gen}\le\min_TF[T],$$
$$\lambda_{\min}(V)=\inf\operatorname{spec}(M_\zeta M_\zeta^*).$$

This is a rigorous lower bound in the ideal coherent-input linearized
scalar NLSE on the line. The bound follows from the shared problem card's
readout restriction; this lane supplies the soliton-specific explicit
kernel, rather than a new general readout theorem. Numerical eigenvalues
of a truncated basis need convergence and are not certified continuum
lower bounds by themselves. There is no claim that an edge optimum is
the unrestricted binary optimum.

### Symmetrized Raman source and pulse-width law

Define the material first moment including the Raman fraction,
$T_R=f_R\int_0^\infty t h_R(t)dt$. Its dimensionless source spectrum is

$$S_R(k;T_0,T)=f_R|\operatorname{Im}\widetilde h_R(k/T_0)|
\coth\!\left(\frac{\hbar|k|}{2k_BT T_0}\right).$$

In shot-noise-normalized real quadratures, the resting-soliton source is
$Q_R=4\operatorname{diag}(0,q\mathcal C_Rq)$, where $\mathcal C_R$ is the
Fourier multiplier $S_R$. Thus the **frozen-Kerr-mean** covariance is

$$V_{\rm fr}(\zeta)=M_\zeta M_\zeta^*
+\int_0^\zeta M_s Q_R M_s^*ds.$$

Its restricted eigenvalue $B_{\rm fr}=\lambda_{\min}
(\mathcal R_q^*V_{\rm fr}\mathcal R_q)$ is a rigorous bound for that
explicit frozen-mean stochastic model. Extending it to the deterministic
Raman GNLSE is an approximation, not an automatic bound. The source
normalization matches the single-mode specialization used in
C-20261008-gpt-b-01, which is **proposed and not independently verified**;
the scalar reservoir is also derived in arXiv:quant-ph/9912095 and
quant-ph/9912096. Native checks use the fetched coth helper and its finite
thermal DC bin, not the default Langevin spectrum.

For $|k|\tau_R/T_0\ll1$, with the material spectrum fixed as temperature
changes,

$$S_R(k)=\frac{T_R}{T_0}|k|\coth(\vartheta|k|)
+O((\tau_R/T_0)^3|k|^3\coth(\vartheta|k|)),\quad
\vartheta=\frac{\hbar}{2k_BT T_0}.$$

At fixed nonzero $T$ and long pulse width,

$$S_R(k)=\rho_T+O(T_0^{-2}k^2),\qquad
\rho_T=\frac{2k_BT T_R}{\hbar},$$
$$V_{\rm fr}=V_K+\rho_T\mathcal W_\zeta+O(T_0^{-2}),\qquad
\mathcal W_\zeta=4\int_0^\zeta M_s
\operatorname{diag}(0,q^2)M_s^*ds.$$

Here the covariance expansion is a quadratic-form expansion on fixed
regular readouts, or on a fixed resolved frequency subspace. It is **not**
an asserted operator-norm expansion uniform over all frequencies. The
lowest isolated eigenmodes show the corresponding order numerically;
an unrestricted uniform spectral remainder requires a separate proof.

For the single damped oscillator, this expansion has an explicit next
term. Write $a_R=1/\tau_2$, $b_R=1/\tau_1$ and
$c_R=2(b_R^2-a_R^2)/(a_R^2+b_R^2)^2$. On a bounded dimensionless
frequency range,

$$S_R(k)=\rho_T\left[1+
\left(c_R+\frac{\hbar^2}{12k_B^2T^2}\right)
\frac{k^2}{T_0^2}+O(k^4/T_0^4)\right].$$

All times in this expression use the same units. The next covariance
coefficient replaces $q^2$ in $\mathcal W_\zeta$ by
$q(-\partial_x^2)q$. At zero temperature instead,
$S_R=(T_R/T_0)|k|[1+c_R k^2/T_0^2+O(k^4/T_0^4)]$.
These are bounded-frequency asymptotic expansions. They are not
pointwise lower bounds on the spectrum at arbitrarily high frequency,
where the oscillator response eventually decays.

For the even centered passband the longitudinal integral is elementary.
Put $d=k-l$, $m=(k+l)/2$, and

$$\mathcal L(k,l)=\frac{H(d)}{(1+k^2)(1+l^2)}
\left[m^4+\frac{m^2(d^2+4)}2+
\frac{3d^4+40d^2+112}{240}\right],$$
$$I_{ss}(k,l;\zeta)=\frac\zeta2
\left[\operatorname{sinc}((E_k-E_l)\zeta)
-\operatorname{sinc}((E_k+E_l)\zeta)\right],$$

where $\operatorname{sinc}x=\sin x/x$. Then

$$\boxed{F_{a,{\rm th}}(\zeta)=F_{a,K}(\zeta)+\rho_T B_a(\zeta),\qquad
B_a=\frac4{n_a}\iint\frac{dk\,dl}{(2\pi)^2}
b_a(k)b_a(l)\mathcal L(k,l)I_{ss}(k,l;\zeta).}$$

This is exact in the white-source frozen-mean model. The identity
$\widehat{q(U_k+W_k)}(\nu)=\nu^2\widehat q(\nu-k)/(1+k^2)$
reduces its source Gram matrix to the polynomial shown. There is no
longitudinal noise propagation in this formula. The same closed source
Gram gives the even/odd amplitude covariance and hence $B_{\rm th}$.
The finite-band implementation contains the odd neutral-frequency term;
dropping it would incorrectly omit frequency jitter from asymmetric masks.

For the full colored reservoir, replace $\rho_T\mathcal L$ in the even
formula by the exact single material-frequency quadrature

$$\mathcal L_R(k,l)=\int\frac{d\nu}{2\pi}\,
S_R(\nu)\frac{\nu^4\widehat q(\nu-k)\widehat q(\nu-l)}
{(1+k^2)(1+l^2)}.$$

It is a positive Gram kernel. This expression keeps the entire oscillator
response and zero-point term, so the frozen-model filter formula does not
need the white approximation. The odd source additionally uses
$D_R=\int S_R(\nu)\nu^2H(\nu)^2d\nu/(8\pi)$ and
$J_R(k)=\int S_R(\nu)\nu^3H(\nu)\widehat q(\nu-k)
d\nu/[4\pi(1+k^2)]$. Their white limits are
$D_R=4\rho_T/15$ and
$J_R=\rho_T k(3k^2+7)\widehat q(k)/30$.

### A one-sided material reduction

For the damped oscillator with $\tau_2>\tau_1$, write
$a_R=1/\tau_2$, $b_R=1/\tau_1$ and $D_R^0=a_R^2+b_R^2$.
Its absorptive response obeys the exact identity

$$\frac{f_R\operatorname{Im}H_R(\omega)}{T_R\omega}
=\frac{(D_R^0)^2}{(D_R^0-\omega^2)^2+4a_R^2\omega^2}
\ge1\quad\text{when}\quad
0\le\omega^2\le2(b_R^2-a_R^2).$$

Define $\Omega_c=\sqrt{2(b_R^2-a_R^2)}$, $K_c=T_0\Omega_c$, and

$$S_L(k)=\frac{T_R}{T_0}|k|
\coth\!\left(\frac{\hbar|k|}{2k_BT T_0}\right)
1_{|k|\le K_c}.$$

At zero temperature replace coth by one; at $k=0$, use its finite thermal
limit. Pointwise $0\le S_L\le S_R$, so the corresponding frozen
covariances satisfy $V_L\preceq V_{\rm fr}$. Therefore

$$\boxed{B_L(\zeta;T_0,T)=\inf\operatorname{spec}
(\mathcal R_q^*V_L\mathcal R_q)
\le\lambda_{\rm gen}(V_{\rm fr})\le\min_TF_{\rm fr}[T].}$$

This is a rigorous **one-sided material approximation inside the frozen
model**, with no response-time remainder. It keeps only the material first
moment and an explicit response-time cutoff. The further spectrum
$\rho_T1_{|k|\le K_c}$ is also a lower bound at positive temperature.
Extending that white spectrum beyond the cutoff would lose the pointwise
ordering. Combining $B_L$ with the full-field bound by taking
$\max\{B_L,\lambda_{\min}(V_{\rm fr})\}$ remains a lower bound;
the tested soliton points have $B_L$ strictly higher.

The cutoff source is inserted into the same explicit Jost Gram integral,
not into a nonlinear propagation. `scripts/soliton_material_lower_bound.py`
is an independent Fourier-collocation evaluation of the ordered models.
Its eigenvalues are still finite approximations to the exact operator
bound. A second physical held-out case, including a negative third-order
coefficient, was frozen in `2026-10-10-gpt-b-soliton-freeze` before its
propagation. Whether the frozen approximation remains one-sided for that
physical deterministic model is a test, not part of this theorem.

The registered pilot cutoff calculation, including the quartet and binary
search on its 256-point frozen grid, took 0.827 s. The finest independent
physical pilot forward/covariance/search took 1141.55 s; native export and
selected-mask verification are separate (`2026-10-10-gpt-b-soliton-raman`,
`material_pilot_n256_w40.json`; `2026-10-10-gpt-b-soliton-solver`,
`pilot_finest/batch.json`). These are observed evaluator timings on the
shared machine, with different models and resolutions; they demonstrate
the practical cost separation, not an equal-accuracy speed benchmark.

There is a sharper polynomial minorant when $\tau_2>\sqrt3\tau_1$.
Put $D=a_R^2+b_R^2$, $c_R=2(b_R^2-a_R^2)/D^2$ and
$\Omega_2^2=(c_R^2D^2-1)/c_R$. Then

$$S_{L,2}(k)=\frac{T_R}{T_0}|k|\coth(\vartheta|k|)
\left(1+c_Rk^2/T_0^2\right)1_{|k|\le T_0\Omega_2}
\le S_R(k).$$

Indeed, with $y=\omega^2$, subtracting $1+c_Ry$ from
$(1-c_Ry+y^2/D^2)^{-1}$ leaves a numerator
$y^2[(c_R^2-D^{-2})-c_Ry/D^2]$. It is nonnegative on the stated
interval. Either minorant gives a rigorous frozen-model bound, and the
maximum of their restricted eigenvalue bounds remains valid. For fixed
regular readouts the sharper source error is $O(T_0^{-4})$ at positive
temperature and $O(T_0^{-5})$ at zero temperature. These orders require
frequency-tail control; they are not uniform over arbitrary masks.
The pilot's refined bound is 0.23893144, only $5.16\times10^{-6}$ below
the complete frozen amplitude eigenvalue, in the Raman run. It is still
slightly **above** the physical pilot eigenvalue: sharpening the source
does not repair the missing deterministic physical remainder.
A third physical case and the refined prediction were frozen in commit
`55d2da6` before propagation (`2026-10-10-gpt-b-soliton-freeze`).

Consequently the leading thermal penalty at **fixed normalized length**
does not decrease as $1/T_0$. At zero temperature the source and leading
penalty instead scale as $T_R/T_0$, with the $|k|$ multiplier. This is a
law for the covariance and its readouts; it is not a universal additive
constant independent of the filter or propagation distance. Optimizing
over distance must still use the Kerr-continuum and source kernels.

There is a useful distance asymptote for a **fixed**, nontrivial centered
passband. Stationary phase at the continuum threshold $k=0$ gives

$$B_a(\zeta)=\frac{14\,b_a(0)^2}{15\pi n_a}\log\zeta+O(1),\qquad
\zeta\longrightarrow\infty,$$

where $b_a(0)=\pi[-1+4\int_0^a p/\sinh(\pi p)\,dp]$.
Indeed the phase-quadrature adjoint at fixed $x$ is
$b_a(0)(2q^2-1)\sin(\zeta/2+\pi/4)/\sqrt{2\pi\zeta}
+O(\zeta^{-1}\log\zeta)$, and
$\int q^2(2q^2-1)^2dx=14/15$. The nonstationary logarithmic
filter-edge singularities give an integrable correction to its squared
source norm. This is an asymptote of the frozen white-source model, with
the mask fixed before taking the limit; it does not commute with filter
optimization or establish a long-distance physical GNLSE law.

The exact colored-source coefficient is also only a single quadrature:

$$c_{a,R}(T_0,T)=\frac{b_a(0)^2}{\pi n_a}\mathcal L_R(0,0),\qquad
\mathcal L_R(0,0)=\int\frac{d\nu}{2\pi}
S_R(\nu)\nu^4\widehat q(\nu)^2.$$

At positive temperature its first two long-pulse terms are
$\rho_T[14/15+(62/21)(c_R+\hbar^2/(12k_B^2T^2))/T_0^2]$.
At zero temperature the leading threshold Gram is
$(T_R/T_0)450\zeta_{\mathrm R}(5)/\pi^5$, where
$\zeta_{\mathrm R}$ is the Riemann zeta function. These are asymptotes of
the displayed fixed-readout integral, whose exponentially decaying weight
controls the frequency tails. They are not operator-norm expansions over
arbitrary filters. `colored_log_coefficient.json` in the Raman run checks
the coefficients against the full oscillator quadrature.

The slow apparent convergence of $\zeta B_a'(\zeta)$ is explained by
the filter edges. Put $Q_a=\widehat q(a)/(1+a^2)$,
$\ell_a=Q_a a/c$, $j_a=Q_a(a^2-1)$, and
$S_a(x)=\operatorname{Re}[U_a(x)+W_a(x)]$. Besides the threshold term,
the phase-quadrature adjoint contains

$$h_{\rm edge}(x,\zeta)=-\frac{S_a(x)}{a\zeta}
\left[\ell_a\sin(E_a\zeta)+\frac{j_a}{\pi}\cos(E_a\zeta)\right].$$

This follows from the logarithm and jump in $b_a$ at each edge. Its
interference with the threshold term gives an oscillating
$O(\zeta^{-1/2})$ correction to $\zeta B_a'$. Subtracting the explicit
threshold-plus-edge prediction substantially reduces the error in the
period-averaged numerical growth; the quadrature refinement is retained in
`log_growth_fine.json`. For a fixed $a>0$, the integrated result sharpens
to $B_a=c_a\log\zeta+C_a+O(\zeta^{-1})$, with constants that are not
uniform as $a\to0$. No large-distance physical claim follows from this
frozen-propagator asymptote.

At the opposite, short-distance limit, let $g=\mathcal F^{-1}
[1_{|k|<a}\widehat q]$ and $n=\|g\|^2$. Direct expansion of the same
propagator gives

$$F_{a,K}=1+A_a^{(2)}\zeta^2+O(\zeta^4),\qquad
A_a^{(2)}=\frac1n\int q^2[(g')^2-\tanh^2x\,g^2]dx,$$
$$F_{a,R}=\frac{4\zeta^3}{3n}
\langle qL_-g,\mathcal C_R qL_-g\rangle+O(\zeta^5).$$

Thus a fixed symmetric passband has cubic leading reservoir noise,
although an asymmetric readout can see the phase-source quadrature at
linear order in distance. The finite-basis unfitted test in
`2026-10-10-gpt-b-soliton-raman/short_distance.json` gives residual
powers 4.0018 and 4.9953 for the smallest distance doubling. It records
the full quartet and binary search at every scored distance as well.

This filtered-readout penalty is not an absolute lower floor for every
quadrature. In the frozen model, the neutral observable $a-\theta/\zeta$
has its input-amplitude shear cancelled. It gives the explicit upper bound

$$\lambda_{\min}(V_{\rm fr})\le
\frac{c_\theta+4\rho_T c_{q\theta}\zeta}
{2\zeta^2+c_\theta},\qquad
c_\theta=\frac23+\frac{\pi^2}{18},\quad
c_{q\theta}=\frac23+\frac{\pi^2}{45}.$$

Its long-distance scaling is $O(\rho_T/\zeta)$, in this frozen model.
An external phase reference is required for this observable. The physical
GNLSE also needs the small-drift and linearization restrictions; this is
not a claim about arbitrarily long propagation in a fixed real fibre.

### Deterministic perturbations and parity

With the solver's physical Fourier convention $\mathcal F_+(u)=\int
u(x)e^{ikx}dx$, set $s=(\omega_0T_0)^{-1}$ and
$\delta_3=\beta_3/(6|\beta_2|T_0)$. The first-order forcing on the
resting sech is

$$f_1=-i(T_R/T_0)q(q^2)'-s(q^3)'+\delta_3q'''.$$

Projecting the first term gives the standard Raman shift
$d(\Omega T_0)/d\zeta=-8T_R/(15T_0)$; in a frame following the pulse,
this is a translation of the spectral mask. Shock and third-order
dispersion also drive odd shape/timing corrections. Their neutral
projections give

$$X(\zeta)=(s+\delta_3)\zeta+
\frac{4T_R}{15T_0}\zeta^2+O(\epsilon^2),\quad
a(\zeta)=a(0)+O(\epsilon^2),\quad
\theta(\zeta)=\theta(0)+\zeta a(0)+O(\epsilon^2),$$

for an initially resting soliton. The continuum shape correction is
$u_1(\zeta)=\int_0^\zeta M_{\zeta-r} f_1\,dr$, using the same
neutral/Jost map. It cannot in general be represented by a frequency and
position shift alone. All these first-order
forcings are odd in $x$. Therefore a fixed even spectral mask has no
first-order correction to its scalar Fano factor about the even Kerr
mean and even Raman source. An isolated parity eigenvalue has the same
first-order cancellation; a parity-level crossing or a symmetry-broken
binary minimizer needs separate treatment and may give an absolute-value
linear response. The second-order coefficients and a uniform remainder
bound have not yet been derived. The batch evaluator tests the order below.
This parity statement concerns the odd first-moment forcing. The exact
delayed response also has an even correction of order
$f_R(\max\{\tau_1,\tau_2\}/T_0)^2$. It is second order in response
width at fixed $f_R$, but not uniformly second order in $T_R/T_0$ if
$f_R$ is independently taken to zero with the response width fixed.

Gaussian launches retain their soliton-radiation noise correlations;
fitting their output mean to a sech does not prepare a coherent soliton.
The coherent-sech formulas cannot be transferred to them without a
calculation of that inherited covariance.

### Gaussian launch: a computable inherited neutral covariance

For $u(x,0)=N\exp(-x^2/2)$, the imaginary Zakharov–Shabat eigenvalue
$i\eta$ of the largest soliton can be found on the half line from

$$\theta'=u-\eta\sin(2\theta),\qquad
\theta(-\infty)=0,\quad \theta(0)=\pi/4.$$

Its classical soliton amplitude is $a_s=2\eta$. Define

$$K(x)=\exp\left[-2\eta\int_x^0\cos(2\theta(r))dr\right],\quad
J=\int_{-\infty}^0K\sin(2\theta)dx,\quad
g(x)=K(-|x|)/J.$$

Differentiation of the shooting condition gives
$\delta a_s=\int g(x)\operatorname{Re}\delta u(x)dx$ and therefore

$$F_{\text{separated soliton energy}}=
\frac{\int g^2 dx}{2a_s}$$

for coherent input, at the level of linearized scattering data. This
observable is the energy of the asymptotically separated Kerr soliton,
**not** the Fano factor of a binary spectral mask. For a coherent sech
soliton $g=q$ and the expression is one. For a Gaussian it need not be.
The finite-difference derivative and exact-sech controls are in
`2026-10-10-gpt-b-soliton-gaussian`. The rest of the inherited scattering
covariance, including its correlations with radiation, remains necessary
for a Gaussian spectral-filter formula.

The same scattering eigenfunction gives the inherited carrier-frequency
gradient. On the negative half-line it is
$h(x)=-g(x)\cos(2\theta(x))$; extend it oddly. Then
$\delta v=\int h\operatorname{Im}\delta u\,dx$. Its normalization is
checked by $\int hx u\,dx=1$, the response to an imposed carrier shift.
Here $v$ multiplies $x$ in the field phase $e^{ivx}$; with the physical
$\mathcal F_+$ convention the frequency offset is $\Omega T_0=-v$.
This sign does not change the reported variances.
The amplitude/frequency covariance vanishes by parity for a real even
coherent launch. These are two neutral coordinates, not the complete
scattering covariance.

For the separate exactly solvable launch family $u=N\operatorname{sech}x$,
$N>1/2$, the largest soliton has $a_s=2N-1$ and
$\theta=\arctan e^x$. Thus

$$g=\frac{\operatorname{sech}^{a_s}x}{J_N},\quad
J_N=\frac{\sqrt\pi\,\Gamma(N)}{2\Gamma(N+1/2)},\quad
h=g\tanh x,$$
$$F_{\rm eigenvalue\ energy}=
\frac{2\Gamma(2N-1)\Gamma(N+1/2)^2}
{(2N-1)\sqrt\pi\,\Gamma(2N-1/2)\Gamma(N)^2},\quad
\|h\|^2=\frac{2a_s F_{\rm eigenvalue\ energy}}{2a_s+1}.$$

This is an input scattering-data identity in the ideal Kerr model.
Interpreting it as a separated pulse's energy noise requires actual
separation and preservation of that scattering coordinate. An unperturbed
higher-order bound soliton does not separate by itself; Raman fission does
not automatically preserve this covariance. The numerical shooting and
gamma-function checks are registered in the Gaussian run. No novelty or
binary-filter bound is claimed for this identity.

### Carrying a small launch mismatch through the soliton map

There is a controlled alternative to resetting the covariance. In soliton
coordinates let $u_\epsilon(0)=q+\epsilon d$, with $d$ real and even.
In the rotating frame put $m_s=M_s(d,0)^T=(r_s,j_s)^T$. The Kerr
generator's first derivative is the explicit multiplication operator

$$A_1(s)=\begin{pmatrix}-2qj_s&-2qr_s\\6qr_s&2qj_s\end{pmatrix},\qquad
M_1(\zeta)=\int_0^\zeta M_{\zeta-s}A_1(s)M_s\,ds.$$

Then the mean is $q+\epsilon m_\zeta+O(\epsilon^2)$ and the noise
propagator is $M_\zeta+\epsilon M_1+O(\epsilon^2)$. The output readout
must use the perturbed mean phase as well. The resulting first-order
covariance contains the inherited launch/radiation coupling that the
coherent-width substitution drops. For a Gaussian whose largest
scattering amplitude is $a_s$, the mismatch is
$d(y)=(N/a_s)\exp[-y^2/(2a_s^2)]-\operatorname{sech}y$ and
$\zeta_s=a_s^2\zeta$.

The $O(\epsilon^2)$ remainder follows from differentiating the finite
Galerkin ODE at fixed length; its coefficient can grow with length.
No continuum-uniform or one-sided remainder is asserted. In particular,
setting $\epsilon=1$ is a tested approximation, not a theorem for all
Gaussian launches. `scripts/soliton_launch_perturbation.py` evaluates the
Duhamel integral and compares it with a full nonlinear Kerr discrete
adjoint in the same basis.

### Conditional multimode limit and the missing reservoir hypothesis

The earlier claim C-20261008-claude-b-01 was read from commit
`6c16dc1a0d8ecc348351dbe56a01d28249e1b8ff`. It is **proposed and
unverified**. Its second-order law concerns a common filter and a
cross-phase-only Kerr model; it explicitly excludes both delayed Raman
response and the reservoir. It does not supply Raman coefficients for
the present problem, and this session does not audit or change its status.

A precise common limit can nevertheless be checked. Let $c_m=\sqrt{p_m}$,
$\sum p_m=1$, and take the ideal Manakov soliton $u_m=c_m q$. Assume
equal dispersion, no walk-off, and one scalar phase reservoir common to
all modes. In the frozen model the bright covariance is $V_s$ and each
dark mode remains vacuum, so in a mode-aligned quadrature ordering

$$V_M=cc^T\otimes V_s+(I-cc^T)\otimes I.$$

Consequently the field, passive and spectral-amplitude minima are
$\min(\lambda_{s,j},1)$, respectively. A common binary mask has exactly
the scalar Fano factor. For different binary masks $T_m(k)$ define
$\bar T(k)=\sum_m p_mT_m(k)$ and $b=|\widehat q|\bar T$. Then

$$F[\{T_m\}]=1+
\frac{\langle b,(V_{s,\rm amp}-I)b\rangle}
{\int |\widehat q|^2\bar T\,dk}.$$

The normalization of the Fourier measure cancels. This is precisely
the scalar fractional-transmission formula **including loss vacuum**;
one must not use the binary denominator $\|b\|^2$ for a fractional
$\bar T$. The scalar cutoff-source bound extends as $\min(B_L,1)$
in this conditional model, including mode-dependent binary filters.
This identity is a shared-limit check, not a proposed physical model of
a general GRIN reservoir. `manakov_readout.json` in the Raman run
checks it for two and three modes with independently varied masks.

The obstruction to importing the second-order law is visible directly
in the source Duhamel integral. Write the adjoint readout as
$w=w_0+\epsilon w_1+\cdots$ and reservoir covariance as
$Q=Q_0+\epsilon Q_1+\cdots$. Its linear correction contains

$$\int\!ds\,[\langle w_0,Q_1w_0\rangle
+2\langle w_1,Q_0w_0\rangle].$$

The Kerr first-order null extends to the reservoir only if the bright
source has no first-order change, the unperturbed bright/dark source
cross block vanishes, and the launch/readout normalization has the same
null property. A deterministic Manakov XPM matrix alone does not establish
these conditions: the physical Raman source has its own overlap tensor.
Its mode correlations must be projected, as in the still-unverified
C-20261008-gpt-b-01. If the conditions and dark isotropy do hold, the
second-order coefficients become material-, temperature- and
distance-dependent source contractions. Their signs and the previous
Kerr numerical coefficients cannot be reused. Deriving and verifying
those physical coefficients remains a follow-up.

### Final-hour shared-limit cross-check

After entering the final hour, the readout note and reference table on
gpt-a's branch were read at commit
`2a406511ac1f558fdbe87080dae67d00646299e5`. They are **unverified work in
progress**. The vacuum normalization, spectral-amplitude embedding and
global-phase hyperplane defining $\lambda_{\rm pass}$ agree with this
session's implementation. No binary certificate or optimization method
from that lane was imported. The tabulated passive limit allows arbitrary
mode mixing; a spectral phase followed by counting the same bins leaves
their counts unchanged and does not attain that general limit by itself.

The common uniform-phase-noise limit was checked directly on this
session's frozen soliton covariance. Removing its DC source term changes
$\lambda_{\min}$ from 0.05141644 to 0.05031684 on the declared window,
while the passive, amplitude and binary readouts remain unchanged to
roundoff. The removed amplitude-covariance entries are below
$2.5\times10^{-25}$. This is a finite-window diagnostic, not permission
to zero the physical Raman DC bin: the source used throughout the physical
runs retains it. `dc_shared_limit.json` in the Raman run records all four
readouts. Differential modal reservoirs need not have this null property.

## Assumption ledger and regimes

- The exact Kerr kernel is for one scalar, lossless focusing NLSE soliton,
  $N=1$, coherent input and linearized quadrature fluctuations. It assumes
  second-order dispersion, an instantaneous Kerr response and no gain,
  polarization coupling, higher spatial modes, loss, detector noise or GAWBS.
  The mathematical linearized model allows finite $\zeta\ge0$; a physical
  bright-pulse interpretation additionally needs its amplified fluctuations
  to remain small compared with the classical field.
- The frozen Raman model adds a longitudinally Markovian, symmetrized phonon
  reservoir, independent of the input vacuum. Its deterministic propagator
  remains $M_\zeta$. The oscillator response is fixed as temperature changes.
  Its eigenvalue bound is exact for this declared model for $T_0>0$ and
  $T\ge0$; it is not automatically a bound on a drifting physical soliton.
- The white thermal expansion is at fixed normalized length and on fixed
  regular readouts. On $|k|\le K$ its explicit small parameters are
  $K\max(\tau_1,\tau_2)/T_0$ and
  $K\hbar/(2k_BT T_0)$, both tending to zero. Taking both at most one
  quarter gives a bounded-frequency expansion domain; the omitted spectral
  tails must be controlled separately. At $T=0$ use the $|k|/T_0$ source,
  not a coth Taylor expansion.
- For deterministic first-order soliton perturbation theory use
  $\epsilon_R=T_R/T_0$, $s=(\omega_0T_0)^{-1}$ and
  $\delta_3=\beta_3/(6|\beta_2|T_0)$. The physical fundamental checks lie
  in $\zeta\le6$ and
  $\zeta\max(\epsilon_R,|s|,|\delta_3|)\le0.06$.
  The first-moment expansion of the deterministic Raman response also
  requires $\max(\tau_1,\tau_2)/T_0\ll1$; the tested fundamental points
  have this ratio at most 0.256, with $f_R=0.18$. A small $T_R/T_0$
  alone is insufficient if the response shape or fraction is varied.
  These are the tested small-drift bounds in the solver run, not a proven
  universal error constant. An even-mask scalar correction begins at
  second order. An eigenvalue needs an isolated parity branch to inherit
  that order. A global binary optimum may change branches.
- The Gaussian and notebook-anchor cases relax the fundamental coherent-sech
  assumption. Their propagated covariance is evaluated directly. The
  classical presence of one isolated scattering eigenvalue does not supply
  a fresh coherent input covariance for that soliton.
- Numerical continuum cutoffs, Fourier windows, cell widths and output bands
  are approximation parameters rather than physical assumptions. A Ritz
  minimum decreases when its readout space is enlarged; convergence is
  evidence, not a rigorous enclosure of the full operator minimum.

## Numerical evidence

The following are proposer checks, not independent verification. Every
quoted simulation number is registered in the runs named below. All
covariance eigenvalues are numerical approximations in the declared basis;
the analytic operator bound and a finite numerical Ritz value are different
objects.

### Fundamental-soliton scores

All entries in this table are dB relative to shot noise. The Kerr row uses
the common normalized window of the physical pilot; finer spectral-cell
checks are recorded separately.

| Case | $\lambda_{\min}$ | $\lambda_{\rm pass}$ | $\lambda_{\rm gen}$ | Best binary found | Run |
|---|---:|---:|---:|---:|---|
| Kerr, $\zeta=3\pi/2$ | -19.7728 | -10.8550 | -7.2639 | -6.5904 | `2026-10-10-gpt-b-soliton-kerr`, `pilot` |
| Physical Raman, $T_0=0.25$ ps, 300 K, $\zeta=3\pi/2$ | -12.8910 | -6.8178 | -6.2229 | -5.6781 | `2026-10-10-gpt-b-soliton-solver`, `pilot_finest` |
| Held out: $T_0=0.35$ ps, 77 K, $\zeta=3.7$, nonzero $\beta_3$ | -15.0510 | -7.4529 | -5.6875 | -5.2196 | `2026-10-10-gpt-b-soliton-solver`, `held_out` |
| Held out: $T_0=0.2$ ps, 150 K, $\zeta=4.25$, negative $\beta_3$ | -14.3972 | -7.2454 | -6.2227 | -5.7375 | `2026-10-10-gpt-b-soliton-solver`, `held_out_second` |
| Held out: $T_0=0.4$ ps, 225 K, $\zeta=5.1$, positive $\beta_3$ | -14.2002 | -7.1652 | -6.6820 | -5.9130 | `2026-10-10-gpt-b-soliton-solver`, `held_out_third` |

For the first four rows, the Kerr restriction and cutoff-source formula-to-best-binary gaps are
respectively 0.6735, 0.5484, 0.4711 and 0.4899 dB. The corresponding
directly propagated $\lambda_{\rm gen}$ gaps are 0.6735, 0.5448, 0.4678
and 0.4852 dB; the $\lambda_{\min}$ gaps are 13.1824, 7.2129, 9.8314
and 8.6597 dB. Formula values come from the Kerr and Raman runs, with
held-out preregistrations in `2026-10-10-gpt-b-soliton-freeze`.
The Raman formula is $B_L$, not the full frozen-oscillator eigenvalue.
For example, the full frozen eigenvalue 0.23893660 is slightly above
the finest physical pilot eigenvalue 0.23862224. This directly prevents
interpreting that approximation as a proved physical lower bound.
The [complete quartet/gap table](../runs/2026-10-10-gpt-b-soliton-solver/scored_cases.md)
also lists the Gaussian and fission checks. This is evidence that the
soliton-specific restriction is useful; it does not certify the approximate
frozen formula as a lower bound on every physical GNLSE case.

For the recorded pilot, the cutoff-source Fourier calculation, including
its binary search, took 0.827 s; the finest physical covariance calculation
took 1141.55 s. These are wall times on the shared machine, not a controlled
benchmark, and the former uses the reduced frozen model. Both timings are
registered in the Raman and solver runs. The formula avoids nonlinear
longitudinal propagation; it still requires spectral quadrature or a small
matrix exponential/eigenproblem.

The held-out prediction was committed before its physical propagation.
It predicted $F_{\rm binary}=0.30080536$, $B_{\rm fr}=0.26981747$,
and $\lambda_{\min}=0.03123566$. The propagated values are
0.30063339, 0.26993214 and 0.03125342, respectively. The binary
prediction differs by 0.00249 dB. These are a held-out check of the
approximation, not fitted coefficients or proof of a one-sided error.

The third held-out case was frozen after deriving the quadratic-coth
minorant. Its full frozen amplitude prediction is 0.21462911, versus
the physical 0.21468408; its binary prediction is 0.25689831, versus
0.25627015. Both errors pass the frozen 0.003 absolute target. The
native discrete adjoint gives 0.2562701547513 for the achieved mask,
matching the batch value. The refined formula, amplitude and field gaps
are 0.77011, 0.76898 and 8.28716 dB. The cutoff value is below the
physical amplitude eigenvalue in this held-out test, again without a
general physical-ordering theorem. The score and native mean comparison
are in the solver run's `third_heldout_score.json`.

The search exhausts all contiguous frequency intervals, then uses 64
starts (the best interval, all-pass, both signs of thresholded lowest
amplitude eigenvectors and seeded random masks), one-bit descent and
four annealing sweeps of 10,000 flips. The seed is recorded in every
summary. Tiny mean bins below the recorded threshold are excluded.
No global binary optimality is certified. The best found masks include
disconnected bands, so comparing only centered passbands would miss
some achievable squeezing.

### Temperature and pulse-width laws

For the oscillator used here, the material parameter is
$\rho_{300\,\mathrm K}=0.1148396191$; its exact first moment and all
coefficients are recorded in `2026-10-10-gpt-b-soliton-raman`.
At fixed $\zeta=3\pi/2$, the measured power for convergence of the best
binary Fano factor to its white-source limit is 2.0008 at 300 K and
2.0003 at 77 K, using the final pulse-width doubling in the frozen
sweep. At zero temperature the excess above Kerr instead has power
1.0010. The eigenvalue observables show the same respective powers.
These are asymptotic source/covariance tests, not fits used to construct
the theory.

For an isolated eigenvalue, ordinary perturbation of the explicit source
operator also predicts the **coefficient**, without fitting pulse-width
data. At positive temperature the next covariance is
$\rho_T[c_R+\hbar^2/(12k_B^2T^2)]\mathcal W_2/T_0^2$, where
$\mathcal W_2=4\int M_s\operatorname{diag}(0,q(-\partial_x^2)q)M_s^*ds$.
Its expectation in the white-limit eigenvector is the eigenvalue's next
coefficient. In the declared Fourier basis at $\zeta=3\pi/2$, the 300 K
amplitude bound is

$$\lambda_{\rm gen}=0.23828591+
\frac{4.0228038\times10^{-5}\ {\rm ps}^2}{T_0^2}+O(T_0^{-4}).$$

At zero temperature, eigenvector mixing contributes at second order even
though the source's next term is cubic in $1/T_0$. The same calculation gives

$$\lambda_{\rm gen}=0.18776376+
\frac{0.001170503\ {\rm ps}}{T_0}
-\frac{1.636564\times10^{-6}\ {\rm ps}^2}{T_0^2}
+O(T_0^{-3}).$$

`thermal_asymptote.json` in the Raman run records both full-field and
amplitude coefficients. After subtracting these unfitted predictions,
the last doubling gives residual powers 4.0005 at 300 K, 4.0064 at 77 K,
and 2.9988 at zero temperature for the amplitude eigenvalue. These are
fixed-basis isolated-eigenvalue asymptotes; they do not supply a uniform
physical GNLSE remainder. The relevant length is fixed $\zeta$, so a
physical distance that follows this limit scales as $T_0^2$.

In the white-source model, each fixed binary mask has
$F_T(\rho)=F_{T,K}+\rho B_T$, with $B_T\ge0$. The optimized value at fixed
distance is consequently nondecreasing and concave in $\rho$, and is
piecewise linear for a finite mask grid. Its slope can change when the
best filter changes. The eigenvalue bound has the same monotonicity and
concavity by its Rayleigh variational principle. This explains why a
filter-independent additive thermal penalty is not the correct floor law.

For a centered passband optimized over its edge and the first distance
minimum, direct differentiation of the explicit Jost integral gives the
useful thermal expansion

$$F_{\rm centered,opt}=0.22482+0.51498\rho_T
-0.14762\rho_T^2+O(\rho_T^3),$$
$$a_{\rm opt}=0.73468+0.21294\rho_T+O(\rho_T^2),\qquad
\zeta_{\rm opt}=4.77274-0.62237\rho_T+O(\rho_T^2).$$

The universal coefficients and their finite-quadrature precision are
recorded in that run's `edge_optimum.json`. At the oscillator's 300 K
thermal limit, the direct centered result is 0.2820166. This is an
**upper**, achievable edge-filter value for the arbitrary-binary
optimization. It is not the lower bound, not a universal material-independent
floor, and not a claimed replication of Werner–Friberg's material/noise
model. The general readout lower bound still requires the continuum
amplitude eigenvalue.

### Perturbative corrections and Gaussian counterexample

`2026-10-10-gpt-b-soliton-perturbation` tests positive and negative
shock and third-order-dispersion coefficients. For the fixed even
mask, the measured small-parameter powers are 2.0000 for shock and
2.0014 for third-order dispersion at the smallest parameter doubling.
The isolated amplitude and full-field eigenvalues have the same quadratic
onset. The mean timing shift is linear and agrees with $(s+\delta_3)\zeta$.
At the largest tested third-order coefficient the best binary branch
changes; its value should not be assigned the fixed-mask exponent.

`2026-10-10-gpt-b-soliton-gaussian` contains two preregistered tests of
substituting the classical IST soliton width into a **coherent-sech**
noise formula. For $N=1.25$, $\zeta=3$, the actual best binary value is
0.223056; for $N=1.5$, $\zeta=4$, it is 0.176372. The latter's
directly propagated quartet in dB is
$(-27.1683,-16.8162,-8.8031,-7.5357)$ in the order
$(\lambda_{\min},\lambda_{\rm pass},\lambda_{\rm gen},F_{\rm binary})$.
The frozen substitution predicts $\lambda_{\rm gen}=0.344645$, which
is **above** an achievable binary Fano factor. The independent Jost-cell
calculation confirms the coherent-sech prediction's scale; the native
solver with both time sampling and step count doubled preserves the
counterexample's achieved value to the displayed precision.

The scattering calculation gives a separated-soliton energy Fano factor
of 0.659807 for this Gaussian launch, whereas a freshly coherent sech
would give one. This identifies an inherited-noise mechanism; it does
not by itself reproduce the spectral covariance or its filtered optimum.
In the declared Gaussian width convention the second discrete soliton
appears at $N=(3/2)\sqrt{\pi/2}$; the numerical shooting and exact-sech
controls are in the Gaussian run. Thus the whole interval usually called
“N near one to two” cannot be assumed to contain only one soliton.

Classical mean fits in the same Gaussian run delimit the word “settled.”
For $N=1.25$, $\zeta=3$, the dominant-soliton core fit has relative field
error 0.0350, increasing to 0.0818 over the entire window. For $N=1.5$
the core error falls from 0.1267 at $\zeta=4$ to 0.0857 at $\zeta=8$,
while the full-window error remains about 0.215 because radiation remains.
Thus the latter is a one-discrete-soliton launch with residual radiation,
not an exactly isolated final coherent sech. The late readout quartet is
$(-27.4875,-20.6973,-13.3647,-9.3242)$ dB in 0.08-wide spectral cells.
The native late-case check with doubled time-grid and step counts gives
$F=0.1168378035$, agreeing with the batch value 0.1168378071.
The $N=1.25$, 300 K Raman case gives
$(-13.7665,-7.4986,-6.7762,-5.8580)$ dB. These direct physical scores
retain the inherited covariance; no coherent-state reset is made.

The first launch-mismatch Duhamel correction does recover a local
small-mismatch expansion. For $N=1.25$ its amplitude-eigenvalue errors at
$\epsilon=0.05,0.1,0.2$ are respectively
$-1.5881\times10^{-6},-6.3073\times10^{-6},-2.4764\times10^{-5}$,
consistent with the derived $O(\epsilon^2)$ order. At the full Gaussian
mismatch the error is $-0.000467$ in the declared basis. For $N=1.5$
the effective soliton distance is much longer: at full mismatch the
mean error reaches 0.3934 and the amplitude eigenvalue error is 0.1749.
Its spurious all-pass value 16.2673 is an immediate warning that this
truncated propagator is outside its useful regime. The small-mismatch
expansion is neither a uniformly accurate Gaussian formula nor a one-sided
bound. Both the useful local regime and the failure are retained.

### Gaussian Raman fission and the first-moment limit

The stretch test in `2026-10-10-gpt-b-soliton-gaussian` freezes an $N=2$
Gaussian, $T_0=0.125$ ps, 300 K, $\zeta=8$ and positive $\beta_3$
before propagation. The largest Kerr scattering amplitude is 2.92621.
The frozen classical first-moment prediction for the dominant carrier is
$\Omega T_0=-3.65877$, with a 20% target. The final core fit gives
$-4.78115$: the relative error, measured against the frozen prediction,
is 30.7%, so the prediction **fails** its target. The total-field spectral
moment is a different observable and is not substituted to rescue it.

For a resting sech of amplitude $a$, the full deterministic response gives
the instantaneous momentum law

$$\frac{d(\Omega T_0)}{d\zeta}=-\frac{a^3}{2}
\int\frac{dk}{2\pi}\,k f_R\operatorname{Im}H_R(ak/T_0)
\left[\frac{\pi k}{\sinh(\pi k/2)}\right]^2.$$

Its first-moment limit is $-8T_Ra^4/(15T_0)$. In this case the ratio
$\tau_2 a/T_0=0.7491$ is not small. The full-response rate is 1.34637
times the first-moment rate. Multiplying by the full distance gives
$-4.92606$, with a 2.94% relative discrepancy measured against that prediction.
This is a **post-hoc**
unfitted response diagnostic, not a passed frozen prediction: it still
omits formation distance, changing shape, shock and $\beta_3$.
`ssfs_response.json` records the calculation and its quadrature settings.
The same moment law gives an unfitted long-pulse correction,

$$\frac{d(\Omega T_0)}{d\zeta}=-\frac{8T_Ra^4}{15T_0}
\left[1+\frac{20c_Ra^2}{7T_0^2}
+O\!\left((a\max\{\tau_1,\tau_2\}/T_0)^4\right)\right].$$

Here $c_R=2(b_R^2-a_R^2)/(a_R^2+b_R^2)^2$ as in the reservoir expansion.
The factor $20/7$ is the ratio of the fourth and second spectral moments
of the sech intensity. After subtracting this coefficient, the final
pulse-width doubling gives relative-residual power 4.00035. This is a
classical instantaneous-law check, not a propagated carrier-error bound.

The directly propagated fission quartet in 0.3-wide spectral cells is
$(-15.8622,-15.5970,-11.3629,-10.5885)$ dB. The achieved binary value
is 0.08732761, with vacuum and reservoir parts 0.03640521 and 0.05092240.
Its amplitude and field gaps in that cell space are 0.7744 and 5.2737 dB.
The final soliton core has 0.0510 relative field-fit error. The physical
mask is a numerical result; the frozen fundamental bound is not applied
to this two-soliton fission launch. The independent native scalar check
gives $F=0.0873276084933$ on the same grid. Doubling the time-grid and
propagation-step counts gives $F=0.08619936$ (-10.64496 dB), so the
coarse quartet has residual physical-grid error even though its
implementation is independently reproduced. A further time-grid check
and a finer readout-cell calculation are recorded separately.

Halving the fission readout-cell width to 0.15 gives the quartet
$(-16.1338,-15.8773,-12.0578,-11.0057)$ dB on the same propagation grid.
The new achieved value is 0.07932911, with vacuum and reservoir parts
0.02652252 and 0.05280659. Its amplitude and field gaps in that space
are 1.0521 and 5.1281 dB. The change is material: the coarse-cell
eigenvalues and binary search are not converged in readout resolution.
The native solver reproduces the finer-cell mask on the search grid to
$8\times10^{-13}$ in $F$. Successive finer temporal grids give
$F=0.07882757$ (-11.03322 dB) and 0.07871674 (-11.03933 dB); their
last difference is 0.00611 dB. The final vacuum and reservoir parts are
0.02613622 and 0.05258052. These are fixed-mask checks; the finer-grid
full covariance and a continuum search certificate are not computed.

### Native checks and convergence

All Raman propagation uses the fetched symmetrized coth spectrum and
time samples no larger than 3 fs. Native and independent batch fields
agree near floating-point accuracy; native discrete adjoints reproduce
the batch's selected vacuum and bath variances separately. The pilot's
output-band enlargement from six to eight changes
$\lambda_{\min}$ by $1.12\times10^{-7}$ and
$\lambda_{\rm gen}$ by $7.3\times10^{-9}$, while preserving the best
found mask value. Time-step, source-quadrature and temporal-grid checks
are recorded in `2026-10-10-gpt-b-soliton-solver`.

The notebook anchor is a different regime: its actual soliton number
is 1.968972. With the original 50 ps window and original filter bins,
the present discrete adjoint gives $F=0.2984225$ at 4 mm steps and
0.2984084 at 2 mm steps with finer source quadrature, or -5.2519 dB
in the latter check (`2026-10-10-gpt-b-soliton-anchor`). Its vacuum
and shock-inclusive Raman terms agree with the archived fine-grid
terms in `2026-10-05-claude-interactive-raman-stochastic`.
The archive's quoted -5.322 dB total used the Raman contraction
without the shock multiplier. The initial shorter-window/resampled-filter
attempt disagreed and is retained as an inconclusive diagnostic.

The broader cell-based binary search does **not** reproduce the archived
mask as an optimum. At 80 spectral cells of width 0.3 in dimensionless
frequency, it finds $F=0.12133826$ (-9.1600 dB), transmitting about
0.79647 of the photons. The native discrete adjoint independently gives
$F_{\rm vac}=0.05372910$ and $F_R=0.06760916$ for this exact mask,
matching the batch contraction. The restricted-cell quartet is
$(-14.0439,-14.0199,-11.1915,-9.1600)$ dB. These eigenvalues are
**Ritz values in the declared cell space**, not certified whole-field
minima; the mask value is an achieved physical discrete-model readout.
The source, mask and native cross-check are in
`2026-10-10-gpt-b-soliton-anchor`. At 2 mm propagation steps, successive
temporal samples of 0.76294 fs and 0.38147 fs give -9.14675 and -9.14317 dB
for the same mask. The finest value is $F=0.12181008$, comprising
$F_{\rm vac}=0.05428095$ and $F_R=0.06752914$. The two finest values
differ by 0.00358 dB; the bath quadrature is also recorded and is not
identical between them. Doubling the window to 100 ps at the 0.76294 fs
sample gives -9.16719 dB. This also halves the frequency-bin spacing
and changes the discrete edge sampling. The common central-window mean
differs by only $3.38\times10^{-9}$ in relative norm, so a large reflected
mean is not seen; this alone does not isolate the covariance/window effect.
The observed range of the achieved fine-grid mask values is about
-9.14 to -9.17 dB. No global optimality is claimed. This
higher-order Raman-fission case is outside
the fundamental frozen-soliton bound's validity domain.

A late launch-mismatch stress test exposed cancellation in the original
incremental binary-search score when a mask became empty or nearly empty.
That failed diagnostic is retained as `launch_born_N1.5.json` in the
Gaussian run, explicitly marked `failed-search-diagnostic`; its negative
cached Fano estimate is invalid. The search now excludes empty masks,
recontracts every accepted descent step and every proposed best mask, and
uses interval sums that do not subtract large almost-equal global sums.
`2026-10-10-gpt-b-soliton-kerr/search_integrity.json` recontracts saved
achieved masks directly and compares small stress cases with exhaustive
enumeration. The previously reported saved masks pass this check, including
the new anchor mask. The corrected Gaussian stress test is recorded
separately; failed output is not erased.

## Limitations and outstanding work

The rigorous statements are within the ideal Kerr or explicitly
frozen-mean linear stochastic model. The physical GNLSE comparison is
strong numerical evidence in the tested small-drift regime. A uniform,
one-sided remainder for arbitrary physical binary filters has not been
proved, and numerical Ritz eigenvalues have not been converted into
certified continuum enclosures. No elementary closed form for the
arbitrary-binary optimum has been obtained. The proposed Gaussian
coherent-width substitution fails; a full inherited scattering covariance
is still needed. Novelty against the inaccessible primary filtering and
Raman-limit papers remains unresolved. No result is promoted.
