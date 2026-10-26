"""Second solver for H3 / claim C-20261016-claude-interactive.6-01: the main Z75 case (const Aeff, T0 = 20 fs, 8 m)
run with the agents' Julia solver (b9fa957).  Differences from the numpy run, by construction:
the Julia frame is the group velocity at the grid centre (3.3 um, numpy used 3.7 um), the Raman kernel is
sampled in time at dt = 6 fs (numpy uses the analytic spectrum), and the solver applies its blue-edge window.
Observables are computed with the same soliton window as h3_edge.py."""
import sys, os, json, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
COMMON = os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common")
sys.path.insert(0, COMMON)
import numpy as np
from lwir import *

RUN = "2026-10-16-claude-interactive.6-h3-edge"
D = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN}/julia_case")
os.makedirs(D, exist_ok=True)
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
fz = StepIndexFiber("ZrF4", 3.75, 0.30, n=600, n2=2.1e-20)
B_ = 92.0; A_ = 1.0 * np.exp(B_ / 4.2)
alpha = lambda w: edge_loss(w, A_, B_)
wp = wl_to_w(2.8); wg = wl_to_w(3.3)
aeff0 = float(fz.aeff_um2(np.array([wp]))[0])
nt, dt, L, dz = 2 ** 14, 0.006, 8.0, 2.5e-4
g = Grid(nt, dt, wg)
b2 = abs(fz.beta2(np.array([wp]))[0]); gam = fz.n2 * wp / C_M_PS / (aeff0 * 1e-12)
T0 = 0.020; P0 = b2 / (gam * T0 ** 2)
A0w = sech_pulse(g, P0, T0, W_off=wp - wg)
At_c = at_from_aw(A0w)
Wc = np.fft.fftshift(g.W)
np.savetxt(os.path.join(D, "omega.txt"), Wc)
np.savetxt(os.path.join(D, "beta.txt"), fz.beta(wg + Wc))
np.savetxt(os.path.join(D, "alpha.txt"), alpha(wg + Wc))
np.savetxt(os.path.join(D, "At.txt"), np.c_[At_c.real, At_c.imag])
with open(os.path.join(D, "params.txt"), "w") as f:
    for k, v in dict(nt=nt, dt=dt, omega0=wg, L=L, dz=dz, n2=fz.n2, S=1 / (aeff0 * 1e-12),
                     fR=0.20, tau1=0.0209, tau2=0.053, nsave=80).items():
        f.write(f"{k} {v!r}\n")
t0 = time.time()
r = subprocess.run(["julia", "--project=" + os.path.join(REPO, "solver"), os.path.join(COMMON, "jl_forward_planes.jl"), D],
                   capture_output=True, text=True, env=dict(os.environ, JULIA_NUM_THREADS="2"))
print(r.stdout[-500:], r.stderr[-2000:])
z = np.loadtxt(os.path.join(D, "jl_planes_z.txt"))
raw = np.fromfile(os.path.join(D, "jl_planes_B.bin"), dtype=np.float64)
npl = len(z)
Bc = (raw[: nt * npl] + 1j * raw[nt * npl:]).reshape((npl, nt))          # column-major nt x npl -> rows are planes
wabs = wg + Wc
N0 = float((np.abs(Bc[0]) ** 2).sum())
rows = []
for k in range(npl):
    b = Bc[k]                                    # photon-unit spectrum, centred
    # time-domain envelope of the photon-unit field is enough to locate the soliton; use power-unit field for the window
    weights = np.where(wabs > 0, (nt * dt * 1e-12) / (HBAR * np.maximum(wabs, 1e-30) * 1e12), 0)
    a = np.where(weights > 0, b / np.sqrt(np.maximum(weights, 1e-300)), 0)       # power units, centred
    At = np.fft.fft(np.fft.ifftshift(a)); I = np.abs(At) ** 2
    kk = int(np.argmax(I)); idx = (np.arange(nt) - kk + nt // 2) % nt - nt // 2
    win = np.abs(idx) * dt <= 1.5
    a1 = np.fft.fftshift(np.fft.ifft(np.where(win, At, 0)))
    n1 = np.abs(a1) ** 2 * weights
    rec = {"z": float(z[k]), "Nsol": float(n1.sum() / N0), "Ntot": float((np.abs(b) ** 2).sum() / N0),
           "lam_sol": float(w_to_wl((n1 * wabs).sum() / n1.sum()))}
    for lc in [3.3, 3.4, 3.5, 3.6, 3.7]:
        rec[f"eta_{lc}"] = float((np.abs(b[wabs < wl_to_w(lc)]) ** 2).sum() / N0)
    rows.append(rec)
res = {"wall_s_incl_compile": time.time() - t0, "solver_commit": "b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa"}
zz = np.array([r_["z"] for r_ in rows])
for zq in [2.0, 4.0, 6.0, 8.0]:
    k = int(np.argmin(abs(zz - zq)))
    res[f"at_{zq}m"] = {"Nsol": rows[k]["Nsol"], "Ntot": rows[k]["Ntot"], "lam_sol_um": rows[k]["lam_sol"]}
for lc in [3.3, 3.4, 3.5, 3.6, 3.7]:
    e = np.array([r_[f"eta_{lc}"] for r_ in rows]); k = int(np.argmax(e))
    res[f"opt_{lc}"] = {"eta_star": float(e[k]), "L_star_m": float(zz[k]), "interior": bool(k < len(zz) - 1)}
json.dump(res, open(os.path.join(HERE, "summary_julia_crosscheck.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
