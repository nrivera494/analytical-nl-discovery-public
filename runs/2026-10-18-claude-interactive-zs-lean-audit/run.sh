#!/usr/bin/env bash
# Cross-family audit of the ZSFormalization Lean library (formal/ZSFormalization).
# Agent: claude-interactive (claude-opus-5-5, family claude). Task: T-20261018-claude-interactive-04.
#
#   PYTHON=/path/to/python-with-mpmath bash runs/2026-10-18-claude-interactive-zs-lean-audit/run.sh
#
# Needs elan with leanprover/lean4:v4.35.0-rc4 and about 6 GB of disk for the Mathlib cache. Peak memory
# is about 3 GB (one Lean process at a time). Wall time is about 3 minutes once the cache is present.
# Small text outputs go to out/; the 378 MB nanoda export goes to the raw-data location in meta.yaml.
set -euo pipefail
RUN=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$RUN/../.." && pwd)
RAW="$HOME/analytical-nl-discovery-data/$(basename "$RUN")"
OUT="$RUN/out"
TC="$HOME/.elan/toolchains/leanprover--lean4---v4.35.0-rc4/bin"
PY="${PYTHON:-python3}"   # needs mpmath for step 11
export PATH="$HOME/.elan/bin:$PATH"
mkdir -p "$OUT" "$RAW"
cd "$ROOT/formal"

echo "1. Source hashes against the formalizer's record"
"$PY" - "$OUT/hashes.txt" <<'PY'
import hashlib, pathlib, sys
moved = {"README.md": "ZSFormalization/README.md", "Audit.lean": "ZSFormalization/verification/Audit.lean"}
superseded = {"lakefile.toml", "lake-manifest.json", "lean-toolchain", ".gitignore"}
lines, bad = [], 0
for row in pathlib.Path("ZSFormalization/verification/source-sha256.txt").read_text().split("\n"):
    if not row.strip():
        continue
    digest, name = row.split(None, 1)
    if name in superseded:
        lines.append(f"superseded by formal/{name}: {name}")
        continue
    here = moved.get(name, name)
    ok = hashlib.sha256(pathlib.Path(here).read_bytes()).hexdigest() == digest
    bad += not ok
    lines.append(f"{'ok' if ok else 'MISMATCH'}: {name} -> formal/{here}")
lines.append(f"mismatches: {bad}")
pathlib.Path(sys.argv[1]).write_text("\n".join(lines) + "\n")
print(lines[-1])
sys.exit(1 if bad else 0)
PY

echo "2. Dependency pins of formal/ against the formalizer's manifest (recorded in environment.json)"
"$PY" - "$OUT/pins.txt" <<'PY'
import json, sys
env = json.load(open("ZSFormalization/verification/environment.json"))["dependency_revisions_verified_against_checkouts"]
man = {p["name"]: p["rev"] for p in json.load(open("lake-manifest.json"))["packages"]}
rows = [f"{'ok' if man.get(k) == v else 'DIFFERENT'}: {k} {v}" for k, v in sorted(env.items())]
rows.append(f"different: {sum(r.startswith('DIFFERENT') for r in rows)}")
open(sys.argv[1], "w").write("\n".join(rows) + "\n")
print(rows[-1])
PY

echo "3. Build (Mathlib cache, then both libraries)"
lake exe cache get > /dev/null
lake build ZSFormalization AnalyticalNL > "$OUT/build.txt" 2>&1
grep -cE '^(warning|error)' "$OUT/build.txt" > "$OUT/build_warning_count.txt" || true
tail -1 "$OUT/build.txt"

echo "4. Each file compiled alone with default options: count of messages"
: > "$OUT/per_file_messages.txt"
for f in ZSFormalization/*.lean; do
  n=$(lake env lean "$f" 2>&1 | grep -c . || true)
  echo "$f $n" >> "$OUT/per_file_messages.txt"
done
awk '{s+=$2} END {print "total messages:", s}' "$OUT/per_file_messages.txt"

echo "5. Escape hatches in the sources"
grep -nE '\bsorry\b|\badmit\b|^axiom |native_decide|implemented_by|@\[extern|\bunsafe\b|\bopaque\b|set_option|^macro|^elab|run_cmd|ofReduceBool' \
  ZSFormalization/*.lean ZSFormalization.lean > "$OUT/escape_hatches.txt" || true
wc -l < "$OUT/escape_hatches.txt"

echo "6. Axioms of every theorem and lemma"
{ echo "import ZSFormalization"; grep -hoE '^(theorem|lemma) [^ ]+' ZSFormalization/*.lean | awk '{print "#print axioms ZS." $2}'; } > "$OUT/AxiomsAll.lean"
lake env lean "$OUT/AxiomsAll.lean" > "$OUT/axioms_all.txt" 2>&1
echo "declarations: $(grep -c '#print' "$OUT/AxiomsAll.lean"); standard three only: $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]' "$OUT/axioms_all.txt")"

echo "7. Lean's replay checker, module by module"
: > "$OUT/leanchecker.txt"
for m in Scalar BoundState Endpoints Moment FourierMajorant SpectralBound Sech SechSharpness Gaussian Corollaries Sources GaussianSource RealSech; do
  if lake env "$TC/leanchecker" "ZSFormalization.$m" >> "$OUT/leanchecker.txt" 2>&1; then echo "ok ZSFormalization.$m" >> "$OUT/leanchecker.txt"; else echo "FAIL ZSFormalization.$m" >> "$OUT/leanchecker.txt"; fi
done
lake env "$TC/leanchecker" ZSFormalization.NoSuchModule > /dev/null 2>&1 && echo "CONTROL FAILED: bogus module passed" >> "$OUT/leanchecker.txt" || echo "control ok: bogus module rejected" >> "$OUT/leanchecker.txt"
grep -c '^ok ' "$OUT/leanchecker.txt"

echo "8. Held-out certificates and statement printouts"
lake env lean "$RUN/AuditHeldOut.lean" > "$OUT/audit_heldout.txt" 2>&1
grep "depends on axioms" "$OUT/audit_heldout.txt"

echo "9. Negative control (must fail)"
if lake env lean "$RUN/NegControl.lean" > "$OUT/neg_control.txt" 2>&1; then echo "NEGATIVE CONTROL PASSED: certificates are vacuous" | tee -a "$OUT/neg_control.txt"; exit 1; else echo "failed as required"; fi

echo "10. Independent kernel (nanoda) on the dependency cone of the headline theorems"
lake env "$TC/leanexport" ZSFormalization -- ZS.canonical_integer_sech_optimality ZS.canonical_integer_sech_fraction_optimality \
  ZS.passive_source_eigenvalue_bound ZS.canonical_sech_polynomial_ceiling ZS.canonical_gaussian_ceiling \
  ZS.rational_sech_height_enclosure ZS.canonical_sech_five_halves_enclosure ZS.canonical_sech_nineteen_halves_enclosure \
  ZS.eigenvalue_even_moment_bound > "$RAW/headline.ndjson"
sed "s#@RAW@#$RAW#" "$RUN/nanoda.template.json" > "$RAW/nanoda.json"
"$TC/nanoda_bin" "$RAW/nanoda.json" > "$RAW/nanoda.out" 2>&1
tail -1 "$RAW/nanoda.out" | tee "$OUT/nanoda_result.txt"
cp "$RAW/nanoda.out" "$OUT/nanoda_output.txt"

echo "11. Gaussian ceilings implied by the even exponents (numerical, not Lean)"
"$PY" -W ignore "$RUN/gaussian_even_ceiling.py" > /dev/null
echo "wrote gaussian_even_ceiling.json"
