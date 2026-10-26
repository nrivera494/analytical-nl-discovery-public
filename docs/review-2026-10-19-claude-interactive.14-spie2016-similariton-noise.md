---
date: 2026-10-19
agent: claude-interactive.14
model: claude-opus-5-5
family: claude
task: T-20261019-claude-interactive-05
claims: [C-20261008-claude-a-02, C-20261019-pi-chatgpt-02]
problem: P-001
orchestrator: claude-interactive
status: complete
---

# Novelty check: Wang, Liu, Song & Hu, Proc. SPIE 9893, 98930J (2016), against the amplifier-similariton noise claims

GPT 6 Pro's verification of 2026-10-18 named this paper as the closest unread lead for the novelty of C-20261008-claude-a-02 and C-20261019-pi-chatgpt-02. This review records what could be read legitimately, what the paper measures, and whether it anticipates any statement of the two cards. It is a literature review only. No simulation was run, and no derivation or number in either card was checked. The claims' derivation notes were not needed and were not read.

## Summary

**Access: abstract only.** No open full text of the SPIE paper was found by legitimate routes.
- The SPIE Digital Library returns an Incapsula bot-protection page to automated requests, so the publisher landing page itself was not seen.
- The abstract was read from the OpenAlex record (W2345226333), which indexes the publisher's abstract. A web-search summary of the same paper gives the same wording.
- OpenAlex, Unpaywall and Semantic Scholar all list the paper as closed, with no repository copy.
- The more complete later journal version is also closed and was read at abstract level only: Wang, Chen, Qin, Song, Hu & Liu, *Opt. Lett.* 41, 5286 (2016), DOI 10.1364/OL.41.005286. Optica's early-posting PDF of it (`upcoming_pdf.cfm?id=274303`) now leads to the subscription page.

**The PI can download both through institutional access:**
- https://doi.org/10.1117/12.2227743, which resolves to https://www.spiedigitallibrary.org/conference-proceedings-of-spie/9893/98930J/
- https://doi.org/10.1364/OL.41.005286, which resolves to https://opg.optica.org/ol/abstract.cfm?uri=ol-41-22-5286

**What the paper does.** It is an experimental paper on classical relative intensity noise (RIN).
- The amplifier is a free-running, high-power, nonlinear Yb-doped fibre amplifier operated in the spectral-breathing similariton regime with a negative launch chirp.
- The quantity measured is the rms RIN of the total output power, integrated over a Fourier band: 10 Hz–10 MHz for the headline reduction, 1 kHz–5 MHz for the minimum value.
- RIN is reported against launch chirp and input pulse energy, at one headline gain of 25 dB.
- The abstract reports no modal or spectral decomposition of the noise, no phase or homodyne measurement, no quantum-noise reference and no gain scaling law.

**Verdict.** None of the quantitative statements of either card is anticipated.
- One qualitative idea is shared. The abstract attributes the reduced ASE-driven RIN partly to the "asymptotic attractive nature of self-similar pulse amplification".
- C-20261008-claude-a-02 attributes a related de-amplification to the attraction, but for intensity-*shape* modes ($l\ge2$).
- The SPIE observable is the total energy. In the cards' flat, unsaturated gain model that noise is exactly the linear-amplifier value and does not depend on the launch chirp.
- So the paper's mechanism is not the card's mechanism, and its chirp-dependent RIN arises from physics both cards exclude.

**Antecedents.** No closer antecedent was found in the paper's six references, in the 14 references of the journal version, or in the one paper that cites it. The citing paper is Haviv, Kozlov, Krüger & Sidorenko, *Opt. Lett.* 51, 1812 (2026), on gain-managed nonlinear amplifiers. It is the nearest experimental neighbour for the spectral statement (b), but it uses a rate-equation model in a different regime.

| Card | Statement | Verdict |
|---|---|---|
| C-20261008-claude-a-02 | (a) shape-mode variance envelopes $G^{1/3}$ (intensity) and $G^{5/3}$ (phase) | Not anticipated |
| C-20261008-claude-a-02 | (a), interpretive sentence: the attraction de-amplifies intensity(-shape) noise relative to a linear amplifier | Partly anticipated, qualitatively only and for a different observable (total energy) |
| C-20261008-claude-a-02 | (b) spectral covariance tends to rank one, $\mu_2/\mu_1=\Theta(G^{-2/3})$ | Not anticipated |
| C-20261008-claude-a-02 | (c) energy–phase locking, $1-r^2=\Theta(G^{-2/3})$ | Not anticipated |
| C-20261019-pi-chatgpt-02 | (i) $C_{PP}\sim(32n_{sp}/9)G\Phi_{NL}^2\propto G^{7/3}/\varepsilon_0^2$ | Not anticipated |
| C-20261019-pi-chatgpt-02 | (ii) short-gain squeezing with full ASE iff $\gamma\int P^2/\int P>n_{sp}g$ | Not anticipated |
| C-20261019-pi-chatgpt-02 | (iii) large-gain $\lambda_{\min}(C_{\rm LO})=\Theta(G^{1/3})$ | Not anticipated |
| both | squeezing, or its absence, with ASE | Not anticipated |

**Confidence.**
- *High* for (b), (c) and (i)–(iii). An experimental RIN paper with no phase, homodyne or spectral-covariance measurement in its abstract is very unlikely to contain them.
- *Medium-high* for the exponents in (a). The full text might show RIN against fibre length or gain. That would still be a total-energy quantity, not a shape-mode variance.

## What the paper reports (abstract only)

All quotations are from the abstract, read through the OpenAlex record.

- **Aim.** A passive scheme to reduce the intensity noise of high-power nonlinear fibre amplifiers, using spectral-breathing parabolic evolution with an optimized negative initial chirp.
- **Mechanism, stated qualitatively.** Three causes are given for suppressing the influence of ASE on the amplifier intensity noise: "lower overall pulse chirp", "shorter spectral broadening distance" and the "asymptotic attractive nature of self-similar pulse amplification". No model or equation is described.
- **Measurement.** "Systematic characterizations of the relative intensity noise (RIN)" of a free-running amplifier, "over a series of initial pulse parameters".
- **Dependence on input energy.** The "measured amplifier RIN increases respect to the decreased input pulse energy", "due to the increased amount of ASE noise".
  - The abstract does not say whether output power was held fixed, so it is not known whether lower input energy also meant higher gain.
  - No law (power or otherwise) is given.
- **Dependence on chirp.** With a proper negative initial chirp, the RIN increase is "smaller than with a positive initial chirp".
- **Headline numbers** (the paper's, not a repository run):
  - at 27 W output and 25 dB gain, an optimum chirp parameter of $-0.84$ reduces rms RIN by about 20.5% over 10 Hz–10 MHz;
  - the minimum rms RIN is 0.025% over 1 kHz–5 MHz, with 55 fs transform-limited compressed pulses.

### Journal version and related papers by the same group (abstract only)

- **Opt. Lett. 41, 5286 (2016)**, DOI 10.1364/OL.41.005286. The abstract was read on the Optica page and on OpenAlex.
  - It reports "spectral and temporal breathing" similariton evolution with negative pre-chirp, from simulations as well as experiments.
  - It reports about 31% lower rms RIN, and 0.029% over 1 kHz–5 MHz with 36 fs pulses from a 2 m Yb-fibre amplifier.
  - The stated mechanism changes from the SPIE version: "enhanced tolerances of this scheme to the gain-shaping distortions and pump fluctuations". ASE and attraction are not mentioned in this abstract.
  - The noise effect is therefore attributed to finite gain bandwidth and pump-noise transfer. The cards exclude both.
- **CLEO-PR 2013**, DOI 10.1109/CLEOPR.2013.6600147, abstract only. The origin of the spectral-breathing scheme: negatively chirped pulses "avoid gain-shaping disturbance and accelerate self-similar evolution". There is no noise content.
- **CLEO-PR 2017**, DOI 10.1109/CLEOPR.2017.8118716, and *Int. J. Opt.* 2021, 5514089, DOI 10.1155/2021/5514089. Both abstract only.
  - Both report lower RIN of a self-similar amplifier when it is pumped at 915 nm instead of 976 nm, attributed to gain shaping and pump-diode fluctuations.
  - The 2021 paper is gold open access (CC BY), but the publisher PDF and pages returned HTTP 403 or a Cloudflare challenge. No repository copy was found.
- **Opt. Express 26, 26411 (2018)**, DOI 10.1364/OE.26.026411, abstract only. Self-similar amplification of picosecond seeds; the abstract has no noise content.

## Why the measured RIN neither anticipates nor tests the cards

1. **The observable is the total energy.** RIN integrated over a low Fourier band measures pulse-to-pulse fluctuations of the total power. In the cards' notation this is the $l=0$ block, or $C_{AA}$.
   - Both cards state that $C_{AA}=G+(2n_{sp}-1)(G-1)=2n_{sp}G-(2n_{sp}-1)$ exactly, in output shot-noise units.
   - C-20261008-claude-a-01 states that "the energy noise is unchanged" by the pulse dynamics.
   - Within the cards' model, then, the energy noise cannot depend on launch chirp or pulse shape.
2. **The chirp dependence comes from excluded physics.** A chirp-dependent RIN, such as the reported 20–31% reduction, needs mechanisms outside the cards' assumptions. Candidates are:
   - finite gain bandwidth and gain shaping, which the journal abstract names;
   - gain saturation and pump-noise transfer, which it also names;
   - the intensity noise of the incoherent ASE background, i.e. the ASE–ASE beat that C-20261008-claude-a-02 assumption 2 neglects.

   This is consistent with the gain-flatness bound in the regime of both cards. It is the abstract's own account, not a test.
3. **The input-energy trend is generic.** RIN rising as input energy falls is the direction expected of any linear amplifier: relative ASE-driven energy noise scales as $2n_{sp}/N_0$ at large gain. Gürel et al. (2014) reproduce measured RIN with a linear model in which seed, pump and ASE contributions add, weighted by transfer functions and the ASE power fraction (full text, Eqs. (9)–(10)). That needs no similariton physics.
4. **There is no quantum reference.** The abstracts give no shot-noise level, so the data cannot be placed relative to the quantum-limited quantities of either card.
5. **The shared idea has no shared observable.** The attraction acts on shape modes in C-20261008-claude-a-02. The SPIE abstract invokes it for the total energy, where the cards' model says it has no effect. If the full text gives a quantitative attraction argument, it would refer to a quantity outside both cards. The card should cite the paper as a qualitative experimental precedent and state this distinction. Its novelty statement does not need to change.

## Verdicts, statement by statement

Evidence is from the abstracts (SPIE and *Opt. Lett.*) unless stated otherwise.

**C-20261008-claude-a-02**

- **(a) Shape-mode variances.** Photon-normalized low-order intensity- and phase-shape variables grow with envelopes $G^{1/3}$ and $G^{5/3}$. *Not anticipated.*
  - Only total-power RIN is measured.
  - There is no Legendre, modal or shape decomposition, no phase quantity, and no gain law.
- **(a), interpretive sentence.** The attraction "acts as a phase-sensitive amplifier on every shape mode" and de-amplifies intensity-shape noise by $G^{-2/3}$ relative to linear amplification. *Partly anticipated, qualitatively only, for a different observable.*
  - The SPIE abstract credits the "asymptotic attractive nature of self-similar pulse amplification" with suppressing ASE-driven intensity noise.
  - It gives no rate and no phase-quadrature counterpart. It refers to total energy, which the attraction cannot change in the flat-gain model.
  - The journal version does not repeat the attraction argument.
- **(b) Single-shot spectral covariance.** For the five-component projection, $\mu_2/\mu_1=\Theta(G^{-2/3})$. *Not anticipated.*
  - No spectrally resolved, single-shot or dispersive-Fourier-transform measurement is described.
  - The nearest experiment found is the citing paper (see Antecedents). It measures spectrally sliced RIN in a gain-managed nonlinear amplifier and finds that "the RIN of the full spectrum is lower than that of individual spectral slices". The spectral profile is "U-shaped".
  - That is a different regime, with classical seed and pump noise, and no covariance eigenvalues are reported. It is relevant as the kind of measurement that could test (b).
- **(c) Energy–phase locking of the matched-LO phase,** $1-r^2=\Theta(G^{-2/3})$. *Not anticipated.* No phase, homodyne or Kerr amplitude-to-phase conversion appears.
- **$C_{AA}$, exact.** This is not claimed as new; it is the standard amplifier result (Caves 1982, recorded in the 2026-10-09 prior-art review). The SPIE input-energy trend points in the same direction, which is not specific to the card.

**C-20261019-pi-chatgpt-02**

- **(i) Phase-quadrature growth**, $C_{PP}\sim(32n_{sp}/9)G\Phi_{NL}^2\propto G^{7/3}/\varepsilon_0^2$. *Not anticipated.* No phase noise is reported.
- **(ii) Squeezing with full ASE at short gain**, if and only if $\gamma\int P^2dt/\int P\,dt>n_{sp}g$. *Not anticipated.*
  - There is no quantum-noise or squeezing content. ASE appears only as a classical RIN source.
  - A bounded search beyond this lead found no fibre criterion of this form (see Search log, step 13).
  - Ren et al. (2026), arXiv:2603.11574, read at abstract level, is a conceptual neighbour outside fibres. It proposes a two-mode bosonic amplifier in which Kerr nonlinearity lets the signal gain exceed the noise gain in one quadrature.
  - Neither the criterion nor the fibre setting appears there. The card's general sentence ("phase-insensitive amplifier noise therefore does not forbid squeezing in a nonlinear amplifier") should not be presented as a new principle until a targeted search is done; see Loose ends.
- **(iii) Large gain**, $\lambda_{\min}(C_{\rm LO})=\Theta(G^{1/3})$. *Not anticipated.*

**Both cards: squeezing, or its absence, with ASE.** *Not anticipated.*

## Antecedents through the reference chain

**The paper's six references** (Crossref deposit, all located):

| # | Reference | DOI | Access (this session) | Closer antecedent? |
|---|---|---|---|---|
| 1 | Fermann & Hartl, "Ultrafast fibre lasers", *Nat. Photon.* 7, 868 (2013) | 10.1038/nphoton.2013.280 | not accessed (metadata only; closed, no abstract in OpenAlex) | No evidence either way; a general review |
| 2 | Wang et al., "Self-similar evolution in a short fiber amplifier through nonlinear pulse preshaping", *Opt. Lett.* 38, 296 (2013) | 10.1364/OL.38.000296 | abstract only | No; pulse shaping, no noise |
| 3 | Liu et al., "Pre-chirp managed nonlinear amplification in fibers delivering 100 W, 60 fs pulses", *Opt. Lett.* 40, 151 (2015) | 10.1364/OL.40.000151 | abstract only | No; no noise |
| 4 | Wang, Liu, Hu & Wang, "Amplification and bandwidth recovery of chirped super-Gaussian pulses by use of gain shaping in ytterbium-doped fiber amplifiers", *J. Lightwave Technol.* 32 (2014) | 10.1109/JLT.2014.2360206 | abstract only | No. A spectrally resolved amplifier model with ASE, but no noise statistics in the abstract. Cited as p. 3827; Crossref gives pp. 4429–4437. |
| 5 | Qin et al., "Reduction of timing jitter and intensity noise in normal-dispersion passively mode-locked fiber lasers by narrow band-pass filtering", *Opt. Express* 22, 28276 (2014) | 10.1364/OE.22.028276 | abstract only. Gold OA, but Optica served a bot-check page. | No. The same group's laser-cavity noise work: amplifier-similariton formation by a narrow filter lowers timing jitter and RIN. It is experimental and has no shape-mode analysis in the abstract. |
| 6 | Paschotta et al., "Ytterbium-doped fiber amplifiers", *IEEE J. Quantum Electron.* 33, 1049 (1997) | 10.1109/3.594865 | abstract only | No; amplifier design |

**Journal version, *Opt. Lett.* 41, 5286, 14 references** (Crossref deposit, all with DOIs except one).
- The only similariton-theory items are Fermann et al., *PRL* 84, 6010 (2000), DOI 10.1103/PhysRevLett.84.6010, and Finot et al., *Opt. Express* 14, 3161 (2006), DOI 10.1364/OE.14.003161.
  - Neither was re-read this session. Both are recorded as full text in `docs/review-2026-10-09-gpt-b-similariton-prior-art.md` (A1, A9), with no noise content.
  - The Finot abstract was read here. It shows the spectral recompression of negatively chirped pulses on which the spectral-breathing scheme rests.
- The other references, which are not antecedents by title, are:
  - Carstens 2016, Optica 3, 366, 10.1364/OPTICA.3.000366
  - Jung 2014, JLT 32, 3742, 10.1109/JLT.2014.2312400
  - Lee 2010, Nat. Photon. 4, 716, 10.1038/nphoton.2010.175
  - Chen 2012, OE 20, 28672, 10.1364/OE.20.028672
  - Liu 2015, OL 40, 151, 10.1364/OL.40.000151
  - Deng 2009, OL 34, 3469, 10.1364/OL.34.003469
  - Wang 2013, OL 38, 296, 10.1364/OL.38.000296
  - Wang 2014, JLT 32 (cited without DOI; see 4 above)
  - Schimpf 2009, OE 17, 4997, 10.1364/OE.17.004997
  - Paschotta 1997, 10.1109/3.594865
  - Andresen 2011, OL 36, 707, 10.1364/OL.36.000707
  - Korobko 2016, JOSA B 33, 239, 10.1364/JOSAB.33.000239

  These were read at title level only, through Crossref.

**The one citing paper** (OpenAlex and Semantic Scholar citation lists):
- Haviv, Kozlov, Krüger & Sidorenko, "Noise suppression in gain-managed nonlinear amplifiers", *Opt. Lett.* 51, 1812 (2026), DOI 10.1364/OL.591606. Abstract only; closed.
- Its CLEO 2025 version is DOI 10.1364/CLEO_SI.2025.SS170_3, abstract only.
- The Technion seminar announcement of 2026-02-11 (phys.technion.ac.il, event 3263) was read in full.
- Content:
  - RIN falls with gain and nonlinearity, below the seed's level;
  - the spectral RIN profile is U-shaped, with full-spectrum RIN below the slice RIN;
  - "a rate-equation-based theoretical model" in which the amplifier "acts as a high-pass filter for seed fluctuations".
- This is classical gain-dynamics noise in a gain-managed regime, not a similariton shape-mode or quantum theory. It is not an antecedent for any statement. It is the closest experimental neighbour for (b).
- The noise-model references of that paper were located:
  - Gürel et al., *Appl. Phys. Lett.* 105, 011111 (2014), DOI 10.1063/1.4888298. **Full text**, from the Bilkent repository (green OA). Model section read: a linear transfer-function model with additive seed, pump and ASE terms, and no nonlinearity.
  - Gierschke et al., *Opt. Express* 27, 17041 (2019), DOI 10.1364/OE.27.017041: title only.
  - Tang et al., *Opt. Commun.* 554, 130131 (2024), DOI 10.1016/j.optcom.2023.130131, preprint SSRN 10.2139/ssrn.4566185: not accessed. SSRN returned 403, and there is no abstract in Crossref or OpenAlex. The title, "Nonlinear dynamics of relative intensity noise transfer at fiber amplification and supercontinuum generation", suggests nonlinear energy-noise transfer, not shape-mode statistics. That is not verified.
  - Novak 2002, DOI 10.1109/JLT.2002.1018809; Freeman 1993, DOI 10.1109/68.196012; Tröbs 2005, DOI 10.1364/OPEX.13.002224; Mukhopadhyay 2009, DOI 10.1109/JSTQE.2008.2010261; Smith 2022, DOI 10.1364/OE.450819. Title only: gain-modulation and RIN-measurement papers.

## Source ledger

Access levels: **full text** means the body was read in the stated sections; **abstract only**; **not accessed** means title or metadata only.

| Id | Source | DOI / id | Access | Used for |
|---|---|---|---|---|
| S1 | Wang, Liu, Song & Hu, Proc. SPIE 9893, 98930J (2016), SPIE Photonics Europe, Brussels | 10.1117/12.2227743; OpenAlex W2345226333 | abstract only, via OpenAlex. SPIE page blocked (Incapsula). Crossref holds no abstract but deposits 6 references. | Main lead |
| S2 | Wang, Chen, Qin, Song, Hu & Liu, Opt. Lett. 41, 5286 (2016) | 10.1364/OL.41.005286; PMID 27842114 | abstract only (Optica page and OpenAlex); 14 references via Crossref | Journal version |
| S3 | Wang, Liu, Hu, Chai & Wang, CLEO-PR 2013 | 10.1109/CLEOPR.2013.6600147 | abstract only | Origin of the spectral-breathing scheme |
| S4 | Wang & Qin, CLEO-PR 2017 | 10.1109/CLEOPR.2017.8118716 | abstract only | Follow-up on RIN |
| S5 | Wang, Qin & Wang, Int. J. Opt. 2021, 5514089 | 10.1155/2021/5514089 | abstract only; gold OA, but publisher returned 403 | Follow-up on RIN |
| S6 | Song et al., Opt. Express 26, 26411 (2018) | 10.1364/OE.26.026411 | abstract only | Same group; no noise content |
| S7 | References 1–6 of S1 | see table above | as listed | Reference chain |
| S8 | Haviv, Kozlov, Krüger & Sidorenko, Opt. Lett. 51, 1812 (2026), and CLEO 2025 | 10.1364/OL.591606; 10.1364/CLEO_SI.2025.SS170_3 | abstract only, plus the seminar announcement in full | Only citing work |
| S9 | Gürel et al., Appl. Phys. Lett. 105, 011111 (2014) | 10.1063/1.4888298 | full text (Bilkent repository); model section and Eqs. (9)–(10) | Linear RIN model |
| S10 | Tang et al., Opt. Commun. 554, 130131 (2024) | 10.1016/j.optcom.2023.130131 | not accessed | Possible nonlinear RIN transfer |
| S11 | Ren et al., "Surpassing quantum noise limits with nonlinear amplification" (2026) | arXiv:2603.11574 | abstract only | Neighbour for (ii) |
| S12 | Edelmann, Hua, Şafak & Kärtner, "Nonlinear fiber system for shot-noise limited intensity noise suppression and amplification" (2021) | arXiv:2105.04182; 10.1364/OL.431861 | abstract only | Not an antecedent: polarization-based nonlinear transmission, not a similariton |
| S13 | Minglie Hu's Tianjin University faculty pages (English home page, Chinese publication list pp. 1–10) | faculty.tju.edu.cn/HuMinglie; /070011/zh_CN/lwcg/25164/ | read; no PDFs hosted; S2 is listed, S1 is not | Author pages |
| S14 | Fermann et al., PRL 84, 6010 (2000); Finot et al., Opt. Express 14, 3161 (2006) | 10.1103/PhysRevLett.84.6010; 10.1364/OE.14.003161 | not re-read; full text per the 2026-10-09 review (A1, A9); Finot abstract read | Similariton background |

## Search log

All searches ran on 2026-10-19, 07:08–07:24 EDT. No sign-in was used, no paywall or bot check was bypassed, and no shadow library was used.

1. **Crossref API**, `works/10.1117/12.2227743`. Metadata, 6 deposited references, no abstract, no full-text link. Each reference was resolved by DOI; reference 4, which had no DOI, was found by a bibliographic title query.
2. **doi.org → proceedings.spiedigitallibrary.org → www.spiedigitallibrary.org/redirect/...** WebFetch returned an empty page. A curl GET returned an Incapsula "Request unsuccessful" page.
3. **SPIE canonical article URL** (`/conference-proceedings-of-spie/9893/98930J/...short`). WebFetch returned an empty page.
4. **OpenAlex API**, work record. Abstract obtained; OA status `closed`; `any_repository_has_fulltext: false`; 6 references; 1 citing work.
5. **Unpaywall API.** `is_oa: false`, no OA locations.
6. **Semantic Scholar API.** The first attempt was rate-limited (429); the retry gave `CLOSED`. The abstract is elided by the publisher. One citation (the CLEO 2025 GMNA paper).
7. **OpenAlex author works**, first author A5100321886 (44 works, some merged from other people). Found the journal version S2, the CLEO-PR 2013 and 2017 papers, Int. J. Opt. 2021, Opt. Express 2018 and Acta Phys. Sin. 2013. Abstracts were fetched for each. OpenAlex full-text search for "spectral-breathing parabolic amplification" found nothing that bears on the claims. Its one similar hit, Wang, Chen & Wise, "Partial parabolic amplification in rare-earth-doped optical fiber", arXiv:2603.27554 (2026), was read at abstract level: a regime optimization with no noise content.
8. **Optica** abstract page for S2: abstract read, subscription required. `upcoming_pdf.cfm?id=274303`, the early-posting PDF of S2 that a web search surfaced: curl received a Radware CAPTCHA, and WebFetch received the subscription page. Not pursued further.
9. **Hindawi and Wiley** for S5 (`downloads.hindawi.com` PDF, `hindawi.com` article page, `onlinelibrary.wiley.com/doi/full/`): 403 and a Cloudflare challenge. The DOAJ record links only to the publisher.
10. **SAO/NASA ADS** (`2016SPIE.9893E..0JW`): WebFetch hit a certificate error, and curl received a "Human Verification" page.
11. **Google Scholar**: one query on the exact title phrase, which returned zero results. No further Scholar queries were made.
12. **Web searches:**
    - the exact SPIE title;
    - the exact S2 title with "pdf";
    - Chinese queries for a thesis by 王思佳 (Sijia Wang) on self-similar amplification at Tianjin University, and on 光谱呼吸 / 强度噪声 / 负啁啾 (spectral breathing / intensity noise / negative chirp);
    - an English thesis query;
    - the Minglie Hu group's pages;
    - the citing paper's title;
    - the Tang et al. title.

    No thesis was found in open sources. CNKI, which needs a login, was not tried. The web-search summary for the S2 query attributed the title to the wrong authors and pages ("Tang, Liu, Fu & Wise, OL 41, 2290"); the Optica page and Crossref confirm the correct record.
13. **arXiv API**, eight queries combining the following, plus four on Kerr squeezing with gain or ASE in fibre amplifiers:
    - similariton with noise, squeezing or intensity noise;
    - parabolic with amplifier, intensity noise or squeezing;
    - "gain-managed" with noise;
    - "intensity fluctuation" with "fiber amplifiers";
    - RIN with supercontinuum and amplification.

    Hits were arXiv:2603.08467 (already N11 of the 2026-10-09 review), arXiv:2105.04182 (S12) and arXiv:2603.11574 (S11). There was no fibre squeezing-with-gain criterion. One general web search on squeezing in Kerr fibre amplifiers with spontaneous emission found nothing on point.
14. **Faculty pages** (S13), and the entry page for S2: no attachments.
15. **Bilkent repository** PDF of S9: downloaded and model section read.
16. **SSRN** abstract page for S10: 403.

## What remains

- **Full text of S1 and S2.** The PI can download both through institutional access (URLs in the Summary). The figures could show RIN against fibre length or gain, spectrally resolved RIN, or a stochastic noise simulation.
  - Once read, the verdict for (a) should be rechecked. The other verdicts would change only if the full text contains phase, homodyne or spectral-covariance data, which the abstracts give no sign of.
- **A targeted prior-art search for C-20261019-pi-chatgpt-02 (ii).** Search for squeezing in Kerr media with distributed gain and full spontaneous emission (fibre-amplifier and Raman-amplifier quantum noise, nonlinear-amplifier squeezing) before its general sentence is presented as new.
- **Not done here.** Tang et al. (S10) was not read. Its title is the closest of the citing paper's references to a nonlinear noise-transfer theory.

## Loose ends

- `T-20261019-claude-interactive.14-01` (PI): download S1 and S2 through institutional access and put them where an agent can read them.
- `T-20261019-claude-interactive.14-02` (blocked on -01): read the S1 and S2 full texts and update this review's verdicts.
- `T-20261019-claude-interactive.14-03`: targeted prior-art search for the short-gain squeezing criterion (ii) of C-20261019-pi-chatgpt-02, including Tang et al. (S10).
