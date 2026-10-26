"""H2.1 / H2.3: TL sech fission in S28 (const Aeff, shock, Raman, silica IR edge).
Leading-soliton photon fraction vs IST and vs the sketch-1 input-content cap 2/N; reach law from the separation plane.
Frozen in commit 4f0f1ff.  Usage: python h2_fission.py [N T0_fs L_m] (no args: all cases)."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

RUN = "2026-10-16-claude-interactive.6-h2-fission"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN}")
os.makedirs(RAW, exist_ok=True)
fib = StepIndexFiber("SiO2", 4.1, 0.14, n=600, n2=2.6e-20)
ram = OscillatorRaman(0.18, 0.0122, 0.032)
wp = wl_to_w(1.55); wg = wl_to_w(1.75)
aeff0 = float(fib.aeff_um2(np.array([wp]))[0])
ac = lambda w: np.full_like(np.asarray(w, float), aeff0)
alpha = lambda w: edge_loss(w, 7.81e8, 48.48)          # 7.81e11 dB/km -> 7.81e8 dB/m
b2 = abs(fib.beta2(np.array([wp]))[0]); gam = fib.n2 * wp / C_M_PS / (aeff0 * 1e-12)


def leading(g, sim, Aw):
    """Isolate the highest-peak pulse in time; return photons, photon-mean frequency, T (FWHM/1.763), isolation."""
    At = np.fft.fft(Aw)                      # fft-order time samples t_j = j dt (periodic)
    I = np.abs(At) ** 2
    k = int(np.argmax(I)); nt = g.nt
    half = I[k] / 2
    r = 0
    while r < nt // 2 and I[(k + r) % nt] > half: r += 1
    l = 0
    while l < nt // 2 and I[(k - l) % nt] > half: l += 1
    T = max((r + l) * g.dt / 1.763, 2 * g.dt)
    idx = (np.arange(nt) - k + nt // 2) % nt - nt // 2      # signed sample offset from the peak
    win = np.abs(idx) * g.dt <= 8 * T
    Wn = np.where(win, At, 0)
    Aw1 = np.fft.ifft(Wn)
    ring = (np.abs(idx) * g.dt > 8 * T) & (np.abs(idx) * g.dt <= 16 * T)
    iso = float(I[ring].max() / I[k]) if ring.any() else 0.0
    return dict(N=float(sim.photons(Aw1)), w=float(sim.mean_w(Aw1)), T=float(T), P=float(I[k]), iso=iso)


def run_case(N, T0, L, nt=2 ** 14, dt=0.003):
    g = Grid(nt, dt, wg)
    sim = GNLSE(g, fib.beta, fib.n2, ac, aeff0, raman=ram, alpha_w=alpha, shock=True, aeff_mode="const", w_ref=wl_to_w(1.65))
    P0 = N ** 2 * b2 / (gam * T0 ** 2)
    A0 = sech_pulse(g, P0, T0, W_off=wp - wg)
    Ntot = sim.photons(A0)
    T1 = T0 / (2 * N - 1)
    dz = min(1e-3, np.pi / 2 * T1 ** 2 / b2 / 40)
    t0 = time.time()
    def diag(z, Aw):
        d = leading(g, sim, Aw); d["z"] = z; d["Ntot"] = float(sim.photons(Aw))
        for lc in [1.7, 1.8, 1.9, 2.0, 2.1]:
            d[f"eta_{lc}"] = float(sim.photons(Aw, g.w < wl_to_w(lc)) / Ntot)
        return d
    out = sim.run(A0, L, dz, n_save=80, callback=diag)
    D = out["diag"]
    np.savez_compressed(os.path.join(RAW, f"N{N}_T{T0*1e3:.1f}fs_L{L}m" + ("" if dt == 0.003 else f"_dt{dt*1e3:.1f}fs") + ".npz"), Aw=out["Aw"], w=g.w,
                        diag=json.dumps(D))
    f1 = np.array([d["N"] for d in D]) / Ntot
    iso = np.array([d["iso"] for d in D]); zz = np.array([d["z"] for d in D])
    # separation plane: first plane after the global max of peak power where the ring is < 2% of the peak
    kmax = int(np.argmax([d["P"] for d in D[: len(D) // 2 + 1]]))
    ks = next((k for k in range(kmax, len(D)) if iso[k] < 0.02), None)
    rec = {"N": N, "T0_fs": T0 * 1e3, "L_m": L, "nt": g.nt, "dt_fs": g.dt * 1e3, "dz_mm": out["dz"] * 1e3, "E_pJ": 2 * P0 * T0, "wall_s": time.time() - t0,
           "f1_final": float(f1[-1]), "f1_max": float(f1[ks:].max()) if ks is not None else None,
           "IST_fraction": (2 * N - 1) / N ** 2, "cap_2_over_N": 2 / N,
           "lam1_final_um": float(w_to_wl(D[-1]["w"])), "T1_final_fs": D[-1]["T"] * 1e3,
           "eta_final": {k: v for k, v in D[-1].items() if k.startswith("eta_")},
           "photon_drift_total": float((D[-1]["Ntot"] - D[0]["Ntot"]) / D[0]["Ntot"])}
    if ks is not None:
        rec["z_sep_m"] = float(zz[ks]); rec["f1_at_sep"] = float(f1[ks]); rec["lam1_at_sep_um"] = float(w_to_wl(D[ks]["w"]))
        m = ReachModel(fib, ram, alpha_w=alpha, rate="exact", aeff_const_um2=aeff0)
        zr, wr, Nr, Tr = m.integrate(D[ks]["w"], D[ks]["N"], L - zz[ks], dz=(L - zz[ks]) / 3000)
        rec["reach_model_lam_final_um"] = float(w_to_wl(wr[-1]))
        sh_g = D[ks]["w"] - D[-1]["w"]; sh_m = D[ks]["w"] - wr[-1]
        rec["shift_after_sep_gnlse"] = float(sh_g); rec["shift_after_sep_model"] = float(sh_m)
        rec["reach_rel_err"] = float((sh_m - sh_g) / sh_g)
        mg = ReachModel(fib, ram, alpha_w=alpha, rate="gordon", aeff_const_um2=aeff0)
        zg, wgd, Ng, Tg = mg.integrate(D[ks]["w"], D[ks]["N"], L - zz[ks], dz=(L - zz[ks]) / 3000)
        rec["reach_rel_err_gordon"] = float((D[ks]["w"] - wgd[-1] - sh_g) / sh_g)
    rec["traj"] = [[round(d["z"], 4), round(d["N"] / Ntot, 4), round(float(w_to_wl(d["w"])), 4), round(d["T"] * 1e3, 2), round(d["iso"], 4)] for d in D[::4]]
    return rec


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cases = [(int(sys.argv[1]), float(sys.argv[2]) * 1e-3, float(sys.argv[3]))]
        extra = dict(nt=int(sys.argv[4]), dt=float(sys.argv[5]) * 1e-3) if len(sys.argv) > 5 else {}
    else:
        cases = [(3, 0.0567, 1.0), (4, 0.0567, 1.0), (6, 0.0567, 1.0), (3, 0.1702, 4.0), (4, 0.1702, 4.0), (6, 0.1702, 4.0)]
    allres = []
    sp = os.path.join(HERE, "summary.json")
    if os.path.exists(sp):
        allres = json.load(open(sp))["cases"]
    extra = locals().get("extra", {})
    for N, T0, L in cases:
        rec = run_case(N, T0, L, **extra)
        allres = [r for r in allres if not (r["N"] == N and abs(r["T0_fs"] - T0 * 1e3) < 0.1 and r["L_m"] == L and r["dz_mm"] == rec["dz_mm"] and r.get("dt_fs", 3.0) == rec["dt_fs"])] + [rec]
        json.dump({"run_id": RUN, "cases": allres}, open(sp, "w"), indent=1)
        print(json.dumps({k: v for k, v in rec.items() if k != "traj"}), flush=True)
