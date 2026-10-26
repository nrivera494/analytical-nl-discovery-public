---
id: T-20261020-claude-interactive-03
title: "Scout longstanding open problems in optical thermalization where novelty could be argued as high (GPT family)"
type: literature
status: done
priority: 1
problem: null
claim: null
family_required: gpt
lease_hours: 8
created_by: claude-interactive
created: 2026-10-20
---

## Goal

The PI's request (2026-10-20): "Try to be more ambitious in looking for longstanding problems in optical thermalization. Only stuff where novelty could be argued as high."

This is one of two independent scouts; the other is T-20261020-claude-interactive-04, a Claude scout running in parallel.

## Context

The previous round produced P-20261020-gpt-f-01 (PR #89; priority 3, low novelty) and claim C-20261020-claude-interactive.21-01 (PR #90). No card in the registry has `novelty_confidence: high`.

## Deliverables

- A scouting review, `docs/review-2026-10-20-gpt-g-longstanding-optical-thermalization.md`. It contains a long list of at least 10 candidate problems, each with a verdict and the source that decided it, a kill search for recent solutions, a source ledger, a search log and a PI download list.
- Two to four candidate cards, `problems/P-20261020-gpt-g-NN-*.md`, for the problems that survive.

T-20261020-claude-interactive-05 is the cross-family novelty review of these cards.

## Completion (2026-10-20)

Completed by gpt-g (family gpt, model gpt-6-astra). Delivered the scouting review, 11 assessed candidates, three new candidate cards, source/access and exact search logs, and a five-paper PI download list. Six follow-up tasks preserve the access and technical-preflight loose ends. The other scout's branch/review remained unread. No claim, result, solver, generated-file or other-card status changes.

Validation: `~/agent-work/venv/bin/python -W ignore scripts/validate.py` and `~/agent-work/venv/bin/python -W ignore scripts/check_generated.py origin/main` both passed (`ok`) on 2026-10-20. `git diff --check` also passed.
