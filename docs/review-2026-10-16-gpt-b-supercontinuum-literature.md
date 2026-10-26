---
date: 2026-10-16
agent: gpt-b
model: gpt-6-astra
family: gpt
task: T-20261016-claude-interactive-05
---

# Second-family review of the supercontinuum bounds cards

This reviews the three candidate cards in PR #44. It is a literature and mathematical-premise review, not simulation verification of a claim. The original Claude reviews and merged GPT audits remain in the cards. The source ledger below distinguishes this reviewer's access from those historical access claims. A located bibliographic record verifies identity, not every statement attributed to the paper.

## Verdicts

| Card | Verdict | Closest prior work | What remains open in this search | Novelty / impact | Recommended status |
|---|---|---|---|---|---|
| P-20261016-claude-interactive-01, DW | **open, narrowed** | Castelló-Lurbe optical Hamiltonian constraints; Akhmediev–Karlsson stationary emission; Roy fission-daughter peak law; Li integrated-yield shaping; Liu gradient control | A nontrivial, continuum-certified integrated-band ceiling for a specified dispersion and launch class, with finite-length achieved yield and fair mask headroom | **3 / 3** | **candidate**, literature_state **partial** |
| P-20261016-claude-interactive-02, IR cutoff | **open, narrowed** | Bonetti photon-conserving dynamics; Gordon and corrected drift models; Petersen taper-length/loss trade-off; Rosenberg prechirp-enhanced reach | A loss-aware upper bound on complementary spectral reach or propagated peak power that closes the moment inequality, including radiation and intersoliton transfer | **3 / 3** | **candidate**, literature_state **partial** |
| P-20261016-claude-interactive-03, Raman frontier | **open, narrowed** | Standard ZS amplitude enclosure and trace bound; Fourier majorant theorem; Kormokar Raman-transfer model; Corney–Drummond covariance; adaptive SSFS shaping | A controlled efficiency–shift–final-jitter bound for a specified perturbed regime and passive launch class, with quantified transfer and covariance transport | **2 / 3** | **candidate**, literature_state **partial** |

DW novelty **3**: a useful certified anomalous-dispersion band bound would extend established Hamiltonian and convex-relaxation methods to a new, constrained observable. DW impact **3**: a tight enough bound would give specialist fibre designers a rule for deciding whether shaping is worth attempting.

IR novelty **3**: a uniform reach estimate closing a known moment inequality would be a new result with clear precedents in moment methods and adiabatic reach calculations. IR impact **3**: a loss-aware cutoff-yield rule would guide length, material and pulse-shape choices for specialist sources.

Raman novelty **2**: the proposed elementary bounds and several correction mechanisms are already established; novelty depends on an error-controlled combination rather than a new input-content theorem. Raman impact **3**: a reliable efficiency–shift–noise trade-off would be a useful specialist design rule.

These are prospective problem scores on `docs/RANKING_RUBRIC.md`, not scores for a verified result. Both families have real literature reviews, but this GPT review materially narrows the open questions and corrects premises. No Claude-family assent to these revised gaps has yet been recorded. Therefore `audited_by: [claude, gpt]` records participation while **candidate** remains the honest status. Priority is unchanged.

## Common conventions needed before a bound can be tested

1. Passive attenuation makes $\mathcal S_\phi\subset\mathcal S_{A\phi}$, but $\mathcal S_{A\phi}$ is **not** a subset of the exact-energy class $\mathcal S_E$. Replace the latter by $\mathcal S_{\le E}$, or compare fixed-throughput slices. Reamplifying an attenuated mask changes the experiment and its admissible class.
2. Normalize yields to the laser **before** the mask; record mask transmission and post-mask spectral moments separately. Distinguish coupled input, output spectral fraction, and an amplifier's output. Narrow-channel integrated energy is a legitimate objective, but is not the broad-cutoff or whole-DW-band objective.
3. For a power envelope, $|\widehat A|^2/(2\pi)$ is an **energy** spectrum. Physical photon density is $|\widehat A(\omega)|^2/(2\pi\hbar\omega)$ on positive absolute frequencies. NLSE mass is not exactly broadband photon number. Zheltikov, DOI [10.1103/PhysRevA.98.043833](https://doi.org/10.1103/PhysRevA.98.043833), **full text**, and Bonetti et al., DOI [10.1364/JOSAB.377891](https://doi.org/10.1364/JOSAB.377891), **full text**, explain why the choice matters.
4. The exact quantum-defect statement is $\eta^E_{\rm red}\le(\omega_c/\bar\omega_{\rm laser})\eta^N_{\rm red}$; replacing the laser photon mean by a carrier is a narrowband approximation. A fraction normalized to surviving photons must be multiplied by $N_{\rm out}/N_{\rm laser}$ before it is an input-normalized yield.
5. Specify a finite $L_{\max}$, the output band and its initial leakage, and how a soliton is separated from overlapping radiation. An input bandwidth does not impose an output support bound. A Gaussian has no literal compact spectral support unless truncation is specified.
6. A relative headroom requires a nonzero baseline for the same target, length/shift constraint and denominator. A small transform-limited target can make relative gain arbitrarily misleading. Initial peak optimality does not imply optimal output conversion.

## DW card: a valid relaxation, but not yet a useful certified ceiling

### Mathematical premise

Fix signs by writing $iA_z=K(i\partial_t)A-\gamma|A|^2A$, $\gamma>0$. In the common propagation convention $A_z=i\beta(i\partial_t)A+i\gamma|A|^2A$, this means $K=-\beta$. Set $n=|\widehat A|^2/(2\pi)$, $M=\int n$, $P=\int\Omega n$, $M_2=\int\Omega^2n$, and $M_K=\int Kn$. For sufficiently regular decaying solutions, $H=M_K-\gamma\int|A|^4/2$ is conserved. These are mass/energy-envelope invariants, not the physical photon invariants of an arbitrary broadband GNLSE.

The sharp one-dimensional inequality, after removing mean frequency, is

$$\int|A|^4dt\le {M^{3/2}\over\sqrt3}\sqrt{M_2-P^2/M}.$$

Weinstein, DOI [10.1007/BF01208265](https://doi.org/10.1007/BF01208265), **full text**, §§I–III, is the sharp-interpolation reference; the sech normalization is checked independently in run `2026-10-16-gpt-b-sclit-premises`. The resulting necessary constraints include **both**

$$H\le M_K,\qquad M_K-{\gamma M^{3/2}\over2\sqrt3}\sqrt{M_2-P^2/M}\le H.$$

The second constraint is convex in $n$ at fixed $M,P$, and maximizing band mass is a convex optimization problem in the usual sense of a linear objective over a convex feasible set. Dropping the first constraint still gives an outer relaxation, but can destroy useful information. Neither constraint implies that an arbitrary feasible spectrum is dynamically reachable.

For example, take $K(\Omega)=\Omega^2/2+\Omega^3/6$, $M=1$, $P=H=0$ and $n=(1-\epsilon)\delta_1+\epsilon\delta_{-(1-\epsilon)/\epsilon}$. As $\epsilon\downarrow0$, the objective mass near $+1$ approaches all the mass while $M_K\to-\infty$. The sketch's sole Hamiltonian inequality is satisfied for small $\epsilon$; $H\le M_K$ excludes this sequence. Run `2026-10-16-gpt-b-sclit-premises` checks finite examples. These are counterexamples to nontriviality of the **relaxation**, not proposed physical output spectra. Adding the omitted inequality alone does not establish compactness for every sign-changing dispersion.

If a global coercive lower bound $K\ge a\Omega^2-b$ with $a>0$ is available, the GN inequality gives a quadratic bound in $\sqrt{M_2}$; this is a familiar route to moment control. A cubic Taylor dispersion on the entire real line has no such lower bound. A physical dispersion, validity interval and certified tail budget must replace an implicit unlimited Taylor extrapolation.

A finite-grid primal maximum is generally **below** the continuum relaxation maximum, so it is not automatically a rigorous ceiling. A continuous dual inequality or interval/tail enclosure is needed. At fixed input spectral magnitude, the transform-limited pulse minimizes $H$ in the convention above. With only the sketch's lower inequality, increasing $H$ enlarges the feasible set: the TL case gives the smallest relaxed ceiling, not an automatic ceiling for all phases. With both inequalities, feasible sets need not be nested. Optimize or enclose the whole attainable Hamiltonian range.

### Closest prior work and corrections

Optical Hamiltonian constraints predate this card: Castelló-Lurbe et al., DOIs [10.1364/OE.21.028550](https://doi.org/10.1364/OE.21.028550), **abstract only**, and [10.1364/OE.24.026629](https://doi.org/10.1364/OE.24.026629), **full text**, connect dispersion, nonlinear length and spectral evolution. They are strong precedents, not a located solution of the proposed arbitrary-dispersion, passive-mask DW ceiling. The older GPT audit's full-text access to the former is preserved separately.

Akhmediev–Karlsson, DOI [10.1103/PhysRevA.51.2602](https://doi.org/10.1103/PhysRevA.51.2602), **full text**, derive exponentially small stationary-soliton radiation and recoil. Roy et al., DOI [10.1103/PhysRevA.79.023824](https://doi.org/10.1103/PhysRevA.79.023824), **full text**, Eq. 6 concerns spectral **peak** power of a fission daughter. With this card's $\delta_3=\beta_3/(6|\beta_2|T_0)$, the daughter's parameter is $(2N-1)\delta_3$, without another division by six. A note corrects that normalization in the preserved Merged cards section.

Li et al., DOI [10.1016/j.rinp.2020.103518](https://doi.org/10.1016/j.rinp.2020.103518), **full text**, already optimize quadratic/cubic spectral phase and report an integrated DW-energy objective. However, their model rescales peak power to preserve soliton order across shaped inputs, so the comparisons are not the card's passive fixed-laser-energy experiment. Li et al., DOI [10.1002/andp.202200601](https://doi.org/10.1002/andp.202200601), **abstract only**, also treat sinusoidal spectral phase and enhanced conversion.

Liu et al., DOI [10.34133/ultrafastscience.0107](https://doi.org/10.34133/ultrafastscience.0107), arXiv:[2411.14410](https://arxiv.org/abs/2411.14410), **full text**, use a differentiable physical convolutional model and experimental gradient descent for DW conversion, frequency and bandwidth. Their shaper is followed by an amplifier; Eq. 5 normalizes integrated DW output to DW-plus-soliton energy in the measured spectral window. This directly supersedes “no gradient optimization found,” while leaving the upstream-normalized passive-mask ceiling open. Lefevre et al., DOI [10.1364/OE.22.019423](https://doi.org/10.1364/OE.22.019423), **full text**, supply an earlier nonlinear coupled-mode adjoint precedent, including Raman conversion in silicon.

Petty's thesis, DOI [10.17630/sta/690](https://doi.org/10.17630/sta/690), **full text**, chapter 4, supports chirp-dependent broad visible conversion and calibrated power measurements. It does **not** establish the card's asserted matched-TL headroom ratio: the quoted starting record, chirp examples and normalization are not a common zero-GDD baseline. Output spectral fractions and coupling-inclusive efficiency must be separated. The record range copied from the thesis table cannot substitute for checking its original sources; their identities and remaining denominator checks are listed below.

**Narrowed gap:** a useful, continuum-certified outer bound for a stated physical dispersion and output band, together with an integrated finite-length yield approximation and optimization gap at fixed upstream laser spectrum/energy. Neither the broad “first Hamiltonian ceiling” claim nor “first gradient-controlled DW yield” survives this search. Exponential stationary emission and higher-order-soliton peak laws are prior work; a transient integrated-yield law needs its own specific novelty test.

## IR card: the moment algebra is correct; dynamical closure is missing

### Moment and Raman premises

For a lossless photon distribution, let the blue band's conditional mean be at least $\Omega_b>0$, its fraction be $\eta_b$, the complement mean be $-R$, and the total mean be $-D$. Then

$$-D\ge\eta_b\Omega_b-(1-\eta_b)R,\qquad \eta_b\le {R-D\over\Omega_b+R}.$$

This is an elementary conditional-mean inequality. It becomes predictive only with an independent $R\le R_{\max}$ and appropriate $R\ge D$. The two-atom saturation check is in run `2026-10-16-gpt-b-sclit-premises`. The red mirror likewise requires a genuine upper support bound $\omega_{\max}$, yielding $(\omega_{\max}-\bar\omega)/(\omega_{\max}-\omega_c)$, capped at one, for surviving-photon normalization. An imposed numerical window is not that support proof.

For constant $\gamma$ and the shock form

$$A_z=iD A+i\gamma A S-\gamma\partial_t(A S)/\omega_0,\qquad S=(1-f_R)|A|^2+f_R h_R*|A|^2,$$

use $\widehat f(\Omega)=\int f(t)e^{i\Omega t}dt$. With no loss, a real dispersive multiplier, positive absolute frequencies and suitable decay,

$$E'=-{\gamma f_R\over2\pi\omega_0}\int\Omega\operatorname{Im}\widehat h_R(\Omega)|\widehat I(\Omega)|^2d\Omega\le0,$$

provided **passivity**, $\Omega\operatorname{Im}\widehat h_R\ge0$, holds. Causality alone does not imply this sign. The shock factor cancels the photon weighting in $N'$, giving $N'=0$ and $\bar\omega'=E'/(\hbar N)\le0$. The corresponding peak bound is

$$|\bar\omega'|\le\gamma f_R{\bar\omega\over\omega_0}P_{\rm pk}\sup_\Omega\{\Omega\operatorname{Im}\widehat h_R(\Omega)\}.$$

The card omits $\bar\omega/\omega_0$ for a power envelope; replacing it by one needs a narrowband approximation. Run `2026-10-16-gpt-b-sclit-premises` verifies the instantaneous RHS identity, photon cancellation and bound on refined Fourier grids. It does not establish a propagation bound on $P_{\rm pk}$.

Bonetti et al., DOI [10.1364/JOSAB.377891](https://doi.org/10.1364/JOSAB.377891), **full text**, Eqs. 4–14, show that the conventional form is photon-conserving for the special linear nonlinear-dispersion factor $\gamma_0(1+\Omega/\omega_0)$. A general $\gamma(\omega)$ needs their symmetric weighted interaction; inserting an arbitrary multiplier is insufficient. Thus “the standard GNLSE always violates photon number” is too broad. Linale et al., DOI [10.1109/JQE.2020.3047691](https://doi.org/10.1109/JQE.2020.3047691), **abstract only**, is a journal article in 2021 with online DOI registration/publication in 2020.

Huang et al., arXiv:[2607.05244](https://arxiv.org/abs/2607.05244), **full text**, Eqs. 17–21, must be read with its definition of centroid. Its power-weighted frequency equation contains a chirp-dependent term; that centroid is not $E/(\hbar N)$. Do not cite its abstract as a proof of monotonicity for every centroid and every lossy GNLSE.

With frequency-dependent attenuation, the surviving photon mean instead obeys

$$\bar\omega'=-Q_R/(\hbar N)-\operatorname{Cov}_N(\omega,\alpha),$$

where $Q_R\ge0$ in the passive model. Preferential removal of red photons can raise the surviving mean. The run includes an explicit two-frequency example. A usable output budget must include lost photon number and moment.

### Reach, loss and shaping

For an isolated adiabatic sech soliton, write $E_s=2P_sT_s$ and $P_sT_s^2=|\beta_2|/\gamma$. Substitution into Gordon's short-response law gives

$$\omega_s'=-{T_R\gamma^4E_s^4\over30|\beta_2|^3}=-{T_R\gamma^4(\hbar\omega_sN_s)^4\over30|\beta_2|^3}.$$

The coefficient in the sketch is correct within this approximation. Gordon, DOI [10.1364/OL.11.000662](https://doi.org/10.1364/OL.11.000662), **abstract only**, is the original rate-law source; the algebra here is independent. It is not a global reach upper bound after fission. Kormokar et al., DOI [10.1364/JOSAB.409240](https://doi.org/10.1364/JOSAB.409240), **full text**, give a corrected adiabatic model including loss, shock and dispersion slope, with limitations when radiation matters. Gorbach–Skryabin, DOI [10.1103/PhysRevA.76.053803](https://doi.org/10.1103/PhysRevA.76.053803), arXiv:[0707.1598](https://arxiv.org/abs/0707.1598), **full text**, §VI, show trapped-light backaction. Kormokar et al., DOI [10.1364/JOSAB.478975](https://doi.org/10.1364/JOSAB.478975), arXiv:[2301.02945](https://arxiv.org/abs/2301.02945), **full text**, model energy transfer between solitons. Both defeat an unqualified input-IST reach cap.

Petersen et al., DOI [10.1364/OE.25.015336](https://doi.org/10.1364/OE.25.015336), **full text**, already optimize the pre-taper length in chalcogenide supercontinuum against spectral extension and long-wavelength loss. Pant et al., DOI [10.1364/JOSAB.27.001894](https://doi.org/10.1364/JOSAB.27.001894), **abstract only**, and Zheltikov, DOI [10.1103/PhysRevE.75.037603](https://doi.org/10.1103/PhysRevE.75.037603), **abstract only**, are close reach-model precedents. A loss edge alone does not prove a unique interior optimum: the cutoff might never be reached, or the supremum might occur at a length boundary.

Rosenberg et al., DOI [10.1364/OE.383014](https://doi.org/10.1364/OE.383014), **abstract only** for the primary-source verification in this session, experimentally find negative prechirp that increases few-cycle Raman-soliton reach across an absorption band. This is a particularly close missed counterexample to the qualitative claim “shaping cannot raise reach.” It does not refute the mathematical bound on **input** ZS eigenvalues.

Arteaga-Sierra et al., DOI [10.31349/RevMexFis.63.2.111](https://doi.org/10.31349/RevMexFis.63.2.111), **full text**, already use a genetic algorithm to maximize integrated Raman-channel output by varying carrier wavelength, peak power and duration. Their Eqs. 2–3 distinguish the channel-energy fitness from the output-normalized conversion fraction. This is direct prior work on Raman conversion optimization, but changes the laser spectrum and energy rather than optimizing a passive mask at fixed upstream input. The reported search is not a certified global bound.

The original Gauthier, Kulkarni and Martinez records mostly report fractions of **output** power, not input-to-red conversion. Gauthier's active source architecture also differs from a passive fibre launch; see DOI [10.1038/s41598-022-19658-8](https://doi.org/10.1038/s41598-022-19658-8), **full text**, and the other record entries in the ledger. These demonstrations show relevance, not a common ceiling.

**Narrowed gap:** a rigorous or controlled asymptotic loss-aware bound on red reach/propagated peak power for a bounded launch and fibre class, including or quantitatively excluding trapped radiation, intersoliton Raman transfer and red DWs. Use it to bound upstream-normalized broad-cutoff yield and finite-length shaping headroom. Mere moment balance, adiabatic drift, numerical cutback optimization and the existence of chirp gains are already known.

## Raman card: the input bounds are standard; the propagated frontier is not closed

### ZS amplitude bound and passive-mask extremality

For the card's decaying-line ZS system and an $L^2$ eigenfunction with vanishing boundary term,

$$\operatorname{Im}\zeta\int(|\psi_1|^2+|\psi_2|^2)=-2\operatorname{Re}\int q\bar\psi_1\psi_2.$$

Cauchy–Schwarz pointwise gives $|\operatorname{Im}\zeta|\le\|q\|_\infty$. The sketch is correct for bounded decaying potentials and discrete eigenstates. It is an elementary numerical-range enclosure, not a new spectral principle. Biondini–Oregero–Tovbis, DOI [10.4171/JST/432](https://doi.org/10.4171/JST/432), arXiv:[2010.04263](https://arxiv.org/abs/2010.04263), **full text**, Lemma 3.8 and §6.1, explicitly publish the same amplitude strip and integration argument for periodic/Floquet and Dirichlet spectra. Their setting is not the decaying line; the displayed calculation supplies that extension directly. This search did not establish the earliest publication of the exact general complex decaying-line formulation.

Klaus–Shaw, DOI [10.1103/PhysRevE.65.036607](https://doi.org/10.1103/PhysRevE.65.036607), **full text**, treat real single-lobe potentials and imaginary spectrum; DOI [10.1137/S0036141002403067](https://doi.org/10.1137/S0036141002403067), **abstract only**, gives the sharp area threshold and counting results. The count needs care exactly at threshold: count positive-imaginary eigenvalues, not a zero spectral resonance. These are stronger specialized results, not a theorem that all complex multi-lobe masked pulses have imaginary eigenvalues.

DiFranco–Miller, arXiv:[nlin/0702028](https://arxiv.org/abs/nlin/0702028), **full text**, Theorem 1 and the end of §3, connect modified-NLS enclosures to the semiclassical ZS shadow bound of Deift–Venakides–Zhou. Their cited original notes are unpublished; no DOI is invented here. Bronski, DOI [10.1016/0167-2789(95)00311-8](https://doi.org/10.1016/0167-2789(95)00311-8), **abstract only**, is a located semiclassical ZS reference. Self-adjoint Schrödinger Lieb–Thirring inequalities cannot simply be applied to this non-self-adjoint complex ZS operator. The positive mass trace formula already supplies the safe aggregate bound $4\sum_k\operatorname{Im}\zeta_k\le M$ under the standard focusing-scattering assumptions.

For $\widehat q=mQ$ with $|m|\le1$,

$$\|q\|_\infty\le{1\over2\pi}\int|Q|=\|q_{\rm TL}\|_\infty,$$

$$\int|q|^4={1\over(2\pi)^3}\|mQ*mQ\|_2^2\le{1\over(2\pi)^3}\||Q|*|Q|\|_2^2.$$

Both extremality statements are correct. Lenzmann–Sok, arXiv:[1805.06294](https://arxiv.org/abs/1805.06294), **full text**, Lemma 5.1 states the Fourier majorant property for even powers and infinity; Lemma 5.2 gives affine-phase equality conditions under regular connected-support assumptions. Use these lemmas, not their stronger Fourier rearrangement theorem, which also changes spectral magnitude. Random-mask checks in run `2026-10-16-gpt-b-sclit-premises` support implementation only; they do not prove extremality of a ZS eigenvalue or of propagated yield.

Combining peak and trace bounds improves the sketch to

$$4\operatorname{Im}\zeta_1\le\min(M,4\|q_{\rm TL}\|_\infty).$$

For $q_{\rm TL}=N\,\mathrm{sech}\,t$, $M=2N^2$ and $N>1/2$, the largest TL discrete mass is $4(N-1/2)$. Consequently

$$H_{\rm input\,IST}\le\min\left\{{N^2\over2N-1},{2N\over2N-1}\right\}.$$

At the fundamental sech launch, the trace constraint removes the sketch's apparent amplitude/rate headroom. Satsuma–Yajima, DOI [10.1143/PTPS.55.284](https://doi.org/10.1143/PTPS.55.284), **abstract only** here, and Chekhovskoy et al., arXiv:[2003.02215](https://arxiv.org/abs/2003.02215), **full text**, supply exact-profile anchors. Reflectionlessness of $N\,\mathrm{sech}$ requires integer $N$; the positive discrete eigenvalues exist more generally. The temporally chirped sech and Gaussian families change Fourier magnitude, so their chirp results are not a proof of an optimum over a fixed laser spectrum. Integrable bound states breathe; fission itself requires a perturbation.

### What is already known about propagation and noise

Kormokar et al., DOI [10.1364/JOSAB.478975](https://doi.org/10.1364/JOSAB.478975), arXiv:[2301.02945](https://arxiv.org/abs/2301.02945), **full text**, go beyond identifying an escape mechanism: Eq. 24 is an analytic model of the leading-soliton conversion correction, depending on pulse parameters, length and Raman spectral overlap. Eq. 25 contains an empirically adjusted factor. Thus “find a dependence on $N,T_0,L$ and response” is partly solved. A uniform one-sided bound or error-controlled model, including shaped launches and radiation, is not supplied by that fit. Driben et al., DOI [10.1103/PhysRevA.87.063808](https://doi.org/10.1103/PhysRevA.87.063808), arXiv:[1305.5911](https://arxiv.org/abs/1305.5911), **full text**, is another prior mechanism for changing the fission partition.

Adaptive SSFS control is quantitative prior work: Efimov et al., DOI [10.1364/OL.29.000271](https://doi.org/10.1364/OL.29.000271), **abstract only**; Hu et al., DOI [10.1103/PhysRevLett.114.073901](https://doi.org/10.1103/PhysRevLett.114.073901), **full text**; and Rosenberg et al., DOI [10.1364/OE.383014](https://doi.org/10.1364/OE.383014), **abstract only**, address distinct phase-control regimes. Hary and Wetzel in the ledger further establish adaptive channel enhancement. A universal claim that TL gives the greatest propagated red shift is untenable; none of these sources is a certified general passive-mask frontier.

Drummond–Corney, DOI [10.1364/JOSAB.18.000139](https://doi.org/10.1364/JOSAB.18.000139), arXiv:[quant-ph/9912095](https://arxiv.org/abs/quant-ph/9912095), **full text**, and Corney–Drummond, DOI [10.1364/JOSAB.18.000153](https://doi.org/10.1364/JOSAB.18.000153), arXiv:[quant-ph/9912096](https://arxiv.org/abs/quant-ph/9912096), **full text**, already connect Raman reservoir noise and soliton covariance. The latter's analytic instantaneous-response approximation neglects deterministic SSFS; its numerical treatment need not. Local diffusion divided by local drift is not a lower bound on final variance without the response/transport matrix. Zhou et al., DOI [10.1364/OL.40.005105](https://doi.org/10.1364/OL.40.005105), **abstract only** at primary-source verification, also show experimentally how input intensity noise becomes Raman wavelength and timing jitter. Technical input noise, intrinsic quantum noise, frequency-centroid variance and timing variance must be named separately.

**Narrowed gap:** a specified perturbed regime in which the input trace/peak bounds, transfer corrections, wavelength-dependent drift and covariance transport yield a controlled outer frontier for final efficiency, shift and jitter. Quantify the error and optimize the same passive launch class against the same TL baseline. Merely restating the amplitude enclosure, Fourier majorant theorem, Gordon law or fitted Raman-transfer correction is not enough.

## Source ledger and search log

The ledger below is part of this report; historical full-text labels are not silently inherited. `not accessed` means the source was located but only its bibliographic identity was checked in this session. `full text` may mean the named relevant sections were read, not every page. Searches and unresolved access are recorded below.

### DW, mathematical bounds and shared shaping sources

| Source | DOI or arXiv identifier | Access in this review | Verification / limitation |
|---|---|---|---|
| Akhmediev & Karlsson (1995) | [10.1103/PhysRevA.51.2602](https://doi.org/10.1103/PhysRevA.51.2602) | full text | Chalmers author copy, all pages visually inspected; Eqs. 13, 17 and recoil section. Stationary soliton, not an integrated fission yield. |
| Skryabin & Gorbach (2010) | [10.1103/RevModPhys.82.1287](https://doi.org/10.1103/RevModPhys.82.1287); arXiv:1005.2777 | full text | Cherenkov, trapping and Raman sections. Exponential overlaps and sign-dependent Raman detuning; do not reuse an undefined exponential-width parameter. |
| Roy, Bhadra & Agrawal (2009), PRA | [10.1103/PhysRevA.79.023824](https://doi.org/10.1103/PhysRevA.79.023824) | full text | Rochester author copy via indexed text; Eq. 6 is peak spectral power. Daughter TOD normalization corrected above. |
| Roy et al. (2009), Opt. Commun. | [10.1016/j.optcom.2009.06.018](https://doi.org/10.1016/j.optcom.2009.06.018) | abstract only | Fourth-order-dispersion paper located; original sideband-power denominator not independently checked beyond abstract/first page. |
| Austin et al. (2006) | [10.1364/OE.14.011997](https://doi.org/10.1364/OE.14.011997) | abstract only | Compression-window emission and recoil explicitly supported; full transient formula remains to inspect. |
| Modotto et al. (2015) | [10.1364/JOSAB.32.001676](https://doi.org/10.1364/JOSAB.32.001676) | abstract only | Radiation efficiency in dual-concentric-core fibre; earlier gpt-a full-text assessment preserved, not claimed as this reviewer's access. |
| Webb et al. (2014) | [10.1364/OL.39.005850](https://doi.org/10.1364/OL.39.005850); arXiv:1607.04945 | full text | Dual-frequency beat signal, effective soliton order and cascaded mixing. Later arXiv deposit is valid; not a general mask ceiling. |
| Erkintalo, Genty & Dudley (2010) | [10.1364/OL.35.000658](https://doi.org/10.1364/OL.35.000658) | abstract only | Collision enhancement explicitly concerns peak power, not integrated conversion. |
| Travers et al. (2019) | [10.1038/s41566-019-0416-4](https://doi.org/10.1038/s41566-019-0416-4); arXiv:1811.05877 | full text | Scaling and experimental conversion sections. A useful operating range is not a universal soliton-order cap or efficiency theorem. |
| Brahms et al. (2019) | [arXiv:1903.12103](https://arxiv.org/abs/1903.12103) | full text | Compact hollow-capillary UV source; experimental efficiency depends on wavelength and source conditions. |
| Brahms & Travers (2021) | [arXiv:2101.04014](https://arxiv.org/abs/2101.04014) | full text | Saturation and energy/timing noise results; no universal yield ceiling. |
| Chang, Chen & Kärtner (2010) | [10.1364/OL.35.002361](https://doi.org/10.1364/OL.35.002361) | abstract only | Efficient broadband visible conversion record located; full denominator/control comparison not independently audited. |
| Petty (2024), thesis | [10.17630/sta/690](https://doi.org/10.17630/sta/690) | full text | St Andrews thesis, chapter 4 and calibration discussion; valid DataCite DOI. Supports chirp dependence, not the claimed matched-TL gain ratio. |
| Tartara, Cristiani & Degiorgio (2003), Petty table original | [10.1007/s00340-003-1172-0](https://doi.org/10.1007/s00340-003-1172-0) | abstract only | Primary publisher abstract identifies blue conversion relative to input; full mechanism and denominator audit remains open. |
| Hu, Wang, Chai & Zheltikov (2004), Petty table original | [10.1364/OPEX.12.001932](https://doi.org/10.1364/OPEX.12.001932) | abstract only | Primary abstract verifies birefringence-assisted frequency conversion; thesis bibliography has extraneous author strings, so use the publisher identity. Table efficiency not independently checked in full text. |
| Lu, Deng & Knox (2005), Petty table original | [10.1364/OL.30.001566](https://doi.org/10.1364/OL.30.001566) | abstract only | Primary abstract explicitly uses total input for conversion in short dispersion-micromanaged fibre. |
| Lei et al. (2013), Petty table original | [10.1088/2040-8978/15/7/075201](https://doi.org/10.1088/2040-8978/15/7/075201) | abstract only | Publisher first-page preview: visible/mid-IR generation with two ZDWs. Detailed table record not independently checked. |
| Xin et al. (2013), Petty table original | [10.1007/s00340-012-5329-6](https://doi.org/10.1007/s00340-012-5329-6) | abstract only | Primary publisher abstract supports high conversion in GeO2-doped two-ZDW fibre; full normalization remains to inspect. |
| Chan et al. (2014), Petty table original | [10.1364/OE.22.009498](https://doi.org/10.1364/OE.22.009498) | abstract only | Primary abstract supports the efficient visible source. Accessible manuscript excerpts leave the pump denominator ambiguous; do not silently equate it to coupled input. |
| Manili et al. (2012), Petty table original | [10.1364/OL.37.004101](https://doi.org/10.1364/OL.37.004101) | abstract only | Primary abstract supports efficient broadband infrared conversion with subnanosecond pumping; different regime from femtosecond soliton emission. |
| Cheng et al. (2015), tellurite entry in Petty | [10.1109/JPHOT.2014.2381662](https://doi.org/10.1109/JPHOT.2014.2381662) | abstract only | Located original corresponding to the high record in the thesis; full integrated-band definition and input denominator unresolved. Other entries have been identified below; full denominator harmonization remains unfinished. |
| Grassani et al. (2019) | [10.1038/s41467-019-09590-3](https://doi.org/10.1038/s41467-019-09590-3) | abstract only | Photonic-chip conversion, not silica fibre; journal and preprint record values differ by version, not a nonexistent citation. |
| Chen et al. (2020) | [10.1364/OE.393959](https://doi.org/10.1364/OE.393959) | abstract only | Photoionization-assisted gas-fibre conversion. Output spectral fraction differs from overall conversion; plasma is outside Kerr-only theory. |
| Lei et al. (2009) | [10.1088/0256-307X/26/6/064213](https://doi.org/10.1088/0256-307X/26/6/064213) | abstract only | Chirp-dependent DW generation located. The assertion that both signs always lower yield is not verified from the accessible abstract. |
| Li et al. (2020) | [10.1016/j.rinp.2020.103518](https://doi.org/10.1016/j.rinp.2020.103518) | full text | Model and results: integrated DW energy, quadratic/cubic spectral phase; peak normalization changes energy across masks. |
| Li et al. (2023) | [10.1002/andp.202200601](https://doi.org/10.1002/andp.202200601) | abstract only | Sinusoidal-phase conversion enhancement; no rigorous mask optimum inferred. |
| Liu et al. (2025) | [10.34133/ultrafastscience.0107](https://doi.org/10.34133/ultrafastscience.0107); arXiv:2411.14410 | full text | Gradient descent, shaper–amplifier–HNLF pipeline and measured-window efficiency Eq. 5. Direct correction to the negative gradient-search statement. |
| Hary et al. (2023) | [10.1364/OL.492064](https://doi.org/10.1364/OL.492064); arXiv:2304.00829 | full text | Fitness integrates channel intensity; a control gene changes coupling/throughput. More than phase alone at equal coupled energy. |
| Hary et al. (2025) | [10.1038/s41598-024-84567-x](https://doi.org/10.1038/s41598-024-84567-x) | full text | Optimizer comparison, channel-integrated enhancement and injected-power control. Narrow-channel energy is not merely a peak-density observable. |
| Wetzel et al. (2018) | [10.1038/s41467-018-07141-w](https://doi.org/10.1038/s41467-018-07141-w) | full text | Programmable pulse splitting and amplification, comparison to a best single pulse; different input spectrum/class from fixed-magnitude phase masks. |
| Efimov et al. (2004) | [10.1364/OL.29.000271](https://doi.org/10.1364/OL.29.000271) | abstract only | Adaptive femtosecond SSFS control exists; full masks, throughput and quantitative baseline remain to inspect. |
| Castelló-Lurbe, Andrés & Silvestre (2013) | [10.1364/OE.21.028550](https://doi.org/10.1364/OE.21.028550) | abstract only | Optical wave-breaking/Hamiltonian precedent; original full text inaccessible in this attempt, historical GPT audit retained. |
| Castelló-Lurbe, Vermeulen & Silvestre (2016) | [10.1364/OE.24.026629](https://doi.org/10.1364/OE.24.026629) | full text | Conserved inverse dispersion/nonlinear lengths and analytical SC tailoring. A direct prior framework, not the proposed certified DW program. |
| Weinstein (1983) | [10.1007/BF01208265](https://doi.org/10.1007/BF01208265) | full text | Publisher PDF, §§I–III: sharp interpolation/ground-state constant and invariant control. Earlier Euclid retrieval failed; publisher copy resolved access. Independent sech constant check is registered. |
| Koch & Tataru (2018) | [10.1215/00127094-2018-0033](https://doi.org/10.1215/00127094-2018-0033) | abstract only | Conserved energies for cubic one-dimensional NLS, not arbitrary GNLSE dispersion/Raman. |
| Deift & Zhou (2003) | [10.1002/cpa.3034](https://doi.org/10.1002/cpa.3034) | not accessed | Identity/title checked: long-time NLS asymptotics with weighted Sobolev data. No new inference from this unread source; original audit retained. |
| Lefevre et al. (2014) | [10.1364/OE.22.019423](https://doi.org/10.1364/OE.22.019423) | full text | VUB author copy; nonlinear coupled-mode adjoint, Raman-converter example. Different design variables and platform. |
| Mohajan et al. (2023) | [arXiv:2307.06414](https://arxiv.org/abs/2307.06414) | full text | Fundamental limits on second-harmonic generation: undepleted-pump quadratic constraints/relaxations; neighbouring method, not depleted SC. |
| Babushkin et al. (2017 issue; online 2016) | [10.1038/lsa.2016.218](https://doi.org/10.1038/lsa.2016.218) | full text | Publisher results: few-cycle two-ZDW high-order pulse breakdown into radiation without ordinary compression/fission. A missed regime that defeats treating record lists as universal limits. |
| Smyth (2000) | [10.1016/S0030-4018(00)00486-7](https://doi.org/10.1016/S0030-4018(00)00486-7) | abstract only | Soliton-effect compression and dispersive radiation; reduced ODE/compression precedent, full exponential-yield relevance unresolved. |
| Zheng & Liu (2022) | [10.3389/fphy.2022.1043168](https://doi.org/10.3389/fphy.2022.1043168) | full text | Publisher text: Cherenkov radiation from a Kuznetsov–Ma breather, repeated compression, nonzero background; not a located decaying higher-order-soliton strip-width yield law. |
| Moston-Duggan, Porter & Lustri (2023) | [10.1007/s00332-022-09834-5](https://doi.org/10.1007/s00332-022-09834-5) | full text | Publisher introduction/formulation of *Nanoptera in Higher-Order Nonlinear Schrödinger Equations: Effects of Discretization*; stationary singularity/Stokes framework. Exact transient relevance reserved for the separate novelty task; arXiv:2203.08407. |

### IR reach, conservation and reported cutoff fractions

| Source | DOI or arXiv identifier | Access in this review | Verification / limitation |
|---|---|---|---|
| Mitschke & Mollenauer (1986) | [10.1364/OL.11.000659](https://doi.org/10.1364/OL.11.000659) | abstract only | Original SSFS observation located; no conversion ceiling claimed. |
| Gordon (1986) | [10.1364/OL.11.000662](https://doi.org/10.1364/OL.11.000662) | abstract only | Original isolated-soliton rate; coefficient conversion in this report is algebra, not a new propagation simulation. |
| Santhanam & Agrawal (2003) | [10.1016/S0030-4018(03)01561-X](https://doi.org/10.1016/S0030-4018(03)01561-X) | abstract only | General moment-method treatment with width/chirp effects; full saturation assumptions remain to check. |
| Zheltikov (2007) | [10.1103/PhysRevE.75.037603](https://doi.org/10.1103/PhysRevE.75.037603) | abstract only | Perturbative adiabatic SSFS moderation; full reach formula/conditions remain to inspect. |
| Arteaga-Sierra, Antikainen & Agrawal (2017) | [arXiv:1707.06258](https://arxiv.org/abs/1707.06258) | abstract only | Nonlinear-dispersion control of SSFS; incomplete PDF transfer prevented a complete independent equation check. Prior “partial full text” is not promoted. |
| Arteaga-Sierra et al. (2017), genetic optimization | [10.31349/RevMexFis.63.2.111](https://doi.org/10.31349/RevMexFis.63.2.111) | full text | Publisher PDF, §§2–4 and Eqs. 2–3: integrated Raman-channel fitness, output-normalized efficiency, variable wavelength/power/duration; not a fixed-spectrum passive-mask bound. |
| Skryabin et al. (2003) | [10.1126/science.1088516](https://doi.org/10.1126/science.1088516) | abstract only | Cancellation by resonant radiation near a second ZDW supported. |
| Biancalana, Skryabin & Yulin (2004) | [10.1103/PhysRevE.70.016615](https://doi.org/10.1103/PhysRevE.70.016615) | abstract only | Original compensation theory located; abstract/first page read, full coefficient derivation not independently checked. |
| Frosz, Falk & Bang (2005) | [10.1364/OPEX.13.006181](https://doi.org/10.1364/OPEX.13.006181) | abstract only | Two-ZDW continua and soliton pairs. The unusual `OPEX` DOI is valid and should not be silently “corrected” to `OE`. |
| Xia et al. (2006) | [10.1364/OL.31.002553](https://doi.org/10.1364/OL.31.002553) | abstract only | ZBLAN material-loss-limited edge in a nanosecond-pumped regime. |
| Xia et al. (2007) | [10.1364/OE.15.000865](https://doi.org/10.1364/OE.15.000865) | abstract only | Peak-pump-power-limited reach in the studied regime; not inconsistent with an eventual material absorption edge. |
| Pant et al. (2010) | [10.1364/JOSAB.27.001894](https://doi.org/10.1364/JOSAB.27.001894) | abstract only | Fission/reach model and fibre optimization; priority full-text loose end for any claim of new closed-form reach. |
| Judge et al. (2009) | [10.1364/JOSAB.26.002064](https://doi.org/10.1364/JOSAB.26.002064) | abstract only | Optimal taper degree and designed axial profile avoid recoil and enhance SSFS. |
| Bendahmane et al. (2013) | [10.1364/OL.38.003390](https://doi.org/10.1364/OL.38.003390) | abstract only | Inverse-designed topographic fibres; geometry optimization is already established. |
| Gorbach & Skryabin (2007), Nature Photonics | [10.1038/nphoton.2007.202](https://doi.org/10.1038/nphoton.2007.202) | abstract only | Light trapping/expansion mechanism. |
| Gorbach & Skryabin (2007), PRA | [10.1103/PhysRevA.76.053803](https://doi.org/10.1103/PhysRevA.76.053803); arXiv:0707.1598 | full text | Trapping theory, especially §VI backaction on soliton acceleration. |
| Kormokar, Shamim & Rochette (2021) | [10.1364/JOSAB.409240](https://doi.org/10.1364/JOSAB.409240) | full text | High-order analytical drift; loss, shock, dispersion slope and limitations from radiation/cross terms. Not a uniform upper bound. |
| Kormokar, Shamim & Rochette (2023) | [10.1364/JOSAB.478975](https://doi.org/10.1364/JOSAB.478975); arXiv:2301.02945 | full text | Eqs. 24–25 and validation: analytic conversion correction with empirical calibration, not only qualitative transfer. |
| Gauthier et al. (2022) | [10.1038/s41598-022-19658-8](https://doi.org/10.1038/s41598-022-19658-8) | full text | Author manuscript, source/cutback/results: InF3 Raman soliton; quoted fraction is of total output, architecture includes an amplifier. |
| Gauthier et al. (2016) | [10.1364/OL.41.001756](https://doi.org/10.1364/OL.41.001756) | abstract only | Red-cutoff fraction explicitly refers to output power. |
| Kulkarni et al. (2011) | [10.1364/JOSAB.28.002486](https://doi.org/10.1364/JOSAB.28.002486) | abstract only | Red-band power divided by total SC output is distinct from pump-to-SC conversion. |
| Martinez et al. (2018) | [10.1364/OL.43.000296](https://doi.org/10.1364/OL.43.000296) | abstract only | Long-pass power is a subset of total output; quoted powers use the stated pump duty cycle. |
| Tang et al. (2016) | [10.1364/OPTICA.3.000948](https://doi.org/10.1364/OPTICA.3.000948) | abstract only | Intense tunable fluoride-fibre solitons; record, not a bound. |
| Chen et al. (2022) | [10.1364/OL.445499](https://doi.org/10.1364/OL.445499) | abstract only | Hydrogen-filled hollow-core SSFS; efficiency changes across tuning range, model differs from silica. |
| Petersen et al. (2014) | [10.1038/nphoton.2014.213](https://doi.org/10.1038/nphoton.2014.213) | not accessed | Bibliographic identity located; stated spectral span was not independently verified against original text. |
| Petersen et al. (2017) | [10.1364/OE.25.015336](https://doi.org/10.1364/OE.25.015336) | full text | DTU author copy; pre-taper-length optimization balances spectral extension and loss/output power. |
| Kormokar, Nayan & Rochette (2025) | [10.1364/OL.551176](https://doi.org/10.1364/OL.551176) | abstract only | Optimal prechirp inside a thulium amplifier; not a passive-fibre ceiling. |
| Solli, Ropers & Jalali (2008) | [10.1103/PhysRevLett.101.233902](https://doi.org/10.1103/PhysRevLett.101.233902) | abstract only | Active weak-seed control of rogue-wave/SC dynamics; different input control class. |
| Blow & Wood (1989) | [10.1109/3.40655](https://doi.org/10.1109/3.40655) | not accessed | Identity verified; do not infer arbitrary frequency-dependent photon conservation from an unread original derivation. |
| Bonetti et al. (2020) | [10.1364/JOSAB.377891](https://doi.org/10.1364/JOSAB.377891) | full text | Model and conservation derivation; special linear nonlinear-dispersion equivalence and general symmetric kernel. |
| Linale, Fierens & Grosz (2021; online 2020) | [10.1109/JQE.2020.3047691](https://doi.org/10.1109/JQE.2020.3047691) | abstract only | Short-soliton discrepancy in relevant generalized models; not universal failure of the special shock equation. |
| Huang et al. (2026) | [arXiv:2607.05244](https://arxiv.org/abs/2607.05244) | full text | Download accessed 2026-10-16, Eqs. 17–21. Energy and power-centroid equations must be distinguished from the photon mean; preprint status retained. |
| Zheltikov (2018) | [10.1103/PhysRevA.98.043833](https://doi.org/10.1103/PhysRevA.98.043833) | full text | APS accepted manuscript: physical photon conservation versus envelope norm. |
| Vanvincq, Travers & Kudlinski (2011) | [10.1103/PhysRevA.84.063820](https://doi.org/10.1103/PhysRevA.84.063820) | abstract only | Photon conservation in axially varying fibres requires an additional term; relevant if tapers enter the admissible fibre class. |
| Kibler et al. (2011) | [10.1103/PhysRevE.84.066605](https://doi.org/10.1103/PhysRevE.84.066605) | abstract only | Spectral incoherent solitons at a red SC edge; stochastic/kinetic regime, not a bound for a deterministic femtosecond launch. |
| Michel, Kibler & Picozzi (2011) | [10.1103/PhysRevA.83.023806](https://doi.org/10.1103/PhysRevA.83.023806) | not accessed | Identity verified: discrete spectral incoherent solitons with noninstantaneous response. Full kinetic assumptions not independently checked. |

### ZS, Raman source and jitter sources

| Source | DOI or arXiv identifier | Access in this review | Verification / limitation |
|---|---|---|---|
| Satsuma & Yajima (1974) | [10.1143/PTPS.55.284](https://doi.org/10.1143/PTPS.55.284) | abstract only | Original located; exact sech content independently read in later full-text sources, original derivation still an access loose end. |
| Prilepsky, Derevyanko & Turitsyn (2007) | [10.1364/JOSAB.24.001254](https://doi.org/10.1364/JOSAB.24.001254) | abstract only | Gaussian chirp and partition study; historical Claude full-text access is separate. The fixed-time-profile chirp family is not fixed Fourier magnitude. |
| Klaus & Shaw (2002) | [10.1103/PhysRevE.65.036607](https://doi.org/10.1103/PhysRevE.65.036607) | full text | Real single-lobe theorem; symmetry alone does not force imaginary spectrum for general profiles. |
| Klaus & Shaw (2003) | [10.1137/S0036141002403067](https://doi.org/10.1137/S0036141002403067) | abstract only | Sharp area threshold and eigenvalue-count bounds located. Strict eigenvalue threshold caveat stated above. |
| Klaus & Shaw (2001) | [10.1016/S0030-4018(01)01461-4](https://doi.org/10.1016/S0030-4018(01)01461-4) | abstract only | Pulse-shape/chirp influence on optical-soliton stability; related spectral precedent, full theorem not used. |
| Tovbis & Venakides (2000) | [10.1016/S0167-2789(00)00126-3](https://doi.org/10.1016/S0167-2789(00)00126-3) | abstract only | Solvable focusing-NLS scattering cases; not a universal phase-mask optimum. |
| Burzlaff (1988) | [10.1088/0305-4470/21/2/034](https://doi.org/10.1088/0305-4470/21/2/034) | not accessed | Identity/title verified: soliton number for two special input families. Original Claude full-text claim preserved but not independently reproduced. |
| Hmurcik & Kaup (1979) | [10.1364/JOSA.69.000597](https://doi.org/10.1364/JOSA.69.000597) | abstract only | Self-induced transparency/Zakharov–Shabat problem, not directly a fibre-NLS experiment. Chirp can lower higher-branch box-profile thresholds; global “chirp always removes solitons” is false. Publisher lists an erratum; inspect it before using detailed formulas. |
| Desaix, Anderson & Lisak (1994) | [10.1103/PhysRevE.50.2253](https://doi.org/10.1103/PhysRevE.50.2253) | abstract only | Variational approximation to ZS scattering, not a rigorous universal upper bound. |
| Kaup & Malomed (1995) | [10.1016/0167-2789(95)00057-B](https://doi.org/10.1016/0167-2789(95)00057-B) | abstract only | Variational soliton-formation criterion; do not promote approximate thresholds to exact enclosures. |
| Desaix et al. (2002) | [10.1103/PhysRevE.65.056602](https://doi.org/10.1103/PhysRevE.65.056602) | abstract only | Chirped soliton propagation/pairs; full parameter domain not checked. |
| Chekhovskoy et al. (2020) | [arXiv:2003.02215](https://arxiv.org/abs/2003.02215) | full text | Eq. 17 chirped-sech eigenvalues; only positive imaginary branches are bound states. |
| Biondini & Luo (2018) | [10.1016/j.physleta.2018.06.045](https://doi.org/10.1016/j.physleta.2018.06.045) | abstract only | Single-lobe/nonzero-background spectral extension; do not transfer its setting without conditions. |
| Biondini, Oregero & Tovbis | [10.4171/JST/432](https://doi.org/10.4171/JST/432); arXiv:2010.04263 | full text | Lemma 3.8, Eqs. 3.9–3.11, proof §6.1: amplitude strip in periodic/Dirichlet settings. Journal volume is 2022; online publication is 2023. |
| DiFranco & Miller (2008) | [arXiv:nlin/0702028](https://arxiv.org/abs/nlin/0702028) | full text | Modified-NLS spectral bounds and semiclassical shadow-bound discussion. Unpublished Deift notes are identified as such. |
| Bronski (1996) | [10.1016/0167-2789(95)00311-8](https://doi.org/10.1016/0167-2789(95)00311-8) | abstract only | Semiclassical ZS eigenvalue distributions; no exact line-amplitude theorem attributed without full text. |
| Lenzmann & Sok | [arXiv:1805.06294](https://arxiv.org/abs/1805.06294) | full text | Lemmas 5.1–5.2: Fourier majorant and equality; even-power/peak statement covers the input extremality. |
| Lieb, Lieb–Thirring survey | [arXiv:math-ph/0003039](https://arxiv.org/abs/math-ph/0003039) | abstract only | Self-adjoint Schrödinger context; not a located complex-ZS bound. |
| Laptev & Weidl | [arXiv:math-ph/9903007](https://arxiv.org/abs/math-ph/9903007) | abstract only | Sharp Lieb–Thirring context; not directly applicable to complex ZS. |
| Kodama & Hasegawa (1987) | [10.1109/JQE.1987.1073392](https://doi.org/10.1109/JQE.1987.1073392) | not accessed | Identity verified: nonlinear pulse propagation in a monomode guide. No independent detailed fission statement asserted from this unread original. |
| Tai, Hasegawa & Bekki (1988) | [10.1364/OL.13.000392](https://doi.org/10.1364/OL.13.000392) | abstract only | Raman-induced fission in the studied weakly perturbed regime; does not prove universal preservation of IST amplitudes. |
| Husakou & Herrmann (2001) | [10.1103/PhysRevLett.87.203901](https://doi.org/10.1103/PhysRevLett.87.203901) | abstract only | Higher-order-soliton fission contribution to SC; not a yield ceiling. |
| Dudley, Genty & Coen (2006) | [10.1103/RevModPhys.78.1135](https://doi.org/10.1103/RevModPhys.78.1135) | full text | Fission/scaling sections in accessible copy; exact integrable anchors become approximations in a perturbed SC. |
| Driben et al. (2013) | [10.1103/PhysRevA.87.063808](https://doi.org/10.1103/PhysRevA.87.063808); arXiv:1305.5911 | full text | Newton's-cradle fission and energy exchange; input partition need not persist. |
| Liu et al. (2001) | [10.1364/OL.26.000358](https://doi.org/10.1364/OL.26.000358) | abstract only | Tapered air–silica source record supported; detailed input/collection accounting still requires full text. |
| Lee et al. (2008) | [10.1109/JSTQE.2008.915526](https://doi.org/10.1109/JSTQE.2008.915526) | full text | PMC author manuscript, theory/platform sections; energy–dispersion–mode-area scaling and records. Repository author ordering differs across versions; no unsupported correction to the card's author order. |
| Wang et al. (2017) | [10.1364/OL.42.003518](https://doi.org/10.1364/OL.42.003518) | abstract only | Thulium-doped amplifier explicitly supplies gain; incomparable to a passive input-energy ceiling. |
| Horton et al. (2013) | [10.1038/nphoton.2012.336](https://doi.org/10.1038/nphoton.2012.336) | full text | Cornell author PDF, source paragraph and methods; source-energy record verified, no universal conversion claim. |
| Hu et al. (2015) | [10.1103/PhysRevLett.114.073901](https://doi.org/10.1103/PhysRevLett.114.073901) | full text | APS accepted manuscript; Airy asymmetry and cubic-phase offset control primary/secondary solitons. |
| Caldarola et al. (2012) | [10.4279/PIP.040001](https://doi.org/10.4279/PIP.040001) | full text | Journal PDF, §IV and comparisons: heavily chirped pumping needs more power for the same reach in this setup; no universal chirp theorem. |
| Rosenberg et al. (2020) | [10.1364/OE.383014](https://doi.org/10.1364/OE.383014) | abstract only | Primary publisher/PubMed and author-institution abstract verified. Indexed manuscript excerpts show the experiment; original full PDF not reached. Negative prechirp increases few-cycle reach. |
| Drummond & Corney (2001) | [10.1364/JOSAB.18.000139](https://doi.org/10.1364/JOSAB.18.000139); arXiv:quant-ph/9912095 | full text | Quantum Raman reservoir derivation. |
| Corney & Drummond (2001) | [10.1364/JOSAB.18.000153](https://doi.org/10.1364/JOSAB.18.000153); arXiv:quant-ph/9912096 | full text | Eq. 3.15 frequency/velocity covariance and timing result; analytic versus numerical treatment of deterministic SSFS distinguished. |
| Zhou et al. (2015) | [10.1364/OL.40.005105](https://doi.org/10.1364/OL.40.005105) | abstract only | Primary abstract and indexed DESY first-page text: intensity-to-wavelength-to-timing noise. Full file did not download; no final intrinsic-noise bound inferred. |

### Corrections and unresolved verification

No located DOI in the original cards was shown to identify a different paper. Missing identifiers have been supplied in this ledger. The Petty identifier is a thesis DOI; its absence from Crossref is not evidence that it is invalid. Frosz's `OPEX` identifier and Webb's later arXiv deposit are also valid. Linale's year needs the journal/online distinction. Several original references without identifiers had to be located by author, volume and page.

The material errors are mostly in **what was inferred**: the extra factor in Roy's daughter TOD parameter; calling energy-envelope invariants physical photons; exact-energy nesting under attenuation; an uncertified grid optimum treated as an upper bound; asserting TL reach optimality from input peak optimality; omitting the photon-mean normalization factor and loss covariance; overlooking existing gradient DW control and analytic Raman-transfer correction; and treating narrow-channel/output/amplified records as a common passive broad-band conversion measure. Caldarola's particular heavily chirped comparison is supported, but cannot be generalized in light of Rosenberg's different few-cycle regime.

The Petty matched-TL headroom ratio, Lei's both-sign chirp claim, the fully harmonized thesis record-table range, and detailed formulas in the ledger's inaccessible originals remain **unverified**, not refuted. The earliest decaying-line attribution of the amplitude enclosure also remains unresolved. These limitations do not justify claiming that the associated elementary inequality is novel.

### Search log

Search date: **2026-10-16**. Public web search, publisher pages, Crossref DOI records, DataCite for the thesis, arXiv, author/institutional copies (including Chalmers, Rochester, DTU, VUB, Cornell, Tampere and APS accepted manuscripts), and accessible indexed manuscript text were used. HAL/repository queries were attempted where publisher PDFs were unavailable. Only the three authorized problem cards and project instructions were read locally for this task; no other-project conversations were searched. The separate Task 2 claim and its proposer notes had not been read when this report was drafted.

| Search family | Representative actual queries / follow-up terms | Outcome and scope of negative conclusion |
|---|---|---|
| Verify originals | Exact DOI; author/year/volume/page; exact title plus `pdf`, `arxiv`, `HAL`, `author manuscript`; `Petty 2024 dispersive wave thesis`; `Klaus Shaw 34 759`; `Burzlaff 21 561` | Located the named original works, filled missing identifiers, separated blocked originals from read full texts. Does not imply every original numerical record was remeasured. |
| ZS enclosure | `Zakharov Shabat eigenvalue imaginary part sup norm`; `Klaus Shaw single lobe eigenvalue bound`; `Deift Zakharov Shabat shadow bound`; `Bronski semiclassical eigenvalue`; `Lieb Thirring Zakharov Shabat complex potential` | Explicit published amplitude strip and related enclosures found; no direct transfer of self-adjoint Lieb–Thirring theory to general complex ZS established. Earliest exact line attribution unresolved. |
| Spectral-phase extremality | `Fourier majorant even p equality phase Lenzmann Sok`; `fixed Fourier modulus L4 norm phase`; `Zakharov Shabat spectral phase optimal soliton eigenvalue` | Peak/even-power majorant is known. No general largest-eigenvalue TL optimality theorem established for this mask class. |
| DW theory | `Akhmediev Karlsson Cherenkov radiation 1995`; `Roy Bhadra Agrawal dispersive waves fission 2009`; `Austin dispersive wave compression recoil`; `higher order soliton compression complex singularity radiation exponential asymptotics`; `soliton effect compression dispersive radiation Smyth` | Stationary flux, fission-daughter peak law, compression-window recoil and breather-radiation precedents found. The specific transient integrated-yield exponent requires Task 2, not a blanket novelty declaration here. |
| DW control | `gradient descent dispersive wave conversion efficiency pulse shaper`; `adjoint nonlinear coupled mode Raman optimization`; `Li quadratic cubic spectral phase dispersive wave conversion efficiency`; `sinusoidal spectral phase dispersive wave` | Li and Liu directly supersede the negative shaping/control statements; denominators and amplification differ. |
| Mathematical/photonic bounds | `Hamiltonian spectral band bound nonlinear Schrodinger Gagliardo Nirenberg`; `fundamental limits nonlinear frequency conversion convex`; `supercontinuum conservation Hamiltonian upper bound`; `nonlinear photonic inverse design adjoint bounds` | Optical invariants and neighbouring nonlinear convex limits found. No nontrivial continuum-certified passive-mask GNLSE DW-band bound was located in the inspected sources. |
| IR reach and loss | `photon conserving GNLSE Raman mean frequency energy loss Bonetti`; `Raman spectral moment passive response monotonic frequency`; `mid infrared chalcogenide supercontinuum optimal length loss edge taper`; `fluoride supercontinuum conversion efficiency beyond cutoff`; `supercontinuum integrated energy cutoff bound` | Photon-conserving formulations, corrected drift and length/loss optimization found; no uniform reach/peak closure for the full stated class established. |
| Raman shaping and transfer | `adaptive pulse shaping soliton self frequency shift genetic algorithm`; `Optimization for maximum Raman frequency conversion`; `Raman soliton conversion efficiency interpulse Raman scattering`; `negative prechirp few cycle soliton`; `Boosting few-cycle soliton self-frequency shift`; `inverse design tapered fiber soliton self frequency shift` | Quantitative adaptive/GA control, prechirp-enhanced reach and a calibrated analytic transfer correction found. No controlled general propagated passive-mask frontier established. |
| Noise frontier | `Raman soliton timing jitter frequency variance`; `Corney Drummond Raman quantum noise covariance`; `Timing jitter optimization Raman solitons` | Published reservoir/covariance and technical-noise conversion results; no universal final-variance-per-shift floor without transport and a specified ensemble established. |

Source PDFs, extracted text, metadata responses and retrieval-failure records are outside git at `~/analytical-nl-discovery-data/2026-10-16-gpt-b-sclit-sources/`. No copyrighted full text or raw numerical arrays are committed. The registered numerical check is `runs/2026-10-16-gpt-b-sclit-premises/`; it uses NumPy only, no Julia or propagation solver. Its algebraic examples and refined-grid identity checks are reproducible from the committed script/configuration. Run numbers are not literature records and literature percentages are not presented as newly measured results.

## Follow-up work

- **T-20261016-gpt-b-01:** original-text access, detailed attribution/denominators and earliest decaying-line enclosure reference; consult every unresolved ledger row.
- **T-20261016-gpt-b-02:** physical-dispersion DW relaxation, nontriviality and continuum certification.
- **T-20261016-gpt-b-03:** passivity/loss-aware IR reach or peak-power closure, including transfer/radiation channels.
- **T-20261016-gpt-b-04:** controlled Raman-transfer correction and transported final covariance frontier.
- **T-20261016-gpt-b-05** (Claude family): agree or disagree explicitly with each revised scope before changing candidate to audited.

The review itself is complete with these explicit access and theorem limitations; it does not claim the new bounds have been proved or simulation-verified.
