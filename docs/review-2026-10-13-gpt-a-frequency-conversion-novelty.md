---
date: 2026-10-13
agent: gpt-a
model: gpt-6-astra
family: gpt
task: T-20261013-gpt-a-01
orchestrator: claude-interactive
base: "PR #41, task/T-20261013-claude-interactive-01"
scope: "Cross-family novelty audit of the assigned chi3 fibre set"
---

# Frequency-conversion novelty audit: chi3 fibre set

All four cards remain **open, narrowed**. Their proposed starting structures include published results, ambiguous observables or unjustified steps. The defensible gaps are constrained attainability, integrated radiation yield, transported frequency covariance and interacting-field red reach. None is a verified new law.

The status recommendation is **candidate for every card**. Claude literature work is already recorded, but this audit changes substantive parts of every gap. Adding GPT to the review record is not evidence that both families agree with those changes. Task T-20261013-gpt-a-02 requests that agreement; no card is promoted merely because two family names are present. Priorities are unchanged.

## Summary

| Card | Verdict | Closest prior work and access | What remains open in this search | Novelty / impact | Recommended status |
|---|---|---|---|---|---|
| [P-20261012-claude-interactive-01](../problems/P-20261012-claude-interactive-01-conservation-law-ceilings.md) | Open, narrowed | Castelló-Lurbe et al., DOI 10.1364/OE.21.028550; full text. Koch–Tataru, DOI 10.1215/00127094-2018-0033; full text. | A stronger or demonstrably attainable band-energy ceiling under launch-Hamiltonian/bandwidth and finite-length constraints. | 3 / 3 | candidate |
| [P-20261012-claude-interactive.4-01](../problems/P-20261012-claude-interactive.4-01-dispersive-wave-yield-law.md) | Open, narrowed | Roy et al., DOI 10.1103/PhysRevA.79.023824; full text. Modotto et al., DOI 10.1364/JOSAB.32.001676; full text. | Integrated finite-length yield over a bounded input family, with seed leakage and the required additional parameters identified. | 2 / 3 | candidate |
| [P-20261012-claude-interactive.4-02](../problems/P-20261012-claude-interactive.4-02-ssfs-jitter-floor.md) | Open, narrowed | Corney–Drummond, DOI 10.1364/JOSAB.18.000153; full text. Kärtner et al., DOI 10.1364/JOSAB.11.001267; abstract only. | A bound or counterexample for the final frequency variance at fixed shift/efficiency within restricted designs, including covariance transport. | 3 / 3 | candidate |
| [P-20261012-claude-interactive.4-04](../problems/P-20261012-claude-interactive.4-04-blue-band-raman-budget.md) | Open, narrowed | Gorbach–Skryabin, DOI 10.1103/PhysRevA.76.053803; full text. Bonetti et al., DOI 10.1364/JOSAB.377891; full text. | A proven dynamic upper bound on the complementary red moment with radiation backaction and Raman transfer, then its attainability. | 2 / 3 | candidate |

Scores use docs/RANKING_RUBRIC.md. They are reviewer assessments, not measured quantities or result rankings; their provenance is run **2026-10-13-gpt-a-novelty-literature**. Every new numerical premise check is in run **2026-10-13-gpt-a-novelty-premises**. Literature-reported conversion examples are not treated as this project's simulations.

## Method and limits

I read the assigned problem cards and the workflow/rubric/validation instructions, searched independently, checked the cited DOI identities against publisher-deposited Crossref metadata, and checked arXiv identifiers against their records. I did not read the selection memo, proposers' derivation notes, earlier PR discussions or conversation history. No claims or other problem cards were edited.

“Full text” means the paper body was available and the indicated relevant sections were inspected; it does not mean every derivation in the paper was reproduced. “Abstract only” certifies only what the abstract supports. “Not accessed” means the publication was located bibliographically but its scientific assertion was not independently verified from a primary text. Detailed access locations are in [the source ledger](../runs/2026-10-13-gpt-a-novelty-literature/source-ledger.json). A failed direct PDF fetch was sometimes offset by an indexed author copy; that distinction is recorded.

No identified inherited DOI or arXiv identifier was found to point to an unrelated or nonexistent paper. The substantive citation errors are attribution, scope, observables and missing prior work. Vague references without a title or identifier cannot count as verified literature. The original card content is retained in explicitly superseded sections so that erroneous claims are not silently erased.

## P-20261012-claude-interactive-01: conservation-law ceilings

The Hamiltonian in the proposal is already written in optical variables in [Castelló-Lurbe, Andrés and Silvestre (2013); 10.1364/OE.21.028550](https://doi.org/10.1364/OE.21.028550) (**full text**), Eqs. 2 and 19. Its role in spectral broadening is developed by [Castelló-Lurbe, Vermeulen and Silvestre (2016); 10.1364/OE.24.026629](https://doi.org/10.1364/OE.24.026629) (**full text**). The elementary Markov corollary therefore has little novelty by itself. [Diao, Chen and Chang (2021); 10.1364/OE.442348](https://doi.org/10.1364/OE.442348) (**full text**) also optimizes SESS conversion and tuning numerically, using the combined energy of both outer lobes and pulse Strehl quality while varying fiber parameters. [Wang, Chen and Chang (2022); 10.1364/OE.466033](https://doi.org/10.1364/OE.466033) (**full text**) gives approximate peak/width maxima using a fitted lumped-chirp parameter. Neither supplies a certified maximum in one prescribed band.

The original photon interpretation fails for a power envelope. The exact no-shock scalar invariant is $E=\int|A|^2dt$, while physical photon number weights spectral energy by the inverse absolute frequency. [Zheltikov (2018); 10.1103/PhysRevA.98.043833](https://doi.org/10.1103/PhysRevA.98.043833) (**full text**) discusses exactly this distinction. Broadband photon conversion must be studied in a model that conserves that physical quantity.

There is also an input-class gap. Quadratic chirp preserves the Gaussian's energy, intensity duration, peak power and launch centroid but changes its spectral variance and Hamiltonian. Thus even those fixed quantities cannot support an input-independent ceiling expressed solely in the proposed parameters. The algebra and quadrature are in run **2026-10-13-gpt-a-novelty-premises**. Fix a Hamiltonian or spectral-bandwidth budget, initial target-band leakage and a maximum distance before interpreting a supremum as conversion.

The mathematical search found established conserved Sobolev energies in [Koch and Tataru (2018); 10.1215/00127094-2018-0033](https://doi.org/10.1215/00127094-2018-0033) (**full text**) and defocusing long-time asymptotics in [Deift and Zhou (2003); 10.1002/cpa.3034](https://doi.org/10.1002/cpa.3034) (**full text**). Higher invariants are not just Fourier moments; exponential tails need additional analytic regularity or hierarchy bounds. The known asymptotics also carry a logarithmic phase, so a statement about a limiting spectral **intensity** should not be confused with ordinary linear scattering of the full complex field.

**Remaining gap:** a useful improvement on moment bounds, or their dynamical attainability under realizable launch restrictions, in a fixed fiber. A simple optical reparameterization of a known invariant or scattering formula is insufficient.

**Novelty 3/5:** constrained attainability has close optical and mathematical precedents but could still yield a distinct result. **Impact 3/5:** a tight ceiling tied to launch constraints could become a specialist design rule. Follow-up: **T-20261013-gpt-a-04**.

## P-20261012-claude-interactive.4-01: dispersive-wave yield

[Roy, Bhadra and Agrawal (2009), PRA; 10.1103/PhysRevA.79.023824](https://doi.org/10.1103/PhysRevA.79.023824) (**full text**), Eq. 6, already supplies a radiation-peak-power law in soliton order and TOD. Its normalization differs from the proposal by the factorial in the cubic dispersion coefficient. Its peak-power saturation is not a limit on integrated photon yield. The proposed comparison with energy-conversion demonstrations therefore does not establish missing physics.

Compression and recoil are also established mechanisms: [Austin et al. (2006); 10.1364/OE.14.011997](https://doi.org/10.1364/OE.14.011997) (**abstract only**). An explicit perturbative radiation spectrum is given by [Modotto et al. (2015); 10.1364/JOSAB.32.001676](https://doi.org/10.1364/JOSAB.32.001676) (**full text**), and effective soliton-order/compression/length arguments are used for beat inputs by [Webb et al. (2014); 10.1364/OL.39.005850](https://doi.org/10.1364/OL.39.005850) (**full text**). The open portion is narrower than a first $N$–TOD radiation law.

The compression-length normalization is also wrong at leading order. [Zheltikov (2018), SPM theory; 10.1364/OE.26.017571](https://doi.org/10.1364/OE.26.017571) (**full text**), Eq. 6, writes the high-order empirical scale as $0.32(\pi/2)L_D/N$, whereas the proposal uses $0.32L_D/N$. The soliton period is $\pi L_D/2$. This literature-equation check is recorded in run **2026-10-13-gpt-a-novelty-literature**; the full finite-order fit remains unverified.

The cubic phase-matching expansion independently changes the proposed recoil coefficient. For a soliton at $-r$, relative detuning is $3|\beta_2|/\beta_3+3r$ when its nonlinear phase is neglected; the laboratory detuning has $2r$. Run **2026-10-13-gpt-a-novelty-premises** checks the polynomial substitution. This correction alone does not supply a yield bound.

An arbitrary input class can seed the normal band directly. A compressed-sech tail describes an assumed pulse spectrum, not a bound on all subsequent radiation. The zero-dispersion edge is also not the resonant frequency. Fix a launch family, spectral leakage and propagation interval; report integrated energy, spectral peak and physical-photon yield separately. The convention and input-shape restrictions must precede a collapse test.

**Remaining gap:** a finite-distance integrated-yield law or certified bound for that class, with the extra parameters required beyond $N\delta_3$ identified. No theorem optimizing this precise observable was located, but the older perturbative papers still warrant full-text follow-up.

**Novelty 2/5:** the proposed mechanisms and peak scaling are close to existing work; an integrated constrained maximum is the possible addition. **Impact 3/5:** a valid rule could guide specialized radiation sources. Follow-up: **T-20261013-gpt-a-05**.

## P-20261012-claude-interactive.4-02: SSFS frequency jitter

The closest direct result is not only timing jitter. [Corney and Drummond (2001), II; 10.1364/JOSAB.18.000153](https://doi.org/10.1364/JOSAB.18.000153) (**full text**), preprint Eq. 3.15, gives the soliton frequency-coordinate covariance before the timing integral. The dissipative response and Langevin spectrum already share a microscopic construction in [Drummond and Corney (2001), I; 10.1364/JOSAB.18.000139](https://doi.org/10.1364/JOSAB.18.000139) (**full text**). [Kärtner et al. (1994); 10.1364/JOSAB.11.001267](https://doi.org/10.1364/JOSAB.11.001267) (**abstract only**) explicitly combines SSFS with thermal and quantum Raman noise, although its full projected formulas remain unread.

The unresolved step is the passage from local noise injection to the final selected soliton's variance. Covariance transported by the linearized dynamics can contract as well as grow. The toy drift/covariance ODE in run **2026-10-13-gpt-a-novelty-premises** has a fixed local diffusion/drift ratio but a final ratio suppressed exponentially by restoring drift. It shows a missing logical step; it does not establish that the proposed fiber family realizes that suppression. The cavity literature offers a nearby dynamical-noise precedent: [Yang et al. (2021); 10.1038/s41467-021-21658-7](https://doi.org/10.1038/s41467-021-21658-7) (**abstract only**).

The coherent-input energy derivative also depends on the varied family. [Gordon (1986); 10.1364/OL.11.000662](https://doi.org/10.1364/OL.11.000662) (**abstract only**) gives an inverse fourth-power duration law, which yields a fourth-power energy dependence only when the fundamental-soliton relation is maintained while energy changes; it cannot automatically describe amplitude noise at fixed launch duration. Define the estimator and transport the complete covariance instead of assuming independent additive terms.

The claimed fission-efficiency cap is not valid with Raman interactions. [Kormokar, Shamim and Rochette (2023); 10.1364/JOSAB.478975](https://doi.org/10.1364/JOSAB.478975) (**full text**) is the previously missing journal paper and changes the Raman-independent partition. The tuning-efficiency example belongs to [Shamim, Alamgir and Rochette (2023); 10.1109/JLT.2022.3223802](https://doi.org/10.1109/JLT.2022.3223802) (**abstract only**). These are distinct papers. A modern deterministic drift baseline is also available in [Kormokar, Shamim and Rochette (2021); 10.1364/JOSAB.409240](https://doi.org/10.1364/JOSAB.409240) (**full text**); its adiabatic, nearly unchirped ansatz omits emitted radiation and cannot bound the whole interacting field.

**Remaining gap:** prove a positive final-output bound, or construct a physical counterexample, within an explicitly restricted family at fixed shift, length and efficiency. Neither the shared-kernel observation nor a constant-width baseline alone establishes a design-independent law. Critical uncertainty remains until Kärtner's full text is reviewed.

**Novelty 3/5:** a constrained efficiency/shift/final-noise frontier could add to established soliton-noise theory. **Impact 3/5:** a measurable and attainable rule would guide specialist source design. Follow-up: **T-20261013-gpt-a-06**.

## P-20261012-claude-interactive.4-04: blue-band Raman budget

The moment identity requires the blue conditional mean $\bar\Omega_b$, not the band edge $\Omega_b$. Taking the initial photon-weighted mean as the frequency origin, with conserved photon number, total mean shift $-D$ and complementary red mean $-R$,
$$\eta_b\bar\Omega_b-(1-\eta_b)R=-D,\qquad
\eta_b\le (R-D)/(\Omega_b+R)\le R/(\Omega_b+R).$$
This is elementary probability algebra. The numerical identity check and selective-loss counterexample are in run **2026-10-13-gpt-a-novelty-premises**.

The Raman sign can be stated rigorously for a specified baseline. For constant positive $\gamma_0$, standard shock coefficient $1/\omega_0$, passive Raman response, real dispersion, lossless propagation and positive absolute frequencies, the card now gives the signed energy balance and $Q'=0$. Their combination makes the **photon-weighted** mean frequency nonincreasing. Direct generator evaluation verifies the identity in the premise run. [Bonetti et al. (2020); 10.1364/JOSAB.377891](https://doi.org/10.1364/JOSAB.377891) (**full text**) is the missing foundational pcGNLSE reference; [Linale et al. (2020); 10.1364/OL.401096](https://doi.org/10.1364/OL.401096) (**full text**) is a self-steepening measurement application.

The proposed reach substitution is the more serious issue. [Gorbach and Skryabin (2007), PRA; 10.1103/PhysRevA.76.053803](https://doi.org/10.1103/PhysRevA.76.053803) (**full text**), section VI, includes radiation backaction that accelerates the soliton red shift beyond the bare value, and [Skryabin and Gorbach (2010); 10.1103/RevModPhys.82.1287](https://doi.org/10.1103/RevModPhys.82.1287) (**full text**) reviews this regime. Interpulse Raman transfer supplies another failure of a fixed daughter-energy assumption: [Kormokar, Shamim and Rochette (2023); 10.1364/JOSAB.478975](https://doi.org/10.1364/JOSAB.478975) (**full text**). A bare Gordon trajectory is not a general upper reach bound.

Nor does group-velocity matching determine a photon population. The matching applies to trapped components; other blue radiation and leakage need separate treatment. Tapered trapping depends on acceleration matching as well: [Sørensen et al. (2011); 10.1364/OL.36.000816](https://doi.org/10.1364/OL.36.000816) (**abstract only**). Frequency-selective loss changes the surviving distribution and requires a lost-energy/photon ledger. No hard red cutoff follows merely from a region of high loss.

**Remaining gap:** bound the conditional red moment of the entire complement for a specified input class and finite length while allowing these interactions, then test whether the resulting blue ceiling is useful. The current algebra does not establish that such a sharp bound exists.

**Novelty 2/5:** the balance and trapping ingredients are known; a new dynamical red-reach result would supply the novelty. **Impact 3/5:** that result could guide specialist blue-continuum design. Follow-up: **T-20261013-gpt-a-07**.

## Neighbouring communities

The integrable-PDE search supplied [Koch and Tataru (2018); 10.1215/00127094-2018-0033](https://doi.org/10.1215/00127094-2018-0033) (**full text**) and [Deift and Zhou (2003); 10.1002/cpa.3034](https://doi.org/10.1002/cpa.3034) (**full text**). NMR pulse design supplied [Epstein (2004); 10.1016/j.jmr.2003.12.014](https://doi.org/10.1016/j.jmr.2003.12.014) (**abstract only**): trace identities already connect inverse-scattering profiles to an energy optimum, although its RF magnetization objective differs from an optical output spectrum. Molecular optics supplied [Kuzyk (2000); 10.1364/OL.25.001183](https://doi.org/10.1364/OL.25.001183) (**abstract only**); a bound on molecular susceptibility is not a propagation-conversion ceiling at fixed material response.

Photonic inverse design supplied [Lee et al. (2023); arXiv:2312.10640](https://arxiv.org/abs/2312.10640) (**full text**), whose method is particle-swarm optimization, and [Diao, Chen and Chang (2021); 10.1364/OE.442348](https://doi.org/10.1364/OE.442348) (**full text**). They establish earlier optimization work but do not certify a global maximum for these revised fiber problems. Quantum optics supplied the shared reservoir and frequency covariance above. [Tsang (2007); 10.1103/PhysRevA.75.063809](https://doi.org/10.1103/PhysRevA.75.063809) (**full text**) treats pulse position/frequency operators and quantum soliton control but explicitly excludes Raman from its analyzed model; microresonator work includes [Bao et al. (2021); 10.1038/s41567-020-01152-5](https://doi.org/10.1038/s41567-020-01152-5) (**abstract only**) and [Yang et al. (2021); 10.1038/s41467-021-21658-7](https://doi.org/10.1038/s41467-021-21658-7) (**abstract only**), which are cognate driven/dissipative systems. These searches did not locate a source settling the precise narrowed questions. They do not prove absence of prior work.

## Citation corrections and unresolved access

- “Aston” is not an author of the SPM-pattern paper. The authors are Finot, Chaussard and Boscolo; arXiv:1808.04672 (**full text**). The journal DOI is 10.1364/JOSAB.35.003143, confirmed by the publisher.
- DESY record 400022 resolves to Chung et al., DOI 10.1364/OE.26.003684 (**abstract only**). Its negative-GVD example cannot be used as an ANDi limit.
- The compression-length leading coefficient omits the soliton-period factor; compare Zheltikov, DOI 10.1364/OE.26.017571 (**full text**), Eq. 6. The later finite-order fit is still not certified.
- Roy's DOI is correct, but its observable and the claim that it has no analytical law were wrong: DOI 10.1103/PhysRevA.79.023824 (**full text**).
- The cancellation example has red Cherenkov radiation and blue soliton recoil: DOI 10.1126/science.1088516 (**abstract only**). The opposite direction in the proposed argument was unsupported.
- The collision and intermodal examples use different quantities or systems: DOI 10.1364/OL.35.000658 (**abstract only**, numerical radiation peaks) and DOI 10.1364/OE.590355 (**abstract only**, SiN waveguide probe photons).
- The missing fission-efficiency journal paper is Kormokar, Shamim and Rochette, DOI 10.1364/JOSAB.478975 / arXiv:2301.02945 (**full text**). The separate high-efficiency tuning report is Shamim, Alamgir and Rochette, DOI 10.1109/JLT.2022.3223802 (**abstract only**); the vague thesis attribution was not a sufficient source for that number.
- Linale et al., DOI 10.1364/OL.401096 (**full text**), concerns measuring self-steepening and has additional coauthors omitted from the card. Bonetti et al., DOI 10.1364/JOSAB.377891 (**full text**), supplies the foundational Raman model.
- Huang arXiv:2607.05244 exists (**full text**); the issue is overextending its model, not a nonexistent citation.
- Yi et al.'s publisher's note, DOI 10.1364/OL.41.003722 (**full text**), was omitted. The corrected main article, DOI 10.1364/OL.41.003419 (**full text**), assumes large detuning and operation near the maximum existence detuning; its efficiency uses the minimum sustaining pump power at that operating point.
- Unspecified Heidt theses and NLS notes cannot identify a unique publication. Identifiable substitutes have been added; the vague entries are retained only as superseded proposal material.

Task **T-20261013-gpt-a-03** collects the critical remaining full texts: Kärtner 1994; Santhanam–Agrawal 2003; and Roy 2010. Wang 2022, Diao 2021, Kormokar 2021 and the corrected Yi article/notice were subsequently obtained and inspected. Background equations or measurements not checked in full text include the original compression/fission papers, Blow–Wood, Matsuo and Travers 2010. Their identities are located; their specific asserted equations or measurements are not certified here.

No optimized yield, tightness factor, stochastic noise coefficient, physical counterexample to a universal Raman floor, or interacting-field reach theorem was established. The solver's available capabilities were recorded from the proposal, not revalidated. The analytic checks do not change that limitation.

## Source-by-source verification

The following ledger covers each identifiable inherited source and the additions used above. Every DOI was located bibliographically; access levels are conservative and belong to this review. Specific reading scope and retrieval locations are in the versioned JSON ledger. Unidentified references are treated separately above.

| Source and identifier | Access | What was checked |
|---|---|---|
| Chung et al. (2018), [10.1364/OE.26.003684](https://doi.org/10.1364/OE.26.003684) | abstract only | Correct identity for DESY record 400022. SESS in negative GVD before fission; does not establish a normal-dispersion bound. |
| Eisenberg et al. (2024), [arXiv:2410.00889](https://arxiv.org/abs/2410.00889) | abstract only | Argon hollow-core SESS demonstration; supports an application, not a universal efficiency ceiling. |
| Finot, Chaussard and Boscolo (2018), [arXiv:1808.04672](https://arxiv.org/abs/1808.04672) | full text | Corrects the author attribution 'Aston', which is an institution. Interference description predicts spectral patterns; no optimized band-fraction bound. |
| Finot et al. (2008), [10.1364/JOSAB.25.001938](https://doi.org/10.1364/JOSAB.25.001938) | abstract only | Wave-breaking contribution to normally dispersive continuum formation, including gain/loss. The abstract does not verify a universal saturation theorem. |
| Heidt (2010), [10.1364/JOSAB.27.000550](https://doi.org/10.1364/JOSAB.27.000550) | abstract only | Identifiable replacement for the vague Heidt reference: coherent pulse-preserving ANDi generation, not a band-energy ceiling. |
| Castelló-Lurbe, Andrés and Silvestre (2013), [10.1364/OE.21.028550](https://doi.org/10.1364/OE.21.028550) | full text | Equations 2 and 19 give the same dispersion-weighted Hamiltonian invariant; normal-dispersion spectral design already uses it. |
| Castelló-Lurbe, Vermeulen and Silvestre (2016), [10.1364/OE.24.026629](https://doi.org/10.1364/OE.24.026629) | full text | Generalized inverse dispersive and nonlinear lengths sum to a constant. A direct optical precedent for the proposed invariant-based analysis. |
| Wang, Chen and Chang (2022), [10.1364/OE.466033](https://doi.org/10.1364/OE.466033) | full text | Sections 3–4 estimate SPM/GVD spectral peak positions and widths for Gaussian/sech launches using a fitted lumped-chirp parameter. These are approximate spectral-width maxima, not optimized band-energy ceilings. |
| Diao, Chen and Chang (2021), [10.1364/OE.442348](https://doi.org/10.1364/OE.442348) | full text | PSO varies fiber length, mode-field diameter and dispersion for a fixed Gaussian input. The fitness combines both outer-lobe energy fractions with pulse Strehl quality; this is prior optimization, not a global one-band ceiling. |
| Deift and Zhou (2003), [10.1002/cpa.3034](https://doi.org/10.1002/cpa.3034) | full text | Defocusing NLS long-time asymptotics in weighted Sobolev spaces are established, including a logarithmic phase. Rewriting them in optical units alone is not novel. |
| Koch and Tataru (2018), [10.1215/00127094-2018-0033](https://doi.org/10.1215/00127094-2018-0033) | full text | Conserved energies control Sobolev norms. Higher invariants are nonlinear functionals, not conserved ordinary Fourier moments. |
| Zheltikov (2018), [10.1103/PhysRevA.98.043833](https://doi.org/10.1103/PhysRevA.98.043833) | full text | Explicitly distinguishes the NLSE norm from physical photon number and explains the role of the optical shock term. |
| Epstein (2004), [10.1016/j.jmr.2003.12.014](https://doi.org/10.1016/j.jmr.2003.12.014) | abstract only | NMR inverse-scattering trace formulas yield minimum RF pulse energy for a prescribed magnetization profile. Different observable, but close optimization precedent. |
| Kuzyk (2000), [10.1364/OL.25.001183](https://doi.org/10.1364/OL.25.001183) | abstract only | Quantum sum-rule limits constrain molecular third-order susceptibility; they do not solve fixed-material fiber propagation efficiency. |
| Akhmediev and Karlsson (1995), [10.1103/PhysRevA.51.2602](https://doi.org/10.1103/PhysRevA.51.2602) | abstract only | Abstract explicitly promises an analytic amount of radiation, not phase matching alone; full quantitative scope remains to be checked. |
| Elgin, Brabec and Kelly (1995), [10.1016/0030-4018(94)00602-Q](https://doi.org/10.1016/0030-4018(94)00602-Q) | abstract only | Associate-field inverse-scattering perturbation describes radiation growth and structure as well as soliton changes. |
| Erkintalo et al. (2012), [10.1103/PhysRevLett.109.223904](https://doi.org/10.1103/PhysRevLett.109.223904) | abstract only | Cascaded phase matching and nonlinear symmetry breaking in fiber combs; supports the cascaded mixing mechanism. |
| Webb et al. (2013), [10.1364/OL.38.000151](https://doi.org/10.1364/OL.38.000151) | abstract only | Generalized radiation from non-solitonic pulses; a soliton-tail-only yield argument needs a restricted input class. |
| Roy, Bhadra and Agrawal (2009), PRA, [10.1103/PhysRevA.79.023824](https://doi.org/10.1103/PhysRevA.79.023824) | full text | Equations 2 and 6 provide a TOD/soliton-order radiation-peak-power law. The reported saturation concerns peak power, not integrated photon yield. |
| Roy, Bhadra and Agrawal (2009), OL, [10.1364/OL.34.002072](https://doi.org/10.1364/OL.34.002072) | abstract only | Higher dispersion orders change the number and location of radiation peaks; no universal integrated-yield statement in the abstract. |
| Roy et al. (2010), [10.1016/j.optcom.2010.04.003](https://doi.org/10.1016/j.optcom.2010.04.003) | abstract only | Dispersion-profile effects on radiation emission; a direct precursor that must be read fully before claiming an optimized law. |
| Webb et al. (2014), [10.1364/OL.39.005850](https://doi.org/10.1364/OL.39.005850) | full text | Effective soliton order, compression and finite fiber length explain efficiency trends for a dual-frequency beat input. |
| Austin et al. (2006), [10.1364/OE.14.011997](https://doi.org/10.1364/OE.14.011997) | abstract only | Compression-window emission and recoil-induced blue shift are already identified; they are not missing mechanisms. |
| Chang, Chen and Kärtner (2010), [10.1364/OL.35.002361](https://doi.org/10.1364/OL.35.002361) | abstract only | Efficient visible Cherenkov conversion is a source demonstration; its energy efficiency is not Roy's peak-power observable. |
| Chang, Chen and Kärtner (2011), [10.1364/OE.19.006635](https://doi.org/10.1364/OE.19.006635) | abstract only | Few-cycle Cherenkov conversion study; broadband/shock physics limits comparison with the narrowband TOD model. |
| Modotto et al. (2015), [10.1364/JOSAB.32.001676](https://doi.org/10.1364/JOSAB.32.001676) | full text | Contains an analytical perturbative radiation spectrum, Eq. 4, and an energy-conversion experiment in a multi-zero-dispersion fiber. |
| Erkintalo, Genty and Dudley (2010), [10.1364/OL.35.000658](https://doi.org/10.1364/OL.35.000658) | abstract only | Numerical collision-enhanced radiation peak power; the card's description as measured integrated yield is unsupported. |
| Timmerkamp and Fallnich (2026), [10.1364/OE.590355](https://doi.org/10.1364/OE.590355) | abstract only | Integrated silicon-nitride waveguide, orthogonally polarized modes, and probe-photon conversion; not scalar-fiber pump conversion. |
| Travers et al. (2019), [10.1038/s41566-019-0416-4](https://doi.org/10.1038/s41566-019-0416-4) | full text | Gas-capillary source and conversion measurements; ionization and full dispersion distinguish it from the pure TOD model. |
| Brahms, Belli and Travers (2020), PRR, [10.1103/PhysRevResearch.2.043037](https://doi.org/10.1103/PhysRevResearch.2.043037) | abstract only | High-energy capillary compression and tunable radiation; an achievable operating point, not a ceiling. |
| Brahms, Belli and Travers (2020), OL, [10.1364/OL.398343](https://doi.org/10.1364/OL.398343) | abstract only | Pressure-gradient scaling and radiation-pulse duration; not a band-yield upper bound. |
| Köttig et al. (2017), [10.1364/OPTICA.4.001272](https://doi.org/10.1364/OPTICA.4.001272) | abstract only | High repetition-rate deep-UV source using optimized gas-filled fiber stages. |
| Mak et al. (2013), [10.1364/OE.21.010942](https://doi.org/10.1364/OE.21.010942) | abstract only | Gas-filled hollow-core tunable radiation and pressure-gradient experiments. |
| Joly et al. (2011), [10.1103/PhysRevLett.106.203901](https://doi.org/10.1103/PhysRevLett.106.203901) | abstract only | Argon-filled fiber deep-UV conversion experiment; no Raman and pressure-tunable dispersion. |
| Kodama and Hasegawa (1987), [10.1109/JQE.1987.1073392](https://doi.org/10.1109/JQE.1987.1073392) | not accessed | Correct bibliographic record. The specific fission-partition attribution was not checked in its full text; the baseline is reproduced in Kormokar 2023. |
| Mollenauer et al. (1983), [10.1364/OL.8.000289](https://doi.org/10.1364/OL.8.000289) | full text | Scanned three-page reprint confirms first-compression position is measured in soliton periods, and plots compressed width and central-spike energy. The later fit constants are not independently recovered from this paper. |
| Dudley, Genty and Coen (2006), [10.1103/RevModPhys.78.1135](https://doi.org/10.1103/RevModPhys.78.1135) | abstract only | Broad supercontinuum review; no absence claim is inferred from its abstract. |
| Skryabin et al. (2003), [10.1126/science.1088516](https://doi.org/10.1126/science.1088516) | abstract only | Negative dispersion slope: red Cherenkov radiation recoils the soliton toward blue and cancels Raman shift. The proposal reversed the relevant radiation direction. |
| Corney and Drummond (2001), II, [10.1364/JOSAB.18.000153](https://doi.org/10.1364/JOSAB.18.000153) | full text | Direct frequency-coordinate covariance precedes the timing-jitter formula (preprint Eq. 3.15). Analytic treatment neglects deterministic SSFS. |
| Drummond and Corney (2001), I, [10.1364/JOSAB.18.000139](https://doi.org/10.1364/JOSAB.18.000139) | full text | The dissipative Raman susceptibility and thermal/zero-point Langevin spectrum already share a reservoir model (preprint Eqs. 6.11 and 6.16). |
| Kärtner et al. (1994), [10.1364/JOSAB.11.001267](https://doi.org/10.1364/JOSAB.11.001267) | abstract only | Already models SSFS, measured Raman gain and quantum/thermal phonon noise together. The precise projected ratio is unverified without the full text. |
| Haus and Lai (1990), [10.1364/JOSAB.7.000386](https://doi.org/10.1364/JOSAB.7.000386) | abstract only | Linearized quantum soliton theory includes photon-number, phase, time and frequency uncertainties. |
| Gordon (1986), [10.1364/OL.11.000662](https://doi.org/10.1364/OL.11.000662) | abstract only | Classical fundamental-soliton self-frequency-shift law. Its energy derivative depends on how width and energy are varied. |
| Santhanam and Agrawal (2003), [10.1016/S0030-4018(03)01561-X](https://doi.org/10.1016/S0030-4018(03)01561-X) | abstract only | General moment-method treatment and broadening-induced shift saturation; no unrestricted reach or quantum-noise floor follows from the abstract. |
| Santhanam and Agrawal (2002), [10.1109/JSTQE.2002.1016367](https://doi.org/10.1109/JSTQE.2002.1016367) | abstract only | Amplifier-noise fluctuations transferred through Raman dynamics in dispersion-managed communication systems; not the intrinsic Raman-reservoir floor. |
| Zhou et al. (2015), [10.1364/OL.40.005105](https://doi.org/10.1364/OL.40.005105) | abstract only | Pump intensity noise transfers through center-wavelength changes to timing jitter; reducing accumulated dispersion reduces timing jitter. |
| Matsuo et al. (2000), [10.1007/s10043-000-0317-1](https://doi.org/10.1007/s10043-000-0317-1) | not accessed | Title, authors and DOI match. The original card's quantitative timing/intensity values were not independently checked from a primary text. |
| Erkintalo, Genty and Dudley (2009), [10.1364/OL.34.002468](https://doi.org/10.1364/OL.34.002468) | abstract only | Rogue-wave-like filtered-intensity statistics; not a direct derivation of soliton centroid quantum variance. |
| Kormokar and Rochette (2022), [10.1364/NP.2022.NpTu4F.7](https://doi.org/10.1364/NP.2022.NpTu4F.7) | abstract only | Conference abstract includes interpulse Raman gain in conversion efficiency. A journal version is now located. |
| Kormokar, Shamim and Rochette (2023), [10.1364/JOSAB.478975](https://doi.org/10.1364/JOSAB.478975) | full text | Journal version, arXiv:2301.02945. Interpulse Raman transfer enhances the leading soliton beyond the Raman-independent inverse-scattering energy partition. |
| Chen et al. (2022), [10.1364/OL.445499](https://doi.org/10.1364/OL.445499) | abstract only | Hydrogen hollow-core SSFS conversion; a distinct Raman reservoir from silica. |
| Yi et al. (2016), [10.1364/OL.41.003419](https://doi.org/10.1364/OL.41.003419) | full text | Corrected author copy: Lagrangian shift and efficiency laws for driven cavity solitons, with large detuning and operation near the maximum existence detuning. Efficiency is relative to the minimum pump power at that operating point, not a universal conversion bound. |
| Yi et al. (2016), publisher’s note, [10.1364/OL.41.003722](https://doi.org/10.1364/OL.41.003722) | full text | Publisher note identifies omitted text above Eq. 1 and below Eq. 15; the corrected online article is dated 19 July 2016. The corresponding operating-point assumptions were checked in the corrected author copy. |
| Bao et al. (2021), [10.1038/s41567-020-01152-5](https://doi.org/10.1038/s41567-020-01152-5) | abstract only | Quantum timing diffusion of dissipative microcavity solitons; relevant noise precedent but a different dynamical system. |
| Blow and Wood (1989), [10.1109/3.40655](https://doi.org/10.1109/3.40655) | not accessed | Correct bibliographic identity. The original wording 'energy loss by the Raman term' needs the field normalization and shock term specified; see Bonetti 2020. |
| Linale et al. (2020), [10.1364/OL.401096](https://doi.org/10.1364/OL.401096) | full text | Actual title is Measuring self-steepening with the photon-conserving nonlinear Schrödinger equation. It is an application of the model, not its founding Raman derivation. |
| Bonetti et al. (2020), [10.1364/JOSAB.377891](https://doi.org/10.1364/JOSAB.377891) | full text | Foundational photon-conserving generalized NLSE for frequency-dependent nonlinearities, with Raman. Standard GNLSE photon conservation requires the appropriate frequency dependence. |
| Huang et al. (2026), [arXiv:2607.05244](https://arxiv.org/abs/2607.05244) | full text | The preprint exists. It derives a time-domain expansion and soliton moment equations from pcGNLSE; its conclusions cannot silently cover arbitrary lossy spectra. |
| Gorbach and Skryabin (2007), NP, [10.1038/nphoton.2007.202](https://doi.org/10.1038/nphoton.2007.202) | abstract only | Gravity-like radiation trapping and supercontinuum extension; supports mechanism, not a universal band-fraction ceiling. |
| Gorbach and Skryabin (2007), PRA, [10.1103/PhysRevA.76.053803](https://doi.org/10.1103/PhysRevA.76.053803) | full text | Section VI and Eqs. 28–30 include radiation backaction that accelerates the soliton beyond its bare Raman rate; that rate is not an upper bound. |
| Skryabin and Gorbach (2010), [10.1103/RevModPhys.82.1287](https://doi.org/10.1103/RevModPhys.82.1287) | full text | Section VI reviews trapping, accelerated red shift, leakage and interactions. Blue-edge matching does not determine the blue photon fraction. |
| Stone and Knight (2008), [10.1364/OE.16.002670](https://doi.org/10.1364/OE.16.002670) | abstract only | Uniform-fiber visible supercontinuum source; the exact group-velocity edge argument was not checked in the full text. |
| Sørensen et al. (2011), [10.1364/OL.36.000816](https://doi.org/10.1364/OL.36.000816) | abstract only | Group-acceleration matching controls trapped blue power in tapers; group-velocity equality alone is insufficient. |
| Travers (2010), [10.1088/2040-8978/12/11/113001](https://doi.org/10.1088/2040-8978/12/11/113001) | not accessed | Correct title and DOI for the blue-extension review. No mathematical claim is certified from metadata alone. |
| Wetzel et al. (2018), [10.1038/s41467-018-07141-w](https://doi.org/10.1038/s41467-018-07141-w) | abstract only | Adaptive temporal pulse splitting experimentally customizes supercontinuum properties; no certified ceiling. |
| Michaeli and Bahabad (2018), [10.1088/2040-8986/aab59c](https://doi.org/10.1088/2040-8986/aab59c) | abstract only | Genetic-algorithm control of shaped supercontinuum spectra. |
| Hary et al. (2023), [10.1364/OL.492064](https://doi.org/10.1364/OL.492064) | abstract only | Genetic optimization of narrow spectral channels; enhancement relative to a reference is not absolute conversion efficiency. |
| Hary et al. (2025), [10.1038/s41598-024-84567-x](https://doi.org/10.1038/s41598-024-84567-x) | abstract only | Comparison of genetic, particle-swarm and annealing optimization. GPT independently read the abstract; the retained Claude proposal reports full-text access. |
| Lee et al. (2023), [arXiv:2312.10640](https://arxiv.org/abs/2312.10640) | full text | Free-form SiN waveguides optimized for power, flatness and coherence using particle-swarm optimization; this cited work is not an adjoint-gradient method. |
| Shamim, Alamgir and Rochette (2023), [10.1109/JLT.2022.3223802](https://doi.org/10.1109/JLT.2022.3223802) | abstract only | The source of the quoted high-efficiency tuning range. Distinct from the Kormokar fission-efficiency journal paper; pulse compression preserves soliton order. |
| Kormokar, Shamim and Rochette (2021), [10.1364/JOSAB.409240](https://doi.org/10.1364/JOSAB.409240) | full text | Adiabatic, nearly unchirped fundamental-soliton drift including TOD, shock and loss; Sections 2.3–3 derive the reduced law. Section 4.2.2 notes that the ansatz omits dispersive radiation. Not an all-field reach bound or a noise theory. |
| Yang et al. (2021), [10.1038/s41467-021-21658-7](https://doi.org/10.1038/s41467-021-21658-7) | abstract only | Cavity quiet-point noise suppression balances Raman shift and dispersive-wave recoil, with added thermal noise. Relevant precedent for including the dynamical noise transfer. |
| Tsang (2007), [10.1103/PhysRevA.75.063809](https://doi.org/10.1103/PhysRevA.75.063809) | full text | Pulse position/frequency operators, optical-loss noise and adiabatic quantum soliton control. Raman is explicitly outside the analyzed model; this does not settle an SSFS noise floor. |
| Zheltikov (2018), SPM theory, [10.1364/OE.26.017571](https://doi.org/10.1364/OE.26.017571) | full text | Approximate short-distance SPM/GVD broadening and high-order compression-length scaling. Section 3 Eq. 6 includes the soliton-period factor omitted from the proposal’s leading compression-length coefficient. |

## Search log

Search date: 2026-10-13. Live search used DOI/title verification plus concept searches in ultrafast fiber optics, integrable PDEs, NMR, quantum optics, molecular response limits, photonic inverse design and microresonators. Publisher/author papers are the scientific sources; aggregators were used only to locate them. Full query/result records, bibliographic metadata and reachable PDFs are outside git at the raw location recorded in run **2026-10-13-gpt-a-novelty-literature**.

- "Photon-conserving Raman soliton attractors"
- "2607.05244"
- "soliton" "frequency" "fluctuation-dissipation" Raman
- "dispersive wave" "conversion efficiency" analytical Akhmediev Karlsson Elgin
- "defocusing" "nonlinear Schrödinger" "spectral" "upper bound"
- "self phase modulation" "spectral selection" "3684"
- "Raman" "frequency jitter" "diffusion" soliton
- "023824" Roy Bhadra Agrawal pdf
- "normal dispersion" "spectral broadening" "conservation" Hamiltonian
- "On the frequency spanning of SPM-enabled spectral broadening"
- "defocusing" "asymptotic spectrum" nonlinear Schrödinger
- "Raman" soliton "drift" "diffusion" frequency
- "Towards an analytical framework for tailoring supercontinuum generation"
- "soliton" "Raman" "fluctuation dissipation" frequency shift noise
- "Kormokar" "Rochette" "conversion efficiency" Raman
- "Elgin" "Brabec" "Kelly" "1995" soliton
- "10.1364/OL.34.002072"
- "10.1016/j.optcom.2010.04.003"
- "10.1364/OE.590355"
- "10.1364/OE.14.011997"
- "10.1364/OL.8.000289"
- "10.1016/0030-4018(94)00602-Q"
- "10.1103/PhysRevLett.109.223904"
- "10.1364/OL.38.000151"
- "soliton" "frequency jitter" "Raman" "limit"
- "Raman" "Einstein relation" soliton
- "soliton" "drift diffusion" Raman quantum
- "Raman" "thermodynamic uncertainty"
- "10.1364/JOSAB.11.001267"
- "10.1364/JOSAB.7.000386"
- "10.1364/OL.11.000662"
- "10.1016/S0030-4018(03)01561-X"
- "10.1109/JSTQE.2002.1016367"
- "10.1364/OL.40.005105"
- "10.1007/s10043-000-0317-1"
- "10.1364/OL.34.002468"
- "Santhanam" "Agrawal" "632" "2002"
- "10.1109/JSTQE.2002.1016367"
- "Matsuo" "Nishizawa" "317" "2000"
- "Raman noise and soliton squeezing" pdf Kärtner
- "10.1364/OL.35.002361"
- "10.1364/OE.19.006635"
- "10.1364/JOSAB.32.001676"
- "10.1364/OL.35.000658"
- "10.1109/3.40655"
- "10.1364/OL.401096"
- "10.1364/OE.16.002670"
- "10.1364/OL.36.000816"
- "10.1126/science.1088516"
- "10.1364/OL.445499"
- "10.1364/OL.41.003419"
- "10.1038/s41567-020-01152-5"
- defocusing nonlinear Schrodinger long time asymptotics reflection coefficient logarithm 1 r squared Deift Zhou
- nonlinear Schrodinger conserved energies Sobolev norms Koch Tataru integrable
- NMR inverse scattering pulse design trace formula energy bandwidth bounds
- nonlinear frequency conversion efficiency upper bounds conservation law photon energy photonic inverse design
- "Raman noise and soliton squeezing" "pdf" site:mit.edu
- "Long-time asymptotics" "Deift" "Zhou" "2003" arxiv
- "spectral broadening" "Hamiltonian" "Castelló"
- "upper bounds" "nonlinear frequency conversion" Miller
- "Raman" "soliton" "frequency fluctuations"
- "self-frequency shift" "quantum noise" diffusion
- "Raman" "frequency variance" soliton
- "soliton" "Raman" "frequency noise" "bound"
- "10.1103/PhysRevResearch.2.043037"
- "10.1364/OPTICA.4.001272"
- "10.1364/OE.21.010942"
- "10.1103/PhysRevLett.106.203901"
- "10.1364/OL.34.002072" abstract
- "10.1016/j.optcom.2010.04.003" abstract
- "10.1364/OL.8.000289" "0.32"
- "10.1109/JQE.1987.1073392"
- "Gorbach" "053803" arxiv
- "Photon-conserving nonlinear Schrödinger equation" Bonetti 2020
- "Raman noise and soliton squeezing" filetype:pdf
- "Raman-induced spectral shifts in optical fibers" pdf
- "10.1364/JOSAB.7.000386"
- "10.1364/JOSAB.25.001938"
- "10.1364/OE.26.003684"
- "10.1016/0030-4018(94)00602-Q"
- "Dispersive waves emitted by solitons perturbed" filetype:pdf
- "Raman noise and soliton squeezing" Kärtner 1994 full text
- "On the frequency spanning of SPM-enabled spectral broadening" pdf
- "Photon-conserving generalized nonlinear Schrödinger" "377891"
- "Dispersion-to-spectrum mapping in nonlinear fibers"
- "particle swarm optimization of SPM-enabled spectral selection"
- "Cherenkov radiation emitted by solitons" "pdf"
- "Minimum energy pulse synthesis" Epstein DOI
- "Particle swarm optimization" "39766" DOI
- "Photon-conserving generalized nonlinear Schrödinger equation for frequency-dependent nonlinearities" DOI
- "Dispersion-to-spectrum mapping" "pdf" uv
- "On the frequency spanning" "466033"
- "nonlinear optical" "conversion efficiency" "bounds" Miller
- "molecular" "nonlinear" "fundamental limits" Kuzyk
- "supercontinuum" "adjoint" optimization spectral
- "inverse design" "dispersive wave" efficiency analytical
- normal dispersion nonlinear Schrodinger sech initial pulse asymptotic spectrum inverse scattering
- Hamiltonian upper bound spectral energy normal dispersion nonlinear fiber conversion
- Raman soliton frequency jitter fundamental limit dispersion engineering stabilization
- fluctuation dissipation soliton self frequency shift variance relation
- "10.1364/OE.442348"
- "10.1364/OE.21.028550"
- "Raman noise and soliton squeezing" "self-frequency"
- "Raman noise and soliton squeezing" site:pubmed.ncbi.nlm.nih.gov
- "Pulse preserving flat-top supercontinuum generation"
- "10.1007/s10043-000-0317-1" site:link.springer.com
- "10.1109/3.40655" abstract
- "10.1109/JQE.1987.1073392" abstract
- "Theory and measurement of the soliton self-frequency shift and efficiency"
- "Blue extension of optical fibre supercontinuum generation"
- "Looking at a soliton through the prism" arxiv
- "Measuring self-steepening" "Linale" authors
- Kormokar McGill thesis 2025 Raman soliton conversion efficiency
- "10.1364/OL.41.003722" erratum
- "Aston" "Simple guidelines to predict self-phase"
- "10.1364/OL.25.001183"
- "High-order analytical formulation of soliton self-frequency shift"
- "Dispersive-wave induced noise limits in miniature soliton microwave sources" arxiv
- "nonlinear optical" "bounds" "frequency conversion" Miller susceptibility
- "Raman-induced spectral shifts" "413" pdf -site:researchgate.net
- "Santhanam" "paper_2003_05"
- "Dispersion-to-spectrum mapping" site:roderic.uv.es
- "On the frequency spanning" pdf -site:researchgate.net -site:openalex.org
- "Raman noise and soliton squeezing" site:mit.edu
- "Raman noise and soliton squeezing" site:desy.de
- "Raman noise and soliton squeezing" "1267" pdf -site:researchgate.net
- "Kärtner" "Dougherty" "1994" pdf
- "Raman noise and soliton squeezing" filetype:pdf
- "Kaertner" "Dougherty" "Haus" "Ippen" "1267"
- "Raman noise and soliton squeezing" "full"
- "Raman-induced spectral shifts" Santhanam Agrawal pdf
- "Raman noise and soliton squeezing" Kärtner repository
- "Raman noise and soliton squeezing" "pdf" -site:researchgate.net -site:opg.optica.org
- "Raman-induced spectral shifts" "Santhanam" -site:scispace.com -site:researchgate.net
- "Analytical soliton self-frequency shift" Kormokar
- "Raman noise and soliton squeezing" site:dspace.mit.edu
- "Raman noise and soliton squeezing" site:pubdb.desy.de
- "High-order analytical formulation of soliton self-frequency shift" pdf
- "Raman-induced spectral shifts" "moment" site:researchgate.net/publication
- "Raman noise and soliton squeezing" "pdf" Kärtner 1994 -site:researchgate.net -site:opg.optica.org -site:scispace.com
- "Experimental observations of picosecond pulse narrowing and solitons in optical fibers" pdf
- "On the frequency spanning of SPM-enabled spectral broadening" pdf
- "SPM-enabled spectral selection" "Diao" pdf
- "On the frequency spanning of SPM-enabled spectral broadening" "ResearchGate"
- "10.1364/OL.8.000289" pdf
- "10.1016/j.optcom.2010.04.003" pdf
- "Raman-induced spectral shifts" "pdf" "Agrawal" -site:researchgate.net -site:scispace.com -site:labsites.rochester.edu
- "Role of dispersion profile in controlling emission" "pdf" -site:researchgate.net -site:labsites.rochester.edu
- "Raman noise and soliton squeezing" "repository"
- "Mollenauer" "0.32" "1.1" "1983"
- "Mollenauer" "0.32/N"
- "Mollenauer" "1.1/N"
- "Extreme picosecond pulse narrowing" filetype:pdf
- "Raman noise and soliton squeezing" "1267-1276" pdf
- "Analytical insights into self-phase modulation: beyond the basic theory"
- "Raman-induced spectral shifts" "paper_2003_05"
- "Extreme picosecond" "0.32"
- "soliton" "0.32/N" "z0"

## Follow-up tasks

| Task | Purpose |
|---|---|
| T-20261013-gpt-a-02 | Claude concurrence or disagreement with the narrowed gaps; needed before audited status. |
| T-20261013-gpt-a-03 | Critical full texts and remaining source-equation checks. |
| T-20261013-gpt-a-04 | Define the Kerr admissible class and identify a nontrivial attainability target. |
| T-20261013-gpt-a-05 | Integrated finite-length dispersive-wave yield beyond published peak-power laws. |
| T-20261013-gpt-a-06 | Raman frequency covariance with deterministic transport and bounded profile freedom. |
| T-20261013-gpt-a-07 | Interacting-field red reach and an explicit treatment of loss. |
