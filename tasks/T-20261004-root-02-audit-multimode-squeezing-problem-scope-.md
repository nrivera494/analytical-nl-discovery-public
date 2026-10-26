---
id: T-20261004-root-02
title: "Audit multimode squeezing problem scope and literature"
type: registry-review
status: open
priority: 2
problem: null
claim: null
family_required: not-gpt
lease_hours: 8
created_by: /root
created: 2026-10-04
agent: /root
model: unknown
family: gpt
---

## Round-1 focus (2026-10-04)

First complete the Claude-family full-text review of P-20261004-root-03, P-20261004-claude-interactive-01 and P-20261004-claude-interactive-02. Read Levandovsky–Vasilyev–Kumar 1999, Lantz et al., Steiglitz & Rand 2009, Sloan et al. (arXiv:2509.03482), Gordon–Haus 1986, and Corney–Drummond. root-01 follows later. Add `claude` to `audited_by` only for cards whose review is complete. Derivation on those cards needs a GPT review as well (T-20261004-claude-interactive-01).

## Goal

Independently audit the four new multimode squeezing candidates and their literature, reduction criteria, regime boundaries, and overlaps before derivation or novelty claims.

## Context

Review P-20261004-root-01, P-20261004-root-02, P-20261004-root-03, and P-20261004-root-04 together with `docs/multimode-squeezing-scope.md`. The initial GPT-family intake read primary-source abstracts only; all cards remain `candidate`, `literature_state: unaudited`, with no completed family audit. Earlier local campaign reports are background, not repository-verified results.

Read full texts and follow their references for normal-dispersion filtering, scalar/vector soliton noise, zero-dispersion and intermodal parametric limits, Raman/acoustic noise, and constrained readout. Resolve overlap with P-001, P-002, P-011, and P-013. Independent review must not infer absence of prior theory from the short intake. Record exact DOI/arXiv identifiers and access depth for every literature statement.

## Deliverables

- Current problem cards with the sharpest defensible gap, known sublimits, and any narrowing/merger recommendation; retain demoted candidates if appropriate.
- Source/access ledger and audit-trail entries. A single new family review does not automatically satisfy two-family review: the initial intake was not a completed GPT audit. Keep candidate status until the workflow's audit requirements are actually met.
- Evaluate whether each proposed reduction has physical coordinates, predictive scaling, and a controlled regime rather than merely a many-waveform fit. Do not require elementary closed forms or a universal theory.
- Log and follow-up tasks for unresolved sources or gaps. No derivation campaign or code implementation is part of this task.

## Progress, 2026-10-04 (claude-interactive, claude-opus-5-5)

On the PI's instruction the set was restructured to four problems:
- root-01, rewritten: minimum noise under spectral filtering in normal dispersion;
- root-03, rewritten: minimum noise for a multimode soliton launch;
- P-20261004-claude-interactive-01, new: weak LP02/LP11 admixture;
- P-20261004-claude-interactive-02, new: vacuum-, gain- and Raman-driven noise of the soliton's collective coordinates.

root-02 and root-04 are parked, each with its reactivation question. `docs/multimode-squeezing-scope.md` now holds only the shared definitions and the parabolic-profile overlap table.

Literature: targeted searches located the single-mode soliton-squeezing baseline, weak-probe trapping (Steiglitz & Rand 2009), vector spatial-soliton squeezing (Lantz et al.), and the PI group's own multimode-fiber noise papers (Nat. Photon. 19, 751 (2025), DOI 10.1038/s41566-025-01677-2, preprint arXiv:2311.05535; arXiv:2509.03482). Access was abstract or bibliographic only; levels are recorded on each card.

**Still open:**
- full-text reading of Levandovsky et al. 1999, Lantz et al., Steiglitz & Rand, Sloan et al. and Gordon–Haus;
- a second-family (GPT) review of the two new cards.

No card is marked audited.

## Progress, 2026-10-04 (claude-b, claude-opus-5-5; replaces the stopped subagent claude-interactive.2)

The round-1 focus is done: the Claude-family full-text review of P-20261004-root-03, P-20261004-claude-interactive-01 and P-20261004-claude-interactive-02. All three cards now list `audited_by: [claude]` and `last_audited: 2026-10-04`. They still need the GPT-family review (T-20261004-claude-interactive-01) before they can become `audited`.

Reading done (access levels are recorded on the cards):
- **Full text:** Lantz et al.; Steiglitz & Rand 2009 (author copy); Sloan et al. (main text); Corney & Drummond.
- **Abstract only:** Levandovsky et al. 1999 and Gordon & Haus 1986. The Optica pages returned a CAPTCHA, which was not bypassed. Their content is single-mode; for Gordon & Haus, the formula is confirmed in Corney & Drummond's full text.
- **Additional full texts:** Rand, Steiglitz & Prucnal 2005; Lee, Lai & Malomed 2005; Konyukhov 2025; Derevyanko et al. 2006; Sun et al. 2024; Werner & Friberg; Rivera 2026.

Main outcomes:
- **root-03.** Narrowed to the deviation from the Manakov/LP01 value. In the Manakov limit, every readout that treats the modes alike gives the scalar $F$. Walk-off is a launch frequency offset. Multimode solitons exist only for $\delta\lesssim1$. Photon number is not a channel for $F$.
- **-01.** The $\delta=0$, $\varepsilon\to0$ derive item is the Manakov rotation of the scalar result. Walk-off at first order became the main target. novelty_confidence medium → low.
- **-02.** The vacuum and ASE parts for two-component Manakov solitons are known (Rand et al. 2005; Derevyanko et al. 2006). Modal-partition jitter is the multimode form of birefringence-mediated jitter (Mollenauer & Gordon 1994) and follows from conservation laws. The target was refocused on Raman and acoustic intermodal exchange.

Follow-up tasks: T-20261004-claude-b-01 (non-Claude solver check of the reductions), T-20261004-claude-b-02 (gated full texts), T-20261004-claude-b-03 (GIF625 walk-off parameter and existence window).

**P-20261004-root-01** was then reviewed in the same session. The classical counterpart of its part 1 is the Mamyshev-regenerator literature: the transfer-function plateau where the bright term $T_NG^2$ vanishes, with scaling rules (Provost et al. 2007) linked to wave breaking (Finot & Rochette 2025). The target was refocused on the offset of $P_{\min}$ from that plateau, on the depth, and on the flank. Sloan et al. was read in full and does not cover part 3. root-01 now lists `audited_by: [claude]`.

**Still open in this task:** the parked root-02 and root-04, if they are reactivated. Status stays `open`; the PI can close it once the GPT-family review (T-20261004-claude-interactive-01) covers the same cards.
