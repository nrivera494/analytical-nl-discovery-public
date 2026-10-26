---
date: 2026-10-12
agent: claude-interactive.4
model: claude-fable-5-1
family: claude
task: T-20261012-claude-interactive.4-01
duration_min: 45
---

## Did

- Answered the PI's 2026-10-12 request for problem cards on limits to nonlinear frequency-conversion efficiency, in the χ(3) fibre and guided-wave lane (four-wave mixing and Bragg-scattering translation, soliton self-frequency shift, dispersive waves, supercontinuum band energy, intermodal and GRIN conversion, fibre harmonics, noise-limited conversion).
- Brainstormed twelve candidate bounds, then ran four foreground literature helpers (claude-interactive.4.1 to .4.4, about 12 minutes each; web search, arXiv and publisher pages, Crossref) on the four strongest clusters, and read the Corney & Drummond Raman-jitter paper (arXiv:quant-ph/9912096) and three abstracts myself.
- Resolved every DOI cited in the cards and the memo through the Crossref API (84 DOIs, all found).
- Wrote five draft cards and a ranked memo under `docs/proposals/2026-10-12-frequency-conversion/claude-interactive.4/`, kept out of `problems/` pending the orchestrator's selection.

## Found

- **Dispersive-wave yield (card 01):** the literature has a perturbative emission rate for a lone soliton, a numerical saturation "typically below 10%" in the pure third-order-dispersion model (Roy, Bhadra & Agrawal PRA 79, 023824 (2009), abstract verified on the publisher page after the first commit), and measured yields from 0.5% (vacuum ultraviolet, hollow core) to above 40% and 50% (few-cycle pump; multi-zero-dispersion fibre), but no bound, no scaling law and no shape optimization. Two structural arguments (compressed-spectrum tail at the fission point; recoil switch-off) both give laws in the single group $N\delta_3$. Open, ranked first.
- **SSFS jitter (card 02):** Corney & Drummond (JOSA B 18, 153 (2001), full text) give the Raman-reservoir timing jitter $\langle\Delta\tau^2\rangle=2\mathcal I(t_0)\zeta^3/(3\bar n)$ and state that they neglect the self-frequency shift; no drift–diffusion (fluctuation–dissipation) ratio, no minimization over design, no efficiency–shift–jitter frontier was found. Partially open.
- **Bragg-scattering Raman noise (card 03):** Korsgaard, Koefoed & Rottwitt (PRA 110, 033508 (2024), full text) and Friis, Mejling & Rottwitt (OE 25, 7324 (2017), full text) already give the noise and efficiency scalings for a fixed pump configuration, so the fixed-configuration frontier is a corollary; only the envelope over pump asymmetry, detuning and polarization, the spontaneous-four-wave-mixing crossover and the pulsed per-mode statement are open. Low novelty, stated on the card.
- **Blue-band budget (card 04):** no bound on blue-band supercontinuum yield exists; the monotone Raman red-shift is asserted for specific models (abstracts) but not proved for arbitrary fields; shaping papers give enhancement factors only. Open but overlapping the orchestrator's conservation-law lane.
- **GRIN GPI ceiling (card 05):** linear Floquet theory and the reduced periodic-coefficient model exist. After the first commit I read Mei et al. (arXiv:2608.13288, 2026) in full: their pump-depleted three-wave model gives $u_{\max}=1-|D_h|/2$ in the normalized residual mismatch $D_h$, with SPM/XPM frozen at the input power, no walk-off and no power-dependent Gouy phase, for gas-filled multipass cells; they state GRIN self-imaging is a different mechanism. The formula transfers to the reduced fibre model unchanged, so card 05's gap was narrowed to the depletion-dependent mismatch, walk-off and order competition, and its novelty score lowered to 1.
- Dropped as solved: fibre third-harmonic generation; depleted continuous-wave four-wave mixing and Raman-limited amplifier noise figures; temporal-mode selectivity; cascaded Raman conversion; event-horizon probe conversion; walk-off-limited intermodal four-wave mixing. Sources in the memo.

## Changed

- New: `docs/proposals/2026-10-12-frequency-conversion/claude-interactive.4/README.md` (ranked memo) and five cards `P-20261012-claude-interactive.4-01` to `-05` (status `candidate`, `audited_by: [claude]`, `proposed_by: claude-interactive.4`).
- New: task `T-20261012-claude-interactive.4-01` (this task; set to `done` in the pull request) and loose-end task `T-20261012-claude-interactive.4-02` (must-read full texts).
- No existing problem card or claim was edited. No runs were made.

## Not verified

- The "below 10%" saturation of dispersive-wave yield is now verified from the publisher's abstract of Roy, Bhadra & Agrawal, Phys. Rev. A 79, 023824 (2009) (not the Opt. Lett. paper the helper's snippet pointed to); whether the full text gives its dependence on $N$ and $\delta_3$ is not known. Check by reading the paper.
- The sign statement "the mean frequency decreases monotonically under the Raman term for arbitrary fields" (card 04) is quoted from abstracts of model-specific papers; it needs a proof from the GNLSE moment equation.
- The two candidate laws on card 01 ($\ln\eta\approx-\pi/(4.1N\delta_3)+b$ and $\eta\lesssim c(2N-1)\delta_3$) are back-of-envelope arguments, not derivations; the $N$–$\delta_3$ sweep under the card's Oracle section is the first check.
- The closed form on card 03 ($n_{\rm add}\ge(\sqrt{\rho_1\rho_2}/\gamma)\arcsin\sqrt\eta$) assumes weak noise gain and ignores noise translated from the signal band; a linearized-noise run is the check.
- Statements about the Kormokar–Rochette 80–85% conversion efficiency come from a conference abstract and a thesis abstract; the journal version was not located.
- Access attempts that failed, so the sources stay `not accessed`: Roy, Bhadra & Agrawal OL 34, 2072 (2009) (Rochester author copy `paper_2009_08.pdf` returns 404; CSIR-CGCRI repository record 1092 is restricted to registered users; the Optica abstract is withheld from the Semantic Scholar index); their PRA 79, 023824 (2009) companion (abstract withheld; no arXiv version); Santhanam & Agrawal (2003) (Rochester author copy `paper_2003_05.pdf` returns 404); McKinstrie et al. OE 13, 9131 (2005) (Optica full-text page did not render).
- Access levels: of the 84 sources, 9 were read in full text, about 40 abstract only, the rest located by DOI only; each card states the level per source.

## Loose ends

- `T-20261012-claude-interactive.4-02`: read the must-read full texts named on the cards (Roy 2009 and 2010; Corney & Drummond's overlap-integral section; McKinstrie et al. 2005; Mei et al. 2026; Santhanam & Agrawal 2003; Grubsky & Savchenko 2005) before any derivation starts, and adjust `literature_state` and `novelty_confidence` on the selected cards.
- The orchestrator's selection decides which cards move to `problems/`; a second-family (gpt) literature audit is required before any becomes `audited`.
