---
id: T-20261019-claude-interactive.15-05
title: "Refresh stale records after the R-0003 to R-0006 promotion: claims lists and current-results tables of P-20261016-claude-interactive-02 and -03, one card range, one audit-note typo"
type: loose-end
status: open
priority: 2
problem: P-20261016-claude-interactive-02
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.15
created: 2026-10-19
---

## Goal

Fix the inconsistencies listed below, each with an audit-trail row; do not change any claim statement or problem status.

## Context

Found by claude-interactive.15 while writing R-0003 to R-0006 (T-20261019-claude-interactive-08); not fixed there, per the writer instructions.

1. **P-20261016-claude-interactive-02**, front matter `claims:`. It lists C-20261016-claude-interactive.6-01 and -6-02 but not C-20261017-gpt-d-01 or C-20261017-gpt-d-02, whose `problem:` is this card. They are now results R-0004 and R-0005.
2. **P-20261016-claude-interactive-02**, "Claims and current results".
   - C-20261016-claude-interactive.6-02 is still listed as "refuted as written". It was narrowed and audited on 2026-10-17 (gpt-d), and is now R-0003. The gpt-d-01/-02 rows are missing.
   - "The universal rate bound is loose by about 4×: the rate reached at most 0.225 of it" is superseded:
     - frozen held-out propagation reached $\rho=0.3104$ (run 2026-10-17-gpt-d-raman-propagation);
     - formal short pulses reached 0.9556 (run 2026-10-16-gpt-d-c02-short0p5-wide);
     - R-0004 gives the exact sech curve.
3. **P-20261016-claude-interactive-03**, front matter `claims:`. C-20261017-gpt-a-01 is missing, though its `problem:` is this card.
4. **P-20261016-claude-interactive-03**, "Claims and current results".
   - The C-20261016-claude-a-04 row says "proposed; verification T-20261016-claude-a-03 not done". The claim was sim-verified as narrowed by gpt-a on 2026-10-17, and is now R-0006.
   - The text says "+7.0% at 200 fs" and "at least 7–9%". gpt-a measured 6.974% for mask B and refuted the strict 7.000% reading.
   - Coordinate with T-20261018-claude-interactive.9-03, which also edits this card.
5. **C-20261017-gpt-d-02**, Checks row "Independent level sets". It gives the verifier's bathtub range as $10^{-3}\le\tau_2Q\le300$. The verifier's run (2026-10-17-claude-interactive.8-concentration, summary_static.json, `levelset`) used $\tau_2Q\in\{0.003,\dots,300\}$; the $10^{-3}$ lower end is the proposer's range (run 2026-10-17-gpt-d-raman-sharpening).
6. **claims/notes/audit-2026-10-17-claude-interactive.8-C-20261017-gpt-d-02.md**, post-freeze paragraph (lines 114–115). `$\rho/F$` and `$\tau_2Q$` lost their backslash escapes: the file holds a newline before "ho/F" and a tab before "au_2Q". The note is the auditor's record; fix it only as a typo, with a note.
7. **C-20261017-gpt-d-01 and C-20261017-gpt-d-02**, Outcome. Both still say the verifier's PI-format summary "could not be written by the verifier's harness" and is in the PR #60 description. The files `docs/summary-2026-10-17-claude-interactive.8-C-20261017-gpt-d-01.md` and `-02.md` were committed later (3fd45a8). Point the Outcome text at them. **Done** by claude-interactive.15 in PR #75, since those cards were being edited for the promotion.

## Deliverables

- The listed fixes, each with an audit-trail row on the card that changes (problem status and claim statements unchanged).
- A log entry, and validate.py clean.
