---
id: T-20261016-claude-a-07
title: "Check whether Kormokar, Shamim & Rochette 2023 (arXiv:2301.02945) Fig. 3 already shows the maximum of the leading-soliton efficiency versus duration and its N-dependence"
type: literature
status: done
priority: 2
problem: P-20261016-claude-interactive-03
claim: C-20261016-claude-a-02
family_required: not-claude
lease_hours: 2
created_by: claude-a
created: 2026-10-16
---

## Goal

View Fig. 3 of arXiv:2301.02945 (and the published JOSA B version, DOI 10.1364/JOSAB.478975), extract ECE_GNLSE versus T_FWHM for each N, and compare with C-20261016-claude-a-02 (peak position, peak value 1.29/sqrt(N)). Also search the soliton-collision Raman-transfer literature (Luan et al. 2006; rogue-soliton papers) for the same scaling. Report access levels.

## Context

The orchestrator claude-interactive widened this task on the PI's request on 2026-10-16 to a novelty and experimental-consistency search for items (a)-(d) of C-20261016-claude-a-02. Here (d) means the physical-energy corollary in the PI's brief, not the separately lettered self-steepening item in the claim card. The search includes Kormokar/Rochette's other work, Raman soliton collisions, SSFS energy scaling and saturation, experiments, and neighbouring materials. It distinguishes the duration that maximises energy share from a maximum of absolute soliton energy.

Researcher: agent gpt-b; model gpt-6-astra; family gpt. Clean context: read the claim card and this task, without reading the proposer's logs, explorations, derivation files, or run outputs before the review is committed. Literature only; no Julia or fibre simulations.

## Deliverables

Review at `docs/review-2026-10-16-gpt-b-raman-transfer-energy-novelty.md`, figure digitisation with uncertainties, experimental-consistency table, explicit verdicts for (a)-(d), search/access log, one claim-card novelty-check row, session log, and tasks for unresolved work. Validate and push a PR against main, explicitly stacked on PR #48.

## Completion

Completed by gpt-b (gpt-6-astra, family gpt) on 2026-10-16. The report gives individual verdicts, digitised Fig. 3 symbols with reading bounds, the limits on fitting censored peak positions, conditional experimental conversions, the energy/share distinction, the close 18 fs response-overlap antecedent, and exact search/access records. No Julia or fibre simulations were run. Only one independent novelty-search row was added to the claim card. Follow-ups: T-20261016-gpt-b-08 through T-20261016-gpt-b-11.
