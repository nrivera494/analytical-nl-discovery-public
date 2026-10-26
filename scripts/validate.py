#!/usr/bin/env python3
"""Check that problems, claims, tasks and results follow the schema and the project rules.

Exit status 0 if clean, 1 if any error. Run before every push; CI runs it on every pull request.
"""
import re
import sys
from common import RESULT_TIERS, ROOT, docs, read_doc, result_dirs

errors = []


def err(path, msg):
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def require(path, meta, fields):
    for f in fields:
        if f not in meta:
            err(path, f"missing field '{f}'")


def enum(path, meta, field, allowed):
    if field in meta and meta[field] not in allowed:
        err(path, f"{field}={meta[field]!r} not in {sorted(map(str, allowed))}")


def id_matches(path, meta, prefix):
    i = str(meta.get("id", ""))
    if not re.fullmatch(prefix + r"-[A-Za-z0-9.\-]+", i):
        err(path, f"bad id {i!r}")
    stem = path.parent.name if path.name == "RESULT.md" else path.stem
    if not stem.startswith(i):
        err(path, f"name does not start with id {i!r}")
    return i


P_STATUS = {"candidate", "audited", "active", "parked", "demoted", "solved"}
P_LIT = {"unaudited", "open", "partial", "largely-solved"}
C_STATUS = ["proposed", "cheap-checks-passed", "sim-verified", "audited", "promoted", "refuted", "withdrawn"]
T_STATUS = {"open", "done", "blocked", "cancelled"}
T_TYPE = {"registry-review", "literature", "derive", "verify", "audit", "explore", "loose-end", "rank", "infra"}
T_FAMILY = re.compile(r"any|not-[a-z0-9]+|[a-z0-9]+")
P_SECTIONS = ["Target quantity", "Literature state", "Sharpest statement of the gap", "Oracle", "Audit trail"]
C_SECTIONS = ["Statement", "Regime", "Assumptions", "Predictions", "Checks"]
R_SECTIONS = ["Problem", "Result", "Regime of validity", "Derivation", "Validation against numerics",
              "Adversarial audit", "Novelty", "Experimental test"]
R_TOP = {"README.md", "RANKING.md", "weights.yaml", "_TEMPLATE", *RESULT_TIERS}
GATES = [f"G{k}" for k in range(1, 8)]
GATE_STATES = {"met", "open", "n/a"}
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
FORMAL_FIELDS = ["project", "library", "theorems", "toolchain", "mathlib_commit", "axioms",
                 "formalizer", "formalizer_family", "auditor", "auditor_family", "audit_run"]


def has_sections(path, body, names):
    for n in names:
        if not re.search(r"^##\s+(\d+\.\s+)?" + re.escape(n) + r"\s*$", body, re.M):
            err(path, f"missing section '{n}'")


def main():
    problems, claims = {}, {}
    seen = {}

    def unique(path, i):
        if i in seen:
            err(path, f"duplicate id {i} (also {seen[i].relative_to(ROOT)})")
        seen[i] = path

    for folder, bucket in (("problems", "P"), ("claims", "C"), ("tasks", "T")):
        try:
            items = list(docs(folder))
        except ValueError as e:
            errors.append(f"{folder}: {e}")
            continue
        for path, meta, body in items:
            i = id_matches(path, meta, bucket)
            unique(path, i)
            if bucket == "P":
                problems[i] = meta
                require(path, meta, ["title", "status", "priority", "literature_state", "novelty_confidence",
                                     "target_quantity", "model", "oracle_ready", "audited_by", "claims", "results"])
                enum(path, meta, "status", P_STATUS)
                enum(path, meta, "literature_state", P_LIT)
                enum(path, meta, "novelty_confidence", {"low", "medium", "high"})
                enum(path, meta, "oracle_ready", {"available", "partial", "missing"})
                enum(path, meta, "priority", {1, 2, 3, 4, 5})
                has_sections(path, body, P_SECTIONS)
                fams = meta.get("audited_by") or []
                if meta.get("status") in {"audited", "active"} and len(set(fams)) < 2:
                    err(path, f"status {meta['status']} needs literature review by two families (audited_by={fams})")
                if meta.get("status") in {"audited", "active"} and meta.get("literature_state") == "unaudited":
                    err(path, "audited problem cannot have literature_state unaudited")
            elif bucket == "C":
                claims[i] = meta
                require(path, meta, ["problem", "title", "type", "status", "proposed_by", "proposer_family", "created"])
                enum(path, meta, "status", set(C_STATUS))
                has_sections(path, body, C_SECTIONS)
                st = meta.get("status")
                pf = meta.get("proposer_family")
                if st in {"sim-verified", "audited", "promoted"}:
                    vf = meta.get("verifier_family")
                    if not vf:
                        err(path, f"status {st} requires verifier_family")
                    elif vf == pf:
                        err(path, "verifier_family must differ from proposer_family")
                    if not meta.get("solver_commit"):
                        err(path, f"status {st} requires solver_commit")
                af = meta.get("auditor_family")
                if st == "audited" and not af:
                    err(path, "status audited requires auditor_family")
                if af and af == pf:
                    err(path, "auditor_family must differ from proposer_family")
                if st == "promoted" and not meta.get("result"):
                    err(path, "promoted claim must name its result")
            else:
                require(path, meta, ["title", "type", "status", "priority", "family_required", "lease_hours", "created_by"])
                enum(path, meta, "status", T_STATUS)
                enum(path, meta, "type", T_TYPE)
                if not T_FAMILY.fullmatch(str(meta.get("family_required", ""))):
                    err(path, "bad family_required")

    # cross references
    for path, meta, _ in docs("claims"):
        if meta.get("problem") not in problems:
            err(path, f"unknown problem {meta.get('problem')!r}")
    for path, meta, _ in docs("problems"):
        for c in meta.get("claims") or []:
            if c not in claims:
                err(path, f"lists unknown claim {c}")
    for path, meta, _ in docs("tasks"):
        if meta.get("problem") and meta["problem"] not in problems:
            err(path, f"unknown problem {meta['problem']!r}")
        if meta.get("claim") and meta["claim"] not in claims:
            err(path, f"unknown claim {meta['claim']!r}")

    # results: results/<tier>/R-NNNN-name/, tier in RESULT_TIERS (docs/PROMOTION.md)
    for entry in sorted((ROOT / "results").iterdir()):
        if entry.name not in R_TOP and not entry.name.startswith("."):
            errors.append(f"{entry.relative_to(ROOT)}: results go in results/promising/ or results/formalized/")
    result_ids = set()
    for d in result_dirs():
        rp = d / "RESULT.md"
        if not rp.exists():
            errors.append(f"{d.relative_to(ROOT)}: missing RESULT.md")
            continue
        try:
            meta, body = read_doc(rp)
        except ValueError as e:
            err(rp, str(e))
            continue
        i = id_matches(rp, meta, "R")
        unique(rp, i)
        result_ids.add(i)
        tier = d.parent.name
        require(rp, meta, ["title", "claim", "problem", "tier", "status", "gates", "proposer_family",
                           "verifier_family", "auditor_family", "solver_commit"])
        enum(rp, meta, "status", {"under-review", "accepted", "retracted"})
        if meta.get("tier") != tier:
            err(rp, f"tier={meta.get('tier')!r} but the folder is in results/{tier}/")
        sections = R_SECTIONS + (["Formal verification"] if tier == "formalized" else [])
        has_sections(rp, body, sections)
        c = meta.get("claim")
        if c not in claims:
            err(rp, f"unknown claim {c!r}")
        elif claims[c].get("status") not in {"sim-verified", "audited", "promoted"}:
            err(rp, f"claim {c} is {claims[c].get('status')!r}; a result needs a cross-family verified claim")
        if meta.get("problem") not in problems:
            err(rp, f"unknown problem {meta.get('problem')!r}")
        pf = meta.get("proposer_family")
        if meta.get("verifier_family") == pf or meta.get("auditor_family") == pf:
            err(rp, "verifier and auditor families must differ from proposer family")
        gates = meta.get("gates") if isinstance(meta.get("gates"), dict) else {}
        if not isinstance(meta.get("gates"), dict):
            err(rp, "gates must map G1..G7 (and G8 for formalized results) to met, open or n/a")
        for g in GATES + ["G8"]:
            if g in gates and gates[g] not in GATE_STATES:
                err(rp, f"gates.{g}={gates[g]!r} not in {sorted(GATE_STATES)}")
        for g in GATES:
            if g not in gates:
                err(rp, f"gates.{g} missing")
        if gates.get("G4") != "met":
            err(rp, "gates.G4 must be met: every tier needs cross-family verification")
        if tier == "formalized" and gates.get("G8") != "met":
            err(rp, "a formalized result needs gates.G8 met")
        if tier == "promising" and gates.get("G8") == "met":
            err(rp, "gates.G8 is met: this result belongs in results/formalized/")
        if meta.get("status") == "accepted":
            for g in GATES:
                if gates.get(g) in {"open", "n/a"} and not re.search(rf"\b{g}\b", body):
                    err(rp, f"gates.{g} is {gates[g]}; say why in the body")
        imgs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", body)
        for img in imgs:
            if not (d / img).exists():
                err(rp, f"figure not found: {img}")
        if not imgs:
            err(rp, "needs at least one figure (docs/PROMOTION.md lists the four expected ones)")
        audits = list((d / "audit").glob("audit-*.md"))
        reports = audits + list((d / "audit").glob("verification-*.md"))
        if not reports:
            err(rp, "no cross-family report in audit/ (audit-*.md or verification-*.md)")
        if gates.get("G5") == "met" and not audits:
            err(rp, "gates.G5 is met but there is no adversarial audit report (audit/audit-*.md)")
        for a in reports:
            try:
                am, _ = read_doc(a)
            except ValueError as e:
                err(a, str(e))
                continue
            if am.get("family") == pf:
                err(a, "a report by the proposer's family does not count")
            enum(a, am, "verdict", {"pass", "pass-reduced-regime", "fail"})
        if tier == "formalized":
            fm = meta.get("formal") if isinstance(meta.get("formal"), dict) else None
            if fm is None:
                err(rp, "formalized result needs a 'formal' block")
                fm = {}
            require(rp, fm, FORMAL_FIELDS)
            if fm.get("formalizer_family") and fm.get("auditor_family") == fm.get("formalizer_family"):
                err(rp, "formal.auditor_family must differ from formal.formalizer_family")
            extra = set(fm.get("axioms") or []) - STANDARD_AXIOMS
            if extra:
                err(rp, f"formal.axioms beyond propext, Classical.choice, Quot.sound: {sorted(extra)}")
            proj = ROOT / str(fm.get("project", ""))
            lib = str(fm.get("library", ""))
            if not (proj / "lakefile.toml").exists():
                err(rp, f"formal.project {fm.get('project')!r} has no lakefile.toml")
            elif f'name = "{lib}"' not in (proj / "lakefile.toml").read_text():
                err(rp, f"library {lib!r} is not declared in {fm.get('project')}/lakefile.toml")
            else:
                src = "\n".join(f.read_text() for f in [proj / f"{lib}.lean", *(proj / lib).rglob("*.lean")]
                                if f.exists())
                for t in fm.get("theorems") or []:
                    short = str(t).split(".")[-1]
                    if not re.search(rf"^(theorem|lemma)\s+{re.escape(short)}\b", src, re.M):
                        err(rp, f"formal theorem {t} not found in {fm.get('project')}/{lib}")
            if fm.get("audit_run") and not (ROOT / "runs" / str(fm["audit_run"])).is_dir():
                err(rp, f"formal.audit_run {fm['audit_run']!r} not found under runs/")
            faudits = list((d / "audit").glob("formal-audit-*.md"))
            if not faudits:
                err(rp, "no formal audit report (audit/formal-audit-*.md)")
            for a in faudits:
                try:
                    am, _ = read_doc(a)
                except ValueError as e:
                    err(a, str(e))
                    continue
                if am.get("family") == fm.get("formalizer_family"):
                    err(a, "formal audit by the formalizer's family does not count")
                enum(a, am, "verdict", {"pass", "pass-reduced-regime", "fail"})
        if meta.get("status") == "accepted" and not (d / "repro" / "README.md").exists():
            err(rp, "accepted result needs repro/README.md")

    # promoted claims name results that exist
    for path, meta, _ in docs("claims"):
        if meta.get("status") == "promoted":
            named = meta.get("result")
            for r in (named if isinstance(named, list) else [named]):
                if r and str(r) not in result_ids:
                    err(path, f"names result {r} that is not under results/")

    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} error(s)")
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
