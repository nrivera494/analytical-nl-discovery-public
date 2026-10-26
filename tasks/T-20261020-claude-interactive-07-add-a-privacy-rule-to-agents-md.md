---
id: T-20261020-claude-interactive-07
title: "Add a privacy rule to AGENTS.md: no personal data in web requests"
type: infra
status: done
priority: 1
problem: null
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-20
---

## Goal

Three headless Claude sessions put the PI's e-mail address in scholarly-API requests (Crossref User-Agent, 2026-10-12/13; arXiv User-Agent and OpenAlex mailto= query strings, 2026-10-20). Add a hard rule to AGENTS.md so that every agent, and every helper it briefs, uses a generic User-Agent and never sends personal data in headers, URLs or payloads.

## Context

## Deliverables

## Outcome

Done 2026-10-20 by claude-interactive: hard rule 15 added to AGENTS.md. The orchestrator's agent prompts carry the same rule from 2026-10-20 on.
