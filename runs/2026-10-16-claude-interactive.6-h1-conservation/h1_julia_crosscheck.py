"""H1(g): same case as h1_numpy.py (const Aeff, dz = 0.25 mm) run with the agents' Julia solver; compare."""
import sys, os, json, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
COMMON = os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common")
sys.path.insert(0, COMMON)
import numpy as np
from lwir import *

RUN = "2026-10-16-claude-interactive.6-h1-conservation"
D = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN}/julia_case")
os.makedirs(D, exist_ok=True)
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

fib = StepIndexFiber("SiO2", 4.1, 0.14, n=600, n2=2.6e-20)
wp = wl_to_w(1.55); wg = wl_to_w(1.75)
g = Grid(2 ** 13, 0.003, wg)
aeff0 = float(fib.aeff_um2(np.array([wp]))[0])
b2 = abs(fib.beta2(np.array([wp]))[0]); gam = fib.n2 * wp / C_M_PS / (aeff0 * 1e-12)
P0 = 9 * b2 / (gam * 0.0567 ** 2)
A0w = sech_pulse(g, P0, 0.0567, W_off=wp - wg)
At_c = at_from_aw(A0w)                         # centred time grid
Wc = np.fft.fftshift(g.W)                      # centred detuning
np.savetxt(os.path.join(D, "omega.txt"), Wc)
np.savetxt(os.path.join(D, "beta.txt"), fib.beta(wg + Wc))
np.savetxt(os.path.join(D, "At.txt"), np.c_[At_c.real, At_c.imag])
with open(os.path.join(D, "params.txt"), "w") as f:
    for k, v in dict(nt=g.nt, dt=g.dt, omega0=wg, L=1.0, dz=2.5e-4, n2=fib.n2, S=1 / (aeff0 * 1e-12),
                     fR=0.18, tau1=0.0122, tau2=0.032, nsave=20).items():
        f.write(f"{k} {v!r}\n")
env = dict(os.environ, JULIA_NUM_THREADS="2")
t0 = time.time()
r = subprocess.run(["julia", "--project=" + os.path.join(REPO, "solver"), os.path.join(COMMON, "jl_forward.jl"), D],
                   capture_output=True, text=True, env=env)
print(r.stdout[-2000:], r.stderr[-3000:])
B = np.loadtxt(os.path.join(D, "jl_out_Aw_photon.txt")); B = B[:, 0] + 1j * B[:, 1]
NJ = np.loadtxt(os.path.join(D, "jl_out_N.txt"))
nJ = np.abs(B) ** 2                              # photons per bin, centred order
wabs_c = wg + Wc
# numpy reference (saved by h1_numpy.py)
ref = np.load(os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN}/const_dz0.25mm.npz"))
sim = GNLSE(g, fib.beta, fib.n2, lambda w: np.full_like(np.asarray(w, float), aeff0), aeff0,
            raman=OscillatorRaman(0.18, 0.0122, 0.032), w_ref=wg)
n_np = np.fft.fftshift(np.abs(ref["Aw"]) ** 2 * sim.pw)
N0 = sim.photons(A0w)
out = {"julia_wall_s_incl_compile": time.time() - t0,
       "julia_rel_photon_drift": float((NJ[-1, 1] - NJ[0, 1]) / NJ[0, 1]),
       "julia_N0_over_numpy_N0": float(NJ[0, 1] / N0)}
for lc in [1.65, 1.75, 1.85]:
    m = wabs_c < wl_to_w(lc)
    out[f"eta_julia_{lc}"] = float(nJ[m].sum() / NJ[0, 1])
    out[f"eta_numpy_{lc}"] = float(n_np[m].sum() / N0)
out["spectrum_rel_L1_diff"] = float(np.abs(nJ / nJ.sum() - n_np / n_np.sum()).sum())
out["mean_w_julia"] = float((nJ * wabs_c).sum() / nJ.sum())
out["mean_w_numpy"] = float((n_np * wabs_c).sum() / n_np.sum())
json.dump(out, open(os.path.join(HERE, "summary_julia_crosscheck.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
