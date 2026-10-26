"""Fourth binary-search stage seeded by the parity structure (claude-b, T-20261010-claude-interactive-05): starts from
binarized combinations of the optimal even and odd sector modes, y = cos(a) e_even + sin(a) e_odd (a in a grid, both
signs), T = 1[y / sqrt(nbar) > q max] for several q, then flip descent and 1000-step ILS on the full kept set.
Reports whether any start beats the final filter of transfer_binary.py. Writes parity_search.json."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nd_cov as nd
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data")
S = {p["tag"]: p for p in json.load(open(os.path.join(HERE, "summary.json")))["points"]}
rng = np.random.default_rng(31)
out = {}
for tag in ("N20_zr0.7", "N40_zr0.7", "N40_zr1", "N20_zr0.3", "N20_zr1.5"):
    p = S[tag]
    d = np.load(os.path.join(RAW, p["run"], tag + ".npz"))
    C, nb, keep, w = d["C"], d["nbar"], d["keep"], d["w"]
    Tf = np.load(os.path.join(RAW, p["run"], tag + "_transfer.npz"))["T"].astype(float)
    F0 = nd.fano(Tf, C, nb)
    kk = np.rint(w[keep] / (2 * np.pi / p["TW"])).astype(int)
    pos = {k: i for i, k in enumerate(kk)}
    perm = np.array([pos.get(-k, i) for i, k in enumerate(kk)])
    A = C / np.sqrt(nb)[:, None] / np.sqrt(nb)[None, :]
    P = np.zeros_like(A); P[np.arange(len(nb)), perm] = 1
    ue, se, _ = np.linalg.svd((np.eye(len(nb)) + P) / 2); Be = ue[:, se > 0.5]
    uo, so, _ = np.linalg.svd((np.eye(len(nb)) - P) / 2); Bo = uo[:, so > 0.5]
    ee = Be @ np.linalg.eigh(Be.T @ A @ Be)[1][:, 0]
    eo = Bo @ np.linalg.eigh(Bo.T @ A @ Bo)[1][:, 0]
    if ee.sum() < 0:
        ee = -ee
    best = (F0, Tf, "transfer")
    for a in np.linspace(0, np.pi / 2, 7):
        for sgn in (1, -1):
            y = np.cos(a) * ee + sgn * np.sin(a) * eo
            t = y / np.sqrt(nb)
            for q in (0.02, 0.05, 0.1, 0.2, 0.35, 0.5):
                T0 = (t > q * np.max(t)).astype(float)
                if T0.sum() == 0:
                    continue
                F, T = nd.flip_descent(T0, C, nb)
                if F < best[0] - 1e-12:
                    best = (F, T, f"parity a={a:.2f} s={sgn} q={q}")
    F, T = nd.iterated_local_search(best[1], best[0], C, nb, rng, n_iter=1000)
    if F < best[0] - 1e-12:
        best = (F, T, best[2] + "+ils")
    out[tag] = dict(F_transfer=F0, F_parity_search=best[0], rel=best[0] / F0 - 1, source=best[2])
    print(tag, out[tag], flush=True)
json.dump(out, open(os.path.join(HERE, "parity_search.json"), "w"), indent=1)
