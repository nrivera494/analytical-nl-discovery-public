---
date: 2026-10-16
agent: gpt-a
model: gpt-6-astra
family: gpt
task: T-20261016-claude-b-01
duration_min: 224
status: done
---

## Did

Completed the independent audit of claim C-20261016-claude-b-01 on the
assigned task branch, stacked on PR #45 and its parent PR #44. PR #50
contains this audit. Implemented independent scalar GNLSE propagators,
computed TOD-free strips, ran the frozen and new held-out predictions,
and reproduced the full Roy benchmark approximately. Compared independent
RK4IP and Yoshida methods and the pinned agents' Julia solver. Added a
Double64 full-TOD attack below the Float64 field-noise floor.

Repository validation and the generated-file check passed. The independent
Python scripts compile, the serial launcher passes shell syntax checking,
and the scientific figures were visually inspected. The pinned solver
working tree remains clean.

Kept one heavy numerical process active at a time, checking memory before
launch. Stored raw fields, strip scans, spectra and source PDF outside git.
Larger grids were used only for documented convergence tests. No other
clone or original solver repository was changed. No other-project
conversation history was accessed.

Maintained the clean-context restriction through the completed report's
commit. Shared solver API examples and the limited proposer gate-function
context used after independent results are explicitly recorded in the
audit. No proposer propagation or optimization algorithm, derivation note,
log, PR description or branch history was read. At the independent-audit
commit, gpt-b's separate novelty report remained unread. After commit
2c63a4c3b92b022dae5bfab347115a597c1d23bd, I read that report and added the
post-commit literature note. Its partly-published verdict changes no
numerical result or audit verdict. The new observable-repair task is
cross-referenced to its existing T-20261016-gpt-b-07 asymptotic task.

## Found

The specified fixed gate fails to isolate radiation at smaller TOD. In the
unique-minimum case N=2, xi=2.25, delta3=0.003, its band yield is about
114 times the separated DW yield; physical photon weighting does not remove
the discrepancy (`2026-10-16-gpt-a-dw-highprecision`).
Step, doubled-window and paired finer-grid controls pass the frozen one-percent tolerance; the grid pair uses a matched coarser step.
The exact TOD-free gate null and the recompression-end full-TOD rate
diagnostic explain the slower core-tail contribution. This is a numerical
refutation of the measurement premise, not a proof of the full perturbed
PDE's ultimate remote-frequency limit.

The finite-range strip law survives. Local-slope error powers are
1.076–1.191 across the passing frozen and new-launch grids, versus the
predicted first power. The original Raman-free 39.49 dB gap from Roy Eq. 6
at delta3=0.02 becomes 7.67 dB in the paper's full model. The independently
computed full-model strip is about 0.4655; fitting only p,c gives better
observable-range peak predictions over delta3=0.016–0.03, while both
descriptions fail at larger TOD. The published circles are reproduced to
1.3724 dB RMS, with a residual left open. Sources:
`2026-10-16-gpt-a-dw-analysis`, `2026-10-16-gpt-a-dw-roy`,
`2026-10-16-gpt-a-dw-strips`, `2026-10-16-gpt-a-roy-reference`.

## Changed

Added independent run configurations, scripts, summaries and figures,
and completed the audit report. Claim 01 changes from cheap-checks-passed
to refuted, with new GPT-family Checks and an audit-trail entry. Its old
regime is retained as superseded. The replacement regime describes only
the finite cases supported numerically. Its Statement and Derivation were
not rewritten. Verify task T-20261016-claude-b-01 is done.

Claims C-20261016-claude-b-03 and -02 and their verify tasks remain
unstarted and unchanged. No problem cards, results or generated indices
were edited.

## Not verified

A uniform repaired radiation observable, nonzero leading coupling,
coherent multi-burst asymptotics, a derived prefactor, a global optimized
ceiling and a laboratory noise floor remain unestablished. The remaining
high-N collapse points and deferred precision cases are not counted as
passes. The recompression-end separated radiation changed by 1.2565
percent on its first step halving, slightly outside the one-percent
target; its diagnostic status is explicit in the report and run summary.

## Loose ends

- T-20261016-gpt-a-01: repair the fixed-gate observable and finish or
  supersede the deferred precision checks.
- T-20261016-gpt-a-02: resolve or bound the residual Roy figure offset.
- T-20261016-gpt-a-03: finish the N=6,8 descriptive collapse replication.
- T-20261016-claude-b-03 and T-20261016-claude-b-02: the assigned
  conservation and shaping audits were not started within this budget.

## Proposed card changes

No problem card was edited. Proposed changes for the PI: distinguish a
finite-range, calibrated exponential law from a yield ceiling; replace
the literal fixed-gate limit with a justified outgoing-radiation measure;
distinguish the conserved envelope norm from broadband physical photon
number. Correct the exact-strip decimal in a future proposer revision.
The supplied claim already confines the large Roy discrepancy to the
Raman-free model; retain that qualification. The paper's shock coefficient
is 1/(omega0*T0); both it and the requested doubled variant were tested
(`2026-10-16-gpt-a-roy-reference`, `2026-10-16-gpt-a-dw-roy`).
