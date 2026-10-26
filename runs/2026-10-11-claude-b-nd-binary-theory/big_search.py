"""Harder binary search at the large-N points (claude-b, T-20261010-claude-interactive-05, continuation): from the stored
best filter, from filters of the other large-N point at the same z/z_wb mapped by v = omega/N, and from roundings of the
non-negative-weight solution and of the even-sector optimal mode; flip descent and 8 x 2500-step ILS (kicks of 1..10 flips).
Writes big_search.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle"))
import nd_cov as nd
import refine_binary as rb
RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-11-claude-b-nd-binary-theory")
rows = {json.loads(l)["tag"]: json.loads(l) for l in open(os.path.join(RAW, "rows.jsonl"))}
tags = [t for t in ("N56_zr0.7", "N80_zr0.7", "N56_zr1", "N80_zr1") if t in rows]
data = {t: np.load(os.path.join(RAW, t + ".npz")) for t in tags}
rng = np.random.default_rng(17)
out = {}
for t in tags:
    d, r = data[t], rows[t]
    C, nb, keep, w = d["C"], d["nbar"], d["keep"], d["w"]
    v = w[keep] / r["N"]
    cands = {"stored": d["T"].astype(float)}
    for u in tags:
        if u != t and rows[u]["zr"] == r["zr"]:
            vu = data[u]["w"][data[u]["keep"]] / rows[u]["N"]
            idx = np.clip(np.searchsorted(vu, v), 0, len(vu) - 1)
            cands["from " + u] = data[u]["T"][idx].astype(float)
    Fnn, wnn = rb.nonneg_rq(C, nb, [d["T"].astype(float), np.ones_like(nb)], iters=3000)
    for q in (0.05, 0.1, 0.2, 0.3, 0.5):
        cands[f"nonneg>{q}"] = (wnn > q * wnn.max()).astype(float)
    best = None
    for name, T0 in cands.items():
        if T0.sum() == 0:
            continue
        F, T = nd.flip_descent(T0, C, nb)
        if best is None or F < best[0]:
            best = (F, T, name)
    for k in range(8):
        T = best[1].copy()
        if k:
            idx = rng.choice(len(nb), size=len(nb) // 10, replace=False); T[idx] = 1 - T[idx]
            F, T = nd.flip_descent(T, C, nb)
        else:
            F = best[0]
        F, T = nd.iterated_local_search(T, F, C, nb, rng, n_iter=2500, kmax=10)
        if F < best[0]:
            best = (F, T, best[2] + f"+ils{k}")
    out[t] = dict(F_stored=r["F_bin"], F_new=float(best[0]), rel=float(best[0] / r["F_bin"] - 1), source=best[2],
                  F_par=r["F_par"], dB_over_Fpar=float(10 * np.log10(best[0] / r["F_par"])))
    np.savez(os.path.join(RAW, t + "_search.npz"), T=best[1])
    print(t, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in out[t].items()}, flush=True)
json.dump(out, open(os.path.join(HERE, "big_search.json"), "w"), indent=1)
