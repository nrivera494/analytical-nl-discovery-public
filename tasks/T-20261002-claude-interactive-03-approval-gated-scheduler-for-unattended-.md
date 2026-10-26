---
id: T-20261002-claude-interactive-03
title: "Approval-gated scheduler for unattended sessions"
type: infra
status: blocked
priority: 2
problem: null
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-02
---

## Goal

At each scheduled time, the PI gets a push notification asking whether to run sessions. The PI can answer run, delay until a given time, or skip to the next slot, and can restrict which roster accounts the session may use. Approved sessions start through `automation/run_session.sh`.

## Context

Blocked until the PI chooses the notification channel and the machine that runs sessions (discussed 2026-10-02). On macOS, a launchd agent rather than cron is the natural trigger, because it catches up on slots missed while the Mac slept. `automation/README.md` lists the set-up the launcher already needs.

## Deliverables

`automation/scheduler.py` (or similar), a launchd plist template, a section in `automation/README.md`, and a manual test from the PI's phone.
