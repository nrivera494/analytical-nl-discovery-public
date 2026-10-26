---
id: T-20261002-claude-interactive-05
title: "Separate agent-identity fields from the governing model in front matter"
type: infra
status: open
priority: 3
problem: null
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-02
---

## Goal

Front matter does not use one key for two meanings, and `validate.py` checks the identity fields and log entries.

## Context

AGENTS.md asks every artifact to record `agent`, `model` and `family`, but problem cards already use `model` for the governing equations. gpt-a worked around this with `updated_by`, `updated_model` and `updated_family`. Log entries are named `<date>_<agent>_<task-id>.md` in `log/README.md`, but `log/2026-10-01-gpt-a-T-0001.md` uses hyphens, and nothing checks this.

## Deliverables

A schema decision written into `docs/WORKFLOW.md` and the templates: for example, rename the problem key to `governing_model` and keep `model` for the AI model. Migrate the existing cards. Extend `validate.py` to check the identity fields and log entries (front matter keys, file name pattern). Do not rename existing log files; they are append-only.
