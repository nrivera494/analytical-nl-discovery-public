"""Read-only scientific provenance checks. gpt-c / gpt-6-astra / gpt."""
import hashlib
import json
import re
import struct
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FREEZE = "b042d48fd03e65791b577d869b585e36fd48b07f"
SOLVER = "b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    checks = {}
    frozen = {}
    for name in ["predictions.md", "material.py", "independent.py", "zs_shoot.c"]:
        path = HERE / name
        original = git("show", f"{FREEZE}:{path.relative_to(ROOT)}")
        current = path.read_bytes()
        frozen[name] = {"sha256": sha(current), "unchanged": original == current}
    checks["frozen_prediction_and_primary_code_unchanged"] = all(
        row["unchanged"] for row in frozen.values()
    )

    preserved = json.loads(
        (HERE.parent / "2026-10-17-gpt-c-raman-sharpening" /
         "preserved_claim_sections.json").read_text()
    )
    claim_text = (ROOT / "claims" / preserved["claim"]).read_text()
    protected = {}
    for heading, expected in preserved["original_sections"].items():
        # The original manifest omits the separating newline before the next ##.
        content = re.search(
            rf"^## {re.escape(heading)}\n(.*?)(?=\n## |\Z)",
            claim_text, re.M | re.S
        )[1].encode()
        protected[heading] = {
            "sha256": sha(content), "bytes": len(content),
            "unchanged": sha(content) == expected["sha256"]
                         and len(content) == expected["bytes"]
        }
    checks["original_claim_sections_unchanged"] = all(
        row["unchanged"] for row in protected.values()
    )

    inventory = json.loads((HERE / "inventory.json").read_text())
    summary = json.loads((HERE / "summary.json").read_text())
    accuracy = json.loads((HERE / "accuracy.json").read_text())
    cases = [json.loads((HERE / (r["id"] + ".json")).read_text())
             for r in inventory["cases"]]
    checks["all_cases_record_original_prediction_freeze"] = all(
        c["predictions_commit"] == FREEZE for c in cases
    )
    checks["all_cases_record_frozen_forward_hash"] = all(
        c["implementation_sha256"] == frozen["independent.py"]["sha256"]
        for c in cases
    )
    checks["all_planned_material_cases_attempted"] = (
        inventory["counts"] == {"complete": 149, "edge-terminated": 2}
    )
    checks["all_eight_peaks_bracketed"] = summary["all_eight_peaks_bracketed"]
    scores = [s for p in summary["peaks"] for s in p["scores"].values()]
    checks["all_40_prediction_scores_resolved"] = (
        len(scores) == 40 and all(s["verdict"] in ["pass", "fail"] for s in scores)
    )
    checks["all_numerical_controls_pass"] = summary["all_numerical_checks_pass"]
    checks["accuracy_script_matches_executed_hash"] = (
        sha((HERE / "numerical_checks.py").read_bytes()) == accuracy["script_sha256"]
    )
    checks["summary_contains_current_accuracy"] = summary["accuracy"] == accuracy
    checks["source_shooting_matches_phase1"] = (
        (HERE / "zs_shoot.c").read_bytes()
        == (HERE.parent / "2026-10-17-gpt-c-raman-sharpening" / "zs_shoot.c").read_bytes()
    )
    checks["task_branch"] = git("branch", "--show-current").decode().strip() == (
        "task/T-20261017-gpt-c-01"
    )
    checks["solver_pin_and_worktree_unchanged"] = (
        git("-C", "solver", "rev-parse", "HEAD").decode().strip() == SOLVER
        and not git("-C", "solver", "status", "--porcelain").strip()
    )
    ancestry = {}
    for key, value in summary["freeze_commits"].items():
        if "commit" in key:
            ancestry[key] = subprocess.run(
                ["git", "merge-base", "--is-ancestor", value, "HEAD"],
                cwd=ROOT, check=False
            ).returncode == 0
    checks["all_design_freezes_are_committed_ancestors"] = all(ancestry.values())

    figures = {}
    for name in ["fig_summary.png", "fig_position.png"]:
        data = (HERE / name).read_bytes()
        width, height = struct.unpack(">II", data[16:24])
        figures[name] = {"width": width, "height": height,
                         "bytes": len(data), "sha256": sha(data)}
    checks["figures_single_panel_size_budget"] = all(
        r["bytes"] < 250_000 and (r["width"], r["height"]) == (720, 540)
        for r in figures.values()
    )
    changed = git("diff", "--name-only", "origin/main", "--", "runs").decode().splitlines()
    checks["no_raw_field_files_in_run_diff"] = not any(
        Path(name).suffix.lower() in [".npz", ".npy", ".csv", ".h5", ".hdf5", ".jld2", ".so"]
        for name in changed
    )
    result = {
        "agent": "gpt-c", "model": "gpt-6-astra", "family": "gpt",
        "run_id": HERE.name, "checked_utc": datetime.now(timezone.utc).isoformat(),
        "checks": checks, "all_pass": all(checks.values()),
        "frozen_files": frozen, "protected_original_sections": protected,
        "freeze_ancestry": ancestry, "figures": figures,
        "visual_check": "Both final single-panel figures inspected by gpt-c on 2026-10-17."
    }
    (HERE / "integrity.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checks": checks, "all_pass": result["all_pass"]}, indent=2))
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
