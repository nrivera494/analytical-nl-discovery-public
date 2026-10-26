#!/usr/bin/env bash
# Launch one unattended session for one agent.
#   automation/run_session.sh <agent-id>
# Reads automation/roster.yaml and automation/policy.yaml from the main checkout, works in a
# separate clone per agent so that parallel sessions never share a working tree.
#
# Environment overrides:
#   DISCOVERY_MODE     force a mode from policy.yaml instead of drawing one at random
#   DISCOVERY_PYTHON   python with PyYAML (default: automation/.venv/bin/python, else python3)
#   DISCOVERY_CLONES   where agent clones live (default: automation/worktrees)
#   DISCOVERY_LOGS     where session transcripts go (default: automation/session-logs)
set -euo pipefail

AGENT="${1:?usage: run_session.sh <agent-id>}"
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
CLONES="${DISCOVERY_CLONES:-$HERE/worktrees}"
LOGS="${DISCOVERY_LOGS:-$HERE/session-logs}"
mkdir -p "$CLONES" "$LOGS"

# Schedulers (cron, launchd) start with a minimal PATH. Add the usual install locations.
export PATH="$HOME/.local/bin:$HOME/.juliaup/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

PY="${DISCOVERY_PYTHON:-}"
if [ -z "$PY" ]; then
  if [ -x "$HERE/.venv/bin/python" ]; then PY="$HERE/.venv/bin/python"; else PY=python3; fi
fi
"$PY" -c 'import yaml' 2>/dev/null || { echo "PyYAML is not available to $PY; see automation/README.md" >&2; exit 1; }

# GNU timeout enforces the time budget: `timeout` on Linux, `gtimeout` from Homebrew coreutils on macOS.
TIMEOUT="$(command -v timeout || command -v gtimeout || true)"
[ -n "$TIMEOUT" ] || { echo "need timeout or gtimeout (macOS: brew install coreutils)" >&2; exit 1; }
# Keep a Mac awake while the session runs.
AWAKE=()
if command -v caffeinate >/dev/null; then AWAKE=(caffeinate -i); fi

VARS="$("$PY" - "$HERE" "$AGENT" "${DISCOVERY_MODE:-}" <<'PY'
import os, random, shlex, sys, yaml
here, agent, forced = sys.argv[1], sys.argv[2], sys.argv[3]
roster = yaml.safe_load(open(f"{here}/roster.yaml"))["agents"]
policy = yaml.safe_load(open(f"{here}/policy.yaml"))
if agent not in roster:
    sys.exit(f"unknown agent {agent}: add it to automation/roster.yaml")
a = roster[agent]
names = list(policy["modes"])
if forced:
    if forced not in names:
        sys.exit(f"unknown mode {forced}: choose from {names}")
    mode = forced
else:
    mode = random.choices(names, weights=[policy["modes"][n]["weight"] for n in names])[0]
out = {"FAMILY": a["family"], "COMMAND": a["command"], "MINUTES": policy["session_minutes"],
       "SUBAGENTS": policy["subagents_max"], "MODE": mode, "TYPES": ",".join(policy["modes"][mode]["task_types"])}
lines = [f"{k}={shlex.quote(str(v))}" for k, v in out.items()]
for k, v in (a.get("env") or {}).items():
    lines.append(f"export {k}={shlex.quote(os.path.expanduser(os.path.expandvars(str(v))))}")
print("\n".join(lines))
PY
)" || exit 1
eval "$VARS"

# Each account must have been logged in once by hand in its own configuration directory.
for d in "${CLAUDE_CONFIG_DIR:-}" "${CODEX_HOME:-}"; do
  if [ -n "$d" ] && [ ! -d "$d" ]; then
    echo "$AGENT: $d does not exist; log this account in first (automation/README.md)" >&2
    exit 1
  fi
done

ORIGIN="$(git -C "$REPO" remote get-url origin)"
DIR="$CLONES/$AGENT"
if [ ! -d "$DIR/.git" ]; then
  git clone "$ORIGIN" "$DIR"
fi
cd "$DIR"
git config user.name "$AGENT"
git config user.email "${AGENT}@agents.invalid"
git fetch --prune origin
git checkout main
git reset --hard origin/main
# Follow the submodule URL in .gitmodules (the agents' copy of the solver; the original is read-only),
# then fetch only the pinned commit.
git submodule sync solver
git submodule update --init --depth 1 solver

PROMPT="$(sed -e "s/{{AGENT}}/$AGENT/g" -e "s/{{FAMILY}}/$FAMILY/g" -e "s/{{MINUTES}}/$MINUTES/g" \
              -e "s/{{MODE}}/$MODE/g" -e "s/{{TYPES}}/$TYPES/g" -e "s/{{SUBAGENTS}}/$SUBAGENTS/g" \
              automation/session_prompt.md)"

STAMP="$(date +%Y%m%d-%H%M%S)"
echo "[$STAMP] $AGENT mode=$MODE minutes=$MINUTES" | tee -a "$LOGS/sessions.log"
set +e
printf '%s\n' "$PROMPT" | ${AWAKE[@]+"${AWAKE[@]}"} "$TIMEOUT" -k 60 "${MINUTES}m" bash -c "$COMMAND" > "$LOGS/$STAMP-$AGENT.out" 2>&1
RC=$?
set -e
echo "[$(date +%Y%m%d-%H%M%S)] $AGENT finished rc=$RC (124 means the time budget ran out)" | tee -a "$LOGS/sessions.log"

# Safety net: if the agent was cut off, push whatever is committed on its task branch so nothing is lost.
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [ "$BRANCH" != "main" ]; then
  git push origin "$BRANCH" || true
  if [ -n "$(git status --porcelain)" ]; then
    echo "[$(date +%Y%m%d-%H%M%S)] $AGENT left uncommitted changes in $DIR on $BRANCH" | tee -a "$LOGS/sessions.log"
  fi
fi
