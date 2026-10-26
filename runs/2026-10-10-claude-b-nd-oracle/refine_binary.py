"""Second search stage for binary filters, and a non-negative-weight diagnostic (claude-b, T-20261010-claude-interactive-05).

For every stored point (runs 2026-10-10-claude-b-nd-oracle and 2026-10-10-claude-b-nd-heldout):
  1. Non-negative weights: minimise R(w) = w^T C w / w^T diag(nbar) w over w >= 0 by projected gradient on the sphere
     (in x = sqrt(nbar) w), from the stored best binary filter, all-ones, the two sign parts of the lambda_gen
     eigenvector, 12 uniform random vectors and 12 random 0/1 vectors. The result F_nonneg is a heuristic (an upper
     estimate of the non-negative optimum, not a bound). It shows how much of the gap between lambda_gen and the binary
     optimum is due to the sign constraint alone.
  2. Binary refinement: flip descent (nd_cov.flip_descent) from the stored best filter and from the support of the
     non-negative solution thresholded at 2, 5, 10, 20, 30 and 50 % of its maximum, and from 20 randomised roundings
     (bin k on with probability min(1, w_k / (q max w)), q random in [0.1, 0.6]); then iterated local search (1000
     perturbations of 1..6 flips) from the best. F_binary_refined = min(stored F_best, refined).
Writes binary_refine.json here and <tag>_refined.npz (filters) in the raw-data directory of each run.
Usage: python refine_binary.py
"""
import glob, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nd_cov as nd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data")


def nonneg_rq(C, nb, starts, iters=4000):
    Dm = 1 / np.sqrt(nb)
    A = Dm[:, None] * C * Dm[None, :]
    L = np.linalg.eigvalsh(A)[-1]
    best = (np.inf, None)
    for x in starts:
        x = np.maximum(x * np.sqrt(nb), 0)
        if np.linalg.norm(x) == 0:
            continue
        x /= np.linalg.norm(x)
        for _ in range(iters):
            g = A @ x - (x @ A @ x) * x
            x = np.maximum(x - g / L, 0)
            n = np.linalg.norm(x)
            if n == 0:
                break
            x /= n
        if np.linalg.norm(x) > 0 and x @ A @ x < best[0]:
            best = (float(x @ A @ x), x * Dm)
    return best


def refine(C, nb, Tstored, evec, rng):
    starts = [Tstored, np.ones_like(nb), np.maximum(evec, 0), np.maximum(-evec, 0)]
    starts += [rng.random(len(nb)) for _ in range(12)] + [(rng.random(len(nb)) < 0.4).astype(float) for _ in range(12)]
    Fnn, wnn = nonneg_rq(C, nb, starts)
    cands = {"stored": Tstored.astype(float)}
    for q in (0.02, 0.05, 0.1, 0.2, 0.3, 0.5):
        cands[f"nonneg>{q}"] = (wnn > q * wnn.max()).astype(float)
    for r in range(20):
        q = rng.uniform(0.1, 0.6)
        cands[f"round{r}"] = (rng.random(len(nb)) < np.minimum(1, wnn / (q * wnn.max()))).astype(float)
    best = None
    for name, T0 in cands.items():
        if T0.sum() == 0:
            continue
        F, T = nd.flip_descent(T0, C, nb)
        if best is None or F < best[0]:
            best = (F, T, name)
    Fils, Tils = nd.iterated_local_search(best[1], best[0], C, nb, rng, n_iter=1000)
    if Fils < best[0]:
        best = (Fils, Tils, best[2] + "+ils")
    return Fnn, wnn, best


if __name__ == "__main__":
    out = {}
    rng = np.random.default_rng(7)
    for run in ("2026-10-10-claude-b-nd-oracle", "2026-10-10-claude-b-nd-heldout"):
        rows = {json.loads(l)["tag"]: json.loads(l) for l in open(os.path.join(RAW, run, "rows.jsonl"))}
        for f in sorted(glob.glob(os.path.join(RAW, run, "*.npz"))):
            tag = os.path.basename(f)[:-4]
            if tag.endswith("_refined") or tag not in rows:
                continue
            t0 = time.time()
            d = np.load(f)
            C, nb, Ts, ev = d["C"], d["nbar"], d["Tbest"], d["evec"]
            Fnn, wnn, (Fb, Tb, name) = refine(C, nb, Ts, ev, rng)
            Fs = nd.fano(Ts.astype(float), C, nb)
            lam_gen = float(np.linalg.eigvalsh((C / np.sqrt(nb)[:, None]) / np.sqrt(nb)[None, :])[0])
            res = dict(run=run, N=rows[tag]["N"], zr=rows[tag]["zr"], s=rows[tag]["s"], lam_gen=lam_gen,
                       F_nonneg_heuristic=Fnn, F_binary_stored=Fs, F_binary_refined=min(Fs, Fb),
                       refined_start=name if Fb < Fs else "stored", n_on=int((Tb if Fb < Fs else Ts).sum()),
                       photon_fraction_on=float(nb[(Tb if Fb < Fs else Ts) > 0].sum() / nb.sum()), wall=time.time() - t0)
            out[tag] = res
            np.savez(os.path.join(RAW, run, tag + "_refined.npz"), T=(Tb if Fb < Fs else Ts), w_nonneg=wnn)
            print(tag, {k: (round(v, 5) if isinstance(v, float) else v) for k, v in res.items()}, flush=True)
    json.dump(out, open(os.path.join(HERE, "binary_refine.json"), "w"), indent=1)
