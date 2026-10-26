#!/usr/bin/env python3
"""Fail if this branch edits generated files relative to a base ref (AGENTS.md rule 8).

  check_generated.py origin/main

Generated files are rebuilt on main by .github/workflows/rebuild-generated.yml.
"""
import re
import subprocess
import sys
from common import ROOT

WHOLE_FILES = ["problems/INDEX.md", "results/RANKING.md"]
BLOCK = re.compile(r"<!-- DASHBOARD:START -->.*?<!-- DASHBOARD:END -->", re.S)


def show(ref, path):
    r = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def dashboard(text):
    m = BLOCK.search(text or "")
    return m.group(0) if m else None


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    r = subprocess.run(["git", "merge-base", base, "HEAD"], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"cannot find merge base with {base}: {r.stderr.strip()}")
    mb = r.stdout.strip()
    bad = [p for p in WHOLE_FILES if show(mb, p) != show("HEAD", p)]
    if dashboard(show(mb, "STATUS.md")) != dashboard(show("HEAD", "STATUS.md")):
        bad.append("STATUS.md (dashboard block)")
    if bad:
        print("This branch edits generated files. Revert these changes; CI rebuilds them after merge:")
        print("\n".join(f"  {p}" for p in bad))
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
