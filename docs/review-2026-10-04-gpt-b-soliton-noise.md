---
agent: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-04
task: T-20261004-claude-interactive-01
---

# Independent GPT review of the round-one soliton-noise cards

This is a problem-scope and literature review, not verification of a new claim. The Claude review branch and PR were not read. The three problem cards, shared definitions, primary papers and repository workflow were the inputs. `audited_by: [gpt]` records a completed GPT review of the narrowed scope; a second completed family review is still needed for `status: audited`. Novelty is not certified by an unsuccessful search.

## Disposition

| Card | Disposition | Reason |
|---|---|---|
| P-20261004-claude-interactive-01 | Retain candidate; narrow to the first nonzero quantum correction | The fixed-pump minority equation is a passive linear optical evolution. Capture and the zeroth-order shot-noise limit are baselines, not new squeezing results. |
| P-20261004-claude-interactive-02 | Retain candidate; narrow to departures from Manakov and polarization-jitter baselines | Vector vacuum noise and additive-noise collective-coordinate covariance already exist. Population-dependent group delay has a polarization precedent. |
| P-20261004-root-03 | Retain candidate; narrow to specified readouts and a verified mean-field family | An energy-only effective nonlinearity does not construct a finite-fraction vector soliton. Manakov squeezing already reduces to scalar squeezing for a particular optimized local oscillator. |

All remain `literature_state: partial`, `novelty_confidence: low`. None is promoted, and task -09 remains blocked in this session.

## Independent overlap calculation

Take dimensionless transverse coordinates, $s=x^2+y^2$, and unit-normalized real modes

$$\phi_{01}=\pi^{-1/2}e^{-s/2},\quad \phi_{02}=(1-s)\phi_{01},\quad
\phi_{03}=(1-2s+s^2/2)\phi_{01},\quad
\phi_{11a}=\sqrt2x\phi_{01},\quad \phi_{11b}=\sqrt2y\phi_{01}.$$

Then $S_{0101}=\int\phi_{01}^4d^2r=1/(2\pi)$ and every ratio is
$2\int_0^\infty e^{-2s}\langle P(s,\vartheta)\rangle_\vartheta ds$.
Using $\int_0^\infty s^ne^{-2s}ds=n!/2^{n+1}$ gives

| Product | Angularly averaged polynomial | Ratio to $S_{0101}$ |
|---|---|---|
| $\phi_{01}^2\phi_{02}^2$ | $(1-s)^2$ | $1/2$ |
| $\phi_{01}^2\phi_{11a}^2$ | $s$ | $1/2$ |
| $\phi_{02}^4$ | $(1-s)^4$ | $1/2$ |
| $\phi_{11a}^4$ | $3s^2/2$ | $3/4$ |
| $\phi_{11a}^2\phi_{11b}^2$ | $s^2/2$ | $1/4$ |
| $\phi_{01}^2\phi_{03}^2$ | $(1-2s+s^2/2)^2$ | $3/8$ |
| $\phi_{01}\phi_{03}\phi_{02}^2$ | $(1-2s+s^2/2)(1-s)^2$ | $1/4$ |

The sign of the last overlap uses the displayed real-mode phases. A modal phase redefinition changes the coefficient and the corresponding amplitudes together. The XPM factor of two makes $\sigma=1$ for both minorities. Equal *propagation-constant* spacing explains the stated LP03 resonance in the ideal model; a measured fiber requires the actual phase mismatch.

These are mathematical ideal-profile identities. They are not measured GIF625 overlaps. Independent symbolic integration and Fourier quadrature are registered as [2026-10-04-gpt-b-overlap-capture](../runs/2026-10-04-gpt-b-overlap-capture/summary.json); the run is explicitly not a solver propagation test.

## Independent capture derivation

For equal anomalous modal GVD, no Raman or gain, no resonant conjugate coupling, and an undepleted fixed pump, write

$$iv_\zeta+i\delta v_\tau+\tfrac12v_{\tau\tau}+\operatorname{sech}^2\tau\,v=0.$$

The substitution $v=e^{-i\delta\tau+i\delta^2\zeta/2}w$ cancels the first derivative. The self-adjoint operator $H=-\tfrac12\partial_\tau^2-\operatorname{sech}^2\tau$ has the normalized bound state $b=\operatorname{sech}\tau/\sqrt2$ with eigenvalue $-1/2$. A same-carrier launch $v(0)=\operatorname{sech}\tau$ gives $w(0)=e^{i\delta\tau}\operatorname{sech}\tau$. Therefore

$$f_b=\frac{|\langle b,w(0)\rangle|^2}{\|w(0)\|^2}
=\left[\frac12\int_{-\infty}^{\infty}\operatorname{sech}^2\tau\,e^{i\delta\tau}d\tau\right]^2
=\left[\frac{\pi\delta}{2\sinh(\pi\delta/2)}\right]^2.$$

For completeness, the integral follows from $y=e^{2\tau}$:
$2\int_0^\infty y^{i\delta/2}(1+y)^{-2}dy
=2\Gamma(1+i\delta/2)\Gamma(1-i\delta/2)
=\pi\delta/\sinh(\pi\delta/2)$.
The limit is $f_b(0)=1$, and $f_b=1-\pi^2\delta^2/12+O(\delta^4)$. There is no finite capture threshold in this linear projection problem. This is a bound-state fraction, not the fraction inside an arbitrary finite time gate at finite distance. Radiation need not have left that gate. The continuum has no reflected asymptotic wave for the ideal well, which does not mean the initially localized continuum component vanishes instantly.

If the minority-to-pump GVD ratio is $r>0$, the kinetic coefficient is $r/2$, the gauge phase is $-\delta\tau/r$, and the well index satisfies $\nu(\nu+1)=2\sigma/r$. The displayed sech projection is specific to $r=\sigma=1$. Its validity also requires the shifted spectrum to remain within the quadratic-dispersion, fixed-overlap bandwidth. With $u$ fixed and $\varepsilon v$ added, the actual minority fraction is $p=\varepsilon^2/(1+\varepsilon^2)$; $p=\varepsilon^2$ is only the leading-order identification.

## Scope corrections from the equations

1. **Passive probe noise.** With a classical pump, the minority Hamiltonian is number conserving and quadratic. It maps a coherent minority and vacuum in empty modes to a coherent output. Any fixed passive filter, with its rejected-port vacuum, still gives $F_m=1$. At fixed finite distance and finite nonzero detected fraction, a regular coupled Bogoliubov expansion instead has $F_{01}=F_{\rm scalar}+O(p)$, $F_m=1+O(p)$ and $\rho=O(\sqrt p)$. Obtaining those coefficients requires pump fluctuations, backreaction and the full linearized coupling. Filtering alone cannot squeeze a coherent passive probe. The bright-minority expansion requires $pN\gg1$; an exactly empty minority has undefined count Fano factor, so the literal fixed-$N$, $p\to0$ limit must not be taken through that approximation. In an XPM-only model each mode's total count commutes with the Hamiltonian: initially independent coherent total counts remain independent and Poissonian even beyond first order.
2. **Finite-fraction soliton family.** Substitution of $u_m=\sqrt{p_m}A\operatorname{sech}(\tau/T)e^{i\lambda_m\zeta}$ into an equal-GVD XPM system requires $(Cp)_m$ to be equal for all occupied modes. The LP01/LP02 matrix gives $(Cp)_{01}=1$ and $(Cp)_{02}=1-p_{02}/2$. Thus $\gamma_{\rm eff}=\gamma p^TCp$ is an averaged launch normalization, not an exact common-sech soliton coefficient at finite $p_{02}$. Unequal shapes and propagation constants, radiation and FWM must be solved or bounded first.
3. **Neutral coordinates and timing.** Independent phase rotations are symmetries only for combinations left unbroken by coherent coupling. Conserved modal fractions are not automatically a set of zero-eigenvalue shape directions. Nor is a bound pulse velocity determined solely by $\sum p_m\Delta\beta_{1,m}$. Modal frequency offsets contribute through dispersion. In the linear bound solution above the phase slope $-\delta$ exactly compensates the minority walk-off. Timing of the bound pulse must be distinguished from the centroid of pulse plus radiation. A prospective partition-jitter coefficient must be derived from the actual family and its dual modes, not postulated from launch powers.
4. **Readout and participation.** A covariance eigenvalue, a homodyne variance, a Stokes variance and a filtered count Fano factor are different measurements. Fix the filter, reference power and loss before optimization. $M_{\rm occ}$ does not determine the overlap tensor or modal delay vector; no universal participation-only law is supported here.

## Primary-source ledger

Access date: 2026-10-04. “Full text” below means the accessible paper was read, with the relevant sections identified. PDFs were extracted locally; key equations in Rand and Corney were also checked against rendered pages. No copyrighted paper is committed.

| Source and persistent identifier | Access | Bearing on scope |
|---|---|---|
| Steiglitz & Rand, [10.1103/PhysRevA.79.021802](https://doi.org/10.1103/PhysRevA.79.021802); [author PDF](https://www.cs.princeton.edu/~ken/photon_trapping_transfer09.pdf) | **full text**, all four pages | Eqs. (5)-(12) reduce the weak-probe problem to associated Legendre bound states; simulations set pump-probe walk-off to zero and study collision transfer. The same-carrier nonzero-walk-off capture expression was not printed there. Its elementary projection derivation is still a baseline, not an asserted new discovery. |
| Rand, Steiglitz & Prucnal, [10.1103/PhysRevA.71.053805](https://doi.org/10.1103/PhysRevA.71.053805); [author PDF](https://www.cs.princeton.edu/~ken/QuantumTheoryManakov05.pdf) | **full text**, especially III-IV, V and Appendix | Six-parameter vacuum covariance and dual modes already exist for the integrable Manakov soliton. Eq. (22) gives quadratic position/phase growth and constant amplitude/frequency/partition noise. Eqs. (33)-(39) give the scalar optimum for a restricted optimized homodyne family; arbitrary readouts need continuum contributions. Both components must remain bright. |
| Derevyanko, Prilepsky & Yakushev, [arXiv:nlin/0509024](https://arxiv.org/abs/nlin/0509024), [10.1088/0305-4470/39/6/006](https://doi.org/10.1088/0305-4470/39/6/006) | **full text**, especially II, IV, conclusion and Appendix | Vector additive-noise Langevin/Fokker-Planck theory, all coordinate variances, and a matrix covariance integral are established. Isotropic noise reduces the energy/frequency/timing sector to the scalar result; anisotropic noise gives polarization-dependent coefficients. This excludes a general claim that vector Gordon-Haus theory is missing. |
| Corney & Drummond, [arXiv:quant-ph/9912096v2](https://arxiv.org/abs/quant-ph/9912096v2) | **full text**, especially II, III A, IV-V | Separates input vacuum, balanced gain/loss noise and Raman reservoir noise. Eqs. (3.15)-(3.18), (4.1), (4.3)-(4.4) are the scalar timing/frequency baselines. The additive-noise timing has linear plus cubic terms, while input vacuum gives constant plus quadratic terms. The Raman cubic approximation neglects changing mean soliton parameters; combined gain and Raman drift can add higher powers at long distance. |
| Lantz et al., [arXiv:quant-ph/0311088](https://arxiv.org/abs/quant-ph/0311088), [10.1088/1464-4266/6/5/018](https://doi.org/10.1088/1464-4266/6/5/018) | **full text**, especially III-IV | Gives numerical quantum correlations and squeezing of vector spatial solitons with a strong XPM coefficient and symmetry-breaking instability. Its diffraction coordinate can map mathematically to retarded time; “spatial rather than temporal” alone is not a novelty distinction. The modal-overlap matrix, pump family, walk-off, Raman reservoir and actual readout must differ. |
| Sloan et al., [arXiv:2509.03482v1](https://arxiv.org/abs/2509.03482v1) | **full text**, main paper; supplementary information **not accessed** | General multimode quantum-noise propagation, programmable spatial filtering, and input-to-relative-phase noise conversion are already present. The main paper does not supply an analytical soliton-coordinate covariance or the fixed spectral/reference-readout law at issue here. |
| Mollenauer & Gordon, [10.1364/OL.19.000375](https://doi.org/10.1364/OL.19.000375) | **abstract only**, publisher and PubMed | Explicit prior mechanism: noisy polarization states couple through birefringence to timing. Exact coefficients, random-coupling assumptions and comparison to fixed spatial-mode walk-off remain unresolved; do not label the mechanism itself new. |
| Zitelli et al., [10.1109/JLT.2022.3205846](https://doi.org/10.1109/JLT.2022.3205846) | **abstract only** plus a search-indexed passage; attempted repository PDF returned 403 | Reports multimode SSFS theory and Raman-delay jitter. The accessible abstract does not establish separation of quantum reservoir, launch and modal noise. Full-text comparison is required before a novelty claim about multimode Raman jitter. |
| Haus & Lai, [10.1364/JOSAB.7.000386](https://doi.org/10.1364/JOSAB.7.000386) | **abstract only**, publisher | Scalar linearized squeezing and coordinate detection are established. For numerical coefficients use the accessible Rand/Corney derivations and independent projection, not an imagined reading of this article. |
| Gordon & Haus, [10.1364/OL.11.000665](https://doi.org/10.1364/OL.11.000665); Gordon, [10.1364/OL.11.000662](https://doi.org/10.1364/OL.11.000662) | **abstract only**, publisher | Amplifier-induced velocity random walk and deterministic Raman shift are known scalar baselines. Their original full texts were not obtained. |
| Kärtner & Boivin, [10.1103/PhysRevA.53.454](https://doi.org/10.1103/PhysRevA.53.454) | **abstract only**, APS | The chosen quantum state matters; a quantum soliton state is not automatically the same as a coherent sech launch. Linearized propagation has a finite validity range. |
| Levandovsky, Vasilyev & Kumar, [10.1364/OL.24.000043](https://doi.org/10.1364/OL.24.000043) | **abstract only**, publisher; indexed author-upload excerpts also seen, not a full-text review | Continuum-aware spectral-filter optimization is established. Do not equate a discrete-coordinate optimum with an arbitrary finite spectral filter. |
| Menyuk, [10.1364/JOSAB.5.000392](https://doi.org/10.1364/JOSAB.5.000392) | **abstract only**, publisher; UMBC author PDF link returned 404 | Polarization trapping includes compensating frequency shifts. It already warns against identifying pulse speed with bare weighted group delays. |

The inaccessible originals, the new polarization precedent, Zitelli and Sloan supplementary information are assigned to T-20261004-gpt-b-01. These access limits lower novelty confidence but do not undo the positive evidence sufficient to narrow the cards.

## Search record and remaining question

Web search queried exact titles/DOIs above and the following phrases: `weak probe trapped by soliton cross-phase modulation reflectionless sech2 potential`; `vector soliton Gordon Haus timing jitter quantum noise polarization`; `multimode soliton quantum noise timing jitter spatial modes`; `vector soliton jitter noise`; `Manakov soliton noise timing`; `multimode soliton Raman jitter quantum`; `timing jitter polarization amplifier soliton theory`; `Birefringence-mediated timing jitter`; and `Characterization of Multimode Soliton Self-Frequency Shift`. Backward references in Rand and Derevyanko were inspected for earlier Manakov perturbation/noise theory; they were not represented as separately read papers.

These searches found the vector and multimode precedents listed above. They did not locate a source giving the particular unequal-overlap GRIN-fiber, finite-walk-off, source-separated covariance and fixed-readout correction with a validated bound-pulse family. That is a search-limited remaining question, not proof of absence. T-20261004-claude-interactive-08 supplies scalar oracle checks. T-20261004-claude-interactive-02 supplies the independent finite-admixture capture test. No new multimode noise derivation or claim was started here.
