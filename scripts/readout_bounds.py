#!/usr/bin/env python3
"""agent: gpt-a; model: gpt-6-astra; family: gpt.

Covariance-only binary-filter bounds, certified dual reconstruction, and
multistart one-/two-flip searches. T-20261010-claude-interactive-03.
All arrays stay in the raw-data directory; JSON summaries are small.
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import argparse
import json
import time
from pathlib import Path
import numpy as np
from scipy import linalg as la


def loweig(a, vectors=False, count=1):
    return la.eigh(a, subset_by_index=(0, count-1), eigvals_only=not vectors,
                   check_finite=False, driver="evr")


def binary_overlap(v, n):
    """Exact maximum squared overlap over all nonempty masks by thresholds."""
    b = np.sqrt(n)
    best, best_mask = 0.0, np.zeros(len(n), bool)
    candidates = []
    for sign in (1.0, -1.0):
        ids = np.flatnonzero((sign*v > 0) & (b > 0))
        ids = ids[np.argsort(-(sign*v[ids]/b[ids]), kind="stable")]
        if not len(ids):
            continue
        values = np.cumsum(sign*b[ids]*v[ids])**2/np.cumsum(n[ids])
        j = int(np.argmax(values))
        mask = np.zeros(len(n), bool)
        mask[ids[:j+1]] = True
        candidates.append(mask)
        if values[j] > best:
            best, best_mask = float(values[j]), mask
    return min(1.0, best), best_mask, candidates


def eigenvector_bound(a, n):
    ev, vec = loweig(a, vectors=True, count=min(8, len(n)))
    rho, mask, candidates = binary_overlap(vec[:, 0], n)
    if len(n) == 1:
        return float(ev[0]), {"rho_binary": 1.0, "lambda_2_amp": float(ev[0])}, mask, candidates
    gap = float(ev[1]-ev[0])
    residual_matrix = a - ev[1]*np.eye(len(n)) + gap*np.outer(vec[:, 0], vec[:, 0])
    margin = 2e-10*max(1.0, la.norm(a, np.inf))
    correction = max(0.0, -float(loweig(residual_matrix)[0]))+margin
    bound = float(ev[1]-gap*rho-correction)
    for j in range(1, vec.shape[1]):
        candidates.extend(binary_overlap(vec[:, j], n)[2])
    return bound, {"rho_binary": rho, "lambda_2_amp": float(ev[1]),
                   "eigen_certificate_margin": correction}, mask, candidates


def fano(sigma, n, mask):
    t = np.asarray(mask, float)
    denom = n@t
    return float(t@sigma@t/denom) if denom > 0 else np.inf


def improve_mask(sigma, n, initial, active, max_flips=10000):
    t = np.array(initial, bool, copy=True)
    if not np.any(t & (n > 0)):
        t[np.argmax(n)] = True
    st = sigma@t.astype(float)
    s = float(n@t)
    q = float(t@st)
    diag = np.diag(sigma)
    flips = 0
    for _ in range(max_flips):
        signs = 1.0-2.0*t[active]
        den = s+signs*n[active]
        nums = q+2*signs*st[active]+diag[active]
        values = np.full(len(active), np.inf)
        valid = den > 1e-14*max(s, np.max(n))
        values[valid] = nums[valid]/den[valid]
        k = int(np.argmin(values))
        if values[k] >= q/s-2e-12*max(1.0, abs(q/s)):
            break
        i = active[k]
        sign = signs[k]
        q, s = float(nums[k]), float(den[k])
        st += sign*sigma[:, i]
        t[i] = not t[i]
        flips += 1
    return t, fano(sigma, n, t), flips


def pair_escape(sigma, n, t, active, rounds=12):
    t = t.copy()
    total = 0
    si = sigma[np.ix_(active, active)]
    diag = np.diag(si)
    for _ in range(rounds):
        st = sigma@t.astype(float)
        s, q = float(n@t), float(t@st)
        signs = 1.0-2.0*t[active]
        ds = signs*n[active]
        dq = 2*signs*st[active]+diag
        den = s+ds[:, None]+ds[None, :]
        num = q+dq[:, None]+dq[None, :]+2*np.outer(signs, signs)*si
        values = np.full_like(den, np.inf)
        valid = np.triu(np.ones_like(den, bool), 1) & (den > 1e-14*max(s, np.max(n)))
        values[valid] = num[valid]/den[valid]
        k, j = np.unravel_index(np.argmin(values), values.shape)
        if values[k, j] >= q/s-2e-12*max(1.0, abs(q/s)):
            break
        t[active[[k, j]]] = ~t[active[[k, j]]]
        t, _, _ = improve_mask(sigma, n, t, active)
        total += 1
    return t, fano(sigma, n, t), total


def binary_search(a, n, seeds=(), seed=20261010, restarts=96):
    n = n/max(n)
    b = np.sqrt(n)
    sigma = b[:, None]*a*b[None, :]
    active = np.flatnonzero(n > 1e-12)
    rng = np.random.default_rng(seed)
    starts = [np.ones(len(n), bool), *seeds]
    singleton = np.zeros(len(n), bool)
    singleton[active[np.argmin(np.diag(a)[active])]] = True
    starts.append(singleton)
    # Best single interval and its complement, scored using a 2D prefix sum.
    core = np.arange(active[0], active[-1]+1)
    sc = sigma[np.ix_(core, core)]
    prefix = np.pad(sc.cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    ns = np.r_[0.0, np.cumsum(n[core])]
    best_band, band_score = None, np.inf
    for i in range(len(core)):
        js = np.arange(i+1, len(core)+1)
        den = ns[js]-ns[i]
        vals = (prefix[js, js]-prefix[i, js]-prefix[js, i]+prefix[i, i])/np.maximum(den, 1e-300)
        k = int(np.argmin(vals))
        if den[k] > 0 and vals[k] < band_score:
            band_score = float(vals[k])
            best_band = np.zeros(len(n), bool)
            best_band[core[i:js[k]]] = True
    if best_band is not None:
        starts.extend((best_band, ~best_band))
    for j in range(restarts):
        t = np.zeros(len(n), bool)
        t[active] = rng.random(len(active)) < (0.15+0.7*(j % 7)/6)
        starts.append(t)
    results, flips = [], 0
    for initial in starts:
        t, val, nf = improve_mask(sigma, n, initial, active)
        results.append((val, t))
        flips += nf
    results.sort(key=lambda item: item[0])
    pair_count = 0
    for val, t in results[:min(8, len(results))]:
        t, val, npair = pair_escape(sigma, n, t, active)
        pair_count += npair
        results.append((val, t))
    results.sort(key=lambda item: item[0])
    val, mask = results[0]
    return float(val), mask, {"seed": seed, "random_starts": restarts,
        "total_starts": len(starts), "one_flip_updates": flips,
        "two_flip_escapes": pair_count, "search_active_bins": len(active),
        "best_single_interval_F": band_score,
        "method": "interval/eigenvector seeds + random starts; sequential one-flip descent; two-flip escapes"}


def passive_eigenvalue(v, n):
    """Householder compression of the global phase hyperplane."""
    m = len(n)
    g = np.r_[np.zeros(m), np.sqrt(n/np.sum(n))]
    h = g.copy()
    h[-1] -= 1.0
    if la.norm(h) > 1e-14:
        h /= la.norm(h)
        vh = v@h
        rotated = v-2*np.outer(h, vh)-2*np.outer(vh, h)+4*(h@vh)*np.outer(h, h)
    else:
        h[:] = 0
        rotated = v
    eig, vec = loweig(rotated[:-1, :-1], vectors=True)
    q = np.r_[vec[:, 0], 0.0]
    q -= 2*h*(h@q)
    brightness = float(np.sqrt(n)@q[:m])**2
    return float(eig[0]), brightness, q


def moment_certificate(a, n, upper, initial, max_core=72, iterations=4):
    """Optimize core RLT multipliers, then certify on the *full* matrix.

    A Schur complement reduces the SDP dimensions; no frequency bin is
    discarded from the final lower-bound certificate. Each accepted K is a
    nonnegative combination of globally valid binary inequality matrices.
    """
    import cvxpy as cp
    begun = time.time()
    active = np.flatnonzero(n > 0)
    m = min(max_core, len(active))
    core = np.sort(active[np.argsort(n[active])[-m:]])
    tail = np.setdiff1d(np.arange(len(n)), core)
    b = np.sqrt(n[core]/max(n[core]))
    scale = np.maximum(b[:, None], b[None, :])
    dc = np.broadcast_to(b[None, :], (m, m))/scale
    oc = np.broadcast_to(b[:, None], (m, m))/scale
    np.fill_diagonal(dc, 0)
    np.fill_diagonal(oc, 0)
    y = cp.Variable((m, m), symmetric=True)
    ae = cp.Parameter((m, m), symmetric=True)
    positivity = y >= 0
    rlt = cp.multiply(dc, cp.reshape(cp.diag(y), (m, 1), order="C"))-cp.multiply(oc, y) >= 0
    problem = cp.Problem(cp.Minimize(cp.sum(cp.multiply(ae, y))),
                         [y >> 0, cp.trace(y) == 1, positivity, rlt])
    acc = a[np.ix_(core, core)]
    if len(tail):
        et, ut = la.eigh(a[np.ix_(tail, tail)], check_finite=False)
        cross = a[np.ix_(core, tail)]@ut
        ceiling = min(float(upper), float(et[0])-1e-6)
    else:
        et, cross, ceiling = np.array([]), None, float(upper)
    lower = float(initial)
    history, bestk = [], np.zeros_like(a)
    margin = 1e-8*max(1.0, la.norm(a, np.inf))
    for iteration in range(iterations):
        trial = lower+0.7*max(0, ceiling-lower)
        effective = acc.copy()
        if len(tail):
            effective -= (cross/(et-trial))@cross.T
        ae.value = (effective+effective.T)/2
        problem.solve(solver="SCS", eps=2e-6, max_iters=12000, warm_start=True, verbose=False)
        if positivity.dual_value is None or rlt.dual_value is None:
            history.append({"status": str(problem.status), "trial": trial})
            break
        nu = np.maximum(rlt.dual_value, 0)
        nn = np.maximum(positivity.dual_value, 0)
        rawk = nn-nu*oc
        kcore = (rawk+rawk.T)/2+np.diag(np.sum(nu*dc, axis=1))
        k = np.zeros_like(a)
        k[np.ix_(core, core)] = kcore
        candidate = float(loweig(a-k)[0])-margin
        # A successful Cholesky provides a second floating-point PSD check.
        la.cholesky(a-k-candidate*np.eye(len(n)), lower=True, check_finite=False)
        history.append({"status": str(problem.status), "trial": trial,
                        "primal_value": float(problem.value), "full_dual_bound": candidate,
                        "solver_seconds": float(problem.solver_stats.solve_time or 0),
                        "solver_iterations": int(problem.solver_stats.num_iters or 0)})
        if candidate > lower:
            lower, bestk = candidate, k
        if upper-lower < 1e-5 or iteration > 0 and candidate <= history[-2].get("full_dual_bound", -np.inf)+1e-7:
            break
    return lower, bestk, {"core_bins": core.tolist(), "full_bin_count": len(n),
        "tail_min_eigenvalue": float(et[0]) if len(tail) else None,
        "certificate_margin": margin, "history": history, "elapsed_seconds": time.time()-begun}


def score_file(path, use_sdp=True, restarts=96, max_core=72, use_smooth=True):
    started = time.time()
    data = np.load(path)
    v, n = data["V"], data["nbar"]
    m = len(n)
    if v.shape != (2*m, 2*m):
        raise ValueError("A complete covariance is required")
    a = v[:m, :m]
    ev = loweig(v, count=2)
    gen = float(loweig(a)[0])
    passive, port_n, passive_q = passive_eigenvalue(v, n)
    eigbound, eiginfo, rounded, seeds = eigenvector_bound(a, n)
    best, mask, search = binary_search(a, n, seeds, restarts=restarts)
    relaxed, k, sdp = gen, np.zeros_like(a), {"status": "not requested"}
    if use_sdp:
        relaxed, k, sdp = moment_certificate(a, n, best, gen, max_core=max_core)
    if use_sdp and use_smooth:
        from readout_smooth_dual import smooth_dual
        smooth, sk, smultipliers, sinfo = smooth_dual(a, n)
        if smooth > relaxed:
            relaxed, k = smooth, sk
        sdp["full_grid_smooth_dual"] = sinfo
        sdp["full_grid_smooth_bound"] = smooth
        np.savez_compressed(Path(path).with_suffix(".smooth.npz"), dual_K=sk, multipliers=smultipliers)
    lower = max(gen, eigbound, relaxed)
    vac, bath = data["Vvac"], data["Vbath"]
    weyl = float(loweig(vac)[0]+loweig(bath)[0])
    amp_weyl = float(loweig(vac[:m, :m])[0]+loweig(bath[:m, :m])[0])
    conjugate = 1.0/float(la.eigh(v[m:, m:], subset_by_index=(m-1, m-1), eigvals_only=True, check_finite=False)[0])
    b = np.sqrt(n)
    u = b*mask/la.norm(b*mask)
    residual2 = float(la.norm(a@u-best*u)**2)
    second = eiginfo["lambda_2_amp"]
    temple = float(best-residual2/(second-best)) if second > best else None
    result = {"agent": "gpt-a", "model": "gpt-6-astra", "family": "gpt",
        "label": Path(path).stem, "lambda_min": float(ev[0]), "lambda_2_full": float(ev[1]),
        "lambda_pass": passive, "passive_minimizer_port_photons": port_n,
        "lambda_gen": gen, "binary_eigen_bound": eigbound, "moment_bound": relaxed,
        "best_bound": lower, "best_binary_F": best,
        "transmitted_fraction": float(n@mask/sum(n)), "transmitted_photons": float(n@mask),
        "rounding_F": fano(b[:, None]*a*b[None, :], n, rounded),
        "eigenvector_certificate": eiginfo, "binary_search": search, "moment_certificate": sdp,
        "cheap_certificates": {"full_Weyl": weyl, "amplitude_Weyl": amp_weyl,
            "amplitude_uncertainty": conjugate, "Temple": temple,
            "Temple_valid_gap": second > best, "trial_residual_squared": residual2},
        "gap_bound_dB": float(10*np.log10(best/lower)) if lower > 0 else None,
        "gap_gen_dB": float(10*np.log10(best/gen)) if gen > 0 else None,
        "gap_min_dB": float(10*np.log10(best/ev[0])) if ev[0] > 0 else None,
        "elapsed_seconds": time.time()-started}
    if not ev[0]-1e-7 <= passive <= gen+1e-7 <= best+2e-7:
        raise AssertionError("Readout hierarchy failed")
    if lower > best+1e-6:
        raise AssertionError("A lower bound exceeds a feasible mask")
    dest = Path(path).with_suffix(".bounds.json")
    dest.write_text(json.dumps(result, indent=2)+"\n")
    np.savez_compressed(Path(path).with_suffix(".bounds.npz"), best_mask=mask,
                        eigen_rounding_mask=rounded, dual_K=k, passive_q=passive_q)
    print(json.dumps({key: result[key] for key in ("label", "lambda_min", "lambda_gen", "best_bound", "best_binary_F", "gap_bound_dB", "elapsed_seconds")}), flush=True)
    return result


def synthetic_checks(output):
    rng = np.random.default_rng(20261010)
    brightness_rng = np.random.default_rng(2026101013)
    records = []
    for j in range(16):
        m = 9 if j < 8 else 12
        q, _ = la.qr(rng.normal(size=(m, m)))
        eigenvalues = np.exp(rng.uniform(-2, 2, m))
        a = (q*eigenvalues)@q.T
        n = np.exp(rng.uniform(-3, 3, m))
        masks = ((np.arange(1, 2**m)[:, None] >> np.arange(m)) & 1).astype(float)
        b = np.sqrt(n)
        u = masks*b
        values = np.einsum("bi,ij,bj->b", u, a, u)/np.sum(u*u, axis=1)
        exact = float(values.min())
        bound, info, mask, seeds = eigenvector_bound(a, n)
        ev, vec = loweig(a, True)
        overlap_exact = float(np.max((u@vec[:, 0])**2/np.sum(u*u, axis=1)))
        assert abs(overlap_exact-info["rho_binary"]) < 1e-12
        assert bound <= exact+1e-10
        found, _, _ = binary_search(a, n, seeds, restarts=24)
        relaxed, mk, sdp = moment_certificate(a, n, exact, float(ev[0]), max_core=m, iterations=2)
        assert relaxed <= exact+1e-7
        from readout_smooth_dual import smooth_dual
        smoothed, _, _, _ = smooth_dual(a, n, betas=(50.,200.), maxiter=50)
        assert smoothed <= exact+1e-7
        triangles, tk, _, _ = smooth_dual(a, n, betas=(50.,200.), maxiter=50,triangle_core=m)
        assert triangles <= exact+1e-7
        normalized=u/np.linalg.norm(u,axis=1)[:,None]
        moment_slack=float(np.einsum('bi,ij,bj->b',normalized,mk,normalized).min())
        triangle_slack=float(np.einsum('bi,ij,bj->b',normalized,tk,normalized).min())
        assert moment_slack>=-1e-9 and triangle_slack>=-1e-9
        photon_floor=.25*sum(n)
        nu=brightness_rng.uniform(0,2,m)
        conditional=float(loweig(a-tk+np.diag(nu))[0]-nu@n/photon_floor)
        admissible=masks@n>=photon_floor
        conditional_exact=float(values[admissible].min())
        assert conditional<=conditional_exact+1e-7
        records.append({"case": j, "bins": m, "lambda_gen": float(ev[0]),
            "eigen_bound": bound, "moment_bound": relaxed,
            "smooth_dual_bound": smoothed,
            "triangle_dual_bound": triangles,
            "minimum_moment_dual_slack":moment_slack,"minimum_triangle_dual_slack":triangle_slack,
            "conditional_brightness_bound":conditional,
            "conditional_exhaustive_optimum":conditional_exact,
            "exhaustive_optimum": exact, "best_found": found,
            "overlap_error": abs(overlap_exact-info["rho_binary"])})
    result = {"agent": "gpt-a", "model": "gpt-6-astra", "family": "gpt",
              "seed": 20261010, "cases": records, "passed": True}
    Path(output).write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--synthetic")
    ap.add_argument("--no-sdp", action="store_true")
    ap.add_argument("--no-smooth", action="store_true")
    ap.add_argument("--restarts", type=int, default=96)
    ap.add_argument("--max-core", type=int, default=72)
    args = ap.parse_args()
    if args.synthetic:
        synthetic_checks(args.synthetic)
    for path in args.paths:
        score_file(path, use_sdp=not args.no_sdp, restarts=args.restarts, max_core=args.max_core,
                   use_smooth=not args.no_smooth)
