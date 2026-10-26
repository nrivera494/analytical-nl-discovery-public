---
date: 2026-10-19
agent: claude-interactive.15
model: claude-opus-5-5
family: claude
task: T-20261019-claude-interactive-08
duration_min: 55
---

## Did

- Wrote four promising-result folders, stacked on PR #70 (branch `task/T-20261019-claude-interactive-07`). Each has `RESULT.md`, `audit/` pointers and `repro/README.md`:

  | Result | Claim | Content |
  |---|---|---|
  | R-0003 | C-20261016-claude-interactive.6-02 | The narrowed core: the Raman energy identity, the $\kappa_UE^2$ ceiling and the retention bound |
  | R-0004 | C-20261017-gpt-d-01 | The exact sech loss ratio and its expansions |
  | R-0005 | C-20261017-gpt-d-02 | The arctangent concentration ceiling |
  | R-0006 | C-20261016-claude-a-04 | As narrowed by gpt-a: phase-mask witnesses A2 and B at $N=4$ |

- **Figures.** R-0003 to R-0005 use existing committed run figures. For R-0006 no committed figure shows the verified numbers: gpt-a's run figure mostly shows its own new masks (claim C-20261017-gpt-a-01). So I redrew one figure from gpt-a's committed `verification.json` with `repro/make_fig1.py` (colors checked with the dataviz validator). No simulation was run.
- **G7 check for R-0003.** I reran `runs/2026-10-16-gpt-d-raman-bound-audit/plot_audit.py` on a scratch copy. It regenerates figure 1 from the committed JSON.
- **Records.**
  - Claim cards: status → promoted, `result` set, an Outcome paragraph and an audit-trail row on each. Statements unchanged.
  - Problem cards: R-0003, R-0004 and R-0005 added to P-20261016-claude-interactive-02, and R-0006 to P-20261016-claude-interactive-03, each with an audit-trail row. Status unchanged.
- **Tasks.** Created T-20261019-claude-interactive.15-01 to -05.
- **Fact check.** A read-only subagent, claude-interactive.15.1 (claude-opus-5-5), cross-checked the numbers and attributions in the four folders against the cited runs and notes. Its findings are under Found.
- **Transcription check.** I checked the formulas as transcribed into R-0004 and R-0005 with an uncommitted mpmath/numpy script. This is not a verification and no number from it is quoted in a result.
  - The trigamma closed form equals the spectral integral to $10^{-15}$ at five $(r,x)$ points.
  - The long-pulse errors fall as $x^{-2}$ and $x^{-4}$, and the short-pulse residual as $x^4$.
  - A crude bathtub reproduces the arctangent to $10^{-4}$.
  - $Q=1/(3T)$ for a sech², and $\sup W=k\tau_2/2$.

## Found

**G5 (clean-context adversarial audit), from each report's own description.**
- **R-0003: met.** By their own descriptions, gpt-d's audits did not read the proposer's material:
  - 2026-10-16: no scripts, derivation notes, logs, PR description or branch history;
  - 2026-10-17: no explorations, logs, PR descriptions or run implementation.
  - Both also read the configs and summaries of the runs the card cites. `docs/AUDIT_PROTOCOL.md` does not list these, but they are not the proposer's notes. I counted the audits as clean-context and said so in RESULT.md, so the PI can overrule.
  - The 2026-10-16 report's formal verdict is "fail as written". The only failing part is the tightness law, which is excluded from R-0003. The pointer records verdict `fail`, with a `scope` field.
- **R-0004 and R-0005: met.** claude-interactive.8 committed its audits (6320014) before reading any proposer material, and it froze its held-out points in f784fed.
- **R-0006: open.** gpt-a's report was clean-context by its own description, but gpt-a classed it as verification and requested no audited status. I filed it as `verification-2026-10-17-gpt-a.md`, although its file in `claims/notes/` is named `audit-…`. The audit task is T-20261019-claude-interactive.15-01. The PI may judge the report sufficient; it lacks only an explicit attempt to break the narrowed lower bound.

**G6 is open for all four.**
- R-0003 to R-0005: both families searched, but Gordon 1986 and Herrmann & Nazarkin 1994 are abstract-only, and T-20261017-gpt-d-04 explicitly covers the $E^2$ bound, the trigamma formula, the short coefficient and the arctangent.
- R-0006: Efimov 2004, the closest prior work, is abstract-only for both families. Rosenberg 2020 was read in full only by gpt-d, for another claim (T-20261019-claude-interactive.15-02).

**G8 is open for all four**: T-20261019-claude-interactive.15-03 (Lean, R-0003 to R-0005) and -04 (validated numerics, R-0006). **G2 is n/a for R-0006**, which has no derivation.

**Inconsistencies.** Items 1–6 are reported and not fixed (task T-20261019-claude-interactive.15-05). Items 7–8 are stale Outcome text in cards I was editing anyway, fixed openly:
1. P-20261016-claude-interactive-02's `claims:` lacks C-20261017-gpt-d-01 and -02.
2. P-20261016-claude-interactive-02's current-results table still calls C-20261016-claude-interactive.6-02 "refuted as written" and says the bound is "loose by about 4×" (0.225). Later runs reached 0.3104 in propagation and 0.9556 for formal short pulses.
3. P-20261016-claude-interactive-03's `claims:` lacks C-20261017-gpt-a-01.
4. P-20261016-claude-interactive-03's current-results row for C-20261016-claude-a-04 says "proposed; verification not done", and the card quotes "+7.0%" and "at least 7–9%". Mask B measured 6.974%.
5. C-20261017-gpt-d-02's Checks row gives the verifier's bathtub range as $10^{-3}\le\tau_2Q\le300$. The run's grid starts at 0.003; $10^{-3}$ is the proposer's range.
6. In `claims/notes/audit-2026-10-17-claude-interactive.8-C-20261017-gpt-d-02.md` (lines 114–115), `\rho` and `\tau` became a newline and a tab.
7. The C-20261017-gpt-d-01 and -02 Outcome sections still said the verifier's summary "could not be written". Those files have existed in `docs/` since 3fd45a8. **Fixed here**, because I was editing those Outcomes anyway; the change is noted in each card's audit-trail row.
8. C-20261016-claude-interactive.6-02's Outcome said the gpt-d claims "await Claude-family verification", which has since happened. **Fixed here** the same way.

**Fact check.** claude-interactive.15.1 found three mismatches, two unsupported statements and several last-digit or wording items, all fixed before the final push:
- a misattributed $dt=3$ fs aliasing in R-0003;
- R-0006's published-dispersion row, which was a domain attack, not a frozen test;
- Rosenberg 2020, which gpt-d had read in full;
- '±10% energy' in R-0006's falsification;
- an unrecorded palette check.

It confirmed:
- about 480 other numbers and attributions;
- all 13 commit hashes and 15 task ids;
- the mathematics: the closed form against the spectral integral, the expansion coefficients, the asymptotes of $F$, $\sup W$, and the retention bounds.

**Process.** `task.py claim` creates the branch from `origin/main`, where this task file did not exist, so the claim commit was empty. The merge of PR #70's branch brought in the task file.

## Changed

- New: `results/promising/R-0003-raman-energy-loss-ceiling-and-retention/`, `R-0004-exact-sech-raman-loss-ratio/`, `R-0005-arctangent-raman-concentration-ceiling/` and `R-0006-phase-mask-headroom-leading-raman-soliton/` (with `figures/fig1-witness-headroom.png` and `repro/make_fig1.py`).
- Claims: C-20261016-claude-interactive.6-02 (audited → promoted, R-0003), C-20261017-gpt-d-01 (audited → promoted, R-0004), C-20261017-gpt-d-02 (audited → promoted, R-0005), C-20261016-claude-a-04 (sim-verified → promoted, R-0006).
- Problems: P-20261016-claude-interactive-02 (`results: [R-0003, R-0004, R-0005]`) and P-20261016-claude-interactive-03 (R-0006 added). Status, priority and literature state unchanged.
- Tasks: T-20261019-claude-interactive-08 → done; new T-20261019-claude-interactive.15-01 to -05.

## Not verified

- I ran no simulation. All numbers are copied from committed run summaries and from the verifiers' and auditors' reports.
  - claude-interactive.15.1 checked them against the sources.
  - I spot-checked the 2026-10-16 and 2026-10-17 gpt-d retention and $\rho$ numbers, the claude-interactive.8 summaries, and gpt-a's `verification.json` myself.
- The figure pipelines that need raw data (R-0003 figure 2, R-0004, R-0005) were not rerun. Only their commands were checked against each run's `config.yaml` or README.
- I read no paper. Access levels and findings in the Novelty sections are those recorded by gpt-d, gpt-a, claude-a and claude-interactive.8/.8.1.
- The model of gpt-d and gpt-a is recorded as `gpt-6-astra`, as in their reports. I did not check it independently.

## Loose ends

- T-20261019-claude-interactive.15-01: clean-context GPT audit of C-20261016-claude-a-04 as narrowed (G5 of R-0006).
- T-20261019-claude-interactive.15-02: dedicated novelty search for R-0006 (G6).
- T-20261019-claude-interactive.15-03: Lean formalization of R-0003 and R-0005, and of R-0004 if feasible (G8).
- T-20261019-claude-interactive.15-04: validated-numerics certificate for R-0006 (G8 analog).
- T-20261019-claude-interactive.15-05: the stale records listed above.
- Existing tasks cited as open questions in the results: T-20261017-gpt-d-04, T-20261017-gpt-d-05, T-20261016-gpt-d-05, T-20261016-gpt-d-06, T-20261016-gpt-b-03, T-20261017-claude-interactive.8-01, T-20261017-claude-interactive.8-02, T-20261017-gpt-a-01, T-20261017-gpt-a-02, T-20261017-gpt-a-03 and T-20261016-claude-a-03.
