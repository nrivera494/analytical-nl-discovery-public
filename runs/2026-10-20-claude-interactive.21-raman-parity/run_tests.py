"""Driver for the pre-registered tests P1-P3 (see predictions.md).

usage: python run_tests.py predict          -> closed-form predictions only (predictions.json)
       python run_tests.py P1|P2|P3|conv     -> simulations; results appended to results/*.json
Raw per-realization arrays go to ~/analytical-nl-discovery-data/<run-id>/.
"""
import json
import os
import sys
import time

import numpy as np

from mmfield import Model, launch, mirror, first_order_slope

RUN_ID = "2026-10-20-claude-interactive.21-raman-parity"
RAW = os.path.expanduser("~/analytical-nl-discovery-data/" + RUN_ID)
os.makedirs(RAW, exist_ok=True)
os.makedirs("results", exist_ok=True)
cfg = json.load(open("config.json"))
B = cfg["base"]


def make_model(**over):
    p = dict(B)
    p.update(over)
    return Model(N=p["N"], dt=p["dt_ps"], gamma=p["gamma_perWm"], fR=p["fR"], tau1=p["tau1_ps"],
                 tau2=p["tau2_ps"], omega0=p["omega0_radps"], dbeta=p["dbeta_perm"],
                 beta2=p["beta2_ps2perm"], b1=p["b1_psperm"], s=p["s"], lam=p["lam"], Dd=p["Dd_perm"])


def propagate(model, B0, nsteps, dz, gseq, save_every):
    Bz = B0.copy()
    rec = [model.photon(Bz)]
    for n in range(nsteps):
        Bz = model.step(Bz, dz, gseq[n])
        if (n + 1) % save_every == 0:
            rec.append(model.photon(Bz))
    return Bz, np.array(rec)


def predict():
    out = {}
    for name, case in cfg["P2"].items():
        m = make_model(s=case["s"], lam=1.0, N=case.get("N", B["N"]))
        _, dens = launch(np.random.default_rng(0), 1, m.N, m.dt, case["powers_W"], case["sigma_radps"],
                         case["centre_radps"], photon_symmetric=case["photon_symmetric"], omega0=B["omega0_radps"])
        slope = first_order_slope(m, dens)
        W = m.W
        cen = [np.sum(W * dens[p]) / np.sum(dens[p]) for p in range(3)]
        out[name] = dict(slope_W_per_m=slope.tolist(), energy_centroids_radps=cen,
                         total=float(slope.sum()))
    json.dump(out, open("predictions.json", "w"), indent=1)
    print(json.dumps(out, indent=1))


def run_P1():
    """Exact time-reversal identity, trajectory by trajectory."""
    c = cfg["P1"]
    rng = np.random.default_rng(c["seed"])
    B0, _ = launch(rng, c["R"], B["N"], B["dt_ps"], c["powers_W"], c["sigma_radps"], c["centre_radps"])
    g = rng.standard_normal((c["nsteps"], 3))
    res = []
    for lam, s, b1 in c["cases"]:
        mA = make_model(lam=lam, s=s, b1_psperm=b1)
        mB = make_model(lam=-lam, s=-s, b1_psperm=-b1)
        BA, _ = propagate(mA, B0, c["nsteps"], c["dz_m"], g, c["nsteps"])
        BB, _ = propagate(mB, mirror(B0), c["nsteps"], c["dz_m"], g, c["nsteps"])
        dev = np.max(np.abs(mirror(BA) - BB)) / np.max(np.abs(BA))
        nA, nB = mA.photon(BA), mB.photon(BB)
        res.append(dict(lam=lam, s=s, b1=b1, max_rel_field_dev=float(dev),
                        max_rel_photon_dev=float(np.max(np.abs(nA - nB) / nA)),
                        photon_change_rel=float(np.max(np.abs(nA - mA.photon(B0)) / mA.photon(B0)))))
        print(res[-1], flush=True)
    json.dump(res, open("results/P1.json", "w"), indent=1)


def run_P2():
    """Initial slope of the lam-odd part of <N~_p> against the closed form."""
    out = {}
    for name, case in cfg["P2"].items():
        mp = make_model(s=case["s"], lam=1.0)
        mm = make_model(s=case["s"], lam=-1.0)
        rng = np.random.default_rng(case["seed"])
        est = []
        t0 = time.time()
        for b in range(case["batches"]):
            B0, dens = launch(rng, case["R"], B["N"], B["dt_ps"], case["powers_W"], case["sigma_radps"],
                              case["centre_radps"], photon_symmetric=case["photon_symmetric"],
                              omega0=B["omega0_radps"])
            g = np.zeros((case["nsteps"], 3))   # disorder off for the slope test
            Bp, _ = propagate(mp, B0, case["nsteps"], case["dz_m"], g, case["nsteps"])
            Bm, _ = propagate(mm, B0, case["nsteps"], case["dz_m"], g, case["nsteps"])
            z1 = case["nsteps"] * case["dz_m"]
            est.append((mp.photon(Bp) - mm.photon(Bm)) / (2 * z1))
        est = np.concatenate(est)
        np.save(os.path.join(RAW, "P2_%s_estimates.npy" % name), est)
        mean, se = est.mean(0), est.std(0, ddof=1) / np.sqrt(est.shape[0])
        out[name] = dict(n=int(est.shape[0]), mean_W_per_m=mean.tolist(), se_W_per_m=se.tolist(),
                         wall_s=time.time() - t0)
        print(name, out[name], flush=True)
    json.dump(out, open("results/P2.json", "w"), indent=1)


def run_P3(tag="P3", over=None, lams=None, svals=None, R=None, nsteps=None, dz=None):
    """Finite-z decomposition of <N~_p>(lam) into lam-odd and lam-even parts; mirror pairs."""
    c = dict(cfg["P3"])
    over = over or {}
    lams = lams if lams is not None else c["lams"]
    svals = svals if svals is not None else c["svals"]
    R = R or c["R_base"]
    nsteps = nsteps or c["nsteps"]
    dz = dz or c["dz_m"]
    rng = np.random.default_rng(c["seed"])
    N = over.get("N", B["N"])
    fresh = over.pop("fresh_launch", False) if over else False
    B0, dens = launch(rng, R, N if fresh else B["N"], B["dt_ps"], c["powers_W"], c["sigma_radps"], c["centre_radps"])
    if N != B["N"] and not fresh:  # finer time grid, same window: embed the coarse spectrum (zero padding)
        N0 = B["N"]
        Bf = np.zeros(B0.shape[:2] + (N,), complex)
        Bf[..., :N0 // 2] = B0[..., :N0 // 2]
        Bf[..., N - N0 // 2 + 1:] = B0[..., N0 // 2 + 1:]
        B0 = Bf
    g_coarse = rng.standard_normal((c["nsteps"], 3))
    refine = c["nsteps"] // nsteps if nsteps < c["nsteps"] else 1
    if nsteps > c["nsteps"]:  # Brownian refinement: each coarse increment split into two halves
        k = nsteps // c["nsteps"]
        assert k == 2
        rng2 = np.random.default_rng(c["seed"] + 99)
        u = rng2.standard_normal((c["nsteps"], 3))
        ga = (g_coarse + u) / np.sqrt(2)
        gb = (g_coarse - u) / np.sqrt(2)
        g = np.empty((nsteps, 3))
        g[0::2], g[1::2] = ga, gb
    else:
        g = g_coarse
    Ball = np.concatenate([B0, mirror(B0)], axis=0)    # base realizations then their mirrors
    out = {"R_base": R, "nsteps": nsteps, "dz_m": dz, "over": over, "runs": {}}
    save_every = nsteps // c["nsave"]
    for s in svals:
        for lam in lams:
            m = make_model(s=s, lam=lam, **over)
            t0 = time.time()
            _, rec = propagate(m, Ball, nsteps, dz, g, save_every)
            np.save(os.path.join(RAW, "%s_s%g_lam%g_photon.npy" % (tag, s, lam)), rec)
            out["runs"]["s%g_lam%g" % (s, lam)] = dict(wall_s=time.time() - t0)
            print(tag, s, lam, "done in %.0f s" % (time.time() - t0), flush=True)
    json.dump(out, open("results/%s_meta.json" % tag, "w"), indent=1)


if __name__ == "__main__":
    what = sys.argv[1]
    if what == "predict":
        predict()
    elif what == "P1":
        run_P1()
    elif what == "P2":
        run_P2()
    elif what == "P3":
        run_P3()
    elif what == "P3s05":
        run_P3(tag="P3s05", lams=[-1.0, 1.0], svals=[0.5])
    elif what == "conv_dz":
        c = cfg["P3"]
        run_P3(tag="conv_dz", lams=[-1.0, 0.0, 1.0], svals=[1], nsteps=2 * c["nsteps"], dz=c["dz_m"] / 2)
    elif what == "conv_window":  # post hoc (not pre-registered): doubled window, same dt, fresh realizations
        run_P3(tag="conv_window", over={"N": 2 * B["N"], "fresh_launch": True}, lams=[-1.0, 0.0, 1.0], svals=[1])
    elif what == "conv_dt":
        run_P3(tag="conv_dt", over={"N": 2 * B["N"], "dt_ps": B["dt_ps"] / 2}, lams=[-1.0, 0.0, 1.0], svals=[1])
