---
id: T-20261011-claude-interactive-01
title: "Results highlights document: catalog of results, top three, audit and HTML briefing"
type: explore
status: done
priority: 1
problem: null
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-11
---

## Goal

A repo document (docs/HIGHLIGHTS.md) that organizes every result found so far and opens with the three strongest (novelty x impact) as mini-abstracts with figures; the top three chosen by a Fable 5.1 agent and audited for novelty and correctness by a GPT-6 Astra agent; an HTML briefing for the PI.

## Context

PI request (2026-10-11, in chat):
- Create a document in the repository that organizes and highlights the results found so far.
- At the top, put the three strongest results, where strongest means the largest combination of novelty and impact. Each gets the problem, the main results in a paragraph, and one or two figures, like a mini-abstract.
- One Fable 5.1 agent at Extra effort determines the candidate top three.
- GPT-6 Astra at max effort audits their novelty and correctness.
- Also provide the document as an HTML briefing.

Plan:
- **Curator.** claude-interactive.3 (claude-fable-5-1, effort xhigh) runs through the new agent definition `.claude/agents/results-curator.md`. It catalogs main and every open PR, drafts `docs/HIGHLIGHTS.md`, and writes a clean-context audit packet for the shortlist.
- **Auditor.** A GPT-6 Astra agent (effort max) audits the three candidates under docs/AUDIT_PROTOCOL.md: clean context, novelty search and correctness checks.
  - Where a candidate's claims were proposed by the GPT family, that review is same-family and is labelled as such.
- **Integration.** The curator folds the audit outcomes into the document; the orchestrator then builds the HTML briefing.

## Deliverables

- `docs/HIGHLIGHTS.md`, with its figures under `docs/highlights/`.
- The audit report.
- PI addition (2026-10-11): the document also describes how the project works (problem cards, repository structure, task statuses, the solver) and what simulation access added. That part is a ledger of where simulation refuted, narrowed, corrected or confirmed candidate analytical results, with refutation first. The curator writes it while the audit runs.
- The HTML briefing, delivered as an artifact and kept as a local copy under `briefings/`.

## Outcome

- Draft and integration: PR #33 (curator). Audit: PR #34 (gpt-a).
- HTML briefing: published as an artifact, with a local copy in `briefings/2026-10-11-highlights/`.
- See the log entry for this task.
