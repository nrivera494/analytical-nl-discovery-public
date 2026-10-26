---
id: T-20261002-claude-interactive-02
title: "Choose the raw-data storage platform"
type: infra
status: open
priority: 1
problem: null
claim: null
family_required: human
lease_hours: 8
created_by: claude-interactive
created: 2026-10-02
---

## Interim decision (PI, 2026-10-04)

Until the PI has cloud storage, raw data for the first four problems is stored locally under `~/analytical-nl-discovery-data/` (see `runs/README.md`). This task stays open for the cloud choice and the migration.

## Goal

The PI picks where raw simulation output lives, and `runs/README.md` names it. An agent then wires it up: a small helper that uploads a run's `raw/` folder and records its URI in `meta.yaml`, plus agent credentials that can write but not delete.

## Context

Options discussed with the PI on 2026-10-02: an S3-compatible bucket (Cloudflare R2 or Backblaze B2), institutional research storage, and Zenodo for archiving the data behind accepted results. Whatever the platform, the policy matters more: raw data is kept only for runs cited by a claim, and everything else is reproducible from the committed config and seed. T-0002 is blocked on this decision.

## Deliverables

PI: the choice, in this file or in chat. Agent: `runs/README.md`, the upload helper, and a credentials note in `automation/README.md`.
