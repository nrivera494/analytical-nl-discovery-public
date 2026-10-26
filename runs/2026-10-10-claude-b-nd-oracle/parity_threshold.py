"""Sensitivity of the parity bound to the bin-darkness threshold (claude-b, T-20261010-claude-interactive-05).
For B = {nbar >= thr * max nbar} (made parity-symmetric), lambda_odd, lambda_even and F_par on B, and the best binary
filter (final stage) restricted to B. Writes parity_threshold.json. Usage: python parity_threshold.py"""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data")
S = {p["tag"]: p for p in json.load(open(os.path.join(HERE, "summary.json")))["points"]}
res = {}
for tag in ("N10_zr0.7", "N20_zr0.7", "N28_zr0.7", "N40_zr0.7", "N40_zr1", "N20_zr0.3"):
    p = S[tag]
    d = np.load(os.path.join(RAW, p["run"], tag + ".npz"))
    C, nb, keep, w = d["C"], d["nbar"], d["keep"], d["w"]
    T = np.load(os.path.join(RAW, p["run"], tag + "_transfer.npz"))["T"].astype(float)
    kk = np.rint(w[keep] / (2 * np.pi / p["TW"])).astype(int)
    row = {}
    for thr in (1e-12, 1e-9, 1e-6, 1e-4):
        sel = nb >= thr * nb.max()
        ks = set(kk[sel])
        inB = sel & np.array([(-k in ks) for k in kk])
        Cb, nbb, kb = C[np.ix_(inB, inB)], nb[inB], kk[inB]
        idx = {k: i for i, k in enumerate(kb)}
        perm = np.array([idx[-k] for k in kb])
        A = Cb / np.sqrt(nbb)[:, None] / np.sqrt(nbb)[None, :]
        n = len(nbb)
        P = np.zeros((n, n)); P[np.arange(n), perm] = 1
        ue, se, _ = np.linalg.svd((np.eye(n) + P) / 2); Be = ue[:, se > 0.5]
        uo, so, _ = np.linalg.svd((np.eye(n) - P) / 2); Bo = uo[:, so > 0.5]
        le = np.linalg.eigvalsh(Be.T @ A @ Be)[0]; lo = np.linalg.eigvalsh(Bo.T @ A @ Bo)[0]
        Fp = 0.5 * (lo + le) if lo <= le else le
        Tr = T * inB
        Fr = float(Tr @ C @ Tr / (Tr @ nb)) if Tr.sum() else float("nan")
        row[str(thr)] = dict(n_bins=int(inB.sum()), lam_odd=float(lo), lam_even=float(le), F_par=float(Fp), F_bin_restricted=Fr)
    res[tag] = row
    print(tag, " | ".join(f"thr {t}: n {r['n_bins']} F_par {r['F_par']:.4f} (bin {r['F_bin_restricted']:.4f})" for t, r in row.items()))
json.dump(res, open(os.path.join(HERE, "parity_threshold.json"), "w"), indent=1)
