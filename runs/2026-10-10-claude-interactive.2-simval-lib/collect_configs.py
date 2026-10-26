"""Write config.md in each run folder: the exact commands that produced the raw outputs present in its raw-data folder."""
import os, re, glob

H = os.path.expanduser("~")
RUNS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = H + "/analytical-nl-discovery-data/"
Q = RAW + "2026-10-10-claude-interactive.2-scratch/queueA.txt"

# commands run outside the shared queue (sequential bash chains started at 10:07-10:10)
extra = []
for case, n, seed in (("kerr_ns0.5", 2000, 101), ("kerr_ns1.0", 1500, 102), ("kerr_vac", 1000, 103), ("kerr_ase", 1000, 104)):
    extra.append(f"julia --project=solver runs/2026-10-10-claude-interactive.2-gain-noise-mc/mc.jl {case} {n} {seed} "
                 f"{RAW}2026-10-10-claude-interactive.2-gain-noise-mc/{case}.csv")
ct = "runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl"
d = RAW + "2026-10-10-claude-interactive.2-moment-noise/"
for e in ("0.1",):
    for c in ("main", "heldout"):
        for u in (2, 4, 6):
            extra.append(f"julia --project=solver {ct} {c} {e} {u} all {d}{c}_e{e}_g{u}_all.json")
    for u in (2, 4, 6, 8):
        extra.append(f"julia --project=solver {ct} asym {e} {u} all {d}asym_e{e}_g{u}_all.json")
for c in ("main", "heldout", "asym"):
    for u in (2, 4, 6):
        extra.append(f"julia --project=solver {ct} {c} 0.05 {u} all {d}{c}_e0.05_g{u}_all.json")
extra.append(f"julia --project=solver {ct} asym 0.05 8 TW {d}asym_e0.05_g8_TW.json")
for c in ("p8", "p8_lin", "p8_ss"):
    extra.append(f"julia --project=solver {ct} {c} 0 0 all {d}{c}_all.json")
for u in (2, 4):
    extra.append(f"julia --project=solver {ct} main 0.025 {u} TW {d}main_e0.025_g{u}_TW.json")

lines = [l for l in open(Q).read().splitlines() if l.strip() and l.strip() != "true"]
lines = [re.sub(r"^cd \S+ && JULIA_NUM_THREADS=2 ", "", l).replace(H + "/agent-work/claude-val/", "") for l in lines] + extra

for run in sorted(glob.glob(RUNS + "/2026-10-10-claude-interactive.2-*")):
    rid = os.path.basename(run)
    rawdir = RAW + rid + "/"
    if not os.path.isdir(rawdir):
        continue
    present = set(os.listdir(rawdir))
    used = []
    for l in lines:
        m = re.search(re.escape(rawdir) + r"(\S+)", l)
        if m and m.group(1) in present and l not in used:
            used.append(l)
    with open(os.path.join(run, "config.md"), "w") as f:
        f.write(f"# Configuration of run {rid}\n\n")
        f.write("All commands run from the repository root with `JULIA_NUM_THREADS=2` and the solver submodule at "
                "b9fa957 (agents' copy, unmodified). Arguments are documented at the top of each script. Seeds: the "
                "Monte Carlo seeds are the third argument of `mc.jl`; all other runs are deterministic.\n\n")
        f.write(f"Raw outputs: `{rawdir.replace(H, '~')}` on the Apple M5 laptop. Commands whose output exists there:\n\n```\n")
        for l in sorted(used):
            f.write(l.replace(H, "~") + "\n")
        f.write("```\n")
        if rid.endswith("gain-noise-mc"):
            f.write("\nThe kerr_vac and kerr_ase chains were stopped at 734 and 882 trajectories (10:34, two-process limit). "
                    "kerr_ns1.0 combines kerr_ns1.0.csv (seed 102, 1500) and kerr_ns1.0_b.csv (seed 202, 1000). "
                    "Each CSV line is one trajectory: index, photon number, T_c (ps), Omega_c (rad/ps).\n")
    print(rid, len(used))
