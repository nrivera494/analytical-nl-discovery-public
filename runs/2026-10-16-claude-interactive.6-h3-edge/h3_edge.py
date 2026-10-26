"""H3: loss-edge photon budget and optimal length, Z75 fibre (ZrF4 7.5/125 NA 0.30), fundamental soliton at 2.8 um,
T0 = 20 fs, edge 1 dB/m at 4.2 um (B = 92 um).  Frozen in commit 4f0f1ff.
Usage: python h3_edge.py <mode const|pc> <dz_mm> <dt_fs>"""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

RUN = "2026-10-16-claude-interactive.6-h3-edge"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN}")
os.makedirs(RAW, exist_ok=True)
mode = sys.argv[1] if len(sys.argv) > 1 else "const"
dz = float(sys.argv[2]) * 1e-3 if len(sys.argv) > 2 else 2.5e-4
dt = float(sys.argv[3]) * 1e-3 if len(sys.argv) > 3 else 0.006
T0 = float(sys.argv[4]) * 1e-3 if len(sys.argv) > 4 else 0.020
lam_ref = float(sys.argv[5]) if len(sys.argv) > 5 else 3.7
L = 8.0
fz = StepIndexFiber("ZrF4", 3.75, 0.30, n=600, n2=2.1e-20)
rz = OscillatorRaman(0.20, 0.0209, 0.053)
B = 92.0; A = 1.0 * np.exp(B / 4.2)
alpha = lambda w: edge_loss(w, A, B)
wp = wl_to_w(2.8)
aeff0 = float(fz.aeff_um2(np.array([wp]))[0])
wg = wl_to_w(3.3)
nt = 2 ** 14
g = Grid(nt, dt, wg)
aw = (lambda w: np.full_like(np.asarray(w, float), aeff0)) if mode == "const" else fz.aeff_um2
# frame: group velocity at 3.7 um (the soliton creeps near there for most of the length)
sim = GNLSE(g, fz.beta, fz.n2, aw, aeff0, raman=rz, alpha_w=alpha, shock=True, aeff_mode=mode, w_ref=wl_to_w(lam_ref))
b2 = abs(fz.beta2(np.array([wp]))[0])
gam = fz.n2 * wp / C_M_PS / (aeff0 * 1e-12)
P0 = b2 / (gam * T0 ** 2)
A0 = sech_pulse(g, P0, T0, W_off=wp - wg)
N0 = sim.photons(A0)
lcs = [3.3, 3.4, 3.5, 3.6, 3.7]


def diag(z, Aw):
    At = np.fft.fft(Aw); I = np.abs(At) ** 2
    k = int(np.argmax(I))
    idx = (np.arange(nt) - k + nt // 2) % nt - nt // 2
    # soliton window +-1.5 ps around the peak (soliton FWHM < 0.4 ps throughout)
    win = np.abs(idx) * g.dt <= 1.5
    Aw1 = np.fft.ifft(np.where(win, At, 0))
    d = {"z": z, "Ntot": float(sim.photons(Aw) / N0), "Nsol": float(sim.photons(Aw1) / N0), "lam_sol": float(w_to_wl(sim.mean_w(Aw1))),
         "t_peak_ps": float(((k + nt // 2) % nt - nt // 2) * g.dt), "edge_frac": float((I[np.abs(idx) > nt // 2 - 200].sum()) / I.sum())}
    for lc in lcs:
        d[f"eta_{lc}"] = float(sim.photons(Aw, g.w < wl_to_w(lc)) / N0)
    return d


t0 = time.time()
out = sim.run(A0, L, dz, n_save=160, callback=diag)
Dg = out["diag"]
res = {"run_id": RUN, "mode": mode, "T0_fs": T0 * 1e3, "frame_lambda_um": lam_ref, "dz_mm": out["dz"] * 1e3, "dt_fs": dt * 1e3, "nt": nt, "L_m": L, "E_pJ": 2 * P0 * T0,
       "wall_s": time.time() - t0, "grid_lambda_range_um": [float(w_to_wl(g.w.max())), float(w_to_wl(max(g.w.min(), 1e-3)))]}
zz = np.array([d["z"] for d in Dg])
for zq in [2.0, 4.0, 6.0, 8.0]:
    k = int(np.argmin(abs(zz - zq)))
    res[f"at_{zq}m"] = {"Nsol": Dg[k]["Nsol"], "Ntot": Dg[k]["Ntot"], "lam_sol_um": Dg[k]["lam_sol"]}
for lc in lcs:
    e = np.array([d[f"eta_{lc}"] for d in Dg]); k = int(np.argmax(e))
    res[f"opt_{lc}"] = {"eta_star": float(e[k]), "L_star_m": float(zz[k]), "interior": bool(k < len(zz) - 1)}
res["max_edge_frac"] = float(max(d["edge_frac"] for d in Dg))
res["max_abs_t_peak_ps"] = float(max(abs(d["t_peak_ps"]) for d in Dg))
res["traj"] = [[round(d["z"], 3), round(d["Nsol"], 4), round(d["Ntot"], 4), round(d["lam_sol"], 4)] for d in Dg[::8]]
tag = f"{mode}_T0{T0*1e3:.0f}fs_dz{dz*1e3:.3f}mm_dt{dt*1e3:.1f}fs" + ("" if lam_ref == 3.7 else f"_frame{lam_ref}um")
np.savez_compressed(os.path.join(RAW, tag + ".npz"), Aw=out["Aw"], w=g.w, diag=json.dumps(Dg))
sp = os.path.join(HERE, "summary.json")
allr = json.load(open(sp)) if os.path.exists(sp) else {}
allr[tag] = res
json.dump(allr, open(sp, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "traj"}, indent=1))
