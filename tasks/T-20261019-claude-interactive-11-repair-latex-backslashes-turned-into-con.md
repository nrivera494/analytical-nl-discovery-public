---
id: T-20261019-claude-interactive-11
title: "Repair LaTeX backslashes turned into control characters by the orchestrator's script edits (C-20261010-claude-a-01, P-20261016-claude-interactive-01)"
type: loose-end
status: done
priority: 2
problem: null
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-19
---

## Goal

Python escape sequences in non-raw strings turned \rm into a carriage return and \beta into a backspace. Restore them and scan the repository for any others.

## Context

## Deliverables
