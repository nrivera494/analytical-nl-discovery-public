"""Few-detector signed readouts (claude-b, T-20261010-claude-interactive-05): Fano factor of N_w = sum_k w_k n_k with
(a) the split detector w = sign(omega - mean), (b) the centroid weight quantized to K equal-photon bands (K = 4, 8, 16;
each band weighted by its mean detuning), (c) the exact centroid, against lambda_gen and the best binary filter.
F_w = w^T C w / w^T diag(nbar) w. Writes few_detectors.json."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data")
S = {p["tag"]: p for p in json.load(open(os.path.join(HERE, "summary.json")))["points"]}
out = {}
for run, tag in (("2026-10-10-claude-b-nd-oracle", "N10_zr0.7"), ("2026-10-10-claude-b-nd-oracle", "N20_zr0.7"),
                 ("2026-10-10-claude-b-nd-heldout", "N40_zr0.7"), ("2026-10-10-claude-b-nd-oracle", "N20_zr0.3"),
                 ("2026-10-10-claude-b-nd-oracle", "N20_zr1.5"), ("2026-10-10-claude-b-nd-heldout", "N40_zr1")):
    d = np.load(os.path.join(RAW, run, tag + ".npz"))
    C, nb = d["C"], d["nbar"]
    w = d["w"][d["keep"]]
    wb = (nb * w).sum() / nb.sum()
    F = lambda x: float(x @ C @ x / (x @ (nb * x)))
    res = dict(lam_gen=S[tag]["lam_gen"], F_bin=S[tag]["F_bin"], F_centroid=F(w - wb), F_split=F(np.sign(w - wb)))
    cum = np.cumsum(nb) / nb.sum()
    for K in (4, 8, 16):
        band = np.minimum((cum * K).astype(int), K - 1)
        wq = np.zeros_like(w)
        for b in range(K):
            m = band == b
            wq[m] = (nb[m] * (w[m] - wb)).sum() / nb[m].sum()
        res[f"F_quantized_{K}"] = F(wq)
    res["dB"] = {k: 10 * np.log10(v) for k, v in res.items() if isinstance(v, float)}
    out[tag] = res
    print(tag, {k: round(v, 2) for k, v in res["dB"].items()}, flush=True)
json.dump(out, open(os.path.join(HERE, "few_detectors.json"), "w"), indent=1)
