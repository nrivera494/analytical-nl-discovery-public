"""Where the best single interval puts its edges (claude-b, T-20261010-claude-interactive-05): recomputes the exhaustive
best interval on the stored count covariances and reports the edge positions v = omega/N, the mean photon number at the
edges relative to the maximum, and the photon fraction outside the band, at z/z_wb = 0.7 and 1.0. Tests the scaling
argument of the note (section 3c): edges should move to darker regions as N grows. Writes interval_edges.json."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nd_cov as nd
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data")
S = [p for p in json.load(open(os.path.join(HERE, "summary.json")))["points"] if p["s"] == 0 and p["resolved"]]
out = {}
for zr in (0.7, 1.0):
    for p in sorted([q for q in S if q["zr"] == zr], key=lambda q: q["N"]):
        d = np.load(os.path.join(RAW, p["run"], p["tag"] + ".npz"))
        C, nb, w = d["C"], d["nbar"], d["w"][d["keep"]]
        F, T = nd.best_interval(C, nb)
        on = np.where(T > 0)[0]
        i1, i2 = on[0], on[-1]
        res = dict(N=p["N"], F_interval=F, v_lo=float(w[i1] / p["N"]), v_hi=float(w[i2] / p["N"]),
                   nbar_edge_lo_rel=float(nb[i1] / nb.max()), nbar_edge_hi_rel=float(nb[i2] / nb.max()),
                   photon_fraction_outside=float(1 - nb[on].sum() / nb.sum()))
        out[p["tag"]] = res
        print(p["tag"], {k: (round(v, 5) if isinstance(v, float) else v) for k, v in res.items()}, flush=True)
json.dump(out, open(os.path.join(HERE, "interval_edges.json"), "w"), indent=1)
