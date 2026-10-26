"""Claim C-20261016-claude-interactive.6-01, relaxed assumption 2 (protocol frozen in commit 638af7a):
a soliton born from fission.  TL sech N = 2, T0 = 40 fs at 2.8 um in Z75 (const Aeff, edge, Raman stand-in), L = 8 m.
Leading soliton isolated in time (+-8 T window), separation plane by the h2_reach_post criterion, then the full-response
ODE with loss from (z_s, w1, N1) compared at 2, 4, 6, 8 m."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

RUN = "2026-10-16-claude-interactive.6-h3-edge"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN}")
fz = StepIndexFiber("ZrF4", 3.75, 0.30, n=600, n2=2.1e-20)
rz = OscillatorRaman(0.20, 0.0209, 0.053)
B = 92.0; A = 1.0 * np.exp(B / 4.2)
alpha = lambda w: edge_loss(w, A, B)
wp = wl_to_w(2.8); wg = wl_to_w(3.3)
aeff0 = float(fz.aeff_um2(np.array([wp]))[0])
ac = lambda w: np.full_like(np.asarray(w, float), aeff0)
nt, dt, L, dz = 2 ** 14, 0.003, 8.0, 1.0e-4
g = Grid(nt, dt, wg)
sim = GNLSE(g, fz.beta, fz.n2, ac, aeff0, raman=rz, alpha_w=alpha, shock=True, aeff_mode="const", w_ref=wl_to_w(3.8))
b2 = abs(fz.beta2(np.array([wp]))[0]); gam = fz.n2 * wp / C_M_PS / (aeff0 * 1e-12)
N, T0 = 2, 0.040
P0 = N ** 2 * b2 / (gam * T0 ** 2)
A0 = sech_pulse(g, P0, T0, W_off=wp - wg)
Ntot = sim.photons(A0)


def _window_stats(At, I, k):
    half = I[k] / 2
    r = 0
    while r < nt // 2 and I[(k + r) % nt] > half: r += 1
    l = 0
    while l < nt // 2 and I[(k - l) % nt] > half: l += 1
    T = max((r + l) * dt / 1.763, 2 * dt)
    idx = (np.arange(nt) - k + nt // 2) % nt - nt // 2
    Aw1 = np.fft.ifft(np.where(np.abs(idx) * dt <= 8 * T, At, 0))
    ring = (np.abs(idx) * dt > 8 * T) & (np.abs(idx) * dt <= 16 * T)
    return dict(N=float(sim.photons(Aw1)), w=float(sim.mean_w(Aw1)), T=float(T), P=float(I[k]),
                iso=float(I[ring].max() / I[k]) if ring.any() else 0.0)


def leading(Aw):
    """Leading soliton = the pulse carrying the most photons among the five highest peaks (the highest-peak rule picks a
    weak blue soliton once the red soliton has broadened in strong dispersion; first run of this script, see the log)."""
    from scipy.signal import find_peaks
    At = np.fft.fft(Aw); I = np.abs(At) ** 2
    pk, _ = find_peaks(np.concatenate([I, I[:50]]), height=0.02 * I.max(), distance=20)
    pk = np.unique(pk % nt)
    pk = pk[np.argsort(I[pk])[::-1][:5]] if len(pk) else np.array([int(np.argmax(I))])
    cands = [_window_stats(At, I, int(k)) for k in pk]
    big = [c for c in cands if c["N"] >= 0.1 * Ntot]
    if not big:
        return max(cands, key=lambda d: d["N"])
    return min(big, key=lambda d: d["w"])     # v3: the reddest pulse carrying at least 10% of the photons


t0 = time.time()
out = sim.run(A0, L, dz, n_save=160, callback=lambda z, Aw: dict(z=z, **leading(Aw), Nall=float(sim.photons(Aw))))
D = out["diag"]
z = np.array([d["z"] for d in D]); N1 = np.array([d["N"] for d in D]); w1 = np.array([d["w"] for d in D])
f1 = N1 / Ntot; iso = np.array([d["iso"] for d in D]); P = np.array([d["P"] for d in D])
kc = int(np.argmax(P[: len(P) // 2 + 1]))
ks = next((k for k in range(kc + 1, len(D)) if f1[k] <= 1.05 * f1[-1] and iso[k] < 0.05), None)
res = {"run_id": RUN, "case": "fission_born_N2_T40fs", "leading_rule": "reddest pulse with >= 10% of the photons among the 5 highest peaks (v3)", "E_pJ": 2 * P0 * T0, "dz_mm": dz * 1e3, "dt_fs": dt * 1e3,
       "nt": nt, "wall_s": time.time() - t0, "z_compression_m": float(z[kc]), "f1_final": float(f1[-1]),
       "IST_fraction": (2 * N - 1) / N ** 2}
if ks is not None:
    res.update({"z_sep_m": float(z[ks]), "f1_at_sep": float(f1[ks]), "lam1_at_sep_um": float(w_to_wl(w1[ks]))})
    m = ReachModel(fz, rz, alpha_w=alpha, rate="exact", aeff_const_um2=aeff0, npts=6001)
    zr, wr, Nr, Tr = m.integrate(w1[ks], N1[ks], L - z[ks], dz=(L - z[ks]) / 4000, n_out=800)
    zr = zr + z[ks]
    cmp_ = {}
    for zq in [2.0, 4.0, 6.0, 8.0]:
        if zq < z[ks]:
            continue
        k = int(np.argmin(abs(z - zq))); km = int(np.argmin(abs(zr - zq)))
        cmp_[str(zq)] = {"N1_rel_gnlse": float(N1[k] / N1[ks]), "N1_rel_model": float(Nr[km] / N1[ks]),
                         "lam1_gnlse_um": float(w_to_wl(w1[k])), "lam1_model_um": float(w_to_wl(wr[km]))}
    res["comparison"] = cmp_
    res["max_abs_dN_rel"] = max(abs(v["N1_rel_gnlse"] - v["N1_rel_model"]) for v in cmp_.values())
    res["max_abs_dlam_um"] = max(abs(v["lam1_gnlse_um"] - v["lam1_model_um"]) for v in cmp_.values())
np.savez_compressed(os.path.join(RAW, "fission_born_N2_T40fs_v3.npz"), Aw=out["Aw"], w=g.w, diag=json.dumps(D))
json.dump(res, open(os.path.join(HERE, "summary_fission_born.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
