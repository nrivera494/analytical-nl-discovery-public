"""Anatomy of the optimal even and odd weighted readouts (claude-b, T-20261010-claude-interactive-05, continuation).
For stored count covariances (run 2026-10-10-claude-b-nd-oracle / -heldout): the minimizers of y^T A y / |y|^2
(A = D^-1/2 C D^-1/2) in the even and odd sectors under omega -> -omega. Reports, for each mode, the weight
w = y / sqrt(nbar): its distribution over v = omega/N (fraction of |y|^2 in |v| bands), its correlation with v (odd) or 1
(even), and its 'roughness' (fraction of the power of w on the bin grid at bin-to-bin wavelengths shorter than the local
fringe spacing). Writes mode_anatomy.json."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ORA = os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle")
RAW = os.path.expanduser("~/analytical-nl-discovery-data")
S = {p["tag"]: p for p in json.load(open(os.path.join(ORA, "summary.json")))["points"]}


def sectors(C, nb, kk):
    ks = set(kk)
    inB = np.array([(-k in ks) for k in kk])
    C, nb, kk = C[np.ix_(inB, inB)], nb[inB], kk[inB]
    idx = {k: i for i, k in enumerate(kk)}
    perm = np.array([idx[-k] for k in kk])
    A = C / np.sqrt(nb)[:, None] / np.sqrt(nb)[None, :]
    n = len(nb)
    P = np.zeros((n, n)); P[np.arange(n), perm] = 1
    ue, se, _ = np.linalg.svd((np.eye(n) + P) / 2); Be = ue[:, se > 0.5]
    uo, so, _ = np.linalg.svd((np.eye(n) - P) / 2); Bo = uo[:, so > 0.5]
    le, ve = np.linalg.eigh(Be.T @ A @ Be); lo, vo = np.linalg.eigh(Bo.T @ A @ Bo)
    return C, nb, kk, A, (le[:4], Be @ ve[:, :4]), (lo[:4], Bo @ vo[:, :4])


out = {}
for tag in ("N10_zr0.7", "N20_zr0.7", "N28_zr0.7", "N40_zr0.7", "N40_zr1", "N20_zr0.3"):
    p = S[tag]
    d = np.load(os.path.join(RAW, p["run"], tag + ".npz"))
    kk = np.rint(d["w"][d["keep"]] / (2 * np.pi / p["TW"])).astype(int)
    C, nb, kk, A, (le, Ve), (lo, Vo) = sectors(d["C"], d["nbar"], kk)
    v = kk * (2 * np.pi / p["TW"]) / p["N"]
    res = dict(N=p["N"], zr=p["zr"], lam_even=le.tolist(), lam_odd=lo.tolist())
    for name, y in (("even", Ve[:, 0]), ("odd", Vo[:, 0])):
        y = y / np.linalg.norm(y)
        w = y / np.sqrt(nb)
        bands = [0, 0.2, 0.4, 0.6, 0.8, 1.2, 10]
        frac = [float(np.sum(y[(np.abs(v) >= a) & (np.abs(v) < b)] ** 2)) for a, b in zip(bands[:-1], bands[1:])]
        # smooth fit: project y onto sqrt(nb)*polynomial(v) of degree <= 6 (smooth weights)
        Vm = np.vstack([np.sqrt(nb) * v ** j for j in range(7)]).T
        Q, _ = np.linalg.qr(Vm)
        smooth_frac = float(np.sum((Q.T @ y) ** 2))
        res[name] = dict(band_edges=bands, weight_fraction=frac, smooth_poly6_fraction=smooth_frac,
                         rayleigh=float(y @ A @ y))
    out[tag] = res
    print(tag, "lam_even", np.round(le[:3], 4), "lam_odd", np.round(lo[:3], 5))
    for name in ("even", "odd"):
        r = res[name]
        print("   ", name, "weight by |v| band", [round(x, 3) for x in r["weight_fraction"]], " smooth (poly<=6) fraction %.3f" % r["smooth_poly6_fraction"])
json.dump(out, open(os.path.join(HERE, "mode_anatomy.json"), "w"), indent=1)
