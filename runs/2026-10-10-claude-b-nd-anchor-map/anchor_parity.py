"""Parity bracket at the Gaussian analogues of the two root-01 anchors (claude-b, T-20261010-claude-interactive-05):
same model as anchor_map.py (Nt 1024 over 80 T0, peak phase step 0.01); F_par = (lam_odd + lam_even)/2 (or lam_even) of
C-20261010-claude-a-03 on the parity-symmetric kept bins, against the best binary filter (stage-1 search + refine).
Writes anchor_parity.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle"))
import nd_cov as nd
import refine_binary as rb
pts = {"anchor_0.25m": (18.182869287103614, 0.07477662874402607), "anchor_1m": (9.91961154721838, 0.29910651497610447)}
out = {}
for tag, (N2, xi) in pts.items():
    g = nd.Grid(1024, 80.0)
    n = max(1, int(round(xi / (0.01 / N2)))); dxi = xi / n
    J, alpha = nd.jacobian(g, np.exp(-g.t ** 2 / 2) + 0j, xi, dxi, N2)
    chain, C, nb, keep, evec = nd.bound_chain(g, J, alpha)
    bb, Tb = nd.best_binary(C, nb, evec)
    Fnn, wnn, (Fr, Tr, name) = rb.refine(C, nb, Tb, evec, np.random.default_rng(4))
    Fbin = min(Fr, bb["F_best"])
    kk = np.rint(g.w[keep] / (2 * np.pi / 80)).astype(int); ks = set(kk)
    inB = np.array([(-k in ks) for k in kk])
    Cb, nbb, kb = C[np.ix_(inB, inB)], nb[inB], kk[inB]
    idx = {k: i for i, k in enumerate(kb)}; perm = np.array([idx[-k] for k in kb])
    A = Cb / np.sqrt(nbb)[:, None] / np.sqrt(nbb)[None, :]; m = len(nbb)
    P = np.zeros((m, m)); P[np.arange(m), perm] = 1
    ue, se, _ = np.linalg.svd((np.eye(m) + P) / 2); Be = ue[:, se > 0.5]
    uo, so, _ = np.linalg.svd((np.eye(m) - P) / 2); Bo = uo[:, so > 0.5]
    le = float(np.linalg.eigvalsh(Be.T @ A @ Be)[0]); lo = float(np.linalg.eigvalsh(Bo.T @ A @ Bo)[0])
    Fp = 0.5 * (lo + le) if lo <= le else le
    out[tag] = dict(lam_gen=chain["lam_gen"], lam_odd=lo, lam_even=le, F_par=Fp, F_bin=Fbin, dB_bin_over_Fpar=10 * np.log10(Fbin / Fp))
    print(tag, {k: round(v, 4) for k, v in out[tag].items()}, flush=True)
json.dump(out, open(os.path.join(HERE, "anchor_parity.json"), "w"), indent=1)
