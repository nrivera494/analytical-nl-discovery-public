"""Parity bound for non-negative filters (C-20261010-claude-a-03, claude-a, unverified WIP read at 13:34) evaluated on the
normal-dispersion covariances (claude-b, T-20261010-claude-interactive-05). With y = T sqrt(nbar) >= 0 and the parity
P: omega -> -omega on the kept bin set B (checked symmetric), |y_e|^2 >= |y_o|^2, and V_amp = D^-1/2 C D^-1/2 has no
even-odd cross terms, so F[T] >= F_par = (lam_odd + lam_even)/2 if lam_odd <= lam_even, else lam_even.
Compares F_par with lambda_gen and the best binary filter found. Writes parity_bound.json."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data")
S = {p["tag"]: p for p in json.load(open(os.path.join(HERE, "summary.json")))["points"]}
out = {}
for p in sorted(S.values(), key=lambda p: (p["zr"], p["N"])):
    if p["s"] != 0 or not p["resolved"]:
        continue
    d = np.load(os.path.join(RAW, p["run"], p["tag"] + ".npz"))
    C, nb, keep, w = d["C"], d["nbar"], d["keep"], d["w"]
    dw = 2 * np.pi / p["TW"]
    kk = np.rint(w[keep] / dw).astype(int)
    # B = kept bins whose mirror bin is also kept (the bound holds for filters supported on B)
    inB = np.array([(-k in set(kk)) for k in kk])
    n_dropped = int((~inB).sum())
    C, nb, kk = C[np.ix_(inB, inB)], nb[inB], kk[inB]
    idx = {k: i for i, k in enumerate(kk)}
    perm = np.array([idx[-k] for k in kk])
    Dm = 1 / np.sqrt(nb)
    A = Dm[:, None] * C * Dm[None, :]
    P = np.zeros_like(A); P[np.arange(len(nb)), perm] = 1
    sym_err = float(np.max(np.abs(P @ A @ P.T - A)) / np.max(np.abs(A)))
    Pe, Po = (np.eye(len(nb)) + P) / 2, (np.eye(len(nb)) - P) / 2
    # orthonormal bases of the even and odd subspaces
    ue, se, _ = np.linalg.svd(Pe); Be = ue[:, se > 0.5]
    uo, so, _ = np.linalg.svd(Po); Bo = uo[:, so > 0.5]
    lam_even = float(np.linalg.eigvalsh(Be.T @ A @ Be)[0]); lam_odd = float(np.linalg.eigvalsh(Bo.T @ A @ Bo)[0])
    Fpar = 0.5 * (lam_odd + lam_even) if lam_odd <= lam_even else lam_even
    out[p["tag"]] = dict(N=p["N"], zr=p["zr"], n_bins_dropped_for_symmetry=n_dropped, lam_gen=p["lam_gen"], lam_odd=lam_odd, lam_even=lam_even, F_par=Fpar,
                         F_bin=p["F_bin"], F_nonneg_heuristic=p["F_nonneg_heuristic"], parity_sym_err=sym_err,
                         dB_bin_over_Fpar=10 * np.log10(p["F_bin"] / Fpar), dB_Fpar_over_gen=10 * np.log10(Fpar / p["lam_gen"]))
    o = out[p["tag"]]
    print(f"{p['tag']:11s} gen {o['lam_gen']:.4f} odd {lam_odd:.4f} even {lam_even:.4f} F_par {Fpar:.4f} F_bin {o['F_bin']:.4f} "
          f"| bin over F_par {o['dB_bin_over_Fpar']:.2f} dB, F_par over gen {o['dB_Fpar_over_gen']:.2f} dB (sym err {sym_err:.1e}, dropped {n_dropped})", flush=True)
json.dump(out, open(os.path.join(HERE, "parity_bound.json"), "w"), indent=1)
