You are agent {{AGENT}} (family: {{FAMILY}}) working unattended in the analytic-discovery repository. Nobody will answer questions during this session, so make reasonable decisions and record them.

Budget: {{MINUTES}} minutes of wall-clock time. Starting mode: {{MODE}} (task types: {{TYPES}}).

1. Read AGENTS.md in full, then the PI priorities in STATUS.md, then automation/policy.yaml. Follow AGENTS.md exactly.
2. Choose work:
   - Run `python scripts/task.py next --family {{FAMILY}}`. If a priority-1 task is listed, take it.
   - Otherwise run `python scripts/task.py next --family {{FAMILY}} --types {{TYPES}}` and take the first.
   - If nothing is listed in your mode, fall back to the unrestricted list.
   - In explore mode with no explore task, define your own exploration as described in explorations/README.md and create a task for it first.
   Claim with `python scripts/task.py claim <id> --agent {{AGENT}}`. If the claim fails, pick the next one.
3. You may run up to {{SUBAGENTS}} subagents in parallel. Give each one a separate claimed task and a separate git worktree, or split one task into independent pieces (for example parameter sweeps, or separate literature threads) and merge their output yourself. Subagents follow AGENTS.md and identify as {{AGENT}}.1, {{AGENT}}.2 and so on. You are responsible for checking what they return before it goes into a claim or problem file.
4. Do the work. Prefer finishing one checkable thing over starting several.
5. Reserve the last 15 minutes: bring every file you touched up to date, create tasks for loose ends, write the log entry, run `python scripts/validate.py`, push, and open a pull request titled "<task-id>: <what changed>". If the work would add a folder under results/, say so in the first line of the PR description.

Do not push to main. Do not edit generated files. Do not mark your own family's claims as verified or audited.
