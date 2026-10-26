---
date: 2026-10-02
agent: claude-interactive
model: claude-opus-5-5
family: claude
task: T-20261002-claude-interactive-01
duration_min: 60
---

## Did

On the PI's instruction, repaired the infrastructure that unattended sessions depend on. This was an interactive session on the PI's Mac, not a roster account. Commits are authored as `claude-interactive`. The machine has no GitHub credentials for git, so nothing was pushed; the PI pushes.

## Found

- `.github/` was referenced by README.md, docs/PROMOTION.md and automation/README.md but never committed. As a result, the generated files on `main` were never rebuilt.
- `automation/run_session.sh` could not run on this Mac. macOS has no `timeout`, the system `python3` has no PyYAML, `gh` is not installed, and the `claude` CLI is not on PATH.
- The solver repository (github.com/nrivera494/FastDifferentiableMMNLO, public) has a git history of several GB. A full clone over this connection failed after 12 minutes. The pinned tree is about 330 MB, almost all notebooks and benchmark data; the source is about 1 MB (GitHub API tree listing, 2026-10-02).

## Changed

- Added `.github/CODEOWNERS` and three workflows: `validate.yml` (runs `validate.py` and the new `scripts/check_generated.py`), `rebuild-generated.yml` and `notify-result.yml`.
- Added `.gitignore`, including raw array formats under `runs/`. `.DS_Store` removed from the index; the local file is untouched.
- Added the `solver/` submodule, pinned to 9c1288712ea9 (solver `main` on 2026-10-02). The gitlink was recorded without cloning; `.gitmodules` sets `shallow = true`. Added `docs/SOLVER.md`, a Solver section and a submodule step in AGENTS.md, and pointers from `evaluator/README.md`, `runs/README.md` and T-0003.
- `scripts/build_index.py`: the dashboard now lists open tasks with `family_required: human` under "Waiting on the PI" and lists blocked tasks separately.
- `automation/run_session.sh`: uses `automation/.venv` or `DISCOVERY_PYTHON` for PyYAML, `timeout` or `gtimeout`, and `caffeinate` on macOS. It extends PATH for launchd/cron, exports per-account `env` from the roster, checks the login directory, fetches the solver shallowly, accepts `DISCOVERY_MODE`, and reports uncommitted changes left at cutoff. Checked with `bash -n` under bash 3.2; the roster parsing was tested; no session was launched.
- `automation/roster.yaml`: added `account` and `env` (separate `CLAUDE_CONFIG_DIR` / `CODEX_HOME` per entry). The commands are still the bootstrap placeholders. Writing unattended-permission options into the roster was declined by this session's safety check, so the PI chooses them (automation/README.md step 5).
- `automation/README.md` and README.md rewritten for the current set-up state.
- New tasks: `-02` choose raw-data storage (PI), `-03` approval-gated scheduler (blocked on PI choices), `-04` revise seed claims (claude), `-05` front-matter identity schema.

## Not verified

- None of the GitHub workflows have run. The deploy-key route around branch protection in `rebuild-generated.yml` follows GitHub's ruleset documentation as I remember it, and the PI should confirm it when setting up protection.
- The `CLAUDE_CONFIG_DIR` and `CODEX_HOME` separation of logins is from the CLIs' documentation and was not tested with two accounts.
- `git submodule update --init --depth 1 solver` was not completed on this machine; the shallow fetch was very slow here.

## Loose ends

- T-20261002-claude-interactive-02 to -05 (above).
- T-20261002-gpt-a-07, on the T-0001 branch, still says that no code changes are allowed without a PI instruction. The PI has since allowed solver changes (docs/SOLVER.md). The task file should be updated once both branches are merged.
- The PI's local copy `FastDifferentiableMMNLO for agents/` sits untracked in the checkout and is excluded only through `.git/info/exclude`. It is 86 GB, including about 52 GB of leftover temporary pack files in its `.git`.
