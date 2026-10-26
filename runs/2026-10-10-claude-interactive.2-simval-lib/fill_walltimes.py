"""Fill wall_time_s in each run's meta.yaml from the recorded per-job timings in the raw outputs."""
import os, glob, json, re

H = os.path.expanduser("~")
RUNS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = H + "/analytical-nl-discovery-data/"


def total(run):
    t = 0.0; n = 0
    for p in glob.glob(RAW + run + "/*.json"):
        try:
            d = json.load(open(p))
        except Exception:
            continue
        if "t_forward_s" in d:
            t += d["t_forward_s"] + sum(d.get("t_adjoint_s", []) or [0]); n += 1
        elif "t_total_s" in d:
            t += d["t_total_s"]; n += 1
    return t, n


for run in sorted(glob.glob(RUNS + "/2026-10-10-claude-interactive.2-*")):
    rid = os.path.basename(run)
    meta = os.path.join(run, "meta.yaml")
    s = open(meta).read()
    if rid.endswith("gain-noise-mc"):
        ntraj = sum(sum(1 for _ in open(p)) for p in glob.glob(RAW + rid + "/*.csv"))
        val = f"about {int(0.75 * ntraj)} s for {ntraj} Monte Carlo trajectories (0.6-0.9 s each, one process), plus about 60 s for mc_adjoint.jl"
    elif rid.endswith("simval-lib"):
        val = "n/a (code only)"
    else:
        t, n = total(rid)
        val = f"{int(t)} s summed over {n} jobs (solver time recorded in each raw output; Julia start-up of about 6 s per job not included)"
    s = re.sub(r'wall_time_s: ".*"', f'wall_time_s: "{val}"', s)
    open(meta, "w").write(s)
    print(rid, val)
