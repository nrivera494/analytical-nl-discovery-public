---
id: P-001
title: "Linear response and quantum noise around non-soliton attractors"
status: audited
priority: 1
literature_state: partial
novelty_confidence: medium
target_quantity: "For the amplifier similariton (normal-dispersion NLSE with distributed gain and spontaneous-emission noise): the Gaussian noise channel for energy, phase, timing, frequency and shape fluctuations, with measurable predictions; and a proof, refutation or basin-qualified statement that the similariton is an attractor. The passive parabola is the zero-gain limit."
model: "Normal-dispersion scalar NLSE with Kerr nonlinearity and distributed gain g with its Langevin (spontaneous-emission) noise; linearization about the self-similar parabolic pulse; passive propagation as the g = 0 limit."
oracle_ready: partial
last_audited: 2026-10-02
audited_by: [claude, gpt]
proposed_by: claude-bootstrap
updated_by: claude-interactive
updated_model: claude-opus-5-5
updated_family: claude
claims: [C-0001, C-20261004-claude-a-01, C-20261008-claude-a-01, C-20261008-claude-a-02, C-20261008-gpt-a-01, C-20261008-gpt-a-02, C-20261019-pi-chatgpt-02]
results: [R-0011, R-0014]
---

## Target quantity

**PI direction (2026-10-08).** The passive case is a start, but the minimum for interest is the active case: the amplifier similariton in normally dispersive gain fibre. Two questions.

**A. Noise with gain.** For the NLSE with distributed gain $g$ and its spontaneous-emission noise ($n_{sp}$), predict the full Gaussian channel at a specified distance: input vacuum and ASE propagated to the output. Cover:
- the collective coordinates (energy, phase, timing, frequency), including compressed-pulse timing jitter;
- the shape and chirp fluctuations;
- specified measurements: single-shot spectral intensity covariance (the chirped similariton maps time to frequency), a matched local oscillator, and compressed-pulse timing.

State how the attraction to the similariton changes the noise compared with linear amplification. Frozen eigenmodes, finite-distance singular vectors and covariance eigenmodes are different objects and must not be identified without justification.

**B. Is the similariton an attractor?** Prove or refute that the gain NLSE similariton is an attractor, or replace the statement with one carrying an explicit basin condition (for example a wave-breaking bound) in dimensionless groups. Say which model each statement holds in: the dispersionless (hydrodynamic) limit, the full NLSE, and with which class of inputs. Convergence rates must be stated and tested.

The transient between launch and the asymptotic similariton is in scope, since realistic amplifiers spend much of their length there. The passive results (C-20261004-claude-a-01) are the $g\to0$ limit and remain under verification (T-0002).

**Regime groups.** Gain $gL$; initial semiclassical parameter $\varepsilon_0=1/N_0$ and its decay along the amplifier; $n_{sp}$; similariton bandwidth relative to the gain bandwidth; Raman ($T_R/T_p$); third-order dispersion.

## Signal of hidden simplicity

Published self-similar core and wing solutions supply a structured background. The trapped-Gross–Pitaevskii analogy supplies useful polynomial and boundary-layer problems. It does **not** by itself prove that the evolving optical propagator has the frozen trap's eigenbasis or neutral sector.


**Orchestrator sketch with gain (claude-interactive, in chat with the PI, 2026-10-06). Not checked numerically or by another family; re-derive or refute, do not adopt.** In the dispersionless limit, with $\rho=|A|^2$ and $v=-\beta_2\partial_T\phi$:
$$\rho_z+(\rho v)_T=g\rho,\qquad v_z+vv_T=-\gamma\beta_2\rho_T .$$
- Parabolic intensity with linear chirp, $\bar\rho=\rho_0(1-T^2/T_p^2)$, $\bar v=(\dot T_p/T_p)T$, is an invariant family. The width obeys $\ddot T_p=\tfrac32\gamma\beta_2E_0e^{gz}/T_p^2$, and the asymptote is $T_p\propto e^{gz/3}$, $\rho_0\propto e^{2gz/3}$.
- With $T_p=c\,e^{gz/3}s$ and $\tau=gz$: $s''+\tfrac23s'+\tfrac19s=1/(9s^2)$. The function $V=\tfrac12s'^2+s^2/18+1/(9s)$ obeys $\dot V=-\tfrac23s'^2$, which suggests global convergence of every parabolic launch (any width, chirp, energy).
- About any parabolic background the relative density perturbation separates in Legendre polynomials: $N_l''+2(\dot T_p/T_p)N_l'+l(l+1)(\ddot T_p/2T_p)N_l=0$. The passive Legendre blocks of C-20261004-claude-a-01 would be the $g=0$ case.
- On the asymptote the rates are $\lambda_l=\tfrac g3[-1\pm\sqrt{1-l(l+1)/2}]$: energy ($l=0$) neutral; timing and frequency ($l=1$) a double root at $-g/3$, neutral in absolute terms; every shape mode $l\ge2$ decaying at $g/3$ while oscillating at $\tfrac g3\sqrt{(l(l+1)-2)/2}$.
- Effective semiclassical parameter $\varepsilon_{\rm eff}\propto e^{-2gz/3}$.
- Implied noise statement (unverified): shape modes are amplified phase-sensitively, roughly $G^{1/3}$ in the intensity-shape quadrature and $G^{5/3}$ in the conjugate, against $G=e^{gz}$ for linear amplification.

## Literature state

Access below describes this audit; `full text` means the stated model/results sections were inspected, not that their proofs were independently verified.

- Fermann et al. (2000), [DOI:10.1103/PhysRevLett.84.6010](https://doi.org/10.1103/PhysRevLett.84.6010): asymptotic parabolic amplification with scaling and experimental/numerical support. **Abstract only.** Kruglov et al. (2002), [DOI:10.1364/JOSAB.19.000461](https://doi.org/10.1364/JOSAB.19.000461): also derives low-amplitude wings and amplifier-design conditions; the seed's “existence and attraction only” was incomplete. **Abstract only.** Kruglov & Harvey (2006), [DOI:10.1364/JOSAB.23.002541](https://doi.org/10.1364/JOSAB.23.002541): asymptotically exact parabolic solutions with varying coefficients. **Abstract only.**
- Boscolo, Turitsyn, Novokshenov & Nijhof (2002), [DOI:10.4213/tmf405](https://doi.org/10.4213/tmf405), *Self-Similar Parabolic Optical Solitary Waves*: semiclassical core/tail construction, rather than a quantum-noise theory. **Abstract only** (MathNet record).
- Gallo & Pelinovsky, [arXiv:0806.3516](https://arxiv.org/abs/0806.3516), published as [DOI:10.1016/j.jmaa.2009.02.008](https://doi.org/10.1016/j.jmaa.2009.02.008): **full text**, especially introduction, Theorem 1 and references. The inspected preprint replaces the exact ground state by its Thomas–Fermi profile in spectral problem (1.5), and explicitly declines to establish closeness to the original problem (1.4). The Gegenbauer limit and eigenvalue convergence proved there belong to that model problem. They are not a theorem about an evolving amplifier similariton.
- **Bibliographic correction:** [BT] in that paper is “S. Boscolo and S.K. Turitsyn, private communication (2007).” It is not an identified published article. Its content is **not accessed**; the paper's attribution of a projection cannot establish whether the communication computed a complete spectrum. No DOI/arXiv identifier exists in the reference. The evidence for this correction is arXiv:0806.3516 itself, p. 43.
- Forward follow-up: Gallo & Pelinovsky, [arXiv:0911.3913](https://arxiv.org/abs/0911.3913), [DOI:10.3233/ASY-2011-1034](https://doi.org/10.3233/ASY-2011-1034): **full text**, introduction/main-result statements. Uniform Painlevé-II ground-state asymptotics and the scalar $L_+$ spectrum; the introduction distinguishes that spectrum from the coupled stability problem. This improves the boundary-layer starting point without supplying the optical noise propagator.
- Bale & Boscolo (2010), [DOI:10.1088/2040-8978/12/1/015202](https://doi.org/10.1088/2040-8978/12/1/015202): third-order-dispersion perturbation response. **Abstract only.** The authors' separate conference account, [DOI:10.1117/12.854782](https://doi.org/10.1117/12.854782), was read in **full text** for its perturbation construction; it gives a forced correction and skewness, not a complete fluctuation eigenbasis. Access to the conference account is not access to the journal article.
- Menyuk & Wang (2016), [DOI:10.1515/nanoph-2016-0033](https://doi.org/10.1515/nanoph-2016-0033): **full text**, spectral-noise derivation, Eqs. (25)–(34), and discussion. Gives correlated modal Langevin covariances and timing/power spectra for averaged laser equilibria, using adjoint modes; the worked noise analysis focuses on discrete modes. General noise formulas and their nonorthogonal-mode issue are established. This does not construct the nonautonomous parabolic-pulse propagator. Shinglot & Zweck, [arXiv:2508.01133](https://arxiv.org/abs/2508.01133) and [arXiv:2508.02735](https://arxiv.org/abs/2508.02735): **full text**, theorem statements and Floquet formulation. The former proves an **analytical essential-spectrum characterization**; the latter studies lumped-cavity Floquet stability computationally. “Numerical, not closed form” was an inaccurate blanket description.
- Ashraf, Manjunath & Sugavanam, [arXiv:2603.08467](https://arxiv.org/abs/2603.08467): soliton–similariton **cavity** stability and noise through a numerical Jacobian. **Full text**, model/method inspected. This is important prior art, but a periodic cavity is not single-pass self-similar expansion.
- Kalashnikov & Sorokina, [arXiv:2608.10510](https://arxiv.org/abs/2608.10510): **full text**, Sec. 7.6 and limitations inspected. Its dissipative-soliton/Thomas–Fermi connection is an analogy with stated limits, not a demonstrated equivalence of fluctuation spectra.
- Doerr, Shirasaki & Khatri (1994), [DOI:10.1364/JOSAB.11.000143](https://doi.org/10.1364/JOSAB.11.000143): numerical linearized pulsed Kerr squeezing with dispersion. **Abstract only.** Opatrný, Korolkova & Leuchs (2002), [arXiv:quant-ph/0204131](https://arxiv.org/abs/quant-ph/0204131), [DOI:10.1103/PhysRevA.66.053813](https://doi.org/10.1103/PhysRevA.66.053813): few nonmonochromatic modes can represent Gaussian soliton-pulse correlations. **Abstract only.** Multimode quantum-pulse reduction is therefore established prior art.
- Fedichev & Fischer (2004), [arXiv:cond-mat/0303063](https://arxiv.org/abs/cond-mat/0303063), PRA 69, 033602. **Full text**, Secs. II–IV (claude-a.1; Eqs. (8)–(14) and (22)–(27) re-read by claude-a, 2026-10-04).
  - Linearizes superfluid hydrodynamics about the scaling solution of a condensate in a time-dependent trap.
  - Phase fluctuations separate into static Thomas–Fermi modes times a scalar time equation $\chi_n''+F(\tau_s)\epsilon_n^2\chi_n=0$, solved by WKB.
  - The passive optical parabola is the 1D, $\gamma=2$ free-release special case. The exact separation of the passive propagator is therefore prior art from BEC.
  - Not found there: a closed-form solution, any optical identification, or homodyne covariances.
- Pulsed Kerr squeezing with a local oscillator matched to the pulse:
  - Shirasaki & Haus (1990), [DOI:10.1364/JOSAB.7.000030](https://doi.org/10.1364/JOSAB.7.000030), **abstract only**;
  - Bergman & Haus (1991), [DOI:10.1364/OL.16.000663](https://doi.org/10.1364/OL.16.000663), **abstract only**.
  - The squeezing limit set by the pulse profile is probably published for Gaussian and sech pulses; this is not confirmed. Doerr et al. (1994, above) report numerically that dispersion can enhance it.
- Beyond-Thomas–Fermi corrections to collective modes:
  - Zambelli & Stringari, [arXiv:cond-mat/0107464](https://arxiv.org/abs/cond-mat/0107464), **full text**, Secs. I–III (claude-a.1). In 3D the leading correction scales as (healing length/size)² with a disputed logarithm.
  - No 1D result was found.
- Caves (1982), [DOI:10.1103/PhysRevD.26.1817](https://doi.org/10.1103/PhysRevD.26.1817): quantum added-noise limits depend on phase sensitivity. **Full text**, introduction/theorem summary inspected. The seed's unconditional statement “in an amplifier ... no squeezing” is removed; deterministic gain and a classical SVD alone do not decide the output quantum covariance.

## Sharpest statement of the gap

**Gain case (claude-interactive, 2026-10-06; quick search only).** No analytical single-pass noise theory of the amplifier similariton with spontaneous emission was found. Similariton **laser** noise has been computed numerically (Zweck & Menyuk, [DOI:10.1364/JOSAB.35.001200](https://doi.org/10.1364/JOSAB.35.001200), **abstract only**; Ashraf et al., below). No published decay spectrum or Lyapunov argument for convergence to the similariton was found; reviews describe it as an attractor shown analytically, which rests on Kruglov et al. (2002) and Boscolo et al. (2002), neither read in full here. Searches: "parabolic similariton fiber amplifier linear stability analysis perturbation decay rate asymptotic attractor"; "similariton amplifier quantum noise ASE timing jitter noise properties self-similar parabolic pulse theory"; Kruglov–Peacock–Dudley–Harvey 2002 by title.

**Passive case (earlier audit).** 
In the searches below, no controlled finite-distance core-plus-edge response/noise theory for the **evolving single-pass parabolic pulse** was located. This is a scoped literature finding, not proof of absence. The known forced-TOD response, frozen model spectrum, general laser-noise formulas, and pulsed covariance decompositions must be recovered where applicable.

Searches (2026-10-01): exact titles and authors above; `Gegenbauer similariton spectrum perturbation`; `parabolic pulse quantum noise squeezing adjoint`; Thomas–Fermi/Gross–Pitaevskii collective modes and Painlevé-II edge layers; forward title/author searches from Gallo–Pelinovsky and from Menyuk/Zweck to the later Floquet work. No published [BT] item was located. The unpublished communication remains an access limitation, not positive novelty evidence.

Update (2026-10-04, claude-a).

- At hydrodynamic leading order, the exact separation of the passive propagator is prior art: it is the 1D free-release case of Fedichev & Fischer (2004).
- The open items for the passive case are now:
  - the closed-form finite-distance blocks and their optical meaning;
  - homodyne covariances for specified measurement modes;
  - the edge-layer corrections.
  C-20261004-claude-a-01 proposes the first two and the leading edge term of the covariance. The edge correction to the classical blocks is not derived.
- The amplifier case (gain with Langevin noise) is untouched.
- Searches (2026-10-04): the strings are listed in `log/2026-10-04_claude-a_T-20261004-claude-interactive-05.md`.

## Conjectures

**Current state (2026-10-19, claude-interactive).** The front matter is the record. The amplifier case is no longer untouched:
- **Results:** R-0011 (C-20261008-claude-a-02, shape-mode noise exponents) and R-0014 (C-20261019-pi-chatgpt-02, matched-mode squeezing and phase noise), both promising.
- **Cheap-checks-passed only:** C-20261008-claude-a-01 (collective moments) and C-20261008-gpt-a-01 and -02 (attraction).
- **Manuscript:** `docs/manuscripts/2026-10-19-amplifier-noise-bounds/`.

The entries below are the earlier passive-case history.

- `C-20261004-claude-a-01` (proposed 2026-10-04, status cheap-checks-passed) covers the passive case:
  - a Legendre–Pöschl–Teller block propagator for (density, phase);
  - the matched-local-oscillator covariance, whose squeezing limit set by the pulse profile vanishes at $\zeta^*=4.737$;
  - an edge logarithm in the covariance.
  Verification is T-0002, by a non-Claude family.
- `C-0001` was withdrawn on 2026-10-04 and is superseded by the above. Its singular-vector prediction is not supported, and its amplifier case is open.

## Oracle

**Gain (2026-10-08).** The solver has a deterministic gain profile in `MMGNLSEParameters` and spontaneous-emission kicks in the stochastic backend (`linear_gain_noise`). The gain-noise normalization has not been benchmarked: check it against the analytic amplifier energy noise before any noise run. Also note the open solver issues: the default Raman Langevin spectrum halves the zero-point part (T-20261004-gpt-b-02); the sampled Raman kernel is under-resolved above about 3 fs (T-20261006-claude-interactive-02); the default continuous adjoint can be inaccurate for noise observables (T-20261006-claude-interactive-03).

**Passive.** 
The lab reports a differentiable NLSE solver and Langevin capability; neither was exercised here and the repository evaluator is not yet connected. Passive expansion is the least dependent starting point. Compare a proposed reduced propagator with the full Jacobian and the **noise-weighted covariance**, with independent temporal-window, bandwidth and step convergence. Gain tests additionally need a documented noise convention and a validated gain module. Supply explicit bounds in the effective semiclassical parameter and in neglected Raman, higher-dispersion and gain-bandwidth effects before promoting any claim.

## Lab test

Shaped-local-oscillator homodyne measurements for the passive case; calibrated input energy/frequency modulation and output timing/chirp transfer for the amplifier. Detector bandwidth and optical loss must be part of the prediction.

## Risks and must-reads

- Gain case must-reads: Kruglov et al. (2002) full text (author copies appear to be on UCL Discovery and Southampton ePrints); Boscolo et al. (2002); Kruglov & Harvey (2006); papers on the transition to similaritons. A paper titled "Asymptotic characteristics of parabolic similariton pulses in optical fiber amplifiers" turned up in a search but could not be accessed; identify it and check whether it already gives the convergence rates.
- Finite gain bandwidth eventually ends self-similar growth; state the regime relative to it.


The optical similarity transformation, its nonautonomous terms and boundary conditions need checking before transferring trapped-condensate results. A complete spectrum of the true frozen ground state was not exhaustively audited. Obtain the inaccessible journal texts if their details become load-bearing. No author was contacted about [BT]. PI disposition (2026-10-02): [BT] is treated as unobtainable. It remains a residual novelty risk to name in any claim that arrives at a Gegenbauer projection, but it does not by itself demote the problem.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-01 | claude-bootstrap (claude) | Created; literature_state set to open, novelty_confidence medium | Literature audit, Oct 2026; one must-read not accessed |
| 2026-10-01 | gpt-a (gpt; model unknown) | candidate → audited; open → partial; retained priority 1/medium for the narrowed single-pass target | [BT] private-communication correction; scope of arXiv:0806.3516 and 0911.3913; analytical essential spectrum in arXiv:2508.01133; known covariance and added-noise theory |
| 2026-10-02 | gpt-a (gpt; model unknown) | Recovered general spectral-noise full text; retained scoped gap | DOI:10.1515/nanoph-2016-0033 derives adjoint-mode covariances around laser equilibria; this is a required baseline, not a new method |
| 2026-10-02 | claude-interactive (claude; claude-opus-5-5), on PI instruction | [BT] deliverable closed as unobtainable; status, literature_state, priority and novelty_confidence unchanged | PI decision in chat, 2026-10-02: an unpublished communication of unknown content does not close the gap. Residual risk recorded under Risks and must-reads |
| 2026-10-04 | claude-a (claude; claude-opus-5-5) | No change to status, priority, literature_state or novelty_confidence. C-0001 withdrawn; C-20261004-claude-a-01 added. Fedichev & Fischer (2004) recorded as prior art for the hydrodynamic separation | Derivation and cheap checks: run 2026-10-04-claude-a-c01-cheap-checks. Literature: arXiv:cond-mat/0303063, full text, Secs. II–IV |
| 2026-10-08 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Retargeted to the amplifier similariton: noise with gain, and whether it is an attractor (or a basin-qualified statement). Passive case kept as the $g\to0$ limit. Orchestrator sketch added as unverified. Status, priority, literature_state and novelty_confidence unchanged | PI direction in chat, 2026-10-08; search strings in the gap section |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Claims list completed from the claim files (it omitted several). Recorded GPT 6 Pro's independent verification (run `2026-10-18-pi-chatgpt-independent-verification`): C-20261008-claude-a-02 → sim-verified (narrowed); new claim C-20261019-pi-chatgpt-02. Status, priority and literature_state unchanged | [review](../docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md); task T-20261019-claude-interactive-01 |
| 2026-10-19 | claude-interactive.17 (claude; claude-opus-5-5), task T-20261019-claude-interactive-10, on the PI's promotion decision | Added promising result R-0011 (claim C-20261008-claude-a-02, as narrowed: shape-mode variance envelopes $G^{1/3}$, $G^{5/3}$; five-mode spectral ratio and phase–energy deficit $\Theta(G^{-2/3})$, reduced model). Status, priority, literature_state and novelty_confidence unchanged | [R-0011](../results/promising/R-0011-similariton-shape-noise-exponents/RESULT.md) |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Result R-0014 added (promising; from C-20261019-pi-chatgpt-02). Status unchanged | Task T-20261019-claude-interactive-12 |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5) | Added a current-state note to Conjectures (claims, results R-0011 and R-0014, manuscript); status, priority and literature_state unchanged | Task T-20261019-claude-interactive.20-02 |
