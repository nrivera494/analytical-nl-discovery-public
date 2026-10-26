# Independent verification of the semiclassical normal-dispersion claim

## Conclusion and scope

For claim **C-20261010-claude-b-01**, the leading law

\[
\lambda_{\min}(V)\sim\frac{\Lambda(Z)}{N^2}
\]

survives an independent numerical verification and has a rigorous **conditional finite-dimensional derivation**. The coefficient is the inverse squared largest singular value of an amplitude-to-scaled-phase map. Before gradient catastrophe that map is naturally supplied by the smooth dispersionless hydrodynamics. This verification supplies an actual proof of the matrix reduction, including the relative \(O(N^{-2})\) remainder when the hydrodynamic blocks have regular even expansions.

The title's assertion that the *same globally defined classical hydrodynamic map* applies after wave breaking is not established and is not even a complete mathematical definition. The classical shallow-water solution develops infinite derivatives. Beyond that point the quantum-pressure term cannot be discarded in the shock region. A limit of suitably rescaled **full NLSE tangent maps** could still exist; our converged postbreaking covariance computations support that possibility. They do not prove it.

The specific optimized optical coefficient law was not located in the primary literature searched here. Its ingredients—normal-dispersion squeezing, linearized pulsed-fiber quantum propagation, symplectic mode decompositions, and defocusing semiclassical hydrodynamics—are established. The small-\(Z\) coefficient is the large-\(\Phi\) limit of the weak-normal-dispersion result and must not be counted as a second independent novelty.

## 1. Definitions and canonical normalization

For \(L_D=T_0^2/\beta_2\), \(L_{NL}=1/(\gamma P_0)\), \(\tau=T/T_0\), and \(u=A/\sqrt{P_0}\), use

\[
N^2=\frac{L_D}{L_{NL}},\quad \varepsilon=N^{-1},\quad
Z=\frac{z}{\sqrt{L_DL_{NL}}},\quad \Phi=NZ.
\]

The propagation implemented independently here is

\[
i\varepsilon u_Z-\frac{\varepsilon^2}{2}u_{\tau\tau}+|u|^2u=0,
\qquad u(0,\tau)=e^{-\tau^2/2}.
\]

The mean phase is rapidly varying: \(u=\sqrt\rho\,e^{i\theta/\varepsilon}\). If \(\delta\phi\) denotes the *physical phase fluctuation in radians*, the local field perturbation is

\[
\delta u\,e^{-i\arg u}=X+iY,\quad
X=\frac{\delta\rho}{2\sqrt\rho},\quad
Y=\sqrt\rho\,\delta\phi
=\frac{\sqrt\rho\,\delta\theta}{\varepsilon}.
\]

Thus \(\widetilde Y=\varepsilon Y=\sqrt\rho\,\delta\theta\). Common photon-unit factors rescale both physical quadratures and cancel in the singular values. Physical vacuum is normalized to covariance \(I\) in \((X,Y)\), not in \((X,\widetilde Y)\). In the latter coordinates the input covariance is \(\operatorname{diag}(I,\varepsilon^2I)\). The canonical commutator is likewise multiplied by \(\varepsilon\) when only the phase quadrature is rescaled. The coordinate transformation is conformally symplectic, so the input-to-output map in the scaled coordinates still satisfies the usual matrix symplectic identity.

If \(M\) is the real tangent map in physical quadratures, coherent input gives \(V=MM^{\mathsf T}\). The lossless instantaneous-Kerr dynamics is Hamiltonian, hence \(MJM^{\mathsf T}=J\). Therefore \(VJV=J\), covariance eigenvalues occur in reciprocal pairs, and

\[
\lambda_{\min}(V)=\|M\|_2^{-2}.
\]

A unitary Fourier transform and local phase rotations are orthogonal symplectic transformations, so these eigenvalues are the same for complete temporal and spectral quadrature bases. No frequency bins or input vacuum modes were discarded in the independent NLSE calculation.

These are optimal **quadrature variances**, and only lower bounds on spectral-filter photon-counting Fano factors. Passive counting is a further readout restriction. Neither loss nor Raman reservoir noise is part of this ideal Hamiltonian calculation.

Fixed \(Z\) is a significant order-of-limits condition: as \(N\to\infty\), \(\Phi=NZ\to\infty\) while \(z/L_D=Z/N\to0\). Increasing power at a fixed physical fiber length also changes \(Z\); it is not the fixed-\(Z\) limit. The photon-number limit needed to maintain accurate bright-field linearization must also be maintained. The calculation does not establish an exact non-Gaussian quantum-state asymptotic at arbitrarily large \(N\).

## 2. Derivation of the hydrodynamic block

For a transparent sign convention conjugate the field and write its phase as \(S=-\theta\), with \(v=S_\tau\). Before breaking, neglecting quantum pressure gives

\[
\rho_Z+(\rho v)_\tau=0,\qquad
S_Z+\tfrac12v^2+\rho=0.
\]

For \(\eta=\delta\rho\), \(\psi=\delta S\), the exact linearization of this dispersionless problem is

\[
\eta_Z=-\partial_\tau(v\eta+\rho\partial_\tau\psi),\qquad
\psi_Z=-v\partial_\tau\psi-\eta.
\]

Initialize \(\eta_0=2\sqrt{\rho_0}\,X_0\), \(\psi_0=0\). Then

\[
C_ZX_0=\sqrt{\rho(Z)}\,\psi(Z).
\]

The conjugation changes only the sign of \(C_Z\), not its singular values. More generally the scaled fluctuation map has blocks \(M_h=\left(\begin{smallmatrix}A&B\\C&D\end{smallmatrix}\right)\), while its physical-quadrature version is

\[
M_\varepsilon=
\begin{pmatrix}A_\varepsilon&\varepsilon B_\varepsilon\\
C_\varepsilon/\varepsilon&D_\varepsilon\end{pmatrix}.
\]

## 3. A rigorous finite-block lemma

**Lemma.** Let \(M_\varepsilon\) be a real symplectic \(2d\)-by-\(2d\) matrix of the displayed form. Suppose \(A_\varepsilon=A_0+O(\varepsilon^2)\), \(C_\varepsilon=C_0+O(\varepsilon^2)\), \(D_\varepsilon=D_0+O(\varepsilon^2)\), and \(B_\varepsilon=O(1)\), in matrix norm. If \(s=\sigma_1(C_0)>0\), then

\[
\lambda_{\min}(M_\varepsilon M_\varepsilon^{\mathsf T})
=\frac{\varepsilon^2}{s^2}\,[1+O(\varepsilon^2)].
\]

No inverse of \(C_0\) is required. It may have a nontrivial kernel.

**Proof.** Let \(K_\varepsilon=\varepsilon M_\varepsilon\). Then

\[
K_\varepsilon K_\varepsilon^{\mathsf T}=
\begin{pmatrix}
\varepsilon^2A_0A_0^{\mathsf T}+O(\varepsilon^4)&
\varepsilon A_0C_0^{\mathsf T}+O(\varepsilon^3)\\
\varepsilon C_0A_0^{\mathsf T}+O(\varepsilon^3)&
C_0C_0^{\mathsf T}+O(\varepsilon^2)
\end{pmatrix}.
\]

The unperturbed positive eigenvalues lie entirely in the lower block. The first-order perturbation is off diagonal and has zero compression to every such eigenspace. Their eigenvalue corrections are therefore \(O(\varepsilon^2)\); equivalently this follows from the Schur complement for eigenvalues bounded away from zero. In particular \(\|K_\varepsilon\|_2^2=s^2+O(\varepsilon^2)\). Symplectic reciprocity yields \(\lambda_{\min}(V)=\varepsilon^2/\|K_\varepsilon\|_2^2\), proving the result.

For a simple top singular value and \(\varepsilon\)-independent blocks, let \(C_0C_0^{\mathsf T}w=s^2w\), \(\|w\|=1\). A sharper expansion is

\[
\lambda_{\min}(V)=\frac{\varepsilon^2}{s^2}
\left[1-\varepsilon^2\frac{b}{s^2}+O(\varepsilon^4)\right],
\]

\[
b=\|D_0^{\mathsf T}w\|^2+
\frac{\|A_0C_0^{\mathsf T}w\|^2}{s^2}\ge0.
\]

If \(C_\varepsilon=C_0+\varepsilon^2C_2+\cdots\), add \(2w^{\mathsf T}C_2C_0^{\mathsf T}w\) to \(b\). This term has no fixed sign. Thus the matrix argument does **not** prove the claim's negative correction or the empirical universal-looking bound \(0<c(Z)\le2\), where \(c=Z^2b/s^2\). Even with fixed blocks, symplectic matrices can have arbitrarily large \(b\). These are extra dynamical assertions about the Gaussian pulse, not consequences of symplecticity.

### Why this is not yet an infinite-dimensional proof

Even on a constant positive background the dispersionless amplitude/phase system has Fourier symbols

\[
A_0(k)=D_0(k)=\cos(k\sqrt\rho Z),\quad
B_0(k)=-\frac{k}{2\sqrt\rho}\sin(k\sqrt\rho Z),\quad
C_0(k)=\frac{2\sqrt\rho}{k}\sin(k\sqrt\rho Z).
\]

Consequently \(B_0\) is unbounded on \(L^2\), and the ordinary bounded-matrix lemma cannot simply be applied to the entire white-vacuum continuum. Appropriate Sobolev spaces, high-frequency control, and convergence of the relevant extremal spectrum are additional requirements. A smooth semiclassical limit for a fixed set of smooth perturbations does not supply that uniform spectral control automatically. The independent full-grid NLSE convergence tests give useful evidence, not a replacement theorem.

## 4. Small-\(Z\) coefficient

With \(p=\rho_0=e^{-\tau^2}\), expansion of the tangent hydrodynamics gives

\[
\psi=-Z\eta_0-\frac{Z^3}{6}(p\eta_0)''-
\frac{Z^3}{3}p'\eta_0'+O(Z^5).
\]

Using the evolving output factor \(\sqrt\rho\), the leading terms on a mode localized at \(\tau=O(\sqrt Z)\) are

\[
\frac{C_Z}{-2Z}=1-\tau^2+\frac{Z^2}{6}\partial_\tau^2+O(Z^2).
\]

The remainder here is an estimate on rescaled smooth localized test functions, not a uniform norm estimate on all \(L^2\). Set \(\tau=\sqrt Z\,s\). The leading spectral problem is the harmonic oscillator \(s^2-\partial_s^2/6\), with levels \((2j+1)/\sqrt6\). Hence

\[
4Z^2\Lambda(Z)=1+\frac{2}{\sqrt6}Z+O(Z^2),\qquad
4Z^2\Pi(Z)=1+\sqrt6 Z+O(Z^2).
\]

The amplitude-envelope width is \(\ell=(Z/\sqrt6)^{1/2}\); the RMS width of its squared normalized amplitude is \(\ell/\sqrt2\). The first excited mode is odd. Establishing that these local modes exhaust the top singular values requires excluding competing modes elsewhere, as in a semiclassical localization argument. This coefficient is consistent with the weak-dispersion result because \(y=\Phi z/L_D=Z^2\), and \(\Phi/\sqrt{1+\Phi^2}\to1\).

## 5. Independent numerical results

The NLSE solver uses a fourth-order Yoshida composition of exact Fourier dispersion and exact local Kerr phase flows. The exact differential and real adjoint of each subflow propagate fluctuations. There are no perturbed-mean finite differences and no Hermite truncation. Physical input covariance is \(I\); no absorbing/antialias attenuation is applied to the fluctuations. Lanczos computes the largest eigenvalues of \(MM^{\mathsf T}\); symplectic reciprocity gives the small ones without subtractive loss of precision. Dense direct diagonalization and exact hyperplane projection were additionally checked for the \(N=10\) cases.

| \(Z\) | \(N\) | \(\lambda_{\min}\) | \(N^2\lambda_{\min}\) | \(N^2\lambda_2\) |
|---:|---:|---:|---:|---:|
| 0.75 | 10 | 0.00849475491909 | 0.849475491909 | 2.10329262171 |
| 0.75 | 20 | 0.00214861598479 | 0.859446393918 | 2.16001418543 |
| 0.75 | 40 | 0.000538743360285 | 0.861989376456 | 2.17499614549 |
| 1.50 | 10 | 0.00360415762994 | 0.360415762994 | 1.38497212453 |
| 1.50 | 20 | 0.000904781621298 | 0.361912648519 | 1.41958221733 |
| 1.50 | 40 | 0.000226416782641 | 0.362266852226 | 1.43027064468 |

An independent direct dispersionless mean-plus-tangent DOP853 computation gives \(\Lambda(0.75)=0.86284166134396\), \(\Pi(0.75)=2.18007053159266\). The relative leading-law errors at \(N=10,20,40\) are approximately \(-1.54909\%,-0.393499\%,-0.098777\%\), with fitted error power **\(-1.98555\)** and effective \(c=0.8714,0.8854,0.8890\). This independently reproduces the claimed prebreaking behavior.

At \(Z=1.5\), the \(N^2\lambda_{\min}\) values approach the repository's approximately 0.3625 coefficient. They are reliable evidence for leading \(N^{-2}\) behavior at this postbreaking point. Comparing against the repository's finite-\(N=200\) value 0.3625049833 gives a fitted *error* power of about \(-1.57\) over these three points, not \(-2\); a fit to the absolute \(\lambda_{\min}\) has power \(-1.9963\). The error fit has finite-reference bias and must not be promoted to an asymptotic exponent. The \(N=40\) effective \(c\) exceeds 2, outside the card's explicitly narrower postbreaking finite-\(N\) bound.

**Convergence and quantum checks.** For \(N=20,Z=1.5\):

| Grid points | Window | Steps | \(\lambda_{\min}\) |
|---:|---:|---:|---:|
| 512 | 16 | 600 | 0.0009047816213077796 |
| 1024 | 16 | 1200 | 0.0009047816212975458 |
| 1024 | 32 | 1200 | 0.0009047816212980431 |

This checks spatial resolution, distance step, and window size to about \(1.2\times10^{-11}\) relative for the reported minimum. Representative dense symplectic defects are approximately \(2\times10^{-13}\); tangent-adjoint duality defects are \(10^{-15}\)–\(10^{-14}\), and direct Rayleigh/reciprocal-singular-value minima agree within several \(10^{-12}\) relative. The number-conservation gradient identity \(M^{\mathsf T}\bar u_{out}=\bar u_{in}\) is preserved to about \(10^{-12}\).

After breaking the amplitude block's maximum singular value grows: about 1.66, 2.22, 3.34 for \(N=10,20,40\). The finite-\(N\) amplitude-to-scaled-phase block itself is more sensitive to high-frequency cutoff than the optimum covariance eigenvalue: at \(N=20,Z=1.5\), its inverse squared top singular value changes from 0.3632691850 to 0.3632748777 on doubling grid resolution. Thus convergence of \(\lambda_{\min}\) alone does not certify every rescaled block in operator norm.

As a cross-method check of the priority weak-dispersion problem, \(\Phi=3,y=10^{-4}\) gives **0.02654003090684555** with this exact spectral tangent method, agreeing with the independent finite-difference/DOP853 result 0.02654003090656 to about \(1.1\times10^{-11}\) relative.

### Peripheral correction: Hermite basis bias

At \(Z=0.1\), complete-grid dispersionless propagation gives

\[
\Lambda=27.2339599259846,\qquad \Pi=31.9800336840980.
\]

225 and 441 grid points, and windows 16 and 32, reproduce these values at the shown precision. Projecting our **same independently computed exact tangent map** onto 80 Hermite input functions gives

\[
\Lambda_{H80}=27.2372686197941,\qquad
\Pi_{H80}=32.0326726605127,
\]

reproducing the repository's `hydro_direct.json`. The Hermite Gram defect is \(4.1\times10^{-15}\), so the discrepancy is basis truncation, not bad normalization. The effect is about 0.012% for \(\Lambda\) and 0.165% for \(\Pi\); it rapidly shrinks at larger \(Z\). Grid convergence in the repository did not test this source of error. This refines numerical coefficients and uncertainty claims; it does **not** refute the leading scaling law.

## 6. After wave breaking: the strongest surviving statement

For the exact full-NLSE blocks define

\[
M_N=\begin{pmatrix}A_N&B_N/N\\NC_N&D_N\end{pmatrix}.
\]

A sufficient condition for the leading law, weaker than bounded hydrodynamic blocks, is

\[
C_N\to C_\infty\ \text{in operator norm},\qquad
\|A_N\|/N\to0,\quad \|D_N\|/N\to0,\quad \|B_N\|/N^2\to0,
\]

with \(\|C_\infty\|>0\). Then \(M_N/N\to\left(\begin{smallmatrix}0&0\\C_\infty&0\end{smallmatrix}\right)\), and symplectic reciprocity proves

\[
N^2\lambda_{\min}(V_N)\to\|C_\infty\|^{-2}.
\]

This is a meaningful postbreaking conjecture and a useful route to a theorem. The present data do not prove its hypotheses. In particular, a smooth central squeezed mode does not by itself exclude a more strongly amplified perturbation in a dispersive shock region. Replacing the full dispersive solution by an entropy shock of the shallow-water system is not an automatic remedy: it changes the reversible Hamiltonian structure and omits the rapid oscillatory degrees of freedom.

## 7. Passive detection and parity

All tested first three squeezed modes have even, odd, even parity. The exact projected hyperplane minimum equals \(\lambda_2\) to numerical precision in the two dense \(N=10\) cases. However, parity by itself proves only that odd modes lie in the allowed hyperplane; it does not prove the even restricted sector has a higher minimum. That comparison remains an additional dynamical claim.

There is also a physical achievability qualification. The odd mode is orthogonal to an even mean field, so a passive output port selecting it has **zero coherent amplitude**. Its direct photon counts do not have the linearized bright-carrier Fano normalization. One can approach the hyperplane optimum with a small even carrier admixture, provided the detected carrier contains enough photons for linearization, or directly measure the quadrature with an external local oscillator. Thus the passive-readout quantity is naturally an infimum in the bright-field limit, not an assertion that the exactly dark odd port alone measures that Fano factor.

## 8. Literature and novelty assessment

- **Jin, Levermore and McLaughlin (1999)**, *The semiclassical limit of the defocusing NLS hierarchy*, CPAM 52, 613–654, [DOI](https://doi.org/10.1002/(SICI)1097-0312(199905)52:5%3C613::AID-CPA2%3E3.0.CO;2-L), [author PDF](https://math.nyu.edu/~dmac/docs/DWM-31.pdf). Full text: initial hydrodynamic discussion and §5.3 inspected. It establishes why the classical Euler description is restricted to smooth solutions, and develops a different multiphase characterization beyond breaking. Its detailed global theorem uses nonzero far-field data; it is cited for this structural distinction, not as a theorem for the present zero-background Gaussian covariance. It does not provide the optimized optical quantum covariance coefficient claimed here.
- **Grenier (1998)**, *Semiclassical limit of the nonlinear Schrödinger equation in small time*, Proc. AMS 126, 523–530, [DOI](https://doi.org/10.1090/S0002-9939-98-04164-1). Own publisher access failed; the result is referenced in the primary JLM text above and its abstract limits the argument to before shocks. Do not label this full-text access.
- **Doerr, Shirasaki and Khatri (1994)**, *Simulation of pulsed squeezing in optical fiber with chromatic dispersion*, JOSA B 11, 143–149, [publisher](https://opg.optica.org/josab/abstract.cfm?uri=josab-11-1-143), DOI 10.1364/JOSAB.11.000143. Primary abstract accessed. Arbitrary-pulse linearized squeezing with chromatic dispersion is prior work; the new claim must be the particular asymptotic optimization, not that framework.
- **König et al. (1998)**, *Fibre-optic photon-number squeezing in the normal group-velocity dispersion regime*, J. Modern Optics 45, 2425–2431, [publisher](https://www.tandfonline.com/doi/abs/10.1080/09500349808230495). Primary abstract accessed. Spectral-filter squeezing in normal dispersion was experimentally demonstrated.
- **Krylov, Bergman and Lai (1999)**, *Photon-number squeezing in the normal-dispersion regime*, Opt. Lett. 24, 774–776, [publisher](https://opg.optica.org/ol/abstract.cfm?uri=ol-24-11-774), DOI 10.1364/OL.24.000774. Primary abstract accessed. Normal-dispersion amplitude squeezing and dispersion dependence are prior experimental/theoretical topics.
- **Braunstein (2005; preprint 1999)**, *Squeezing as an irreducible resource*, PRA 71, 055801, [author PDF](https://www-users.york.ac.uk/~sb54/papers/b05B.pdf), DOI 10.1103/PhysRevA.71.055801. Full text: Bloch–Messiah theorem and appendix inspected. Singular-value/canonical decompositions of quantum squeezing are established mathematics, rather than the new physical result here.

Bounded searches included the exact titles and DOI identifiers, and combinations of “normal dispersion”, “squeezing”, “semiclassical”, “optimal mode”, “hydrodynamic”, and “singular values”. No source located in those searches supplied the precise Gaussian \(\Lambda(Z)/N^2\) optimized-covariance law. That is a provisional novelty assessment with explicit access limitations, not certification of priority.
