#!/bin/bash
# Minimal shared job queue: each worker takes the next unclaimed line of $1 (one shell command per line).
# Claims are atomic via mkdir of <queue>.claims/<line number>.
Q="$1"
CL="$Q.claims"
mkdir -p "$CL"
while true; do
  n=$(wc -l < "$Q")
  got=""
  for i in $(seq 1 "$n"); do
    if mkdir "$CL/$i" 2>/dev/null; then got=$i; break; fi
  done
  [ -z "$got" ] && break
  cmd=$(sed -n "${got}p" "$Q")
  echo "[$(date +%H:%M:%S)] start $got: $cmd"
  bash -c "$cmd"
  echo "[$(date +%H:%M:%S)] end $got (exit $?)"
done
