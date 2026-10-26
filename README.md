> **Public snapshot.** This is a curated, read-only snapshot of a private research repository, taken from its state on 2026-10-21. Some problem threads, two of the four manuscript drafts, the private solver fork (the `solver/` submodule) and local configuration have been removed, so a few cross-references point to files that are not included here. The authoritative record is the private repository; this snapshot is published to document the workflow (problem cards, claims, adversarial audits, simulation oracles) and the verified results it has produced so far.

# analytic-discovery

A program to find new analytical results in nonlinear ultrafast, multimode and amplifying fiber systems, with candidate results checked against differentiable simulation and adversarial audit, and the best ones taken to the lab.

Everything the project knows lives in this repository as text. Agents from any provider work from the same files.

## The three layers

| Layer | Folder | One file per | Question it answers |
|---|---|---|---|
| Problems | `problems/` | candidate problem or system | What quantity do we want a theory of, and is it really open? |
| Claims | `claims/` | candidate result | What specific statement is being proposed, and how far has it been checked? |
| Results | `results/` | verified result (a folder) | What have we established, in what regime, with what evidence? |

A problem can have many claims. A claim becomes a result only by passing the gates in `docs/PROMOTION.md` and a merge approved by the PI.

## Where to look

- `STATUS.md` — dashboard (generated) plus the PI's current priorities. The dashboard lists what is waiting on the PI.
- `problems/INDEX.md` — registry of problem candidates (generated).
- `results/RANKING.md` — ranked verified results (generated).
- `tasks/` — the work queue. `python scripts/task.py list` shows what is open.
- `log/` — one entry per agent session.
- `AGENTS.md` — the rules every agent follows. Read this first.
- `docs/SOLVER.md` — the solver (`solver/` submodule) and how agents use and change it.
- `automation/` — how to run scheduled, parallel sessions.

## Set-up state

Done:

- Repository on GitHub; `.github/CODEOWNERS` names `@nrivera494`.
- CI: `validate` runs on every pull request; `rebuild-generated` rebuilds the generated files after every merge to `main`; `notify-result` flags pull requests that touch `results/`.
- Solver pinned as the `solver/` submodule: `git submodule update --init --depth 1 solver`.

Still to do by the PI:

1. `main` is not technically protected. GitHub offers branch protection and rulesets on private repositories only with a paid plan (the API returned 403 on 2026-10-04), so CODEOWNERS review is not enforced either. Until that changes, the rules are convention: agents never push to `main` (AGENTS.md rule 13), and only the PI merges. If protection becomes available, require pull requests and code-owner review, and see `.github/workflows/rebuild-generated.yml` for letting that workflow past the protection.
2. Optional: set the repository variable `PI_HANDLE` and the secret `RESULT_WEBHOOK_URL` (for example an ntfy.sh topic URL) for result notifications.
3. Choose the raw-data storage (`runs/README.md`).
4. Paste the literature audit report into `docs/literature-audit-2026-10.md`.
5. Keep the held-out benchmark outside this repo (see `benchmark/README.md`).
6. Set up the machine that runs sessions (`automation/README.md`).

Local checks: `pip install -r requirements.txt`, then `python scripts/validate.py`. Agents do not run `scripts/build_index.py` on branches; CI runs it on `main`.
