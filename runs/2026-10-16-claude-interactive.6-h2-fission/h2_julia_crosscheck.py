"""Second solver for H2.1: leading-soliton photon fraction f1 after fission, computed from fields of the agents' Julia
solver (b9fa957).  (i) TL N = 4, T_FWHM = 300 fs, L = 4 m, with the silica IR edge, same grid as h2_fission.py except
that the Julia frame is the grid-centre group velocity.  (ii) TL N = 3, 100 fs, L = 1 m, lossless: the final field saved
by ../2026-10-16-claude-interactive.6-h1-conservation/h1_julia_crosscheck.py (no new run)."""
import sys, os, json, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
COMMON = os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common")
sys.path.insert(0, COMMON); sys.path.insert(0, HERE)
import numpy as np
from lwir import *
from h2_fission import fib, ram, wp, wg, aeff0, alpha, b2, gam

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))


def f1_from_centred_photon_field(Bc, nt, dt, w0, Ntot):
    """Leading-soliton photon fraction from a centred photon-unit spectrum (same window rule as h2_fission.leading)."""
    Wc = np.fft.fftshift(2 * np.pi * np.fft.fftfreq(nt, dt)); wabs = w0 + Wc
    weights = np.where(wabs > 0, (nt * dt * 1e-12) / (HBAR * np.maximum(wabs, 1e-30) * 1e12), 0)
    a = np.where(weights > 0, Bc / np.sqrt(np.maximum(weights, 1e-300)), 0)
    At = np.fft.fft(np.fft.ifftshift(a)); I = np.abs(At) ** 2
    k = int(np.argmax(I)); half = I[k] / 2
    r = 0
    while r < nt // 2 and I[(k + r) % nt] > half: r += 1
    l = 0
    while l < nt // 2 and I[(k - l) % nt] > half: l += 1
    T = max((r + l) * dt / 1.763, 2 * dt)
    idx = (np.arange(nt) - k + nt // 2) % nt - nt // 2
    win = np.abs(idx) * dt <= 8 * T
    a1 = np.fft.fftshift(np.fft.ifft(np.where(win, At, 0)))
    n1 = np.abs(a1) ** 2 * weights
    return float(n1.sum() / Ntot), float(w_to_wl((n1 * wabs).sum() / n1.sum())), T


res = {"solver_commit": "b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa"}
# (i) N = 4, 300 fs, 4 m, with loss
D = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-16-claude-interactive.6-h2-fission/julia_N4_300fs")
os.makedirs(D, exist_ok=True)
nt, dt, L, N, T0 = 2 ** 14, 0.003, 4.0, 4, 0.1702
g = Grid(nt, dt, wg)
P0 = N ** 2 * b2 / (gam * T0 ** 2)
A0w = sech_pulse(g, P0, T0, W_off=wp - wg)
At_c = at_from_aw(A0w); Wc = np.fft.fftshift(g.W)
np.savetxt(os.path.join(D, "omega.txt"), Wc)
np.savetxt(os.path.join(D, "beta.txt"), fib.beta(wg + Wc))
np.savetxt(os.path.join(D, "alpha.txt"), alpha(wg + Wc))
np.savetxt(os.path.join(D, "At.txt"), np.c_[At_c.real, At_c.imag])
with open(os.path.join(D, "params.txt"), "w") as f:
    for k_, v in dict(nt=nt, dt=dt, omega0=wg, L=L, dz=1e-3, n2=fib.n2, S=1 / (aeff0 * 1e-12),
                      fR=0.18, tau1=0.0122, tau2=0.032, nsave=4).items():
        f.write(f"{k_} {v!r}\n")
t0 = time.time()
r = subprocess.run(["julia", "--project=" + os.path.join(REPO, "solver"), os.path.join(COMMON, "jl_forward_planes.jl"), D],
                   capture_output=True, text=True, env=dict(os.environ, JULIA_NUM_THREADS="2"))
print(r.stdout[-300:], r.stderr[-1500:])
z = np.loadtxt(os.path.join(D, "jl_planes_z.txt")); npl = len(z)
raw = np.fromfile(os.path.join(D, "jl_planes_B.bin"), dtype=np.float64)
Bc = (raw[: nt * npl] + 1j * raw[nt * npl:]).reshape((npl, nt))
N0 = float((np.abs(Bc[0]) ** 2).sum())
f1, lam1, T1 = f1_from_centred_photon_field(Bc[-1], nt, dt, wg, N0)
res["N4_300fs_L4m"] = {"f1_julia": f1, "lam1_julia_um": lam1, "T1_fs": T1 * 1e3, "wall_s": time.time() - t0,
                       "f1_numpy": 0.6652230893823284, "cap_2_over_N": 0.5}
print(res["N4_300fs_L4m"], flush=True)
# (ii) N = 3, 100 fs, 1 m, lossless: H1 Julia case (saved final field)
D1 = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-16-claude-interactive.6-h1-conservation/julia_case")
B = np.loadtxt(os.path.join(D1, "jl_out_Aw_photon.txt")); B = B[:, 0] + 1j * B[:, 1]
NJ = np.loadtxt(os.path.join(D1, "jl_out_N.txt"))
f1b, lam1b, T1b = f1_from_centred_photon_field(B, 2 ** 13, 0.003, wg, NJ[0, 1])
res["N3_100fs_L1m_lossless"] = {"f1_julia": f1b, "lam1_julia_um": lam1b, "T1_fs": T1b * 1e3,
                                "f1_numpy_with_edge": 0.7123594214211001, "cap_2_over_N": 2 / 3}
print(res["N3_100fs_L1m_lossless"])
json.dump(res, open(os.path.join(HERE, "summary_julia_crosscheck.json"), "w"), indent=1)
