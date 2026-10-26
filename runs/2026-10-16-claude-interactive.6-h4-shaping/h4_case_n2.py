"""H4 extension to N = 2: TL sech N = 2, T0 = 56.7 fs (1.89 nJ) in S28, L = 1 m, lossless.
Writes the Julia case directory and prints the TL photon fractions beyond several cutoffs (numpy, dz = 0.25 mm)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *

D = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-16-claude-interactive.6-h4-shaping/case_N2")
os.makedirs(D, exist_ok=True)
fib = StepIndexFiber("SiO2", 4.1, 0.14, n=600, n2=2.6e-20)
wp = wl_to_w(1.55); wg = wl_to_w(1.75)
g = Grid(2 ** 13, 0.003, wg)
aeff0 = float(fib.aeff_um2(np.array([wp]))[0])
b2 = abs(fib.beta2(np.array([wp]))[0]); gam = fib.n2 * wp / C_M_PS / (aeff0 * 1e-12)
P0 = 4 * b2 / (gam * 0.0567 ** 2)
Q = sech_pulse(g, P0, 0.0567, W_off=wp - wg)
At_c = at_from_aw(Q); Wc = np.fft.fftshift(g.W)
np.savetxt(os.path.join(D, "omega.txt"), Wc)
np.savetxt(os.path.join(D, "beta.txt"), fib.beta(wg + Wc))
np.savetxt(os.path.join(D, "At.txt"), np.c_[At_c.real, At_c.imag])
with open(os.path.join(D, "params.txt"), "w") as f:
    for k, v in dict(nt=g.nt, dt=g.dt, omega0=wg, L=1.0, dz=2.5e-4, n2=fib.n2, S=1 / (aeff0 * 1e-12),
                     fR=0.18, tau1=0.0122, tau2=0.032, nsave=20).items():
        f.write(f"{k} {v!r}\n")
sim = GNLSE(g, fib.beta, fib.n2, lambda w: np.full_like(np.asarray(w, float), aeff0), aeff0,
            raman=OscillatorRaman(0.18, 0.0122, 0.032), w_ref=wg)
Nl = sim.photons(Q)
out = sim.run(Q, 1.0, 2.5e-4)
res = {"E_pJ": 2 * P0 * 0.0567, "eta_TL": {}}
for lc in [1.6, 1.62, 1.64, 1.66, 1.68, 1.7, 1.72, 1.75]:
    res["eta_TL"][str(lc)] = float(sim.photons(out["Aw"], g.w < wl_to_w(lc)) / Nl)
json.dump(res, open(os.path.join(HERE, "summary_case_n2_pilot.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
