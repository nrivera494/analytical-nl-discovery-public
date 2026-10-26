"""Spectral-resolution dependence of the optimal even and odd weighted readouts (claude-b,
T-20261010-claude-interactive-05, continuation). Weights are restricted to be piecewise constant over blocks of b adjacent
bins (blocks paired symmetrically about omega = 0), b = 1, 2, 4, 8, 16, 32; reports the restricted lambda_even, lambda_odd
and the parity bound. Also the local fringe spacing near the line centre in bins. Writes coarse_grain.json."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ORA = os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle")
RAW = os.path.expanduser("~/analytical-nl-discovery-data")
S = {p["tag"]: p for p in json.load(open(os.path.join(ORA, "summary.json")))["points"]}
out = {}
for tag in ("N10_zr0.7", "N20_zr0.7", "N40_zr0.7", "N40_zr1"):
    p = S[tag]
    d = np.load(os.path.join(RAW, p["run"], tag + ".npz"))
    kk = np.rint(d["w"][d["keep"]] / (2 * np.pi / p["TW"])).astype(int)
    ks = set(kk); inB = np.array([(-k in ks) for k in kk])
    C, nb, kk = d["C"][np.ix_(inB, inB)], d["nbar"][inB], kk[inB]
    order = np.argsort(kk); C, nb, kk = C[np.ix_(order, order)], nb[order], kk[order]
    res = {}
    for b in (1, 2, 4, 8, 16, 32):
        # blocks on |k|: block index floor(|k|/b) with sign; k = 0 alone
        blk = np.sign(kk) * (np.abs(kk) // b + (kk != 0))
        labels = sorted(set(blk))
        M = np.zeros((len(kk), len(labels)))
        for j, lab in enumerate(labels):
            M[blk == lab, j] = 1.0
        # restricted generalized eigenproblem in each parity sector: w = M a, a even/odd in the label sign
        pos = [l for l in labels if l > 0]
        Ee = [M[:, labels.index(0)]] + [M[:, labels.index(l)] + M[:, labels.index(-l)] for l in pos]
        Eo = [M[:, labels.index(l)] - M[:, labels.index(-l)] for l in pos]
        lam = {}
        for name, E in (("even", np.array(Ee).T), ("odd", np.array(Eo).T)):
            Cs, Ds = E.T @ C @ E, E.T @ (nb[:, None] * E)
            L = np.linalg.cholesky(Ds)
            Li = np.linalg.inv(L)
            lam[name] = float(np.linalg.eigvalsh(Li @ Cs @ Li.T)[0])
        Fp = 0.5 * (lam["odd"] + lam["even"]) if lam["odd"] <= lam["even"] else lam["even"]
        res[b] = dict(lam_even=lam["even"], lam_odd=lam["odd"], F_par=Fp, block_width_v=b * 2 * np.pi / p["TW"] / p["N"])
        print(tag, "b=%2d (dv=%.4f): lam_even %.4f lam_odd %.5f F_par %.4f" % (b, res[b]["block_width_v"], lam["even"], lam["odd"], Fp), flush=True)
    # fringe spacing near centre: spacing of minima of nbar for |v| < 0.35
    v = kk * (2 * np.pi / p["TW"]) / p["N"]
    m = np.abs(v) < 0.35
    mins = np.where((nb[1:-1] < nb[:-2]) & (nb[1:-1] < nb[2:]) & m[1:-1])[0]
    res["fringe_spacing_bins_centre"] = float(np.median(np.diff(mins))) if len(mins) > 1 else None
    out[tag] = res
    print(tag, "fringe spacing near centre (bins):", res["fringe_spacing_bins_centre"])
json.dump(out, open(os.path.join(HERE, "coarse_grain.json"), "w"), indent=1, default=float)
