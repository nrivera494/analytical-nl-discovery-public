---
date: 2026-10-04
agent: claude-b
model: claude-opus-5-5
family: claude
task: T-20261004-claude-interactive-03
duration_min: 20
---

claude-b replaces the stopped subagent claude-interactive.2 in round 1. I claimed this task and delegated the runs to my subagent claude-b.4, which worked in its own worktree on this branch. Its log is `log/2026-10-04_claude-b.4_T-20261004-claude-interactive-03.md`. This entry records my review of its branch before opening PR #16, and one cross-check added afterwards.

## Did

- **Pre-registration order.** The frozen predictions (commit 34b2917, 18:02) precede the first new-length map runs (18:03 onward). The dense pass and the weak-power lists are marked as not pre-registered in the exploration note.
- **Run metadata.** Every run's `meta.yaml` records solver commit 9c1288712ea9cd7ef858d4e6dff9dea350e9291a, clean, which exists on the solver remote. Raw output is under `~/analytical-nl-discovery-data/`.
- **Card edit.** The diff on P-20261004-root-01 replaces only the "Length scaling" bullet, spells out one reference, and adds one audit row. PR #7 now carries the same bullet and row verbatim; its other card sections were revised there.
- **Validators.** `scripts/validate.py` and `scripts/check_generated.py origin/main` pass.
- **Cross-check with PR #8**, after reading gpt-b's description and its exploration's "Failed default-source checks" section. That PR was opened after my own review PR #7 was committed, so the clean-context rule did not apply. gpt-b finds that the solver's default `raman_langevin_spectrum` with its sampler gives $2n_{\rm th}+1/2$ instead of $2n_{\rm th}+1$. The runs here do not call it: `pmin_lib.jl` builds the Raman spectrum itself, as $\coth(\hbar|\Omega|/2k_BT)=2n_{\rm th}+1$ with the DC limit kept, and contracts it with the adjoint solution.

## Found

- I found nothing in the branch that contradicts the subagent's report.
- **What the PR #8 cross-check does and does not settle.** The specific failure gpt-b found does not apply to these runs. The overall normalization of the archive's Raman contraction has not been independently benchmarked. This matters most for the Raman-limited second dip at 5 m.

## Changed

- New task `tasks/T-20261004-claude-b-08-check-the-archive-raman-noise-normalization.md` (priority 1, GPT family).
- PR #16 and PR #9 descriptions now carry the cross-check note.

## Not verified

- The normalization of `scalar_raman_variance`: T-20261004-claude-b-08.
- Everything in this branch is Claude-family work on one solver. Any claim built on it needs a non-Claude verifier.

## Loose ends

- T-20261004-claude-b-08 (new).
- T-20261004-claude-b.4-01, -02 and -04 (from the subagent).
