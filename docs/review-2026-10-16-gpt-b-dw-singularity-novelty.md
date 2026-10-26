---
agent: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-16
task: T-20261016-claude-b-08
claim: C-20261016-claude-b-01
---

# Novelty review: the evolving-strip law for a dispersive-wave burst

**Verdict: partly published.** Complex-singularity control of exponentially
small radiation is established, including in the third-order-dispersion NLS.
Radiation from higher-order solitons during breathing and compression is also
established. I did **not find the specific integrated-yield limit**
$\lim_{\delta_3\to0}\delta_3\log\eta_{\rm DW}=-\min_{0\le\xi\le\xi_f}d(\xi)$
for the evolving, unperturbed NLS breather. Confidence is high about the
published ingredients and **medium** about the absence of this precise law.
The inaccessible older full texts listed below limit the negative finding.

This is a literature verdict, not a verification or adversarial mathematical
audit. The claim's status should remain `cheap-checks-passed`. Before committing
this report I read only the claim card and the assigned task among the
proposer's task artifacts. I did not read the proposer’s explorations, logs,
run outputs, evaluator code, or branch history. Git checkout/merge output
incidentally displayed a commit subject and changed filenames. This report
uses public literature and the claim's stated definitions. No new numerical
check or simulation was performed.

## What is already published

| Part of the proposed story | Closest evidence | Remaining distinction |
|---|---|---|
| An exponentially small radiation amplitude determined by complex poles | Wai–Chen–Lee (1990), Karpman (1993), Akhmediev–Karlsson (1995); full text, identifiers in the ledger | These calculations use a fundamental sech core, possibly with slow parameter evolution. They do not supply the proposed minimum over a breathing core. |
| Radiation emitted before the higher-order soliton has separated into daughter solitons | Austin et al. (2006), Demircan et al. (2007), Driben–Yulin–Efimov (2015); full text | The physical timing is known. The proposed weak-TOD integrated-yield exponent was not found in their analyses. |
| An analytic exponential estimate for radiation from a higher-order launch | Roy–Bhadra–Agrawal (2009), DOI 10.1103/PhysRevA.79.023824; full text | Their Eq. (6) substitutes the shortest daughter-soliton width into the stationary-core estimate and describes a spectral peak, rather than this gated band integral. |
| Fourier tails as a diagnostic of an evolving analyticity strip | Sulem–Sulem–Frisch (1983), DOI 10.1016/0021-9991(83)90045-1; abstract only | Measuring the strip is an established method. A Fourier-tail diagnostic alone does not establish a radiative-yield law. |

### Closest physical predecessors

**Driben, Yulin and Efimov is the most direct missing higher-order-soliton
reference.** Their full preprint, [arXiv:1505.02716](https://arxiv.org/abs/1505.02716),
is titled *Synchrotron radiation of higher order soliton*. The journal title is
*Resonant radiation from oscillating higher order solitons*,
[DOI 10.1364/OE.23.019112](https://doi.org/10.1364/OE.23.019112).
It uses the exact higher-order breather, follows TOD-induced radiation while
the pulse still oscillates, and derives a phase-matching description of the
radiation comb. Its analytic target is the radiated frequencies. I found no
yield exponent obtained from the nearest complex-time pole or its minimum
over propagation. The exact breather expression in its Eq. (2) is also a
published starting point for locating those poles; that expression itself is
not a novelty of the claim. Access: **full text**, preprint throughout.

Austin et al., [DOI 10.1364/OE.14.011997](https://doi.org/10.1364/OE.14.011997),
already identify the short region of maximum temporal compression as the
main radiation-generation region, before distinct fundamental solitons have
emerged. They calculate the integrated DW energy during propagation and
correct phase matching using the evolving nonlinear wavenumber and spectral
recoil. Thus neither compression-localized emission nor integrating its
energy is new. Their result does not give the claimed strip-width exponent.
Access: **full text**, author-uploaded article, especially §§4–7.

Related precedents extend to other breather settings: Peregrine-pulse local
wavenumbers in Baronio–Chen–Trillo (2020), Kuznetsov–Ma radiation in Zheng–Liu
(2022), and radiation at higher-order-soliton compression in quadratic media
in Bu et al. (2023). These papers analyze resonant frequencies and simulated
emission in their respective models; I did not find the proposed weak-TOD
yield limit in their relevant analyses. Identifiers and full-text scope are
recorded in the ledger. These are comparisons, not equivalent physical
models of the claim.

### Closest asymptotic predecessors

Wai, Chen and Lee, [DOI 10.1103/PhysRevA.41.426](https://doi.org/10.1103/PhysRevA.41.426),
analytically continue the fundamental sech solution to its nearest poles,
match inner and outer expansions, and obtain exponentially small radiation.
The calculation in §§III–V explicitly uses a fundamental core. The concluding
observation that TOD also breaks up breathers is not a derivation of a
breather's radiation exponent. Access: **full text**, especially §§III–VI.

Karpman, [DOI 10.1103/PhysRevE.47.2073](https://doi.org/10.1103/PhysRevE.47.2073),
§III analyzes the NLS fundamental-soliton radiation through a complex
singularity and obtains its exponentially small amplitude. Slowly varying
soliton parameters and radiation dynamics occur in this literature; it would
be inaccurate to dismiss all of it as purely stationary. What is absent from
the NLS calculation read here is the strongly breathing higher-order core
and its minimum strip width over a finite interval. Access: **full text**.

Moston-Duggan, Porter and Lustri,
[DOI 10.1007/s00332-022-09834-5](https://doi.org/10.1007/s00332-022-09834-5),
[arXiv:2203.08407](https://arxiv.org/abs/2203.08407), carry exponential
asymptotics out at the PDE level for higher-order NLS equations and their
discretizations. In the relevant continuous calculations their leading
solution is a travelling fundamental sech pulse and the singulants originate
at its complex poles. This is a closer methodological predecessor than a
general analogy with KdV, but not the evolving-breather minimum law.
Access: **full text**, §§1–4 and the concluding discussion.

McCue et al., [arXiv:2509.07397](https://arxiv.org/abs/2509.07397), is now
published as [DOI 10.1017/jnw.2026.10033](https://doi.org/10.1017/jnw.2026.10033).
It relates complex singularities and exponentially small dispersive waves
for the KdV small-time problem, including exact multi-soliton comparisons.
Its asymptotic variable, equation, and observable differ from the claim.
Crucially, the multiplier in Eq. (2.11) can vanish even though the complex
poles remain: pole distance alone is not universally a radiation law.
This is a reason to establish a nonzero coupling in the NLS problem, not a
refutation by analogy. Access: **full text**, §§1–2, 4–5 and Appendix A.
The published erratum,
[DOI 10.1017/jnw.2026.10036](https://doi.org/10.1017/jnw.2026.10036)
(**full text**), corrects citation numbering rather than the analysis.

## The novelty that remains plausible

The defensible target is a **finite-length, weak-TOD asymptotic law for
escaping, integrated radiation from a specified higher-order launch**, in
which the leading exponential rate is obtained from the *evolving* TOD-free
core rather than the width of an already ejected fundamental soliton.
It should be distinguished from a first application of complex poles to
optical radiation, a first demonstration of breather radiation, or a first
identification of maximum compression as the emission region. Those broader
claims would conflict with the sources above.

The literature review does not establish that this target is true. The
following are derivation or verification obligations, not findings from a
new run:

- Connect the directional Fourier-tail rate to the actual forced-radiation
  amplitude and its nonzero Stokes/coupling multiplier. A nearest singularity
  need not couple to the measured outgoing mode.
- Control coherent contributions from different poles and compression events.
  A minimum of real decay rates is not, by itself, a lower bound on an
  oscillatory amplitude integral.
- Specify the gate exactly and bound residual core tails and gate-generated
  spectral leakage in the stated limit. Changing a fixed gate over a finite
  numerical range does not establish that its contamination remains below an
  exponentially small signal as $\delta_3\to0$.
- Distinguish spectral peak height, radiated flux, and the claimed band
  integral; justify the band edge and fixed-length escape condition. Derive
  the prefactor separately. The Raman extension and the nonasymptotic collapse
  require their own checks.

The existing verification task T-20261016-claude-b-01 remains necessary.
T-20261016-gpt-b-06 covers original-text access; T-20261016-gpt-b-07 covers
the asymptotic observable and coupling.
No claim status or independence gate is advanced by this review.

## Source ledger

“Full text” means the original article or an author preprint was available and
the specified relevant sections were read; it does not mean every cited
simulation was reproduced. “Abstract only” may include bibliographic details
and a publisher's first-page preview. “Not accessed” means the work was located
but its substantive text was not read. Such entries do not support a claim
about what the full paper excludes.

| Source | DOI or arXiv identifier | Access and finding |
|---|---|---|
| Wai, Chen & Lee (1990), *Radiations by “solitons” at the zero group-dispersion wavelength of single-mode optical fibers* | [10.1103/PhysRevA.41.426](https://doi.org/10.1103/PhysRevA.41.426) | **Full text**, APS PDF, §§III–VI. Fundamental-core beyond-all-orders radiation; breather breakup mentioned separately. |
| Karpman (1993), *Radiation by solitons due to higher-order dispersion* | [10.1103/PhysRevE.47.2073](https://doi.org/10.1103/PhysRevE.47.2073) | **Full text**, APS PDF, especially §III. Fundamental NLS complex-pole radiation. |
| Akhmediev & Karlsson (1995), *Cherenkov radiation emitted by solitons in optical fibers* | [10.1103/PhysRevA.51.2602](https://doi.org/10.1103/PhysRevA.51.2602) | **Full text**, APS article inspected during the preceding literature task. Fundamental radiation amplitude/flux and recoil; not the transient minimum law. |
| Roy, Bhadra & Agrawal (2009), *Dispersive waves emitted by solitons perturbed by third-order dispersion inside optical fibers* | [10.1103/PhysRevA.79.023824](https://doi.org/10.1103/PhysRevA.79.023824) | **Full text**, APS PDF, §§II–IV. Eq. (6) uses the shortest daughter width; spectral peak observable. |
| Roy, Bhadra & Agrawal (2009), *Perturbation of higher-order solitons by fourth-order dispersion in optical fibers* | [10.1016/j.optcom.2009.06.018](https://doi.org/10.1016/j.optcom.2009.06.018) | **Abstract only**, original first-page preview also seen. Fourth-order-dispersion comparison; full derivation not excluded. |
| Roy, Bhadra & Agrawal (2009), *Effects of higher-order dispersion on resonant dispersive waves emitted by solitons* | [10.1364/OL.34.002072](https://doi.org/10.1364/OL.34.002072) | **Abstract only**, publisher and author first-page preview. Phase-matching and dispersion-sign classification. |
| Roy, Ghosh, Bhadra & Agrawal (2010), *Role of dispersion profile in controlling emission of dispersive waves by solitons in supercontinuum generation* | [10.1016/j.optcom.2010.04.003](https://doi.org/10.1016/j.optcom.2010.04.003) | **Abstract only**, indexed author first page. Dispersion profiles and emission bands; author PDF now returns 404. |
| Austin, de Sterke, Eggleton & Brown (2006), *Dispersive wave blue-shift in supercontinuum generation* | [10.1364/OE.14.011997](https://doi.org/10.1364/OE.14.011997) | **Full text**, author upload indexed on ResearchGate, §§4–7. Compression-region integrated energy and recoil-corrected frequencies. |
| Demircan, Pietrzyk & Bandelow (2007), *Effect of higher-order dispersion on modulation instability, soliton propagation and pulse splitting* | [10.34657/2265](https://doi.org/10.34657/2265) | **Full text**, WIAS preprint; §2.2 read from rendered pages because font extraction failed. Breathing pulses transfer power whenever their broadened spectrum overlaps the resonance. No transient-strip formula in this section. |
| Driben, Yulin & Efimov (2015), *Resonant radiation from oscillating higher order solitons* | [10.1364/OE.23.019112](https://doi.org/10.1364/OE.23.019112); [1505.02716](https://arxiv.org/abs/1505.02716) | **Full text**, arXiv preprint throughout. Direct higher-order-breather radiation and comb phase matching. |
| Driben et al. (2013), *Newton's cradles in optics: From N-soliton fission to soliton chains* | [10.1103/PhysRevA.87.063808](https://doi.org/10.1103/PhysRevA.87.063808); [1305.5911](https://arxiv.org/abs/1305.5911) | **Full text**, author preprint inspected in the preceding task. Higher-order fission and soliton ejection; no evolving-strip exponent found. |
| Ciret et al. (2018), *Physical origin of higher-order soliton fission in nanophotonic semiconductor waveguides* | [1805.05175](https://arxiv.org/abs/1805.05175) | **Full text**, model, results, conclusion. Separates perturbations causing fission in semiconductor waveguides; different scope. |
| Baronio, Chen & Trillo (2020), *Resonant radiation from Peregrine solitons* | [10.1364/OL.381228](https://doi.org/10.1364/OL.381228) | **Full text**, author manuscript, especially Eqs. (4)–(5). Compression-dependent local wavenumber predicts resonant frequencies. |
| Zheng & Liu (2022), *Cherenkov radiation emitted by Kuznetsov–Ma solitons* | [10.3389/fphy.2022.1043168](https://doi.org/10.3389/fphy.2022.1043168) | **Full text**, model and radiation analysis. Breathing emission on a nonzero background; not the decaying-launch yield limit. |
| Bu, Chen, Baronio & Trillo (2023), *Resonant radiation emitted by solitary waves via cascading in quadratic media* | [10.1364/OE.481676](https://doi.org/10.1364/OE.481676) | **Full text**, author copy, §§3–4. Higher-order-breather compression bursts and local phase matching in a different medium. |
| Pomeau, Ramani & Grammaticos (1988), *Structural stability of the Korteweg-de Vries solitons under a singular perturbation* | [10.1016/0167-2789(88)90018-8](https://doi.org/10.1016/0167-2789(88)90018-8) | **Not accessed**. Identity verified in Crossref and original-paper bibliographies; publisher text blocked. No direct exclusion based on its title. |
| Grimshaw (1995), *Weakly Nonlocal Solitary Waves in a Singularly Perturbed Nonlinear Schrödinger Equation* | [10.1002/sapm1995943257](https://doi.org/10.1002/sapm1995943257) | **Abstract only**, Wiley. Borel-summed radiation amplitude modifies and extends Wai et al.; full-text scope remains to check. |
| Grimshaw & Joshi (1995), *Weakly Nonlocal Solitary Waves in a Singularly Perturbed Korteweg-de Vries Equation* | [10.1137/S0036139993243825](https://doi.org/10.1137/S0036139993243825) | **Abstract only**, publisher. KdV weakly nonlocal solitary-wave comparison. |
| Boyd (1990), *A numerical calculation of a weakly non-local solitary wave: the φ4 breather* | [10.1088/0951-7715/3/1/010](https://doi.org/10.1088/0951-7715/3/1/010) | **Abstract only**. Located Michigan repository copy returned 404/429. Different breather equation; full text still needed. |
| Boyd (1997), *Pseudospectral/Delves–Freeman Computations of the Radiation Coefficient…* | [10.1006/jcph.1997.5840](https://doi.org/10.1006/jcph.1997.5840) | **Not accessed**. Exact title/DOI verified in Crossref and author bibliography; no conclusion based on third-party summaries. |
| Segur & Kruskal (1987), *Nonexistence of Small-Amplitude Breather Solutions in φ4 Theory* | [10.1103/PhysRevLett.58.747](https://doi.org/10.1103/PhysRevLett.58.747) | **Full text**, APS PDF, complex matching and radiation-rate calculation. Exponentially small breather radiation predates the optical claim, but in a different equation and limit. |
| Sulem, Sulem & Frisch (1983), *Tracing complex singularities with spectral methods* | [10.1016/0021-9991(83)90045-1](https://doi.org/10.1016/0021-9991(83)90045-1) | **Abstract only**, publisher. Evolving analyticity-strip diagnostic from Fourier tails; full text not obtained. |
| Moston-Duggan, Porter & Lustri (2023), *Nanoptera in Higher-Order Nonlinear Schrödinger Equations: Effects of Discretization* | [10.1007/s00332-022-09834-5](https://doi.org/10.1007/s00332-022-09834-5); [2203.08407](https://arxiv.org/abs/2203.08407) | **Full text**, UCLA author PDF, §§1–4 and conclusion. PDE exponential asymptotics about a travelling sech core. |
| McCue et al. (2026), *Small-time asymptotics and the emergence of complex singularities for the KdV equation* | [10.1017/jnw.2026.10033](https://doi.org/10.1017/jnw.2026.10033); [2509.07397](https://arxiv.org/abs/2509.07397) | **Full text**, arXiv/journal manuscript, §§1–2, 4–5, Appendix A. Different asymptotic limit; vanishing multiplier illustrates a necessary qualification. |
| McCue et al. (2026), erratum | [10.1017/jnw.2026.10036](https://doi.org/10.1017/jnw.2026.10036) | **Full text**, Cambridge. Citation-number correction only. |
| Calvo & Akylas (1997), *On the formation of bound states by interacting nonlocal solitary waves* | [10.1016/S0167-2789(96)00229-1](https://doi.org/10.1016/S0167-2789(96)00229-1) | **Abstract only**, publisher. Steady multipulse bound states; not evidence for the NLS compression-transient limit. |
| Smyth (2000), *Soliton-effect compression and dispersive radiation* | [10.1016/S0030-4018(00)00486-7](https://doi.org/10.1016/S0030-4018(00)00486-7) | **Abstract only**, plus publisher introduction preview. Variational compression/radiation description; full-text exclusion remains open. |
| Oxtoby & Barashenkov (2007), *Moving solitons in the discrete nonlinear Schrödinger equation* | [nlin/0610059](https://arxiv.org/abs/nlin/0610059) | **Abstract only** for this verdict; PDF retrieved but not systematically read. Moving small-amplitude lattice soliton, rather than the continuum higher-order launch. |
| Mookherjea & Yariv (2001), *Hamiltonian dynamics of breathers with third-order dispersion* | [10.1364/JOSAB.18.001150](https://doi.org/10.1364/JOSAB.18.001150) | **Abstract only**, publisher. Dispersion-managed breather dynamics; full text not checked for a yield formula. |
| Oğuz (2026), *Generalized Thermodynamics of Solitonic Event Horizons in Dispersive Field Theories* | [2601.05156](https://arxiv.org/abs/2601.05156); [10.1088/1361-6382/ae811b](https://doi.org/10.1088/1361-6382/ae811b) | **Full text**, latest author preprint, §§4.3–4.4. Mentions the established fundamental radiation exponential while studying entropy and spectra; no evolving-strip formula there. |

## Search and access log

Searches were performed on 2026-10-16 using live web search, publisher pages,
arXiv, author pages, WIAS, and institutional repositories. Backward references
were followed from Wai, Karpman, Driben, Moston-Duggan, and McCue. The search
covered continuum and discrete NLS, KdV, Klein–Gordon breathers, fibre
compression/fission, and quadratic-media resonant radiation. It was not a
complete citation-index search, and no absence claim is made about unread
full texts.

Representative exact queries:

- `Karpman 1993 radiation by solitons higher order dispersion`
- `Pomeau Ramani Grammaticos structural stability solitons 1988 pdf`
- `Weakly Nonlocal Solitary Waves in a Singularly Perturbed Nonlinear Schrödinger Equation pdf`
- `Pseudospectral Delves Freeman radiation coefficient Boyd 1997 pdf`
- `Tracing complex singularities with spectral methods Sulem Frisch pdf`
- `higher-order soliton fission dispersive wave amplitude maximum compression exponentially small third-order dispersion analytic estimate breather`
- `higher-order soliton exponentially small`
- `breather radiation complex singularities Schrodinger`
- `dispersive wave strip width`
- `soliton fission exponential asymptotics`
- `soliton compression singulant`
- `higher order soliton singularity radiation exponent`
- `breather Cherenkov exponential`
- `Resonant radiation from oscillating higher order solitons`
- `Dispersive wave blue-shift in supercontinuum generation pdf`
- `Roy Bhadra Agrawal 023824` and exact-title searches for their other ledger entries
- `Small-time asymptotics and emergence of complex singularities 10.1017`

The exact strip-width and fission/exponential-asymptotics searches did not
locate the proposed law. Broader searches led to the predecessors discussed
above, not to a proof that no such law exists. Primary sources support the
substantive comparisons; third-party discovery pages were used only to find
identifiers or originals.

APS PDFs were retrieved directly for Wai, Karpman, Roy, and Segur–Kruskal.
Driben, Moston-Duggan, McCue, Ciret, and Oğuz were accessible as author
preprints. Austin's original article was readable in an author-uploaded
ResearchGate full text. Bu and Baronio were reached through Ferrara
repositories. Wiley/Elsevier access and the old Michigan links did not yield
the outstanding originals. Some Rochester PDF URLs remain indexed but now
return 404; an indexed first page was not counted as a full reading.

Source PDFs and extracted text are stored outside git at
`~/analytical-nl-discovery-data/2026-10-16-gpt-b-dw-novelty-sources/`;
previously read Akhmediev–Karlsson and Driben sources are in the adjacent
`2026-10-16-gpt-b-sclit-sources/` directory. No raw source files or simulation
outputs are committed.
