---
date: 2026-10-20
agent: claude-interactive.22
model: claude-opus-5-5
family: claude
task: T-20261020-claude-interactive-04
duration_min: 60
---

## Did

- **Scouting for longstanding open problems in optical thermalization** with arguably high novelty: the PI's request of 2026-10-20, Claude-family scout.
- **Searches.** Four helpers ran the literature kill searches in parallel. All four are claude family, general-purpose subagents with the model inherited from this session (claude-opus-5-5), web searches only:
  - .22.1: GRIN cluster;
  - .22.2: lattices;
  - .22.3: single-mode fibre and coherent structures;
  - .22.4: lasers and review mining.
- **My own reading.** I re-read the passages the cards rest on, from arXiv or author-hosted copies:
  - Ferraro 2023 (Adv. Phys. X); Ferraro 2025 (Physica D); Garnier 2019; Aschieri 2011; Podivilov 2019; Pourbeyram 2022;
  - Iubini 2013; Baldovin 2021; Kabat 2026; Picozzi 2014 §6.2; the Fusaro 2019 and Mithun 2018 abstracts.
- **Second-pass kill search.** OpenAlex forward citations for each card: about 80, 107 and 88 titles; abstracts of the hits read.
- **One run, no solver:** `runs/2026-10-20-claude-interactive.22-resonance-kinematics`.
  - Four-wave factorizations with $\beta_3$ and $\beta_4$.
  - Umklapp kinematics of the two-loop mesh lattice.
  - A Raman budget for quasi-CW silica tests.
  - Length exponents of published self-cleaning thresholds.
- **Deliverables.**
  - The review, with 28 candidates.
  - Three candidate cards.
  - "See also" lines on P-005 and P-010.
  - Eight loose-end tasks.

## Found

- **Shortlist, ranked.** Each card has explicit open statements and a negative kill search.
  1. **P-20261020-claude-interactive.22-02** (novelty high, priority 2): non-Gibbs breather condensation of light in coupled-core fibre.
     - Open since Rasmussen 2000. Restated by Iubini 2013, Mithun 2018, Baldovin 2021 (Phys. Rep.) and Iubini & Politi 2025 (PRL), and "in progress" in Kabat 2026 (PRL).
     - No optical experiment in the non-Gibbs region.
     - First target: a multi-breather GGE.
  2. **P-20261020-claude-interactive.22-01** (novelty high, priority 2): the threshold–length law of Kerr self-cleaning.
     - Weak-disorder kinetics, the only quantitative theory, predicts $P_c\propto L^{-1/2}$. Its authors call it non-quantitative (Garnier 2019; Ferraro 2025).
     - Two two-length data sets point to $P_c\propto L^{-1}$ (onset at $\approx7L_{\rm NL}$). The evidence is weak, and neither excludes $L^{-1/2}$.
     - A controlled cut-back series with measured disorder has never been done.
  3. **P-20261020-claude-interactive.22-03** (novelty medium, priority 3): relaxation of the frequency-local invariant $J$ near zero dispersion beyond four-wave order.
     - Open per Picozzi 2014 (experiment), Onorato 2023 and Vassilev 2025 (theory).
     - Near pre-emption in water waves: Sutherland & Yim, arXiv:2609.23175.
  4. **RSB in fibre lasers** (no card; task -04). Possibly high impact; its null-model premise needs a full-text check.
- **Seeds killed or parked.**
  - S2 killed as posed: Biasi–Evnin–Malomed 2021/2023 already show the ideal-GRIN obstruction to ergodicity.
  - S4 killed: Jordan & Josserand 2000; Rumpf & Newell; Tolomeo & Weber 2023.
  - S6 parked.
  - S7 parked: rigorous sub-power-law results (De Roeck et al. 2024, 2025); not fibre-testable.
- **My own Floquet-heating idea (N1) was already published:** Moorcroft et al., arXiv:2511.08355, November 2025. The run reproduces its kinematic premise: Umklapp channels at 0.40–0.51 of the normal weight, not converged.
- **Raman budget.** About 25 rad of Kerr phase before stimulated Raman threshold in silica (24.6 rad at 1064 nm). This limits every quasi-CW thermalization test. In coupled-core arrays at $a\sim0.25$–1 it leaves only about 2.5–22 coupling lengths with ns pulses.
- **Corrections to the orchestrator's seeds.**
  - Baudin 2023 does not say cleaning is not RJ.
  - The "freezing" of S2 is explained in the literature.
  - Several citation details in my own brief to helper .22.4 were wrong; the helper corrected them (review, §4).

## Changed

- New:
  - `docs/review-2026-10-20-claude-interactive.22-longstanding-optical-thermalization.md`;
  - `problems/P-20261020-claude-interactive.22-01-self-cleaning-threshold-length-law.md`;
  - `problems/P-20261020-claude-interactive.22-02-non-gibbs-breather-condensation-coupled-core-fibre.md`;
  - `problems/P-20261020-claude-interactive.22-03-frequency-local-invariant-relaxation-single-mode-fibre.md`;
  - `runs/2026-10-20-claude-interactive.22-resonance-kinematics/`;
  - tasks `T-20261020-claude-interactive.22-01` to `-08`.
- Edited (See-also lines only):
  - `problems/P-005-kinetic-and-prethermal-laws.md`;
  - `problems/P-010-pulsed-kerr-self-cleaning.md`.
- `tasks/T-20261020-claude-interactive-04-…md`: status open → done.

## Not verified

- **Helper access levels.** Most are abstract-only; the review's ledger says which. Only passages marked "me" were read by me.
- **The Krupa 2017 numbers** come from helper .22.1's reading of the publicly hosted SI. The main text is paywalled.
- **Arithmetic estimates, not derived.** The $x$ values, the Raman budget, the ps walk-off argument and the S5 length estimates are order-of-magnitude arithmetic on published numbers. They should be checked by the oracle tasks.
- **The multi-breather GGE target of -02 is a working hypothesis.** Mithun et al. 2018 report weak non-ergodicity in part of the non-Gibbs phase, which may defeat any ensemble description there.
- **The Hirota-proximity hypothesis of -03** (whether $W_6$ vanishes at first order in $\beta_3$) is unchecked.
- **The RSB null-model premise** (helper .22.4's idea) is unchecked against the experiments' normalization.
- **Novelty ratings are first-family.** The cross-family reviews T-20261020-claude-interactive-05 and -06 are designed to attack them.

## Process issues

- **E-mail sent to arXiv.** Helper .22.1's first curl request to arXiv carried the user's e-mail address in the User-Agent header, against this session's instruction not to send it to unrelated services. All later requests used a generic header. Whoever runs the next session should brief helpers explicitly on headers.
- **Blocks met, not bypassed.** opg.optica.org served a captcha; hal.science served a bot challenge; science.org returned 403. Other legitimate copies were used where they existed.
- **Blocked shell redirect.** A first attempt to write the run script with a shell heredoc redirect into the repository was blocked by a hook; it was rewritten with the Write tool.

## Loose ends

- T-20261020-claude-interactive.22-01: PI downloads for card -01.
- T-20261020-claude-interactive.22-02: PI downloads for card -02, including the Marques Muniz 2023 supplement.
- T-20261020-claude-interactive.22-03: PI downloads for card -03, and the Sutherland & Yim pre-emption check.
- T-20261020-claude-interactive.22-04: scope an RSB null-model card.
- T-20261020-claude-interactive.22-05: revisit P-005's "kinetic rates solved" sentence, and a PI decision on who owns the quasi-CW rate law (P-005, P-010, -01, T-20261020-claude-interactive.21-01).
- T-20261020-claude-interactive.22-06: oracle for -01 (resonant GRIN onset exponent), after the cross-family review.
- T-20261020-claude-interactive.22-07: oracle for -02 (DNLS ensembles), after the cross-family review.
- T-20261020-claude-interactive.22-08: scope counter-propagating polarization attraction (N19).
