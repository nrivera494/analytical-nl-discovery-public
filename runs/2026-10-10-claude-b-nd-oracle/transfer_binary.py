"""Third search stage for binary filters: transfer between N at fixed z/z_wb (claude-b, T-20261010-claude-interactive-05).

Semiclassical scaling maps frequency to v = omega / N. For every point, the current best filters of all other points
with the same z/z_wb and s (from binary_refine.json / *_refined.npz) are mapped to this point's bins by nearest v,
then flip descent and iterated local search (1000 perturbations) are run from each. The result replaces the refined
value only if lower. Writes binary_transfer.json and <tag>_transfer.npz.
Usage: python transfer_binary.py
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nd_cov as nd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data")

if __name__ == "__main__":
    ref = json.load(open(os.path.join(HERE, "binary_refine.json")))
    data = {}
    for tag, r in ref.items():
        d = np.load(os.path.join(RAW, r["run"], tag + ".npz"))
        T = np.load(os.path.join(RAW, r["run"], tag + "_refined.npz"))["T"]
        data[tag] = dict(C=d["C"], nb=d["nbar"], v=d["w"][d["keep"]] / r["N"], T=T.astype(float), r=r)
    rng = np.random.default_rng(11)
    out = {}
    for tag, D in data.items():
        best = (D["r"]["F_binary_refined"], D["T"], "refined")
        for other, O in data.items():
            if other == tag or O["r"]["zr"] != D["r"]["zr"] or O["r"]["s"] != D["r"]["s"]:
                continue
            idx = np.clip(np.searchsorted(O["v"], D["v"]), 0, len(O["v"]) - 1)
            T0 = O["T"][idx]
            if T0.sum() == 0:
                continue
            F, T = nd.flip_descent(T0, D["C"], D["nb"])
            F, T = nd.iterated_local_search(T, F, D["C"], D["nb"], rng, n_iter=1000)
            if F < best[0] - 1e-12:
                best = (F, T, "from " + other)
        out[tag] = dict(D["r"], F_binary_final=best[0], final_source=best[2], n_on_final=int(best[1].sum()),
                        photon_fraction_on_final=float(D["nb"][best[1] > 0].sum() / D["nb"].sum()))
        np.savez(os.path.join(RAW, D["r"]["run"], tag + "_transfer.npz"), T=best[1])
        print(tag, round(D["r"]["F_binary_refined"], 4), "->", round(best[0], 4), best[2], flush=True)
    json.dump(out, open(os.path.join(HERE, "binary_transfer.json"), "w"), indent=1)
