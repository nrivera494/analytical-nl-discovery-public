#!/usr/bin/env python3
"""Work-queue helper.

  task.py list                         all open tasks, with who holds each
  task.py next --family gpt [--types verify,audit]
                                       open, unclaimed tasks this family may take, best first
  task.py claim T-0001 --agent gpt-a   claim by creating and pushing branch task/T-0001
  task.py release T-0001               delete your claim branch (only if you opened no PR)
  task.py new --agent gpt-a --type loose-end --title "..." [--problem P-001] [--claim C-...] [--priority 3]
                                       [--family-required any]

A claim is the remote branch task/<id>. Creating a branch is atomic on the server, so two agents cannot
both claim the same task. A claim whose last commit is older than the task's lease_hours is stale and is
shown as takeable.
"""
import argparse
import datetime
import re
import subprocess
import sys
from common import ROOT, docs


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    return r


def has_remote():
    return git("remote", "get-url", "origin", check=False).returncode == 0


def remote_claims():
    """Map task id -> (age_hours, last_author) for remote branches task/<id>."""
    out = {}
    if not has_remote():
        return out
    git("fetch", "--prune", "origin", check=False)
    r = git("for-each-ref", "--format=%(refname:short)|%(committerdate:unix)|%(authorname)",
            "refs/remotes/origin/task", check=False)
    now = datetime.datetime.now().timestamp()
    for line in r.stdout.splitlines():
        ref, ts, author = line.split("|", 2)
        out[ref.split("task/", 1)[1]] = ((now - float(ts)) / 3600.0, author)
    return out


def allowed(family_required, family):
    fr = str(family_required)
    if fr == "any" or family is None:
        return True
    if fr.startswith("not-"):
        return fr[4:] != family
    return fr == family


def blocked_by_independence(meta, family, claims):
    """Verification and audit must not be done by the proposer's family."""
    if meta.get("type") in {"verify", "audit"} and meta.get("claim") in claims and family:
        return claims[meta["claim"]].get("proposer_family") == family
    return False


def open_tasks(family=None, types=None):
    claims = {m["id"]: m for _, m, _ in docs("claims")}
    held = remote_claims()
    rows = []
    for path, m, _ in docs("tasks"):
        if m["status"] != "open":
            continue
        if types and m["type"] not in types:
            continue
        holder = held.get(str(m["id"]))
        stale = bool(holder and holder[0] > float(m.get("lease_hours", 8)))
        ok = allowed(m["family_required"], family) and not blocked_by_independence(m, family, claims)
        rows.append({"m": m, "holder": holder, "stale": stale, "ok": ok})
    rows.sort(key=lambda r: (r["m"]["priority"], str(r["m"]["id"])))
    return rows


def cmd_list(args):
    for r in open_tasks(args.family):
        m, h = r["m"], r["holder"]
        state = "free" if not h else (f"STALE claim by {h[1]} ({h[0]:.0f} h)" if r["stale"] else f"claimed by {h[1]} ({h[0]:.1f} h)")
        note = "" if r["ok"] else "  [not for this family]"
        print(f"{m['id']:<28} p{m['priority']} {m['type']:<16} {m['family_required']:<11} {state}{note}\n    {m['title']}")


def cmd_next(args):
    n = 0
    types = set(args.types.split(",")) if args.types else None
    for r in open_tasks(args.family, types):
        if r["ok"] and (not r["holder"] or r["stale"]):
            m = r["m"]
            print(f"{m['id']}  p{m['priority']} {m['type']}  {m['title']}" + ("  (stale claim, takeover allowed)" if r["stale"] else ""))
            n += 1
            if n >= args.n:
                break
    if n == 0:
        print("no task available for this family; create an explore task within the policy budget")


def cmd_claim(args):
    ids = {str(m["id"]): m for _, m, _ in docs("tasks")}
    if args.id not in ids:
        sys.exit(f"unknown task {args.id}")
    if ids[args.id]["status"] != "open":
        sys.exit(f"task {args.id} is {ids[args.id]['status']}")
    branch = f"task/{args.id}"
    if not has_remote():
        git("checkout", "-b", branch)
        print(f"no remote configured; created local branch {branch}")
        return
    git("fetch", "origin")
    held = remote_claims().get(args.id)
    lease = float(ids[args.id].get("lease_hours", 8))
    if held and held[0] <= lease:
        sys.exit(f"{args.id} is claimed by {held[1]} ({held[0]:.1f} h ago); pick another task")
    if held:
        git("checkout", "-B", branch, f"origin/{branch}")
        git("commit", "--allow-empty", "-m", f"{args.id}: stale claim taken over by {args.agent}")
        r = git("push", "origin", branch, check=False)
    else:
        git("checkout", "-b", branch, "origin/main")
        git("commit", "--allow-empty", "-m", f"{args.id}: claimed by {args.agent}")
        r = git("push", "-u", "origin", branch, check=False)
    if r.returncode != 0:
        git("checkout", "main", check=False)
        git("branch", "-D", branch, check=False)
        sys.exit(f"claim failed (someone else got there first): {r.stderr.strip()}")
    print(f"claimed {args.id} on branch {branch}")


def cmd_release(args):
    r = git("push", "origin", "--delete", f"task/{args.id}", check=False)
    print("released" if r.returncode == 0 else f"could not release: {r.stderr.strip()}")


def cmd_new(args):
    today = datetime.date.today().strftime("%Y%m%d")
    agent = re.sub(r"[^A-Za-z0-9.-]", "", args.agent)
    existing = {p.name for p in (ROOT / "tasks").glob(f"T-{today}-{agent}-*.md")}
    n = len(existing) + 1
    tid = f"T-{today}-{agent}-{n:02d}"
    slug = re.sub(r"[^a-z0-9]+", "-", args.title.lower()).strip("-")[:40]
    title = args.title.replace('"', "'")
    text = f"""---
id: {tid}
title: "{title}"
type: {args.type}
status: open
priority: {args.priority}
problem: {args.problem or 'null'}
claim: {args.claim or 'null'}
family_required: {args.family_required}
lease_hours: {args.lease_hours}
created_by: {args.agent}
created: {datetime.date.today().isoformat()}
---

## Goal

{args.goal or 'TODO: what done looks like.'}

## Context

## Deliverables
"""
    path = ROOT / "tasks" / f"{tid}-{slug}.md"
    path.write_text(text, encoding="utf-8")
    print(path.relative_to(ROOT))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list"); s.add_argument("--family"); s.set_defaults(f=cmd_list)
    s = sub.add_parser("next"); s.add_argument("--family", required=True); s.add_argument("-n", type=int, default=5)
    s.add_argument("--types", help="comma-separated task types to restrict to"); s.set_defaults(f=cmd_next)
    s = sub.add_parser("claim"); s.add_argument("id"); s.add_argument("--agent", required=True); s.set_defaults(f=cmd_claim)
    s = sub.add_parser("release"); s.add_argument("id"); s.set_defaults(f=cmd_release)
    s = sub.add_parser("new")
    s.add_argument("--agent", required=True); s.add_argument("--type", required=True); s.add_argument("--title", required=True)
    s.add_argument("--problem"); s.add_argument("--claim"); s.add_argument("--priority", type=int, default=3)
    s.add_argument("--family-required", default="any"); s.add_argument("--lease-hours", type=int, default=8)
    s.add_argument("--goal"); s.set_defaults(f=cmd_new)
    args = ap.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
