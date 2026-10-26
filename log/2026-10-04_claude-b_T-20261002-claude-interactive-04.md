---
date: 2026-10-04
agent: claude-b
model: claude-opus-5-5
family: claude
task: T-20261002-claude-interactive-04
duration_min: 20
---

claude-b replaces the stopped claude-interactive.2 in round 1. This Claude-only loose-end task was taken after the round-1 queue: bring seed claims C-0002 to C-0004 in line with their reviewed problem cards. C-0001 belongs to T-20261004-claude-interactive-05 and was not touched. This is a revision by the proposing family (claude), not verification.

## Did

- Read C-0002, C-0003 and C-0004 and their cards, P-002 and P-004 (both audited).
- **C-0002** (occupation-only $\gamma_{\rm eff}$ tracking for multimode solitons): **withdrawn**. Four reasons are recorded in its checks table:
  - its motivating 120-mode simulation anecdote had no source or run id (rule 3) and is removed;
  - the occupation-only closure is the assumption P-002's audited target says must be tested;
  - for the GRIN overlap matrix no equal-width common-sech multimode soliton exists at finite fractions, even with frozen occupations (shown in the root-03 review, PR #7);
  - walk-off acts as a carrier-frequency offset the claim omits, and the regime was still undefined (rule 6).
  
  Superseded by P-002's target and gpt-a's round-1 capture tasks (T-20261004-claude-interactive-02 and -07).
- **C-0003** (gamma-distributed higher-order-mode fraction below the TMI threshold): **withdrawn**. In its stated linear regime it is the classical gamma statistics of window-integrated amplified Gaussian noise (Mandel 1959; coherence modes in Raymer et al. 1985). It cannot be exact for a fraction bounded by 0 and 1, and unequal coherence-mode weights change $M$. P-004's narrowed target (depletion, mode competition, measured fraction) supersedes it.
- **C-0004** (a symmetry mapping that needs a dispersion sign flip): **refuted** by a cheap check, run `2026-10-04-claude-b-c0004-mapping-check`. It uses an independent numpy split-step integrator; the solver was not used.
  - Conjugation plus envelope time reversal plus gain→loss, with $\beta_2$ unchanged, inverts the pulsed NLSE with gain, $\beta_2$, $\beta_3$ and Kerr to a relative error of $7\times10^{-12}$.
  - The claim's $\beta_2$ flip fails with error 1.42.
  - Without the time reversal the map works only if $\beta_3=0$.
  - The algebra agrees: $B(z',t')=A^*(L-z',-t')$ obeys the same NLSE with $g\to-g$.
  - The correct map is the known optical-phase-conjugation compensation condition (Pepper & Yariv 1980; Watanabe & Shirasaki 1996). The slow-envelope amplifier version is Chen et al., Nat. Phys. 2025.
- Updated the claim notes on P-002 and P-004 so they are current, with an audit-trail row on each.

## Found

None of the three seed claims survives as stated. One is refuted by a recorded check (C-0004); two are superseded by the audited problem targets or restate known statistics (C-0002, C-0003).

## Changed

- `claims/C-0002…`, `claims/C-0003…` (withdrawn) and `claims/C-0004…` (refuted): status, `updated`, a checks-table row and an outcome section on each. All three are kept, per rule 7.
- `problems/P-002…` and `problems/P-004…`: claim notes updated, audit-trail rows added. Status, priority and literature_state are unchanged.
- New run `runs/2026-10-04-claude-b-c0004-mapping-check/`.
- `tasks/T-20261002-claude-interactive-04…`: status done.

## Not verified

- **No cross-family review.** Withdrawal and refutation by the proposing family need none under the rules, but the PI may want one.
- **Bibliographic records only.** The Mandel 1959, Pepper & Yariv 1980 and Watanabe & Shirasaki 1996 citations rest on Crossref records. Their content is standard textbook material but was not reread here.

## Loose ends

None new. C-0001 stays with T-20261004-claude-interactive-05.
