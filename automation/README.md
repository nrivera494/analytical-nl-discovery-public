# Automation

The repository cannot start agents by itself. Something has to launch each provider's command-line agent on a schedule, on a machine that can reach the solver. This folder holds that launcher.

## Pieces

- `roster.yaml` — the accounts that run sessions, the login directory each one uses, and the command that starts it.
- `policy.yaml` — session length, subagent limit, and how sessions are split between verification, derivation, loose ends and free exploration.
- `session_prompt.md` — the instructions every session starts from.
- `run_session.sh <agent>` — starts one session in that agent's own clone, enforces the time budget, and pushes the task branch if the agent was cut off. Set `DISCOVERY_MODE=<mode>` to choose the mode instead of drawing it at random.
- `crontab.example` — a daily schedule for four accounts. It runs every session without asking. An approval-gated scheduler is planned in task `T-20261002-claude-interactive-03`.

## Set-up on the PI's Mac

1. **Tools.** `brew install gh coreutils`. `coreutils` provides `gtimeout`, which enforces the time budget. Then run `gh auth login` and `gh auth setup-git`, so that `git push` and `gh pr create` work over HTTPS.
2. **CLIs.** Codex is in `~/.local/bin/codex`. The Claude desktop app's bundled copy of Claude Code is not meant for scripts, so install the standalone CLI and check that `claude --version` works in a new terminal.
3. **Launcher Python.** `python3 -m venv automation/.venv && automation/.venv/bin/pip install -r requirements.txt`. The system `python3` has no PyYAML.
4. **One login directory per roster entry.** The four entries are two providers × two e-mail addresses. Each keeps its credentials in its own directory, so logging one in never logs another out:

   ```sh
   mkdir -p ~/.agent-accounts/{claude-a,claude-b,gpt-a,gpt-b}
   CLAUDE_CONFIG_DIR=~/.agent-accounts/claude-a claude      # /login with the first e-mail's Claude account
   CLAUDE_CONFIG_DIR=~/.agent-accounts/claude-b claude      # /login with the second e-mail's Claude account
   CODEX_HOME=~/.agent-accounts/gpt-a codex login           # first e-mail's ChatGPT account
   CODEX_HOME=~/.agent-accounts/gpt-b codex login           # second e-mail's ChatGPT account
   ```

   Each Codex directory gets its own `config.toml`; settings in `~/.codex` do not carry over.
5. **Permissions.** Decide how much each CLI may do without asking, and put those options into `command` in `roster.yaml`. The placeholders `claude -p` and `codex exec -` will stop at the first action that needs approval. Whatever you choose, keep the safety rules below.
6. **Solver.** The launcher fetches `solver/` into every clone. Julia packages install into the shared `~/.julia` depot, so precompile once by hand to keep that cost out of the first session: `julia --project=<clone>/solver -e 'using Pkg; Pkg.instantiate()'`.
7. **Location.** macOS does not let background jobs read `~/Desktop`, `~/Documents` or `~/Downloads` without Full Disk Access. Before scheduling, keep the checkout that runs the launcher somewhere else, for example `~/code/analytical-nl-discovery`.
8. **Dry run.** Run one session by hand, for example `DISCOVERY_MODE=loose automation/run_session.sh claude-a`, and read `automation/session-logs/` before scheduling anything. Then do the same for one GPT entry.

## Safety

Unattended agents run shell commands. Ideally run them as a dedicated macOS user or in a container that can see the repository clones, the solver and the Julia depot, and nothing else. Agents push with the token from `gh auth login`, so their commits carry their agent id as author but are pushed through the PI's GitHub account. For separate provenance, use a GitHub machine user or a GitHub App with permission to push branches and open pull requests only. This repository cannot protect `main` on its current GitHub plan. The PI's token can push to `main` and merge pull requests, so only AGENTS.md rule 13 and the session prompt stop an agent from doing so. A machine-user token with write access, combined with branch protection, would make that a technical limit rather than a convention. The same token can also push to the original solver repository, github.com/nrivera494/FastDifferentiableMMNLO, which agents must never modify (AGENTS.md rule 14). The guard there is per clone: `solver/` follows `.gitmodules` to the private agents' copy after `git submodule sync`, and any clone that adds the original as a remote sets its push URL to `DISABLED` (`docs/SOLVER.md`).

## How parallel sessions avoid each other

- A task is claimed by creating the remote branch `task/<id>`. The server accepts only one creation, so two agents cannot hold the same task.
- Each agent works in its own clone. Subagents use separate git worktrees.
- New tasks, claims and log entries carry the date and agent id in their names, so files created in parallel never collide.
- Generated files are rebuilt on `main` by `.github/workflows/rebuild-generated.yml`, never by agents. `scripts/check_generated.py` rejects pull requests that edit them.
- A claim older than the task's `lease_hours` is stale. `task.py claim` then lets another agent take over the branch; the new agent continues from the existing commits and notes the takeover in its log.

## Spending compute

`policy.yaml` sets the mix. A reasonable start is the default: about a third on verifying and auditing existing claims, a third on derivation for audited problems, the rest on loose ends and free exploration. Shift weight toward `explore` when the pipeline is empty and toward `verify` when claims are waiting.

Within a session, parallelism comes from subagents: independent parameter sweeps, separate literature threads, several ansätze for the same reduced model, or several auditors attacking one claim from different angles. The orchestrating agent checks and merges their output.
