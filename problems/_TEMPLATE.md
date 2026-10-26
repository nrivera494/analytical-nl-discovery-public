---
id: P-YYYYMMDD-agent-NN
title: "Short name"
status: candidate            # candidate | audited | active | parked | demoted | solved
priority: 3                  # 1 (highest) to 5
literature_state: unaudited  # unaudited | open | partial | largely-solved
novelty_confidence: low      # low | medium | high
target_quantity: "One sentence naming the concrete quantity to develop an analytical theory of."
model: "Governing equations."
oracle_ready: missing             # available | partial | missing  (can the solver check a candidate theory today?)
last_audited: null
audited_by: []               # families that have reviewed the literature, e.g. [claude, gpt]
proposed_by: agent-id
claims: []
results: []
---

## Target quantity

The concrete object to derive, with the form an answer would take (closed form, reduced ODE system, scaling exponent, spectrum, distribution, bound).

## Signal of hidden simplicity

What has been seen in simulation or experiment that suggests a simple description exists.

## Literature state

Key papers, each with DOI or arXiv id, what it derives, and how much of it was read (`full text` / `abstract only` / `not accessed`).

## Sharpest statement of the gap

What exactly is not known. If part is known, say which part.

## Conjectures

Pointers to claim files.

## Oracle

Which solver capability checks a candidate theory, what the cheap test is, and what is missing.

## Lab test

The measurement that would distinguish the new theory from the naive expectation.

## Risks and must-reads

Papers not yet accessed that could change the status. Ways the problem could turn out uninteresting.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
