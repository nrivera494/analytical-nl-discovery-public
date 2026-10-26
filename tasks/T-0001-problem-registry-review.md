---
id: T-0001
title: "Independent review of the problem registry and literature audit"
type: registry-review
status: done
priority: 1
problem: null
claim: null
family_required: not-claude
lease_hours: 24
created_by: claude-bootstrap
created: 2026-10-01
updated_by: claude-interactive
updated_model: claude-opus-5-5
updated_family: claude
last_updated: 2026-10-02
---

## Goal

Every file in `problems/` has been checked by a model family other than `claude`, and the registry reflects the result.

## Context

The registry was seeded by one Claude session from one literature audit of about 18 searches. Treat every "not found" as unverified. `docs/literature-audit-2026-10.md` holds the long-form audit if the PI has pasted it in.

## Deliverables

For each of `P-001` to `P-005`:

1. Verify each cited paper exists and says what the file claims. Mark each as `full text`, `abstract only` or `not accessed`.
2. Search for prior work the file misses. Search by concept and by the neighbouring-field name for the same idea, and follow citations of the key papers forward.
3. Update `literature_state`, `novelty_confidence`, `priority` and the gap statement. Demote the problem if the gap has closed. Add a row to the audit trail and add `gpt` (or your family) to `audited_by`. Set status to `audited` if you agree it is open or partial; `demoted` otherwise.
4. Specifically for `P-001`: obtain and read the Boscolo–Turitsyn Gegenbauer-projection work on similariton perturbations and state whether it computes a spectrum.

Add problems that are missing. Criteria: a robust phenomenon seen in simulation or experiment, an established model the solver covers or could cover, no existing analytical description, and a possible lab test. Use `problems/_TEMPLATE.md`.

Finish with a short memo in `log/` listing every status change and the three problems you would start with, and why.

## Progress at the end of the gpt-a audit

All fifteen seed cards have been reviewed and updated; three provisional problems and seven follow-up tasks were added. The dispositions, evidence limits and derivation recommendations are in [the session memo](../log/2026-10-01-gpt-a-T-0001.md). This is a literature/registry audit, with no derivations, simulations or claim-status changes.

Status remains **open** because deliverable 4 cannot honestly be marked complete: [BT] is a Boscolo–Turitsyn **private communication (2007)** in arXiv:0806.3516, p. 43, rather than an identifiable published paper. That bibliography was read in full text; the communication was not accessed, so whether it computed a spectrum remains unknown. [T-20261002-gpt-a-01](T-20261002-gpt-a-01-resolve-access-to-the-unpublished-bt-com.md) asks the PI to supply it or explicitly dispose of this deliverable. Remaining source-depth and independent-review work is separately queued; repeated searches for a presumed published [BT] article are not a substitute for that disposition.

## PI disposition (2026-10-02)

The PI closed this task. Deliverable 4 is disposed of as unobtainable: [BT] is a 2007 private communication of unknown content, and the PI does not treat its existence as evidence that the P-001 gap is closed. P-001 keeps its status (`audited`), `literature_state: partial`, priority 1 and `novelty_confidence: medium`. [BT] stays listed as a residual novelty risk in P-001. Recorded by claude-interactive on the PI's instruction. This was a status change only; no review work was redone. See [T-20261002-gpt-a-01](T-20261002-gpt-a-01-resolve-access-to-the-unpublished-bt-com.md).
