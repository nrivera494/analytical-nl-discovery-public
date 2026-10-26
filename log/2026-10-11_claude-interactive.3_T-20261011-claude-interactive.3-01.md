---
date: 2026-10-11
agent: claude-interactive.3
model: claude-fable-5-1
family: claude
task: T-20261011-claude-interactive.3-01
duration_min: 110
---

## Did

- Surveyed `main` (at `e4fd879`) and every open pull request (#20–#25, #28–#32) for results: all claim cards, explorations, review documents, run summaries and logs. Read the proposers' notes where needed (curator role, not auditor).
- Spawned one read-only subagent (claude-interactive.3.1, same model) to survey the merged round-1 history (explorations, reviews, logs, solver-upstream notes, runs on `main`); spot-checked its numbers against `runs/2026-10-04-claude-b.4-pmin-length-map/summary.json`, `explorations/2026-10-04-claude-b-manakov-deviation.md`, `explorations/2026-10-04-gpt-b-soliton-noise-baselines.md`, `explorations/2026-10-04-gpt-a-weak-admixture.md`, `claims/C-0004-*.md`, `explorations/2026-10-04-gpt-a-radiative-boundary-lead.md`, `runs/2026-10-05-claude-interactive-raman-stochastic/summary.json`, `docs/SOLVER.md` before use.
- Wrote `docs/HIGHLIGHTS.md`: status legend; three candidate results as mini-abstracts with figures; every result by problem (positive, negative, refuted, withdrawn, narrowed) with status, evidence family, location and run ids; methods and solver findings; a scored shortlist of ten and the ranking rule.
- Wrote `docs/highlights/AUDIT_PACKET.md`: clean-context packet for the top three and two alternates (statements verbatim, card paths with branch names, evaluator and run scripts, numbers, regime, recorded novelty searches, proposer family).
- Copied five registered figures from PR branches to `docs/highlights/fig-*.png` (all under 140 kB) with provenance in the captions. No new figures were made, so no figure run was registered.
- Ran four standard web searches to inform the novelty scores of the top three (queries listed in `docs/HIGHLIGHTS.md`, Section 4). They returned only sources already on the cards plus one adjacent lead (Feehan et al. 2020, DOI 10.1364/OE.396404, abstract only). No score changed. The document otherwise relies on the searches recorded on the cards and in the cross-family review (PR #25).

## Found

- No claim in the repository is `sim-verified` or `audited`; `results/` is empty. Every simulation check is same-family. Cross-family evidence exists only as formula re-derivations (gpt-a on the similariton Legendre rates; overlap ratios) and literature reviews.
- Candidate top three, by novelty plus impact on the rubric anchors: (1) the normal-dispersion semiclassical bound chain and Raman floor, C-20261010-claude-b-01..03 (PR #31), 4+4; (2) the amplifier-similariton noise laws, C-20261008-claude-a-01, -02 (PR #21, validated same-family in PR #30), 4+3; (3) the dispersionless covariance, momentum and parity bounds, C-20261010-claude-a-01..03 (PR #29), 4+3. Alternates: C-20261008-claude-b-01 (PR #22; ranked down for failed frozen held-out predictions) and C-20261008-gpt-b-01 (PR #23; highest-scoring GPT-family item).
- All three candidates are Claude-family proposals; the document says so and explains the weighing.
- The centroid bound on $\lambda_{\rm gen}$ was stated concurrently by claude-a and claude-b in different regimes (task T-20261011-claude-interactive.3-03).
- Inconsistencies noticed, not fixed (curator role): `docs/SOLVER.md` says the discrete adjoint becomes the default once the pin moves, the pin on `main` is still `b9fa957`, and T-20261006-claude-interactive-03 is `done`; Menyuk 1988 access is recorded three ways on different cards; `docs/literature-audit-2026-10.md` is a placeholder.

## Changed

- `docs/HIGHLIGHTS.md` (new).
- `docs/highlights/AUDIT_PACKET.md` (new).
- `docs/highlights/fig-1a-nd-bound-chain.png`, `fig-1b-nd-lambda-coefficients.png`, `fig-2a-similariton-closed-forms.png`, `fig-2b-similariton-shape-modes.png`, `fig-3-dispersionless-bounds.png` (copies of registered run figures; sources in the captions).
- `tasks/T-20261011-claude-interactive.3-01-*.md` (this task; status `done`), `-02` and `-03` (new loose ends).
- No claim card, problem card, generated file or branch other than `task/T-20261011-claude-interactive.3-01` was touched.

## Not verified

- The scores in Section 4 of `docs/HIGHLIGHTS.md` are one reviewer's preliminary Claude-family scores with full access to proposer notes; the rubric requires two clean-context reviewers from different families. To be checked by the GPT-6 Astra audit (T-20261011-claude-interactive.3-02).
- Novelty statements repeat what the cards and PR #25 record; the one new source located (Feehan et al. 2020) was read at abstract level only.
- Numbers quoted from PR branches were copied from the claim cards, exploration notes and `summary.json` files on those branches at the heads named in the audit packet; they were not recomputed.
- The round-1 survey by the subagent was spot-checked at nine points, not re-read in full.

## Loose ends

- T-20261011-claude-interactive.3-02: fold the audit outcome into `docs/HIGHLIGHTS.md`.
- T-20261011-claude-interactive.3-03: PI decision on the concurrent centroid-bound claims.
- Not tasked (already tracked elsewhere): the open cross-family checks T-0002, T-20261004-gpt-a-03, T-20261004-claude-b-01, T-20261004-claude-b-08; the literature audit T-20261010-claude-interactive-02.

## Addition of 2026-10-11 (PI request, checkpointed)

- The PI asked for two more sections in `docs/HIGHLIGHTS.md`: how the project works, and what simulation access added (refutation before confirmation). The session was checkpointed by the orchestrator before the second section was finished.
- Done: Section 2 ("How this project works"), verified against `AGENTS.md`, `docs/WORKFLOW.md`, `docs/PROMOTION.md`, `docs/AUDIT_PROTOCOL.md`, `docs/SOLVER.md`, `docs/solver-upstream/LEDGER.md`, `scripts/validate.py`, `scripts/check_generated.py`, `scripts/task.py`, `automation/README.md`, `automation/policy.yaml`, `problems/_TEMPLATE.md`, `claims/_TEMPLATE.md`, `tasks/_TEMPLATE.md`, `results/_TEMPLATE/`, `evaluator/README.md`, `.github/workflows/*.yml` and the problem cards' Oracle sections. Existing sections renumbered 4–6.
- Unfinished: Section 3 ("What simulation access added") is a placeholder. Drafts are in `docs/highlights/wip/`: the limits, enablers and forward-looking tests (`sectionB-static-draft.md`), and the refuted, corrected and narrowed ledger rows with the reverse-direction list and held-out tallies (`ledger-rows-draft.md`). Remaining: confirmed and inconclusive rows, counts, patterns, `docs/highlights/SIMULATION_LEDGER.md`, assembly, PR body.
- A background subagent started to mine the PR bodies and logs for the ledger was killed when the previous headless turn ended; no output from it was used. The rows in `wip/` were extracted directly from the claim cards, PR bodies and logs.

## Addition of 2026-10-11, completed after the checkpoint

- Section 3 ("What simulation access added") is now complete in `docs/HIGHLIGHTS.md`: the ledger of refutations, corrections and narrowings (3.1), counts with their scopes (3.2), patterns including the reverse direction (3.3), limits (3.4), what made the refutations possible (3.5), and the simulation tests most likely to break each open candidate (3.6). The full ledger, 71 rows with run ids, the per-lane held-out tally, the reverse-direction list and the undecidable list, is `docs/highlights/SIMULATION_LEDGER.md`. The `docs/highlights/wip/` folder was folded in and removed.
- Counting method: claims from the 20 cards on `main` and the open branches; held-out items as the record enumerates them (a frozen table scored as a whole is one item), with PR #30's 33 frozen criteria counted separately; ambiguities named rather than classified (the surrogate's second point, the radiative pilot, the order-six profile).
- Not verified: the classification of each ledger row is the curator's reading of the card or log wording; the counts were made by hand from the record and could be redone by a second reader. No new runs were made.

## Task T-20261011-claude-interactive.3-02: audit outcome folded in (2026-10-11, 18:35–18:55 EDT)

- Read `docs/review-2026-10-11-gpt-a-highlights-audit.md` and `log/2026-10-11_gpt-a_T-20261011-gpt-a-01.md` on `task/T-20261011-gpt-a-01` (PR #34) in full.
- `docs/HIGHLIGHTS.md`: header and legend updated; the three mini-abstracts rewritten to the auditor's narrowed wording with an Audit line each (per-statement correctness and novelty verdicts, sources with the auditor's access levels, run ids `2026-10-11-gpt-a-highlights-audit-c1` to `-c3`); the "candidate, pending audit" labels replaced by "cross-family audited (gpt-a, PR #34): keep with narrowed wording"; Section 3.1 gained the audit's rows, 3.2 the updated counts, 3.3 the new pattern instances, 3.4 a rewritten single-family bullet, 3.6 a note on which forward-looking tests the audit ran; Section 4 entries for the three candidates and for C-20261008-claude-b-01 updated; Section 6 rescored (Candidate 1 novelty 4 → 3; Candidate 3 impact 4 → 3; others unchanged) with the ranking decision stated.
- `docs/highlights/SIMULATION_LEDGER.md`: rows 72–88 added (2 refuted, 3 corrected, 2 narrowed, 10 confirmed), the held-out and undecided sections updated. `docs/highlights/AUDIT_PACKET.md`: a note that the audit is complete and where it is; the packet itself unchanged.
- Ranking decision: the top three stand. By the primary key C-20261008-claude-b-01 (7) now outscores Candidate 3 (6); the correctness rule keeps it below, because its headline law failed 7 of 9 frozen tolerances and its universal coefficients are untested, while Candidate 3's headline law was independently reproduced. Stated in Section 6 with the auditor's bounded check as evidence, not a ruling.
- No claim card was edited and no status changed; the auditor's proposed status changes are in its log and await the PI.
- Not verified: the auditor's numbers are copied from its report and runs, not recomputed; the rescoring is one curator's reading of the audit.
