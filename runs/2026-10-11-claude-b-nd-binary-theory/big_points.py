"""Large-N points for the binary-filter scaling (claude-b, T-20261010-claude-interactive-05, continuation).
Count covariance by the discrete adjoint (adjoint_cov.py, validated against the finite-difference oracle to 2e-9 at
N10 z/z_wb = 0.7). For each point: lambda_gen, the parity-sector minima lambda_odd, lambda_even and the parity bound F_par
(C-20261010-claude-a-03), the centroid readout and its identity check (resolution flag), best single interval, and the best
binary filter found (stage-1 search of nd_cov.best_binary, refine_binary.refine, and descent + ILS from the N = 40 filter
of the same z/z_wb mapped by v = omega/N). Usage: python big_points.py [tags...] -> rows.jsonl and <tag>.npz in the raw dir.
"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ORA = os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle")
sys.path.insert(0, ORA)
import nd_cov as nd
import refine_binary as rb
import adjoint_cov as ac

RUN = "2026-10-11-claude-b-nd-binary-theory"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN}")
CASES = {"N56_zr0.7": (56, 0.7, 2048, 40.0), "N80_zr0.7": (80, 0.7, 2048, 40.0), "N112_zr0.7": (112, 0.7, 4096, 40.0),
         "N56_zr1": (56, 1.0, 2048, 40.0), "N80_zr1": (80, 1.0, 2048, 40.0),
         "N40_zr0.3": (40, 0.3, 1024, 40.0), "N56_zr0.3": (56, 0.3, 2048, 40.0), "N80_zr0.3": (80, 0.3, 2048, 40.0),
         "N40_zr1.5": (40, 1.5, 2048, 40.0), "N56_zr1.5": (56, 1.5, 4096, 40.0)}
REF = {0.7: ("2026-10-10-claude-b-nd-heldout", "N40_zr0.7"), 1.0: ("2026-10-10-claude-b-nd-heldout", "N40_zr1"),
       0.3: ("2026-10-10-claude-b-nd-oracle", "N28_zr0.3"), 1.5: ("2026-10-10-claude-b-nd-oracle", "N20_zr1.5")}


def parity(C, nb, kk):
    ks = set(kk)
    inB = np.array([(-k in ks) for k in kk])
    Cb, nbb, kb = C[np.ix_(inB, inB)], nb[inB], kk[inB]
    idx = {k: i for i, k in enumerate(kb)}
    perm = np.array([idx[-k] for k in kb])
    A = Cb / np.sqrt(nbb)[:, None] / np.sqrt(nbb)[None, :]
    n = len(nbb)
    # even/odd bases directly from the pairing (faster than an SVD of the projector)
    pairs, seen = [], set()
    for i, k in enumerate(kb):
        if k in seen:
            continue
        seen.add(k); seen.add(-k)
        pairs.append((i, idx[-k]))
    Be = np.zeros((n, len(pairs))); Bo = []
    for j, (i1, i2) in enumerate(pairs):
        if i1 == i2:
            Be[i1, j] = 1.0
        else:
            Be[i1, j] = Be[i2, j] = 1 / np.sqrt(2)
            col = np.zeros(n); col[i1], col[i2] = 1 / np.sqrt(2), -1 / np.sqrt(2); Bo.append(col)
    Bo = np.array(Bo).T
    le = float(np.linalg.eigvalsh(Be.T @ A @ Be)[0]); lo = float(np.linalg.eigvalsh(Bo.T @ A @ Bo)[0])
    Fp = 0.5 * (lo + le) if lo <= le else le
    return le, lo, Fp, int((~inB).sum())


def run(tag):
    N, zr, Nt, TW = CASES[tag]
    t0 = time.time()
    r = ac.count_covariance(N, zr, Nt, TW)
    C, nb, keep, w, alpha = r["C"], r["nbar"], r["keep"], r["w"], r["alpha"]
    t_cov = time.time() - t0
    Dm = 1 / np.sqrt(nb)
    e, V = np.linalg.eigh(Dm[:, None] * C * Dm[None, :])
    lam_gen, evec = float(e[0]), V[:, 0] * Dm
    kk = np.rint(w[keep] / (2 * np.pi / TW)).astype(int)
    le, lo, Fp, ndrop = parity(C, nb, kk)
    nall = np.abs(alpha) ** 2
    wb = (nall * w).sum() / nall.sum()
    Fc = 0.5 / ((nall * (w - wb) ** 2).sum() / nall.sum())
    wc = w[keep] - wb
    Fc_cov = float(wc @ C @ wc / (wc @ (nb * wc)))
    rng = np.random.default_rng(13)
    bb, Tb = nd.best_binary(C, nb, evec, n_random=30, n_ils=300)
    Fnn, wnn, (Fr, Tr, name) = rb.refine(C, nb, Tb, evec, rng)
    best = (Fr, Tr, "stage1+refine") if Fr < bb["F_best"] else (bb["F_best"], Tb, "stage1")
    run_ref, tag_ref = REF[zr]
    dref = np.load(os.path.join(os.path.expanduser("~/analytical-nl-discovery-data"), run_ref, tag_ref + ".npz"))
    Tref = np.load(os.path.join(os.path.expanduser("~/analytical-nl-discovery-data"), run_ref, tag_ref + "_transfer.npz"))["T"]
    Nref = int(tag_ref.split("_")[0][1:])
    vref = dref["w"][dref["keep"]] / Nref
    v = w[keep] / N
    idx = np.clip(np.searchsorted(vref, v), 0, len(vref) - 1)
    T0 = Tref[idx].astype(float)
    F, T = nd.flip_descent(T0, C, nb)
    F, T = nd.iterated_local_search(T, F, C, nb, rng, n_iter=1000)
    if F < best[0]:
        best = (F, T, "transfer from " + tag_ref)
    row = dict(tag=tag, N=N, zr=zr, Nt=Nt, TW=TW, xi=r["xi"], Z=N * r["xi"], Phi=N * N * r["xi"], nsteps=r["nsteps"],
               n_bins=len(keep), lam_gen=lam_gen, lam_odd=lo, lam_even=le, F_par=Fp, n_dropped_parity=ndrop,
               F_centroid=Fc, centroid_check=Fc_cov / Fc, F_interval=bb["F_interval"], F_nonneg_heuristic=Fnn,
               F_bin=float(best[0]), F_bin_source=best[2], photon_fraction_on=float(nb[best[1] > 0].sum() / nb.sum()),
               wall_cov=t_cov, wall=time.time() - t0)
    os.makedirs(RAW, exist_ok=True)
    np.savez(os.path.join(RAW, tag + ".npz"), C=C, nbar=nb, keep=keep, w=w, alpha=alpha, T=best[1], evec=evec)
    with open(os.path.join(RAW, "rows.jsonl"), "a") as fh:
        fh.write(json.dumps(row) + "\n")
    print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items()}), flush=True)


if __name__ == "__main__":
    for tag in (sys.argv[1:] or list(CASES)):
        run(tag)
