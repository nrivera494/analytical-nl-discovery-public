"""Independent re-evaluation (numpy RK4IP, dz = 0.25 mm) of masks found by h4_opt.jl (Julia adjoint, dz = 0.5 mm).
Usage: python h4_eval_numpy.py <opt_out_dir> <lambda_c_um> [dz_mm]"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

d = sys.argv[1]; lamc = float(sys.argv[2]); dz = float(sys.argv[3]) * 1e-3 if len(sys.argv) > 3 else 2.5e-4
Nsol = int(sys.argv[4]) if len(sys.argv) > 4 else 3
fib = StepIndexFiber("SiO2", 4.1, 0.14, n=600, n2=2.6e-20)
wp = wl_to_w(1.55); wg = wl_to_w(1.75)
g = Grid(2 ** 13, 0.003, wg)
aeff0 = float(fib.aeff_um2(np.array([wp]))[0])
b2 = abs(fib.beta2(np.array([wp]))[0]); gam = fib.n2 * wp / C_M_PS / (aeff0 * 1e-12)
P0 = Nsol ** 2 * b2 / (gam * 0.0567 ** 2)
Q = sech_pulse(g, P0, 0.0567, W_off=wp - wg)            # TL laser, fft-order spectrum
sim = GNLSE(g, fib.beta, fib.n2, lambda w: np.full_like(np.asarray(w, float), aeff0), aeff0,
            raman=OscillatorRaman(0.18, 0.0122, 0.032), w_ref=wg)
Nl = sim.photons(Q)
M = np.loadtxt(os.path.join(d, "best_phase.txt"))       # columns: detuning W (rad/ps, Julia centred grid), phi, m
phi = np.zeros(g.nt); amp = np.ones(g.nt)
for Wk, ph, mk in M:
    k = int(np.argmin(np.abs(g.W - Wk)))
    phi[k] = ph; amp[k] = mk
res = {}
for name, A0 in [("TL", Q), ("mask", Q * amp * np.exp(1j * phi))]:
    out = sim.run(A0, 1.0, dz)
    res[name] = float(sim.photons(out["Aw"], g.w < wl_to_w(lamc)) / Nl)
res["H"] = res["mask"] / res["TL"]
res["dz_mm"] = dz * 1e3
res["N"] = Nsol
res["launched_photon_fraction"] = float(sim.photons(Q * amp) / Nl)
json.dump(res, open(os.path.join(d, "numpy_eval.json"), "w"), indent=1)
print(json.dumps(res))
