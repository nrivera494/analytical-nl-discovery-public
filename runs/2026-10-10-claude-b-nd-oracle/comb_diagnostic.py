"""Anatomy of the best binary filters at z/z_wb = 0.7 (claude-b, T-20261010-claude-interactive-05).
Splits each final filter (transfer stage) into the central part |v| < v_c (the comb; v = omega/N) and the rest (the
broad band), and reports F of each part alone, of both, the correlation coefficient of the two counts, and the comb
period from the spacing of on-runs against the fringe period from the minima of nbar in the same region.
Writes comb_diagnostic.json."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nd_cov as nd
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data")
out = {}
for run, tag in (("2026-10-10-claude-b-nd-oracle", "N10_zr0.7"), ("2026-10-10-claude-b-nd-oracle", "N14_zr0.7"),
                 ("2026-10-10-claude-b-nd-oracle", "N20_zr0.7"), ("2026-10-10-claude-b-nd-oracle", "N28_zr0.7"),
                 ("2026-10-10-claude-b-nd-heldout", "N40_zr0.7")):
    d = np.load(os.path.join(RAW, run, tag + ".npz"))
    C, nb = d["C"], d["nbar"]
    N = int(tag[1:3].rstrip("_"))
    v = d["w"][d["keep"]] / N
    T = np.load(os.path.join(RAW, run, tag + "_transfer.npz"))["T"].astype(float)
    res = {}
    for vc in (0.3, 0.4):
        Tc = T * (np.abs(v) < vc)
        Tb = T * (np.abs(v) >= vc)
        vc_c, vb = Tc @ C @ Tc, Tb @ C @ Tb
        cov = Tc @ C @ Tb
        res[str(vc)] = dict(F_both=nd.fano(T, C, nb), F_band=float(vb / (Tb @ nb)) if Tb.sum() else None,
                            F_comb=float(vc_c / (Tc @ nb)) if Tc.sum() else None,
                            corr=float(cov / np.sqrt(vc_c * vb)) if Tc.sum() and Tb.sum() else None,
                            photon_fraction_comb=float(nb[Tc > 0].sum() / nb.sum()),
                            photon_fraction_band=float(nb[Tb > 0].sum() / nb.sum()))
    # periods in the central region
    m = np.abs(v) < 0.35
    vv, nn, TT = v[m], nb[m], T[m]
    mins = vv[1:-1][(nn[1:-1] < nn[:-2]) & (nn[1:-1] < nn[2:])]
    starts = vv[1:][(TT[1:] > 0) & (TT[:-1] == 0)]
    res["fringe_period_v"] = float(np.median(np.diff(mins))) if len(mins) > 1 else None
    res["comb_period_v"] = float(np.median(np.diff(starts))) if len(starts) > 1 else None
    res["n_fringe_minima_central"] = int(len(mins))
    out[tag] = res
    print(tag, json.dumps(res), flush=True)
json.dump(out, open(os.path.join(HERE, "comb_diagnostic.json"), "w"), indent=1)
