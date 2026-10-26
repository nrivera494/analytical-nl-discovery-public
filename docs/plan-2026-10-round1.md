# Round 1: four problems, four agents

The PI set this round on 2026-10-04, and claude-interactive orchestrates it. AGENTS.md applies in full; this page only fixes who works on what, in which order, and what each step waits for.

## Assignments

| Agent | Model | Problem | Queue, in order |
|---|---|---|---|
| claude-interactive.1 | Claude Opus 5.5, max effort | P-001 (passive parabolic-pulse noise) | T-20261004-claude-interactive-05 |
| claude-interactive.2 | Claude Opus 5.5, max effort | P-20261004-root-03 (multimode soliton squeezing) | T-20261004-root-02 (round-1 focus) → T-20261004-claude-interactive-06 → T-20261004-claude-interactive-10 |
| gpt-a | gpt-6-astra, max effort | P-002 (modal dynamics inside a multimode soliton) | T-20261004-claude-interactive-02 → T-20261004-claude-interactive-07 |
| gpt-b | gpt-6-astra, max effort | P-20261004-claude-interactive-02 (collective-coordinate noise) | T-20261004-claude-interactive-01 → T-20261004-claude-interactive-08 → T-20261004-claude-interactive-09 |

Each agent works through its own queue. If the next item is blocked, it moves on rather than waiting. Each task ends with its own pull request; agents do not merge.

## Dependencies

- **Before derivation on root-03 and -02 (tasks -10 and -09):** each card needs a review by two families. The Claude review is T-20261004-root-02 and the GPT review is T-20261004-claude-interactive-01.
- **Before task -10:** the first-order capture test, T-20261004-claude-interactive-02, must also have reported.
- **Before task -07 (P-002):** it builds on the capture test, which is why the same agent runs the capture test first.
- **Verification of the C-0001 rewrite:** T-0002, by a non-Claude family, after task -05 is merged.
- **Verification of claims from tasks -07 and -09:** by a Claude agent, in a later round.
- **Verification of the claim from task -10:** by a GPT agent, in a later round.

## Environment

- **Working copies.** Each agent works in its own clone or worktree. Never use the PI's Desktop checkout.
- **Solver.** Fetch it with `git submodule sync solver && git submodule update --init --depth 1 solver` (about 15 s). The Julia packages are already installed in `~/.julia`.
- **Python.** `~/agent-work/venv/bin/python` has PyYAML for `scripts/task.py` and `scripts/validate.py`.
- **Raw data.** Use `~/analytical-nl-discovery-data/<run-id>/` (`runs/README.md`).
- **Identity.** Commits use the agent id as author (`git -c user.name=<agent> -c user.email=<agent>@agents.invalid`). Pushes and pull requests go through the PI's `gh` login.
- **Time.** About 240 minutes per session (`automation/policy.yaml`). Reserve the last 15 for log, validation, push and pull request.

## Interim storage

Raw data stays on this Mac until the PI has cloud storage (T-20261002-claude-interactive-02). Do not delete anything under `~/analytical-nl-discovery-data/`.
