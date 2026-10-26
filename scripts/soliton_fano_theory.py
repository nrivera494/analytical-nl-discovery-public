#!/usr/bin/env python3
"""Scalar soliton linearized covariance evaluator for T-20261010-claude-interactive-06.

agent: gpt-b; model: gpt-6-astra; family: gpt.
The finite Fourier collocation is an evaluator, not a continuum error certificate.
Conventions: u_z=i*u_xx/2+i*|u|^2*u, u=sech(x)*exp(i*z/2).
Quadrature vacuum covariance is the identity.
"""
import argparse
import json
import os
from pathlib import Path
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "2")
import numpy as np
from scipy.linalg import expm, eigh, null_space


def grid_operators(n=256, window=32.0):
    dx = window / n
    x = (np.arange(n) - n // 2) * dx
    k = 2 * np.pi * np.fft.fftfreq(n, dx)
    d2 = np.fft.ifft(-(k[:, None] ** 2) * np.fft.fft(np.eye(n), axis=0), axis=0).real
    q = 1 / np.cosh(x)
    lm = -d2 / 2 + np.diag(0.5 - q * q)
    lp = -d2 / 2 + np.diag(0.5 - 3 * q * q)
    a = np.block([[np.zeros((n, n)), lm], [-lp, np.zeros((n, n))]])
    ft = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(np.eye(n), axes=0), axis=0), axes=0) / np.sqrt(n)
    return x, np.fft.fftshift(k), q, a, ft


def spectral_covariance(v, mean, ft):
    fs = ft @ mean
    phase = np.exp(-1j * np.angle(fs))
    f = phase[:, None] * ft
    amp = np.concatenate([f.real, -f.imag], axis=1)
    return amp @ v @ amp.T, fs, amp


def filter_value(mask, sigma, photons):
    selected = np.flatnonzero(mask)
    if len(selected) == 0:
        return float("inf")
    den = photons[selected].sum()
    # Restrict before summing: a tiny transmitted tail must not inherit
    # cancellation from a large photon count that has already been removed.
    num = sigma[np.ix_(selected, selected)].sum()
    return float(num / den) if den > 1e-30 else float("inf")


def best_intervals(sigma, photons):
    n = len(photons)
    best = (float("inf"), 0, 0)
    for left in range(n):
        # Add rows within each interval, rather than subtracting nearly equal
        # global prefix sums for dim spectral tails.
        local = sigma[left:, left:]
        lower_sums = np.cumsum(local, axis=1).diagonal()
        num = np.cumsum(2 * lower_sums - np.diag(local))
        den = np.cumsum(photons[left:])
        vals = np.divide(num, den, out=np.full_like(num, np.inf), where=den > 1e-25)
        j = int(np.argmin(vals))
        if vals[j] < best[0]:
            best = (float(vals[j]), left, left+j+1)
    mask = np.zeros(n)
    mask[best[1]:best[2]] = 1
    return mask, filter_value(mask, sigma, photons)


def bit_descent(mask, sigma, photons, max_steps=10000):
    mask = np.array(mask, dtype=float, copy=True)
    diag = np.diag(sigma)
    for step in range(max_steps):
        den = photons @ mask
        with np.errstate(over='ignore', divide='ignore', invalid='ignore'):
            sm = sigma @ mask
        num = filter_value(mask, sigma, photons) * den
        flips = 1 - 2 * mask
        ds = den + flips * photons
        ns = num + 2 * flips * sm + diag
        vals = np.divide(ns, ds, out=np.full_like(ns, np.inf), where=ds > 1e-25)
        if np.count_nonzero(mask) == 1:
            vals[mask > 0] = np.inf
        i = int(np.argmin(vals))
        if vals[i] >= num / den - 1e-13:
            break
        candidate = mask.copy(); candidate[i] += flips[i]
        if filter_value(candidate, sigma, photons) >= num / den - 1e-13:
            break
        mask = candidate
    return mask, filter_value(mask, sigma, photons)


def search_binary(vamp, fs, seed=20261010, starts=64, anneal_steps=10000):
    photons_all = abs(fs) ** 2
    active = photons_all > photons_all.max() * 1e-12
    p = photons_all[active]
    va = vamp[np.ix_(active, active)]
    sigma = np.sqrt(p[:, None] * p[None, :]) * va
    interval, fv = best_intervals(sigma, p)
    seeds = [interval, np.ones(len(p))]
    _, eig = eigh(va, subset_by_index=[0, 0])
    weight = eig[:, 0] / np.sqrt(p)
    for sign in (-1, 1):
        for threshold in np.quantile(sign * weight, np.linspace(0.05, 0.95, 10)):
            seeds.append((sign * weight >= threshold).astype(float))
    rng = np.random.default_rng(seed)
    while len(seeds) < starts:
        seeds.append((rng.random(len(p)) < rng.uniform(0.1, 0.9)).astype(float))
    best_mask, best = interval.copy(), fv
    for mask in seeds:
        if not mask.any():
            continue
        mask, val = bit_descent(mask, sigma, p)
        if val < best:
            best_mask, best = mask, val
    mask = best_mask.copy()
    for sweep in range(4):
        den = p @ mask
        sm = sigma @ mask
        num = mask @ sm
        for it in range(anneal_steps):
            i = rng.integers(len(p)); d = 1 - 2 * mask[i]
            if d < 0 and np.count_nonzero(mask) == 1:
                continue
            if it % 128 == 0:
                den = p @ mask
                with np.errstate(over='ignore', divide='ignore', invalid='ignore'):
                    sm = sigma @ mask
                num = filter_value(mask, sigma, p) * den
            nd = den + d * p[i]
            if nd <= 1e-25:
                continue
            nn = num + 2 * d * sm[i] + sigma[i, i]
            delta = nn / nd - num / den
            temp = 0.05 * (1e-4 / 0.05) ** (it / max(anneal_steps - 1, 1))
            if delta < 0 or rng.random() < np.exp(-delta / temp):
                mask[i] += d; sm += d * sigma[:, i]; num, den = nn, nd
                if num / den < best:
                    direct_value = filter_value(mask, sigma, p)
                    if direct_value < best:
                        best_mask, best = mask.copy(), direct_value
        mask, val = bit_descent(mask, sigma, p)
        if val < best:
            best_mask, best = mask, val
        mask = best_mask.copy()
    best = filter_value(best_mask, sigma, p)
    if not np.isfinite(best) or not best_mask.any() or best < 0:
        raise FloatingPointError('Invalid final binary-mask score')
    result_mask = np.zeros(len(fs)); result_mask[active] = best_mask
    interval_mask = np.zeros(len(fs)); interval_mask[active] = interval
    return result_mask, {
        "best_binary_found": best,
        "best_interval": fv,
        "active_bins": int(active.sum()),
        "discarded_mean_fraction": float(photons_all[~active].sum() / photons_all.sum()),
        "starts": len(seeds), "annealing_sweeps": 4, "steps_per_sweep": anneal_steps,
        "seed": seed, "global_optimality_certified": False,
        "final_score_recomputed_directly": True,
        "interval_indices": np.flatnonzero(interval_mask).tolist(),
        "binary_indices": np.flatnonzero(result_mask).tolist(),
    }


def score_covariance(v, mean, ft, seed=20261010, starts=64, anneal_steps=10000):
    vamp, fs, amp = spectral_covariance(v, mean, ft)
    lmin = float(eigh(v, eigvals_only=True, subset_by_index=[0, 0])[0])
    lgen = float(eigh(vamp, eigvals_only=True, subset_by_index=[0, 0])[0])
    phase = np.r_[-mean.imag, mean.real]
    basis = null_space(phase.reshape(1, -1))
    lpass = float(eigh(basis.T @ v @ basis, eigvals_only=True, subset_by_index=[0, 0])[0])
    mask, out = search_binary(vamp, fs, seed, starts, anneal_steps)
    out.update(lambda_min=lmin, lambda_pass=lpass, lambda_gen=lgen)
    for key in ("lambda_min", "lambda_pass", "lambda_gen", "best_binary_found", "best_interval"):
        out[key + "_dB"] = float(10 * np.log10(out[key]))
    out["gap_gen_to_binary_dB"] = out["best_binary_found_dB"] - out["lambda_gen_dB"]
    out["gap_min_to_binary_dB"] = out["best_binary_found_dB"] - out["lambda_min_dB"]
    out["full_filter_F"] = filter_value(np.ones(len(fs)), np.sqrt(abs(fs[:, None]) ** 2 * abs(fs[None, :]) ** 2) * vamp, abs(fs) ** 2)
    return out, mask, vamp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=256)
    ap.add_argument("--window", type=float, default=32.0)
    ap.add_argument("--z", nargs="+", type=float, default=[0, 1, 2, 3, 4, 4.71238898038469, 6, 8])
    ap.add_argument("--raw", required=True)
    ap.add_argument("--starts", type=int, default=64)
    ap.add_argument("--anneal-steps", type=int, default=10000)
    args = ap.parse_args(); dest = Path(args.raw); dest.mkdir(parents=True, exist_ok=True)
    x, k, q, a, ft = grid_operators(args.n, args.window)
    summary = {"agent": "gpt-b", "model": "gpt-6-astra", "family": "gpt", "n": args.n, "window": args.window, "points": []}
    for z in args.z:
        start = time.monotonic()
        m = expm(a * z); v = m @ m.T
        row, mask, vamp = score_covariance(v, q.astype(complex), ft, starts=args.starts, anneal_steps=args.anneal_steps)
        row.update(z_over_LD=z, z_over_z0=2*z/np.pi, wall_time_s=time.monotonic()-start)
        summary["points"].append(row)
        np.savez_compressed(dest / f"cov_z{z:.8g}.npz", x=x, k=k, q=q, M=m, V=v, Vamp=vamp, mask=mask)
        (dest / "summary.json").write_text(json.dumps(summary, indent=2))
        print(json.dumps({key: val for key,val in row.items() if not key.endswith("indices")}), flush=True)


if __name__ == "__main__":
    main()
